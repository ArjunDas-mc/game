import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple 2D Game")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up game clock
clock = pygame.time.Clock()

# Player settings
player_width = 50
player_height = 50
player_speed = 5

# Obstacle settings
obstacle_width = 50
obstacle_height = 50
obstacle_speed = 5
obstacle_frequency = 25  # Higher value = fewer obstacles

# Font for displaying text
font = pygame.font.SysFont("Arial", 30)

# Function to display the score
def display_score(score):
    score_text = font.render("Score: {}".format(score), True, BLACK)
    screen.blit(score_text, (10, 10))

# Function to create a new obstacle
def create_obstacle():
    return pygame.Rect(random.randint(0, WIDTH - obstacle_width), -obstacle_height, obstacle_width, obstacle_height)

# Game loop
def game_loop():
    while True:  # Infinite loop to restart the game after each game over
        # Reset player position and game state
        player_x = WIDTH // 2 - player_width // 2
        player_y = HEIGHT - player_height - 10
        run_game = True
        score = 0
        obstacles = []

        while run_game:  # Main game loop
            screen.fill(WHITE)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return  # Exit the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart if 'R' is pressed
                        return  # Restart the game loop

            # Get the state of the keys (moving left/right)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
                player_x += player_speed

            # Create obstacles randomly
            if random.randint(1, obstacle_frequency) == 1:
                obstacles.append(create_obstacle())

            # Move obstacles and check for collisions
            for obstacle in obstacles[:]:
                obstacle.y += obstacle_speed
                if obstacle.colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
                    print("Collision Detected!")  # Debugging collision
                    run_game = False  # End the game if collision happens
                if obstacle.y > HEIGHT:
                    obstacles.remove(obstacle)
                    score += 1  # Increase score when an obstacle passes

            # Draw obstacles
            for obstacle in obstacles:
                pygame.draw.rect(screen, RED, obstacle)

            # Draw the player
            pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

            # Display score
            display_score(score)

            # Update the screen
            pygame.display.update()

            # Cap the frame rate
            clock.tick(60)

        # End game screen
        game_over_text = font.render("Game Over!", True, BLACK)
        score_text = font.render("Final Score: {}".format(score), True, BLACK)
        restart_text = font.render("Press 'R' to Restart", True, BLACK)
        screen.fill(WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 1.5))
        pygame.display.update()

        # Wait for restart key or quit
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return  # Exit the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart if 'R' is pressed
                        break  # Break out of the waiting loop to restart the game

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                break  # Break out of the main game loop to restart

        pygame.time.wait(1000)  # Wait for a second before restarting

# Run the game loop
game_loop()
