"""Support errors as values.

This module works best with PEP-634 (Structural Pattern Matching)

    https://peps.python.org/pep-0634/

Example:
>>> import random
>>> from dataclasses import dataclass
>>>
>>> class BlueError(Error):
>>>     pass
>>>
>>> class RedError(Error):
>>>     pass
>>>
>>> def get_result(option: int):
>>>     match option:
>>>         case 0:
>>>             return Ok("value")
>>>         case 1:
>>>             return BlueError("blue")
>>>         case 2:
>>>             return RedError("red")
>>>         case _:
>>>             return Error("error")
>>>
>>> r = get_result(random.randint(10))
>>> match r:
>>>     case Ok(value):
>>>         assert value == "value"
>>>         assert r.value == "value"
>>>     case BlueError(value):
>>>         assert value == "blue"
>>>         assert r.message == "blue"
>>>     case RedError(value):
>>>         assert value == "red"
>>>         assert r.message == "red"
>>>     case Error(value):
>>>         assert value == "error"
>>>         assert r.message == "error"

The interface is borrowed from https://doc.rust-lang.org/std/result/enum.Result.html.
"""

from __future__ import annotations

import functools
from abc import abstractmethod
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    Literal,
    NoReturn,
    ParamSpec,
    TypeVar,
    overload,
)

from typing_extensions import Self

from corvic.well_known_types import JSONAble, JSONExpressable, to_json

T_co = TypeVar("T_co", covariant=True)
E = TypeVar("E")
U = TypeVar("U")
V = TypeVar("V")
P = ParamSpec("P")
R = TypeVar("R")
ExceptionT = TypeVar("ExceptionT", bound=BaseException)
_IgnoredFn = Callable[[Any], Any]


class _Resultable(Generic[T_co, E]):
    """Resultable is the common interface that all result types should implement.

    To benefit the most from the typing of results, most users of results
    should refer to specific concrete classes that have this interface or
    unions of such classes rather than this class.
    """

    @abstractmethod
    def is_ok(self) -> bool:
        """Return True if the result is Ok."""

    @abstractmethod
    def is_error(self) -> bool:
        """Return True if the result is Error."""

    @abstractmethod
    def unwrap_or(self, default: U) -> T_co | U:
        """Return the value if Ok; otherwise, return a default.

        If you do not want to eagerly evaluate default, use `unwrap_or_else`
        instead.

        Example:
        >>> assert Error("error").unwrap_or("error happened") == "error happened"
        >>> assert Ok("value").unwrap_or("error happened") == "value"
        """

    @abstractmethod
    def unwrap_or_else(self, default_fn: Callable[[E], T_co]) -> T_co:
        """Return the value if Ok; otherwise, apply the default function to the error.

        Example:
        >>> assert Error("error")\
.unwrap_or_else(lambda err: "error happened") == "error happened"
        >>> assert Ok("value").unwrap_or_else(lambda err: "error happened") == "value"
        """

    @abstractmethod
    def unwrap_or_raise(self) -> T_co:
        """Return the value if Ok; otherwise, raise the error as an exception.

        Example:
        >>> Error("error").unwrap_or_raise()  # raises Error("error")
        >>> assert Ok("value").unwrap_or_raise() == "value"
        """

    @abstractmethod
    def map(self, fn: Callable[[T_co], R]) -> _Resultable[R, E]:
        """Apply a function to the value if Ok. otherwise, preserve the original error.

        This is useful for chaining results.

        Example:
        >>> assert Error("error").map(lambda v: "success") == Error("error")
        >>> assert Ok("value").map(lambda v: "success") == Ok("success")
        """

    @abstractmethod
    def map_or(self, default: R, fn: Callable[[E], R]) -> R:
        """Apply a function to the value if Ok; otherwise, return the default if Error.

        If do not want to eagerly evaluate default, use `map_or_else` instead.

        Example:
        >>> assert Error("error")\
.map_or("error happened", lambda _: "success") == "error happened"
        >>> assert Ok("value")\
.map_or("error happened", lambda _: "success") == "success"
        """

    @abstractmethod
    def map_or_else(self, default_fn: Callable[[E], R], fn: Callable[[T_co], R]) -> R:
        """Apply a function to the value if Ok; otherwise, apply a default function.

        Example:
        >>> assert Error("error")\
.map_or_else(lambda _: "error happened", lambda _: "success")\
        >>>     == "error happened"
        >>> assert Ok("value")\
.map_or_else(lambda _: "error happened", lambda _: "success") == "success"
        """

    @abstractmethod
    def map_error(self, fn: Callable[[E], R]) -> R:
        """Apply a function if Error; otherwise, preserve the original value.

        This is useful for adding more context while handling errors.

        Example:
        >>> assert Error("error").map_error(
        >>>    lambda _: Error("error happened")) == Error("error happened")
        >>> )
        >>> assert Ok("value")\
.map_error(lambda _: Error("error happened")) == Ok("value")
        """

    @abstractmethod
    def and_then(self, fn: Callable[[T_co], U]) -> U:
        """Apply a function to the value if Ok; otherwise, preserve the error.

        This is useful for chaining results. See also `map` and `or_else`.

        Example:
        >>> def converter(value):
        >>>   return Ok(value + " + 1"
        >>>
        >>> assert Error("error").and_then(converter).is_error()
        >>> assert Ok("value").and_then(converter) == Ok("value + 1")
        """

    @abstractmethod
    def or_else(self, fn: Callable[[E], R]) -> R:
        """Apply a function to the error if Error; otherwise, preserve the value.

        This is useful for chaining fallbacks. See also `and_then`.

        Example:
        >>> class BlueError(Error):
        >>>     pass
        >>>
        >>> class RedError(Error):
        >>>     pass
        >>>
        >>> def fallback(err: BlueError | RedError | Any):
        >>>     match err:
        >>>         case BlueError():
        >>>             return Ok("blue fallback")
        >>>         case RedError():
        >>>             return Ok("red fallback")
        >>>         case _:
        >>>             return Error("no fallback")
        >>>
        >>> assert BlueError().or_else(fallback) == Ok("blue fallback")
        >>> assert RedError().or_else(fallback) == Ok("red fallback")
        >>> assert Error("unknown error").or_else(fallback) == Error("no fallback")
        >>> assert Ok("value").or_else(fallback) == Ok("value")
        """


