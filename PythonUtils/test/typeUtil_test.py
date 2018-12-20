'''
Created on 16 Dec 2018

@author: simon
'''
import unittest
from utilities import typeUtil
from classUtil_test import ClassA

class TestTypeUtil(unittest.TestCase):

        
    def test_is_primitive(self):
        
        a = ClassA()
        
        assert typeUtil.is_primitive(1)
        assert typeUtil.is_primitive(1.0)
        assert typeUtil.is_primitive(-1)
        assert typeUtil.is_primitive(-1.0)
        assert typeUtil.is_primitive('string')
        assert typeUtil.is_primitive(True)
        assert typeUtil.is_primitive(False)
        assert not typeUtil.is_primitive([1,2,3])
        assert not typeUtil.is_primitive((1,2,3))
        assert not typeUtil.is_primitive({'a':1, 'b':2, 'c':3})
        assert not typeUtil.is_primitive(a)
 
    def test_is_collection(self):
        
        a = ClassA()
        
        assert not typeUtil.is_collection(1)
        assert not typeUtil.is_collection(1.0)
        assert not typeUtil.is_collection(-1)
        assert not typeUtil.is_collection(-1.0)
        assert not typeUtil.is_collection('string')
        assert not typeUtil.is_collection(False)
        assert typeUtil.is_collection([1,2,3])
        assert typeUtil.is_collection((1,2,3))
        assert not typeUtil.is_collection({'a':1, 'b':2, 'c':3})
        assert not typeUtil.is_collection(a)
 
    def test_is_map(self):
        
        a = ClassA()
        
        assert not typeUtil.is_map(1)
        assert not typeUtil.is_map(1.0)
        assert not typeUtil.is_map(-1)
        assert not typeUtil.is_map(-1.0)
        assert not typeUtil.is_map('string')
        assert not typeUtil.is_map(False)
        assert not typeUtil.is_map([1,2,3])
        assert not typeUtil.is_map((1,2,3))
        assert typeUtil.is_map({'a':1, 'b':2, 'c':3})
        assert not typeUtil.is_map(a)
 
    def test_is_instance(self):
        
        a = ClassA()
        
        assert not typeUtil.is_instance(1)
        assert not typeUtil.is_instance(1.0)
        assert not typeUtil.is_instance(-1)
        assert not typeUtil.is_instance(-1.0)
        assert not typeUtil.is_instance('string')
        assert not typeUtil.is_instance(False)
        assert not typeUtil.is_instance([1,2,3])
        assert not typeUtil.is_instance((1,2,3))
        assert not typeUtil.is_instance({'a':1, 'b':2, 'c':3})
        assert typeUtil.is_instance(a)
 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAliasCase']
    unittest.main()