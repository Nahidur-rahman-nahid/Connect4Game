import pygame
import sys
import time
from math import sqrt
from ConnectFour import ConnectFour
from ai import get_ai_move, HUMAN_PLAYER, AI_PLAYER

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = SQUARESIZE // 2 - 10
WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 2) * SQUARESIZE  # +2: one for header, one for controls
SCREEN_SIZE = (WIDTH, HEIGHT)

# Colors
BLUE = (0, 80, 170)
DARK_BLUE = (0, 40, 100)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
BRIGHT_RED = (255, 50, 50)
YELLOW = (240, 200, 0)
BRIGHT_YELLOW = (255, 235, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
LIGHT_GRAY = (220, 220, 220)
GREEN = (20, 200, 50)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Connect Four - Human vs AI")
title_font = pygame.font.SysFont("Arial", 48, bold=True)
font = pygame.font.SysFont("Arial", 36, bold=True)
small_font = pygame.font.SysFont("Arial", 24)
timer_font = pygame.font.SysFont("Arial", 32, bold=True)

# Game state
game = None
highlighted_cells = []
connection_line = None
game_start_time = 0
game_time = 0
human_turn_time = 0
ai_turn_time = 0
winner = None  # Track who wins: "Human" or "AI" or None


class AnimatedToken:
    def __init__(self, col, row, color, target_row):
        self.col = col
        self.row = row
        self.color = color
        self.target_row = target_row
        self.speed = 0.2
        self.done = False

    def update(self):
        if self.row < self.target_row:
            self.row += self.speed
            if self.row >= self.target_row:
                self.row = self.target_row
                self.done = True
        else:
            self.done = True

    def draw(self):
        y_pos = int((self.row + 1) * SQUARESIZE + SQUARESIZE // 2)
        x_pos = int(self.col * SQUARESIZE + SQUARESIZE // 2)

        # Shadow
        pygame.draw.circle(screen, BLACK, (x_pos + 3, y_pos + 3), RADIUS)

        # Main token
        pygame.draw.circle(screen, self.color, (x_pos, y_pos), RADIUS)

        # Highlight effect
        if self.color == RED:
            highlight = BRIGHT_RED
        else:
            highlight = BRIGHT_YELLOW

        pygame.draw.circle(screen, highlight, (x_pos - RADIUS // 3, y_pos - RADIUS // 3), RADIUS // 3)


def draw_board(board):
    # Background
    screen.fill(DARK_BLUE)

    # Title area
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, SQUARESIZE))

    # Display who wins at the top
    if winner:
        show_message(f"{winner} Wins!", GREEN)

    # Game board
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            # Draw grid cell
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))

            # Draw hole
            pygame.draw.circle(screen, DARK_BLUE,
                               (c * SQUARESIZE + SQUARESIZE // 2, (r + 1) * SQUARESIZE + SQUARESIZE // 2),
                               RADIUS)

    # Draw tokens
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r][c] == HUMAN_PLAYER:
                # Shadow effect
                pygame.draw.circle(screen, BLACK,
                                   (c * SQUARESIZE + SQUARESIZE // 2 + 3, (r + 1) * SQUARESIZE + SQUARESIZE // 2 + 3),
                                   RADIUS)
                # Main token
                pygame.draw.circle(screen, RED,
                                   (c * SQUARESIZE + SQUARESIZE // 2, (r + 1) * SQUARESIZE + SQUARESIZE // 2),
                                   RADIUS)
                # Highlight effect
                pygame.draw.circle(screen, BRIGHT_RED,
                                   (c * SQUARESIZE + SQUARESIZE // 2 - RADIUS // 3,
                                    (r + 1) * SQUARESIZE + SQUARESIZE // 2 - RADIUS // 3),
                                   RADIUS // 3)

            elif board[r][c] == AI_PLAYER:
                # Shadow effect
                pygame.draw.circle(screen, BLACK,
                                   (c * SQUARESIZE + SQUARESIZE // 2 + 3, (r + 1) * SQUARESIZE + SQUARESIZE // 2 + 3),
                                   RADIUS)
                # Main token
                pygame.draw.circle(screen, YELLOW,
                                   (c * SQUARESIZE + SQUARESIZE // 2, (r + 1) * SQUARESIZE + SQUARESIZE // 2),
                                   RADIUS)
                # Highlight effect
                pygame.draw.circle(screen, BRIGHT_YELLOW,
                                   (c * SQUARESIZE + SQUARESIZE // 2 - RADIUS // 3,
                                    (r + 1) * SQUARESIZE + SQUARESIZE // 2 - RADIUS // 3),
                                   RADIUS // 3)

    # Draw highlighted winning cells and connection line
    if highlighted_cells and len(highlighted_cells) >= 2:
        # Get coordinates of first and last winning tokens
        start_c, start_r = highlighted_cells[0]
        end_c, end_r = highlighted_cells[-1]

        # Convert to pixel coordinates
        start_x = start_c * SQUARESIZE + SQUARESIZE // 2
        start_y = (start_r + 1) * SQUARESIZE + SQUARESIZE // 2
        end_x = end_c * SQUARESIZE + SQUARESIZE // 2
        end_y = (end_r + 1) * SQUARESIZE + SQUARESIZE // 2

        # Debug print to verify the coordinates
        print(f"Drawing line from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        print(f"Winning cells: {highlighted_cells}")

        # Draw thick line connecting the winning tokens
        # First draw a black border line (thicker)
        pygame.draw.line(screen, BLACK, (start_x, start_y), (end_x, end_y), 12)
        # Then draw the colored line on top
        pygame.draw.line(screen, GREEN, (start_x, start_y), (end_x, end_y), 8)

        # Highlight the winning cells with a green outline
        for c, r in highlighted_cells:
            x = c * SQUARESIZE + SQUARESIZE // 2
            y = (r + 1) * SQUARESIZE + SQUARESIZE // 2
            pygame.draw.circle(screen, GREEN, (x, y), RADIUS + 5, 5)

    # Draw control panel
    pygame.draw.rect(screen, LIGHT_GRAY, (0, HEIGHT - SQUARESIZE, WIDTH, SQUARESIZE))

    # Draw timer
    minutes = int(game_time) // 60
    seconds = int(game_time) % 60
    timer_text = f"Time: {minutes:02d}:{seconds:02d}"
    timer_label = timer_font.render(timer_text, True, BLACK)
    screen.blit(timer_label, (20, HEIGHT - SQUARESIZE + 30))

    pygame.display.update()


def draw_preview_token(x, board):
    if 0 <= x < WIDTH:
        col = x // SQUARESIZE
        if 0 <= col < COLUMN_COUNT and game.is_valid_column(col):
            # Draw semi-transparent preview token at the top
            s = pygame.Surface((2 * RADIUS, 2 * RADIUS), pygame.SRCALPHA)
            pygame.draw.circle(s, (RED[0], RED[1], RED[2], 128), (RADIUS, RADIUS), RADIUS)
            screen.blit(s, (col * SQUARESIZE + SQUARESIZE // 2 - RADIUS, SQUARESIZE // 2 - RADIUS))
            pygame.display.update()


def animate_drop(col, row, player_color):
    token = AnimatedToken(col, 0, player_color, row)

    # Simple sound effect using pygame.mixer (no file needed)
    if pygame.mixer.get_init():
        try:
            # Create a simple beep sound
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(buffer=bytes([128] * 1760)))
        except:
            pass  # Ignore sound errors

    while not token.done:
        # Redraw the board
        draw_board(game.board)

        # Update and draw the animated token
        token.update()
        token.draw()

        pygame.display.update()
        pygame.time.delay(16)  # Approximately 60 FPS

    return token.done


def show_message(message, color=RED):
    # Create shadow effect for text
    shadow_label = title_font.render(message, True, BLACK)
    label = title_font.render(message, True, color)

    # Calculate center position
    text_width = label.get_width()
    x_pos = (WIDTH - text_width) // 2

    # Draw shadow slightly offset
    screen.blit(shadow_label, (x_pos + 2, 25 + 2))
    # Draw text
    screen.blit(label, (x_pos, 25))

    pygame.display.update()


def draw_reset_button():
    # Button background with shadow
    y = HEIGHT - SQUARESIZE + 20
    pygame.draw.rect(screen, BLACK, (WIDTH - 220, y + 3, 200, 60))
    pygame.draw.rect(screen, WHITE, (WIDTH - 220, y, 200, 60))

    # Button text
    label = font.render("Restart", True, BLACK)
    screen.blit(label, (WIDTH - 180, y + 12))
    pygame.display.update()


def find_winning_cells(board, player):
    # Check horizontal
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r][c + i] == player for i in range(4)):
                # Return coordinates in (column, row) format
                cells = [(c + i, r) for i in range(4)]
                print(f"Found horizontal win at row {r}, cols {c}-{c + 3}: {cells}")
                return cells

    # Check vertical
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT):
            if all(board[r + i][c] == player for i in range(4)):
                cells = [(c, r + i) for i in range(4)]
                print(f"Found vertical win at col {c}, rows {r}-{r + 3}: {cells}")
                return cells

    # Check diagonal (positive slope)
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                cells = [(c + i, r + i) for i in range(4)]
                print(f"Found positive diagonal win starting at ({c},{r}): {cells}")
                return cells

    # Check diagonal (negative slope)
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                cells = [(c + i, r - i) for i in range(4)]
                print(f"Found negative diagonal win starting at ({c},{r}): {cells}")
                return cells

    print("No winning cells found")
    return []


def run_game():
    global game, highlighted_cells, connection_line, game_start_time, game_time
    global human_turn_time, ai_turn_time, winner

    # Initialize game
    game = ConnectFour()
    highlighted_cells = []
    connection_line = None
    game_start_time = time.time()
    game_time = 0
    human_turn_time = 0
    ai_turn_time = 0
    winner = None

    # Initialize sound if possible
    try:
        pygame.mixer.init()
    except:
        pass

    draw_board(game.board)
    show_message("Your Turn", RED)
    running = True
    game_over = False

    # For token preview
    mouse_x = 0

    while running:
        current_time = time.time()
        game_time = current_time - game_start_time

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                mouse_x = event.pos[0]
                if not game_over and game.current_player == HUMAN_PLAYER:
                    draw_board(game.board)
                    draw_preview_token(mouse_x, game.board)

            # Reset button
            elif game_over and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if WIDTH - 220 <= x <= WIDTH - 20 and HEIGHT - SQUARESIZE + 20 <= y <= HEIGHT - SQUARESIZE + 80:
                    # Reset game
                    game = ConnectFour()
                    highlighted_cells = []
                    connection_line = None
                    game_start_time = time.time()
                    game_time = 0
                    human_turn_time = 0
                    ai_turn_time = 0
                    winner = None
                    draw_board(game.board)
                    show_message("Your Turn", RED)
                    game_over = False
                    continue

            # Human move
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and game.current_player == HUMAN_PLAYER:
                x_pos = event.pos[0]
                col = x_pos // SQUARESIZE
                if 0 <= col < COLUMN_COUNT and game.is_valid_column(col):
                    row = game.get_next_open_row(col)
                    game.drop_token(col)

                    # Animate token drop
                    animate_drop(col, row, RED)
                    draw_board(game.board)

                    # Check win condition
                    if game.check_win(HUMAN_PLAYER):
                        highlighted_cells = find_winning_cells(game.board, HUMAN_PLAYER)
                        winner = "Human"
                        print(f"Human wins! Highlighted cells: {highlighted_cells}")
                        # Play win sound
                        if pygame.mixer.get_init():
                            try:
                                # Create a simple win sound
                                pygame.mixer.Channel(0).play(
                                    pygame.mixer.Sound(buffer=bytes([128 + i // 8 for i in range(1760)])))
                            except:
                                pass
                        show_message("You Win!", GREEN)
                        draw_board(game.board)  # Redraw to show the highlighted cells
                        game_over = True
                        draw_reset_button()

                    # Check draw condition
                    elif game.is_draw():
                        show_message("Draw!", BLUE)
                        game_over = True
                        draw_reset_button()

                    else:
                        game.switch_player()
                        show_message("AI Thinking...", YELLOW)

        # AI move
        if not game_over and game.current_player == AI_PLAYER:
            # Add small delay to make AI seem like it's thinking
            pygame.time.wait(400)

            # Get AI move
            col = get_ai_move(game, depth=3)
            if col is not None:
                row = game.get_next_open_row(col)
                game.drop_token(col)

                # Animate token drop
                animate_drop(col, row, YELLOW)
                draw_board(game.board)

                # Check win condition
                if game.check_win(AI_PLAYER):
                    highlighted_cells = find_winning_cells(game.board, AI_PLAYER)
                    winner = "AI"
                    print(f"AI wins! Highlighted cells: {highlighted_cells}")
                    # Play win sound
                    if pygame.mixer.get_init():
                        try:
                            # Create a simple win sound
                            pygame.mixer.Channel(0).play(
                                pygame.mixer.Sound(buffer=bytes([128 + i // 8 for i in range(1760)])))
                        except:
                            pass
                    show_message("AI Wins!", GREEN)
                    draw_board(game.board)  # Redraw to show the highlighted cells
                    game_over = True
                    draw_reset_button()

                # Check draw condition
                elif game.is_draw():
                    show_message("Draw!", BLUE)
                    game_over = True
                    draw_reset_button()

                else:
                    game.switch_player()
                    show_message("Your Turn", RED)

        # Refresh board with current time
        if not game_over:
            draw_board(game.board)
            if game.current_player == HUMAN_PLAYER:
                draw_preview_token(mouse_x, game.board)

        # Control game speed
        pygame.time.delay(16)  # Cap at ~60 FPS


if __name__ == "__main__":
    # Try to initialize mixer for sound effects
    try:
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    except:
        print("Warning: Audio system could not be initialized. Game will run without sound.")

    run_game()
