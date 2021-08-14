from socket import *
import json
from termcolor import colored
from threading import Thread, Lock
import threading


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
                json_collection = json.loads(message.decode())
                for json_obj in json_collection:
                    for json_row in json_obj:
                        str_message = json_row["device_ip_address"] + " -  " + str(json_row["time_of_measurement"]) \
                             + " -  " + str(json_row["temperature"]) + " -  " + str(json_row["humidity"])
                        print(colored(f"SERVER --> Messaggio ricevuto = {str_message} \n", 'blue'))
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

    def __append_data(self, data):
        f = open(self.file_name, "a")
        f.write(data + "\n")
        f.close()
