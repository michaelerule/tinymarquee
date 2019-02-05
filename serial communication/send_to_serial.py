#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial,os,sys,time,tty,termios
from pylab import *
import codecs

newsfile = 'news'
baudrate = 4800
delay = .08

execfile('load_font.py')
execfile('simpleserial.py')


ser=startSerial(baudrate)

while 1:
	with codecs.open(newsfile, encoding='utf-8') as myfile: # keep opening the file, maybe its different this time?
		lines = myfile.readlines()
		lines = ' -- '.join(lines)
		lines = ''.join(lines.split('\n'))
		length = len(lines)
		print repr(lines)
		for ch in lines:
		    sys.stdout.write(' %s '%ch)
		    sys.stdout.flush()
		    if ch in mapping:
		        index = mapping.index(ch)
		        sys.stdout.write(str(index))
		        sys.stdout.flush()
		        if index>=0 and index<len(chars):
		            chardata = chars[index]+[0,];
		            for column in chardata:    
		                ser.write(chr(column))
		                time.sleep(delay)
		                #raw_input('press2advance')

closeSerial(ser)





