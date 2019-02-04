'''
Created on 16 Dec 2018

@author: simon
'''
def is_float(v):
    try:
        num = float(v)
    except ValueError:
        return False
    return True

def is_int(v):
    try:
        num = int(v)
    except ValueError:
        return False
    return True
    

    