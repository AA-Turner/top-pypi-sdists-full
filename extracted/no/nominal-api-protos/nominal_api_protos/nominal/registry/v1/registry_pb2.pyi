import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from nominal_api_protos.nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal_api_protos.nominal.types.time import timestamp_parsers_pb2 as _timestamp_parsers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ContainerImageStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONTAINER_IMAGE_STATUS_UNSPECIFIED: _ClassVar[ContainerImageStatus]
    CONTAINER_IMAGE_STATUS_PENDING: _ClassVar[ContainerImageStatus]
    CONTAINER_IMAGE_STATUS_READY: _ClassVar[ContainerImageStatus]
    CONTAINER_IMAGE_STATUS_FAILED: _ClassVar[ContainerImageStatus]

class FileOutputFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FILE_OUTPUT_FORMAT_UNSPECIFIED: _ClassVar[FileOutputFormat]
    FILE_OUTPUT_FORMAT_PARQUET: _ClassVar[FileOutputFormat]
    FILE_OUTPUT_FORMAT_CSV: _ClassVar[FileOutputFormat]
    FILE_OUTPUT_FORMAT_PARQUET_TAR: _ClassVar[FileOutputFormat]
    FILE_OUTPUT_FORMAT_AVRO_STREAM: _ClassVar[FileOutputFormat]
    FILE_OUTPUT_FORMAT_JSON_L: _ClassVar[FileOutputFormat]
    FILE_OUTPUT_FORMAT_MANIFEST: _ClassVar[FileOutputFormat]
CONTAINER_IMAGE_STATUS_UNSPECIFIED: ContainerImageStatus
CONTAINER_IMAGE_STATUS_PENDING: ContainerImageStatus
CONTAINER_IMAGE_STATUS_READY: ContainerImageStatus
CONTAINER_IMAGE_STATUS_FAILED: ContainerImageStatus
FILE_OUTPUT_FORMAT_UNSPECIFIED: FileOutputFormat
FILE_OUTPUT_FORMAT_PARQUET: FileOutputFormat
FILE_OUTPUT_FORMAT_CSV: FileOutputFormat
FILE_OUTPUT_FORMAT_PARQUET_TAR: FileOutputFormat
FILE_OUTPUT_FORMAT_AVRO_STREAM: FileOutputFormat
FILE_OUTPUT_FORMAT_JSON_L: FileOutputFormat
FILE_OUTPUT_FORMAT_MANIFEST: FileOutputFormat

class FileSuffix(_message.Message):
    __slots__ = ("suffix",)
    SUFFIX_FIELD_NUMBER: _ClassVar[int]
    suffix: str
    def __init__(self, suffix: _Optional[str] = ...) -> None: ...

class FileFilter(_message.Message):
    __slots__ = ("suffix",)
    SUFFIX_FIELD_NUMBER: _ClassVar[int]
    suffix: FileSuffix
    def __init__(self, suffix: _Optional[_Union[FileSuffix, _Mapping]] = ...) -> None: ...

class FileExtractionInput(_message.Message):
    __slots__ = ("environment_variable", "name", "description", "file_filters", "required")
    ENVIRONMENT_VARIABLE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FILE_FILTERS_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_FIELD_NUMBER: _ClassVar[int]
    environment_variable: str
    name: str
    description: str
    file_filters: _containers.RepeatedCompositeFieldContainer[FileFilter]
    required: bool
    def __init__(self, environment_variable: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., file_filters: _Optional[_Iterable[_Union[FileFilter, _Mapping]]] = ..., required: bool = ...) -> None: ...

class FileExtractionParameter(_message.Message):
    __slots__ = ("environment_variable", "name", "description", "required")
    ENVIRONMENT_VARIABLE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_FIELD_NUMBER: _ClassVar[int]
    environment_variable: str
    name: str
    description: str
    required: bool
    def __init__(self, environment_variable: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., required: bool = ...) -> None: ...

class TimestampMetadata(_message.Message):
    __slots__ = ("series_name", "timestamp_type")
    SERIES_NAME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_TYPE_FIELD_NUMBER: _ClassVar[int]
    series_name: str
    timestamp_type: _timestamp_parsers_pb2.TimestampType
    def __init__(self, series_name: _Optional[str] = ..., timestamp_type: _Optional[_Union[_timestamp_parsers_pb2.TimestampType, _Mapping]] = ...) -> None: ...

