from chalk._gen.chalk.artifacts.v1 import cdc_pb2 as _cdc_pb2
from chalk._gen.chalk.artifacts.v1 import chart_pb2 as _chart_pb2
from chalk._gen.chalk.artifacts.v1 import cron_query_pb2 as _cron_query_pb2
from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from chalk._gen.chalk.graph.v1 import graph_pb2 as _graph_pb2
from chalk._gen.chalk.lsp.v1 import lsp_pb2 as _lsp_pb2
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

class ValidationLogSeverity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VALIDATION_LOG_SEVERITY_UNSPECIFIED: _ClassVar[ValidationLogSeverity]
    VALIDATION_LOG_SEVERITY_INFO: _ClassVar[ValidationLogSeverity]
    VALIDATION_LOG_SEVERITY_WARNING: _ClassVar[ValidationLogSeverity]
    VALIDATION_LOG_SEVERITY_ERROR: _ClassVar[ValidationLogSeverity]

VALIDATION_LOG_SEVERITY_UNSPECIFIED: ValidationLogSeverity
VALIDATION_LOG_SEVERITY_INFO: ValidationLogSeverity
VALIDATION_LOG_SEVERITY_WARNING: ValidationLogSeverity
VALIDATION_LOG_SEVERITY_ERROR: ValidationLogSeverity

class EnvironmentSettings(_message.Message):
    __slots__ = ("id", "runtime", "requirements", "dockerfile", "requires_packages", "platform_version")
    ID_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    DOCKERFILE_FIELD_NUMBER: _ClassVar[int]
    REQUIRES_PACKAGES_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_VERSION_FIELD_NUMBER: _ClassVar[int]
    id: str
    runtime: str
    requirements: str
    dockerfile: str
    requires_packages: _containers.RepeatedScalarFieldContainer[str]
    platform_version: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        runtime: _Optional[str] = ...,
        requirements: _Optional[str] = ...,
        dockerfile: _Optional[str] = ...,
        requires_packages: _Optional[_Iterable[str]] = ...,
        platform_version: _Optional[str] = ...,
    ) -> None: ...

class ProjectSettings(_message.Message):
    __slots__ = ("project", "environments", "validation")
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_FIELD_NUMBER: _ClassVar[int]
    project: str
    environments: _containers.RepeatedCompositeFieldContainer[EnvironmentSettings]
    validation: ValidationSettings
    def __init__(
        self,
        project: _Optional[str] = ...,
        environments: _Optional[_Iterable[_Union[EnvironmentSettings, _Mapping]]] = ...,
        validation: _Optional[_Union[ValidationSettings, _Mapping]] = ...,
    ) -> None: ...

class MetadataSettings(_message.Message):
    __slots__ = ("name", "missing")
    NAME_FIELD_NUMBER: _ClassVar[int]
    MISSING_FIELD_NUMBER: _ClassVar[int]
    name: str
    missing: str
    def __init__(self, name: _Optional[str] = ..., missing: _Optional[str] = ...) -> None: ...

class FeatureSettings(_message.Message):
    __slots__ = ("metadata",)
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: _containers.RepeatedCompositeFieldContainer[MetadataSettings]
    def __init__(self, metadata: _Optional[_Iterable[_Union[MetadataSettings, _Mapping]]] = ...) -> None: ...

class ResolverSettings(_message.Message):
    __slots__ = ("metadata",)
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: _containers.RepeatedCompositeFieldContainer[MetadataSettings]
    def __init__(self, metadata: _Optional[_Iterable[_Union[MetadataSettings, _Mapping]]] = ...) -> None: ...

class ValidationSettings(_message.Message):
    __slots__ = ("feature", "resolver")
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FIELD_NUMBER: _ClassVar[int]
    feature: FeatureSettings
    resolver: ResolverSettings
    def __init__(
        self,
        feature: _Optional[_Union[FeatureSettings, _Mapping]] = ...,
        resolver: _Optional[_Union[ResolverSettings, _Mapping]] = ...,
    ) -> None: ...

class FailedImport(_message.Message):
    __slots__ = ("file_name", "module", "traceback")
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    MODULE_FIELD_NUMBER: _ClassVar[int]
    TRACEBACK_FIELD_NUMBER: _ClassVar[int]
    file_name: str
    module: str
    traceback: str
    def __init__(
        self, file_name: _Optional[str] = ..., module: _Optional[str] = ..., traceback: _Optional[str] = ...
    ) -> None: ...

class ChalkpyInfo(_message.Message):
    __slots__ = ("version", "python")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    PYTHON_FIELD_NUMBER: _ClassVar[int]
    version: str
    python: str
    def __init__(self, version: _Optional[str] = ..., python: _Optional[str] = ...) -> None: ...

class ValidationLog(_message.Message):
    __slots__ = ("header", "subheader", "severity")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUBHEADER_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    header: str
    subheader: str
    severity: ValidationLogSeverity
    def __init__(
        self,
        header: _Optional[str] = ...,
        subheader: _Optional[str] = ...,
        severity: _Optional[_Union[ValidationLogSeverity, str]] = ...,
    ) -> None: ...

class Export(_message.Message):
    __slots__ = (
        "graph",
        "crons",
        "charts",
        "cdc_sources",
        "config",
        "chalkpy",
        "failed",
        "logs",
        "lsp",
        "conversion_errors",
    )
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    CRONS_FIELD_NUMBER: _ClassVar[int]
    CHARTS_FIELD_NUMBER: _ClassVar[int]
    CDC_SOURCES_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    CHALKPY_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    LSP_FIELD_NUMBER: _ClassVar[int]
    CONVERSION_ERRORS_FIELD_NUMBER: _ClassVar[int]
    graph: _graph_pb2.Graph
    crons: _containers.RepeatedCompositeFieldContainer[_cron_query_pb2.CronQuery]
    charts: _containers.RepeatedCompositeFieldContainer[_chart_pb2.Chart]
    cdc_sources: _containers.RepeatedCompositeFieldContainer[_cdc_pb2.CDCSource]
    config: ProjectSettings
    chalkpy: ChalkpyInfo
    failed: _containers.RepeatedCompositeFieldContainer[FailedImport]
    logs: _containers.RepeatedCompositeFieldContainer[ValidationLog]
    lsp: _lsp_pb2.LSP
    conversion_errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        graph: _Optional[_Union[_graph_pb2.Graph, _Mapping]] = ...,
        crons: _Optional[_Iterable[_Union[_cron_query_pb2.CronQuery, _Mapping]]] = ...,
        charts: _Optional[_Iterable[_Union[_chart_pb2.Chart, _Mapping]]] = ...,
        cdc_sources: _Optional[_Iterable[_Union[_cdc_pb2.CDCSource, _Mapping]]] = ...,
        config: _Optional[_Union[ProjectSettings, _Mapping]] = ...,
        chalkpy: _Optional[_Union[ChalkpyInfo, _Mapping]] = ...,
        failed: _Optional[_Iterable[_Union[FailedImport, _Mapping]]] = ...,
        logs: _Optional[_Iterable[_Union[ValidationLog, _Mapping]]] = ...,
        lsp: _Optional[_Union[_lsp_pb2.LSP, _Mapping]] = ...,
        conversion_errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...
