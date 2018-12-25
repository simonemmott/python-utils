'''
Created on 25 Dec 2018

@author: simon
'''
import unittest, os
from utilities import pathUtil


class TestPathUtil(unittest.TestCase):


    def test_assure_dir(self):
        
        pathUtil.assureDir('paths/dir1')
        self.assertTrue(os.path.exists('paths/dir1'))

        pathUtil.assureDir('paths/dir1/child1')
        self.assertTrue(os.path.exists('paths/dir1/child1'))
        
        pathUtil.assureDir('paths/dir1')
        self.assertTrue(os.path.exists('paths/dir1/child1'))
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()