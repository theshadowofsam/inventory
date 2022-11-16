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
    def __init__(self, name='', aisles=[]) -> None:
        self.name = name
        self.aisles = aisles
    
    def add_aisle(self, isle_name):
        temp = self._AISLE(isle_name)
        self.aisles.append(temp)

    class _AISLE:
        def __init__(self, name, rows=None) -> None:
            self.name = name
            if rows is None:
                self.rows = []
            else:
                self.rows = rows
        
        def add_row(self, row_name):
            temp = WAREHOUSE._ROW(row_name)
            self.rows.append(temp)

    class _ROW:
        def __init__(self, name, slots=None) -> None:
            self.name = name
            if slots is None:
                self.slots = []
            else:
                self.slots = slots
        
        def add_slot(self, slot_name):
            temp = WAREHOUSE._SLOT(slot_name)
            self.slots.append(temp)

    class _SLOT:
        def __init__(self, name, item=None) -> None:
            self.name = name
            self.item = item

        def add_item(self, item_name, amount):
            temp = WAREHOUSE._ITEM(item_name, amount)
            self.item = temp

    class _ITEM:
        def __init__(self, name, amount=None) -> None:
            self.name = name
            if amount is None:
                self.amount = 0
            else:
                self.amount = amount


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
            self.warehouse = WAREHOUSE()
            self._generate(self.FILENAME)
            self.dump()
        else:    
            name, contents = self.load()
            self.warehouse = WAREHOUSE(name, contents)
            print(self.warehouse)
            print(self.warehouse.name, '\n', self.warehouse.contents)
            
    #prompts user for warehouse information and creates warehouse object
    def _generate(self, fd):
        
        #_AISLES info
        name = input('Enter a name for the warehouse: ')
        self.warehouse.name = name
        while True:
            try:
                num_aisles = int(input('Enter the amount of aisles you want in the warehouse (minimum 1): '))
                if num_aisles <= 0:
                    raise ValueError('There must be at least 1 aisle')
            except ValueError as e:
                print('ValueError:', e)
                continue
            break
        
        #ADD AISLES
        for i in range(num_aisles):
            self.warehouse.add_aisle(f'{i+1}')
        
        #ADD ROWS
        while True:
            eq = input('Will all aisles have the same amount of rows?(y/n):')[0].lower()
            if eq in self.YN:
                break
            else:
                print('Bad input: please enter y or n')

        if eq == 'y':
            while True:
                try:
                    num_rows = int(input('Enter the number of rows for all aisles (minimum 1): '))
                    break
                except ValueError as e:
                    print(f'Bad input: {e}')
                    continue
            
            for aisle in self.warehouse.aisles:
                for i in range(num_rows):
                    aisle.add_row(f'{i+1}')
        else:
             for aisle in self.warehouse.aisles:
                try:
                    num_rows = int(input(f'Enter the number of rows for aisle {aisle.name}: '))
                    for i in range(num_rows):
                        aisle.add_row(f'{i+1}')
                except ValueError as e:
                    print(f'Bad input: {e}')
                    continue
        
        #ADD SLOTS
        while True:
            eq = input('Will all aisles and rows have the same amount of slots?(y/n):')[0].lower()
            if eq in self.YN:
                break
            else:
                print('Bad input: please enter y or n')

        if eq == 'y':
            while True:
                try:
                    num_slots = int(input('Enter the number of slots for all rows (minimum 1): '))
                    break
                except ValueError as e:
                    print(f'Bad input: {e}')
                    continue
            
            for aisle in self.warehouse.aisles:
                for row in aisle.rows:
                    for i in range(num_slots):
                        row.add_slot(f'{i+1}')
        else:
            for aisle in self.warehouse.aisles:
                for row in aisle.rows:
                    while True:
                        try:
                            num_slots = int(input(f'Enter the number of slots for {row.name} (minimum 1): '))
                            break
                        except ValueError as e:
                            print(f'Bad input: {e}')
                            continue
                    for i in range(num_slots):
                        row.add_slot(f'{i+1}')
                    
        print(len(self.warehouse.aisles))
        for aisle in self.warehouse.aisles:
            print('\t', len(aisle.rows))
            for row in aisle.rows:
                print('\t\t', len(row.slots))

    #TODO
    def load(self):
        pass

    #translate to allow json to write out
    def dump(self):
        warehouse = {'name': self.warehouse.name}
        aisles = {}
        for aisle in self.warehouse.aisles:
            rows = {}
            for row in aisle.rows:
                slots = {}
                for slot in row.slots:
                    if slot.item is None:
                        slots[slot.name] = None
                    else:
                        item = {}
                        item['name'] = slot.name                    
                        item['amount'] = slot.amount
                        slots[slot.name] = item
                rows[row.name] = slots
            aisles[aisle.name] = rows
        
        warehouse['aisles'] = aisles

        with open(self.FILENAME, 'w') as f:
            json.dump(warehouse, f, indent='\t')


if __name__ == '__main__':
    handler = JSON_HANDLER()