import socket
import threading

#Get host ip
SERVER = socket.gethostbyname('localhost')
#set a port
PORT = 5678
#create a TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind the socket to the port on the server (everithing that connects to the address goes to the socket)
s.bind((SERVER, PORT))