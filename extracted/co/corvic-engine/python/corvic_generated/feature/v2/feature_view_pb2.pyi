from buf.validate import validate_pb2 as _validate_pb2
from corvic_generated.ingest.v2 import source_pb2 as _source_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OutputEntity(_message.Message):
    __slots__ = ("name", "source_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    source_id: str
    def __init__(self, name: _Optional[str] = ..., source_id: _Optional[str] = ...) -> None: ...

class OutputEntities(_message.Message):
    __slots__ = ("output_entities",)
    OUTPUT_ENTITIES_FIELD_NUMBER: _ClassVar[int]
    output_entities: _containers.RepeatedCompositeFieldContainer[OutputEntity]
    def __init__(self, output_entities: _Optional[_Iterable[_Union[OutputEntity, _Mapping]]] = ...) -> None: ...

class OutputSource(_message.Message):
    __slots__ = ("source_id",)
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    source_id: str
    def __init__(self, source_id: _Optional[str] = ...) -> None: ...

class FeatureViewEntry(_message.Message):
    __slots__ = ("id", "room_id", "source_entries", "name", "description", "output_sources")
    ID_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SOURCES_FIELD_NUMBER: _ClassVar[int]
    id: str
    room_id: str
    source_entries: _containers.RepeatedCompositeFieldContainer[_source_pb2.SourceEntry]
    name: str
    description: str
    output_sources: _containers.RepeatedCompositeFieldContainer[OutputSource]
    def __init__(self, id: _Optional[str] = ..., room_id: _Optional[str] = ..., source_entries: _Optional[_Iterable[_Union[_source_pb2.SourceEntry, _Mapping]]] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., output_sources: _Optional[_Iterable[_Union[OutputSource, _Mapping]]] = ...) -> None: ...

class GetFeatureViewRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetFeatureViewResponse(_message.Message):
    __slots__ = ("feature_view_entry",)
    FEATURE_VIEW_ENTRY_FIELD_NUMBER: _ClassVar[int]
    feature_view_entry: FeatureViewEntry
    def __init__(self, feature_view_entry: _Optional[_Union[FeatureViewEntry, _Mapping]] = ...) -> None: ...

class ListFeatureViewsRequest(_message.Message):
    __slots__ = ("room_id",)
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    def __init__(self, room_id: _Optional[str] = ...) -> None: ...

class ListFeatureViewsResponse(_message.Message):
    __slots__ = ("feature_view_entries",)
    FEATURE_VIEW_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    feature_view_entries: _containers.RepeatedCompositeFieldContainer[FeatureViewEntry]
    def __init__(self, feature_view_entries: _Optional[_Iterable[_Union[FeatureViewEntry, _Mapping]]] = ...) -> None: ...

class CreateFeatureViewRequest(_message.Message):
    __slots__ = ("room_id", "name", "description", "source_ids", "output_sources")
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SOURCE_IDS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SOURCES_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    name: str
    description: str
    source_ids: _containers.RepeatedScalarFieldContainer[str]
    output_sources: _containers.RepeatedCompositeFieldContainer[OutputSource]
    def __init__(self, room_id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., source_ids: _Optional[_Iterable[str]] = ..., output_sources: _Optional[_Iterable[_Union[OutputSource, _Mapping]]] = ...) -> None: ...

class CreateFeatureViewResponse(_message.Message):
    __slots__ = ("feature_view_entry",)
    FEATURE_VIEW_ENTRY_FIELD_NUMBER: _ClassVar[int]
    feature_view_entry: FeatureViewEntry
    def __init__(self, feature_view_entry: _Optional[_Union[FeatureViewEntry, _Mapping]] = ...) -> None: ...

class DeleteFeatureViewRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteFeatureViewResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetFeatureViewRelationshipsRequest(_message.Message):
    __slots__ = ("source_ids", "output_sources")
    SOURCE_IDS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SOURCES_FIELD_NUMBER: _ClassVar[int]
    source_ids: _containers.RepeatedScalarFieldContainer[str]
    output_sources: _containers.RepeatedCompositeFieldContainer[OutputSource]
    def __init__(self, source_ids: _Optional[_Iterable[str]] = ..., output_sources: _Optional[_Iterable[_Union[OutputSource, _Mapping]]] = ...) -> None: ...

class SourceRelationship(_message.Message):
    __slots__ = ("relationship_path_source_ids",)
    RELATIONSHIP_PATH_SOURCE_IDS_FIELD_NUMBER: _ClassVar[int]
    relationship_path_source_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, relationship_path_source_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetFeatureViewRelationshipsResponse(_message.Message):
    __slots__ = ("source_relationships",)
    SOURCE_RELATIONSHIPS_FIELD_NUMBER: _ClassVar[int]
    source_relationships: _containers.RepeatedCompositeFieldContainer[SourceRelationship]
    def __init__(self, source_relationships: _Optional[_Iterable[_Union[SourceRelationship, _Mapping]]] = ...) -> None: ...
