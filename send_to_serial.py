#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial,os,sys,time,tty,termios
from pylab import *

newsfile = 'news'
baudrate = 4800
delay = .05

execfile('load_font.py')
execfile('simpleserial.py')

ser=startSerial(baudrate)

while(1):
	with open(newsfile) as myfile: # keep opening the file, maybe its different this time?
		lines = myfile.readlines()
		lines = ' -- '.join(lines)
		lines = ''.join(lines.split('\n'))
		length = len(lines)
		for ch in lines:
			sys.stdout.write(ch)
			sys.stdout.flush()
			if ch in mapping:
				chardata = chars[mapping.index(ch)]+[0,];
				for column in chardata:	
					ser.write(chr(column))
					time.sleep(delay)
					#raw_input('press2advance')

closeSerial(ser)





