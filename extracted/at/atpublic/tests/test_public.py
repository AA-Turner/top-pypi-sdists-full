import re

from importlib import import_module

import pytest


def test_atpublic_function(example):
    example("""\
from public import public

@public
def a_function():
    pass
""")
    module = import_module('example')
    assert module.__all__ == ['a_function']


def test_atpublic_function_runnable(example):
    example("""\
from public import public

@public
def a_function():
    return 1
""")
    module = import_module('example')
    assert module.a_function() == 1


def test_atpublic_class(example):
    example("""\
from public import public

@public
class AClass:
    pass
""")
    module = import_module('example')
    assert module.__all__ == ['AClass']


def test_atpublic_class_runnable(example):
    example("""\
from public import public

@public
class AClass:
    pass
""")
    module = import_module('example')
    assert isinstance(module.AClass(), module.AClass)


def test_atpublic_two_things(example):
    example("""\
from public import public

@public
def foo():
    pass

@public
class AClass:
    pass
""")
    module = import_module('example')
    assert module.__all__ == ['foo', 'AClass']


def test_decorator_duplicate(example):
    example("""\
from public import public

@public
def foo():
    return 1

@public
def foo():
    return 2
""")
    module = import_module('example')
    assert module.__all__ == ['foo']


def test_function_call_duplicate(example):
    example("""\
from public import public

@public
def foo():
    return 1

public(foo=2)
""")
    module = import_module('example')
    assert module.__all__ == ['foo']


def test_atpublic_append_to_all(example):
    example("""\
__all__ = ['a', 'b']

a = 1
b = 2

from public import public

@public
def foo():
    pass

@public
class AClass:
    pass
""")
    module = import_module('example')
    assert module.__all__ == ['a', 'b', 'foo', 'AClass']


def test_atpublic_keywords(example):
    example("""\
from public import public

public(a=1, b=2)
""")
    module = import_module('example')
    assert sorted(module.__all__) == ['a', 'b']


def test_atpublic_keywords_multicall(example):
    example("""\
from public import public

public(b=1)
public(a=2)
""")
    module = import_module('example')
    assert module.__all__ == ['b', 'a']


def test_atpublic_keywords_global_bindings(example):
    example("""\
from public import public

public(a=1, b=2)
""")
    module = import_module('example')
    assert module.a == 1
    assert module.b == 2


def test_atpublic_mixnmatch(example):
    example("""\
__all__ = ['a', 'b']

a = 1
b = 2

from public import public

@public
def foo():
    pass

@public
class AClass:
    pass

public(c=3)
""")
    module = import_module('example')
    assert module.__all__ == ['a', 'b', 'foo', 'AClass', 'c']


def test_all_is_a_tuple(example):
    example("""\
__all__ = ('foo',)

from public import public

def foo():
    pass

@public
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
from public import public
from bar import Foo

public(Foo)
""")
    module = import_module('example')
    assert module.__all__ == ['Foo']


def test_single_argument_leaves_source_module_alone(example):
    example.module('bar', """\
class Foo:
    pass
""")
    example("""\
from public import public
from bar import Foo

public(Foo)
""")
    import_module('example')
    assert not hasattr(import_module('bar'), '__all__')


def test_single_argument_source_module_all_untouched(example):
    # The source module having no __all__ is the easy case.  When it has one of its own,
    # exporting a name imported from it must leave that __all__ exactly as it was.
    example.module('bar', """\
from public import public

@public
class Guitar:
    pass

class Foo:
    pass
""")
    example("""\
from public import public
from bar import Foo

public(Foo)
""")
    module = import_module('example')
    assert module.__all__ == ['Foo']
    assert import_module('bar').__all__ == ['Guitar']


def test_single_argument_import_alias(example):
    # The locally bound name is the one that has to work for `from example import *`, so
    # that's the one that gets exported.
    example.module('bar', """\
class Foo:
    pass
""")
    example("""\
from public import public
from bar import Foo as Baz

public(Baz)
""")
    module = import_module('example')
    assert module.__all__ == ['Baz']


def test_single_argument_local_definition(example):
    example("""\
from public import public

class Foo:
    pass

public(Foo)
""")
    module = import_module('example')
    assert module.__all__ == ['Foo']


def test_single_argument_local_alias(example):
    # Both names are bound to the same object and nothing records which spelling was typed,
    # so the name the object was defined with wins.  This asymmetry is documented.
    example("""\
from public import public

class Foo:
    pass

Bar = Foo

public(Bar)
""")
    module = import_module('example')
    assert module.__all__ == ['Foo']


