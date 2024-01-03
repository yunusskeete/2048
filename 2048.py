"""Minimal Python implementation of the 2048 Game using NumPy.
"""

import numpy as np
import os
from datetime import datetime
from utils import initialize_board, add_random_tile, display_board, move, is_game_over, save_game_state, actions


def main():
    """Main function to run the 2048 game."""

    if not os.path.exists(os.path.join(os.getcwd(), "runs")):
        os.mkdir("runs")

    save_path = os.path.join(os.getcwd(), "runs", datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    board, score = initialize_board()

    while not is_game_over(board):

        display_board(board, score)

        move_direction = input("Enter move direction (W/A/S/D): ").upper()

        old_board = np.copy(board)

        if move_direction in actions.keys():
            # Save the game state after each move
            save_game_state(board, score, move_direction, save_path)

            if move_direction == "W":
                board, score = move(board, actions[move_direction], score)
            elif move_direction == "A":
                board, score = move(board, actions[move_direction], score)
            elif move_direction == "S":
                board, score = move(board, actions[move_direction], score)
            elif move_direction == "D":
                board, score = move(board, actions[move_direction], score)

            if np.array_equal(old_board, board):
                score -= 1
            else:    
                add_random_tile(board)

        elif move_direction == "C":
            if input("Press 'y' to quit the game. Press any other key to continue...").upper() == "Y":
                print(f"Quitting Game (Score: {score})")
                return -1
        else:
            print("Invalid move! Use W/A/S/D.")

    display_board(board, score)

    print("Game Over!")
    print(f"Final Score: {score}")

if __name__ == "__main__":
    main()
