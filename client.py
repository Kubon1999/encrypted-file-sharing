#--- back ----

from calendar import c
import threading
import socket
import os
from turtle import down
from requests import session
import tqdm
import math
import rsa
import klucze as keys

#STATIC
SIZE_OF_HEADER = 64
SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 3000
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
CLIENT_DISCONNECT_MESSAGE = "/exit"
FORMAT_OF_MESSAGE_IN_SOCKET = "utf-8"
path_private = "private"
recv_file_mode = False
downloading = False
DEV_ENV = False
mode = 'cbc' # cbc or ecb

key_len = 2048 #RSA key length
path_private = "private_client"
path_public = "public_client"
file_private = "private.pem"
file_public = "public.pem"
private_path_to_file = os.path.join(path_private, file_private)
public_path_to_file = os.path.join(path_public, file_public)


#FILE UPLOAD RELATED
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step
CLIENT_SENT_FILE_MESSAGE = "/file"

#-----

#PUBLIC KEY RELATED
CLIENT_SEND_PUBLIC_KEY = "/key"
recv_public_key_mode = False
public_key_base_client = ""
pass_hash = ""
#----

#SESSION
CLIENT_SEND_SESSION = "/session"
recv_public_session = False
session_key = ""
#----

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

def send_key(client):
    send(client, "/key")
    print("sending a public key...")
    readRSAKey = keys.readRSAKey(pass_hash, public_path_to_file)
    send(client, readRSAKey.decode(FORMAT_OF_MESSAGE_IN_SOCKET))


