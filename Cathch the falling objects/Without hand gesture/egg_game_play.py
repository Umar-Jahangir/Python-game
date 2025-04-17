import pygame
import sys
import random
import time
from pygame.locals import *
from database import GameDatabase

# Initialize pygame
pygame.init()

# Game window setup
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Game settings
NEWTON_SPEED = 8
APPLE_SPEED_MIN = 2
APPLE_SPEED_MAX = 6
LIVES = 3
SCORE_PER_CATCH = 10

# Load images
newton_img = pygame.transform.scale(pygame.image.load('assets/basket.png'), (100, 100))
apple_img = pygame.transform.scale(pygame.image.load('assets/egg.png'), (40, 40))
background_img = pygame.transform.scale(pygame.image.load('assets/sky_lawn.jpeg'), (WINDOW_WIDTH, WINDOW_HEIGHT))

# Display setup
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Catch the Falling Eggs!')
clock = pygame.time.Clock()

# Font setup
font = pygame.font.SysFont('Arial', 24)

# Bird animation class
class Bird(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, sprite_paths, direction='right'):
        super().__init__()
        self.sprites = [pygame.transform.scale(pygame.image.load(path), (80, 80)) for path in sprite_paths]
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.animation_speed = 0.2
        self.animation_counter = 0
        self.velocity_x = 2 if direction == 'right' else -2
        self.direction = direction
        self.last_egg_time = time.time()
        self.egg_cooldown = random.uniform(3.0, 6.0)

    def update(self):
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.image = self.sprites[self.current_sprite]
        self.rect.x += self.velocity_x
        if self.direction == 'right' and self.rect.x > WINDOW_WIDTH:
            self.rect.x = -self.rect.width
        elif self.direction == 'left' and self.rect.right < 0:
            self.rect.x = WINDOW_WIDTH

    def can_drop_egg(self):
        current_time = time.time()
        if current_time - self.last_egg_time > self.egg_cooldown:
            self.last_egg_time = current_time
            self.egg_cooldown = random.uniform(3.0, 6.0)
            return True
        return False

# Newton (basket) class
class Newton:
    def __init__(self):
        self.width = newton_img.get_width()
        self.height = newton_img.get_height()
        self.x = (WINDOW_WIDTH - self.width) // 2
        self.y = WINDOW_HEIGHT - self.height - 10
        self.speed = NEWTON_SPEED

    def move(self, direction):
        if direction == 'left' and self.x > 0:
            self.x -= self.speed
        if direction == 'right' and self.x < WINDOW_WIDTH - self.width:
            self.x += self.speed

    def draw(self):
        window.blit(newton_img, (self.x, self.y))

# Falling egg class
class FallingEgg:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.uniform(APPLE_SPEED_MIN, APPLE_SPEED_MAX)
        self.caught = False
        self.missed = False

    def update(self):
        if not self.caught:
            self.y += self.speed
            if self.y > WINDOW_HEIGHT:
                self.missed = True

    def draw(self):
        if not self.caught:
            window.blit(apple_img, (self.x, self.y))

# Utility functions
def show_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    window.blit(text_surface, (x, y))

def draw_lives(lives):
    for i in range(lives):
        pygame.draw.rect(window, RED, (10 + i * 30, 10, 20, 20))

def game_over_screen(score):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    window.blit(overlay, (0, 0))

    show_text("GAME OVER", WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 - 50, RED)
    show_text(f"Your Score: {score}", WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2, WHITE)
    show_text("Press SPACE to play again", WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 50, WHITE)
    show_text("Press ESC to quit", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 100, WHITE)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return True
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        clock.tick(FPS)

# Main game loop
def main():
    db = GameDatabase()
    high_score = db.get_high_score("egg_game")

    while True:
        newton = Newton()
        eggs = []
        score = 0
        db = GameDatabase()
        high_score = db.get_high_score("egg_game")

        lives = LIVES
        game_running = True

        birds = pygame.sprite.Group()

        bird1 = Bird(-100, 10, [f"assets/Bird1/B1{i}.png" for i in range(1, 6)], direction='right')
        bird2 = Bird(WINDOW_WIDTH + 200, 100, [f"assets/Bird2/B3{i}.png" for i in range(1, 5)], direction='left')
        bird3 = Bird(WINDOW_WIDTH + 100, 150, [f"assets/Bird3/B2{i}.png" for i in range(1, 9)], direction='right')
        birds.add(bird1, bird2, bird3)

        while game_running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                newton.move('left')
            if keys[K_RIGHT]:
                newton.move('right')

            for bird in birds:
                if bird.can_drop_egg() and 0 < bird.rect.x < WINDOW_WIDTH:
                    egg_x = bird.rect.x + bird.rect.width // 2 - apple_img.get_width() // 2
                    egg_y = bird.rect.y + bird.rect.height - 10
                    eggs.append(FallingEgg(egg_x, egg_y))

            eggs_to_remove = []
            for egg in eggs:
                egg.update()
                if not egg.caught and egg.y > WINDOW_HEIGHT:
                    lives -= 1
                    egg.missed = True
                    if lives <= 0:
                        if score > high_score:
                            db.set_high_score("egg_game", score)
                            high_score = score
                        if score > high_score:
                            db.set_high_score("egg_game", score)
                        if not game_over_screen(score):
                            pygame.quit()
                            sys.exit()
                        game_running = False
                        break
                if not egg.caught and newton.x < egg.x < newton.x + newton.width and \
                        newton.y < egg.y < newton.y + newton.height:
                    egg.caught = True
                    score += SCORE_PER_CATCH
                    eggs_to_remove.append(egg)

            for egg in eggs_to_remove:
                if egg in eggs:
                    eggs.remove(egg)

            window.blit(background_img, (0, 0))
            birds.update()
            birds.draw(window)
            newton.draw()
            for egg in eggs:
                egg.draw()
            show_text(f"Score: {score}", WINDOW_WIDTH - 150, 10)
            show_text(f"High Score: {high_score}", WINDOW_WIDTH - 150, 40)
            draw_lives(lives)

            pygame.display.update()
            clock.tick(FPS)

# Run game
if __name__ == "__main__":
    main()
