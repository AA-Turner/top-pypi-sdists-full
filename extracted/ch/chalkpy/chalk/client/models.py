from __future__ import annotations

import dataclasses
import json
import os
import traceback
import uuid
from datetime import datetime, timedelta
from enum import Enum, IntEnum
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Mapping, Optional, Sequence, Tuple, Union

import numpy as np
from typing_extensions import TypeAlias

from chalk.byte_transmit.model import ByteBaseModel, ByteDict
from chalk.client._internal_models.models import OfflineQueryGivensVersion
from chalk.features import Feature
from chalk.features._encoding.json import FeatureEncodingOptions
from chalk.features.resolver import Resolver
from chalk.features.tag import EnvironmentId
from chalk.prompts import Prompt
from chalk.queries.query_context import ContextJsonDict
from chalk.utils.df_utils import read_parquet
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl
    from pydantic import BaseModel, Extra, Field, validator

    root_validator = lambda _: (lambda x: x)
else:
    try:
        from pydantic.v1 import BaseModel, Extra, Field, root_validator, validator
    except ImportError:
        from pydantic import BaseModel, Extra, Field, root_validator, validator

MAX_STR_LENGTH = 10_000

CPU_REGEX = r"^(\d+(\.\d+)?m?)$"
MEMORY_REGEX = r"^\d+([EPTGMK]i|[EPTGMk])?$"

TIMEDELTA_PREFIX = "delta:"  # used to disambiguate datetimes and timedeltas in string form

FeatureReference: TypeAlias = Union[str, Any]

_CHALK_DEBUG_FULL_TRACE = os.getenv("CHALK_DEBUG_FULL_TRACE") == "1"


def _category_for_error_code(c: Union[ErrorCode, str]) -> ErrorCodeCategory:
    c = ErrorCode[c]
    return {
        ErrorCode.PARSE_FAILED: ErrorCodeCategory.REQUEST,
        ErrorCode.RESOLVER_NOT_FOUND: ErrorCodeCategory.REQUEST,
        ErrorCode.INVALID_QUERY: ErrorCodeCategory.REQUEST,
        ErrorCode.VALIDATION_FAILED: ErrorCodeCategory.FIELD,
        ErrorCode.RESOLVER_FAILED: ErrorCodeCategory.FIELD,
        ErrorCode.RESOLVER_TIMED_OUT: ErrorCodeCategory.FIELD,
        ErrorCode.UPSTREAM_FAILED: ErrorCodeCategory.FIELD,
        ErrorCode.UNAUTHENTICATED: ErrorCodeCategory.NETWORK,
        ErrorCode.UNAUTHORIZED: ErrorCodeCategory.NETWORK,
        ErrorCode.INTERNAL_SERVER_ERROR: ErrorCodeCategory.NETWORK,
        ErrorCode.CANCELLED: ErrorCodeCategory.NETWORK,
        ErrorCode.DEADLINE_EXCEEDED: ErrorCodeCategory.NETWORK,
    }[c]


class OnlineQueryContext(BaseModel):
    """Context in which to execute a query."""

    environment: Optional[str] = None
    """
    The environment under which to run the resolvers.
    API tokens can be scoped to an # environment.
    If no environment is specified in the query,
    but the token supports only a single environment,
    then that environment will be taken as the scope
    for executing the request.
    """

    tags: Optional[List[str]] = None
    """
    The tags used to scope the resolvers.
    More information at https://docs.chalk.ai/docs/resolver-tags
    """

    required_resolver_tags: Optional[List[str]] = None


class OfflineQueryContext(BaseModel):
    environment: Optional[str] = None
    """
    The environment under which to run the resolvers.
    API tokens can be scoped to an # environment.
    If no environment is specified in the query,
    but the token supports only a single environment,
    then that environment will be taken as the scope
    for executing the request.
    """


class ErrorCode(str, Enum):
    """The detailed error code.

    For a simpler category of error, see `ErrorCodeCategory`.
    """

    PARSE_FAILED = "PARSE_FAILED"
    """The query contained features that do not exist."""

    RESOLVER_NOT_FOUND = "RESOLVER_NOT_FOUND"
    """
    A resolver was required as part of running the dependency
    graph that could not be found.
    """

    INVALID_QUERY = "INVALID_QUERY"
    """
    The query is invalid. All supplied features need to be
    rooted in the same top-level entity.
    """

    VALIDATION_FAILED = "VALIDATION_FAILED"
    """
    A feature value did not match the expected schema
    (e.g. `incompatible type "int"; expected "str"`)
    """

    RESOLVER_FAILED = "RESOLVER_FAILED"
    """The resolver for a feature errored."""

    RESOLVER_TIMED_OUT = "RESOLVER_TIMED_OUT"
    """The resolver for a feature timed out."""

    UPSTREAM_FAILED = "UPSTREAM_FAILED"
    """
    A crash in a resolver that was to produce an input for
    the resolver crashed, and so the resolver could not run
    crashed, and so the resolver could not run.
    """

    UNAUTHENTICATED = "UNAUTHENTICATED"
    """The request was submitted with an invalid authentication header."""

    UNAUTHORIZED = "UNAUTHORIZED"
    """The supplied credentials do not provide the right authorization to execute the request."""

    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    """An unspecified error occurred."""

    CANCELLED = "CANCELLED"
    """The operation was cancelled, typically by the caller."""

    DEADLINE_EXCEEDED = "DEADLINE_EXCEEDED"
    """The deadline expired before the operation could complete."""


class ErrorCodeCategory(str, Enum):
    """The category of an error.

    For more detailed error information, see `ErrorCode`
    """

    REQUEST = "REQUEST"
    """
    Request errors are raised before execution of your
    resolver code. They may occur due to invalid feature
    names in the input or a request that cannot be satisfied
    by the resolvers you have defined.
    """

    FIELD = "FIELD"
    """
    Field errors are raised while running a feature resolver
    for a particular field. For this type of error, you'll
    find a feature and resolver attribute in the error type.
    When a feature resolver crashes, you will receive null
    value in the response. To differentiate from a resolver
    returning a null value and a failure in the resolver,
    you need to check the error schema.
    """

    NETWORK = "NETWORK"
    """
    Network errors are thrown outside your resolvers.
    For example, your request was unauthenticated,
    connection failed, or an error occurred within Chalk.
    """


class ChalkException(BaseModel, frozen=True):
    """Information about an exception from a resolver run."""

    kind: str
    """The name of the class of the exception."""

    message: str
    """The message taken from the exception."""

    stacktrace: str
    """The stacktrace produced by the code."""

    internal_stacktrace: Optional[str] = None
    """The stacktrace produced by the code, full detail."""

    @classmethod
    def from_exception(cls, exc: BaseException) -> "ChalkException":
        return ChalkException.create(
            kind=type(exc).__name__,
            message=str(exc),
            stacktrace="".join(traceback.format_exception(exc)),
        )

    @classmethod
    def create(
        cls,
        kind: str,
        message: str,
        stacktrace: str,
        internal_stacktrace: Optional[str] = None,
    ) -> "ChalkException":
        return ChalkException(
            kind=kind,
            message=message[0:MAX_STR_LENGTH],
            stacktrace=stacktrace[-MAX_STR_LENGTH:],
            internal_stacktrace=internal_stacktrace[-MAX_STR_LENGTH:] if internal_stacktrace is not None else None,
        )


