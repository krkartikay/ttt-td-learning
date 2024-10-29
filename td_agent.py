import random
from typing import Tuple

from ttt import State, value_to_symbol

# Exploration hyperparamters

EXPLORE_COEFF = 0.1  # probability of selecting an 'exploratory move' at start
EXPLORE_DECAY = 0.001  # reduction in EXPLORE_COEFF after every step

# Learning hyperparameters

STEP_SIZE_COEFF = 0.1  # TD learning 'step size' at the start
STEP_SIZE_DECAY = 0.001  # reduction in STEP_SIZE_COEFF after every step

# =============================================================================
# Temporal Difference Learning Agent

# V(state) += (V(new state) - V(state)) * step size


class TDAgent:
    """Temporal Difference Learning Agent

    V(state) += (V(new state) - V(state)) * step size
    """

    # TODO: there should've surely been a better API possible
    # for select_move/update

    def __init__(self, player: int):
        """
        Initializes fresh TDAgent.
        player: which side are we playing as (-1 or 1 == O or X)
        """
        self.exploration_probability = EXPLORE_COEFF
        self.step_size = STEP_SIZE_COEFF
        self.player = player
        # this should start with 0.5 as default value for each state
        # except for terminal states (which should be 0 or 1 depending on who won)
        # 1 only if self.player won (draw counts as 0.5)
        self.value_function = {}

    def select_move(self, s: State) -> Tuple[int, str]:
        possible_moves = s.possible_moves()

        # Returns -1 if no moves are available
        if len(possible_moves) == 0:
            return -1

        # Firstly, roll a die to see if we're gonna make an exploratory move
        if random.random() < self.exploration_probability:
            # Yes, we will make an exploratory move
            return (random.choice(possible_moves), "random")

        # Make a greedy move
        move_values = {}
        for move in possible_moves:
            r = State(s)
            r.fill(move)
            v = self.get_value(r)
            move_values[move] = v

        greedy_move = max(move_values, key=lambda move: move_values[move])

        return (greedy_move, "greedy")

    def update_reward(self, s: State, r: State, reward: float, move_type: str):
        # this should be called only in case of 'greedy' moves!
        if move_type == "random":
            return

        s_val = self.get_value(s)
        r_val = self.get_value(r)
        val_delta = r_val - s_val
        self.value_function[s] = s_val + self.step_size * val_delta

        # update step size and exploratory move probability
        if self.step_size - STEP_SIZE_DECAY >= 0:
            self.step_size -= STEP_SIZE_DECAY
        if self.exploration_probability - EXPLORE_DECAY >= 0:
            self.exploration_probability -= EXPLORE_DECAY

    def get_value(self, s: State):
        # if s is already there we return its value
        # otherwise we will need to initialize it with a value
        if s in self.value_function:
            return self.value_function[s]

        # next 4 branches initialize the value function with some default value
        # game is still ongoing, 0.5 probability of winning
        if not s.terminated():
            self.value_function[s] = 0.5
            return self.value_function[s]

        # game ended, winner is us
        if s.winner() == self.player:
            self.value_function[s] = 1
            return self.value_function[s]

        # game ended in a draw
        if s.winner() == 0:
            self.value_function[s] = 0.5
            return self.value_function[s]

        # game ended and we lost
        return 0
