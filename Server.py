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
        self.CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.CONTROLLER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.processes = {}
        self.request_queue = Queue(maxsize=500)
        self.controller_queue = Queue(maxsize=500)

    def run(self):
            self.CLIENT_SOCKET.bind((self.HOST, self.PORT))
            self.CLIENT_SOCKET.listen()
            self.CLIENT_SOCKET.settimeout(0)
            while True:
                try:
                    self.CONTROLLER_SOCKET.connect(self.HOST)
                except:
                    print('Attempting connection to controller...')
                    continue
                else:
                    break
            while True:
                connection = None
                address = None
                try:
                    connection, address = self.CLIENT_SOCKET.accept()
                    self.processes[address] = (Process(target=self.handle_connection, args=(connection, address)), Queue(maxsize=10))
                except TimeoutError as e:
                    pass
                try:
                    request = self.request_queue.get_nowait()
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
                print(json.loads(more_data.decode()))
            else:
                print("received something weird, stopping")
                break
        conn.close()
        return 1

    def cleanup_client_connection(self, address):
        if address in self.processes.keys():
            self.processes.pop(address)
        else:
            raise KeyError

if __name__ == "__main__":
    s = SERVER()
    s.run()
