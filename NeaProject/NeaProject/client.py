from platform import platform
import pygame as pg
import socket

from pygame import time
from platforms import Platform, Spike
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
        self.font_name = pg.font.match_font(font)
        self.p2ready = False
        self.player1lost = False
        self.player2lost = False


    def new(self):
        
        self.network = Network()
        self.starting_info = self.network.getP() # get the information sent from the server
        self.player = self.starting_info[0]
        # self.starting_info = self.network.getP() # get the information sent from the server
        # self.player = self.starting_info[0]
        # playersPos = self.starting_info[0]
        # player1Pos = playersPos[0]
        # player2Pos = playersPos[1]
        print("You are player", int(self.player) +1)
        if int(self.player) == 0:
            self.player1 = Player(40,screen_height-100,self,green)
            self.player2 = Player(0,screen_height+100,self,red)
        else:
            self.player1 = Player(screen_width-40,(7*screen_height)/8,self,red)
            self.player2 = Player(40,screen_height-100,self,green)

        
        platformPos = self.starting_info[1]

        self.totalSprites = pg.sprite.Group() # making sprite groups 
        self.platforms = pg.sprite.Group()
        self.spikes = pg.sprite.Group()
        

        self.spike = Spike(0,screen_height+200,screen_width,screen_height)
        self.totalSprites.add(self.player1)
        self.totalSprites.add(self.player2)
        self.totalSprites.add(self.spike)
         
        
        self.spikes.add(self.spike)

        self.score = 0
        

        for i in range(len(platformPos)):

            p = Platform(*platformPos[i])       # *platformPos[i] is the same as plafrom[0],plafrom[1],plafrom[2],plafrom[3]
            self.totalSprites.add(p)
            self.platforms.add(p)
        
        self.run()





    def run(self):
        self.run1 = True
        while self.run1:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()


    def events(self):

        # Checks if anyone has won or lost first, this is so that if it is the case, then the client can send one last message to the server to let it know that this client lost or won
        if self.player1.rect.bottom >= self.spike.rect.top:
            print("you lost")
            self.player1lost = True
            

        if self.player2lost:
            self.show_victory_screen()
            self.totalSprites.empty()
            


        self.info_to_send=[int(self.player1.position.x), int(self.player1.position.y),self.player1.pushdown,True,self.player1lost],self.send_more_platforms
        
        info_recv = self.network.send((self.info_to_send))  #when you send player1, the network sends player 2 to this client, and viceversa for player2 
        
        self.send_more_platforms = False
        
        if not self.p2ready:
            
            self.show_lobby()


        player2Pos = info_recv[0]
       
        self.player2.position.x = player2Pos[0]
        self.player2.position.y = player2Pos[1] +(self.player1.pushdown-player2Pos[2])
        self.p2ready = player2Pos[3]
        platformPos = info_recv[1]
        self.player2lost = player2Pos[4]

        for i in range(len(platformPos)):
            
            if not platformPos[i]:
                pass
            else:
                p = Platform(platformPos[i][0],platformPos[i][1],platformPos[i][2],platformPos[i][3])       # *platformPos[i] is the same as plafrom[0],plafrom[1],plafrom[2],plafrom[3]
                self.totalSprites.add(p)
                self.platforms.add(p)
        
        self.player2.update()

        if self.player1lost:
            self.show_go_screen()
            
    
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
        
        # what this does, is it only checks collisions whilst falling, not whilst jumping
        if self.player1.velocity.y>= 0 :  
            hits = pg.sprite.spritecollide(self.player1, self.platforms, False)
            if hits :
                if self.player1.position.y < hits[0].rect.bottom:
                    self.player1.position.y = hits[0].rect.top
                    self.player1.velocity.y = 0

        # the spike will slowly get faster and faster!!
        for spike in self.spikes:
            spike.rect.y -= (1)

        #this is going to act like a camera shift when the player reaches around the top of the screen
        #and delete platforms that go off the screen

        #going up
        
        if self.player1.rect.top <= screen_height/4:
            self.player1.pushdown +=  round(abs(self.player1.velocity.y))
            self.player1.position.y += round(abs(self.player1.velocity.y))
            
            for spike in self.spikes:
                spike.rect.y +=  round(abs(self.player1.velocity.y)) 
           
            for platform in self.platforms:
                platform.rect.y += round(abs(self.player1.velocity.y))

               
        hits = pg.sprite.pygame.sprite.spritecollide(spike, self.platforms, False)
        if hits:
            if self.spike.rect.top<hits[0].rect.top:
                hits[0].kill()
                self.score += 1

        # going down

        if self.player1.rect.bottom >(7*screen_height)/8:
            self.player1.pushdown -= round(abs(self.player1.velocity.y))
            self.player1.position.y -= round(abs(self.player1.velocity.y))
            
            for spike in self.spikes:
                spike.rect.y -=  round(abs(self.player1.velocity.y)) 
           
            for platform in self.platforms:
                platform.rect.y -= round(abs(self.player1.velocity.y))
        
        # make new platforms 

        # this checks wether if there is a platform 1/8 above the screen, if there arent make a new platform, if there are above the 1/8 of screen dont send more platforms
        empty_above = False
        count = 0
        for platform in self.platforms:
            
            if platform.rect.y <screen_height/8 : 
                count += 1

       
        if count  == 0:
            empty_above = True

        
        while self.player1.rect.y <screen_height/4 and empty_above: #and len(self.platforms) <10:
            self.send_more_platforms = True
            break
        
        # while len(self.platforms)<10 and not(self.player1.falling):
        #     self.send_more_platforms = True
        #     break
        
    def show_menu(self):
        self.screen.fill(bgcolour)
        self.draw_text(TITLE, 48 , black,screen_width/2,screen_height/4)
        self.draw_text("press a key",56,red,screen_width/2,screen_height/2)
        pg.display.flip()
        self.wait_for_key()

    def show_lobby(self):
        self.screen.fill(bgcolour)
        self.draw_text("WAITING IN LOBBY...",70,black,screen_width/2,screen_height/2)
        pg.display.flip()
        self.wait_for_player2()
        

    def wait_for_player2(self):
         
        waiting = True
        while waiting:
            info_recv = self.network.send((self.info_to_send))
            print(info_recv)
            self.clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.run = False
                if info_recv[0][3]:
                    waiting = False
            

    def show_go_screen(self):   
        self.screen.fill(red)
        self.draw_text("YOU LOST", 70, black,screen_width/2,screen_height/4)
        

        self.draw_text("Press a key...",16,black,screen_width/2,screen_height/2)
        
        pg.display.flip()
        self.wait_for_key()
        self.run1 = False
        

    def show_victory_screen(self):
        self.screen.fill(green)
        self.draw_text("YOU WON", 70, black,screen_width/2,screen_height/4)
        self.draw_text("Press a key...",16,black,screen_width/2,screen_height/2)
        
        pg.display.flip()
        self.wait_for_key()
        self.run1 = False
        
        

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.run = False
                if event.type == pg.KEYUP:
                    waiting = False

    
   
    def draw(self):
        
        self.screen.fill(white)
        self.totalSprites.draw(self.screen)
        self.spike.draw(self.screen)
        self.draw_text(str(self.score), 22, red,screen_width-50,30)
        pg.display.update() # updates the whole screen, try to limit the times you update screen as this is the most intensive code. slowing the animation by a lot

    def draw_text(self, text, size, colour, x,y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect=text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)


while True:
    game = Game()
    print("yo")
    game.show_menu()

    game.new()

pg.quit()  