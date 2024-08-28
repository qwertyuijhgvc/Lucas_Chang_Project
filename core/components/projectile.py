import pygame
import math
# Initialize Pygame
pygame.init()

class Projectile(pygame.sprite.Sprite):
    def __init__(self, position, angle, projectile_image):
        super().__init__()
        self.image = projectile_image
        self.rect = self.image.get_rect(center=position)
        self.speed = 5
        self.angle = angle
    #end constructor function
    def update(self):
        self.rect.x += self.speed * math.cos(math.radians(self.angle))
        self.rect.y += self.speed * math.sin(math.radians(self.angle))
    #end procedure
    def get_rect_width(self):
        return self.rect.x
    #end function
    def get_rect_height(self):
        return self.rect.y
    #end function
#end class