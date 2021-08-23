from os import system, name

import colorama

from Device import Device
from Server import Server
from Gateway import Gateway
from termcolor import *
import signal
import sys
import time


def print_heading():
    print("Traccia 1 - Progetto IoT \n "
          "Shola Oshodi - Daniel Guariglia \n\n")

def close_thread_on_exit(signal, frame):
    print("Exit...")
    device_1.stop()
    device_2.stop()
    device_3.stop()
    device_4.stop()
    gateway.stop()
    server.stop()
    sys.exit(0)


if __name__ == "__main__":
    colorama.init()
    print_heading()
    signal.signal(signal.SIGINT, close_thread_on_exit)
    signal.signal(signal.SIGTERM, close_thread_on_exit)
    frequency = 0

    while True:
        try:
            while frequency <= 0:
                frequency = int(input("In quanti secondi si vogliono simulare 24 ore : "))
                if frequency <= 0:
                    raise ValueError()
            break
        except ValueError:
            print("Valore inserito non valito. Atteso un valore <= 1")
    #creazione dei dispositivi
    #assegnazione degli indirizzi IP
    gateway = Gateway("192.168.0.1", 8080, "10.10.10.1", 8081, 4)
    server = Server("10.10.10.2", 8081)
    device_1 = Device("192.168.0.10", "localhost", 8080, frequency)
    device_2 = Device("192.168.0.11", "localhost", 8080, frequency)
    device_3 = Device("192.168.0.12", "localhost", 8080, frequency)
    device_4 = Device("192.168.0.13", "localhost", 8080, frequency)

    #inizializzazione dispositivi
    server.start()
    gateway.start()
    device_1.start()
    device_2.start()
    device_3.start()
    device_4.start()
    print(colored("Server buffer size "+str(server.get_buffer_size()),"green"))
    print(colored("Gateway buffer size "+str(gateway.get_buffer_size()),"green"))
    i = input()
