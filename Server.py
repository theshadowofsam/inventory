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
        self.client_processes = {}
        self.controller_process = None
        self.client_request_queue = Queue(maxsize=500)
        self.controller_send_queue = Queue(maxsize=500)
        self.controller_recieve_queue = Queue(maxsize=500)

    def run(self):
        self.prepare_client_socket()
        self.connect_controller()
        self.controller_process = self.spawn_controller_process(self.CONTROLLER_SOCKET)
        self.controller_process.run()
        
        while True:
            connection = None
            address = None
            request = None
            try:
                connection, address = self.CLIENT_SOCKET.accept()
                connection.settimeout(None)
                self.client_processes[address] = (Process(target=self.handle_connection, args=(connection, address)), Queue(maxsize=10))
            except TimeoutError as e:
                pass
            try:
                request = self.client_request_queue.get_nowait()

            except Empty as e:
                print(type(e), f': {e}')

        self.CLIENT_SOCKET.close()
        print(f"count = {self.COUNT}")
        return 1

    def handle_connection(self, conn, addr):
        while True:
            data = conn.recv(1024)
            if data.decode() == 'CODE_END':
                print('end')
                break
            elif data.decode() == 'CODE_CLOSE':
                self.CLOSE = True
                print('close')
                break
            elif data.decode() in self.REQUEST_CODES:
                code = data.decode()
                conn.send(b'GO')
                more_data = conn.recv(1024)
                print(more_data.decode())
            else:
                conn.send(b'BAD_CODE')
                print("received something weird, retrying.")
                continue
        conn.close()
        return 1

    def spawn_controller_process(self, controller_socket):
        return Process(target=self.handle_controller, args=(controller_socket,))

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
        self.CLIENT_SOCKET.settimeout(0)
        self.CLIENT_SOCKET.listen()

    def connect_controller(self):
        while True:
            try:
                self.CONTROLLER_SOCKET.connect(self.HOST)
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
