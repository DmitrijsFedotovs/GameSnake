import pygame
import random
import sys
pygame.init()
CELL = 20
COLS = 32
ROWS = 26
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL + 80
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Metal Snake Solid")
clock = pygame.time.Clock()
BLACK = (12, 15, 20)
DARK = (23, 29, 38)
GREEN = (60, 220, 120)
LIME = (140, 255, 100)
RED = (240, 65, 65)
GOLD = (255, 200, 40)
STEEL = (105, 125, 145)
WHITE = (235, 240, 245)
CYAN = (50, 220, 230)
font = pygame.font.SysFont("consolas", 22, bold=True)
small_font = pygame.font.SysFont("consolas", 16)
title_font = pygame.font.SysFont("consolas", 42, bold=True)
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"
state = MENU
def random_cell(snake, occupied=None):
    occupied = set(occupied or [])
    occupied.update(snake)
    while True:
        pos = (
            random.randrange(COLS),
            random.randrange(ROWS)
        )
        if pos not in occupied:
            return pos
def draw_cell(pos, color, inset=2):
    x, y = pos
    pygame.draw.rect(
        screen,
        color,
        (
            x * CELL + inset,
            y * CELL + inset + 80,
            CELL - inset * 2,
            CELL - inset * 2
        ),
        border_radius=4
    )
def draw_text(text, font_obj, color, x, y, center=True):
    surface = font_obj.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)
