# import pygame
# import sys
# import random
# import time
# import math
# from pygame.locals import *

# # Initialize pygame
# pygame.init()

# # Set up the game window
# WINDOW_WIDTH = 800
# WINDOW_HEIGHT = 600
# FPS = 60

# # Colors
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)
# BLUE = (0, 120, 255, 180)  # Semi-transparent blue for splash

# # Game settings
# DOLPHIN_SPEED = 8
# BALL_SPEED_MIN = 3
# BALL_SPEED_MAX = 5
# BALL_FREQUENCY = 1.5  # seconds between new balls
# LIVES = 3
# SCORE_PER_CATCH = 10

# # Animation settings
# ANIMATION_SPEED = 0.4  # seconds per frame
# JUMP_HEIGHT = 120
# JUMP_DURATION = 1.2  # seconds for full jump cycle
# DIVE_DEPTH = 150  # How deep the dolphin can dive
# DIVE_DURATION = 1.8  # seconds for full dive cycle

# # Load images
# # Left-facing dolphins (PNG files)
# dolphin_left_images = [
#     pygame.image.load('assets/Dolphin/del1.png'),
#     pygame.image.load('assets/Dolphin/del2.png'),
#     pygame.image.load('assets/Dolphin/del3.png')
# ]

# # Right-facing dolphins (JPG files)
# dolphin_right_images = [
#     pygame.image.load('assets/Dolphin/del1-1.png'),
#     pygame.image.load('assets/Dolphin/del2-2.png'),
#     pygame.image.load('assets/Dolphin/del3-3.png')
# ]

# # Scale all dolphin images
# for i in range(len(dolphin_left_images)):
#     dolphin_left_images[i] = pygame.transform.scale(dolphin_left_images[i], (160, 120))

# for i in range(len(dolphin_right_images)):
#     dolphin_right_images[i] = pygame.transform.scale(dolphin_right_images[i], (160, 120))

# ball_img = pygame.image.load('assets/ball1.png')
# ball_img = pygame.transform.scale(ball_img, (50, 50))  # Resize ball

# # Load background image
# background_img = pygame.image.load('assets/oceanBG.jpeg')
# background_img = pygame.transform.scale(background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))

# # Water level position
# WATER_LEVEL = WINDOW_HEIGHT * 0.3

# # Set up the display
# window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# pygame.display.set_caption('Dolphin Ball Catch!')
# clock = pygame.time.Clock()

# # Font for text
# font = pygame.font.SysFont('Arial', 24)
# score_font = pygame.font.SysFont('Arial', 28, bold=True)

# class WaterBackground:
#     def __init__(self):
#         # Create water texture
#         self.base_img = background_img
        
#         # Wave parameters
#         self.time = 0
#         self.wave_speed = 0.5
#         self.wave_amplitude = 10
#         self.wave_frequency = 0.02
        
#         # Create distortion map for wavy effect
#         self.offset_x = 0
        
#         # Create water particles (bubbles, etc.)
#         self.particles = []
#         for _ in range(30):
#             self.particles.append({
#                 'x': random.randint(0, WINDOW_WIDTH),
#                 'y': random.randint(int(WATER_LEVEL), WINDOW_HEIGHT),
#                 'size': random.randint(2, 6),
#                 'speed': random.uniform(0.5, 2.0),
#                 'alpha': random.randint(50, 180)
#             })
    
#     def update(self):
#         # Move water
#         self.time += 0.01
#         self.offset_x += self.wave_speed
#         if self.offset_x > WINDOW_WIDTH:
#             self.offset_x = 0
            
#         # Update particles
#         for particle in self.particles:
#             # Move particles upward
#             particle['y'] -= particle['speed']
            
#             # Fade particles as they rise
#             particle['alpha'] = max(0, particle['alpha'] - 0.5)
            
#             # Reset particles that reach top or become invisible
#             if particle['y'] < WATER_LEVEL or particle['alpha'] <= 0:
#                 particle['x'] = random.randint(0, WINDOW_WIDTH)
#                 particle['y'] = random.randint(int(WATER_LEVEL + 100), WINDOW_HEIGHT)
#                 particle['alpha'] = random.randint(50, 180)
    
#     def draw(self):
#         # Draw base water background
#         window.blit(self.base_img, (0, 0))
        
#         # Draw wavy water surface
#         wave_points = []
#         for x in range(0, WINDOW_WIDTH + 10, 10):
#             # Calculate y position using sine wave
#             y = WATER_LEVEL + self.wave_amplitude * math.sin((x + self.offset_x) * self.wave_frequency + self.time)
#             wave_points.append((x, y))
        
