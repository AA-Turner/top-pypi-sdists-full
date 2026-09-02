#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

def test():
    import bunch_py3
    import doctest
    returned = doctest.testmod(bunch_py3)
    return returned.failed

if __name__ == '__main__':
    sys.exit(test())
