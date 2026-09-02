import os.path
import sys
print(__file__)
sys.path.insert(0, os.path.dirname(__file__))

import import_ipynb

def test1():
    import B
    print(repr(B))
    assert "module 'B'" or "name='B'" in repr(B)
    assert B.b(2, 3) == 5

def test2():
    from B import b
    assert b(2, 3) == 5

def test3():
    import B
    assert B.b(2, 3) == 5

    import importlib
    importlib.reload(B)

    assert B.b(2, 3) == 5

def test4():
    import subdir.C
    assert subdir.C.c(2,3) == 5

def test5():
    from subdir.C import c
    assert c(2, 3) == 5
