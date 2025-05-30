import pygame
import numpy as np
import random

# Window and box constants
WIDTH, HEIGHT = 700, 500
BOX_SIZE = 360
BOX_X = (WIDTH - BOX_SIZE) // 2
BOX_Y = 100  # space for title

# Grid constants (inside box)
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = BOX_SIZE // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)


def run_tictactoe(screen):
    font = pygame.font.SysFont(None, 32)
    title_font = pygame.font.SysFont(None, 54)
    board = np.zeros((BOARD_ROWS, BOARD_COLS))

    def draw_box():
        pygame.draw.rect(screen, (0, 255, 0),
                         (BOX_X-3, BOX_Y-3, BOX_SIZE+6, BOX_SIZE+6), 3)

    def draw_lines():
        # Horizontal
        for i in range(1, BOARD_ROWS):
            pygame.draw.line(
                screen, LINE_COLOR,
                (BOX_X, BOX_Y + i * SQUARE_SIZE),
                (BOX_X + BOX_SIZE, BOX_Y + i * SQUARE_SIZE),
                15
            )
        # Vertical
        for i in range(1, BOARD_COLS):
            pygame.draw.line(
                screen, LINE_COLOR,
                (BOX_X + i * SQUARE_SIZE, BOX_Y),
                (BOX_X + i * SQUARE_SIZE, BOX_Y + BOX_SIZE),
                15
            )

    def draw_figures():
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                cx = BOX_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
                cy = BOX_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2
                if board[row][col] == 1:
                    pygame.draw.circle(
                        screen, CIRCLE_COLOR, (cx,
                                               cy), CIRCLE_RADIUS, CIRCLE_WIDTH
                    )
                elif board[row][col] == 2:
                    # Descending diagonal
                    start_desc = (BOX_X + col * SQUARE_SIZE + SPACE,
                                  BOX_Y + row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                    end_desc = (BOX_X + col * SQUARE_SIZE + SQUARE_SIZE -
                                SPACE, BOX_Y + row * SQUARE_SIZE + SPACE)
                    pygame.draw.line(screen, CROSS_COLOR,
                                     start_desc, end_desc, CROSS_WIDTH)
                    # Ascending diagonal
                    start_asc = (BOX_X + col * SQUARE_SIZE + SPACE,
                                 BOX_Y + row * SQUARE_SIZE + SPACE)
                    end_asc = (BOX_X + col * SQUARE_SIZE + SQUARE_SIZE -
                               SPACE, BOX_Y + row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                    pygame.draw.line(screen, CROSS_COLOR,
                                     start_asc, end_asc, CROSS_WIDTH)

    def mark_square(row, col, player):
        board[row][col] = player

    def available_square(row, col):
        return board[row][col] == 0

    def is_board_full():
        return not (board == 0).any()

    def check_win(player):
        for col in range(BOARD_COLS):
            if all([board[row][col] == player for row in range(BOARD_ROWS)]):
                draw_vertical_winning_line(col, player)
                return True
        for row in range(BOARD_ROWS):
            if all([board[row][col] == player for col in range(BOARD_COLS)]):
                draw_horizontal_winning_line(row, player)
                return True
        if all([board[i][i] == player for i in range(BOARD_COLS)]):
            draw_desc_diagonal(player)
            return True
        if all([board[i][BOARD_COLS - i - 1] == player for i in range(BOARD_COLS)]):
            draw_asc_diagonal(player)
            return True
        return False

    def draw_vertical_winning_line(col, player):
        posX = BOX_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
        color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
        pygame.draw.line(screen, color, (posX, BOX_Y + 15),
                         (posX, BOX_Y + BOX_SIZE - 15), 15)

    def draw_horizontal_winning_line(row, player):
        posY = BOX_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2
        color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
        pygame.draw.line(screen, color, (BOX_X + 15, posY),
                         (BOX_X + BOX_SIZE - 15, posY), 15)

    def draw_asc_diagonal(player):
        color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
        pygame.draw.line(screen, color, (BOX_X + 15, BOX_Y +
                         BOX_SIZE - 15), (BOX_X + BOX_SIZE - 15, BOX_Y + 15), 15)

    def draw_desc_diagonal(player):
        color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
        pygame.draw.line(screen, color, (BOX_X + 15, BOX_Y + 15),
                         (BOX_X + BOX_SIZE - 15, BOX_Y + BOX_SIZE - 15), 15)

    def ai_move():
        empty = [(r, c) for r in range(BOARD_ROWS)
                 for c in range(BOARD_COLS) if board[r][c] == 0]
        if empty:
            move = random.choice(empty)
            mark_square(move[0], move[1], 2)

    def get_grid_pos(mouse_pos):
        mx, my = mouse_pos
        if (BOX_X <= mx < BOX_X + BOX_SIZE) and (BOX_Y <= my < BOX_Y + BOX_SIZE):
            col = (mx - BOX_X) // SQUARE_SIZE
            row = (my - BOX_Y) // SQUARE_SIZE
            return int(row), int(col)
        return None, None

    # Game loop
    screen.fill(BG_COLOR)
    draw_box()
    draw_lines()
    player = 1
    game_over = False
    waiting_for_ai = False
    ai_wait_start = 0
    AI_DELAY = 500  # milliseconds

    clock = pygame.time.Clock()

    while True:
        # Draw background and box each frame
        screen.fill(BG_COLOR)
        draw_box()
        # Draw title above the box
        title_text = title_font.render("TicTacToe", True, (0, 255, 0))
        screen.blit(title_text, (WIDTH // 2 -
                    title_text.get_width() // 2, BOX_Y - 60))
        draw_lines()
        draw_figures()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and not game_over
                and player == 1
                and not waiting_for_ai
            ):
                clicked_row, clicked_col = get_grid_pos(event.pos)
                if clicked_row is not None and available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    if check_win(player):
                        game_over = True
                    else:
                        waiting_for_ai = True
                        ai_wait_start = pygame.time.get_ticks()

        # Handle AI move after a delay
        if waiting_for_ai and not game_over:
            now = pygame.time.get_ticks()
            if now - ai_wait_start >= AI_DELAY:
                ai_move()
                if check_win(2):
                    game_over = True
                else:
                    player = 1
                waiting_for_ai = False
                player = 1

        if is_board_full() and not game_over:
            game_over = True

        clock.tick(30)

        if game_over:
            # Show winner or tie
            screen.fill(BG_COLOR)
            draw_box()
            title_text = title_font.render("TicTacToe", True, (0, 255, 0))
            screen.blit(title_text, (WIDTH // 2 -
                        title_text.get_width() // 2, BOX_Y - 60))
            draw_lines()
            draw_figures()
            if check_win(1):
                msg = "You Win!"
            elif check_win(2):
                msg = "AI Wins!"
            else:
                msg = "It's a Tie!"
            text = font.render(msg, True, (0, 255, 0))
            screen.blit(
                text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 20))
            prompt = font.render("Press ESC to return", True, (0, 255, 0))
            screen.blit(
                prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 20))
            pygame.display.update()

            # Wait for ESC or QUIT
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        return
                    elif event.type == pygame.QUIT:
                        return
                clock.tick(10)


# For standalone testing:
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    run_tictactoe(screen)
