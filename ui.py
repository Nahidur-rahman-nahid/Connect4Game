
import pygame
import sys
from ConnectFour import ConnectFour
from ai import get_ai_move, HUMAN_PLAYER, AI_PLAYER

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = SQUARESIZE // 2 - 5
WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 2) * SQUARESIZE  # +2: one for header, one for reset button
SCREEN_SIZE = (WIDTH, HEIGHT)

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Connect Four - Human vs AI")
font = pygame.font.SysFont("monospace", 60)
button_font = pygame.font.SysFont("monospace", 40)

def draw_board(board):
    screen.fill(BLACK)
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (c * SQUARESIZE + SQUARESIZE // 2, (r + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS)

    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r][c] == HUMAN_PLAYER:
                pygame.draw.circle(screen, RED, (c * SQUARESIZE + SQUARESIZE // 2, (r + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS)
            elif board[r][c] == AI_PLAYER:
                pygame.draw.circle(screen, YELLOW, (c * SQUARESIZE + SQUARESIZE // 2, (r + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS)

    pygame.display.update()


def animate_drop(col, row, player_color):
    for r in range(row + 1):
        draw_board(game.board)
        pygame.draw.circle(screen, player_color, (col * SQUARESIZE + SQUARESIZE // 2, (r + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS)
        pygame.display.update()
        pygame.time.wait(50)






def show_message(message):
    label = font.render(message, True, RED)
    screen.blit(label, (40, 10))
    pygame.display.update()







def draw_reset_button():
    y = HEIGHT - SQUARESIZE  # ✅ Move it up by ~10 pixels
    pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 100, y, 200, 60))  # Full height
    label = button_font.render("Restart", True, BLACK)
    screen.blit(label, (WIDTH // 2 - 90, y + 10))
    pygame.display.update()



