import threading
import socket

#STATIC
SIZE_OF_HEADER = 64
SERVER_IP = "0.0.0.0"
SERVER_PORT = 3000
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
CLIENT_DISCONNECT_MESSAGE = "/exit"
FORMAT_OF_MESSAGE_IN_SOCKET = "utf-8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM because the order of the data that is sent is important 
print("Client started...")
print("Trying to connect...")
client.connect(SERVER_ADDRESS)
print("Connected!")

def send(message):
    message = message.encode(FORMAT_OF_MESSAGE_IN_SOCKET)
    length_of_message = len(message) #check this one why do we store the length in string then int
    length_of_message = str(length_of_message).encode(FORMAT_OF_MESSAGE_IN_SOCKET)
    length_of_message += b' ' * (SIZE_OF_HEADER - len(length_of_message))#lets add the few bytes to make the size of header = 64, so if the 'length_of_message' is 24  we need to add 64-24=40bytes
    #this is because we make server read EXACTLY 64 bytes so now we must send EXACTLY 64 bytes
    client.send(length_of_message)
    print(f"Sending: {message}")
    client.send(message)
    print(f"Send!")



send("Hello world!")
