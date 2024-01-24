# *********************************************************
# Program: main.py
# Course: PSP0101 PROBLEM SOLVING AND PROGRAM DESIGN
# Class: TL12
# Year: 2023/24 Trimester 1
# Names: PAN_HAN_CHENG | LEE_JUN_YAN | LEE_JIA_XIAN
# IDs: 1231100928 | 1231100865 | 1231100945
# Emails: 1231100928@student.mmu.edu.my | 1231100865@student.mmu.edu.my | 1231100945@student.mmu.edu.my
# Phones: 0166137037 | 0128500415 | 0178663768
# *********************************************************

#checks if pygame is installed or not and if not downloads it automatically
import pip
import time
import sys
import random

def install(module):
    pip.main(['install', module])

try: 
    import pygame
except ModuleNotFoundError:
    install('pygame')
    import pygame

#Main Menu
pygame.init()
pygame.display.set_caption('Snake Pong')

#screen size
scrn_width = 800 #2560, 1920, 1600, 1366, 1280, 800, 640
scrn_height = 600 #1440, 1080, 900, 768, 720, 600, 480
size = (scrn_width, scrn_height)

#screen
scrn = pygame.display.set_mode(size)

#music
MusicRun = True
if MusicRun == True:
    #pygame.mixer.music.load('a')
    pygame.mixer.music.set_volume(1)

#images
main_bg_img = pygame.image.load('images/background/grassy_bg.jpg').convert_alpha()
start_button_img = pygame.image.load('images/buttons/start_button_pixel.jpg').convert_alpha()
settings_button_img = pygame.image.load('images/buttons/settings_button_pixel.jpg').convert_alpha()
exit_button_img = pygame.image.load('images/buttons/exit_button_pixel.jpg').convert_alpha()

#image scalling
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
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                IfClicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button
        scrn.blit(self.image, (self.rect.x, self.rect.y))

        return IfClicked
    
#buttons
start_button = Button((scrn_width // 2), (scrn_height // 3), start_button_img, 2)
settings_button = Button((scrn_width // 2), (scrn_height // 2), settings_button_img, 2)
exit_button = Button((scrn_width // 2), (scrn_height / 1.5), exit_button_img, 2)
back_button = Button
resume_button = Button
fullscrn_button = Button
windowed_fullscrn_button = Button
windowed_button = Button


#define fonts and colors for text
Menufont = pygame.font.Font("fonts/MinecraftTen-VGORe.ttf", 60)
Settingsfont = pygame.font.Font("fonts/MinecraftTen-VGORe.ttf", 40)
txt_color = (0, 0, 0)

def txtforall(txt, font, txt_color, x_scale, y_scale):
    text = font.render(txt, True, txt_color)

    #text centering
    text_rect = text.get_rect(center = (scrn_width // x_scale, scrn_height // y_scale))

    scrn.blit(text, text_rect)


#settings menu
def settings_menu():
    txtforall('Screen Size', Settingsfont, txt_color, 5, 6)
    txtforall('Music', Settingsfont, txt_color, 5, 2.5)
    txtforall('Sound', Settingsfont, txt_color, 5, 1.5)
    pass #put window options, music and sound settings and also controls

#Game state
GamePaused = False
GameScreen = 'MainMenu'

#Game loop

run = True

while run:

    if GameScreen == 'MainMenu':
        scrn.blit(main_bg, (0, 0))
        txtforall('Snake Pong', Menufont, txt_color, 2, 5)

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
        settings_menu()

    #check if game is paused
    if GameScreen == 'GamePaused':
        scrn.blit() #add green semi transparent screen

        if resume_button.draw():
            GameScreen = 'GamePlay'

        if settings_button():
            GameScreen == 'Settings'

        if exit_button():
            run = False

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                GameScreen = 'GamePaused'
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()

pygame.quit()