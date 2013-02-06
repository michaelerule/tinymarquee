#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial,os,sys,time,tty,termios
from pylab import *

fontfile = 'marquee_font.txt'
baudrate = 4800
delay = .08
devs = [s for s in os.listdir('/dev') if 'ttyUSB' in s]
if len(devs)<1:
	print "no serial devices found!"
	sys.exit(0)
port = '/dev/'+devs[0]

# Load the font information
mapping = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890., ;:-+=?!\'*^$♥&'
chars = None
with open(fontfile,'r') as f:
    data = ''.join(f.readlines())
    chars = [map(eval,s.split()) for s in data.split('-')]
print chars

class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()
    def __call__(self): return self.impl()
class _GetchUnix:
    def __init__(self):
        import tty, sys
    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
class _GetchWindows:
    def __init__(self):
        import msvcrt
    def __call__(self):
        import msvcrt
        return msvcrt.getch()

gg = _Getch()

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
	ch = gg()	
	sys.stdout.write(ch)
	sys.stdout.flush()
	if ch == '\x1Bc':
		system.exit(0)
	if ch in mapping:
		chardata = chars[mapping.index(ch)]+[0,];
		for column in chardata:	
			ser.write(chr(column))
			time.sleep(delay)

closeSerial(ser)





