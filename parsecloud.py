#!/usr/bin/python

import os
import sys
import time, threading
import socket

import linecache
import re

def getRTT():
	os.system("ping -c 5 192.168.2.1 > pinginfra.txt")
        stri = linecache.getline('pinginfra.txt',10)		
        arr = stri.split('/')
	linecache.clearcache()
	if(4 <= len(arr)):
		return arr[4]
	else:
		return 64000

if __name__ == '__main__':
	s = socket.socket()
	s.bind(("192.168.4.2",9881))
	s.listen(10) 
	while True:
		sc, address = s.accept()
		print address
		name = sc.recv(1024)
		print name
		if(name == 'GET_'):
			rtt = getRTT()
			print rtt		
			sc.send(str(rtt))
		sc.shutdown(socket.SHUT_RDWR)	
		sc.close()
	s.close()
