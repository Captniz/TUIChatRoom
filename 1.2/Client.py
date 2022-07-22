from cmath import rect
import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
import socket
import threading
from wsgiref.simple_server import server_version
import json
import os

#region [rgba(255,255,255,0.05)]
#CONSTANTS

HEADER = 64                                                 #Set a header size for the messages
CLIENT = socket.gethostbyname(socket.gethostname())         #Get host ip
PORT = 5678                                                 #Set a port
DECODER = 'utf-8'                                           #Set a decodder
DC_WORD = '%quit%'                                          #Set a password to quit

#endregion

#region [rgba(255,255,255,0.05)]
#FUNCTIONS

def LoadPreviousServers(stdscr):

    with open(os.path.dirname(os.path.abspath(__file__)) + '\\servers.json', 'r') as f:
        data = json.load(f)
        while True:
            stdscr.clear()
            stdscr.addstr("List of remembered servers, select one to connect (name): \n\n")
            for i in data:
                stdscr.addstr(f'{i}:{data[i]}\n')
            stdscr.refresh()
            win = curses.newwin(1, 30, 0, 58)                            #Create a new window textbox to write ip
            box = Textbox(win)
            box.edit()
            stdscr.refresh()
            n = box.gather()                                        #Get server ip    
            n = str(n).strip()
            for i in data:
                if n == i:
                    return data[i]
            stdscr.clear()
            stdscr.addstr("Invalid option")
            stdscr.refresh()
            stdscr.getch()

#Get info about username and server ip or pick one from the previous servers (return -1 if the second option is chosen)
def Getinfo(stdscr,server):
    while True:
        stdscr.clear()
        stdscr.addstr("Do you want to connect to a previously connected server? (y/n)")
        stdscr.refresh()
        key = chr(stdscr.getch())
        if key == 'y':
            return -1
        elif key == 'n':
            stdscr.clear()
            stdscr.addstr("(TO EXECUTE THIS PROGRAM IS IMPORTANT TO PUT THIS WINDOW FULL SCREEN) Server ip: ")
            stdscr.refresh()                                            #Ask for ip
            win = curses.newwin(2, 30, 1, 0)                            #Create a new window textbox to write ip
            box = Textbox(win)
            box.edit()
            stdscr.refresh()
            ip = box.gather()                                           #Get server ip    
            ip = str(ip).strip()
            data = {}
            remembered = False
            with open(os.path.dirname(os.path.abspath(__file__)) + '\\servers.json', 'r') as f:
                data = json.load(f)
                for i in data:
                    if ip == data[i]:
                        remembered = True
            if remembered == False:
                with open(os.path.dirname(os.path.abspath(__file__)) + '\\servers.json', 'w') as f:
                    stdscr.clear()
                    stdscr.addstr("Name this server: ")
                    stdscr.refresh()                                            #Ask for ip
                    win = curses.newwin(1, 30, 0, 18)                            #Create a new window textbox to write ip
                    box = Textbox(win)
                    box.edit()
                    stdscr.refresh()
                    name = box.gather()                                           #Get server ip    
                    name = str(name).strip()
                    data[name] = ip
                    json.dump(data,f)
            return ip
        else:
            stdscr.clear()
            stdscr.addstr("Invalid option")
            stdscr.refresh()
            stdscr.getch()

#Connect to the server and login with the username 
def Connect(stdscr,server,ip):                                       #While not connected                  
    server.connect((ip, PORT))                              #Try to connect to the server
    stdscr.clear()
    stdscr.addstr(f'Connected succesfully to {ip}')         #Print connection succesfull
    stdscr.getch()  
    connected=True       

    stdscr.clear()
    stdscr.addstr("Username:")
    stdscr.refresh()                                                #Ask for username
    win = curses.newwin(1, 30 , 0, 10)                              #Create a new window textbox to write username
    box = Textbox(win)
    box.edit()
    stdscr.refresh()
    username = box.gather()                                         #Get username  
    username = str(username).strip() 
    return username

#Recieve a single message and returns its content
def RecieveMessage(server):
    len = int(server.recv(HEADER).decode(DECODER))                  #Clean the header message 
    msg = server.recv(len).decode(DECODER)                          #Recieve the message
    return msg                                                      #Return the message

#A function for a thread that recieves messages and prints them on the screen, also handles the scrolling of the messages
def Recieve(server,pad):
    offset = 0
    temp = 0
    while True:
        msg = RecieveMessage(server)                                #Recieve the message
        pad.addstr(msg)                                             #Add the message to the pad
        y,x = pad.getyx()
        if temp>33:                                                 #If the pad is full
            offset=(y-34)                                           #Increase the offset
        else:
            temp=y                                                  #Increase the temp
        refreshpad(pad,offset)                                      #Refresh the pad                               
        stdscr.refresh()
        
#A function for a thread that gets the user input and sends it to the server
def Send(stdscr,server,box,win):
    while True:
        win.clear()
        box.edit()
        stdscr.refresh()
        message = box.gather()                                 #Get message                                        
        message = str(message).strip()                         #Clean the message
        message = message + '\n'
        if message == '\n':                                    #If the message is the password to quit
            pass
        else:
            server.send(bytes(f'{len(message):<{HEADER}}', DECODER))
            server.send(bytes(message, DECODER))

def main(stdscr,server):
    connected = False
    while connected == False:
        ip = Getinfo(stdscr,server)
        if ip == -1:
            ip = LoadPreviousServers(stdscr)
        try:
            username = Connect(stdscr,server,ip)
            connected = True
        except:
            stdscr.clear()
            stdscr.addstr("Could not connect to server, try checking the ip")
            stdscr.getch()
    
    server.send(bytes(f'{len(username):<{HEADER}}', DECODER))       #Send the header
    server.send(bytes(username, DECODER))                           #Send the username
    stdscr.clear()
    stdscr.addstr(f'Registered succesfully as {username}')          #Print connection succesfull
    stdscr.refresh()
    boxes = DrawTui(stdscr)                                         #Draw the test user interface
    threading.Thread(target=Recieve, args=(server,boxes[0])).start()#Start the recieve thread
    Send(stdscr,server,boxes[1],boxes[2])                           #Start the send thread

#Draw the interface and the boxes for the user input and incoming messages
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

#Refresh the pad with the right coordinates
def refreshpad(pad, offset):
    pad.refresh((0+offset),0,1,1,34,149)

#endregion

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Create a socket
stdscr = curses.initscr()                                   #Init the screen
curses.noecho()                                             #Don't show the input (avoids double typed letters)
main(stdscr,server)                                         #Start the main function