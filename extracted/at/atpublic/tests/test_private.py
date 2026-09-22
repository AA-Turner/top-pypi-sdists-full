import re

from importlib import import_module

import pytest


def test_atprivate_does_not_add_dunder_all(example):
    example("""\
from public import private

@private
def a_function():
    pass
""")
    module = import_module('example')
    assert not hasattr(module, '__all__')


def test_atprivate_with_dunder_all(example):
    example("""\
from public import private

__all__ = ['a_function']

@private
def a_function():
    pass
""")
    module = import_module('example')
    assert 'a_function' not in module.__all__


def test_private_does_not_add_dunder_all(example):
    # This looks like a duplicate of test_atprivate_does_not_add_dunder_all above, and
    # both should be kept.  The two forms reach the same answer by different routes
    # through resolve_name().  When the decorator runs, the function it decorates is not
    # bound in the module globals yet, so the name has to be resolved from the object's
    # __module__.  Here AClass is already bound by the time private() is called, so the
    # name is found directly in the globals instead.
    example("""\
from public import private

class AClass:
    pass

private(AClass)
""")
    module = import_module('example')
    assert not hasattr(module, '__all__')


def test_all_is_a_tuple(example):
    example("""\
__all__ = ('foo',)

from public import private

def foo():
    pass

@private
def bar():
    pass
""")
    with pytest.raises(
        TypeError,
        match=re.escape("__all__ must be a list not: <class 'tuple'>"),
    ):
        import_module('example')


# The single argument call form.

def test_single_argument_imported_object(example):
    example.module('bar', """\
class Foo:
    pass
""")
    example("""\
from public import private
from bar import Foo

__all__ = ['Foo']

private(Foo)
""")
    module = import_module('example')
    assert module.__all__ == []


def test_single_argument_leaves_source_module_alone(example):
    # private() used to remove the name from the __all__ of the module where the object was
    # defined, which is destructive to a module the caller doesn't own.
    example.module('bar', """\
from public import public

@public
class Foo:
    pass
""")
    example("""\
from public import private
from bar import Foo

__all__ = ['Foo']

private(Foo)
""")
    import_module('example')
    assert import_module('bar').__all__ == ['Foo']


def test_single_argument_import_alias(example):
    example.module('bar', """\
class Foo:
    pass
""")
    example("""\
from public import private
from bar import Foo as Baz

__all__ = ['Baz']

private(Baz)
""")
    module = import_module('example')
    assert module.__all__ == []


def test_single_argument_local_definition(example):
    example("""\
from public import private

class Foo:
    pass

__all__ = ['Foo']

private(Foo)
""")
    module = import_module('example')
    assert module.__all__ == []


def test_single_argument_submodule(example):
    example.module('pkg.sub')
    example("""\
from public import private
from pkg import sub

__all__ = ['sub']

private(sub)
""")
    module = import_module('example')
    assert module.__all__ == []


def test_single_argument_unbound_module(example):
    example("""\
from public import private
import xml.dom

private(xml.dom)
""")
    with pytest.raises(
        TypeError,
        match=re.escape('Module is not bound in the calling namespace: xml.dom'),
    ):
        import_module('example')


def test_single_argument_constant(example):
    example("""\
from public import private

private(7)
""")
    with pytest.raises(
        TypeError,
        match=re.escape(
            "Cannot infer a name from: <class 'int'>; use the keyword argument form"
        ),
    ):
        import_module('example')


def test_single_argument_all_is_a_tuple(example):
    # A non-list __all__ has to be rejected before any name resolution happens, otherwise
    # this could pass on the wrong TypeError.
    example("""\
__all__ = ('a',)

from public import private

class Foo:
    pass

private(Foo)
""")
    with pytest.raises(
        TypeError,
        match=re.escape("__all__ must be a list not: <class 'tuple'>"),
    ):
        import_module('example')


def test_single_argument_returns_thing(example):
    example.module('bar', """\
class Foo:
    pass
""")
    example("""\
from public import private
from bar import Foo

result = private(Foo)
""")
    module = import_module('example')
    assert module.result is module.Foo


# The string call form.

def test_string(example):
    example("""\
from public import private

__all__ = ['Tuba']

private('Tuba')
""")
    module = import_module('example')
    assert module.__all__ == []


def test_string_returns_the_string(example):
    example("""\
from public import private

result = private('Tuba')
""")
    module = import_module('example')
    assert module.result == 'Tuba'


def test_string_not_an_identifier(example):
    example("""\
from public import private

private('not an identifier')
""")
    with pytest.raises(
        ValueError,
        match=re.escape("Not a valid Python identifier: 'not an identifier'"),
    ):
        import_module('example')


def test_string_is_a_keyword(example):
    example("""\
from public import private

private('class')
""")
    with pytest.raises(
        ValueError,
        match=re.escape("Cannot use a Python keyword as a name: 'class'"),
    ):
        import_module('example')


def test_string_is_a_soft_keyword(example):
    example("""\
from public import private

__all__ = ['match']

private('match')
""")
    module = import_module('example')
    assert module.__all__ == []