def test_single_argument_submodule(example):
    example.module('pkg.sub')
    example("""\
from public import public
from pkg import sub

public(sub)
""")
    module = import_module('example')
    assert module.__all__ == ['sub']


def test_single_argument_submodule_import_as(example):
    example.module('pkg.sub')
    example("""\
from public import public
import pkg.sub as sub

public(sub)
""")
    module = import_module('example')
    assert module.__all__ == ['sub']


def test_single_argument_submodule_renamed(example):
    # A module's __name__ is dotted and can't be used directly, and here it doesn't even
    # match the name it's bound to.
    example.module('pkg.sub')
    example("""\
from public import public
import pkg.sub as elsewhere

public(elsewhere)
""")
    module = import_module('example')
    assert module.__all__ == ['elsewhere']


def test_single_argument_top_level_module(example):
    example("""\
from public import public
import os

public(os)
""")
    module = import_module('example')
    assert module.__all__ == ['os']


def test_single_argument_unbound_module(example):
    # `import xml.dom` binds only `xml`, so there's no name in the calling namespace to
    # export.
    example("""\
from public import public
import xml.dom

public(xml.dom)
""")
    with pytest.raises(
        TypeError,
        match=re.escape('Module is not bound in the calling namespace: xml.dom'),
    ):
        import_module('example')


def test_single_argument_constant(example):
    example("""\
from public import public

public(7)
""")
    with pytest.raises(
        TypeError,
        match=re.escape(
            "Cannot infer a name from: <class 'int'>; use the keyword argument form"
        ),
    ):
        import_module('example')


def test_single_argument_returns_thing(example):
    example.module('bar', """\
class Foo:
    pass
""")
    example("""\
from public import public
from bar import Foo

result = public(Foo)
""")
    module = import_module('example')
    assert module.result is module.Foo


def test_single_argument_duplicate(example):
    example("""\
from public import public

class Foo:
    pass

public(Foo)
public(Foo)
""")
    module = import_module('example')
    assert module.__all__ == ['Foo']


def test_single_argument_appends_to_all(example):
    example("""\
__all__ = ['a']

from public import public

class Foo:
    pass

public(Foo)
""")
    module = import_module('example')
    assert module.__all__ == ['a', 'Foo']


def test_single_argument_all_is_a_tuple(example):
    # A non-list __all__ has to be rejected before any name resolution happens, otherwise
    # this could pass on the wrong TypeError.
    example("""\
__all__ = ('a',)

from public import public

class Foo:
    pass

public(Foo)
""")
    with pytest.raises(
        TypeError,
        match=re.escape("__all__ must be a list not: <class 'tuple'>"),
    ):
        import_module('example')


# The string call form.

def test_string_returns_the_string(example):
    example("""\
from public import public

result = public('Tuba')
""")
    module = import_module('example')
    assert module.result == 'Tuba'


def test_string_need_not_be_bound(example):
    # A string is just a string; nothing checks it against the module's contents, so the
    # name doesn't have to exist at all.
    example("""\
from public import public

public('Tuba')
""")
    module = import_module('example')
    assert module.__all__ == ['Tuba']
    assert not hasattr(module, 'Tuba')


def test_string_duplicate(example):
    example("""\
from public import public

public('Tuba')
public('Tuba')
""")
    module = import_module('example')
    assert module.__all__ == ['Tuba']


def test_string_not_an_identifier(example):
    example("""\
from public import public

public('not an identifier')
""")
    with pytest.raises(
        ValueError,
        match=re.escape("Not a valid Python identifier: 'not an identifier'"),
    ):
        import_module('example')


def test_string_is_a_keyword(example):
    # A reserved word passes str.isidentifier(), but nothing can ever be bound to it.
    example("""\
from public import public

public('class')
""")
    with pytest.raises(
        ValueError,
        match=re.escape("Cannot use a Python keyword as a name: 'class'"),
    ):
        import_module('example')


def test_string_is_a_soft_keyword(example):
    # Soft keywords are ordinary names, so keyword.issoftkeyword() is not consulted.
    example("""\
from public import public

public('match')
""")
    module = import_module('example')
    assert module.__all__ == ['match']


def test_string_dynamically_bound_names(example):
    example("""\
from public import public

orchestra = {'Bassoon': dict, 'Flute': list}

for name, factory in orchestra.items():
    globals()[name] = factory()
    public(name)
""")
    module = import_module('example')
    assert module.__all__ == ['Bassoon', 'Flute']
