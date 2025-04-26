from __future__ import annotations

import dataclasses
import functools
import sys
from typing import Any

# Dataclasses has a bug on python 3.10 where the custom __getstate__ and __setstate__ is ignored if the class also defines __slots__
# See https://github.com/python/cpython/issues/104035
# Fixing via monkeypatch. The code below is pasted from
# https://github.com/python/cpython/blob/83518b3511712eb95e496bed5a8cf7498ebd02ea/Lib/dataclasses.py#L1122-L1146 and
# https://github.com/python/cpython/blob/72eea512b88f8fd68b7258242c37da963ad87360/Lib/dataclasses.py#L1223C1-L1228C51


def _add_slots(cls: type[Any], is_frozen: bool):
    # Need to create a new class, since we can't set __slots__
    #  after a class has been created.

    # Make sure __slots__ isn't already set.
    if "__slots__" in cls.__dict__:
        raise TypeError(f"{cls.__name__} already specifies __slots__")

    # Create a new dict for our new class.
    cls_dict = dict(cls.__dict__)
    field_names = tuple(f.name for f in dataclasses.fields(cls))
    cls_dict["__slots__"] = field_names
    for field_name in field_names:
        # Remove our attributes, if present. They'll still be
        #  available in _MARKER.
        cls_dict.pop(field_name, None)

    # Remove __dict__ itself.
    cls_dict.pop("__dict__", None)

    # And finally create the class.
    qualname = getattr(cls, "__qualname__", None)
    cls = type(cls)(cls.__name__, cls.__bases__, cls_dict)  # pyright: ignore
    if qualname is not None:
        cls.__qualname__ = qualname

    if is_frozen:
        # Need this for pickling frozen classes with slots.
        if "__getstate__" not in cls_dict:
            cls.__getstate__ = dataclasses._dataclass_getstate  # pyright: ignore
        if "__setstate__" not in cls_dict:
            cls.__setstate__ = dataclasses._dataclass_setstate  # pyright: ignore
    return cls


@functools.lru_cache(None)
def install_dataclass_slots_patch_if_needed():
    """Patch the implementation of slots when slots=True and frozen=True in python 3.10"""
    if sys.version_info < (3, 11):
        dataclasses._add_slots = _add_slots  # pyright: ignore -- we want to monkeypatch the buggy implementation
