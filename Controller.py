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
    
    def __init__(self, name=None, aisles=None) -> None:
        if name is None:
            self.name = ''
        else:
            self.name = name
        if aisles is None:
            self.aisles = []
        else:
            self.aisles = aisles
    
    def add_aisle(self, isle_name):
        temp = self._AISLE(isle_name)
        self.aisles.append(temp)
        return temp

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
            return temp

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
            return temp

    class _SLOT:
        def __init__(self, name, item=None) -> None:
            self.name = name
            self.item = item

        def add_item(self, item_name, quantity):
            temp = WAREHOUSE._ITEM(item_name, quantity)
            self.item = temp
            return temp

    class _ITEM:
        def __init__(self, name, quantity=None) -> None:
            self.name = name
            if quantity is None:
                self.quantity = 0
            else:
                self.quantity = quantity
    
    def query(self, aisle=None, row=None, slot=None):
        if aisle is None:
            pass
        elif row is None:
            pass
        elif slot is None:
            pass
        else:
            pass

    def pull(self, aisle, row, slot, quantity):
        pass

    def push(self, aisle, row, slot, quantity):
        pass

    def empty(self, aisle=None, row=None, slot=None):
        if aisle is None:
            pass
        elif row is None:
            pass
        elif slot is None:
            pass
        else:
            pass

    def replace(self, aisle, row, slot, new_item):
        pass

    def set(self, aisle, row, slot, item):
        pass


class JSON_HANDLER:
    
    FILENAME = 'WAREHOUSE.txt'
    YES_NO = ['y', 'n']

    def __init__(self) -> None:
        try:
            with open(self.FILENAME, 'r') as f:
                pass
        except FileNotFoundError as e:
            self.warehouse = WAREHOUSE()
            self._generate(self.FILENAME)
            self.dump()
        else:    
            self.warehouse = WAREHOUSE()
            self.load()
            self.dump()

    # prompts user for warehouse information and creates warehouse object
    def _generate(self, fd):
        
        # aisle info
        name = input('Enter a name for the warehouse: ')
        self.warehouse.name = name
        while True:
            try:
                num_aisles = int(input('Enter the amount of aisles you want in the warehouse (minimum 1): '))
                if num_aisles <= 0:
                    raise ValueError('There must be at least 1 aisle')
            except ValueError as e:
                print('ValueError: ', e)
                continue
            break
        
        # add aisles
        for i in range(num_aisles):
            self.warehouse.add_aisle(f'{i+1}')
        
        # row info
        while True:
            all_equivalent = input('Will all aisles have the same amount of rows?(y/n):')[0].lower()
            if all_equivalent in self.YES_NO:
                break
            else:
                print('Bad input: please enter y or n')
        
        # add rows
        if all_equivalent == 'y':
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
                while True:
                    try:
                        num_rows = int(input(f'Enter the number of rows for aisle {aisle.name}: '))
                        for i in range(num_rows):
                            aisle.add_row(f'{i+1}')
                    except ValueError as e:
                        print(f'Bad input: {e}')
                        continue
        
        # slots info
        while True:
            all_equivalent = input('Will all aisles and rows have the same amount of slots?(y/n):')[0].lower()
            if all_equivalent[0].lower() in self.YES_NO:
                break
            else:
                print('Bad input: please enter y or n')

        # add slots
        if all_equivalent[0].lower() == 'y':
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

    # builds the warehouse onject from loaded json object
    def load(self):
        with open(self.FILENAME, 'r') as f:
            data = json.load(f)
            print(data)
            self.warehouse.name = data['name']
            aisles = data['aisles']
            for aisle in aisles.keys():
                aisle_ref = self.warehouse.add_aisle(aisle)
                aisle_ref.rows = []
                rows = aisles[aisle]
                for row in rows.keys():
                    row_ref = aisle_ref.add_row(row)
                    row_ref.slots = []
                    slots = rows[row]
                    for slot in slots.keys():
                        slot_ref = row_ref.add_slot(slot)
                        slot_ref.item = None
                        if slots[slot] is not None:
                            item_ref = slot_ref.add_item(slots[slot]['name'], slots[slot]['quantity'])    

    # translate to allow json to write out
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
                        item['quantity'] = slot.quantity
                        slots[slot.name] = item
                rows[row.name] = slots
            aisles[aisle.name] = rows
        
        warehouse['aisles'] = aisles

        with open(self.FILENAME, 'w') as f:
            json.dump(warehouse, f, indent='\t')


#TODO inside
class SERVER:
    
    REQUEST_CODES = [
        'CODE_STOP',
        'CODE_END'
        'CODE_QUERY',
        'CODE_PULL',
        'CODE_PUSH',
        'CODE_EMPTY',
        'CODE_REPLACE',
        'CODE_SET'
    ]

    def __init__(self, HOST=None, PORT=None) -> None:
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SOCKET.settimeout(5)
        if HOST is None:
            self.HOST = '127.0.0.1'
        else:
            self.HOST = HOST
        if PORT is None:
            self.PORT = 47469
        else:
            self.PORT = PORT
        self.json_handler = JSON_HANDLER()

    def run(self):
        self.SOCKET.bind((self.HOST, self.PORT))
        self.SOCKET.listen()

        while True:
            try:
                connection, address = self.SOCKET.accept()
                connection.settimeout(None)
            except TimeoutError as e:
                continue
            with connection as conn:
                while True:
                    request = conn.recv(1024).decode()
                    if request in self.REQUEST_CODES:
                        response = self.handle(request)
                        conn.send(response)


    def handle(self, request_type, data=None): # TODO: Handle requests from the server and respond
        match request_type:
            case 'CODE_STOP': # return slot data. perhaps warehouse, aisle, or row too?
                return 'CODE_STOP'
            case 'CODE_END': # pull items from a slot (reduce quantity)
                return 'CODE_END'
            case 'CODE_QUERY': # place additional items in a slot (increase quantity)
                return 'CODE_QUERY'
            case 'CODE_PULL': # clear a slot of all values
                return 'CODE_PULL'
            case 'CODE_PUSH': # same as clear and set for all values
                return 'CODE_PUSH'
            case 'CODE_EMPTY': # set a slot value
                return 'CODE_EMPTY'
            case 'CODE_REPLACE':
                return 'CODE_REPLACE'
            case 'CODE_SET':
                return 'CODE_SET'
            case _:
                return 'Something strange happened here...'
            

if __name__ == '__main__':
    server = SERVER()
    server.run()