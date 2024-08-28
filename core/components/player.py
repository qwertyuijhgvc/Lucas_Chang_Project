import pygame
import math
# Initialize Pygame
pygame.init()
class Player(pygame.sprite.Sprite):
    def __init__(self,sprite_image):
        super().__init__()
        self.image = sprite_image
        self.rect = self.image.get_rect()
        self.position = self.rect.center
        
        self.screen = pygame.display.get_surface()
    #end constructor
    def calculate_angle(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Calculate angle between sprite and mouse
        angle = math.atan2(mouse_y - self.position[1], mouse_x - self.position[0])
        angle = math.degrees(angle)
        return angle
    #end function
    def update(self):
        angle = self.calculate_angle()
        rotated_sprite = pygame.transform.rotate(self.image, -angle)
        self.rect = rotated_sprite.get_rect(center=self.position)
        self.screen.blit(rotated_sprite,self.rect)
    #end procedure
