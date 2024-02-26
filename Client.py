"""
Samuel Lee
Client.py
11/09/2022
"""
import socket
import json
import sys


class JSON_DATA:
    
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
                print(t)
                match t:
                    case 'CODE_STOP':
                        s.send(t.encode())
                        response = s.recv(4096).decode()
                        if response == 'CODE_STOP':
                            print('Stopping and closing')
                            break
                    case 'CODE_END':
                        s.send(t.encode())
                        response = s.recv(4096).decode()
                        if response == 'CODE_END':
                            print('closing')
                            break
                    case 'CODE_QUERY':
                        print("Querying...")
                        s.send(t.encode())
                        response = s.recv(4096).decode()
                    case 'CODE_PULL':
                        s.send(t.encode())
                        response = s.recv(4096).decode()
                    case 'CODE_PUSH':
                        s.send(t.encode())
                        response = s.recv(4096).decode()
                    case 'CODE_EMPTY':
                        s.send(t.encode())
                        response = s.recv(4096).decode()
                    case 'CODE_SET':
                        s.send(t.encode())
                        response = s.recv(4096).decode()
                    case 'CODE_REPLACE':
                        s.send(t.encode())
                        response = s.recv(4096).decode()
                    case _:
                        print('Bad Sendable')
                print('r= ' + response)
            s.close()

    def user_handler(self) -> str:
        print('What would you like to do?')
        for i, code in enumerate(JSON_DATA.CODE_ORDER):
            print(f'{i}. {JSON_DATA.CODES[code]}')
        while True:
            rt = int(input('Enter the number for your request type: '))
            if rt >= 0 and rt < len(JSON_DATA.CODE_ORDER):
                break
            print('Bad input. Please select a valid option.')
        code = JSON_DATA.CODE_ORDER[rt]
        return code


if __name__ == "__main__":
    conn = SOCK_CONN()
    conn.run()