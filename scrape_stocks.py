#!/usr/bin/env python
#
#  Copyright (c) 2012, Michael Rule (mrule7404@gmail.com)
#
#  license: GNU LGPL
#
#  This is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.

import sys

# change function to "pass" to suppress comment printing
def documentation(s):
	print s

# loads name from first command line argument if available
# otherwise, saves data to file "news"
outfilename = 'news'
if len(sys.argv)>1:
	outfilename = sys.argv[1]
outfile = open(outfilename,'w')
def output(s):
	print s
	outfile.write(s+'\n')
	
documentation('''
Generate streaming information for scrolling marquee 

Stock monitoring
-- Keep a list of interesting funds
-- Grab the prices from yahoo using ystockquote

All data is output to file "news" in current working directory. You may 
specify a different output file name as the first command line option.
''')

# USED TO DOWNLOAD WEBSITES
import urllib2 
# USED TO QUERY REDDIT API
import json 
# USED TO PARSE HTML DATA
from BeautifulSoup import BeautifulStoneSoup
# USED TO GET STOCK DATA FROM YAHOO FINANCE
execfile('./ystockquote.py')

stocks = '''
S&P500
DOW
DBV
'''.split('\n')[1:-1]

for name in stocks:
	output( "%s %s"%(name,float(get_price(name))))

outfile.close()


