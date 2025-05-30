import pygame
import random
import math
import os

# Constants
WIDTH, HEIGHT = 700, 500
BOX_X = 50
BOX_Y = 80
BOX_WIDTH = 600
BOX_HEIGHT = 400

PADDLE_WIDTH, PADDLE_HEIGHT = 120, 30
BALL_RADIUS = 10
BRICK_ROWS, BRICK_COLS = 6, 8
BRICK_WIDTH = BOX_WIDTH // BRICK_COLS
BRICK_HEIGHT = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def load_and_scale_image(path, size):
    try:
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.smoothscale(img, size)
        return img
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return None


def calculate_ball_direction(hit_x, paddle_x, paddle_width, speed):
    relative_hit_pos = (
        hit_x - (paddle_x + paddle_width / 2)) / (paddle_width / 2)
    relative_hit_pos = max(-1, min(1, relative_hit_pos))
    max_angle = math.pi / 3
    angle = relative_hit_pos * max_angle
    dx = speed * math.sin(angle)
    dy = -speed * math.cos(angle)
    return dx, dy


def create_bricks(brick_img):
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            rect = pygame.Rect(
                BOX_X + col * BRICK_WIDTH,
                BOX_Y + row * BRICK_HEIGHT,
                BRICK_WIDTH - 5,
                BRICK_HEIGHT - 5,
            )
            bricks.append((rect, brick_img))
    return bricks


def run_brickout(screen):
    pygame.display.set_caption("Brickout")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 54)

    # Load images
    bg_img = load_and_scale_image(
        'images/brickout/background.png', (WIDTH, HEIGHT))
    brick_img = load_and_scale_image(
        'images/brickout/brick.png', (BRICK_WIDTH-5, BRICK_HEIGHT-5))
    ball_img = load_and_scale_image(
        'images/brickout/ball.png', (BALL_RADIUS * 2 + 10, BALL_RADIUS * 2))
    paddle_img = load_and_scale_image(
        'images/brickout/paddle.png', (PADDLE_WIDTH, PADDLE_HEIGHT))

    # Paddle (centered in box)
    paddle = pygame.Rect(
        BOX_X + (BOX_WIDTH - PADDLE_WIDTH) // 2,
        BOX_Y + BOX_HEIGHT - PADDLE_HEIGHT - 10,
        PADDLE_WIDTH, PADDLE_HEIGHT
    )
    paddle_speed = 10

    # Ball (centered in box)
    ball_x = BOX_X + BOX_WIDTH // 2
    ball_y = BOX_Y + BOX_HEIGHT // 2 + 80
    ball_dx = random.choice([-4, 4])
    ball_dy = -4

    # Bricks
    bricks = create_bricks(brick_img)
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.x -= paddle_speed
            if paddle.x < BOX_X:
                paddle.x = BOX_X
        if keys[pygame.K_RIGHT]:
            paddle.x += paddle_speed
            if paddle.x > BOX_X + BOX_WIDTH - PADDLE_WIDTH:
                paddle.x = BOX_X + BOX_WIDTH - PADDLE_WIDTH

        # Ball movement
        ball_x += ball_dx
        ball_y += ball_dy

        # Ball-paddle collision (with angle)
        if paddle.collidepoint(ball_x, ball_y + BALL_RADIUS):
            speed = math.hypot(ball_dx, ball_dy)
            ball_dx, ball_dy = calculate_ball_direction(
                ball_x, paddle.x, PADDLE_WIDTH, speed)

        # Wall collision (box boundaries)
        if ball_x - BALL_RADIUS <= BOX_X or ball_x + BALL_RADIUS >= BOX_X + BOX_WIDTH:
            ball_dx = -ball_dx
        if ball_y - BALL_RADIUS <= BOX_Y:
            ball_dy = -ball_dy

        # Brick collision
        hit_index = None
        for i, (brick_rect, _) in enumerate(bricks):
            if (
                brick_rect.collidepoint(ball_x, ball_y - BALL_RADIUS)
                or brick_rect.collidepoint(ball_x, ball_y + BALL_RADIUS)
                or brick_rect.collidepoint(ball_x - BALL_RADIUS, ball_y)
                or brick_rect.collidepoint(ball_x + BALL_RADIUS, ball_y)
            ):
                hit_index = i
                break
        if hit_index is not None:
            bricks.pop(hit_index)
            score += 10
            ball_dy = -ball_dy

        # Lose condition (ball falls below box)
        if ball_y - BALL_RADIUS > BOX_Y + BOX_HEIGHT:
            running = False  # Ball fell below paddle

        # Win condition
        if not bricks:
            running = False  # All bricks destroyed

        # Drawing
        if bg_img:
            screen.blit(bg_img, (0, 0))
        else:
            screen.fill(BLACK)

        # Draw bordered box
        pygame.draw.rect(screen, (150, 150, 255),
                         (BOX_X-3, BOX_Y-3, BOX_WIDTH+6, BOX_HEIGHT+6), 3)

        # Draw title above the box
        title_text = title_font.render("Brickout", True, (0, 200, 255))
        screen.blit(title_text, (WIDTH // 2 -
                    title_text.get_width() // 2, BOX_Y - 60))

        # Draw bricks
        for brick_rect, brick_img in bricks:
            if brick_img:
                screen.blit(brick_img, brick_rect)
            else:
                pygame.draw.rect(screen, (255, 215, 0), brick_rect)

        # Draw paddle
        if paddle_img:
            screen.blit(paddle_img, paddle)
        else:
            pygame.draw.rect(screen, WHITE, paddle)

        # Draw ball
        if ball_img:
            screen.blit(ball_img, (int(ball_x - BALL_RADIUS),
                        int(ball_y - BALL_RADIUS)))
        else:
            pygame.draw.circle(screen, (220, 20, 60),
                               (int(ball_x), int(ball_y)), BALL_RADIUS)

        # Draw score (top left inside box)
        score_text = font.render(f"Score: {score}", True, (150, 150, 255))
        screen.blit(score_text, (BOX_X+BOX_WIDTH - 100, BOX_Y - 30))
        pygame.display.flip()
        clock.tick(60)

    # Game Over / Win screen
    screen.blit(bg_img, (0, 0)) if bg_img else screen.fill(BLACK)
    pygame.draw.rect(screen, (150, 150, 255),
                     (BOX_X-3, BOX_Y-3, BOX_WIDTH+6, BOX_HEIGHT+6), 3)

    title_text = title_font.render("Brickout", True, (0, 200, 255))

    screen.blit(title_text, (WIDTH // 2 -
                title_text.get_width() // 2, BOX_Y - 60))
    msg = "You Win!" if not bricks else "Game Over!"

    over_text = font.render(f"{msg} Score: {score}", True, (255, 215, 0))
    screen.blit(over_text, (WIDTH // 2 -
                over_text.get_width() // 2, HEIGHT // 2 - 30))

    prompt = font.render("Press ESC to return to menu", True, WHITE)
    screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 10))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False
            elif event.type == pygame.QUIT:
                waiting = False


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    run_brickout(screen)
