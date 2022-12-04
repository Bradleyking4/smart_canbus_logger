import multiprocessing
import wx
import serial_interface
import queue
import time

import can

bustype = 'socketcan'
channel = 'can0'


class SerialProcess(multiprocessing.Process):
	def __init__(self, serial_port, bitrate, TxQueue,RxQueue):
		multiprocessing.Process.__init__(self)
		self._TxQueue = TxQueue
		self._RxQueue = RxQueue
		self._abort_pending = False
		self._connected = False
		self._serial_port = serial_port
		self._bitrate = bitrate
		self.start()

	def run(self):
		self._serial = serial_interface.SerialInterface()
		print("Serial port is " + self._serial_port + " Bitrate is " + self._bitrate)
		self._serial.connect(self._serial_port, self._bitrate)
		while True:
			try:
				stop = self._RxQueue.get_nowait()
				if stop=="stop":
					break
			except queue.Empty:
				pass
			
			can_message = self._serial.read_message()
			if can_message:
				print("Add to queue " +str( can_message.arbitration_id))
				self._RxQueue.put(can_message)
				time.sleep(.001)
				# print(self._queue.qsize())
			try:
				message =  self._TxQueue.get_nowait()
				if message:
					self._serial.write_message(message)
			except queue.Empty:
				pass



class CanProcess(multiprocessing.Process):
	def __init__(self, canChannel, bitrate, TxQueue,RxQueue):
		multiprocessing.Process.__init__(self)
		self._TxQueue = TxQueue
		self._RxQueue = RxQueue
		self._abort_pending = False
		self._connected = False
		self._channel = channel
		self._bitrate = bitrate
		self.start()

	def run(self):
		self._bus = can.interface.Bus(channel=channel, bustype=bustype,bitrate=self._bitrate)
		self._serial = serial_interface.SerialInterface()
		print("Can port is " + self._channel + " Bitrate is " + self._bitrate)
		while True:
			try:
				stop = self._RxQueue.get_nowait()
				if stop=="stop":
					break
			except queue.Empty:
				pass
			
			can_message =  self._bus.recv()
			if can_message:
				print("Add to queue " +str( can_message.arbitration_id))
				self._RxQueue.put(can_message)
				time.sleep(.001) 
				# print(self._queue.qsize())
			try:
				message =  self._TxQueue.get_nowait()

				# msg = can.Message(arbitration_id=0xc0ffee, data=[0, 1, 3, 1, 4, 1], is_extended_id=False)

				if message:
					bus.send(message)
			except queue.Empty:
				pass


git config --global user.email "bradleyking4@gmail.com"
  git config --global user.name "Bradley King"