class ChalkError(BaseModel, frozen=True):
    """
    The `ChalkError` describes an error from running a resolver
    or from a feature that can't be validated.
    """

    code: ErrorCode
    """The type of the error."""

    category: ErrorCodeCategory = ErrorCodeCategory.NETWORK
    """
    The category of the error, given in the type field for the error codes.
    This will be one of "REQUEST", "NETWORK", and "FIELD".
    """

    message: str
    """A readable description of the error message."""

    display_primary_key: Optional[str] = None
    """
    A human-readable hint that can be used to identify the entity that this error is associated with.
    """

    display_primary_key_fqn: Optional[str] = None
    """
    If provided, can be used to add additional context to 'display_primary_key'.
    """

    exception: Optional[ChalkException] = None
    """The exception that caused the failure, if applicable."""

    feature: Optional[str] = None
    """
    The fully qualified name of the failing feature, e.g. `user.identity.has_voip_phone`.
    """

    resolver: Optional[str] = None
    """
    The fully qualified name of the failing resolver, e.g. `my.project.get_fraud_score`.
    """

    def is_resolver_runtime_error(self) -> bool:
        """
        Returns True if the error indicates an issue with user's resolver, rather than an internal Chalk failure.
        """
        return self.code in (ErrorCode.RESOLVER_FAILED, ErrorCode.RESOLVER_TIMED_OUT, ErrorCode.UPSTREAM_FAILED)

    def copy_for_feature(self, feature: str) -> "ChalkError":
        return self.copy(update={"feature": feature})

    def copy_for_pkey(self, pkey: Union[str, int]) -> "ChalkError":
        return self.copy(update={"display_primary_key": str(pkey)})

    @classmethod
    def create(
        cls,
        code: ErrorCode,
        message: str,
        category: Optional[ErrorCodeCategory] = None,
        display_primary_key: Optional[str] = None,
        display_primary_key_fqn: Optional[str] = None,
        exception: Optional[ChalkException] = None,
        feature: Optional[str] = None,
        resolver: Optional[str] = None,
    ) -> "ChalkError":
        category = category or _category_for_error_code(code)
        if not _CHALK_DEBUG_FULL_TRACE:
            # Truncate the message to a specified maximum length.
            message = message[0:MAX_STR_LENGTH]

        _HAS_CHALK_TRACE = "[has chalk trace]"
        if _CHALK_DEBUG_FULL_TRACE and _HAS_CHALK_TRACE not in message:
            # Include a stack trace if it's not already present and the super-verbose
            # full trace flag is enabled.
            import traceback

            formatted_stack = traceback.format_stack()[:-1]  # Exclude this validation function.
            start_stack_from = 0
            for i in range(len(formatted_stack)):
                if "run_endpoint_function" in formatted_stack[i]:
                    # This function occurs in the stack trace before the actual entry into the engine-
                    # everything before it is boilerplate.
                    start_stack_from = i + 1
            message = (
                f"{message}\n{_HAS_CHALK_TRACE}\n"
                + "[" * 200
                + "\n"
                + "\n".join(formatted_stack[start_stack_from:])
                + "\n"
                + "]" * 200
                + "\n"
            )

        return ChalkError(
            code=code,
            category=category,
            message=message,
            display_primary_key=display_primary_key,
            display_primary_key_fqn=display_primary_key_fqn,
            exception=exception,
            feature=feature,
            resolver=resolver,
        )

    if TYPE_CHECKING:
        # Defining __hash__ only when type checking
        # since pydantic provides a hash for frozen models
        def __hash__(self) -> int:
            ...


class ResolverRunStatus(str, Enum):
    """Status of a scheduled resolver run."""

    RECEIVED = "received"
    """The request to run the resolver has been received, and is running or scheduled."""

    SUCCEEDED = "succeeded"
    """The resolver run failed."""

    FAILED = "failed"
    """The resolver run succeeded."""


class ResolverRunResponse(BaseModel):
    """Status of a scheduled resolver run."""

    id: str
    """The ID of the resolver run."""

    status: ResolverRunStatus
    """The current status of the resolver run."""


class WhoAmIResponse(BaseModel):
    """Response for checking the authenticated user."""

    user: str
    """The ID of the user or service token making the query."""

    environment_id: Optional[str] = None
    """The environment under which the client's queries will be run, unless overridden"""

    team_id: Optional[str] = None
    """The team ID pertaining to the client"""


class FeatureResolutionMeta(BaseModel, frozen=True):
    """Detailed metadata about the execution of an online query."""

    chosen_resolver_fqn: str
    """The name of the resolver that computed the feature value."""

    cache_hit: bool
    """Whether the feature request was satisfied by a cached value."""

    primitive_type: Optional[str] = None
    """
    Primitive type name for the feature, e.g. `str` for `some_feature: str`.
    Returned only if query-level 'include_meta' is True.
    """

    version: int = 1
    """
    The version that was selected for this feature. Defaults to `default_version`, if query
    does not specify a constraint. If no versioning information is provided on the feature definition,
    the default version is `1`.
    """


class FeatureResult(BaseModel):
    field: str
    """
    The name of the feature requested, e.g. 'user.identity.has_voip_phone'.
    """

    value: Any  # Value should be a TJSON type
    """
    The value of the requested feature.
    If an error was encountered in resolving this feature,
    this field will be empty.
    """

    pkey: Any = None
    """The primary key of the resolved feature."""

    error: Optional[ChalkError] = None
    """
    The error code encountered in resolving this feature.
    If no error occurred, this field is empty.
    """

    valid: Optional[bool] = None
    """
    Whether the feature was resolved successfully.
    """

    ts: Optional[datetime] = None
    """
    The time at which this feature was computed.
    This value could be significantly in the past if you're using caching.
    """

    meta: Optional[FeatureResolutionMeta] = None
    """Detailed information about how this feature was computed."""

    metadata_val: Optional[int] = None
    """
    Value of the internal metadata that encodes information about how this feature was computed.
    """


class ExchangeCredentialsRequest(BaseModel):
    client_id: str
    client_secret: str
    grant_type: str
    scope: Optional[str] = None


class ExchangeCredentialsResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    # expires_at: datetime
    api_server: str
    primary_environment: Optional[str] = None
    engines: Optional[Mapping[str, str]] = None


class OfflineQueryInput(BaseModel):
    columns: List[str]
    values: List[List[Any]]  # Values should be of type TJSON


