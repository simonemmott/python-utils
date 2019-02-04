'''
Created on 25 Dec 2018

@author: simon
'''
import os

def assureDir(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            return
        else:
            raise FileExistsError('The given path %s exists and is not a directory')
    else:
        os.makedirs(path)