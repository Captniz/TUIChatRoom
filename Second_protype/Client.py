import curses
from curses import wrapper
import socket
import threading

#region [rgba(255,255,255,0.05)]
#CONSTANTS

HEADER = 64                                                 #Set a header size for the messages
CLIENT = socket.gethostbyname(socket.gethostname())         #Get host ip
PORT = 5678                                                 #Set a port
DECODER = 'utf-8'                                           #Set a decodder
DC_WORD =  '%quit%'                                         #Set a password to quit

#endregion

#region [rgba(255,255,255,0.05)]
#FUNCTIONS

#endregion

# https://www.youtube.com/watch?v=3QiPPX-KeSc&t=1141s