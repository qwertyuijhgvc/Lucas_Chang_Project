import pygame
import math
import random

from HP_BAR_Working import HP_BAR, HP_Full

# Initialize Pygame
pygame.init()
hp_bar = HP_BAR(10, 100)

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("GAME")

# Set colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 51, 255)
ORANGE = (255, 128, 0)
RED = (255, 0, 0)

# Set positions
middle_left = (100, 300)

# Load sprites
#Used to create sprite for player character
#note to self to change player sprite whole 3 pieces of code will be needed
sprite_image = pygame.image.load('resources/test_sprite.png')
sprite_rect = sprite_image.get_rect()
sprite_position = sprite_rect.center
#Sprite for projectile
projectile_image = pygame.image.load('resources/test_projectile.png').convert()
#sprite for enemy
enemy_hero_image = pygame.image.load("resources/CollisionTesterJerry.png").convert()
#rescale enemy size
rescale_size = (100,100)
enemy_hero_image = pygame.transform.scale(enemy_hero_image, rescale_size)
#Variables
pause = False
#test variables
hit = 0
dodge_times = 0
Player_HP = 100
#fonts
intro_font = pygame.font.SysFont("Arial", 20)
text_font = pygame.font.SysFont("Arial", 10)
finish_font = pygame.font.SysFont("Arial", 50)
#creating procedure to write text on screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
#end procedure

# Create Classes
#class for all projectiles
class Projectile(pygame.sprite.Sprite):
    def __init__(self, position, angle, type):
        super().__init__()
        self.type = type
        self.gravity = False
        self.image = projectile_image
        self.cooldown = 0
        if self.type == "normal": 
            self.image = projectile_image
            self.rect = self.image.get_rect(center=position)
            self.speed = 5
        elif self.type == "poison":
            #self.image = poison_projectile.image
            self.rect = self.image.get_rect(center=position)
            self.speed = 3
            self.cooldown = -120
        elif self.type == "heavy":
            #self.image = heavy_projectile.image
            self.rect = self.image.get_rect(center=position)
            self.speed = 2
            self.gravity = True
            self.cooldown = -120
        elif self.type == "stun":
            #self.image = stun_projectile.image
            self.rect = self.image.get_rect(center=position)
            self.speed = 5
            self.cooldown = -240
        #end if
        self.angle = angle
    # end constructor function
    def update(self):
        self.rect.x += self.speed * math.cos(math.radians(self.angle))
        self.rect.y += self.speed * math.sin(math.radians(self.angle))
        if self.gravity == True:
            self.rect.y += 1
    # end procedure
    def get_rect_width(self):
        return self.rect.x
    # end function
    def get_rect_height(self):
        return self.rect.y
    # end function
    def get_type(self):
        return self.type
    #end function
    def get_cooldown(self):
        return self.cooldown
    #end function
# end class

class Enemy_Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_hero_image
        self.level = 1
        self.hp = 10
        self.atk = 1
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 300
        self.dodge = 1
        self.projectile_cooldown = 1
        self.speed = 2
        self.old_speed = self.speed
        self.stun_timer = 0
        self.poison_timer = -1
        self.knockback_timer = 0
        self.player_HP = 5
    # end constructor
    def level_up(self):
        self.level += 1
        self.speed = 1 + self.old_speed
        self.old_speed = self.speed
        self.hp = 10 * self.level
        self.atk = 5 * self.level
        self.dodge += 0.2
        self.rect.x = 700
        self.rect.y = 500
        self.stun_timer = 0
        self.poison_timer = -1
        self.knockback_timer = 0
    def get_cooldown(self):
        return self.projectile_cooldown
    #end function
    def set_cooldown(self, cooldown):
        self.projectile_cooldown = cooldown
    #end procedure
    def get_hp(self):
        return self.hp
    #end function
    def set_hp(self, HP):
        self.hp = HP
    #end procedure
    def get_dodge(self):
        return self.dodge
    # end function
    def get_rect_x(self):
        return self.rect.x
    #end function
    def get_rect_y(self):
        return self.rect.y
    #end function
    def get_player_HP(self):
        return self.player_HP
    def stun(self):
        #self.image = stun.image
        self.stun_timer = 120
    #end procedure
    def poison(self):
        #self.image = poison.image
        self.poison_timer = 301
    #end procedure
    def knockback(self,time):
        self.knockback_timer = time
    #end procedure
    def update(self,distance_x, distance_y):
        if self.poison_timer % 60 == 0:
            #self.image = poisoned.image
            self.hp -= 1
        #end if
        if self.poison_timer > -1:
            self.poison_timer -=1
        #end if
        if self.stun_timer > 0:
            #self.image = stunned.image
            self.speed = 0
            self.stun_timer -=1
        #end if
        if self.stun_timer == 0:
            self.speed = self.old_speed
        if self.knockback_timer > 0:
            #self.image = knockback.image
            self.speed = self.speed * -1
            self.knockback_timer -= 1 
        distance = ((distance_x) ** 2 + (distance_y) ** 2) **0.5
        #end if
        if distance > 10:
            self.rect.x += self.speed * distance_x / distance
            self.rect.y += self.speed * distance_y / distance
        #end if
        elif distance <= 10:
            #self.image = attack.image
            self.rect.x += -self.speed * distance_x / distance
            self.rect.y += -self.speed * distance_y / distance
            self.player_HP -= self.atk
            self.knockback(60)
    #end procedure
    
