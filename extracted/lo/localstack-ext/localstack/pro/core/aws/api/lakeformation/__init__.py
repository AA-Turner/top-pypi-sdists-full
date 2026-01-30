from collections.abc import Iterable
from datetime import datetime
from enum import StrEnum
from typing import IO, TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

AccessKeyIdString = str
AccountIdString = str
ApplicationArn = str
AuditContextString = str
Boolean = bool
BooleanNullable = bool
CatalogIdString = str
ContextKey = str
ContextValue = str
CredentialTimeoutDurationSecondInteger = int
DataLakePrincipalString = str
DescriptionString = str
ETagString = str
ErrorMessageString = str
ExpressionString = str
GetQueryStateRequestQueryIdString = str
GetQueryStatisticsRequestQueryIdString = str
GetWorkUnitResultsRequestQueryIdString = str
GetWorkUnitsRequestQueryIdString = str
HashString = str
IAMRoleArn = str
IAMSAMLProviderArn = str
Identifier = str
IdentityCenterInstanceArn = str
IdentityString = str
Integer = int
KeyString = str
LFTagKey = str
LFTagValue = str
MessageString = str
NameString = str
NullableBoolean = bool
NullableString = str
PageSize = int
ParametersMapValue = str
PartitionValueString = str
PathString = str
PredicateString = str
QueryIdString = str
QueryPlanningContextDatabaseNameString = str
RAMResourceShareArn = str
ResourceArnString = str
Result = str
SAMLAssertionString = str
ScopeTarget = str
SearchPageSize = int
SecretAccessKeyString = str
SessionTokenString = str
StorageOptimizerConfigKey = str
StorageOptimizerConfigValue = str
String = str
StringValue = str
SyntheticGetWorkUnitResultsRequestWorkUnitTokenString = str
SyntheticStartQueryPlanningRequestQueryString = str
Token = str
TokenString = str
TransactionIdString = str
TrueFalseString = str
URI = str
ValueString = str
VersionString = str
WorkUnitTokenString = str


