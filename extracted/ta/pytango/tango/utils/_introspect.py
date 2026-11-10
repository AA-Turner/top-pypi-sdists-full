# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Attribute discovery and docstring transfer helpers."""

import contextlib
import types


def __get_meth_func(klass, method_name):
    meth = getattr(klass, method_name)
    func = meth
    if hasattr(meth, "__func__"):
        func = meth.__func__
    return meth, func


def document_method(klass, method_name, d, add=True):
    meth, func = __get_meth_func(klass, method_name)
    if add:
        cpp_doc = meth.__doc__
        if cpp_doc:
            func.__doc__ = f"{d}\n{cpp_doc}"
            return
    func.__doc__ = d

    if func.__name__ != method_name:
        with contextlib.suppress(AttributeError):
            func.__name__ = method_name


def document_static_method(klass, method_name, d, add=True):
    meth, _ = __get_meth_func(klass, method_name)
    if add:
        cpp_doc = meth.__doc__
        if cpp_doc:
            meth.__doc__ = f"{d}\n{cpp_doc}"
            return
    meth.__doc__ = d


def get_attrs(obj):
    """Helper for dir2 implementation."""
    if not hasattr(obj, "__dict__"):
        return []  # slots only
    proxy_type = types.MappingProxyType
    if not isinstance(obj.__dict__, (dict, proxy_type)):
        raise TypeError(f"{obj!r}.__dict__ is a {type(obj.__dict__)}, not a dictionary")
    return obj.__dict__.keys()


def dir2(obj):
    """Default dir implementation.

    Inspired by gist: katyukha/dirmixin.py
    https://gist.github.com/katyukha/c6e5e2b829e247c9b009
    """
    attrs = set()

    if not hasattr(obj, "__bases__"):
        # obj is an instance
        if not hasattr(obj, "__class__"):
            # slots
            return sorted(get_attrs(obj))
        klass = obj.__class__
        attrs.update(get_attrs(klass))
    else:
        # obj is a class
        klass = obj

    for cls in klass.__bases__:
        # dir2(cls) already contributes get_attrs(cls) for a class argument.
        attrs.update(dir2(cls))
    attrs.update(get_attrs(obj))
    return list(attrs)
