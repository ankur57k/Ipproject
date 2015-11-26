from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.util import str_to_bool
import time
import socket
import os
import thread
from Queue import Queue

link_avail=Queue() 	#Define a variable for passing between threads
edgestat=Queue()
cloudstat=Queue()

class InitSwitch(object):
	def __init__ (self,str):
		core.openflow.addListeners(self)

	def _handle_ConnectionUp (self, event):

		print "Switch is up, pushing flows"		
	
		self.connection = event.connection        
		msg = of.ofp_flow_mod()
		msg.priority = 1
		msg.match.dl_type = 0x806	#ARP Flows
		action = of.ofp_action_output(port = of.OFPP_NORMAL)
                msg.actions.append(action)
                self.connection.send(msg)

		msg1 = of.ofp_flow_mod()
		msg1.priority = 1
		msg1.match.dl_type = 0x800	#IP Flows
		action = of.ofp_action_output(port = of.OFPP_NORMAL)
                msg1.actions.append(action)
                self.connection.send(msg1)
 
              	msg2 = of.ofp_flow_mod()
		msg2.priority = 2
                msg2.match.dl_type = 0x800
                msg2.match.nw_proto = 6
		msg2.match.tp_src = 9000
		msg2.actions.append(of.ofp_action_nw_addr.set_src("192.168.2.1"))
		action = of.ofp_action_output(port = of.OFPP_NORMAL)
                msg2.actions.append(action)
		self.connection.send(msg2)

                pmsg2= of.ofp_flow_mod()
		pmsg2.priority = 2
                pmsg2.match.dl_type = 0x800
                pmsg2.match.nw_proto = 6
		pmsg2.match.tp_dst = 9000
		pmsg2.actions.append(of.ofp_action_nw_addr.set_dst("192.168.1.1"))
		action = of.ofp_action_output(port = of.OFPP_NORMAL)
                pmsg2.actions.append(action)
		self.connection.send(pmsg2)

		print "Switch is connected now , Entering flowchange module"
                thread.start_new_thread(flowchange , (self,))


def flowchange(Switch):
  	print "Inside flowchange" 
	linkhis=0 		#Save link history to capture link status changes
	while(1):
		value=link_avail.get()
		if(linkhis!=value and value==1):	#Check that link is down and corresponding flows have not already been pushed
			
			clear = of.ofp_flow_mod(command=of.OFPFC_DELETE) 	#If link status has changed to down (from up), then delete previous flows 
			Switch.connection.send(clear)
			
        	        msg3 = of.ofp_flow_mod()
               		msg3.priority = 3
        	        msg3.match.dl_type = 0x806
               		action = of.ofp_action_output(port = of.OFPP_NORMAL)
               		msg3.actions.append(action)
               		Switch.connection.send(msg3)

                	msg4 = of.ofp_flow_mod()
                	msg4.priority = 3
               		msg4.match.dl_type = 0x800
                	action = of.ofp_action_output(port = of.OFPP_NORMAL)
                	msg4.actions.append(action)
                	Switch.connection.send(msg4)			
		linkhis=value

def linkmonitor(str1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.4.2",9999))		

        sum = 0
        while (1):
		s.send('Hello')
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
			thread.start_new_thread(getEdgeStat,("Thread-edge",))
		 	thread.start_new_thread(getCloudStat,("Thread-cloud",))
                        while(0 == cloudstat.empty())
				pass
			cloudload = cloudstat.get()
			while(0 == edgestat.empty())
				pass
			edgeload = edgestat.get()
			
        s.close()

def getEdgeStat(threadname,):
	gateway_edge_ip = '192.168.4.2'
	s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s1.connect((gateway_edge_ip,9880))	
	s1.send("GET_")
	l = s1.recv(1024)
	edgestat.put(float(l))
	s1.shutdown(socket.SHUT_RDWR)
	s1.close()


def getCloudStat(threadname,):
	gateway_cloud_ip = '192.168.4.2'
	s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s2.connect((gateway_cloud_ip,9881))	
	s2.send("GET_")
	l = s2.recv(1024)
	cloudstat.put(float(l))
	s2.shutdown(socket.SHUT_RDWR)
	s2.close()


def launch():
	NewSwitch = InitSwitch("First")
        core.register("First",NewSwitch)

        thread.start_new_thread(linkmonitor, ("Handler",))
	
			
	
	
