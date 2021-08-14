import sys
from socket import *
import json
import time

from termcolor import colored

from threading import Thread

import timer
from future.backports.datetime import time
server = socket(AF_INET, SOCK_STREAM)
class Server:
    def server_iniz(self):
        #inizializzazione
        print("sever avviato..")

        SERVER_IP = "192.168.1.234"
        SERVER_PORT=49153
        server.bind(("localhost",SERVER_PORT))
        server.listen(2)

    def start_listen(self):
        while True:
            print("sever in ascolto..")
            try:
                connectionSocket, addr = server.accept()
             
                message=connectionSocket.recv(4096)
                print(message.decode())
                json_obj = json.loads(message.decode())
                print(colored("SERVER --> Messaggio ricevuto = " + json_obj[0]["device_ip_address"] +
                              " -  " + str(json_obj[0]["time_of_measurement"]) +
                              " -  " + str(json_obj[0]["temperature"])
                              + " -  " + str(json_obj[0]["humidity"]), 'blue'))
            except IOError as errore:
                print(f"sever error..{errore}")
    def read_file(jFile):
        f= open(jFile,)
        data = json.load(f)
        for i in data['temperature']:
            print(i) #cambiare in base a come è il json

srv=Server()
srv.server_iniz()
srv.start_listen()
server.close()
