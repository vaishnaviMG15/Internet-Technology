import threading
import time
import sys
import socket

lsListenPort = 0
ts1Hostname = ' '
ts1ListenPort = 0
ts2Hostname = ' '
ts2ListenPort = 0

def loadBalancingServer():

	#creating a listening socket on this server side
	try:
            l = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    l1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    l2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as err:
	    print('socket open error: {}\n'.format(err))
            exit()

	#current host this is running on
	host = socket.gethostname()	
	ip = socket.gethostbyname(host)

	#This socket is binding to the host it is running on at the input port
	server_binding = ('', lsListenPort)
	l.bind(server_binding)

	#enable this socket to start listening to connections from the client
	l.listen(1)

	#accepting a connection from client at ip 'addr'. 
	#'csockid' is the socket id of the connecting socket (also on the server side) for this particular connection 
	csockid, addr = l.accept()

	#getting the ip address of the 1st DNS server based on the ts1Hostname as given by the input
	ts1Addr = socket.gethostbyname(ts1Hostname)
	
	#connecting the ls1 socket to the 1st DNS server's host and listening port
	ts1Binding = (ts1Addr, ts1ListenPort)	
	l1.connect(ts1Binding)
	l1.setblocking(0)


	#getting the ip address of the 2nd DNS server based on the ts2Hostname as given by the input
	ts2Addr = socket.gethostbyname(ts2Hostname)
	
	#connecting the l2 socket to the 2nd DNS server's host and listening port
	ts2Binding = (ts2Addr, ts2ListenPort)	
	l2.connect(ts2Binding)
	l2.setblocking(0)

	errorMsg = ' - Error:HOST NOT FOUND'
	
	while True:

		data_from_client = ' '
		try:
		    data_from_client = csockid.recv(200)
			
		except socket.error as err:
		    break
		
		decoded_data = data_from_client.decode('utf-8')

		if len(decoded_data) == 0:
		    continue

		#at this point decoded_data has the client request
		found = False
		

		#send this query to both the DNS servers
		l1.send(decoded_data.encode('utf-8'))
		l2.send(decoded_data.encode('utf-8'))
		
		#wait for 5 seconds
		#time.sleep(5)

                t0 = time.time()
                t1 = time.time()

                

                while(t1 - t0 <= 5.0):
                    
		    #check if either socket sent a response
		    try:
        		response = l1.recv(200)
			csockid.send(response.encode('utf-8'))
                        found = True
                        break
    		    except socket.error, e:
                        try:
                            response = l2.recv(200)
                            csockid.send(response.encode('utf-8'))
                            found = True
                            break
                        except socket.error, e:
                            t1 = time.time()


                if (found == False):
                    response = decoded_data + errorMsg
                    csockid.send(response.encode('utf-8'))
                


		

	l.close()
	l1.close()
	l2.close()
	exit()


if __name__ == "__main__":
	#getting the command line input: 
	#port through which server listens for queries from client: lsListenPort
   	#Hostname of the first DNS server and the port through which it listens for requests: ts1Hostname and ts1ListenPort 
    	#Hostname of the second DNS server and the port through which it listens for requests: ts2Hostname and ts2ListenPort
    

	lsListenPort = int(sys.argv[1])
	ts1Hostname = sys.argv[2]
	ts1ListenPort = int(sys.argv[3])
	ts2Hostname = sys.argv[4]
	ts2ListenPort = int(sys.argv[5])

	#Initiate a thread that will run the loadBalancingServer() function
	t1 = threading.Thread(name='loadBalancingServer', target=loadBalancingServer)
	t1.start()
