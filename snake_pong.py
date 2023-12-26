#checks if pygame is installed or not and if not downloads it automatically
import pip
import time

def install(module):
    pip.main(['install', module])

try: 
    import pygame
except ModuleNotFoundError:
    install('pygame')
    import pygame

#Main Menu
pygame.init()
pygame.display.set_caption('Snake Pong (PSP0101)')

#screen size
scrn_width = 800 #2560, 1920, 1600, 1366, 1280, 800, 640
scrn_height = 600 #1440, 1080, 900, 768, 720, 600, 480
size = (scrn_width, scrn_height)

#screen
scrn = pygame.display.set_mode(size)

#images
main_bg_img = pygame.image.load('snake_pong/images/background/grassy_bg.jpg').convert_alpha()
start_button_img = pygame.image.load('snake_pong/images/buttons/start_button_pixel.jpg').convert_alpha()
settings_button_img = pygame.image.load('snake_pong/images/buttons/settings_button_pixel.jpg').convert_alpha()
exit_button_img = pygame.image.load('snake_pong/images/buttons/exit_button_pixel.jpg').convert_alpha()

#image scaling
main_bg = pygame.transform.scale(main_bg_img, (size))

#buttons class
class Button():
    def __init__(self, x, y, image, scale):
        img_width = image.get_width()
        img_height = image.get_height()
        self.image = pygame.transform.scale(image, (int(img_width * scale), int(img_height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    def draw(self):

        IfClicked = False

        #mouse detection for buttons
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                IfClicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button
        scrn.blit(self.image, (self.rect.x, self.rect.y))

        return False 

#buttons
start_button = Button((scrn_width // 2), (scrn_height // 3), start_button_img, 2)
settings_button = Button((scrn_width // 2), (scrn_height // 2), settings_button_img, 2)
exit_button = Button((scrn_width // 2), (scrn_height / 1.5), exit_button_img, 2)

#define fonts and colors for text
font = pygame.font.Font("snake_pong/fonts/MinecraftTen-VGORe.ttf", 40)
txt_color = (0, 0, 0)

def MainMenutxt(font, txt_color):
    text = font.render("Snake Pong (PSP0101)", True, txt_color)

    #text centering
    text_rect = text.get_rect(center = (scrn_width // 2, scrn_height // 5))

    scrn.blit(text, text_rect)

#Game state
GamePaused = False
GameScreen = 'MainMenu'

#Game loop

run = True

while run:

    if GameScreen == 'MainMenu':
        scrn.blit(main_bg, (0, 0))
        MainMenutxt(font, txt_color)

        if start_button.draw():
            GameScreen = 'GamePlay'
        
        if settings_button.draw():
            GameScreen = 'Settings'
        
        if exit_button.draw():
            run = False
    
    #Gameplay
    if GameScreen == 'GamePlay':
        print('in game')

    #Settings
    if GameScreen == 'Settings':
        print('in settings')

    #check if game is paused
    if GamePaused:
        #pause menu
        print('paused')
    else:
        pass

    #event handler

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                GamePaused = True
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()

pygame.quit()