"""A failure value that still carries the exception behind it.

Helpers that turn a caught exception into a plain value (a manager's ``{"success": False,
"error": str(e)}`` dict, a summarizer's failure sentence) used to drop the exception, so the
tool built its ``ToolError`` with no stack and the executor banner had to guess. Return one of
these instead: it reads exactly like the plain value (same ``==``, same JSON, same
``startswith``), and ``carried_exception(value)`` hands the tool the exception for
``ToolError.declared(..., exc=...)``. A value with no exception means nothing was raised.
"""

from __future__ import annotations

from typing import Any


class FailureDict(dict):
    """A failure dict carrying the exception that produced it (``.exception``)."""

    exception: BaseException | None

    def __init__(self, *args: Any, exception: BaseException | None = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.exception = exception


class FailureText(str):
    """A failure sentence carrying the exception that produced it (``.exception``)."""

    exception: BaseException | None

    def __new__(cls, text: str, exception: BaseException | None = None) -> FailureText:
        obj = super().__new__(cls, text)
        obj.exception = exception
        return obj


def carried_exception(value: Any) -> BaseException | None:
    """The exception a failure value carries, or ``None`` when nothing was raised."""
    exc = getattr(value, "exception", None)
    return exc if isinstance(exc, BaseException) else None
