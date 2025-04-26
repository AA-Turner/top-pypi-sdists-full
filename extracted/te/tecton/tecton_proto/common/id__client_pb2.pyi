from tecton_proto.auditlog import metadata__client_pb2 as _metadata__client_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Id(_message.Message):
    __slots__ = ["least_significant_bits", "most_significant_bits"]
    LEAST_SIGNIFICANT_BITS_FIELD_NUMBER: _ClassVar[int]
    MOST_SIGNIFICANT_BITS_FIELD_NUMBER: _ClassVar[int]
    least_significant_bits: int
    most_significant_bits: int
    def __init__(self, most_significant_bits: _Optional[int] = ..., least_significant_bits: _Optional[int] = ...) -> None: ...
