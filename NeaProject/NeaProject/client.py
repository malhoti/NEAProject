import pygame
import socket
from network import Network
from player import Player

#global varibales
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue= (0,0,255)


width = 600
height = 900

window = pygame.display.set_mode((width,height))
pygame.display.set_caption("Game")



def redrawWindow(window, player1, player2):
    window.fill(white)
    player2.draw(window)
    player1.draw(window)
    
    pygame.display.update()

def main():
    run = True
    network = Network()
    player1 = network.getP()

    
    clock = pygame.time.Clock()


    while run:
        clock.tick(144)
        player2 = network.send(player1) #when you send player1, the network sends player 2 to this client, and viceversa for player2

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player1.move()
        redrawWindow(window, player1, player2)

main()
