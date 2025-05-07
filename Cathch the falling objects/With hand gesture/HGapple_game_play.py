import pygame
import sys
import random
import time
import math 
from pygame.locals import *
from database import GameDatabase

# Initialize pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game settings
NEWTON_SPEED = 8
APPLE_SPEED_MIN = 2
APPLE_SPEED_MAX = 6
APPLE_FREQUENCY = 1.5
LIVES = 3
SCORE_PER_CATCH = 10

# Leaf settings
LEAF_COUNT = 20
LEAF_COLORS = [
    (34, 139, 34),    # Forest Green
    (50, 205, 50),    # Lime Green
    (124, 252, 0),    # Lawn Green
    (0, 128, 0),      # Green
    (107, 142, 35),   # Olive Drab
    (154, 205, 50),   # Yellow Green
    (139, 69, 19),    # Brown
    (160, 82, 45),    # Sienna
    (101, 67, 33),    # Dark Brown
]

# Load images
newton_img = pygame.image.load('assets/newton.png')
newton_img = pygame.transform.scale(newton_img, (100, 100))

apple_img = pygame.image.load('assets/apple.jpeg.png')
apple_img = pygame.transform.scale(apple_img, (40, 40))

background_img = pygame.image.load('assets/apple_lawn.jpeg')
background_img = pygame.transform.scale(background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Set up display
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Catch the Falling Apples!')
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont('Arial', 24)

# High score DB
db = GameDatabase()
GAME_NAME = "apple_game"

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

class FallingApple:
    def __init__(self):  # Fixed: double underscores
        self.x = random.randint(0, WINDOW_WIDTH - apple_img.get_width())
        self.y = 200
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

class Leaf:
    def __init__(self):  # Fixed: double underscores
        self.size = random.randint(5, 15)
        # Position leaves at treetop level (about 1/4 from the top of the screen)
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = random.randint(50, 150)  # Tree level height
        self.speed_y = random.uniform(0.8, 2.5)
        self.speed_x = random.uniform(-1, 1)
        self.rotation = random.randint(0, 360)
        self.rotation_speed = random.uniform(-2, 2)
        self.color = random.choice(LEAF_COLORS)
        self.swaying = random.uniform(0, 6.28)  # Random starting point in the sine wave (0 to 2π)
        self.sway_speed = random.uniform(0.01, 0.05)
        self.sway_amount = random.uniform(0.5, 2)
    
    def update(self):
        # Fall downward
        self.y += self.speed_y
        
        # Add swaying motion
        self.swaying += self.sway_speed
        self.x += math.sin(self.swaying) * self.sway_amount + self.speed_x
        
        # Rotate the leaf
        self.rotation += self.rotation_speed
        
        # Reset if off screen
        if self.y > WINDOW_HEIGHT or self.x < -20 or self.x > WINDOW_WIDTH + 20:
            self.reset()
    
    def reset(self):
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = random.randint(50, 150)  # Reset to tree level
        self.speed_y = random.uniform(0.8, 2.5)
    
    def draw(self):
        # Create a simple leaf shape using a polygon
        points = []
        center_x = self.x
        center_y = self.y
        
        # Create a leaf shape
        angle_rad = math.radians(self.rotation)
        
        # Basic leaf shape as a polygon
        base_shape = [
            (0, -self.size),          # Top point
            (self.size/2, 0),         # Right middle
            (0, self.size),           # Bottom point
            (-self.size/2, 0)         # Left middle
        ]
        
        # Rotate and position the points
        for point in base_shape:
            x, y = point
            # Rotate
            rotated_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
            rotated_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
            # Position
            points.append((center_x + rotated_x, center_y + rotated_y))
        
        # Draw the leaf
        pygame.draw.polygon(window, self.color, points)
        
        # Draw a simple stem/vein
        stem_end_x = center_x + math.sin(angle_rad) * self.size/2
        stem_end_y = center_y - math.cos(angle_rad) * self.size/2
        pygame.draw.line(window, (0, 0, 0), (center_x, center_y), 
                         (stem_end_x, stem_end_y), 1)

def show_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    window.blit(text_surface, (x, y))

def draw_lives(lives):
    for i in range(lives):
        pygame.draw.rect(window, RED, (10 + i * 30, 10, 20, 20))

def game_over_screen(score, high_score):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    window.blit(overlay, (0, 0))

    show_text(f"GAME OVER", WINDOW_WIDTH//2 - 80, WINDOW_HEIGHT//2 - 80, RED)
    show_text(f"Your Score: {score}", WINDOW_WIDTH//2 - 80, WINDOW_HEIGHT//2 - 30)
    show_text(f"High Score: {high_score}", WINDOW_WIDTH//2 - 80, WINDOW_HEIGHT//2)
    show_text("Press SPACE to play again", WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 + 50)
    show_text("Press ESC to quit", WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 100)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    waiting = False
                    return True
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        clock.tick(FPS)

def main():
    # Add missing import for math module
    import math
    
    while True:
        newton = Newton()
        apples = []
        
        # Create leaves
        leaves = [Leaf() for _ in range(LEAF_COUNT)]
        
        last_apple_time = time.time()
        score = 0
        lives = LIVES
        high_score = db.get_high_score(GAME_NAME)
        game_running = True

        while game_running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                newton.move('left')
            if keys[K_RIGHT]:
                newton.move('right')

            current_time = time.time()
            if current_time - last_apple_time > APPLE_FREQUENCY:
                apples.append(FallingApple())
                last_apple_time = current_time

            # Update leaves
            for leaf in leaves:
                leaf.update()

            apples_to_remove = []
            for apple in apples:
                apple.update()
                if not apple.caught and apple.y > WINDOW_HEIGHT:
                    lives -= 1
                    apple.missed = True
                    if lives <= 0:
                        if score > high_score:
                            db.set_high_score(GAME_NAME, score)
                            high_score = score
                        if not game_over_screen(score, high_score):
                            pygame.quit()
                            sys.exit()
                        game_running = False
                        break

                if not apple.caught and newton.x < apple.x < newton.x + newton.width and \
                   newton.y < apple.y < newton.y + newton.height:
                    apple.caught = True
                    score += SCORE_PER_CATCH
                    apples_to_remove.append(apple)

            for apple in apples_to_remove:
                if apple in apples:
                    apples.remove(apple)

            window.blit(background_img, (0, 0))
            
            # Draw leaves
            for leaf in leaves:
                leaf.draw()
                
            newton.draw()
            for apple in apples:
                apple.draw()

            show_text(f"Score: {score}", WINDOW_WIDTH - 150, 10)
            show_text(f"High Score: {high_score}", WINDOW_WIDTH - 150, 40)
            draw_lives(lives)

            pygame.display.update()
            clock.tick(FPS)

if __name__ == "__main__":
    main()