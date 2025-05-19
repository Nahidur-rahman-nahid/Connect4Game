# 🎮 Connect Four Game (Python Console Version)

This is a Python console implementation of the classic **Connect Four** game. Two players take turns dropping tokens (X and O) into a 6×7 grid, and the first to connect four of their tokens in a line — horizontally, vertically, or diagonally — wins!

---

## 📌 Features

- 6 rows × 7 columns standard Connect Four board.
- Two-player support (X vs O).
- Win condition detection:
  - Horizontal
  - Vertical
  - Diagonal (both / and \ directions)
- Draw condition detection.
- Console-based UI with clear column indicators.

---

## 🧠 Rules of the Game

1. Players take turns dropping tokens into one of the 7 columns.
2. The token falls to the lowest available row in that column.
3. The first player to align 4 of their tokens (X or O) in a row — horizontally, vertically, or diagonally — wins.
4. If the board fills up with no winner, the game ends in a draw.

---

## 🚀 How to Run

### ✅ Prerequisites

- Python 3.x installed on your system.

### ▶️ Run the game

```bash
python connect_four.py

```
## 🛠 How It Works
ConnectFour class encapsulates the game state and mechanics.

Methods include:

- print_board() - Displays the game board

- drop_token(col) - Places token in a column

- check_win(player) - Checks if the given player has won

- is_draw() - Detects draw condition

- switch_player() - Alternates between players X and O

---
## 📸 Sample Output
```bash

mathematica
Copy
Edit
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . . X O X .
0 1 2 3 4 5 6

```
---
## 📚 License
This project is open-source and available under the MIT License.
---
## 👨‍💻 Author
1. Nazmus Shakib(BSSE-1452)
2. Nahidur Rahman(BSSE-1429)
3. Md.Mainuddin(BSSE-1472)
  
- CSE 604 - Artificial Intelligence
- Mid-Project 1 Submission: Connect Four Game

Feel free to fork, improve, or add AI to play against the computer!



