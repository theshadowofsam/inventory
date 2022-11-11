"""
Samuel Lee
Client.py
11/09/2022
"""
from ctypes import sizeof
import socket
import json
import sys
from typing import Dict

# self.DATA is a Dict of all data that will be sent to server
# self.TYPE only defaults to 'CODE_DATA' for the moment,
#  but will be used for CODE_STOP and CODE_END and any others
class JSON_DATA:
    CODES = [
        'CODE_DATA',
        'CODE_STOP',
        'CODE_END'
    ]

    def __init__(self, CODE='CODE_DATA', DATA={}):
        if CODE not in self.CODES:
            return f'{CODE} is a bad CODE, must be a string in {self.CODES}'
        if type(DATA) != type({}):
            return f'{type(DATA)} is not of type {type({})}'
        try:
            self.CODE = CODE
            self.DATA = DATA
            self.SIZE = sys.getsizeof(self.DATA)
        except Exception as e:
            return e
        return True

    def bundle(self):
        return json.dumps(self.TYPE, self.SIZE, self.DATA)

    def bundle_new(self, TYPE, DATA):
        SIZE = sys.getsizeof(DATA)
        data = json.dumps(TYPE, SIZE, DATA)
        return data

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