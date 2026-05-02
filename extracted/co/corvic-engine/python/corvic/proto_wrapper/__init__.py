"""Common machinery for wrapping proto messages."""

from corvic.proto_wrapper._errors import ProtoParseError
from corvic.proto_wrapper._wrappers import OneofProtoWrapper, ProtoWrapper

__all__ = [
    "ProtoWrapper",
    "OneofProtoWrapper",
    "ProtoParseError",
]
