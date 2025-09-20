from typing import Any, Mapping, Type, Union

from google.protobuf import timestamp_pb2
from google.protobuf.internal.enum_type_wrapper import EnumTypeWrapper
from google.protobuf.message import Message

from chalk.features._encoding.protobuf import (
    create_empty_pyarrow_scalar_from_proto_type,
    serialize_message_file_descriptor,
)
from chalk.features.underscore import Underscore, UnderscoreFunction


def _is_protobuf_message(obj: Any) -> bool:
    return isinstance(obj, Message) or (
        # If using a different protobuf generation implementation,
        # e.g. google._upb._message.MessageMeta, check for common protobuf fields
        hasattr(obj, "DESCRIPTOR")
        and hasattr(obj, "SerializeToString")
        and hasattr(obj, "ParseFromString")
    )


def _is_protobuf_enum_type(obj: Type) -> bool:
    return isinstance(obj, EnumTypeWrapper) or (
        hasattr(obj, "DESCRIPTOR") and hasattr(obj, "Name") and hasattr(obj, "Value") and hasattr(obj, "items")
    )


def proto_enum_value_to_name(value: Union[Underscore, int], proto_enum: EnumTypeWrapper):
    """
    Convert a serialized proto enum value to its name as a string.
    Calls F.map_get(...) on the enum type's value-to-name mapping.

    Parameters
    ----------
    value
        The enum value
    proto_enum
        The class of the proto enum to convert

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> from protos.gen.v1.transaction_pb2 import GetTransactionResponse, TransactionCategory
    >>> @features
    ... class Transaction:
    ...    id: int
    ...    transaction_response_bytes: bytes
    ...    transaction_response: GetTransactionResponse = F.proto_deserialize(
    ...        _.transaction_response_bytes,
    ...        GetTransactionResponse,
    ...    )
    ...    transaction_category_name: F.proto_enum_value_to_name(_.transaction_response.category, TransactionCategory)

    """
    if not _is_protobuf_enum_type(proto_enum):
        raise TypeError(
            f"F.proto_enum_value_to_name(...) parameter 'proto_enum' must be a protobuf enum type class, instead got {proto_enum}"
        )
    from chalk import functions as F

    mapping = {v: k for k, v in proto_enum.items()}
    return F.map_get(mapping, value)


def proto_serialize(mapping: Mapping[str, Union[Underscore, Any]], message: Type[Message]):
    """
    Serialize a proto message from a mapping of field names to values.

    Parameters
    ----------
    mapping
        The mapping of names to features to serialize.
    message
        The proto message to serialize.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> from protos.gen.v1.transaction_pb2 import GetTransactionRequest
    >>> @features
    ... class Transaction:
    ...    id: int
    ...    transaction_request: bytes = F.proto_serialize(
    ...        {
    ...            "id": _.id,
    ...        },
    ...        GetTransactionRequest,
    ...    )
    """
    if not isinstance(mapping, Mapping):  # pyright: ignore[reportUnnecessaryIsInstance]
        raise TypeError(f"F.proto_serialize(): mapping must be a Mapping: got {type(mapping)}")
    if not _is_protobuf_message(message):
        raise TypeError(f"F.proto_serialize(): message must be a Message: got {type(message)}")

    repr_override = f"F.{proto_serialize.__name__}({mapping!r}, {message.DESCRIPTOR.full_name})"
    return UnderscoreFunction(
        "proto_serialize",
        serialize_message_file_descriptor(message.DESCRIPTOR.file),
        message.DESCRIPTOR.full_name,
        list(mapping.keys()),
        *mapping.values(),
        _chalk__repr_override=repr_override,
    )


def proto_deserialize(body: Union[Underscore, bytes], message: Type[Message]):
    """
    Deserialize a proto message from a bytes feature.

    Parameters
    ----------
    body
        The bytes feature to deserialize.
    message
        The proto message type to deserialize.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features
    >>> from protos.gen.v1.transaction_pb2 import GetTransactionResponse
    >>> @features
    ... class Transaction:
    ...    id: int
    ...    transaction_response_bytes: bytes
    ...    transaction_response: GetTransactionResponse = F.proto_deserialize(
    ...        _.transaction_response_bytes,
    ...        GetTransactionResponse,
    ...    )
    """
    if not isinstance(body, (bytes, Underscore)):  # pyright: ignore[reportUnnecessaryIsInstance]
        raise TypeError(f"F.proto_deserialize(): body must be a bytes or Underscore, got {type(body)}")
    if not _is_protobuf_message(message):
        raise TypeError(f"F.proto_deserialize(): message must be a Message, got {type(message)}")

    message_file_descriptor = serialize_message_file_descriptor(message.DESCRIPTOR.file)
    message_name = message.DESCRIPTOR.full_name
    pa_scalar = create_empty_pyarrow_scalar_from_proto_type(message)
    repr_override = f"F.{proto_deserialize.__name__}({body!r}, {message_name})"
    return UnderscoreFunction(
        "proto_deserialize", message_file_descriptor, message_name, pa_scalar, body, _chalk__repr_override=repr_override
    )


def proto_timestamp_to_datetime(timestamp: Union[Underscore, timestamp_pb2.Timestamp]):
    """
    Converts a google.protobuf.timestamp.Timestamp object (a struct with 'seconds' & 'nanos' fields) into a UTC timestamp.
    """
    return UnderscoreFunction("from_unixtime", timestamp.seconds + (timestamp.nanos / 1_000_000_000.0))


__all__ = ["proto_serialize", "proto_deserialize", "proto_enum_value_to_name", "proto_timestamp_to_datetime"]
