import pygame
pygame.init()

class Hero(pygame.sprite.Sprite):
    def __init__(self):
        self.level = 1
        self.hp = 10 * self.level
        self.atk = 5 * self.level
    
        