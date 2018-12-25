'''
Created on 22 Dec 2018

@author: simon
'''
import unittest
from utilities import Model, Struct, Indentable

class TestClassA(object):
    def __init__(self, **kw):
        self._attr1 = kw.get('attr1', None)
        self._attr2 = kw.get('attr2', None)
        self._attr3 = kw.get('attr3', None)
        self._attr4 = kw.get('attr4', None)
        
    def attr1(self, *args):
        if len(args) > 0:
            self._attr1 = args[0]
        return self._attr1

    def attr2(self, *args):
        if len(args) > 0:
            self._attr2 = args[0]
        return self._attr2
    
    def attr3(self, *args):
        if len(args) > 0:
            self._attr3 = args[0]
        return self._attr3

class TestClassB(object):
    def __init__(self, **kw):
        self._attr1 = kw.get('attr1', None)
        self._attr2 = kw.get('attr2', None)
        self._attr3 = kw.get('attr3', None)
        self._attr4 = kw.get('attr4', None)
        
    def attr1(self, *args):
        if len(args) > 0:
            self._attr1 = args[0]
        return self._attr1

    def attr2(self, *args):
        if len(args) > 0:
            self._attr2 = args[0]
        return self._attr2
    
    def attr3(self, *args):
        if len(args) > 0:
            self._attr3 = args[0]
        return self._attr3

    
class TestStruct(unittest.TestCase):
    
    def test_new_struct(self):
        Test = Struct('aaa', 'bbb', name='MyTest')
        test = Test(aaa='AAA', bbb='BBB')
        self.assertTrue(hasattr(test, 'aaa'))
        self.assertEqual('AAA', test.aaa)
        self.assertTrue(hasattr(test, 'bbb'))
        self.assertEqual('BBB', test.bbb)

                 

class TestModel(unittest.TestCase):

    def test_model(self):
                
        testA = TestClassA(attr1='a1', attr2='a2', attr3='a3', attr4='a4')
        testB = TestClassB(attr1='b1', attr2='b2', attr3='b3', attr4='b4')
                
        mA = Model(testA, 'attr1', 'attr2', 'attr3', 'attr4', 'attr5')
        mB = Model(testB, 'attr1', 'attr2', 'attr3', 'attr4', 'attr5')
                
        self.assertTrue(hasattr(mA, 'attr1'))
        self.assertEqual('a1', mA.attr1())
        self.assertEqual('a1', mA.get('attr1'))
        self.assertTrue(hasattr(mA, 'attr2'))
        self.assertEqual('a2', mA.attr2())
        self.assertEqual('a2', mA.get('attr2'))
        self.assertTrue(hasattr(mA, 'attr3'))
        self.assertEqual('a3', mA.attr3())
        self.assertEqual('a3', mA.get('attr3'))
        self.assertTrue(hasattr(mA, 'attr4'))
        self.assertEqual('a4', mA.attr4())
        self.assertEqual('a4', mA.get('attr4'))
        self.assertTrue(hasattr(mA, 'attr5'))
        self.assertEqual(None, mA.attr5())
        self.assertEqual(None, mA.get('attr5'))

        self.assertTrue(hasattr(mB, 'attr4'))
        self.assertEqual('b1', mB.attr1())
        self.assertTrue(hasattr(mB, 'attr2'))
        self.assertEqual('b2', mB.attr2())
        self.assertTrue(hasattr(mB, 'attr3'))
        self.assertEqual('b3', mB.attr3())
        self.assertTrue(hasattr(mB, 'attr4'))
        self.assertEqual('b4', mB.attr4())
        self.assertTrue(hasattr(mB, 'attr5'))
        self.assertEqual(None, mB.attr5())
        
    def test_model_set(self):
        
        testA = TestClassA(attr1='a1', attr2='a2', attr3='a3', attr4='a4')
        mA = Model(testA, 'attr1', 'attr2', 'attr3', 'attr4', 'attr5').set(attr2='A2', attr3='A3')

        self.assertTrue(hasattr(mA, 'attr1'))
        self.assertEqual('a1', mA.attr1())
        self.assertEqual('a1', mA.get('attr1'))
        self.assertTrue(hasattr(mA, 'attr2'))
        self.assertEqual('A2', mA.attr2())
        self.assertEqual('A2', mA.get('attr2'))
        self.assertTrue(hasattr(mA, 'attr3'))
        self.assertEqual('A3', mA.attr3())
        self.assertEqual('A3', mA.get('attr3'))
        self.assertTrue(hasattr(mA, 'attr4'))
        self.assertEqual('a4', mA.attr4())
        self.assertEqual('a4', mA.get('attr4'))
        self.assertTrue(hasattr(mA, 'attr5'))
        self.assertEqual(None, mA.attr5())
        self.assertEqual(None, mA.get('attr5'))

    def test_model_set_inline(self):
        
        testA = TestClassA(attr1='a1', attr2='a2', attr3='a3', attr4='a4')
        mA = Model(testA, 'attr1', 'attr2', 'attr3', 'attr4', 'attr5', attr2='A2', attr3='A3')

        self.assertTrue(hasattr(mA, 'attr1'))
        self.assertEqual('a1', mA.attr1())
        self.assertEqual('a1', mA.get('attr1'))
        self.assertTrue(hasattr(mA, 'attr2'))
        self.assertEqual('A2', mA.attr2())
        self.assertEqual('A2', mA.get('attr2'))
        self.assertTrue(hasattr(mA, 'attr3'))
        self.assertEqual('A3', mA.attr3())
        self.assertEqual('A3', mA.get('attr3'))
        self.assertTrue(hasattr(mA, 'attr4'))
        self.assertEqual('a4', mA.attr4())
        self.assertEqual('a4', mA.get('attr4'))
        self.assertTrue(hasattr(mA, 'attr5'))
        self.assertEqual(None, mA.attr5())
        self.assertEqual(None, mA.get('attr5'))

class TestIndentable(unittest.TestCase):
    
    def test_indentable(self):
        i = Indentable()    
        
        self.assertEqual('', i.get_indent())  
        self.assertEqual(0, i.depth())
        
        i.indent()
        self.assertEqual('  ', i.get_indent())  
        self.assertEqual(1, i.depth())
        
        i.indent()
        self.assertEqual('    ', i.get_indent())  
        self.assertEqual(2, i.depth())

        i.indent()
        self.assertEqual('      ', i.get_indent())  
        self.assertEqual(3, i.depth())

        i.outdent()
        self.assertEqual('    ', i.get_indent())  
        self.assertEqual(2, i.depth())

        i.outdent()
        self.assertEqual('  ', i.get_indent())  
        self.assertEqual(1, i.depth())

        i.outdent()
        self.assertEqual(0, i.depth())
        self.assertEqual('', i.get_indent())  

        i.outdent()
        self.assertEqual('', i.get_indent())  
        self.assertEqual(0, i.depth())
                 



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()