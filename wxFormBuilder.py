# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.aui
import wx.richtext

###########################################################################
## Class MainWindow
###########################################################################

class MainWindow ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"CANBus logger", pos = wx.DefaultPosition, size = wx.Size( 735,418 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 735,418 ), wx.DefaultSize )

		bSizer26 = wx.BoxSizer( wx.VERTICAL )

		self.m_auinotebook4 = wx.aui.AuiNotebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.aui.AUI_NB_DEFAULT_STYLE )
		self.wxpanel23 = wx.Panel( self.m_auinotebook4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer5 = wx.GridSizer( 0, 2, 0, 0 )

		bSizer29 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText6 = wx.StaticText( self.wxpanel23, wx.ID_ANY, u"Serial Port:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		bSizer29.Add( self.m_staticText6, 0, wx.ALL, 5 )

		serial_comboboxChoices = []
		self.serial_combobox = wx.ComboBox( self.wxpanel23, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, serial_comboboxChoices, 0 )
		self.serial_combobox.SetMinSize( wx.Size( 120,-1 ) )

		bSizer29.Add( self.serial_combobox, 0, wx.ALL, 5 )

		self.m_staticText7 = wx.StaticText( self.wxpanel23, wx.ID_ANY, u"CAN baud rate (kbps):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		bSizer29.Add( self.m_staticText7, 0, wx.ALL, 5 )

		bitrate_comboboxChoices = []
		self.bitrate_combobox = wx.ComboBox( self.wxpanel23, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, bitrate_comboboxChoices, 0 )
		self.bitrate_combobox.SetMinSize( wx.Size( 120,-1 ) )

		bSizer29.Add( self.bitrate_combobox, 0, wx.ALL, 5 )


		gSizer5.Add( bSizer29, 1, wx.EXPAND, 5 )

		bSizer30 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText8 = wx.StaticText( self.wxpanel23, wx.ID_ANY, u"Filter (ID or data):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		bSizer30.Add( self.m_staticText8, 0, wx.ALL, 5 )

		self.filter_textbox = wx.TextCtrl( self.wxpanel23, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer30.Add( self.filter_textbox, 0, wx.ALL, 5 )

		self.ignore_button = wx.Button( self.wxpanel23, wx.ID_ANY, u"Start ignore", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer30.Add( self.ignore_button, 0, wx.ALL, 5 )

		self.clear_ignore_button = wx.Button( self.wxpanel23, wx.ID_ANY, u"Clear ignore list", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer30.Add( self.clear_ignore_button, 0, wx.ALL, 5 )


		gSizer5.Add( bSizer30, 1, wx.EXPAND, 5 )

		bSizer31 = wx.BoxSizer( wx.VERTICAL )

		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )

		self.connect_button = wx.Button( self.wxpanel23, wx.ID_ANY, u"Connect", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.connect_button, 0, wx.ALL, 5 )

		self.pause_button = wx.Button( self.wxpanel23, wx.ID_ANY, u"Pause", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.pause_button, 0, wx.ALL, 5 )

		self.save_button = wx.Button( self.wxpanel23, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.save_button, 0, wx.ALL, 5 )

		self.clear_button = wx.Button( self.wxpanel23, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.clear_button, 0, wx.ALL, 5 )


		bSizer31.Add( bSizer17, 1, wx.EXPAND, 5 )

		bSizer161 = wx.BoxSizer( wx.VERTICAL )

		self.ota_FilePicker = wx.FilePickerCtrl( self.wxpanel23, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		bSizer161.Add( self.ota_FilePicker, 0, wx.ALL, 5 )

		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )

		self.loadImage = wx.Button( self.wxpanel23, wx.ID_ANY, u"Upload", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.loadImage, 0, wx.ALL, 5 )

		self.cancelOTA = wx.Button( self.wxpanel23, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.cancelOTA, 0, wx.ALL, 5 )


		bSizer161.Add( bSizer18, 1, wx.EXPAND, 5 )

		self.imageInfo = wx.StaticText( self.wxpanel23, wx.ID_ANY, u"Can:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.imageInfo.Wrap( -1 )

		bSizer161.Add( self.imageInfo, 0, wx.ALL, 5 )

		self.OTA_progress = wx.Gauge( self.wxpanel23, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.OTA_progress.SetValue( 0 )
		bSizer161.Add( self.OTA_progress, 0, wx.ALL, 5 )


		bSizer31.Add( bSizer161, 1, wx.EXPAND, 5 )


		gSizer5.Add( bSizer31, 1, wx.EXPAND, 5 )

		bSizer32 = wx.BoxSizer( wx.VERTICAL )

		fgSizer3 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		bSizer38 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText9 = wx.StaticText( self.wxpanel23, wx.ID_ANY, u"Number of occurences:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		bSizer38.Add( self.m_staticText9, 0, wx.ALL, 5 )


		fgSizer3.Add( bSizer38, 1, wx.EXPAND, 5 )

		bSizer39 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText11 = wx.StaticText( self.wxpanel23, wx.ID_ANY, u">=", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		bSizer39.Add( self.m_staticText11, 0, wx.ALL, 5 )

		self.gte_occurences_text = wx.TextCtrl( self.wxpanel23, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer39.Add( self.gte_occurences_text, 0, wx.ALL, 5 )

		self.m_staticText10 = wx.StaticText( self.wxpanel23, wx.ID_ANY, u"<=", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		bSizer39.Add( self.m_staticText10, 0, wx.ALL, 5 )

		self.lte_occurences_text = wx.TextCtrl( self.wxpanel23, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer39.Add( self.lte_occurences_text, 0, wx.ALL, 5 )


		fgSizer3.Add( bSizer39, 1, wx.EXPAND, 5 )


		bSizer32.Add( fgSizer3, 1, wx.EXPAND, 5 )


		gSizer5.Add( bSizer32, 1, wx.EXPAND, 5 )


		self.wxpanel23.SetSizer( gSizer5 )
		self.wxpanel23.Layout()
		gSizer5.Fit( self.wxpanel23 )
		self.m_auinotebook4.AddPage( self.wxpanel23, u"Connection", True, wx.NullBitmap )
		self.m_panelLogger = wx.Panel( self.m_auinotebook4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizerLogger = wx.BoxSizer( wx.VERTICAL )

		self.ObjectListViewPlaceHolder = wx.richtext.RichTextCtrl( self.m_panelLogger, wx.ID_ANY, u"fdgdsfg", wx.DefaultPosition, wx.Size( 1,1 ), 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		self.ObjectListViewPlaceHolder.SetMinSize( wx.Size( 1,1 ) )
		self.ObjectListViewPlaceHolder.SetMaxSize( wx.Size( 700,500 ) )

		bSizerLogger.Add( self.ObjectListViewPlaceHolder, 1, wx.EXPAND |wx.ALL, 5 )


		self.m_panelLogger.SetSizer( bSizerLogger )
		self.m_panelLogger.Layout()
		bSizerLogger.Fit( self.m_panelLogger )
		self.m_auinotebook4.AddPage( self.m_panelLogger, u"Logger", False, wx.NullBitmap )
		self.SMU_PANEL = wx.Panel( self.m_auinotebook4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer2 = wx.GridSizer( 0, 2, 0, 0 )

		bSizer33 = wx.BoxSizer( wx.VERTICAL )

		self.SMU_PackVoltage = wx.Gauge( self.SMU_PANEL, wx.ID_ANY, 132, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.SMU_PackVoltage.SetValue( 25 )
		bSizer33.Add( self.SMU_PackVoltage, 0, wx.ALL, 5 )

		SMU_STATEChoices = [ u"CHARGE_IDLE", u"CHARGE_J17772", u"CHARGE_AC", u"CHARGE_PRE", u"CHARGE_RUN", u"CHARGE_ERROR", wx.EmptyString, wx.EmptyString ]
		self.SMU_STATE = wx.ComboBox( self.SMU_PANEL, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, SMU_STATEChoices, 0 )
		bSizer33.Add( self.SMU_STATE, 0, wx.ALL, 5 )

		self.estopPressed = wx.CheckBox( self.SMU_PANEL, wx.ID_ANY, u"E-stop Pressed", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer33.Add( self.estopPressed, 0, wx.ALL, 5 )

		self.MainContactor = wx.CheckBox( self.SMU_PANEL, wx.ID_ANY, u"Main Contactor", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer33.Add( self.MainContactor, 0, wx.ALL, 5 )

		self.ChargeContractor = wx.CheckBox( self.SMU_PANEL, wx.ID_ANY, u"Charge Contactor", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer33.Add( self.ChargeContractor, 0, wx.ALL, 5 )

		self.prechargeComplete = wx.CheckBox( self.SMU_PANEL, wx.ID_ANY, u"Precharge Complete", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer33.Add( self.prechargeComplete, 0, wx.ALL, 5 )

		self.AC1present = wx.CheckBox( self.SMU_PANEL, wx.ID_ANY, u"AC 1 Present", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer33.Add( self.AC1present, 0, wx.ALL, 5 )

		self.AC2present = wx.CheckBox( self.SMU_PANEL, wx.ID_ANY, u"AC 2 Present", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer33.Add( self.AC2present, 0, wx.ALL, 5 )


		gSizer2.Add( bSizer33, 1, wx.EXPAND, 5 )

		bSizer16 = wx.BoxSizer( wx.VERTICAL )

		self.tbxPackVoltage = wx.StaticText( self.SMU_PANEL, wx.ID_ANY, u"Pack Voltage:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.tbxPackVoltage.Wrap( -1 )

		bSizer16.Add( self.tbxPackVoltage, 0, wx.ALL, 5 )

		self.tbxPreChargeVoltage = wx.StaticText( self.SMU_PANEL, wx.ID_ANY, u"PreCharge Voltage:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.tbxPreChargeVoltage.Wrap( -1 )

		bSizer16.Add( self.tbxPreChargeVoltage, 0, wx.ALL, 5 )

		self.tbxAcVoltage = wx.StaticText( self.SMU_PANEL, wx.ID_ANY, u"AC Voltage:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.tbxAcVoltage.Wrap( -1 )

		bSizer16.Add( self.tbxAcVoltage, 0, wx.ALL, 5 )

		self.tbxACcurrent = wx.StaticText( self.SMU_PANEL, wx.ID_ANY, u"AC Current:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.tbxACcurrent.Wrap( -1 )

		bSizer16.Add( self.tbxACcurrent, 0, wx.ALL, 5 )


		gSizer2.Add( bSizer16, 1, wx.EXPAND, 5 )


		self.SMU_PANEL.SetSizer( gSizer2 )
		self.SMU_PANEL.Layout()
		gSizer2.Fit( self.SMU_PANEL )
		self.m_auinotebook4.AddPage( self.SMU_PANEL, u"SMU", False, wx.NullBitmap )
		self.ECU_PANEL = wx.Panel( self.m_auinotebook4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_auinotebook4.AddPage( self.ECU_PANEL, u"ECU", False, wx.NullBitmap )
		self.m_panel13 = wx.Panel( self.m_auinotebook4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer34 = wx.BoxSizer( wx.VERTICAL )

		self.m_auinotebook5 = wx.aui.AuiNotebook( self.m_panel13, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.aui.AUI_NB_DEFAULT_STYLE )
		self.Overview = wx.Panel( self.m_auinotebook5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer51 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer51.SetFlexibleDirection( wx.BOTH )
		fgSizer51.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		bSizer361 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText53 = wx.StaticText( self.Overview, wx.ID_ANY, u"State", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText53.Wrap( -1 )

		bSizer361.Add( self.m_staticText53, 0, wx.ALL, 5 )

		self.m_staticText121 = wx.StaticText( self.Overview, wx.ID_ANY, u"Number of cells", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText121.Wrap( -1 )

		bSizer361.Add( self.m_staticText121, 0, wx.ALL, 5 )

		self.m_staticText131 = wx.StaticText( self.Overview, wx.ID_ANY, u"Max Voltage", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText131.Wrap( -1 )

		bSizer361.Add( self.m_staticText131, 0, wx.ALL, 5 )

		self.m_staticText141 = wx.StaticText( self.Overview, wx.ID_ANY, u"Avg Voltage", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText141.Wrap( -1 )

		bSizer361.Add( self.m_staticText141, 0, wx.ALL, 5 )

		self.m_staticText151 = wx.StaticText( self.Overview, wx.ID_ANY, u"Min Voltage", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText151.Wrap( -1 )

		bSizer361.Add( self.m_staticText151, 0, wx.ALL, 5 )

		self.m_staticText161 = wx.StaticText( self.Overview, wx.ID_ANY, u"Max Temp", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText161.Wrap( -1 )

		bSizer361.Add( self.m_staticText161, 0, wx.ALL, 5 )

		self.m_staticText171 = wx.StaticText( self.Overview, wx.ID_ANY, u"Average Temp", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText171.Wrap( -1 )

		bSizer361.Add( self.m_staticText171, 0, wx.ALL, 5 )

		self.m_staticText181 = wx.StaticText( self.Overview, wx.ID_ANY, u"Min Temp", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText181.Wrap( -1 )

		bSizer361.Add( self.m_staticText181, 0, wx.ALL, 5 )

		self.m_staticText191 = wx.StaticText( self.Overview, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText191.Wrap( -1 )

		bSizer361.Add( self.m_staticText191, 0, wx.ALL, 5 )


		fgSizer51.Add( bSizer361, 1, wx.EXPAND, 5 )

		bSizer351 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText54 = wx.StaticText( self.Overview, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText54.Wrap( -1 )

		bSizer351.Add( self.m_staticText54, 0, wx.ALL, 5 )

		self.m_staticText52 = wx.StaticText( self.Overview, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText52.Wrap( -1 )

		bSizer351.Add( self.m_staticText52, 0, wx.ALL, 5 )

		self.m_gauge31 = wx.Gauge( self.Overview, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge31.SetValue( 60 )
		bSizer351.Add( self.m_gauge31, 0, wx.ALL, 5 )

		self.m_gauge41 = wx.Gauge( self.Overview, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge41.SetValue( 45 )
		bSizer351.Add( self.m_gauge41, 0, wx.ALL, 5 )

		self.m_gauge51 = wx.Gauge( self.Overview, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge51.SetValue( 70 )
		bSizer351.Add( self.m_gauge51, 0, wx.ALL, 5 )

		self.m_gauge61 = wx.Gauge( self.Overview, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge61.SetValue( 0 )
		bSizer351.Add( self.m_gauge61, 0, wx.ALL, 5 )

		self.m_gauge71 = wx.Gauge( self.Overview, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge71.SetValue( 0 )
		bSizer351.Add( self.m_gauge71, 0, wx.ALL, 5 )

		self.m_gauge81 = wx.Gauge( self.Overview, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge81.SetValue( 0 )
		bSizer351.Add( self.m_gauge81, 0, wx.ALL, 5 )

		self.m_gauge91 = wx.Gauge( self.Overview, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge91.SetValue( 0 )
		bSizer351.Add( self.m_gauge91, 0, wx.ALL, 5 )


		fgSizer51.Add( bSizer351, 1, wx.EXPAND, 5 )


		self.Overview.SetSizer( fgSizer51 )
		self.Overview.Layout()
		fgSizer51.Fit( self.Overview )
		self.m_auinotebook5.AddPage( self.Overview, u"Overview", True, wx.NullBitmap )
		self.m_panel14 = wx.Panel( self.m_auinotebook5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer5 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		bSizer36 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText12 = wx.StaticText( self.m_panel14, wx.ID_ANY, u"Cell1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )

		bSizer36.Add( self.m_staticText12, 0, wx.ALL, 5 )

		self.m_staticText13 = wx.StaticText( self.m_panel14, wx.ID_ANY, u"Cell2", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )

		bSizer36.Add( self.m_staticText13, 0, wx.ALL, 5 )

		self.m_staticText14 = wx.StaticText( self.m_panel14, wx.ID_ANY, u"Cell3", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )

		bSizer36.Add( self.m_staticText14, 0, wx.ALL, 5 )

		self.m_staticText15 = wx.StaticText( self.m_panel14, wx.ID_ANY, u"Cell4", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )

		bSizer36.Add( self.m_staticText15, 0, wx.ALL, 5 )

		self.m_staticText16 = wx.StaticText( self.m_panel14, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )

		bSizer36.Add( self.m_staticText16, 0, wx.ALL, 5 )

		self.m_staticText17 = wx.StaticText( self.m_panel14, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )

		bSizer36.Add( self.m_staticText17, 0, wx.ALL, 5 )

		self.m_staticText18 = wx.StaticText( self.m_panel14, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )

		bSizer36.Add( self.m_staticText18, 0, wx.ALL, 5 )

		self.m_staticText19 = wx.StaticText( self.m_panel14, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )

		bSizer36.Add( self.m_staticText19, 0, wx.ALL, 5 )


		fgSizer5.Add( bSizer36, 1, wx.EXPAND, 5 )

		bSizer35 = wx.BoxSizer( wx.VERTICAL )

		self.m_gauge2 = wx.Gauge( self.m_panel14, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge2.SetValue( 60 )
		bSizer35.Add( self.m_gauge2, 0, wx.ALL, 5 )

		self.m_gauge3 = wx.Gauge( self.m_panel14, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge3.SetValue( 60 )
		bSizer35.Add( self.m_gauge3, 0, wx.ALL, 5 )

		self.m_gauge4 = wx.Gauge( self.m_panel14, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge4.SetValue( 45 )
		bSizer35.Add( self.m_gauge4, 0, wx.ALL, 5 )

		self.m_gauge5 = wx.Gauge( self.m_panel14, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge5.SetValue( 70 )
		bSizer35.Add( self.m_gauge5, 0, wx.ALL, 5 )

		self.m_gauge6 = wx.Gauge( self.m_panel14, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge6.SetValue( 0 )
		bSizer35.Add( self.m_gauge6, 0, wx.ALL, 5 )

		self.m_gauge7 = wx.Gauge( self.m_panel14, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge7.SetValue( 0 )
		bSizer35.Add( self.m_gauge7, 0, wx.ALL, 5 )

		self.m_gauge8 = wx.Gauge( self.m_panel14, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge8.SetValue( 0 )
		bSizer35.Add( self.m_gauge8, 0, wx.ALL, 5 )

		self.m_gauge9 = wx.Gauge( self.m_panel14, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge9.SetValue( 0 )
		bSizer35.Add( self.m_gauge9, 0, wx.ALL, 5 )


		fgSizer5.Add( bSizer35, 1, wx.EXPAND, 5 )


		self.m_panel14.SetSizer( fgSizer5 )
		self.m_panel14.Layout()
		fgSizer5.Fit( self.m_panel14 )
		self.m_auinotebook5.AddPage( self.m_panel14, u"Lot 1", False, wx.NullBitmap )
		self.m_panel15 = wx.Panel( self.m_auinotebook5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_auinotebook5.AddPage( self.m_panel15, u"Lot 2", False, wx.NullBitmap )
		self.m_panel16 = wx.Panel( self.m_auinotebook5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_auinotebook5.AddPage( self.m_panel16, u"Lot 3", False, wx.NullBitmap )

		bSizer34.Add( self.m_auinotebook5, 1, wx.EXPAND |wx.ALL, 5 )


		self.m_panel13.SetSizer( bSizer34 )
		self.m_panel13.Layout()
		bSizer34.Fit( self.m_panel13 )
		self.m_auinotebook4.AddPage( self.m_panel13, u"BMS", False, wx.NullBitmap )
		self.charger = wx.Panel( self.m_auinotebook4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_auinotebook4.AddPage( self.charger, u"Charger", False, wx.NullBitmap )
		self.motorController = wx.Panel( self.m_auinotebook4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_auinotebook4.AddPage( self.motorController, u"Kelly", False, wx.NullBitmap )

		bSizer26.Add( self.m_auinotebook4, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer26 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.connect_button.Bind( wx.EVT_BUTTON, self.on_connect )
		self.pause_button.Bind( wx.EVT_BUTTON, self.on_pause )
		self.save_button.Bind( wx.EVT_BUTTON, self.on_save )
		self.clear_button.Bind( wx.EVT_BUTTON, self.on_clear )
		self.ota_FilePicker.Bind( wx.EVT_FILEPICKER_CHANGED, self.load_image_file )
		self.loadImage.Bind( wx.EVT_BUTTON, self.upload_image )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def on_connect( self, event ):
		event.Skip()

	def on_pause( self, event ):
		event.Skip()

	def on_save( self, event ):
		event.Skip()

	def on_clear( self, event ):
		event.Skip()

	def load_image_file( self, event ):
		event.Skip()

	def upload_image( self, event ):
		event.Skip()


