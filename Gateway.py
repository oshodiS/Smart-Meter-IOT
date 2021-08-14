import json
from Device import Device
from socket import *
import time
from termcolor import colored
from threading import Thread


class Gateway(Thread):
    def __init__(self, internal_ip, UDP_port, external_ip, TCP_port):
        # inizializzazione socket UDP
        self.UDP_socket = socket(AF_INET, SOCK_DGRAM)
        self.UDP_socket.bind(('', UDP_port))
        self.internal_ip = internal_ip

        # inizializzazione socket TCP
        self.TCP_socket = socket(AF_INET, SOCK_STREAM)
        self.external_TCP_port = TCP_port
        self.external_ip = external_ip

    def send_to_server(self, message_to_send):
        # il gateway invia il messaggio al Cloud in TCP
        self.TCP_socket.connect(("localhost", self.external_TCP_port))
        try:
            self.TCP_socket.send(message_to_send)
        except Exception as exc:
            print(colored(f"Server exception {exc}", 'red'))
        self.TCP_socket.close()

    def run(self):
        while True:
            try:
                # Attende il file dai device
                message, addr = self.UDP_socket.recvfrom(4096)
                # Manda il messaggio in TCP al server
                self.send_to_server(message)

            except Exception as exc:
                print(colored(f"Gateway exception {exc}", 'red'))
