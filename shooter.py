import pygame
import os

# --- Game Constants ---
WIDTH, HEIGHT = 700, 500
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


def run_shooter(screen):
    # Load images
    yellow_ship = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(
            "images/Shooter/spaceship_yellow.png"), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90
    )
    red_ship = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load(
            "images/Shooter/spaceship_red.png"), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270
    )
    space_bg = pygame.transform.scale(
        pygame.image.load("images/Shooter/space.png"), (WIDTH, HEIGHT))

    # Default font
    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 80)

    red = pygame.Rect(500, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width,
                        yellow.y + yellow.height // 2 - 2,
                        10,
                        5,
                    )
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 1

            if event.type == YELLOW_HIT:
                yellow_health -= 1

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(screen, winner_text, big_font)
            pygame.time.wait(2000)
            return

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        # Draw everything
        screen.blit(space_bg, (0, 0))
        pygame.draw.rect(screen, BLACK, BORDER)

        red_health_text = font.render(f"Health: {red_health}", True, WHITE)
        yellow_health_text = font.render(
            f"Health: {yellow_health}", True, WHITE)
        screen.blit(red_health_text,
                    (WIDTH - red_health_text.get_width() - 10, 10))
        screen.blit(yellow_health_text, (10, 10))

        screen.blit(yellow_ship, (yellow.x, yellow.y))
        screen.blit(red_ship, (red.x, red.y))

        for bullet in red_bullets:
            pygame.draw.rect(screen, RED, bullet)
        for bullet in yellow_bullets:
            pygame.draw.rect(screen, YELLOW, bullet)

        pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets[:]:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets[:]:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(screen, text, font):
    draw_text = font.render(text, True, WHITE)
    screen.blit(
        draw_text,
        (
            WIDTH / 2 - draw_text.get_width() / 2,
            HEIGHT / 2 - draw_text.get_height() / 2,
        ),
    )
    pygame.display.update()


# For standalone testing:
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    run_shooter(screen)