def send_file(client, file):
    # get the file size
    filesize = os.path.getsize(file)
    filename = os.path.basename(file)
    #send a information to the client that we will soon send you a file
    send(client, "/file")

    # start sending the file
    print("sending a file...")
    # send the filename and filesize
    #the message we want to send
    message = f"{filename}{SEPARATOR}{filesize}"
    
    message = message.encode(FORMAT_OF_MESSAGE_IN_SOCKET)
    length_of_message = len(message) #check this one why do we store the length in string then int
    length_of_message = str(length_of_message).encode(FORMAT_OF_MESSAGE_IN_SOCKET)
    length_of_message += b' ' * (SIZE_OF_HEADER - len(length_of_message))#lets add the few bytes to make the size of header = 64, so if the 'length_of_message' is 24  we need to add 64-24=40bytes
    #this is because we make server read EXACTLY 64 bytes so now we must send EXACTLY 64 bytes
    client.send(length_of_message)
    #print(f"Sending: {message}")
    client.send(message)


    # --- send file in chunks function ---
    
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(file, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                print("file send done!")
                downloading = False
                recv_file_mode = False
                f.close()
                break
            client.send(bytes_read)
            # we use sendall to assure transimission in 
            # busy networks
            # update the progress bar
            #print("part of file send! continue...")
            progress.update(len(bytes_read))
    # close the socket
   # client.close()
    # --- end ---

def recieve_message(connection, address, window):
    global recv_file_mode
    global recv_public_key_mode
    global recv_public_session
    global downloading
    print(f"{address} connection established")
    send_key(connection)
    connected = True

    while connected:
        if recv_file_mode and not downloading:
            #recieving file
            print("reciving a file...")
            recieve_a_file(connection)
            recv_file_mode = False
        elif recv_public_key_mode:
            print("recieving a public key")
            recieve_public_key(connection)
            recv_public_key_mode = False
        elif recv_public_session:
            print("recieving a session key")
            recieve_session_key(connection)
            recv_public_session = False
        else:
            #recieving a text message
            message_size = connection.recv(SIZE_OF_HEADER).decode(FORMAT_OF_MESSAGE_IN_SOCKET)        
            if session_key:
                #decode
                pk = keys.readRSAKey(pass_hash, private_path_to_file)
                pk = rsa.PrivateKey.load_pkcs1(pk)
                print(len(message_size))
                #print(len(pk))
                print(type(message_size))
                print(type(pk))
                string = '=' * (-len(message_size) % 4)
                if string:
                    message_size = message_size + string.encode()
                print(len(message_size))
                #print(len(pk))
                print(type(message_size))
                print(type(pk))
                message_size = keys.decryptWithPrivateKey(pk, message_size)
                print("wiadomosc size")
                print(message_size)
            if message_size:
                message_size = int(message_size)
                message = connection.recv(message_size).decode(FORMAT_OF_MESSAGE_IN_SOCKET)
                if session_key:
                    #decode
                    pk = keys.readRSAKey(pass_hash, private_path_to_file)
                    pk = rsa.PrivateKey.load_pkcs1(pk)
                    print(len(message))
                    #print(len(pk))
                    print(type(message))
                    print(type(pk))
                    string = '=' * (-len(message) % 4)
                    if string:
                        message = message + string.encode()
                    print(len(message))
                    #print(len(pk))
                    print(type(message))
                    print(type(pk))
                    message = keys.decryptWithPrivateKey(pk, message)
                    print("wiadomosc")
                    print(message)
                if message == CLIENT_DISCONNECT_MESSAGE:
                    connected = False
                    print("disconnected")
                elif message == CLIENT_SENT_FILE_MESSAGE:
                    print("preparing to recieve a file from client...")
                    recv_file_mode = True
                elif message == CLIENT_SEND_PUBLIC_KEY:
                    print("preparing to recieve a public key from client...")
                    recv_public_key_mode = True
                elif message == CLIENT_SEND_SESSION:
                    print("preparing to recieve a session key from client...")
                    recv_public_session = True                
                else:
                    #normal message
                    chat = window['chat']
                    chat.update(chat.get()+'\n client#1: ' + message)
    connection.close()

def recieve_session_key(connection):
    global session_key
    message_size = connection.recv(SIZE_OF_HEADER).decode(FORMAT_OF_MESSAGE_IN_SOCKET)       
    message_size = int(message_size)
    session_key_from_message = connection.recv(message_size).decode(FORMAT_OF_MESSAGE_IN_SOCKET)

    private_key = keys.readRSAKey(pass_hash, private_path_to_file)
    private_key = rsa.PrivateKey.load_pkcs1(private_key)
    session_key = keys.decryptWithPrivateKey(private_key, session_key_from_message)
    print(session_key)
    return

def recieve_public_key(connection):
    global public_key_base_client
    message_size = connection.recv(SIZE_OF_HEADER).decode(FORMAT_OF_MESSAGE_IN_SOCKET)       
    message_size = int(message_size)
    message = connection.recv(message_size).decode(FORMAT_OF_MESSAGE_IN_SOCKET)
    public_key_base_client = message
    print(public_key_base_client)
    return 

def recieve_a_file(connection):
    global downloading
    downloading = True
    #first get info about the file (filename and size)
    # --- get file info size ---
    message_size = connection.recv(SIZE_OF_HEADER).decode(FORMAT_OF_MESSAGE_IN_SOCKET)
    message_size = int(message_size)
    # --- get file info ---
    message_info = connection.recv(message_size).decode(FORMAT_OF_MESSAGE_IN_SOCKET)
    filename, filesize = message_info.split(SEPARATOR)
    # remove absolute path if there is
    filename = os.path.basename(filename)
    # convert to integer
    filesize = int(filesize)
    print("Got file info:")
    print(filename)
    print(filesize)
    # --- then get the whole file --- 
    # start receiving the file from the socket
    # and writing to the file stream
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    number_of_packages = math.floor(filesize / BUFFER_SIZE)
    #print("number of packages(4096): " + number_of_packages)
    last_package_size = filesize-(number_of_packages*BUFFER_SIZE)
   # print("last package size: " +  last_package_size)
    i = 1
    with open(filename, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            if(i <= number_of_packages and i != 0):
                bytes_read = connection.recv(BUFFER_SIZE)
            else:
                bytes_read = connection.recv(last_package_size)
                f.write(bytes_read)
                progress.update(len(bytes_read))
                # nothing is received
                # file transmitting is done
                print("downloaded the whole file! done!")
                downloading = False
                recv_file_mode = False
                f.close()
                break
            i+=1
            # write to the file the bytes we just received
            f.write(bytes_read)
            #print("dowloaded part of file! continue...")
            # update the progress bar
            progress.update(len(bytes_read))
   # connection.close()


#--- front ---
import PySimpleGUI as sg
sg.theme('DarkBlue14')

layout = [[sg.Text('Chat:')],
    [sg.Text('', key="chat")],
        [sg.InputText(do_not_clear=False)],
          [sg.Button('Ok')],
          [sg.Text('Send file:')],
          [sg.Text('File:', size=(8, 1)), sg.Input( key="file"), sg.FileBrowse('FileBrowse')],
          [sg.Button('Send file'), sg.Cancel()],
          [sg.Radio('ECB', "RADIO1", default=False, key="-ECB-")],
          [sg.Radio('CBC', "RADIO1", default=True, key="-CBC-")],
            [sg.Button('Change mode'), sg.Cancel()]]

layout_first_time_pass = [[sg.Text('Enter passsword:'), sg.InputText()],
[sg.Text('Enter again:'), sg.InputText()],
[sg.Text('', key='messagePassword')],
          [sg.Button('Ok')]]

layout_pass = [[sg.Text('Enter passsword:'), sg.InputText()],
          [sg.Button('Ok')]]

window = sg.Window('Client #2', layout)

#--- front ---

def client_start():
    global window
    global pass_hash
    global mode
    if DEV_ENV == False:
        if not(os.path.exists(private_path_to_file)) or not(os.path.exists(public_path_to_file )):
            print("first time opening the app - lets create a password")
            window_password_creation = sg.Window('Client#2', layout_first_time_pass)
            while True:
                event, values = window_password_creation.read()
                if event == 'Ok':
                    print("entered passw ", values[0], values[1])
                    if(values[0] == values[1]):
                        #create dirs
                        if not(os.path.exists(path_private)) or not(os.path.exists(path_public)):
                            os.makedirs(path_private)
                            os.makedirs(path_public)
                        #generate RSA keys
                        (pub, priv) = rsa.newkeys(key_len)
                        #hash of user password
                        pass_hash = keys.getHash(values[1].encode('UTF-8'))
                        #write keys to file
                        keys.writeRSAKey(pass_hash, private_path_to_file, priv)
                        keys.writeRSAKey(pass_hash, public_path_to_file, pub)

                        window_password_creation.close()
                        break
                    else:
                        window_password_creation['messagePassword'].update('\n passwords dont match')
        else:
            print("pass already set - type in password")   
            window_pass = sg.Window('Client#2', layout_pass)
            while True:
                event, values = window_pass.read()
                if event == sg.WIN_CLOSED or event == 'Cancel':
                    print("Closing the password creator window...")
                    break
                if event == 'Ok':
                    print("entered passw ", values[0])
                    pass_hash = keys.getHash(values[0].encode('UTF-8'))
                    try:
                        xd = keys.readRSAKey(pass_hash, private_path_to_file)
                        pass_right = True
                    except:
                        pass_right = False
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
        if event == 'Send file':
            send_file(client, values['FileBrowse'])
        if(values[0]):
            chat.update(chat.get()+'\n client#2: ' + values[0])
            send(client, values[0])
        if event == 'Change mode':
            if values['-CBC-'] == True:
                mode = 'cbc'
                print("changed mode to CBC.")
            else:             
                mode = 'ebc'
                print("changed mode to EBC.")

client_start()
os._exit(0)
