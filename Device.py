import random
import socket
import time
from threading import Thread

import colorama
from termcolor import *
import datetime
import json
import sys

# Ogni device rappresenta 24 ore in 24 secondi.
# Ogni secondo vengono generati dei valori dal device, e ogni 24 secondi (che rappresentano 24 ore)
# vengono inviati al gateway

# Numero di campionature ogni 24 ore del device
NUMBER_OF_SAMPLES = 4


class Device(Thread):
    def __init__(self, device_ip_address, gateway_ip_address, gateway_port, frequency):
        # variable initialization
        self.device_ip_address = device_ip_address
        self.gateway_ip_address = gateway_ip_address
        self.gateway_port = gateway_port
        self.frequency = frequency
        self.data = []
        self.flag = True
        # Thread setting
        Thread.__init__(self)
        self.daemon = True
        colorama.init()
        # socket initialization
        self.UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_values(self, values):
        try:
            self.UDP_socket.sendto(values.encode(), (self.gateway_ip_address, int(self.gateway_port)))
        except Exception as exc:
            print(colored(f"Client error = {exc}", 'red'))

    # ritorna una stringa nel formato oggetto json -> { id_address = "", ... }
    def __generate_random_measurements(self):
        return {
            "device_ip_address": self.device_ip_address,
            "time_of_measurement": datetime.datetime.now().isoformat(),
            "temperature": random.randint(18, 36),
            "humidity": random.randint(0, 100)
        }

    def run(self):
        print(colored(f"Device {self.device_ip_address}  created \n ", "yellow"))
        while self.flag:
            # Esegue 4 misure in un giorno, la lunghezza del giorno è specificata da frequency nel costruttore
            for i in range(NUMBER_OF_SAMPLES):
                # aggiunge all'array di dizionari il valore di una lettura
                self.data.append(self.__generate_random_measurements())
                time.sleep(self.frequency / NUMBER_OF_SAMPLES)
            # Trasformazione dei dati in json per l'invio
            self.data.insert(0, str(datetime.datetime.now()))
            self.send_values(json.dumps(self.data))
            # Dopo l'invio dei dati vengono resettati
            self.data = []
            
    def stop(self):
        self.flag = False

if __name__ == "__main__":
    print("not executable as main")
