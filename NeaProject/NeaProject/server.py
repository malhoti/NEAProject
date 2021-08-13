import socket
from _thread import *
import sys
from player import Player
import pickle

hostname = socket.gethostname()  # this gets the hostname 
ip_address = socket.gethostbyname(hostname) 

server = str(ip_address)
port = 5555  # port that is open and free to use

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 'socket.AF_INET' is the internet address family for IPv4  
# SOCK_STREAM is the socket type for TCP, protocal that is used to trasnport packets on a network
# you can use socket.SOCK_DGRAM for UDP, but it isnt that reliable

try:
    sock.bind((server,port)) # this makes a connection to the server host and the port in order to make a functioning connection
except: # if the 'binding' fails instead of crashing we send an output of the error
    print(socket.error)

sock.listen(2) # opens the socket making it ready to accept connection, it takes one arguement, limiting how many clients can join the server. If empty it is unlimited
# if all goes well up to here, the server has started and is waiting for connections

print("SERVER STARTED!")

players = [Player(0,0,100,100,(0,255,0)),Player(30,200,100,100,(255,0,0))]



def threaded_client(connection, player):
    global currentplayer
    connection.send(pickle.dumps(players[player])) # sending message to client 
    reply= ""
    
    while True:
        try:
            data = pickle.loads((connection.recv(2048)))  # number of bits that the connection can recieve
            players[player] = data

            

            if not data:  # if no data was sent from client, it means they are not in connection, so we print disconnected

                print("Disconnected")
                currentPlayer = 0
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Recieved: ", reply)
                print("Sending: ", reply)
            
            connection.sendall(pickle.dumps(reply)) # this data is sent back to the client in encoded form, meaning it will have to be decoded by the client once again
        except:
            break

    print("Lost connection")
    currentPlayer = 0
    connection.close() # we close connection if we lose connection, so that client could joi back if they want. not adding this would cause a confusion or crash






# threading is basically allowing many function to be processed at the same time. For this case, whilst the while loop is running, if it callsthreaded_client, it doesnt need that function to finish to carry on the while loop, the while loop will still run whilt the function is also running
# this is so that it is always allowing for connections to connect. if the function is being run, and a client joins the server, then they wont be able to join as te while loop isnt running at that current time. so threading fixes that problem

currentPlayer = 0 # how many connetion are on

while True:
    connection, address = sock.accept()
    print("Connected to:" , address)

    start_new_thread(threaded_client,(connection,currentPlayer%2))
    currentPlayer+= 1
