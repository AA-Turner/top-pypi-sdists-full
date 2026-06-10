"""A common gRPC interface for both the gRPC connection implementation
and the Isolate Server to share."""

import functools
from typing import Any, Optional

from isolate.common import timestamp
from isolate.connections.common import load_serialized_object, serialize_object
from isolate.connections.grpc import definitions
from isolate.logs import Log, LogLevel, LogSource


@functools.singledispatch
def from_grpc(message: definitions.Message) -> Any:
    """Materialize a gRPC message into a Python object."""
    wrong_type = type(message).__name__
    raise NotImplementedError(f"Can't convert {wrong_type} to a Python object.")


@functools.singledispatch
def to_grpc(obj: Any) -> definitions.Message:
    """Convert a Python object into a gRPC message."""
    wrong_type = type(obj).__name__
    raise NotImplementedError(f"Cannot convert {wrong_type} to a gRPC message.")


@from_grpc.register
def _(message: definitions.SerializedObject) -> Any:
    exception_type_name = None
    if message.HasField("exception_type_name"):
        exception_type_name = message.exception_type_name

    exception_message = None
    if message.HasField("exception_message"):
        exception_message = message.exception_message

    return load_serialized_object(
        message.method,
        message.definition,
        was_it_raised=message.was_it_raised,
        # This field predates optional exception metadata; absent values arrive
        # as "", and _prepare_traceback treats that the same as None.
        stringized_traceback=message.stringized_traceback,
        exception_type_name=exception_type_name,
        exception_message=exception_message,
    )


@from_grpc.register
def _(message: definitions.Log) -> Log:
    source = LogSource(definitions.LogSource.Name(message.source).lower())
    level = LogLevel[definitions.LogLevel.Name(message.level).upper()]
    return Log(
        message=message.message,
        source=source,
        level=level,
        timestamp=timestamp.to_datetime(message.timestamp),
    )


@to_grpc.register
def _(obj: Log) -> definitions.Log:
    return definitions.Log(
        message=obj.message_str(),
        source=definitions.LogSource.Value(obj.source.name.upper()),
        level=definitions.LogLevel.Value(obj.level.name.upper()),
        timestamp=timestamp.from_datetime(obj.timestamp),
    )


def to_serialized_object(
    obj: Any,
    method: str,
    was_it_raised: bool = False,
    stringized_traceback: Optional[str] = None,
    exception_type_name: Optional[str] = None,
    exception_message: Optional[str] = None,
) -> definitions.SerializedObject:
    """Convert a Python object into a gRPC message."""
    if was_it_raised:
        if exception_type_name is None:
            exception_type_name = type(obj).__name__
        if exception_message is None:
            exception_message = str(obj)

    serialized_obj = definitions.SerializedObject(
        method=method,
        definition=serialize_object(method, obj),
        was_it_raised=was_it_raised,
        stringized_traceback=stringized_traceback,
    )
    # Current code can run against older generated protobuf classes that do not
    # know about newly added optional fields.
    if (
        exception_type_name is not None
        and "exception_type_name" in serialized_obj.DESCRIPTOR.fields_by_name
    ):
        serialized_obj.exception_type_name = exception_type_name
    if (
        exception_message is not None
        and "exception_message" in serialized_obj.DESCRIPTOR.fields_by_name
    ):
        serialized_obj.exception_message = exception_message
    return serialized_obj
