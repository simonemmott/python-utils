'''
Created on 16 Dec 2018

@author: simon
'''
import re, string, itertools, os
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

RE_ENV_TOKEN = re.compile(".*(\$\{.+\}).*")

def list_env_tokens(s):
    _s = s
    lst = []
    m = RE_ENV_TOKEN.match(_s)
    while(m):
        var = m.group(1)
        lst.append(var)
        _s = _s.replace(var, '')
        m = RE_ENV_TOKEN.match(_s)
    return lst
    
def env_replace(s):
    for token in list_env_tokens(s):
        env_key=token[2:-1]
        val = os.getenv(env_key, '')
        s = s.replace(token, val)
    return s
        
        
