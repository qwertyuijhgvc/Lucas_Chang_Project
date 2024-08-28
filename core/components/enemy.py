import pygame
import math
# Initialize Pygame
pygame.init()
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_image):
        super().__init__()
        self.image = enemy_image
        self.level = 1
        self.hp = 10 * self.level
        self.atk = 5 * self.level
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 300
        self.shield_HP = 5
        self.projectile_cooldown = 1
    #end constructor
    def level_up(self):
        self.level = self.level +1
    def get_cooldown(self):
        return self.projectile_cooldown
    def set_cooldown(self,cooldown):
        self.projectile_cooldown = cooldown
    def get_hp(self):
        return self.hp
    def set_hp(self, HP):
        self.hp = HP
    #end procedure
#end class