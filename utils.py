"""Utils for the minimal Python implementation of the 2048 Game using NumPy.
"""

import numpy as np
import os
import jsonlines
from datetime import datetime


LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3 

# 2048 game actions
actions = {
    "W": UP,
    "A": LEFT,
    "S": DOWN,
    "D": RIGHT
}

def initialize_board() -> (np.ndarray, int):
    """Initialize the game board with two random tiles."""

    board = np.zeros((4, 4), dtype=int)
    add_random_tile(board)
    add_random_tile(board)

    score = 0

    return board, score

def add_random_tile(board: np.ndarray) -> None:
    """Add a random tile (either 2 or 4) to an empty cell on the board."""

    empty_cells = np.argwhere(board == 0)

    if empty_cells.size > 0:
        i, j = empty_cells[np.random.choice(empty_cells.shape[0])]
        board[i, j] = np.random.choice([2, 4], p=[0.75, 0.25])

def display_board(board: np.ndarray, score: int) -> None:
    """Display the current state of the game board."""

    os.system('cls' if os.name == 'nt' else 'clear') # Clear the console
    print(f"Score: {score}")

    _max = np.max(np.max(board))
    max_tile_length = len(str(_max))

    for row in board:
        # Make all tiles the length of the longest tile
        print(' '.join(f"{cell:>{max_tile_length}}" if cell != 0 else '.'.rjust(max_tile_length) for cell in row))

    print() # Empty line

def move(board: np.ndarray, direction: int, score: int) -> (np.ndarray, int):
    """Perform a move in the specified direction and update the game board."""

    rotated_board = np.rot90(board, -direction)

    for i in range(4):
        row = rotated_board[i, :]
        row = np.concatenate((row[row != 0], np.zeros(4 - np.count_nonzero(row))))

        for j in range(3):
            if row[j] == row[j + 1]:
                row[j] *= 2
                row[j + 1] = 0
                score += row[j]  # Increment the score when tiles combine

        row = row[row != 0]
        row = np.concatenate((row, np.zeros(4 - len(row))))
        rotated_board[i, :] = row

    return np.rot90(rotated_board, direction), score

def is_game_over(board) -> bool:
    """Check if the game is over (no more valid moves)."""

    # Check for adjacent identical cells
    rows_equal = (board[:, :-1] == board[:, 1:]).any()
    cols_equal = (board[:-1, :] == board[1:, :]).any()
    # Check for empty cells
    empty_cells = (board == 0).any()

    # Game is over if there are no adjacent identical cells and no empty cells
    return not (rows_equal or cols_equal or empty_cells)

def save_game_state(board: np.ndarray, score: int, move_direction: str, file_name: str) -> None:
    """Save the game state to a JSONL file."""
    
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "board": board.tolist(),
        "score": score,
        "move_direction": move_direction
    }

    with jsonlines.open(f"{file_name}.jsonl", mode='a') as writer:
        writer.write(data)