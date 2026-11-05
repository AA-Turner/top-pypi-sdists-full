"""Read the chain of causes below an exception.

A database driver error usually reaches a traced function wrapped one or two
levels down (``raise QueryError(...) from timeout``). Recording only the top
message makes a connection timeout read as a broken query, so spans and replay
results carry the deepest cause too.
"""

from __future__ import annotations

from typing import Any, Callable

MAX_ERROR_CAUSE_DEPTH = 10
"""How many causes below an exception are followed."""

_CODE_ATTRIBUTES = ("code", "sqlstate", "pgcode", "errno")


def _cause_of(error: BaseException) -> BaseException | None:
    # The same rule Python's traceback uses: an explicit ``from`` cause wins,
    # and an implicit context counts unless ``from None`` suppressed it. Bitfab's
    # own replay errors also keep their cause on a ``cause`` attribute.
    if error.__cause__ is not None:
        return error.__cause__
    attribute = getattr(error, "cause", None)
    if isinstance(attribute, BaseException):
        return attribute
    if error.__suppress_context__:
        return None
    return error.__context__


def _error_code(error: BaseException) -> str | int | None:
    for attribute in _CODE_ATTRIBUTES:
        value = getattr(error, attribute, None)
        if isinstance(value, (str, int)) and not isinstance(value, bool):
            return value
    return None


def error_causes(error: BaseException) -> list[BaseException]:
    """The causes below ``error``, nearest first, stopping at the depth limit
    or at a cause already seen."""
    causes: list[BaseException] = []
    seen = {id(error)}
    current = error
    while len(causes) < MAX_ERROR_CAUSE_DEPTH:
        cause = _cause_of(current)
        if cause is None or id(cause) in seen:
            break
        causes.append(cause)
        seen.add(id(cause))
        current = cause
    return causes


def describe_error(error: BaseException) -> str:
    """The exception's message, followed by the deepest cause's message when
    it wraps another exception, e.g. ``Failed query: ... (caused by:
    connection timeout)``. The cause is left off when the message already
    contains it."""
    message = str(error)
    causes = error_causes(error)
    if not causes:
        return message
    deepest = str(causes[-1]).strip()
    if not deepest or deepest in message:
        return message
    return f"{message} (caused by: {deepest})"


def serialize_error(
    error: BaseException,
    extra: Callable[[BaseException], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """An exception as a JSON record: type, message, the driver's code when it
    has one, and its causes nested under ``cause`` down to the depth limit.
    ``extra`` adds fields a specific exception type carries."""
    seen: set[int] = set()

    def serialize(value: BaseException, depth: int) -> dict[str, Any]:
        seen.add(id(value))
        serialized: dict[str, Any] = {
            "type": type(value).__name__,
            "message": str(value),
        }
        code = _error_code(value)
        if code is not None:
            serialized["code"] = code
        if extra is not None:
            serialized.update(extra(value))
        cause = _cause_of(value)
        if (
            cause is not None
            and id(cause) not in seen
            and depth < MAX_ERROR_CAUSE_DEPTH
        ):
            serialized["cause"] = serialize(cause, depth + 1)
        return serialized

    return serialize(error, 1)
