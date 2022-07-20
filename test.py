import curses
import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("192.168.178.44", 5678))

print('yay')
