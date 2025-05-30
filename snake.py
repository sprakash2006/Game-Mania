import pygame
import random
import os

# Constants
WIDTH, HEIGHT = 700, 500
CELL_SIZE = 25
GRID_COLS = 25
GRID_ROWS = 15
BOX_WIDTH = GRID_COLS * CELL_SIZE
BOX_HEIGHT = GRID_ROWS * (CELL_SIZE)
BOX_X = (WIDTH - BOX_WIDTH) // 2
BOX_Y = 80  # Leave space for title above

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def load_and_scale_image(path, size):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(img, size)


class Snake:
    def __init__(self):
        head_x = GRID_COLS // 2
        head_y = GRID_ROWS // 2
        self.positions = [
            (head_x, head_y),
            (head_x - 1, head_y),
            (head_x - 2, head_y),
            (head_x - 3, head_y)
        ]

        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.grow = False

    def move(self):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        # Check wall collision (inside box)
        if (
            new_head[0] < 0
            or new_head[0] >= GRID_COLS
            or new_head[1] < 0
            or new_head[1] >= GRID_ROWS
        ):
            return False  # Collision with wall

        # Check self collision
        if new_head in self.positions[1:]:
            return False

        self.positions.insert(0, new_head)
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
        return True

    def change_direction(self, new_direction):
        # Prevent reversing into itself
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction

    def eat(self):
        self.grow = True


class Food:
    def __init__(self, snake_positions):
        self.position = self.random_position(snake_positions)

    def random_position(self, snake_positions):
        positions = [
            (x, y)
            for x in range(GRID_COLS)
            for y in range(GRID_ROWS)
            if (x, y) not in snake_positions
        ]
        return random.choice(positions)

    def respawn(self, snake_positions):
        self.position = self.random_position(snake_positions)


def run_snake(screen):
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    title_font = pygame.font.SysFont(None, 54)

    # Load images AFTER display is initialized
    snake_head_img_base = load_and_scale_image(
        'images/snake/snake_head.png', (CELL_SIZE, CELL_SIZE))
    snake_body_img = load_and_scale_image(
        "images/snake/snake_body.png", (CELL_SIZE, CELL_SIZE))
    food_img = load_and_scale_image(
        "images/snake/food.png", (CELL_SIZE, CELL_SIZE))
    bg_img = load_and_scale_image(
        "images/snake/background.png", (WIDTH, HEIGHT))

    def get_head_image(direction):
        if direction == DOWN:
            return snake_head_img_base
        elif direction == UP:
            return pygame.transform.rotate(snake_head_img_base, 180)
        elif direction == RIGHT:
            return pygame.transform.rotate(snake_head_img_base, 90)
        elif direction == LEFT:
            return pygame.transform.rotate(snake_head_img_base, -90)
        return snake_head_img_base

    snake = Snake()
    food = Food(snake.positions)
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)

        if not snake.move():
            running = False  # Snake collided with itself or wall

        if snake.positions[0] == food.position:
            snake.eat()
            score += 1
            food.respawn(snake.positions)

        # Draw background
        screen.blit(bg_img, (0, 0))

        # Draw bordered box
        pygame.draw.rect(screen, (0, 255, 0),
                         (BOX_X-3, BOX_Y-3, BOX_WIDTH+6, BOX_HEIGHT+6), 3)

        # Draw game name above the box
        title_text = title_font.render("Snake Game", True, (0, 255, 0))
        screen.blit(title_text, (WIDTH // 2 -
                    title_text.get_width() // 2, BOX_Y - 60))

        # Draw snake (inside box)
        for i, pos in enumerate(snake.positions):
            rect = pygame.Rect(
                BOX_X + pos[0] * CELL_SIZE, BOX_Y +
                pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE
            )
            if i == 0:
                head_img = get_head_image(snake.direction)
                screen.blit(head_img, rect)
            else:
                screen.blit(snake_body_img, rect)

        # Draw food (inside box)
        food_rect = pygame.Rect(
            BOX_X + food.position[0] * CELL_SIZE,
            BOX_Y + food.position[1] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE,
        )
        screen.blit(food_img, food_rect)

        # Draw score (inside box, top-left)
        score_text = font.render(f"Score: {score}", True, (0, 255, 0))
        screen.blit(score_text, (BOX_X + BOX_WIDTH - 100, BOX_Y - 30))

        pygame.display.flip()
        clock.tick(10)

    # Game over message
    screen.blit(bg_img, (0, 0))
    pygame.draw.rect(screen, (0, 255, 0),
                     (BOX_X-3, BOX_Y-3, BOX_WIDTH+6, BOX_HEIGHT+6), 3)
    title_text = title_font.render("Snake Game", True, (0, 255, 0))
    screen.blit(title_text, (WIDTH // 2 -
                title_text.get_width() // 2, BOX_Y - 60))

    game_over_text = font.render(
        "Game Over! Press ESC to return to menu.", True, (255, 0, 0))
    screen.blit(
        game_over_text, (WIDTH // 2 -
                         game_over_text.get_width() // 2, HEIGHT // 2)
    )

    score_text = font.render(f"Score: {score}", True, (255, 255, 255),)
    screen.blit(score_text, (WIDTH // 2, HEIGHT // 2-40))
    
    pygame.display.flip()

    # Wait for ESC to return
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
    run_snake(screen)
