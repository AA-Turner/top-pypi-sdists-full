from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TopLogprobs(_message.Message):
    __slots__ = ("rows", "width", "token_ids", "logprobs", "row_counts")
    ROWS_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IDS_FIELD_NUMBER: _ClassVar[int]
    LOGPROBS_FIELD_NUMBER: _ClassVar[int]
    ROW_COUNTS_FIELD_NUMBER: _ClassVar[int]
    rows: int
    width: int
    token_ids: bytes
    logprobs: bytes
    row_counts: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, rows: _Optional[int] = ..., width: _Optional[int] = ..., token_ids: _Optional[bytes] = ..., logprobs: _Optional[bytes] = ..., row_counts: _Optional[_Iterable[int]] = ...) -> None: ...

class NativeGenerateItem(_message.Message):
    __slots__ = ("metadata_json", "top_logprobs", "prompt_top_logprobs")
    METADATA_JSON_FIELD_NUMBER: _ClassVar[int]
    TOP_LOGPROBS_FIELD_NUMBER: _ClassVar[int]
    PROMPT_TOP_LOGPROBS_FIELD_NUMBER: _ClassVar[int]
    metadata_json: bytes
    top_logprobs: TopLogprobs
    prompt_top_logprobs: TopLogprobs
    def __init__(self, metadata_json: _Optional[bytes] = ..., top_logprobs: _Optional[_Union[TopLogprobs, _Mapping]] = ..., prompt_top_logprobs: _Optional[_Union[TopLogprobs, _Mapping]] = ...) -> None: ...

class NativeGenerateFrame(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[NativeGenerateItem]
    def __init__(self, results: _Optional[_Iterable[_Union[NativeGenerateItem, _Mapping]]] = ...) -> None: ...
