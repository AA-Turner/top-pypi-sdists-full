import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal.gen.v1 import error_pb2 as _error_pb2
from nominal.scout.elements.v1 import elements_pb2 as _elements_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GroupErrors(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GROUP_ERRORS_UNAUTHORIZED: _ClassVar[GroupErrors]
    GROUP_ERRORS_NOT_FOUND: _ClassVar[GroupErrors]
    GROUP_ERRORS_REQUESTED_PAGE_SIZE_TOO_LARGE: _ClassVar[GroupErrors]
GROUP_ERRORS_UNAUTHORIZED: GroupErrors
GROUP_ERRORS_NOT_FOUND: GroupErrors
GROUP_ERRORS_REQUESTED_PAGE_SIZE_TOO_LARGE: GroupErrors

class Group(_message.Message):
    __slots__ = ("rid", "org_rid", "group_id", "display_name", "description", "user_rids", "created_at", "updated_at", "symbol")
    RID_FIELD_NUMBER: _ClassVar[int]
    ORG_RID_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    USER_RIDS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    rid: str
    org_rid: str
    group_id: str
    display_name: str
    description: str
    user_rids: _containers.RepeatedScalarFieldContainer[str]
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    symbol: _elements_pb2.Symbol
    def __init__(self, rid: _Optional[str] = ..., org_rid: _Optional[str] = ..., group_id: _Optional[str] = ..., display_name: _Optional[str] = ..., description: _Optional[str] = ..., user_rids: _Optional[_Iterable[str]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., symbol: _Optional[_Union[_elements_pb2.Symbol, _Mapping]] = ...) -> None: ...

class SearchGroupsQuery(_message.Message):
    __slots__ = ("exact_substring_text",)
    EXACT_SUBSTRING_TEXT_FIELD_NUMBER: _ClassVar[int]
    AND_FIELD_NUMBER: _ClassVar[int]
    OR_FIELD_NUMBER: _ClassVar[int]
    exact_substring_text: str
    def __init__(self, exact_substring_text: _Optional[str] = ..., **kwargs) -> None: ...

class SearchQueryAnd(_message.Message):
    __slots__ = ("queries",)
    QUERIES_FIELD_NUMBER: _ClassVar[int]
    queries: _containers.RepeatedCompositeFieldContainer[SearchGroupsQuery]
    def __init__(self, queries: _Optional[_Iterable[_Union[SearchGroupsQuery, _Mapping]]] = ...) -> None: ...

class SearchQueryOr(_message.Message):
    __slots__ = ("queries",)
    QUERIES_FIELD_NUMBER: _ClassVar[int]
    queries: _containers.RepeatedCompositeFieldContainer[SearchGroupsQuery]
    def __init__(self, queries: _Optional[_Iterable[_Union[SearchGroupsQuery, _Mapping]]] = ...) -> None: ...

class SearchGroupsRequest(_message.Message):
    __slots__ = ("page_size", "next_page_token", "query")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    next_page_token: str
    query: SearchGroupsQuery
    def __init__(self, page_size: _Optional[int] = ..., next_page_token: _Optional[str] = ..., query: _Optional[_Union[SearchGroupsQuery, _Mapping]] = ...) -> None: ...

class SearchGroupsResponse(_message.Message):
    __slots__ = ("results", "next_page_token")
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[Group]
    next_page_token: str
    def __init__(self, results: _Optional[_Iterable[_Union[Group, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class GetGroupRequest(_message.Message):
    __slots__ = ("group_rid",)
    GROUP_RID_FIELD_NUMBER: _ClassVar[int]
    group_rid: str
    def __init__(self, group_rid: _Optional[str] = ...) -> None: ...

class GetGroupResponse(_message.Message):
    __slots__ = ("group",)
    GROUP_FIELD_NUMBER: _ClassVar[int]
    group: Group
    def __init__(self, group: _Optional[_Union[Group, _Mapping]] = ...) -> None: ...

class GetGroupByIdRequest(_message.Message):
    __slots__ = ("group_id",)
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    group_id: str
    def __init__(self, group_id: _Optional[str] = ...) -> None: ...

class GetGroupByIdResponse(_message.Message):
    __slots__ = ("group",)
    GROUP_FIELD_NUMBER: _ClassVar[int]
    group: Group
    def __init__(self, group: _Optional[_Union[Group, _Mapping]] = ...) -> None: ...

class GetGroupsRequest(_message.Message):
    __slots__ = ("group_rids",)
    GROUP_RIDS_FIELD_NUMBER: _ClassVar[int]
    group_rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, group_rids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetGroupsResponse(_message.Message):
    __slots__ = ("groups",)
    class GroupsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Group
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Group, _Mapping]] = ...) -> None: ...
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    groups: _containers.MessageMap[str, Group]
    def __init__(self, groups: _Optional[_Mapping[str, Group]] = ...) -> None: ...

class UpdateGroupMetadataRequest(_message.Message):
    __slots__ = ("display_name", "description", "symbol")
    class UpdateGroupSymbolWrapper(_message.Message):
        __slots__ = ("value",)
        VALUE_FIELD_NUMBER: _ClassVar[int]
        value: _elements_pb2.Symbol
        def __init__(self, value: _Optional[_Union[_elements_pb2.Symbol, _Mapping]] = ...) -> None: ...
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    description: str
    symbol: UpdateGroupMetadataRequest.UpdateGroupSymbolWrapper
    def __init__(self, display_name: _Optional[str] = ..., description: _Optional[str] = ..., symbol: _Optional[_Union[UpdateGroupMetadataRequest.UpdateGroupSymbolWrapper, _Mapping]] = ...) -> None: ...

class UpdateGroupMetadataRequestWrapper(_message.Message):
    __slots__ = ("group_rid", "request")
    GROUP_RID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    group_rid: str
    request: UpdateGroupMetadataRequest
    def __init__(self, group_rid: _Optional[str] = ..., request: _Optional[_Union[UpdateGroupMetadataRequest, _Mapping]] = ...) -> None: ...

class UpdateGroupMetadataResponse(_message.Message):
    __slots__ = ("group",)
    GROUP_FIELD_NUMBER: _ClassVar[int]
    group: Group
    def __init__(self, group: _Optional[_Union[Group, _Mapping]] = ...) -> None: ...
