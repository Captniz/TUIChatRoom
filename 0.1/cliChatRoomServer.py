#TODO:
#fai si che il server non scoppi quando escidal client esce in modo fornzato o meno
#per renderlo disponibile da remoto usare il port forwarding
from pydoc import cli
import socket
from sqlite3 import connect
import threading
import time

HEADER_SIZE = 64
DECODER = "utf-8"
SERVER = "0.0.0.0"

def SendToAll(clients,msg,username,activeClient):
    for client in clients:
        if client != activeClient:
            message = username + ' : ' + msg
            client.send(bytes(f'{len(message):<{HEADER_SIZE}}', DECODER))
            client.send(bytes(message, DECODER))


def HandleUser(clientsocket, address, username,clients):
    connected = True
    while connected==True:
        len = clientsocket.recv(HEADER_SIZE).decode(DECODER)
        message = clientsocket.recv(int(len)).decode(DECODER)
        if message == '\\quit':
            print(f'0 - Disconnected : {username} -> ' + str(address[0]) + ':' + str(address[1]))
            clientsocket.close()
            connected = False
            clients.remove(clientsocket)
            exit()
        print(f'{username} : {message}')
        SendToAll(clients,message,username,clientsocket)


def HandleConnections(s,clients):
    while True:
        clientsocket, address = s.accept()                                                                      #accetto la connessione
        len = clientsocket.recv(HEADER_SIZE).decode(DECODER)                                                    #ricevo la lunghezza del username
        username = clientsocket.recv(int(len)).decode(DECODER)                                                  #ricevo il username
        print(f'Accepted connection from : {username} -> ' + str(address[0]) + ':' + str(address[1]))
        clients.append(clientsocket)                                                                            #aggiungo il client alla lista
        threading.Thread(target=HandleUser, args=(clientsocket,address,username,clients)).start()               # Create a new thread to handle the connection


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostbyname('localhost'), 5000))
    s.listen(20)
    print(f'Server started on {SERVER}')

    clients = []

    HandleConnections(s,clients)