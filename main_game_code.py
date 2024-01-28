import pygame
import sys
import os

# Constants
tile_size = 20
snake_size = 20
FPS_snake = 15
FPS_paddle = 70 

is_Paused = False
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 80

# Colors
DARK_GREEN = (0, 128, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class SnakeGame:
    def __init__(self, v):
        
        # Game Window Settings
        self.width = scrn_width
        self.height = scrn_height
        self.grid_size = tile_size # grid sizes for the game

        # Display Surfaces
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("SnakePong")
        self.surf = pygame.Surface((scrn_width, scrn_height), pygame.SRCALPHA)

        # FPS settings
        self.FPS_snake = FPS_snake
        self.FPS_paddle = FPS_paddle
        
        # Control Frame Rates
        self.clock_snake = pygame.time.Clock()
        self.clock_paddle = pygame.time.Clock()
        
        # Fonts
        self.font = pygame.font.Font(None, 36)

        # Music
        pygame.mixer.music.load('bgm\_rickrolltest.mp3')
        pygame.mixer.music.set_volume(v)  # Adjust the volume as needed

        # Plays bgm
        pygame.mixer.music.play(-1)

        # Bg Img
        self.background_image = pygame.image.load('images\_background\grassy_bg.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

        # Snake and Paddle
        self.snake_lives = 3 # Snake lives and Paddle lives
        self.paddle_lives = 3
        self.snake_size = snake_size  # Snake sizes according to the Tiles
        # Snake position
        self.snake = [(scrn_width/2, scrn_height/2),(scrn_width/2, scrn_height/2),(scrn_width/2, scrn_height/2),(scrn_width/2, scrn_height/2),(scrn_width/2, scrn_height/2)]
        self.direction = RIGHT  # Snake pointing direction
        
        # Create paddles for left and right sides
        self.paddle_left = Paddle(20, scrn_height // 2, PADDLE_HEIGHT, self.FPS_paddle)
        self.paddle_right = Paddle(self.width - 20, scrn_height // 2, PADDLE_HEIGHT, self.FPS_paddle)

    def draw_snake(self):
        for segment in self.snake:
            pygame.draw.rect(self.screen, DARK_GREEN, (*segment, self.snake_size, self.snake_size))

    def check_paddle_collision(self, x, y):
    # Check if the head of the snake collides with the paddles
        if self.paddle_left.rect.colliderect(pygame.Rect(x, y, self.snake_size, self.snake_size)):
            return True
        elif self.paddle_right.rect.colliderect(pygame.Rect(x, y, self.snake_size, self.snake_size)):
            return True
        return False

    def snake_spawn(self):
        while True:
            # Spawn in center of screen
            spawn_position = [(self.width // 2), (self.height // 2)]
            return spawn_position
        
    def game_paused(self):
        paused_text = self.font.render('Game is Paused', True, BLACK)

        #add green semi transparent screen
        self.screen.blit(self.surf, (0, 0))
        pygame.draw.rect(self.surf, (0, 255, 0, 40), [0, 0, scrn_width, scrn_height])
        
        paused_x = self.width // 2 - paused_text.get_width() // 2
        paused_y = self.height // 2 - paused_text.get_height() // 2 - 20

        self.screen.blit(paused_text, (paused_x, paused_y))

    def game_over(self):
        game_over_text = self.font.render("Game Over", True, BLACK)
        winner_text_s = self.font.render("Snake Wins!", True, BLACK)
        winner_text_p = self.font.render("Paddle Wins!", True, BLACK)
        replay_text = self.font.render("Press R to replay", True, BLACK)

        # Draw background image
        self.screen.blit(self.background_image, (0, 0))

        # Calculate center positions for text elements
        game_over_x = self.width // 2 - game_over_text.get_width() // 2
        game_over_y = self.height // 2 - game_over_text.get_height() // 2 - 20

        winner_x_s = self.width // 2 - winner_text_s.get_width() // 2
        winner_y_s = self.height // 2 - winner_text_s.get_height() // 2 + 20

        winner_x_p = self.width // 2 - winner_text_p.get_width() // 2
        winner_y_p = self.height // 2 - winner_text_p.get_height() // 2 + 20

        replay_x = self.width // 2 - replay_text.get_width() // 2
        replay_y = self.height // 2 - replay_text.get_height() // 2 + 60

        # Draw game over elements at center position
        self.screen.blit(game_over_text, (game_over_x, game_over_y))
        self.screen.blit(replay_text, (replay_x, replay_y))
        
        # Winner Checker
        if self.paddle_lives < 1:
            self.screen.blit(winner_text_s, (winner_x_s, winner_y_s))
        if self.snake_lives < 1:
            self.screen.blit(winner_text_p, (winner_x_p, winner_y_p))

        pygame.display.flip()  # updates the frame

        pygame.time.wait(2000)  # wait for 2 seconds

        pygame.mixer.music.pause()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # restarts the game
                        self.__init__()  # resets game attributes
                        self.run()
                        #resets paddle height
                        PADDLE_HEIGHT = 80
                    elif event.key == pygame.K_ESCAPE:
                        # Exit the program
                        pygame.quit()
                        sys.exit()
                    else:
                        waiting_for_input = False


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    global is_Paused
                    #Pausing the game
                    if event.key == pygame.K_SPACE:
                        if is_Paused == False:
                            is_Paused = True
                        elif is_Paused == True:
                            is_Paused = False

                    if is_Paused == False:
                        # Snake Control
                        if event.key == pygame.K_UP: self.direction = UP
                        elif event.key == pygame.K_DOWN: self.direction = DOWN
                        elif event.key == pygame.K_LEFT: self.direction = LEFT
                        elif event.key == pygame.K_RIGHT: self.direction = RIGHT

                        # Paddle Control
                        elif event.key == pygame.K_w:
                            self.paddle_left.move_up()
                            self.paddle_right.move_up()
                        elif event.key == pygame.K_s:
                            self.paddle_left.move_down()
                            self.paddle_right.move_down()

            if is_Paused == False:
                # Move the snake
                x, y = self.snake[0]
                x += self.direction[0] * self.snake_size
                y += self.direction[1] * self.snake_size

                # Wrap around if the snake hits the top or bottom boundary
                if y < 0:
                    y = self.height - self.snake_size
                elif y >= self.height:
                    y = 0

                # Check for collisions with paddles
                if self.check_paddle_collision(x, y):
                    self.snake = self.snake[:-1]  # Reduce the snake length by 1
                    x, y = self.snake_spawn()
                    self.snake_lives -= 1  # Decrease snake lives
                    if self.snake_lives == 0:
                        self.game_over()

                # Check for collision with left and right boundaries
                if not (0 <= x < self.width):

                    # Respawn snake at the center
                    x, y = self.snake_spawn()

                    # Increase paddle height by 20
                    global PADDLE_HEIGHT
                    PADDLE_HEIGHT += 20

                    # Update the height of the paddles
                    self.paddle_left.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
                    self.paddle_left.image.fill(BLUE)
                    self.paddle_right.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
                    self.paddle_right.image.fill(BLUE)

                    # Decrease paddle lives
                    self.paddle_lives -= 1
                    if self.paddle_lives <= 0:
                        PADDLE_HEIGHT = 80
                        self.game_over()

                # update snake position
                new_head = (x, y)
                self.snake = [new_head] + self.snake[:-1]  # Update the snake's position without increasing its length

            # draw background image
            self.screen.blit(self.background_image, (0, 0))

            # draw snake 
            self.draw_snake()

            # Update and draw the paddles
            self.paddle_left.update()
            self.screen.blit(self.paddle_left.image, self.paddle_left.rect.topleft)

            self.paddle_right.update()
            self.screen.blit(self.paddle_right.image, self.paddle_right.rect.topleft)

            # Display lives
            snake_lives_text = self.font.render(f"Snake Lives: {self.snake_lives}", True, BLACK)
            paddle_lives_text = self.font.render(f"Paddle Lives: {self.paddle_lives}", True, BLACK)

            self.screen.blit(snake_lives_text, (10, 10))
            self.screen.blit(paddle_lives_text, (self.width - paddle_lives_text.get_width() - 10, 10))

            #pause screen
            if is_Paused:
                self.game_paused()

            pygame.display.flip()

            self.clock_snake.tick(self.FPS_snake)
            self.clock_paddle.tick(self.FPS_paddle)

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, height, fps):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.height = height
        self.speed = 20
        self.FPS = fps
        self.clock = pygame.time.Clock()

    def move_up(self):
        # Wrap around if the paddle reaches the top boundary
        if self.rect.top <= 0:
            self.rect.y = scrn_height - self.height
        else:
            self.rect.y -= self.speed

    def move_down(self):
        # Wrap around if the paddle reaches the bottom boundary
        if self.rect.bottom >= scrn_height:
            self.rect.y = 0
        else:
            self.rect.y += self.speed

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move_up()
        if keys[pygame.K_s]:
            self.move_down()

        self.clock.tick(self.FPS)

# Initialize pygame
pygame.init()
pygame.mixer.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
scrn_width = info.current_w
scrn_height = info.current_h