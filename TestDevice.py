import json
from Device import Device
from socket import *

import time
from termcolor import colored

def send_to_server(message_to_send):
    #il gateway invia il messaggio al Cloud in TCP
    socket_gateway = socket(AF_INET, SOCK_STREAM)
    socket_gateway.connect(("localhost",49153))
    while True:
        try:
            socket_gateway.send(message_to_send.encode())
        except Exception as exc:
         print(colored(f"Server exception {exc}", 'red'))

if __name__ == '__main__':
    UDP_socket = socket(AF_INET, SOCK_DGRAM)
    UDP_socket.bind(('', 8080))
    #ISTANZIA IL TUO SOCKET TCP
    dev = Device("127.0.0.1", "127.0.0.1", 8080)
    dev.start()

    while True:
        try:
            message, addr = UDP_socket.recvfrom(4096)
            #MANDATI IL MESSAGE IN TCP
            print(message.decode())
            send_to_server(message)

        except Exception as exc:
            print(colored(f"Gateway exception {exc}", 'red'))

