import numpy as np
from typing import List

value_to_symbol = {-1: "O", 0: "None", 1: "X"}


class State:
    def __init__(self, r: "State" = None):
        if r is None:
            self.board = np.zeros((3, 3), dtype=int)
            self.current_turn = 1  # 1 for 'X', -1 for 'O'
        else:
            self.board = np.copy(r.board)
            self.current_turn = r.current_turn

    def print(self):
        symbol_map = {0: ".", 1: "X", -1: "O"}
        for row in self.board:
            print(" ".join(symbol_map[cell] for cell in row))
        print()

    def turn(self) -> int:
        return self.current_turn

    def fill(self, x: int):
        row, col = divmod(x, 3)
        if self.board[row, col] == 0:
            self.board[row, col] = self.current_turn
            self.current_turn = -self.current_turn  # Switch turns
        else:
            raise ValueError("Cell is already filled")

    def __hash__(self) -> int:
        return hash(tuple(self.board.flatten()))

    def __eq__(self, r: "State") -> bool:
        return np.array_equal(self.board, r.board)

    def possible_moves(self) -> List[int]:
        return [i for i in range(9) if self.board[i // 3, i % 3] == 0]

    def terminated(self) -> bool:
        # Check if there's a winner or no empty cells left
        return self.winner() != 0 or not self.possible_moves()

    def winner(self) -> int:
        # Check rows, columns, and diagonals
        for i in range(3):
            if abs(sum(self.board[i, :])) == 3:  # Row win
                return self.board[i, 0]
            if abs(sum(self.board[:, i])) == 3:  # Column win
                return self.board[0, i]
        if (
            abs(self.board[0, 0] + self.board[1, 1] + self.board[2, 2]) == 3
        ):  # Diagonal win
            return self.board[1, 1]
        if (
            abs(self.board[0, 2] + self.board[1, 1] + self.board[2, 0]) == 3
        ):  # Anti-diagonal win
            return self.board[1, 1]
        return 0  # No winner


if __name__ == "__main__":
    # Example usage:
    s = State()
    s.print()  # Should print an empty board
    s.fill(0)  # X's move
    s.print()
    print("Turn:", s.turn())
    print("Possible moves:", s.possible_moves())
    print("Winner:", s.winner())
