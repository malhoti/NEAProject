import pygame as pg
import socket
from platforms import Platform
from network import Network
from player import Player

from settings import *

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((screen_width, screen_height))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        self.running = True


    def new(self):
        self.network = Network()
        
        self.startPos = self.read_pos(self.network.getP())
        print(self.startPos)

        self.totalSprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
 #______________________________________________________________________________________________       
        self.player1 = Player(self.startPos[0],self.startPos[1],100,100,green) # PLAYER 1
        self.totalSprites.add(self.player1)

        self.player2 = Player(0,0,100,100,red)  # PLAYER 2
        self.totalSprites.add(self.player2)
    
#______________________________________________________________________________________________
        p1 = Platform(0, screen_height - 40, screen_width, 40)
        self.totalSprites.add(p1)
        self.platforms.add(p1)

        p2 = Platform(screen_width / 2 - 50, screen_height * 3 / 4, 100, 20)
        self.totalSprites.add(p2)
        self.platforms.add(p2)
        self.run()


    def run(self):
        self.run = True
        while self.run:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()


    def events(self):
        print(self.player1.position.x)
        player2Pos = self.read_pos(self.network.send(self.make_pos((int(self.player1.position.x), int(self.player1.position.y))))) #when you send player1, the network sends player 2 to this client, and viceversa for player2
        print(player2Pos)
        self.player2.position.x = player2Pos[0]
        
        self.player2.position.y = player2Pos[1]
        self.player2.update()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.run:
                    self.run = False
                self.running = False
                

    def update(self):
        self.player1.move()
        
        

        hits = pg.sprite.spritecollide(self.player1, self.platforms, False)
        if hits:
            self.player1.position.y = hits[0].rect.top
            self.player1.velocity.y = 0

       



    def draw(self):

        self.screen.fill(white)
        self.totalSprites.draw(self.screen)
        pg.display.flip() # updates the whole screen


    def read_pos(self, str):
        str = str.split(",")
        return int(str[0]), int(str[1])


    def make_pos(self, tup):
        return str(tup[0]) + "," + str(tup[1])

    

    # def main():
       
    #     clock = pygame.time.Clock()

    #     run = True
    #     while run:
    #         totalSprites.update()

    #         clock.tick(144)

    #         player2Pos = read_pos(network.send(make_pos((player1.x, player1.y)))) #when you send player1, the network sends player 2 to this client, and viceversa for player2
    #         print(player2Pos)
    #         player2.x = player2Pos[0]
    #         print(player2.x)
    #         player2.y = player2Pos[1]
    #         print(player2.x)
    #         player2.update()
            

    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 run = False
    #                 pygame.quit()

            
    #         redrawWindow(window, player1, player2, platforms)
game = Game()
while game.running:
    game.new()

pg.quit()  
