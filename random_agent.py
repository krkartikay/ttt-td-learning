import random
from typing import Tuple

from ttt import State, value_to_symbol


class RandomAgent:

    def __init__(self, player: int):
        pass  # No initialization needed for a RandomAgent

    def select_move(self, s: State) -> Tuple[int, str]:
        possible_moves = s.possible_moves()
        return (
            random.choice(possible_moves) if possible_moves else -1,
            "random",
        )  # Returns -1 if no moves are available

    def update_reward(self, s: State, r: State, reward: float, move_type: str):
        pass  # No reward handling for a random agent


if __name__ == "__main__":
    # Example usage:
    s = State()
    agent = RandomAgent()
    while not s.terminated():
        s.print()
        move = agent.select_move(s)
        print("Random move selected by agent:", move)
        s.fill(move)
    s.print()
    print("Winner: ", value_to_symbol[s.winner()])
