from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class ValueTone(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VALUE_TONE_UNSPECIFIED: _ClassVar[ValueTone]
    VALUE_TONE_NEUTRAL: _ClassVar[ValueTone]
    VALUE_TONE_GREEN: _ClassVar[ValueTone]
    VALUE_TONE_BLUE: _ClassVar[ValueTone]
    VALUE_TONE_YELLOW: _ClassVar[ValueTone]
    VALUE_TONE_ORANGE: _ClassVar[ValueTone]
    VALUE_TONE_RED: _ClassVar[ValueTone]
    VALUE_TONE_PURPLE: _ClassVar[ValueTone]

VALUE_TONE_UNSPECIFIED: ValueTone
VALUE_TONE_NEUTRAL: ValueTone
VALUE_TONE_GREEN: ValueTone
VALUE_TONE_BLUE: ValueTone
VALUE_TONE_YELLOW: ValueTone
VALUE_TONE_ORANGE: ValueTone
VALUE_TONE_RED: ValueTone
VALUE_TONE_PURPLE: ValueTone
