from datetime import datetime
from enum import StrEnum
from typing import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

Age = int
AllocatedDpusInteger = int
AmazonResourceName = str
AuthToken = str
AwsAccountId = str
Boolean = bool
BoxedBoolean = bool
CalculationExecutionId = str
CalculationResultType = str
CapacityReservationName = str
CatalogNameString = str
ClientRequestToken = str
CodeBlock = str
CommentString = str
CoordinatorDpuSize = int
DatabaseString = str
DefaultExecutorDpuSize = int
DescriptionString = str
DpuCount = float
ErrorCategory = int
ErrorCode = str
ErrorMessage = str
ErrorType = int
ExecutionParameter = str
ExecutorId = str
ExpressionString = str
IdempotencyToken = str
IdentityCenterApplicationArn = str
IdentityCenterInstanceArn = str
Integer = int
KeyString = str
KmsKey = str
LogGroupName = str
LogStreamNamePrefix = str
LogTypeKey = str
LogTypeValue = str
MaxApplicationDPUSizesCount = int
MaxCalculationsCount = int
MaxCapacityReservationsCount = int
MaxConcurrentDpus = int
MaxDataCatalogsCount = int
MaxDatabasesCount = int
MaxEngineVersionsCount = int
MaxListExecutorsCount = int
MaxNamedQueriesCount = int
MaxNotebooksCount = int
MaxPreparedStatementsCount = int
MaxQueryExecutionsCount = int
MaxQueryResults = int
MaxSessionsCount = int
MaxTableMetadataCount = int
MaxTagsCount = int
MaxWorkGroupsCount = int
NameString = str
NamedQueryDescriptionString = str
NamedQueryId = str
NotebookId = str
NotebookName = str
ParametersMapValue = str
Payload = str
QueryExecutionId = str
QueryString = str
ResultOutputLocation = str
RoleArn = str
S3OutputLocation = str
S3Uri = str
SessionId = str
SessionIdleTimeoutInMinutes = int
SessionManagerToken = str
StatementName = str
String = str
TableTypeString = str
TagKey = str
TagValue = str
TargetDpusInteger = int
Token = str
TypeString = str
WorkGroupDescriptionString = str
WorkGroupName = str
datumString = str


class AuthenticationType(StrEnum):
    DIRECTORY_IDENTITY = "DIRECTORY_IDENTITY"


class CalculationExecutionState(StrEnum):
    CREATING = "CREATING"
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    CANCELING = "CANCELING"
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class CapacityAllocationStatus(StrEnum):
    PENDING = "PENDING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class CapacityReservationStatus(StrEnum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    CANCELLING = "CANCELLING"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"
    UPDATE_PENDING = "UPDATE_PENDING"


class ColumnNullable(StrEnum):
    NOT_NULL = "NOT_NULL"
    NULLABLE = "NULLABLE"
    UNKNOWN = "UNKNOWN"


class ConnectionType(StrEnum):
    DYNAMODB = "DYNAMODB"
    MYSQL = "MYSQL"
    POSTGRESQL = "POSTGRESQL"
    REDSHIFT = "REDSHIFT"
    ORACLE = "ORACLE"
    SYNAPSE = "SYNAPSE"
    SQLSERVER = "SQLSERVER"
    DB2 = "DB2"
    OPENSEARCH = "OPENSEARCH"
    BIGQUERY = "BIGQUERY"
    GOOGLECLOUDSTORAGE = "GOOGLECLOUDSTORAGE"
    HBASE = "HBASE"
    DOCUMENTDB = "DOCUMENTDB"
    CMDB = "CMDB"
    TPCDS = "TPCDS"
    TIMESTREAM = "TIMESTREAM"
    SAPHANA = "SAPHANA"
    SNOWFLAKE = "SNOWFLAKE"
    DATALAKEGEN2 = "DATALAKEGEN2"
    DB2AS400 = "DB2AS400"


class DataCatalogStatus(StrEnum):
    CREATE_IN_PROGRESS = "CREATE_IN_PROGRESS"
    CREATE_COMPLETE = "CREATE_COMPLETE"
    CREATE_FAILED = "CREATE_FAILED"
    CREATE_FAILED_CLEANUP_IN_PROGRESS = "CREATE_FAILED_CLEANUP_IN_PROGRESS"
    CREATE_FAILED_CLEANUP_COMPLETE = "CREATE_FAILED_CLEANUP_COMPLETE"
    CREATE_FAILED_CLEANUP_FAILED = "CREATE_FAILED_CLEANUP_FAILED"
    DELETE_IN_PROGRESS = "DELETE_IN_PROGRESS"
    DELETE_COMPLETE = "DELETE_COMPLETE"
    DELETE_FAILED = "DELETE_FAILED"


class DataCatalogType(StrEnum):
    LAMBDA = "LAMBDA"
    GLUE = "GLUE"
    HIVE = "HIVE"
    FEDERATED = "FEDERATED"


class EncryptionOption(StrEnum):
    SSE_S3 = "SSE_S3"
    SSE_KMS = "SSE_KMS"
    CSE_KMS = "CSE_KMS"


class ExecutorState(StrEnum):
    CREATING = "CREATING"
    CREATED = "CREATED"
    REGISTERED = "REGISTERED"
    TERMINATING = "TERMINATING"
    TERMINATED = "TERMINATED"
    FAILED = "FAILED"


class ExecutorType(StrEnum):
    COORDINATOR = "COORDINATOR"
    GATEWAY = "GATEWAY"
    WORKER = "WORKER"


class NotebookType(StrEnum):
    IPYNB = "IPYNB"


