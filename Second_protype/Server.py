import socket
import threading

#region [rgba(255,255,255,0.05)]
#CONSTANTS

HEADER = 64                                                 #Set a header size for the messages
SERVER = socket.gethostbyname(socket.gethostname())         #Get host ip
PORT = 5678                                                 #Set a port
DECODER = 'utf-8'                                           #Set a decodder
DC_WORD =  '%quit%'                                         #Set a password to quit
CLIENTS = []

#endregion

#region [rgba(255,255,255,0.05)]
#FUNCTIONS

def ShareMsg(msg):
    print(msg)                                                  #Print the message
    for client in CLIENTS:                                      #Send the message to all clients
        client.send(bytes(f'{len(msg):<{HEADER}}', DECODER))    #Send the header
        client.send(bytes(msg, DECODER))                        #Send the message

def RecieveMessage(client):
    len = int(client.recv(HEADER).decode(DECODER))      #Clean the header message 
    msg = client.recv(len).decode(DECODER)              #Recieve the message
    return msg                                          #Return the message

def Start(s):
    s.listen()                                                                  #Listen for connections

    while True:                                                                 #Loop for connections
        client, addr = s.accept()                                               #Accept the connection         
        thread = threading.Thread(target=HandleClient, args=(client, addr))     #Create a thread for the client
        thread.start()                                                          #Start the thread             

def HandleClient(client,addr):
    CLIENTS.append(client)                                                                      #Add the client to the list of clients         
    username = RecieveMessage(client)                                                           #Recieve the username
    ShareMsg(f'[SERVER]: Succesfully accepted connection from {addr}; username: {username}')    #Share the login message
   
    connected = True                                                                            #Set the connected variable to true         
    while connected == True:                                                                    #Loop for the client                
        msg = RecieveMessage(client)                                                            #Recieve the message
        if msg != DC_WORD:                                                                      #If the message is not the quit word
            ShareMsg(f'({username}): {msg}')                                                    #Share the message
        else:                                                                                   #If the message is the quit word               
            connected=False                                                                     #Set the connected variable to false             
            ShareMsg(f'[SERVER]: User {username}: {addr} disconnected')                         #Share the disconnect message
    client.close()                                                                              #Close the client
    CLIENTS.remove(client)                                                                      #Remove the client from the list of clients

#endregion

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #Create a TCP socket
s.bind((SERVER, PORT))                                      #Bind the socket to the port on the server (everithing that connects to the address goes to the socket)

print(f'Server started on ' + SERVER + ':' + str(PORT))     #Print the server ip and port
Start(s)                                                     #Start the server


