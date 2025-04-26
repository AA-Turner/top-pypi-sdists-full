from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.dataobs import expectation__client_pb2 as _expectation__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
RESULT_ERROR: ExpectationResultEnum
RESULT_FAILED: ExpectationResultEnum
RESULT_PASSED: ExpectationResultEnum
RESULT_UNKNOWN: ExpectationResultEnum

class ExpectationResult(_message.Message):
    __slots__ = ["feature_expectation_metadata", "feature_interval_end_time", "feature_interval_start_time", "feature_package_id", "feature_view_name", "metric_expectation_metadata", "result", "result_id", "validation_job_id", "validation_time", "workspace"]
    FEATURE_EXPECTATION_METADATA_FIELD_NUMBER: _ClassVar[int]
    FEATURE_INTERVAL_END_TIME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_INTERVAL_START_TIME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_PACKAGE_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: _ClassVar[int]
    METRIC_EXPECTATION_METADATA_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    RESULT_ID_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_TIME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    feature_expectation_metadata: FeatureExpectationMetadata
    feature_interval_end_time: _timestamp_pb2.Timestamp
    feature_interval_start_time: _timestamp_pb2.Timestamp
    feature_package_id: _id__client_pb2.Id
    feature_view_name: str
    metric_expectation_metadata: MetricExpectationMetadata
    result: ExpectationResultEnum
    result_id: _id__client_pb2.Id
    validation_job_id: _id__client_pb2.Id
    validation_time: _timestamp_pb2.Timestamp
    workspace: str
    def __init__(self, validation_job_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., workspace: _Optional[str] = ..., feature_view_name: _Optional[str] = ..., feature_package_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., validation_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., feature_interval_start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., feature_interval_end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., feature_expectation_metadata: _Optional[_Union[FeatureExpectationMetadata, _Mapping]] = ..., metric_expectation_metadata: _Optional[_Union[MetricExpectationMetadata, _Mapping]] = ..., result: _Optional[_Union[ExpectationResultEnum, str]] = ..., result_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ...) -> None: ...

class ExpectationResultSummary(_message.Message):
    __slots__ = ["expectation_name", "summary"]
    EXPECTATION_NAME_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    expectation_name: str
    summary: ResultSummary
    def __init__(self, expectation_name: _Optional[str] = ..., summary: _Optional[_Union[ResultSummary, _Mapping]] = ...) -> None: ...

class FeatureExpectationMetadata(_message.Message):
    __slots__ = ["alert_msg", "expectation", "failed_join_key_samples", "failure_percentage"]
    ALERT_MSG_FIELD_NUMBER: _ClassVar[int]
    EXPECTATION_FIELD_NUMBER: _ClassVar[int]
    FAILED_JOIN_KEY_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    FAILURE_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    alert_msg: str
    expectation: _expectation__client_pb2.FeatureExpectation
    failed_join_key_samples: _containers.RepeatedScalarFieldContainer[str]
    failure_percentage: float
    def __init__(self, expectation: _Optional[_Union[_expectation__client_pb2.FeatureExpectation, _Mapping]] = ..., alert_msg: _Optional[str] = ..., failure_percentage: _Optional[float] = ..., failed_join_key_samples: _Optional[_Iterable[str]] = ...) -> None: ...

class FeatureViewResultSummary(_message.Message):
    __slots__ = ["expectation_summary", "feature_view_name", "summary"]
    EXPECTATION_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    expectation_summary: _containers.RepeatedCompositeFieldContainer[ExpectationResultSummary]
    feature_view_name: str
    summary: ResultSummary
    def __init__(self, feature_view_name: _Optional[str] = ..., summary: _Optional[_Union[ResultSummary, _Mapping]] = ..., expectation_summary: _Optional[_Iterable[_Union[ExpectationResultSummary, _Mapping]]] = ...) -> None: ...

class MetricExpectationMetadata(_message.Message):
    __slots__ = ["alert_msg", "expectation", "param_values"]
    class ParamValue(_message.Message):
        __slots__ = ["actual_value", "interval_start_time", "metric_name"]
        ACTUAL_VALUE_FIELD_NUMBER: _ClassVar[int]
        INTERVAL_START_TIME_FIELD_NUMBER: _ClassVar[int]
        METRIC_NAME_FIELD_NUMBER: _ClassVar[int]
        actual_value: str
        interval_start_time: _timestamp_pb2.Timestamp
        metric_name: str
        def __init__(self, metric_name: _Optional[str] = ..., actual_value: _Optional[str] = ..., interval_start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
    ALERT_MSG_FIELD_NUMBER: _ClassVar[int]
    EXPECTATION_FIELD_NUMBER: _ClassVar[int]
    PARAM_VALUES_FIELD_NUMBER: _ClassVar[int]
    alert_msg: str
    expectation: _expectation__client_pb2.MetricExpectation
    param_values: _containers.RepeatedCompositeFieldContainer[MetricExpectationMetadata.ParamValue]
    def __init__(self, expectation: _Optional[_Union[_expectation__client_pb2.MetricExpectation, _Mapping]] = ..., alert_msg: _Optional[str] = ..., param_values: _Optional[_Iterable[_Union[MetricExpectationMetadata.ParamValue, _Mapping]]] = ...) -> None: ...

class ResultSummary(_message.Message):
    __slots__ = ["error", "failed", "passed", "unknown"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    PASSED_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_FIELD_NUMBER: _ClassVar[int]
    error: int
    failed: int
    passed: int
    unknown: int
    def __init__(self, passed: _Optional[int] = ..., failed: _Optional[int] = ..., error: _Optional[int] = ..., unknown: _Optional[int] = ...) -> None: ...

class WorkspaceResultSummary(_message.Message):
    __slots__ = ["feature_view_summary", "summary", "workspace"]
    FEATURE_VIEW_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    feature_view_summary: _containers.RepeatedCompositeFieldContainer[FeatureViewResultSummary]
    summary: ResultSummary
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., summary: _Optional[_Union[ResultSummary, _Mapping]] = ..., feature_view_summary: _Optional[_Iterable[_Union[FeatureViewResultSummary, _Mapping]]] = ...) -> None: ...

class ExpectationResultEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
