"""
Samuel Lee
Server.py
11/09/2022
"""
import socket
import multiprocessing
import json

class SERVER:
    def __init__(self):
        self.HOST = '127.0.0.1'
        self.PORT = 47468
        self.PROCESSES = []
        self.COUNT = 0
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.CLOSE = False

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
                    p = multiprocessing.Process(target=self.handle_connection, args=[conn, addr])
                    p.run()
                    self.COUNT += 1
            self.SOCKET.close()
            print(f"count = {self.COUNT}")
            return 1

    def handle_connection(self, conn, addr):
        while True:
            data = conn.recv(4096)
            print(data.decode('utf-8'))
            if data.decode('utf-8').endswith('CODE_END'):
                print('end')
                break
            if data.decode('utf-8').endswith('CODE_CLOSE'):
                self.CLOSE = True
                print('close')
                break
        conn.close()
        return 1

if __name__ == "__main__":
    s = SERVER()
    s.run()
