from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import datasets_pb2 as _datasets_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
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

class DatasetSearchMatchMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATASET_SEARCH_MATCH_MODE_UNSPECIFIED: _ClassVar[DatasetSearchMatchMode]
    DATASET_SEARCH_MATCH_MODE_ANY: _ClassVar[DatasetSearchMatchMode]
    DATASET_SEARCH_MATCH_MODE_ALL: _ClassVar[DatasetSearchMatchMode]

DATASET_SEARCH_MATCH_MODE_UNSPECIFIED: DatasetSearchMatchMode
DATASET_SEARCH_MATCH_MODE_ANY: DatasetSearchMatchMode
DATASET_SEARCH_MATCH_MODE_ALL: DatasetSearchMatchMode

class SearchDatasetsFilters(_message.Message):
    __slots__ = (
        "output_names",
        "input_root_fqns",
        "match_mode",
        "start_time",
        "end_time",
        "statuses",
        "min_num_rows",
        "include_archived",
    )
    OUTPUT_NAMES_FIELD_NUMBER: _ClassVar[int]
    INPUT_ROOT_FQNS_FIELD_NUMBER: _ClassVar[int]
    MATCH_MODE_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    STATUSES_FIELD_NUMBER: _ClassVar[int]
    MIN_NUM_ROWS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    output_names: _containers.RepeatedScalarFieldContainer[str]
    input_root_fqns: _containers.RepeatedScalarFieldContainer[str]
    match_mode: DatasetSearchMatchMode
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    statuses: _containers.RepeatedScalarFieldContainer[_datasets_pb2.DatasetRevisionStatus]
    min_num_rows: int
    include_archived: bool
    def __init__(
        self,
        output_names: _Optional[_Iterable[str]] = ...,
        input_root_fqns: _Optional[_Iterable[str]] = ...,
        match_mode: _Optional[_Union[DatasetSearchMatchMode, str]] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        statuses: _Optional[_Iterable[_Union[_datasets_pb2.DatasetRevisionStatus, str]]] = ...,
        min_num_rows: _Optional[int] = ...,
        include_archived: bool = ...,
    ) -> None: ...

class SearchDatasetsRequest(_message.Message):
    __slots__ = ("filters", "limit", "cursor", "include_output_columns")
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_OUTPUT_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    filters: SearchDatasetsFilters
    limit: int
    cursor: str
    include_output_columns: bool
    def __init__(
        self,
        filters: _Optional[_Union[SearchDatasetsFilters, _Mapping]] = ...,
        limit: _Optional[int] = ...,
        cursor: _Optional[str] = ...,
        include_output_columns: bool = ...,
    ) -> None: ...

class DatasetSearchResult(_message.Message):
    __slots__ = (
        "revision",
        "dataset_name",
        "query_name",
        "query_name_version",
        "matched_output_names",
        "matched_input_root_fqns",
    )
    REVISION_FIELD_NUMBER: _ClassVar[int]
    DATASET_NAME_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_VERSION_FIELD_NUMBER: _ClassVar[int]
    MATCHED_OUTPUT_NAMES_FIELD_NUMBER: _ClassVar[int]
    MATCHED_INPUT_ROOT_FQNS_FIELD_NUMBER: _ClassVar[int]
    revision: _datasets_pb2.DatasetRevisionMeta
    dataset_name: str
    query_name: str
    query_name_version: str
    matched_output_names: _containers.RepeatedScalarFieldContainer[str]
    matched_input_root_fqns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        revision: _Optional[_Union[_datasets_pb2.DatasetRevisionMeta, _Mapping]] = ...,
        dataset_name: _Optional[str] = ...,
        query_name: _Optional[str] = ...,
        query_name_version: _Optional[str] = ...,
        matched_output_names: _Optional[_Iterable[str]] = ...,
        matched_input_root_fqns: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class SearchDatasetsResponse(_message.Message):
    __slots__ = ("results", "cursor")
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[DatasetSearchResult]
    cursor: str
    def __init__(
        self, results: _Optional[_Iterable[_Union[DatasetSearchResult, _Mapping]]] = ..., cursor: _Optional[str] = ...
    ) -> None: ...
