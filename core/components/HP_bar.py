import pygame
from pygame.locals import *

pygame.init()

# Define some colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set screen size
size = (700, 500)
screen = pygame.display.set_mode(size)

# Sprite List
all_sprites_list = pygame.sprite.Group()
HP_Bar_list = pygame.sprite.Group()

# Classes
class HP_BAR(pygame.sprite.Sprite):
    def __init__(self, x_cord, y_cord):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x_cord
        self.rect.y = y_cord
#HP = 70
# Create new HP BAR
def HP_Full(HP, bar_list):
    for i in range(HP):
        Bar = HP_BAR(i * 10, 100)
        bar_list.add(Bar)
