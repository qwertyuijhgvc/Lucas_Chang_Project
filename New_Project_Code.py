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
projectile_image = pygame.image.load('resources/test_projectile.png')
#sprite for enemy
enemy_hero_image = pygame.image.load("resources/CollisionTesterJerry.png")
#rescale enemy size
rescale_size = (100,100)
enemy_hero_image = pygame.transform.scale(enemy_hero_image, rescale_size)
#Variables
pause = True
levelSelect = False
bossSelect = False
controlScreen = False
playerBoss = ""
usr_txt = ""
menu = ""
mouse_x = 0
mouse_y = 0
leftClickSymbol = pygame.image.load("resources/left_click.png")
leftClickSymbol = pygame.transform.scale(leftClickSymbol, (100,100))
#test variables
hit = 0
dodge_times = 0
Player_HP = 100
#fonts
small_font = pygame.font.SysFont("Arial", 15)
usr_font = pygame.font.SysFont("Arial", 20)
text_font = pygame.font.SysFont("Arial", 30)
menu_font = pygame.font.SysFont("Arial", 60)
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
        elif self.type == "bubble":
            #self.image = bubble_projectile.image
            self.rect = self.image.get_rect(center=position)
            self.speed = 0
            self.cooldown = -100
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
    #end procedure
    def set_speed(self,speed):
        self.speed = speed
    #end procedure
    def set_level(self,level):
        self.level = level
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
    #end procedure
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
        #end if
        distance = ((distance_x) ** 2 + (distance_y) ** 2) **0.5
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
#Create level selection
def Level_Select(enemyLevel, bossChosen, Enemy):
    Enemy.set_level(enemyLevel) 
    #if bossChosen == "Plant":
        #sprite_image = pygame.image.load('resources/Plant_Boss_Head.png')
        #Background_image = pygame.image.load('resources/Forest.png')
        #
    #end if
#end procedure
def toggle(boolean):
    if boolean == True:
        return False
    else:
        return True
