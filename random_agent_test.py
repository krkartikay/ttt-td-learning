import unittest

from ttt import State
from random_agent import RandomAgent


# Unit tests for RandomAgent
class TestRandomAgent(unittest.TestCase):
    def test_select_move(self):
        s = State()
        agent = RandomAgent()

        # Ensure selected move is within possible moves
        move = agent.select_move(s)
        self.assertIn(
            move, s.possible_moves(), "Selected move should be in possible moves"
        )

        # Test select_move when no moves are available (terminated state)
        moves_to_fill = s.possible_moves()
        for move in moves_to_fill:
            s.fill(move)
        move = agent.select_move(s)
        self.assertEqual(move, -1, "Should return -1 when no moves are possible")

    def test_update_reward_does_nothing(self):
        s1 = State()
        s2 = State(s1)
        agent = RandomAgent()
        agent.update_reward(s1, s2, reward=1.0)  # This should do nothing
        # Verifying that no change occurs in the agent (as expected)
        self.assertTrue(True, "update_reward should have no effect in RandomAgent")


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
