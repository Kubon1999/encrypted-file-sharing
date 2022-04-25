import threading
import socket

#STATIC
SIZE_OF_HEADER = 64
IP = "0.0.0.0"
PORT = 3000
ADDRESS = (IP, PORT)
#CLIENT_DISCONNECT_MESSAGE = "/exit"
FORMAT_OF_MESSAGE_IN_SOCKET = "utf-8" 

def client_connection(connection, address):
    print(f"{address} connection established")
    connected = True

    while connected:
        message_size = connection.recv(SIZE_OF_HEADER).decode(FORMAT_OF_MESSAGE_IN_SOCKET)
        if message_size:
            message_size = int(message_size)
            message = connection.recv(message_size).decode(FORMAT_OF_MESSAGE_IN_SOCKET)
            if message == CLIENT_DISCONNECT_MESSAGE:
                connected = False

            print(f"[{address}] {message}")
        
    connection.close()


def base_client_start():
    print("Starting the base client...")
    client_running = True

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM because the order of the data that is sent is important 
    client.bind(ADDRESS)

    client.listen()
    print("Client running...")
  #  while client_running:
    connection, address = client.accept()
        #client_thread = threading.Thread(target=client_connection, args=(connection, address)) #args method
    client_connection(connection,address)
        #client_thread.start()
        #print(f"Clients connected: {threading.active_count() - 1}") #-1 becausue one thread is our sever thread 


        


base_client_start()
