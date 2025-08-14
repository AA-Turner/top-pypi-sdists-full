import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal.scout.elements.v1 import elements_pb2 as _elements_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuthorizedGroups(_message.Message):
    __slots__ = ("group_rids",)
    GROUP_RIDS_FIELD_NUMBER: _ClassVar[int]
    group_rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, group_rids: _Optional[_Iterable[str]] = ...) -> None: ...

class Marking(_message.Message):
    __slots__ = ("rid", "id", "description", "authorized_groups", "symbol", "color", "created_at", "updated_at", "is_archived")
    RID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZED_GROUPS_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    IS_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    rid: str
    id: str
    description: str
    authorized_groups: AuthorizedGroups
    symbol: _elements_pb2.Symbol
    color: _elements_pb2.Color
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    is_archived: bool
    def __init__(self, rid: _Optional[str] = ..., id: _Optional[str] = ..., description: _Optional[str] = ..., authorized_groups: _Optional[_Union[AuthorizedGroups, _Mapping]] = ..., symbol: _Optional[_Union[_elements_pb2.Symbol, _Mapping]] = ..., color: _Optional[_Union[_elements_pb2.Color, _Mapping]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., is_archived: bool = ...) -> None: ...

class MarkingMetadata(_message.Message):
    __slots__ = ("rid", "id", "description", "symbol", "color", "created_at", "updated_at", "is_archived")
    RID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    IS_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    rid: str
    id: str
    description: str
    symbol: _elements_pb2.Symbol
    color: _elements_pb2.Color
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    is_archived: bool
    def __init__(self, rid: _Optional[str] = ..., id: _Optional[str] = ..., description: _Optional[str] = ..., symbol: _Optional[_Union[_elements_pb2.Symbol, _Mapping]] = ..., color: _Optional[_Union[_elements_pb2.Color, _Mapping]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., is_archived: bool = ...) -> None: ...

class CreateMarkingRequest(_message.Message):
    __slots__ = ("id", "description", "authorized_groups", "symbol", "color")
    ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZED_GROUPS_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    description: str
    authorized_groups: AuthorizedGroups
    symbol: _elements_pb2.Symbol
    color: _elements_pb2.Color
    def __init__(self, id: _Optional[str] = ..., description: _Optional[str] = ..., authorized_groups: _Optional[_Union[AuthorizedGroups, _Mapping]] = ..., symbol: _Optional[_Union[_elements_pb2.Symbol, _Mapping]] = ..., color: _Optional[_Union[_elements_pb2.Color, _Mapping]] = ...) -> None: ...

class CreateMarkingResponse(_message.Message):
    __slots__ = ("marking",)
    MARKING_FIELD_NUMBER: _ClassVar[int]
    marking: Marking
    def __init__(self, marking: _Optional[_Union[Marking, _Mapping]] = ...) -> None: ...

class GetMarkingRequest(_message.Message):
    __slots__ = ("rid",)
    RID_FIELD_NUMBER: _ClassVar[int]
    rid: str
    def __init__(self, rid: _Optional[str] = ...) -> None: ...

class GetMarkingResponse(_message.Message):
    __slots__ = ("marking",)
    MARKING_FIELD_NUMBER: _ClassVar[int]
    marking: Marking
    def __init__(self, marking: _Optional[_Union[Marking, _Mapping]] = ...) -> None: ...

class GetMarkingByIdRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetMarkingByIdResponse(_message.Message):
    __slots__ = ("marking",)
    MARKING_FIELD_NUMBER: _ClassVar[int]
    marking: Marking
    def __init__(self, marking: _Optional[_Union[Marking, _Mapping]] = ...) -> None: ...

class BatchGetMarkingsRequest(_message.Message):
    __slots__ = ("marking_rids",)
    MARKING_RIDS_FIELD_NUMBER: _ClassVar[int]
    marking_rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, marking_rids: _Optional[_Iterable[str]] = ...) -> None: ...

class BatchGetMarkingsResponse(_message.Message):
    __slots__ = ("markings",)
    MARKINGS_FIELD_NUMBER: _ClassVar[int]
    markings: _containers.RepeatedCompositeFieldContainer[Marking]
    def __init__(self, markings: _Optional[_Iterable[_Union[Marking, _Mapping]]] = ...) -> None: ...

class BatchGetMarkingMetadataRequest(_message.Message):
    __slots__ = ("marking_rids",)
    MARKING_RIDS_FIELD_NUMBER: _ClassVar[int]
    marking_rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, marking_rids: _Optional[_Iterable[str]] = ...) -> None: ...

