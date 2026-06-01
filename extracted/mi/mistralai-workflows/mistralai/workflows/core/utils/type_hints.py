import typing
from typing import Any, Callable


def get_type_hints(fn: Callable[..., Any]) -> dict[str, Any]:
    """Resolve type hints from a function, unwrapping decorator chains if needed.

    PEP 649 (Python 3.14+) changes annotation semantics so that
    ``typing.get_type_hints`` fails on functions wrapped via
    ``functools.wraps``.  The ``@activity`` decorator stores the
    original function as ``__original_func__``; this helper falls back
    to that attribute when present.
    """
    return typing.get_type_hints(getattr(fn, "__original_func__", fn))