class OnlineQueryRequest(BaseModel):
    inputs: Mapping[str, Any]  # Values should be of type TJSON
    outputs: List[str]
    expression_outputs: List[str] = Field(default_factory=list)
    now: Optional[str] = None  # iso format so we can json
    staleness: Optional[Mapping[str, str]] = None
    context: Optional[OnlineQueryContext] = None
    include_meta: bool = True
    explain: Union[bool, Literal["only"]] = False
    skip_online_storage: Optional[bool] = False
    skip_offline_storage: Optional[bool] = False
    skip_metrics_storage: Optional[bool] = False
    skip_cache_lookups: Optional[bool] = False
    correlation_id: Optional[str] = None
    query_name: Optional[str] = None
    query_name_version: Optional[str] = None
    deployment_id: Optional[str] = None
    branch_id: Optional[str] = None
    meta: Optional[Mapping[str, str]] = None
    store_plan_stages: Optional[bool] = False
    encoding_options: FeatureEncodingOptions = FeatureEncodingOptions()
    planner_options: Optional[Mapping[str, Any]] = None
    query_context: Optional[ContextJsonDict] = None
    value_metrics_tag_by_features: Tuple[str, ...] = ()
    overlay_graph: Optional[str] = None  # base64-encoded chalk.graph.v1.OverlayGraph proto


@dataclasses.dataclass
class OnlineQuery:
    input: Union[Mapping[FeatureReference, Sequence[Any]], Any]
    output: Sequence[str]
    staleness: Optional[Mapping[str, str]] = None
    tags: Optional[Sequence[str]] = None
    required_resolver_tags: Optional[Sequence[str]] = None
    value_metrics_tag_by_features: Sequence[str] = ()
    planner_options: Optional[Mapping[str, Any]] = None


class OnlineQueryManyRequest(BaseModel):
    inputs: Mapping[str, List[Any]]
    outputs: List[str]
    expression_outputs: List[str] = Field(default_factory=list)
    now: Optional[List[str]] = None
    staleness: Optional[Mapping[str, str]] = None
    context: Optional[OnlineQueryContext] = None
    include_meta: bool = True
    explain: bool = False
    skip_online_storage: Optional[bool] = False
    skip_offline_storage: Optional[bool] = False
    skip_metrics_storage: Optional[bool] = False
    skip_cache_lookups: Optional[bool] = False
    correlation_id: Optional[str] = None
    query_name: Optional[str] = None
    query_name_version: Optional[str] = None
    deployment_id: Optional[str] = None
    branch_id: Optional[str] = None
    meta: Optional[Mapping[str, str]] = None
    store_plan_stages: Optional[bool] = False
    query_context: Optional[ContextJsonDict] = None
    encoding_options: FeatureEncodingOptions = FeatureEncodingOptions()
    value_metrics_tag_by_features: Tuple[str, ...] = ()
    overlay_graph: Optional[str] = None


class MultiUploadFeaturesRequest(ByteBaseModel):
    features: List[str]
    table_compression: str
    table_bytes: bytes


class MultiUploadFeaturesResponse(BaseModel):
    operation_id: str
    errors: List[ChalkError]


class PersistenceSettings(BaseModel):
    persist_online_storage: Optional[bool] = None
    persist_offline_storage: Optional[bool] = None


class TriggerResolverRunRequest(BaseModel):
    resolver_fqn: str
    upper_bound: Optional[str] = None
    lower_bound: Optional[str] = None
    timestamping_mode: Literal["feature_time", "online_store_write_time"] = "feature_time"
    persistence_settings: Optional[PersistenceSettings] = None
    override_target_image_tag: Optional[str] = None
    idempotency_key: Optional[str] = None


class QueryMeta(BaseModel, extra=Extra.allow):
    execution_duration_s: float
    """
    The time, expressed in seconds, that Chalk spent executing this query.
    """

    deployment_id: Optional[str] = None
    """
    The id of the deployment that served this query.
    """

    environment_id: Optional[str] = None
    """
    The id of the environment that served this query. Not intended to be human readable, but helpful for support.
    """

    environment_name: Optional[str] = None
    """
    The short name of the environment that served this query. For example: "dev" or "prod".
    """

    query_id: Optional[str] = None
    """
    A unique ID generated and persisted by Chalk for this query. All computed features, metrics, and logs are
    associated with this ID. Your system can store this ID for audit and debugging workflows.
    """

    query_timestamp: Optional[datetime] = None
    """
    At the start of query execution, Chalk computes 'datetime.now()'. This value is used to timestamp computed features.
    """

    query_hash: Optional[str] = None
    """
    Deterministic hash of the 'structure' of the query. Queries that have the same input/output features will
    typically have the same hash; changes may be observed over time as we adjust implementation details.
    """

    explain_output: Optional[str] = None
    """
    An unstructured string containing diagnostic information about the query execution. Only included if `explain` is True.
    """


class OnlineQueryResponse(BaseModel):
    data: List[FeatureResult]
    errors: Optional[List[ChalkError]] = None
    meta: Optional[QueryMeta] = None

    def for_fqn(self, fqn: str):
        return next((x for x in self.data if x.field == fqn), None)

    class Config:
        json_encoders = {
            np.integer: int,
            np.floating: float,
        }


@dataclasses.dataclass
class BulkUploadFeaturesResult:
    errors: List[ChalkError]
    trace_id: Optional[str] = None


@dataclasses.dataclass
class BulkOnlineQueryResult:
    """
    Represents the result of a single `OnlineQuery`, returned by
    `query_bulk`.

    The `scalars_df` member holds the primary results of the `OnlineQuery`.
    Access this data using `to_polars()` or `to_pandas()`.
    """

    scalars_df: Optional[pl.DataFrame]
    groups_dfs: Optional[Dict[str, pl.DataFrame]]  # change to chalk df whenever we figure out pydantic
    errors: Optional[List[ChalkError]]
    meta: Optional[QueryMeta]
    trace_id: Optional[str] = None
    """Chalk Support can use this trace ID to investigate a query if an internal error occurs."""

    def to_polars(self) -> pl.DataFrame:
        """
        Allows access to the results of an `OnlineQuery` submitted to `query_bulk` as a Polars dataframe.
        """
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")

        return self.scalars_df if self.scalars_df is not None else pl.DataFrame()

    def to_pandas(self) -> pd.DataFrame:
        """
        Allows access to the results of an `OnlineQuery` submitted to `query_bulk` as a Pandas dataframe.
        """
        if self.scalars_df is not None:
            return self.scalars_df.to_pandas()
        else:
            import pandas as pd

            return pd.DataFrame()

    # def get_feature_value(self, pkey: str | int, f: FeatureReference):
    #     f_casted = ensure_feature(f)
    #     if f_casted.is_has_many:
    #         return self.groups_dfs[f_casted.root_fqn]
    #     else:
    #         return self.scalars_df[0][f_casted.root_fqn].item()


@dataclasses.dataclass
class BulkOnlineQueryResponse:
    results: List[BulkOnlineQueryResult]
    global_errors: List[ChalkError] = dataclasses.field(default_factory=list)
    """Errors that don't correspond to a specific individual query."""

    trace_id: Optional[str] = None
    """Chalk Support can use this trace ID to investigate a query if an internal error occurs."""

    def __getitem__(self, item: int):
        """
        Support `client.query_bulk(...)[0]` syntax.
        """
        return self.results[item]


