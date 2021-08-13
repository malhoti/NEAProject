import pygame
from settings import *
vec = pygame.math.Vector2 # vectors for easier handling when creating positions

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, colour):
        pygame.sprite.Sprite.__init__(self)
        
        self.width = width
        self.height = height
        self.colour = colour
        self.rect = (x, y, width, height)

        self.position = vec(width/2,height/2)

        self.velocity = vec(0,0)
        self.acceleration = vec(0,0)
        
        
        self.jump_velocity = PLAYER_jumpvelocity
        self.isJump = False
        
        
        self.mass = 1
        self.turning_point = 1

    def draw(self, window):
        pygame.draw.rect(window, self.colour, self.rect)

    def move(self):
        self.acceleration = vec(0,PLAYER_gravity) # id keys arent being pressed put acceleration to 0 as its not moving
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.acceleration.x = -PLAYER_acceleration
        if keys[pygame.K_RIGHT]:
            self.acceleration.x = PLAYER_acceleration

        self.acceleration.x += self.velocity.x * PLAYER_friction
        self.velocity += self.acceleration
        self.position += self.acceleration*0.5  + self.velocity
        
        
       
        # if not (self.isJump): # this is so that you can only move left and right when jumping
        #     if keys[pygame.K_UP] and self.y >0:
        #         self.y -= self.velocity
        #     if keys[pygame.K_DOWN] and self.y < (screen.height-self.height):
        #         self.y += self.velocity

        if keys[pygame.K_SPACE]:
            self.isJump = True
            
        if self.isJump:
            self.jump()
             
       
        if self.position.x > screen_width:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = screen_width
        self.update()

    def jump(self):
        
        force = ((1/2)*self.mass*((self.jump_velocity*2.5)**2))*self.turning_point
        print(force)
        self.position.y -= force

        self.jump_velocity -= 0.2

        if self.jump_velocity < 0:
            self.turning_point=-1

        if self.velocity <= (self.velocity*-1)-0.2:
            self.isJump = False

            self.turning_point=1

            self.temp_velocity = self.velocity
        
        
        


    
    def update(self):

        self.rect = (self.position.x,self.position.y, self.width, self.height)