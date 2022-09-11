CS352 - Spring 2021
Project 1: Recursive DNS client and DNS servers
Gal Zandani (gz113) and Vaishnavi Manthena (vm504)



1. Briefly discuss how you implemented your iterative client functionality.

Client.py:

At the client side, I maintained a list of strings which stores the responses. At the end I printed this list to output txt file.
I also used a thread to run the client functionality. 

The client connects to the IP address determined by the rsHostname at the input root server listening port. This socket on client side is called 'cr.' The connection to the servers are made through .connect() command.

The client goes through the host names file line by line.

For each line it does the following:
->strips of any trailing whitespace characters
->encodes and sends the line/query to the root server through cr
->waits for response from server with recv(200) function
->if root server response ends with NS:
	-> connect to top level server if not done so already
		Note: In my implementation, the client only connects to the top server the first time. Later, it maintains this connection till the end. The connection is made using  
		IP address determined by the tsHostname and the input top level server listening port. Socket used on client side: 'ct'
	-> send query to ts using 'ct'socket
	-> wait for response
	->decode and add response to output list. 
->if root server response ends with A:
	->decode and add response to an output list.

Once the loop terminates write everything in output list to RESOLVED.txt
Close client sockets
Exit from thread

Servers:
Both rs.py and ts.py store a domain name table each. In each program I used a thread to run the significant functions rootServer() and topLevelServer().

The domain name table is implemented through a dictionary. The key value of the dictionary is the hostname. The value is a two tuple (x,y).
Here 'x' is an IP address or '-'. The 'y' is 'A' or 'NS'. Both of the servers first read through the respective files and load the information into the DNS table implementation. Later they create a socket and bind it to the host they are running on and the input listening port using .bind() command. Then the servers listen through these sockets for connections. Connections are established through accept() function. At this point the connecting sockets are instantiated at server's side. Then each of them go through an infinite while loop. In each iteration of the loop they receive data from their connecting sockets, do a lookup in their DNS table and respond to the client.

2. Are there known issues or functions that aren't working currently in your
   attached code? If so, explain.

We don't think there are any issues for this project. One small concern is that according to our implementation when the client.py program terminates, rs.py and ts.py keep running. From my side on the iLab machine, I tried to stop them using Ctrl-C which terminates the process completely. However, I am not able to do that. I am having to use Ctrl-Z and then use 'kill -9 processID' to kill the rs.py and ts.py processes. 


3. What problems did you face developing code for this project?

Some of the problems we faced when developing the code for this project are:

(a) Killing the rs.py, ts.py programs:
This is the same problem I have mentioned in the previous question. We spent a while to terminate (using kill command) our ts.py and rs.py programs, because we had to do it each time we tested the code.


(b) Trying to make rs.py and ts.py terminate successfully:
We tried to implement the project in order to smoothly terminate rs.py and ts.py after client.py stops running. We have made two attempts to do this:

	1. Putting recv() statement in a try except block. Our hope was that when the client closes its socket this would result in an error which could be handled so that we break out of the while true loop and terminate the program.

	2. We tried to check if the length of received string is 0. If so to break out of loop and terminate.
However both of these attempts did not work so we left it as our current implementation. 


(c)Working with python:
This was our first python project. We really liked the experience. It was interesting to deal with problems and debugging issues when it comes to dealing with strings and files. The extra trailing string characters caused issues with string comparisons which we later realized how to fix.



(d)Testing:
We ran a lot of test cases. There were two instances where the programs did not work. As far as we understood this was potentially due to that same port number being used by other students. Cause changing the port number resulted in the programs running normally again.



4. Reflect on what you learned by working on this project. 

By working on this project we learned the following:

(a) Better knowledge about coding with python and socket programming.

(b) Appreciate the interface sockets provide in networking (btw applications and the rest of the system). Through recv and send command it was easy to picture how our application layer message goes through a socket on one end and appears through the socket on the other end, effectively abstracting the complex intermediate steps.

(c) We got a practical understanding of the iterative approach of DNS, through client.py. We were also able to appreciate what kind of processes happen under the hood when we use a domain name in real life.

(d) We also understood the difference between listening sockets and connecting sockets on server sides. We were not sure of what exactly the accept() function returns. The difference between this socket and the one bounded to the listening port was unclear. The recent lectures and working on the project made this concept clear.

(e) We got an understanding of how recv() potentially works. Through our attempts to the check how recv() functions in the server after client closes, we believe that it is a function which only returns once it receives actual data from the client. Even after client terminates we guess that the server can still wait for information from the recv() call.







