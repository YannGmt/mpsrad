# -*- coding: utf-8 -*-
"""
Wiltron local oscillator communication for stepping frequency

Last modification: 09.07.2018
Author: Borys Dabrowski, dabrowski@mps.mpg.de
"""

import socket,time

class wiltron68169B:
	""" Interactions with wiltron68169B functionality

	Loads the shared wiltron-library as ../lib/libwiltron68169B.so on import
	and handles translation of python input to ctypes and ctypes output to
	python-readable variables

	Functions:
		ask_name:
			Asks the name (to see it there is a response)

		set_frequency:
			Sets the frequency to provided GHz
	"""
	def __init__(self, address=5, host='gpib', tcp_port=1234,
			timeout=.5, name="wiltron68169B-python"):
		self._initialized=False
		self._address=address
		self._timeout=timeout

		# Host information
		self._tcp_port=tcp_port
		self._host=host

	def ask_name(self):
		# Connect
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((self._host,self._tcp_port))
		s.setblocking(0)	# make socket non blocking

		# Set address
		s.sendall(b'++addr '+str(self._address).encode()+b'\r\n')

		# Ask name
		s.sendall(b"OI\r\n")
		time.sleep(.1)

		# Get the answer
		t0,ready=time.time(),False
		while time.time()-t0<self._timeout and not ready:
			time.sleep(.1)
			try:
				# get the beginning of the message
				answ=s.recv(1024)
				time.sleep(.1)
				# get the rest
				try: answ=answ+s.recv(1024)
				except: pass
				ready=True
			except: pass

		# Close socket
		s.close()

		if ready: return answ.replace(b'\r\n',b'')
		else: return ''


	def init(self):
		assert not self._initialized, "Cannot init initialized Wiltron"

		self.ask_name()
		self._initialized=True

	def close(self):
		assert self._initialized, "Cannot close an uninitialized Wiltron"
		self.ask_name()
		self._initialized=False

	def set_frequency(self, freq):
		assert self._initialized, "Must first initialize the Wiltron"

		# Connect
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((self._host,self._tcp_port))
		s.setblocking(0)	# make socket non blocking

		# Set address
		s.sendall(b'++addr '+str(self._address).encode()+b'\r\n')
		time.sleep(.1)

		# Set frequency
		s.sendall(b"CF1 "+str(freq).encode()+b" GH\r\n")
		time.sleep(.1)

		# Close socket
		s.close()
