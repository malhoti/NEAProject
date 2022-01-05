import socket
from _thread import *
import sys
from player import Player
from platforms import Platform
import random
import pickle
import copy


from settings import *

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

#players = [Player(0,0,100,100,(0,255,0)),Player(30,200,100,100,(255,0,0))]

def make_platform(onscreen):
    if onscreen:
        yrange =  random.randint(0,screen_height) #make platform on screen

    else:
        yrange =  random.randint(-75,-40) # make platform out of screen

    platform = [random.randint(0,screen_width-80), yrange,80,40]                               

    return platform



pos = [[40,screen_height-50,0],[0,screen_height+100,0]]
platform_pos = [[0,screen_height-40,screen_width,40]] # this is the bottom platform

for i in range(10):
    platform_pos.append(make_platform(True))

player1_platform = [] 
player2_platform = []
def threaded_client(connection, player): 
    
    # if player 1 connects , then you send players 2 cooridinates outside the screen so it appaers player 1 is in lobby by itself
    # if player connects  2 this changes the coordiantes and send it on screen, so on player 1's screen it appear as player 2 just joined the lobby
    if player ==0:    
        info_to_send = pickle.dumps([pos,platform_pos])
        connection.send(info_to_send)
    else : 
        info_to_send = pickle.dumps([[[screen_width-150,screen_height-40],pos[0],0],platform_pos])
        connection.send(info_to_send)


    reply= []
    new_platform = []
    run_p1 =True
    run_p2 = True
    while True:
        
        try:
            data = pickle.loads(connection.recv(2048)) # number of bits that the connection can recieve
            pos[player] = data[0]
            send_platform = data[1]
            
            if not data:  # if no data was sent from client, it means they are not in connection, so we print disconnected
                print("Disconnected")
                break

            else:
                if send_platform:
                    temp_plat = make_platform(False)
                    player1_platform.append(temp_plat)
                    player2_platform.append(temp_plat)

                if player == 1:
                    reply = pos[0]
                    
                    new_platform = copy.deepcopy(player2_platform) # this copies the list onto the other
                    if send_platform:
                        for platform in player1_platform:
                            platform[1] = platform[1]-(pos[1][2]-pos[0][2])
                                            
                    player2_platform.clear()
                    
                    
                else: 
                   
                    reply = pos[1]
                    
                    new_platform= copy.deepcopy(player1_platform)
                    if send_platform: 
                        for platform in player2_platform: 
                           
                            platform[1] = platform[1]-(pos[0][2]-pos[1][2])

                    player1_platform.clear()
                   
            #change to sendall if something doesnt work
            connection.sendall(pickle.dumps([reply,new_platform])) # this data is sent back to the client in encoded form, meaning it will have to be decoded by the client once again
        except:
            break


    print("Lost connection")
    currentPlayer = 0
    connection.close() # we close connection if we lose connection, so that client could joi back if they want. not adding this would cause a confusion or crash

# threading is basically allowing many function to be processed at the same time. For this case, whilst the while loop is running, if it callsthreaded_client, it doesnt need that function to finish to carry on the while loop, the while loop will still run whilt the function is also running
# this is so that it is always allowing for connections to connect. if the function is being run, and a client joins the server, then they wont be able to join as te while loop isnt running at that current time. so threading fixes that problem

currentPlayer = 0 # how many connetion are on

while True:
    print(ip_address)
    connection, address = sock.accept()
    print("Connected to:" , address)

    start_new_thread(threaded_client,(connection,currentPlayer%2))
    currentPlayer+= 1
