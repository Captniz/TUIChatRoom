from cmath import rect
import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
import socket
import threading
from wsgiref.simple_server import server_version

#region [rgba(255,255,255,0.05)]
#CONSTANTS

HEADER = 64                                                 #Set a header size for the messages
CLIENT = socket.gethostbyname(socket.gethostname())         #Get host ip
PORT = 5678                                                 #Set a port
DECODER = 'utf-8'                                           #Set a decodder
DC_WORD = '%quit%'                                         #Set a password to quit

#endregion

#region [rgba(255,255,255,0.05)]
#FUNCTIONS

def Connect(stdscr,server):
    connected=False
    while connected==False:                                         #While not connected
        stdscr.clear()
        stdscr.addstr("(TO EXECUTE THIS PROGRAM IS IMPORTANT TO PUT THIS WINDOW FULL SCREEN) Server ip: ")
        stdscr.refresh()                                            #Ask for ip
        win = curses.newwin(2, 30, 1, 0)                            #Create a new window textbox to write ip
        box = Textbox(win)
        box.edit()
        stdscr.refresh()
        ip = box.gather()                                           #Get server ip    
        ip = str(ip).strip()                                        #Clean the ip                        
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
    stdscr.refresh()                                                #Ask for username
    win = curses.newwin(1, 30 , 0, 10)                              #Create a new window textbox to write username
    box = Textbox(win)
    box.edit()
    stdscr.refresh()
    username = box.gather()                                         #Get username  
    username = str(username).strip() 
    server.send(bytes(f'{len(username):<{HEADER}}', DECODER))       #Send the header
    server.send(bytes(username, DECODER))                           #Send the username
    stdscr.clear()
    stdscr.addstr(f'Registered succesfully as {username}')          #Print connection succesfull
    stdscr.refresh()
    boxes = DrawTui(stdscr)                                         #Draw the test user interface
    threading.Thread(target=Recieve, args=(server,boxes[0])).start()#Start the recieve thread
    Send(stdscr,server,boxes[1],boxes[2])                           #Start the send thread

def RecieveMessage(server):
    len = int(server.recv(HEADER).decode(DECODER))                  #Clean the header message 
    msg = server.recv(len).decode(DECODER)                          #Recieve the message
    return msg                                                      #Return the message


def Recieve(server,pad):
    offset = 0
    temp = 0
    while True:
        msg = RecieveMessage(server)                                #Recieve the message
        pad.addstr(msg)                                             #Add the message to the pad
        if temp>33:                                                 #If the pad is full
            offset+=1                                               #Increase the offset
        else:
            temp+=1                                                 #Increase the temp
        refreshpad(pad,offset)                                      #Refresh the pad                               
        stdscr.refresh()
        

def Send(stdscr,server,box,win):
    while True:
        win.clear()
        box.edit()
        stdscr.refresh()
        message = box.gather()                                      #Get message                                        
        message = str(message)
        if message == DC_WORD:                                      #If the message is the password to quit
            server.send(bytes(f'{len(message):<{HEADER}}', DECODER))
            server.send(bytes(message, DECODER))
            exit(1)                                                 #Quit the program
        else:
            server.send(bytes(f'{len(message):<{HEADER}}', DECODER))
            server.send(bytes(message, DECODER))

def main(stdscr,server):
    Connect(stdscr,server)

def DrawTui(stdscr):
    stdscr.clear()                                                  #Clear the screen                            
    rectangle(stdscr,0,0,35,150)                                    #Draw a rectangle for the message incoming
    pad = curses.newpad(500, 148)
    rectangle(stdscr,36,0,45,150)                                   #Draw a rectangle for the message outgoing
    win = curses.newwin(8, 148, 37, 1)                            
    box = Textbox(win)                                            
    stdscr.refresh()
    refreshpad(pad,0)

    return (pad, box, win)

def refreshpad(pad, offset):
    pad.refresh((0+offset),0,1,1,34,149)

#endregion

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a socket
stdscr = curses.initscr()
curses.noecho()
main(stdscr,server)