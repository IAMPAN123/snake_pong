import os
import json
import pygame

def load(savefile):
    with open(os.path.join(savefile), 'r+') as file:
        config = json.load(file)
    return config

def write_save(data):
    with open(os.path.join(os.getcwd(), 'config.json'), 'w') as file:
        json.dump(data, file)

def load_save():
    #will try to load the existing save
    try:
        save = load('config.json')
    #if no save file or something wrong with the save and cannot load it, create a new one and load it
    except:
        save = create_save()
        write_save(save)
    return save

def create_save():
    win_size = 'fullscreen'
    volume = 100
    return win_size, volume