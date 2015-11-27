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
decision=Queue()
edgeload=Queue()

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
 
              
		print "Switch is connected now , Entering flowchange module"
                thread.start_new_thread(flowchange , (self,))


def flowchange(Switch):
  	print "Inside flowchange" 
	olddecision=0	#Save decision history

	while(True):
		if(decision.empty()==0):	#Check that link is down and corresponding flows have not already been pushed
			currentdecision=decision.get()
			print "currentdecision is :",currentdecision
			if(olddecision==0 and currentdecision==1):
				
				print "Clearing old entries"
						
				clear = of.ofp_flow_mod(command=of.OFPFC_DELETE) 	#If link status has changed to down (from up), then delete previous flows 
				Switch.connection.send(clear)


				print "Pushing flows to send to edge"				

				pmsg = of.ofp_flow_mod()
				pmsg.priority = 1
				pmsg.match.dl_type = 0x806	#ARP Flows
				action = of.ofp_action_output(port = of.OFPP_NORMAL)
				pmsg.actions.append(action)
				Switch.connection.send(pmsg)

				pmsg1 = of.ofp_flow_mod()
				pmsg1.priority = 1
				pmsg1.match.dl_type = 0x800	#IP Flows
				action = of.ofp_action_output(port = of.OFPP_NORMAL)
				pmsg1.actions.append(action)
				Switch.connection.send(pmsg1)
		 
			      	pmsg2 = of.ofp_flow_mod()
				pmsg2.priority = 2
				pmsg2.match.dl_type = 0x800
				pmsg2.match.nw_proto = 6
				pmsg2.match.tp_src = 9000
				pmsg2.actions.append(of.ofp_action_nw_addr.set_src("192.168.2.1"))
				action = of.ofp_action_output(port = of.OFPP_NORMAL)
				pmsg2.actions.append(action)
				Switch.connection.send(pmsg2)

				pmsg3= of.ofp_flow_mod()
				pmsg3.priority = 2
				pmsg3.match.dl_type = 0x800
				pmsg3.match.nw_proto = 6
				pmsg3.match.tp_dst = 9000
				pmsg3.actions.append(of.ofp_action_nw_addr.set_dst("192.168.1.1"))
				action = of.ofp_action_output(port = of.OFPP_NORMAL)
				pmsg3.actions.append(action)
				Switch.connection.send(pmsg3)


			elif(olddecision==1 and currentdecision==0):
				
				print "Clearing Old Entries"

				clear = of.ofp_flow_mod(command=of.OFPFC_DELETE)        #If link status has changed to down (from up), then delete previous flows 
                                Switch.connection.send(clear)
				
				print "Pushing flow to send to Infrastructure"
					 
				pmsg4 = of.ofp_flow_mod()
				pmsg4.priority = 1
				pmsg4.match.dl_type = 0x806	#ARP Flows
				action = of.ofp_action_output(port = of.OFPP_NORMAL)
				pmsg.actions.append(action)
				Switch.connection.send(pmsg4)

				pmsg5 = of.ofp_flow_mod()
				pmsg5.priority = 1
				pmsg5.match.dl_type = 0x800	#IP Flows
				action = of.ofp_action_output(port = of.OFPP_NORMAL)
				pmsg5.actions.append(action)
				Switch.connection.send(pmsg5)
	
			olddecision = currentdecision	
			

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
                                decision.put(0)
                                print "Edge is down"
                else:
                        print "Edge is up"
			sum = 0			
			thread.start_new_thread(getEdgeStat,("Thread-edge",))
		 	thread.start_new_thread(getCloudStat,("Thread-cloud",))
			thread.start_new_thread(getEdgeLoad,("Thred-load",))
			while(edgestat.empty()==0 or cloudstat.empty()==0 or edgeload.empty()==0):
				pass
			edgestatus=edgestat.get()
			cloudstatus=cloudstat.get()
			edgeld=edgeload.get()
			arr = edgelod.split(',')
			min_1_load = float(arr[0])
			min_15_load = float(arr[1])
			print float(arr[0]), float(arr[1])
			if(min_1_load < 0.85):
				if(edgestatus < cloudstatus):
					print "Decision to send to Edge made"
					decision.put(1)
				else:
					print "Decision to sent to Infrastructure made"
					decision.put(0)
			else:
				decision.put(0)
				
        s.close()


def getEdgeStat(threadname,):
	gateway_edge_ip = "192.168.4.2"
	s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s1.connect((gateway_edge_ip,9880))	
	s1.send("GET_")
	l = s1.recv(1024)
	edgestat.put(float(l))
	s1.shutdown(socket.SHUT_RDWR)
	s1.close()


def getCloudStat(threadname,):
	gateway_cloud_ip = "192.168.4.2"
	s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s2.connect((gateway_cloud_ip,9881))	
	s2.send("GET_")
	l = s2.recv(1024)
	cloudstat.put(float(l))
	s2.shutdown(socket.SHUT_RDWR)
	s2.close()

def getEdgeLoad(threadname,):
	edge_ip = "192.168.1.1"
	s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s3.connect((edge_ip,9882))	
	s3.send("GET_")
	l = s3.recv(1024)
	edgeload.put(l)
	s3.shutdown(socket.SHUT_RDWR)
	s3.close()


def launch():
	NewSwitch = InitSwitch("First")
        core.register("First",NewSwitch)

        thread.start_new_thread(linkmonitor, ("Handler",))
	
			
	
	
