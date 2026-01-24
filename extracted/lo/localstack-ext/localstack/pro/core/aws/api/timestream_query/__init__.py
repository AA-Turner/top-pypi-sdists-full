from datetime import datetime
from enum import StrEnum
from typing import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

AmazonResourceName = str
ClientRequestToken = str
ClientToken = str
Double = float
ErrorMessage = str
MaxQueryCapacity = int
MaxQueryResults = int
MaxScheduledQueriesResults = int
MaxTagsForResourceResult = int
NextScheduledQueriesResultsToken = str
NextTagsForResourceResultsToken = str
NullableBoolean = bool
PaginationToken = str
PartitionKey = str
QueryId = str
QueryString = str
QueryTCU = int
ResourceName = str
S3BucketName = str
S3ObjectKey = str
S3ObjectKeyPrefix = str
ScalarValue = str
ScheduleExpression = str
ScheduledQueryName = str
SchemaName = str
ServiceErrorMessage = str
String = str
StringValue2048 = str
TagKey = str
TagValue = str
Timestamp = str


class ComputeMode(StrEnum):
    ON_DEMAND = "ON_DEMAND"
    PROVISIONED = "PROVISIONED"


class DimensionValueType(StrEnum):
    VARCHAR = "VARCHAR"


class LastUpdateStatus(StrEnum):
    PENDING = "PENDING"
    FAILED = "FAILED"
    SUCCEEDED = "SUCCEEDED"


class MeasureValueType(StrEnum):
    BIGINT = "BIGINT"
    BOOLEAN = "BOOLEAN"
    DOUBLE = "DOUBLE"
    VARCHAR = "VARCHAR"
    MULTI = "MULTI"


class QueryInsightsMode(StrEnum):
    ENABLED_WITH_RATE_CONTROL = "ENABLED_WITH_RATE_CONTROL"
    DISABLED = "DISABLED"


class QueryPricingModel(StrEnum):
    BYTES_SCANNED = "BYTES_SCANNED"
    COMPUTE_UNITS = "COMPUTE_UNITS"


class S3EncryptionOption(StrEnum):
    SSE_S3 = "SSE_S3"
    SSE_KMS = "SSE_KMS"


class ScalarMeasureValueType(StrEnum):
    BIGINT = "BIGINT"
    BOOLEAN = "BOOLEAN"
    DOUBLE = "DOUBLE"
    VARCHAR = "VARCHAR"
    TIMESTAMP = "TIMESTAMP"


class ScalarType(StrEnum):
    VARCHAR = "VARCHAR"
    BOOLEAN = "BOOLEAN"
    BIGINT = "BIGINT"
    DOUBLE = "DOUBLE"
    TIMESTAMP = "TIMESTAMP"
    DATE = "DATE"
    TIME = "TIME"
    INTERVAL_DAY_TO_SECOND = "INTERVAL_DAY_TO_SECOND"
    INTERVAL_YEAR_TO_MONTH = "INTERVAL_YEAR_TO_MONTH"
    UNKNOWN = "UNKNOWN"
    INTEGER = "INTEGER"


class ScheduledQueryInsightsMode(StrEnum):
    ENABLED_WITH_RATE_CONTROL = "ENABLED_WITH_RATE_CONTROL"
    DISABLED = "DISABLED"


class ScheduledQueryRunStatus(StrEnum):
    AUTO_TRIGGER_SUCCESS = "AUTO_TRIGGER_SUCCESS"
    AUTO_TRIGGER_FAILURE = "AUTO_TRIGGER_FAILURE"
    MANUAL_TRIGGER_SUCCESS = "MANUAL_TRIGGER_SUCCESS"
    MANUAL_TRIGGER_FAILURE = "MANUAL_TRIGGER_FAILURE"