# end class

class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_image):
        self.image = sprite_image
        self.HP = 100
#end class
#Projectile fire
def projectile_fire(type):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    angle = math.atan2(mouse_y - sprite_position[1], mouse_x - sprite_position[0])
    angle = math.degrees(angle)
    projectile = Projectile(sprite_position, angle, type)
    projectiles.add(projectile)
    Jerry.set_cooldown(projectile.get_cooldown())
# All sprites list
all_sprites_list = pygame.sprite.Group()
HP_Bar_list = pygame.sprite.Group()

# Create Enemy_Hero
Jerry = Enemy_Hero()
all_sprites_list.add(Jerry)

# Create HP bar
HP_Full(Jerry.get_hp(), HP_Bar_list)

# Main game loop
running = True
projectiles = pygame.sprite.Group()
while running:
    keys = pygame.key.get_pressed()
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # end if
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            cooldown = Jerry.get_cooldown()
            if cooldown > 1:
                projectile_fire("normal")
            #end if
        elif keys[pygame.K_1]:
            cooldown = Jerry.get_cooldown()
            if cooldown > 1:
                projectile_fire("poison")
        elif keys[pygame.K_2]:
            cooldown = Jerry.get_cooldown()
            if cooldown > 1:
                projectile_fire("heavy")        
        elif keys[pygame.K_3]:
            cooldown = Jerry.get_cooldown()
            if cooldown > 1:
                projectile_fire("stun")        
        # end if
    for projectile in projectiles:
        projectile_hit_list = pygame.sprite.spritecollide(projectile, all_sprites_list, False)
        for _ in projectile_hit_list:
            projectiles.remove(projectile)
            hit += 1
            dodge_check = random.randrange(0, 100)
            if dodge_check >= Jerry.get_dodge():
                if projectile.get_type() == "normal":
                    Jerry.set_hp(Jerry.get_hp() - 1)
                elif projectile.get_type() == "heavy": 
                    Jerry.set_hp(Jerry.get_hp() - 2)
                    #Jerry knockback
                    Jerry.knockback(60)
                elif projectile.get_type() == "poison":
                    Jerry.poison()
                elif projectile.get_type() == "stun":
                    Jerry.stun()
                #end if
            else:
                dodge_times += 1
        if projectile.get_rect_width() > 800 or projectile.get_rect_height() > 600 or projectile.get_rect_width() < 0 or projectile.get_rect_height() < 0:
            projectiles.remove(projectile)
    for sprite in HP_Bar_list:
        sprite.kill()
        # next sprite
    HP_Full(Jerry.get_hp(), HP_Bar_list)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Calculate angle between sprite and mouse
    if keys[pygame.K_a]:
        sprite_position = (sprite_position[0] - 5, sprite_position[1])
    if keys[pygame.K_d]:
        sprite_position = (sprite_position[0] + 5, sprite_position[1])
    if keys[pygame.K_w]:
        sprite_position = (sprite_position[0], sprite_position[1] - 5)
    if keys[pygame.K_s]:
        sprite_position = (sprite_position[0], sprite_position[1] + 5)
    #Sprite change test
    if keys[pygame.K_q]:
        sprite_image = pygame.image.load('resources/CollisionTesterJerry.png')
        sprite_rect = sprite_image.get_rect()
        sprite_position = sprite_rect.center
    #end if
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
    # next projectile
    #update Jerry position to move towards player
    distance_x = int(sprite_position[0]) - Jerry.get_rect_x()
    distance_y = int(sprite_position[1]) - Jerry.get_rect_y()
    Jerry.update(distance_x, distance_y)
    #update Jerry status effect timers
    # draw sprites
    all_sprites_list.draw(screen)
    HP_Bar_list.draw(screen)
    # test to check if hit works
    draw_text(str(hit), text_font, BLACK, 650, 475)
    # test to check if dodge works
    draw_text(str(dodge_times), text_font, BLACK, 650, 375)
    # test to check if cooldown works
    draw_text(str(Jerry.get_cooldown()), text_font, BLACK, 650, 275)
    # test to check if hp works
    draw_text(str(Jerry.get_hp()), text_font, BLACK, 650, 75)
    # What to do once you beat enemy
    if Jerry.get_hp() <= 0:
        # To remove projectiles so they don't stay around next level
        for projectile in projectiles:
            projectiles.remove(projectile)
        # next projectile
        # Next level screen
        screen.fill(WHITE)
        draw_text(str("You beat the stage!"), finish_font, BLACK, 200, 250)
        pygame.display.flip()
        # give time for player to read
        pygame.time.delay(600)
        screen.fill(WHITE)
        draw_text(str("Next stage"), finish_font, BLACK, 300, 250)
        pygame.display.flip()
        pygame.time.delay(600)
        # Make enemy stronger for next level
        Jerry.level_up()
        #reset pos
        sprite_position = (100,100)
        # positions
    #end if
    if Jerry.get_player_HP() == 0:
        screen.fill(WHITE)
        draw_text(str("YOU LOSE"), finish_font, BLACK, 300, 250)
    #end if       
    # Update display
    pygame.display.flip()
    # Cap the frame rate
    pygame.time.Clock().tick(60)
    # Increase cooldown value
    Jerry.set_cooldown(Jerry.get_cooldown() + 1)

# Quit Pygame
pygame.quit()
