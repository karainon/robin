#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from enum import Enum


def compare_speed(fn1, fn2, times):
    start = datetime.now()
    for i in range(times):
        fn1()
    end = datetime.now()
    print("fn1", end - start)

    start = datetime.now()
    for i in range(times):
        fn2()
    end = datetime.now()
    print("fn2", end - start)


def test_enum():
    class E(Enum):
        a = 'aaa'
        b = 2
        c = 3

    e = E.a
    print(e == 'aaa')


def test_fstr():
    import dis

    def fstring():
        a = None
        b = 2
        return f'a:{a}, b:{b}'

    dis.dis(fstring)


def test_logging():
    import logging
    logging.basicConfig(level=logging.ERROR)
    logging.debug('asdfsaf')
    logging.info('asdfsaf')
    logging.warning('asdfsaf')
    logging.error('asdfsaf')


if __name__ == '__main__':
    import tokenize, token

    # a = 'a\n    b\nc\rd\r\ne'
    # print(a.splitlines(keepends=True))
    # test_fstr()
    # test_func()
    #  test_logging()
    a = 1
    while a <= 4:
        print(a)
        a += 1
    else:
        print('else', a)

    print(type(NotImplemented))
