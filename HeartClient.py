import socket
import thread

def handler(s):
        sum = 0
        while (1):
                result=s.recv(512)
                if int(result) == 1:
                        sum=sum+int(result)
                        print "Response not received from Edge"
                        if sum >= 3:
                                link_avail.put(1)
                                print "Edge is down"
                else:
                        print "Edge is up"
                        sum = 0

        s.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.4.2",9999))
	
thread.start_new_thread(handler, (s,))
handler(s)

