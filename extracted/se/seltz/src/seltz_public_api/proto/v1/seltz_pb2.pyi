from seltz_public_api.proto.v1 import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SearchRequest(_message.Message):
    __slots__ = ("query", "api_key", "max_results", "scope", "include_domains", "exclude_domains", "from_date", "to_date", "tier", "fields")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    MAX_RESULTS_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DOMAINS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_DOMAINS_FIELD_NUMBER: _ClassVar[int]
    FROM_DATE_FIELD_NUMBER: _ClassVar[int]
    TO_DATE_FIELD_NUMBER: _ClassVar[int]
    TIER_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    query: str
    api_key: str
    max_results: int
    scope: str
    include_domains: _containers.RepeatedScalarFieldContainer[str]
    exclude_domains: _containers.RepeatedScalarFieldContainer[str]
    from_date: str
    to_date: str
    tier: str
    fields: Fields
    def __init__(self, query: _Optional[str] = ..., api_key: _Optional[str] = ..., max_results: _Optional[int] = ..., scope: _Optional[str] = ..., include_domains: _Optional[_Iterable[str]] = ..., exclude_domains: _Optional[_Iterable[str]] = ..., from_date: _Optional[str] = ..., to_date: _Optional[str] = ..., tier: _Optional[str] = ..., fields: _Optional[_Union[Fields, _Mapping]] = ...) -> None: ...

class Fields(_message.Message):
    __slots__ = ("content_enabled", "content_options", "snippets_enabled", "snippet_options")
    CONTENT_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CONTENT_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    SNIPPETS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SNIPPET_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    content_enabled: bool
    content_options: ContentOptions
    snippets_enabled: bool
    snippet_options: SnippetOptions
    def __init__(self, content_enabled: bool = ..., content_options: _Optional[_Union[ContentOptions, _Mapping]] = ..., snippets_enabled: bool = ..., snippet_options: _Optional[_Union[SnippetOptions, _Mapping]] = ...) -> None: ...

class Document(_message.Message):
    __slots__ = ("url", "content", "published_date", "snippets")
    URL_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    PUBLISHED_DATE_FIELD_NUMBER: _ClassVar[int]
    SNIPPETS_FIELD_NUMBER: _ClassVar[int]
    url: str
    content: str
    published_date: str
    snippets: _containers.RepeatedCompositeFieldContainer[Snippet]
    def __init__(self, url: _Optional[str] = ..., content: _Optional[str] = ..., published_date: _Optional[str] = ..., snippets: _Optional[_Iterable[_Union[Snippet, _Mapping]]] = ...) -> None: ...

class ContentOptions(_message.Message):
    __slots__ = ("max_characters_per_result",)
    MAX_CHARACTERS_PER_RESULT_FIELD_NUMBER: _ClassVar[int]
    max_characters_per_result: int
    def __init__(self, max_characters_per_result: _Optional[int] = ...) -> None: ...

class SnippetOptions(_message.Message):
    __slots__ = ("max_snippets", "max_snippets_per_result", "max_tokens", "max_tokens_per_result")
    MAX_SNIPPETS_FIELD_NUMBER: _ClassVar[int]
    MAX_SNIPPETS_PER_RESULT_FIELD_NUMBER: _ClassVar[int]
    MAX_TOKENS_FIELD_NUMBER: _ClassVar[int]
    MAX_TOKENS_PER_RESULT_FIELD_NUMBER: _ClassVar[int]
    max_snippets: int
    max_snippets_per_result: int
    max_tokens: int
    max_tokens_per_result: int
    def __init__(self, max_snippets: _Optional[int] = ..., max_snippets_per_result: _Optional[int] = ..., max_tokens: _Optional[int] = ..., max_tokens_per_result: _Optional[int] = ...) -> None: ...

class Snippet(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...

class SearchResponse(_message.Message):
    __slots__ = ("documents",)
    DOCUMENTS_FIELD_NUMBER: _ClassVar[int]
    documents: _containers.RepeatedCompositeFieldContainer[Document]
    def __init__(self, documents: _Optional[_Iterable[_Union[Document, _Mapping]]] = ...) -> None: ...
