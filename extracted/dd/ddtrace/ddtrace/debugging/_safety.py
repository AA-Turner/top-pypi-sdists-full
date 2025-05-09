from inspect import CO_VARARGS
from inspect import CO_VARKEYWORDS
from itertools import chain
from types import FrameType
from typing import Any
from typing import Dict
from typing import Iterator
from typing import Tuple

from ddtrace.internal.safety import get_slots


GetSetDescriptor = type(type.__dict__["__dict__"])  # type: ignore[index]  # noqa: F821


def get_args(frame: FrameType) -> Iterator[Tuple[str, Any]]:
    code = frame.f_code
    nargs = code.co_argcount + bool(code.co_flags & CO_VARARGS) + bool(code.co_flags & CO_VARKEYWORDS)
    arg_names = code.co_varnames[:nargs]
    arg_values = (frame.f_locals[name] for name in arg_names)

    return zip(arg_names, arg_values)


def get_locals(frame: FrameType) -> Iterator[Tuple[str, Any]]:
    code = frame.f_code
    _locals = frame.f_locals
    nargs = code.co_argcount + bool(code.co_flags & CO_VARARGS) + bool(code.co_flags & CO_VARKEYWORDS)
    return (
        (name, _locals.get(name)) for name in chain(code.co_varnames[nargs:], code.co_freevars, code.co_cellvars)
    )  # include freevars and cellvars


def get_globals(frame: FrameType) -> Iterator[Tuple[str, Any]]:
    nonlocal_names = frame.f_code.co_names
    _globals = frame.f_globals

    return ((name, _globals[name]) for name in nonlocal_names if name in _globals)


def safe_getattr(obj: Any, name: str) -> Any:
    try:
        return object.__getattribute__(obj, name)
    except Exception as e:
        return e


def safe_getitem(obj, index):
    if isinstance(obj, list):
        return list.__getitem__(obj, index)
    elif isinstance(obj, dict):
        return dict.__getitem__(obj, index)
    elif isinstance(obj, tuple):
        return tuple.__getitem__(obj, index)
    raise TypeError("Type is not indexable collection " + str(type(obj)))


def _safe_dict(o: Any) -> Dict[str, Any]:
    try:
        __dict__ = object.__getattribute__(o, "__dict__")
        if type(__dict__) is dict:
            return __dict__
    except Exception:
        pass  # nosec

    raise AttributeError("No safe __dict__")


def get_fields(obj: Any) -> Dict[str, Any]:
    try:
        return _safe_dict(obj)
    except AttributeError:
        # Check for slots
        return {s: safe_getattr(obj, s) for s in get_slots(obj)}
