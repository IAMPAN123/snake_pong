https://youtu.be/Qf3-aDXG8q4?si=DrAeBzBFTgMMHeNl

import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 120
BALL_SIZE = 15
FPS = 120

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE  = (0,0,255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Initialize clock and font
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def draw_text(text, x, y):
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x, y))

# Paddle class
class Paddle(pygame.sprite.Sprite):
    def _init_(self, x):
        super()._init_()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = HEIGHT // 2
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

# Ball class
class Ball(pygame.sprite.Sprite):
    def _init_(self):
        super()._init_()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = [4, 4]

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        # Bounce off walls
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]

# Create sprites
paddle1 = Paddle(PADDLE_WIDTH // 2)
paddle2 = Paddle(WIDTH - PADDLE_WIDTH // 2)
ball = Ball()

# Create sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(paddle1, paddle2, ball)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    all_sprites.update()

    # Check for collisions with paddles
    if pygame.sprite.collide_rect(ball, paddle1) or pygame.sprite.collide_rect(ball, paddle2):
        ball.speed[0] = -ball.speed[0]

    # Check for scoring
    if ball.rect.left <= 0 or ball.rect.right >= WIDTH:
        ball.rect.center = (WIDTH // 2, HEIGHT // 2)

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