@dataclass
class Ok(Generic[T_co], _Resultable[T_co, Any]):
    """A successful result."""

    value: T_co

    def is_ok(self) -> Literal[True]:
        return True

    def is_error(self) -> Literal[False]:
        return False

    def unwrap_or(self, default: object) -> T_co:
        return self.value

    def unwrap_or_raise(self) -> T_co:
        return self.value

    def unwrap_or_else(self, default_fn: _IgnoredFn) -> T_co:
        return self.value

    def map(self, fn: Callable[[T_co], R]) -> Ok[R]:
        return Ok(fn(self.value))

    def map_or(self, default: R, fn: Callable[[T_co], R]) -> R:
        return fn(self.value)

    def map_or_else(self, default_fn: _IgnoredFn, fn: Callable[[T_co], R]) -> R:
        return fn(self.value)

    def map_error(self, fn: _IgnoredFn) -> Self:
        return self

    def and_then(self, fn: Callable[[T_co], U]) -> U:
        return fn(self.value)

    def or_else(self, fn: _IgnoredFn) -> Self:
        return self


class Error(Exception, _Resultable[Any, "Error"]):
    """The base class of all corvic errors.

    Usually returned as part of a Result, but can also be raised as an exception
    """

    __match_args__ = ("message",)

    _extra_info: dict[str, JSONExpressable]
    _message: str

    def __init__(self, message: str, **extra_info: JSONAble):
        self._extra_info = {key: to_json(val) for key, val in extra_info.items()}
        self._message = message

    @classmethod
    def from_(cls, other_error: Exception | Error) -> Self:
        """Re-package other_error as an error of this type."""
        # TODO(thunt): Probably set __cause__ on the new exception, but that
        # would probably only be useful if we capture more context a la the
        # information that `raise` attaches.
        if isinstance(other_error, Error):
            return cls(other_error.message, **other_error.extra_info)
        return cls(str(other_error))

    def _render_extra_args(self) -> Iterator[str]:
        return (f"{key}={value}" for key, value in self.extra_info.items())

    def __repr__(self):
        if self.extra_info:
            kwarg_string = ", ".join(("", *self._render_extra_args()))
        else:
            kwarg_string = ""
        return f"{type(self).__name__}({self.message!r}{kwarg_string})"

    def __str__(self):
        return " ".join((self.message, *self._render_extra_args()))

    def __eq__(self, other: object):
        if not isinstance(other, Error):
            return False
        if type(self) is not type(other):
            # also fail if other is not this specific error type
            return False
        return self.message == other.message and self.extra_info == other.extra_info

    @property
    def extra_info(self) -> dict[str, JSONExpressable]:
        return self._extra_info

    @property
    def message(self) -> str:
        return self._message

    def is_ok(self) -> Literal[False]:
        return False

    def is_error(self) -> Literal[True]:
        return True

    def unwrap_or(self, default: U) -> U:
        return default

    def unwrap_or_else(self, default_fn: Callable[[Error], T_co]) -> T_co:
        return default_fn(self)

    def unwrap_or_raise(self) -> NoReturn:
        raise self

    def map(self, fn: _IgnoredFn) -> Self:
        return self

    def map_or(self, default: R, fn: _IgnoredFn) -> R:
        return default

    def map_or_else(self, default_fn: Callable[[Error], R], fn: _IgnoredFn) -> R:
        return default_fn(self)

    def map_error(self, fn: Callable[[Error], R]) -> R:
        return fn(self)

    def and_then(self, fn: _IgnoredFn) -> Self:
        return self

    def or_else(self, fn: Callable[[Error], R]) -> R:
        return fn(self)


