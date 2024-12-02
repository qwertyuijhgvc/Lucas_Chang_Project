#https://www.naukri.com/code360/library/input-box-with-pygame
import pygame
import sys
pygame.init()
display = pygame.display.set_mode([700, 600])
size = (700, 500)
screen = pygame.display.set_mode(size)
font_size = pygame.font.Font(None, 45)
usr_txt = ""
usr_inp_rect = pygame.Rect(400, 400, 320, 50)
intro_font = pygame.font.SysFont("Arial", 20)
BLACK = (0, 0, 0)
color = BLACK
active = True
WHITE = (255, 255, 255)
screen.fill(WHITE)
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))
while True:
    for event in pygame.event.get():
	# if the user types QUIT then the screen will close
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  
        if event.type == pygame.KEYDOWN:
			# Check for backspace
            if event.key == pygame.K_BACKSPACE:
                  usr_txt = usr_txt[:-1]
            elif event.key == pygame.K_RETURN:
                usr_txt = ""
            else:
                usr_txt += event.unicode
    # draw rectangle and the argument passed which should be on-screen
    pygame.draw.rect(display, color, usr_inp_rect)
    draw_text(usr_txt, intro_font, BLACK, 100, 100)
    # display.flip() will try to update only a portion of the screen to updated, not full area
    pygame.display.flip()