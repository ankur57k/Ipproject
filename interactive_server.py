import socket
import sys
import os

ack = "Processed"
s = socket.socket()
s.bind(("localhost",9994))
s.listen(10) 
while True:
	sc, address = s.accept()
	print address
	path = "Team_Members"
	name = sc.recv(1024)
	print name
	print os.path.join(path, name+".jpg")
	if os.path.isfile(os.path.join(path, name+".jpg")):
		print "Valid Team Member"
		f=open (os.path.join(path, name+".jpg"), "rb") 
		f.seek(0,os.SEEK_END)
		size = f.tell()
		sc.send(str(size))
		l = sc.recv(1024)
		if (l == 'Processed'):
			f.seek(0,0)
			l = f.read(1024)
			while (l):
				sc.send(l)
				l = f.read(1024)
			f.close()
	else:
		l = "Invalid Team Member"
		sc.send(l)
	sc.shutdown(socket.SHUT_RDWR)	
	sc.close()
s.close()
