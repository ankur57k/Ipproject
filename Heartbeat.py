import subprocess
import os
import sys
import time
import datetime
import socket

#Define a TCP socket to listen on interface connected to controller
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(("192.168.4.2",9999))
serversocket.listen(1)
connection,clientaddr = serversocket.accept()
address = "192.168.1.1"
#Dump output for subprocess call to null deivce
#This ensures that ping output is not printed to CLI Screen
 
with open(os.devnull, 'w') as f:
	while(1):
		l = connection.recv(1024)
		time.sleep(1)
		# Ping edge server IP address to check availability
		res = subprocess.call(['ping', '-c', '1','-W','1', address],stdout=f) 
		# res = 0 if ping successful
		# res = 1 if destination does not reply
		# res = 2 if destination is not reachable
		print res
		connection.send(str(res))
	  	if res == 0:
        		print "ping to", address, "OK"
   	 	elif res == 1:
        		print "no response from", address
		else:
        		print "ping to", address, "failed!" 
		# Uncomment the print statement to print the datetime 
	 	print datetime.datetime.utcnow()
		# Ping the edge server at an interval of 2 seconds ( Heartbeat messages )
		
