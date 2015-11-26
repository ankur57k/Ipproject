import os
import zipfile
import glob
import shutil

contents = glob.glob('./*.jpg')
path="toSend"
if os.path.exists(path):
    shutil.rmtree(path)

os.makedirs(path)
for filename in contents:
        read_file = open(filename[2:],'rb')
        buff = read_file.read()
	temp_file = open((os.path.join(path, filename)), 'wb')  
	temp_file.write(buff)
	temp_file.close()
        read_file.close()

def zipdir(dirPath=None, zipFilePath=None, includeDirInZip=True):

    if not zipFilePath:
        zipFilePath = dirPath + ".zip"
    if not os.path.isdir(dirPath):
        raise OSError("dirPath argument must point to a directory. '%s' does not." % dirPath)
    parentDir, dirToZip = os.path.split(dirPath)
    def trimPath(path):
        archivePath = path.replace(parentDir, "", 1)
        if parentDir:
            archivePath = archivePath.replace(os.path.sep, "", 1)
        if not includeDirInZip:
            archivePath = archivePath.replace(dirToZip + os.path.sep, "", 1)
        return os.path.normcase(archivePath)

    outFile = zipfile.ZipFile(zipFilePath, "w",
        compression=zipfile.ZIP_DEFLATED)
    for (archiveDirPath, dirNames, fileNames) in os.walk(dirPath):
        for fileName in fileNames:
            filePath = os.path.join(archiveDirPath, fileName)
            outFile.write(filePath, trimPath(filePath))
        if not fileNames and not dirNames:
            zipInfo = zipfile.ZipInfo(trimPath(archiveDirPath) + "/")
            outFile.writestr(zipInfo, "")
    outFile.close()

zipdir("toSend")

#Done with the zipping portion.

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = "192.168.2.1" 
port = 9001                # Reserve a port for your service.

s.connect((host, port))
f = open('toSend.zip','rb')
l = f.read(1024)
while l:
    s.send(l)
    l = f.read(1024)
f.close()
print("Done Sending")
s.shutdown(socket.SHUT_WR)
print(s.recv(1024))
s.close                     # Close the socket when done