class QueryExecutionState(StrEnum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class QueryResultType(StrEnum):
    DATA_MANIFEST = "DATA_MANIFEST"
    DATA_ROWS = "DATA_ROWS"


class S3AclOption(StrEnum):
    BUCKET_OWNER_FULL_CONTROL = "BUCKET_OWNER_FULL_CONTROL"


class SessionState(StrEnum):
    CREATING = "CREATING"
    CREATED = "CREATED"
    IDLE = "IDLE"
    BUSY = "BUSY"
    TERMINATING = "TERMINATING"
    TERMINATED = "TERMINATED"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"


class StatementType(StrEnum):
    DDL = "DDL"
    DML = "DML"
    UTILITY = "UTILITY"


class ThrottleReason(StrEnum):
    CONCURRENT_QUERY_LIMIT_EXCEEDED = "CONCURRENT_QUERY_LIMIT_EXCEEDED"


class WorkGroupState(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class InternalServerException(ServiceException):
    """Indicates a platform issue, which may be due to a transient condition or
    outage.
    """

    code: str = "InternalServerException"
    sender_fault: bool = False
    status_code: int = 400


class InvalidRequestException(ServiceException):
    """Indicates that something is wrong with the input to the request. For
    example, a required parameter may be missing or out of range.
    """

    code: str = "InvalidRequestException"
    sender_fault: bool = False
    status_code: int = 400
    AthenaErrorCode: ErrorCode | None


class MetadataException(ServiceException):
    """An exception that Athena received when it called a custom metastore.
    Occurs if the error is not caused by user input
    (``InvalidRequestException``) or from the Athena platform
    (``InternalServerException``). For example, if a user-created Lambda
    function is missing permissions, the Lambda ``4XX`` exception is
    returned in a ``MetadataException``.
    """

    code: str = "MetadataException"
    sender_fault: bool = False
    status_code: int = 400


class ResourceNotFoundException(ServiceException):
    """A resource, such as a workgroup, was not found."""

    code: str = "ResourceNotFoundException"
    sender_fault: bool = False
    status_code: int = 400
    ResourceName: AmazonResourceName | None


class SessionAlreadyExistsException(ServiceException):
    """The specified session already exists."""

    code: str = "SessionAlreadyExistsException"
    sender_fault: bool = False
    status_code: int = 400


class TooManyRequestsException(ServiceException):
    """Indicates that the request was throttled."""

    code: str = "TooManyRequestsException"
    sender_fault: bool = False
    status_code: int = 400
    Reason: ThrottleReason | None


class AclConfiguration(TypedDict, total=False):
    """Indicates that an Amazon S3 canned ACL should be set to control
    ownership of stored query results, including data files inserted by
    Athena as the result of statements like CTAS or INSERT INTO. When Athena
    stores query results in Amazon S3, the canned ACL is set with the
    ``x-amz-acl`` request header. For more information about S3 Object
    Ownership, see `Object Ownership
    settings <https://docs.aws.amazon.com/AmazonS3/latest/userguide/about-object-ownership.html#object-ownership-overview>`__
    in the *Amazon S3 User Guide*.
    """

    S3AclOption: S3AclOption


SupportedDPUSizeList = list[Integer]


class ApplicationDPUSizes(TypedDict, total=False):
    """Contains the application runtime IDs and their supported DPU sizes."""

    ApplicationRuntimeId: NameString | None
    SupportedDPUSizes: SupportedDPUSizeList | None


ApplicationDPUSizesList = list[ApplicationDPUSizes]


class AthenaError(TypedDict, total=False):
    """Provides information about an Athena query error. The ``AthenaError``
    feature provides standardized error information to help you understand
    failed queries and take steps after a query failure occurs.
    ``AthenaError`` includes an ``ErrorCategory`` field that specifies
    whether the cause of the failed query is due to system error, user
    error, or other error.
    """

    ErrorCategory: ErrorCategory | None
    ErrorType: ErrorType | None
    Retryable: Boolean | None
    ErrorMessage: String | None


NamedQueryIdList = list[NamedQueryId]


class BatchGetNamedQueryInput(ServiceRequest):
    """Contains an array of named query IDs."""

    NamedQueryIds: NamedQueryIdList


class UnprocessedNamedQueryId(TypedDict, total=False):
    """Information about a named query ID that could not be processed."""

    NamedQueryId: NamedQueryId | None
    ErrorCode: ErrorCode | None
    ErrorMessage: ErrorMessage | None


UnprocessedNamedQueryIdList = list[UnprocessedNamedQueryId]


class NamedQuery(TypedDict, total=False):
    """A query, where ``QueryString`` contains the SQL statements that make up
    the query.
    """

    Name: NameString
    Description: DescriptionString | None
    Database: DatabaseString
    QueryString: QueryString
    NamedQueryId: NamedQueryId | None
    WorkGroup: WorkGroupName | None


NamedQueryList = list[NamedQuery]


class BatchGetNamedQueryOutput(TypedDict, total=False):
    NamedQueries: NamedQueryList | None
    UnprocessedNamedQueryIds: UnprocessedNamedQueryIdList | None


PreparedStatementNameList = list[StatementName]


class BatchGetPreparedStatementInput(ServiceRequest):
    PreparedStatementNames: PreparedStatementNameList
    WorkGroup: WorkGroupName


class UnprocessedPreparedStatementName(TypedDict, total=False):
    """The name of a prepared statement that could not be returned."""

    StatementName: StatementName | None
    ErrorCode: ErrorCode | None
    ErrorMessage: ErrorMessage | None


UnprocessedPreparedStatementNameList = list[UnprocessedPreparedStatementName]
Date = datetime


class PreparedStatement(TypedDict, total=False):
    """A prepared SQL statement for use with Athena."""

    StatementName: StatementName | None
    QueryStatement: QueryString | None
    WorkGroupName: WorkGroupName | None
    Description: DescriptionString | None
    LastModifiedTime: Date | None


PreparedStatementDetailsList = list[PreparedStatement]


class BatchGetPreparedStatementOutput(TypedDict, total=False):
    PreparedStatements: PreparedStatementDetailsList | None
    UnprocessedPreparedStatementNames: UnprocessedPreparedStatementNameList | None


QueryExecutionIdList = list[QueryExecutionId]


class BatchGetQueryExecutionInput(ServiceRequest):
    """Contains an array of query execution IDs."""

    QueryExecutionIds: QueryExecutionIdList


class UnprocessedQueryExecutionId(TypedDict, total=False):
    """Describes a query execution that failed to process."""

    QueryExecutionId: QueryExecutionId | None
    ErrorCode: ErrorCode | None
    ErrorMessage: ErrorMessage | None


UnprocessedQueryExecutionIdList = list[UnprocessedQueryExecutionId]


class QueryResultsS3AccessGrantsConfiguration(TypedDict, total=False):
    """Specifies whether Amazon S3 access grants are enabled for query results."""

    EnableS3AccessGrants: BoxedBoolean
    CreateUserLevelPrefix: BoxedBoolean | None
    AuthenticationType: AuthenticationType


ExecutionParameters = list[ExecutionParameter]


class EngineVersion(TypedDict, total=False):
    """The Athena engine version for running queries, or the PySpark engine
    version for running sessions.
    """

    SelectedEngineVersion: NameString | None
    EffectiveEngineVersion: NameString | None


class ResultReuseInformation(TypedDict, total=False):
    """Contains information about whether the result of a previous query was
    reused.
    """

    ReusedPreviousResult: Boolean


Long = int


class QueryExecutionStatistics(TypedDict, total=False):
    """The amount of data scanned during the query execution and the amount of
    time that it took to execute, and the type of statement that was run.
    """

    EngineExecutionTimeInMillis: Long | None
    DataScannedInBytes: Long | None
    DataManifestLocation: String | None
    TotalExecutionTimeInMillis: Long | None
    QueryQueueTimeInMillis: Long | None
    ServicePreProcessingTimeInMillis: Long | None
    QueryPlanningTimeInMillis: Long | None
    ServiceProcessingTimeInMillis: Long | None
    ResultReuseInformation: ResultReuseInformation | None
    DpuCount: DpuCount | None


class QueryExecutionStatus(TypedDict, total=False):
    """The completion date, current state, submission time, and state change
    reason (if applicable) for the query execution.
    """

    State: QueryExecutionState | None
    StateChangeReason: String | None
    SubmissionDateTime: Date | None
    CompletionDateTime: Date | None
    AthenaError: AthenaError | None


class QueryExecutionContext(TypedDict, total=False):
    """The database and data catalog context in which the query execution
    occurs.
    """

    Database: DatabaseString | None
    Catalog: CatalogNameString | None


class ResultReuseByAgeConfiguration(TypedDict, total=False):
    """Specifies whether previous query results are reused, and if so, their
    maximum age.
    """

    Enabled: Boolean
    MaxAgeInMinutes: Age | None


class ResultReuseConfiguration(TypedDict, total=False):
    """Specifies the query result reuse behavior for the query."""

    ResultReuseByAgeConfiguration: ResultReuseByAgeConfiguration | None


class EncryptionConfiguration(TypedDict, total=False):
    """If query and calculation results are encrypted in Amazon S3, indicates
    the encryption option used (for example, ``SSE_KMS`` or ``CSE_KMS``) and
    key information.
    """

    EncryptionOption: EncryptionOption
    KmsKey: String | None


class ResultConfiguration(TypedDict, total=False):
    """The location in Amazon S3 where query and calculation results are stored
    and the encryption option, if any, used for query and calculation
    results. These are known as "client-side settings". If workgroup
    settings override client-side settings, then the query uses the
    workgroup settings.
    """

    OutputLocation: ResultOutputLocation | None
    EncryptionConfiguration: EncryptionConfiguration | None
    ExpectedBucketOwner: AwsAccountId | None
    AclConfiguration: AclConfiguration | None


class ManagedQueryResultsEncryptionConfiguration(TypedDict, total=False):
    """If you encrypt query and calculation results in Athena owned storage,
    this field indicates the encryption option (for example, SSE_KMS or
    CSE_KMS) and key information.
    """

    KmsKey: KmsKey


class ManagedQueryResultsConfiguration(TypedDict, total=False):
    """The configuration for storing results in Athena owned storage, which
    includes whether this feature is enabled; whether encryption
    configuration, if any, is used for encrypting query results.
    """

    Enabled: Boolean
    EncryptionConfiguration: ManagedQueryResultsEncryptionConfiguration | None


class QueryExecution(TypedDict, total=False):
    """Information about a single instance of a query execution."""

    QueryExecutionId: QueryExecutionId | None
    Query: QueryString | None
    StatementType: StatementType | None
    ManagedQueryResultsConfiguration: ManagedQueryResultsConfiguration | None
    ResultConfiguration: ResultConfiguration | None
    ResultReuseConfiguration: ResultReuseConfiguration | None
    QueryExecutionContext: QueryExecutionContext | None
    Status: QueryExecutionStatus | None
    Statistics: QueryExecutionStatistics | None
    WorkGroup: WorkGroupName | None
    EngineVersion: EngineVersion | None
    ExecutionParameters: ExecutionParameters | None
    SubstatementType: String | None
    QueryResultsS3AccessGrantsConfiguration: QueryResultsS3AccessGrantsConfiguration | None


QueryExecutionList = list[QueryExecution]


class BatchGetQueryExecutionOutput(TypedDict, total=False):
    QueryExecutions: QueryExecutionList | None
    UnprocessedQueryExecutionIds: UnprocessedQueryExecutionIdList | None


BytesScannedCutoffValue = int


class CalculationConfiguration(TypedDict, total=False):
    """Contains configuration information for the calculation."""

    CodeBlock: CodeBlock | None


class CalculationResult(TypedDict, total=False):
    """Contains information about an application-specific calculation result."""

    StdOutS3Uri: S3Uri | None
    StdErrorS3Uri: S3Uri | None
    ResultS3Uri: S3Uri | None
    ResultType: CalculationResultType | None


class CalculationStatistics(TypedDict, total=False):
    """Contains statistics for a notebook calculation."""

    DpuExecutionInMillis: Long | None
    Progress: DescriptionString | None


class CalculationStatus(TypedDict, total=False):
    """Contains information about the status of a notebook calculation."""

    SubmissionDateTime: Date | None
    CompletionDateTime: Date | None
    State: CalculationExecutionState | None
    StateChangeReason: DescriptionString | None


class CalculationSummary(TypedDict, total=False):
    """Summary information for a notebook calculation."""

    CalculationExecutionId: CalculationExecutionId | None
    Description: DescriptionString | None
    Status: CalculationStatus | None


CalculationsList = list[CalculationSummary]


class CancelCapacityReservationInput(ServiceRequest):
    Name: CapacityReservationName


class CancelCapacityReservationOutput(TypedDict, total=False):
    pass


Timestamp = datetime


class CapacityAllocation(TypedDict, total=False):
    """Contains the submission time of a single allocation request for a
    capacity reservation and the most recent status of the attempted
    allocation.
    """

    Status: CapacityAllocationStatus
    StatusMessage: String | None
    RequestTime: Timestamp
    RequestCompletionTime: Timestamp | None


WorkGroupNamesList = list[WorkGroupName]


class CapacityAssignment(TypedDict, total=False):
    """A mapping between one or more workgroups and a capacity reservation."""

    WorkGroupNames: WorkGroupNamesList | None


CapacityAssignmentsList = list[CapacityAssignment]


class CapacityAssignmentConfiguration(TypedDict, total=False):
    """Assigns Athena workgroups (and hence their queries) to capacity
    reservations. A capacity reservation can have only one capacity
    assignment configuration, but the capacity assignment configuration can
    be made up of multiple individual assignments. Each assignment specifies
    how Athena queries can consume capacity from the capacity reservation
    that their workgroup is mapped to.
    """

    CapacityReservationName: CapacityReservationName | None
    CapacityAssignments: CapacityAssignmentsList | None


class CapacityReservation(TypedDict, total=False):
    """A reservation for a specified number of data processing units (DPUs).
    When a reservation is initially created, it has no DPUs. Athena
    allocates DPUs until the allocated amount equals the requested amount.
    """

    Name: CapacityReservationName
    Status: CapacityReservationStatus
    TargetDpus: TargetDpusInteger
    AllocatedDpus: AllocatedDpusInteger
    LastAllocation: CapacityAllocation | None
    LastSuccessfulAllocationTime: Timestamp | None
    CreationTime: Timestamp


CapacityReservationsList = list[CapacityReservation]
ParametersMap = dict[KeyString, ParametersMapValue]


class Classification(TypedDict, total=False):
    """A classification refers to a set of specific configurations."""

    Name: NameString | None
    Properties: ParametersMap | None


ClassificationList = list[Classification]
LogTypeValuesList = list[LogTypeValue]
LogTypesMap = dict[LogTypeKey, LogTypeValuesList]


class CloudWatchLoggingConfiguration(TypedDict, total=False):
    """Configuration settings for delivering logs to Amazon CloudWatch log
    groups.
    """

    Enabled: BoxedBoolean
    LogGroup: LogGroupName | None
    LogStreamNamePrefix: LogStreamNamePrefix | None
    LogTypes: LogTypesMap | None


class Column(TypedDict, total=False):
    """Contains metadata for a column in a table."""

    Name: NameString
    Type: TypeString | None
    Comment: CommentString | None


class ColumnInfo(TypedDict, total=False):
    """Information about the columns in a query execution result."""

    CatalogName: String | None
    SchemaName: String | None
    TableName: String | None
    Name: String
    Label: String | None
    Type: String
    Precision: Integer | None
    Scale: Integer | None
    Nullable: ColumnNullable | None
    CaseSensitive: Boolean | None


ColumnInfoList = list[ColumnInfo]
ColumnList = list[Column]


class Tag(TypedDict, total=False):
    """A label that you assign to a resource. Athena resources include
    workgroups, data catalogs, and capacity reservations. Each tag consists
    of a key and an optional value, both of which you define. For example,
    you can use tags to categorize Athena resources by purpose, owner, or
    environment. Use a consistent set of tag keys to make it easier to
    search and filter the resources in your account. For best practices, see
    `Tagging Best
    Practices <https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/tagging-best-practices.html>`__.
    Tag keys can be from 1 to 128 UTF-8 Unicode characters, and tag values
    can be from 0 to 256 UTF-8 Unicode characters. Tags can use letters and
    numbers representable in UTF-8, and the following characters: + - = . _
    : / @. Tag keys and values are case-sensitive. Tag keys must be unique
    per resource. If you specify more than one tag, separate them by commas.
    """

    Key: TagKey | None
    Value: TagValue | None


TagList = list[Tag]


class CreateCapacityReservationInput(ServiceRequest):
    TargetDpus: TargetDpusInteger
    Name: CapacityReservationName
    Tags: TagList | None


class CreateCapacityReservationOutput(TypedDict, total=False):
    pass


class CreateDataCatalogInput(ServiceRequest):
    Name: CatalogNameString
    Type: DataCatalogType
    Description: DescriptionString | None
    Parameters: ParametersMap | None
    Tags: TagList | None


class DataCatalog(TypedDict, total=False):
    """Contains information about a data catalog in an Amazon Web Services
    account.

    In the Athena console, data catalogs are listed as "data sources" on the
    **Data sources** page under the **Data source name** column.
    """

    Name: CatalogNameString
    Description: DescriptionString | None
    Type: DataCatalogType
    Parameters: ParametersMap | None
    Status: DataCatalogStatus | None
    ConnectionType: ConnectionType | None
    Error: ErrorMessage | None


class CreateDataCatalogOutput(TypedDict, total=False):
    DataCatalog: DataCatalog | None


class CreateNamedQueryInput(ServiceRequest):
    Name: NameString
    Description: DescriptionString | None
    Database: DatabaseString
    QueryString: QueryString
    ClientRequestToken: IdempotencyToken | None
    WorkGroup: WorkGroupName | None


class CreateNamedQueryOutput(TypedDict, total=False):
    NamedQueryId: NamedQueryId | None


class CreateNotebookInput(ServiceRequest):
    WorkGroup: WorkGroupName
    Name: NotebookName
    ClientRequestToken: ClientRequestToken | None


class CreateNotebookOutput(TypedDict, total=False):
    NotebookId: NotebookId | None


class CreatePreparedStatementInput(ServiceRequest):
    StatementName: StatementName
    WorkGroup: WorkGroupName
    QueryStatement: QueryString
    Description: DescriptionString | None


class CreatePreparedStatementOutput(TypedDict, total=False):
    pass


class CreatePresignedNotebookUrlRequest(ServiceRequest):
    SessionId: SessionId


class CreatePresignedNotebookUrlResponse(TypedDict, total=False):
    NotebookUrl: String
    AuthToken: AuthToken
    AuthTokenExpirationTime: Long


class IdentityCenterConfiguration(TypedDict, total=False):
    """Specifies whether the workgroup is IAM Identity Center supported."""

    EnableIdentityCenter: BoxedBoolean | None
    IdentityCenterInstanceArn: IdentityCenterInstanceArn | None


class CustomerContentEncryptionConfiguration(TypedDict, total=False):
    """Specifies the customer managed KMS key that is used to encrypt the
    user's data stores in Athena. When an Amazon Web Services managed key is
    used, this value is null. This setting does not apply to Athena SQL
    workgroups.
    """

    KmsKey: KmsKey


class EngineConfiguration(TypedDict, total=False):
    """Contains data processing unit (DPU) configuration settings and parameter
    mappings for a notebook engine.
    """

    CoordinatorDpuSize: CoordinatorDpuSize | None
    MaxConcurrentDpus: MaxConcurrentDpus | None
    DefaultExecutorDpuSize: DefaultExecutorDpuSize | None
    AdditionalConfigs: ParametersMap | None
    SparkProperties: ParametersMap | None
    Classifications: ClassificationList | None


class S3LoggingConfiguration(TypedDict, total=False):
    """Configuration settings for delivering logs to Amazon S3 buckets."""

    Enabled: BoxedBoolean
    KmsKey: KmsKey | None
    LogLocation: S3OutputLocation | None


class ManagedLoggingConfiguration(TypedDict, total=False):
    """Configuration settings for delivering logs to Amazon S3 buckets."""

    Enabled: BoxedBoolean
    KmsKey: KmsKey | None


class MonitoringConfiguration(TypedDict, total=False):
    """Contains the configuration settings for managed log persistence,
    delivering logs to Amazon S3 buckets, Amazon CloudWatch log groups etc.
    """

    CloudWatchLoggingConfiguration: CloudWatchLoggingConfiguration | None
    ManagedLoggingConfiguration: ManagedLoggingConfiguration | None
    S3LoggingConfiguration: S3LoggingConfiguration | None


class WorkGroupConfiguration(TypedDict, total=False):
    """The configuration of the workgroup, which includes the location in
    Amazon S3 where query and calculation results are stored, the encryption
    option, if any, used for query and calculation results, whether the
    Amazon CloudWatch Metrics are enabled for the workgroup and whether
    workgroup settings override query settings, and the data usage limits
    for the amount of data scanned per query or per workgroup. The workgroup
    settings override is specified in ``EnforceWorkGroupConfiguration``
    (true/false) in the ``WorkGroupConfiguration``. See
    WorkGroupConfiguration$EnforceWorkGroupConfiguration.
    """

    ResultConfiguration: ResultConfiguration | None
    ManagedQueryResultsConfiguration: ManagedQueryResultsConfiguration | None
    EnforceWorkGroupConfiguration: BoxedBoolean | None
    PublishCloudWatchMetricsEnabled: BoxedBoolean | None
    BytesScannedCutoffPerQuery: BytesScannedCutoffValue | None
    RequesterPaysEnabled: BoxedBoolean | None
    EngineVersion: EngineVersion | None
    AdditionalConfiguration: NameString | None
    ExecutionRole: RoleArn | None
    MonitoringConfiguration: MonitoringConfiguration | None
    EngineConfiguration: EngineConfiguration | None
    CustomerContentEncryptionConfiguration: CustomerContentEncryptionConfiguration | None
    EnableMinimumEncryptionConfiguration: BoxedBoolean | None
    IdentityCenterConfiguration: IdentityCenterConfiguration | None
    QueryResultsS3AccessGrantsConfiguration: QueryResultsS3AccessGrantsConfiguration | None


class CreateWorkGroupInput(ServiceRequest):
    Name: WorkGroupName
    Configuration: WorkGroupConfiguration | None
    Description: WorkGroupDescriptionString | None
    Tags: TagList | None


class CreateWorkGroupOutput(TypedDict, total=False):
    pass


class DataCatalogSummary(TypedDict, total=False):
    """The summary information for the data catalog, which includes its name
    and type.
    """

    CatalogName: CatalogNameString | None
    Type: DataCatalogType | None
    Status: DataCatalogStatus | None
    ConnectionType: ConnectionType | None
    Error: ErrorMessage | None


DataCatalogSummaryList = list[DataCatalogSummary]


class Database(TypedDict, total=False):
    """Contains metadata information for a database in a data catalog."""

    Name: NameString
    Description: DescriptionString | None
    Parameters: ParametersMap | None


DatabaseList = list[Database]


class Datum(TypedDict, total=False):
    """A piece of data (a field in the table)."""

    VarCharValue: datumString | None


class DeleteCapacityReservationInput(ServiceRequest):
    Name: CapacityReservationName


class DeleteCapacityReservationOutput(TypedDict, total=False):
    pass


class DeleteDataCatalogInput(ServiceRequest):
    Name: CatalogNameString
    DeleteCatalogOnly: Boolean | None


class DeleteDataCatalogOutput(TypedDict, total=False):
    DataCatalog: DataCatalog | None


class DeleteNamedQueryInput(ServiceRequest):
    NamedQueryId: NamedQueryId


class DeleteNamedQueryOutput(TypedDict, total=False):
    pass


class DeleteNotebookInput(ServiceRequest):
    NotebookId: NotebookId


class DeleteNotebookOutput(TypedDict, total=False):
    pass


class DeletePreparedStatementInput(ServiceRequest):
    StatementName: StatementName
    WorkGroup: WorkGroupName


class DeletePreparedStatementOutput(TypedDict, total=False):
    pass


class DeleteWorkGroupInput(ServiceRequest):
    WorkGroup: WorkGroupName
    RecursiveDeleteOption: BoxedBoolean | None


class DeleteWorkGroupOutput(TypedDict, total=False):
    pass


EngineVersionsList = list[EngineVersion]


class ExecutorsSummary(TypedDict, total=False):
    """Contains summary information about an executor."""

    ExecutorId: ExecutorId
    ExecutorType: ExecutorType | None
    StartDateTime: Long | None
    TerminationDateTime: Long | None
    ExecutorState: ExecutorState | None
    ExecutorSize: Long | None


ExecutorsSummaryList = list[ExecutorsSummary]


class ExportNotebookInput(ServiceRequest):
    NotebookId: NotebookId


class NotebookMetadata(TypedDict, total=False):
    """Contains metadata for notebook, including the notebook name, ID,
    workgroup, and time created.
    """

    NotebookId: NotebookId | None
    Name: NotebookName | None
    WorkGroup: WorkGroupName | None
    CreationTime: Date | None
    Type: NotebookType | None
    LastModifiedTime: Date | None


class ExportNotebookOutput(TypedDict, total=False):
    NotebookMetadata: NotebookMetadata | None
    Payload: Payload | None


class FilterDefinition(TypedDict, total=False):
    """A string for searching notebook names."""

    Name: NotebookName | None


class GetCalculationExecutionCodeRequest(ServiceRequest):
    CalculationExecutionId: CalculationExecutionId


class GetCalculationExecutionCodeResponse(TypedDict, total=False):
    CodeBlock: CodeBlock | None


class GetCalculationExecutionRequest(ServiceRequest):
    CalculationExecutionId: CalculationExecutionId


class GetCalculationExecutionResponse(TypedDict, total=False):
    CalculationExecutionId: CalculationExecutionId | None
    SessionId: SessionId | None
    Description: DescriptionString | None
    WorkingDirectory: S3Uri | None
    Status: CalculationStatus | None
    Statistics: CalculationStatistics | None
    Result: CalculationResult | None


class GetCalculationExecutionStatusRequest(ServiceRequest):
    CalculationExecutionId: CalculationExecutionId


class GetCalculationExecutionStatusResponse(TypedDict, total=False):
    Status: CalculationStatus | None
    Statistics: CalculationStatistics | None


class GetCapacityAssignmentConfigurationInput(ServiceRequest):
    CapacityReservationName: CapacityReservationName


class GetCapacityAssignmentConfigurationOutput(TypedDict, total=False):
    CapacityAssignmentConfiguration: CapacityAssignmentConfiguration


class GetCapacityReservationInput(ServiceRequest):
    Name: CapacityReservationName


class GetCapacityReservationOutput(TypedDict, total=False):
    CapacityReservation: CapacityReservation


class GetDataCatalogInput(ServiceRequest):
    Name: CatalogNameString
    WorkGroup: WorkGroupName | None


class GetDataCatalogOutput(TypedDict, total=False):
    DataCatalog: DataCatalog | None


class GetDatabaseInput(ServiceRequest):
    CatalogName: CatalogNameString
    DatabaseName: NameString
    WorkGroup: WorkGroupName | None


class GetDatabaseOutput(TypedDict, total=False):
    Database: Database | None


class GetNamedQueryInput(ServiceRequest):
    NamedQueryId: NamedQueryId


class GetNamedQueryOutput(TypedDict, total=False):
    NamedQuery: NamedQuery | None


class GetNotebookMetadataInput(ServiceRequest):
    NotebookId: NotebookId


class GetNotebookMetadataOutput(TypedDict, total=False):
    NotebookMetadata: NotebookMetadata | None


class GetPreparedStatementInput(ServiceRequest):
    StatementName: StatementName
    WorkGroup: WorkGroupName


class GetPreparedStatementOutput(TypedDict, total=False):
    PreparedStatement: PreparedStatement | None


class GetQueryExecutionInput(ServiceRequest):
    QueryExecutionId: QueryExecutionId


class GetQueryExecutionOutput(TypedDict, total=False):
    QueryExecution: QueryExecution | None


class GetQueryResultsInput(ServiceRequest):
    QueryExecutionId: QueryExecutionId
    NextToken: Token | None
    MaxResults: MaxQueryResults | None
    QueryResultType: QueryResultType | None


class ResultSetMetadata(TypedDict, total=False):
    """The metadata that describes the column structure and data types of a
    table of query results. To return a ``ResultSetMetadata`` object, use
    GetQueryResults.
    """

    ColumnInfo: ColumnInfoList | None


datumList = list[Datum]


class Row(TypedDict, total=False):
    """The rows that make up a query result table."""

    Data: datumList | None


RowList = list[Row]


class ResultSet(TypedDict, total=False):
    """The metadata and rows that make up a query result set. The metadata
    describes the column structure and data types. To return a ``ResultSet``
    object, use GetQueryResults.
    """

    Rows: RowList | None
    ResultSetMetadata: ResultSetMetadata | None


class GetQueryResultsOutput(TypedDict, total=False):
    UpdateCount: Long | None
    ResultSet: ResultSet | None
    NextToken: Token | None


class GetQueryRuntimeStatisticsInput(ServiceRequest):
    QueryExecutionId: QueryExecutionId


class QueryStage(TypedDict, total=False):
    """Stage statistics such as input and output rows and bytes, execution time
    and stage state. This information also includes substages and the query
    stage plan.
    """

    StageId: "Long | None"
    State: "String | None"
    OutputBytes: "Long | None"
    OutputRows: "Long | None"
    InputBytes: "Long | None"
    InputRows: "Long | None"
    ExecutionTime: "Long | None"
    QueryStagePlan: "QueryStagePlanNode | None"
    SubStages: "QueryStages | None"


QueryStages = list[QueryStage]
StringList = list[String]


class QueryStagePlanNode(TypedDict, total=False):
    """Stage plan information such as name, identifier, sub plans, and remote
    sources.
    """

    Name: "String | None"
    Identifier: "String | None"
    Children: "QueryStagePlanNodes | None"
    RemoteSources: "StringList | None"


QueryStagePlanNodes = list[QueryStagePlanNode]


class QueryRuntimeStatisticsRows(TypedDict, total=False):
    """Statistics such as input rows and bytes read by the query, rows and
    bytes output by the query, and the number of rows written by the query.
    """

    InputRows: Long | None
    InputBytes: Long | None
    OutputBytes: Long | None
    OutputRows: Long | None


class QueryRuntimeStatisticsTimeline(TypedDict, total=False):
    """Timeline statistics such as query queue time, planning time, execution
    time, service processing time, and total execution time.
    """

    QueryQueueTimeInMillis: Long | None
    ServicePreProcessingTimeInMillis: Long | None
    QueryPlanningTimeInMillis: Long | None
    EngineExecutionTimeInMillis: Long | None
    ServiceProcessingTimeInMillis: Long | None
    TotalExecutionTimeInMillis: Long | None


class QueryRuntimeStatistics(TypedDict, total=False):
    """The query execution timeline, statistics on input and output rows and
    bytes, and the different query stages that form the query execution
    plan.
    """

    Timeline: QueryRuntimeStatisticsTimeline | None
    Rows: QueryRuntimeStatisticsRows | None
    OutputStage: QueryStage | None


class GetQueryRuntimeStatisticsOutput(TypedDict, total=False):
    QueryRuntimeStatistics: QueryRuntimeStatistics | None


class GetResourceDashboardRequest(ServiceRequest):
    ResourceARN: AmazonResourceName


class GetResourceDashboardResponse(TypedDict, total=False):
    Url: String


class GetSessionEndpointRequest(ServiceRequest):
    SessionId: SessionId


class GetSessionEndpointResponse(TypedDict, total=False):
    EndpointUrl: String
    AuthToken: String
    AuthTokenExpirationTime: Timestamp


class GetSessionRequest(ServiceRequest):
    SessionId: SessionId


class SessionStatistics(TypedDict, total=False):
    """Contains statistics for a session."""

    DpuExecutionInMillis: Long | None


class SessionStatus(TypedDict, total=False):
    """Contains information about the status of a session."""

    StartDateTime: Date | None
    LastModifiedDateTime: Date | None
    EndDateTime: Date | None
    IdleSinceDateTime: Date | None
    State: SessionState | None
    StateChangeReason: DescriptionString | None


class SessionConfiguration(TypedDict, total=False):
    """Contains session configuration information."""

    ExecutionRole: RoleArn | None
    WorkingDirectory: ResultOutputLocation | None
    IdleTimeoutSeconds: Long | None
    SessionIdleTimeoutInMinutes: SessionIdleTimeoutInMinutes | None
    EncryptionConfiguration: EncryptionConfiguration | None


class GetSessionResponse(TypedDict, total=False):
    SessionId: SessionId | None
    Description: DescriptionString | None
    WorkGroup: WorkGroupName | None
    EngineVersion: NameString | None
    EngineConfiguration: EngineConfiguration | None
    NotebookVersion: NameString | None
    MonitoringConfiguration: MonitoringConfiguration | None
    SessionConfiguration: SessionConfiguration | None
    Status: SessionStatus | None
    Statistics: SessionStatistics | None


class GetSessionStatusRequest(ServiceRequest):
    SessionId: SessionId


class GetSessionStatusResponse(TypedDict, total=False):
    SessionId: SessionId | None
    Status: SessionStatus | None


class GetTableMetadataInput(ServiceRequest):
    CatalogName: CatalogNameString
    DatabaseName: NameString
    TableName: NameString
    WorkGroup: WorkGroupName | None


class TableMetadata(TypedDict, total=False):
    """Contains metadata for a table."""

    Name: NameString
    CreateTime: Timestamp | None
    LastAccessTime: Timestamp | None
    TableType: TableTypeString | None
    Columns: ColumnList | None
    PartitionKeys: ColumnList | None
    Parameters: ParametersMap | None


class GetTableMetadataOutput(TypedDict, total=False):
    TableMetadata: TableMetadata | None


class GetWorkGroupInput(ServiceRequest):
    WorkGroup: WorkGroupName


class WorkGroup(TypedDict, total=False):
    """A workgroup, which contains a name, description, creation time, state,
    and other configuration, listed under WorkGroup$Configuration. Each
    workgroup enables you to isolate queries for you or your group of users
    from other queries in the same account, to configure the query results
    location and the encryption configuration (known as workgroup settings),
    to enable sending query metrics to Amazon CloudWatch, and to establish
    per-query data usage control limits for all queries in a workgroup. The
    workgroup settings override is specified in
    ``EnforceWorkGroupConfiguration`` (true/false) in the
    ``WorkGroupConfiguration``. See
    WorkGroupConfiguration$EnforceWorkGroupConfiguration.
    """

    Name: WorkGroupName
    State: WorkGroupState | None
    Configuration: WorkGroupConfiguration | None
    Description: WorkGroupDescriptionString | None
    CreationTime: Date | None
    IdentityCenterApplicationArn: IdentityCenterApplicationArn | None


class GetWorkGroupOutput(TypedDict, total=False):
    WorkGroup: WorkGroup | None


class ImportNotebookInput(ServiceRequest):
    WorkGroup: WorkGroupName
    Name: NotebookName
    Payload: Payload | None
    Type: NotebookType
    NotebookS3LocationUri: S3Uri | None
    ClientRequestToken: ClientRequestToken | None


class ImportNotebookOutput(TypedDict, total=False):
    NotebookId: NotebookId | None


class ListApplicationDPUSizesInput(ServiceRequest):
    MaxResults: MaxApplicationDPUSizesCount | None
    NextToken: Token | None


class ListApplicationDPUSizesOutput(TypedDict, total=False):
    ApplicationDPUSizes: ApplicationDPUSizesList | None
    NextToken: Token | None


class ListCalculationExecutionsRequest(ServiceRequest):
    SessionId: SessionId
    StateFilter: CalculationExecutionState | None
    MaxResults: MaxCalculationsCount | None
    NextToken: SessionManagerToken | None


class ListCalculationExecutionsResponse(TypedDict, total=False):
    NextToken: SessionManagerToken | None
    Calculations: CalculationsList | None


class ListCapacityReservationsInput(ServiceRequest):
    NextToken: Token | None
    MaxResults: MaxCapacityReservationsCount | None


class ListCapacityReservationsOutput(TypedDict, total=False):
    NextToken: Token | None
    CapacityReservations: CapacityReservationsList


class ListDataCatalogsInput(ServiceRequest):
    NextToken: Token | None
    MaxResults: MaxDataCatalogsCount | None
    WorkGroup: WorkGroupName | None


class ListDataCatalogsOutput(TypedDict, total=False):
    DataCatalogsSummary: DataCatalogSummaryList | None
    NextToken: Token | None


class ListDatabasesInput(ServiceRequest):
    CatalogName: CatalogNameString
    NextToken: Token | None
    MaxResults: MaxDatabasesCount | None
    WorkGroup: WorkGroupName | None


class ListDatabasesOutput(TypedDict, total=False):
    DatabaseList: DatabaseList | None
    NextToken: Token | None


class ListEngineVersionsInput(ServiceRequest):
    NextToken: Token | None
    MaxResults: MaxEngineVersionsCount | None


class ListEngineVersionsOutput(TypedDict, total=False):
    EngineVersions: EngineVersionsList | None
    NextToken: Token | None


class ListExecutorsRequest(ServiceRequest):
    SessionId: SessionId
    ExecutorStateFilter: ExecutorState | None
    MaxResults: MaxListExecutorsCount | None
    NextToken: SessionManagerToken | None


class ListExecutorsResponse(TypedDict, total=False):
    SessionId: SessionId
    NextToken: SessionManagerToken | None
    ExecutorsSummary: ExecutorsSummaryList | None


class ListNamedQueriesInput(ServiceRequest):
    NextToken: Token | None
    MaxResults: MaxNamedQueriesCount | None
    WorkGroup: WorkGroupName | None


class ListNamedQueriesOutput(TypedDict, total=False):
    NamedQueryIds: NamedQueryIdList | None
    NextToken: Token | None


class ListNotebookMetadataInput(ServiceRequest):
    Filters: FilterDefinition | None
    NextToken: Token | None
    MaxResults: MaxNotebooksCount | None
    WorkGroup: WorkGroupName


NotebookMetadataArray = list[NotebookMetadata]


class ListNotebookMetadataOutput(TypedDict, total=False):
    NextToken: Token | None
    NotebookMetadataList: NotebookMetadataArray | None


class ListNotebookSessionsRequest(ServiceRequest):
    NotebookId: NotebookId
    MaxResults: MaxSessionsCount | None
    NextToken: Token | None


class NotebookSessionSummary(TypedDict, total=False):
    """Contains the notebook session ID and notebook session creation time."""

    SessionId: SessionId | None
    CreationTime: Date | None


NotebookSessionsList = list[NotebookSessionSummary]


class ListNotebookSessionsResponse(TypedDict, total=False):
    NotebookSessionsList: NotebookSessionsList
    NextToken: Token | None


class ListPreparedStatementsInput(ServiceRequest):
    WorkGroup: WorkGroupName
    NextToken: Token | None
    MaxResults: MaxPreparedStatementsCount | None


class PreparedStatementSummary(TypedDict, total=False):
    """The name and last modified time of the prepared statement."""

    StatementName: StatementName | None
    LastModifiedTime: Date | None


PreparedStatementsList = list[PreparedStatementSummary]


class ListPreparedStatementsOutput(TypedDict, total=False):
    PreparedStatements: PreparedStatementsList | None
    NextToken: Token | None


class ListQueryExecutionsInput(ServiceRequest):
    NextToken: Token | None
    MaxResults: MaxQueryExecutionsCount | None
    WorkGroup: WorkGroupName | None


class ListQueryExecutionsOutput(TypedDict, total=False):
    QueryExecutionIds: QueryExecutionIdList | None
    NextToken: Token | None


class ListSessionsRequest(ServiceRequest):
    WorkGroup: WorkGroupName
    StateFilter: SessionState | None
    MaxResults: MaxSessionsCount | None
    NextToken: SessionManagerToken | None


class SessionSummary(TypedDict, total=False):
    """Contains summary information about a session."""

    SessionId: SessionId | None
    Description: DescriptionString | None
    EngineVersion: EngineVersion | None
    NotebookVersion: NameString | None
    Status: SessionStatus | None


SessionsList = list[SessionSummary]


class ListSessionsResponse(TypedDict, total=False):
    NextToken: SessionManagerToken | None
    Sessions: SessionsList | None


class ListTableMetadataInput(ServiceRequest):
    CatalogName: CatalogNameString
    DatabaseName: NameString
    Expression: ExpressionString | None
    NextToken: Token | None
    MaxResults: MaxTableMetadataCount | None
    WorkGroup: WorkGroupName | None


TableMetadataList = list[TableMetadata]


class ListTableMetadataOutput(TypedDict, total=False):
    TableMetadataList: TableMetadataList | None
    NextToken: Token | None


class ListTagsForResourceInput(ServiceRequest):
    ResourceARN: AmazonResourceName
    NextToken: Token | None
    MaxResults: MaxTagsCount | None


class ListTagsForResourceOutput(TypedDict, total=False):
    Tags: TagList | None
    NextToken: Token | None


class ListWorkGroupsInput(ServiceRequest):
    NextToken: Token | None
    MaxResults: MaxWorkGroupsCount | None


class WorkGroupSummary(TypedDict, total=False):
    """The summary information for the workgroup, which includes its name,
    state, description, and the date and time it was created.
    """

    Name: WorkGroupName | None
    State: WorkGroupState | None
    Description: WorkGroupDescriptionString | None
    CreationTime: Date | None
    EngineVersion: EngineVersion | None
    IdentityCenterApplicationArn: IdentityCenterApplicationArn | None


WorkGroupsList = list[WorkGroupSummary]


class ListWorkGroupsOutput(TypedDict, total=False):
    WorkGroups: WorkGroupsList | None
    NextToken: Token | None


class ManagedQueryResultsConfigurationUpdates(TypedDict, total=False):
    """Updates the configuration for managed query results."""

    Enabled: BoxedBoolean | None
    EncryptionConfiguration: ManagedQueryResultsEncryptionConfiguration | None
    RemoveEncryptionConfiguration: BoxedBoolean | None


class PutCapacityAssignmentConfigurationInput(ServiceRequest):
    CapacityReservationName: CapacityReservationName
    CapacityAssignments: CapacityAssignmentsList


class PutCapacityAssignmentConfigurationOutput(TypedDict, total=False):
    pass


class ResultConfigurationUpdates(TypedDict, total=False):
    """The information about the updates in the query results, such as output
    location and encryption configuration for the query results.
    """

    OutputLocation: ResultOutputLocation | None
    RemoveOutputLocation: BoxedBoolean | None
    EncryptionConfiguration: EncryptionConfiguration | None
    RemoveEncryptionConfiguration: BoxedBoolean | None
    ExpectedBucketOwner: AwsAccountId | None
    RemoveExpectedBucketOwner: BoxedBoolean | None
    AclConfiguration: AclConfiguration | None
    RemoveAclConfiguration: BoxedBoolean | None


class StartCalculationExecutionRequest(ServiceRequest):
    SessionId: SessionId
    Description: DescriptionString | None
    CalculationConfiguration: CalculationConfiguration | None
    CodeBlock: CodeBlock | None
    ClientRequestToken: IdempotencyToken | None


class StartCalculationExecutionResponse(TypedDict, total=False):
    CalculationExecutionId: CalculationExecutionId | None
    State: CalculationExecutionState | None


class StartQueryExecutionInput(ServiceRequest):
    QueryString: QueryString
    ClientRequestToken: IdempotencyToken | None
    QueryExecutionContext: QueryExecutionContext | None
    ResultConfiguration: ResultConfiguration | None
    WorkGroup: WorkGroupName | None
    ExecutionParameters: ExecutionParameters | None
    ResultReuseConfiguration: ResultReuseConfiguration | None
    EngineConfiguration: EngineConfiguration | None


class StartQueryExecutionOutput(TypedDict, total=False):
    QueryExecutionId: QueryExecutionId | None


class StartSessionRequest(ServiceRequest):
    Description: DescriptionString | None
    WorkGroup: WorkGroupName
    EngineConfiguration: EngineConfiguration
    ExecutionRole: RoleArn | None
    MonitoringConfiguration: MonitoringConfiguration | None
    NotebookVersion: NameString | None
    SessionIdleTimeoutInMinutes: SessionIdleTimeoutInMinutes | None
    ClientRequestToken: IdempotencyToken | None
    Tags: TagList | None
    CopyWorkGroupTags: BoxedBoolean | None


class StartSessionResponse(TypedDict, total=False):
    SessionId: SessionId | None
    State: SessionState | None


class StopCalculationExecutionRequest(ServiceRequest):
    CalculationExecutionId: CalculationExecutionId


class StopCalculationExecutionResponse(TypedDict, total=False):
    State: CalculationExecutionState | None


class StopQueryExecutionInput(ServiceRequest):
    QueryExecutionId: QueryExecutionId


class StopQueryExecutionOutput(TypedDict, total=False):
    pass


TagKeyList = list[TagKey]


class TagResourceInput(ServiceRequest):
    ResourceARN: AmazonResourceName
    Tags: TagList


class TagResourceOutput(TypedDict, total=False):
    pass


class TerminateSessionRequest(ServiceRequest):
    SessionId: SessionId


class TerminateSessionResponse(TypedDict, total=False):
    State: SessionState | None


class UntagResourceInput(ServiceRequest):
    ResourceARN: AmazonResourceName
    TagKeys: TagKeyList


class UntagResourceOutput(TypedDict, total=False):
    pass


class UpdateCapacityReservationInput(ServiceRequest):
    TargetDpus: TargetDpusInteger
    Name: CapacityReservationName


class UpdateCapacityReservationOutput(TypedDict, total=False):
    pass


class UpdateDataCatalogInput(ServiceRequest):
    Name: CatalogNameString
    Type: DataCatalogType
    Description: DescriptionString | None
    Parameters: ParametersMap | None


class UpdateDataCatalogOutput(TypedDict, total=False):
    pass


class UpdateNamedQueryInput(ServiceRequest):
    NamedQueryId: NamedQueryId
    Name: NameString
    Description: NamedQueryDescriptionString | None
    QueryString: QueryString


class UpdateNamedQueryOutput(TypedDict, total=False):
    pass


class UpdateNotebookInput(ServiceRequest):
    NotebookId: NotebookId
    Payload: Payload
    Type: NotebookType
    SessionId: SessionId | None
    ClientRequestToken: ClientRequestToken | None


class UpdateNotebookMetadataInput(ServiceRequest):
    NotebookId: NotebookId
    ClientRequestToken: ClientRequestToken | None
    Name: NotebookName


class UpdateNotebookMetadataOutput(TypedDict, total=False):
    pass


class UpdateNotebookOutput(TypedDict, total=False):
    pass


class UpdatePreparedStatementInput(ServiceRequest):
    StatementName: StatementName
    WorkGroup: WorkGroupName
    QueryStatement: QueryString
    Description: DescriptionString | None


class UpdatePreparedStatementOutput(TypedDict, total=False):
    pass


class WorkGroupConfigurationUpdates(TypedDict, total=False):
    """The configuration information that will be updated for this workgroup,
    which includes the location in Amazon S3 where query and calculation
    results are stored, the encryption option, if any, used for query
    results, whether the Amazon CloudWatch Metrics are enabled for the
    workgroup, whether the workgroup settings override the client-side
    settings, and the data usage limit for the amount of bytes scanned per
    query, if it is specified.
    """

    EnforceWorkGroupConfiguration: BoxedBoolean | None
    ResultConfigurationUpdates: ResultConfigurationUpdates | None
    ManagedQueryResultsConfigurationUpdates: ManagedQueryResultsConfigurationUpdates | None
    PublishCloudWatchMetricsEnabled: BoxedBoolean | None
    BytesScannedCutoffPerQuery: BytesScannedCutoffValue | None
    RemoveBytesScannedCutoffPerQuery: BoxedBoolean | None
    RequesterPaysEnabled: BoxedBoolean | None
    EngineVersion: EngineVersion | None
    RemoveCustomerContentEncryptionConfiguration: BoxedBoolean | None
    AdditionalConfiguration: NameString | None
    ExecutionRole: RoleArn | None
    CustomerContentEncryptionConfiguration: CustomerContentEncryptionConfiguration | None
    EnableMinimumEncryptionConfiguration: BoxedBoolean | None
    QueryResultsS3AccessGrantsConfiguration: QueryResultsS3AccessGrantsConfiguration | None
    MonitoringConfiguration: MonitoringConfiguration | None
    EngineConfiguration: EngineConfiguration | None


class UpdateWorkGroupInput(ServiceRequest):
    WorkGroup: WorkGroupName
    Description: WorkGroupDescriptionString | None
    ConfigurationUpdates: WorkGroupConfigurationUpdates | None
    State: WorkGroupState | None


class UpdateWorkGroupOutput(TypedDict, total=False):
    pass


class AthenaApi:
    service: str = "athena"
    version: str = "2017-05-18"

    @handler("BatchGetNamedQuery")
    def batch_get_named_query(
        self, context: RequestContext, named_query_ids: NamedQueryIdList, **kwargs
    ) -> BatchGetNamedQueryOutput:
        """Returns the details of a single named query or a list of up to 50
        queries, which you provide as an array of query ID strings. Requires you
        to have access to the workgroup in which the queries were saved. Use
        ListNamedQueriesInput to get the list of named query IDs in the
        specified workgroup. If information could not be retrieved for a
        submitted query ID, information about the query ID submitted is listed
        under UnprocessedNamedQueryId. Named queries differ from executed
        queries. Use BatchGetQueryExecutionInput to get details about each
        unique query execution, and ListQueryExecutionsInput to get a list of
        query execution IDs.

        :param named_query_ids: An array of query IDs.
        :returns: BatchGetNamedQueryOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("BatchGetPreparedStatement")
    def batch_get_prepared_statement(
        self,
        context: RequestContext,
        prepared_statement_names: PreparedStatementNameList,
        work_group: WorkGroupName,
        **kwargs,
    ) -> BatchGetPreparedStatementOutput:
        """Returns the details of a single prepared statement or a list of up to
        256 prepared statements for the array of prepared statement names that
        you provide. Requires you to have access to the workgroup to which the
        prepared statements belong. If a prepared statement cannot be retrieved
        for the name specified, the statement is listed in
        ``UnprocessedPreparedStatementNames``.

        :param prepared_statement_names: A list of prepared statement names to return.
        :param work_group: The name of the workgroup to which the prepared statements belong.
        :returns: BatchGetPreparedStatementOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("BatchGetQueryExecution")
    def batch_get_query_execution(
        self, context: RequestContext, query_execution_ids: QueryExecutionIdList, **kwargs
    ) -> BatchGetQueryExecutionOutput:
        """Returns the details of a single query execution or a list of up to 50
        query executions, which you provide as an array of query execution ID
        strings. Requires you to have access to the workgroup in which the
        queries ran. To get a list of query execution IDs, use
        ListQueryExecutionsInput$WorkGroup. Query executions differ from named
        (saved) queries. Use BatchGetNamedQueryInput to get details about named
        queries.

        :param query_execution_ids: An array of query execution IDs.
        :returns: BatchGetQueryExecutionOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("CancelCapacityReservation")
    def cancel_capacity_reservation(
        self, context: RequestContext, name: CapacityReservationName, **kwargs
    ) -> CancelCapacityReservationOutput:
        """Cancels the capacity reservation with the specified name. Cancelled
        reservations remain in your account and will be deleted 45 days after
        cancellation. During the 45 days, you cannot re-purpose or reuse a
        reservation that has been cancelled, but you can refer to its tags and
        view it for historical reference.

        :param name: The name of the capacity reservation to cancel.
        :returns: CancelCapacityReservationOutput
        :raises InvalidRequestException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("CreateCapacityReservation")
    def create_capacity_reservation(
        self,
        context: RequestContext,
        target_dpus: TargetDpusInteger,
        name: CapacityReservationName,
        tags: TagList | None = None,
        **kwargs,
    ) -> CreateCapacityReservationOutput:
        """Creates a capacity reservation with the specified name and number of
        requested data processing units.

        :param target_dpus: The number of requested data processing units.
        :param name: The name of the capacity reservation to create.
        :param tags: The tags for the capacity reservation.
        :returns: CreateCapacityReservationOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("CreateDataCatalog", expand=False)
    def create_data_catalog(
        self, context: RequestContext, request: CreateDataCatalogInput, **kwargs
    ) -> CreateDataCatalogOutput:
        """Creates (registers) a data catalog with the specified name and
        properties. Catalogs created are visible to all users of the same Amazon
        Web Services account.

        For a ``FEDERATED`` catalog, this API operation creates the following
        resources.

        -  CFN Stack Name with a maximum length of 128 characters and prefix
           ``athenafederatedcatalog-CATALOG_NAME_SANITIZED`` with length 23
           characters.

        -  Lambda Function Name with a maximum length of 64 characters and
           prefix ``athenafederatedcatalog_CATALOG_NAME_SANITIZED`` with length
           23 characters.

        -  Glue Connection Name with a maximum length of 255 characters and a
           prefix ``athenafederatedcatalog_CATALOG_NAME_SANITIZED`` with length
           23 characters.

        :param name: The name of the data catalog to create.
        :param type: The type of data catalog to create: ``LAMBDA`` for a federated catalog,
        ``GLUE`` for an Glue Data Catalog, and ``HIVE`` for an external Apache
        Hive metastore.
        :param description: A description of the data catalog to be created.
        :param parameters: Specifies the Lambda function or functions to use for creating the data
        catalog.
        :param tags: A list of comma separated tags to add to the data catalog that is
        created.
        :returns: CreateDataCatalogOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("CreateNamedQuery")
    def create_named_query(
        self,
        context: RequestContext,
        name: NameString,
        database: DatabaseString,
        query_string: QueryString,
        description: DescriptionString | None = None,
        client_request_token: IdempotencyToken | None = None,
        work_group: WorkGroupName | None = None,
        **kwargs,
    ) -> CreateNamedQueryOutput:
        """Creates a named query in the specified workgroup. Requires that you have
        access to the workgroup.

        :param name: The query name.
        :param database: The database to which the query belongs.
        :param query_string: The contents of the query with all query statements.
        :param description: The query description.
        :param client_request_token: A unique case-sensitive string used to ensure the request to create the
        query is idempotent (executes only once).
        :param work_group: The name of the workgroup in which the named query is being created.
        :returns: CreateNamedQueryOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("CreateNotebook")
    def create_notebook(
        self,
        context: RequestContext,
        work_group: WorkGroupName,
        name: NotebookName,
        client_request_token: ClientRequestToken | None = None,
        **kwargs,
    ) -> CreateNotebookOutput:
        """Creates an empty ``ipynb`` file in the specified Apache Spark enabled
        workgroup. Throws an error if a file in the workgroup with the same name
        already exists.

        :param work_group: The name of the Spark enabled workgroup in which the notebook will be
        created.
        :param name: The name of the ``ipynb`` file to be created in the Spark workgroup,
        without the ``.
        :param client_request_token: A unique case-sensitive string used to ensure the request to create the
        notebook is idempotent (executes only once).
        :returns: CreateNotebookOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("CreatePreparedStatement")
    def create_prepared_statement(
        self,
        context: RequestContext,
        statement_name: StatementName,
        work_group: WorkGroupName,
        query_statement: QueryString,
        description: DescriptionString | None = None,
        **kwargs,
    ) -> CreatePreparedStatementOutput:
        """Creates a prepared statement for use with SQL queries in Athena.

        :param statement_name: The name of the prepared statement.
        :param work_group: The name of the workgroup to which the prepared statement belongs.
        :param query_statement: The query string for the prepared statement.
        :param description: The description of the prepared statement.
        :returns: CreatePreparedStatementOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("CreatePresignedNotebookUrl")
    def create_presigned_notebook_url(
        self, context: RequestContext, session_id: SessionId, **kwargs
    ) -> CreatePresignedNotebookUrlResponse:
        """Gets an authentication token and the URL at which the notebook can be
        accessed. During programmatic access, ``CreatePresignedNotebookUrl``
        must be called every 10 minutes to refresh the authentication token. For
        information about granting programmatic access, see `Grant programmatic
        access <https://docs.aws.amazon.com/athena/latest/ug/setting-up.html#setting-up-grant-programmatic-access>`__.

        :param session_id: The session ID.
        :returns: CreatePresignedNotebookUrlResponse
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("CreateWorkGroup")
    def create_work_group(
        self,
        context: RequestContext,
        name: WorkGroupName,
        configuration: WorkGroupConfiguration | None = None,
        description: WorkGroupDescriptionString | None = None,
        tags: TagList | None = None,
        **kwargs,
    ) -> CreateWorkGroupOutput:
        """Creates a workgroup with the specified name. A workgroup can be an
        Apache Spark enabled workgroup or an Athena SQL workgroup.

        :param name: The workgroup name.
        :param configuration: Contains configuration information for creating an Athena SQL workgroup
        or Spark enabled Athena workgroup.
        :param description: The workgroup description.
        :param tags: A list of comma separated tags to add to the workgroup that is created.
        :returns: CreateWorkGroupOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("DeleteCapacityReservation")
    def delete_capacity_reservation(
        self, context: RequestContext, name: CapacityReservationName, **kwargs
    ) -> DeleteCapacityReservationOutput:
        """Deletes a cancelled capacity reservation. A reservation must be
        cancelled before it can be deleted. A deleted reservation is immediately
        removed from your account and can no longer be referenced, including by
        its ARN. A deleted reservation cannot be called by
        ``GetCapacityReservation``, and deleted reservations do not appear in
        the output of ``ListCapacityReservations``.

        :param name: The name of the capacity reservation to delete.
        :returns: DeleteCapacityReservationOutput
        :raises InvalidRequestException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("DeleteDataCatalog")
    def delete_data_catalog(
        self,
        context: RequestContext,
        name: CatalogNameString,
        delete_catalog_only: Boolean | None = None,
        **kwargs,
    ) -> DeleteDataCatalogOutput:
        """Deletes a data catalog.

        :param name: The name of the data catalog to delete.
        :param delete_catalog_only: Deletes the Athena Data Catalog.
        :returns: DeleteDataCatalogOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("DeleteNamedQuery")
    def delete_named_query(
        self, context: RequestContext, named_query_id: NamedQueryId, **kwargs
    ) -> DeleteNamedQueryOutput:
        """Deletes the named query if you have access to the workgroup in which the
        query was saved.

        :param named_query_id: The unique ID of the query to delete.
        :returns: DeleteNamedQueryOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("DeleteNotebook")
    def delete_notebook(
        self, context: RequestContext, notebook_id: NotebookId, **kwargs
    ) -> DeleteNotebookOutput:
        """Deletes the specified notebook.

        :param notebook_id: The ID of the notebook to delete.
        :returns: DeleteNotebookOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeletePreparedStatement")
    def delete_prepared_statement(
        self,
        context: RequestContext,
        statement_name: StatementName,
        work_group: WorkGroupName,
        **kwargs,
    ) -> DeletePreparedStatementOutput:
        """Deletes the prepared statement with the specified name from the
        specified workgroup.

        :param statement_name: The name of the prepared statement to delete.
        :param work_group: The workgroup to which the statement to be deleted belongs.
        :returns: DeletePreparedStatementOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("DeleteWorkGroup")
    def delete_work_group(
        self,
        context: RequestContext,
        work_group: WorkGroupName,
        recursive_delete_option: BoxedBoolean | None = None,
        **kwargs,
    ) -> DeleteWorkGroupOutput:
        """Deletes the workgroup with the specified name. The primary workgroup
        cannot be deleted.

        :param work_group: The unique name of the workgroup to delete.
        :param recursive_delete_option: The option to delete the workgroup and its contents even if the
        workgroup contains any named queries, query executions, or notebooks.
        :returns: DeleteWorkGroupOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("ExportNotebook")
    def export_notebook(
        self, context: RequestContext, notebook_id: NotebookId, **kwargs
    ) -> ExportNotebookOutput:
        """Exports the specified notebook and its metadata.

        :param notebook_id: The ID of the notebook to export.
        :returns: ExportNotebookOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetCalculationExecution")
    def get_calculation_execution(
        self, context: RequestContext, calculation_execution_id: CalculationExecutionId, **kwargs
    ) -> GetCalculationExecutionResponse:
        """Describes a previously submitted calculation execution.

        :param calculation_execution_id: The calculation execution UUID.
        :returns: GetCalculationExecutionResponse
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetCalculationExecutionCode")
    def get_calculation_execution_code(
        self, context: RequestContext, calculation_execution_id: CalculationExecutionId, **kwargs
    ) -> GetCalculationExecutionCodeResponse:
        """Retrieves the unencrypted code that was executed for the calculation.

        :param calculation_execution_id: The calculation execution UUID.
        :returns: GetCalculationExecutionCodeResponse
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetCalculationExecutionStatus")
    def get_calculation_execution_status(
        self, context: RequestContext, calculation_execution_id: CalculationExecutionId, **kwargs
    ) -> GetCalculationExecutionStatusResponse:
        """Gets the status of a current calculation.

        :param calculation_execution_id: The calculation execution UUID.
        :returns: GetCalculationExecutionStatusResponse
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetCapacityAssignmentConfiguration")
    def get_capacity_assignment_configuration(
        self, context: RequestContext, capacity_reservation_name: CapacityReservationName, **kwargs
    ) -> GetCapacityAssignmentConfigurationOutput:
        """Gets the capacity assignment configuration for a capacity reservation,
        if one exists.

        :param capacity_reservation_name: The name of the capacity reservation to retrieve the capacity assignment
        configuration for.
        :returns: GetCapacityAssignmentConfigurationOutput
        :raises InvalidRequestException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("GetCapacityReservation")
    def get_capacity_reservation(
        self, context: RequestContext, name: CapacityReservationName, **kwargs
    ) -> GetCapacityReservationOutput:
        """Returns information about the capacity reservation with the specified
        name.

        :param name: The name of the capacity reservation.
        :returns: GetCapacityReservationOutput
        :raises InvalidRequestException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("GetDataCatalog")
    def get_data_catalog(
        self,
        context: RequestContext,
        name: CatalogNameString,
        work_group: WorkGroupName | None = None,
        **kwargs,
    ) -> GetDataCatalogOutput:
        """Returns the specified data catalog.

        :param name: The name of the data catalog to return.
        :param work_group: The name of the workgroup.
        :returns: GetDataCatalogOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("GetDatabase")
    def get_database(
        self,
        context: RequestContext,
        catalog_name: CatalogNameString,
        database_name: NameString,
        work_group: WorkGroupName | None = None,
        **kwargs,
    ) -> GetDatabaseOutput:
        """Returns a database object for the specified database and data catalog.

        :param catalog_name: The name of the data catalog that contains the database to return.
        :param database_name: The name of the database to return.
        :param work_group: The name of the workgroup for which the metadata is being fetched.
        :returns: GetDatabaseOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises MetadataException:
        """
        raise NotImplementedError

    @handler("GetNamedQuery")
    def get_named_query(
        self, context: RequestContext, named_query_id: NamedQueryId, **kwargs
    ) -> GetNamedQueryOutput:
        """Returns information about a single query. Requires that you have access
        to the workgroup in which the query was saved.

        :param named_query_id: The unique ID of the query.
        :returns: GetNamedQueryOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("GetNotebookMetadata")
    def get_notebook_metadata(
        self, context: RequestContext, notebook_id: NotebookId, **kwargs
    ) -> GetNotebookMetadataOutput:
        """Retrieves notebook metadata for the specified notebook ID.

        :param notebook_id: The ID of the notebook whose metadata is to be retrieved.
        :returns: GetNotebookMetadataOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetPreparedStatement")
    def get_prepared_statement(
        self,
        context: RequestContext,
        statement_name: StatementName,
        work_group: WorkGroupName,
        **kwargs,
    ) -> GetPreparedStatementOutput:
        """Retrieves the prepared statement with the specified name from the
        specified workgroup.

        :param statement_name: The name of the prepared statement to retrieve.
        :param work_group: The workgroup to which the statement to be retrieved belongs.
        :returns: GetPreparedStatementOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetQueryExecution")
    def get_query_execution(
        self, context: RequestContext, query_execution_id: QueryExecutionId, **kwargs
    ) -> GetQueryExecutionOutput:
        """Returns information about a single execution of a query if you have
        access to the workgroup in which the query ran. Each time a query
        executes, information about the query execution is saved with a unique
        ID.

        :param query_execution_id: The unique ID of the query execution.
        :returns: GetQueryExecutionOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("GetQueryResults")
    def get_query_results(
        self,
        context: RequestContext,
        query_execution_id: QueryExecutionId,
        next_token: Token | None = None,
        max_results: MaxQueryResults | None = None,
        query_result_type: QueryResultType | None = None,
        **kwargs,
    ) -> GetQueryResultsOutput:
        """Streams the results of a single query execution specified by
        ``QueryExecutionId`` from the Athena query results location in Amazon
        S3. For more information, see `Working with query results, recent
        queries, and output
        files <https://docs.aws.amazon.com/athena/latest/ug/querying.html>`__ in
        the *Amazon Athena User Guide*. This request does not execute the query
        but returns results. Use StartQueryExecution to run a query.

        To stream query results successfully, the IAM principal with permission
        to call ``GetQueryResults`` also must have permissions to the Amazon S3
        ``GetObject`` action for the Athena query results location.

        IAM principals with permission to the Amazon S3 ``GetObject`` action for
        the query results location are able to retrieve query results from
        Amazon S3 even if permission to the ``GetQueryResults`` action is
        denied. To restrict user or role access, ensure that Amazon S3
        permissions to the Athena query location are denied.

        :param query_execution_id: The unique ID of the query execution.
        :param next_token: A token generated by the Athena service that specifies where to continue
        pagination if a previous request was truncated.
        :param max_results: The maximum number of results (rows) to return in this request.
        :param query_result_type: When you set this to ``DATA_ROWS`` or empty, ``GetQueryResults`` returns
        the query results in rows.
        :returns: GetQueryResultsOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetQueryRuntimeStatistics")
    def get_query_runtime_statistics(
        self, context: RequestContext, query_execution_id: QueryExecutionId, **kwargs
    ) -> GetQueryRuntimeStatisticsOutput:
        """Returns query execution runtime statistics related to a single execution
        of a query if you have access to the workgroup in which the query ran.
        Statistics from the ``Timeline`` section of the response object are
        available as soon as QueryExecutionStatus$State is in a SUCCEEDED or
        FAILED state. The remaining non-timeline statistics in the response
        (like stage-level input and output row count and data size) are updated
        asynchronously and may not be available immediately after a query
        completes or, in some cases, may not be returned. The non-timeline
        statistics are also not included when a query has row-level filters
        defined in Lake Formation.

        :param query_execution_id: The unique ID of the query execution.
        :returns: GetQueryRuntimeStatisticsOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("GetResourceDashboard")
    def get_resource_dashboard(
        self, context: RequestContext, resource_arn: AmazonResourceName, **kwargs
    ) -> GetResourceDashboardResponse:
        """Gets the Live UI/Persistence UI for a session.

        :param resource_arn: The The Amazon Resource Name (ARN) for a session.
        :returns: GetResourceDashboardResponse
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetSession")
    def get_session(
        self, context: RequestContext, session_id: SessionId, **kwargs
    ) -> GetSessionResponse:
        """Gets the full details of a previously created session, including the
        session status and configuration.

        :param session_id: The session ID.
        :returns: GetSessionResponse
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetSessionEndpoint")
    def get_session_endpoint(
        self, context: RequestContext, session_id: SessionId, **kwargs
    ) -> GetSessionEndpointResponse:
        """Gets a connection endpoint and authentication token for a given session
        Id.

        :param session_id: The session ID.
        :returns: GetSessionEndpointResponse
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetSessionStatus")
    def get_session_status(
        self, context: RequestContext, session_id: SessionId, **kwargs
    ) -> GetSessionStatusResponse:
        """Gets the current status of a session.

        :param session_id: The session ID.
        :returns: GetSessionStatusResponse
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetTableMetadata")
    def get_table_metadata(
        self,
        context: RequestContext,
        catalog_name: CatalogNameString,
        database_name: NameString,
        table_name: NameString,
        work_group: WorkGroupName | None = None,
        **kwargs,
    ) -> GetTableMetadataOutput:
        """Returns table metadata for the specified catalog, database, and table.

        :param catalog_name: The name of the data catalog that contains the database and table
        metadata to return.
        :param database_name: The name of the database that contains the table metadata to return.
        :param table_name: The name of the table for which metadata is returned.
        :param work_group: The name of the workgroup for which the metadata is being fetched.
        :returns: GetTableMetadataOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises MetadataException:
        """
        raise NotImplementedError

    @handler("GetWorkGroup")
    def get_work_group(
        self, context: RequestContext, work_group: WorkGroupName, **kwargs
    ) -> GetWorkGroupOutput:
        """Returns information about the workgroup with the specified name.

        :param work_group: The name of the workgroup.
        :returns: GetWorkGroupOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("ImportNotebook", expand=False)
    def import_notebook(
        self, context: RequestContext, request: ImportNotebookInput, **kwargs
    ) -> ImportNotebookOutput:
        """Imports a single ``ipynb`` file to a Spark enabled workgroup. To import
        the notebook, the request must specify a value for either ``Payload`` or
        ``NoteBookS3LocationUri``. If neither is specified or both are
        specified, an ``InvalidRequestException`` occurs. The maximum file size
        that can be imported is 10 megabytes. If an ``ipynb`` file with the same
        name already exists in the workgroup, throws an error.

        :param work_group: The name of the Spark enabled workgroup to import the notebook to.
        :param name: The name of the notebook to import.
        :param type: The notebook content type.
        :param payload: The notebook content to be imported.
        :param notebook_s3_location_uri: A URI that specifies the Amazon S3 location of a notebook file in
        ``ipynb`` format.
        :param client_request_token: A unique case-sensitive string used to ensure the request to import the
        notebook is idempotent (executes only once).
        :returns: ImportNotebookOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("ListApplicationDPUSizes")
    def list_application_dpu_sizes(
        self,
        context: RequestContext,
        max_results: MaxApplicationDPUSizesCount | None = None,
        next_token: Token | None = None,
        **kwargs,
    ) -> ListApplicationDPUSizesOutput:
        """Returns the supported DPU sizes for the supported application runtimes
        (for example, ``Athena notebook version 1``).

        :param max_results: Specifies the maximum number of results to return.
        :param next_token: A token generated by the Athena service that specifies where to continue
        pagination if a previous request was truncated.
        :returns: ListApplicationDPUSizesOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("ListCalculationExecutions")
    def list_calculation_executions(
        self,
        context: RequestContext,
        session_id: SessionId,
        state_filter: CalculationExecutionState | None = None,
        max_results: MaxCalculationsCount | None = None,
        next_token: SessionManagerToken | None = None,
        **kwargs,
    ) -> ListCalculationExecutionsResponse:
        """Lists the calculations that have been submitted to a session in
        descending order. Newer calculations are listed first; older
        calculations are listed later.

        :param session_id: The session ID.
        :param state_filter: A filter for a specific calculation execution state.
        :param max_results: The maximum number of calculation executions to return.
        :param next_token: A token generated by the Athena service that specifies where to continue
        pagination if a previous request was truncated.
        :returns: ListCalculationExecutionsResponse
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListCapacityReservations")
    def list_capacity_reservations(
        self,
        context: RequestContext,
        next_token: Token | None = None,
        max_results: MaxCapacityReservationsCount | None = None,
        **kwargs,
    ) -> ListCapacityReservationsOutput:
        """Lists the capacity reservations for the current account.

        :param next_token: A token generated by the Athena service that specifies where to continue
        pagination if a previous request was truncated.
        :param max_results: Specifies the maximum number of results to return.
        :returns: ListCapacityReservationsOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("ListDataCatalogs")
    def list_data_catalogs(
        self,
        context: RequestContext,
        next_token: Token | None = None,
        max_results: MaxDataCatalogsCount | None = None,
        work_group: WorkGroupName | None = None,
        **kwargs,
    ) -> ListDataCatalogsOutput:
        """Lists the data catalogs in the current Amazon Web Services account.

        In the Athena console, data catalogs are listed as "data sources" on the
        **Data sources** page under the **Data source name** column.

        :param next_token: A token generated by the Athena service that specifies where to continue
        pagination if a previous request was truncated.
        :param max_results: Specifies the maximum number of data catalogs to return.
        :param work_group: The name of the workgroup.
        :returns: ListDataCatalogsOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("ListDatabases")
    def list_databases(
        self,
        context: RequestContext,
        catalog_name: CatalogNameString,
        next_token: Token | None = None,
        max_results: MaxDatabasesCount | None = None,
        work_group: WorkGroupName | None = None,
        **kwargs,
    ) -> ListDatabasesOutput:
        """Lists the databases in the specified data catalog.

        :param catalog_name: The name of the data catalog that contains the databases to return.
        :param next_token: A token generated by the Athena service that specifies where to continue
        pagination if a previous request was truncated.
        :param max_results: Specifies the maximum number of results to return.
        :param work_group: The name of the workgroup for which the metadata is being fetched.
        :returns: ListDatabasesOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises MetadataException:
        """
        raise NotImplementedError

    @handler("ListEngineVersions")
    def list_engine_versions(
        self,
        context: RequestContext,
        next_token: Token | None = None,
        max_results: MaxEngineVersionsCount | None = None,
        **kwargs,
    ) -> ListEngineVersionsOutput:
        """Returns a list of engine versions that are available to choose from,
        including the Auto option.

        :param next_token: A token generated by the Athena service that specifies where to continue
        pagination if a previous request was truncated.
        :param max_results: The maximum number of engine versions to return in this request.
        :returns: ListEngineVersionsOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("ListExecutors")
    def list_executors(
        self,
        context: RequestContext,
        session_id: SessionId,
        executor_state_filter: ExecutorState | None = None,
        max_results: MaxListExecutorsCount | None = None,
        next_token: SessionManagerToken | None = None,
        **kwargs,
    ) -> ListExecutorsResponse:
        """Lists, in descending order, the executors that joined a session. Newer
        executors are listed first; older executors are listed later. The result
        can be optionally filtered by state.

        :param session_id: The session ID.
        :param executor_state_filter: A filter for a specific executor state.
        :param max_results: The maximum number of executors to return.
        :param next_token: A token generated by the Athena service that specifies where to continue
        pagination if a previous request was truncated.
        :returns: ListExecutorsResponse
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListNamedQueries")
    def list_named_queries(
        self,
        context: RequestContext,
        next_token: Token | None = None,
        max_results: MaxNamedQueriesCount | None = None,
        work_group: WorkGroupName | None = None,
        **kwargs,
    ) -> ListNamedQueriesOutput:
        """Provides a list of available query IDs only for queries saved in the
        specified workgroup. Requires that you have access to the specified
        workgroup. If a workgroup is not specified, lists the saved queries for
        the primary workgroup.

        :param next_token: A token generated by the Athena service that specifies where to continue
        pagination if a previous request was truncated.
        :param max_results: The maximum number of queries to return in this request.
        :param work_group: The name of the workgroup from which the named queries are being
        returned.
        :returns: ListNamedQueriesOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("ListNotebookMetadata")
    def list_notebook_metadata(
        self,
        context: RequestContext,
        work_group: WorkGroupName,
        filters: FilterDefinition | None = None,
        next_token: Token | None = None,
        max_results: MaxNotebooksCount | None = None,
        **kwargs,
    ) -> ListNotebookMetadataOutput:
        """Displays the notebook files for the specified workgroup in paginated
        format.

        :param work_group: The name of the Spark enabled workgroup to retrieve notebook metadata
        for.
        :param filters: Search filter string.
        :param next_token: A token generated by the Athena service that specifies where to continue
        pagination if a previous request was truncated.
        :param max_results: Specifies the maximum number of results to return.
        :returns: ListNotebookMetadataOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("ListNotebookSessions")
    def list_notebook_sessions(
        self,
        context: RequestContext,
        notebook_id: NotebookId,
        max_results: MaxSessionsCount | None = None,
        next_token: Token | None = None,
        **kwargs,
    ) -> ListNotebookSessionsResponse:
        """Lists, in descending order, the sessions that have been created in a
        notebook that are in an active state like ``CREATING``, ``CREATED``,
        ``IDLE`` or ``BUSY``. Newer sessions are listed first; older sessions
        are listed later.

        :param notebook_id: The ID of the notebook to list sessions for.
        :param max_results: The maximum number of notebook sessions to return.
        :param next_token: A token generated by the Athena service that specifies where to continue
        pagination if a previous request was truncated.
        :returns: ListNotebookSessionsResponse
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListPreparedStatements")
    def list_prepared_statements(
        self,
        context: RequestContext,
        work_group: WorkGroupName,
        next_token: Token | None = None,
        max_results: MaxPreparedStatementsCount | None = None,
        **kwargs,
    ) -> ListPreparedStatementsOutput:
        """Lists the prepared statements in the specified workgroup.

        :param work_group: The workgroup to list the prepared statements for.
        :param next_token: A token generated by the Athena service that specifies where to continue
        pagination if a previous request was truncated.
        :param max_results: The maximum number of results to return in this request.
        :returns: ListPreparedStatementsOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("ListQueryExecutions")
    def list_query_executions(
        self,
        context: RequestContext,
        next_token: Token | None = None,
        max_results: MaxQueryExecutionsCount | None = None,
        work_group: WorkGroupName | None = None,
        **kwargs,
    ) -> ListQueryExecutionsOutput:
        """Provides a list of available query execution IDs for the queries in the
        specified workgroup. Athena keeps a query history for 45 days. If a
        workgroup is not specified, returns a list of query execution IDs for
        the primary workgroup. Requires you to have access to the workgroup in
        which the queries ran.

        :param next_token: A token generated by the Athena service that specifies where to continue
        pagination if a previous request was truncated.
        :param max_results: The maximum number of query executions to return in this request.
        :param work_group: The name of the workgroup from which queries are being returned.
        :returns: ListQueryExecutionsOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("ListSessions")
    def list_sessions(
        self,
        context: RequestContext,
        work_group: WorkGroupName,
        state_filter: SessionState | None = None,
        max_results: MaxSessionsCount | None = None,
        next_token: SessionManagerToken | None = None,
        **kwargs,
    ) -> ListSessionsResponse:
        """Lists the sessions in a workgroup that are in an active state like
        ``CREATING``, ``CREATED``, ``IDLE``, or ``BUSY``. Newer sessions are
        listed first; older sessions are listed later.

        :param work_group: The workgroup to which the session belongs.
        :param state_filter: A filter for a specific session state.
        :param max_results: The maximum number of sessions to return.
        :param next_token: A token generated by the Athena service that specifies where to continue
        pagination if a previous request was truncated.
        :returns: ListSessionsResponse
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListTableMetadata")
    def list_table_metadata(
        self,
        context: RequestContext,
        catalog_name: CatalogNameString,
        database_name: NameString,
        expression: ExpressionString | None = None,
        next_token: Token | None = None,
        max_results: MaxTableMetadataCount | None = None,
        work_group: WorkGroupName | None = None,
        **kwargs,
    ) -> ListTableMetadataOutput:
        """Lists the metadata for the tables in the specified data catalog
        database.

        :param catalog_name: The name of the data catalog for which table metadata should be
        returned.
        :param database_name: The name of the database for which table metadata should be returned.
        :param expression: A regex filter that pattern-matches table names.
        :param next_token: A token generated by the Athena service that specifies where to continue
        pagination if a previous request was truncated.
        :param max_results: Specifies the maximum number of results to return.
        :param work_group: The name of the workgroup for which the metadata is being fetched.
        :returns: ListTableMetadataOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises MetadataException:
        """
        raise NotImplementedError

    @handler("ListTagsForResource")
    def list_tags_for_resource(
        self,
        context: RequestContext,
        resource_arn: AmazonResourceName,
        next_token: Token | None = None,
        max_results: MaxTagsCount | None = None,
        **kwargs,
    ) -> ListTagsForResourceOutput:
        """Lists the tags associated with an Athena resource.

        :param resource_arn: Lists the tags for the resource with the specified ARN.
        :param next_token: The token for the next set of results, or null if there are no
        additional results for this request, where the request lists the tags
        for the resource with the specified ARN.
        :param max_results: The maximum number of results to be returned per request that lists the
        tags for the resource.
        :returns: ListTagsForResourceOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListWorkGroups")
    def list_work_groups(
        self,
        context: RequestContext,
        next_token: Token | None = None,
        max_results: MaxWorkGroupsCount | None = None,
        **kwargs,
    ) -> ListWorkGroupsOutput:
        """Lists available workgroups for the account.

        :param next_token: A token generated by the Athena service that specifies where to continue
        pagination if a previous request was truncated.
        :param max_results: The maximum number of workgroups to return in this request.
        :returns: ListWorkGroupsOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("PutCapacityAssignmentConfiguration")
    def put_capacity_assignment_configuration(
        self,
        context: RequestContext,
        capacity_reservation_name: CapacityReservationName,
        capacity_assignments: CapacityAssignmentsList,
        **kwargs,
    ) -> PutCapacityAssignmentConfigurationOutput:
        """Puts a new capacity assignment configuration for a specified capacity
        reservation. If a capacity assignment configuration already exists for
        the capacity reservation, replaces the existing capacity assignment
        configuration.

        :param capacity_reservation_name: The name of the capacity reservation to put a capacity assignment
        configuration for.
        :param capacity_assignments: The list of assignments for the capacity assignment configuration.
        :returns: PutCapacityAssignmentConfigurationOutput
        :raises InvalidRequestException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("StartCalculationExecution")
    def start_calculation_execution(
        self,
        context: RequestContext,
        session_id: SessionId,
        description: DescriptionString | None = None,
        calculation_configuration: CalculationConfiguration | None = None,
        code_block: CodeBlock | None = None,
        client_request_token: IdempotencyToken | None = None,
        **kwargs,
    ) -> StartCalculationExecutionResponse:
        """Submits calculations for execution within a session. You can supply the
        code to run as an inline code block within the request.

        The request syntax requires the
        StartCalculationExecutionRequest$CodeBlock parameter or the
        CalculationConfiguration$CodeBlock parameter, but not both. Because
        CalculationConfiguration$CodeBlock is deprecated, use the
        StartCalculationExecutionRequest$CodeBlock parameter instead.

        :param session_id: The session ID.
        :param description: A description of the calculation.
        :param calculation_configuration: Contains configuration information for the calculation.
        :param code_block: A string that contains the code of the calculation.
        :param client_request_token: A unique case-sensitive string used to ensure the request to create the
        calculation is idempotent (executes only once).
        :returns: StartCalculationExecutionResponse
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("StartQueryExecution")
    def start_query_execution(
        self,
        context: RequestContext,
        query_string: QueryString,
        client_request_token: IdempotencyToken | None = None,
        query_execution_context: QueryExecutionContext | None = None,
        result_configuration: ResultConfiguration | None = None,
        work_group: WorkGroupName | None = None,
        execution_parameters: ExecutionParameters | None = None,
        result_reuse_configuration: ResultReuseConfiguration | None = None,
        engine_configuration: EngineConfiguration | None = None,
        **kwargs,
    ) -> StartQueryExecutionOutput:
        """Runs the SQL query statements contained in the ``Query``. Requires you
        to have access to the workgroup in which the query ran. Running queries
        against an external catalog requires GetDataCatalog permission to the
        catalog. For code samples using the Amazon Web Services SDK for Java,
        see `Examples and Code
        Samples <http://docs.aws.amazon.com/athena/latest/ug/code-samples.html>`__
        in the *Amazon Athena User Guide*.

        :param query_string: The SQL query statements to be executed.
        :param client_request_token: A unique case-sensitive string used to ensure the request to create the
        query is idempotent (executes only once).
        :param query_execution_context: The database within which the query executes.
        :param result_configuration: Specifies information about where and how to save the results of the
        query execution.
        :param work_group: The name of the workgroup in which the query is being started.
        :param execution_parameters: A list of values for the parameters in a query.
        :param result_reuse_configuration: Specifies the query result reuse behavior for the query.
        :param engine_configuration: Contains data processing unit (DPU) configuration settings and parameter
        mappings for a notebook engine.
        :returns: StartQueryExecutionOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("StartSession")
    def start_session(
        self,
        context: RequestContext,
        work_group: WorkGroupName,
        engine_configuration: EngineConfiguration,
        description: DescriptionString | None = None,
        execution_role: RoleArn | None = None,
        monitoring_configuration: MonitoringConfiguration | None = None,
        notebook_version: NameString | None = None,
        session_idle_timeout_in_minutes: SessionIdleTimeoutInMinutes | None = None,
        client_request_token: IdempotencyToken | None = None,
        tags: TagList | None = None,
        copy_work_group_tags: BoxedBoolean | None = None,
        **kwargs,
    ) -> StartSessionResponse:
        """Creates a session for running calculations within a workgroup. The
        session is ready when it reaches an ``IDLE`` state.

        :param work_group: The workgroup to which the session belongs.
        :param engine_configuration: Contains engine data processing unit (DPU) configuration settings and
        parameter mappings.
        :param description: The session description.
        :param execution_role: The ARN of the execution role used to access user resources for Spark
        sessions and Identity Center enabled workgroups.
        :param monitoring_configuration: Contains the configuration settings for managed log persistence,
        delivering logs to Amazon S3 buckets, Amazon CloudWatch log groups etc.
        :param notebook_version: The notebook version.
        :param session_idle_timeout_in_minutes: The idle timeout in minutes for the session.
        :param client_request_token: A unique case-sensitive string used to ensure the request to create the
        session is idempotent (executes only once).
        :param tags: A list of comma separated tags to add to the session that is created.
        :param copy_work_group_tags: Copies the tags from the Workgroup to the Session when.
        :returns: StartSessionResponse
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises SessionAlreadyExistsException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("StopCalculationExecution")
    def stop_calculation_execution(
        self, context: RequestContext, calculation_execution_id: CalculationExecutionId, **kwargs
    ) -> StopCalculationExecutionResponse:
        """Requests the cancellation of a calculation. A
        ``StopCalculationExecution`` call on a calculation that is already in a
        terminal state (for example, ``STOPPED``, ``FAILED``, or ``COMPLETED``)
        succeeds but has no effect.

        Cancelling a calculation is done on a best effort basis. If a
        calculation cannot be cancelled, you can be charged for its completion.
        If you are concerned about being charged for a calculation that cannot
        be cancelled, consider terminating the session in which the calculation
        is running.

        :param calculation_execution_id: The calculation execution UUID.
        :returns: StopCalculationExecutionResponse
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("StopQueryExecution")
    def stop_query_execution(
        self, context: RequestContext, query_execution_id: QueryExecutionId, **kwargs
    ) -> StopQueryExecutionOutput:
        """Stops a query execution. Requires you to have access to the workgroup in
        which the query ran.

        :param query_execution_id: The unique ID of the query execution to stop.
        :returns: StopQueryExecutionOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("TagResource")
    def tag_resource(
        self, context: RequestContext, resource_arn: AmazonResourceName, tags: TagList, **kwargs
    ) -> TagResourceOutput:
        """Adds one or more tags to an Athena resource. A tag is a label that you
        assign to a resource. Each tag consists of a key and an optional value,
        both of which you define. For example, you can use tags to categorize
        Athena workgroups, data catalogs, or capacity reservations by purpose,
        owner, or environment. Use a consistent set of tag keys to make it
        easier to search and filter the resources in your account. For best
        practices, see `Tagging Best
        Practices <https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/tagging-best-practices.html>`__.
        Tag keys can be from 1 to 128 UTF-8 Unicode characters, and tag values
        can be from 0 to 256 UTF-8 Unicode characters. Tags can use letters and
        numbers representable in UTF-8, and the following characters: + - = . _
        : / @. Tag keys and values are case-sensitive. Tag keys must be unique
        per resource. If you specify more than one tag, separate them by commas.

        :param resource_arn: Specifies the ARN of the Athena resource to which tags are to be added.
        :param tags: A collection of one or more tags, separated by commas, to be added to an
        Athena resource.
        :returns: TagResourceOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("TerminateSession")
    def terminate_session(
        self, context: RequestContext, session_id: SessionId, **kwargs
    ) -> TerminateSessionResponse:
        """Terminates an active session. A ``TerminateSession`` call on a session
        that is already inactive (for example, in a ``FAILED``, ``TERMINATED``
        or ``TERMINATING`` state) succeeds but has no effect. Calculations
        running in the session when ``TerminateSession`` is called are
        forcefully stopped, but may display as ``FAILED`` instead of
        ``STOPPED``.

        :param session_id: The session ID.
        :returns: TerminateSessionResponse
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("UntagResource")
    def untag_resource(
        self,
        context: RequestContext,
        resource_arn: AmazonResourceName,
        tag_keys: TagKeyList,
        **kwargs,
    ) -> UntagResourceOutput:
        """Removes one or more tags from an Athena resource.

        :param resource_arn: Specifies the ARN of the resource from which tags are to be removed.
        :param tag_keys: A comma-separated list of one or more tag keys whose tags are to be
        removed from the specified resource.
        :returns: UntagResourceOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("UpdateCapacityReservation")
    def update_capacity_reservation(
        self,
        context: RequestContext,
        target_dpus: TargetDpusInteger,
        name: CapacityReservationName,
        **kwargs,
    ) -> UpdateCapacityReservationOutput:
        """Updates the number of requested data processing units for the capacity
        reservation with the specified name.

        :param target_dpus: The new number of requested data processing units.
        :param name: The name of the capacity reservation.
        :returns: UpdateCapacityReservationOutput
        :raises InvalidRequestException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("UpdateDataCatalog", expand=False)
    def update_data_catalog(
        self, context: RequestContext, request: UpdateDataCatalogInput, **kwargs
    ) -> UpdateDataCatalogOutput:
        """Updates the data catalog that has the specified name.

        :param name: The name of the data catalog to update.
        :param type: Specifies the type of data catalog to update.
        :param description: New or modified text that describes the data catalog.
        :param parameters: Specifies the Lambda function or functions to use for updating the data
        catalog.
        :returns: UpdateDataCatalogOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("UpdateNamedQuery")
    def update_named_query(
        self,
        context: RequestContext,
        named_query_id: NamedQueryId,
        name: NameString,
        query_string: QueryString,
        description: NamedQueryDescriptionString | None = None,
        **kwargs,
    ) -> UpdateNamedQueryOutput:
        """Updates a NamedQuery object. The database or workgroup cannot be
        updated.

        :param named_query_id: The unique identifier (UUID) of the query.
        :param name: The name of the query.
        :param query_string: The contents of the query with all query statements.
        :param description: The query description.
        :returns: UpdateNamedQueryOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("UpdateNotebook", expand=False)
    def update_notebook(
        self, context: RequestContext, request: UpdateNotebookInput, **kwargs
    ) -> UpdateNotebookOutput:
        """Updates the contents of a Spark notebook.

        :param notebook_id: The ID of the notebook to update.
        :param payload: The updated content for the notebook.
        :param type: The notebook content type.
        :param session_id: The active notebook session ID.
        :param client_request_token: A unique case-sensitive string used to ensure the request to create the
        notebook is idempotent (executes only once).
        :returns: UpdateNotebookOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateNotebookMetadata")
    def update_notebook_metadata(
        self,
        context: RequestContext,
        notebook_id: NotebookId,
        name: NotebookName,
        client_request_token: ClientRequestToken | None = None,
        **kwargs,
    ) -> UpdateNotebookMetadataOutput:
        """Updates the metadata for a notebook.

        :param notebook_id: The ID of the notebook to update the metadata for.
        :param name: The name to update the notebook to.
        :param client_request_token: A unique case-sensitive string used to ensure the request to create the
        notebook is idempotent (executes only once).
        :returns: UpdateNotebookMetadataOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdatePreparedStatement")
    def update_prepared_statement(
        self,
        context: RequestContext,
        statement_name: StatementName,
        work_group: WorkGroupName,
        query_statement: QueryString,
        description: DescriptionString | None = None,
        **kwargs,
    ) -> UpdatePreparedStatementOutput:
        """Updates a prepared statement.

        :param statement_name: The name of the prepared statement.
        :param work_group: The workgroup for the prepared statement.
        :param query_statement: The query string for the prepared statement.
        :param description: The description of the prepared statement.
        :returns: UpdatePreparedStatementOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("UpdateWorkGroup")
    def update_work_group(
        self,
        context: RequestContext,
        work_group: WorkGroupName,
        description: WorkGroupDescriptionString | None = None,
        configuration_updates: WorkGroupConfigurationUpdates | None = None,
        state: WorkGroupState | None = None,
        **kwargs,
    ) -> UpdateWorkGroupOutput:
        """Updates the workgroup with the specified name. The workgroup's name
        cannot be changed. Only ``ConfigurationUpdates`` can be specified.

        :param work_group: The specified workgroup that will be updated.
        :param description: The workgroup description.
        :param configuration_updates: Contains configuration updates for an Athena SQL workgroup.
        :param state: The workgroup state that will be updated for the given workgroup.
        :returns: UpdateWorkGroupOutput
        :raises InternalServerException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError
