import pygame
import sys
import subprocess
import os
import random

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Catch the Falling Object")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.SysFont("Arial", 56, bold=True)
menu_title_font = pygame.font.SysFont("Arial", 48)
button_font = pygame.font.SysFont("Arial", 36)
option_font = pygame.font.SysFont("Arial", 32)
instruction_font = pygame.font.SysFont("Arial", 24)  # Smaller font for instructions

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (30, 80, 180)
LIGHT_BLUE = (100, 180, 255)
GRAY = (100, 100, 100)
ORANGE = (255, 165, 0)
LIGHT_ORANGE = (255, 200, 100)
DOLPHIN_BLUE = (0, 120, 215)
LIGHT_DOLPHIN_BLUE = (100, 180, 255)
GOLD = (238, 213, 120)  # Gold background color for mode selection
TURQUOISE = (64, 224, 208)  # Turquoise color for mode buttons
LIGHT_TURQUOISE = (95, 255, 239)  # Light turquoise for button hover

# Game states
current_screen = "home"

# Scrolling variables for instructions
instruction_scroll_y = 0
max_scroll_y = 0  # Will be calculated based on content

# Particles
particles = []
for _ in range(30):
    particles.append({
        'pos': pygame.math.Vector2(random.randint(0, 800), random.randint(0, 600)),
        'velocity': pygame.math.Vector2(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)),
        'size': random.randint(2, 5),
        'color': (255, 255, 255, random.randint(50, 150))
    })

# Load icons
try:
    if not os.path.exists("assets"):
        os.makedirs("assets")

    for game, color in [("egg", (255, 220, 180)), ("newton", (255, 0, 0)), ("einstein", (220, 220, 220)), ("dolphin", DOLPHIN_BLUE)]:
        if not os.path.exists(f"assets/{game}_icon.png"):
            icon_surface = pygame.Surface((120, 120), pygame.SRCALPHA)
            if game == "egg":
                pygame.draw.ellipse(icon_surface, color, (10, 10, 100, 100))
            elif game == "newton":
                pygame.draw.circle(icon_surface, color, (60, 60), 50)
                pygame.draw.rect(icon_surface, (100, 70, 0), (55, 10, 10, 20))
            elif game == "dolphin":
                pygame.draw.circle(icon_surface, color, (60, 60), 50)
                # Add simple dolphin silhouette
                pygame.draw.rect(icon_surface, (100, 70, 0), (55, 10, 10, 20))
            else:
                pygame.draw.rect(icon_surface, color, (10, 10, 100, 100))
                font = pygame.font.SysFont(None, 48)
                text = font.render("E=mc²", True, (0, 0, 0))
                icon_surface.blit(text, (20, 40))
            pygame.image.save(icon_surface, f"assets/{game}_icon.png")

    # Try to load custom dolphin logo if it exists
    if os.path.exists("assets/dolphin_logo.png"):
        os.rename("assets/dolphin_icon.png", "assets/dolphin_icon_backup.png")
        os.rename("assets/dolphin_logo.png", "assets/dolphin_icon.png")

    def load_and_scale_icon(filename, target_size=(80, 80)):
        icon = pygame.image.load(f"assets/{filename}").convert_alpha()
        return pygame.transform.scale(icon, target_size)

    egg_icon = load_and_scale_icon("egg_icon.png")
    newton_icon = load_and_scale_icon("newton_icon.png")
    einstein_icon = load_and_scale_icon("einstein_icon.png")
    dolphin_icon = load_and_scale_icon("dolphin_icon.png")

except Exception as e:
    print(f"Error loading/creating icons: {e}")
    egg_icon = newton_icon = einstein_icon = dolphin_icon = None

def draw_text(text, font, color, x, y, align="center", max_width=None):
    if max_width is None:
        text_surface = font.render(text, True, color)
        if align == "center":
            text_rect = text_surface.get_rect(center=(x, y))
        elif align == "left":
            text_rect = text_surface.get_rect(midleft=(x, y))
        screen.blit(text_surface, text_rect)
        return text_rect
    else:
        # Word wrap for long text
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width = font.size(test_line)[0]
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                if current_line:  # Add the current line if it's not empty
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:  # If a single word is too long, just add it
                    lines.append(word)
                    current_line = []
        
        if current_line:  # Add the last line
            lines.append(' '.join(current_line))
        
        # Render each line
        rendered_height = 0
        rendered_rects = []
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            if align == "center":
                text_rect = text_surface.get_rect(center=(x, y + i * font.get_height()))
            elif align == "left":
                text_rect = text_surface.get_rect(midleft=(x, y + i * font.get_height()))
            
            rendered_height += font.get_height()
            rendered_rects.append((text_surface, text_rect))
        
        return rendered_rects, rendered_height

