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
#load sprites
projectile_image = pygame.image.load('resources/Test_Projectile.png')
sprite_image = pygame.image.load('resources/test_sprite.png')
enemy_image = pygame.image.load('resources/CollisionTesterJerry.png')
# create obkects
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
#variables
hit = 0

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #end if
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            cooldown = Jerry.get_cooldown()
            if cooldown > 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.atan2(mouse_y - sprite_position[1], mouse_x - sprite_position[0])
                angle = math.degrees(angle)
                projectile = Projectile(sprite_position, angle, projectile_image)
                projectile_list.add(projectile)
                Jerry.set_cooldown(0)
        #end if
    for projectile in projectile_list:
        projectile_hit_list = pygame.sprite.spritecollide(projectile, all_sprites_list, False)
        for _ in projectile_hit_list:
            projectile_list.remove(projectile)
            hit += 1
            Jerry.set_hp(Jerry.get_hp()-1)
        if projectile.get_rect_width() > 800 or projectile.get_rect_height() > 600 or projectile.get_rect_width() < 0 or projectile.get_rect_height() < 0:
            projectile_list.remove(projectile)

        
    # Update display
    screen.fill(WHITE)
    projectile_list.draw(screen)
    all_sprites_list.draw(screen)
    all_sprites_list.update()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pokemon.update()
    print(pokemon.get_position())
    pygame.display.flip()
    # Cap the frame rate
    pygame.time.Clock().tick(60)
    #increase cooldown value
# Quit Pygame
pygame.quit()