class ForeignError(Generic[ExceptionT], _Resultable[Any, "ForeignError[ExceptionT]"]):
    """Resultable wrapper around non-corvic errors."""

    __match_args__ = ("exception",)

    _exception: ExceptionT

    def __init__(self, exception: ExceptionT):
        self._exception = exception

    @property
    def exception(self):
        return self._exception

    def is_ok(self) -> Literal[False]:
        return False

    def is_error(self) -> Literal[True]:
        return True

    def unwrap_or(self, default: U) -> U:
        return default

    def unwrap_or_else(
        self, default_fn: Callable[[ForeignError[ExceptionT]], T_co]
    ) -> T_co:
        return default_fn(self)

    def unwrap_or_raise(self) -> NoReturn:
        raise self._exception

    def map(self, fn: _IgnoredFn) -> Self:
        return self

    def map_or(self, default: R, fn: _IgnoredFn) -> R:
        return default

    def map_or_else(
        self, default_fn: Callable[[ForeignError[ExceptionT]], R], fn: _IgnoredFn
    ) -> R:
        return default_fn(self)

    def map_error(self, fn: Callable[[ForeignError[ExceptionT]], R]) -> R:
        return fn(self)

    def and_then(self, fn: _IgnoredFn) -> Self:
        return self

    def or_else(self, fn: Callable[[ForeignError[ExceptionT]], R]) -> R:
        return fn(self)


# Spiritually, a Result is Ok[T_co] | Error[E0] | Error[E1] | ... but there is no
# way to represent this directly in the type system. Instead, instantiate
# `as_result` for an enumerated number of (type) arguments.
#
# The specific number of instantiations (5) was chosen because any more than 5
# distinct errors from a function certainly deserves a refactor. Do not add more
# instantiations without good reason.
#
# It is probably a feature and not a bug that callers can not create as_result
# for a lot of error types.

ExceptionT0 = TypeVar("ExceptionT0", bound=BaseException)
ExceptionT1 = TypeVar("ExceptionT1", bound=BaseException)
ExceptionT2 = TypeVar("ExceptionT2", bound=BaseException)
ExceptionT3 = TypeVar("ExceptionT3", bound=BaseException)
ExceptionT4 = TypeVar("ExceptionT4", bound=BaseException)


