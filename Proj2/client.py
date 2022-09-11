import threading
import sys
import socket

lsHostName = ''
lsListenPort = 0

def client():

	#opens the file with all the hostnames to be queried. Name of this file: PROJI-HNS.txt

	f_input = open("PROJ2-HNS.txt", "r")

	f_output = open("RESOLVED.txt", "w")

	outputList = []

	#creating one sockets on client side
	#cl connects to load balancing server

	try:
        	cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
        	print('socket open error: {} \n'.format(err))
        	exit()

	#getting the ip address of the load balancing server based on the lb servers host name as given by the input
	hostAddr = socket.gethostbyname(lsHostname)
	
	#connecting the cr socket to the root server's host and root server's listening port
	hostBinding = (hostAddr, lsListenPort)	
	cl.connect(hostBinding)


	for query in f_input:

                query = query.strip()
		
		#send this query to lb server
		cl.send(query.encode('utf-8'))	

		#get response from lb server
		data_from_host = cl.recv(200)
		host_response = data_from_host.decode('utf-8')		
		outputList.append(host_response + '\n')
			

	f_output.writelines(outputList)

	cl.close()
	exit()

if __name__ == "__main__":

	lsHostname = sys.argv[1]

	lsListenPort = int(sys.argv[2])

	t2 = threading.Thread(name='client', target=client)
    	t2.start()
