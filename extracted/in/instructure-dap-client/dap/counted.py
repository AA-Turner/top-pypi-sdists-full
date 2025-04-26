import inspect
import typing
from functools import wraps
from typing import Any, Callable, Dict, Optional, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def call_counted(func: F) -> F:
    "Tracks invocations to a free function or an instance method."

    if not callable(func):
        raise TypeError("expected: callable instance")

    sig = inspect.signature(func)
    is_instance_method = "self" in sig.parameters

    @wraps(func)
    def counter(*args: Any, **kwargs: Any) -> Any:
        if is_instance_method:
            ref = id(args[0])  # do not prevent garbage collection
        else:
            ref = 0

        calls: Dict[int, int] = getattr(counter, "_calls")
        calls[ref] = calls.get(ref, 0) + 1

        return func(*args, **kwargs)

    setattr(counter, "_calls", {})
    return typing.cast(F, counter)


def _get_calls(func: Callable[..., Any]) -> Dict[int, int]:
    if not callable(func):
        raise TypeError("expected: callable instance")

    calls: Optional[Dict[int, int]] = getattr(func, "_calls", None)
    if calls is None:
        raise ValueError("expected: call-counted function")

    return calls


def reset_calls(func: Callable[..., Any]) -> None:
    "Clears call data from previous invocations."

    _get_calls(func).clear()


def total_calls(func: Callable[..., Any]) -> int:
    "Returns the number of calls to a free function or an instance method."

    return sum(_get_calls(func).values())


def instance_calls(func: Callable[..., Any], obj: object) -> int:
    "Returns the number of calls to an instance method on an object."

    return _get_calls(func).get(id(obj), 0)
