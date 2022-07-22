import curses
from curses.textpad import rectangle
import socket
import time

scr = curses.initscr()
scr.clear() 

text_win = curses.newpad(10, 10)
text_win.addstr("a\nab")
cury, curx = text_win.getyx()

text_win.addstr(f'\n\n{cury}\n{curx}')
text_win.addstr('A')

scr.refresh()
text_win.refresh(0, 0, 0, 0, 10, 10)

scr.getch()