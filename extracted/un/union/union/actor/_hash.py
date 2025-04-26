# From https://github.com/python/cpython/blob/fb0cf7d1408c904e40142a74cd7a53eb52a8e568/Lib/functools.py#L444-L489

# Python module wrapper for _functools C module
# to allow utilities written in Python to be added
# to the functools module.
# Written by Nick Coghlan <ncoghlan at gmail.com>,
# Raymond Hettinger <python at rcn.com>,
# and Łukasz Langa <lukasz at langa.pl>.
#   Copyright (C) 2006-2013 Python Software Foundation.
# See C source code for _functools credits/copyright
from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import FlyteFile


def _extract_key(obj):
    if isinstance(obj, (FlyteFile, FlyteDirectory)):
        if obj.remote_source:
            return obj.remote_source
        else:
            return obj.path
    return obj


class _HashedSeq(list):
    __slots__ = ("hashvalue",)

    def __init__(self, tup, hash=hash):
        self[:] = tup
        self.hashvalue = hash(tup)

    def __hash__(self):
        return self.hashvalue


def _make_key(args, kwds, kwd_mark=(object(),), fasttypes={int, str}, type=type, len=len):
    key = args
    if kwds:
        key += kwd_mark
        for item in kwds.items():
            key += item
    if len(key) == 1 and type(key[0]) in fasttypes:
        return key[0]
    key_ = tuple(_extract_key(k) for k in key)
    return _HashedSeq(key_)
