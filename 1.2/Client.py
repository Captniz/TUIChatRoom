from cmath import rect
import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
import socket
import threading
from wsgiref.simple_server import server_version
import json
import os

HEADER = 64  # Set a header size for the messages
CLIENT = socket.gethostbyname(socket.gethostname())  # Get host ip
PORT = 5678  # Set a port
DECODER = 'utf-8'  # Set a decodder
DC_WORD = '%quit%'  # Set a password to quit

# Open a menu with a list of servers and connect to one of them


def LoadPreviousServers(stdscr):
    # Open the file with the servers
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "servers.json"), 'r') as f:
        data = json.load(f)  # Load the file in a dict
        while True:
            stdscr.clear()
            stdscr.addstr(
                "List of remembered servers, select one to connect (name): \n\n")
            for i in data:  # Display the list of server
                stdscr.addstr(f'{i}:{data[i]}\n')
            stdscr.refresh()
            # Create a new window textbox to write chosen server name
            win = curses.newwin(1, 30, 0, 58)
            box = Textbox(win)
            box.edit()
            stdscr.refresh()
            n = box.gather()
            n = str(n).strip()
            for i in data:
                if n == i:  # If the server name is in the list
                    return data[i]  # Return the ip of the chosen server
            stdscr.clear()  # If the server name is not in the list
            stdscr.addstr("Invalid option")  # Print invalid option
            stdscr.refresh()
            stdscr.getch()

# Get info about username and server ip or pick one from the previous servers (return -1 if the second option is chosen)


def Getinfo(stdscr, server):
    while True:
        stdscr.clear()
        # Ask if the user wants to connect to a previously connected server
        stdscr.addstr(
            "Do you want to connect to a previously connected server? (y/n)")
        stdscr.refresh()
        key = chr(stdscr.getch())
        if key == 'y':  # If the user wants to connect to a previously connected server return -1
            return -1
        elif key == 'n':  # If the user does not want to connect to a previously connected server ask for ip
            stdscr.clear()
            stdscr.addstr(
                "(TO EXECUTE THIS PROGRAM IS IMPORTANT TO PUT THIS WINDOW FULL SCREEN) Server ip: ")
            stdscr.refresh()
            # Create a new window textbox to write ip
            win = curses.newwin(2, 30, 1, 0)
            box = Textbox(win)
            box.edit()
            stdscr.refresh()
            ip = box.gather()  # Get server ip
            ip = str(ip).strip()
            data = {}
            remembered = False
            # Open the file with the servers
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "servers.json"), 'r') as f:
                data = json.load(f)  # Load the file in a dict
                for i in data:
                    if ip == data[i]:  # If the ip is in the list return ip
                        remembered = True
            if remembered == False:  # If the ip is not in the list ask for new server name
                with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "servers.json"), 'w') as f:
                    stdscr.clear()
                    stdscr.addstr("Name this server: ")  # Ask for server name
                    stdscr.refresh()
                    # Create a new window textbox to write name
                    win = curses.newwin(1, 30, 0, 18)
                    box = Textbox(win)
                    box.edit()
                    stdscr.refresh()
                    name = box.gather()
                    name = str(name).strip()
                    # Add the server name and ip to the list of servers
                    data[name] = ip
                    json.dump(data, f)  # Save the list of servers
            return ip
        else:  # If the user writes something else than y or n ask again
            stdscr.clear()
            stdscr.addstr("Invalid option")  # Print invalid option
            stdscr.refresh()
            stdscr.getch()

# Connect to the server and ask for username (returns it)


def Connect(stdscr, server, ip):
    server.connect((ip, PORT))  # Try to connect to the server
    stdscr.clear()
    # Print connection succesfull
    stdscr.addstr(f'Connected succesfully to {ip}')
    stdscr.getch()

    stdscr.clear()
    stdscr.addstr("Username:")
    stdscr.refresh()  # Ask for username
    # Create a new window textbox to write username
    win = curses.newwin(1, 30, 0, 10)
    box = Textbox(win)
    box.edit()
    stdscr.refresh()
    username = box.gather()  # Get username
    username = str(username).strip()
    return username  # Return username

# Recieve a single message and returns its content


def RecieveMessage(server):
    len = int(server.recv(HEADER).decode(DECODER))  # Clean the header message
    msg = server.recv(len).decode(DECODER)  # Recieve the message
    return msg  # Return the message

# A function for a thread that recieves messages and prints them on the screen, also handles the scrolling of the messages


def Recieve(server, pad):
    offset = 0
    temp = 0
    while True:
        msg = RecieveMessage(server)  # Recieve the message
        pad.addstr(msg)  # Add the message to the pad
        y, x = pad.getyx()
        if temp > 33:  # If the temp is over 33 the pad is full and the messages are scrolled
            offset = (y-34)  # Increase the offset in the pad
        else:
            temp = y  # Increase the temp until the pad is full
        refreshpad(pad, offset)  # Refresh the pad
        stdscr.refresh()

# A function for a thread that gets the user input and sends it to the server


def Send(stdscr, server, box, win):
    while True:
        win.clear()
        box.edit()
        stdscr.refresh()
        message = box.gather()  # Get message
        message = str(message).strip()  # Clean the message
        message = message + '\n'
        if message == '\n':  # If the message is empty do not send it
            pass
        else:
            # Send the length of the message to avoid errors
            server.send(bytes(f'{len(message):<{HEADER}}', DECODER))
            server.send(bytes(message, DECODER))  # Send the message


def main(stdscr, server):
    connected = False
    while connected == False:  # While the user is not connected ask for ip
        ip = Getinfo(stdscr, server)
        # If the user wants to connect to a previously connected server (GetInfo returns -1)
        if ip == -1:
            ip = LoadPreviousServers(stdscr)  # Load the previous servers
        try:
            # Connect to the server and ask for username
            username = Connect(stdscr, server, ip)
            connected = True  # Set connected to true
        except:  # If the connection fails ask for ip again
            stdscr.clear()
            # Print connection failed
            stdscr.addstr("Could not connect to server, try checking the ip")
            stdscr.getch()

    # Send the header
    server.send(bytes(f'{len(username):<{HEADER}}', DECODER))
    server.send(bytes(username, DECODER))  # Send the username
    stdscr.clear()
    # Print connection succesfull
    stdscr.addstr(f'Registered succesfully as {username}')
    stdscr.refresh()
    boxes = DrawTui(stdscr)  # Draw the text user interface
    # Start the recieve thread
    threading.Thread(target=Recieve, args=(server, boxes[0])).start()
    Send(stdscr, server, boxes[1], boxes[2])  # Start the send thread

# Draw the interface and the boxes for the user input and incoming messages
def DrawTui(stdscr):
    stdscr.clear()  # Clear the screen
    # Draw a rectangle for the message incoming
    rectangle(stdscr, 0, 0, 35, 150)
    pad = curses.newpad(500, 148)
    # Draw a rectangle for the message outgoing
    rectangle(stdscr, 36, 0, 45, 150)
    win = curses.newwin(8, 148, 37, 1)
    box = Textbox(win)
    stdscr.refresh()
    refreshpad(pad, 0)

    return (pad, box, win)

# Refresh the pad with the right coordinates
def refreshpad(pad, offset):
    # Refresh the pad with the right coordinates
    pad.refresh((0+offset), 0, 1, 1, 34, 149)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket
stdscr = curses.initscr()  # Init the screen
curses.noecho()  # Don't show the input (avoids double typed letters)
main(stdscr, server)  # Start the main function