class ContainerImage(_message.Message):
    __slots__ = ("rid", "name", "tag", "size_bytes", "status", "created_at", "extractor_rid", "inputs", "parameters", "file_output_format", "default_timestamp_metadata")
    RID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    EXTRACTOR_RID_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    FILE_OUTPUT_FORMAT_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_TIMESTAMP_METADATA_FIELD_NUMBER: _ClassVar[int]
    rid: str
    name: str
    tag: str
    size_bytes: int
    status: ContainerImageStatus
    created_at: _timestamp_pb2.Timestamp
    extractor_rid: str
    inputs: _containers.RepeatedCompositeFieldContainer[FileExtractionInput]
    parameters: _containers.RepeatedCompositeFieldContainer[FileExtractionParameter]
    file_output_format: FileOutputFormat
    default_timestamp_metadata: TimestampMetadata
    def __init__(self, rid: _Optional[str] = ..., name: _Optional[str] = ..., tag: _Optional[str] = ..., size_bytes: _Optional[int] = ..., status: _Optional[_Union[ContainerImageStatus, str]] = ..., created_at: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., extractor_rid: _Optional[str] = ..., inputs: _Optional[_Iterable[_Union[FileExtractionInput, _Mapping]]] = ..., parameters: _Optional[_Iterable[_Union[FileExtractionParameter, _Mapping]]] = ..., file_output_format: _Optional[_Union[FileOutputFormat, str]] = ..., default_timestamp_metadata: _Optional[_Union[TimestampMetadata, _Mapping]] = ...) -> None: ...

class CreateImageRequest(_message.Message):
    __slots__ = ("workspace_rid", "name", "tag", "object_path")
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    OBJECT_PATH_FIELD_NUMBER: _ClassVar[int]
    workspace_rid: str
    name: str
    tag: str
    object_path: str
    def __init__(self, workspace_rid: _Optional[str] = ..., name: _Optional[str] = ..., tag: _Optional[str] = ..., object_path: _Optional[str] = ...) -> None: ...

class CreateImageResponse(_message.Message):
    __slots__ = ("image",)
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    image: ContainerImage
    def __init__(self, image: _Optional[_Union[ContainerImage, _Mapping]] = ...) -> None: ...

class GetImageRequest(_message.Message):
    __slots__ = ("rid", "workspace_rid")
    RID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    rid: str
    workspace_rid: str
    def __init__(self, rid: _Optional[str] = ..., workspace_rid: _Optional[str] = ...) -> None: ...

class GetImageResponse(_message.Message):
    __slots__ = ("image",)
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    image: ContainerImage
    def __init__(self, image: _Optional[_Union[ContainerImage, _Mapping]] = ...) -> None: ...

class DeleteImageRequest(_message.Message):
    __slots__ = ("rid", "workspace_rid")
    RID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    rid: str
    workspace_rid: str
    def __init__(self, rid: _Optional[str] = ..., workspace_rid: _Optional[str] = ...) -> None: ...

class DeleteImageResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class NameFilter(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class TagFilter(_message.Message):
    __slots__ = ("tag",)
    TAG_FIELD_NUMBER: _ClassVar[int]
    tag: str
    def __init__(self, tag: _Optional[str] = ...) -> None: ...

class StatusFilter(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: ContainerImageStatus
    def __init__(self, status: _Optional[_Union[ContainerImageStatus, str]] = ...) -> None: ...

class AndFilter(_message.Message):
    __slots__ = ("clauses",)
    CLAUSES_FIELD_NUMBER: _ClassVar[int]
    clauses: _containers.RepeatedCompositeFieldContainer[SearchFilter]
    def __init__(self, clauses: _Optional[_Iterable[_Union[SearchFilter, _Mapping]]] = ...) -> None: ...

class SearchFilter(_message.Message):
    __slots__ = ("name", "tag", "status")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    AND_FIELD_NUMBER: _ClassVar[int]
    name: NameFilter
    tag: TagFilter
    status: StatusFilter
    def __init__(self, name: _Optional[_Union[NameFilter, _Mapping]] = ..., tag: _Optional[_Union[TagFilter, _Mapping]] = ..., status: _Optional[_Union[StatusFilter, _Mapping]] = ..., **kwargs) -> None: ...

class SearchImagesRequest(_message.Message):
    __slots__ = ("workspace_rid", "filter", "page_size", "next_page_token")
    WORKSPACE_RID_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    workspace_rid: str
    filter: SearchFilter
    page_size: int
    next_page_token: str
    def __init__(self, workspace_rid: _Optional[str] = ..., filter: _Optional[_Union[SearchFilter, _Mapping]] = ..., page_size: _Optional[int] = ..., next_page_token: _Optional[str] = ...) -> None: ...

class SearchImagesResponse(_message.Message):
    __slots__ = ("images", "next_page_token")
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    images: _containers.RepeatedCompositeFieldContainer[ContainerImage]
    next_page_token: str
    def __init__(self, images: _Optional[_Iterable[_Union[ContainerImage, _Mapping]]] = ..., next_page_token: _Optional[str] = ...) -> None: ...
