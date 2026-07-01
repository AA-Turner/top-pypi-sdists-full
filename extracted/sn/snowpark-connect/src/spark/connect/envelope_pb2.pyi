from pyspark.sql.connect.proto import base_pb2 as _base_pb2
from google.rpc import status_pb2 as _status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataframeQueryResult(_message.Message):
    __slots__ = ("result_job_uuid", "arrow_schema", "spark_schema")
    RESULT_JOB_UUID_FIELD_NUMBER: _ClassVar[int]
    ARROW_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    SPARK_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    result_job_uuid: str
    arrow_schema: bytes
    spark_schema: bytes
    def __init__(self, result_job_uuid: _Optional[str] = ..., arrow_schema: _Optional[bytes] = ..., spark_schema: _Optional[bytes] = ...) -> None: ...

class ResponseEnvelope(_message.Message):
    __slots__ = ("execute_plan_response", "analyze_plan_response", "config_response", "add_artifacts_response", "artifact_status_response", "interrupt_response", "release_execute_response", "status", "dataframe_query_result", "query_id", "request_id", "result_partitions")
    EXECUTE_PLAN_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ANALYZE_PLAN_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ADD_ARTIFACTS_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ARTIFACT_STATUS_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    INTERRUPT_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    RELEASE_EXECUTE_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATAFRAME_QUERY_RESULT_FIELD_NUMBER: _ClassVar[int]
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_PARTITIONS_FIELD_NUMBER: _ClassVar[int]
    execute_plan_response: _base_pb2.ExecutePlanResponse
    analyze_plan_response: _base_pb2.AnalyzePlanResponse
    config_response: _base_pb2.ConfigResponse
    add_artifacts_response: _base_pb2.AddArtifactsResponse
    artifact_status_response: _base_pb2.ArtifactStatusesResponse
    interrupt_response: _base_pb2.InterruptResponse
    release_execute_response: _base_pb2.ReleaseExecuteResponse
    status: _status_pb2.Status
    dataframe_query_result: DataframeQueryResult
    query_id: str
    request_id: str
    result_partitions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, execute_plan_response: _Optional[_Union[_base_pb2.ExecutePlanResponse, _Mapping]] = ..., analyze_plan_response: _Optional[_Union[_base_pb2.AnalyzePlanResponse, _Mapping]] = ..., config_response: _Optional[_Union[_base_pb2.ConfigResponse, _Mapping]] = ..., add_artifacts_response: _Optional[_Union[_base_pb2.AddArtifactsResponse, _Mapping]] = ..., artifact_status_response: _Optional[_Union[_base_pb2.ArtifactStatusesResponse, _Mapping]] = ..., interrupt_response: _Optional[_Union[_base_pb2.InterruptResponse, _Mapping]] = ..., release_execute_response: _Optional[_Union[_base_pb2.ReleaseExecuteResponse, _Mapping]] = ..., status: _Optional[_Union[_status_pb2.Status, _Mapping]] = ..., dataframe_query_result: _Optional[_Union[DataframeQueryResult, _Mapping]] = ..., query_id: _Optional[str] = ..., request_id: _Optional[str] = ..., result_partitions: _Optional[_Iterable[str]] = ...) -> None: ...
