# -*- coding: utf-8 -*-


def encode(x=''):
    '''Return encoded string'''
    x = x if isinstance(x, str) else ''

    return x.encode('utf-8')
