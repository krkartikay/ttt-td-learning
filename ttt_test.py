import unittest

from ttt import State


class TestState(unittest.TestCase):
    def test_initial_state(self):
        s = State()
        self.assertEqual(s.turn(), 1, "Initial turn should be 1 (X)")
        self.assertEqual(s.winner(), 0, "Initial state should have no winner")
        self.assertFalse(s.terminated(), "Initial state should not be terminated")
        self.assertEqual(
            s.possible_moves(),
            list(range(9)),
            "All cells should be possible moves in the initial state",
        )

    def test_fill_and_turn(self):
        s = State()
        s.fill(0)
        self.assertEqual(s.turn(), -1, "Turn should switch to -1 (O) after first move")
        self.assertNotIn(
            0, s.possible_moves(), "Position 0 should no longer be a possible move"
        )
        s.fill(1)
        self.assertEqual(
            s.turn(), 1, "Turn should switch back to 1 (X) after second move"
        )

    def test_invalid_fill(self):
        s = State()
        s.fill(0)
        with self.assertRaises(ValueError):
            s.fill(0)  # Trying to fill the same cell should raise an error

    def test_win_conditions(self):
        s = State()
        # Test row win for X
        s.fill(0)
        s.fill(3)
        s.fill(1)
        s.fill(4)
        s.fill(2)
        self.assertEqual(s.winner(), 1, "X should win with a row")
        self.assertTrue(s.terminated(), "Game should terminate when there is a winner")

        # Test column win for O
        s = State()
        s.fill(0)
        s.fill(3)
        s.fill(1)
        s.fill(4)
        s.fill(6)
        s.fill(5)
        self.assertEqual(s.winner(), -1, "O should win with a column")
        self.assertTrue(s.terminated(), "Game should terminate when there is a winner")

    def test_diagonal_win(self):
        s = State()
        s.fill(0)
        s.fill(1)
        s.fill(4)
        s.fill(2)
        s.fill(8)
        self.assertEqual(s.winner(), 1, "X should win with a diagonal")
        self.assertTrue(s.terminated(), "Game should terminate when there is a winner")

    def test_anti_diagonal_win(self):
        s = State()
        s.fill(2)
        s.fill(0)
        s.fill(4)
        s.fill(1)
        s.fill(6)
        self.assertEqual(s.winner(), 1, "X should win with an anti-diagonal")
        self.assertTrue(s.terminated(), "Game should terminate when there is a winner")

    def test_draw(self):
        s = State()
        moves = [0, 1, 2, 4, 3, 5, 7, 6, 8]  # A sequence leading to a draw
        for move in moves:
            s.fill(move)
        self.assertEqual(s.winner(), 0, "There should be no winner in a draw")
        self.assertTrue(s.terminated(), "Game should terminate in a draw")

    def test_copy_constructor(self):
        s1 = State()
        s1.fill(0)
        s1.fill(1)
        s2 = State(s1)
        self.assertEqual(s1, s2, "Copied state should be equal to original state")
        s1.fill(2)
        self.assertNotEqual(
            s1, s2, "Changes to original state should not affect copied state"
        )

    def test_hash_equality(self):
        s1 = State()
        s2 = State()
        self.assertEqual(
            hash(s1),
            hash(s2),
            "Hash values should be the same for identical initial states",
        )
        s1.fill(0)
        self.assertNotEqual(
            hash(s1), hash(s2), "Hash values should differ when board states differ"
        )


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
