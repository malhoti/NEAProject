import pygame as pg
import socket

from pygame import time
from platforms import Platform
from network import Network
from player import Player
import pickle
from settings import *
import time



class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((screen_width, screen_height))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        self.running = True
        self.send_more_platforms = False
        


    def new(self):
        self.network = Network()
        
        self.starting_info = self.network.getP() # get the information sent from the server

        playersPos = self.starting_info[0]
        player1Pos = playersPos[0]
        player2Pos = playersPos[1]
        
        platformPos = self.starting_info[1]

        self.totalSprites = pg.sprite.Group() # making sprite groups 
        self.platforms = pg.sprite.Group()
     
        self.player1 = Player(player1Pos[0],player1Pos[1],self,green) # PLAYER 1
        self.totalSprites.add(self.player1)

        self.player2 = Player(player2Pos[0],player2Pos[1],self,red)  
        self.totalSprites.add(self.player2)
    

        for i in range(len(platformPos)):

            p = Platform(*platformPos[i])       # *platformPos[i] is the same as plafrom[0],plafrom[1],plafrom[2],plafrom[3]
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
        
        info_recv = self.network.send(([int(self.player1.position.x), int(self.player1.position.y),self.player1.pushdown],self.send_more_platforms))  #when you send player1, the network sends player 2 to this client, and viceversa for player2 
        
        self.send_more_platforms = False
        player2Pos = info_recv[0]
        self.player2.position.x = player2Pos[0]
        self.player2.position.y = player2Pos[1] +(self.player1.pushdown-player2Pos[2])
        

        
        self.player2.update()
    
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.run:
                    self.run = False
                self.running = False
            if event.type == pg.KEYDOWN:    
               if event.key == pg.K_SPACE:
                  
                   self.player1.jump()
        
       
        
        #for platform in self.platforms:
            # platform.rect.y += 1
       


    def update(self):
        self.player1.move()
        
        # what this does, is it only checks collisions whilst falling, not whilst jumping
        if self.player1.velocity.y>= 0 :  
            hits = pg.sprite.spritecollide(self.player1, self.platforms, False)
            if hits :
                if self.player1.position.y < hits[0].rect.bottom:
                    self.player1.position.y = hits[0].rect.top
                    self.player1.velocity.y = 0

        #this is going to act like a camera shift when the player reaches around the top of the screen
        #and delete platforms that go off the screen

        if self.player1.rect.top <= screen_height/4:
            self.player1.pushdown +=  round(abs(self.player1.velocity.y))
            self.player1.position.y += round(abs(self.player1.velocity.y))
           
            for platform in self.platforms:
                platform.rect.y += round(abs(self.player1.velocity.y))

                if platform.rect.top >= screen_height:#+(screen_height/4):
                    platform.kill()
            
        # make new platforms 
        #while len(self.platforms)>10:
         #   self.send_more_platforms = True
        
        
    def draw(self):
        
        self.screen.fill(white)
       
        self.totalSprites.draw(self.screen)
        pg.display.update() # updates the whole screen, try to limit the times you update screen as this is the most intensive code. slowing the animation by a lot



game = Game()
while game.running:
    game.new()

pg.quit()  
