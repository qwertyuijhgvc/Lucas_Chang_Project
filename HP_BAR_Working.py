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
HP = 100
# Create new HP BAR
def HP_Full():
    for i in range(HP):
        Bar = HP_BAR(i * 10, 100)
        HP_Bar_list.add(Bar)

# Main Program Loop
done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for sprite in HP_Bar_list:
                sprite.kill()
            #next sprite
            HP = HP - 1
        for i in range(HP):
            Bar = HP_BAR(i * 10, 100)
            HP_Bar_list.add(Bar)

    screen.fill(BLACK)
    all_sprites_list.draw(screen)
    HP_Bar_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
