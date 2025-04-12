# pacman recreated in python using pygame

import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_WIDTH = 448  # Pac-Man's original width
SCREEN_HEIGHT = 576  # Pac-Man's original height
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

# Define colors
BLACK = (0, 0, 0)
WALL_COLOR = (0, 0, 255)
PACMAN_COLOR = (255, 255, 0)
PELLET_COLOR = (255, 255, 255)

# Set up the clock
clock = pygame.time.Clock()

# Maze layout
maze = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "X..........X..........X",
    "X.XXXX.XXX.X.XXX.XXXX.X",
    "XoXXXX.XXX.X.XXX.XXXXoX",
    "X.XXXX.XXX.X.XXX.XXXX.X",
    "X.....................X",
    "X.XXXX.X.XXXXX.X.XXXX.X",
    "X......X...X...X......X",
    "XXXXXX.XXX X XXX.XXXXXX",
    "     X.X       X.X     ",
    "     X.X XXXXX X.X     ",
    "XXXXXX.X XXXXX X.XXXXXX",
    "      .          .     ",
    "XXXXXX.X XXXXX X.XXXXXX",
    "     X.X XXXXX X.X     ",
    "     X.X       X.X     ",
    "XXXXXX.X XXXXX X.XXXXXX",
    "X..........X..........X",
    "X.XXXX.XXX.X.XXX.XXXX.X",
    "Xo...X.....P.....X...oX",
    "XXX.X.X.XXXXX.X.X.XXX.X",
    "X......X...X...X......X",
    "X.XXXXXXXX.X.XXXXXXXX.X",
    "X.....................X",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
]

