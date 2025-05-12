import math
import random
from copy import deepcopy
from ConnectFour import ConnectFour, ROWS, COLUMNS, EMPTY

AI_PLAYER = 'O'
HUMAN_PLAYER = 'X'


def get_valid_moves(board):
    return [col for col in range(COLUMNS) if board[0][col] == EMPTY]


def evaluate_window(window, player):
    score = 0
    opponent = HUMAN_PLAYER if player == AI_PLAYER else AI_PLAYER

    if window.count(player) == 4:
        score += 100000
    elif window.count(player) == 3 and window.count(EMPTY) == 1:
        score += 1000
    elif window.count(player) == 2 and window.count(EMPTY) == 2:
        score += 100

    # Block opponent aggressively
    if window.count(opponent) == 4:
        score -= 100000
    elif window.count(opponent) == 3 and window.count(EMPTY) == 1:
        score -= 1200  # must block
    elif window.count(opponent) == 2 and window.count(EMPTY) == 2:
        score -= 100

    return score



def score_position(board, player):
    score = 0

    # Score center column
    center_array = [board[row][COLUMNS // 2] for row in range(ROWS)]
    score += center_array.count(player) * 3

    # Score horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            window = [board[row][col + i] for i in range(4)]
            score += evaluate_window(window, player)

    # Score vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            window = [board[row + i][col] for i in range(4)]
            score += evaluate_window(window, player)

    # Score positive diagonal
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += evaluate_window(window, player)

    # Score negative diagonal
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            window = [board[row - i][col + i] for i in range(4)]
            score += evaluate_window(window, player)

    return score

def get_ai_move(game, depth=4):
    col, _ = minimax(game, depth, -math.inf, math.inf, True)
    return col