def create_button(text, x, y, width, height, color=BLUE, hover_color=LIGHT_BLUE):
    button_rect = pygame.Rect(x, y, width, height)
    mouse_pos = pygame.mouse.get_pos()
    current_color = hover_color if button_rect.collidepoint(mouse_pos) else color
    pygame.draw.rect(screen, current_color, button_rect, border_radius=15)
    pygame.draw.rect(screen, WHITE, button_rect, width=2, border_radius=15)
    text_surf = button_font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)
    return button_rect

def update_particles():
    for particle in particles:
        particle['pos'] += particle['velocity']
        if particle['pos'].x < 0:
            particle['pos'].x = 800
        elif particle['pos'].x > 800:
            particle['pos'].x = 0
        if particle['pos'].y < 0:
            particle['pos'].y = 600
        elif particle['pos'].y > 600:
            particle['pos'].y = 0
        surf = pygame.Surface((particle['size']*2, particle['size']*2), pygame.SRCALPHA)
        pygame.draw.circle(surf, particle['color'], (particle['size'], particle['size']), particle['size'])
        screen.blit(surf, (int(particle['pos'].x - particle['size']), int(particle['pos'].y - particle['size'])))

def home_screen():
    screen.fill(BLACK)
    update_particles()
    draw_text("CATCH THE FALLING OBJECT", title_font, GRAY, 400, 102)
    draw_text("CATCH THE FALLING OBJECT", title_font, WHITE, 398, 100)
    draw_text("Select an option to begin", option_font, GRAY, 400, 170)
    play_btn = create_button("PLAY GAMES", 250, 250, 300, 60)
    settings_btn = create_button("SETTINGS", 250, 330, 300, 60)
    instructions_btn = create_button("INSTRUCTIONS", 250, 410, 300, 60)
    quit_btn = create_button("QUIT", 250, 490, 300, 60)
    return {
        "play": play_btn,
        "settings": settings_btn,
        "instructions": instructions_btn,
        "quit": quit_btn
    }

def mode_selection_screen():
    screen.fill(BLACK)
    update_particles()
    
    # Draw the Mode header with shadow effect like the home screen
    draw_text("MODE SELECTION", title_font, GRAY, 400, 102)
    draw_text("MODE SELECTION", title_font, WHITE, 398, 100)
    draw_text("Select your preferred mode", option_font, GRAY, 400, 170)
    
    # Create buttons in the same style as the home screen
    normal_btn = create_button("NORMAL", 250, 250, 300, 60)
    hand_gesture_btn = create_button("HAND GESTURE", 250, 330, 300, 60)
    back_btn = create_button("BACK", 250, 410, 300, 60)
    
    return {
        "normal": normal_btn,
        "hand_gesture": hand_gesture_btn,
        "back": back_btn
    }

