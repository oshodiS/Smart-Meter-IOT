import random
import socket
import time
from threading import Thread
from termcolor import colored
import datetime
import json


# Ogni device rappresenta 24 ore in 24 secondi.
# Ogni secondo vengono generati dei valori dal device, e ogni 24 secondi (che rappresentano 24 ore)
# vengono inviati al gateway


class Device(Thread):
    def __init__(self, device_ip_address, server_ip_address, server_port):
        self.device_ip_address = device_ip_address
        self.server_ip_address = server_ip_address
        self.server_port = server_port
        Thread.__init__(self)
        self.daemon = True
        self.send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.data = []
        print(colored(f"Device {server_ip_address}  creato", "yellow"))

    def send_values(self, values):
        try:
            self.send.sendto(values.encode(), (self.server_ip_address, int(self.server_port)))
            print(colored(f"CLIENT --> Messaggio Inviato =  {values}", 'green'))
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
        while True:
            # una misurazione per ora
            for i in range(24):
                # aggiunge all'array di dizionari il valore di una lettura
                self.data.append(self.__generate_random_measurements())


            json_data = json.dumps(self.data)
            self.send_values(json.dumps(self.data))
            # Dopo l'invio dei dati vengono resettati
            self.data = []
            time.sleep(10)


if __name__ == "__main__":
    client1 = Device("127.0.0.1", "127.0.0.1", 8080, 12)