def reset_game():
    global snake, direction, next_direction
    global food, speed_fruit, bonus, wall
    global score, base_speed, speed_until
    global last_move, last_spawn, last_bonus
    global state
    snake = [(COLS // 2, ROWS // 2),
             (COLS // 2 - 1, ROWS // 2),
             (COLS // 2 - 2, ROWS // 2)]

    direction = (1, 0)
    next_direction = direction
    food = random_cell(snake)
    speed_fruit = None
    bonus = None
    wall = []
    score = 0
    base_speed = 8
    speed_until = 0
    last_move = pygame.time.get_ticks()
    last_spawn = pygame.time.get_ticks()
    last_bonus = pygame.time.get_ticks()
    state = PLAYING
def spawn_wall():
    global wall
    occupied = set(snake)
    occupied.add(food)
    if speed_fruit:
        occupied.add(speed_fruit)
    if bonus:
        occupied.add(bonus)
    for _ in range(100):
        x = random.randint(3, COLS - 4)
        y = random.randint(3, ROWS - 4)
        candidate = [
            (x, y),
            (x + 1, y),
            (x + 2, y)
        ]
        if not any(pos in occupied for pos in candidate):
            wall = candidate
            return
def draw_background():
    screen.fill(BLACK)
    for x in range(COLS + 1):
        pygame.draw.line(
            screen, DARK,
            (x * CELL, 80),
            (x * CELL, HEIGHT)
        )
    for y in range(ROWS + 1):
        pygame.draw.line(
            screen, DARK,
            (0, y * CELL + 80),
            (WIDTH, y * CELL + 80)
        )
    pygame.draw.rect(screen, (30, 38, 48), (0, 0, WIDTH, 80))
    pygame.draw.line(screen, STEEL, (0, 79), (WIDTH, 79), 2)
    draw_text(
        "METAL SNAKE SOLID",
        font, CYAN, 12, 10, center=False
    )
    draw_text(
        f"SCORE: {score}",
        small_font, WHITE, 12, 47, center=False
    )
    now = pygame.time.get_ticks()
    if now < speed_until:
        remaining = (speed_until - now) / 1000
        status = f"SPEED BOOST: {remaining:.1f}s"
        color = GOLD
    else:
        status = "TACTICAL MODE"
        color = GREEN
    draw_text(
        status, small_font, color,
        WIDTH - 12, 47, center=False
    )
    status_surface = small_font.render(status, True, color)
    screen.blit(
        status_surface,
        (WIDTH - status_surface.get_width() - 12, 47)
    )
def draw_game():
    draw_background()
    draw_cell(food, RED, 3)
    if speed_fruit:
        draw_cell(speed_fruit, GOLD, 2)
        pygame.draw.circle(
            screen, WHITE,
            (
                speed_fruit[0] * CELL + CELL // 2,
                speed_fruit[1] * CELL + 80 + CELL // 2
            ),
            3
        )
    if bonus:
        draw_cell(bonus, CYAN, 4)
    for pos in wall:
        draw_cell(pos, STEEL, 1)
    for i, pos in enumerate(snake):
        draw_cell(pos, LIME if i == 0 else GREEN)

    pygame.display.flip()
def draw_overlay(title, subtitle, hint):
    draw_game()
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 185))
    screen.blit(overlay, (0, 0))
    draw_text(title, title_font, CYAN, WIDTH // 2, HEIGHT // 2 - 65)
    draw_text(subtitle, font, WHITE, WIDTH // 2, HEIGHT // 2)
    draw_text(hint, small_font, GOLD, WIDTH // 2, HEIGHT // 2 + 45)
    pygame.display.flip()
while True:
    now = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if state == MENU:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    reset_game()
            elif state == GAME_OVER:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    state = MENU
            elif state == PLAYING:
                if event.key in (pygame.K_UP, pygame.K_w):
                    if direction != (0, 1):
                        next_direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if direction != (0, -1):
                        next_direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    if direction != (1, 0):
                        next_direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if direction != (-1, 0):
                        next_direction = (1, 0)
                elif event.key == pygame.K_ESCAPE:
                    state = MENU
    if state == MENU:
        screen.fill(BLACK)
        draw_text(
            "METAL SNAKE SOLID",
            title_font, CYAN, WIDTH // 2, HEIGHT // 2 - 100
        )
        draw_text(
            "TACTICAL SNAKE OPERATION",
            small_font, GREEN, WIDTH // 2, HEIGHT // 2 - 48
        )
        draw_text(
            "ARROW KEYS / WASD - MOVE",
            font, WHITE, WIDTH // 2, HEIGHT // 2 + 10
        )
        draw_text(
            "ENTER - START MISSION",
            font, GOLD, WIDTH // 2, HEIGHT // 2 + 55
        )
        draw_text(
            "ESC - RETURN TO MENU",
            small_font, STEEL, WIDTH // 2, HEIGHT // 2 + 95
        )
        pygame.display.flip()
    elif state == PLAYING:
        if speed_fruit is None and now - last_spawn > 7000:
            speed_fruit = random_cell(
                snake, [food] + wall
            )
            last_spawn = now
        if bonus is None and now - last_bonus > 10000:
            bonus = random_cell(
                snake,
                [food] + wall +
                ([speed_fruit] if speed_fruit else [])
            )
            last_bonus = now
        if not wall and now - last_spawn > 14000:
            spawn_wall()
        current_speed = (
            base_speed * 1.8
            if now < speed_until
            else base_speed
        )
        interval = 1000 / current_speed
        if now - last_move >= interval:
            last_move = now
            direction = next_direction
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)
            if (
                new_head[0] < 0 or new_head[0] >= COLS
                or new_head[1] < 0 or new_head[1] >= ROWS
            ):
                state = GAME_OVER
            elif new_head in wall:
                state = GAME_OVER

            else:
                eating = new_head == food
                growing = (
                    eating
                    or new_head == speed_fruit
                    or new_head == bonus
                )
                body = snake if growing else snake[:-1]
                if new_head in body:
                    state = GAME_OVER
                else:
                    snake.insert(0, new_head)
                    if eating:
                        score += 10
                        food = random_cell(
                            snake,
                            wall +
                            ([speed_fruit] if speed_fruit else []) +
                            ([bonus] if bonus else [])
                        )
                    elif new_head == speed_fruit:
                        score += 20
                        speed_fruit = None
                        speed_until = now + 5000
                        last_spawn = now
                    elif new_head == bonus:
                        score += 50
                        bonus = None
                        last_bonus = now
                    else:
                        snake.pop()
                    base_speed = min(16, 8 + score // 100)

        draw_game()
    elif state == GAME_OVER:
        draw_overlay(
            "MISSION FAILED",
            f"FINAL SCORE: {score}",
            "PRESS R TO RESTART"
        )
    clock.tick(60)