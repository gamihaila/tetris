from colorama import Fore, Back, Style
from curses import wrapper, initscr, start_color
import curses
from time import sleep
import random



COLS = 50
ROWS = 30
board = [0] * COLS * ROWS

for row in range(ROWS-1):
    board[row * COLS + 0] = -1
    board[row * COLS + COLS - 1] = -1
for col in range(COLS):
    board[(ROWS - 1) * COLS + col] = -1

def can_move(id, row, col, piece):
    for square in piece:
        y, x = square
        Y = row+y
        X = col+x
        if Y >= ROWS:
            return False
        if X >= COLS:
            return False
        square = board[Y* COLS + X]
        if square == 0:
            continue
        if square != id:
            return False
    return True

def draw(scr, id, row, col, piece, color):
    for square in piece:
        y, x = square
        Y = row+y
        X = col+x
        scr.addch(Y, X, " ", curses.color_pair(color))
        board[Y * COLS + X] = id

def hide(scr, row, col, piece):
    for square in piece:
        y, x = square
        Y = row+y
        X = col+x
        scr.addch(Y, X, " ", curses.color_pair(6))
        board[Y * COLS + X] = 0

def getkey(scr):
    try:
        k = scr.getkey()
    except Exception:
        k = ""
    return k
        
def fall(scr, id, row, col, piece, color):
    prev_y = -1
    prev_x = -1
    for i in range(ROWS):
        k = getkey(scr)
        if (k == "n"):
            col -= 1
        if (k == "m"):
            col += 1
        if (k == "k"):
            piece = turn(piece)
        if (not can_move(id, row+i, col, piece)):
            break
        if prev_y >= 0:
            hide(scr, prev_y, prev_x, prev_piece)
        draw(scr, id, row+i, col, piece, color)
        prev_y=row+i
        prev_x=col
        prev_piece = piece
        scr.refresh()
        sleep(0.3)
    scr.refresh()

def turn(piece):
    turned = []
    for y, x in piece:
        turned.append((x, -y))
    return turned

def main(stdscr):
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    MAGENTA = 5
    BLACK = 6
    colors = (RED, BLUE, GREEN, YELLOW, MAGENTA)
    stdscr.clear()
    #curses.resizeterm(ROWS, COLS)
    curses.curs_set(0)
    curses.cbreak()
    stdscr.nodelay(True)
    curses.halfdelay(1)

    curses.init_pair(RED, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(BLUE, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(GREEN, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(YELLOW, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(MAGENTA, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(BLACK, curses.COLOR_BLACK, curses.COLOR_BLACK)

    O = ((0,0), (0,1), (1,0), (1,1))
    L = ((0,0), (1,0), (2,0), (2,1))
    L1 = ((0,0), (1,0), (2,0), (2,-1))
    I = ((0,0), (1,0), (2,0), (3,0))
    T = ((0,0), (0,1), (0,2), (1,1))
    Z = ((0,0), (0,1), (1,1), (1,2))
    Z1 = ((0,0), (0,1), (1,0), (1,-1))

    pieces = (O, L, L1, I, T, Z, Z1)

    color = random.choice(colors)

    prevcol = BLACK
    random.seed()
    for id in range(1, 100):
        while(True):
            color = random.choice(colors)
            if (color != prevcol):
                break
        fall(stdscr, id, 3, 24, random.choice(pieces), color)
        prevcol = color

    
    stdscr.refresh()
    while(getkey(stdscr) != "q"):
        pass


wrapper(main)







