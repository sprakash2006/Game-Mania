import pygame
import random
import os
import sys

GRAVITY = 0.5
FLAP_STRENGTH = -8
PIPE_GAP = 170
PIPE_SPEED = 3
PIPE_FREQ = 1500  # ms

# Target sizes for gameplay
BIRD_SIZE = (40, 28)      # width, height
PIPE_WIDTH = 70           # width (height will be scaled as needed)
BASE_HEIGHT = 100         # height (width will be scaled to window)

def load_and_scale_image(name, size=None, width=None, height=None):
    path = os.path.join(os.path.dirname(__file__), name)
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.smoothscale(img, size)
        elif width and height:
            img = pygame.transform.smoothscale(img, (width, height))
        elif width:
            scale = width / img.get_width()
            img = pygame.transform.smoothscale(img, (width, int(img.get_height() * scale)))
        elif height:
            scale = height / img.get_height()
            img = pygame.transform.smoothscale(img, (int(img.get_width() * scale), height))
        return img
    except Exception as e:
        print(f"Error loading {name}: {e}")
        sys.exit(1)

def check_collision(bird_rect, pipes, base_y):
    if bird_rect.top < 0 or bird_rect.bottom > base_y:
        return True
    for pipe in pipes:
        if bird_rect.colliderect(pipe['top']) or bird_rect.colliderect(pipe['bottom']):
            return True
    return False

def draw_pipes(screen, pipe_img, pipes):
    for pipe in pipes:
        top_pipe_img = pygame.transform.flip(pipe_img, False, True)
        screen.blit(top_pipe_img, (pipe['top'].x, pipe['top'].y))
        screen.blit(pipe_img, (pipe['bottom'].x, pipe['bottom'].y))

def run_flappybird(screen):
    width, height = screen.get_size()
    BIRD_X = width // 4
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)

    # Load and scale images (use PNG for best results)
    background_img = load_and_scale_image(
        "images/flappybird/background.png", size=(width, height))
    bird_img = load_and_scale_image(
        "images/flappybird/bird.gif", size=BIRD_SIZE)
    pipe_img = load_and_scale_image(
        "images/flappybird/pipe.png", width=PIPE_WIDTH, height=200)
    base_img = load_and_scale_image(
        "images/flappybird/base.png", width=width, height=BASE_HEIGHT)
    base_height = base_img.get_height()
    base_y = height - base_height

    # Game state
    bird_y = height // 2
    bird_vel = -10
    pipes = []
    score = 0
    last_pipe = pygame.time.get_ticks()
    base_x = 0

    # pygame.time.wait(1000)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or \
               (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                bird_vel = FLAP_STRENGTH

        # Bird physics
        bird_vel += GRAVITY
        bird_y += bird_vel
        bird_rect = pygame.Rect(BIRD_X, int(bird_y), bird_img.get_width(), bird_img.get_height())

        # Pipe management
        now = pygame.time.get_ticks()
        if now - last_pipe > PIPE_FREQ:
            last_pipe = now
            pipe_height = random.randint(60, height - PIPE_GAP - base_height - 60)
            top_rect = pygame.Rect(
                width, pipe_height - pipe_img.get_height(), pipe_img.get_width(), pipe_img.get_height())
            bottom_rect = pygame.Rect(
                width, pipe_height + PIPE_GAP, pipe_img.get_width(), pipe_img.get_height())
            pipes.append({'top': top_rect, 'bottom': bottom_rect, 'scored': False})

        for pipe in pipes:
            pipe['top'].x -= PIPE_SPEED
            pipe['bottom'].x -= PIPE_SPEED

        pipes = [p for p in pipes if p['top'].right > 0]

        base_x = (base_x - PIPE_SPEED) % width

        # Collision
        if check_collision(bird_rect, pipes, base_y):
            running = False

        # Score
        for pipe in pipes:
            if not pipe['scored'] and pipe['top'].right < BIRD_X:
                score += 1
                pipe['scored'] = True

        # Drawing
        screen.blit(background_img, (0, 0))
        draw_pipes(screen, pipe_img, pipes)
        # Draw base twice for seamless scrolling
        screen.blit(base_img, (base_x, base_y))
        screen.blit(base_img, (base_x - width, base_y))
        screen.blit(bird_img, (BIRD_X, bird_y))
        score_surf = font.render(str(score), True, (0, 0, 0))
        screen.blit(score_surf, (width//2 - score_surf.get_width()//2, 30))
        pygame.display.flip()
        clock.tick(60)

    # Game Over screen (after game loop ends)
    screen.fill((0,0,0))
    game_over_text = font.render("Game Over! Press ESC to return to menu.", True, (255, 0, 0))
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2))
    pygame.display.flip()

    # Wait for ESC to return
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False
            elif event.type == pygame.QUIT:
                waiting = False

# Uncomment below to test standalone:
# pygame.init()
# WIDTH, HEIGHT = 700, 500
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# run_flappybird(screen)
