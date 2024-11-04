import pygame
import random
import string
import math

# Initialize Pygame
pygame.init()

# Get native device resolution for full-screen display
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Searching for Characters")
font = pygame.font.SysFont(None, 48)
clock = pygame.time.Clock()

# Load background image
background_image = pygame.image.load("Tests/Background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Load flying images
flying_image_1 = pygame.image.load("Tests/Diode.png")
flying_image_1 = pygame.transform.scale(flying_image_1, (50, 50))
flying_image_1.set_alpha(128)

flying_image_2 = pygame.image.load("Tests/Buzzer.png")
flying_image_2 = pygame.transform.scale(flying_image_2, (50, 50))
flying_image_2.set_alpha(128)

# Load Struktorizer image
struktorizer_image = pygame.image.load("Tests/Struktorizer.png")  # Ensure the correct path
struktorizer_image = pygame.transform.scale(struktorizer_image, (500, 700))  # Resize to fit if needed
struktorizer_image.set_alpha(200)  # Set alpha for transparency

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FPS = 60

# The text to search for
target_text = '-Yo Yo Yo, Goodbye and have a nice day- -CySy-!!!'

# Characters orbit around text
orbiting_chars = ['<', 'L', 'E', 'R', 'N', 'E', 'N>', '<', 'L', 'E', 'R', 'N', 'E', 'N>', '<', 'L', 'E', 'R', 'N', 'E', 'N>']
orbit_radius = 400
orbit_speed = 0.01
angles = [i * (2 * math.pi / len(orbiting_chars)) for i in range(len(orbiting_chars))]

# Target character class
class TargetChar:
    def __init__(self, target_char, index):
        self.char = random.choice(string.printable)
        self.target_char = target_char
        self.index = index
        self.reached_target = False
        self.reset_position()

    def reset_position(self):
        if random.choice([True, False]):
            self.x = random.randint(-100, screen_width + 100)
            self.y = random.choice([-100, random.randint(0, screen_height + 100)])
        else:
            self.x = random.choice([-100, random.randint(0, screen_width + 100)])
            self.y = random.randint(-100, screen_height + 100)

    def move_towards_target(self, target_x, target_y):
        if not self.reached_target:
            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.hypot(dx, dy)

            # If distance is small enough, snap to target and change character
            if distance < 5:  # Adjust the threshold for reaching the target
                self.reached_target = True
                self.char = self.target_char  # Change to intended character
                self.x, self.y = target_x, target_y  # Snap to target position
            else:
                self.x += dx / distance * 4  # Increased speed
                self.y += dy / distance * 4  # Increased speed

    def draw(self, screen, font, visible):
        if visible:  # Only draw if visible
            text_surface = font.render(self.char, True, RED)
            screen.blit(text_surface, (self.x, self.y))

# Flying character class
class FlyingChar:
    def __init__(self):
        self.formulas = [
            "V = I * R", "I = V / R", "R = V / I",
            "P = V * I", "P = I^2 * R", "P = V^2 / R",
            "Q = I * t", "C = Q / V", "F = m * a",
            "E = mc^2", "S = B * log2(1 + SNR)", "R = 1 / (C * f)",
            "X_L = 2 * π * f * L", "X_C = 1 / (2 * π * f * C)",
            "N = V_out / V_in", "A = π * r^2", "D = R * T",
            "H = -∑(p * log2(p))",
        ]
        self.char = random.choice(self.formulas)
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        # Bounce off screen edges
        if self.x < 0 or self.x > screen_width:
            self.speed_x = -self.speed_x
        if self.y < 0 or self.y > screen_height:
            self.speed_y = -self.speed_y

    def draw(self, screen, font, image):
        text_surface = font.render(self.char, True, WHITE)
        screen.blit(text_surface, (self.x, self.y))
        screen.blit(image, (self.x, self.y))

# Create target characters and flying characters
target_chars = [TargetChar(target_text[i], i) for i in range(len(target_text))]
flying_chars = [FlyingChar() for _ in range(100)]  # Create 100 flying characters

# Calculate starting x-position and total width for target text
total_text_width = sum(font.size(char)[0] for char in target_text)
start_x = (screen_width - total_text_width) // 2
center_y = screen_height // 2

# Main loop
running = True
visible = True  # Variable to control text visibility
blink_timer = 0  # Timer for controlling blink rate
blink_rate = 30  # Adjust this for how fast you want the text to blink

while running:
    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Draw flying characters
    for i, fc in enumerate(flying_chars):
        fc.move()
        if i % 2 == 0:
            fc.draw(screen, font, flying_image_1)
        else:
            fc.draw(screen, font, flying_image_2)

    # Draw target characters moving to the center
    for tc in target_chars:
        target_x = start_x + sum(font.size(target_text[i])[0] for i in range(tc.index))
        tc.move_towards_target(target_x, center_y)
        tc.draw(screen, font, visible)  # Pass visibility to draw method

    # Draw orbiting characters in blue
    for i, char in enumerate(orbiting_chars):
        angle = angles[i]
        x = start_x + total_text_width // 2 + orbit_radius * math.cos(angle)
        y = center_y + orbit_radius * math.sin(angle)
        char_surface = font.render(char, True, BLUE)  # Set orbiting character color to blue
        screen.blit(char_surface, (x, y))
        angles[i] += orbit_speed  # Increment angle

    # Draw Struktorizer image in bottom right corner with transparency
    struktorizer_x = screen_width - struktorizer_image.get_width() - 0  # 1 pixel from the right edge
    struktorizer_y = screen_height - struktorizer_image.get_height() - 0  # 1 pixel from the bottom edge
    screen.blit(struktorizer_image, (struktorizer_x, struktorizer_y))

    # Update blink state
    blink_timer += 1
    if blink_timer >= blink_rate:
        visible = not visible  # Toggle visibility
        blink_timer = 0  # Reset timer

    # Update display and limit FPS
    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
