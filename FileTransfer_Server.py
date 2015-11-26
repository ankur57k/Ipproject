import socket               # Import socket module
import os
import glob
import zipfile
import shutil
import subprocess

contents = glob.glob('./*.zip')
for filename in contents:
	os.remove(filename)

s = socket.socket()         # Create a socket object
host = "192.168.2.1"        # Get local machine name
port = 9001                 # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

f = open('toReceive.zip','wb')
s.listen(20)                 # Now wait for client connection.
c, addr = s.accept()     # Establish connection with client.
l = c.recv(1024)
while l:
    f.write(l)
    l = c.recv(1024)
f.close()
print("Done Receiving")
c.close()                # Close the connection

with zipfile.ZipFile('toReceive.zip', "r") as z:
    z.extractall()

contents = glob.glob('./toSend/*.jpg')
for filename in contents:
	read_file = open(filename,'rb')
	buf = read_file.read()
        write_file = open(filename[9:],'wb')
        write_file.write(buf)
        read_file.close()
        write_file.close()

os.remove("toReceive.zip")
shutil.rmtree("toSend")
subprocess.call("./Video_Make.sh", shell=True)
#p = subprocess.Popen(["avconv","-start_number 1 -r 2 -i Image%d.jpg -vcodec libx264 Demo567.mp4"]) 
#p.kill()






