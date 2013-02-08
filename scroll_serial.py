#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''    
Scroll format : 
[date][three headlines] .. repeat until all headlines are used
[date][stock prices]
.. repeat forever
'''
import time,sys,os,random
import codecs
import serial,os,sys,time,tty,termios
import codecs
import datetime

newsfile = 'news'
stockfile = 'stocks'
baudrate = 4800
delay = .08

execfile('load_font.py')
execfile('simpleserial.py')

ser=startSerial(baudrate)

def sendchar(ch):
    i = mapping.index(ch)
    if i>=0 and i<len(chars):
        chardata = chars[i]+[0,];
        for column in chardata:
            ser.write(chr(column))
            time.sleep(delay)
            #raw_input('press2advance')

def send(lines):
    for ch in lines:
        if ch in mapping:
            sendchar(ch)

def sendtime():
    t = datetime.datetime.now().strftime("%b %d, %Y %H:%M")+' -- '
    send(t)

def sendnews():
    with codecs.open(newsfile, encoding='utf-8') as myfile: # keep opening the file, maybe its different this time?
        lines = myfile.readlines()
        random.shuffle(lines)
        while len(lines)>3:
            show = lines[:3]
            lines = lines[3:]
            show = u''.join(u''.join([x+u' -- ' for x in show]).split('\n'))
            sendtime()
            print show
            send(show)
        if len(lines)>0:
            show = lines
            show = u''.join(u''.join([x+u' -- ' for x in show]).split('\n'))
            sendtime()
            print show
            send(show)

def sendstocks():
    with codecs.open(stockfile, encoding='utf-8') as myfile: # keep opening the file, maybe its different this time?
        lines = myfile.readlines()
        show = lines
        show = u''.join(u''.join([x+u' -- ' for x in show]).split('\n'))
        sendtime()
        print show
        send(show)

while 1:
    sendnews()
    sendstocks()

closeSerial(ser)





