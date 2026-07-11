from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class DatasetFilePartition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATASET_FILE_PARTITION_UNSPECIFIED: _ClassVar[DatasetFilePartition]
    DATASET_FILE_PARTITION_OUTPUT: _ClassVar[DatasetFilePartition]
    DATASET_FILE_PARTITION_GIVENS: _ClassVar[DatasetFilePartition]
    DATASET_FILE_PARTITION_PERFORMANCE_SUMMARY: _ClassVar[DatasetFilePartition]
    DATASET_FILE_PARTITION_TRACE: _ClassVar[DatasetFilePartition]
    DATASET_FILE_PARTITION_REQUEST_BODY: _ClassVar[DatasetFilePartition]

class DatasetFlightTicketKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATASET_FLIGHT_TICKET_KIND_UNSPECIFIED: _ClassVar[DatasetFlightTicketKind]
    DATASET_FLIGHT_TICKET_KIND_LINKS: _ClassVar[DatasetFlightTicketKind]
    DATASET_FLIGHT_TICKET_KIND_DATA: _ClassVar[DatasetFlightTicketKind]

DATASET_FILE_PARTITION_UNSPECIFIED: DatasetFilePartition
DATASET_FILE_PARTITION_OUTPUT: DatasetFilePartition
DATASET_FILE_PARTITION_GIVENS: DatasetFilePartition
DATASET_FILE_PARTITION_PERFORMANCE_SUMMARY: DatasetFilePartition
DATASET_FILE_PARTITION_TRACE: DatasetFilePartition
DATASET_FILE_PARTITION_REQUEST_BODY: DatasetFilePartition
DATASET_FLIGHT_TICKET_KIND_UNSPECIFIED: DatasetFlightTicketKind
DATASET_FLIGHT_TICKET_KIND_LINKS: DatasetFlightTicketKind
DATASET_FLIGHT_TICKET_KIND_DATA: DatasetFlightTicketKind

class DatasetFlightCommand(_message.Message):
    __slots__ = ("revision_id", "kind", "partitions", "limit_rows", "max_concurrency")
    REVISION_ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    PARTITIONS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_ROWS_FIELD_NUMBER: _ClassVar[int]
    MAX_CONCURRENCY_FIELD_NUMBER: _ClassVar[int]
    revision_id: str
    kind: DatasetFlightTicketKind
    partitions: _containers.RepeatedScalarFieldContainer[DatasetFilePartition]
    limit_rows: int
    max_concurrency: int
    def __init__(
        self,
        revision_id: _Optional[str] = ...,
        kind: _Optional[_Union[DatasetFlightTicketKind, str]] = ...,
        partitions: _Optional[_Iterable[_Union[DatasetFilePartition, str]]] = ...,
        limit_rows: _Optional[int] = ...,
        max_concurrency: _Optional[int] = ...,
    ) -> None: ...

class DatasetFlightTicket(_message.Message):
    __slots__ = ("command", "object_uris")
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    OBJECT_URIS_FIELD_NUMBER: _ClassVar[int]
    command: DatasetFlightCommand
    object_uris: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        command: _Optional[_Union[DatasetFlightCommand, _Mapping]] = ...,
        object_uris: _Optional[_Iterable[str]] = ...,
    ) -> None: ...
