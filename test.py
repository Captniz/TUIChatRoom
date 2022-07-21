import curses
from curses.textpad import rectangle
import socket
import time

stdscr = curses.initscr() #Initialize curses
curses.noecho() #Don't show the user input
stdscr.clear() #Clear the screen
rectangle(stdscr,0,0,35,150)
rectangle(stdscr,36,0,45,150)
stdscr.refresh() #Refresh the screen
stdscr.getch() #Wait for a keypress
