#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''    
We have a Python script that grabs news headlines for us. 
This script tests out our scrolling marquee in the terminal.
This is a quick hack. For example it will get upset if you resize terminal
after it starts.
'''
import time,sys,os,random
import codecs

newsfile = 'news'
onsymbol = "▒"

execfile('load_font.py')
execfile('get_terminal_size.py')

vpad = ((height-5)/2)
clear = vpad+5
os.system('reset')

# initialize an empty text buffer
slideaway = [' '*5 for i in range(width)]

while 1:
	with codecs.open(newsfile, encoding='utf-8') as myfile: # keep opening the file, maybe its different this time?
		lines = myfile.readlines()
		random.shuffle(lines)
		lines = u' -- '.join(lines)
		lines = u''.join(lines.split('\n'))
		length = len(lines)
		for ch in lines:
			if ch in mapping:
				i = mapping.index(ch)
				if i>=0 and i<len(chars):
					chardata = chars[i]+[0,];
					for column in chardata:
						columndata = [ onsymbol if ((column>>i)&1) else ' ' for i in range(5)]
						slideaway = slideaway[1:]+[columndata]
						data = '\n'.join(''.join(x) for x in zip(*slideaway))
						sys.stdout.write('\x1B[%dA'%clear+'\n'*vpad+'\r'+data)
						sys.stdout.flush()
						time.sleep(0.03)

os.system('reset')


