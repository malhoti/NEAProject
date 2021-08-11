import socket
from _thread import *
import sys


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

pos = [(0,0),(100,100)]

def read_position(string):      # this reads the position that is given as string and converts to integers we can use
    string = string.split(",")
    return int(string[0]), int(string[1])

def make_position(tuple):      # this takes the int value of position and converts to string
    return str(tuple[0]) + "," + str(tuple[1])

def threaded_client(connection, player):
    connection.send(str.encode(make_position(pos[player]))) # sending message to client 
    reply= ""
    
    while True:
        try:
            data = read_position(connection.recv(2048).decode())   # number of bits that the connection can recieve
            pos[player] = data

            

            if not data:  # if no data was sent from client, it means they are not in connection, so we print disconnected

                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Recieved: ", reply)
                print("Sending: ", reply)
            
            connection.sendall(str.encode(make_position(reply))) # this data is sent back to the client in encoded form, meaning it will have to be decoded by the client once again
        except:
            break

    print("Lost connection")
    connection.close() # we close connection if we lose connection, so that client could joi back if they want. not adding this would cause a confusion or crash






# threading is basically allowing many function to be processed at the same time. For this case, whilst the while loop is running, if it callsthreaded_client, it doesnt need that function to finish to carry on the while loop, the while loop will still run whilt the function is also running
# this is so that it is always allowing for connections to connect. if the function is being run, and a client joins the server, then they wont be able to join as te while loop isnt running at that current time. so threading fixes that problem

currentPlayer = 0 # how many connetion are on

while True:
    connection, address = sock.accept()
    print("Connected to:" , address)

    start_new_thread(threaded_client,(connection,currentPlayer))
    currentPlayer+= 1
