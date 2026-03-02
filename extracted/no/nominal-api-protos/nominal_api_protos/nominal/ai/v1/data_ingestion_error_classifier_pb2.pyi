from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ErrorClassification(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERROR_CLASSIFICATION_UNSPECIFIED: _ClassVar[ErrorClassification]
    ERROR_CLASSIFICATION_CLIENT: _ClassVar[ErrorClassification]
    ERROR_CLASSIFICATION_SERVER: _ClassVar[ErrorClassification]
ERROR_CLASSIFICATION_UNSPECIFIED: ErrorClassification
ERROR_CLASSIFICATION_CLIENT: ErrorClassification
ERROR_CLASSIFICATION_SERVER: ErrorClassification

class ClassifyErrorRequest(_message.Message):
    __slots__ = ("error_message",)
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    error_message: str
    def __init__(self, error_message: _Optional[str] = ...) -> None: ...

class ClassifyErrorResponse(_message.Message):
    __slots__ = ("classification", "reason")
    CLASSIFICATION_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    classification: ErrorClassification
    reason: str
    def __init__(self, classification: _Optional[_Union[ErrorClassification, str]] = ..., reason: _Optional[str] = ...) -> None: ...
