"""
Samuel Lee
Client.py
11/09/2022
"""
import socket
import json
import time

class JSON_DATA:
    def __init__(self) -> None:
        pass

class SOCK_CONN:
    def __init__(self) -> None:
        self.HOST = '127.0.0.1'
        self.PORT = 47468
        self.CODE_CLOSE = 'CODE_CLOSE'
        self.CODE_END = 'CODE_END'
            
    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            while True:
                t = input("Enter text to send: ")
                if t == self.CODE_END:
                    s.send(b'CODE_END')
                    break
                if t == self.CODE_CLOSE:
                    s.send(b'CODE_CLOSE')
                    break
                else:
                    s.send(t.encode())
            s.close()

if __name__ == "__main__":
    conn = SOCK_CONN()
    conn.run()