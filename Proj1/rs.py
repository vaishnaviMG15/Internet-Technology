import threading
import socket
import sys

port = 0

def rootServer():
    
	#first, the root server has to load information from the PROJI-DNSRS.txt
	#this information could be stored in a dictionary.
	#key: string representing the domain name
	#value: (IP address, A) or (-, NS)

	table = {}

	f_input = open("PROJI-DNSRS.txt", "r")

	#reading in each line of input file and filling in the table
	for line in f_input:
		words = line.split(' ')
		table[words[0].strip()] = (words[1].strip(), words[2].strip())

	#Now that the server has its information, we can implement the functionality

	#creating a listening socket on root server side
	try:
        	rSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as err:
		print('socket open error: {}\n'.format(err))
        	exit()

	#current host this is running on
	host = socket.gethostname()	
	ip = socket.gethostbyname(host)

	#This socket is binding to the host it is running on at the input port
	server_binding = ('', port)
	rSocket.bind(server_binding)

	#enable this socket to start listening to connections
	rSocket.listen(1)

	#accepting a connection from client at ip 'addr'. 
	#'csockid' is the socket id of the connecting socket (also on the server side) for this particular connection 
	csockid, addr = rSocket.accept()

	while True:


		data_from_client = ' '
		try:
			data_from_client = csockid.recv(200)
			
		except socket.error as err:
			break
		
		decoded_data = data_from_client.decode('utf-8')
		if len(decoded_data) == 0:
			continue

		string1 = decoded_data.lower()

		found = False

                for key in table:
                    if key.lower() == string1:
                        found = True
			(a,b) = table[key]
			output_data = key + ' ' + a + ' ' + b 
			csockid.send(output_data.encode('utf-8'))
			break;

		if not found:
			for key2 in table:
				(a,b) = table[key2]
				if b == 'NS':
					output_data = key2 + ' ' + a + ' ' + b
					csockid.send(output_data.encode('utf-8'))
                                        break

	rSocket.close()
	exit()
		 	

if __name__ == "__main__":

    #getting the command line input: port through which root server listens for requests
    port = int(sys.argv[1])

    #Initiate a thread that will run the rootServer() function
    t1 = threading.Thread(name='rootServer', target=rootServer)
    t1.start()

