import os
from utilities import Indentable

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
    
class IndentableWriter(Indentable):
    def __init__(self, writer, **kw):
        Indentable.__init__(self, **kw)
        self._writer = writer
        self._last_char = ''
        
    def write(self, *args, **kw):
        for arg in args:
            if self._last_char == '\n':
                self._writer.write(self.get_indent())
            if len(arg) > 1:
                self._writer.write(arg[:-1].replace('\n', '\n'+self.get_indent()))
            self._last_char = arg[-1]
            self._writer.write(self._last_char)
            
    