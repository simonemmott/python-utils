'''
Created on 16 Dec 2018

@author: simon
'''
import unittest
from utilities import classUtil
import json

class ClassA(object):
    
    _name = None
    _description = None
    
    def __init__(self, **kw):
        self._name = kw.get('name', self._name)
        self._description = kw.get('description', self._description)

class ClassB(ClassA):
    
    _title = None
    
    def __init__(self, **kw):
        ClassA.__init__(self, **kw)
        self._title = kw.get('title', self._title)

class ClassC(ClassA):
    
    _a = None
    _bs = None
    _d = None
    
    def __init__(self, **kw):
        ClassA.__init__(self, **kw)
        self._a = kw.get('a', self._a)
        self._bs = kw.get('bs', self._bs)
        self._d = kw.get('d', self._d)

class TestClassUtil(unittest.TestCase):


    def test_get_attributes(self):
        
        assert len(classUtil.get_attributes(ClassA)) == 2
        assert '_name' in classUtil.get_attributes(ClassA)
        assert '_description' in classUtil.get_attributes(ClassA)
        assert len(classUtil.get_attributes(ClassB)) == 3
        assert '_name' in classUtil.get_attributes(ClassB)
        assert '_description' in classUtil.get_attributes(ClassB)
        assert '_title' in classUtil.get_attributes(ClassB)
        
    def test_to_dict(self):
        
        a = ClassA(name='Fred', description='caveman')
        d = classUtil.to_dict(a)
        
        assert d['_name'] == 'Fred'
        assert d['_description'] == 'caveman'

        b1 = ClassB(name='Fred', description='caveman', title='Mr')
        b2 = ClassB(name='Wilma', description='cavewoman', title='Mrs')
        d = classUtil.to_dict(b1)
        
        assert d['_name'] == 'Fred'
        assert d['_description'] == 'caveman'
        assert d['_title'] == 'Mr'

        c = ClassC(name='Flintstones', description='A family of cavemen', a=a, bs=[b1,b2], d={'b1': b1, 'b2': b2})
        d = classUtil.to_dict(c)
        
        assert d['_name'] == 'Flintstones'
        assert d['_description'] == 'A family of cavemen'
        assert d['_a']['_name'] == 'Fred'
        assert d['_a']['_description'] == 'caveman'
        assert d['_bs'][0]['_name'] == 'Fred'
        assert d['_bs'][0]['_description'] == 'caveman'
        assert d['_bs'][0]['_title'] == 'Mr'
        assert d['_bs'][1]['_name'] == 'Wilma'
        assert d['_bs'][1]['_description'] == 'cavewoman'
        assert d['_bs'][1]['_title'] == 'Mrs'
        assert d['_d']['b1']['_name'] == 'Fred'
        assert d['_d']['b1']['_description'] == 'caveman'
        assert d['_d']['b1']['_title'] == 'Mr'
        assert d['_d']['b2']['_name'] == 'Wilma'
        assert d['_d']['b2']['_description'] == 'cavewoman'
        assert d['_d']['b2']['_title'] == 'Mrs'
        
        d = classUtil.to_dict(None)
        assert d == None
        
    def test_add_method(self):
        b = ClassB(name='Fred', description='caveman', title='Dr')
        c = ClassC(name='Fred', description='caveman')
        
        @classUtil.add_method(ClassB, ClassC)
        def foo(self):
            return 'Hello %s' % (('%s %s' % (self._title, self._name)) if hasattr(self, '_title') and hasattr(self, '_name') else self._name if hasattr(self, '_name') else 'world')

        @classUtil.add_method(ClassB, ClassC)
        def bar(self, msg):
            return self._name+' says: '+msg
            
        assert b.foo() == 'Hello Dr Fred'
        assert b.bar('humbug') == 'Fred says: humbug'
        assert c.foo() == 'Hello Fred'
        assert c.bar('fish') == 'Fred says: fish'
 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAliasCase']
    unittest.main()