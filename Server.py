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
        'CODE_SET',
        'CODE_REPLACE'
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
        self.controller_receive_queue = Queue(maxsize=500)

    def run(self):
        self.prepare_client_socket()
        # self.prepare_controller_socket()
        # self.controller_process = self.spawn_controller_process(self.CONTROLLER_SOCKET)
        # self.controller_process.run()
        
        while True:
            connection = None
            address = None
            request = None
            try:
                connection, address = self.CLIENT_SOCKET.accept()
                connection.settimeout(None)
                self.client_processes[address] = (Process(target=self.handle_client_connection, args=(connection, address)), Queue(maxsize=10))
                self.client_processes[address][0].start()
            except Exception as e:
                pass
            
            try:
                request = self.client_request_queue.get_nowait()
                match request[0]:
                    case 'CODE_STOP':
                        print('got CODE_STOP. Shutting down...')
                        break
                    case 'CODE_END':
                        print(f'{request[1]} ended their connection.')
                    case 'CODE_QUERY':
                        print(f'{request[1]} want to know what is in a slot')
                    case 'CODE_PULL':
                        print(f'{request[1]} wants to pull from a slot.')
                    case 'CODE_PUSH':
                        print(f'{request[1]} wants to put items in a slot.')
                    case 'CODE_EMPTY':
                        print(f'{request[1]} wants to empty a slot.')
                    case 'CODE_SET':
                        print(f'{request[1]} wants to set the data for a slot.')
                    case 'CODE_REPLACE':
                        print(f'{request[1]} wants to replace a slot.')
                    case 'CLEANUP':
                        print(f'Cleaning up {request[1]}')
                        self.cleanup_client_connection(request[1])
                    case _:
                        print(f'got something else from {request[1]}: {request[0]}')
            except Empty:
                pass

        self.CLIENT_SOCKET.close()
        self.CONTROLLER_SOCKET.close()
        return 1

    def handle_client_connection(self, conn, addr): #TODO needs a rework
        while True:
            data = conn.recv(1024).decode()
            if data in self.REQUEST_CODES:
                response = f'Got request {data} from {addr}'
                conn.send(response.encode())
                self.client_request_queue.put([data, addr])
            else:
                response = f'Got something weird: {data} from {addr}'
                conn.send(response.encode())
            if data == 'CODE_STOP' or data == 'CODE_END':
                break
        conn.close()
        self.client_request_queue.put(['CLEANUP', addr])
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
                receive = self.controller_receive_queue.get_nowait()
            except Empty:
                pass

    def prepare_client_socket(self):
        self.CLIENT_SOCKET.bind((self.HOST, self.PORT))
        self.CLIENT_SOCKET.settimeout(0)
        self.CLIENT_SOCKET.listen()

    def prepare_controller_socket(self):
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
