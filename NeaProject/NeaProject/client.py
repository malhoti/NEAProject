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
        
        #self.startPos = self.read_pos(self.network.getP())
        
        
        self.totalSprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
 #______________________________________________________________________________________________       
        self.player1 = Player(self,green) # PLAYER 1
        self.totalSprites.add(self.player1)

        self.player2 = Player(self,red)  # PLAYER 2
        self.totalSprites.add(self.player2)
    
#______________________________________________________________________________________________
        for platform in PLATFROM_ARRAY:
            p = Platform(*platform)             # *platform is the same as plafrom[0],plafrom[1],plafrom[2],plafrom[3]
            self.totalSprites.add(p)
            self.platforms.add(p)
       
        self.run()


    def run(self):
        self.run = True
        while self.run:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()


    def events(self):
        info_recv = self.read_pos(self.network.send(self.make_pos((int(self.player1.position.x), int(self.player1.position.y)))))
        
        for reply in info_recv:
            
            player2Pos = self.read_pos(reply[0]) #when you send player1, the network sends player 2 to this client, and viceversa for player2
            self.read_pos(reply[1])
            p = Platform(*reply)             # *platform is the same as plafrom[0],plafrom[1],plafrom[2],plafrom[3]
            self.totalSprites.add(p)
            self.platforms.add(p)

        
        self.player2.position.x = player2Pos[0]
        
        self.player2.position.y = player2Pos[2]
        self.player2.update()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.run:
                    self.run = False
                self.running = False
            if event.type == pg.KEYDOWN:    
                if event.key == pg.K_SPACE:
                    self.player1.jump()
                

    def update(self):
        self.player1.move()
        
        
        if self.player1.velocity.y> 0:  # what this does, is it only checks collisions whilst falling, not whilst jumping
            hits = pg.sprite.spritecollide(self.player1, self.platforms, False)
            if hits:
                self.player1.position.y = hits[0].rect.top
                self.player1.velocity.y = 0

    def draw(self):

        self.screen.fill(white)
        self.totalSprites.draw(self.screen)
        pg.display.update() # updates the whole screen, try to limit the times you update screen as this is the most intensive code. slowing the animation by a lot


    def read_pos(self, str):
        list = []
        str = str.split(",")
        length = len(str)-1
        for i in range(len(str)-1):
            list.append(str[i])
        
        return list #int(str[0]),int(str[1]), int(str[2])


    def make_pos(self, tup):
        string = ""
        for i in range(len(tup)):
            string = string + str(tup[i])+","
     
        #str( str() + "," + str(tup[0]) + "," + str(tup[1]))
       
        return string[:-1]

    

game = Game()
while game.running:
    game.new()

pg.quit()  
