import curses
from curses import wrapper
from curses.textpad import Textbox
import socket
import threading
from wsgiref.simple_server import server_version

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

def Connect(stdscr,server):

    connected=False
    while connected==False:                                         #While not connected
        stdscr.clear()
        stdscr.addstr("Server ip:")
        stdscr.refresh()                                            #Ask for ip
        win = curses.newwin(1, 30 , 0, 10)                          #Create a new window textbox to write ip
        box = Textbox(win)
        box.edit()
        stdscr.refresh()
        ip = box.gather()                                           #Get server ip    
        ip.strip()                                                  #Clean the ip                        
        try:
            server.connect((ip, PORT))                              #Try to connect to the server
            stdscr.clear()
            stdscr.addstr(f'Connected succesfully to {ip}')         #Print connection succesfull
            stdscr.getch()  
            connected=True
            
        except:                                                     #If not connected        
            stdscr.clear()
            stdscr.addstr("Could not connect to server")            #Print error message
            stdscr.getch()                                          #Wait for keypress and retry
    
    stdscr.clear()
    stdscr.addstr("Username:")
    stdscr.refresh()                                            #Ask for username
    win = curses.newwin(1, 30 , 0, 10)                          #Create a new window textbox to write username
    box = Textbox(win)
    box.edit()
    stdscr.refresh()
    username = box.gather()                                      #Get username  
    server.send(bytes(f'{len(username):<{HEADER}}', DECODER))    #Send the header
    server.send(bytes(username, DECODER))                        #Send the username

def Recieve():
    pass

def Send():
    pass

def main(stdscr,server):
    Connect(stdscr,server)


#endregion

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a socket
stdscr = curses.initscr()
main(stdscr,server)

#WHY DOES CURSES WRITE ON THE SCREEN DOUBLE THE LETTERS I TYPE!!?!