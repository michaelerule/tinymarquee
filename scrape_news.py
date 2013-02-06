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

news headlines
-- al jazeera
-- reddit world news with Reddit's JSON API
stock prices
-- Yahoo finance

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

# For the URL library, 
# create a custom user agent string to conform to reddit API TOS
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'headline_scraper michaelerule')]
urlopen = opener.open

# START WITH AN EMPTY SET OF HEADLINES
headlines = set()

documentation('''
Scrape Al Jazeera Headlines
-- Crawl over the regional Al Jazeera news sites. 
-- Rely on their stories being stored in a table ( BRITTLE! ), and grab all 
     table data from the sites using beautifulsoup. 
-- Rely on a specific CSS class ( BRITTLE! ) currently used to format their
     headline text to identify headlines. 
-- Trim of surplus whitespace.
''')
stem    = 'http://www.aljazeera.com/'
tocrawl = [stem]+[stem+'news/'+rest for rest in 'africa americas asia-pacific asia europe middleeast'.split()]
for site in tocrawl:
	print "crawling %s"%site
	for soup in BeautifulStoneSoup(urlopen(site).read()).findAll('td'):
		for a in soup.findAll('a', attrs={'class':'indexText-Bold2 indexText-Font2'}):
			if len(a):
				trim = ' '.join(a.contents[0].split())
				if trim:
					headlines.add(trim)

documentation('''
Scrape reddit headlines
-- Focus on worldnews and news
-- Grab all top stories
-- Extract post title as a headline
-- Trim whitespace
''')
subreddits = 'worldnews news'.split()
for subreddit in subreddits:
	for child in json.load(urlopen("http://www.reddit.com/r/%s/top/.json"%subreddit))['data']['children']:
		trim = ' '.join(child['data']['title'].split())
		if trim:
			headlines.add(trim)

documentation('''
Done scraping news, headlines are:
''')
headlines = [h for h in headlines if len(h)<60] # enforce 60 char limit -- some reddit titles are long
for headline in headlines:
	output(headline)

outfile.close()


