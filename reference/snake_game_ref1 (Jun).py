import pygame as pg
from random import randrange

tile_size = 50
Range = (tile_size // 2, 500 - tile_size // 2, tile_size)
get_random_position = lambda: [randrange(*Range), randrange(*Range)]
snake = pg.rect.Rect([0, 0, tile_size - 2, tile_size - 2])
snake.center = get_random_position()
length = 3
segments = [snake.copy()]
snake_dir = (0,0)
time, time_step = 0, 110
screen = pg.display.set_mode((1000,700)) 
clock = pg.time.Clock() #frame rate
dirs = {pg.K_UP: 1, pg.K_LEFT: 1, pg.K_DOWN: 1, pg.K_RIGHT: 1}

while True: #main loop of program
    for event in pg.event.get():
        if event.type == pg.QUIT: #check for close application
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and dirs[pg.K_UP]:
                snake_dir = (0, -tile_size)
                dirs = {pg.K_UP: 1, pg.K_LEFT: 1, pg.K_DOWN: 0, pg.K_RIGHT: 1,}
            if event.key == pg.K_LEFT and dirs[pg.K_LEFT]:
                snake_dir = (-tile_size, 0)
                dirs = {pg.K_UP: 1, pg.K_LEFT: 1, pg.K_DOWN: 1, pg.K_RIGHT: 0,}
            if event.key == pg.K_DOWN and dirs[pg.K_DOWN]:
                snake_dir = (0, tile_size)
                dirs = {pg.K_UP: 0, pg.K_LEFT: 1, pg.K_DOWN: 1, pg.K_RIGHT: 1,}
            if event.key == pg.K_RIGHT and dirs[pg.K_RIGHT]:
                snake_dir = (tile_size, 0)
                dirs = {pg.K_UP: 1, pg.K_LEFT: 0, pg.K_DOWN: 1, pg.K_RIGHT: 1,}
    screen.fill('black') #make surface black
    self_eating = pg.Rect.collidelist(snake,segments[:-1]) != -1 # prevent self eating
    # draw snake
    [pg.draw.rect(screen, 'green',segment)for segment in segments]
    # move snake
    time_now = pg.time.get_ticks()
    if time_now  - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]
    pg.display.flip() #update the frame
    clock.tick(1) #set a delay to 60 frames oer second