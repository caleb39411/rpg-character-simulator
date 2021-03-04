#!/usr/bin/env python3

import random
import pickle
import sys
import time
import os
from distutils.util import strtobool
from tabulate import tabulate


attr_dict = {
    1: ['power', 'Power'],
    2: ['sp_power', 'Special Power'],
    3: ['speed', 'Speed'],
}

headers = [
    'Number', 'Name', 'Type', 'Health',
    'Power', 'Special Power', 'Speed',
]


def prompt(query):
    val = input('{0} [y/n]: '.format(query))
    try:
        ret = strtobool(val)
    except ValueError:
        print('\n\x1b[31m' + 'Please answer with [y/n].' + '\x1b[0m')
        return prompt(query)
    return ret


def name_gen():
    vowels = ['a', 'e', 'i', 'o', 'u']
    consonants = [
        'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n',
        'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z',
    ]

    return str(
        random.choice(vowels).upper() +
        random.choice(consonants) +
        '-' +
        random.choice(consonants) +
        random.choice(vowels) +
        random.choice([random.choice(consonants), '']) +
        '-' +
        random.choice(consonants) +
        random.choice(vowels) +
        random.choice([random.choice(consonants), ''])
    )


def gen_table():
    global table
    table = []
    for _ in range(10):
        table.append([
            _ + 1,
            getattr(globals()['char{0}'.format(_)], 'name'),
            getattr(globals()['char{0}'.format(_)], 'class_name'),
            100,
            getattr(globals()['char{0}'.format(_)], 'power'),
            getattr(globals()['char{0}'.format(_)], 'sp_power'),
            getattr(globals()['char{0}'.format(_)], 'speed'),
        ])


def char_replace():
    try:
        replace_no = int(input(
            'Enter the number of the character to be replaced [1-10]: '
        ))
    except ValueError:
        print('\n\x1b[31m' + 'Please enter a valid number.' + '\x1b[0m')
        return char_replace()
    if 1 <= replace_no <= 10:
        globals()['char{0}'.format(replace_no - 1)] = random.choice(classes)()
        print('Character', str(replace_no), 'replaced.')
        time.sleep(1.5)
        gen_table()
        return menu()
    print('\n\x1b[31m' + 'Please enter a valid number.' + '\x1b[0m')
    return char_replace()


def char_edit():
    try:
        edit_no = int(input(
            'Enter the number of the character to be edited [1-10]: '
        ))
    except ValueError:
        print('\n\x1b[31m' + 'Please enter a number [1-10]:' + '\x1b[0m')
        return char_edit()
    if 1 <= edit_no <= 10:
        print(
            'You are editing {0}'.format(
                globals()['char{0}'.format(edit_no - 1)].name
            )
        )
        for entry in attr_dict:
            print('{0}. {1}'.format(entry, attr_dict[entry][1]))
        try:
            attr_select = int(input('Which attribute is to be changed? [1-3]: '))
        except ValueError:
            print('\n\x1b[31m' + 'Please enter a number [1-10]:' + '\x1b[0m')
            return char_edit()
        if 1 <= attr_select <= 3:
            return attr_edit(attr_select, edit_no)
    print('\n\x1b[31m' + 'Please enter a valid number.' + '\x1b[0m')
    return char_edit()


def attr_edit(attr_no, char_no):
    try:
        attr_val = int(input(
            'Enter the new value of the attribute [1-100]: '
        ))
    except ValueError:
        print('\n\x1b[31m' + 'Please enter a valid number.' + '\x1b[0m')
        return attr_edit(attr_no, char_no)
    if 1 <= attr_val <= 100:
        setattr(
            globals()['char{0}'.format(char_no - 1)],
            attr_dict[attr_no][0],
            attr_val,
        )
        gen_table()
        return menu()
    print('\n\x1b[31m' + 'Please enter a valid number.' + '\x1b[0m')
    return attr_edit(attr_no, char_no)


def save_data():
    if prompt(
            '\nSaving a file will overwrite the current save (if any).\n' +
            'Do you wish to continue?'
    ):
        with open((os.path.join(sys.path[0], 'save.dat')), 'wb') as file:
            for _ in range(10):
                pickle.dump(globals()['char{0}'.format(_)], file)
        print('\nSaved to save.dat.\n')
    else:
        print('\nSave cancelled.\n')
    time.sleep(1.5)
    return menu()


def load_data():
    if prompt(
            '\nLoading a file will overwrite the current configuration.\n' +
            'Do you wish to continue?'
    ):
        if os.path.exists(os.path.join(sys.path[0], 'save.dat')):
            global char0, char1, char2, char3, char4, char5, char6, char7, char8, char9
            with open(os.path.join(sys.path[0], 'save.dat'), 'rb') as file:
                for _ in range(10):
                    globals()['char{0}'.format(_)] = pickle.load(file)
            gen_table()
            print('\nFile save.dat loaded.\n')
        else:
            print(
                '\nFile save.dat does not exist in the',
                'directory containing this script.\n'
            )
    else:
        print('\nFile not loaded.\n')
    time.sleep(1.5)
    return menu()


def exit_check():
    if prompt('Any unsaved data will be lost. Do you wish to continue?'):
        return sys.exit(0)
    return menu()


menu_dict = {
    1: [char_replace, 'Replace character'],
    2: [char_edit, 'Edit character attribute'],
    3: [save_data, 'Save'],
    4: [load_data, 'Load'],
    5: [exit_check, 'Exit'],
}

def menu():
    print(tabulate(table, headers))
    input('\nPress ENTER to continue to menu:\n')
    for entry in menu_dict:
        print('{0}. {1}'.format(entry, menu_dict[entry][1]))
    selection = int(input('Please select an option [1-5]: '))
    if 1 <= selection <= 5:
        menu_dict[selection][0]()
    else:
        print(
            '\n\x1b[31m' +
            'Unknown option selected. Please enter a valid number.' +
            '\x1b[0m\n'
        )
        menu()


class Barbarian:
    class_name = 'Barbarian'
    power = 70
    sp_power = 20
    speed = 50

    def __init__(self):
        self.name = name_gen()


class Elf:
    class_name = 'Elf'
    power = 30
    sp_power = 60
    speed = 10

    def __init__(self):
        self.name = name_gen()


class Wizard:
    class_name = 'Wizard'
    power = 50
    sp_power = 70
    speed = 30

    def __init__(self):
        self.name = name_gen()


class Dragon:
    class_name = 'Dragon'
    power = 90
    sp_power = 40
    speed = 50

    def __init__(self):
        self.name = name_gen()


class Knight:
    class_name = 'Knight'
    power = 60
    sp_power = 10
    speed = 60

    def __init__(self):
        self.name = name_gen()


classes = [Barbarian, Elf, Wizard, Dragon, Knight]

for _ in range(10):
    globals()['char{0}'.format(_)] = random.choice(classes)()
gen_table()
menu()
