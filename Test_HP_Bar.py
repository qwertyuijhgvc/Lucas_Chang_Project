import pygame
import random
from pygame.locals import *
from pygame import mixer
pygame.init()
mixer.init()
# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 153,   0,   0)
BLUE    =   (0,   0, 255)
YELLOW = (255, 255, 0)
BROWN = (102, 51, 0)
LIGHT_BROWN = (153, 76, 0)
DORITO_YELLOW = (250,133,19)
# Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
#Sets screen
size = (700, 500)
screen = pygame.display.set_mode(size)
# Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
#Sprite List
all_sprites_list = pygame.sprite.Group()
#Classes
class HP_BAR(pygame.sprite.Sprite):
    def __init__(self,x_cord,y_cord):
        super().__init__()
        self.image = pygame.Surface([10,10])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x_cord
        self.rect.y = y_cord
    #end function
#end class
#Variables
HP = 100
time = 0
keys = pygame.key.get_pressed()
#functions/procedures
#Create new HP BAR
def HP_FUll():
    for i in range(HP):
        Bar = HP_BAR(0+i*10, 100)
        all_sprites_list.add(Bar)
    #next i
#end procedure
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
    # --- Game logic should go here
    #Increments time variable so intro text disappears after a certian amount of time
    time += 1
    #next i
    if event.type == pygame.MOUSEBUTTONDOWN:
        HP -= 1
    #end if
    
    #end if
    # Drawing objects on screen
    screen.fill(BLACK)  
    all_sprites_list.draw(screen)
    all_sprites_list.update()
    pygame.display.flip()   
    clock.tick(60)  
pygame.quit()