# -*- coding:utf-8 -*-


def min_qty(form, field):

    if field.data <= 0:
        raise ValueError('Quantidade nao pode ser menor que zero')
