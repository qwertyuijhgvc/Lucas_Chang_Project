import pygame
pygame.init()
import math
#Set Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0,   0, 255)
PINK = (255,51,255)
ORANGE = (255,128,0)
RED = (255,0,0)
# Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
#Sets screen
size = (700, 500)
screen = pygame.display.set_mode(size)
#Set variables
mouse_point = pygame.mouse.get_pos()
mouse_point = list(mouse_point)
#A List of all sprites
all_sprites_list = pygame.sprite.Group()
#Create Classes
class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.hp = 10 * self.level
        self.atk = 5 * self.level
    #end constructor
    def level_up(self):
        self.level = self.level +1
    #end procedure
#end class
class Monster(pygame.sprite.Sprite):
    def __init__(self,hp,atk,s_width,s_length):
        super().__init__()
        self.width = s_width
        self.length = s_length
        self.image = pygame.Surface([self.width,self.length])
        self.image.fill(BLUE)
        self.hp = hp
        self.atk = atk
        self.rect = self.image.get_rect()
    #end constructor
    def update(self):
        old_center = self.rect.center
        angle_to_pointer = math.degrees(math.atan2(self.length/2 - mouse_point[1], self.width/2 - mouse_point[0]))+180
        self.image = pygame.transform.rotate(self.image, angle_to_pointer)
        self.rect = self.image.get_rect()
        self.rect.center = old_center
#Make Monster
Plant = Monster(100,100,100,100)
all_sprites_list.add(Plant)
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop


               
    #Drawing objects on screen       
    screen.fill(BLACK)  
    all_sprites_list.draw(screen)
    all_sprites_list.update()
    pygame.display.flip()   
    clock.tick(60)  
pygame.quit