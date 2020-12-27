#!/usr/bin/env python

import curses
import serial  # pip install pyserial

s = serial.Serial('/dev/ttyUSB1', baudrate=19200)
scr = curses.initscr()
curses.noecho()

klawisz_na_opis = {
    '\n': 'Enter',
    'D': 'Lewo',
    'C': 'Prawo',
    'B': 'Dol',
    'A': 'Gora',
}

klawisz_na_komende = {
    '\n': 'C00',
    'q': 'C01',
    '1': 'C05',
    '2': 'C06',
    'm': 'C1C',
    'c': 'C1D',
    # tak naprawde to sa escape sequences i to dziala raczej przez przypadek
    'D': 'C3B',
    'C': 'C3A',
    'A': 'C3C',
    'B': 'C3D',
    ' ': 'C3F',
}

komenda_na_opis = {
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
}


def generuj_instrukcje():
    opisy_klawiszy = {chr(getattr(curses, x)): x[4:]
                      for x in dir(curses) if x.startswith('KEY_')}
    ret = ''
    for klawisz, komenda in klawisz_na_komende.items():
        opis_klawisza = None
        if opis_klawisza is None:
            opis_klawisza = klawisz_na_opis.get(klawisz)
        if opis_klawisza is None:
            opis_klawisza = opisy_klawiszy.get(klawisz)
        if opis_klawisza is None:
            opis_klawisza = klawisz if klawisz.isalnum() else repr(klawisz)
        opis_komendy = komenda_na_opis[komenda]
        ret += f'{opis_klawisza}: {opis_komendy}'
        if ret:
            ret += '\n'
    return ret


char = '.'
while True:
    scr.clear()
    scr.addstr(0, 0, 'Kod klawisza: ' + str(ord(char)) +
               '\n\n' + generuj_instrukcje())
    char = chr(scr.getch())
    komenda = klawisz_na_komende.get(char)
    if komenda:
        s.write(komenda.encode() + b'\r\n')
