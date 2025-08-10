from typing import Any, Mapping, Union

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


def proto_serialize(mapping: Mapping[str, Union[Underscore, Any]], message: Message):
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

    return UnderscoreFunction(
        "proto_serialize",
        serialize_message_file_descriptor(message.DESCRIPTOR.file),
        message.DESCRIPTOR.full_name,
        list(mapping.keys()),
        *mapping.values(),
    )


def proto_deserialize(body: Union[Underscore, bytes], message: Message):
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
    return UnderscoreFunction(
        "proto_deserialize",
        message_file_descriptor,
        message_name,
        pa_scalar,
        body,
    )


__all__ = [
    "proto_serialize",
    "proto_deserialize",
]
