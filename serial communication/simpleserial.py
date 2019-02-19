#!/usr/bin/env python
# -*- coding: utf-8 -*-

devs = [s for s in os.listdir('/dev') if 'ttyUSB' in s or 'ttyACM' in s]
if len(devs)<1:
	print "no serial devices found!"
	sys.exit(0)
port = '/dev/'+devs[0]

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
