import pygame
import math

pygame.init()

# Set Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 51, 255)
ORANGE = (255, 128, 0)
RED = (255, 0, 0)

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Sets screen
size = (700, 500)
screen = pygame.display.set_mode(size)

# A List of all sprites
all_sprites_list = pygame.sprite.Group()

# Create Classes
class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.hp = 10 * self.level
        self.atk = 5 * self.level

    def level_up(self):
        self.level += 1

class Monster(pygame.sprite.Sprite):
    def __init__(self, hp, atk, s_width, s_length):
        super().__init__()
        self.width = s_width
        self.length = s_length
        self.image_orig = pygame.Surface([self.width, self.length])
        self.image_orig.fill(BLUE)
        self.hp = hp
        self.atk = atk
        self.image = self.image_orig  # Assign the original image to the image attribute
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 200
    def update(self):
        mouse_point = pygame.mouse.get_pos()
        angle_to_pointer = math.atan2(mouse_point[1] - self.rect.centery, mouse_point[0] - self.rect.centerx)
        angle_to_pointer_degrees = math.degrees(angle_to_pointer)
        self.image = pygame.transform.rotate(self.image_orig, -angle_to_pointer_degrees)
        self.rect = self.image.get_rect(center=self.rect.center)

# Make Monster
Plant = Monster(100, 100, 50, 100)
all_sprites_list.add(Plant)

# Main Program Loop
done = False
while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True 

    # Drawing objects on screen
    screen.fill(BLACK)  
    all_sprites_list.draw(screen)
    all_sprites_list.update()
    pygame.display.flip()   
    clock.tick(60)  

pygame.quit()
