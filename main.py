import pygame
import sys
import traceback

from snake import run_snake
from brickout import run_brickout
from shooter import run_shooter
from tictactoe import run_tictactoe
from flappybird import run_flappybird

# Initialize
pygame.init()
WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu")

# Fonts
font = pygame.font.SysFont("arial", 36)
title_font = pygame.font.SysFont("arial", 60, bold=True)

# Menu options
MENU_OPTIONS = [
    "Snake", "Brickout", "Tictactoe",
    "2-Player Shooter", "Flappy Bird", "Quit"
]

# --- Menu Layout ---
COLS = 2
ROWS = 3
BUTTON_WIDTH = 260
BUTTON_HEIGHT = 60
BUTTON_MARGIN_X = 40
BUTTON_MARGIN_Y = 18

# Colors
BG_COLOR = (20, 20, 30)
MENU_BG_COLOR = (40, 40, 60)
BUTTON_COLOR = (70, 70, 100)
HIGHLIGHT_COLOR = (255, 200, 0)
TEXT_COLOR = (230, 230, 230)
TITLE_COLOR = (0, 200, 255)

# Calculate layout
menu_width = COLS * BUTTON_WIDTH + (COLS - 1) * BUTTON_MARGIN_X
menu_height = ROWS * BUTTON_HEIGHT + (ROWS - 1) * BUTTON_MARGIN_Y
menu_x = (WIDTH - menu_width) // 2
menu_y = HEIGHT - menu_height - 30

button_rects = []
for row in range(ROWS):
    for col in range(COLS):
        idx = row * COLS + col
        if idx >= len(MENU_OPTIONS):
            continue
        rect = pygame.Rect(
            menu_x + col * (BUTTON_WIDTH + BUTTON_MARGIN_X),
            menu_y + row * (BUTTON_HEIGHT + BUTTON_MARGIN_Y),
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
        )
        button_rects.append(rect)


def draw_menu(mouse_pos=None):
    screen.fill(BG_COLOR)

    # Draw title
    title_text = title_font.render("Games Mania", True, TITLE_COLOR)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

    # Draw menu background
    menu_bg_rect = pygame.Rect(
        menu_x - 20, menu_y - 20, menu_width + 40, menu_height + 40)
    pygame.draw.rect(screen, MENU_BG_COLOR, menu_bg_rect, border_radius=22)

    # Draw buttons
    for idx, option in enumerate(MENU_OPTIONS):
        rect = button_rects[idx]
        is_hovered = mouse_pos and rect.collidepoint(mouse_pos)
        text_color = HIGHLIGHT_COLOR if is_hovered else TEXT_COLOR
        bg_color = BUTTON_COLOR

        pygame.draw.rect(screen, bg_color, rect, border_radius=14)
        text = font.render(option, True, text_color)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    pygame.display.flip()


def main_menu():
    while True:
        mouse_pos = pygame.mouse.get_pos()
        draw_menu(mouse_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for idx, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        try:
                            if idx == 0:
                                run_snake(screen)
                            elif idx == 1:
                                run_brickout(screen)
                            elif idx == 2:
                                run_tictactoe(screen)
                            elif idx == 3:
                                run_shooter(screen)
                            elif idx == 4:
                                run_flappybird(screen)
                            elif idx == 5:
                                pygame.quit()
                                sys.exit()
                        except Exception as e:
                            print(f"Error running {MENU_OPTIONS[idx]}: {e}")
                            traceback.print_exc()
        pygame.time.Clock().tick(30)


if __name__ == "__main__":
    main_menu()
