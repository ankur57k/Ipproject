#!/usr/bin/python

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.util import str_to_bool
import time
import socket
import os
import thread
from Queue import Queue

def getEdgeStat(threadname,flag1,edgestat):
	gateway_ip = '192.168.4.1'
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((gateway_ip,9880))	
	s.send("GET_")
	l = s.recv(1024)
	edgestat.put(float(l))
	s.shutdown(socket.SHUT_RDWR)
	s.close()
	flag1.put(1)

def getCloudStat(threadname,flag2,cloudstat):
	gateway_ip = '192.168.4.1'
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((gateway_ip,9881))	
	s.send("GET_")
	l = s.recv(1024)
	cloudstat(float(l))
	s.shutdown(socket.SHUT_RDWR)
	s.close()
	flag2.put(1)


if __name__ = '__main__':
	NewSwitch = InitSwitch("First")
        core.register("First",NewSwitch)
	default_route = 0
	flag1 = Queue()
	flag2 = Queue()
	edgestat = Queue()
	cloudstat = Queue()
	while True:
		flag1.put(0)
		flag2.put(0)
		thread.start_new_thread(getEdgeStat, ("Thread-1",flag1,edgestat,))
		thread.start_new_thread(getCloudStat, ("Thread-2",flag2,cloudstat,))

		while(0 == flag1.get()):
			pass
		edgeload = edgestat.get()

		while(0 == flag2.get()):
			pass
		cloudload = cloudstat.get()		
	
		if(edgeload > cloudload):
			if (!default_route):
				#call function to push default_route - route to cloud 
		else:
			if(default_route):
				#call function to push no default_route - route to edge
		time.sleep(2)
			

