from chalk._gen.chalk.artifacts.v1 import export_pb2 as _export_pb2
from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DirectoryOptions(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DIRECTORY_OPTIONS_UNSPECIFIED: _ClassVar[DirectoryOptions]
    DIRECTORY_OPTIONS_MAIN: _ClassVar[DirectoryOptions]
    DIRECTORY_OPTIONS_SHADOW: _ClassVar[DirectoryOptions]
    DIRECTORY_OPTIONS_DRY_RUN: _ClassVar[DirectoryOptions]
    DIRECTORY_OPTIONS_INDEXING_JOB: _ClassVar[DirectoryOptions]
    DIRECTORY_OPTIONS_VENV_INDEXING: _ClassVar[DirectoryOptions]

class IndexingJobStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INDEXING_JOB_STATUS_UNSPECIFIED: _ClassVar[IndexingJobStatus]
    INDEXING_JOB_STATUS_PENDING: _ClassVar[IndexingJobStatus]
    INDEXING_JOB_STATUS_RUNNING: _ClassVar[IndexingJobStatus]
    INDEXING_JOB_STATUS_SUCCEEDED: _ClassVar[IndexingJobStatus]
    INDEXING_JOB_STATUS_FAILED: _ClassVar[IndexingJobStatus]
    INDEXING_JOB_STATUS_UNKNOWN: _ClassVar[IndexingJobStatus]

class IndexingJobIssue(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INDEXING_JOB_ISSUE_UNSPECIFIED: _ClassVar[IndexingJobIssue]
    INDEXING_JOB_ISSUE_NONE: _ClassVar[IndexingJobIssue]
    INDEXING_JOB_ISSUE_WAITING_FOR_RESOURCES: _ClassVar[IndexingJobIssue]
    INDEXING_JOB_ISSUE_UNSCHEDULABLE: _ClassVar[IndexingJobIssue]
    INDEXING_JOB_ISSUE_IMAGE_PULL_FAILED: _ClassVar[IndexingJobIssue]
    INDEXING_JOB_ISSUE_OTHER: _ClassVar[IndexingJobIssue]

DIRECTORY_OPTIONS_UNSPECIFIED: DirectoryOptions
DIRECTORY_OPTIONS_MAIN: DirectoryOptions
DIRECTORY_OPTIONS_SHADOW: DirectoryOptions
DIRECTORY_OPTIONS_DRY_RUN: DirectoryOptions
DIRECTORY_OPTIONS_INDEXING_JOB: DirectoryOptions
DIRECTORY_OPTIONS_VENV_INDEXING: DirectoryOptions
INDEXING_JOB_STATUS_UNSPECIFIED: IndexingJobStatus
INDEXING_JOB_STATUS_PENDING: IndexingJobStatus
INDEXING_JOB_STATUS_RUNNING: IndexingJobStatus
INDEXING_JOB_STATUS_SUCCEEDED: IndexingJobStatus
INDEXING_JOB_STATUS_FAILED: IndexingJobStatus
INDEXING_JOB_STATUS_UNKNOWN: IndexingJobStatus
INDEXING_JOB_ISSUE_UNSPECIFIED: IndexingJobIssue
INDEXING_JOB_ISSUE_NONE: IndexingJobIssue
INDEXING_JOB_ISSUE_WAITING_FOR_RESOURCES: IndexingJobIssue
INDEXING_JOB_ISSUE_UNSCHEDULABLE: IndexingJobIssue
INDEXING_JOB_ISSUE_IMAGE_PULL_FAILED: IndexingJobIssue
INDEXING_JOB_ISSUE_OTHER: IndexingJobIssue

class GetIndexingJobStatusRequest(_message.Message):
    __slots__ = ("deployment_id", "directory_prefix_enum", "indexing_job_id", "include_diagnostics")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_PREFIX_ENUM_FIELD_NUMBER: _ClassVar[int]
    INDEXING_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    directory_prefix_enum: DirectoryOptions
    indexing_job_id: str
    include_diagnostics: bool
    def __init__(
        self,
        deployment_id: _Optional[str] = ...,
        directory_prefix_enum: _Optional[_Union[DirectoryOptions, str]] = ...,
        indexing_job_id: _Optional[str] = ...,
        include_diagnostics: bool = ...,
    ) -> None: ...

class IndexingJobDiagnostics(_message.Message):
    __slots__ = ("pod_phase", "pod_name", "issue", "summary", "raw_message")
    POD_PHASE_FIELD_NUMBER: _ClassVar[int]
    POD_NAME_FIELD_NUMBER: _ClassVar[int]
    ISSUE_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    RAW_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    pod_phase: str
    pod_name: str
    issue: IndexingJobIssue
    summary: str
    raw_message: str
    def __init__(
        self,
        pod_phase: _Optional[str] = ...,
        pod_name: _Optional[str] = ...,
        issue: _Optional[_Union[IndexingJobIssue, str]] = ...,
        summary: _Optional[str] = ...,
        raw_message: _Optional[str] = ...,
    ) -> None: ...

class GetIndexingJobStatusResponse(_message.Message):
    __slots__ = ("export", "status", "diagnostics")
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    export: _export_pb2.Export
    status: IndexingJobStatus
    diagnostics: IndexingJobDiagnostics
    def __init__(
        self,
        export: _Optional[_Union[_export_pb2.Export, _Mapping]] = ...,
        status: _Optional[_Union[IndexingJobStatus, str]] = ...,
        diagnostics: _Optional[_Union[IndexingJobDiagnostics, _Mapping]] = ...,
    ) -> None: ...

class GetIndexingExportRequest(_message.Message):
    __slots__ = ("deployment_id", "directory_prefix_enum", "shadow_run_id")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_PREFIX_ENUM_FIELD_NUMBER: _ClassVar[int]
    SHADOW_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    directory_prefix_enum: DirectoryOptions
    shadow_run_id: str
    def __init__(
        self,
        deployment_id: _Optional[str] = ...,
        directory_prefix_enum: _Optional[_Union[DirectoryOptions, str]] = ...,
        shadow_run_id: _Optional[str] = ...,
    ) -> None: ...

class GetIndexingExportResponse(_message.Message):
    __slots__ = ("export",)
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    export: _export_pb2.Export
    def __init__(self, export: _Optional[_Union[_export_pb2.Export, _Mapping]] = ...) -> None: ...

class CancelIndexingJobRequest(_message.Message):
    __slots__ = ("deployment_id", "build_id")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    BUILD_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    build_id: str
    def __init__(self, deployment_id: _Optional[str] = ..., build_id: _Optional[str] = ...) -> None: ...

class CancelIndexingJobResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
