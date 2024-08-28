#imports
import pygame
import math
import sys
sys.path.append('/Users/lucaschang/Documents/GitHub/Lucas_Chang_Project/core')
sys.path.append('../')
from components import Player
from components import Enemy
from components import HP_BAR, HP_Full
from components import Projectile


#screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#Set colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 51, 255)
ORANGE = (255, 128, 0)
RED = (255, 0, 0)
# Initialize Pygame
pygame.init()
projectile_image = pygame.image.load('resources/Test_Projectile.png')
sprite_image = pygame.image.load('resources/test_sprite.png')
enemy_image = pygame.image.load('resources/CollisionTesterJerry.png')
sprite_rect = sprite_image.get_rect()
sprite_position = sprite_rect.center
mouse_x, mouse_y = pygame.mouse.get_pos()
angle = math.atan2(mouse_y - sprite_position[1], mouse_x - sprite_position[0])
angle = math.degrees(angle)
bullet = Projectile(sprite_position, angle, projectile_image)
Jerry = Enemy(enemy_image)
pokemon = Player(sprite_image)
projectile_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
projectile_list.add(bullet)
#all_sprites_list.add(pokemon)


# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #end if
        
        
    # Update display
    screen.fill(WHITE)
    projectile_list.draw(screen)
    all_sprites_list.draw(screen)
    all_sprites_list.update()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pokemon.update()
    
    pygame.draw.rect(screen, ORANGE, [0, SCREEN_HEIGHT - 200,SCREEN_WIDTH, 200] )
    pygame.display.flip()
    # Cap the frame rate
    pygame.time.Clock().tick(60)
    #increase cooldown value
# Quit Pygame
pygame.quit()