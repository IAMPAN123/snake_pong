import pygame as pg
from random import randrange

WINDOW = 600
tile_size = 30
range = (tile_size // 2, WINDOW - tile_size//2, tile_size) 
get_random_position = lambda: [randrange(*range), randrange(*range)] #random snake spawn position
snake = pg.rect.Rect([0, 0, tile_size - 2, tile_size - 2]) #snake head position
snake.center =get_random_position() #position on grid
length = 5
segments = [snake.copy()]
snake_dir = (0, 0)
time, time_step = 0, 110 #timestep is delay in milliseconds
food = snake.copy()
food.center = get_random_position()
screen = pg.display.set_mode([WINDOW]*2) #screen rendering
clock = pg.time.Clock() #Clock class for frame rate
dirs = {pg.K_UP: 1, pg.K_LEFT: 1, pg.K_DOWN: 1, pg.K_RIGHT: 1,}

#Main
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT: #determine quit option
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
    #check borders and self eating
    self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1
    if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW or self_eating:
        snake.center, food.center = get_random_position(), get_random_position()
        length, snake_dir = 1, (0, 0)
        segments = [snake.copy()]
    #check food
    if snake.center == food.center:
        food.center = get_random_position()
        length += 1
    #draw food
    pg.draw.rect(screen, 'red', food)
    #draw snake
    [pg.draw.rect(screen, 'green', segment) for segment in segments]
    #move snake
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]
    pg.display.flip() #update the frame
    clock.tick(60) #fps
