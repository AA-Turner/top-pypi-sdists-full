"""Projection for oneofs that cross JSON under one key.

A oneof marked ``json_union`` in the proto carries one scalar member and one message
member sharing a single JSON key -- the group's own name. Callers write that key; the
generated class names the members. This rewrites the former into the latter.

Nothing here names a field. The marker is read off the descriptor, so a new union costs
a line in the proto and nothing in the SDK.
"""

from typing import Any, Dict, Mapping, Set, Type, TypeVar, Union

from google.protobuf.descriptor import Descriptor, FieldDescriptor, OneofDescriptor
from google.protobuf.message import Message

from seltz_public_api.proto.v1 import options_pb2

_M = TypeVar("_M", bound=Message)


def _is_union(oneof: OneofDescriptor) -> bool:
    """Whether this oneof crosses JSON under its group name rather than its members'."""
    return bool(oneof.GetOptions().Extensions[options_pb2.json_union])


def _member_for(oneof: OneofDescriptor, value: Any, parameter: str) -> FieldDescriptor:
    """The member of `oneof` that takes `value`, chosen by the value's own type.

    A boolean and a message cannot be confused, which is what lets one key carry either.
    """
    if isinstance(value, bool):
        wanted, described = FieldDescriptor.TYPE_BOOL, "a boolean"
    elif isinstance(value, (Message, Mapping)):
        wanted, described = FieldDescriptor.TYPE_MESSAGE, "an options message"
    else:
        raise TypeError(
            f"{parameter}[{oneof.name!r}] takes a boolean, an options message or a "
            f"mapping, not {type(value).__name__}"
        )

    member = next((field for field in oneof.fields if field.type == wanted), None)
    if member is None:
        raise TypeError(f"{parameter}[{oneof.name!r}] takes no {described}")
    return member


def _accepted_keys(descriptor: Descriptor) -> Set[str]:
    """The keys a caller may write, which are the message's own fields with each marked
    oneof's members collapsed to the group name they share.

    That is the JSON surface, not the message's field set. A marked oneof's members are
    reachable only through the group name, so one selection has one spelling.
    """
    accepted = set()
    for field in descriptor.fields:
        oneof = field.containing_oneof
        accepted.add(
            oneof.name if oneof is not None and _is_union(oneof) else field.name
        )
    return accepted


def _project(
    descriptor: Descriptor, selection: Mapping[str, Any], parameter: str
) -> Dict[str, Any]:
    """`selection` with every marked oneof rewritten to the member its value picks.

    Recurses into a message-typed field given a mapping, so a nested selection is
    projected and a nested key is checked at the depth it was written. protobuf builds a
    submessage from a mapping, so the result stays a plain dict.
    """
    accepted = _accepted_keys(descriptor)
    unknown = sorted(set(selection) - accepted)
    if unknown:
        named = ", ".join(repr(name) for name in unknown)
        raise TypeError(
            f"{parameter} has no member {named}; expected "
            + " or ".join(repr(name) for name in sorted(accepted))
        )

    built: Dict[str, Any] = {}
    for key, value in selection.items():
        oneof = next(
            (o for o in descriptor.oneofs if _is_union(o) and o.name == key), None
        )
        field = (
            _member_for(oneof, value, parameter)
            if oneof is not None
            else descriptor.fields_by_name[key]
        )

        where = f"{parameter}[{key!r}]"
        if value is None:
            raise TypeError(f"{where} is None; leave the key out to leave it unset")

        if field.message_type is not None:
            if isinstance(value, Message):
                if value.DESCRIPTOR is not field.message_type:
                    raise TypeError(
                        f"{where} takes {field.message_type.name}, "
                        f"not {value.DESCRIPTOR.name}"
                    )
            elif isinstance(value, Mapping):
                value = _project(field.message_type, value, where)

        built[field.name] = value

    return built


def from_json_unions(
    message: Type[_M],
    selection: Union[_M, Mapping[str, Any]],
    parameter: str,
) -> _M:
    """Builds a `message` from a caller's mapping, projecting every marked oneof.

    A key must be one the JSON surface has, at whatever depth it is written, so a typo
    fails rather than reaching the service as a selection nobody wrote. A marked oneof is
    addressed by its group name and rewritten to the member the value's type picks.

    An already-built message passes through, so the faithful form stays available beside
    the shorthand.

    `parameter` names the SDK parameter in errors, which is not always the message name.

    Raises:
        TypeError: for a key the JSON surface has no member for, for a value that is
            neither a boolean nor a message or mapping where a union expects one, for
            an options message of the wrong type, and for a `None`.
    """
    if isinstance(selection, message):
        return selection

    return message(**_project(message.DESCRIPTOR, selection, parameter))
