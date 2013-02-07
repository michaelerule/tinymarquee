#!/usr/bin/env python
# -*- coding: utf-8 -*-

fontfile = 'marquee_font.txt'
# Load the font information
mapping = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890., ;:-+=?!\'*^[♥&$'
chars = None
with open(fontfile,'r') as f:
    data = ''.join(f.readlines())
    chars = [map(eval,s.split()) for s in data.split('-')]
print chars


