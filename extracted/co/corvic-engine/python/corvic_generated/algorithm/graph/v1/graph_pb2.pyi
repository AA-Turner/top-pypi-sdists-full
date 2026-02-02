from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Node2VecParameters(_message.Message):
    __slots__ = ("ndim", "walk_length", "window", "p", "q", "alpha", "min_alpha", "negative", "epochs")
    NDIM_FIELD_NUMBER: _ClassVar[int]
    WALK_LENGTH_FIELD_NUMBER: _ClassVar[int]
    WINDOW_FIELD_NUMBER: _ClassVar[int]
    P_FIELD_NUMBER: _ClassVar[int]
    Q_FIELD_NUMBER: _ClassVar[int]
    ALPHA_FIELD_NUMBER: _ClassVar[int]
    MIN_ALPHA_FIELD_NUMBER: _ClassVar[int]
    NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    EPOCHS_FIELD_NUMBER: _ClassVar[int]
    ndim: int
    walk_length: int
    window: int
    p: float
    q: float
    alpha: float
    min_alpha: float
    negative: int
    epochs: int
    def __init__(self, ndim: _Optional[int] = ..., walk_length: _Optional[int] = ..., window: _Optional[int] = ..., p: _Optional[float] = ..., q: _Optional[float] = ..., alpha: _Optional[float] = ..., min_alpha: _Optional[float] = ..., negative: _Optional[int] = ..., epochs: _Optional[int] = ...) -> None: ...
