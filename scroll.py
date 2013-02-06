#!/usr/bin/env python
# -*- coding: utf-8 -*-
    
'''
We have a Python script that grabs news headlines for us. 
This script tests out our scrolling marquee in the terminal.

This is a quick hack. For example it will get upset if you resize terminal
after it starts.
'''

import time
import sys
import os
import random

def getTerminalSize():
    '''
    get terminal dimension functions
    ripped from stackoverflow
    http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
    '''
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,'1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])

(width, height) = getTerminalSize()
vpad = ((height-5)/2)
clear = vpad+5

newsfile = 'news'
fontfile = 'marquee_font.txt'
onsymbol = "▒"

# define the font mapping -- it's nonstandard
mapping = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890., ;:-+=?!\'*^$♥&'

# Load the font information
chars = None
with open(fontfile,'r') as f:
    data = ''.join(f.readlines())
    chars = [map(eval,s.split()) for s in data.split('-')]
print chars

os.system('reset')

# initialize an empty text buffer
slideaway = [' '*5 for i in range(width)]

while 1:
	with open(newsfile) as myfile: # keep opening the file, maybe its different this time?
		lines = myfile.readlines()
		random.shuffle(lines)
		lines = ' -- '.join(lines)
		lines = ''.join(lines.split('\n'))
		length = len(lines)
		for ch in lines:
			if ch in mapping:
				chardata = chars[mapping.index(ch)]+[0,];
				for column in chardata:
				    columndata = [ onsymbol if ((column>>i)&1) else ' ' for i in range(5)]
				    slideaway = slideaway[1:]+[columndata]
				    data = '\n'.join(''.join(x) for x in zip(*slideaway))
				    sys.stdout.write('\x1B[%dA'%clear+'\n'*vpad+'\r'+data)
				    sys.stdout.flush()
				    time.sleep(0.03)

os.system('reset')


