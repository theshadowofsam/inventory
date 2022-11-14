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

    WAREHOUSE = 'WAREHOUSE.txt'

    def __init__(self) -> None:
        try:
            with open(self.WAREHOUSE, 'r') as f:
                pass
        except FileNotFoundError as e:
            self._generate()

    def _generate(self, filename=None):
        pass

    def load(self):
        r = None
        with open(self.WAREHOUSE, 'r') as f:
            r = json.load(f)
        return r

if __name__ == '__main__':
    handler = JSON_HANDLER()