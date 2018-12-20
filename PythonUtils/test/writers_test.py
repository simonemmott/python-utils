'''
Created on 18 Dec 2018

@author: simon
'''
import unittest, os
from utilities.writers import StringWriter


class TestStringWriter(unittest.TestCase):


    def test_new_StringWriter(self):
        sw = StringWriter()
        assert sw is not None
        
    def test_write(self):
        sw = StringWriter()
        sw.write('Hello')
        sw.write(' ')
        sw.write('World')
        sw.write('!')
        assert sw.__str__() == 'Hello World!'
    
    def test_writerln(self):
        sw = StringWriter()
        sw.writeln('Hello')
        sw.writeln(' ')
        sw.writeln('World')
        sw.writeln('!')
        assert sw.__str__() == 'Hello{0} {0}World{0}!{0}'.format(os.linesep)
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()