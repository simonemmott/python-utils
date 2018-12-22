'''
Created on 18 Dec 2018

@author: simon
'''
import unittest, os
from utilities.readers import StringReader


class TestStringReader(unittest.TestCase):


    def test_new_StringReader(self):
        sr = StringReader('0123456789ABCDEF')
        assert sr is not None
        assert sr.__str__() == '0123456789ABCDEF'
        
    def test_read_chars(self):
        sr = StringReader('0123456789ABCDEF')
        
        assert sr._read_chars(3) == '012'
        assert sr._read_chars(3) == '345'
        assert sr._read_chars(0) == ''
        assert sr._read_chars(5) == '6789A'
        assert sr._read_chars(8) == 'BCDEF'
        assert sr._read_chars(0) == None
        assert sr._read_chars(1) == None
        
    def test_read(self):
        sr = StringReader('0123456789ABCDEF')
        
        assert sr.read(3) == '012'
        assert sr.read(3) == '345'
        assert sr.read(0) == ''
        assert sr.read(5) == '6789A'
        assert sr.read(8) == 'BCDEF'
        assert sr.read(0) == None
        assert sr.read(1) == None
        
    
    def test_read_chars_starting_at(self):
        sr = StringReader('0123456789ABCDEF', start_at=4)
        
        assert sr._read_chars(3) == '456'
        assert sr._read_chars(5) == '789AB'
        assert sr._read_chars(8) == 'CDEF'
        assert sr._read_chars(0) == None
        assert sr._read_chars(1) == None
    
    def test_read_until_char(self):
        sr = StringReader('0123456789ABCDEF')
        
        assert sr._read_until('4') == '01234'
        assert sr._read_until('A') == '56789A'
        assert sr._read_until('X') == 'BCDEF'
        assert sr._read_until('X') == None
    
    def test_read_until_token(self):
        sr = StringReader('0123456789ABCDEF')
        
        assert sr._read_until('56') == '0123456'
        assert sr._read_until('A') == '789A'
        assert sr._read_until('CDE') == 'BCDE'
        assert sr._read_until('X') == 'F'
    
    def test_read_until_tokens(self):
        sr = StringReader('0123456789ABCDEF')
        
        assert sr._read_until('56', '45') == '012345'
        assert sr._read_until('A', 'D') == '6789A'
    
    def test_read_until_max_chars(self):
        sr = StringReader('0123456789ABCDEF')
        
        assert sr._read_until('4', max_chars=3) == '012'
        assert sr._read_until('A') == '3456789A'
        assert sr._read_until('X') == 'BCDEF'
        assert sr._read_until('X') == None
    
    def test_peek_chars(self):
        sr = StringReader('0123456789ABCDEF', start_at=6)
        
        assert sr._peek_chars(4) == '6789'
        assert sr._peek_chars(6) == '6789AB'
        assert sr._peek_chars(1) == '6'
        assert sr._peek_chars(1000) == '6789ABCDEF'
    
    def test_peek_until_char(self):
        sr = StringReader('0123456789ABCDEF', start_at=6)
        
        assert sr._peek_until('4') == '6789ABCDEF'
        assert sr._peek_until('A') == '6789A'
    
    def test_peek_until_char_max_chars(self):
        sr = StringReader('0123456789ABCDEF', start_at=6)
        
        assert sr._peek_until('4', max_chars=4) == '6789'
        assert sr._peek_until('A', max_chars=6) == '6789A'
        assert sr._peek_until('A', max_chars=3) == '678'
    
    def test_peek_until_token(self):
        sr = StringReader('0123456789ABCDEF', start_at=3)
        
        assert sr._peek_until('56') == '3456'
        assert sr._peek_until('A') == '3456789A'
    
    def test_readln(self):
        sr = StringReader('0123456789ABCDEF\nAAA\rBBB\n\rCCC\r\nDDD\n\nFFF\r\rGGG\nHHH')
        
        assert sr.readln() == '0123456789ABCDEF'
        assert sr.readln() == 'AAA'
        assert sr.readln() == 'BBB'
        assert sr.readln() == 'CCC'
        assert sr.readln() == 'DDD'
        assert sr.readln() == ''
        assert sr.readln() == 'FFF'
        assert sr.readln() == ''
        assert sr.readln() == 'GGG'
        assert sr.readln() == 'HHH'
        assert sr.readln() == None
    
    def test_read(self):
        sr = StringReader('0123456789ABCDEF', start_at=6)
        assert sr.read(chars=4, peek=True) == '6789'
        assert sr.read(chars=4) == '6789'

        sr = StringReader('0123456789ABCDEF', start_at=6)
        assert sr.read(until='A', peek=True) == '6789A'
        assert sr.read(until='A') == '6789A'

        sr = StringReader('0123456789ABCDEF', start_at=6)
        assert sr.read(until='A', max_chars=3, peek=True) == '678'
        assert sr.read(until='A', max_chars=3) == '678'

    def test_read2(self):
        sr = StringReader('0123456789ABCDEF', start_at=6)
        assert sr._peek_until('A', '9') == '6789'
        assert sr._read_until('A', '9') == '6789'


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()