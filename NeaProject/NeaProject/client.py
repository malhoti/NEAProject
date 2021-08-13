import pygame
import socket
from network import Network
from player import Player
from platform import *
from settings import *

#global varibales
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue= (0,0,255)




window = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Game")



def redrawWindow(window, player1, player2,p1):
    window.fill(white)
    player2.draw(window)
    player1.draw(window)
    p1.draw(window)
    
    pygame.display.update()

def main():
    network = Network()

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    
    player1 = network.getP()
    all_sprites.add(player1)

    p1 = Platform(0, screen_height - 40, screen_width, 40)
    all_sprites.add(p1)
    platforms.add(p1)

    p2 = Platform(screen_width / 2 - 50, screen_height * 3 / 4, 100, 20)
    all_sprites.add(p2)
    platforms.add(p2)
    
    
    
    
    
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(144)
        player2 = network.send(player1) #when you send player1, the network sends player 2 to this client, and viceversa for player2

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player1.move()
        redrawWindow(window, player1, player2,p1)

main()
