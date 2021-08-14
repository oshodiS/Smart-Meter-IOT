import json
from Device import Device
from socket import *
import time
from termcolor import colored
from threading import Thread


class Gateway(Thread):
    def __init__(self, internal_ip, UDP_port, external_ip, server_TCP_port, number_of_devices):
        # inizializzazione varibili
        self.number_of_devices = number_of_devices

        # inizializzazione socket UDP
        self.UDP_socket = socket(AF_INET, SOCK_DGRAM)
        self.UDP_socket.bind(('localhost', UDP_port))
        self.internal_ip = internal_ip

        # inizializzazione socket TCP
        self.TCP_socket = socket(AF_INET, SOCK_STREAM)
        self.server_TCP_port = server_TCP_port
        self.external_ip = external_ip

        # Inizializzazione thread
        Thread.__init__(self)
        self.daemon = True

    def send_to_server(self, message_to_send):
        # il gateway invia il messaggio al Cloud in TCP
        try:
            self.TCP_socket.send(message_to_send)
        except Exception as exc:
            print(colored(f"Server exception {exc}", 'red'))

    def run(self):
        print(colored("Gateway started", "yellow"))
        self.TCP_socket.connect(("localhost", self.server_TCP_port))
        # conta quanti device hanno inviato i dati
        device_count = 0
        # contiene tutti i messaggi dei device, quando tutti i device hanno inviato vengono girati al server
        messages = []
        while True:
            try:
                # Attende il file dai device
                while device_count < self.number_of_devices:
                    message, addr = self.UDP_socket.recvfrom(4096)
                    messages.append(json.loads(message))
                    device_count += 1
                # Manda il messaggio in TCP al server
                self.send_to_server(json.dumps(messages).encode())

                device_count = 0
                messages = []
            except Exception as exc:
                print(colored(f"Gateway exception {exc}", 'red'))
