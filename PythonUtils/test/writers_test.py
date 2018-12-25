'''
Created on 18 Dec 2018

@author: simon
'''
import unittest, os
from utilities.writers import StringWriter, IndentableWriter


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
    
    
class TestIndentableWriter(unittest.TestCase):
    
    def test_indentable_writer(self):
        sw = StringWriter()
        iw = IndentableWriter(sw)
        
        iw.write('aaa')
        iw.write('bbb')
        iw.write('ccc')
        
        self.assertEqual('aaabbbccc', sw.__str__())
        
    def test_indentable_writer_lines(self):
        sw = StringWriter()
        iw = IndentableWriter(sw)
        
        iw.write('aaa\n')
        iw.write('bbb\n')
        iw.write('ccc\n')
        
        self.assertEqual('aaa\nbbb\nccc\n', sw.__str__())
        
    def test_indentable_writer_indented_lines(self):
        sw = StringWriter()
        iw = IndentableWriter(sw)
        
        iw.write('aaa\n')
        iw.indent()
        iw.write('bbb\n')
        iw.indent()
        iw.write('ccc\n')
        iw.outdent()
        iw.write('ddd\n')
        iw.outdent()
        iw.write('eee\n')
        
        ex = StringWriter()
        ex.write('aaa\n')
        ex.write('  bbb\n')
        ex.write('    ccc\n')
        ex.write('  ddd\n')
        ex.write('eee\n')
         
        self.assertEqual(ex.__str__(), sw.__str__())
        
    def test_indentable_writer_indented_lines_2(self):
        sw = StringWriter()
        iw = IndentableWriter(sw)
        
        iw.write('aaa\nAAA')
        iw.write('ZZZ\n')
        iw.indent()
        iw.write('bbb\nBBB')
        iw.write('YYY\n')
        iw.indent()
        iw.write('ccc\nCCC')
        iw.write('XXX\n')
        iw.outdent()
        iw.write('ddd\nDDD')
        iw.write('WWW\n')
        iw.outdent()
        iw.write('eee\nEEE')
        iw.write('VVV\n')
        
        ex = StringWriter()
        ex.write('aaa\n')
        ex.write('AAAZZZ\n')
        ex.write('  bbb\n')
        ex.write('  BBBYYY\n')
        ex.write('    ccc\n')
        ex.write('    CCCXXX\n')
        ex.write('  ddd\n')
        ex.write('  DDDWWW\n')
        ex.write('eee\n')
        ex.write('EEEVVV\n')
         
        self.assertEqual(ex.__str__(), sw.__str__())
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()