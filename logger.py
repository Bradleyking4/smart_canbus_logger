import wx
import serial_interface
import wxFormBuilder

import process
import multiprocessing
import queue
import datetime
import time

import can

bustype = 'socketcan'
channel = 'can0'
motorCurrent = 0

from ObjectListView import GroupListView, ObjectListView, ColumnDefn, BatchedUpdate

class CANMessage(object):

	def __init__(self,arbitration_id, data, timestamp=None):
		self.arbitration_id = arbitration_id
		self.data = data
		self.timestamp = timestamp or datetime.datetime.now()


def dataFormatter(line):
    
    data = ''
    for i in range(0,len(line)):
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
            # ColumnDefn("ID", "left", 200, "arbitration_id",groupKeyGetter = "arbitration_id"),
            ColumnDefn("Timestamp", "left", 300, "timestamp"),
            ColumnDefn("ID", "left", 100, "arbitration_id",groupKeyGetter = "arbitration_id",stringConverter="%#X"),
            ColumnDefn("Data", "left", 250, "data", minimumWidth=250, stringConverter=dataFormatter),
            ]

            )

    def update_port_selection(self):
        """
        Updates serial port selection with available serial ports
        """
        self.serial_combobox.Clear()

        self.serial_combobox.AppendItems(self.serial_interface.scan())
        
        
        try:
            bus = can.interface.Bus(channel=channel, bustype=bustype,bitrate=250000)
            self.serial_combobox.AppendItems(channel)
            _hardware_can = True
            print("HW can Found")

        except:
            _hardware_can = False
            print("HW can not Found")



# msg = can.Message(arbitration_id=0xc0ffee, data=[0, 1, 3, 1, 4, 1], is_extended_id=False)
# while True:
# 	bus.send(msg)
# 	time.sleep(1)

        self.serial_combobox.SetSelection(0)
        if _hardware_can == True:
            self.on_connect( 0)
            self.Maximize(True)



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
            mv = m.arbitration_id
            if mv in self._ignored_messages:
                continue

            if len(val)==0:
                matches_filter = True
            else:
                matches_filter = (m.arbitration_id.startswith(val) or m.data.startswith(val))
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
                    
                    if serial_port == channel:
                        self._process = process.CanProcess(serial_port, bitrate, self._TxQueue,self._RxQueue)
                    else:
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
                print("removed from queue " + str(message.arbitration_id))

                if hasattr(message, 'timestamp'):
                    message_val = message.arbitration_id

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

    def process_message(self, message):
        global motorCurrent
        if message.arbitration_id == 0x420:
            self.SMU_STATE.SetSelection(int(message.data[0]))
            self.estopPressed.SetValue(int(message.data[1]))
            try:
                self.SMU_PackVoltage.SetValue(int(message.data[2]))
            except:
                pass
            self.tbxPackVoltage.SetLabel(
                "Pack Voltage: " + str(message.data[2]))
            self.tbxPreChargeVoltage.SetLabel(
                "PreCharge Voltage: " + str(message.data[3]))
            self.MainContactor.SetValue(int(message.data[4] & 1))
            self.ChargeContractor.SetValue(int((message.data[4] & 2)/2))
            # if self.packetSent > 0:
            #     self.send_next_packet()

        elif message.arbitration_id == 0x421:
            self.send_next_packet()

        elif message.arbitration_id == 0x423:
            self.AC1present.SetValue(int(message.data[0] & 1))
            self.AC2present.SetValue(int((message.data[0] & 2)/2))
            self.tbxAcVoltage.SetLabel(
                "AC Voltage:" + str(int(message.data[1])*256+int(message.data[2])))
            self.tbxACcurrent.SetLabel(
                "AC Current:" + str(int(message.data[3])*256+int(message.data[4])))
        elif message.arbitration_id == 0x440:
            if len(message.data) < 8:
                return
            self.ECU_PowerState.SetSelection(int(message.data[0]))
            self.ECU_SpeedState.SetSelection(int(message.data[1]))

            print(int(message.data[2]))

            self.MainContactor1.SetValue((int(message.data[2]) & 1))
            self.KellyPowered.SetValue(int((message.data[2] & 2)/2))
            self.ChargeContractor1.SetValue(int((message.data[2] & 4)/4))
            self.prechargeComplete1.SetValue(int((message.data[2] & 8)/8))
            self.DCDCContactor.SetValue(int((message.data[2] & 16)/16))
            self.StopPedal.SetValue(int((message.data[2] & 32)/32))

            self.tbxGear.SetLabel("Gearbox Pos: " + str(message.data[3]))
            self.tbxGearStickPos.SetLabel(
                "Gear Stick Pos: " + str(message.data[4]))

            if int(message.data[5]) <= 100:
                self.ECU_ThrottlePos.SetValue(int(message.data[5]))
            else:
                print(" 5 ")
                print(int(message.data[5]))
                print(" ")
            
            if (int(message.data[6])*256+int(message.data[7]))/100 <= 100:
                 self.ECU_KellyAccel.SetValue(
                (int(message.data[6])*256+int(message.data[7]))/100)
            else:
                print(" ")

        elif message.arbitration_id == 0x441:
            print(" ")

        elif message.arbitration_id == 0x0CF11E05:
            # global motorCurrent
            speed = message.data[1] * 256 + message.data[0]
            motorCurrent = motorCurrent * 0.8 + 0.2 *(message.data[3] * 256 + message.data[2]) / 10
            voltage = (message.data[5] * 256 + message.data[4]) / 10
            power = motorCurrent * voltage
            self.tbxKellyVoltage.SetLabel("Pack Voltage:" + str(voltage))
            self.tbxKellyCurrent.SetLabel("Pack Current:" + str(motorCurrent))
            self.tbxKellyPower.SetLabel("Pack Power:" + str(power))

            
            print(voltage)

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