class BatchGetMarkingMetadataResponse(_message.Message):
    __slots__ = ("marking_metadatas",)
    MARKING_METADATAS_FIELD_NUMBER: _ClassVar[int]
    marking_metadatas: _containers.RepeatedCompositeFieldContainer[MarkingMetadata]
    def __init__(self, marking_metadatas: _Optional[_Iterable[_Union[MarkingMetadata, _Mapping]]] = ...) -> None: ...

class GetAuthorizedGroupsByMarkingRequest(_message.Message):
    __slots__ = ("marking_rids",)
    MARKING_RIDS_FIELD_NUMBER: _ClassVar[int]
    marking_rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, marking_rids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetAuthorizedGroupsByMarkingResponse(_message.Message):
    __slots__ = ("authorized_groups_by_marking",)
    class AuthorizedGroupsByMarkingEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: AuthorizedGroups
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[AuthorizedGroups, _Mapping]] = ...) -> None: ...
    AUTHORIZED_GROUPS_BY_MARKING_FIELD_NUMBER: _ClassVar[int]
    authorized_groups_by_marking: _containers.MessageMap[str, AuthorizedGroups]
    def __init__(self, authorized_groups_by_marking: _Optional[_Mapping[str, AuthorizedGroups]] = ...) -> None: ...

class SearchMarkingsQuery(_message.Message):
    __slots__ = ("id_exact_substring_search",)
    ID_EXACT_SUBSTRING_SEARCH_FIELD_NUMBER: _ClassVar[int]
    AND_FIELD_NUMBER: _ClassVar[int]
    OR_FIELD_NUMBER: _ClassVar[int]
    id_exact_substring_search: str
    def __init__(self, id_exact_substring_search: _Optional[str] = ..., **kwargs) -> None: ...

class SearchMarkingsQueryList(_message.Message):
    __slots__ = ("queries",)
    QUERIES_FIELD_NUMBER: _ClassVar[int]
    queries: _containers.RepeatedCompositeFieldContainer[SearchMarkingsQuery]
    def __init__(self, queries: _Optional[_Iterable[_Union[SearchMarkingsQuery, _Mapping]]] = ...) -> None: ...

