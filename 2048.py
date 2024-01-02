"""Python implementation of the 2048 Game using NumPy.
"""

import numpy as np
import random
import os
import jsonlines
from datetime import datetime

def initialize_board() -> np.ndarray:
    """Initialize the game board with two random tiles."""

    board = np.zeros((4, 4), dtype=int)
    add_random_tile(board)
    add_random_tile(board)

    return board

def add_random_tile(board: np.ndarray):
    """Add a random tile (either 2 or 4) to an empty cell on the board."""

    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i, j] == 0]

    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i, j] = random.choices([2, 4], weights=[.75, .25], k=1).pop()

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

    rotated_board = np.rot90(board, -direction // 90)

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

    return np.rot90(rotated_board, direction // 90), score

def is_game_over(board) -> bool:
    """Check if the game is over (no more valid moves)."""

    for i in range(4):
        for j in range(4):
            if board[i, j] == 0 or (i < 3 and board[i, j] == board[i + 1, j]) or (j < 3 and board[i, j] == board[i, j + 1]):
                return False

    return True

def save_game_state(board: np.ndarray, score: int, move_direction: str, file_name: str):
    """Save the game state to a JSONL file."""
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "board": board.tolist(),
        "score": score,
        "move_direction": move_direction
    }

    with jsonlines.open(f"{file_name}.jsonl", mode='a') as writer:
        writer.write(data)

def main():
    """Main function to run the 2048 game."""

    if not os.path.exists(os.path.join(os.getcwd(), "runs")):
        os.mkdir("runs")

    save_path = os.path.join(os.getcwd(), "runs", datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    board = initialize_board()
    score = 0

    while not is_game_over(board):

        display_board(board, score)

        move_direction = input("Enter move direction (W/A/S/D): ").upper()

        old_board = np.copy(board)

        if move_direction in ['W', 'A', 'S', 'D']:
            # Save the game state after each move
            save_game_state(board, score, move_direction, save_path)

            if move_direction == 'W':
                board, score = move(board, 270, score)
            elif move_direction == 'A':
                board, score = move(board, 0, score)
            elif move_direction == 'S':
                board, score = move(board, 90, score)
            elif move_direction == 'D':
                board, score = move(board, 180, score)

            if np.array_equal(old_board, board):
                print(f"Invalid move! No moves in {move_direction}")
            else:    
                add_random_tile(board)

        else:
            print("Invalid move! Use W/A/S/D.")

    display_board(board, score)

    print("Game Over!")

if __name__ == "__main__":
    main()
