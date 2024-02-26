"""
Samuel Lee
Server.py
11/09/2022
"""
import socket
from multiprocessing import Process, Queue
from queue import Empty
import json
import sys


class SERVER:
    
    REQUEST_CODES = [
        'CODE_STOP',
        'CODE_END',
        'CODE_QUERY',
        'CODE_PULL',
        'CODE_PUSH',
        'CODE_EMPTY',
        'CODE_REPLACE',
        'CODE_SET'
    ]
    
    def __init__(self):
        self.HOST = '127.0.0.1'
        self.PORT = 47468
        self.CONTROLLER_PORT = 47469
        self.CONTROLLER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.STOP = False
        self.client_processes = {}
        self.controller_process = None
        self.client_request_queue = Queue(maxsize=500)
        self.controller_send_queue = Queue(maxsize=500)
        self.controller_recieve_queue = Queue(maxsize=500)

    def run(self):
        self.prepare_client_socket()
        self.connect_controller()
        self.controller_process = self.spawn_controller_process(self.CONTROLLER_SOCKET)
        # self.controller_process.run()
        print("TEST")
        while True:
            connection = None
            address = None
            request = None
            try:
                connection, address = self.CLIENT_SOCKET.accept()
                connection.settimeout(None)
                self.client_processes[address] = (Process(target=self.handle_client, args=(connection, address)).start(), Queue(maxsize=10))
            except TimeoutError as e:
                pass
            try:
                request = self.client_request_queue.get_nowait()
            except Empty as e:
                print(type(e), f': {e}')

        self.CLIENT_SOCKET.close()
        print(f"count = {self.COUNT}")
        return 1

    def handle_client(self, conn, addr): #TODO Send client requests to controller and handle the controller response
        while True:
            data = conn.recv(4096).decode()
            print(data)
            if data in self.REQUEST_CODES:
                print(data)
                response = f'Got request {data} from {addr}'
                conn.send(response.encode())
                break
            else:
                response = f'Got something weird: {data} from {addr}'
                conn.send(response.encode())
                break
        return 1

    def spawn_controller_process(self, controller_socket):
        return Process(target=self.handle_controller, args=(controller_socket,)).start()

    def handle_controller(self, connection):
        while True:
            send = None
            receive = None
            try:
                send = self.controller_send_queue.get_nowait()
            except Empty:
                pass
            try:
                receive = self.controller_recieve_queue.get_nowait()
            except Empty:
                pass

    def prepare_client_socket(self):
        self.CLIENT_SOCKET.bind((self.HOST, self.PORT))
        self.CLIENT_SOCKET.settimeout(5)
        self.CLIENT_SOCKET.listen()

    def connect_controller(self):
        while True:
            try:
                self.CONTROLLER_SOCKET.connect((self.HOST, self.CONTROLLER_PORT))
            except:
                print('Attempting connection to controller...')
                continue
            else:
                print('Controller Connected...')
                return 1


    def cleanup_client_connection(self, address):
        if address in self.client_processes.keys():
            self.client_processes.pop(address)
        else:
            raise KeyError


if __name__ == "__main__":
    s = SERVER()
    s.run()