class SearchMarkingsRequest(_message.Message):
    __slots__ = ("query", "page_size", "next_page_token")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    query: SearchMarkingsQuery
    page_size: int
    next_page_token: str
    def __init__(self, query: _Optional[_Union[SearchMarkingsQuery, _Mapping]] = ..., page_size: _Optional[int] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class SearchMarkingsResponse(_message.Message):
    __slots__ = ("marking_metadatas", "next_page_token")
    MARKING_METADATAS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    marking_metadatas: _containers.RepeatedCompositeFieldContainer[MarkingMetadata]
    next_page_token: str
    def __init__(self, marking_metadatas: _Optional[_Iterable[_Union[MarkingMetadata, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class UpdateMarkingRequest(_message.Message):
    __slots__ = ("rid", "id", "description", "authorized_groups", "symbol", "color")
    class UpdateMarkingSymbolWrapper(_message.Message):
        __slots__ = ("value",)
        VALUE_FIELD_NUMBER: _ClassVar[int]
        value: _elements_pb2.Symbol
        def __init__(self, value: _Optional[_Union[_elements_pb2.Symbol, _Mapping]] = ...) -> None: ...
    class UpdateMarkingColorWrapper(_message.Message):
        __slots__ = ("value",)
        VALUE_FIELD_NUMBER: _ClassVar[int]
        value: _elements_pb2.Color
        def __init__(self, value: _Optional[_Union[_elements_pb2.Color, _Mapping]] = ...) -> None: ...
    RID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZED_GROUPS_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    rid: str
    id: str
    description: str
    authorized_groups: AuthorizedGroups
    symbol: UpdateMarkingRequest.UpdateMarkingSymbolWrapper
    color: UpdateMarkingRequest.UpdateMarkingColorWrapper
    def __init__(self, rid: _Optional[str] = ..., id: _Optional[str] = ..., description: _Optional[str] = ..., authorized_groups: _Optional[_Union[AuthorizedGroups, _Mapping]] = ..., symbol: _Optional[_Union[UpdateMarkingRequest.UpdateMarkingSymbolWrapper, _Mapping]] = ..., color: _Optional[_Union[UpdateMarkingRequest.UpdateMarkingColorWrapper, _Mapping]] = ...) -> None: ...

class UpdateMarkingResponse(_message.Message):
    __slots__ = ("marking",)
    MARKING_FIELD_NUMBER: _ClassVar[int]
    marking: Marking
    def __init__(self, marking: _Optional[_Union[Marking, _Mapping]] = ...) -> None: ...

class ArchiveMarkingsRequest(_message.Message):
    __slots__ = ("marking_rids",)
    MARKING_RIDS_FIELD_NUMBER: _ClassVar[int]
    marking_rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, marking_rids: _Optional[_Iterable[str]] = ...) -> None: ...

class ArchiveMarkingsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UnarchiveMarkingsRequest(_message.Message):
    __slots__ = ("marking_rids",)
    MARKING_RIDS_FIELD_NUMBER: _ClassVar[int]
    marking_rids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, marking_rids: _Optional[_Iterable[str]] = ...) -> None: ...

class UnarchiveMarkingsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdateMarkingsOnResourceRequest(_message.Message):
    __slots__ = ("resource", "markings_to_apply", "markings_to_remove")
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    MARKINGS_TO_APPLY_FIELD_NUMBER: _ClassVar[int]
    MARKINGS_TO_REMOVE_FIELD_NUMBER: _ClassVar[int]
    resource: str
    markings_to_apply: _containers.RepeatedScalarFieldContainer[str]
    markings_to_remove: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, resource: _Optional[str] = ..., markings_to_apply: _Optional[_Iterable[str]] = ..., markings_to_remove: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateMarkingsOnResourceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetResourcesForMarkingRequest(_message.Message):
    __slots__ = ("marking_rid", "page_size", "next_page_token")
    MARKING_RID_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    marking_rid: str
    page_size: int
    next_page_token: str
    def __init__(self, marking_rid: _Optional[str] = ..., page_size: _Optional[int] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class GetResourcesForMarkingResponse(_message.Message):
    __slots__ = ("resources", "next_page_token")
    class MarkedResource(_message.Message):
        __slots__ = ("resource", "applied_at")
        RESOURCE_FIELD_NUMBER: _ClassVar[int]
        APPLIED_AT_FIELD_NUMBER: _ClassVar[int]
        resource: str
        applied_at: _timestamp_pb2.Timestamp
        def __init__(self, resource: _Optional[str] = ..., applied_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    resources: _containers.RepeatedCompositeFieldContainer[GetResourcesForMarkingResponse.MarkedResource]
    next_page_token: str
    def __init__(self, resources: _Optional[_Iterable[_Union[GetResourcesForMarkingResponse.MarkedResource, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class GetMarkingsForResourcesRequest(_message.Message):
    __slots__ = ("resources",)
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    resources: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, resources: _Optional[_Iterable[str]] = ...) -> None: ...

class GetMarkingsForResourcesResponse(_message.Message):
    __slots__ = ("resource_to_markings",)
    class ResourceToMarkingsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: GetMarkingsForResourcesResponse.ResourceMarkingsList
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[GetMarkingsForResourcesResponse.ResourceMarkingsList, _Mapping]] = ...) -> None: ...
    class ResourceMarkingsList(_message.Message):
        __slots__ = ("applied_markings",)
        class AppliedMarking(_message.Message):
            __slots__ = ("marking_rid", "applied_at")
            MARKING_RID_FIELD_NUMBER: _ClassVar[int]
            APPLIED_AT_FIELD_NUMBER: _ClassVar[int]
            marking_rid: str
            applied_at: _timestamp_pb2.Timestamp
            def __init__(self, marking_rid: _Optional[str] = ..., applied_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
        APPLIED_MARKINGS_FIELD_NUMBER: _ClassVar[int]
        applied_markings: _containers.RepeatedCompositeFieldContainer[GetMarkingsForResourcesResponse.ResourceMarkingsList.AppliedMarking]
        def __init__(self, applied_markings: _Optional[_Iterable[_Union[GetMarkingsForResourcesResponse.ResourceMarkingsList.AppliedMarking, _Mapping]]] = ...) -> None: ...
    RESOURCE_TO_MARKINGS_FIELD_NUMBER: _ClassVar[int]
    resource_to_markings: _containers.MessageMap[str, GetMarkingsForResourcesResponse.ResourceMarkingsList]
    def __init__(self, resource_to_markings: _Optional[_Mapping[str, GetMarkingsForResourcesResponse.ResourceMarkingsList]] = ...) -> None: ...
