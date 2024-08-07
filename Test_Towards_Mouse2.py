import pygame
import math

from HP_BAR_Working import HP_BAR, HP_Full
# Initialize Pygame
pygame.init()
hp_bar = HP_BAR(10,100)

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Rotate Sprite towards Mouse")
#Set colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 51, 255)
ORANGE = (255, 128, 0)
RED = (255, 0, 0)
#set positions
middle_left = (100,300)
# Load sprites
sprite_image = pygame.image.load('test_sprite.png')
sprite_rect = sprite_image.get_rect()
sprite_position = sprite_rect.center
projectile_image = pygame.image.load('test_projectile.png').convert()
hero_image = pygame.image.load("CollisionTesterJerry.png").convert()
#Variables
hit = 0
intro_font = pygame.font.SysFont("Arial", 20)
text_font = pygame.font.SysFont("Arial", 10)
finish_font = pygame.font.SysFont("Arial", 100)
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))
#Create Classes
class Projectile(pygame.sprite.Sprite):
    def __init__(self, position, angle):
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
class Hero(pygame.sprite.Sprite):
    def __init__(self, ):
        super().__init__()
        self.image = hero_image
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
class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        self.image = sprite_image
#all sprites list
all_sprites_list = pygame.sprite.Group()
HP_Bar_list = pygame.sprite.Group()
#Create Hero
Jerry = Hero()
all_sprites_list.add(Jerry)
#create HP bar
HP_Full(Jerry.get_hp(),HP_Bar_list)
# Main game loop
running = True
projectiles = pygame.sprite.Group()
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
                projectile = Projectile(sprite_position, angle)
                projectiles.add(projectile)
                Jerry.set_cooldown(0)
        #end if
    for projectile in projectiles:
        projectile_hit_list = pygame.sprite.spritecollide(projectile, all_sprites_list, False)
        for _ in projectile_hit_list:
            projectiles.remove(projectile)
            hit += 1
            Jerry.set_hp(Jerry.get_hp()-1)
        if projectile.get_rect_width() > 800 or projectile.get_rect_height() > 600 or projectile.get_rect_width() < 0 or projectile.get_rect_height() < 0:
            projectiles.remove(projectile)
    for sprite in HP_Bar_list:
            sprite.kill()
        #next sprite
    HP_Full(Jerry.get_hp(), HP_Bar_list)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calculate angle between sprite and mouse
    angle = math.atan2(mouse_y - sprite_position[1], mouse_x - sprite_position[0])
    angle = math.degrees(angle)
    rotated_sprite = pygame.transform.rotate(sprite_image, -angle)
    rotated_rect = rotated_sprite.get_rect(center=sprite_position)

    # Clear screen
    screen.fill(WHITE)
    # Draw rotated sprite
    screen.blit(rotated_sprite, rotated_rect)
    # Update and draw projectiles
    for projectile in projectiles:
        projectile.update()
        screen.blit(projectile.image, projectile.rect.topleft)
    #next projectile
    #draw sprites
    all_sprites_list.draw(screen)
    HP_Bar_list.draw(screen)
    draw_text(str(hit), text_font, BLACK, 650, 475)
    draw_text(str(Jerry.get_cooldown()), text_font, BLACK, 650, 275)
    draw_text(str(Jerry.get_hp()), text_font, BLACK, 650, 75)
    # Update display
    pygame.display.flip()
    # Cap the frame rate
    pygame.time.Clock().tick(60)
    
    #increase cooldown value
    Jerry.set_cooldown(Jerry.get_cooldown()+1)

# Quit Pygame
pygame.quit()
