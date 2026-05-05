from curses import wrapper, initscr, start_color
import curses
from colorama import Fore, Back, Style
from time import sleep
import random

from board import Board, COLS, ROWS


class Tetris(Board):

    def __init__(self, scr):
        self.scr = scr
        self.init_colors()
        super().__init__()

    def set(self, y, x, id, color):
        super().set(y, x, id, color)
        self.scr.addch(y, x, " ", curses.color_pair(color))

    def debug(self, text):
        self.scr.addstr(ROWS, 0, text, curses.color_pair(3))

    def getkey(self):
        try:
            k = self.scr.getkey()
        except Exception:
            k = ""
        return k

    def fall(self, id, piece, color):
        row = 1
        col = 7
        rcol, rpiece = self.find_best_col(id, piece)
        prev_y = -1
        prev_x = -1
        k = ""
        while (True):
            if (k == "p" and self.getkey() == ""):
                continue
            k = self.getkey()
            if (k == "p"):
                continue
            elif (k == "n"):
                col -= 1
            elif (k == "m"):
                col += 1
            elif (k == "k"):
                piece = self.turn(piece)
            else:
                row += 1
            if (rpiece != piece and row > 2):
                piece = rpiece
                col = rcol

            if (k != "" and not self.can_move(id, row, col, piece)):
                piece = prev_piece
                col = prev_x
            if (not self.can_move(id, row, col, piece)):
                break
            if prev_y >= 0:
                self.hide(prev_y, prev_x, prev_piece)
            self.draw(id, row, col, piece, color)
            prev_y = row
            prev_x = col
            prev_piece = piece
            full = self.find_full_row()
            if full:
                self.remove(full)
            self.scr.refresh()
            self.scr.refresh()

    def init_colors(self):
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_BLACK)


def main(stdscr):
    curses.use_default_colors()
    stdscr.clear()
    curses.curs_set(0)
    curses.cbreak()
    stdscr.nodelay(True)
    curses.halfdelay(5)
    curses.start_color()

    O = ((0, 0), (0, 1), (1, 0), (1, 1))
    L = ((0, 0), (1, 0), (2, 0), (2, 1))
    L1 = ((0, 0), (1, 0), (2, 0), (2, -1))
    I = ((0, 0), (1, 0), (2, 0), (3, 0))
    T = ((0, 0), (0, 1), (0, 2), (1, 1))
    Z = ((0, 0), (0, 1), (1, 1), (1, 2))
    Z1 = ((0, 0), (0, 1), (1, 0), (1, -1))

    pieces = (O, L, L1, I, T, Z, Z1)

    game = Tetris(stdscr)

    prevcol = 1
    random.seed()
    for id in range(1, 1000):
        color = random.choice(range(1, 7))
        game.fall(id, random.choice(pieces), color)

    stdscr.refresh()
    while(game.getkey() != "q"):
        pass


wrapper(main)
