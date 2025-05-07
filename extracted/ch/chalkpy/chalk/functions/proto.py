from typing import Any, Mapping, Union

from google.protobuf.descriptor import FileDescriptor
from google.protobuf.descriptor_pb2 import FileDescriptorProto, FileDescriptorSet
from google.protobuf.message import Message

from chalk.features._encoding.protobuf import create_empty_pyarrow_scalar_from_proto_type
from chalk.features.underscore import Underscore, UnderscoreFunction


def _is_protobuf_message(obj: Any) -> bool:
    if isinstance(obj, Message):
        return True

    # If using a different protobuf generation implemention, e.g. google._upb._message.MessageMeta,
    # just check for common protobuf fields fields
    required_methods = [
        "DESCRIPTOR",
        "SerializeToString",
        "ParseFromString",
    ]
    return all(hasattr(obj, method) for method in required_methods)


def serialize_message_file_descriptor(message: Message) -> bytes:
    """Create a FileDescriptorSet containing the given message and its dependencies."""
    file_descriptor = message.DESCRIPTOR.file
    file_descriptor_set = FileDescriptorSet()
    processed_files = set()

    def add_file_and_deps(fd: FileDescriptor):
        if fd.name in processed_files:
            return

        for dep in fd.dependencies:
            add_file_and_deps(dep)

        fd_proto = FileDescriptorProto()
        fd.CopyToProto(fd_proto)

        file_descriptor_set.file.append(fd_proto)
        processed_files.add(fd.name)

    add_file_and_deps(file_descriptor)
    return file_descriptor_set.SerializeToString()


class UnderscoreProtoSerialize(UnderscoreFunction):
    def __init__(
        self,
        mapping: Mapping[str, Union[Underscore, Any]],
        message: Message,
    ):
        if not isinstance(mapping, Mapping):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(f"F.proto_serialize(): mapping must be a Mapping: got {type(mapping)}")
        if not _is_protobuf_message(message):
            raise TypeError(f"F.proto_serialize(): message must be a Message: got {type(message)}")

        message_file_descriptor = serialize_message_file_descriptor(message)
        super().__init__(
            "proto_serialize",
            message_file_descriptor,
            message.DESCRIPTOR.full_name,
            list(mapping.keys()),
            *mapping.values(),
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
    return UnderscoreProtoSerialize(mapping, message)


class UnderscoreProtoDeserialize(UnderscoreFunction):
    def __init__(
        self,
        body: Union[Underscore, bytes],
        message: Message,
    ):
        if not isinstance(body, (bytes, Underscore)):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(f"F.proto_deserialize(): body must be a bytes or Underscore, got {type(body)}")
        if not _is_protobuf_message(message):
            raise TypeError(f"F.proto_deserialize(): message must be a Message, got {type(message)}")

        message_file_descriptor = serialize_message_file_descriptor(message)
        message_name = message.DESCRIPTOR.full_name
        pa_scalar = create_empty_pyarrow_scalar_from_proto_type(message)
        super().__init__(
            "proto_deserialize",
            message_file_descriptor,
            message_name,
            pa_scalar,
            body,
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
    return UnderscoreProtoDeserialize(body, message)


__all__ = [
    "proto_serialize",
    "proto_deserialize",
]
