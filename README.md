# Othello Game

A local implementation of the classic Othello (Reversi) game with both single-player and two-player modes.

## Features
- Play against a computer opponent with adjustable difficulty levels
- Two-player mode on the same system
- Modern graphical interface
- Score tracking
- Valid move highlighting

## Requirements
- Python 3.8 or higher
- Pygame
- NumPy

## Installation
1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## How to Play
Run the game using:
```bash
python main.py
```

### Game Rules
- Players take turns placing their pieces (black or white) on the board
- A valid move must capture at least one opponent's piece
- Pieces are captured by flanking them with your pieces
- The game ends when no more valid moves are available
- The player with the most pieces wins

### Controls
- Left-click to place a piece
- Press 'R' to reset the game
- Select game mode (single-player/two-player) from the start menu
- Select difficulty level from the start menu in single-player mode
- Press 'Q' to resign 