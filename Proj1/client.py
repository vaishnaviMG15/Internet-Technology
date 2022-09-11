import threading
import socket
import sys

rsHostName = ''
rsListenPort = 0
tsListenPort = 0

def client():

	#opens the file with all the hostnames to be queried. Name of this file: PROJI-HNS.txt

	f_input = open("PROJI-HNS.txt", "r")

	f_output = open("RESOLVED.txt", "w")

	outputList = []
	
	#creating two sockets on client side
	#cr connects to root server
	#ct connects to top level server

	try:
        	cr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
        	print('socket open error: {} \n'.format(err))
        	exit()	



	#getting the ip address of the root srver based on the root servers host name as given by the input
	rootserverAddr = socket.gethostbyname(rsHostname)
	


	#connecting the cr socket to the root server's host and root server's listening port
	rootserverBinding = (rootserverAddr, rsListenPort)	
	cr.connect(rootserverBinding)

        #b keeps track of whether or not we are already connected to the top level server
        b = False
	#reading in each query from PROJI-HNS.txt and communicating with servers

	for query in f_input:

                
                query=query.strip()

		#send this query to root server
		cr.send(query.encode('utf-8'))	

		#get response from root server
		data_from_root_server = cr.recv(200)
		root_response = data_from_root_server.decode('utf-8')

 		rwords = root_response.split(' ')

		if rwords[2] == 'A':
			outputList.append(root_response + '\n' )

		elif rwords[2] == 'NS':
                        
                        if not b:
			    #connecting to top level server through socket ct			
			    tsHostname = rwords[0]
			    tsAddr = socket.gethostbyname(tsHostname)
			    tsBinding = (tsAddr, tsListenPort)
			    ct.connect(tsBinding)
                            b = True
			
			#communicating with top level server
			ct.send(query.encode('utf-8'))
			data_from_tls = ct.recv(200)
			tl_response = data_from_tls.decode('utf-8')
			
			outputList.append(tl_response + '\n')
               
	f_output.writelines(outputList)
        ct.close()
	cr.close()
	exit()
			

if __name__ == "__main__":


	rsHostname = sys.argv[1]
	rsListenPort = int(sys.argv[2])
	tsListenPort = int(sys.argv[3])

	t2 = threading.Thread(name='client', target=client)
    	t2.start()

