import socket
import sys
from PIL import Image
import time
import subprocess

ack="Processed"
while True:
	user_input = raw_input("Enter name of a team member: ")
	print user_input
	s = socket.socket()
	s.connect(("localhost",9994))	
	s.send(user_input)
	l = s.recv(1024)
	if (l and l == 'Invalid Team Member'):
		print l
	elif (l and l != 'Invalid Team Member'):
		size=l
		print "Size of file is : ",size
		s.send(ack)
		iterations,last_packet=divmod(int(size),1024)
		cnt=0
		f = open("Team_Member" + ".jpg",'wb') 
		while cnt < iterations:
			cnt = cnt+1
			l = s.recv(1024)
			f.write(l)
		if last_packet > 0:
			y = s.recv(last_packet)
			f.write(y)
        	f.close()
                p = subprocess.Popen(["display","Team_Member.jpg"]) 
                time.sleep(5)
                p.kill()
	s.shutdown(socket.SHUT_RDWR)	
	s.close()