#end function
# Main game loop
#menu = "Boss Control 1"
running = True
projectiles = pygame.sprite.Group()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # end if
    #next event
    #variable for key presses
        keys = pygame.key.get_pressed()
        #to pause and unpause the game
        if menu == "":
            if keys[pygame.K_ESCAPE]:
                pause = toggle(pause)
            #end if
        else:
            if keys[pygame.K_ESCAPE]:
                menu = ""
            #end if
        #end if
        #for entering text while in pause screen
        if pause == True:
            #check if player is typing
            if event.type == pygame.KEYDOWN:
                # Check for backspace
                if event.key == pygame.K_BACKSPACE:
                    usr_txt = usr_txt[:-1]
                #check if player is entering the level
                elif event.key == pygame.K_RETURN:
                    #check if player inputted valid input
                    try:
                        Jerry.set_level(int(usr_txt))
                        usr_txt = ""
                        screen.fill(WHITE)
                    except:
                        usr_txt = ""
                        screen.fill(WHITE)
                    #end try
                #add the inputted text to a string variable
                else:
                    usr_txt += event.unicode
                    #end if
            #end if
    #check if game is paused
    if pause == True:
        #pause the game
        screen.fill(WHITE)
        Jerry.set_speed(0)
        for projectile in projectiles:
            projectiles.remove(projectile)
        #next projectile
        #check if player is clicking on screen
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            #get position of mouse
            mouse_x, mouse_y = pygame.mouse.get_pos()
        #end if
        #Drawing UI elements on screen
        pygame.draw.ellipse(screen, BLACK, (50,250,200,100), 3)
        pygame.draw.ellipse(screen, BLACK, (300,250,200,100), 3)
        pygame.draw.ellipse(screen, BLACK, (550,250,200,100), 3)
        #drawing text box and user text
        pygame.draw.rect(screen, BLACK, [70,360,175,50])
        pygame.draw.rect(screen, WHITE, [80,370,155,30])
        draw_text(usr_txt, usr_font, BLACK, 100, 375)
        draw_text("Main Menu", menu_font, BLACK, 200, 100)
        draw_text("Level", text_font, BLACK, 115, 285)
        draw_text("Boss Select", text_font, BLACK, 320, 285)
        draw_text("Controls", text_font, BLACK, 590, 285)
        #Creating variable for differnet pause screens
        #If statement to change menu value
        if menu == "": 
            if mouse_x > 300 and mouse_x < 500 and mouse_y > 250 and mouse_y < 350:
                menu = "Boss Select"
            elif mouse_x > 550 and mouse_x < 650 and mouse_y > 250 and mouse_y < 350:
                menu = "Controls"
            #end if
        #end if
        #If statement in order to travel between different menu screens
        if menu == "Boss Select":
            screen.fill(WHITE)
            pygame.draw.ellipse(screen, BLACK, (100,250,200,100), 3)
            pygame.draw.ellipse(screen, BLACK, (500,250,200,100), 3)
            #creates a button to go back to main menu
            pygame.draw.ellipse(screen, BLACK, (10,10,50,50), 2)
            draw_text("Back", small_font, BLACK, 20, 25)
            draw_text("Boss Select", menu_font, BLACK, 225, 100)
            draw_text("Boss 1", text_font, BLACK, 150, 275)
            draw_text("Boss 2", text_font, BLACK, 550, 275)
            if mouse_x > 0 and mouse_x < 60 and mouse_y > 0 and mouse_y < 60:
                menu = ""
            elif mouse_x > 100 and mouse_x < 300 and mouse_y > 250 and mouse_y < 350:
                playerBoss = "Fish Boss"
                menu = ""
                toggle(pause)
            elif mouse_x > 500 and mouse_x < 700 and mouse_y > 250 and mouse_y < 350:
                playerBoss = "Plant Boss Phase1"
                menu = ""
                toggle(pause)
            #end if
        elif menu == "Controls":
            screen.fill(WHITE)
            pygame.draw.ellipse(screen, BLACK, (100,250,200,100), 3)
            pygame.draw.ellipse(screen, BLACK, (500,250,200,100), 3)
            #creates a button to go back to main menu
            pygame.draw.ellipse(screen, BLACK, (10,10,50,50), 2)
            draw_text("Back", small_font, BLACK, 20, 25)
            draw_text("Controls", menu_font, BLACK, 275, 100)
            draw_text("Boss 1", text_font, BLACK, 150, 275)
            draw_text("Boss 2", text_font, BLACK, 550, 275)
            if mouse_x > 0 and mouse_x < 60 and mouse_y > 0 and mouse_y < 60:
                menu = ""
            elif mouse_x > 100 and mouse_x < 300 and mouse_y > 250 and mouse_y < 350:
                menu = "Boss Control 1"
            elif mouse_x > 500 and mouse_x < 700 and mouse_y > 250 and mouse_y < 350:
                menu = "Boss Control 2"
            #end if
        elif menu == "Boss Control 1":
            screen.fill(WHITE)
            if mouse_x > 0 and mouse_x < 60 and mouse_y > 0 and mouse_y < 60:
                menu = ""
            #end if
            pygame.draw.ellipse(screen, BLACK, (10,10,50,50), 2)
            draw_text("Back", small_font, BLACK, 20, 25)
            bossImagePlant1 = pygame.image.load("resources/Plant_Boss_Phase 1-Idle.png")
            bossImagePlant1 = pygame.transform.scale(bossImagePlant1, (200,200))
            bossImagePlant2 = pygame.image.load("resources/Plant_Boss_Phase_2.png")
            bossImagePlant2 = pygame.transform.scale(bossImagePlant2, (200,200))
            screen.blit(bossImagePlant1, (50, 100))
            screen.blit(bossImagePlant2, (450, 100))
            screen.blit(leftClickSymbol, (-10, 300))
            draw_text("This attack shoots a fast small seed which deals", small_font, BLACK, 70, 325)
            draw_text("a little damage", small_font, BLACK, 70, 350)
            pygame.draw.rect(screen, BLACK, [20,400,50,50])
            pygame.draw.rect(screen, BLACK, [20,475,50,50])
            draw_text("1", menu_font, WHITE, 25, 390)
            draw_text("2", menu_font, WHITE, 25, 465)
            draw_text("This attack shoots a small yellow seed ", small_font, BLACK, 75, 400)
            draw_text("which stuns your opponents", small_font, BLACK, 75, 425)
            draw_text("This phase doesn't have a third attack", small_font, BLACK, 75, 490)
            draw_text("This attack is similar to the first phase", small_font, BLACK, 450, 325)
            draw_text("but shoots 3 seeds instead", small_font, BLACK, 450, 350)
            draw_text("This attack is the same as the first phase", small_font, BLACK, 450, 410)
            draw_text("This shoots a swarm of flies which deal", small_font, BLACK, 450, 475)
            draw_text("poison damage to your enemy over time", small_font, BLACK, 450, 500)
            #img = pygame.image.load("image.png")
            #screen.blit(img, 0,0)
        elif menu == "Boss Control 2":
            screen.fill(WHITE)
        #end if
        # Update display
        pygame.display.flip()
    else:
        oceanMap = pygame.image.load('resources/Ocean_Map.png')
        oceanMap = pygame.transform.scale(oceanMap, (800,600))
        #Changing the player's character depending on which character they chose
        if playerBoss == "Fish Boss":
            #Changes player's sprite to match chosen boss
            sprite_image = pygame.image.load('resources/Fish_Boss.png')
            #Rescale sprite to fit screen proportions cus actual png of the sprite is too large
            sprite_image = pygame.transform.scale(sprite_image, (200,75))
            sprite_rect = sprite_image.get_rect()
            sprite_position = sprite_rect.center
            #reset the variable player boss since if not done the program will continue to reload this secton every tick and cause large lag
            playerBoss = ""
            #displays the proper background for the boss
            oceanMap = pygame.image.load('resources/Ocean_Map.png')
            oceanMap = pygame.transform.scale(oceanMap, (800,600))
            screen.blit(oceanMap, (0,0))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            cooldown = Jerry.get_cooldown()
            if cooldown > 1:
                projectile_fire("bubble")
            #end if
        #different keys for different types of projectiles
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
                    if projectile.get_type() == "normal" or projectile.get_type() == "bubble":
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
        screen.blit(oceanMap, (0,0))
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
        #draw_text(str(hit), text_font, BLACK, 650, 475)
        # test to check if dodge works
        #draw_text(str(dodge_times), text_font, BLACK, 650, 375)
        # test to check if cooldown works
        #draw_text(str(Jerry.get_cooldown()), text_font, BLACK, 650, 275)
        # test to check if hp works
        #draw_text(str(Jerry.get_hp()), text_font, BLACK, 650, 75)
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
        # Increase cooldown value
        Jerry.set_cooldown(Jerry.get_cooldown() + 1)
        # Update display
        pygame.display.flip()
    # Cap the frame rate
    pygame.time.Clock().tick(60)
    #end if
#end while
# Quit Pygame
pygame.quit()
