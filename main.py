#!/usr/bin/env python

import sys
import curses
from curses import wrapper
import serial  # pip install pyserial

keylabels = {
    chr(curses.KEY_RIGHT): 'Right',
    chr(curses.KEY_LEFT): 'Left',
    chr(curses.KEY_UP): 'Up',
    chr(curses.KEY_DOWN): 'Down',
    '\n': 'Enter'
}

keys = {
    'w': 'C00',
    'q': 'C01',
    '1': 'C05',
    '2': 'C06',
    's': 'C1C',
    'a': 'C1D',
    chr(curses.KEY_RIGHT): 'C3A',
    chr(curses.KEY_LEFT): 'C3B',
    chr(curses.KEY_UP): 'C3C',
    chr(curses.KEY_DOWN): 'C3D',
    '\n': 'C3F',
    'x': 'x'
}

commands = {
    'C00': 'Power ON',
    'C01': 'Power OFF',
    'C05': 'Computer 1',
    'C06': 'Computer 2',
    'C1C': 'Menu ON',
    'C1D': 'Menu OFF',
    'C3A': 'Pointer right',
    'C3B': 'Pointer left',
    'C3C': 'Pointer up',
    'C3D': 'Pointer down',
    'C3F': 'Enter',
    'x': 'Exit'
}

def usage():
    key_descriptions = {chr(getattr(curses, x)): x[4:]
                      for x in dir(curses) if x.startswith('KEY_')}
    ret = ''

    for known_key, command in keys.items():
        key_description = None
        if known_key in keylabels.keys():
            key_description = keylabels.get(known_key)
        if key_description is None:
            key_description = known_key if str(known_key).isalnum() else repr(known_key)
        cmd_description = commands.get(command)
        ret += f'{key_description}: {cmd_description}'
        if ret:
            ret += '\n'
    return ret

def main(scr):
    char = '\0'

    if len(sys.argv) != 2:
        print("usage: {} serialdevice".format(sys.argv[0]))
        quit(1)

    try:
        s = serial.Serial(sys.argv[1], baudrate=19200)
    except serial.serialutil.SerialException as err:
        print("Error while trying to open device {}: {}".format(sys.argv[1], err))
        quit(1)

    curses.noecho()

    while True:
        scr.clear()
        scr.addstr(0, 0, 'Last key: ' + str(ord(char)) +
               '\n\n' + usage())
        char = chr(scr.getch())
        if char == 'x':
            curses.endwin()
            quit(0)
        else:
            command = keys.get(char)
            if command:
                s.write(command.encode() + b'\r\n')

if __name__ == "__main__":
    wrapper(main)
