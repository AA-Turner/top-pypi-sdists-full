from __future__ import annotations

import builtins
import textwrap
import traceback
from collections.abc import Awaitable

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol  # type: ignore  # noqa
from types import TracebackType


class AsyncExceptionHandler(Protocol):
    """
    A shorthand for an async exception handler type.
    This is always called under exception context where
    :func:`sys.exc_info()` is available.
    """

    def __call__(
        self,
        exc_type: type[BaseException],
        exc_obj: BaseException,
        exc_tb: TracebackType,
    ) -> Awaitable[None]: ...


if not hasattr(builtins, "ExceptionGroup"):

    class MultiError(Exception):  # type: ignore[no-redef]
        def __init__(self, msg, errors=()):
            if errors:
                types = set(type(e).__name__ for e in errors)
                msg = f"{msg}; {len(errors)} sub errors: ({', '.join(types)})"
                for er in errors:
                    msg += f"\n + {type(er).__name__}: {er}"
                    if er.__traceback__:
                        er_tb = "".join(traceback.format_tb(er.__traceback__))
                        er_tb = textwrap.indent(er_tb, " | ")
                        msg += f"\n{er_tb}\n"
            super().__init__(msg)
            self.__errors__ = tuple(errors)

        def get_error_types(self):
            return {type(e) for e in self.__errors__}

        def __reduce__(self):
            return (type(self), (self.args,), {"__errors__": self.__errors__})

    class TaskGroupError(MultiError):  # type: ignore[no-redef]
        """
        An alias to :exc:`MultiError`.
        """

        pass

else:

    class MultiError(ExceptionGroup):  # type: ignore[no-redef,name-defined]  # noqa: F821
        def __init__(self, msg, errors=()):
            super().__init__(msg, errors)
            self.__errors__ = errors

        def get_error_types(self):
            return {type(e) for e in self.exceptions}

    class TaskGroupError(MultiError):  # type: ignore[no-redef]
        pass
