from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.chart.v1 import densetimeserieschart_pb2 as _densetimeserieschart_pb2
from chalk._gen.chalk.chart.v1 import histogram_pb2 as _histogram_pb2
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

class ParquetChartMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PARQUET_CHART_MODE_UNSPECIFIED: _ClassVar[ParquetChartMode]
    PARQUET_CHART_MODE_TIMESERIES: _ClassVar[ParquetChartMode]
    PARQUET_CHART_MODE_HISTOGRAM: _ClassVar[ParquetChartMode]

PARQUET_CHART_MODE_UNSPECIFIED: ParquetChartMode
PARQUET_CHART_MODE_TIMESERIES: ParquetChartMode
PARQUET_CHART_MODE_HISTOGRAM: ParquetChartMode

class ParquetColumnConfig(_message.Message):
    __slots__ = (
        "timestamp_column",
        "value_columns",
        "group_by_columns",
        "bucket_lower_bound_column",
        "bucket_upper_bound_column",
        "count_column",
        "bucket_label_column",
    )
    TIMESTAMP_COLUMN_FIELD_NUMBER: _ClassVar[int]
    VALUE_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    BUCKET_LOWER_BOUND_COLUMN_FIELD_NUMBER: _ClassVar[int]
    BUCKET_UPPER_BOUND_COLUMN_FIELD_NUMBER: _ClassVar[int]
    COUNT_COLUMN_FIELD_NUMBER: _ClassVar[int]
    BUCKET_LABEL_COLUMN_FIELD_NUMBER: _ClassVar[int]
    timestamp_column: str
    value_columns: _containers.RepeatedScalarFieldContainer[str]
    group_by_columns: _containers.RepeatedScalarFieldContainer[str]
    bucket_lower_bound_column: str
    bucket_upper_bound_column: str
    count_column: str
    bucket_label_column: str
    def __init__(
        self,
        timestamp_column: _Optional[str] = ...,
        value_columns: _Optional[_Iterable[str]] = ...,
        group_by_columns: _Optional[_Iterable[str]] = ...,
        bucket_lower_bound_column: _Optional[str] = ...,
        bucket_upper_bound_column: _Optional[str] = ...,
        count_column: _Optional[str] = ...,
        bucket_label_column: _Optional[str] = ...,
    ) -> None: ...

class RenderParquetChartRequest(_message.Message):
    __slots__ = ("signed_uris", "mode", "column_config", "title")
    SIGNED_URIS_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    COLUMN_CONFIG_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    signed_uris: _containers.RepeatedScalarFieldContainer[str]
    mode: ParquetChartMode
    column_config: ParquetColumnConfig
    title: str
    def __init__(
        self,
        signed_uris: _Optional[_Iterable[str]] = ...,
        mode: _Optional[_Union[ParquetChartMode, str]] = ...,
        column_config: _Optional[_Union[ParquetColumnConfig, _Mapping]] = ...,
        title: _Optional[str] = ...,
    ) -> None: ...

class RenderParquetChartResponse(_message.Message):
    __slots__ = ("timeseries_chart", "histogram_chart")
    TIMESERIES_CHART_FIELD_NUMBER: _ClassVar[int]
    HISTOGRAM_CHART_FIELD_NUMBER: _ClassVar[int]
    timeseries_chart: _densetimeserieschart_pb2.DenseTimeSeriesChart
    histogram_chart: _histogram_pb2.HistogramChart
    def __init__(
        self,
        timeseries_chart: _Optional[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]] = ...,
        histogram_chart: _Optional[_Union[_histogram_pb2.HistogramChart, _Mapping]] = ...,
    ) -> None: ...