class SpineSqlRequest(BaseModel):
    sql_query: str


class OfflineQueryInputUri(BaseModel):
    """
    Offline query input that was uploaded to cloud storage by the user.
    We need to figure out how to shard this data when creating jobs.
    The uris aren't in any bucket.
    """

    parquet_uri: str
    """A list of global uris of the sharded parquet files"""

    start_row: Optional[int] = None
    """The start row to read the parquet file from"""

    end_row: Optional[int] = None
    """The end row to read the parquet file from"""

    is_iceberg: bool = False
    """"If this is `True`, this represents an Iceberg source"""

    iceberg_snapshot_id: Optional[int] = None
    """The snapshot_id to use if parquet_uri points to an Iceberg metadata file"""

    iceberg_start_partition: Optional[int] = None
    """The index of the first partition file to load"""

    iceberg_end_partition: Optional[int] = None
    """One-after the index of the last partition file to load"""

    iceberg_filter: Optional[str] = None
    """A SQL filter string applied to the Iceberg source table."""

    aws_role_arn: Optional[str] = None
    """An AWS role arn to assume while performing Iceberg read operations"""

    aws_region: Optional[str] = None
    """The AWS region to query while performing Iceberg read operations"""

    column_name_to_feature_name: Optional[dict[str, Union[str, list[str]]]] = None
    """An optional remapping from column name to (namespace-qualified) Chalk feature names"""


def OfflineQueryIcebergUri(
    *,
    iceberg_uri: str,
    snapshot_id: Optional[int] = None,
    filter: Optional[str] = None,
    aws_role_arn: Optional[str] = None,
    aws_region: Optional[str] = None,
    column_name_to_feature_name: Optional[dict[str, Union[str, list[str]]]] = None,
    start_partition: Optional[int] = None,
    end_partition: Optional[int] = None,
):
    """
    Creates a query input for an Iceberg table.

    - `iceberg_uri`: The URI of a Glue table `glue://<account_id>/<database>/<table_name>` or the S3
      URI of an Iceberg metadata file `s3://example_bucket/example_table/00001-abcdef123.metadata.json`.

    - `snapshot_id`: The snapshot ID of the Iceberg table to read. If `None`, uses the current snapshot.

    - `filter`: A SQL filter expression applied as a filter to the rows of the Iceberg table.
    Iceberg filters can contain logical operations (AND, OR, NOT) and comparison between columns and constants.

    - `aws_role_arn`: A role to assume before accessing the Iceberg table.

    - `aws_region`: The region to load the Iceberg table from.

    - `column_name_to_feature_name`: A mapping from Iceberg column name to Chalk feature name.
    A column can be mapped to a single feature: `user_id: str(User.id)` or to multiple, e.g.
    `created_time: [str(User.created_time), "__ts__"]` to provide an input time column.
    """
    return OfflineQueryInputUri(
        is_iceberg=True,
        parquet_uri=iceberg_uri,
        iceberg_snapshot_id=snapshot_id,
        iceberg_start_partition=start_partition,
        iceberg_end_partition=end_partition,
        iceberg_filter=filter,
        aws_role_arn=aws_role_arn,
        aws_region=aws_region,
        column_name_to_feature_name=column_name_to_feature_name,
    )


class UploadedParquetShardedOfflineQueryInput(BaseModel):
    """
    Offline query input that is sharded parquet files uploaded to cloud storage.
    """

    filenames: Tuple[str, ...] = Field(description="A list of filenames of the sharded parquet files")
    version: OfflineQueryGivensVersion = Field(description="Version of how the inputs is represented in a table")


def _matches_pattern(pattern: str):
    return Field(pattern=pattern, regex=pattern)


class ResourceRequests(BaseModel):
    """
    Override resource requests for processes with isolated resources, e.g., offline queries and cron jobs.
    Note that making these too large could prevent your job from being scheduled, so please test
    before using these in a recurring pipeline.
    """

    cpu: Optional[str] = _matches_pattern(r"^(\d+(\.\d+)?m?)$")
    """
    CPU requests: Increasing this will make some Chalk operations that are parallel and CPU-bound faster.
    Default unit is physical CPU cores, i.e. "8" means 8 CPU cores, "0.5" means half of a CPU core.
    An alternative unit is "millicore", which is one-thousandth of a CPU core, i.e. 500m is half of a CPU core.
    """

    memory: Optional[str] = _matches_pattern(MEMORY_REGEX)
    """
    Memory requests: you can use these to give your pod more memory, i.e. to prevent especially large jobs from OOMing.
    Default unit is bytes, i.e. 1000000000 is 1 gigabyte of memory.
    You can also specify a suffix such as K, M, or G for kilobytes, megabytes, and gigabytes, respectively.
    It's also possible to use the power of two equivalents, such as Ki, Mi, and Gi.
    """

    ephemeral_volume_size: Optional[str] = _matches_pattern(MEMORY_REGEX)
    """Chalk can use this for spilling intermediate state of some large computations, i.e.
    joins, aggregations, and sorting.
    Default unit is bytes, i.e. 1000000000 is 1 gigabyte of memory.
    You can also specify a suffix such as K, M, or G for kilobytes, megabytes, and gigabytes, respectively.
    It's also possible to use the power of two equivalents, such as Ki, Mi, and Gi.
    """

    ephemeral_storage: Optional[str] = _matches_pattern(MEMORY_REGEX)
    """Ephemeral storage for miscellaneous file system access.
    Should probably not be below 1Gi to ensure there's enough space for the Docker image, etc.
    Should also not be too high or else the pod will not be scheduled.
    """

    resource_group: Optional[str] = None
    """Resource group to use for this job. If not specified, the default resource group will be used."""


class CreateOfflineQueryJobRequest(BaseModel):
    output: List[str]
    """A list of output feature root fqns to query"""

    output_expressions: List[str] = Field(default_factory=list)
    """A list of underscore expressions to compute as query outputs, encoded as
    b64-serialized `FeatureExpression` protos"""

    required_output: List[str] = Field(default_factory=list)
    """A list of required output feature root fqns"""

    required_output_expressions: List[str] = Field(default_factory=list)
    """A list of required underscore expressions feature root fqns, , encoded as b64-serialized FeatureExpression protos"""

    destination_format: str
    """The desired output format. Should be 'CSV' or 'PARQUET'"""

    job_id: Optional[uuid.UUID] = None
    """A unique job id. If not specified, one will be auto generated by the server. If specified by the client,
    then jobs with the same ID will be rejected."""

    input: Union[
        OfflineQueryInput,
        Tuple[OfflineQueryInput, ...],
        None,
        UploadedParquetShardedOfflineQueryInput,
        OfflineQueryInputUri,
    ] = None
    """Any givens"""

    max_samples: Optional[int] = None
    """The maximum number of samples. If None, no limit"""

    # Defaults to ``OFFLINE_QUERY_MAX_CACHE_AGE_SECS`` in the chalkengine config
    max_cache_age_secs: Optional[int] = None
    """The maximum staleness, in seconds, for how old the view on the offline store can be.
    That is, data ingested within this interval will not be reflected in this offline query.
    Set to ``0`` to ignore the cache. If not specified, it defaults to 30 minutes.
    """

    observed_at_lower_bound: Optional[str] = None
    """The lower bound for the observed at timestamp (inclusive). If not specified, defaults to the beginning of time"""

    observed_at_upper_bound: Optional[str] = None
    """The upper bound for the observed at timestamp (inclusive). If not specified, defaults to the end of time."""

    dataset_name: Optional[str] = None
    branch: Optional[str] = None
    recompute_features: Union[bool, List[str]] = False
    sample_features: Optional[List[str]] = None
    store_plan_stages: bool = False
    explain: Union[bool, Literal["only"]] = False  # only is deprecated, leaving for backcompat
    tags: Optional[List[str]] = None
    required_resolver_tags: Optional[List[str]] = None
    """
    If specified, all resolvers invoked as part of this query must be tagged with all of these tags.
    Can be used to ensure that expensive resolvers are not executed.
    """

    correlation_id: Optional[str] = None
    query_context: Optional[ContextJsonDict] = None
    planner_options: Optional[Mapping[str, Any]] = None
    use_multiple_computers: bool = False

    spine_sql_query: Optional[Union[str, SpineSqlRequest]] = None

    recompute_request_revision_id: Optional[str] = None
    resources: Optional[ResourceRequests] = None
    env_overrides: Optional[Dict[str, str]] = None

    override_target_image_tag: Optional[str] = None
    enable_profiling: bool = False
    """Enable engine profiling for the job"""

    store_online: bool = False
    store_offline: bool = False

    num_shards: Optional[int] = None
    num_workers: Optional[int] = None
    feature_for_lower_upper_bound: Optional[str] = None

    completion_deadline: Optional[str] = None
    max_retries: Optional[int] = None

    use_job_queue: bool = False

    overlay_graph: Optional[str] = None

    @root_validator
    def _validate_multiple_computers(cls, values: Dict[str, Any]):
        if values["input"] is None or isinstance(
            values["input"], (UploadedParquetShardedOfflineQueryInput, OfflineQueryInputUri)
        ):
            return values
        expected_use_multiple_computers = isinstance(values["input"], tuple)
        if values["use_multiple_computers"] != expected_use_multiple_computers:
            raise ValueError("input should be tuple or uploaded shards exactly when use_multiple_computers is True")
        return values


class OutputExpression(BaseModel):
    base64_proto: str
    python_repr: str
    output_column_name: Optional[str] = None


class CreatePromptEvaluationRequest(CreateOfflineQueryJobRequest):
    prompts: List[Union[Prompt, str]]
    dataset_id: Optional[str] = None
    dataset_revision_id: Optional[str] = None
    reference_output: Optional[Union[OutputExpression, str]] = None
    evaluators: Optional[List[str]] = None
    related_named_prompt_ids: Optional[List[str]] = None
    related_evaluation_ids: Optional[List[str]] = None
    meta: Optional[Mapping[str, str]] = None
    overlay_graph: Optional[str] = None


class ComputeResolverOutputRequest(BaseModel):
    input: OfflineQueryInput
    resolver_fqn: str
    branch: Optional[str] = None
    environment: Optional[str] = None


class DatasetJobStatusRequest(BaseModel):
    job_id: Optional[str]  # same as revision_id
    dataset_id: Optional[str] = None
    dataset_name: Optional[str] = None
    ignore_errors: bool = False
    query_inputs: bool = False


class DatasetRecomputeRequest(BaseModel):
    dataset_name: Optional[str] = None
    branch: str
    dataset_id: Optional[str] = None
    revision_id: Optional[str] = None
    features: List[str]


class RecomputeResolverOutputRequest(BaseModel):
    persistent_id: str
    resolver_fqn: str
    branch: Optional[str] = None
    environment: Optional[str] = None


class ComputeResolverOutputResponse(BaseModel):
    job_id: str
    persistent_id: str
    errors: Optional[List[ChalkError]] = None


class OfflineQueryRequest(BaseModel):
    """V1 OfflineQueryRequest. Not used by the current Chalk Client."""

    output: List[str]  # output features which can be null
    input: Optional[OfflineQueryInput] = None
    dataset: Optional[str] = None
    resources: Optional[ResourceRequests] = None
    max_samples: Optional[int] = None
    max_cache_age_secs: Optional[int] = None
    required_outputs: List[str] = Field(default_factory=list)  # output features which cannot be null


class OfflineQueryResponse(BaseModel):
    """V1 OfflineQueryResponse. Not used by the current Chalk Client."""

    columns: List[str]
    output: List[List[Any]]  # values should be of TJSON types
    errors: Optional[List[ChalkError]] = None


class CreateOfflineQueryJobResponse(BaseModel):
    """
    Attributes:
        job_id: A job ID, which can be used to retrieve the results.
    """

    job_id: uuid.UUID
    version: int = 1  # Field is deprecated
    errors: Optional[List[ChalkError]] = None


class CreateBranchResponse(BaseModel):
    branch_already_exists: bool
    errors: Optional[List[ChalkError]] = None


class ColumnMetadata(BaseModel):
    """This entire model is deprecated."""

    feature_fqn: str
    """The root FQN of the feature for a column"""

    column_name: str
    """The name of the column that corresponds to this feature"""

    dtype: str
    """The data type for this feature"""
    # This field is currently a JSON-stringified version of the SerializeDType property
    # Using a string instead of a pydantic model the SerializedDType encoding does not affect
    # the api layer


class GetOfflineQueryJobResponse(BaseModel):
    is_finished: bool
    """Whether the export job is finished (it runs asynchronously)"""

    version: int = 1  # Backwards compatibility
    """Version number representing the format of the data. The client uses this version number
    to properly decode and load the query results into DataFrames."""

    urls: List[str]
    """A list of short-lived, authenticated URLs that the client can download to retrieve the exported data."""

    errors: Optional[List[ChalkError]] = None

    # deprecated
    columns: Optional[List[ColumnMetadata]] = None
    """Expected columns for the dataframe, including data type information"""


class QueryStatus(IntEnum):
    PENDING_SUBMISSION = 1
    """Pending submission to the database."""

    SUBMITTED = 2
    """Submitted to the database, but not yet running."""

    RUNNING = 3
    """Running in the database."""

    ERROR = 4
    """Error with either submitting or running the job."""

    EXPIRED = 5
    """The job did not complete before an expiration deadline, so there are no results."""

    CANCELLED = 6
    """Manually cancelled before it errored or finished successfully."""

    SUCCESSFUL = 7  #
    """Successfully ran the job."""


class DatasetSampleFilter(BaseModel):
    lower_bound: Union[datetime, timedelta, None] = None
    upper_bound: Union[datetime, timedelta, None] = None
    max_samples: Optional[int] = None


class DatasetFilter(BaseModel):
    sample_filters: DatasetSampleFilter = Field(default_factory=DatasetSampleFilter)
    max_cache_age_secs: Optional[float] = None


class DatasetPartitionResponse(BaseModel):
    performance_summary: Optional[str] = None


class DatasetRevisionResponse(BaseModel):
    dataset_name: Optional[str] = None
    dataset_id: Optional[uuid.UUID] = None
    environment_id: EnvironmentId
    revision_id: Optional[uuid.UUID] = None  # Currently, the revision ID is the job ID that created the revision
    creator_id: str
    outputs: List[str]
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    terminated_at: Optional[datetime] = None
    givens_uri: Optional[str] = None
    status: QueryStatus
    filters: DatasetFilter
    num_partitions: Optional[int] = None
    partitions: Optional[List[DatasetPartitionResponse]] = None
    num_bytes: Optional[int] = None
    output_uris: str
    output_version: int
    branch: Optional[str] = None
    dashboard_url: Optional[str] = None
    num_computers: int = 1
    errors: Optional[List[ChalkError]] = None
    metadata: Optional[Mapping[str, Any]] = None


class SetDatasetRevisionMetadataRequest(BaseModel):
    metadata: Mapping[str, Any]


class SetDatasetRevisionMetadataResponse(BaseModel):
    revision_id: str
    errors: Optional[List[ChalkError]] = None


class DatasetRecomputeResponse(DatasetRevisionResponse):
    num_computers: Literal[1] = 1  # pyright: ignore[reportIncompatibleVariableOverride]

    @classmethod
    def from_revision_response(
        cls, revision: DatasetRevisionResponse, errors: Optional[List[ChalkError]] = None
    ) -> "DatasetRecomputeResponse":
        return cls(
            revision_id=revision.revision_id,
            environment_id=revision.environment_id,
            creator_id=revision.creator_id,
            outputs=revision.outputs,
            givens_uri=revision.givens_uri,
            status=revision.status,
            filters=revision.filters,
            num_partitions=revision.num_partitions,
            output_uris=revision.output_uris,
            output_version=revision.output_version,
            num_bytes=revision.num_bytes,
            created_at=revision.created_at,
            started_at=revision.started_at,
            terminated_at=revision.terminated_at,
            dataset_name=revision.dataset_name,
            dataset_id=revision.dataset_id,
            branch=revision.branch,
            dashboard_url=revision.dashboard_url,
            errors=errors,
            num_computers=1,
        )


class DatasetResponse(BaseModel):
    is_finished: bool
    """Whether the export job is finished (it runs asynchronously)"""

    version: int = 1  # Backwards compatibility
    """Version number representing the format of the data. The client uses this version number
    to properly decode and load the query results into DataFrames."""

    environment_id: EnvironmentId
    dataset_id: Optional[uuid.UUID] = None
    dataset_name: Optional[str] = None
    revisions: List[DatasetRevisionResponse]
    errors: Optional[List[ChalkError]] = None


class DatasetRevisionResponseType(str, Enum):
    SUMMARY = "summary"
    """
    A summary of the output table
    """

    PREVIEW = "preview"
    """
    A preview (e.g. df.head()) of the output table
    """


class ShardBatchKey(BaseModel):
    shard_id: int
    """
    The identifier for the shard (or 'pod') on which the offline query was run.
    In standard offline queries, this value is always '0'.
    In asynchronous offline queries, this value is 0-indexed and
    incremented for every shard run on a kube pod.
    """

    batch_id: int
    """
    The identifier for the batch run on a single pod/server.
    In most cases, this value is '0', but offline queries may be multi-batch
    in the case of large primary key spines.
    """

    class Config:
        frozen = True

    def __hash__(self):
        return hash((self.shard_id, self.batch_id))

    def __str__(self):
        return f"{self.shard_id}_{self.batch_id}"

    @classmethod
    def from_str(cls, key_str: str) -> "ShardBatchKey":
        shard_id, batch_id = map(int, key_str.split("_"))
        return cls(shard_id=shard_id, batch_id=batch_id)


def read_parquet_with_shard_batch_columns(key: ShardBatchKey, url: str) -> pl.DataFrame:
    try:
        import polars as pl
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    return read_parquet(url).with_columns(
        [pl.lit(key.shard_id).alias("shard_id"), pl.lit(key.batch_id).alias("batch_id")]
    )


class DatasetRevisionInfoResponse(BaseModel):
    revision_id: uuid.UUID
    type: DatasetRevisionResponseType
    urls: Optional[Mapping[ShardBatchKey, str]] = None
    error: Optional[str] = None

    class Config:
        json_encoders = {ShardBatchKey: lambda v: str(v)}

    @validator("urls", pre=True)  # pyright: ignore[reportUntypedFunctionDecorator]
    def parse_shard_batch_key_map(
        cls, value: Optional[Union[Mapping[str, str], Mapping[ShardBatchKey, str]]]
    ) -> Union[Mapping[ShardBatchKey, str], None]:
        if value is None:
            return None
        return {(ShardBatchKey.from_str(k) if isinstance(k, str) else k): v for k, v in value.items()}

    def dict(self, **kwargs: Any) -> Dict[str, Any]:
        d = super().dict(**kwargs)
        if d.get("urls") is not None:
            d["urls"] = {str(k): v for k, v in d["urls"].items()}
        return d

    def json(self, *args: Any, **kwargs: Any) -> str:
        data = self.dict()
        if data.get("revision_id"):
            data["revision_id"] = str(data["revision_id"])
        return json.dumps(data, **kwargs)

    def get_shard_batch_keys(self) -> List[ShardBatchKey]:
        if self.urls is None or len(self.urls) == 0:
            default_err_msg = f"dataset revision '{self.revision_id}' {self.type.value} could not be found"
            raise ValueError(self.error or default_err_msg)
        return list(self.urls.keys())

    def concat_urls(self) -> pl.DataFrame:
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")
        assert self.urls is not None, "check self.urls is not None before this call"
        dfs = [read_parquet_with_shard_batch_columns(key, url) for key, url in self.urls.items()]
        return pl.concat(dfs)

    def to_polars(self, shard_batch_key: Optional[ShardBatchKey] = None) -> pl.LazyFrame:
        raise NotImplementedError("not implemented for base class")

    def to_pandas(self, shard_batch_key: Optional[ShardBatchKey] = None) -> pd.DataFrame:
        raise NotImplementedError("not implemented for base class")


DEFAULT_SHARD_BATCH_KEY = ShardBatchKey(shard_id=0, batch_id=0)


class DatasetRevisionSummaryResponse(DatasetRevisionInfoResponse):
    type: DatasetRevisionResponseType = DatasetRevisionResponseType.SUMMARY

    def to_polars(self, shard_batch_key: Optional[ShardBatchKey] = None) -> pl.LazyFrame:
        if shard_batch_key is None:
            shard_batch_key = DEFAULT_SHARD_BATCH_KEY
        if self.urls is None or len(self.urls) == 0:
            default_err_msg = f"dataset revision '{self.revision_id}' {self.type.value} could not be found"
            raise ValueError(self.error or default_err_msg)
        if shard_batch_key in self.urls:
            return read_parquet_with_shard_batch_columns(shard_batch_key, self.urls[shard_batch_key]).lazy()
        raise ValueError(f"ShardBatchKey {shard_batch_key} not found in return")

    def to_pandas(self, shard_batch_key: Optional[ShardBatchKey] = None) -> pd.DataFrame:
        if shard_batch_key is None:
            shard_batch_key = DEFAULT_SHARD_BATCH_KEY
        if self.urls is None or len(self.urls) == 0:
            default_err_msg = f"dataset revision '{self.revision_id}' {self.type.value} could not be found"
            raise ValueError(self.error or default_err_msg)
        if shard_batch_key in self.urls:
            return read_parquet_with_shard_batch_columns(shard_batch_key, self.urls[shard_batch_key]).to_pandas()
        raise ValueError(f"ShardBatchKey {shard_batch_key} not found in return")


class DatasetRevisionPreviewResponse(DatasetRevisionInfoResponse):
    type: DatasetRevisionResponseType = DatasetRevisionResponseType.PREVIEW

    def to_polars(self, shard_batch_key: Optional[ShardBatchKey] = None) -> pl.LazyFrame:
        if self.urls is None or len(self.urls) == 0:
            default_err_msg = f"dataset revision '{self.revision_id}' {self.type.value} could not be found"
            raise ValueError(self.error or default_err_msg)
        if shard_batch_key is None:
            return self.concat_urls().lazy()
        else:
            if shard_batch_key in self.urls:
                return read_parquet_with_shard_batch_columns(shard_batch_key, self.urls[shard_batch_key]).lazy()
            raise ValueError(f"ShardBatchKey {shard_batch_key} not found in return")

    def to_pandas(self, shard_batch_key: Optional[ShardBatchKey] = None) -> pd.DataFrame:
        if self.urls is None or len(self.urls) == 0:
            default_err_msg = f"dataset revision '{self.revision_id}' {self.type.value} could not be found"
            raise ValueError(self.error or default_err_msg)
        if shard_batch_key is None:
            return self.concat_urls().to_pandas()
        else:
            if shard_batch_key in self.urls:
                return read_parquet_with_shard_batch_columns(shard_batch_key, self.urls[shard_batch_key]).to_pandas()
            raise ValueError(f"ShardBatchKey {shard_batch_key} not found in return")


class SingleEntityUpdate(BaseModel):
    entity_type: Literal["feature", "resolver"]
    entity_fqn: str
    entity_shortname: str

    @classmethod
    def for_resolver(cls, resolver: Resolver) -> "SingleEntityUpdate":
        return cls(
            entity_type="resolver",
            entity_fqn=resolver.fqn,
            entity_shortname=resolver.fqn.split(".")[-1],
        )

    @classmethod
    def for_feature(cls, feature: Feature) -> "SingleEntityUpdate":
        return cls(
            entity_type="feature",
            entity_fqn=feature.fqn,
            entity_shortname=feature.name,
        )


class UpdateGraphEntityResponse(BaseModel):
    """
    Represents the result of live updating a graph entity like a resolver or feature class.
    This may result in multiple individual resolvers/features being updated, e.g. if the user
    adds a new feature class w/ multiple new fields.
    """

    added: Optional[List[SingleEntityUpdate]] = None
    modified: Optional[List[SingleEntityUpdate]] = None
    removed: Optional[List[SingleEntityUpdate]] = None

    errors: Optional[List[ChalkError]] = None


class UpdateResolverResponse(BaseModel):
    updated_fqn: Optional[str] = None
    """The resolver fqn that was updated (may not be the same as the one that was requested)"""

    is_new: Optional[bool] = None
    """Whether a new resolver was created, or if an existing one was replaced"""

    errors: Optional[List[ChalkError]] = None


class FeatureObservationDeletionRequest(BaseModel):
    """
    Represents a request to target particular feature observations for deletion. Note that
    the "features" and "tags" fields are mutually exclusive -- either only one of them is
    specified, or neither is specified, in which case deletion will proceed for all
    features of the primary keys specified.
    """

    namespace: str
    """
    The namespace in which the features targeted for deletion reside.
    """

    features: Optional[List[str]]
    """
    An optional list of the feature names of the features that should be deleted
    for the targeted primary keys. Not specifying this and not specifying the "tags" field
    will result in all features being targeted for deletion for the specified primary keys.
    Note that this parameter and the "tags" parameter are mutually exclusive.
    """

    tags: Optional[List[str]]
    """
    An optional list of tags that specify features that should be targeted for deletion.
    If a feature has a tag in this list, its observations for the primary keys you listed
    will be targeted for deletion. Not specifying this and not specifying the "features"
    field will result in all features being targeted for deletion for the specified primary
    keys. Note that this parameter and the "features" parameter are mutually exclusive.
    """

    primary_keys: List[str]
    """
    The primary keys of the observations that should be targeted for deletion.
    """

    retain_offline: bool = False
    """
    If True, the given observations will not be removed from the offline store. (False by default)
    """

    retain_online: bool = False
    """
    If True, the given observations will not be removed from the online store. (False by default)
    """


class FeatureObservationDeletionResponse(BaseModel):
    """
    Contains ChalkErrors for any failures, if any, that might have occurred when trying
    to delete the features that were requested.
    """

    errors: Optional[List[ChalkError]]


class FeatureDropRequest(BaseModel):
    namespace: str
    """Namespace in which the features targeted for drop reside."""

    features: List[str]
    """Names of the features that should be dropped."""

    retain_offline: bool = False
    """
    If True, the given features will not be removed from the offline store. (False by default)
    """

    retain_online: bool = False
    """
    If True, the given features will not be removed from the online store. (False by default)
    """


class FeatureDropResponse(BaseModel):
    """
    Contains ChalkErrors for any failures, if any, that might have occurred when trying
    to drop the features that were requested.
    """

    errors: Optional[List[ChalkError]]


class GetIncrementalProgressResponse(BaseModel):
    """
    Returns information about the current state of an incremental resolver.
    Specifically, the recorded timestamps that the resolver uses to process recent data.
    If both timestamp fields are returned as None, this means the current resolver hasn't
    run yet or hasn't stored any progress data. The next time it runs it will ingest all historical data

    More information at https://docs.chalk.ai/docs/sql#incremental-queries
    """

    environment_id: EnvironmentId

    resolver_fqn: str
    """The fully qualified name of the given resolver."""

    query_name: Optional[str] = None

    max_ingested_timestamp: Optional[datetime]
    """The latest timestamp found in ingested data."""

    last_execution_timestamp: Optional[datetime]
    """The latest timestamp at which the resolver was run. If configured to do so, the
    resolver uses this timestamp instead of max_ingested_timestamp to filter input data.
    If None, this means that this value isn't currently used by this resolver.
    """

    errors: Optional[List[ChalkError]] = None


class SetIncrementalProgressRequest(BaseModel):
    """
    Sets the current state of an incremental resolver, specifically the timestamps it uses
    to filter inputs to only recent data, to the given timestamps.

    More information at https://docs.chalk.ai/docs/sql#incremental-queries
    """

    max_ingested_timestamp: Optional[datetime] = None
    """The latest timestamp found in ingested data.
    Timestamp must have a timezone specified.
    """

    last_execution_timestamp: Optional[datetime] = None
    """The latest time the resolver was run. If configured to do so, the
    resolver uses this timestamp instead of max_ingested_timestamp to filter input data.
    Timestamp must have a timezone specified.
    """


class BranchDeployRequest(BaseModel):
    branch_name: str
    """Name of the branch. If branch does not exist, it will be created."""

    create_only: bool = False
    """If true, tries to create a new branch returns an error if the branch already exists."""

    source_deployment_id: Optional[str] = None
    """Use the given deployment's source on the branch. If None, the latest active deployment will be used."""


class BranchDeployResponse(BaseModel):
    branch_name: str
    new_branch_created: bool = False  # deprecated field, API Server takes care of this logic now.

    source_deployment_id: str
    branch_deployment_id: str

    proto_graph_b64: Optional[str] = None
    proto_export_b64: Optional[str] = None
    errors: List[ChalkError] = Field(default_factory=list)


class BranchStartRequest(BaseModel):
    branch_environment_id: str
    """
    The environment id of the branch to start.
    """


class BranchStartResponse(BaseModel):
    status: Union[Literal["ok"], Literal["error"]]
    message: str


BranchIdParam: TypeAlias = Union[None, str, "ellipsis"]
"""
Type used for the 'branch' parameter in calls to the Chalk Client.
The branch can either be:
 1. A string that is used as the branch name for the request
 2. None, in which case the request is _not_ sent to a branch server,
 3. Ellipsis (...), indicating that the branch name (or lack thereof) is
    inferred from the ChalkClient's current branch.
"""


class StreamResolverTestStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class StreamResolverTestMessagePayload(BaseModel):
    key: Optional[str]
    message_str: Optional[str]
    message_bytes: Optional[str]
    timestamp: Optional[datetime]

    class Config:
        # Add custom encoders to make `datetime` JSON serializable
        json_encoders = {datetime: lambda v: v.isoformat()}  # Converts datetime to ISO 8601 string

    def dict(self, *args: Any, **kwargs: Any):
        original_dict = super().dict(*args, **kwargs)
        encoders = self.__config__.json_encoders or {}
        return {
            key: (encoders[type(value)](value) if type(value) in encoders else value)
            for key, value in original_dict.items()
        }


class StreamResolverTestRequest(BaseModel):
    resolver_fqn: str
    num_messages: Optional[int] = None
    test_messages: Optional[List[StreamResolverTestMessagePayload]] = None
    kafka_auto_offset_reset: Optional[Literal["earliest", "latest"]] = "earliest"


class StreamResolverTestResponse(BaseModel):
    status: StreamResolverTestStatus
    data_uri: Optional[str] = None
    errors: Optional[List[ChalkError]] = None
    message: Optional[str] = None

    @property
    def features(self) -> pl.DataFrame:
        if self.data_uri is None:
            raise ValueError(
                (
                    "Features were not saved to storage. "
                    "Please inspect 'ResolverTestResponse.errors' and 'ResolverTestResponse.message'."
                )
            )
        return read_parquet(self.data_uri)


class FeatherBodyType(str, Enum):
    TABLE = "TABLE"
    RECORD_BATCHES = "RECORD_BATCHES"


class OnlineQueryResultFeather(ByteBaseModel):
    has_data: bool
    scalar_data: bytes
    groups_data: ByteDict
    errors: Optional[List[str]]  # inner str is json of ChalkError to mimic Optional[List[ChalkError]]
    meta: Optional[str]  # inner str is json of QueryMeta to mimic Optional[QueryMeta]


class OnlineQueryResponseFeather(ByteBaseModel):
    query_results_bytes: ByteDict


class ResolverReplayResponse(BaseModel):
    urls: Optional[List[str]] = None
    error: Optional[str] = None


class UploadFeaturesRequest(BaseModel):
    input: Mapping[str, List[Any]]  # Values should be of type List[TJSON]
    preview_deployment_id: Optional[str] = None
    correlation_id: Optional[str] = None
    query_name: Optional[str] = None
    meta: Optional[Mapping[str, str]] = None


class UploadFeaturesResponse(BaseModel):
    errors: List[ChalkError]
    """Errors that occurred during feature upload, if any."""

    trace_id: Optional[str] = None
    """If an internal error occurs, this trace ID can be sent to Chalk Support to help debug the root cause."""


class PlanQueryRequest(BaseModel):
    inputs: List[str]
    outputs: List[str]
    expression_outputs: List[str] = Field(default_factory=list)
    staleness: Optional[Mapping[str, str]] = None
    context: Optional[OnlineQueryContext] = None
    query_name: Optional[str] = None
    query_name_version: Optional[str] = None
    deployment_id: Optional[str] = None
    branch_id: Optional[str] = None
    meta: Optional[Mapping[str, str]] = None
    num_input_rows: Optional[int] = None
    explain: bool = False
    store_plan_stages: bool = False
    encoding_options: FeatureEncodingOptions = FeatureEncodingOptions()


class FeatureSchema(BaseModel):
    fqn: str
    primitive_type: Optional[str]
    rich_type: Optional[str]
    nullable: bool
    pyarrow_dtype: str


class PlanQueryResponse(BaseModel):
    rendered_plan: Optional[str]
    output_schema: List[FeatureSchema]
    errors: List[ChalkError]
    structured_plan: Optional[str] = None


class IngestDatasetRequest(BaseModel):
    revision_id: str
    """The ID of the dataset revision to ingest"""

    branch: Optional[str]
    """The branch to ingest the dataset into"""

    outputs: List[str]
    """The output features to return from the dataset"""

    store_online: bool
    """Whether to store the dataset into the online store"""

    store_offline: bool
    """Whether to store the dataset into the offline store"""

    enable_profiling: bool = False
    """Enable engine profiling for the ingestion"""

    planner_options: Optional[Mapping[str, Any]] = None

    online_timestamping_mode: Optional[str] = None
    explain: bool = False


class AnnotatedSignedUploadURL(BaseModel):
    signed_url: str
    """Signed URLs which can be uploaded to using PUT requests"""

    filename: str
    """Filenames which the signed URLs correspond to"""


class OfflineQueryParquetUploadURLResponse(BaseModel):
    # there is one pair of url for each partition
    urls: Tuple[AnnotatedSignedUploadURL, ...]
    """Signed URLs which can be uploaded to using PUT requests"""


class FeatureStatistics(BaseModel):
    feature_fqn: str
    count: int
    null_count: int
    zero_count: Optional[int]
    mean: Optional[float]
    std: Optional[float]
    max: Optional[float]
    min: Optional[float]
    # each tuple is of the form (percentile, value) where 0 (minimum) <= percentile <= 1 (maximum)
    approx_percentiles: Optional[List[Tuple[float, float]]]
    logical_type: Optional[str]


class FeatureStatisticsResponse(BaseModel):
    data: List[FeatureStatistics]


class PingRequest(BaseModel):
    num: Optional[int] = None


class PingResponse(BaseModel):
    num: int
