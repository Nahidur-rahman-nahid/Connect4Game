ROWS = 6
COLUMNS = 7
EMPTY = '.'


class ConnectFour:
    def __init__(self):
        # Create a 6x7 board initialized with EMPTY tokens
        self.board = [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.current_player = 'X'  # Player X always starts

    def print_board(self):
        # Print the board row by row
        for row in self.board:
            print(' '.join(row))
        print('0 1 2 3 4 5 6')  # Show column numbers for user input

    def is_valid_column(self, col):
        # A move is valid if the top cell in the column is still EMPTY
        return self.board[0][col] == EMPTY

    def get_next_open_row(self, col):
        # Return the bottom-most empty row in a column
        for row in reversed(range(ROWS)):  # Start from bottom row
            if self.board[row][col] == EMPTY:
                return row
        return None  # Column is full

    def drop_token(self, col, player=None):
        if not (0 <= col < COLUMNS):
            print("❌ Invalid column number.")
            return False
        if not self.is_valid_column(col):
            print("❌ Column is full.")
            return False

        row = self.get_next_open_row(col)
        if player is None:
            player = self.current_player
        self.board[row][col] = player
        return True

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_win(self, player):
        # Check horizontal wins
        for row in range(ROWS):
            for col in range(COLUMNS - 3):  # Only start where 4 fit
                if all(self.board[row][col + i] == player for i in range(4)):
                    return True

        # Check vertical wins
        for col in range(COLUMNS):
            for row in range(ROWS - 3):  # Only start where 4 fit
                if all(self.board[row + i][col] == player for i in range(4)):
                    return True

        # Check positively sloped diagonals (/)
        for row in range(3, ROWS):
            for col in range(COLUMNS - 3):
                if all(self.board[row - i][col + i] == player for i in range(4)):
                    return True

        # Check negatively sloped diagonals (\)
        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                if all(self.board[row + i][col + i] == player for i in range(4)):
                    return True

        return False


    def is_draw(self):
        # If there is no EMPTY cell in the top row, it's a draw
        return all(cell != EMPTY for cell in self.board[0])

