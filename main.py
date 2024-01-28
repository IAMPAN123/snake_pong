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
import os
import time
from main_game_code import SnakeGame as sp
from save import load_save, write_save

def install(module):
    pip.main(['install', module])

try: 
    import pygame
except ModuleNotFoundError:
    install('pygame')
    import pygame

#load settings
save = load_save()
win_size = save[0]
volume = save[1]

#Main Menu
pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Snake Pong')

#screen size
os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
scrn_width = info.current_w
scrn_height = info.current_h

#screen and surface
monitor_w = info.current_w
monitor_h = info.current_h
scrn = pygame.display.set_mode((scrn_width, scrn_height), pygame.RESIZABLE)
if win_size == 'fullscreen':
    scrn = pygame.display.set_mode((scrn_width, scrn_height), pygame.FULLSCREEN)
elif win_size == 'windowed_fullscreen':
    scrn = pygame.display.set_mode((monitor_w - 10, monitor_h - 50), pygame.RESIZABLE)
    scrn_width = monitor_w - 10
    scrn_height = monitor_h - 50
surf = pygame.Surface((scrn_width, scrn_height), pygame.SRCALPHA)

#music
v = volume / 100
pygame.mixer.music.load('bgm\_rickrolltest.mp3')
pygame.mixer.music.set_volume(v)
pygame.mixer.music.play(-1)

#images
main_bg_img = pygame.image.load('images/_background/grassy_bg.jpg').convert_alpha()
start_button_img = pygame.image.load('images/buttons/start_button_pixel.jpg').convert_alpha()
settings_button_img = pygame.image.load('images/buttons/settings_button_pixel.jpg').convert_alpha()
exit_button_img = pygame.image.load('images/buttons/exit_button_pixel.jpg').convert_alpha()
fullscrn_button_img = pygame.image.load('images/buttons/fullscreen_button_pixel.jpg').convert_alpha()
windowed_button_img = pygame.image.load('images/buttons/windowed_button_pixel.jpg').convert_alpha()
windowed_fullscreen_button_img = pygame.image.load('images/buttons/windowed_fullscreen_pixel.jpg').convert_alpha()

#image scalling
main_bg = pygame.transform.scale(main_bg_img, (scrn_width, scrn_height))

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
fullscrn_button = Button((scrn_width // 4), (scrn_height // 3), fullscrn_button_img, 2)
windowed_fullscrn_button = Button((scrn_width // 1.5), (scrn_height // 3), windowed_fullscreen_button_img, 2)
windowed_button = Button((scrn_width // 1.25), (scrn_height // 3), windowed_button_img, 2)

#define fonts and colors for text
Menufont = pygame.font.Font("fonts/MinecraftTen-VGORe.ttf", 60)
Settingsfont = pygame.font.Font("fonts/MinecraftTen-VGORe.ttf", 40)
txt_color = (0, 0, 0)

def txt(txt, font, txt_color, x_scale, y_scale):
    text = font.render(txt, True, txt_color)

    #text centering
    text_rect = text.get_rect(center = (scrn_width // x_scale, scrn_height // y_scale))

    scrn.blit(text, text_rect)

#settings menu
class setting():
    def __init__(self, save):
        self.save_file = save

class music_txt_box():
    def __init__(self):
        self.val = str(volume)
        self.txt_box = pygame.Rect(scrn_width // 2, scrn_height // 1.5, 80, 60)
        self.tb_active = False
        self.tb_color = pygame.Color('black')

    def draw(self):
        for events in pygame.event.get():
            if events.type == pygame.MOUSEBUTTONDOWN:
                if self.txt_box.collidepoint(events.pos):
                    self.tb_active = True
                else:
                    self.tb_active = False

            if events.type == pygame.KEYDOWN:
                if self.tb_active == True:
                    if events.key == pygame.K_BACKSPACE:
                        self.val = self.val[:-1]
                    else:
                        self.val += events.unicode

        if self.tb_active == True:
            self.tb_color = pygame.Color('white')
        else:
            self.tb_color = pygame.Color('black')
            volval = int(self.val)
            try:
                if volval > 100:
                    self.val = '100'
                    volval = 100
                elif volval < 0:
                    self.val = '0'
                    volval = 0
                else:
                    pass
            except ValueError:
                self.val = '100'
                volval = 100
            
            global volume
            volume = volval

        pygame.draw.rect(scrn, self.tb_color, self.txt_box, 4)
        valtxt = Settingsfont.render(self.val, True, 'yellow')
        scrn.blit(valtxt, (self.txt_box.x + 5, self.txt_box.y + 5))

        pygame.display.update()

def settings_menu():
    scrn.blit(main_bg, (0, 0))
    txt('Screen Size', Settingsfont, txt_color, 5, 6)
    txt('Music', Settingsfont, txt_color, 5, 2)

# Game state
isPaused = False
GameScreen = 'MainMenu'
fullscrn = False

# Countdown variables
countdown_duration = 3  # Adjust the duration of the countdown in seconds
countdown_start_time = 0

# Game loop
vol = music_txt_box()
spg = sp(v)
run = True

while run:

    #Main menu
    if GameScreen == 'MainMenu':
        scrn.blit(main_bg, (0, 0))
        txt('Snake Pong', Menufont, txt_color, 2, 5)

        if start_button.draw():
            GameScreen = 'Countdown'
            countdown_start_time = time.time()
        
        if settings_button.draw():
            GameScreen = 'Settings'
        
        if exit_button.draw():
            write_save([win_size, volume])
            run = False

    elif GameScreen == 'Countdown':
        #Calculate the remaining time in the countdown
        remaining_time = countdown_duration - (time.time() - countdown_start_time)

        # Display the countdown on the screen
        if remaining_time > 0:
            countdown_text = Menufont.render(str(int(remaining_time) + 1), True, txt_color)
            countdown_x = scrn_width // 2 - countdown_text.get_width() // 2
            countdown_y = scrn_height // 2 - countdown_text.get_height() // 2
            scrn.blit(main_bg, (0, 0))
            scrn.blit(countdown_text, (countdown_x, countdown_y))
        else:
            GameScreen = 'GamePlay'  # Switch to gameplay once the countdown is over
    
    #Gameplay
    elif GameScreen == 'GamePlay':
        spg.run()

    #Settings
    if GameScreen == 'Settings':
        settings_menu()

        if fullscrn_button.draw():
            fullscrn = True
            scrn = pygame.display.set_mode((monitor_w, monitor_h), pygame.FULLSCREEN)
            scrn_width = info.current_w
            scrn_height = info.current_h
            win_size = 'fullscreen'
        
        if windowed_fullscrn_button.draw():
            fullscrn = False
            scrn = pygame.display.set_mode((monitor_w - 10, monitor_h - 50), pygame.RESIZABLE)
            scrn_width = monitor_w - 10
            scrn_height = monitor_h - 50
            win_size = 'windowed_fullscreen'
            print(win_size)

        vol.draw()

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                GameScreen = 'MainMenu'
        if event.type == pygame.VIDEORESIZE:
            if fullscrn == False:
                scrn = pygame.display.set_mode((scrn_width, scrn_height), pygame.RESIZABLE)
        if event.type == pygame.QUIT:
            write_save([win_size, volume])
            run = False
    
    pygame.display.update()
    pygame.display.flip()

pygame.quit()