#         # Add points to close the polygon at bottom of screen
#         wave_points.append((WINDOW_WIDTH, WINDOW_HEIGHT))
#         wave_points.append((0, WINDOW_HEIGHT))
        
#         # Draw semi-transparent water overlay
#         water_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
#         water_color = (64, 164, 223, 60)  # Semi-transparent blue
#         pygame.draw.polygon(water_surface, water_color, wave_points)
#         window.blit(water_surface, (0, 0))
        
#         # Draw water particles (bubbles)
#         particle_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
#         for particle in self.particles:
#             # Draw bubble as a circle with alpha
#             bubble_color = (255, 255, 255, int(particle['alpha']))
#             pygame.draw.circle(particle_surface, bubble_color, 
#                               (int(particle['x']), int(particle['y'])), 
#                               particle['size'])
#         window.blit(particle_surface, (0, 0))

# class WaterSplash:
#     def __init__(self, x, width):
#         self.x = x
#         self.y = WATER_LEVEL - 10  # Just above water level
#         self.width = width
#         self.height = 5  # Initial height
#         self.max_height = 40
#         self.lifetime = 0.8  # Seconds
#         self.created_time = time.time()
#         self.alpha = 230  # Start with high opacity
        
#     def update(self):
#         elapsed = time.time() - self.created_time
#         progress = elapsed / self.lifetime
        
#         if progress >= 1:
#             return True  # Should be removed
        
#         # Splash grows quickly then fades
#         if progress < 0.4:  # First 40% of lifetime - grow
#             self.height = self.max_height * (progress / 0.4)
#         else:  # Remaining 60% - fade out
#             self.height = self.max_height * (1 - ((progress - 0.4) / 0.6))
            
#         # Fade out over time
#         self.alpha = max(0, 230 * (1 - progress))
#         return False
        
#     def draw(self):
#         # Draw multiple droplets for the splash effect
#         for i in range(5):  # 5 droplets
#             drop_x = self.x + (i * self.width // 4) - (self.width // 8)
#             drop_height = self.height * random.uniform(0.7, 1.0)  # Vary heights slightly
            
#             # Create semi-transparent splash surface
#             splash_surf = pygame.Surface((self.width // 5, drop_height), pygame.SRCALPHA)
#             splash_color = (*BLUE[:3], int(self.alpha))  # Apply alpha to blue color
            
#             # Draw droplet as elongated oval
#             pygame.draw.ellipse(splash_surf, splash_color, (0, 0, self.width // 5, drop_height))
#             window.blit(splash_surf, (drop_x, self.y - drop_height))

# class ScoreIndicator:
#     def __init__(self, x, y, value="+10"):
#         self.x = x
#         self.y = y
#         self.value = value
#         self.alpha = 255  # Start fully visible
#         self.created_time = time.time()
#         self.lifetime = 1.5  # Show for 1.5 seconds
        
#     def update(self):
#         elapsed = time.time() - self.created_time
#         if elapsed > self.lifetime:
#             return True  # Should be removed
        
#         # Fade out over time and float upward
#         self.alpha = max(0, 255 * (1 - elapsed / self.lifetime))
#         self.y -= 1  # Float upward
#         return False
        
#     def draw(self):
#         text_surface = score_font.render(self.value, True, GREEN)
#         text_surface.set_alpha(self.alpha)
#         window.blit(text_surface, (self.x, self.y))

# class Dolphin:
#     def __init__(self):
#         self.width = dolphin_right_images[0].get_width()
#         self.height = dolphin_right_images[0].get_height()
#         self.x = (WINDOW_WIDTH - self.width) // 2
#         self.y = WINDOW_HEIGHT * 0.2  # Default position at water level
#         self.speed = DOLPHIN_SPEED
        
#         # Direction (1 for right, -1 for left)
#         self.direction = 1  # Start facing right
        
#         # Animation properties
#         self.current_frame = 0
#         self.last_frame_time = time.time()
        
#         # Jumping properties
#         self.is_jumping = False
#         self.jump_start_time = 0
#         self.original_y = self.y
#         self.landing = False  # Flag to track if dolphin is landing
#         self.has_splashed = False  # Flag to prevent multiple splashes
        
