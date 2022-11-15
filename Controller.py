"""
Samuel Lee
Controller.py
11/14/2022
"""
import json
import socket
import sys
import os

# warehouse of aisles of rows of slots of item
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
    YN = ['y', 'n']

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
        
    #prompts user for warehouse information and creates warehouse object
    def _generate(self, fd):
        name = input('Enter a name for the warehouse: ')
        while True:
            try:
                num_aisles = int(input('Enter the amount of aisles you want in the warehouse (minimum 1): '))
                if num_aisles <= 0:
                    raise ValueError('There must be at least 1 aisle')
            except ValueError as e:
                print('ValueError:', e)
                continue
            break
        
        #TODO do same as above for rows in aisles, slots in rows, don't populate items

        #TODO create warehouse object and make a method for dumping to file 
        # warehouse = {
        #     'name': name,
        #     'contents': {}
        # }

        # with open(fd, 'w') as f:
        #     json.dump(warehouse, f, indent="\t",)


    def load(self):
        r = None
        with open(self.FILENAME, 'r') as f:
            r = json.load(f)
            print(r)
        return r['name'], r['contents']


if __name__ == '__main__':
    handler = JSON_HANDLER()