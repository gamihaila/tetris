import unittest

from board import Board, COLS, ROWS


class TurnTests(unittest.TestCase):

    def test_turn_four_times_is_identity(self):
        pieces = [
            [(0, 0), (0, 1), (1, 0), (1, 1)],    # O
            [(0, 0), (1, 0), (2, 0), (2, 1)],    # L
            [(0, 0), (1, 0), (2, 0), (3, 0)],    # I
            [(0, 0), (0, 1), (0, 2), (1, 1)],    # T
            [(0, 0), (0, 1), (1, 1), (1, 2)],    # Z
        ]
        for p in pieces:
            rotated = list(p)
            for _ in range(4):
                rotated = Board.turn(rotated)
            self.assertEqual(sorted(rotated), sorted(p))

    def test_turn_rotates_i_piece_90_degrees(self):
        I = [(0, 0), (1, 0), (2, 0), (3, 0)]
        self.assertEqual(
            sorted(Board.turn(I)),
            sorted([(0, 0), (0, -1), (0, -2), (0, -3)]),
        )

    def test_turn_rotates_square_into_itself(self):
        O = [(0, 0), (0, 1), (1, 0), (1, 1)]
        self.assertEqual(sorted(Board.turn(O)), sorted([(0, 0), (1, 0), (0, -1), (1, -1)]))


class FullRowTests(unittest.TestCase):

    def test_empty_board_has_no_full_rows(self):
        board = Board()
        self.assertIsNone(board.find_full_row())

    def test_completely_filled_interior_row_is_full(self):
        board = Board()
        target = 5
        for col in range(1, COLS - 1):
            board.set(target, col, 1, 1)
        self.assertEqual(board.find_full_row(), target)

    def test_row_with_a_gap_is_not_full(self):
        board = Board()
        target = 5
        for col in range(1, COLS - 1):
            board.set(target, col, 1, 1)
        board.clear(target, 10)
        self.assertIsNone(board.find_full_row())

    def test_returns_topmost_full_row_when_multiple_exist(self):
        board = Board()
        for target in (5, 7):
            for col in range(1, COLS - 1):
                board.set(target, col, 1, 1)
        self.assertEqual(board.find_full_row(), 5)


class RemoveTests(unittest.TestCase):

    def test_remove_shifts_interior_row_down(self):
        board = Board()
        board.set(3, 5, 9, 3)
        board.remove(4)
        self.assertEqual(board.get(4, 5), 9)
        self.assertEqual(board.get_color(4, 5), 3)


class CanMoveTests(unittest.TestCase):

    def test_can_move_into_empty_space(self):
        board = Board()
        piece = [(0, 0), (0, 1), (1, 0), (1, 1)]
        self.assertTrue(board.can_move(1, 2, 5, piece))

    def test_cannot_move_into_side_wall(self):
        board = Board()
        piece = [(0, 0), (0, 1), (1, 0), (1, 1)]
        self.assertFalse(board.can_move(1, 2, 0, piece))

    def test_cannot_move_into_floor(self):
        board = Board()
        piece = [(0, 0), (0, 1), (1, 0), (1, 1)]
        self.assertFalse(board.can_move(1, ROWS - 1, 5, piece))


if __name__ == "__main__":
    unittest.main()