#         # Diving properties
#         self.is_diving = False
#         self.dive_start_time = 0
#         self.water_level_y = self.y  # Store water level position
#         self.underwater_opacity = 255  # Full opacity above water
#         self.coming_up = False  # Flag to track if dolphin is resurfacing
#         self.has_dive_splashed = False  # Flag to prevent multiple dive splashes
        
#         # Natural movement - dolphin gently bobs up and down in water
#         self.bob_factor = 0
#         self.bob_direction = 1
#         self.bob_speed = 0.5
#         self.bob_amount = 3
    
#     def move(self, direction):
#         if direction == 'left':
#             if self.x > 0:
#                 self.x -= self.speed
#             self.direction = -1  # Set facing left
        
#         if direction == 'right':
#             if self.x < WINDOW_WIDTH - self.width:
#                 self.x += self.speed
#             self.direction = 1   # Set facing right
            
#         if direction == 'up':
#             # Only jump if not already jumping or diving
#             if not self.is_jumping and not self.is_diving:
#                 self.start_jump()
                
#         if direction == 'down':
#             # Only dive if not already jumping or diving
#             if not self.is_jumping and not self.is_diving:
#                 self.start_dive()
    
#     def start_jump(self):
#         if not self.is_jumping and not self.is_diving:
#             self.is_jumping = True
#             self.jump_start_time = time.time()
#             self.original_y = self.y
#             self.landing = False
#             self.has_splashed = False
            
#     def start_dive(self):
#         if not self.is_diving and not self.is_jumping:
#             self.is_diving = True
#             self.dive_start_time = time.time()
#             self.water_level_y = self.y
#             self.coming_up = False
#             self.has_dive_splashed = False
    
#     def update_jump(self):
#         if self.is_jumping:
#             elapsed = time.time() - self.jump_start_time
#             if elapsed < JUMP_DURATION:
#                 # Parabolic jump - comes up and then back down
#                 progress = elapsed / JUMP_DURATION
#                 # Jump height follows a parabola: 4 * p * (1-p)
#                 jump_factor = 4 * progress * (1 - progress)
                
#                 # Calculate previous and current height to detect landing
#                 prev_y = self.y
#                 self.y = self.original_y - JUMP_HEIGHT * jump_factor
                
#                 # Detect if dolphin is in landing phase (moving downward in second half of jump)
#                 if progress > 0.5 and self.y > prev_y:
#                     self.landing = True
                
#                 return False  # Jump not complete
#             else:
#                 # Jump finished
#                 completed = self.is_jumping  # Store if we were jumping
#                 self.is_jumping = False
#                 self.y = self.original_y
                
#                 # Reset landing status but return whether we were jumping
#                 # This signals that we just landed
#                 landed = self.landing
#                 self.landing = False
#                 return completed and landed and not self.has_splashed
#         return False
        
#     def update_dive(self):
#         if self.is_diving:
#             elapsed = time.time() - self.dive_start_time
#             if elapsed < DIVE_DURATION:
#                 # Similar to jump but going down then up
#                 progress = elapsed / DIVE_DURATION
                
#                 # First half of animation: diving deeper
#                 if progress < 0.5:
#                     dive_progress = progress * 2  # Rescale to 0-1 for first half
#                     self.y = self.water_level_y + DIVE_DEPTH * dive_progress
#                     # Gradually reduce opacity as dolphin goes deeper
#                     self.underwater_opacity = max(100, 255 - 155 * dive_progress)
#                     self.coming_up = False
#                 # Second half: coming back up
#                 else:
#                     resurface_progress = (progress - 0.5) * 2  # Rescale to 0-1 for second half
#                     self.y = self.water_level_y + DIVE_DEPTH * (1 - resurface_progress)
#                     # Gradually increase opacity as dolphin resurfaces
#                     self.underwater_opacity = min(255, 100 + 155 * resurface_progress)
#                     self.coming_up = True
                
#                 return False  # Dive not complete
#             else:
#                 # Dive finished
#                 completed = self.is_diving
#                 self.is_diving = False
#                 self.y = self.water_level_y
#                 self.underwater_opacity = 255  # Reset to full opacity
                
#                 # Return whether we were coming up and haven't splashed yet
#                 splash_needed = self.coming_up and not self.has_dive_splashed
#                 self.coming_up = False
#                 self.has_dive_splashed = False
#                 return completed and splash_needed
#         return False
    
#     def update_animation(self):
#         # Only update animation when moving, jumping, or diving
#         keys = pygame.key.get_pressed()
#         is_moving = keys[K_LEFT] or keys[K_RIGHT] or self.is_jumping or self.is_diving
        
