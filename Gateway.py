import json

import colorama

from Device import Device
from socket import *
import time
from termcolor import *
from threading import Thread, Lock
from datetime import datetime

lock = Lock()
BUFFER_SIZE=4096


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
        colorama.init()

    def send_to_server(self, message_to_send):
        # il gateway invia il messaggio al Cloud in TCP
        try:
            self.TCP_socket.send(message_to_send)
        except Exception as exc:
            print(colored(f"Server exception {exc}", 'red'))

    def __print_time_to_receve_UDP(self, loaded_json):
        total_millisec = datetime.now() - datetime.strptime(loaded_json[0], "%Y-%m-%d %H:%M:%S.%f")
        print(colored(
            "\n La trasmissione UDP ha richiesto " + str(total_millisec.total_seconds() * 1000) + "  millisecondi " ,
            "yellow"))

    def run(self):
        print(colored("Gateway started", "yellow"))
        self.TCP_socket.connect(("localhost", self.server_TCP_port))
        # conta quanti device hanno inviato i dati
        device_count = 0
        # contiene tutti i messaggi dei device, quando tutti i device hanno inviato vengono girati al server
        messages = []
        while True:
            try:

                while device_count < self.number_of_devices:
                    # Attende il file dai device
                    message, addr = self.UDP_socket.recvfrom(4096)
                    loaded_json = json.loads(message.decode())
                    # Stampa il tempo di trasmissione effettuando la differanza tra i timestamp
                    self.__print_time_to_receve_UDP(json.loads(message.decode()))
                    # Rimuove i time stamp delle trasmissioni in UDP e crea una unica struttura dati
                    # con tutte le misurazioni dei device
                    for i in range(1, len(loaded_json)):
                        messages.append(loaded_json[i])

                    device_count += 1
                # Manda il messaggio in TCP al server

                messages.insert(0, str(datetime.now()))

                self.send_to_server(json.dumps(messages).encode())

                # reset delle variabili per attendere nuove trasmissioni in UDP
                device_count = 0
                messages = []
            except Exception as exc:
                print(colored(f"Gateway exception {exc}", 'red'))
    def get_buffer_size(self):
      return BUFFER_SIZE