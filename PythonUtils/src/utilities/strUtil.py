'''
Created on 16 Dec 2018

@author: simon
'''
import re, string, itertools
from random import choice

def aliasCase(s):
    cc = camelCase(s)
    if startsWithNumeral(cc):
        cc = '_'+cc
    return cc[0].lower() if len(cc) == 1 else cc[0].lower()+cc[1:] if len(cc) > 1 else ''

def camelCase(s):
    return re.sub('\s+', ' ', re.sub('_', ' ', re.sub('-', ' ', s.lower()))).title().replace(' ', '')

def kebabCase(s):
    return re.sub('\s', '-', s.lower())

def underscoreCase(s):
    return re.sub('\s', '_', s.lower())

def literalCase(s):
    return re.sub('\s', '_', s.upper())

def titleCase(s):
    return re.sub('\s+', ' ', re.sub('_', ' ', re.sub('-', ' ', s.lower()))).title()

def sentenceCase(s):
    return re.sub('\s+', ' ', re.sub('_', ' ', re.sub('-', ' ', s.lower()))).capitalize()

_startsWithNumeral = re.compile('^[0-9]')
def startsWithNumeral(s):
    return _startsWithNumeral.match(s)

_SALT = string.digits + string.ascii_letters
def random(size, **kw):
    rnd = ''
    salt = kw.get('salt', _SALT)
    for _ in range(size):
        rnd += choice(salt)

    return rnd      

def ends_with_token(s, *tokens):
    for token in tokens:
        if len(s) >= len(token) and s[-len(token):] == token:
            return True
    return False
