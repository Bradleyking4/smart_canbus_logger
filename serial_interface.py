import serial
import datetime
import time

import os

# chose an implementation, depending on os
if os.name == 'nt': #sys.platform == 'win32':
    from serial.tools.list_ports_windows import *
elif os.name == 'posix':
    from serial.tools.list_ports_posix import *

class SerialException(serial.SerialException):
	pass


class CANMessage(object):

	def __init__(self,id, data, timestamp=None):
		self.arbitration_id = arbitration_id
		self.data = data
		self.timestamp = timestamp or datetime.datetime.now()



class SerialInterface(object):
	"""Serial interface to CAN bus logger. Handles communication protocol and processes incoming data frames
	and formats them to look pythonic"""

	supported_can_bitrates = [10, 20, 50, 100, 125, 250, 500, 1000]

	def scan(self):
		"""Scans for available ports. Returns a list of device names."""
		ports = []

		for i, desc, hwid in comports():
			try:
				s = serial.Serial(i)
				ports.append(s.portstr)
				s.close()
			except serial.SerialException:
				pass
		return ports

	def connect(self, serial_port, can_bitrate):
		"""Connects to MCU via serial port, sends bitrate selection packet"""
		
		self.serial = serial.Serial(
			port=str(serial_port),
			baudrate=250000,
			timeout=1
		)
		try:
			self.serial.setDTR(True)
			time.sleep(0.2)
			self.serial.setDTR(False)
			time.sleep(2)
			self.serial.write(chr(self.supported_can_bitrates.index(int(can_bitrate))).encode())
		except ValueError:
			raise SerialException("CAN bitrate not supported!")

	def read_message(self):
		line = self.serial.readline()
		if len(line)>2 and line[0]==126 and line[-2]==46:
			# print(line)

			#we have full line, decode it
			# print("Length",len(line), chr(line[0]), line[0]==126, chr(line[-2]), line[-2]==46)
			try:
				data = bytearray(8)
				for i in range(1,9):
					data[i-1] = (line[i])
				# for i in range(9,13):
				identifier  = (line[9]<<24) + (line[10]<<16) + (line[11]<<8) + line[12]
				print("<- ID:",identifier, " data:", data )

				return CANMessage(identifier, data)
			except IndexError:
				print ("Index error on line: %s" , line)
		return None

	def write_message(self,message):
		print("-> ID:",message.arbitration_id, " data:",message.data )

		line = bytearray(15)
		line[0] = 126
		for i in range(1,9):
			line[i] = message.data[i-1]
		line[9] = (message.arbitration_id >>24)& 0xff
		line[10] = (message.arbitration_id >>26)& 0xff
		line[11] = (message.arbitration_id >>8)& 0xff
		line[12] = message.arbitration_id & 0xff
		line[13] = 46
		line[14] = 10
		self.serial.write(line)


	def disconnect(self):
		self.serial.close()
		self.serial = None

