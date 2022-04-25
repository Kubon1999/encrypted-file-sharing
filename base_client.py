import threading
import socket

#STATIC
SIZE_OF_HEADER = 64
IP = "0.0.0.0"
PORT = 3000
ADDRESS = (IP, PORT)
FORMAT_OF_MESSAGE_IN_SOCKET = "utf-8" 
CLIENT_DISCONNECT_MESSAGE = "/exit"

def client_connection(connection, address):
    print(f"{address} connection established")
    connected = True

    while connected:
        message_size = connection.recv(SIZE_OF_HEADER).decode(FORMAT_OF_MESSAGE_IN_SOCKET)
        if message_size:
            message_size = int(message_size)
            message = connection.recv(message_size).decode(FORMAT_OF_MESSAGE_IN_SOCKET)
            if message == CLIENT_DISCONNECT_MESSAGE:
                print("Client disconnnected.")
                connected = False

            print(f"[{address}] {message}")
        
    connection.close()

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


def base_client_start():
    print("Starting the base client...")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM because the order of the data that is sent is important 
    client.bind(ADDRESS)

    client.listen()
    print("Base client running...")
    connection, address = client.accept()
    connection_thread = threading.Thread(target=client_connection, args=(connection,"client"))
    connection_thread.start()
    #while recieving thread is up lets send messages
    while True:
        message = input()
        send(connection, message)

base_client_start()
