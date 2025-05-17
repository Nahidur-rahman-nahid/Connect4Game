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
