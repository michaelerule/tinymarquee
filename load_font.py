#!/usr/bin/env python
# -*- coding: utf-8 -*-

fontfile = 'marquee_font.txt'
# Load the font information
mapping = [u'A',u'B',u'C',u'D',u'E',u'F',u'G',u'H',u'I',u'J',u'K',u'L',u'M',u'N',u'O',u'P',
u'Q',u'R',u'S',u'T',u'U',u'V',u'W',u'X',u'Y',u'Z',u'a',u'b',u'c',u'd',u'e',u'f',u'g',u'h',u'i',
u'j',u'k',u'l',u'm',u'n',u'o',u'p',u'q',u'r',u's',u't',u'u',u'v',u'w',u'x',u'y',u'z',u'1',u'2',
u'3',u'4',u'5',u'6',u'7',u'8',u'9',u'0',u'.',u',u',u'',u';',u':',u'-',u'+',u'=',u'?',u'!',
u'\'',u'*',u'⌶',u'█',u'♥',u'&',u'$',u'%',u'^',u'#',u'[',u']',u'(',u')',u'@',u'"',
u'/',u'\\',u'|',u'<',u'>',u'{',u'}',u'∘',u':',u'÷']

chars = None
with open(fontfile,'r') as f:
    data = ''.join(f.readlines())
    chars = [map(eval,s.split()) for s in data.split('-')]
print chars


