import socket
from Device import Device
import time
from termcolor import colored

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 8080))
    dev = Device("127.0.0.1", "127.0.0.1", 8080)
    dev.start()
    while True:
        time.sleep(0.5)
        try:
            message, addr = s.recvfrom(1024)
            print(colored("SERVER --> Messaggio ricevuto = " + message.decode(), 'blue'))
        except Exception as exc:
            print(colored(f"Server exception {exc}", 'red'))
