"""
Samuel Lee
Server.py
11/09/2022
"""
import socket
import multiprocessing
import json
import sys

class SERVER:
    def __init__(self):
        self.HOST = '127.0.0.1'
        self.PORT = 47468
        self.PROCESSES = []
        self.ACCEPTING = True
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.CLOSE = False
        self.COUNT = 0

    def run(self):
            self.SOCKET.bind((self.HOST, self.PORT))
            self.SOCKET.listen()
            self.SOCKET.settimeout(2)
            while True:
                conn = None
                addr = None
                if self.CLOSE:
                    break
                try:
                    conn, addr = self.SOCKET.accept()
                except:
                    continue
                if conn:
                    self.PROCESSES.append((multiprocessing.Process(target=self.handle_connection, args=[conn, addr]), self.COUNT))
                    self.PROCESSES[-1][0].run()
                    self.COUNT += 1

            self.SOCKET.close()
            print(f"count = {self.COUNT}")
            return 1

    def handle_connection(self, conn, addr):
        while True:
            data = conn.recv(4096)
            if data.decode() == 'CODE_END':
                print('end')
                break
            elif data.decode() == 'CODE_CLOSE':
                self.CLOSE = True
                print('close')
                break
            elif data.decode() == 'CODE_DATA':
                more_data = conn.recv(4096)
                print(json.loads(more_data.decode()))
            else:
                print("received something weird, stopping")
                break
        conn.close()
        return 1

if __name__ == "__main__":
    s = SERVER()
    s.run()
