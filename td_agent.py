import random
from typing import Tuple

from ttt import State, value_to_symbol
from metrics import log_metric, increment_metric

# Exploration hyperparamters

EXPLORE_COEFF = 0.1  # probability of selecting an 'exploratory move' at start

# Learning hyperparameters

STEP_SIZE_COEFF = 0.1  # TD learning 'step size' at the start

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
        self.steps = 1
        self.player = player
        # this should start with 0.5 as default value for each state
        # except for terminal states (which should be 0 or 1 depending on who won)
        # 1 only if self.player won (draw counts as 0.5)
        self.value_function = {}

        # we also maintain history of previous state and move type to help update
        self.previous_state = None
        self.previous_move_type = None

    def select_move(self, s: State) -> int:
        possible_moves = s.possible_moves()

        # Returns -1 if no moves are available
        if len(possible_moves) == 0:
            return -1

        # Firstly, roll a die to see if we're gonna make an exploratory move
        if random.random() < self.exploration_probability:
            # Yes, we will make an exploratory move
            self.previous_move_type = "random"
            self.previous_state = State(s)
            return random.choice(possible_moves)

        # Make a greedy move
        move_values = {}
        for move in possible_moves:
            r = s.fill(move)
            v = self.get_value(r)
            move_values[move] = v

        greedy_move = max(move_values, key=lambda move: move_values[move])
        print(move_values)
        if move_values[greedy_move] > 0.5:
            increment_metric("better_move", str(s) + str(move))

        self.previous_move_type = "greedy"
        return greedy_move

    def update_reward(self, new_state: State, reward: float):
        old_state = self.previous_state
        self.previous_state = State(new_state)
        if old_state is None:
            old_state = State()

        # this should be called only in case of 'greedy' moves!
        if self.previous_move_type == "random":
            increment_metric("update_reward_random")
            return

        increment_metric("update_reward_greedy")
        s_val = self.get_value(old_state)
        r_val = self.get_value(new_state)
        val_delta = r_val - s_val
        log_metric("s_val", s_val, old_state)
        log_metric("r_val", r_val, new_state)
        log_metric("td_error", val_delta)
        log_metric("td_update", self.step_size * val_delta)

        self.value_function[old_state] = s_val + self.step_size * val_delta
        # print("\n".join(f"{k}:{v}" for k, v in self.value_function.items()))

    def get_value(self, s: State):
        # if s is already there we return its value
        # otherwise we will need to initialize it with a value
        increment_metric("get_value")
        if s in self.value_function:
            return self.value_function[s]

        # next 4 branches initialize the value function with some default value
        # game is still ongoing, 0.5 probability of winning
        if not s.terminated():
            increment_metric("get_value_init", "unk")
            # self.value_function[s] = 0.5
            # return self.value_function[s]
            return 0.5

        # game ended, winner is us
        if s.winner() == self.player:
            increment_metric("get_value_init", "win")
            self.value_function[s] = 1
            return self.value_function[s]

        # game ended in a draw
        if s.winner() == 0:
            increment_metric("get_value_init", "draw")
            self.value_function[s] = 0.5
            return self.value_function[s]

        # game ended and we lost
        increment_metric("get_value_init", "lose")
        return 0
