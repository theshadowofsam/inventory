"""
Samuel Lee
Client.py
11/09/2022
"""
import socket
import json
import time

HOST = '127.0.0.1'
PORT = 47468
CODE_CLOSE = 'CODE_CLOSE'
CODE_END = 'CODE_END'

class JSON_DATA:
    def __init__(self) -> None:
        pass

class SOCK_CONN:
    def __init__(self) -> None:
        pass
            
    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            while True:
                t = input("Enter text to send: ")
                if t == CODE_END:
                    s.send(b'CODE_END')
                    break
                if t == CODE_CLOSE:
                    s.send(b'CODE_CLOSE')
                    break
                else:
                    s.send(t.encode())
            s.close()

if __name__ == "__main__":
    pass