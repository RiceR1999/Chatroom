
#!/usr/bin/env python3
#Client part of the UDP chatroom
#Author: Ryan Rice
import socket
import threading
import sys 

#grab client hostname and setup connection variables
hostname = socket.gethostname()
#change address to your local machine ip to run this program
addr = "127.0.1.1"
port = 4444
server_address = (addr, port)
qmsg = "!quit"
quit = False

#create the client socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#connect the client to the server"
clientSocket.sendto(str.encode("!Join"), server_address)



#This is the function that runs on thread one, it recieves UDP packets from the server and prints them
#When a user inputs the quit signal it will end the thread once the server sends an acknowledgement that the user inputed
#the quit signal
def recvAndPrint(serverSocket,quit):
    while quit == False:
        data, address = clientSocket.recvfrom(1024)
        message = data.decode("utf-8")
        if message != qmsg:
            print(data.decode())
            print("\n")
        else:
            print("You have left the chatroom.")
            quit = True


#This is the function that runs on thread two, waits for user input and then 
#sends user input to the server as a UDP packet
def sendMsg(serverSocket,quit):
    while quit == False:
        msg = input("<You>: ")
        if msg == qmsg:
            clientSocket.sendto(str.encode(qmsg), server_address)
            quit = True
        else:
            clientSocket.sendto(str.encode(msg), server_address)


#Set up our threads
threadOne = threading.Thread(target=recvAndPrint, args=(clientSocket,quit,))
threadTwo = threading.Thread(target=sendMsg, args=(clientSocket,quit,))     

#Start our threads, order matters here as the user must first input the quit message before we are able to recieve it
#and finish executing thread one, thus thread two must start and end first
threadTwo.start()
threadOne.start()

#Join the threads in order of execution
threadTwo.join()
threadOne.join()

#Close our connection
clientSocket.close()

#Exit the program
exit()
