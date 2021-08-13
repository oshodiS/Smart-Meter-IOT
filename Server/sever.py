import sys
from socket import *
import json
import time

from termcolor import colored

import Device
from threading import Thread

import timer
from future.backports.datetime import time
server = socket(AF_INET, SOCK_STREAM)
class Server:
    def server_iniz(self):
        #inizializzazione
        print("sever avviato..")

        SERVER_IP = "192.168.1.234"
        SERVER_PORT=8080
        server.bind(("localhost",SERVER_PORT))
        server.listen(2)

    def start_listen(self):
        while True:
            print("sever in ascolto..")
            try:
                connectionSocket, addr = server.accept()
                print("sever in ascolto..")
                message=connectionSocket.recv(1024)
                print(colored("SERVER --> Messaggio ricevuto = " + message.decode(), 'blue'))
            except IOError:
                print("sever error..")
    def read_file(jFile):
        f= open(jFile,)
        data = json.load(f)
        for i in data['temperature']:
            print(i) #cambiare in base a come è il json

print("costruttore!")
srv=Server()
srv.server_iniz()
srv.start_listen()
server.close()