class ApplicationStatus(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class ComparisonOperator(StrEnum):
    EQ = "EQ"
    NE = "NE"
    LE = "LE"
    LT = "LT"
    GE = "GE"
    GT = "GT"
    CONTAINS = "CONTAINS"
    NOT_CONTAINS = "NOT_CONTAINS"
    BEGINS_WITH = "BEGINS_WITH"
    IN = "IN"
    BETWEEN = "BETWEEN"


class CredentialsScope(StrEnum):
    READ = "READ"
    READWRITE = "READWRITE"


class DataLakeResourceType(StrEnum):
    CATALOG = "CATALOG"
    DATABASE = "DATABASE"
    TABLE = "TABLE"
    DATA_LOCATION = "DATA_LOCATION"
    LF_TAG = "LF_TAG"
    LF_TAG_POLICY = "LF_TAG_POLICY"
    LF_TAG_POLICY_DATABASE = "LF_TAG_POLICY_DATABASE"
    LF_TAG_POLICY_TABLE = "LF_TAG_POLICY_TABLE"
    LF_NAMED_TAG_EXPRESSION = "LF_NAMED_TAG_EXPRESSION"


class EnableStatus(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class FieldNameString(StrEnum):
    RESOURCE_ARN = "RESOURCE_ARN"
    ROLE_ARN = "ROLE_ARN"
    LAST_MODIFIED = "LAST_MODIFIED"


class OptimizerType(StrEnum):
    COMPACTION = "COMPACTION"
    GARBAGE_COLLECTION = "GARBAGE_COLLECTION"
    ALL = "ALL"


class Permission(StrEnum):
    ALL = "ALL"
    SELECT = "SELECT"
    ALTER = "ALTER"
    DROP = "DROP"
    DELETE = "DELETE"
    INSERT = "INSERT"
    DESCRIBE = "DESCRIBE"
    CREATE_DATABASE = "CREATE_DATABASE"
    CREATE_TABLE = "CREATE_TABLE"
    DATA_LOCATION_ACCESS = "DATA_LOCATION_ACCESS"
    CREATE_LF_TAG = "CREATE_LF_TAG"
    ASSOCIATE = "ASSOCIATE"
    GRANT_WITH_LF_TAG_EXPRESSION = "GRANT_WITH_LF_TAG_EXPRESSION"
    CREATE_LF_TAG_EXPRESSION = "CREATE_LF_TAG_EXPRESSION"
    CREATE_CATALOG = "CREATE_CATALOG"
    SUPER_USER = "SUPER_USER"


class PermissionType(StrEnum):
    COLUMN_PERMISSION = "COLUMN_PERMISSION"
    CELL_FILTER_PERMISSION = "CELL_FILTER_PERMISSION"
    NESTED_PERMISSION = "NESTED_PERMISSION"
    NESTED_CELL_PERMISSION = "NESTED_CELL_PERMISSION"


class QueryStateString(StrEnum):
    PENDING = "PENDING"
    WORKUNITS_AVAILABLE = "WORKUNITS_AVAILABLE"
    ERROR = "ERROR"
    FINISHED = "FINISHED"
    EXPIRED = "EXPIRED"


class ResourceShareType(StrEnum):
    FOREIGN = "FOREIGN"
    ALL = "ALL"


class ResourceType(StrEnum):
    DATABASE = "DATABASE"
    TABLE = "TABLE"


class ServiceAuthorization(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class TransactionStatus(StrEnum):
    ACTIVE = "ACTIVE"
    COMMITTED = "COMMITTED"
    ABORTED = "ABORTED"
    COMMIT_IN_PROGRESS = "COMMIT_IN_PROGRESS"


class TransactionStatusFilter(StrEnum):
    ALL = "ALL"
    COMPLETED = "COMPLETED"
    ACTIVE = "ACTIVE"
    COMMITTED = "COMMITTED"
    ABORTED = "ABORTED"


class TransactionType(StrEnum):
    READ_AND_WRITE = "READ_AND_WRITE"
    READ_ONLY = "READ_ONLY"


class VerificationStatus(StrEnum):
    VERIFIED = "VERIFIED"
    VERIFICATION_FAILED = "VERIFICATION_FAILED"
    NOT_VERIFIED = "NOT_VERIFIED"


class AccessDeniedException(ServiceException):
    """Access to a resource was denied."""

    code: str = "AccessDeniedException"
    sender_fault: bool = True
    status_code: int = 403


class AlreadyExistsException(ServiceException):
    """A resource to be created or added already exists."""

    code: str = "AlreadyExistsException"
    sender_fault: bool = False
    status_code: int = 400


class ConcurrentModificationException(ServiceException):
    """Two processes are trying to modify a resource simultaneously."""

    code: str = "ConcurrentModificationException"
    sender_fault: bool = False
    status_code: int = 400


class ConflictException(ServiceException):
    """Multiple resources exist with the same Amazon S3 location"""

    code: str = "ConflictException"
    sender_fault: bool = False
    status_code: int = 400


class EntityNotFoundException(ServiceException):
    """A specified entity does not exist."""

    code: str = "EntityNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class ExpiredException(ServiceException):
    """Contains details about an error where the query request expired."""

    code: str = "ExpiredException"
    sender_fault: bool = True
    status_code: int = 410


class GlueEncryptionException(ServiceException):
    """An encryption operation failed."""

    code: str = "GlueEncryptionException"
    sender_fault: bool = False
    status_code: int = 400


class InternalServiceException(ServiceException):
    """An internal service error occurred."""

    code: str = "InternalServiceException"
    sender_fault: bool = False
    status_code: int = 500


class InvalidInputException(ServiceException):
    """The input provided was not valid."""

    code: str = "InvalidInputException"
    sender_fault: bool = True
    status_code: int = 400


class OperationTimeoutException(ServiceException):
    """The operation timed out."""

    code: str = "OperationTimeoutException"
    sender_fault: bool = False
    status_code: int = 400


class PermissionTypeMismatchException(ServiceException):
    """The engine does not support filtering data based on the enforced
    permissions. For example, if you call the
    ``GetTemporaryGlueTableCredentials`` operation with
    ``SupportedPermissionType`` equal to ``ColumnPermission``, but
    cell-level permissions exist on the table, this exception is thrown.
    """

    code: str = "PermissionTypeMismatchException"
    sender_fault: bool = False
    status_code: int = 400


class ResourceNotReadyException(ServiceException):
    """Contains details about an error related to a resource which is not ready
    for a transaction.
    """

    code: str = "ResourceNotReadyException"
    sender_fault: bool = False
    status_code: int = 400


class ResourceNumberLimitExceededException(ServiceException):
    """A resource numerical limit was exceeded."""

    code: str = "ResourceNumberLimitExceededException"
    sender_fault: bool = False
    status_code: int = 400


class StatisticsNotReadyYetException(ServiceException):
    """Contains details about an error related to statistics not being ready."""

    code: str = "StatisticsNotReadyYetException"
    sender_fault: bool = True
    status_code: int = 420


class ThrottledException(ServiceException):
    """Contains details about an error where the query request was throttled."""

    code: str = "ThrottledException"
    sender_fault: bool = True
    status_code: int = 429


class TransactionCanceledException(ServiceException):
    """Contains details about an error related to a transaction that was
    cancelled.
    """

    code: str = "TransactionCanceledException"
    sender_fault: bool = False
    status_code: int = 400


class TransactionCommitInProgressException(ServiceException):
    """Contains details about an error related to a transaction commit that was
    in progress.
    """

    code: str = "TransactionCommitInProgressException"
    sender_fault: bool = False
    status_code: int = 400


class TransactionCommittedException(ServiceException):
    """Contains details about an error where the specified transaction has
    already been committed and cannot be used for ``UpdateTableObjects``.
    """

    code: str = "TransactionCommittedException"
    sender_fault: bool = False
    status_code: int = 400


class WorkUnitsNotReadyYetException(ServiceException):
    """Contains details about an error related to work units not being ready."""

    code: str = "WorkUnitsNotReadyYetException"
    sender_fault: bool = True
    status_code: int = 420


TagValueList = list[LFTagValue]


class LFTagPair(TypedDict, total=False):
    """A structure containing an LF-tag key-value pair."""

    CatalogId: CatalogIdString | None
    TagKey: LFTagKey
    TagValues: TagValueList


LFTagsList = list[LFTagPair]


class LFTagExpressionResource(TypedDict, total=False):
    """A structure containing a LF-Tag expression (keys and values)."""

    CatalogId: CatalogIdString | None
    Name: NameString


class LFTag(TypedDict, total=False):
    """A structure that allows an admin to grant user permissions on certain
    conditions. For example, granting a role access to all columns that do
    not have the LF-tag 'PII' in tables that have the LF-tag 'Prod'.
    """

    TagKey: LFTagKey
    TagValues: TagValueList


Expression = list[LFTag]


class LFTagPolicyResource(TypedDict, total=False):
    """A structure containing a list of LF-tag conditions or saved LF-Tag
    expressions that apply to a resource's LF-tag policy.
    """

    CatalogId: CatalogIdString | None
    ResourceType: ResourceType
    Expression: Expression | None
    ExpressionName: NameString | None


class LFTagKeyResource(TypedDict, total=False):
    """A structure containing an LF-tag key and values for a resource."""

    CatalogId: CatalogIdString | None
    TagKey: NameString
    TagValues: TagValueList


class DataCellsFilterResource(TypedDict, total=False):
    """A structure for a data cells filter resource."""

    TableCatalogId: CatalogIdString | None
    DatabaseName: NameString | None
    TableName: NameString | None
    Name: NameString | None


class DataLocationResource(TypedDict, total=False):
    """A structure for a data location object where permissions are granted or
    revoked.
    """

    CatalogId: CatalogIdString | None
    ResourceArn: ResourceArnString


ColumnNames = list[NameString]


class ColumnWildcard(TypedDict, total=False):
    """A wildcard object, consisting of an optional list of excluded column
    names or indexes.
    """

    ExcludedColumnNames: ColumnNames | None


class TableWithColumnsResource(TypedDict, total=False):
    """A structure for a table with columns object. This object is only used
    when granting a SELECT permission.

    This object must take a value for at least one of ``ColumnsNames``,
    ``ColumnsIndexes``, or ``ColumnsWildcard``.
    """

    CatalogId: CatalogIdString | None
    DatabaseName: NameString
    Name: NameString
    ColumnNames: ColumnNames | None
    ColumnWildcard: ColumnWildcard | None


class TableWildcard(TypedDict, total=False):
    """A wildcard object representing every table under a database."""

    pass


class TableResource(TypedDict, total=False):
    """A structure for the table object. A table is a metadata definition that
    represents your data. You can Grant and Revoke table privileges to a
    principal.
    """

    CatalogId: CatalogIdString | None
    DatabaseName: NameString
    Name: NameString | None
    TableWildcard: TableWildcard | None


class DatabaseResource(TypedDict, total=False):
    """A structure for the database object."""

    CatalogId: CatalogIdString | None
    Name: NameString


class CatalogResource(TypedDict, total=False):
    """A structure for the catalog object."""

    Id: CatalogIdString | None


class Resource(TypedDict, total=False):
    """A structure for the resource."""

    Catalog: CatalogResource | None
    Database: DatabaseResource | None
    Table: TableResource | None
    TableWithColumns: TableWithColumnsResource | None
    DataLocation: DataLocationResource | None
    DataCellsFilter: DataCellsFilterResource | None
    LFTag: LFTagKeyResource | None
    LFTagPolicy: LFTagPolicyResource | None
    LFTagExpression: LFTagExpressionResource | None


class AddLFTagsToResourceRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    Resource: Resource
    LFTags: LFTagsList


class ErrorDetail(TypedDict, total=False):
    """Contains details about an error."""

    ErrorCode: NameString | None
    ErrorMessage: DescriptionString | None


class LFTagError(TypedDict, total=False):
    """A structure containing an error related to a ``TagResource`` or
    ``UnTagResource`` operation.
    """

    LFTag: LFTagPair | None
    Error: ErrorDetail | None


LFTagErrors = list[LFTagError]


class AddLFTagsToResourceResponse(TypedDict, total=False):
    Failures: LFTagErrors | None


PartitionValuesList = list[PartitionValueString]
ObjectSize = int


class AddObjectInput(TypedDict, total=False):
    """A new object to add to the governed table."""

    Uri: URI
    ETag: ETagString
    Size: ObjectSize
    PartitionValues: PartitionValuesList | None


AdditionalContextMap = dict[ContextKey, ContextValue]


class AllRowsWildcard(TypedDict, total=False):
    """A structure that you pass to indicate you want all rows in a filter."""

    pass


class AssumeDecoratedRoleWithSAMLRequest(ServiceRequest):
    SAMLAssertion: SAMLAssertionString
    RoleArn: IAMRoleArn
    PrincipalArn: IAMSAMLProviderArn
    DurationSeconds: CredentialTimeoutDurationSecondInteger | None


ExpirationTimestamp = datetime


class AssumeDecoratedRoleWithSAMLResponse(TypedDict, total=False):
    AccessKeyId: AccessKeyIdString | None
    SecretAccessKey: SecretAccessKeyString | None
    SessionToken: SessionTokenString | None
    Expiration: ExpirationTimestamp | None


class AuditContext(TypedDict, total=False):
    """A structure used to include auditing information on the privileged API."""

    AdditionalAuditContext: AuditContextString | None


AuthorizedSessionTagValueList = list[NameString]
PermissionList = list[Permission]


class Condition(TypedDict, total=False):
    """A Lake Formation condition, which applies to permissions and opt-ins
    that contain an expression.
    """

    Expression: ExpressionString | None


class DataLakePrincipal(TypedDict, total=False):
    """The Lake Formation principal. Supported principals are IAM users or IAM
    roles.
    """

    DataLakePrincipalIdentifier: DataLakePrincipalString | None


class BatchPermissionsRequestEntry(TypedDict, total=False):
    """A permission to a resource granted by batch operation to the principal."""

    Id: Identifier
    Principal: DataLakePrincipal | None
    Resource: Resource | None
    Permissions: PermissionList | None
    Condition: Condition | None
    PermissionsWithGrantOption: PermissionList | None


BatchPermissionsRequestEntryList = list[BatchPermissionsRequestEntry]


class BatchGrantPermissionsRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    Entries: BatchPermissionsRequestEntryList


class BatchPermissionsFailureEntry(TypedDict, total=False):
    """A list of failures when performing a batch grant or batch revoke
    operation.
    """

    RequestEntry: BatchPermissionsRequestEntry | None
    Error: ErrorDetail | None


BatchPermissionsFailureList = list[BatchPermissionsFailureEntry]


class BatchGrantPermissionsResponse(TypedDict, total=False):
    Failures: BatchPermissionsFailureList | None


class BatchRevokePermissionsRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    Entries: BatchPermissionsRequestEntryList


class BatchRevokePermissionsResponse(TypedDict, total=False):
    Failures: BatchPermissionsFailureList | None


class CancelTransactionRequest(ServiceRequest):
    TransactionId: TransactionIdString


class CancelTransactionResponse(TypedDict, total=False):
    pass


class ColumnLFTag(TypedDict, total=False):
    """A structure containing the name of a column resource and the LF-tags
    attached to it.
    """

    Name: NameString | None
    LFTags: LFTagsList | None


ColumnLFTagsList = list[ColumnLFTag]


class CommitTransactionRequest(ServiceRequest):
    TransactionId: TransactionIdString


class CommitTransactionResponse(TypedDict, total=False):
    TransactionStatus: TransactionStatus | None


class RowFilter(TypedDict, total=False):
    """A PartiQL predicate."""

    FilterExpression: PredicateString | None
    AllRowsWildcard: AllRowsWildcard | None


class DataCellsFilter(TypedDict, total=False):
    """A structure that describes certain columns on certain rows."""

    TableCatalogId: CatalogIdString
    DatabaseName: NameString
    TableName: NameString
    Name: NameString
    RowFilter: RowFilter | None
    ColumnNames: ColumnNames | None
    ColumnWildcard: ColumnWildcard | None
    VersionId: VersionString | None


class CreateDataCellsFilterRequest(ServiceRequest):
    TableData: DataCellsFilter


class CreateDataCellsFilterResponse(TypedDict, total=False):
    pass


class CreateLFTagExpressionRequest(ServiceRequest):
    Name: NameString
    Description: DescriptionString | None
    CatalogId: CatalogIdString | None
    Expression: Expression


class CreateLFTagExpressionResponse(TypedDict, total=False):
    pass


class CreateLFTagRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    TagKey: LFTagKey
    TagValues: TagValueList


class CreateLFTagResponse(TypedDict, total=False):
    pass


class RedshiftConnect(TypedDict, total=False):
    """Configuration for enabling trusted identity propagation with Redshift
    Connect.
    """

    Authorization: ServiceAuthorization


class RedshiftScopeUnion(TypedDict, total=False):
    """A union structure representing different Redshift integration scopes."""

    RedshiftConnect: RedshiftConnect | None


RedshiftServiceIntegrations = list[RedshiftScopeUnion]


class ServiceIntegrationUnion(TypedDict, total=False):
    """A union structure representing different service integration types."""

    Redshift: RedshiftServiceIntegrations | None


ServiceIntegrationList = list[ServiceIntegrationUnion]
DataLakePrincipalList = list[DataLakePrincipal]
ScopeTargets = list[ScopeTarget]


class ExternalFilteringConfiguration(TypedDict, total=False):
    """Configuration for enabling external data filtering for third-party
    applications to access data managed by Lake Formation .
    """

    Status: EnableStatus
    AuthorizedTargets: ScopeTargets


class CreateLakeFormationIdentityCenterConfigurationRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    InstanceArn: IdentityCenterInstanceArn | None
    ExternalFiltering: ExternalFilteringConfiguration | None
    ShareRecipients: DataLakePrincipalList | None
    ServiceIntegrations: ServiceIntegrationList | None


class CreateLakeFormationIdentityCenterConfigurationResponse(TypedDict, total=False):
    ApplicationArn: ApplicationArn | None


class CreateLakeFormationOptInRequest(ServiceRequest):
    Principal: DataLakePrincipal
    Resource: Resource
    Condition: Condition | None


class CreateLakeFormationOptInResponse(TypedDict, total=False):
    pass


DataCellsFilterList = list[DataCellsFilter]
TrustedResourceOwners = list[CatalogIdString]
ParametersMap = dict[KeyString, ParametersMapValue]


class PrincipalPermissions(TypedDict, total=False):
    """Permissions granted to a principal."""

    Principal: DataLakePrincipal | None
    Permissions: PermissionList | None


PrincipalPermissionsList = list[PrincipalPermissions]


class DataLakeSettings(TypedDict, total=False):
    """A structure representing a list of Lake Formation principals designated
    as data lake administrators and lists of principal permission entries
    for default create database and default create table permissions.
    """

    DataLakeAdmins: DataLakePrincipalList | None
    ReadOnlyAdmins: DataLakePrincipalList | None
    CreateDatabaseDefaultPermissions: PrincipalPermissionsList | None
    CreateTableDefaultPermissions: PrincipalPermissionsList | None
    Parameters: ParametersMap | None
    TrustedResourceOwners: TrustedResourceOwners | None
    AllowExternalDataFiltering: NullableBoolean | None
    AllowFullTableExternalDataAccess: NullableBoolean | None
    ExternalDataFilteringAllowList: DataLakePrincipalList | None
    AuthorizedSessionTagValueList: AuthorizedSessionTagValueList | None


class TaggedDatabase(TypedDict, total=False):
    """A structure describing a database resource with LF-tags."""

    Database: DatabaseResource | None
    LFTags: LFTagsList | None


DatabaseLFTagsList = list[TaggedDatabase]
DateTime = datetime


class DeleteDataCellsFilterRequest(ServiceRequest):
    TableCatalogId: CatalogIdString | None
    DatabaseName: NameString | None
    TableName: NameString | None
    Name: NameString | None


class DeleteDataCellsFilterResponse(TypedDict, total=False):
    pass


class DeleteLFTagExpressionRequest(ServiceRequest):
    Name: NameString
    CatalogId: CatalogIdString | None


class DeleteLFTagExpressionResponse(TypedDict, total=False):
    pass


class DeleteLFTagRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    TagKey: LFTagKey


class DeleteLFTagResponse(TypedDict, total=False):
    pass


class DeleteLakeFormationIdentityCenterConfigurationRequest(ServiceRequest):
    CatalogId: CatalogIdString | None


class DeleteLakeFormationIdentityCenterConfigurationResponse(TypedDict, total=False):
    pass


class DeleteLakeFormationOptInRequest(ServiceRequest):
    Principal: DataLakePrincipal
    Resource: Resource
    Condition: Condition | None


class DeleteLakeFormationOptInResponse(TypedDict, total=False):
    pass


class DeleteObjectInput(TypedDict, total=False):
    """An object to delete from the governed table."""

    Uri: URI
    ETag: ETagString | None
    PartitionValues: PartitionValuesList | None


class VirtualObject(TypedDict, total=False):
    """An object that defines an Amazon S3 object to be deleted if a
    transaction cancels, provided that ``VirtualPut`` was called before
    writing the object.
    """

    Uri: URI
    ETag: ETagString | None


VirtualObjectList = list[VirtualObject]


class DeleteObjectsOnCancelRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    DatabaseName: NameString
    TableName: NameString
    TransactionId: TransactionIdString
    Objects: VirtualObjectList


class DeleteObjectsOnCancelResponse(TypedDict, total=False):
    pass


class DeregisterResourceRequest(ServiceRequest):
    ResourceArn: ResourceArnString


class DeregisterResourceResponse(TypedDict, total=False):
    pass


class DescribeLakeFormationIdentityCenterConfigurationRequest(ServiceRequest):
    CatalogId: CatalogIdString | None


class DescribeLakeFormationIdentityCenterConfigurationResponse(TypedDict, total=False):
    CatalogId: CatalogIdString | None
    InstanceArn: IdentityCenterInstanceArn | None
    ApplicationArn: ApplicationArn | None
    ExternalFiltering: ExternalFilteringConfiguration | None
    ShareRecipients: DataLakePrincipalList | None
    ServiceIntegrations: ServiceIntegrationList | None
    ResourceShare: RAMResourceShareArn | None


class DescribeResourceRequest(ServiceRequest):
    ResourceArn: ResourceArnString


LastModifiedTimestamp = datetime


class ResourceInfo(TypedDict, total=False):
    """A structure containing information about an Lake Formation resource."""

    ResourceArn: ResourceArnString | None
    RoleArn: IAMRoleArn | None
    LastModified: LastModifiedTimestamp | None
    WithFederation: NullableBoolean | None
    HybridAccessEnabled: NullableBoolean | None
    WithPrivilegedAccess: NullableBoolean | None
    VerificationStatus: VerificationStatus | None
    ExpectedResourceOwnerAccount: AccountIdString | None


class DescribeResourceResponse(TypedDict, total=False):
    ResourceInfo: ResourceInfo | None


class DescribeTransactionRequest(ServiceRequest):
    TransactionId: TransactionIdString


Timestamp = datetime


class TransactionDescription(TypedDict, total=False):
    """A structure that contains information about a transaction."""

    TransactionId: TransactionIdString | None
    TransactionStatus: TransactionStatus | None
    TransactionStartTime: Timestamp | None
    TransactionEndTime: Timestamp | None


class DescribeTransactionResponse(TypedDict, total=False):
    TransactionDescription: TransactionDescription | None


ResourceShareList = list[RAMResourceShareArn]


class DetailsMap(TypedDict, total=False):
    """A structure containing the additional details to be returned in the
    ``AdditionalDetails`` attribute of ``PrincipalResourcePermissions``.

    If a catalog resource is shared through Resource Access Manager (RAM),
    then there will exist a corresponding RAM resource share ARN.
    """

    ResourceShare: ResourceShareList | None


NumberOfItems = int
NumberOfBytes = int
NumberOfMilliseconds = int


class ExecutionStatistics(TypedDict, total=False):
    """Statistics related to the processing of a query statement."""

    AverageExecutionTimeMillis: NumberOfMilliseconds | None
    DataScannedBytes: NumberOfBytes | None
    WorkUnitsExecutedCount: NumberOfItems | None


class ExtendTransactionRequest(ServiceRequest):
    TransactionId: TransactionIdString | None


class ExtendTransactionResponse(TypedDict, total=False):
    pass


StringValueList = list[StringValue]


class FilterCondition(TypedDict, total=False):
    """This structure describes the filtering of columns in a table based on a
    filter condition.
    """

    Field: FieldNameString | None
    ComparisonOperator: ComparisonOperator | None
    StringValueList: StringValueList | None


FilterConditionList = list[FilterCondition]


class GetDataCellsFilterRequest(ServiceRequest):
    TableCatalogId: CatalogIdString
    DatabaseName: NameString
    TableName: NameString
    Name: NameString


class GetDataCellsFilterResponse(TypedDict, total=False):
    DataCellsFilter: DataCellsFilter | None


class GetDataLakePrincipalRequest(ServiceRequest):
    pass


class GetDataLakePrincipalResponse(TypedDict, total=False):
    Identity: IdentityString | None


class GetDataLakeSettingsRequest(ServiceRequest):
    CatalogId: CatalogIdString | None


class GetDataLakeSettingsResponse(TypedDict, total=False):
    DataLakeSettings: DataLakeSettings | None


class GetEffectivePermissionsForPathRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    ResourceArn: ResourceArnString
    NextToken: Token | None
    MaxResults: PageSize | None


class PrincipalResourcePermissions(TypedDict, total=False):
    """The permissions granted or revoked on a resource."""

    Principal: DataLakePrincipal | None
    Resource: Resource | None
    Condition: Condition | None
    Permissions: PermissionList | None
    PermissionsWithGrantOption: PermissionList | None
    AdditionalDetails: DetailsMap | None
    LastUpdated: LastModifiedTimestamp | None
    LastUpdatedBy: NameString | None


PrincipalResourcePermissionsList = list[PrincipalResourcePermissions]


class GetEffectivePermissionsForPathResponse(TypedDict, total=False):
    Permissions: PrincipalResourcePermissionsList | None
    NextToken: Token | None


class GetLFTagExpressionRequest(ServiceRequest):
    Name: NameString
    CatalogId: CatalogIdString | None


class GetLFTagExpressionResponse(TypedDict, total=False):
    Name: NameString | None
    Description: DescriptionString | None
    CatalogId: CatalogIdString | None
    Expression: Expression | None


class GetLFTagRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    TagKey: LFTagKey


class GetLFTagResponse(TypedDict, total=False):
    CatalogId: CatalogIdString | None
    TagKey: LFTagKey | None
    TagValues: TagValueList | None


class GetQueryStateRequest(ServiceRequest):
    QueryId: GetQueryStateRequestQueryIdString


class GetQueryStateResponse(TypedDict, total=False):
    """A structure for the output."""

    Error: ErrorMessageString | None
    State: QueryStateString


class GetQueryStatisticsRequest(ServiceRequest):
    QueryId: GetQueryStatisticsRequestQueryIdString


class PlanningStatistics(TypedDict, total=False):
    """Statistics related to the processing of a query statement."""

    EstimatedDataToScanBytes: NumberOfBytes | None
    PlanningTimeMillis: NumberOfMilliseconds | None
    QueueTimeMillis: NumberOfMilliseconds | None
    WorkUnitsGeneratedCount: NumberOfItems | None


class GetQueryStatisticsResponse(TypedDict, total=False):
    ExecutionStatistics: ExecutionStatistics | None
    PlanningStatistics: PlanningStatistics | None
    QuerySubmissionTime: DateTime | None


class GetResourceLFTagsRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    Resource: Resource
    ShowAssignedLFTags: BooleanNullable | None


class GetResourceLFTagsResponse(TypedDict, total=False):
    LFTagOnDatabase: LFTagsList | None
    LFTagsOnTable: LFTagsList | None
    LFTagsOnColumns: ColumnLFTagsList | None


class GetTableObjectsRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    DatabaseName: NameString
    TableName: NameString
    TransactionId: TransactionIdString | None
    QueryAsOfTime: Timestamp | None
    PartitionPredicate: PredicateString | None
    MaxResults: PageSize | None
    NextToken: TokenString | None


class TableObject(TypedDict, total=False):
    """Specifies the details of a governed table."""

    Uri: URI | None
    ETag: ETagString | None
    Size: ObjectSize | None


TableObjectList = list[TableObject]


class PartitionObjects(TypedDict, total=False):
    """A structure containing a list of partition values and table objects."""

    PartitionValues: PartitionValuesList | None
    Objects: TableObjectList | None


PartitionedTableObjectsList = list[PartitionObjects]


class GetTableObjectsResponse(TypedDict, total=False):
    Objects: PartitionedTableObjectsList | None
    NextToken: TokenString | None


PathStringList = list[PathString]


class GetTemporaryDataLocationCredentialsRequest(ServiceRequest):
    DurationSeconds: CredentialTimeoutDurationSecondInteger | None
    AuditContext: AuditContext | None
    DataLocations: PathStringList | None
    CredentialsScope: CredentialsScope | None


class TemporaryCredentials(TypedDict, total=False):
    """A temporary set of credentials for an Lake Formation user. These
    credentials are scoped down to only access the raw data sources that the
    user has access to.

    The temporary security credentials consist of an access key and a
    session token. The access key consists of an access key ID and a secret
    key. When the credentials are created, they are associated with an IAM
    access control policy that limits what the user can do when using the
    credentials.
    """

    AccessKeyId: AccessKeyIdString | None
    SecretAccessKey: SecretAccessKeyString | None
    SessionToken: SessionTokenString | None
    Expiration: ExpirationTimestamp | None


class GetTemporaryDataLocationCredentialsResponse(TypedDict, total=False):
    Credentials: TemporaryCredentials | None
    AccessibleDataLocations: PathStringList | None
    CredentialsScope: CredentialsScope | None


PermissionTypeList = list[PermissionType]
ValueStringList = list[ValueString]


class PartitionValueList(TypedDict, total=False):
    """Contains a list of values defining partitions."""

    Values: ValueStringList


class GetTemporaryGluePartitionCredentialsRequest(ServiceRequest):
    TableArn: ResourceArnString
    Partition: PartitionValueList
    Permissions: PermissionList | None
    DurationSeconds: CredentialTimeoutDurationSecondInteger | None
    AuditContext: AuditContext | None
    SupportedPermissionTypes: PermissionTypeList | None


class GetTemporaryGluePartitionCredentialsResponse(TypedDict, total=False):
    AccessKeyId: AccessKeyIdString | None
    SecretAccessKey: SecretAccessKeyString | None
    SessionToken: SessionTokenString | None
    Expiration: ExpirationTimestamp | None


class QuerySessionContext(TypedDict, total=False):
    """A structure used as a protocol between query engines and Lake Formation
    or Glue. Contains both a Lake Formation generated authorization
    identifier and information from the request's authorization context.
    """

    QueryId: HashString | None
    QueryStartTime: Timestamp | None
    ClusterId: NullableString | None
    QueryAuthorizationId: HashString | None
    AdditionalContext: AdditionalContextMap | None


class GetTemporaryGlueTableCredentialsRequest(ServiceRequest):
    TableArn: ResourceArnString
    Permissions: PermissionList | None
    DurationSeconds: CredentialTimeoutDurationSecondInteger | None
    AuditContext: AuditContext | None
    SupportedPermissionTypes: PermissionTypeList | None
    S3Path: PathString | None
    QuerySessionContext: QuerySessionContext | None


class GetTemporaryGlueTableCredentialsResponse(TypedDict, total=False):
    AccessKeyId: AccessKeyIdString | None
    SecretAccessKey: SecretAccessKeyString | None
    SessionToken: SessionTokenString | None
    Expiration: ExpirationTimestamp | None
    VendedS3Path: PathStringList | None


GetWorkUnitResultsRequestWorkUnitIdLong = int


class GetWorkUnitResultsRequest(ServiceRequest):
    QueryId: GetWorkUnitResultsRequestQueryIdString
    WorkUnitId: GetWorkUnitResultsRequestWorkUnitIdLong
    WorkUnitToken: SyntheticGetWorkUnitResultsRequestWorkUnitTokenString


ResultStream = bytes


class GetWorkUnitResultsResponse(TypedDict, total=False):
    """A structure for the output."""

    ResultStream: ResultStream | IO[ResultStream] | Iterable[ResultStream] | None


class GetWorkUnitsRequest(ServiceRequest):
    NextToken: Token | None
    PageSize: Integer | None
    QueryId: GetWorkUnitsRequestQueryIdString


WorkUnitIdLong = int


class WorkUnitRange(TypedDict, total=False):
    """Defines the valid range of work unit IDs for querying the execution
    service.
    """

    WorkUnitIdMax: WorkUnitIdLong
    WorkUnitIdMin: WorkUnitIdLong
    WorkUnitToken: WorkUnitTokenString


WorkUnitRangeList = list[WorkUnitRange]


class GetWorkUnitsResponse(TypedDict, total=False):
    """A structure for the output."""

    NextToken: Token | None
    QueryId: QueryIdString
    WorkUnitRanges: WorkUnitRangeList


class GrantPermissionsRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    Principal: DataLakePrincipal
    Resource: Resource
    Permissions: PermissionList
    Condition: Condition | None
    PermissionsWithGrantOption: PermissionList | None


class GrantPermissionsResponse(TypedDict, total=False):
    pass


class LFTagExpression(TypedDict, total=False):
    """A structure consists LF-Tag expression name and catalog ID."""

    Name: NameString | None
    Description: DescriptionString | None
    CatalogId: CatalogIdString | None
    Expression: Expression | None


LFTagExpressionsList = list[LFTagExpression]


class LakeFormationOptInsInfo(TypedDict, total=False):
    """A single principal-resource pair that has Lake Formation permissins
    enforced.
    """

    Resource: Resource | None
    Principal: DataLakePrincipal | None
    Condition: Condition | None
    LastModified: LastModifiedTimestamp | None
    LastUpdatedBy: NameString | None


LakeFormationOptInsInfoList = list[LakeFormationOptInsInfo]


class ListDataCellsFilterRequest(ServiceRequest):
    Table: TableResource | None
    NextToken: Token | None
    MaxResults: PageSize | None


class ListDataCellsFilterResponse(TypedDict, total=False):
    DataCellsFilters: DataCellsFilterList | None
    NextToken: Token | None


class ListLFTagExpressionsRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    MaxResults: PageSize | None
    NextToken: Token | None


class ListLFTagExpressionsResponse(TypedDict, total=False):
    LFTagExpressions: LFTagExpressionsList | None
    NextToken: Token | None


class ListLFTagsRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    ResourceShareType: ResourceShareType | None
    MaxResults: PageSize | None
    NextToken: Token | None


class ListLFTagsResponse(TypedDict, total=False):
    LFTags: LFTagsList | None
    NextToken: Token | None


class ListLakeFormationOptInsRequest(ServiceRequest):
    Principal: DataLakePrincipal | None
    Resource: Resource | None
    MaxResults: PageSize | None
    NextToken: Token | None


class ListLakeFormationOptInsResponse(TypedDict, total=False):
    LakeFormationOptInsInfoList: LakeFormationOptInsInfoList | None
    NextToken: Token | None


class ListPermissionsRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    Principal: DataLakePrincipal | None
    ResourceType: DataLakeResourceType | None
    Resource: Resource | None
    NextToken: Token | None
    MaxResults: PageSize | None
    IncludeRelated: TrueFalseString | None


class ListPermissionsResponse(TypedDict, total=False):
    PrincipalResourcePermissions: PrincipalResourcePermissionsList | None
    NextToken: Token | None


class ListResourcesRequest(ServiceRequest):
    FilterConditionList: FilterConditionList | None
    MaxResults: PageSize | None
    NextToken: Token | None


ResourceInfoList = list[ResourceInfo]


class ListResourcesResponse(TypedDict, total=False):
    ResourceInfoList: ResourceInfoList | None
    NextToken: Token | None


class ListTableStorageOptimizersRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    DatabaseName: NameString
    TableName: NameString
    StorageOptimizerType: OptimizerType | None
    MaxResults: PageSize | None
    NextToken: Token | None


StorageOptimizerConfig = dict[StorageOptimizerConfigKey, StorageOptimizerConfigValue]


class StorageOptimizer(TypedDict, total=False):
    """A structure describing the configuration and details of a storage
    optimizer.
    """

    StorageOptimizerType: OptimizerType | None
    Config: StorageOptimizerConfig | None
    ErrorMessage: MessageString | None
    Warnings: MessageString | None
    LastRunDetails: MessageString | None


StorageOptimizerList = list[StorageOptimizer]


class ListTableStorageOptimizersResponse(TypedDict, total=False):
    StorageOptimizerList: StorageOptimizerList | None
    NextToken: Token | None


class ListTransactionsRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    StatusFilter: TransactionStatusFilter | None
    MaxResults: PageSize | None
    NextToken: TokenString | None


TransactionDescriptionList = list[TransactionDescription]


class ListTransactionsResponse(TypedDict, total=False):
    Transactions: TransactionDescriptionList | None
    NextToken: TokenString | None


class PutDataLakeSettingsRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    DataLakeSettings: DataLakeSettings


class PutDataLakeSettingsResponse(TypedDict, total=False):
    pass


QueryParameterMap = dict[String, String]


class QueryPlanningContext(TypedDict, total=False):
    """A structure containing information about the query plan."""

    CatalogId: CatalogIdString | None
    DatabaseName: QueryPlanningContextDatabaseNameString
    QueryAsOfTime: Timestamp | None
    QueryParameters: QueryParameterMap | None
    TransactionId: TransactionIdString | None


class RegisterResourceRequest(ServiceRequest):
    ResourceArn: ResourceArnString
    UseServiceLinkedRole: NullableBoolean | None
    RoleArn: IAMRoleArn | None
    WithFederation: NullableBoolean | None
    HybridAccessEnabled: NullableBoolean | None
    WithPrivilegedAccess: Boolean | None
    ExpectedResourceOwnerAccount: AccountIdString | None


class RegisterResourceResponse(TypedDict, total=False):
    pass


class RemoveLFTagsFromResourceRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    Resource: Resource
    LFTags: LFTagsList


class RemoveLFTagsFromResourceResponse(TypedDict, total=False):
    Failures: LFTagErrors | None


class RevokePermissionsRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    Principal: DataLakePrincipal
    Resource: Resource
    Permissions: PermissionList
    Condition: Condition | None
    PermissionsWithGrantOption: PermissionList | None


class RevokePermissionsResponse(TypedDict, total=False):
    pass


class SearchDatabasesByLFTagsRequest(ServiceRequest):
    NextToken: Token | None
    MaxResults: SearchPageSize | None
    CatalogId: CatalogIdString | None
    Expression: Expression


class SearchDatabasesByLFTagsResponse(TypedDict, total=False):
    NextToken: Token | None
    DatabaseList: DatabaseLFTagsList | None


class SearchTablesByLFTagsRequest(ServiceRequest):
    NextToken: Token | None
    MaxResults: SearchPageSize | None
    CatalogId: CatalogIdString | None
    Expression: Expression


class TaggedTable(TypedDict, total=False):
    """A structure describing a table resource with LF-tags."""

    Table: TableResource | None
    LFTagOnDatabase: LFTagsList | None
    LFTagsOnTable: LFTagsList | None
    LFTagsOnColumns: ColumnLFTagsList | None


TableLFTagsList = list[TaggedTable]


class SearchTablesByLFTagsResponse(TypedDict, total=False):
    NextToken: Token | None
    TableList: TableLFTagsList | None


class StartQueryPlanningRequest(ServiceRequest):
    QueryPlanningContext: QueryPlanningContext
    QueryString: SyntheticStartQueryPlanningRequestQueryString


class StartQueryPlanningResponse(TypedDict, total=False):
    """A structure for the output."""

    QueryId: QueryIdString


class StartTransactionRequest(ServiceRequest):
    TransactionType: TransactionType | None


class StartTransactionResponse(TypedDict, total=False):
    TransactionId: TransactionIdString | None


StorageOptimizerConfigMap = dict[OptimizerType, StorageOptimizerConfig]


class UpdateDataCellsFilterRequest(ServiceRequest):
    TableData: DataCellsFilter


class UpdateDataCellsFilterResponse(TypedDict, total=False):
    pass


class UpdateLFTagExpressionRequest(ServiceRequest):
    Name: NameString
    Description: DescriptionString | None
    CatalogId: CatalogIdString | None
    Expression: Expression


class UpdateLFTagExpressionResponse(TypedDict, total=False):
    pass


class UpdateLFTagRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    TagKey: LFTagKey
    TagValuesToDelete: TagValueList | None
    TagValuesToAdd: TagValueList | None


class UpdateLFTagResponse(TypedDict, total=False):
    pass


class UpdateLakeFormationIdentityCenterConfigurationRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    ShareRecipients: DataLakePrincipalList | None
    ServiceIntegrations: ServiceIntegrationList | None
    ApplicationStatus: ApplicationStatus | None
    ExternalFiltering: ExternalFilteringConfiguration | None


class UpdateLakeFormationIdentityCenterConfigurationResponse(TypedDict, total=False):
    pass


class UpdateResourceRequest(ServiceRequest):
    RoleArn: IAMRoleArn
    ResourceArn: ResourceArnString
    WithFederation: NullableBoolean | None
    HybridAccessEnabled: NullableBoolean | None
    ExpectedResourceOwnerAccount: AccountIdString | None


class UpdateResourceResponse(TypedDict, total=False):
    pass


class WriteOperation(TypedDict, total=False):
    """Defines an object to add to or delete from a governed table."""

    AddObject: AddObjectInput | None
    DeleteObject: DeleteObjectInput | None


WriteOperationList = list[WriteOperation]


class UpdateTableObjectsRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    DatabaseName: NameString
    TableName: NameString
    TransactionId: TransactionIdString | None
    WriteOperations: WriteOperationList


class UpdateTableObjectsResponse(TypedDict, total=False):
    pass


class UpdateTableStorageOptimizerRequest(ServiceRequest):
    CatalogId: CatalogIdString | None
    DatabaseName: NameString
    TableName: NameString
    StorageOptimizerConfig: StorageOptimizerConfigMap


class UpdateTableStorageOptimizerResponse(TypedDict, total=False):
    Result: Result | None


class LakeformationApi:
    service: str = "lakeformation"
    version: str = "2017-03-31"

    @handler("AddLFTagsToResource")
    def add_lf_tags_to_resource(
        self,
        context: RequestContext,
        resource: Resource,
        lf_tags: LFTagsList,
        catalog_id: CatalogIdString | None = None,
        **kwargs,
    ) -> AddLFTagsToResourceResponse:
        """Attaches one or more LF-tags to an existing resource.

        :param resource: The database, table, or column resource to which to attach an LF-tag.
        :param lf_tags: The LF-tags to attach to the resource.
        :param catalog_id: The identifier for the Data Catalog.
        :returns: AddLFTagsToResourceResponse
        :raises EntityNotFoundException:
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises AccessDeniedException:
        :raises ConcurrentModificationException:
        """
        raise NotImplementedError

    @handler("AssumeDecoratedRoleWithSAML")
    def assume_decorated_role_with_saml(
        self,
        context: RequestContext,
        saml_assertion: SAMLAssertionString,
        role_arn: IAMRoleArn,
        principal_arn: IAMSAMLProviderArn,
        duration_seconds: CredentialTimeoutDurationSecondInteger | None = None,
        **kwargs,
    ) -> AssumeDecoratedRoleWithSAMLResponse:
        """Allows a caller to assume an IAM role decorated as the SAML user
        specified in the SAML assertion included in the request. This decoration
        allows Lake Formation to enforce access policies against the SAML users
        and groups. This API operation requires SAML federation setup in the
        caller’s account as it can only be called with valid SAML assertions.
        Lake Formation does not scope down the permission of the assumed role.
        All permissions attached to the role via the SAML federation setup will
        be included in the role session.

        This decorated role is expected to access data in Amazon S3 by getting
        temporary access from Lake Formation which is authorized via the virtual
        API ``GetDataAccess``. Therefore, all SAML roles that can be assumed via
        ``AssumeDecoratedRoleWithSAML`` must at a minimum include
        ``lakeformation:GetDataAccess`` in their role policies. A typical IAM
        policy attached to such a role would include the following actions:

        -  glue:*Database\\*

        -  glue:*Table\\*

        -  glue:*Partition\\*

        -  glue:*UserDefinedFunction\\*

        -  lakeformation:GetDataAccess

        :param saml_assertion: A SAML assertion consisting of an assertion statement for the user who
        needs temporary credentials.
        :param role_arn: The role that represents an IAM principal whose scope down policy allows
        it to call credential vending APIs such as
        ``GetTemporaryTableCredentials``.
        :param principal_arn: The Amazon Resource Name (ARN) of the SAML provider in IAM that
        describes the IdP.
        :param duration_seconds: The time period, between 900 and 43,200 seconds, for the timeout of the
        temporary credentials.
        :returns: AssumeDecoratedRoleWithSAMLResponse
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises EntityNotFoundException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("BatchGrantPermissions")
    def batch_grant_permissions(
        self,
        context: RequestContext,
        entries: BatchPermissionsRequestEntryList,
        catalog_id: CatalogIdString | None = None,
        **kwargs,
    ) -> BatchGrantPermissionsResponse:
        """Batch operation to grant permissions to the principal.

        :param entries: A list of up to 20 entries for resource permissions to be granted by
        batch operation to the principal.
        :param catalog_id: The identifier for the Data Catalog.
        :returns: BatchGrantPermissionsResponse
        :raises InvalidInputException:
        :raises OperationTimeoutException:
        """
        raise NotImplementedError

    @handler("BatchRevokePermissions")
    def batch_revoke_permissions(
        self,
        context: RequestContext,
        entries: BatchPermissionsRequestEntryList,
        catalog_id: CatalogIdString | None = None,
        **kwargs,
    ) -> BatchRevokePermissionsResponse:
        """Batch operation to revoke permissions from the principal.

        :param entries: A list of up to 20 entries for resource permissions to be revoked by
        batch operation to the principal.
        :param catalog_id: The identifier for the Data Catalog.
        :returns: BatchRevokePermissionsResponse
        :raises InvalidInputException:
        :raises OperationTimeoutException:
        """
        raise NotImplementedError

    @handler("CancelTransaction")
    def cancel_transaction(
        self, context: RequestContext, transaction_id: TransactionIdString, **kwargs
    ) -> CancelTransactionResponse:
        """Attempts to cancel the specified transaction. Returns an exception if
        the transaction was previously committed.

        :param transaction_id: The transaction to cancel.
        :returns: CancelTransactionResponse
        :raises InvalidInputException:
        :raises EntityNotFoundException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises TransactionCommittedException:
        :raises TransactionCommitInProgressException:
        :raises ConcurrentModificationException:
        """
        raise NotImplementedError

    @handler("CommitTransaction")
    def commit_transaction(
        self, context: RequestContext, transaction_id: TransactionIdString, **kwargs
    ) -> CommitTransactionResponse:
        """Attempts to commit the specified transaction. Returns an exception if
        the transaction was previously aborted. This API action is idempotent if
        called multiple times for the same transaction.

        :param transaction_id: The transaction to commit.
        :returns: CommitTransactionResponse
        :raises InvalidInputException:
        :raises EntityNotFoundException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises TransactionCanceledException:
        :raises ConcurrentModificationException:
        """
        raise NotImplementedError

    @handler("CreateDataCellsFilter")
    def create_data_cells_filter(
        self, context: RequestContext, table_data: DataCellsFilter, **kwargs
    ) -> CreateDataCellsFilterResponse:
        """Creates a data cell filter to allow one to grant access to certain
        columns on certain rows.

        :param table_data: A ``DataCellsFilter`` structure containing information about the data
        cells filter.
        :returns: CreateDataCellsFilterResponse
        :raises AlreadyExistsException:
        :raises InvalidInputException:
        :raises EntityNotFoundException:
        :raises ResourceNumberLimitExceededException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("CreateLFTag")
    def create_lf_tag(
        self,
        context: RequestContext,
        tag_key: LFTagKey,
        tag_values: TagValueList,
        catalog_id: CatalogIdString | None = None,
        **kwargs,
    ) -> CreateLFTagResponse:
        """Creates an LF-tag with the specified name and values.

        :param tag_key: The key-name for the LF-tag.
        :param tag_values: A list of possible values an attribute can take.
        :param catalog_id: The identifier for the Data Catalog.
        :returns: CreateLFTagResponse
        :raises EntityNotFoundException:
        :raises InvalidInputException:
        :raises ResourceNumberLimitExceededException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("CreateLFTagExpression")
    def create_lf_tag_expression(
        self,
        context: RequestContext,
        name: NameString,
        expression: Expression,
        description: DescriptionString | None = None,
        catalog_id: CatalogIdString | None = None,
        **kwargs,
    ) -> CreateLFTagExpressionResponse:
        """Creates a new LF-Tag expression with the provided name, description,
        catalog ID, and expression body. This call fails if a LF-Tag expression
        with the same name already exists in the caller’s account or if the
        underlying LF-Tags don't exist. To call this API operation, caller needs
        the following Lake Formation permissions:

        ``CREATE_LF_TAG_EXPRESSION`` on the root catalog resource.

        ``GRANT_WITH_LF_TAG_EXPRESSION`` on all underlying LF-Tag key:value
        pairs included in the expression.

        :param name: A name for the expression.
        :param expression: A list of LF-Tag conditions (key-value pairs).
        :param description: A description with information about the LF-Tag expression.
        :param catalog_id: The identifier for the Data Catalog.
        :returns: CreateLFTagExpressionResponse
        :raises InvalidInputException:
        :raises ResourceNumberLimitExceededException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises AccessDeniedException:
        :raises EntityNotFoundException:
        """
        raise NotImplementedError

    @handler("CreateLakeFormationIdentityCenterConfiguration")
    def create_lake_formation_identity_center_configuration(
        self,
        context: RequestContext,
        catalog_id: CatalogIdString | None = None,
        instance_arn: IdentityCenterInstanceArn | None = None,
        external_filtering: ExternalFilteringConfiguration | None = None,
        share_recipients: DataLakePrincipalList | None = None,
        service_integrations: ServiceIntegrationList | None = None,
        **kwargs,
    ) -> CreateLakeFormationIdentityCenterConfigurationResponse:
        """Creates an IAM Identity Center connection with Lake Formation to allow
        IAM Identity Center users and groups to access Data Catalog resources.

        :param catalog_id: The identifier for the Data Catalog.
        :param instance_arn: The ARN of the IAM Identity Center instance for which the operation will
        be executed.
        :param external_filtering: A list of the account IDs of Amazon Web Services accounts of third-party
        applications that are allowed to access data managed by Lake Formation.
        :param share_recipients: A list of Amazon Web Services account IDs and/or Amazon Web Services
        organization/organizational unit ARNs that are allowed to access data
        managed by Lake Formation.
        :param service_integrations: A list of service integrations for enabling trusted identity propagation
        with external services such as Redshift.
        :returns: CreateLakeFormationIdentityCenterConfigurationResponse
        :raises InvalidInputException:
        :raises AlreadyExistsException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises AccessDeniedException:
        :raises ConcurrentModificationException:
        """
        raise NotImplementedError

    @handler("CreateLakeFormationOptIn")
    def create_lake_formation_opt_in(
        self,
        context: RequestContext,
        principal: DataLakePrincipal,
        resource: Resource,
        condition: Condition | None = None,
        **kwargs,
    ) -> CreateLakeFormationOptInResponse:
        """Enforce Lake Formation permissions for the given databases, tables, and
        principals.

        :param principal: The Lake Formation principal.
        :param resource: A structure for the resource.
        :param condition: A Lake Formation condition, which applies to permissions and opt-ins
        that contain an expression.
        :returns: CreateLakeFormationOptInResponse
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises EntityNotFoundException:
        :raises AccessDeniedException:
        :raises ConcurrentModificationException:
        :raises ResourceNumberLimitExceededException:
        """
        raise NotImplementedError

    @handler("DeleteDataCellsFilter")
    def delete_data_cells_filter(
        self,
        context: RequestContext,
        table_catalog_id: CatalogIdString | None = None,
        database_name: NameString | None = None,
        table_name: NameString | None = None,
        name: NameString | None = None,
        **kwargs,
    ) -> DeleteDataCellsFilterResponse:
        """Deletes a data cell filter.

        :param table_catalog_id: The ID of the catalog to which the table belongs.
        :param database_name: A database in the Glue Data Catalog.
        :param table_name: A table in the database.
        :param name: The name given by the user to the data filter cell.
        :returns: DeleteDataCellsFilterResponse
        :raises InvalidInputException:
        :raises EntityNotFoundException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("DeleteLFTag")
    def delete_lf_tag(
        self,
        context: RequestContext,
        tag_key: LFTagKey,
        catalog_id: CatalogIdString | None = None,
        **kwargs,
    ) -> DeleteLFTagResponse:
        """Deletes an LF-tag by its key name. The operation fails if the specified
        tag key doesn't exist. When you delete an LF-Tag:

        -  The associated LF-Tag policy becomes invalid.

        -  Resources that had this tag assigned will no longer have the tag
           policy applied to them.

        :param tag_key: The key-name for the LF-tag to delete.
        :param catalog_id: The identifier for the Data Catalog.
        :returns: DeleteLFTagResponse
        :raises EntityNotFoundException:
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("DeleteLFTagExpression")
    def delete_lf_tag_expression(
        self,
        context: RequestContext,
        name: NameString,
        catalog_id: CatalogIdString | None = None,
        **kwargs,
    ) -> DeleteLFTagExpressionResponse:
        """Deletes the LF-Tag expression. The caller must be a data lake admin or
        have ``DROP`` permissions on the LF-Tag expression. Deleting a LF-Tag
        expression will also delete all ``LFTagPolicy`` permissions referencing
        the LF-Tag expression.

        :param name: The name for the LF-Tag expression.
        :param catalog_id: The identifier for the Data Catalog.
        :returns: DeleteLFTagExpressionResponse
        :raises EntityNotFoundException:
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("DeleteLakeFormationIdentityCenterConfiguration")
    def delete_lake_formation_identity_center_configuration(
        self, context: RequestContext, catalog_id: CatalogIdString | None = None, **kwargs
    ) -> DeleteLakeFormationIdentityCenterConfigurationResponse:
        """Deletes an IAM Identity Center connection with Lake Formation.

        :param catalog_id: The identifier for the Data Catalog.
        :returns: DeleteLakeFormationIdentityCenterConfigurationResponse
        :raises InvalidInputException:
        :raises EntityNotFoundException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises AccessDeniedException:
        :raises ConcurrentModificationException:
        """
        raise NotImplementedError

    @handler("DeleteLakeFormationOptIn")
    def delete_lake_formation_opt_in(
        self,
        context: RequestContext,
        principal: DataLakePrincipal,
        resource: Resource,
        condition: Condition | None = None,
        **kwargs,
    ) -> DeleteLakeFormationOptInResponse:
        """Remove the Lake Formation permissions enforcement of the given
        databases, tables, and principals.

        :param principal: The Lake Formation principal.
        :param resource: A structure for the resource.
        :param condition: A Lake Formation condition, which applies to permissions and opt-ins
        that contain an expression.
        :returns: DeleteLakeFormationOptInResponse
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises EntityNotFoundException:
        :raises AccessDeniedException:
        :raises ConcurrentModificationException:
        """
        raise NotImplementedError

    @handler("DeleteObjectsOnCancel")
    def delete_objects_on_cancel(
        self,
        context: RequestContext,
        database_name: NameString,
        table_name: NameString,
        transaction_id: TransactionIdString,
        objects: VirtualObjectList,
        catalog_id: CatalogIdString | None = None,
        **kwargs,
    ) -> DeleteObjectsOnCancelResponse:
        """For a specific governed table, provides a list of Amazon S3 objects that
        will be written during the current transaction and that can be
        automatically deleted if the transaction is canceled. Without this call,
        no Amazon S3 objects are automatically deleted when a transaction
        cancels.

        The Glue ETL library function ``write_dynamic_frame.from_catalog()``
        includes an option to automatically call ``DeleteObjectsOnCancel``
        before writes. For more information, see `Rolling Back Amazon S3
        Writes <https://docs.aws.amazon.com/lake-formation/latest/dg/transactions-data-operations.html#rolling-back-writes>`__.

        :param database_name: The database that contains the governed table.
        :param table_name: The name of the governed table.
        :param transaction_id: ID of the transaction that the writes occur in.
        :param objects: A list of VirtualObject structures, which indicates the Amazon S3
        objects to be deleted if the transaction cancels.
        :param catalog_id: The Glue data catalog that contains the governed table.
        :returns: DeleteObjectsOnCancelResponse
        :raises InternalServiceException:
        :raises InvalidInputException:
        :raises OperationTimeoutException:
        :raises EntityNotFoundException:
        :raises TransactionCommittedException:
        :raises TransactionCanceledException:
        :raises ResourceNotReadyException:
        :raises ConcurrentModificationException:
        """
        raise NotImplementedError

    @handler("DeregisterResource")
    def deregister_resource(
        self, context: RequestContext, resource_arn: ResourceArnString, **kwargs
    ) -> DeregisterResourceResponse:
        """Deregisters the resource as managed by the Data Catalog.

        When you deregister a path, Lake Formation removes the path from the
        inline policy attached to your service-linked role.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource that you want to
        deregister.
        :returns: DeregisterResourceResponse
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises EntityNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeLakeFormationIdentityCenterConfiguration")
    def describe_lake_formation_identity_center_configuration(
        self, context: RequestContext, catalog_id: CatalogIdString | None = None, **kwargs
    ) -> DescribeLakeFormationIdentityCenterConfigurationResponse:
        """Retrieves the instance ARN and application ARN for the connection.

        :param catalog_id: The identifier for the Data Catalog.
        :returns: DescribeLakeFormationIdentityCenterConfigurationResponse
        :raises InvalidInputException:
        :raises EntityNotFoundException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("DescribeResource")
    def describe_resource(
        self, context: RequestContext, resource_arn: ResourceArnString, **kwargs
    ) -> DescribeResourceResponse:
        """Retrieves the current data access role for the given resource registered
        in Lake Formation.

        :param resource_arn: The resource ARN.
        :returns: DescribeResourceResponse
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises EntityNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeTransaction")
    def describe_transaction(
        self, context: RequestContext, transaction_id: TransactionIdString, **kwargs
    ) -> DescribeTransactionResponse:
        """Returns the details of a single transaction.

        :param transaction_id: The transaction for which to return status.
        :returns: DescribeTransactionResponse
        :raises EntityNotFoundException:
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        """
        raise NotImplementedError

    @handler("ExtendTransaction")
    def extend_transaction(
        self, context: RequestContext, transaction_id: TransactionIdString | None = None, **kwargs
    ) -> ExtendTransactionResponse:
        """Indicates to the service that the specified transaction is still active
        and should not be treated as idle and aborted.

        Write transactions that remain idle for a long period are automatically
        aborted unless explicitly extended.

        :param transaction_id: The transaction to extend.
        :returns: ExtendTransactionResponse
        :raises InvalidInputException:
        :raises EntityNotFoundException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises TransactionCommittedException:
        :raises TransactionCanceledException:
        :raises TransactionCommitInProgressException:
        """
        raise NotImplementedError

    @handler("GetDataCellsFilter")
    def get_data_cells_filter(
        self,
        context: RequestContext,
        table_catalog_id: CatalogIdString,
        database_name: NameString,
        table_name: NameString,
        name: NameString,
        **kwargs,
    ) -> GetDataCellsFilterResponse:
        """Returns a data cells filter.

        :param table_catalog_id: The ID of the catalog to which the table belongs.
        :param database_name: A database in the Glue Data Catalog.
        :param table_name: A table in the database.
        :param name: The name given by the user to the data filter cell.
        :returns: GetDataCellsFilterResponse
        :raises EntityNotFoundException:
        :raises InvalidInputException:
        :raises OperationTimeoutException:
        :raises InternalServiceException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("GetDataLakePrincipal")
    def get_data_lake_principal(
        self, context: RequestContext, **kwargs
    ) -> GetDataLakePrincipalResponse:
        """Returns the identity of the invoking principal.

        :returns: GetDataLakePrincipalResponse
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("GetDataLakeSettings")
    def get_data_lake_settings(
        self, context: RequestContext, catalog_id: CatalogIdString | None = None, **kwargs
    ) -> GetDataLakeSettingsResponse:
        """Retrieves the list of the data lake administrators of a Lake
        Formation-managed data lake.

        :param catalog_id: The identifier for the Data Catalog.
        :returns: GetDataLakeSettingsResponse
        :raises InternalServiceException:
        :raises InvalidInputException:
        :raises EntityNotFoundException:
        """
        raise NotImplementedError

    @handler("GetEffectivePermissionsForPath")
    def get_effective_permissions_for_path(
        self,
        context: RequestContext,
        resource_arn: ResourceArnString,
        catalog_id: CatalogIdString | None = None,
        next_token: Token | None = None,
        max_results: PageSize | None = None,
        **kwargs,
    ) -> GetEffectivePermissionsForPathResponse:
        """Returns the Lake Formation permissions for a specified table or database
        resource located at a path in Amazon S3.
        ``GetEffectivePermissionsForPath`` will not return databases and tables
        if the catalog is encrypted.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource for which you want to get
        permissions.
        :param catalog_id: The identifier for the Data Catalog.
        :param next_token: A continuation token, if this is not the first call to retrieve this
        list.
        :param max_results: The maximum number of results to return.
        :returns: GetEffectivePermissionsForPathResponse
        :raises InvalidInputException:
        :raises EntityNotFoundException:
        :raises OperationTimeoutException:
        :raises InternalServiceException:
        """
        raise NotImplementedError

    @handler("GetLFTag")
    def get_lf_tag(
        self,
        context: RequestContext,
        tag_key: LFTagKey,
        catalog_id: CatalogIdString | None = None,
        **kwargs,
    ) -> GetLFTagResponse:
        """Returns an LF-tag definition.

        :param tag_key: The key-name for the LF-tag.
        :param catalog_id: The identifier for the Data Catalog.
        :returns: GetLFTagResponse
        :raises EntityNotFoundException:
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("GetLFTagExpression")
    def get_lf_tag_expression(
        self,
        context: RequestContext,
        name: NameString,
        catalog_id: CatalogIdString | None = None,
        **kwargs,
    ) -> GetLFTagExpressionResponse:
        """Returns the details about the LF-Tag expression. The caller must be a
        data lake admin or must have ``DESCRIBE`` permission on the LF-Tag
        expression resource.

        :param name: The name for the LF-Tag expression.
        :param catalog_id: The identifier for the Data Catalog.
        :returns: GetLFTagExpressionResponse
        :raises EntityNotFoundException:
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("GetQueryState")
    def get_query_state(
        self, context: RequestContext, query_id: GetQueryStateRequestQueryIdString, **kwargs
    ) -> GetQueryStateResponse:
        """Returns the state of a query previously submitted. Clients are expected
        to poll ``GetQueryState`` to monitor the current state of the planning
        before retrieving the work units. A query state is only visible to the
        principal that made the initial call to ``StartQueryPlanning``.

        :param query_id: The ID of the plan query operation.
        :returns: GetQueryStateResponse
        :raises InternalServiceException:
        :raises InvalidInputException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("GetQueryStatistics")
    def get_query_statistics(
        self, context: RequestContext, query_id: GetQueryStatisticsRequestQueryIdString, **kwargs
    ) -> GetQueryStatisticsResponse:
        """Retrieves statistics on the planning and execution of a query.

        :param query_id: The ID of the plan query operation.
        :returns: GetQueryStatisticsResponse
        :raises StatisticsNotReadyYetException:
        :raises InternalServiceException:
        :raises InvalidInputException:
        :raises AccessDeniedException:
        :raises ExpiredException:
        :raises ThrottledException:
        """
        raise NotImplementedError

    @handler("GetResourceLFTags")
    def get_resource_lf_tags(
        self,
        context: RequestContext,
        resource: Resource,
        catalog_id: CatalogIdString | None = None,
        show_assigned_lf_tags: BooleanNullable | None = None,
        **kwargs,
    ) -> GetResourceLFTagsResponse:
        """Returns the LF-tags applied to a resource.

        :param resource: The database, table, or column resource for which you want to return
        LF-tags.
        :param catalog_id: The identifier for the Data Catalog.
        :param show_assigned_lf_tags: Indicates whether to show the assigned LF-tags.
        :returns: GetResourceLFTagsResponse
        :raises EntityNotFoundException:
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises GlueEncryptionException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("GetTableObjects")
    def get_table_objects(
        self,
        context: RequestContext,
        database_name: NameString,
        table_name: NameString,
        catalog_id: CatalogIdString | None = None,
        transaction_id: TransactionIdString | None = None,
        query_as_of_time: Timestamp | None = None,
        partition_predicate: PredicateString | None = None,
        max_results: PageSize | None = None,
        next_token: TokenString | None = None,
        **kwargs,
    ) -> GetTableObjectsResponse:
        """Returns the set of Amazon S3 objects that make up the specified governed
        table. A transaction ID or timestamp can be specified for time-travel
        queries.

        :param database_name: The database containing the governed table.
        :param table_name: The governed table for which to retrieve objects.
        :param catalog_id: The catalog containing the governed table.
        :param transaction_id: The transaction ID at which to read the governed table contents.
        :param query_as_of_time: The time as of when to read the governed table contents.
        :param partition_predicate: A predicate to filter the objects returned based on the partition keys
        defined in the governed table.
        :param max_results: Specifies how many values to return in a page.
        :param next_token: A continuation token if this is not the first call to retrieve these
        objects.
        :returns: GetTableObjectsResponse
        :raises EntityNotFoundException:
        :raises InternalServiceException:
        :raises InvalidInputException:
        :raises OperationTimeoutException:
        :raises TransactionCommittedException:
        :raises TransactionCanceledException:
        :raises ResourceNotReadyException:
        """
        raise NotImplementedError

    @handler("GetTemporaryDataLocationCredentials")
    def get_temporary_data_location_credentials(
        self,
        context: RequestContext,
        duration_seconds: CredentialTimeoutDurationSecondInteger | None = None,
        audit_context: AuditContext | None = None,
        data_locations: PathStringList | None = None,
        credentials_scope: CredentialsScope | None = None,
        **kwargs,
    ) -> GetTemporaryDataLocationCredentialsResponse:
        """Allows a user or application in a secure environment to access data in a
        specific Amazon S3 location registered with Lake Formation by providing
        temporary scoped credentials that are limited to the requested data
        location and the caller's authorized access level.

        The API operation returns an error in the following scenarios:

        -  The data location is not registered with Lake Formation.

        -  No Glue table is associated with the data location.

        -  The caller doesn't have required permissions on the associated table.
           The caller must have ``SELECT`` or ``SUPER`` permissions on the
           associated table, and credential vending for full table access must
           be enabled in the data lake settings.

           For more information, see `Application integration for full table
           access <https://docs.aws.amazon.com/lake-formation/latest/dg/full-table-credential-vending.html>`__.

        -  The data location is in a different Amazon Web Services Region. Lake
           Formation doesn't support cross-Region access when vending
           credentials for a data location. Lake Formation only supports Amazon
           S3 paths registered within the same Region as the API call.

        :param duration_seconds: The time period, between 900 and 43,200 seconds, for the timeout of the
        temporary credentials.
        :param audit_context: A structure used to include auditing information on the privileged API.
        :param data_locations: The Amazon S3 data location that you want to access.
        :param credentials_scope: The credential scope is determined by the caller's Lake Formation
        permission on the associated table.
        :returns: GetTemporaryDataLocationCredentialsResponse
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises GlueEncryptionException:
        :raises EntityNotFoundException:
        :raises AccessDeniedException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("GetTemporaryGluePartitionCredentials")
    def get_temporary_glue_partition_credentials(
        self,
        context: RequestContext,
        table_arn: ResourceArnString,
        partition: PartitionValueList,
        permissions: PermissionList | None = None,
        duration_seconds: CredentialTimeoutDurationSecondInteger | None = None,
        audit_context: AuditContext | None = None,
        supported_permission_types: PermissionTypeList | None = None,
        **kwargs,
    ) -> GetTemporaryGluePartitionCredentialsResponse:
        """This API is identical to ``GetTemporaryTableCredentials`` except that
        this is used when the target Data Catalog resource is of type Partition.
        Lake Formation restricts the permission of the vended credentials with
        the same scope down policy which restricts access to a single Amazon S3
        prefix.

        :param table_arn: The ARN of the partitions' table.
        :param partition: A list of partition values identifying a single partition.
        :param permissions: Filters the request based on the user having been granted a list of
        specified permissions on the requested resource(s).
        :param duration_seconds: The time period, between 900 and 21,600 seconds, for the timeout of the
        temporary credentials.
        :param audit_context: A structure representing context to access a resource (column names,
        query ID, etc).
        :param supported_permission_types: A list of supported permission types for the partition.
        :returns: GetTemporaryGluePartitionCredentialsResponse
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises EntityNotFoundException:
        :raises AccessDeniedException:
        :raises PermissionTypeMismatchException:
        """
        raise NotImplementedError

    @handler("GetTemporaryGlueTableCredentials")
    def get_temporary_glue_table_credentials(
        self,
        context: RequestContext,
        table_arn: ResourceArnString,
        permissions: PermissionList | None = None,
        duration_seconds: CredentialTimeoutDurationSecondInteger | None = None,
        audit_context: AuditContext | None = None,
        supported_permission_types: PermissionTypeList | None = None,
        s3_path: PathString | None = None,
        query_session_context: QuerySessionContext | None = None,
        **kwargs,
    ) -> GetTemporaryGlueTableCredentialsResponse:
        """Allows a caller in a secure environment to assume a role with permission
        to access Amazon S3. In order to vend such credentials, Lake Formation
        assumes the role associated with a registered location, for example an
        Amazon S3 bucket, with a scope down policy which restricts the access to
        a single prefix.

        To call this API, the role that the service assumes must have
        ``lakeformation:GetDataAccess`` permission on the resource.

        :param table_arn: The ARN identifying a table in the Data Catalog for the temporary
        credentials request.
        :param permissions: Filters the request based on the user having been granted a list of
        specified permissions on the requested resource(s).
        :param duration_seconds: The time period, between 900 and 21,600 seconds, for the timeout of the
        temporary credentials.
        :param audit_context: A structure representing context to access a resource (column names,
        query ID, etc).
        :param supported_permission_types: A list of supported permission types for the table.
        :param s3_path: The Amazon S3 path for the table.
        :param query_session_context: A structure used as a protocol between query engines and Lake Formation
        or Glue.
        :returns: GetTemporaryGlueTableCredentialsResponse
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises EntityNotFoundException:
        :raises AccessDeniedException:
        :raises PermissionTypeMismatchException:
        """
        raise NotImplementedError

    @handler("GetWorkUnitResults")
    def get_work_unit_results(
        self,
        context: RequestContext,
        query_id: GetWorkUnitResultsRequestQueryIdString,
        work_unit_id: GetWorkUnitResultsRequestWorkUnitIdLong,
        work_unit_token: SyntheticGetWorkUnitResultsRequestWorkUnitTokenString,
        **kwargs,
    ) -> GetWorkUnitResultsResponse:
        """Returns the work units resulting from the query. Work units can be
        executed in any order and in parallel.

        :param query_id: The ID of the plan query operation for which to get results.
        :param work_unit_id: The work unit ID for which to get results.
        :param work_unit_token: A work token used to query the execution service.
        :returns: GetWorkUnitResultsResponse
        :raises InternalServiceException:
        :raises InvalidInputException:
        :raises AccessDeniedException:
        :raises ExpiredException:
        :raises ThrottledException:
        """
        raise NotImplementedError

    @handler("GetWorkUnits")
    def get_work_units(
        self,
        context: RequestContext,
        query_id: GetWorkUnitsRequestQueryIdString,
        next_token: Token | None = None,
        page_size: Integer | None = None,
        **kwargs,
    ) -> GetWorkUnitsResponse:
        """Retrieves the work units generated by the ``StartQueryPlanning``
        operation.

        :param query_id: The ID of the plan query operation.
        :param next_token: A continuation token, if this is a continuation call.
        :param page_size: The size of each page to get in the Amazon Web Services service call.
        :returns: GetWorkUnitsResponse
        :raises WorkUnitsNotReadyYetException:
        :raises InternalServiceException:
        :raises InvalidInputException:
        :raises AccessDeniedException:
        :raises ExpiredException:
        """
        raise NotImplementedError

    @handler("GrantPermissions")
    def grant_permissions(
        self,
        context: RequestContext,
        principal: DataLakePrincipal,
        resource: Resource,
        permissions: PermissionList,
        catalog_id: CatalogIdString | None = None,
        condition: Condition | None = None,
        permissions_with_grant_option: PermissionList | None = None,
        **kwargs,
    ) -> GrantPermissionsResponse:
        """Grants permissions to the principal to access metadata in the Data
        Catalog and data organized in underlying data storage such as Amazon S3.

        For information about permissions, see `Security and Access Control to
        Metadata and
        Data <https://docs.aws.amazon.com/lake-formation/latest/dg/security-data-access.html>`__.

        :param principal: The principal to be granted the permissions on the resource.
        :param resource: The resource to which permissions are to be granted.
        :param permissions: The permissions granted to the principal on the resource.
        :param catalog_id: The identifier for the Data Catalog.
        :param condition: A Lake Formation condition, which applies to permissions and opt-ins
        that contain an expression.
        :param permissions_with_grant_option: Indicates a list of the granted permissions that the principal may pass
        to other users.
        :returns: GrantPermissionsResponse
        :raises ConcurrentModificationException:
        :raises EntityNotFoundException:
        :raises InvalidInputException:
        """
        raise NotImplementedError

    @handler("ListDataCellsFilter")
    def list_data_cells_filter(
        self,
        context: RequestContext,
        table: TableResource | None = None,
        next_token: Token | None = None,
        max_results: PageSize | None = None,
        **kwargs,
    ) -> ListDataCellsFilterResponse:
        """Lists all the data cell filters on a table.

        :param table: A table in the Glue Data Catalog.
        :param next_token: A continuation token, if this is a continuation call.
        :param max_results: The maximum size of the response.
        :returns: ListDataCellsFilterResponse
        :raises InvalidInputException:
        :raises OperationTimeoutException:
        :raises InternalServiceException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("ListLFTagExpressions")
    def list_lf_tag_expressions(
        self,
        context: RequestContext,
        catalog_id: CatalogIdString | None = None,
        max_results: PageSize | None = None,
        next_token: Token | None = None,
        **kwargs,
    ) -> ListLFTagExpressionsResponse:
        """Returns the LF-Tag expressions in caller’s account filtered based on
        caller's permissions. Data Lake and read only admins implicitly can see
        all tag expressions in their account, else caller needs DESCRIBE
        permissions on tag expression.

        :param catalog_id: The identifier for the Data Catalog.
        :param max_results: The maximum number of results to return.
        :param next_token: A continuation token, if this is not the first call to retrieve this
        list.
        :returns: ListLFTagExpressionsResponse
        :raises EntityNotFoundException:
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("ListLFTags")
    def list_lf_tags(
        self,
        context: RequestContext,
        catalog_id: CatalogIdString | None = None,
        resource_share_type: ResourceShareType | None = None,
        max_results: PageSize | None = None,
        next_token: Token | None = None,
        **kwargs,
    ) -> ListLFTagsResponse:
        """Lists LF-tags that the requester has permission to view.

        :param catalog_id: The identifier for the Data Catalog.
        :param resource_share_type: If resource share type is ``ALL``, returns both in-account LF-tags and
        shared LF-tags that the requester has permission to view.
        :param max_results: The maximum number of results to return.
        :param next_token: A continuation token, if this is not the first call to retrieve this
        list.
        :returns: ListLFTagsResponse
        :raises EntityNotFoundException:
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("ListLakeFormationOptIns")
    def list_lake_formation_opt_ins(
        self,
        context: RequestContext,
        principal: DataLakePrincipal | None = None,
        resource: Resource | None = None,
        max_results: PageSize | None = None,
        next_token: Token | None = None,
        **kwargs,
    ) -> ListLakeFormationOptInsResponse:
        """Retrieve the current list of resources and principals that are opt in to
        enforce Lake Formation permissions.

        :param principal: The Lake Formation principal.
        :param resource: A structure for the resource.
        :param max_results: The maximum number of results to return.
        :param next_token: A continuation token, if this is not the first call to retrieve this
        list.
        :returns: ListLakeFormationOptInsResponse
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("ListPermissions")
    def list_permissions(
        self,
        context: RequestContext,
        catalog_id: CatalogIdString | None = None,
        principal: DataLakePrincipal | None = None,
        resource_type: DataLakeResourceType | None = None,
        resource: Resource | None = None,
        next_token: Token | None = None,
        max_results: PageSize | None = None,
        include_related: TrueFalseString | None = None,
        **kwargs,
    ) -> ListPermissionsResponse:
        """Returns a list of the principal permissions on the resource, filtered by
        the permissions of the caller. For example, if you are granted an ALTER
        permission, you are able to see only the principal permissions for
        ALTER.

        This operation returns only those permissions that have been explicitly
        granted. If both ``Principal`` and ``Resource`` parameters are provided,
        the response returns effective permissions rather than the explicitly
        granted permissions.

        For information about permissions, see `Security and Access Control to
        Metadata and
        Data <https://docs.aws.amazon.com/lake-formation/latest/dg/security-data-access.html>`__.

        :param catalog_id: The identifier for the Data Catalog.
        :param principal: Specifies a principal to filter the permissions returned.
        :param resource_type: Specifies a resource type to filter the permissions returned.
        :param resource: A resource where you will get a list of the principal permissions.
        :param next_token: A continuation token, if this is not the first call to retrieve this
        list.
        :param max_results: The maximum number of results to return.
        :param include_related: Indicates that related permissions should be included in the results
        when listing permissions on a table resource.
        :returns: ListPermissionsResponse
        :raises InvalidInputException:
        :raises OperationTimeoutException:
        :raises InternalServiceException:
        """
        raise NotImplementedError

    @handler("ListResources")
    def list_resources(
        self,
        context: RequestContext,
        filter_condition_list: FilterConditionList | None = None,
        max_results: PageSize | None = None,
        next_token: Token | None = None,
        **kwargs,
    ) -> ListResourcesResponse:
        """Lists the resources registered to be managed by the Data Catalog.

        :param filter_condition_list: Any applicable row-level and/or column-level filtering conditions for
        the resources.
        :param max_results: The maximum number of resource results.
        :param next_token: A continuation token, if this is not the first call to retrieve these
        resources.
        :returns: ListResourcesResponse
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        """
        raise NotImplementedError

    @handler("ListTableStorageOptimizers")
    def list_table_storage_optimizers(
        self,
        context: RequestContext,
        database_name: NameString,
        table_name: NameString,
        catalog_id: CatalogIdString | None = None,
        storage_optimizer_type: OptimizerType | None = None,
        max_results: PageSize | None = None,
        next_token: Token | None = None,
        **kwargs,
    ) -> ListTableStorageOptimizersResponse:
        """Returns the configuration of all storage optimizers associated with a
        specified table.

        :param database_name: Name of the database where the table is present.
        :param table_name: Name of the table.
        :param catalog_id: The Catalog ID of the table.
        :param storage_optimizer_type: The specific type of storage optimizers to list.
        :param max_results: The number of storage optimizers to return on each call.
        :param next_token: A continuation token, if this is a continuation call.
        :returns: ListTableStorageOptimizersResponse
        :raises EntityNotFoundException:
        :raises InvalidInputException:
        :raises AccessDeniedException:
        :raises InternalServiceException:
        """
        raise NotImplementedError

    @handler("ListTransactions")
    def list_transactions(
        self,
        context: RequestContext,
        catalog_id: CatalogIdString | None = None,
        status_filter: TransactionStatusFilter | None = None,
        max_results: PageSize | None = None,
        next_token: TokenString | None = None,
        **kwargs,
    ) -> ListTransactionsResponse:
        """Returns metadata about transactions and their status. To prevent the
        response from growing indefinitely, only uncommitted transactions and
        those available for time-travel queries are returned.

        This operation can help you identify uncommitted transactions or to get
        information about transactions.

        :param catalog_id: The catalog for which to list transactions.
        :param status_filter: A filter indicating the status of transactions to return.
        :param max_results: The maximum number of transactions to return in a single call.
        :param next_token: A continuation token if this is not the first call to retrieve
        transactions.
        :returns: ListTransactionsResponse
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        """
        raise NotImplementedError

    @handler("PutDataLakeSettings")
    def put_data_lake_settings(
        self,
        context: RequestContext,
        data_lake_settings: DataLakeSettings,
        catalog_id: CatalogIdString | None = None,
        **kwargs,
    ) -> PutDataLakeSettingsResponse:
        """Sets the list of data lake administrators who have admin privileges on
        all resources managed by Lake Formation. For more information on admin
        privileges, see `Granting Lake Formation
        Permissions <https://docs.aws.amazon.com/lake-formation/latest/dg/lake-formation-permissions.html>`__.

        This API replaces the current list of data lake admins with the new list
        being passed. To add an admin, fetch the current list and add the new
        admin to that list and pass that list in this API.

        :param data_lake_settings: A structure representing a list of Lake Formation principals designated
        as data lake administrators.
        :param catalog_id: The identifier for the Data Catalog.
        :returns: PutDataLakeSettingsResponse
        :raises InternalServiceException:
        :raises InvalidInputException:
        """
        raise NotImplementedError

    @handler("RegisterResource")
    def register_resource(
        self,
        context: RequestContext,
        resource_arn: ResourceArnString,
        use_service_linked_role: NullableBoolean | None = None,
        role_arn: IAMRoleArn | None = None,
        with_federation: NullableBoolean | None = None,
        hybrid_access_enabled: NullableBoolean | None = None,
        with_privileged_access: Boolean | None = None,
        expected_resource_owner_account: AccountIdString | None = None,
        **kwargs,
    ) -> RegisterResourceResponse:
        """Registers the resource as managed by the Data Catalog.

        To add or update data, Lake Formation needs read/write access to the
        chosen data location. Choose a role that you know has permission to do
        this, or choose the AWSServiceRoleForLakeFormationDataAccess
        service-linked role. When you register the first Amazon S3 path, the
        service-linked role and a new inline policy are created on your behalf.
        Lake Formation adds the first path to the inline policy and attaches it
        to the service-linked role. When you register subsequent paths, Lake
        Formation adds the path to the existing policy.

        The following request registers a new location and gives Lake Formation
        permission to use the service-linked role to access that location.

        ``ResourceArn = arn:aws:s3:::my-bucket/ UseServiceLinkedRole = true``

        If ``UseServiceLinkedRole`` is not set to true, you must provide or set
        the ``RoleArn``:

        ``arn:aws:iam::12345:role/my-data-access-role``

        :param resource_arn: The Amazon Resource Name (ARN) of the resource that you want to
        register.
        :param use_service_linked_role: Designates an Identity and Access Management (IAM) service-linked role
        by registering this role with the Data Catalog.
        :param role_arn: The identifier for the role that registers the resource.
        :param with_federation: Whether or not the resource is a federated resource.
        :param hybrid_access_enabled: Specifies whether the data access of tables pointing to the location can
        be managed by both Lake Formation permissions as well as Amazon S3
        bucket policies.
        :param with_privileged_access: Grants the calling principal the permissions to perform all supported
        Lake Formation operations on the registered data location.
        :param expected_resource_owner_account: The Amazon Web Services account that owns the Glue tables associated
        with specific Amazon S3 locations.
        :returns: RegisterResourceResponse
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises AlreadyExistsException:
        :raises EntityNotFoundException:
        :raises ResourceNumberLimitExceededException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("RemoveLFTagsFromResource")
    def remove_lf_tags_from_resource(
        self,
        context: RequestContext,
        resource: Resource,
        lf_tags: LFTagsList,
        catalog_id: CatalogIdString | None = None,
        **kwargs,
    ) -> RemoveLFTagsFromResourceResponse:
        """Removes an LF-tag from the resource. Only database, table, or
        tableWithColumns resource are allowed. To tag columns, use the column
        inclusion list in ``tableWithColumns`` to specify column input.

        :param resource: The database, table, or column resource where you want to remove an
        LF-tag.
        :param lf_tags: The LF-tags to be removed from the resource.
        :param catalog_id: The identifier for the Data Catalog.
        :returns: RemoveLFTagsFromResourceResponse
        :raises EntityNotFoundException:
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises GlueEncryptionException:
        :raises AccessDeniedException:
        :raises ConcurrentModificationException:
        """
        raise NotImplementedError

    @handler("RevokePermissions")
    def revoke_permissions(
        self,
        context: RequestContext,
        principal: DataLakePrincipal,
        resource: Resource,
        permissions: PermissionList,
        catalog_id: CatalogIdString | None = None,
        condition: Condition | None = None,
        permissions_with_grant_option: PermissionList | None = None,
        **kwargs,
    ) -> RevokePermissionsResponse:
        """Revokes permissions to the principal to access metadata in the Data
        Catalog and data organized in underlying data storage such as Amazon S3.

        :param principal: The principal to be revoked permissions on the resource.
        :param resource: The resource to which permissions are to be revoked.
        :param permissions: The permissions revoked to the principal on the resource.
        :param catalog_id: The identifier for the Data Catalog.
        :param condition: A Lake Formation condition, which applies to permissions and opt-ins
        that contain an expression.
        :param permissions_with_grant_option: Indicates a list of permissions for which to revoke the grant option
        allowing the principal to pass permissions to other principals.
        :returns: RevokePermissionsResponse
        :raises ConcurrentModificationException:
        :raises EntityNotFoundException:
        :raises InvalidInputException:
        """
        raise NotImplementedError

    @handler("SearchDatabasesByLFTags")
    def search_databases_by_lf_tags(
        self,
        context: RequestContext,
        expression: Expression,
        next_token: Token | None = None,
        max_results: SearchPageSize | None = None,
        catalog_id: CatalogIdString | None = None,
        **kwargs,
    ) -> SearchDatabasesByLFTagsResponse:
        """This operation allows a search on ``DATABASE`` resources by
        ``TagCondition``. This operation is used by admins who want to grant
        user permissions on certain ``TagConditions``. Before making a grant,
        the admin can use ``SearchDatabasesByTags`` to find all resources where
        the given ``TagConditions`` are valid to verify whether the returned
        resources can be shared.

        :param expression: A list of conditions (``LFTag`` structures) to search for in database
        resources.
        :param next_token: A continuation token, if this is not the first call to retrieve this
        list.
        :param max_results: The maximum number of results to return.
        :param catalog_id: The identifier for the Data Catalog.
        :returns: SearchDatabasesByLFTagsResponse
        :raises EntityNotFoundException:
        :raises InternalServiceException:
        :raises InvalidInputException:
        :raises OperationTimeoutException:
        :raises GlueEncryptionException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("SearchTablesByLFTags")
    def search_tables_by_lf_tags(
        self,
        context: RequestContext,
        expression: Expression,
        next_token: Token | None = None,
        max_results: SearchPageSize | None = None,
        catalog_id: CatalogIdString | None = None,
        **kwargs,
    ) -> SearchTablesByLFTagsResponse:
        """This operation allows a search on ``TABLE`` resources by ``LFTag`` s.
        This will be used by admins who want to grant user permissions on
        certain LF-tags. Before making a grant, the admin can use
        ``SearchTablesByLFTags`` to find all resources where the given
        ``LFTag`` s are valid to verify whether the returned resources can be
        shared.

        :param expression: A list of conditions (``LFTag`` structures) to search for in table
        resources.
        :param next_token: A continuation token, if this is not the first call to retrieve this
        list.
        :param max_results: The maximum number of results to return.
        :param catalog_id: The identifier for the Data Catalog.
        :returns: SearchTablesByLFTagsResponse
        :raises EntityNotFoundException:
        :raises InternalServiceException:
        :raises InvalidInputException:
        :raises OperationTimeoutException:
        :raises GlueEncryptionException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("StartQueryPlanning")
    def start_query_planning(
        self,
        context: RequestContext,
        query_planning_context: QueryPlanningContext,
        query_string: SyntheticStartQueryPlanningRequestQueryString,
        **kwargs,
    ) -> StartQueryPlanningResponse:
        """Submits a request to process a query statement.

        This operation generates work units that can be retrieved with the
        ``GetWorkUnits`` operation as soon as the query state is
        WORKUNITS_AVAILABLE or FINISHED.

        :param query_planning_context: A structure containing information about the query plan.
        :param query_string: A PartiQL query statement used as an input to the planner service.
        :returns: StartQueryPlanningResponse
        :raises InternalServiceException:
        :raises InvalidInputException:
        :raises AccessDeniedException:
        :raises ThrottledException:
        """
        raise NotImplementedError

    @handler("StartTransaction")
    def start_transaction(
        self, context: RequestContext, transaction_type: TransactionType | None = None, **kwargs
    ) -> StartTransactionResponse:
        """Starts a new transaction and returns its transaction ID. Transaction IDs
        are opaque objects that you can use to identify a transaction.

        :param transaction_type: Indicates whether this transaction should be read only or read and
        write.
        :returns: StartTransactionResponse
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        """
        raise NotImplementedError

    @handler("UpdateDataCellsFilter")
    def update_data_cells_filter(
        self, context: RequestContext, table_data: DataCellsFilter, **kwargs
    ) -> UpdateDataCellsFilterResponse:
        """Updates a data cell filter.

        :param table_data: A ``DataCellsFilter`` structure containing information about the data
        cells filter.
        :returns: UpdateDataCellsFilterResponse
        :raises ConcurrentModificationException:
        :raises InvalidInputException:
        :raises EntityNotFoundException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("UpdateLFTag")
    def update_lf_tag(
        self,
        context: RequestContext,
        tag_key: LFTagKey,
        catalog_id: CatalogIdString | None = None,
        tag_values_to_delete: TagValueList | None = None,
        tag_values_to_add: TagValueList | None = None,
        **kwargs,
    ) -> UpdateLFTagResponse:
        """Updates the list of possible values for the specified LF-tag key. If the
        LF-tag does not exist, the operation throws an EntityNotFoundException.
        The values in the delete key values will be deleted from list of
        possible values. If any value in the delete key values is attached to a
        resource, then API errors out with a 400 Exception - "Update not
        allowed". Untag the attribute before deleting the LF-tag key's value.

        :param tag_key: The key-name for the LF-tag for which to add or delete values.
        :param catalog_id: The identifier for the Data Catalog.
        :param tag_values_to_delete: A list of LF-tag values to delete from the LF-tag.
        :param tag_values_to_add: A list of LF-tag values to add from the LF-tag.
        :returns: UpdateLFTagResponse
        :raises EntityNotFoundException:
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises ConcurrentModificationException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("UpdateLFTagExpression")
    def update_lf_tag_expression(
        self,
        context: RequestContext,
        name: NameString,
        expression: Expression,
        description: DescriptionString | None = None,
        catalog_id: CatalogIdString | None = None,
        **kwargs,
    ) -> UpdateLFTagExpressionResponse:
        """Updates the name of the LF-Tag expression to the new description and
        expression body provided. Updating a LF-Tag expression immediately
        changes the permission boundaries of all existing ``LFTagPolicy``
        permission grants that reference the given LF-Tag expression.

        :param name: The name for the LF-Tag expression.
        :param expression: The LF-Tag expression body composed of one more LF-Tag key-value pairs.
        :param description: The description with information about the saved LF-Tag expression.
        :param catalog_id: The identifier for the Data Catalog.
        :returns: UpdateLFTagExpressionResponse
        :raises EntityNotFoundException:
        :raises InvalidInputException:
        :raises ResourceNumberLimitExceededException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("UpdateLakeFormationIdentityCenterConfiguration")
    def update_lake_formation_identity_center_configuration(
        self,
        context: RequestContext,
        catalog_id: CatalogIdString | None = None,
        share_recipients: DataLakePrincipalList | None = None,
        service_integrations: ServiceIntegrationList | None = None,
        application_status: ApplicationStatus | None = None,
        external_filtering: ExternalFilteringConfiguration | None = None,
        **kwargs,
    ) -> UpdateLakeFormationIdentityCenterConfigurationResponse:
        """Updates the IAM Identity Center connection parameters.

        :param catalog_id: The identifier for the Data Catalog.
        :param share_recipients: A list of Amazon Web Services account IDs or Amazon Web Services
        organization/organizational unit ARNs that are allowed to access to
        access data managed by Lake Formation.
        :param service_integrations: A list of service integrations for enabling trusted identity propagation
        with external services such as Redshift.
        :param application_status: Allows to enable or disable the IAM Identity Center connection.
        :param external_filtering: A list of the account IDs of Amazon Web Services accounts of third-party
        applications that are allowed to access data managed by Lake Formation.
        :returns: UpdateLakeFormationIdentityCenterConfigurationResponse
        :raises InvalidInputException:
        :raises EntityNotFoundException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises AccessDeniedException:
        :raises ConcurrentModificationException:
        """
        raise NotImplementedError

    @handler("UpdateResource")
    def update_resource(
        self,
        context: RequestContext,
        role_arn: IAMRoleArn,
        resource_arn: ResourceArnString,
        with_federation: NullableBoolean | None = None,
        hybrid_access_enabled: NullableBoolean | None = None,
        expected_resource_owner_account: AccountIdString | None = None,
        **kwargs,
    ) -> UpdateResourceResponse:
        """Updates the data access role used for vending access to the given
        (registered) resource in Lake Formation.

        :param role_arn: The new role to use for the given resource registered in Lake Formation.
        :param resource_arn: The resource ARN.
        :param with_federation: Whether or not the resource is a federated resource.
        :param hybrid_access_enabled: Specifies whether the data access of tables pointing to the location can
        be managed by both Lake Formation permissions as well as Amazon S3
        bucket policies.
        :param expected_resource_owner_account: The Amazon Web Services account that owns the Glue tables associated
        with specific Amazon S3 locations.
        :returns: UpdateResourceResponse
        :raises InvalidInputException:
        :raises InternalServiceException:
        :raises OperationTimeoutException:
        :raises EntityNotFoundException:
        """
        raise NotImplementedError

    @handler("UpdateTableObjects")
    def update_table_objects(
        self,
        context: RequestContext,
        database_name: NameString,
        table_name: NameString,
        write_operations: WriteOperationList,
        catalog_id: CatalogIdString | None = None,
        transaction_id: TransactionIdString | None = None,
        **kwargs,
    ) -> UpdateTableObjectsResponse:
        """Updates the manifest of Amazon S3 objects that make up the specified
        governed table.

        :param database_name: The database containing the governed table to update.
        :param table_name: The governed table to update.
        :param write_operations: A list of ``WriteOperation`` objects that define an object to add to or
        delete from the manifest for a governed table.
        :param catalog_id: The catalog containing the governed table to update.
        :param transaction_id: The transaction at which to do the write.
        :returns: UpdateTableObjectsResponse
        :raises InternalServiceException:
        :raises InvalidInputException:
        :raises OperationTimeoutException:
        :raises EntityNotFoundException:
        :raises TransactionCommittedException:
        :raises TransactionCanceledException:
        :raises TransactionCommitInProgressException:
        :raises ResourceNotReadyException:
        :raises ConcurrentModificationException:
        """
        raise NotImplementedError

    @handler("UpdateTableStorageOptimizer")
    def update_table_storage_optimizer(
        self,
        context: RequestContext,
        database_name: NameString,
        table_name: NameString,
        storage_optimizer_config: StorageOptimizerConfigMap,
        catalog_id: CatalogIdString | None = None,
        **kwargs,
    ) -> UpdateTableStorageOptimizerResponse:
        """Updates the configuration of the storage optimizers for a table.

        :param database_name: Name of the database where the table is present.
        :param table_name: Name of the table for which to enable the storage optimizer.
        :param storage_optimizer_config: Name of the configuration for the storage optimizer.
        :param catalog_id: The Catalog ID of the table.
        :returns: UpdateTableStorageOptimizerResponse
        :raises EntityNotFoundException:
        :raises InvalidInputException:
        :raises AccessDeniedException:
        :raises InternalServiceException:
        """
        raise NotImplementedError
