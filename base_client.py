#--- back ---

from optparse import Values
import threading
import socket
import os
import os
path_private = "private"

#STATIC
SIZE_OF_HEADER = 64
IP = socket.gethostbyname(socket.gethostname())
PORT = 3000
ADDRESS = (IP, PORT)
FORMAT_OF_MESSAGE_IN_SOCKET = "utf-8" 
CLIENT_DISCONNECT_MESSAGE = "/exit"
DEV_ENV = True
connected = False
pass_right = False

#FILE UPLOAD RELATED
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step

#-----



#this is a separate thread  
#it runs when a connection is established with second client
#then recieves messages and updates the chat text in ui
def client_connection(connection, address, window):
    global connected
    print(f"{address} connection established")

    while connected:
        message_size = connection.recv(SIZE_OF_HEADER).decode(FORMAT_OF_MESSAGE_IN_SOCKET)
        if message_size:
            message_size = int(message_size)
            message = connection.recv(message_size).decode(FORMAT_OF_MESSAGE_IN_SOCKET)
            if message == CLIENT_DISCONNECT_MESSAGE:
                print("Client disconnnected.")
                connected = False
 
            #print(f"[{address}] {message}")
            chat = window['chat']
            chat.update(chat.get()+'\n client#2: ' + message)
        
    connection.close()

#taking a string and turn it into a message that we can send
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

def send_file(client, message, file):

    message = message.encode(FORMAT_OF_MESSAGE_IN_SOCKET)
    length_of_message = len(message) #check this one why do we store the length in string then int
    length_of_message = str(length_of_message).encode(FORMAT_OF_MESSAGE_IN_SOCKET)
    length_of_message += b' ' * (SIZE_OF_HEADER - len(length_of_message))#lets add the few bytes to make the size of header = 64, so if the 'length_of_message' is 24  we need to add 64-24=40bytes
    #this is because we make server read EXACTLY 64 bytes so now we must send EXACTLY 64 bytes
    client.send(length_of_message)
    #print(f"Sending: {message}")
    client.send(message)

#--- front ---
import PySimpleGUI as sg
sg.theme('DarkAmber')

layout = [[sg.Text('Chat:')],
    [sg.Text('', key="chat")],
        [sg.InputText(do_not_clear=False)],
          [sg.Button('Ok')],
          [sg.Text('Send file:')],
          [sg.Text('File:', size=(8, 1)), sg.Input( key="file"), sg.FileBrowse('FileBrowse')],
          [sg.Button('Send file'), sg.Cancel()]]

layout_first_time_pass = [[sg.Text('Enter passsword:'), sg.InputText()],
[sg.Text('Enter again:'), sg.InputText()],
[sg.Text('', key='messagePassword')],
          [sg.Button('Ok')]]

layout_pass = [[sg.Text('Enter passsword:'), sg.InputText()],
          [sg.Button('Ok')]]

window = sg.Window('Client #1', layout)
# --- main ---

def base_client_start():
    global connected
    global window
    global pass_right
    if DEV_ENV == False:
        if not os.path.exists(path_private):
            print("first time opening the app - lets create a password")
            window_password_creation = sg.Window('Client#1', layout_first_time_pass)
            while True:
                event, values = window_password_creation.read()
                if event == sg.WIN_CLOSED or event == 'Cancel':
                    print("Closing the password creator window...")
                    break
                if event == 'Ok':
                    print("entered passw ", values[0], values[1])
                    if(values[0] == values[1]):
                        #writing private key to file
                        os.makedirs(path_private)
                    # f = open('private/mykey.pem','wb')
                    # f.write(values[0])
                    # f.close()
                        window_password_creation.close()
                        break
                    else:
                        window_password_creation['messagePassword'].update('\n passwords dont match')
        else:
            print("pass aready set - type in password")   
            window_pass = sg.Window('Client#1', layout_pass)
            while True:
                event, values = window_pass.read()
                if event == sg.WIN_CLOSED or event == 'Cancel':
                    print("Closing the password creator window...")
                    break
                if event == 'Ok':
                    print("entered passw ", values[0])
                    window_pass.close()
                    break
                    #jezeli haslo dobre odszyfruj 
                    #jezeli nie to pisz bzdury
                    # if(values[0] == values[1]):
                    #     pass_right = True
                    #     window_pass.close()
                    #     break
                    # else:
                    #     window_pass.close()
                    #     break


    print("Starting the base client...")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM because the order of the data that is sent is important 
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #to not show the error: address already in use
    client.bind(ADDRESS)

    client.listen()
    print("Base client running...")
    print("Waiting for the second client...")
    connection, address = client.accept()
    connected = True
    connection_thread = threading.Thread(target=client_connection, args=(connection,"client", window))
    connection_thread.start()
    #while recieving thread is up lets send messages

    while True:
        #message = input()
        chat = window['chat']
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            print("Closing...")
            break
        if event == 'Send file':
            send_file(connection, os.path.splitext(values['FileBrowse'][0]))

        #print('You entered ',values[0])
        chat.update(chat.get()+'\n client#1: ' + values[0])
        send(connection, values[0])
    client.close()
    connected = False
    print("Connection closed.")

base_client_start()
window.close()