#         current_time = time.time()
#         if is_moving and current_time - self.last_frame_time > ANIMATION_SPEED:
#             self.current_frame = (self.current_frame + 1) % 3  # Three frames for each direction
#             self.last_frame_time = current_time
    
#     def update_bobbing(self):
#         # Only bob when not jumping or diving
#         if not self.is_jumping and not self.is_diving:
#             self.bob_factor += self.bob_speed * self.bob_direction
#             if self.bob_factor > 5 or self.bob_factor < -5:
#                 self.bob_direction *= -1
            
#             # Apply subtle bobbing movement
#             self.y = self.original_y + self.bob_factor
    
#     def update(self):
#         # Update dive and jump, check if we need to create splashes
#         just_landed_jump = self.update_jump()
#         just_surfaced_dive = self.update_dive()
        
#         self.update_animation()
#         self.update_bobbing()
        
#         # Return True if we need to create a splash
#         return just_landed_jump or just_surfaced_dive
    
#     def draw(self):
#         # Choose the correct image array based on direction
#         if self.direction == 1:  # Facing right
#             current_image = dolphin_right_images[self.current_frame]
#         else:  # Facing left
#             current_image = dolphin_left_images[self.current_frame]
        
#         # Create a copy of the image to adjust opacity if underwater
#         if self.is_diving and self.underwater_opacity < 255:
#             # Create a copy of the image with adjusted opacity
#             transparent_image = current_image.copy()
#             transparent_image.set_alpha(self.underwater_opacity)
#             window.blit(transparent_image, (self.x, self.y))
#         else:
#             window.blit(current_image, (self.x, self.y))
        
#         # Add bubble effect when underwater
#         if self.is_diving:
#             # Create random bubbles coming from dolphin when underwater
#             if random.random() < 0.3:  # 30% chance each frame
#                 bubble_surface = pygame.Surface((10, 10), pygame.SRCALPHA)
#                 bubble_color = (255, 255, 255, 150)
#                 pygame.draw.circle(bubble_surface, bubble_color, (5, 5), 
#                                   random.randint(2, 5))
                
#                 # Position bubble near dolphin's head
#                 bubble_x = self.x + self.width // 3
#                 bubble_y = self.y + self.height // 3
#                 window.blit(bubble_surface, (bubble_x, bubble_y))
        
#     def get_center_x(self):
#         return self.x + self.width // 2
    
#     def is_underwater(self):
#         return self.is_diving and self.y > WATER_LEVEL

# class FallingBall:
#     def __init__(self):
#         self.x = random.randint(0, WINDOW_WIDTH - ball_img.get_width())
#         self.y = -ball_img.get_height()  # Start above the screen
#         self.speed = random.uniform(BALL_SPEED_MIN, BALL_SPEED_MAX)
#         self.caught = False
#         self.missed = False
    
#     def update(self):
#         if not self.caught:
#             self.y += self.speed
#             if self.y > WINDOW_HEIGHT:
#                 self.missed = True
    
#     def draw(self):
#         if not self.caught:
#             window.blit(ball_img, (self.x, self.y))

# def show_text(text, x, y, color=WHITE):
#     text_surface = font.render(text, True, color)
#     window.blit(text_surface, (x, y))

# def draw_lives(lives):
#     for i in range(lives):
#         pygame.draw.rect(window, RED, (10 + i * 30, 10, 20, 20))

# def game_over_screen(score):
#     # Create a semi-transparent overlay
#     overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
#     overlay.fill((0, 0, 0, 180))  # Black with 180 alpha (semi-transparent)
#     window.blit(overlay, (0, 0))
    
#     # Draw game over message
#     game_over_font = pygame.font.SysFont('Arial', 48, bold=True)
#     game_over_text = game_over_font.render("GAME OVER", True, RED)
#     window.blit(game_over_text, (WINDOW_WIDTH//2 - game_over_text.get_width()//2, WINDOW_HEIGHT//2 - 100))
    
#     # Draw final score with larger font
#     final_score_font = pygame.font.SysFont('Arial', 36, bold=True)
#     final_score_text = final_score_font.render(f"FINAL SCORE: {score}", True, WHITE)
#     window.blit(final_score_text, (WINDOW_WIDTH//2 - final_score_text.get_width()//2, WINDOW_HEIGHT//2 - 20))
    
