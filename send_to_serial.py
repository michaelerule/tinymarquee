#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial,os,sys,time,tty,termios
from pylab import *

newsfile = 'news'
fontfile = 'marquee_font.txt'
baudrate = 4800
delay = .05
devs = [s for s in os.listdir('/dev') if 'ttyUSB' in s]
if len(devs)<1:
	print "no serial devices found!"
	sys.exit(0)
port = '/dev/'+devs[0]

# Load the font information
mapping = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890., ;:-+=?!\'*^[♥&$'
chars = None
with open(fontfile,'r') as f:
    data = ''.join(f.readlines())
    chars = [map(eval,s.split()) for s in data.split('-')]
print chars

def startSerial(baudrate = 9600):
    os.system('stty -F %s %d cs8 cread'%(port,baudrate))
    ser = serial.Serial(port,baudrate,timeout=0)
    time.sleep(.1)
    if not ser.isOpen():
        print 'CONNECTION FAILED'
        sys.exit(0)
    print 'SUCCESS, USING PORT %s AT %d'%(port,baudrate)
    return ser
    
def closeSerial(ser):
    ser.close()
    print 'CLOSED'

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





