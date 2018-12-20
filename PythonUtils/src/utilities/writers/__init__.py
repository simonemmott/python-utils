import os

class Writer(object):
    def __init__(self):
        pass
    
    def write(self, *s):
        pass
    
    def writeln(self, *s):
        self.write(*s)
        self._buff += os.linesep
        
    def flush(self):
        pass
        
    def close(self):
        pass

class StringWriter(Writer):
    def __init__(self, **kw):
        self._buff = ''
        
    def write(self, *s):
        for a in s:
            self._buff += a
            
    def __str__(self):
        return self._buff
            
    