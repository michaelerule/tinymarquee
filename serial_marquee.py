#!/usr/bin/env python
''''
Operates the marquee. 
General purpose : 
Start scrolling marquee.
Intermittently update news signals and stock prices.
Every 10 minutes or so, perhaps
'''

import random
import os
import time

os.system('./scroll_serial.py &')
while True:
	os.system('./scrape_news.py news 1>/dev/null &')
	os.system('./scrape_stocks.py stocks 1>/dev/null &')
	time.sleep(int(random.random()*6000)+1000)


