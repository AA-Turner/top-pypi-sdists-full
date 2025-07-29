from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

import dataclasses_json


@dataclasses_json.dataclass_json
@dataclass
class UpsertFeatureIdGQL:
    fqn: str
    name: str
    namespace: str
    isPrimary: bool
    className: Optional[str] = None
    attributeName: Optional[str] = None
    explicitNamespace: Optional[bool] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertReferencePathComponentGQL:
    parent: UpsertFeatureIdGQL
    child: UpsertFeatureIdGQL
    parentToChildAttributeName: str


@dataclasses_json.dataclass_json
@dataclass
class UpsertFilterGQL:
    lhs: UpsertFeatureIdGQL
    op: str
    rhs: UpsertFeatureIdGQL


@dataclasses_json.dataclass_json
@dataclass
class UpsertDataFrameGQL:
    columns: Optional[List[UpsertFeatureIdGQL]] = None
    filters: Optional[List[UpsertFilterGQL]] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertFeatureReferenceGQL:
    underlying: UpsertFeatureIdGQL
    path: Optional[List[UpsertReferencePathComponentGQL]] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertHasOneKindGQL:
    join: UpsertFilterGQL


@dataclasses_json.dataclass_json
@dataclass
class UpsertHasManyKindGQL:
    join: UpsertFilterGQL
    columns: Optional[List[UpsertFeatureIdGQL]] = None
    filters: Optional[List[UpsertFilterGQL]] = None


@dataclasses_json.dataclass_json
@dataclass
class VersionInfoGQL:
    version: int
    maximum: int
    default: int
    versions: List[str]


@dataclasses_json.dataclass_json
@dataclass
class UpsertScalarKindGQL:
    primary: bool
    dtype: Optional[str] = None  # The JSON-serialized form of the chalk.features.SerializedDType model
    version: Optional[int] = None  # Deprecated. Use the `versionInfo` instead
    versionInfo: Optional[VersionInfoGQL] = None
    baseClasses: Optional[List[str]] = None  # Deprecated. Use the `dtype` instead
    hasEncoderAndDecoder: bool = False  # Deprecated. Use the `dtype` instead
    scalarKind: Optional[str] = None  # Deprecated. Use the `dtype` instead
    isDeprecated: Optional[bool] = False
    defaultValueJson: Optional[str] = None
    hasExplicitDtype: Optional[bool] = False


@dataclasses_json.dataclass_json
@dataclass
class UpsertFeatureTimeKindGQL:
    format: Optional[str] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertWindowMaterializationGQL:
    namespace: str
    groupBy: List[UpsertFeatureReferenceGQL]
    bucketDuration: float
    aggregation: str
    aggregateOn: Optional[UpsertFeatureReferenceGQL]
    dtype: Optional[str] = None
    backfillResolver: Optional[str] = None
    backfillLookbackDuration: Optional[float] = None
    backfillStartTime: Optional[datetime] = None
    backfillSchedule: Optional[str] = None
    continuousResolver: Optional[str] = None
    continuousBufferDuration: Optional[float] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertFeatureGQL:
    id: UpsertFeatureIdGQL

    scalarKind: Optional[UpsertScalarKindGQL] = None
    hasManyKind: Optional[UpsertHasManyKindGQL] = None
    hasOneKind: Optional[UpsertHasOneKindGQL] = None
    featureTimeKind: Optional[UpsertFeatureTimeKindGQL] = None
    etlOfflineToOnline: bool = False
    windowBuckets: Optional[List[float]] = None
    windowMaterialization: Optional[UpsertWindowMaterializationGQL] = None

    tags: Optional[List[str]] = None
    maxStaleness: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[str] = None

    namespacePath: Optional[str] = None
    isSingleton: Optional[bool] = None


@dataclasses_json.dataclass_json
@dataclass
class KafkaConsumerConfigGQL:
    broker: List[str]
    topic: List[str]
    sslKeystoreLocation: Optional[str]
    clientIdPrefix: Optional[str]
    groupIdPrefix: Optional[str]
    topicMetadataRefreshIntervalMs: Optional[int]
    securityProtocol: Optional[str]


