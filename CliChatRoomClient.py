#TODO:
#fixxa ip
from pydoc import cli
import socket
from sqlite3 import connect
import threading
import time
import sys

HEADER_SIZE = 64
DECODER = "utf-8"


def ReceiveMsg(client,username):
    while True:
        sassuolo = client.recv(HEADER_SIZE)
        if not len(sassuolo):
            print('Connection closed by the server')
            sys.exit()
        sassuolo = int(sassuolo.decode(DECODER).strip())
        message = client.recv(sassuolo).decode(DECODER)
        print(f'\r{message}')
        print(f'{username} : ', end='', flush=True)


def SendMsg(client,username):
    while True:
        msg = input(username + ' : ')
        if msg == '\quit':
            sys.exit()
        msg = msg.encode(DECODER)
        msg = bytes(f'{len(msg):<{HEADER_SIZE}}', DECODER) + msg
        client.send(msg)


if __name__ == '__main__':
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip=input("ip:")
    ip.strip()
    print(ip)
    client.connect((ip, 5000))
    client.setblocking(1)

    username = input('Username: ')
    client.send(bytes(f'{len(username):<{HEADER_SIZE}}', DECODER))
    client.send(bytes(username, DECODER))
    
    threading.Thread(target=SendMsg, args=(client,username)).start()
    ReceiveMsg(client,username)