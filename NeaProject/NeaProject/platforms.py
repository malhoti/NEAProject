import pygame 
from settings import *


class Platform(pygame.sprite.Sprite):
    def __init__(self,types,x,y,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(blue)
        self.colour = blue
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.types = types

    def draw(self, window):
        pygame.draw.rect(window, self.colour, self.rect)
