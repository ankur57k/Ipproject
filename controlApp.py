#!/usr/bin/python

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.util import str_to_bool
import time
import socket
import os
import thread

def getEdgeStat(flag1,stat1):
	gateway_ip = '192.168.4.1'
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((gateway_ip,9880))	
	s.send("GET_")
	l = s.recv(1024)
	stat1 = float(l)
	s.shutdown(socket.SHUT_RDWR)
	s.close()
	flag1 = 1 

def getCloudStat(flag2,stat2):
	gateway_ip = '192.168.4.1'
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((gateway_ip,9881))	
	s.send("GET_")
	l = s.recv(1024)
	stat2 = float(l)
	s.shutdown(socket.SHUT_RDWR)
	s.close()
	flag2 = 1 


if __name__ = '__main__':
	NewSwitch = InitSwitch("First")
        core.register("First",NewSwitch)
	default_route = 0
	while True:
		flag1 = 0
		flag2 = 0
		edgestat=0
		cloudstat=0
		thread.start_new_thread(getEdgeStat, (flag1,edgestat,))
		thread.start_new_thread(getCloudStat, (flag2,cloudstat,))
		getEdgeStat(flag1,stat2)
		getCloudStat(flag2,stat2)

		while(!flag1 || !flag2):

		if(edgestat > cloudstat):
			if (!default_route):
				#call function to push default_route - route to cloud 
		else:
			if(defaulr_route):
				#call function to push no default_route - route to edge

	