def select_game_screen():
    screen.fill(BLACK)
    update_particles()
    back_rect = create_button("BACK", 20, 20, 100, 40)
    draw_text("SELECT A GAME", menu_title_font, WHITE, 400, 80)

    icon_size = 80
    circle_radius = 70

    center_x = 400
    top_y = 180
    middle_y = 300
    bottom_y = 420
    side_gap = 160

    # Game positions in a diamond pattern
    egg_center = (center_x, top_y)
    newton_center = (center_x - side_gap, middle_y)
    einstein_center = (center_x + side_gap, middle_y)
    dolphin_center = (center_x, bottom_y)

    mouse_pos = pygame.mouse.get_pos()

    # Egg Catcher with hover effect
    egg_hover = pygame.Rect(egg_center[0] - circle_radius, egg_center[1] - circle_radius,
                            circle_radius*2, circle_radius*2).collidepoint(mouse_pos)
    egg_color = LIGHT_ORANGE if egg_hover else ORANGE
    pygame.draw.circle(screen, egg_color, egg_center, circle_radius)
    if egg_icon:
        screen.blit(egg_icon, (egg_center[0] - icon_size//2, egg_center[1] - icon_size//2))
    pygame.draw.circle(screen, WHITE, egg_center, circle_radius, 2)
    # draw_text("Egg Catcher", button_font, WHITE, egg_center[0], egg_center[1] + circle_radius + 20)

    # Newton's Lab with hover effect
    newton_hover = pygame.Rect(newton_center[0] - circle_radius, newton_center[1] - circle_radius,
                               circle_radius*2, circle_radius*2).collidepoint(mouse_pos)
    newton_color = LIGHT_ORANGE if newton_hover else ORANGE
    pygame.draw.circle(screen, newton_color, newton_center, circle_radius)
    if newton_icon:
        screen.blit(newton_icon, (newton_center[0] - icon_size//2, newton_center[1] - icon_size//2))
    pygame.draw.circle(screen, WHITE, newton_center, circle_radius, 2)
    # draw_text("Newton's Lab", button_font, WHITE, newton_center[0], newton_center[1] + circle_radius + 20)

    # Einstein's Puzzle with hover effect
    einstein_hover = pygame.Rect(einstein_center[0] - circle_radius, einstein_center[1] - circle_radius,
                                 circle_radius*2, circle_radius*2).collidepoint(mouse_pos)
    einstein_color = LIGHT_ORANGE if einstein_hover else ORANGE
    pygame.draw.circle(screen, einstein_color, einstein_center, circle_radius)
    if einstein_icon:
        screen.blit(einstein_icon, (einstein_center[0] - icon_size//2, einstein_center[1] - icon_size//2))
    pygame.draw.circle(screen, WHITE, einstein_center, circle_radius, 2)
    # draw_text("Einstein's Puzzle", button_font, WHITE, einstein_center[0], einstein_center[1] + circle_radius + 20)

    # Dolphin Game with hover effect
    dolphin_hover = pygame.Rect(dolphin_center[0] - circle_radius, dolphin_center[1] - circle_radius,
                               circle_radius*2, circle_radius*2).collidepoint(mouse_pos)
    dolphin_color = LIGHT_DOLPHIN_BLUE if dolphin_hover else DOLPHIN_BLUE
    pygame.draw.circle(screen, dolphin_color, dolphin_center, circle_radius)
    if dolphin_icon:
        screen.blit(dolphin_icon, (dolphin_center[0] - icon_size//2, dolphin_center[1] - icon_size//2))
    pygame.draw.circle(screen, WHITE, dolphin_center, circle_radius, 2)
    # draw_text("Dolphin Game", button_font, WHITE, dolphin_center[0], dolphin_center[1] + circle_radius + 20)

    click_area_size = circle_radius * 2
    return {
        "back": back_rect,
        "egg": pygame.Rect(egg_center[0] - circle_radius, egg_center[1] - circle_radius, click_area_size, click_area_size),
        "newton": pygame.Rect(newton_center[0] - circle_radius, newton_center[1] - circle_radius, click_area_size, click_area_size),
        "einstein": pygame.Rect(einstein_center[0] - circle_radius, einstein_center[1] - circle_radius, click_area_size, click_area_size),
        "dolphin": pygame.Rect(dolphin_center[0] - circle_radius, dolphin_center[1] - circle_radius, click_area_size, click_area_size)
    }

def instructions_screen():
    global instruction_scroll_y, max_scroll_y
    
    screen.fill(BLACK)
    update_particles()
    
    # Create back button and title
    back_rect = create_button("BACK", 20, 20, 100, 40)
    draw_text("INSTRUCTIONS", menu_title_font, WHITE, 400, 80)
    
    # Create scroll buttons
    scroll_up_rect = create_button("▲", 720, 150, 60, 40)
    scroll_down_rect = create_button("▼", 720, 500, 60, 40)
    
    # Define the scrollable area
    scroll_area = pygame.Rect(100, 150, 600, 400)
    pygame.draw.rect(screen, (30, 30, 30), scroll_area, border_radius=10)
    pygame.draw.rect(screen, WHITE, scroll_area, width=2, border_radius=10)
    
    # Create a clipping rect for the text area
    screen.set_clip(scroll_area)
    
    instructions = [
        "Dolphins Ocean!",
        "Dive into the ocean adventure where you control a cheerful dolphin on a mission to catch colorful falling balls! Test your reflexes, time your jumps, and rack up the highest score in this fun, fast-paced game!",
        "",
        "Your Mission:",
        "Help the dolphin catch as many falling balls as possible before they hit the water. Every ball you catch boosts your score and keeps the game going!",
        "Move Left: ← Arrow Key",
        "Move Right: → Arrow Key",
        "Jump: ↑↑ Double Arrow Key",
        "Swim Down: ↓ Arrow Key",
        " ",
        "Newton's Apple Garden",
        "Objective: Help Newton, a small apple, bounce up and reach different platforms. Avoid falling and catch apples to score points.",
        "Keep Newton from falling off the screen, land on platforms, and catch apples to score points.",
        "Use the Left Arrow key to move Newton left.",
        "Use the Right Arrow key to move Newton right.",
        " ",
        "Einstein Lab",
        "The main goal of the game is to help Einstein catch light bulbs falling from the top of the screen. Each light bulb caught gives you points.",
        "Use the Left Arrow key to move Einstein left.",
        "Use the Right Arrow key to move Einstein right.",
        " ",
        "Birds Open Home",
        "The goal of the game is to catch falling eggs with the basket. Each egg you catch gives you points.",
        "Use the Left Arrow key to move the basket left.",
        "Use the Right Arrow key to move the basket right.",
        " ",
        "Game Controls:",
        "- Arrow keys for movement",
        "- Spacebar for actions",
        "- ESC to pause/quit"
    ]
    
    # Calculate total height of all text
    total_height = 0
    rendered_lines = []
    
    for line in instructions:
        if line.strip():  # Skip empty lines for height calculation
            result, line_height = draw_text(line, instruction_font, WHITE, 
                                           scroll_area.left + 20, 0, 
                                           align="left", max_width=scroll_area.width - 40)
            rendered_lines.append((line, result, line_height))
            total_height += line_height + 10  # Add some padding between lines
        else:
            # Just add some space for empty lines
            rendered_lines.append((line, None, 20))
            total_height += 20
    
    # Calculate maximum scroll value
    max_scroll_y = max(0, total_height - scroll_area.height)
    
    # Render the text with scrolling
    current_y = scroll_area.top + 20 - instruction_scroll_y
    
    for line, result, line_height in rendered_lines:
        if line.strip():  # If not an empty line
            for text_surface, text_rect in result:
                # Only render if within the visible area
                adjusted_rect = text_rect.copy()
                adjusted_rect.y = current_y
                if (adjusted_rect.bottom > scroll_area.top and 
                    adjusted_rect.top < scroll_area.bottom):
                    screen.blit(text_surface, adjusted_rect)
            current_y += line_height + 10
        else:
            # Just add space for empty lines
            current_y += 20
    
    # Reset the clipping rect
    screen.set_clip(None)
    
    # Draw scroll indicators if needed
    if max_scroll_y > 0:
        # Draw scroll bar background
        scroll_bar_bg = pygame.Rect(scroll_area.right + 10, scroll_area.top, 10, scroll_area.height)
        pygame.draw.rect(screen, (50, 50, 50), scroll_bar_bg, border_radius=5)
        
        # Draw scroll bar handle
        scroll_ratio = instruction_scroll_y / max_scroll_y
        handle_height = max(30, scroll_area.height * (scroll_area.height / total_height))
        handle_pos = scroll_area.top + (scroll_area.height - handle_height) * scroll_ratio
        scroll_handle = pygame.Rect(scroll_area.right + 10, handle_pos, 10, handle_height)
        pygame.draw.rect(screen, LIGHT_BLUE, scroll_handle, border_radius=5)
    
    return {
        "back": back_rect,
        "scroll_up": scroll_up_rect,
        "scroll_down": scroll_down_rect,
        "scroll_area": scroll_area
    }

def settings_screen():
    screen.fill(BLACK)
    update_particles()
    back_rect = create_button("BACK", 20, 20, 100, 40)
    draw_text("SETTINGS", menu_title_font, WHITE, 400, 80)

    draw_text("Difficulty:", option_font, WHITE, 200, 200, "left")
    create_button("EASY", 350, 180, 120, 40)
    create_button("MEDIUM", 480, 180, 120, 40, ORANGE, LIGHT_ORANGE)
    create_button("HARD", 610, 180, 120, 40)

    draw_text("Sound:", option_font, WHITE, 200, 260, "left")
    create_button("ON", 350, 240, 120, 40, ORANGE, LIGHT_ORANGE)
    create_button("OFF", 480, 240, 120, 40)

    draw_text("Fullscreen:", option_font, WHITE, 200, 320, "left")
    create_button("ON", 350, 300, 120, 40)
    create_button("OFF", 480, 300, 120, 40, ORANGE, LIGHT_ORANGE)

    return {"back": back_rect}

def launch_game(game_file):
    try:
        pygame.quit()
        subprocess.Popen([sys.executable, game_file])
        sys.exit()
    except Exception as e:
        print(f"Error launching game: {e}")
        pygame.init()
        screen = pygame.display.set_mode((800, 600))

def main():
    global current_screen, instruction_scroll_y
    running = True
    
    # For mouse wheel scrolling
    scroll_speed = 20
    
    while running:
        mouse_click = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_click = event.pos
                elif event.button == 4 and current_screen == "instructions":  # Mouse wheel up
                    instruction_scroll_y = max(0, instruction_scroll_y - scroll_speed)
                elif event.button == 5 and current_screen == "instructions":  # Mouse wheel down
                    instruction_scroll_y = min(max_scroll_y, instruction_scroll_y + scroll_speed)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if current_screen == "mode_selection":
                        current_screen = "home"
                    elif current_screen != "home":
                        current_screen = "home"
                    else:
                        running = False
                # Add keyboard scrolling for instructions
                elif current_screen == "instructions":
                    if event.key == pygame.K_UP:
                        instruction_scroll_y = max(0, instruction_scroll_y - scroll_speed)
                    elif event.key == pygame.K_DOWN:
                        instruction_scroll_y = min(max_scroll_y, instruction_scroll_y + scroll_speed)
                    elif event.key == pygame.K_PAGE_UP:
                        instruction_scroll_y = max(0, instruction_scroll_y - 4 * scroll_speed)
                    elif event.key == pygame.K_PAGE_DOWN:
                        instruction_scroll_y = min(max_scroll_y, instruction_scroll_y + 4 * scroll_speed)
                    elif event.key == pygame.K_HOME:
                        instruction_scroll_y = 0
                    elif event.key == pygame.K_END:
                        instruction_scroll_y = max_scroll_y

        elements = {}
        if current_screen == "home":
            elements = home_screen()
            if mouse_click:
                if elements["play"].collidepoint(mouse_click):
                    current_screen = "mode_selection"  # Changed to go to mode selection first
                elif elements["settings"].collidepoint(mouse_click):
                    current_screen = "settings"
                elif elements["instructions"].collidepoint(mouse_click):
                    current_screen = "instructions"
                    instruction_scroll_y = 0  # Reset scroll position when entering instructions
                elif elements["quit"].collidepoint(mouse_click):
                    running = False
        elif current_screen == "mode_selection":
            elements = mode_selection_screen()
            if mouse_click:
                if elements["normal"].collidepoint(mouse_click):
                    current_screen = "select"  # Normal mode goes to game selection
                elif elements["hand_gesture"].collidepoint(mouse_click):
                    # Here you would implement hand gesture mode functionality
                    # For now, we'll just print a message
                    print("Hand gesture mode selected - functionality not implemented")
                elif elements["back"].collidepoint(mouse_click):
                    current_screen = "home"
        elif current_screen == "select":
            elements = select_game_screen()
            if mouse_click:
                if elements["back"].collidepoint(mouse_click):
                    current_screen = "mode_selection"  # Go back to mode selection instead of home
                elif elements["egg"].collidepoint(mouse_click):
                    launch_game("egg_game_play.py")
                elif elements["newton"].collidepoint(mouse_click):
                    launch_game("apple_game_play.py")
                elif elements["einstein"].collidepoint(mouse_click):
                    launch_game("bulb_game_play.py")
                elif elements["dolphin"].collidepoint(mouse_click):
                    launch_game("dolphin_game_play.py")
        elif current_screen == "instructions":
            elements = instructions_screen()
            if mouse_click:
                if elements["back"].collidepoint(mouse_click):
                    current_screen = "home"
                elif elements["scroll_up"].collidepoint(mouse_click):
                    instruction_scroll_y = max(0, instruction_scroll_y - scroll_speed * 2)
                elif elements["scroll_down"].collidepoint(mouse_click):
                    instruction_scroll_y = min(max_scroll_y, instruction_scroll_y + scroll_speed * 2)
                # Check if clicked on scroll bar area for direct scrolling
                elif pygame.Rect(elements["scroll_area"].right + 10, elements["scroll_area"].top, 10, elements["scroll_area"].height).collidepoint(mouse_click):
                    # Calculate position based on click
                    click_ratio = (mouse_click[1] - elements["scroll_area"].top) / elements["scroll_area"].height
                    instruction_scroll_y = min(max_scroll_y, max(0, int(max_scroll_y * click_ratio)))
        elif current_screen == "settings":
            elements = settings_screen()
            if mouse_click and elements["back"].collidepoint(mouse_click):
                current_screen = "home"

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
