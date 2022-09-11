import threading
import socket
import sys

port = 0

def DNS_Server_1 ():

	#first, the DNS server has to load information from the PROJ2-DNSTS1.txt
	#this information could be stored in a dictionary.
	#key: string representing the domain name
	#value: (IP address, A) 

	table = {}

	f_input = open("PROJ2-DNSTS1.txt", "r")

	#reading in each line of input file and filling in the table
	for line in f_input:
		words = line.split(' ')
		table[words[0].strip()] = (words[1].strip(), words[2].strip())

	#Now that the server has its information, we can implement the functionality

	#creating a socket on DNS server side
	try:
        	t1Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as err:
		print('socket open error: {}\n'.format(err))
        	exit()

	#current host this is running on
	host = socket.gethostname()	
	ip = socket.gethostbyname(host)

	#This socket is binding to the host it is running on at the input port
	server_binding = ('', port)
	t1Socket.bind(server_binding)

	#enable this socket to start listening to connections
	t1Socket.listen(1)

	#accepting a connection from load balancing server  at ip 'addr'. 
	#'csockid' is the socket id for the connecting socket (on this DNS server) for this particular connection 
	csockid, addr = t1Socket.accept()

	while True:

		data_from_host = ' '
		try:
			data_from_host = csockid.recv(200)
			
		except socket.error as err:
			break
		
		decoded_data = data_from_host.decode('utf-8')

		if len(decoded_data) == 0:
			continue

		#To convert data to lower case
		string1 = decoded_data.lower()

	
		for key in table:
			(a,b) = table[key]
			string2 = key.lower()
			if string1 == string2 :
				output_data = key + ' ' + a + ' ' + b 
				csockid.send(output_data.encode('utf-8'))
				break;


	t1Socket.close()
	exit()


if __name__ == "__main__":

    #getting the command line input: port through which DNS server listens for requests
    port = int(sys.argv[1])

    #Initiate a thread that will run the DNS_Server_1() function
    t1 = threading.Thread(name='DNS_Server_1', target=DNS_Server_1)
    t1.start()
