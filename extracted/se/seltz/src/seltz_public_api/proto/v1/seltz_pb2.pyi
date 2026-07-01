from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SearchRequest(_message.Message):
    __slots__ = ("query", "api_key", "max_results", "scope", "include_domains", "exclude_domains", "from_date", "to_date")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    MAX_RESULTS_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DOMAINS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_DOMAINS_FIELD_NUMBER: _ClassVar[int]
    FROM_DATE_FIELD_NUMBER: _ClassVar[int]
    TO_DATE_FIELD_NUMBER: _ClassVar[int]
    query: str
    api_key: str
    max_results: int
    scope: str
    include_domains: _containers.RepeatedScalarFieldContainer[str]
    exclude_domains: _containers.RepeatedScalarFieldContainer[str]
    from_date: str
    to_date: str
    def __init__(self, query: _Optional[str] = ..., api_key: _Optional[str] = ..., max_results: _Optional[int] = ..., scope: _Optional[str] = ..., include_domains: _Optional[_Iterable[str]] = ..., exclude_domains: _Optional[_Iterable[str]] = ..., from_date: _Optional[str] = ..., to_date: _Optional[str] = ...) -> None: ...

class Document(_message.Message):
    __slots__ = ("url", "content", "published_date")
    URL_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    PUBLISHED_DATE_FIELD_NUMBER: _ClassVar[int]
    url: str
    content: str
    published_date: str
    def __init__(self, url: _Optional[str] = ..., content: _Optional[str] = ..., published_date: _Optional[str] = ...) -> None: ...

class SearchResponse(_message.Message):
    __slots__ = ("documents",)
    DOCUMENTS_FIELD_NUMBER: _ClassVar[int]
    documents: _containers.RepeatedCompositeFieldContainer[Document]
    def __init__(self, documents: _Optional[_Iterable[_Union[Document, _Mapping]]] = ...) -> None: ...
