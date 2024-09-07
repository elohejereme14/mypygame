# Game Instructions
# There will be incoming box from above that is the enemy
# The player is in the lower part of the screen and should shoot the enemy to destroy them
# 1 score per shoot down enemy
# if the player have been hit by the box or the box hit the ground it will be game over
# the highscore will be save on the textfile

import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('GAME SHOOTER')

# color ng game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = ('#84A59D')
VIOLET = ('#6B3074')

# smoothness ng game
fps = 60
clock = pygame.time.Clock()

# object sa game
player_size = (50, 30)
player_speed = 5
bullet_width = 5
bullet_height = 10
bullet_speed = 7
enemy_size = (50, 30)
num_enemies = 5
initial_enemy_speed = 1.5
enemy_speed_decrease = 0 
min_enemy_speed = 1.5

# Define font
font = pygame.font.SysFont(None, 36)

# File for storing high score
high_score_file = "high_score.txt"

# Game state variables
player = None
bullets = []
enemies = []
enemy_speed = initial_enemy_speed
score = 0
high_score = 0
game_over = True

def load_high_score():
    global high_score
    if os.path.exists(high_score_file):
        with open(high_score_file, "r") as file:
            try:
                high_score = int(file.read())
            except ValueError:
                high_score = 0
    else:
        high_score = 0

def save_high_score():
    global high_score
    with open(high_score_file, "w") as file:
        file.write(str(high_score))

def draw_game_objects():
    # Clear screen
    screen.fill('#F7EDE2')
    
    if game_over:
        # Eto yung start menu
        menu_text = font.render('Press P to Play', True, BLACK)
        screen.blit(menu_text, (width // 2 - 100, height // 2 - 20))
        high_score_text = font.render(f'High Score: {high_score}', True, BLACK)
        screen.blit(high_score_text, (width // 2 - 100, height // 2 + 20))
    else:
        # Player design to
        pygame.draw.rect(screen, VIOLET, player)
        
        # eto yung baril ko
        for bullet in bullets:
            pygame.draw.rect(screen, RED, bullet)
        
        # kalaban design to
        for enemy in enemies:
            pygame.draw.rect(screen, GREEN, enemy)
        
        # score indicator
        score_text = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_text, (10, 10))
        
        # game over screen to
        if game_over:
            game_over_text = font.render('Game Over! Press R to Restart', True, BLACK)
            screen.blit(game_over_text, (width // 2 - 150, height // 2 - 20))
    
    pygame.display.flip()

def handle_player_movement(keys):
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < width:
        player.x += player_speed

def handle_bullets():
    global bullets, score
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.bottom < 0:
            bullets.remove(bullet)
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                spawn_enemy()
                break

def spawn_enemy():
    x = random.randint(0, width - enemy_size[0])
    y = random.randint(-height, -enemy_size[1])
    enemies.append(pygame.Rect(x, y, *enemy_size))

def move_enemies():
    global enemies, game_over, enemy_speed
    for enemy in enemies[:]:
        enemy.y += enemy_speed
        if enemy.top > height:
            game_over = True
        if enemy.colliderect(player):
            game_over = True
        if enemy_speed > min_enemy_speed:
            enemy_speed -= enemy_speed_decrease  # to slow down enemy from the start

def start_game():
    global player, bullets, enemies, enemy_speed, score, game_over
    player = pygame.Rect(width // 2 - player_size[0] // 2, height - player_size[1] - 10, *player_size)
    bullets = []
    enemies = []
    enemy_speed = initial_enemy_speed
    score = 0
    game_over = False
    for _ in range(num_enemies):
        spawn_enemy()

def end_game():
    global high_score
    if score > high_score:
        high_score = score
        save_high_score()

# highscore calling
load_high_score()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and game_over:
                start_game()
            if event.key == pygame.K_r and game_over:
                start_game()
            if event.key == pygame.K_SPACE and not game_over:
                bullet = pygame.Rect(player.centerx - bullet_width // 2, player.top - bullet_height, bullet_width, bullet_height)
                bullets.append(bullet)
    
    if not game_over:
        keys = pygame.key.get_pressed()
        handle_player_movement(keys)
        handle_bullets()
        move_enemies()
    
    draw_game_objects()
    
    if game_over:
        end_game()
    
    clock.tick(fps)
