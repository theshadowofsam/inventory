"""
Samuel Lee
Controller.py
11/14/2022
"""
import json
import socket
import sys
import os

class WAREHOUSE:
    def __init__(self, name='', contents={}) -> None:
        self.name = name
        self.contents = contents


class JSON_HANDLER:
    REQUEST_CODES = [
        'CODE_QUERY',
        'CODE_PULL',
        'CODE_PUSH',
        'CODE_EMPTY',
        'CODE_REPLACE',
        'CODE_SET'
    ]

    FILENAME = 'WAREHOUSE.txt'

    def __init__(self) -> None:
        try:
            with open(self.FILENAME, 'r') as f:
                pass
        except FileNotFoundError as e:
            self._generate(self.FILENAME)
        self.warehouse = WAREHOUSE(self.load())
        print(self.warehouse)
        print(self.warehouse['name'], '\n', self.warehouse['content'])
        

    def _generate(self, fd):
        warehouse = {
            'name': 'warehouse',
            'contents': {}
        }

        with open(fd, 'w') as f:
            json.dump(warehouse, f, indent="\t",)


    def load(self):
        r = None
        with open(self.FILENAME, 'r') as f:
            r = json.load(f)
            print(r)
        return r['name'], r['contents']


if __name__ == '__main__':
    handler = JSON_HANDLER()