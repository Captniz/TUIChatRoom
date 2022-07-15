#TODO:
#fixxa ip
#aggiungi history dei server
#aggiungi history messaggi
from curses.textpad import Textbox, rectangle
from pydoc import cli
import socket
from sqlite3 import connect
import threading
import time
import sys
import curses
from curses import wrapper

HEADER_SIZE = 64
DECODER = "utf-8"


def ReceiveMsg(client,username,stdscr,pad):
    while True:
        sassuolo = client.recv(HEADER_SIZE)
        if not len(sassuolo):
            print('Connection closed by the server')
            sys.exit()
        sassuolo = int(sassuolo.decode(DECODER).strip())
        message = client.recv(sassuolo).decode(DECODER)
        print(f'\r{message}')
        print(f'{username} : ', end='', flush=True)


def SendMsg(client,username,stdscr):
    while True:
        msg = input(username + ' : ')
        if msg == '\quit':
            sys.exit()
        msg = msg.encode(DECODER)
        msg = bytes(f'{len(msg):<{HEADER_SIZE}}', DECODER) + msg
        client.send(msg)


def main(stdscr):
    #region [ rgba(203, 166, 247, 0.2) ]   creo lo standard sceen
    stdscr.clear()
    stdscr.refresh()
    #endregion
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #creo il socket
    #region [ rgba(203, 166, 247, 0.2) ]   richiedo l'ip
    stdscr.addstr(0,0,"ip:")
    win=curses.newwin(1,30,0,3)
    box=Textbox(win)
    stdscr.refresh()
    box.edit()
    ip=box.gather()
    ip=ip.strip()
    stdscr.clear()
    #endregion
    client.connect((ip, 5000))  #connetto al server
    client.setblocking(1)       #sblocco il socket
    #region [ rgba(203, 166, 247, 0.2) ]    confermo la connessione e richiedo l'username
    stdscr.addstr(0,0,"Connection successful! Welcome to the server")
    stdscr.addstr(1,0,"username:")
    win=curses.newwin(1,30,1,10)
    box=Textbox(win)
    stdscr.refresh()
    box.edit()
    username=box.gather()
    username=username.strip()
    stdscr.clear()
    stdscr.refresh()
    #endregion
    #region [ rgba(203, 166, 247, 0.2) ]   avvio le due finestre per l'interfaccia
    rectangle(stdscr,0,0,31,101)
    #msgin=curses.newwin(30,100,1,1)
    rectangle(stdscr,32,0,36,101)
    msgout=curses.newwin(3,100,33,1)
    pad=curses.newpad(10000,100)
    stdscr.refresh()
    stdscr.getch()
    #endregion
    client.send(bytes(f'{len(username):<{HEADER_SIZE}}', DECODER))  #invio la lunghezza dell'username
    client.send(bytes(username, DECODER))                           #invio l'username
    
    threading.Thread(target=SendMsg, args=(client,username,stdscr)).start() #creo un thread per la scrittura dei messaggi
    ReceiveMsg(client,username)                                             #chiamo la funzione per ricevere i messaggi

if __name__ == '__main__':
    wrapper(main)                                                           #richiamo la funzione main con wrapper per lo stdscr