#checks if pygame is installed or not and if not downloads it automatically
import pip

def install(module):
    pip.main(['install', module])

try: 
    import pygame
except ModuleNotFoundError:
    install('pygame')
    import pygame

#Main Menu
pygame.init()