from socket import *
import json
from termcolor import colored
from threading import Thread, Lock
import threading
import numpy as np
from datetime import datetime

class Server(Thread):
    def __init__(self, server_ip, server_port):
        # socket initialization
        self.TCP_socket = socket(AF_INET, SOCK_STREAM)
        self.TCP_socket.bind(("localhost", server_port))
        self.TCP_socket.listen(5)
        # variable initialization
        self.server_ip = server_ip
        self.server_port = server_port
        self.file_name = "storico_misurazioni.txt"
        # Thread setting
        Thread.__init__(self)
        self.daemon = True


    def on_new_client(self, connection_socket, addr):

        try:
            while True:
                message = connection_socket.recv(16384)
                if not message:
                    break
                #crea un file jason con le misurazioni
                json_collection = json.loads(message.decode())
                self.__print_time_to_receve_TCP(json_collection)
                #stampa i dati delle misurazioni memorizzati nel file json
                for i in range(1, (len(json_collection)-1)):
                    str_message = json_collection[i]["device_ip_address"] + " -  " + str(json_collection[i]["time_of_measurement"]) \
                                  + " -  " + str(json_collection[i]["temperature"]) + " -  " + str(json_collection[i]["humidity"])
                    print(colored(f"SERVER --> Messaggio ricevuto = {str_message} \n", 'blue'))
                  #salvo la misurazione sul file
                    self.__append_data(str_message)
            connection_socket.close()
        except IOError as errore:
            print(f"Sever error: {errore}")

    def run(self):
        print(colored(f"Sever {self.server_ip} listening ...", "yellow"))
        thread_esistenti = 0
        while True:
            connection_socket, addr = self.TCP_socket.accept()
            # self.on_new_client(connection_socket, addr)
            threading.Thread(target=self.on_new_client, args=(connection_socket, addr)).start()
        self.TCP_socket.close()


#aggiunge a un file le misurazioni fatte per creare uno storico dei dati
    def __append_data(self, data):
        f = open(self.file_name, "a")
        f.write(data + "\n")
        f.close()
#stampa del tempo necessario a trasmettere in TCP
    def __print_time_to_receve_TCP(self, loaded_json):
        total_millisec = datetime.now() - datetime.strptime(loaded_json[0], "%Y-%m-%d %H:%M:%S.%f")
        print(colored(
            "\n La trasmissione TCP ha richiesto " + str(total_millisec.total_seconds() * 1000) + "  millisecondi " ,
            "yellow"))