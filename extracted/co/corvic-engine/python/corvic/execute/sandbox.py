"""Sandboxed method execution."""

import concurrent.futures
from collections.abc import Callable
from typing import (
    Generic,
    ParamSpec,
    TypeVar,
)

from corvic.execute.errors import ExceptionError, SignaledError
from corvic.result import Ok

P = ParamSpec("P")
R = TypeVar("R")


class Sandboxed(Generic[P, R]):
    """Sandboxes the execution of a function.

    The sandboxing is implemented by executing the function in a separate process. The
    primary purpose of the sandboxing is to ensure that signal errors occur outside the
    callers process and can thus be converted into python exceptions.

    Example usage:
        class Foo:
            def __init__(self, args):
                ...

            def _might_segfault(self)
                ...
            def calls_might_segfault(self, ...):
                return corvic.system.execute.Sandboxed(self._might_segfault, ...)

    """

    def __init__(self, method: Callable[P, R]):
        self._method = method

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        with concurrent.futures.ProcessPoolExecutor(max_workers=1) as pool:
            try:
                return pool.submit(self._method, *args, **kwargs).result()
            except concurrent.futures.process.BrokenProcessPool as exc:
                raise SignaledError(
                    "signal received during sandboxed method execution"
                ) from exc
            except Exception:
                raise

    def as_result(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> Ok[R] | ExceptionError | SignaledError:
        try:
            return Ok(value=self.__call__(*args, **kwargs))
        except SignaledError as exc:
            return exc
        except Exception as exc:
            return ExceptionError(exc=exc)
