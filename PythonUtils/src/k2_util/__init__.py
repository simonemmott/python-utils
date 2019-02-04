
def Struct(*args, **kwargs):
    def init(self, *iargs, **ikwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)
        for i in range(len(iargs)):
            setattr(self, args[i], iargs[i])
        for k,v in ikwargs.items():
            setattr(self, k, v)

    name = kwargs.pop("name", "MyStruct")
    kwargs.update(dict((k, None) for k in args))
    return type(name, (object,), {'__init__': init, '__slots__': kwargs.keys()})

class FunctionBuilder(object):
    def __init__(self, name, attr):
        if attr == None:
            def func(self):
                return None
        else:
            if callable(attr):
                def func(self):
                    return attr()
            else:
                def func(self):
                    return attr  
        self.func = func
        

def Model(src, *attributes, **kw):
    
    class M():
        def __init__(self, src):
            self.attributes = {}
            self.__src__ = src
            
        def register(self, name, attr):
            self.attributes[name] = attr
            setattr(M, name, attr)
            
        def get(self, name):
            attr = self.attributes.get(name, None)
            if attr == None:
                return None
            else:
                return attr(self)
            
        def set(self, **kw):
            for key in kw.keys():
                val = kw.get(key)
                fb = FunctionBuilder(key, val)
                self.register(key, fb.func)
                    
            return self
    
    model = M(src)
    for name in attributes:
        if hasattr(src, name):
            attr = getattr(src, name)
            fb = FunctionBuilder(name, attr)
        elif hasattr(src, '_'+name):
            attr = getattr(src, '_'+name)
            fb = FunctionBuilder(name, attr)
        else:
            fb = FunctionBuilder(name, None)
        model.register(name, fb.func)
                    
    return model.set(**kw)

class Indentable(object):
    def __init__(self, **kw):
        self._indent_str = kw.get('indent', '  ')
        self._indent = ''
        self._depth = 0
        
    def get_indent(self):
        return self._indent
    
    def depth(self):
        return self._depth
    
    def indent(self):
        self._depth += 1
        self._indent += self._indent_str
        
    def outdent(self):
        if self._depth > 0:
            self._depth -= 1
            self._indent = self._indent[:-len(self._indent_str)]