#     # Draw instructions
#     show_text("Press SPACE to play again", WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 + 50, WHITE)
#     show_text("Press ESC to quit", WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 100, WHITE)
#     pygame.display.update()
    
#     waiting = True
#     while waiting:
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == KEYDOWN:
#                 if event.key == K_SPACE:
#                     waiting = False
#                     return True  # Play again
#                 if event.key == K_ESCAPE:
#                     pygame.quit()
#                     sys.exit()
#         clock.tick(FPS)
    
#     return False

# def main():
#     while True:  # Main game loop
#         dolphin = Dolphin()
#         water_bg = WaterBackground()  # Initialize water background
#         balls = []
#         score_indicators = []  # List to store the +10 indicators
#         water_splashes = []    # List to store water splash animations
#         last_ball_time = time.time()
#         score = 0
#         lives = LIVES
#         game_running = True
        
#         while game_running:
#             for event in pygame.event.get():
#                 if event.type == QUIT:
#                     pygame.quit()
#                     sys.exit()
#                 if event.type == KEYDOWN:
#                     if event.key == K_ESCAPE:
#                         pygame.quit()
#                         sys.exit()
#                     if event.key == K_UP:
#                         dolphin.move('up')  # Up key triggers jump
#                     if event.key == K_DOWN:
#                         dolphin.move('down')  # Down key triggers dive
            
#             # Process movement input
#             keys = pygame.key.get_pressed()
#             if keys[K_LEFT]:
#                 dolphin.move('left')
#             if keys[K_RIGHT]:
#                 dolphin.move('right')
            
#             # Update water background
#             water_bg.update()
            
#             # Update dolphin animation, jump, and dive
#             # If the dolphin just landed or surfaced, create a splash
#             if dolphin.update():
#                 splash = WaterSplash(dolphin.get_center_x(), dolphin.width // 2)
#                 water_splashes.append(splash)
            
#             # Generate new balls
#             current_time = time.time()
#             if current_time - last_ball_time > BALL_FREQUENCY:
#                 balls.append(FallingBall())
#                 last_ball_time = current_time
            
#             # Update and check all balls
#             balls_to_remove = []
#             for ball in balls:
#                 ball.update()
#                 if not ball.caught and ball.y > WINDOW_HEIGHT:
#                     lives -= 1
#                     ball.missed = True
#                     if lives <= 0:
#                         if not game_over_screen(score):
#                             pygame.quit()
#                             sys.exit()
#                         game_running = False
#                         break
                
#                 # Check for collision with dolphin - now works underwater too!
#                 if not ball.caught and dolphin.x < ball.x < dolphin.x + dolphin.width and \
#                    dolphin.y < ball.y < dolphin.y + dolphin.height:
#                     ball.caught = True
#                     score += SCORE_PER_CATCH
                    
#                     # Create a new score indicator where the ball was caught
#                     score_indicators.append(ScoreIndicator(ball.x, ball.y, f"+{SCORE_PER_CATCH}"))
                    
#                     balls_to_remove.append(ball)
            
#             for ball in balls_to_remove:
#                 if ball in balls:
#                     balls.remove(ball)
            
#             # Update and draw score indicators
#             indicators_to_remove = []
#             for indicator in score_indicators:
#                 if indicator.update():  # If indicator should be removed
#                     indicators_to_remove.append(indicator)
            
#             for indicator in indicators_to_remove:
#                 if indicator in score_indicators:
#                     score_indicators.remove(indicator)
            
#             # Update water splashes
#             splashes_to_remove = []
#             for splash in water_splashes:
#                 if splash.update():  # If splash animation is done
#                     splashes_to_remove.append(splash)
                    
#             for splash in splashes_to_remove:
#                 if splash in water_splashes:
#                     water_splashes.remove(splash)
            
#             # Draw everything
#             # First draw the animated water background
#             water_bg.draw()
            
#             # Draw the dolphin
#             dolphin.draw()
            
#             # Draw water splashes
#             for splash in water_splashes:
#                 splash.draw()
            
#             # Draw balls
#             for ball in balls:
#                 ball.draw()
            
#             # Draw score indicators
#             for indicator in score_indicators:
#                 indicator.draw()
                
#             show_text(f"Score: {score}", WINDOW_WIDTH - 150, 10)
#             draw_lives(lives)
            
#             show_text("← → to move | ↑ to jump | ↓ to dive", 10, WINDOW_HEIGHT - 30)
            
#             pygame.display.update()
#             clock.tick(FPS)

# if __name__ == "__main__":
#     main()