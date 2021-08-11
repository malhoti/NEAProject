import pygame
import socket
from network import Network
#global varibales
white=(255,255,255)
red=(255,0,0)

width = 600
height = 900

window = pygame.display.set_mode((width,height))
pygame.display.set_caption("Game")

clientNumber=0

class Player():
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.rect = (x, y, width, height)
        self.velocity = 3

    def draw(self, window):
        pygame.draw.rect(window, self.colour, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.x += self.velocity
        if keys[pygame.K_UP]:
            self.y -= self.velocity
        if keys[pygame.K_DOWN]:
            self.y += self.velocity

        self.update()
    
    def update(self):

        self.rect = (self.x, self.y, self.width, self.height)

def read_position(string):      # this reads the position that is given as string and converts to integers we can use
    string = string.split(",")
    return int(string[0]), int (string[1])

def make_position(tuple):      # this takes the int value of position and converts to string
    return str(tuple[0]) + "," + str(tuple[1])

def redrawWindow(window, player1, player2):
    window.fill(white)
    player1.draw(window)
    player2.draw(window)
    pygame.display.update()

def main():
    run = True
    network = Network()
    startPosition = read_position(network.getPosition())


    player1 = Player(startPosition[0],startPosition[1],100,100,(0,255,0))
    player2 = Player(0,0,100,100,(0,255,0))
    clock = pygame.time.Clock()


    while run:
        clock.tick(144)

        player2Position = read_position(network.send(make_position((player1.x,player1.y))))
        player2.x = player2Position[0]
        player2.y = player2Position[1]

        player2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(window, player1, player2)

main()
