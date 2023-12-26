import pygame
import random
import sys
import pygame.mixer


#initialize pygame
pygame.init()
pygame.mixer.init()

#parameters
window_x, window_y = 600, 400 #640 480,800 600, 1280 720, 1600 900, 1920 1080, 2560 1440
tile_size = 20
snake_size = 20
FPS = 10

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (1, 32, 20)
RED = (255, 0, 0)

#direction (learnt tht it doesn't apply like the coordinate in the cartesian plane)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

#songs
pygame.mixer.music.load('snake_pong/bgm/sunflower.mp3')
pygame.mixer.music.set_volume(0.4)  # Adjust the volume as needed

#background image
bg_image = pygame.image.load('snake_pong/images/background/grassy_bg.jpg')
bg_image = pygame.transform.scale(bg_image, (window_x, window_y))

#defining Elements and Functions
class SnakeGame:
    def __init__(game):
            #game window
            game.width = window_x
            game.height = window_y
            #grid sizes for the game
            game.grid_size = tile_size
            #snake sizes according to the tiles
            game.snake_size = snake_size
            #FPS
            game.fps = FPS

            #display surfaces
            game.screen = pygame.display.set_mode((game.width, game.height))
            pygame.display.set_caption("SnakePong")

            #control frame rates
            game.clock = pygame.time.Clock()

            #load bg_img
            game.background_image = pygame.image.load('snake_pong/images/background/grassy_bg.jpg')
            game.background_image = pygame.transform.scale(game.background_image, (game.width, game.height))
    
            
            #snake position
            game.snake = [(100, 100), (90, 100), (80, 100)]
            #snake pointing direction
            game.direction = RIGHT

            #erm... like what it says its food spawn
            game.food = game.foodspawn()

            #scoreboard
            game.score = 0
            game.font = pygame.font.Font(None, 36)

            #plays bgm
            pygame.mixer.music.play(-1)

    def foodspawn(game):
        while True:
            #generate random position in coordinates x and y, so 2 random.randint is used
            food = (random.randint(0, (game.width - game.snake_size) // game.snake_size) * game.snake_size,
                    random.randint(0, (game.height - game.snake_size) // game.snake_size) * game.snake_size)
            #checker (if food is spawn on the position of snake, it spawns on another unoccupied position)
            if food not in game.snake:
                return food

    def draw_snake(game):
        for segment in game.snake:
            pygame.draw.rect(game.screen, DARK_GREEN, (*segment, game.snake_size, game.snake_size))

    def draw_food(game):
        pygame.draw.rect(game.screen, RED, (*game.food, game.snake_size, game.snake_size))

    def draw_score(game):
        score_text = game.font.render(f"Score: {game.score}", True, BLACK)
        game.screen.blit(score_text, (10, 10))

    def game_over(game):
        game_over_text = game.font.render("Game Over", True, BLACK)
        score_text = game.font.render(f"Score: {game.score}", True, BLACK)
        replay_text = game.font.render("Press R to replay", True, BLACK)

        # Draw background image
        game.screen.blit(game.background_image, (0, 0))

        # Calculate center positions for text elements
        game_over_x = game.width // 2 - game_over_text.get_width() // 2
        game_over_y = game.height // 2 - game_over_text.get_height() // 2 - 20

        score_x = game.width // 2 - score_text.get_width() // 2
        score_y = game.height // 2 - score_text.get_height() // 2 + 20

        replay_x = game.width // 2 - replay_text.get_width() // 2
        replay_y = game.height // 2 - replay_text.get_height() // 2 + 60

        # Draw game over elements at center positions
        game.screen.blit(game_over_text, (game_over_x, game_over_y))
        game.screen.blit(score_text, (score_x, score_y))
        game.screen.blit(replay_text, (replay_x, replay_y))
        
        pygame.display.flip() #updates the frame

        pygame.time.wait(2000)  #wait for 2 seconds

        pygame.mixer.music.pause()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        #restarts the game
                        game.__init__()  #resets game attributes
                        game.run()
                    elif event.key == pygame.K_ESCAPE:
                        # Exit the program
                        pygame.quit()
                        sys.exit()
                    else:
                        waiting_for_input = False

    def run(game):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and game.direction != DOWN:
                        game.direction = UP
                    elif event.key == pygame.K_DOWN and game.direction != UP:
                        game.direction = DOWN
                    elif event.key == pygame.K_LEFT and game.direction != RIGHT:
                        game.direction = LEFT
                    elif event.key == pygame.K_RIGHT and game.direction != LEFT:
                        game.direction = RIGHT

            # Move the snake
            x, y = game.snake[0]
            x += game.direction[0] * game.snake_size
            y += game.direction[1] * game.snake_size

            # Check for collisions
            if (x, y) in game.snake[1:]:
                game.game_over()

            # Check if the snake ate the food
            if (x, y) == game.food:
                game.score += 1
                game.food = game.foodspawn()
            else:
                game.snake.pop()

            # Check if the snake hit the walls
            if not (0 <= x < game.width and 0 <= y < game.height):
                game.game_over()

            # Update snake position
            game.snake.insert(0, (x, y))

            # Draw background image
            game.screen.blit(game.background_image, (0, 0))

            # Draw everything
            game.draw_snake()
            game.draw_food()
            game.draw_score()

            pygame.display.flip()

            game.clock.tick(game.fps)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()