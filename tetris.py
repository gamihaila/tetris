from colorama import Fore, Back, Style
from curses import wrapper, initscr, start_color
import curses
from time import sleep
import random

COLS = 20
ROWS = 30

class Tetris:

    def __init__(self, scr):
        self.board = [0] * COLS * ROWS
        self.board_color = [1] * COLS * ROWS
        self.scr = scr
        self.init_colors()
        for row in range(ROWS-1):
            self.set(row, 0, -1, 4)
            self.set(row, COLS-1, -1, 4)
            for col in range(1, COLS-1):
                self.set(row, col, 0, 6)
        for col in range(COLS):
            self.set(ROWS - 1, col, -1, 4)

    def debug(self, text):
        self.scr.addstr(ROWS, 0, text, curses.color_pair(3))
            
    def set(self, y, x, id, color):
        self.board[y * COLS + x] = id
        self.board_color[y * COLS + x] = color
        self.scr.addch(y, x, " ", curses.color_pair(color))

    def clear(self, y, x):
        self.set(y, x, 0, 6)

    def get(self, y, x):
        if y < 0 or y >= ROWS or x < 0 or x >= COLS:
            return -1
        return self.board[y * COLS + x]
        
    def get_color(self, y, x):
        if y < 0 or y >= ROWS or x < 0 or x >= COLS:
            return -1
        return self.board_color[y * COLS + x]
        
    def can_move(self, id, row, col, piece):
        for y,x in piece:
            Y = row+y
            X = col+x
            square = self.get(Y, X)
            if square == 0:
                continue
            if square != id:
                return False
        return True

    def draw(self, id, row, col, piece, color):
        for y, x in piece:
            self.set(row+y, col+x, id, color)

    def hide(self, row, col, piece):
        for y, x in piece:
            self.clear(row+y, col+x)

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
            prev_y=row
            prev_x=col
            prev_piece = piece
            full = self.find_full_row()
            if full:
                self.remove(full)
            self.scr.refresh()
            self.scr.refresh()

    def potential_energy(self, piece, row):
        energy = 0
        for y, x in piece:
            energy += (ROWS-2-(row+y))
        return energy

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
        for orientation in range(4):
            piece = self.turn(piece)
            for col in range(COLS):
                row = self.find_lowest_row(id, col, piece)
                energy = self.potential_energy(piece, row)
                if energy < min_potential_energy:
                    min_potential_energy = energy
                    best_col = col
                    best_piece = piece
        #self.debug('E = {}   '.format(min_potential_energy))
        return best_col, best_piece

    def turn(self, piece):
        turned = []
        for y, x in piece:
            turned.append((x, -y))
        return turned

    def find_full_row(self):
        for row in range(ROWS-1):
            full = True
            for col in range(COLS):
                if self.get(row, col) == 0:
                    full = False
            if full:
                return row
        return None

    def remove(self, row):
        for dy in range(0, row-1):
            for col in range(1, COLS-1):
                self.set(row-dy, col, self.get(row-dy-1, col),
                         self.get_color(row-dy-1, col))
            
    def init_colors(self):
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)	
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)	
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)	
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_BLACK)	
        #    for i in range(0, curses.COLORS):
        #        curses.init_pair(i + 1, i, i)


def main(stdscr):
    curses.use_default_colors()
    stdscr.clear()
    curses.curs_set(0)
    curses.cbreak()
    stdscr.nodelay(True)
    curses.halfdelay(5)
    curses.start_color()

    O = ((0,0), (0,1), (1,0), (1,1))
    L = ((0,0), (1,0), (2,0), (2,1))
    L1 = ((0,0), (1,0), (2,0), (2,-1))
    I = ((0,0), (1,0), (2,0), (3,0))
    T = ((0,0), (0,1), (0,2), (1,1))
    Z = ((0,0), (0,1), (1,1), (1,2))
    Z1 = ((0,0), (0,1), (1,0), (1,-1))

    pieces = (O, L, L1, I, T, Z, Z1)

    game = Tetris(stdscr)

    #game.set(3, 4, 5, 3)



    prevcol = 1
    random.seed()
    for id in range(1, 1000):
        color = random.choice(range(1, 6))
        game.fall(id, random.choice(pieces), color)
    
    stdscr.refresh()
    while(game.getkey() != "q"):
        pass


wrapper(main)







