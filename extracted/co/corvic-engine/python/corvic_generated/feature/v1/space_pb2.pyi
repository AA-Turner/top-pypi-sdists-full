from buf.validate import validate_pb2 as _validate_pb2
from corvic_generated.ingest.v2 import source_pb2 as _source_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OutputEntityOperator(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OUTPUT_ENTITY_OPERATOR_UNSPECIFIED: _ClassVar[OutputEntityOperator]
    OUTPUT_ENTITY_OPERATOR_CONJUNCTION: _ClassVar[OutputEntityOperator]
    OUTPUT_ENTITY_OPERATOR_DISJUNCTION: _ClassVar[OutputEntityOperator]
OUTPUT_ENTITY_OPERATOR_UNSPECIFIED: OutputEntityOperator
OUTPUT_ENTITY_OPERATOR_CONJUNCTION: OutputEntityOperator
OUTPUT_ENTITY_OPERATOR_DISJUNCTION: OutputEntityOperator

class OutputEntity(_message.Message):
    __slots__ = ("name", "source_id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    source_id: str
    def __init__(self, name: _Optional[str] = ..., source_id: _Optional[str] = ...) -> None: ...

class SpaceOutput(_message.Message):
    __slots__ = ("output_entity_operator", "output_entities")
    OUTPUT_ENTITY_OPERATOR_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_ENTITIES_FIELD_NUMBER: _ClassVar[int]
    output_entity_operator: OutputEntityOperator
    output_entities: _containers.RepeatedCompositeFieldContainer[OutputEntity]
    def __init__(self, output_entity_operator: _Optional[_Union[OutputEntityOperator, str]] = ..., output_entities: _Optional[_Iterable[_Union[OutputEntity, _Mapping]]] = ...) -> None: ...

class SpaceEntry(_message.Message):
    __slots__ = ("id", "org_id", "room_id", "source_entries", "name", "description", "space_output")
    ID_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SPACE_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    id: str
    org_id: str
    room_id: str
    source_entries: _containers.RepeatedCompositeFieldContainer[_source_pb2.SourceEntry]
    name: str
    description: str
    space_output: SpaceOutput
    def __init__(self, id: _Optional[str] = ..., org_id: _Optional[str] = ..., room_id: _Optional[str] = ..., source_entries: _Optional[_Iterable[_Union[_source_pb2.SourceEntry, _Mapping]]] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., space_output: _Optional[_Union[SpaceOutput, _Mapping]] = ...) -> None: ...

class GetSpaceRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetSpaceResponse(_message.Message):
    __slots__ = ("space_entry",)
    SPACE_ENTRY_FIELD_NUMBER: _ClassVar[int]
    space_entry: SpaceEntry
    def __init__(self, space_entry: _Optional[_Union[SpaceEntry, _Mapping]] = ...) -> None: ...

class ListSpacesRequest(_message.Message):
    __slots__ = ("room_id",)
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    def __init__(self, room_id: _Optional[str] = ...) -> None: ...

class ListSpacesResponse(_message.Message):
    __slots__ = ("space_entries",)
    SPACE_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    space_entries: _containers.RepeatedCompositeFieldContainer[SpaceEntry]
    def __init__(self, space_entries: _Optional[_Iterable[_Union[SpaceEntry, _Mapping]]] = ...) -> None: ...

class CreateSpaceRequest(_message.Message):
    __slots__ = ("room_id", "name", "description", "source_ids", "space_output")
    ROOM_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SOURCE_IDS_FIELD_NUMBER: _ClassVar[int]
    SPACE_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    room_id: str
    name: str
    description: str
    source_ids: _containers.RepeatedScalarFieldContainer[str]
    space_output: SpaceOutput
    def __init__(self, room_id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., source_ids: _Optional[_Iterable[str]] = ..., space_output: _Optional[_Union[SpaceOutput, _Mapping]] = ...) -> None: ...

class CreateSpaceResponse(_message.Message):
    __slots__ = ("space_entry",)
    SPACE_ENTRY_FIELD_NUMBER: _ClassVar[int]
    space_entry: SpaceEntry
    def __init__(self, space_entry: _Optional[_Union[SpaceEntry, _Mapping]] = ...) -> None: ...

class DeleteSpaceRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteSpaceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetSpaceRelationshipsRequest(_message.Message):
    __slots__ = ("source_ids", "space_output")
    SOURCE_IDS_FIELD_NUMBER: _ClassVar[int]
    SPACE_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    source_ids: _containers.RepeatedScalarFieldContainer[str]
    space_output: SpaceOutput
    def __init__(self, source_ids: _Optional[_Iterable[str]] = ..., space_output: _Optional[_Union[SpaceOutput, _Mapping]] = ...) -> None: ...

class SourceRelationship(_message.Message):
    __slots__ = ("source_entry_start", "source_entry_end", "start_source_id", "end_source_id", "relationship_path_sources")
    SOURCE_ENTRY_START_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ENTRY_END_FIELD_NUMBER: _ClassVar[int]
    START_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    END_SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    RELATIONSHIP_PATH_SOURCES_FIELD_NUMBER: _ClassVar[int]
    source_entry_start: _source_pb2.SourceEntry
    source_entry_end: _source_pb2.SourceEntry
    start_source_id: str
    end_source_id: str
    relationship_path_sources: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, source_entry_start: _Optional[_Union[_source_pb2.SourceEntry, _Mapping]] = ..., source_entry_end: _Optional[_Union[_source_pb2.SourceEntry, _Mapping]] = ..., start_source_id: _Optional[str] = ..., end_source_id: _Optional[str] = ..., relationship_path_sources: _Optional[_Iterable[str]] = ...) -> None: ...

class GetSpaceRelationshipsResponse(_message.Message):
    __slots__ = ("source_relationships",)
    SOURCE_RELATIONSHIPS_FIELD_NUMBER: _ClassVar[int]
    source_relationships: _containers.RepeatedCompositeFieldContainer[SourceRelationship]
    def __init__(self, source_relationships: _Optional[_Iterable[_Union[SourceRelationship, _Mapping]]] = ...) -> None: ...
