"""
Samuel Lee
Controller.py
11/14/2022
"""
import json
import socket
import sys
import os

# warehouse of aisles of rows of slots of items
class WAREHOUSE:
    class _AISLE:
        def __init__(self, name='', contents=[]) -> None:
            self.name = name
            self.contents = contents

    class _ROW:
        def __init__(self, name='', contents=[]) -> None:
            self.name = name
            self.contents = contents

    class _SLOT:
        def __init__(self, name='', item=None) -> None:
            self.name = name
            self.item = item

    class _ITEM:
        def __init__(self, name='', amount=0) -> None:
            self.name = name
            self.amount = amount

    def __init__(self, name='', contents=[]) -> None:
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
        name, contents = self.load()
        self.warehouse = WAREHOUSE(name, contents)
        print(self.warehouse)
        print(self.warehouse.name, '\n', self.warehouse.contents)
        

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