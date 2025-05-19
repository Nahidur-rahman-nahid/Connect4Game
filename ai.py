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

def minimax(board_obj, depth, alpha, beta, maximizing_player):
    board = board_obj.board
    valid_locations = get_valid_moves(board)
    is_terminal = board_obj.check_win(AI_PLAYER) or board_obj.check_win(HUMAN_PLAYER) or board_obj.is_draw()

    if depth == 0 or is_terminal:
        if board_obj.check_win(AI_PLAYER):
            return (None, 1_000_000)
        elif board_obj.check_win(HUMAN_PLAYER):
            return (None, -1_000_000)
        elif board_obj.is_draw():
            return (None, 0)
        else:
            return (None, score_position(board, AI_PLAYER))

    if maximizing_player:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            temp_game = deepcopy(board_obj)
            temp_game.drop_token(col, AI_PLAYER)
            new_score = minimax(temp_game, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            temp_game = deepcopy(board_obj)
            temp_game.drop_token(col, HUMAN_PLAYER)
            new_score = minimax(temp_game, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value


def get_ai_move(game, depth=4):
    col, _ = minimax(game, depth, -math.inf, math.inf, True)
    return col