@overload
def as_result(
    exc0: type[ExceptionT0],
    exc1: type[ExceptionT1],
    exc2: type[ExceptionT2],
    exc3: type[ExceptionT3],
    exc4: type[ExceptionT4],
) -> Callable[
    [Callable[P, R]],
    Callable[
        P,
        Ok[R]
        | ForeignError[ExceptionT0]
        | ForeignError[ExceptionT1]
        | ForeignError[ExceptionT2]
        | ForeignError[ExceptionT3]
        | ForeignError[ExceptionT4],
    ],
]: ...


@overload
def as_result(
    exc0: type[ExceptionT0],
    exc1: type[ExceptionT1],
    exc2: type[ExceptionT2],
    exc3: type[ExceptionT3],
) -> Callable[
    [Callable[P, R]],
    Callable[
        P,
        Ok[R]
        | ForeignError[ExceptionT0]
        | ForeignError[ExceptionT1]
        | ForeignError[ExceptionT2]
        | ForeignError[ExceptionT3],
    ],
]: ...


@overload
def as_result(
    exc0: type[ExceptionT0], exc1: type[ExceptionT1], exc2: type[ExceptionT2]
) -> Callable[
    [Callable[P, R]],
    Callable[
        P,
        Ok[R]
        | ForeignError[ExceptionT0]
        | ForeignError[ExceptionT1]
        | ForeignError[ExceptionT2],
    ],
]: ...


@overload
def as_result(
    exc0: type[ExceptionT0], exc1: type[ExceptionT1]
) -> Callable[
    [Callable[P, R]],
    Callable[P, Ok[R] | ForeignError[ExceptionT0] | ForeignError[ExceptionT1]],
]: ...


@overload
def as_result(
    exc0: type[ExceptionT0],
) -> Callable[[Callable[P, R]], Callable[P, Ok[R] | ForeignError[ExceptionT0]]]: ...


def as_result(
    exc0: type[ExceptionT0],
    exc1: type[ExceptionT1] | None = None,
    exc2: type[ExceptionT2] | None = None,
    exc3: type[ExceptionT3] | None = None,
    exc4: type[ExceptionT4] | None = None,
) -> ...:
    """Convert a function that raises into one that returns Ok or Err.

    Raised exceptions of the provided exception types are turned into `Err(exc)`.
    """
    exc_types = [exc for exc in [exc0, exc1, exc2, exc3, exc4] if exc is not None]

    def decorator(f: ...) -> ...:
        @functools.wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> ...:
            try:
                return Ok(f(*args, **kwargs))
            except BaseException as exc:
                for exc_type in exc_types:
                    if isinstance(exc, exc_type):
                        return ForeignError(exc)
                raise

        return wrapper

    return decorator


class CancelledError(Error):
    """Raised when the action was cancelled."""


class UnknownError(Error):
    """Raised when the cause of the error is not known."""


class InvalidArgumentError(Error):
    """Raised when arguments violate the contract."""


class DeadlineExceededError(Error):
    """Raised when the action takes longer than allowed."""


class NotFoundError(Error):
    """Raised when the action references an object that does not exist."""


class AlreadyExistsError(Error):
    """Raised when an object already exists."""


class PermissionDeniedError(Error):
    """Raised the caller does not have premisson to do the action."""


class UnauthenticatedError(Error):
    """Raised the caller could not be authenticated."""


class ResourceExhaustedError(Error):
    """Raised when a resource is exhausted."""


class FailedPreconditionError(Error):
    """Raised when a required precondition was not satisfied."""


class AbortedError(Error):
    """Raised when an action was aborted."""


class UnimplementedError(Error):
    """Raised when an action is not implemented."""


class InternalError(Error):
    """Raised when an internal assumption is violated."""


class UnavailableError(Error):
    """Raised when action depends on a resource that is temporarily unavailable."""


class DataLossError(Error):
    """Raised when action resulted in, or encountered a problem due to data loss."""


class UnknownErrorError(Error):
    """Defined for completeness; you probably don't want to use this."""


class OkError(Error):
    """Defined for completeness; you probably don't want to use this."""
