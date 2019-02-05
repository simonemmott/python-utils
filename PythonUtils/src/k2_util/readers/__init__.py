import os
from k2_util import strUtil

class Reader(object):
    def __init__(self):
        pass
    
    def read(self, **kw):
        pass
    
    def readln(self, *s):
        self.write(*s)
        self._buff += os.linesep
        
    def close(self):
        pass

class StringReader(Reader):
    def __init__(self, buff, **kw):
        self._buff = buff
        self._index = kw.get('start_at', 0)
        
    def _read_chars(self, nchars):
        if nchars < 0:
            raise ValueError('Unable to read backwards! The number of characters to read (%d) must be >= 0' % nchars)
        if self._index >= len(self._buff):
            return None
        elif self._index+nchars <= len(self._buff):
            rval = self._buff[self._index:self._index+nchars]
            self._index += nchars
        else:
            rval = self._buff[self._index:]
            self._index = len(self._buff)
        return rval
    
    def _read_until(self, *tokens, **kw):
        max_chars = kw.get('max_chars', None)
        rval = ''
        if max_chars != None and max_chars < 0:
            raise ValueError('Unable to read backwards! The maximum number of characters to read (%d) must be >= 0' % max_chars)
        c = self._read_chars(1)
        if c == None:
            return
        rval += c
#        while rval[-len(token):] != token and c != None:
        while not strUtil.ends_with_token(rval, *tokens) and c != None:
            if max_chars != None and len(rval) >= max_chars:
                return rval
            c = self._read_chars(1)
            if c != None:
                rval += c
        return rval
    
    def _peek_chars(self, nchars):
        if nchars < 0:
            raise ValueError('Unable to read backwards! The number of characters to read (%d) must be >= 0' % nchars)
        if self._index >= len(self._buff):
            return None
        elif self._index+nchars <= len(self._buff):
            rval = self._buff[self._index:self._index+nchars]
        else:
            rval = self._buff[self._index:]
        return rval
    
    def _peek_until(self, *tokens, **kw):
        max_chars = kw.get('max_chars', None)
        if max_chars != None and max_chars < 0:
            raise ValueError('Unable to read backwards! The maximum number of characters to read (%d) must be >= 0' % max_chars)
        if max_chars != None and max_chars == 0:
            return ''
        i=1
        rval = self._peek_chars(i)
        if rval == None:
            return None
#        while rval[-len(token):] != token and self._index + i < len(self._buff):
        while not strUtil.ends_with_token(rval, *tokens) and self._index + i < len(self._buff):
            if max_chars != None and i >= max_chars:
                return rval
            i += 1
            rval = self._peek_chars(i)
        return rval
    
    def readln(self):
        if self._index >= len(self._buff):
            return None
        line = ''
        c = self._read_chars(1)
        while  c != None:
            if c != '\n' and c != '\r':
                line += c
            else:
                if c == '\n' and self._peek_chars(1) == '\r':
                    self._read_chars(1)
                elif c == '\r' and self._peek_chars(1) == '\n':
                    self._read_chars(1)
                return line 
            c = self._read_chars(1)           
        return line
            
        
    def read(self, *args, **kw):
        if len(args) > 0:
            return self._read_chars(args[0])
        if kw.get('chars'):
            if kw.get('peek'):
                return self._peek_chars(kw.get('chars'))
            else:
                return self._read_chars(kw.get('chars'))
        if kw.get('until'):
            if kw.get('peek'):
                if kw.get('max_chars'):
                    return self._peek_until(kw.get('until'), max_chars=kw.get('max_chars'))
                else:
                    return self._peek_until(kw.get('until'))
            else:
                if kw.get('max_chars'):
                    return self._read_until(kw.get('until'), max_chars=kw.get('max_chars'))
                else:
                    return self._read_until(kw.get('until'))
            
    def __str__(self):
        return self._buff
            
