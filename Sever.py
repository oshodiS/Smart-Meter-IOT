from socket import *
import json
from termcolor import colored
from threading import Thread


class Server(Thread):
    def __init__(self, server_ip, server_port):
        # socket initialization
        self.TCP_socket = socket(AF_INET, SOCK_STREAM)
        self.TCP_socket.bind(("localhost", server_port))
        self.TCP_socket.listen(2)
        # variable initialization
        self.server_ip = server_ip
        self.server_port = server_port
        self.file_name = "storico_misurazioni.txt"
        # Thread setting
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        print(f"Sever {self.server_ip} listening ...")
        while True:
            try:
                connection_socket, addr = self.TCP_socket.accept()
                message = connection_socket.recv(4096)
                print(message.decode())
                json_obj = json.loads(message.decode())
                str_message = json_obj[0]["device_ip_address"] + " -  " + str(json_obj[0]["time_of_measurement"]) \
                              + " -  " + str(json_obj[0]["temperature"]) + " -  " + str(json_obj[0]["humidity"])
                print(colored("SERVER --> Messaggio ricevuto = " + str_message, 'blue'))
                self.__append_data(str_message)
            except IOError as errore:
                print(f"sever error..{errore}")

    def __append_data(self, data):
        f = open(self.file_name, "a")
        f.write(data + "\n")
        f.close()
