'''
Created on 20 Jan 2019

@author: simon
'''
import imp
import os
MODULE_EXTENSIONS = ('.py', '.pyc', '.pyo')

def package_contents(package):
    
    if not package.__file__:
        raise ImportError('Not a package: %r', package.__name__)
    # Use a set because some may be both source and compiled.
    return set([os.path.splitext(module)[0]
        for module in os.listdir(package.__file__[:-12])
        if module.endswith(MODULE_EXTENSIONS)])
    