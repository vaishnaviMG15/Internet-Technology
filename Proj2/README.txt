CS352 - Spring 2021
Project 2: Load-balancing across DNS servers
Gal Zandani (gz113) and Vaishnavi Manthena (vm504)



1. Briefly discuss how you implemented the LS functionality of tracking which TS responded to the query and timing out if neither TS responded.

Client.py:

This just connects to the load balancing server. It does this by using a socket to bind to the IP address of load balancing server and it listening port as given by the inputs. Then, for each line of the input (PROJ2-HNS.txt) it does the following: encodes the input and passes it to server using the mentioned socket, receives the response from the server, and add response to an output list.

After all input lines are dealt with, everything from output list is written on RESOLVED.txt.



Servers ls.py:

This creates 3 sockets. One socket is a listening socket that binds to the listening port (as given by the input) of this load balancing server (machine where this code is running on). This socket listens to accept a connection from the client. Another socket connects to the listening port at the IP address of the ts1 server as determined by ts1hostname. The last socket does the same but connects with the ts2 server. Both of these sockets are made to be non blocking by using 'setblocking(0)'.
Now, the thread running the program goes into an infinite while loop. In each iteration data is received from the client, then passed to both of the ts servers by using the 2nd and 3rd sockets. Then we have a loop which iterates for at most 5 seconds waiting for ts1 and ts2 to get the information. If information is received it is passed to the client, else returns the host name searched with an error message.



Servers ts1.py and ts2.py:

This represents the DNS tables consisting the hostname, IP address, and flag (which is always assumed to be A) for each item in separate lines. It copies each table from the respective test files PROJ2-DNSTS1.txt and PROJ2-DNSTS2.txt in the corresponding file (ts1.py and ts2.py) to a dictionary for easier and most efficient search. Each table maintains a connection with ls.py while running the code, which searches through those tables for the input given and returns the information if found, else it returns nothing.



2. Are there known issues or functions that aren't working currently in your attached code? If so, explain.

We don't think there are any issues for this project. One small concern is that according to our implementation when the client.py program terminates, ls.py, ts1.py, and ts2.py keep running. From my side on the iLab machine, I tried to stop them using Ctrl-C which terminates the process completely. However, I am not able to do that. I am having to use Ctrl-Z and then use 'kill -9 processID' to kill the ls.py, ts1.py, and ts2.py processes. 

We formatted our test inputs according to the given instructions for valid inputs. So, our input has the correct/valid lines for all the text files (HNS, DNSTS1, DNSTS2) without any extra line at the bottom. 


3. What problems did you face developing code for this project?

Some of the problems we faced when developing the code for this project are:

(a) Killing the ls.py, ts1.py, and ts2.py programs:
This is the same problem I have mentioned in the previous question. We spent a while to terminate (using kill command) our ls.py, ts1.py, and ts2.py programs, because we had to do it each time we tested the code.


(b) Trying to make ls.py, ts1.py, and ts2.py terminate successfully:
We tried to implement the project in order to smoothly terminate ls.py, ts1.py, and ts2.py after client.py stops running. We have made two attempts to do this:

	1. Putting recv() statement in a try except block. Our hope was that when the client closes its socket this would result in an error which could be handled so that we break out of the while true loop and terminate the program.

	2. We tried to check if the length of received string is 0. If so to break out of loop and terminate.
However both of these attempts did not work so we left it as our current implementation. 


(c)Testing:
We had to change the port numbers sometimes while testing because when we reuse a port number, it sometimes gives an error cause we just recently used that port in our previous test or potentially due to some other student using that port at the same time.



4. What did you learn by working on this project?

By working on this project we learned the following: 

We learned about how recv really works. So, it just waits for the input and does not move forward until it collects some input. It was interesting to realize that by using a simple function like setblocking(0) we could change the behaviour of recv calls and work with sockets more efficiently.

By setting the timer of 5 seconds for receiving information it allows for more efficiency in using recv function. As soon as it gets some information it collects it, but if it does not it gives a decent amounts of time (in this case 5 seconds) which is not too much or too less to try and get information.



