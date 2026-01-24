
REPR_TEMPLATE = """
def __repr__(self):
    return '{}({})' % ({})
"""

def auto_repr(cls):
    """Generates a `__repr__` method for the given class, using `__slots__`.

    >>> @auto_repr
    ... class Foo(object):
    ...     __slots__ = ['bar']
    ...     def __init__(self, bar):
    ...         self.bar = bar

    >>> Foo(0)
    Foo(bar=0)
    """
    slots = cls.__slots__
    repr_slots = ', '.join('{}=%r'.format(attr) for attr in slots)
    repr_values = ', '.join('self.' + attr for attr in slots)
    repr_def = REPR_TEMPLATE.format(cls.__name__, repr_slots, repr_values)
    namespace = dict(__name__='auto_repr_%s' % cls.__name__)
    exec(repr_def, namespace)
    cls.__repr__ = namespace['__repr__']
    try:
        cls.__repr__._source = repr_def
    except AttributeError:
        pass
    return cls


class Constant(object):
    """A simple class that creates lightweight constants.

    >>> c = Constant('OK')
    >>> c
    OK
    >>> c.name
    'OK'
    >>> c == c
    True

    >>> c.name = 'KO'
    Traceback (most recent call last):
    ...
    AttributeError: constants cannot be modified

    >>> c2 = Constant('OK')
    >>> c2 == c
    False
    """

    __slots__ = 'name'

    def __init__(self, name):
        object.__setattr__(self, 'name', name)

    def __repr__(self):
        return self.name

    def __setattr__(self, name, value):
        raise AttributeError("constants cannot be modified")
