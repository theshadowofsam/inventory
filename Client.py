"""
Samuel Lee
Client.py
11/09/2022
"""
import socket
import json
import sys


class REQUEST_CODES:
    CODES = {
        'CODE_STOP':    'Close the server when all current requests are completed.', 
        'CODE_END':     'Close your client.',
        'CODE_QUERY':   'Query a slot in the warehouse.',
        'CODE_PULL':    'Pull items from an item slot.',
        'CODE_PUSH':    'Add items to an item slot',
        'CODE_EMPTY':   'Clear an item slot of all data.',
        'CODE_REPLACE': 'Replace an item slots data. Same as Empty + Set.',
        'CODE_SET':     'Set a currently empty item slots data.'
    }
    CODE_ORDER = [
        'CODE_STOP', 
        'CODE_END',
        'CODE_QUERY',
        'CODE_PULL',
        'CODE_PUSH',
        'CODE_EMPTY',
        'CODE_SET',
        'CODE_REPLACE'        
    ]

    #!!! Hopefully i can get rid of all of this crap
    # def __init__(self, CODE='CODE_DATA', DATA={}) -> None:
    #     if CODE not in self.CODES:
    #         raise ValueError(f'{CODE} is a bad CODE, must be a string in {self.CODES}')
    #     if type(DATA) != type({}):
    #         raise TypeError(f'DATA type:{type(DATA)} is of incorrect type, should be Dict')    
    #     self.CODE = CODE
    #     self.DATA = DATA # a Dict of all data that will be sent to server
    #     self.SIZE = sys.getsizeof(DATA)

    # def bundle(self):
    #     return json.dumps([self.CODE, self.SIZE, self.DATA])

    # def bundle_new(self, CODE, DATA):
    #     SIZE = sys.getsizeof(DATA)
    #     return json.dumps(CODE, SIZE, DATA)

    # def size(self):
    #     self.SIZE = sys.getsizeof(self.DATA)
    #     return self.SIZE

class SOCK_CONN:
    def __init__(self) -> None:
        self.HOST = '127.0.0.1'
        self.PORT = 47468
        self.CODE_STOP = 'CODE_STOP'
        self.CODE_END = 'CODE_END'
            
    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            while True:
                t = self.user_handler()
                match t:
                    case 'CODE_STOP':
                        s.send(t.encode())
                        response = s.recv(4096)
                        print(response)
                        break
                    case 'CODE_END':
                        s.send(t.encode())
                        response = s.recv(4096)
                        print(response)
                        break
                    case 'CODE_QUERY':
                        s.send(t.encode())
                        response = s.recv(4096)
                        print(response)
                    case 'CODE_PULL':
                        s.send(t.encode())
                        response = s.recv(4096)
                        print(response)
                    case 'CODE_PUSH':
                        s.send(t.encode())
                        response = s.recv(4096)
                        print(response)
                    case 'CODE_EMPTY':
                        s.send(t.encode())
                        response = s.recv(4096)
                        print(response)
                    case 'CODE_SET':
                        s.send(t.encode())
                        response = s.recv(4096)
                        print(response)
                    case 'CODE_REPLACE':
                        s.send(t.encode())
                        response = s.recv(4096)
                        print(response)
                    case _:
                        print('Bad Sendable')
                print(response)
            s.close()
    
    def user_handler(self) -> str:
        print('What would you like to do?')
        for i, code in enumerate(REQUEST_CODES.CODE_ORDER):
            print(f'{i}. {REQUEST_CODES.CODES[code]}')
        while True:
            rt = int(input('Enter the number for your request type: '))
            if rt >= 0 and rt < len(REQUEST_CODES.CODE_ORDER):
                break
            print('Bad input. Please select a valid option.')
        code = REQUEST_CODES.CODE_ORDER[rt]
        return code

if __name__ == "__main__":
    conn = SOCK_CONN()
    conn.run()