import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from nominal_api_protos.nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal_api_protos.nominal.registry.v1 import registry_pb2 as _registry_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ContainerizedExtractor(_message.Message):
    __slots__ = ("rid", "workspace_rid", "name", "description", "created_at", "is_archived", "active_container_image")
    RID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    IS_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_CONTAINER_IMAGE_FIELD_NUMBER: _ClassVar[int]
    rid: str
    workspace_rid: str
    name: str
    description: str
    created_at: _timestamp_pb2.Timestamp
    is_archived: bool
    active_container_image: _registry_pb2.ContainerImage
    def __init__(self, rid: _Optional[str] = ..., workspace_rid: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., is_archived: bool = ..., active_container_image: _Optional[_Union[_registry_pb2.ContainerImage, _Mapping]] = ...) -> None: ...

class CreateContainerizedExtractorRequest(_message.Message):
    __slots__ = ("workspace_rid", "name", "description")
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    workspace_rid: str
    name: str
    description: str
    def __init__(self, workspace_rid: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class CreateContainerizedExtractorResponse(_message.Message):
    __slots__ = ("extractor",)
    EXTRACTOR_FIELD_NUMBER: _ClassVar[int]
    extractor: ContainerizedExtractor
    def __init__(self, extractor: _Optional[_Union[ContainerizedExtractor, _Mapping]] = ...) -> None: ...

class GetContainerizedExtractorRequest(_message.Message):
    __slots__ = ("rid", "workspace_rid")
    RID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    rid: str
    workspace_rid: str
    def __init__(self, rid: _Optional[str] = ..., workspace_rid: _Optional[str] = ...) -> None: ...

class GetContainerizedExtractorResponse(_message.Message):
    __slots__ = ("extractor",)
    EXTRACTOR_FIELD_NUMBER: _ClassVar[int]
    extractor: ContainerizedExtractor
    def __init__(self, extractor: _Optional[_Union[ContainerizedExtractor, _Mapping]] = ...) -> None: ...

class UpdateContainerizedExtractorRequest(_message.Message):
    __slots__ = ("rid", "workspace_rid", "name", "description", "is_archived", "active_container_image_rid")
    RID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IS_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_CONTAINER_IMAGE_RID_FIELD_NUMBER: _ClassVar[int]
    rid: str
    workspace_rid: str
    name: str
    description: str
    is_archived: bool
    active_container_image_rid: str
    def __init__(self, rid: _Optional[str] = ..., workspace_rid: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., is_archived: bool = ..., active_container_image_rid: _Optional[str] = ...) -> None: ...

class UpdateContainerizedExtractorResponse(_message.Message):
    __slots__ = ("extractor",)
    EXTRACTOR_FIELD_NUMBER: _ClassVar[int]
    extractor: ContainerizedExtractor
    def __init__(self, extractor: _Optional[_Union[ContainerizedExtractor, _Mapping]] = ...) -> None: ...

class SearchContainerizedExtractorsRequest(_message.Message):
    __slots__ = ("workspace_rid", "include_archived", "page_size", "next_page_token")
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    workspace_rid: str
    include_archived: bool
    page_size: int
    next_page_token: str
    def __init__(self, workspace_rid: _Optional[str] = ..., include_archived: bool = ..., page_size: _Optional[int] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class SearchContainerizedExtractorsResponse(_message.Message):
    __slots__ = ("extractors", "next_page_token")
    EXTRACTORS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    extractors: _containers.RepeatedCompositeFieldContainer[ContainerizedExtractor]
    next_page_token: str
    def __init__(self, extractors: _Optional[_Iterable[_Union[ContainerizedExtractor, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...
