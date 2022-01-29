import pygame as pg


class Button(pg.sprite.Sprite):
    def __init__(self,x,y,text,colour,size,width,height,Game):
        pg.sprite.Sprite.__init__(self)
        self.pressed = False
        self.image = pg.Surface((width,height))
        self.colour = colour
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        
        
        self.game = Game
        self.text  = text
        #self.top_rect = pg.Rect(pos,(width,height))
        # self.top_colour = '#52de1b'
        
        self.font = pg.font.Font(None,size)
        self.text_surf = self.font.render(self.text,True,(100,43,200)) #this gives all options
        
        self.text_rect = self.text_surf.get_rect()

        

    def draw(self):
        self.rect.center = (self.x,self.y)
        self.text_rect.center = (self.x,self.y)
        pg.draw.rect(self.game.screen,self.colour,self.rect,border_radius= 12)
        self.game.screen.blit(self.text_surf,self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.colour = '#47b51b'
            if pg.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed == True:
                   
                    return True
            
            return False
                    
        else:
            self.colour = '#52de1b'
        
        
            