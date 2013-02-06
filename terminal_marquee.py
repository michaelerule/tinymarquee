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

os.system('./scroll.py &')
while True:
	os.system('./scrape_news.py 1>/dev/null &')
	time.sleep(int(random.random()*6000/60))


