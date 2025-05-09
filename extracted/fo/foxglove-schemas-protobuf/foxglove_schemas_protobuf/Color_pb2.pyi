"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Generated by https://github.com/foxglove/schemas"""

import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class Color(google.protobuf.message.Message):
    """A color in RGBA format"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    R_FIELD_NUMBER: builtins.int
    G_FIELD_NUMBER: builtins.int
    B_FIELD_NUMBER: builtins.int
    A_FIELD_NUMBER: builtins.int
    r: builtins.float
    """Red value between 0 and 1"""
    g: builtins.float
    """Green value between 0 and 1"""
    b: builtins.float
    """Blue value between 0 and 1"""
    a: builtins.float
    """Alpha value between 0 and 1"""
    def __init__(
        self,
        *,
        r: builtins.float = ...,
        g: builtins.float = ...,
        b: builtins.float = ...,
        a: builtins.float = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["a", b"a", "b", b"b", "g", b"g", "r", b"r"]) -> None: ...

global___Color = Color
