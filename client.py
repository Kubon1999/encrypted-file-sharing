import sys
import threading
import socket

randesvous_server = ('0.0.0.0', 3000)

print('connecting to the randesvous server')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind('0.0.0.0', 50001)
sock.sendto(b'0', randesvous_server)

while True:
    data = sock.recv(1024).decode()

    if data.strip() == 'ready':
        print('checked with server, waiting')
        break

data = sock.recv(1024).decode()
ip, sport, dport = data.split(' ')
sport = int(sport)
dport = int(dport)

print('\n got peer')
print('ip: ', format(ip))
print(' source port: ', format(sport))
print(' dest port: ', format(dport))

