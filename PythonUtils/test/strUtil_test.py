'''
Created on 16 Dec 2018

@author: simon
'''
import unittest, os
from utilities import strUtil


class TestStrUtil(unittest.TestCase):


    def test_alias_case(self):
        assert strUtil.aliasCase('This is a title') == 'thisIsATitle'
        assert strUtil.aliasCase('0 This is a title') == '_0ThisIsATitle'

    def test_camel_case(self):
        assert strUtil.camelCase('This is a title') == 'ThisIsATitle'

    def test_kebab_case(self):
        assert strUtil.kebabCase('This is a title') == 'this-is-a-title'

    def test_underscore_case(self):
        assert strUtil.underscoreCase('This is a title') == 'this_is_a_title'

    def test_literal_lase(self):
        assert strUtil.literalCase('This is a title') == 'THIS_IS_A_TITLE'

    def test_title_case(self):
        assert strUtil.titleCase('this_is_a_title') == 'This Is A Title'

    def test_sentence_case(self):
        assert strUtil.sentenceCase('this_is_a_title') == 'This is a title'
        
    def test_random_string(self):
        assert len(strUtil.random(10)) == 10
        
    def test_ends_with_token(self):
        assert not strUtil.ends_with_token('aabbccdd', 'aa', 'bb', 'cc')
        assert strUtil.ends_with_token('aabbccdd', 'aa', 'bb', 'cc', 'dd')
        
class TestStrTokens(unittest.TestCase):
    
    def test_list_tokens(self):
        lst = strUtil.list_env_tokens('AAA${XXX}BBB${YYY}DDDD')
        self.assertEqual(['${YYY}', '${XXX}'], lst)
        
    def test_env_replace(self):
        xxx = os.getenv('XXX', '')
        yyy = os.getenv('YYY', '')
        
        self.assertEqual('AAA%sBBB%sDDDD'%(xxx,yyy), strUtil.env_replace('AAA${XXX}BBB${YYY}DDDD'))
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAliasCase']
    unittest.main()