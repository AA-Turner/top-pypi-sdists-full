from __future__ import annotations

import importlib
import os
from contextlib import contextmanager
from dataclasses import dataclass
from types import TracebackType
from typing import TYPE_CHECKING, Any, Iterator, cast

from tblib import Traceback, TracebackParseError
from tblib.pickling_support import install as tblib_install

if TYPE_CHECKING:
    from typing import Protocol

    class SerializationBackend(Protocol):
        def loads(self, data: bytes) -> Any: ...

        def dumps(self, obj: Any) -> bytes: ...


AGENT_SIGNATURE = "IS_ISOLATE_AGENT"


@dataclass
class SerializationError(Exception):
    """An error that happened during the serialization process."""

    message: str


@dataclass
class ExceptionDeserializationError(SerializationError):
    """Raised when a remote exception cannot be deserialized locally (e.g. the
    module that defines its type isn't importable here)."""

    original_traceback: TracebackType | None
    original_stringized_traceback: str | None
    # Display-only simple type name, matching traceback text (for example,
    # "RemoteOnlyError").
    original_exception_type_name: str | None = None
    # Display-only str() of the remote exception.
    original_exception_message: str | None = None


# NOTE: tblib's install() will search for BaseException subclasses,
# so we have to call it after the SerializationError is defined.
tblib_install()


@contextmanager
def _step(message: str) -> Iterator[None]:
    """A context manager to capture every expression
    underneath it and if any of them fails for any reason
    then it will raise a SerializationError with the
    given message."""

    try:
        yield
    except BaseException as exception:
        raise SerializationError("Error while " + message) from exception


def as_serialization_method(backend: Any) -> SerializationBackend:
    """Ensures that the given backend has loads/dumps methods, and returns
    it as is (also convinces type checkers that the given object satisfies
    the serialization protocol)."""

    if not hasattr(backend, "loads") or not hasattr(backend, "dumps"):
        raise TypeError(
            f"The given serialization backend ({backend.__name__}) does "
            "not have one of the required methods (loads/dumps)."
        )

    return cast("SerializationBackend", backend)


def load_serialized_object(
    serialization_method: str,
    raw_object: bytes,
    *,
    was_it_raised: bool = False,
    stringized_traceback: str | None = None,
    exception_type_name: str | None = None,
    exception_message: str | None = None,
) -> Any:
    """Load the given serialized object using the given serialization method. If
    anything fails, then a SerializationError will be raised. If the was_it_raised
    flag is set to true, then the given object will be raised as an exception (instead
    of being returned)."""

    with _step(f"preparing the serialization backend ({serialization_method})"):
        serialization_backend = as_serialization_method(
            importlib.import_module(serialization_method)
        )

    try:
        with _step("deserializing the given object"):
            result = serialization_backend.loads(raw_object)
    except SerializationError as exc:
        if was_it_raised:
            # We were trying to reconstruct a remote exception but its type
            # isn't importable here, so loads() failed. Surface the genuine
            # local cause along with the remote traceback.
            # Keep both traceback forms: Traceback.from_string() preserves
            # frames, while the string also includes the exception type/message.
            raise ExceptionDeserializationError(
                exc.message,
                original_traceback=_prepare_traceback(stringized_traceback),
                original_stringized_traceback=stringized_traceback,
                original_exception_type_name=exception_type_name,
                original_exception_message=exception_message,
            ) from exc.__cause__
        raise

    if was_it_raised:
        raise prepare_exc(result, stringized_traceback=stringized_traceback)
    else:
        return result


def serialize_object(serialization_method: str, object: Any) -> bytes:
    """Serialize the given object using the given serialization method. If
    anything fails, then a SerializationError will be raised."""

    with _step(f"preparing the serialization backend ({serialization_method})"):
        serialization_backend = as_serialization_method(
            importlib.import_module(serialization_method)
        )

    with _step("serializing the given object"):
        return serialization_backend.dumps(object)


def is_agent() -> bool:
    """Returns true if the current process is an isolate agent."""
    return os.environ.get(AGENT_SIGNATURE) == "1"


def validate_entrypoint(entrypoint: str) -> None:
    """Syntax check for ``"module:attr"``. The agent resolves the module."""
    module, sep, attr = entrypoint.partition(":")
    if not sep or not module or not attr or ":" in attr:
        raise ValueError(f"Invalid entrypoint {entrypoint!r}: expected 'module:attr'.")


def _prepare_traceback(stringized_traceback: str | None) -> TracebackType | None:
    if stringized_traceback:
        try:
            return Traceback.from_string(stringized_traceback).as_traceback()
        except TracebackParseError:
            pass
    return None


def prepare_exc(
    exc: BaseException,
    *,
    stringized_traceback: str | None = None,
) -> BaseException:
    exc.__traceback__ = _prepare_traceback(stringized_traceback)
    return exc