@dataclasses_json.dataclass_json
@dataclass
class UpsertStreamResolverParamMessageGQL:
    """
    GQL split union input pattern
    """

    name: str
    typeName: str
    bases: List[str]
    schema: Optional[Any] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertStreamResolverParamKeyedStateGQL:
    """
    GQL split union input pattern
    """

    name: str
    typeName: str
    bases: List[str]
    schema: Optional[Any] = None
    defaultValue: Optional[Any] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertStreamResolverParamGQL:
    message: Optional[UpsertStreamResolverParamMessageGQL]
    state: Optional[UpsertStreamResolverParamKeyedStateGQL]


@dataclasses_json.dataclass_json
@dataclass
class UpsertStreamResolverGQL:
    fqn: str
    kind: str
    functionDefinition: str
    sourceClassName: Optional[str] = None
    sourceConfig: Optional[Any] = None
    machineType: Optional[str] = None
    environment: Optional[List[str]] = None
    output: Optional[List[UpsertFeatureIdGQL]] = None
    inputs: Optional[List[UpsertStreamResolverParamGQL]] = None
    doc: Optional[str] = None
    owner: Optional[str] = None
    filename: Optional[str] = None
    sourceLine: Optional[int] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertResolverOutputGQL:
    features: Optional[List[UpsertFeatureIdGQL]] = None
    dataframes: Optional[List[UpsertDataFrameGQL]] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertResolverInputUnionGQL:
    feature: Optional[UpsertFeatureReferenceGQL] = None
    dataframe: Optional[UpsertDataFrameGQL] = None
    pseudoFeature: Optional[UpsertFeatureReferenceGQL] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertResolverGQL:
    fqn: str
    kind: str
    functionDefinition: str
    output: UpsertResolverOutputGQL
    environment: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    doc: Optional[str] = None
    cron: Optional[str] = None
    inputs: Optional[List[UpsertFeatureReferenceGQL]] = None
    allInputs: Optional[List[UpsertResolverInputUnionGQL]] = None
    machineType: Optional[str] = None
    owner: Optional[str] = None
    timeout: Optional[str] = None
    filename: Optional[str] = None
    sourceLine: Optional[int] = None
    dataSources: Optional[List[Any]] = None
    dataLineage: Optional[Any] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertSinkResolverGQL:
    fqn: str
    functionDefinition: str
    environment: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    doc: Optional[str] = None
    inputs: Optional[List[UpsertFeatureReferenceGQL]] = None
    machineType: Optional[str] = None
    bufferSize: Optional[int] = None
    debounce: Optional[str] = None
    maxDelay: Optional[str] = None
    upsert: Optional[bool] = None
    owner: Optional[str] = None
    filename: Optional[str] = None
    sourceLine: Optional[int] = None


@dataclasses_json.dataclass_json
@dataclass
class RecomputeFeaturesGQL:
    featureFqns: Optional[List[str]]
    all: Optional[bool]


@dataclasses_json.dataclass_json
@dataclass
class UpsertCronQueryGQL:
    name: str
    cron: str
    filename: str
    output: List[str]  # exploded engine-side
    maxSamples: Optional[int]
    recomputeFeatures: RecomputeFeaturesGQL
    lowerBound: Optional[datetime]  # deprecated: can't use datetime
    upperBound: Optional[datetime]  # deprecated: can't use datetime
    tags: Optional[List[str]]
    requiredResolverTags: Optional[List[str]]
    storeOnline: Optional[bool] = True  # None = True
    storeOffline: Optional[bool] = True  # None = True
    incrementalSources: Optional[List[str]] = None
    lowerBoundStr: Optional[str] = None
    upperBoundStr: Optional[str] = None
    resourceGroup: Optional[str] = None
    plannerOptions: Optional[Dict[str, str]] = None


@dataclasses_json.dataclass_json
@dataclass
class UpsertNamedQueryGQL:
    name: str
    filename: str
    queryVersion: Optional[str] = None
    input: Optional[List[str]] = None
    output: Optional[List[str]] = None
    additionalLoggedFeatures: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    description: Optional[str] = None
    owner: Optional[str] = None
    meta: Optional[Dict[str, str]] = None
    staleness: Optional[Dict[str, str]] = None
    plannerOptions: Optional[Dict[str, str]] = None
    code: Optional[str] = None
    sourceLineStart: Optional[int] = None
    sourceLineEnd: Optional[int] = None
    validPlanNotRequired: Optional[bool] = True


@dataclasses_json.dataclass_json
@dataclass
class MetadataSettings:
    name: str
    missing: str


@dataclasses_json.dataclass_json
@dataclass
class FeatureSettings:
    metadata: Optional[List[MetadataSettings]] = None


@dataclasses_json.dataclass_json
@dataclass
class ResolverSettings:
    metadata: Optional[List[MetadataSettings]] = None


@dataclasses_json.dataclass_json
@dataclass
class ValidationSettings:
    feature: Optional[FeatureSettings] = None
    resolver: Optional[ResolverSettings] = None


@dataclasses_json.dataclass_json
@dataclass
class EnvironmentSettingsGQL:
    id: str
    runtime: Optional[str]
    requirements: Optional[str]
    dockerfile: Optional[str]
    requiresPackages: Optional[List[str]] = None  # deprecated
    platformVersion: Optional[str] = None


@dataclasses_json.dataclass_json
@dataclass
class ProjectSettingsGQL:
    project: str
    environments: Optional[List[EnvironmentSettingsGQL]]
    validation: Optional[ValidationSettings] = None


@dataclasses_json.dataclass_json
@dataclass
class FailedImport:
    filename: str
    module: str
    traceback: str


@dataclasses_json.dataclass_json
@dataclass
class ChalkPYInfo:
    version: str
    python: Optional[str] = None


class MetricKindGQL(str, Enum):
    FEATURE_REQUEST_COUNT = "FEATURE_REQUEST_COUNT"
    FEATURE_LATENCY = "FEATURE_LATENCY"
    FEATURE_STALENESS = "FEATURE_STALENESS"
    FEATURE_VALUE = "FEATURE_VALUE"
    FEATURE_WRITE = "FEATURE_WRITE"
    FEATURE_NULL_RATIO = "FEATURE_NULL_RATIO"
    # Statistics about features computed by resolvers
    FEATURE_COMPUTED_COUNT = "FEATURE_COMPUTED_COUNT"
    FEATURE_COMPUTED_NULL_RATIO = "FEATURE_COMPUTED_NULL_RATIO"
    # statistics about features looked up from the online store during a query
    FEATURE_LOOKED_UP_COUNT = "FEATURE_LOOKED_UP_COUNT"
    FEATURE_LOOKED_UP_NULL_RATIO = "FEATURE_LOOKED_UP_NULL_RATIO"
    # statistics about features whose values were produced during a query
    # either computed OR looked up. Differs from request_count as they do
    # not necessarily need to be requested as an output.
    FEATURE_INTERMEDIATE_COUNT = "FEATURE_INTERMEDIATE_COUNT"
    FEATURE_INTERMEDIATE_NULL_RATIO = "FEATURE_INTERMEDIATE_NULL_RATIO"

    RESOLVER_REQUEST_COUNT = "RESOLVER_REQUEST_COUNT"
    RESOLVER_LATENCY = "RESOLVER_LATENCY"
    RESOLVER_SUCCESS_RATIO = "RESOLVER_SUCCESS_RATIO"

    QUERY_COUNT = "QUERY_COUNT"
    QUERY_LATENCY = "QUERY_LATENCY"
    QUERY_SUCCESS_RATIO = "QUERY_SUCCESS_RATIO"

    BILLING_INFERENCE = "BILLING_INFERENCE"
    BILLING_CRON = "BILLING_CRON"
    BILLING_MIGRATION = "BILLING_MIGRATION"

    CRON_COUNT = "CRON_COUNT"
    CRON_LATENCY = "CRON_LATENCY"

    STREAM_MESSAGES_PROCESSED = "STREAM_MESSAGES_PROCESSED"
    STREAM_MESSAGE_LATENCY = "STREAM_MESSAGE_LATENCY"

    STREAM_WINDOWS_PROCESSED = "STREAM_WINDOWS_PROCESSED"
    STREAM_WINDOW_LATENCY = "STREAM_WINDOW_LATENCY"


class FilterKindGQL(str, Enum):
    FEATURE_STATUS = "FEATURE_STATUS"
    FEATURE_NAME = "FEATURE_NAME"
    FEATURE_TAG = "FEATURE_TAG"

    RESOLVER_STATUS = "RESOLVER_STATUS"
    RESOLVER_NAME = "RESOLVER_NAME"
    RESOLVER_TAG = "RESOLVER_TAG"

    CRON_STATUS = "CRON_STATUS"
    MIGRATION_STATUS = "MIGRATION_STATUS"

    ONLINE_OFFLINE = "ONLINE_OFFLINE"
    CACHE_HIT = "CACHE_HIT"
    OPERATION_ID = "OPERATION_ID"

    QUERY_NAME = "QUERY_NAME"
    QUERY_STATUS = "QUERY_STATUS"

    IS_NULL = "IS_NULL"


class ComparatorKindGQL(str, Enum):
    EQ = "EQ"
    NEQ = "NEQ"
    ONE_OF = "ONE_OF"


class WindowFunctionKindGQL(str, Enum):
    COUNT = "COUNT"
    MEAN = "MEAN"
    SUM = "SUM"
    MIN = "MIN"
    MAX = "MAX"

    PERCENTILE_99 = "PERCENTILE_99"
    PERCENTILE_95 = "PERCENTILE_95"
    PERCENTILE_75 = "PERCENTILE_75"
    PERCENTILE_50 = "PERCENTILE_50"
    PERCENTILE_25 = "PERCENTILE_25"
    PERCENTILE_5 = "PERCENTILE_5"

    ALL_PERCENTILES = "ALL_PERCENTILES"


class GroupByKindGQL(str, Enum):
    FEATURE_STATUS = "FEATURE_STATUS"
    FEATURE_NAME = "FEATURE_NAME"
    IS_NULL = "IS_NULL"

    RESOLVER_STATUS = "RESOLVER_STATUS"
    RESOLVER_NAME = "RESOLVER_NAME"

    QUERY_STATUS = "QUERY_STATUS"
    QUERY_NAME = "QUERY_NAME"

    ONLINE_OFFLINE = "ONLINE_OFFLINE"
    CACHE_HIT = "CACHE_HIT"


class MetricFormulaKindGQL(str, Enum):
    SUM = "SUM"
    TOTAL_RATIO = "TOTAL_RATIO"
    RATIO = "RATIO"
    PRODUCT = "PRODUCT"
    ABS = "ABS"
    KS_STAT = "KS_STAT"
    KS_TEST = "KS_TEST"
    KS_THRESHOLD = "KS_THRESHOLD"
    TIME_OFFSET = "TIME_OFFSET"


class AlertSeverityKindGQL(str, Enum):
    critical = "critical"
    error = "error"
    warning = "warning"
    info = "info"


class ThresholdKindGQL(str, Enum):
    ABOVE = "ABOVE"
    BELOW = "BELOW"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS_EQUAL = "LESS_EQUAL"
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"


@dataclasses_json.dataclass_json
@dataclass
class CreateMetricFilterGQL:
    kind: FilterKindGQL
    comparator: ComparatorKindGQL
    value: List[str]


@dataclasses_json.dataclass_json
@dataclass
class CreateMetricConfigSeriesGQL:
    metric: MetricKindGQL
    filters: List[CreateMetricFilterGQL]
    name: Optional[str] = None
    windowFunction: Optional[WindowFunctionKindGQL] = None
    groupBy: Optional[List[GroupByKindGQL]] = None


@dataclasses_json.dataclass_json
@dataclass
class CreateDatasetFeatureOperandGQL:
    """
    Can't do a Tuple[int, str] so we're going to use a wrapper
    """

    dataset: str
    feature: str


@dataclasses_json.dataclass_json
@dataclass
class CreateMetricFormulaGQL:
    """
    No input unions in graphql means we have to use parallel optional input keys
    and do additional validation work ourselves
    """

    kind: MetricFormulaKindGQL
    # ----- Input Union ------
    singleSeriesOperands: Optional[int]  # index of a single series
    multiSeriesOperands: Optional[List[int]]  # index of multiple series
    datasetFeatureOperands: Optional[CreateDatasetFeatureOperandGQL]  # dataset id and feature name
    # ----- End Union  ------
    name: Optional[str] = None


@dataclasses_json.dataclass_json
@dataclass
class CreateAlertTriggerGQL:
    name: str
    severity: AlertSeverityKindGQL
    thresholdPosition: ThresholdKindGQL
    thresholdValue: float
    seriesName: Optional[str] = None
    channelName: Optional[str] = None
    description: Optional[str] = None


@dataclasses_json.dataclass_json
@dataclass
class CreateMetricConfigGQL:
    name: str
    windowPeriod: str
    series: List[CreateMetricConfigSeriesGQL]
    formulas: Optional[List[CreateMetricFormulaGQL]] = None
    trigger: Optional[CreateAlertTriggerGQL] = None


@dataclasses_json.dataclass_json
@dataclass
class CreateChartGQL:
    id: str
    config: CreateMetricConfigGQL
    entityKind: str
    entityId: Optional[str] = None


class GraphLogSeverity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclasses_json.dataclass_json
@dataclass
class UpdateGraphError:
    header: str
    subheader: str
    severity: GraphLogSeverity


@dataclasses_json.dataclass_json
@dataclass
class UpsertSQLSourceGQL:
    name: Optional[str]
    kind: str


@dataclasses_json.dataclass_json
@dataclass
class UpsertCDCSourceGQL:
    integrationName: str
    schemaDotTableList: List[str]


@dataclasses_json.dataclass_json
@dataclass
class FeatureClassGQL:
    isSingleton: bool
    doc: Optional[str]
    name: str
    owner: Optional[str]
    tags: List[str]


@dataclasses_json.dataclass_json
@dataclass(frozen=True)
class PositionGQL:
    """Mirrors an LSP Position

    https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#position
    """

    line: int
    """Line position in a document (one-based)."""

    character: int
    """Character offset on a line in a document (zero-based)."""


@dataclasses_json.dataclass_json
@dataclass(frozen=True)
class RangeGQL:
    """Mirrors an LSP Range

    https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#range
    """

    start: PositionGQL
    end: PositionGQL


class DiagnosticSeverityGQL(str, Enum):
    """Mirrors an LSP DiagnosticSeverity"""

    Error = "Error"
    Warning = "Warning"
    Information = "Information"
    Hint = "Hint"


@dataclasses_json.dataclass_json
@dataclass
class CodeDescriptionGQL:
    href: str


@dataclasses_json.dataclass_json
@dataclass
class LocationGQL:
    uri: str
    range: RangeGQL


@dataclasses_json.dataclass_json
@dataclass
class DiagnosticRelatedInformationGQL:
    location: LocationGQL
    """The location of this related diagnostic information."""

    message: str
    """The message of this related diagnostic information."""


@dataclasses_json.dataclass_json
@dataclass
class DiagnosticGQL:
    range: RangeGQL
    message: str
    severity: Optional[DiagnosticSeverityGQL]
    code: Optional[str]
    codeDescription: Optional[CodeDescriptionGQL]
    relatedInformation: Optional[List[DiagnosticRelatedInformationGQL]] = None


@dataclasses_json.dataclass_json
@dataclass
class PublishDiagnosticsParams:
    """Mirrors an LSP PublishDiagnosticsParams

    https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#publishDiagnosticsParams
    """

    uri: str
    diagnostics: List[DiagnosticGQL]


@dataclasses_json.dataclass_json
@dataclass
class TextDocumentIdentifierGQL:
    uri: str


@dataclasses_json.dataclass_json
@dataclass
class TextEditGQL:
    range: RangeGQL
    newText: str


@dataclasses_json.dataclass_json
@dataclass
class TextDocumentEditGQL:
    textDocument: TextDocumentIdentifierGQL
    edits: List[TextEditGQL]


@dataclasses_json.dataclass_json
@dataclass
class WorkspaceEditGQL:
    documentChanges: List[TextDocumentEditGQL]


@dataclasses_json.dataclass_json
@dataclass
class CodeActionGQL:
    title: str
    diagnostics: Optional[List[DiagnosticGQL]]
    edit: WorkspaceEditGQL


@dataclasses_json.dataclass_json
@dataclass
class LspGQL:
    diagnostics: List[PublishDiagnosticsParams]
    actions: List[CodeActionGQL]


@dataclasses_json.dataclass_json
@dataclass
class UpsertGraphGQL:
    resolvers: Optional[List[UpsertResolverGQL]] = None
    features: Optional[List[UpsertFeatureGQL]] = None
    streams: Optional[List[UpsertStreamResolverGQL]] = None
    sinks: Optional[List[UpsertSinkResolverGQL]] = None
    cronQueries: Optional[List[UpsertCronQueryGQL]] = None
    namedQueries: Optional[List[UpsertNamedQueryGQL]] = None
    charts: Optional[List[CreateChartGQL]] = None
    config: Optional[ProjectSettingsGQL] = None
    failed: Optional[List[FailedImport]] = None
    chalkpy: Optional[ChalkPYInfo] = None
    validated: Optional[bool] = None
    errors: Optional[List[UpdateGraphError]] = None
    cdcSources: Optional[List[UpsertCDCSourceGQL]] = None
    sqlSources: Optional[List[UpsertSQLSourceGQL]] = None
    featureClasses: Optional[List[FeatureClassGQL]] = None
    lsp: Optional[LspGQL] = None
