#--- back ----

import threading
import socket
import os

#STATIC
SIZE_OF_HEADER = 64
SERVER_IP = "0.0.0.0"
SERVER_PORT = 3000
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
CLIENT_DISCONNECT_MESSAGE = "/exit"
FORMAT_OF_MESSAGE_IN_SOCKET = "utf-8"
path_private = "private"

def send(client,message):
    message = message.encode(FORMAT_OF_MESSAGE_IN_SOCKET)
    length_of_message = len(message) #check this one why do we store the length in string then int
    length_of_message = str(length_of_message).encode(FORMAT_OF_MESSAGE_IN_SOCKET)
    length_of_message += b' ' * (SIZE_OF_HEADER - len(length_of_message))#lets add the few bytes to make the size of header = 64, so if the 'length_of_message' is 24  we need to add 64-24=40bytes
    #this is because we make server read EXACTLY 64 bytes so now we must send EXACTLY 64 bytes
    client.send(length_of_message)
    #print(f"Sending: {message}")
    client.send(message)
    #print(f"Send!")

def recieve_message(connection, address, window):
    print(f"{address} connection established")
    connected = True

    while connected:
        message_size = connection.recv(SIZE_OF_HEADER).decode(FORMAT_OF_MESSAGE_IN_SOCKET)
        if message_size:
            message_size = int(message_size)
            message = connection.recv(message_size).decode(FORMAT_OF_MESSAGE_IN_SOCKET)
            if message == CLIENT_DISCONNECT_MESSAGE:
                connected = False

            chat = window['chat']
            chat.update(chat.get()+'\n client#1: ' + message)
            #print(f"[{address}] {message}")
        
    connection.close()

#--- front ---
import PySimpleGUI as sg
sg.theme('DarkAmber')

layout = [[sg.Text('', key="chat")],
        [sg.InputText()],
          [sg.Button('Ok'), sg.Button('Cancel')]]

layout_first_time_pass = [[sg.Text('Enter passsword:'), sg.InputText()],
[sg.Text('Enter again:'), sg.InputText()],
[sg.Text('', key='messagePassword')],
          [sg.Button('Ok')]]

window = sg.Window('Client #2', layout)

#--- front ---

def client_start():
    global window
    if not os.path.exists(path_private):
        print("first time opening the app - lets create a password")
        window_password_creation = sg.Window('Client#2', layout_first_time_pass)
        while True:
            event, values = window_password_creation.read()
            if event == 'Ok':
                print("entered passw ", values[0], values[1])
                if(values[0] == values[1]):
                    window_password_creation.close()
                    break
                else:
                    window_password_creation['messagePassword'].update('\n passwords dont match')

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM because the order of the data that is sent is important 
    print("Client started...")
    print("Trying to connect...")
    client.connect(SERVER_ADDRESS)
    print("Connected!")
    recieve_message_thread = threading.Thread(target=recieve_message, args=(client, "base_client", window))
    recieve_message_thread.start()

  

    #while recieving thread is up lets send messages
    while True:
        #message = input()
        chat = window['chat']
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            print("Closing...")
            break
        chat.update(chat.get()+'\n client#2: ' + values[0])
        send(client, values[0])

client_start()
