COLS = 20
ROWS = 30


class Board:
    """Pure-Python Tetris board geometry, independent of any rendering."""

    def __init__(self):
        self.board = [0] * COLS * ROWS
        self.board_color = [1] * COLS * ROWS
        for row in range(ROWS - 1):
            self.set(row, 0, -1, 4)
            self.set(row, COLS - 1, -1, 4)
            for col in range(1, COLS - 1):
                self.set(row, col, 0, 7)
        for col in range(COLS):
            self.set(ROWS - 1, col, -1, 4)

    def set(self, y, x, id, color):
        self.board[y * COLS + x] = id
        self.board_color[y * COLS + x] = color

    def clear(self, y, x):
        self.set(y, x, 0, 7)

    def get(self, y, x):
        if y < 0 or y >= ROWS or x < 0 or x >= COLS:
            return -1
        return self.board[y * COLS + x]

    def get_color(self, y, x):
        if y < 0 or y >= ROWS or x < 0 or x >= COLS:
            return -1
        return self.board_color[y * COLS + x]

    def can_move(self, id, row, col, piece):
        for y, x in piece:
            square = self.get(row + y, col + x)
            if square == 0:
                continue
            if square != id:
                return False
        return True

    def draw(self, id, row, col, piece, color):
        for y, x in piece:
            self.set(row + y, col + x, id, color)

    def hide(self, row, col, piece):
        for y, x in piece:
            self.clear(row + y, col + x)

    @staticmethod
    def turn(piece):
        return [(x, -y) for y, x in piece]

    def find_full_row(self):
        for row in range(ROWS - 1):
            full = True
            for col in range(COLS):
                if self.get(row, col) == 0:
                    full = False
            if full:
                return row
        return None

    def remove(self, row):
        for dy in range(0, row - 1):
            for col in range(1, COLS - 1):
                self.set(row - dy, col, self.get(row - dy - 1, col),
                         self.get_color(row - dy - 1, col))

    def potential_energy(self, piece, row):
        energy = 0
        for y, _ in piece:
            energy += (ROWS - 2 - (row + y))
        return energy

    def num_blocked_squares(self, row, col, piece):
        num = 0
        for y, x in piece:
            if self.get(row + y + 1, col + x) == 0:
                num += 1
        return num

    def find_lowest_row(self, id, col, piece):
        max_row = -1
        for row in range(ROWS):
            if self.can_move(id, row, col, piece):
                max_row = row
        return max_row

    def find_best_col(self, id, piece):
        best_col = 0
        best_piece = piece
        min_potential_energy = ROWS * 4
        for _ in range(4):
            piece = self.turn(piece)
            for col in range(COLS):
                row = self.find_lowest_row(id, col, piece)
                energy = self.potential_energy(piece, row)
                blocked = self.num_blocked_squares(row, col, piece)
                energy += 5 * blocked
                if energy < min_potential_energy:
                    min_potential_energy = energy
                    best_col = col
                    best_piece = piece
        return best_col, best_piece
