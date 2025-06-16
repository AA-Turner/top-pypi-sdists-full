def extend_class(cls):
    """
    Given class cls, apply decorator @extend_class to function f so
    that f becomes a regular method of cls:
    >>> class cls: pass
    >>> @extend_class(cls)
    ... def f(self):
    ...   pass
    """
    return lambda f: (setattr(cls, f.__name__, f) or f)
