import curses
from curses import wrapper


def main(stdscr):
    stdscr.clear()
    stdscr.refresh()
    pad=curses.newpad(1000,200)
    stdscr.refresh()

    for i in range(2000):
        for j in range(26):
            char = chr(65+j)
            pad.addstr(char)

    pad.refresh(0,0,1,2,3,4)

    stdscr.getch()
    
if __name__ == '__main__':
    wrapper(main)     