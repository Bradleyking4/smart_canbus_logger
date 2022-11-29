import wx
import serial_interface
import wxFormBuilder

import process
import multiprocessing
import queue
import datetime
import time


from ObjectListView import GroupListView, ObjectListView, ColumnDefn, BatchedUpdate

class CANMessage(object):

	def __init__(self,id, data, timestamp=None):
		self.id = id
		self.data = data
		self.timestamp = timestamp or datetime.datetime.now()


def dataFormatter(line):
    data = ''
    for i in range(0,8):
        data += " " + hex(line[i])[2:]
    return data

class Main(wxFormBuilder.MainWindow):
    _process = None
    _paused = False
    _paused_batch = []
    _ignore = False
    _ignored_messages = []
    _message_occurences = {}

    def __init__(self, parent):
        wxFormBuilder.MainWindow.__init__(self,parent)

        self.serial_interface = serial_interface.SerialInterface()

        self.CreateStatusBar() # A Statusbar in the bottom of the window
        
        self.create_tools()

        sizer = self.ObjectListViewPlaceHolder.GetContainingSizer()
        self.ObjectListViewPlaceHolder.Destroy()
        self.message_list = ObjectListView(self.m_panelLogger, style=wx.LC_REPORT|wx.SUNKEN_BORDER,)
        self.message_list.SetSize(680,450) #hack to make it "Fullscreen"
        self.batched_message_list = BatchedUpdate(self.message_list, 1)
        self.message_list.SetFilter(self.filter)
        sizer.Add(self.message_list, 1, flag=wx.EXPAND|wx.ALL, border=5)
       
        
        self.init_message_list()
        self.Bind (wx.EVT_IDLE, self.on_idle)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.Show()

    def create_tools(self):
        self.bitrate_combobox.AppendItems([str(i) for i in self.serial_interface.supported_can_bitrates])
        self.bitrate_combobox.SetSelection(6)

       
        self.update_port_selection()




    # def create_filters(self):
    #     b = 5
    #     self.filter_sizer = wx.BoxSizer(wx.HORIZONTAL)
    #     self.filter_sizer.Add(wx.StaticText(self, label="Filter (ID or data):", pos=(10, 5)), flag=wx.EXPAND|wx.ALL, border=b)
    #     self.filter_textbox = wx.TextCtrl(self)
    #     self.filter_sizer.Add(self.filter_textbox, flag=wx.EXPAND)
    #     self.main_sizer.Add(self.filter_sizer)

    #     self.ignore_button = wx.Button(self, label="Start ignore")
    #     self.filter_sizer.Add(self.ignore_button, flag=wx.EXPAND)
    #     self.Bind(wx.EVT_BUTTON, self.on_ignore, self.ignore_button)

    #     self.clear_ignore_button = wx.Button(self, label="Clear ignore list")
    #     self.filter_sizer.Add(self.clear_ignore_button, flag=wx.EXPAND)
    #     self.Bind(wx.EVT_BUTTON, self.on_clear_ignore, self.clear_ignore_button)

    #     self.Bind(wx.EVT_TEXT, self.on_filter_update, self.filter_textbox)

    #     self.filter_sizer.Add(wx.StaticText(self, label="Number of occurences:", pos=(10, 5)), flag=wx.EXPAND|wx.ALL, border=b)
    #     self.filter_sizer.Add(wx.StaticText(self, label=">=", pos=(10, 5)), flag=wx.EXPAND|wx.ALL, border=b)
    #     self.gte_occurences_text = wx.TextCtrl(self)
    #     self.filter_sizer.Add(self.gte_occurences_text, flag=wx.EXPAND)
    #     self.Bind(wx.EVT_TEXT, self.on_filter_update, self.gte_occurences_text)

    #     self.filter_sizer.Add(wx.StaticText(self, label="<=", pos=(10, 5)), flag=wx.EXPAND|wx.ALL, border=b)
        
    #     self.lte_occurences_text = wx.TextCtrl(self)
    #     self.filter_sizer.Add(self.lte_occurences_text, flag=wx.EXPAND)
    #     self.Bind(wx.EVT_TEXT, self.on_filter_update, self.lte_occurences_text)





    def init_message_list(self):
        self.message_list.SetColumns([
            # ColumnDefn("ID", "left", 200, "id",groupKeyGetter = "id"),
            ColumnDefn("Timestamp", "left", 300, "timestamp"),
            ColumnDefn("ID", "left", 100, "id",groupKeyGetter = "id",stringConverter="%#X"),
            ColumnDefn("Data", "left", 250, "data", minimumWidth=250, stringConverter=dataFormatter),
            ]

            )

    def update_port_selection(self):
        """
        Updates serial port selection with available serial ports
        """
        self.serial_combobox.Clear()
        self.serial_combobox.AppendItems(self.serial_interface.scan())
        self.serial_combobox.SetSelection(0)


    def on_ignore(self, event):
        if self._ignore:
            self._ignore = False
            self.ignore_button.SetLabel("Start ignore")
        else:
            self._ignore = True
            self.ignore_button.SetLabel("Stop ignore")

    def on_clear_ignore(self, event):
        self._ignored_messages = []


    def on_filter_update(self, event):
        self.batched_message_list.RepopulateList()

    def filter(self, object_list):
        val = self.filter_textbox.GetValue()
        try:
            gte = int(self.gte_occurences_text.GetValue())
        except ValueError:
            gte = -1
        try:
            lte = int(self.lte_occurences_text.GetValue())
        except ValueError:
            lte = -1

        res = []
        for m in object_list:
            mv = m.id
            if mv in self._ignored_messages:
                continue

            if len(val)==0:
                matches_filter = True
            else:
                matches_filter = (m.id.startswith(val) or m.data.startswith(val))
            if mv not in self._message_occurences:
                matches_occurences = True
            else:
                matches_gte = gte==-1 or self._message_occurences[mv]>=gte
                matches_lte = lte==-1 or self._message_occurences[mv]<=lte
                matches_occurences = matches_gte and matches_lte
            if matches_filter and matches_occurences:
                res.append(m)

        return res

    def on_connect(self, event):
        """Executed on click of Connect button. 
        Spawns a new thread which listens for messages on serial port, if no connection is present.
        If already connected, stops existing thread (disconnects).
        """
        if not self._process:
            serial_port = self.serial_combobox.GetStringSelection()
            bitrate = self.bitrate_combobox.GetStringSelection()

            if serial_port and bitrate:
                try:
                    self._TxQueue = multiprocessing.Queue(10)
                    self._RxQueue = multiprocessing.Queue(10)
                    self._process = process.SerialProcess(serial_port, bitrate, self._TxQueue,self._RxQueue)
                    self.connect_button.SetLabel("Disconnect")
                except (serial_interface.SerialException, e):
                    wx.MessageBox("Cannot open serial port! "+e.message, "Error", wx.OK | wx.ICON_ERROR)
            else:
                wx.MessageBox("Please select serial port and bitrate.", "Error", wx.OK | wx.ICON_ERROR)
        else:
            self._RxQueue.put("stop")
            self.connect_button.SetLabel("Connect")
            self._process = None

    def on_pause(self, event):
        if self._paused:
            self._paused = False
            self.batched_message_list.AddObjects(self._paused_batch)
            self._paused_batch = []
            self.pause_button.SetLabel("Pause")
        else:
            self.pause_button.SetLabel("Play")
            self._paused = True

    def on_idle(self, event):
        if hasattr(self, '_RxQueue'):
            try:
                message = self._RxQueue.get_nowait()
                print("removed from queue " + str(message.id))

                if hasattr(message, 'timestamp'):
                    message_val = message.id

                    self.process_message(message)

                    if self._ignore:
                        self._ignored_messages.append(message_val)

                    if message_val in self._message_occurences:
                        self._message_occurences[message_val]+=1
                    else:
                        self._message_occurences[message_val]=1


                    if self._paused:
                        self._paused_batch.append(message)
                    else:
                        self.batched_message_list.AddObject(message)

                elif message=="stop":
                    self._RxQueue.put("stop")
            except queue.Empty:
                pass
            event.RequestMore()

    def process_message(self,message):
        if message.id == 0x420:
            self.SMU_STATE.SetSelection(int(message.data[0]))
            self.estopPressed.SetValue(int(message.data[1]))
            self.SMU_PackVoltage.SetValue(int(message.data[2]))

            self.tbxPackVoltage.SetLabel("Pack Voltage: "+ str(message.data[2]))
            self.tbxPreChargeVoltage.SetLabel("PreCharge Voltage: "+ str(message.data[3]))
            self.MainContactor.SetValue(int(message.data[4]&1))
            self.MainContactor.SetValue(int(message.data[4]&2))
            if self.packetSent > 0:
                self.send_next_packet()

        elif message.id == 0x421:
            self.send_next_packet()

        elif message.id == 0x423:    
            self.tbxAcVoltage.SetLabel()
            self.tbxACcurrent.SetLabel()
        elif message.id == 0x440:
            print(" ")
            
        elif message.id == 0x441:
            print(" ")

    def send_next_packet(self):
        print("send packet:" + str(self.packetSent) )
        if self.packetSent < len(self.data)/8:
            self._TxQueue.put(CANMessage(self.canAddress+2,self.data[self.packetSent*8:self.packetSent*8+8]))
            # self._RxQueue.put(CANMessage(self.canAddress+2,self.data[self.packetSent*8:self.packetSent*8+8]))
            self.packetSent = self.packetSent + 1
        elif(self.packetSent*8 < len(self.data)):
             self._TxQueue.put(CANMessage(self.canAddress+2,self.data[self.packetSent*8:len(self.data)]))
             self.packetSent = self.packetSent + 1
        else:
            canData = bytearray(8)
            canData[5] =1      
            self._TxQueue.put(CANMessage(self.canAddress+1,canData))
            self._RxQueue.put (CANMessage(self.canAddress+1,canData))
        self.OTA_progress.Value = self.packetSent  
        self.OTA_progress.ToolTip =         str(self.packetSent) + " of " + str(len(self.data)/8)


           
    def load_image_file_STR(self,path):
        #= sizeof(esp_image_header_t) + sizeof(esp_image_segment_header_t)
        #0xABCD5432   binaryHeader size 24 bytes  esp_image_segment_header_t size = 8bytes
        magicString = bytearray.fromhex('ABCD5432')
        canAddress = 0
        deviceName = ""
        file = open(path,"rb")
        self.data = file.read()
        print(len(self.data))
        # for i in range(len(data)):
        if(self.data[0] != 0xE9 ):
            print("Not an ESP32 image")
        for i in range(24+8+32):
            if (self.data[i] == magicString[3]):
                if (self.data[i+1] == magicString[2]):
                    if (self.data[i+2] == magicString[1]):
                        if (self.data[i+3] == magicString[0]):
                            print(i)
                            structPos = i
                            secure_version = structPos +4
                            reserv1 = secure_version + 4
                            versionPos = reserv1 + 8
                            project_namePos = versionPos + 32
                            buildTime = project_namePos + 32
                            date = buildTime + 16
                            idf_ver = date + 16
                            app_elf_sha256 = idf_ver +32
                            
                            deviceName = self.data[project_namePos:buildTime].decode()

                            print(deviceName )
                            print(self.data[versionPos:project_namePos].decode() )
                            print(self.data[buildTime:date].decode() )
                            print(self.data[date:idf_ver].decode() )
                            print(self.data[idf_ver:app_elf_sha256].decode() )

                            customImage = i + 256
                            baseCanAddress = customImage + 20
                            release = baseCanAddress + 4

                            self.canAddress = int.from_bytes(self.data[baseCanAddress : release ], "little")
                            print(self.data[customImage : baseCanAddress].decode() )
                            print(hex(canAddress))
                            print(self.data[release : release +4] )
        self.imageInfo.Label = deviceName + " Can:" + hex(canAddress)
        canData = bytearray(8)
        canData[4] =1 
        self._TxQueue.put(CANMessage(self.canAddress+1,canData))
        self._RxQueue.put (CANMessage(self.canAddress+1,canData))
        self.packetSent = 0
        self.OTA_progress.SetRange(len(self.data))

        

        

    def load_image_file(self,event):
        print(event.GetPath())
        self.load_image_file_STR(event.GetPath())
        

        # with open(event.GetPath(), mode='rb') as file: # b is important -> binary
        #     fileContent = file.read()
       

    def upload_image(self,event):
        self.load_image_file_STR(self.ota_FilePicker.Path)



    def on_close(self, event):
        if self._process:
            self._RxQueue.put("stop")
            self._process.join()
        self.Destroy()


    def on_save(self, event):
        dlg = wx.FileDialog(
            self, message="Save file as ...",
            defaultFile="", style=wx.SAVE, wildcard="All files (*.*)|*.*"
            )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            try:
                f = open(path,'w')
                f.write("#Timestamp, #ID, #Data\n")
                for o in self.message_list.GetObjects():
                    f.write("%s, %s, %s\n" % (o.timestamp, o.id, o.data))
                f.close()
            except IOError:
                wx.MessageBox("Cannot save file! \n"+e.message, "Error", wx.OK | wx.ICON_ERROR)
        dlg.Destroy()

    def on_clear(self, event):
        self.message_list.DeleteAllItems()

class MyApp(wx.App):
    def OnInit(self):
        frame = Main(None)
        frame.Show(True)
        self.SetTopWindow(frame)
        return True



if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()