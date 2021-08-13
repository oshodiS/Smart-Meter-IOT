import socket
from Device import Device
import time
from termcolor import colored

if __name__ == '__main__':
    UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDP_socket.bind(('', 8080))
    #ISTANZIA IL TUO SOCKET TCP
    dev = Device("127.0.0.1", "127.0.0.1", 8080)
    dev.start()
    while True:
        try:
            message, addr = UDP_socket.recvfrom(4096)
            #MANDATI IL MESSAGE IN TCP
            print(colored("SERVER --> Messaggio ricevuto = " + message.decode(), 'blue'))
        except Exception as exc:
            print(colored(f"Server exception {exc}", 'red'))
