#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial,os,sys,time,tty,termios
from pylab import *
import codecs
import codecs

baudrate = 4800
delay = .08

execfile('load_font.py')
execfile('getchar.py')
execfile('simpleserial.py')

gg = _Getch()

ser=startSerial(baudrate)

while(1):
	ch = unicode(gg()	)
	sys.stdout.write(ch)
	sys.stdout.flush()
	if ch == '\x1Bc': # THIS IS BROKEN!
		system.exit(0)
	if ch in mapping:
		index = mapping.index(ch)
		if index >=0 and index < len(chars):
			chardata = chars[index]+[0,];
			for column in chardata:	
				ser.write(chr(column))
				time.sleep(delay)

closeSerial(ser)





