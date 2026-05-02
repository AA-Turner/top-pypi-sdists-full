# -*- coding: utf-8 -*-
"""

This module helps to kill global state in your program
and replace it with execution-bound state which preserves
a lot of the good properties of using true locals.

This module uses a bit of code from "werkzeug.local" by Armin Ronacher.

:copyright: (c) 2012 by Holger Krekel, partially Armin Ronacher
:license: BSD, see LICENSE for more details.
"""

# use since each thread has its own greenlet we can just use those as identifiers
# for the context.  If greenlets are not available we fall back to the
# current thread ident.

try:
    from greenlet import getcurrent as _getident
except ImportError:
    try:
        from thread import get_ident as _getident
    except ImportError:
        try:
            from _thread import get_ident as _getident
        except ImportError:
            from dummy_thread import get_ident as _getident

class xlocal(object):
    """ Implementation of an execution local object. """
    def __init__(self):
        d = self.__dict__
        d["_getident"] = _getident
        d["_storage"] = {}

    def _getlocals(self, autocreate=False):
        ident = self._getident()
        try:
            return self._storage[ident]
        except KeyError:
            if not autocreate:
                raise
            self._storage[ident] = loc = {}
            return loc

    def _checkremove(self):
        ident = self._getident()
        val = self._storage.get(ident)
        if val is not None:
            if not val:
                del self._storage[ident]

    def __call__(self, **kwargs):
        """ return context manager which will set execution locals
        for all code within the with-body.
        """
        return WithXLocals(self, kwargs)

    def __getattr__(self, name):
        try:
            return self._getlocals()[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, val):
        raise AttributeError("cannot setattr, use 'with scoping'")

    def __delattr__(self, name):
        raise AttributeError("cannot delattr xlocal local attr")

class WithXLocals:
    def __init__(self, xlocal, kwargs):
        self._xlocal = xlocal
        self._kwargs = kwargs

    def __enter__(self):
        loc = self._xlocal._getlocals(autocreate=True)
        self._undostack = undostack = []
        for name, val in self._kwargs.items():
            assert name[0] != "_", "names with underscore reserved for future use"
            try:
                undostack.append(lambda n=name,v=loc[name]: loc.__setitem__(n, v))
            except KeyError:
                undostack.append(lambda n=name: loc.__delitem__(n))
            loc[name] = val
        return self

    def __exit__(self, *args):
        for action in self.__dict__.pop("_undostack"):
            action()
        self._xlocal._checkremove()
