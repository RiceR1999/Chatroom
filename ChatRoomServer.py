#!/usr/bin/env python3
#Server part of the UDP chat room
#Author: Ryan Rice
import socket
import sys

#Declare the list of clients currently on the server
clients = [] 
init = True

#Generic welcome message to be sent to all clients for new incoming clients
welcomeMessage = "Welcome to the chatroom! "
#Generice leave message to be sent to all clients
leaveMessage = " Has left the chatroom!"

#Grab server hostname
hostname = socket.gethostname()

#Grab server IP, this allows for the server IP to be dynamically
#changed instead of hardcoded if the server script is run on a 
#different machine
addr = socket.gethostbyname(hostname)

#We'll be running our server on port 4444
port = 4444

#Creat the UDP server socket using DGRAM protocol and bind it
#to the server address
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (addr, port)
serverSocket.bind(server_address)

print("Server initilized connection available at: " + addr)

#Listen on port 4444 for incoming data, do stuff with client data
while init:
    
    #listen for client data with a buffer size of 1024
    clientData = serverSocket.recvfrom(1024)
    #grab the message
    message = clientData[0]
    message = message.decode()
    #grab the client IP
    address = clientData[1]

    #check if address is new, if it is, welcome that client and add it to the active client list
    if address not in clients:
        clients.append(address)
        print("Welcome to the chat room: " + format(address))
        for clientAddress in clients:
            #send welcome message for new client and client message
            serverSocket.sendto(str.encode(format(address) + welcomeMessage), clientAddress)
    
    #check if client message contains the quit command, if it does, remove that client from
    #the active clients list and notify all active clients
    elif message == "!quit":
        if address in clients:
            serverSocket.sendto(str.encode("!quit"), address)
            print(format(address) + " has left the chatroom")
            clients.remove(address)
            for clientAddress in clients:
                serverSocket.sendto(str.encode(format(address) + ": " +  leaveMessage), clientAddress)
    
    #If we reach this point then we know this message is from an active client
    #send this clients message to all active clients in the chat room
    else:
        for clientAddress in clients:
            serverSocket.sendto(str.encode(format(address) + ": " + format(message)), clientAddress)
serverSocket.close()