class ScheduledQueryState(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class AccessDeniedException(ServiceException):
    """You do not have the necessary permissions to access the account
    settings.
    """

    code: str = "AccessDeniedException"
    sender_fault: bool = False
    status_code: int = 400


class ConflictException(ServiceException):
    """Unable to poll results for a cancelled query."""

    code: str = "ConflictException"
    sender_fault: bool = False
    status_code: int = 400


class InternalServerException(ServiceException):
    """An internal server error occurred while processing the request."""

    code: str = "InternalServerException"
    sender_fault: bool = False
    status_code: int = 400


class InvalidEndpointException(ServiceException):
    """The requested endpoint is invalid."""

    code: str = "InvalidEndpointException"
    sender_fault: bool = False
    status_code: int = 400


class QueryExecutionException(ServiceException):
    """Timestream was unable to run the query successfully."""

    code: str = "QueryExecutionException"
    sender_fault: bool = False
    status_code: int = 400


class ResourceNotFoundException(ServiceException):
    """The requested resource could not be found."""

    code: str = "ResourceNotFoundException"
    sender_fault: bool = False
    status_code: int = 400
    ScheduledQueryArn: AmazonResourceName | None


class ServiceQuotaExceededException(ServiceException):
    """You have exceeded the service quota."""

    code: str = "ServiceQuotaExceededException"
    sender_fault: bool = False
    status_code: int = 400


class ThrottlingException(ServiceException):
    """The request was throttled due to excessive requests."""

    code: str = "ThrottlingException"
    sender_fault: bool = False
    status_code: int = 400


class ValidationException(ServiceException):
    """Invalid or malformed request."""

    code: str = "ValidationException"
    sender_fault: bool = False
    status_code: int = 400


class SnsConfiguration(TypedDict, total=False):
    """Details on SNS that are required to send the notification."""

    TopicArn: AmazonResourceName


class AccountSettingsNotificationConfiguration(TypedDict, total=False):
    """Configuration settings for notifications related to account settings."""

    SnsConfiguration: SnsConfiguration | None
    RoleArn: AmazonResourceName


class CancelQueryRequest(ServiceRequest):
    QueryId: QueryId


class CancelQueryResponse(TypedDict, total=False):
    CancellationMessage: String | None


class ColumnInfo(TypedDict, total=False):
    """Contains the metadata for query results such as the column names, data
    types, and other attributes.
    """

    Name: "String | None"
    Type: "Type"


ColumnInfoList = list[ColumnInfo]


class Type(TypedDict, total=False):
    """Contains the data type of a column in a query result set. The data type
    can be scalar or complex. The supported scalar data types are integers,
    Boolean, string, double, timestamp, date, time, and intervals. The
    supported complex data types are arrays, rows, and timeseries.
    """

    ScalarType: ScalarType | None
    ArrayColumnInfo: ColumnInfo | None
    TimeSeriesMeasureValueColumnInfo: ColumnInfo | None
    RowColumnInfo: ColumnInfoList | None


class S3Configuration(TypedDict, total=False):
    """Details on S3 location for error reports that result from running a
    query.
    """

    BucketName: S3BucketName
    ObjectKeyPrefix: S3ObjectKeyPrefix | None
    EncryptionOption: S3EncryptionOption | None


class ErrorReportConfiguration(TypedDict, total=False):
    """Configuration required for error reporting."""

    S3Configuration: S3Configuration


class Tag(TypedDict, total=False):
    """A tag is a label that you assign to a Timestream database and/or table.
    Each tag consists of a key and an optional value, both of which you
    define. Tags enable you to categorize databases and/or tables, for
    example, by purpose, owner, or environment.
    """

    Key: TagKey
    Value: TagValue


TagList = list[Tag]


class MultiMeasureAttributeMapping(TypedDict, total=False):
    """Attribute mapping for MULTI value measures."""

    SourceColumn: SchemaName
    TargetMultiMeasureAttributeName: SchemaName | None
    MeasureValueType: ScalarMeasureValueType


MultiMeasureAttributeMappingList = list[MultiMeasureAttributeMapping]


class MixedMeasureMapping(TypedDict, total=False):
    """MixedMeasureMappings are mappings that can be used to ingest data into a
    mixture of narrow and multi measures in the derived table.
    """

    MeasureName: SchemaName | None
    SourceColumn: SchemaName | None
    TargetMeasureName: SchemaName | None
    MeasureValueType: MeasureValueType
    MultiMeasureAttributeMappings: MultiMeasureAttributeMappingList | None


MixedMeasureMappingList = list[MixedMeasureMapping]


class MultiMeasureMappings(TypedDict, total=False):
    """Only one of MixedMeasureMappings or MultiMeasureMappings is to be
    provided. MultiMeasureMappings can be used to ingest data as multi
    measures in the derived table.
    """

    TargetMultiMeasureName: SchemaName | None
    MultiMeasureAttributeMappings: MultiMeasureAttributeMappingList


class DimensionMapping(TypedDict, total=False):
    """This type is used to map column(s) from the query result to a dimension
    in the destination table.
    """

    Name: SchemaName
    DimensionValueType: DimensionValueType


DimensionMappingList = list[DimensionMapping]


class TimestreamConfiguration(TypedDict, total=False):
    """Configuration to write data into Timestream database and table. This
    configuration allows the user to map the query result select columns
    into the destination table columns.
    """

    DatabaseName: ResourceName
    TableName: ResourceName
    TimeColumn: SchemaName
    DimensionMappings: DimensionMappingList
    MultiMeasureMappings: MultiMeasureMappings | None
    MixedMeasureMappings: MixedMeasureMappingList | None
    MeasureNameColumn: SchemaName | None


class TargetConfiguration(TypedDict, total=False):
    """Configuration used for writing the output of a query."""

    TimestreamConfiguration: TimestreamConfiguration


class NotificationConfiguration(TypedDict, total=False):
    """Notification configuration for a scheduled query. A notification is sent
    by Timestream when a scheduled query is created, its state is updated or
    when it is deleted.
    """

    SnsConfiguration: SnsConfiguration


class ScheduleConfiguration(TypedDict, total=False):
    """Configuration of the schedule of the query."""

    ScheduleExpression: ScheduleExpression


class CreateScheduledQueryRequest(ServiceRequest):
    Name: ScheduledQueryName
    QueryString: QueryString
    ScheduleConfiguration: ScheduleConfiguration
    NotificationConfiguration: NotificationConfiguration
    TargetConfiguration: TargetConfiguration | None
    ClientToken: ClientToken | None
    ScheduledQueryExecutionRoleArn: AmazonResourceName
    Tags: TagList | None
    KmsKeyId: StringValue2048 | None
    ErrorReportConfiguration: ErrorReportConfiguration


class CreateScheduledQueryResponse(TypedDict, total=False):
    Arn: AmazonResourceName


class Datum(TypedDict, total=False):
    """Datum represents a single data point in a query result."""

    ScalarValue: "ScalarValue | None"
    TimeSeriesValue: "TimeSeriesDataPointList | None"
    ArrayValue: "DatumList | None"
    RowValue: "Row | None"
    NullValue: "NullableBoolean | None"


DatumList = list[Datum]


class Row(TypedDict, total=False):
    """Represents a single row in the query results."""

    Data: DatumList


class TimeSeriesDataPoint(TypedDict, total=False):
    """The timeseries data type represents the values of a measure over time. A
    time series is an array of rows of timestamps and measure values, with
    rows sorted in ascending order of time. A TimeSeriesDataPoint is a
    single data point in the time series. It represents a tuple of (time,
    measure value) in a time series.
    """

    Time: Timestamp
    Value: Datum


TimeSeriesDataPointList = list[TimeSeriesDataPoint]


class DeleteScheduledQueryRequest(ServiceRequest):
    ScheduledQueryArn: AmazonResourceName


class DescribeAccountSettingsRequest(ServiceRequest):
    pass


class LastUpdate(TypedDict, total=False):
    """Configuration object that contains the most recent account settings
    update, visible only if settings have been updated previously.
    """

    TargetQueryTCU: QueryTCU | None
    Status: LastUpdateStatus | None
    StatusMessage: String | None


class ProvisionedCapacityResponse(TypedDict, total=False):
    """The response to a request to update the provisioned capacity settings
    for querying data.
    """

    ActiveQueryTCU: QueryTCU | None
    NotificationConfiguration: AccountSettingsNotificationConfiguration | None
    LastUpdate: LastUpdate | None


class QueryComputeResponse(TypedDict, total=False):
    """The response to a request to retrieve or update the compute capacity
    settings for querying data.
    """

    ComputeMode: ComputeMode | None
    ProvisionedCapacity: ProvisionedCapacityResponse | None


class DescribeAccountSettingsResponse(TypedDict, total=False):
    MaxQueryTCU: MaxQueryCapacity | None
    QueryPricingModel: QueryPricingModel | None
    QueryCompute: QueryComputeResponse | None


class DescribeEndpointsRequest(ServiceRequest):
    pass


Long = int


class Endpoint(TypedDict, total=False):
    """Represents an available endpoint against which to make API calls
    against, as well as the TTL for that endpoint.
    """

    Address: String
    CachePeriodInMinutes: Long


Endpoints = list[Endpoint]


class DescribeEndpointsResponse(TypedDict, total=False):
    Endpoints: Endpoints


class DescribeScheduledQueryRequest(ServiceRequest):
    ScheduledQueryArn: AmazonResourceName


class S3ReportLocation(TypedDict, total=False):
    """S3 report location for the scheduled query run."""

    BucketName: S3BucketName | None
    ObjectKey: S3ObjectKey | None


class ErrorReportLocation(TypedDict, total=False):
    """This contains the location of the error report for a single scheduled
    query call.
    """

    S3ReportLocation: S3ReportLocation | None


class QueryTemporalRangeMax(TypedDict, total=False):
    """Provides insights into the table with the most sub-optimal temporal
    pruning scanned by your query.
    """

    Value: Long | None
    TableArn: AmazonResourceName | None


class QueryTemporalRange(TypedDict, total=False):
    """Provides insights into the temporal range of the query, including the
    table with the largest (max) time range.
    """

    Max: QueryTemporalRangeMax | None


PartitionKeyList = list[PartitionKey]


class QuerySpatialCoverageMax(TypedDict, total=False):
    """Provides insights into the table with the most sub-optimal spatial range
    scanned by your query.
    """

    Value: Double | None
    TableArn: AmazonResourceName | None
    PartitionKey: PartitionKeyList | None


class QuerySpatialCoverage(TypedDict, total=False):
    """Provides insights into the spatial coverage of the query, including the
    table with sub-optimal (max) spatial pruning. This information can help
    you identify areas for improvement in your partitioning strategy to
    enhance spatial pruning

    For example, you can do the following with the ``QuerySpatialCoverage``
    information:

    -  Add measure_name or use `customer-defined partition
       key <https://docs.aws.amazon.com/timestream/latest/developerguide/customer-defined-partition-keys.html>`__
       (CDPK) predicates.

    -  If you've already done the preceding action, remove functions around
       them or clauses, such as ``LIKE``.
    """

    Max: QuerySpatialCoverageMax | None


class ScheduledQueryInsightsResponse(TypedDict, total=False):
    """Provides various insights and metrics related to the
    ``ExecuteScheduledQueryRequest`` that was executed.
    """

    QuerySpatialCoverage: QuerySpatialCoverage | None
    QueryTemporalRange: QueryTemporalRange | None
    QueryTableCount: Long | None
    OutputRows: Long | None
    OutputBytes: Long | None


class ExecutionStats(TypedDict, total=False):
    """Statistics for a single scheduled query run."""

    ExecutionTimeInMillis: Long | None
    DataWrites: Long | None
    BytesMetered: Long | None
    CumulativeBytesScanned: Long | None
    RecordsIngested: Long | None
    QueryResultRows: Long | None


Time = datetime


class ScheduledQueryRunSummary(TypedDict, total=False):
    """Run summary for the scheduled query"""

    InvocationTime: Time | None
    TriggerTime: Time | None
    RunStatus: ScheduledQueryRunStatus | None
    ExecutionStats: ExecutionStats | None
    QueryInsightsResponse: ScheduledQueryInsightsResponse | None
    ErrorReportLocation: ErrorReportLocation | None
    FailureReason: ErrorMessage | None


ScheduledQueryRunSummaryList = list[ScheduledQueryRunSummary]


class ScheduledQueryDescription(TypedDict, total=False):
    """Structure that describes scheduled query."""

    Arn: AmazonResourceName
    Name: ScheduledQueryName
    QueryString: QueryString
    CreationTime: Time | None
    State: ScheduledQueryState
    PreviousInvocationTime: Time | None
    NextInvocationTime: Time | None
    ScheduleConfiguration: ScheduleConfiguration
    NotificationConfiguration: NotificationConfiguration
    TargetConfiguration: TargetConfiguration | None
    ScheduledQueryExecutionRoleArn: AmazonResourceName | None
    KmsKeyId: StringValue2048 | None
    ErrorReportConfiguration: ErrorReportConfiguration | None
    LastRunSummary: ScheduledQueryRunSummary | None
    RecentlyFailedRuns: ScheduledQueryRunSummaryList | None


class DescribeScheduledQueryResponse(TypedDict, total=False):
    ScheduledQuery: ScheduledQueryDescription


class ScheduledQueryInsights(TypedDict, total=False):
    """Encapsulates settings for enabling ``QueryInsights`` on an
    ``ExecuteScheduledQueryRequest``.
    """

    Mode: ScheduledQueryInsightsMode


class ExecuteScheduledQueryRequest(ServiceRequest):
    ScheduledQueryArn: AmazonResourceName
    InvocationTime: Time
    ClientToken: ClientToken | None
    QueryInsights: ScheduledQueryInsights | None


class ListScheduledQueriesRequest(ServiceRequest):
    MaxResults: MaxScheduledQueriesResults | None
    NextToken: NextScheduledQueriesResultsToken | None


class TimestreamDestination(TypedDict, total=False):
    """Destination for scheduled query."""

    DatabaseName: ResourceName | None
    TableName: ResourceName | None


class TargetDestination(TypedDict, total=False):
    """Destination details to write data for a target data source. Current
    supported data source is Timestream.
    """

    TimestreamDestination: TimestreamDestination | None


class ScheduledQuery(TypedDict, total=False):
    """Scheduled Query"""

    Arn: AmazonResourceName
    Name: ScheduledQueryName
    CreationTime: Time | None
    State: ScheduledQueryState
    PreviousInvocationTime: Time | None
    NextInvocationTime: Time | None
    ErrorReportConfiguration: ErrorReportConfiguration | None
    TargetDestination: TargetDestination | None
    LastRunStatus: ScheduledQueryRunStatus | None


ScheduledQueryList = list[ScheduledQuery]


class ListScheduledQueriesResponse(TypedDict, total=False):
    ScheduledQueries: ScheduledQueryList
    NextToken: NextScheduledQueriesResultsToken | None


class ListTagsForResourceRequest(ServiceRequest):
    ResourceARN: AmazonResourceName
    MaxResults: MaxTagsForResourceResult | None
    NextToken: NextTagsForResourceResultsToken | None


class ListTagsForResourceResponse(TypedDict, total=False):
    Tags: TagList
    NextToken: NextTagsForResourceResultsToken | None


class ParameterMapping(TypedDict, total=False):
    """Mapping for named parameters."""

    Name: String
    Type: Type


ParameterMappingList = list[ParameterMapping]


class PrepareQueryRequest(ServiceRequest):
    QueryString: QueryString
    ValidateOnly: NullableBoolean | None


class SelectColumn(TypedDict, total=False):
    """Details of the column that is returned by the query."""

    Name: String | None
    Type: Type | None
    DatabaseName: ResourceName | None
    TableName: ResourceName | None
    Aliased: NullableBoolean | None


SelectColumnList = list[SelectColumn]


class PrepareQueryResponse(TypedDict, total=False):
    QueryString: QueryString
    Columns: SelectColumnList
    Parameters: ParameterMappingList


class ProvisionedCapacityRequest(TypedDict, total=False):
    """A request to update the provisioned capacity settings for querying data."""

    TargetQueryTCU: QueryTCU
    NotificationConfiguration: AccountSettingsNotificationConfiguration | None


class QueryComputeRequest(TypedDict, total=False):
    """A request to retrieve or update the compute capacity settings for
    querying data.
    """

    ComputeMode: ComputeMode | None
    ProvisionedCapacity: ProvisionedCapacityRequest | None


class QueryInsights(TypedDict, total=False):
    """``QueryInsights`` is a performance tuning feature that helps you
    optimize your queries, reducing costs and improving performance. With
    ``QueryInsights``, you can assess the pruning efficiency of your queries
    and identify areas for improvement to enhance query performance. With
    ``QueryInsights``, you can also analyze the effectiveness of your
    queries in terms of temporal and spatial pruning, and identify
    opportunities to improve performance. Specifically, you can evaluate how
    well your queries use time-based and partition key-based indexing
    strategies to optimize data retrieval. To optimize query performance,
    it's essential that you fine-tune both the temporal and spatial
    parameters that govern query execution.

    The key metrics provided by ``QueryInsights`` are
    ``QuerySpatialCoverage`` and ``QueryTemporalRange``.
    ``QuerySpatialCoverage`` indicates how much of the spatial axis the
    query scans, with lower values being more efficient.
    ``QueryTemporalRange`` shows the time range scanned, with narrower
    ranges being more performant.

    **Benefits of QueryInsights**

    The following are the key benefits of using ``QueryInsights``:

    -  **Identifying inefficient queries** – ``QueryInsights`` provides
       information on the time-based and attribute-based pruning of the
       tables accessed by the query. This information helps you identify the
       tables that are sub-optimally accessed.

    -  **Optimizing your data model and partitioning** – You can use the
       ``QueryInsights`` information to access and fine-tune your data model
       and partitioning strategy.

    -  **Tuning queries** – ``QueryInsights`` highlights opportunities to
       use indexes more effectively.

    The maximum number of ``Query`` API requests you're allowed to make with
    ``QueryInsights`` enabled is 1 query per second (QPS). If you exceed
    this query rate, it might result in throttling.
    """

    Mode: QueryInsightsMode


class QueryInsightsResponse(TypedDict, total=False):
    """Provides various insights and metrics related to the query that you
    executed.
    """

    QuerySpatialCoverage: QuerySpatialCoverage | None
    QueryTemporalRange: QueryTemporalRange | None
    QueryTableCount: Long | None
    OutputRows: Long | None
    OutputBytes: Long | None
    UnloadPartitionCount: Long | None
    UnloadWrittenRows: Long | None
    UnloadWrittenBytes: Long | None


class QueryRequest(ServiceRequest):
    QueryString: QueryString
    ClientToken: ClientRequestToken | None
    NextToken: PaginationToken | None
    MaxRows: MaxQueryResults | None
    QueryInsights: QueryInsights | None


class QueryStatus(TypedDict, total=False):
    """Information about the status of the query, including progress and bytes
    scanned.
    """

    ProgressPercentage: Double | None
    CumulativeBytesScanned: Long | None
    CumulativeBytesMetered: Long | None


RowList = list[Row]


class QueryResponse(TypedDict, total=False):
    QueryId: QueryId
    NextToken: PaginationToken | None
    Rows: RowList
    ColumnInfo: ColumnInfoList
    QueryStatus: QueryStatus | None
    QueryInsightsResponse: QueryInsightsResponse | None


TagKeyList = list[TagKey]


class TagResourceRequest(ServiceRequest):
    ResourceARN: AmazonResourceName
    Tags: TagList


class TagResourceResponse(TypedDict, total=False):
    pass


class UntagResourceRequest(ServiceRequest):
    ResourceARN: AmazonResourceName
    TagKeys: TagKeyList


class UntagResourceResponse(TypedDict, total=False):
    pass


class UpdateAccountSettingsRequest(ServiceRequest):
    MaxQueryTCU: MaxQueryCapacity | None
    QueryPricingModel: QueryPricingModel | None
    QueryCompute: QueryComputeRequest | None


class UpdateAccountSettingsResponse(TypedDict, total=False):
    MaxQueryTCU: MaxQueryCapacity | None
    QueryPricingModel: QueryPricingModel | None
    QueryCompute: QueryComputeResponse | None


class UpdateScheduledQueryRequest(ServiceRequest):
    ScheduledQueryArn: AmazonResourceName
    State: ScheduledQueryState


class TimestreamQueryApi:
    service: str = "timestream-query"
    version: str = "2018-11-01"

    @handler("CancelQuery")
    def cancel_query(
        self, context: RequestContext, query_id: QueryId, **kwargs
    ) -> CancelQueryResponse:
        """Cancels a query that has been issued. Cancellation is provided only if
        the query has not completed running before the cancellation request was
        issued. Because cancellation is an idempotent operation, subsequent
        cancellation requests will return a ``CancellationMessage``, indicating
        that the query has already been canceled. See `code
        sample <https://docs.aws.amazon.com/timestream/latest/developerguide/code-samples.cancel-query.html>`__
        for details.

        :param query_id: The ID of the query that needs to be cancelled.
        :returns: CancelQueryResponse
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        :raises ValidationException:
        :raises InvalidEndpointException:
        """
        raise NotImplementedError

    @handler("CreateScheduledQuery")
    def create_scheduled_query(
        self,
        context: RequestContext,
        name: ScheduledQueryName,
        query_string: QueryString,
        schedule_configuration: ScheduleConfiguration,
        notification_configuration: NotificationConfiguration,
        scheduled_query_execution_role_arn: AmazonResourceName,
        error_report_configuration: ErrorReportConfiguration,
        target_configuration: TargetConfiguration | None = None,
        client_token: ClientToken | None = None,
        tags: TagList | None = None,
        kms_key_id: StringValue2048 | None = None,
        **kwargs,
    ) -> CreateScheduledQueryResponse:
        """Create a scheduled query that will be run on your behalf at the
        configured schedule. Timestream assumes the execution role provided as
        part of the ``ScheduledQueryExecutionRoleArn`` parameter to run the
        query. You can use the ``NotificationConfiguration`` parameter to
        configure notification for your scheduled query operations.

        :param name: Name of the scheduled query.
        :param query_string: The query string to run.
        :param schedule_configuration: The schedule configuration for the query.
        :param notification_configuration: Notification configuration for the scheduled query.
        :param scheduled_query_execution_role_arn: The ARN for the IAM role that Timestream will assume when running the
        scheduled query.
        :param error_report_configuration: Configuration for error reporting.
        :param target_configuration: Configuration used for writing the result of a query.
        :param client_token: Using a ClientToken makes the call to CreateScheduledQuery idempotent,
        in other words, making the same request repeatedly will produce the same
        result.
        :param tags: A list of key-value pairs to label the scheduled query.
        :param kms_key_id: The Amazon KMS key used to encrypt the scheduled query resource,
        at-rest.
        :returns: CreateScheduledQueryResponse
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ServiceQuotaExceededException:
        :raises ThrottlingException:
        :raises ValidationException:
        :raises InvalidEndpointException:
        """
        raise NotImplementedError

    @handler("DeleteScheduledQuery")
    def delete_scheduled_query(
        self, context: RequestContext, scheduled_query_arn: AmazonResourceName, **kwargs
    ) -> None:
        """Deletes a given scheduled query. This is an irreversible operation.

        :param scheduled_query_arn: The ARN of the scheduled query.
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ValidationException:
        :raises InvalidEndpointException:
        """
        raise NotImplementedError

    @handler("DescribeAccountSettings")
    def describe_account_settings(
        self, context: RequestContext, **kwargs
    ) -> DescribeAccountSettingsResponse:
        """Describes the settings for your account that include the query pricing
        model and the configured maximum TCUs the service can use for your query
        workload.

        You're charged only for the duration of compute units used for your
        workloads.

        :returns: DescribeAccountSettingsResponse
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        :raises InvalidEndpointException:
        """
        raise NotImplementedError

    @handler("DescribeEndpoints")
    def describe_endpoints(self, context: RequestContext, **kwargs) -> DescribeEndpointsResponse:
        """DescribeEndpoints returns a list of available endpoints to make
        Timestream API calls against. This API is available through both Write
        and Query.

        Because the Timestream SDKs are designed to transparently work with the
        service’s architecture, including the management and mapping of the
        service endpoints, *it is not recommended that you use this API unless*:

        -  You are using `VPC endpoints (Amazon Web Services PrivateLink) with
           Timestream <https://docs.aws.amazon.com/timestream/latest/developerguide/VPCEndpoints>`__

        -  Your application uses a programming language that does not yet have
           SDK support

        -  You require better control over the client-side implementation

        For detailed information on how and when to use and implement
        DescribeEndpoints, see `The Endpoint Discovery
        Pattern <https://docs.aws.amazon.com/timestream/latest/developerguide/Using.API.html#Using-API.endpoint-discovery>`__.

        :returns: DescribeEndpointsResponse
        :raises InternalServerException:
        :raises ValidationException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DescribeScheduledQuery")
    def describe_scheduled_query(
        self, context: RequestContext, scheduled_query_arn: AmazonResourceName, **kwargs
    ) -> DescribeScheduledQueryResponse:
        """Provides detailed information about a scheduled query.

        :param scheduled_query_arn: The ARN of the scheduled query.
        :returns: DescribeScheduledQueryResponse
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ValidationException:
        :raises InvalidEndpointException:
        """
        raise NotImplementedError

    @handler("ExecuteScheduledQuery")
    def execute_scheduled_query(
        self,
        context: RequestContext,
        scheduled_query_arn: AmazonResourceName,
        invocation_time: Time,
        client_token: ClientToken | None = None,
        query_insights: ScheduledQueryInsights | None = None,
        **kwargs,
    ) -> None:
        """You can use this API to run a scheduled query manually.

        If you enabled ``QueryInsights``, this API also returns insights and
        metrics related to the query that you executed as part of an Amazon SNS
        notification. ``QueryInsights`` helps with performance tuning of your
        query. For more information about ``QueryInsights``, see `Using query
        insights to optimize queries in Amazon
        Timestream <https://docs.aws.amazon.com/timestream/latest/developerguide/using-query-insights.html>`__.

        :param scheduled_query_arn: ARN of the scheduled query.
        :param invocation_time: The timestamp in UTC.
        :param client_token: Not used.
        :param query_insights: Encapsulates settings for enabling ``QueryInsights``.
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ValidationException:
        :raises InvalidEndpointException:
        """
        raise NotImplementedError

    @handler("ListScheduledQueries")
    def list_scheduled_queries(
        self,
        context: RequestContext,
        max_results: MaxScheduledQueriesResults | None = None,
        next_token: NextScheduledQueriesResultsToken | None = None,
        **kwargs,
    ) -> ListScheduledQueriesResponse:
        """Gets a list of all scheduled queries in the caller's Amazon account and
        Region. ``ListScheduledQueries`` is eventually consistent.

        :param max_results: The maximum number of items to return in the output.
        :param next_token: A pagination token to resume pagination.
        :returns: ListScheduledQueriesResponse
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        :raises ValidationException:
        :raises InvalidEndpointException:
        """
        raise NotImplementedError

    @handler("ListTagsForResource")
    def list_tags_for_resource(
        self,
        context: RequestContext,
        resource_arn: AmazonResourceName,
        max_results: MaxTagsForResourceResult | None = None,
        next_token: NextTagsForResourceResultsToken | None = None,
        **kwargs,
    ) -> ListTagsForResourceResponse:
        """List all tags on a Timestream query resource.

        :param resource_arn: The Timestream resource with tags to be listed.
        :param max_results: The maximum number of tags to return.
        :param next_token: A pagination token to resume pagination.
        :returns: ListTagsForResourceResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ValidationException:
        :raises InvalidEndpointException:
        """
        raise NotImplementedError

    @handler("PrepareQuery")
    def prepare_query(
        self,
        context: RequestContext,
        query_string: QueryString,
        validate_only: NullableBoolean | None = None,
        **kwargs,
    ) -> PrepareQueryResponse:
        """A synchronous operation that allows you to submit a query with
        parameters to be stored by Timestream for later running. Timestream only
        supports using this operation with ``ValidateOnly`` set to ``true``.

        :param query_string: The Timestream query string that you want to use as a prepared
        statement.
        :param validate_only: By setting this value to ``true``, Timestream will only validate that
        the query string is a valid Timestream query, and not store the prepared
        query for later use.
        :returns: PrepareQueryResponse
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        :raises ValidationException:
        :raises InvalidEndpointException:
        """
        raise NotImplementedError

    @handler("Query")
    def query(
        self,
        context: RequestContext,
        query_string: QueryString,
        client_token: ClientRequestToken | None = None,
        next_token: PaginationToken | None = None,
        max_rows: MaxQueryResults | None = None,
        query_insights: QueryInsights | None = None,
        **kwargs,
    ) -> QueryResponse:
        """``Query`` is a synchronous operation that enables you to run a query
        against your Amazon Timestream data.

        If you enabled ``QueryInsights``, this API also returns insights and
        metrics related to the query that you executed. ``QueryInsights`` helps
        with performance tuning of your query. For more information about
        ``QueryInsights``, see `Using query insights to optimize queries in
        Amazon
        Timestream <https://docs.aws.amazon.com/timestream/latest/developerguide/using-query-insights.html>`__.

        The maximum number of ``Query`` API requests you're allowed to make with
        ``QueryInsights`` enabled is 1 query per second (QPS). If you exceed
        this query rate, it might result in throttling.

        ``Query`` will time out after 60 seconds. You must update the default
        timeout in the SDK to support a timeout of 60 seconds. See the `code
        sample <https://docs.aws.amazon.com/timestream/latest/developerguide/code-samples.run-query.html>`__
        for details.

        Your query request will fail in the following cases:

        -  If you submit a ``Query`` request with the same client token outside
           of the 5-minute idempotency window.

        -  If you submit a ``Query`` request with the same client token, but
           change other parameters, within the 5-minute idempotency window.

        -  If the size of the row (including the query metadata) exceeds 1 MB,
           then the query will fail with the following error message:

           ``Query aborted as max page response size has been exceeded by the output result row``

        -  If the IAM principal of the query initiator and the result reader are
           not the same and/or the query initiator and the result reader do not
           have the same query string in the query requests, the query will fail
           with an ``Invalid pagination token`` error.

        :param query_string: The query to be run by Timestream.
        :param client_token: Unique, case-sensitive string of up to 64 ASCII characters specified
        when a ``Query`` request is made.
        :param next_token: A pagination token used to return a set of results.
        :param max_rows: The total number of rows to be returned in the ``Query`` output.
        :param query_insights: Encapsulates settings for enabling ``QueryInsights``.
        :returns: QueryResponse
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises QueryExecutionException:
        :raises ThrottlingException:
        :raises ValidationException:
        :raises InvalidEndpointException:
        """
        raise NotImplementedError

    @handler("TagResource")
    def tag_resource(
        self, context: RequestContext, resource_arn: AmazonResourceName, tags: TagList, **kwargs
    ) -> TagResourceResponse:
        """Associate a set of tags with a Timestream resource. You can then
        activate these user-defined tags so that they appear on the Billing and
        Cost Management console for cost allocation tracking.

        :param resource_arn: Identifies the Timestream resource to which tags should be added.
        :param tags: The tags to be assigned to the Timestream resource.
        :returns: TagResourceResponse
        :raises ResourceNotFoundException:
        :raises ServiceQuotaExceededException:
        :raises ThrottlingException:
        :raises ValidationException:
        :raises InvalidEndpointException:
        """
        raise NotImplementedError

    @handler("UntagResource")
    def untag_resource(
        self,
        context: RequestContext,
        resource_arn: AmazonResourceName,
        tag_keys: TagKeyList,
        **kwargs,
    ) -> UntagResourceResponse:
        """Removes the association of tags from a Timestream query resource.

        :param resource_arn: The Timestream resource that the tags will be removed from.
        :param tag_keys: A list of tags keys.
        :returns: UntagResourceResponse
        :raises ValidationException:
        :raises ThrottlingException:
        :raises ResourceNotFoundException:
        :raises InvalidEndpointException:
        """
        raise NotImplementedError

    @handler("UpdateAccountSettings")
    def update_account_settings(
        self,
        context: RequestContext,
        max_query_tcu: MaxQueryCapacity | None = None,
        query_pricing_model: QueryPricingModel | None = None,
        query_compute: QueryComputeRequest | None = None,
        **kwargs,
    ) -> UpdateAccountSettingsResponse:
        """Transitions your account to use TCUs for query pricing and modifies the
        maximum query compute units that you've configured. If you reduce the
        value of ``MaxQueryTCU`` to a desired configuration, the new value can
        take up to 24 hours to be effective.

        After you've transitioned your account to use TCUs for query pricing,
        you can't transition to using bytes scanned for query pricing.

        :param max_query_tcu: The maximum number of compute units the service will use at any point in
        time to serve your queries.
        :param query_pricing_model: The pricing model for queries in an account.
        :param query_compute: Modifies the query compute settings configured in your account,
        including the query pricing model and provisioned Timestream Compute
        Units (TCUs) in your account.
        :returns: UpdateAccountSettingsResponse
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        :raises ValidationException:
        :raises InvalidEndpointException:
        """
        raise NotImplementedError

    @handler("UpdateScheduledQuery")
    def update_scheduled_query(
        self,
        context: RequestContext,
        scheduled_query_arn: AmazonResourceName,
        state: ScheduledQueryState,
        **kwargs,
    ) -> None:
        """Update a scheduled query.

        :param scheduled_query_arn: ARN of the scheuled query.
        :param state: State of the scheduled query.
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ValidationException:
        :raises InvalidEndpointException:
        """
        raise NotImplementedError
