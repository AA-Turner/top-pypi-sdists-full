from importlib import import_module

import pytest


def test_populate_all(example):
    example("""\
from public import populate_all

def foo():
    pass

class Foo:
    pass

fooint: int = 7
foostr: str = 'hello'

# This isn't public.
_foobool: bool = True

populate_all()
""")
    module = import_module('example')
    assert module.__all__ == ['foo', 'Foo', 'fooint', 'foostr']


def test_populate_all_preserves_all(example):
    example("""\
from public import populate_all

__all__ = ['missing']

def foo():
    pass

populate_all()
""")
    module = import_module('example')
    assert module.__all__ == ['missing', 'foo']


def test_populate_all_skips_duplicates(example):
    example("""\
from public import populate_all

__all__ = ['foo']

def foo():
    pass

populate_all()
""")
    module = import_module('example')
    assert module.__all__ == ['foo']


def test_populate_all_skips_decorated_duplicates(example):
    example("""\
from public import populate_all, public

@public
def foo():
    pass

populate_all()
""")
    module = import_module('example')
    assert module.__all__ == ['foo']


def test_populate_all_skips_modules(example):
    example("""\
import public

public.populate_all()
""")
    module = import_module('example')
    assert module.__all__ == []


def test_populate_all_noop_unsupported_getmodule(example, monkeypatch):
    # inspect.getmodule() is documented as possibly returning None, and the code is prepared for
    # that, but I don't know under what circumstances that can occur, so just monkeypatch the
    # function for full coverage.
    #
    # https://docs.python.org/3/library/inspect.html#inspect.getmodule
    monkeypatch.setattr('inspect.getmodule', lambda *_: None)
    example("""\
from public import populate_all

def foo():
    pass

populate_all()
""")
    module = import_module('example')
    # There will be no __all__ because it wasn't added explicitly, and nothing could be inferred
    # because of the monkey patch.
    assert not hasattr(module, '__all__')


# This can't pass because sys.abiflags is a string, for which inspect.getmodule() returns None.
@pytest.mark.xfail
def test_populate_all_gets_fooled(example):
    example("""\
from public import populate_all
from sys import abiflags

populate_all()
""")
    module = import_module('example')
    assert module.__all__ == []
