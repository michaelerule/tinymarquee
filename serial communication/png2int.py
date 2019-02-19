#!/usr/bin/env jython
'''
This script examines a PNG containing a bitmap font and outputs each caracter
as a series of numbers. Each number represents a column of the character,
where the bits represent the row states on / off. This way, we can just send
these numbers to the scrolling marquee without further processing, and they
will draw out a character. 
'''

fname = 'alphabet2.png'

from javax.imageio import ImageIO
from java.io import File
from java.awt.image import BufferedImage

fileimage = ImageIO.read(File(fname))
image = BufferedImage(fileimage.width,fileimage.height,BufferedImage.TYPE_INT_RGB);
image.graphics.drawImage(fileimage,0,0,None)

def getcol(image,col):
	return [int(image.getRGB(col,row)) for row in range(image.height)];

f=open('marquee_font.txt','w')

clist=[]
for col in range(image.width):
	c = getcol(image,col)
	if c[0]==-65281:
		for c in clist:
			print c
			intcode = sum([ 2**i if c[i] else 0 for i in range(len(c))])
			f.write('0x%02x\n'%intcode)
		f.write('-\n')
		clist = []
	else:
		clist.append([int(x==-16777216) for x in c])

f.write('\n')
f.flush()
f.close()



