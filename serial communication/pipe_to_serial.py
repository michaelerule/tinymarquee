#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import serial,os,sys,time,tty,termios
from pylab import *
import codecs

baudrate = 9600#4800
delay = .08

execfile('load_font.py')
execfile('getchar.py')
execfile('simpleserial.py')

gg = _Getch()

ser=startSerial(baudrate)

print('supported characters:')
print('  ',''.join(mapping))

while(1):
    ch = gg()
    if ch in ['\x1Bc','\x03','\x04','\x0C','\x0A','\x33']:
        print('\n\n Exiting...')
        sys.exit(0)
    sys.stdout.write(ch)
    sys.stdout.flush()
    if ch in mapping:
        index = mapping.index(ch)
        if index >=0 and index < len(chars):
            chardata = chars[index]+[0,];
            for column in chardata:    
                ser.write(chr(column))
                time.sleep(delay)

closeSerial(ser)





