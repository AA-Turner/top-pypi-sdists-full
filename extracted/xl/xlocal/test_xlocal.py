
from __future__ import with_statement

import pytest

@pytest.fixture
def xlocal(request):
    import xlocal
    return xlocal.xlocal()

def test_scoping(xlocal):
    def f():
        assert xlocal.x == 3

    with xlocal(x=3):
        f()
    assert not hasattr(xlocal, "x")
    assert not xlocal._storage # no garbage

def test_stacking(xlocal):
    def f():
        assert xlocal.x == 3

    with xlocal(x=5):
        assert xlocal.x == 5
        with xlocal(x=3):
            assert xlocal.x == 3
        assert xlocal.x == 5
    assert not hasattr(xlocal, "x")

def test_nodelset(xlocal):
    with xlocal(y=3):
        assert xlocal.y == 3
        pytest.raises(AttributeError, lambda: delattr(xlocal, "y"))
    assert not hasattr(xlocal, "y")
    pytest.raises(AttributeError, lambda: setattr(xlocal, "x", None))