def draw_maze():
    block_size = 24  # Each block is 24x24 pixels
    for row_index, row in enumerate(maze):
        for col_index, item in enumerate(row):
            x = col_index * block_size
            y = row_index * block_size
            if item == 'X':
                pygame.draw.rect(screen, WALL_COLOR, (x, y, block_size, block_size))
            elif item == '.':
                pygame.draw.circle(screen, PELLET_COLOR, (x + block_size // 2, y + block_size // 2), 3)
            elif item == 'o':
                pygame.draw.circle(screen, PELLET_COLOR, (x + block_size // 2, y + block_size // 2), 6)

# Load images at the top level
try:
    pacman_image = pygame.image.load('images/pacman.png').convert_alpha()
except pygame.error:
    # Fallback if image not found
    pacman_image = pygame.Surface((24, 24), pygame.SRCALPHA)
    pygame.draw.circle(pacman_image, PACMAN_COLOR, (12, 12), 12)

try:
    ghost_image = pygame.image.load('images/ghost.png').convert_alpha()
except pygame.error:
    # Fallback if image not found
    ghost_image = pygame.Surface((24, 24), pygame.SRCALPHA)
    pygame.draw.circle(ghost_image, (255, 0, 0), (12, 12), 12)


# In main function, after losing a life
if pacman.rect.colliderect(ghost.rect):
    lives -= 1
    if lives == 0:
        print("Game Over")
        running = False
    else:
        # Reset positions
        pacman.reset_position()
        for ghost in ghosts:
            ghost.reset_position()

class Pacman:
    def __init__(self, x, y):
        self.start_pos = (x, y)
        self.image = pacman_image
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = pygame.Vector2(0, 0)
        self.speed = 2

    def update(self):
        self.move()
        self.check_collisions()

    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def check_collisions(self):
        block_size = 24
        for row_index, row in enumerate(maze):
            for col_index, item in enumerate(row):
                if item == 'X':
                    x = col_index * block_size
                    y = row_index * block_size
                    wall_rect = pygame.Rect(x, y, block_size, block_size)
                    if self.rect.colliderect(wall_rect):
                        # Reset position if collision detected
                        if self.direction.x > 0:  # Moving right
                            self.rect.right = wall_rect.left
                        if self.direction.x < 0:  # Moving left
                            self.rect.left = wall_rect.right
                        if self.direction.y > 0:  # Moving down
                            self.rect.bottom = wall_rect.top
                        if self.direction.y < 0:  # Moving up
                            self.rect.top = wall_rect.bottom

    def reset_position(self):
        self.rect.center = self.start_pos
        self.direction = pygame.Vector2(0, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def handle_input(pacman):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman.direction = pygame.Vector2(-1, 0)
    elif keys[pygame.K_RIGHT]:
        pacman.direction = pygame.Vector2(1, 0)
    elif keys[pygame.K_UP]:
        pacman.direction = pygame.Vector2(0, -1)
    elif keys[pygame.K_DOWN]:
        pacman.direction = pygame.Vector2(0, 1)
    else:
        pacman.direction = pygame.Vector2(0, 0)

# Load sound files
pygame.mixer.init()
eat_sound = pygame.mixer.Sound('sounds/eat_pellet.wav')
death_sound = pygame.mixer.Sound('sounds/death.wav')

def eat_pellets(pacman):
    global score
    block_size = 24
    row = pacman.rect.centery // block_size
    col = pacman.rect.centerx // block_size
    if maze[row][col] == '.' or maze[row][col] == 'o':
        # Play sound when eating a pellet 
        eat_sound.play()
        if maze[row][col] == '.':
            score += 10
        elif maze[row][col] == 'o':
            score += 50
            # Implement power-up effects here
        maze[row] = maze[row][:col] + ' ' + maze[row][col+1:]



class Ghost:
    def __init__(self, x, y, color):
        self.image = ghost_image.copy()
        self.start_pos = (x, y)        
        # Optionally, tint the ghost image with the provided color
        self.image.fill(color, special_flags=pygame.BLEND_MULT)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = pygame.Vector2(1, 0)
        self.speed = 2

    def update(self):
        self.move()
        self.check_collisions()

    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def check_collisions(self):
        block_size = 24
        for row_index, row in enumerate(maze):
            for col_index, item in enumerate(row):
                if item == 'X':
                    x = col_index * block_size
                    y = row_index * block_size
                    wall_rect = pygame.Rect(x, y, block_size, block_size)
                    if self.rect.colliderect(wall_rect):
                        # Change direction upon collision
                        self.direction *= -1

    def reset_position(self):
        self.rect.center = self.start_pos
        self.direction = pygame.Vector2(1, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Initialize Pac-Man
for row_index, row in enumerate(maze):
    for col_index, item in enumerate(row):
        if item == 'P':
            pacman = Pacman(col_index * 24 + 12, row_index * 24 + 12)
            maze[row_index] = maze[row_index][:col_index] + ' ' + maze[row_index][col_index+1:]

# Initialize ghosts
ghosts = [
    Ghost(12 * 24 + 12, 13 * 24 + 12, (255, 0, 0)),  # Red ghost
    # Add more ghosts as needed
]

score = 0
lives = 3
font = pygame.font.Font(None, 36)

def draw_hud():
    score_text = font.render(f"Score: {score}", True, PELLET_COLOR)
    lives_text = font.render(f"Lives: {lives}", True, PELLET_COLOR)
    screen.blit(score_text, (10, SCREEN_HEIGHT - 30))
    screen.blit(lives_text, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 30))



def chase_pacman(ghost, pacman):
    direction = pygame.Vector2(pacman.rect.center) - pygame.Vector2(ghost.rect.center)
    if direction.length() != 0:
        direction = direction.normalize()
    ghost.direction = direction

def main():
    global lives  # Declare global variable
    running = True
    while running:
        clock.tick(60)  # 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_input(pacman)
        pacman.update()
        eat_pellets(pacman)



        # Rest of the code...
        for ghost in ghosts:
            chase_pacman(ghost, pacman)
            ghost.update()
            # Check collision with Pac-Man
            if pacman.rect.colliderect(ghost.rect):
                # Handle collision (e.g., reduce lives)
                lives -= 1
                # Reset positions or end game
                if lives == 0:
                    print("Game Over")
                    running = False
                else:
                    # Play death sound
                    death_sound.play()
                    # Reset positions
                    pacman.reset_position()
                    for g in ghosts:
                        g.reset_position()

        # Drawing
        screen.fill(BLACK)
        draw_maze()
        pacman.draw(screen)
        for ghost in ghosts:
            ghost.draw(screen)
        draw_hud()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
