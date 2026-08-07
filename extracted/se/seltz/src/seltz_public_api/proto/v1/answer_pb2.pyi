from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AnswerRequest(_message.Message):
    __slots__ = ("query", "api_key", "include_content", "scope", "model", "response_format")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_CONTENT_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FORMAT_FIELD_NUMBER: _ClassVar[int]
    query: str
    api_key: str
    include_content: bool
    scope: str
    model: str
    response_format: str
    def __init__(self, query: _Optional[str] = ..., api_key: _Optional[str] = ..., include_content: bool = ..., scope: _Optional[str] = ..., model: _Optional[str] = ..., response_format: _Optional[str] = ...) -> None: ...

class AnswerStreamRequest(_message.Message):
    __slots__ = ("query", "api_key", "include_content", "scope", "model", "response_format")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_CONTENT_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FORMAT_FIELD_NUMBER: _ClassVar[int]
    query: str
    api_key: str
    include_content: bool
    scope: str
    model: str
    response_format: str
    def __init__(self, query: _Optional[str] = ..., api_key: _Optional[str] = ..., include_content: bool = ..., scope: _Optional[str] = ..., model: _Optional[str] = ..., response_format: _Optional[str] = ...) -> None: ...

class AnswerResponse(_message.Message):
    __slots__ = ("answer", "citations")
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    CITATIONS_FIELD_NUMBER: _ClassVar[int]
    answer: str
    citations: _containers.RepeatedCompositeFieldContainer[Citation]
    def __init__(self, answer: _Optional[str] = ..., citations: _Optional[_Iterable[_Union[Citation, _Mapping]]] = ...) -> None: ...

class Citation(_message.Message):
    __slots__ = ("url", "content")
    URL_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    url: str
    content: str
    def __init__(self, url: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...

class AnswerStreamResponse(_message.Message):
    __slots__ = ("citations", "text_delta", "finish_reason")
    CITATIONS_FIELD_NUMBER: _ClassVar[int]
    TEXT_DELTA_FIELD_NUMBER: _ClassVar[int]
    FINISH_REASON_FIELD_NUMBER: _ClassVar[int]
    citations: Citations
    text_delta: str
    finish_reason: str
    def __init__(self, citations: _Optional[_Union[Citations, _Mapping]] = ..., text_delta: _Optional[str] = ..., finish_reason: _Optional[str] = ...) -> None: ...

class Citations(_message.Message):
    __slots__ = ("citations",)
    CITATIONS_FIELD_NUMBER: _ClassVar[int]
    citations: _containers.RepeatedCompositeFieldContainer[Citation]
    def __init__(self, citations: _Optional[_Iterable[_Union[Citation, _Mapping]]] = ...) -> None: ...
