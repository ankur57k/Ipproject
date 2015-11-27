#!/usr/bin/python

import os
import sys
import time, threading
import socket

import re

def getload():
	ld = os.getloadavg()
	ldstr = str(ld[0]) + ',' + str(ld[2])
	return ldstr	

if __name__ == '__main__':
	s = socket.socket()
	s.bind(("192.168.1.1",9882))
	s.listen(10) 
	while True:
		sc, address = s.accept()
		print address
		name = sc.recv(1024)
		print name
		if(name == 'GET_'):
			load = getload()
			print load		
			sc.send(load)
		sc.shutdown(socket.SHUT_RDWR)	
		sc.close()
	s.close()
