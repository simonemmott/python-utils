'''
Created on 16 Dec 2018

@author: simon
'''
from functools import wraps
from types import MethodType

def get_attributes(cls):
    return [member for member in dir(cls) if not member.startswith('__') and not callable(getattr(cls,member))]

def to_dict(obj):
    if obj == None:
        return obj
    if  isinstance(obj, str) or isinstance(obj, int) or isinstance(obj, float) or isinstance(obj, bool):
        return obj
    if isinstance(obj, list):
        l = []
        for item in obj:
            l.append(to_dict(item))
        return l
    if isinstance(obj, tuple):
        t = ()
        for item in obj:
            t = t + (to_dict(item),)
        return t
    if isinstance(obj, dict):
        d = {}
        for (attr, value) in obj.items():
            d[attr] = to_dict(value)
        return d
    d = {}
    for attr in get_attributes(obj):
        d[attr] = to_dict(getattr(obj, attr))
    return d

_primitives = (int, str, bool)
def is_primitive(obj):
    return False

_collections = (list,tuple)
def is_collection(obj):
    return False

_maps = (dict)
def is_map(obj):
    return False

def is_instance(obj):
    return False

def add_method(*classes):
    def decorator(func):
        for cls in classes:
            setattr(cls, func.__name__, func)
        return func 
    return decorator
