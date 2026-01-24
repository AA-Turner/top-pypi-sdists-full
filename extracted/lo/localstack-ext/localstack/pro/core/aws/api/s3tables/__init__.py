from datetime import datetime
from enum import StrEnum
from typing import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

AccountId = str
Boolean = bool
EncryptionConfigurationKmsKeyArnString = str
ErrorMessage = str
IAMRole = str
ListNamespacesLimit = int
ListNamespacesRequestPrefixString = str
ListTableBucketsLimit = int
ListTableBucketsRequestPrefixString = str
ListTablesLimit = int
ListTablesRequestPrefixString = str
MetadataLocation = str
NamespaceId = str
NamespaceName = str
NextToken = str
PositiveInteger = int
ResourceArn = str
ResourcePolicy = str
String = str
TableARN = str
TableBucketARN = str
TableBucketId = str
TableBucketName = str
TableName = str
TagKey = str
TagValue = str
VersionToken = str
WarehouseLocation = str


class IcebergCompactionStrategy(StrEnum):
    auto = "auto"
    binpack = "binpack"
    sort = "sort"
    z_order = "z-order"


class JobStatus(StrEnum):
    Not_Yet_Run = "Not_Yet_Run"
    Successful = "Successful"
    Failed = "Failed"
    Disabled = "Disabled"


class MaintenanceStatus(StrEnum):
    enabled = "enabled"
    disabled = "disabled"


class OpenTableFormat(StrEnum):
    ICEBERG = "ICEBERG"


class ReplicationStatus(StrEnum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class SSEAlgorithm(StrEnum):
    AES256 = "AES256"
    aws_kms = "aws:kms"


class StorageClass(StrEnum):
    STANDARD = "STANDARD"
    INTELLIGENT_TIERING = "INTELLIGENT_TIERING"


class TableBucketMaintenanceType(StrEnum):
    icebergUnreferencedFileRemoval = "icebergUnreferencedFileRemoval"


class TableBucketType(StrEnum):
    customer = "customer"
    aws = "aws"


class TableMaintenanceJobType(StrEnum):
    icebergCompaction = "icebergCompaction"
    icebergSnapshotManagement = "icebergSnapshotManagement"
    icebergUnreferencedFileRemoval = "icebergUnreferencedFileRemoval"


class TableMaintenanceType(StrEnum):
    icebergCompaction = "icebergCompaction"
    icebergSnapshotManagement = "icebergSnapshotManagement"


class TableRecordExpirationJobStatus(StrEnum):
    NotYetRun = "NotYetRun"
    Successful = "Successful"
    Failed = "Failed"
    Disabled = "Disabled"


class TableRecordExpirationStatus(StrEnum):
    enabled = "enabled"
    disabled = "disabled"


class TableType(StrEnum):
    customer = "customer"
    aws = "aws"


class AccessDeniedException(ServiceException):
    """The action cannot be performed because you do not have the required
    permission.
    """

    code: str = "AccessDeniedException"
    sender_fault: bool = True
    status_code: int = 403


class BadRequestException(ServiceException):
    """The request is invalid or malformed."""

    code: str = "BadRequestException"
    sender_fault: bool = True
    status_code: int = 400


class ConflictException(ServiceException):
    """The request failed because there is a conflict with a previous write.
    You can retry the request.
    """

    code: str = "ConflictException"
    sender_fault: bool = True
    status_code: int = 409


class ForbiddenException(ServiceException):
    """The caller isn't authorized to make the request."""

    code: str = "ForbiddenException"
    sender_fault: bool = True
    status_code: int = 403


class InternalServerErrorException(ServiceException):
    """The request failed due to an internal server error."""

    code: str = "InternalServerErrorException"
    sender_fault: bool = False
    status_code: int = 500


class MethodNotAllowedException(ServiceException):
    """The requested operation is not allowed on this resource. This may occur
    when attempting to modify a resource that is managed by a service or has
    restrictions that prevent the operation.
    """

    code: str = "MethodNotAllowedException"
    sender_fault: bool = True
    status_code: int = 405


class NotFoundException(ServiceException):
    """The request was rejected because the specified resource could not be
    found.
    """

    code: str = "NotFoundException"
    sender_fault: bool = True
    status_code: int = 404


class TooManyRequestsException(ServiceException):
    """The limit on the number of requests per second was exceeded."""

    code: str = "TooManyRequestsException"
    sender_fault: bool = True
    status_code: int = 429


CreateNamespaceRequestNamespaceList = list[NamespaceName]


class CreateNamespaceRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    namespace: CreateNamespaceRequestNamespaceList


NamespaceList = list[NamespaceName]


class CreateNamespaceResponse(TypedDict, total=False):
    tableBucketARN: TableBucketARN
    namespace: NamespaceList


Tags = dict[TagKey, TagValue]


class StorageClassConfiguration(TypedDict, total=False):
    """The configuration details for the storage class of tables or table
    buckets. This allows you to optimize storage costs by selecting the
    appropriate storage class based on your access patterns and performance
    requirements.
    """

    storageClass: StorageClass


class EncryptionConfiguration(TypedDict, total=False):
    """Configuration specifying how data should be encrypted. This structure
    defines the encryption algorithm and optional KMS key to be used for
    server-side encryption.
    """

    sseAlgorithm: SSEAlgorithm
    kmsKeyArn: EncryptionConfigurationKmsKeyArnString | None


class CreateTableBucketRequest(ServiceRequest):
    name: TableBucketName
    encryptionConfiguration: EncryptionConfiguration | None
    storageClassConfiguration: StorageClassConfiguration | None
    tags: Tags | None


class CreateTableBucketResponse(TypedDict, total=False):
    arn: TableBucketARN


TableProperties = dict[String, String]


class SchemaField(TypedDict, total=False):
    name: String
    type: String
    required: Boolean | None


SchemaFieldList = list[SchemaField]


class IcebergSchema(TypedDict, total=False):
    """Contains details about the schema for an Iceberg table."""

    fields: SchemaFieldList


class IcebergMetadata(TypedDict, total=False):
    """Contains details about the metadata for an Iceberg table."""

    schema: IcebergSchema
    properties: TableProperties | None


class TableMetadata(TypedDict, total=False):
    """Contains details about the table metadata."""

    iceberg: IcebergMetadata | None


class CreateTableRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    namespace: NamespaceName
    name: TableName
    format: OpenTableFormat
    metadata: TableMetadata | None
    encryptionConfiguration: EncryptionConfiguration | None
    storageClassConfiguration: StorageClassConfiguration | None
    tags: Tags | None


class CreateTableResponse(TypedDict, total=False):
    tableARN: TableARN
    versionToken: VersionToken


class DeleteNamespaceRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    namespace: NamespaceName


class DeleteTableBucketEncryptionRequest(ServiceRequest):
    tableBucketARN: TableBucketARN


class DeleteTableBucketMetricsConfigurationRequest(ServiceRequest):
    tableBucketARN: TableBucketARN


class DeleteTableBucketPolicyRequest(ServiceRequest):
    tableBucketARN: TableBucketARN


class DeleteTableBucketReplicationRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    versionToken: VersionToken | None


class DeleteTableBucketRequest(ServiceRequest):
    tableBucketARN: TableBucketARN


class DeleteTablePolicyRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    namespace: NamespaceName
    name: TableName


class DeleteTableReplicationRequest(ServiceRequest):
    tableArn: TableARN
    versionToken: String


class DeleteTableRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    namespace: NamespaceName
    name: TableName
    versionToken: VersionToken | None


class GetNamespaceRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    namespace: NamespaceName


SyntheticTimestamp_date_time = datetime


class GetNamespaceResponse(TypedDict, total=False):
    namespace: NamespaceList
    createdAt: SyntheticTimestamp_date_time
    createdBy: AccountId
    ownerAccountId: AccountId
    namespaceId: NamespaceId | None
    tableBucketId: TableBucketId | None


class GetTableBucketEncryptionRequest(ServiceRequest):
    tableBucketARN: TableBucketARN


class GetTableBucketEncryptionResponse(TypedDict, total=False):
    encryptionConfiguration: EncryptionConfiguration


class GetTableBucketMaintenanceConfigurationRequest(ServiceRequest):
    tableBucketARN: TableBucketARN


class IcebergUnreferencedFileRemovalSettings(TypedDict, total=False):
    """Contains details about the unreferenced file removal settings for an
    Iceberg table bucket.
    """

    unreferencedDays: PositiveInteger | None
    nonCurrentDays: PositiveInteger | None


class TableBucketMaintenanceSettings(TypedDict, total=False):
    """Contains details about the maintenance settings for the table bucket."""

    icebergUnreferencedFileRemoval: IcebergUnreferencedFileRemovalSettings | None


class TableBucketMaintenanceConfigurationValue(TypedDict, total=False):
    """Details about the values that define the maintenance configuration for a
    table bucket.
    """

    status: MaintenanceStatus | None
    settings: TableBucketMaintenanceSettings | None


TableBucketMaintenanceConfiguration = dict[
    TableBucketMaintenanceType, TableBucketMaintenanceConfigurationValue
]


class GetTableBucketMaintenanceConfigurationResponse(TypedDict, total=False):
    tableBucketARN: TableBucketARN
    configuration: TableBucketMaintenanceConfiguration


class GetTableBucketMetricsConfigurationRequest(ServiceRequest):
    tableBucketARN: TableBucketARN


class GetTableBucketMetricsConfigurationResponse(TypedDict, total=False):
    tableBucketARN: TableBucketARN
    id: String | None


class GetTableBucketPolicyRequest(ServiceRequest):
    tableBucketARN: TableBucketARN


class GetTableBucketPolicyResponse(TypedDict, total=False):
    resourcePolicy: ResourcePolicy


class GetTableBucketReplicationRequest(ServiceRequest):
    tableBucketARN: TableBucketARN


class ReplicationDestination(TypedDict, total=False):
    """Specifies a destination table bucket for replication."""

    destinationTableBucketARN: TableBucketARN


ReplicationDestinations = list[ReplicationDestination]


class TableBucketReplicationRule(TypedDict, total=False):
    """Defines a rule for replicating tables from a source table bucket to one
    or more destination table buckets.
    """

    destinations: ReplicationDestinations


TableBucketReplicationRules = list[TableBucketReplicationRule]


class TableBucketReplicationConfiguration(TypedDict, total=False):
    """The replication configuration for a table bucket. This configuration
    defines how tables in the source bucket are replicated to destination
    table buckets, including the IAM role used for replication.
    """

    role: IAMRole
    rules: TableBucketReplicationRules


class GetTableBucketReplicationResponse(TypedDict, total=False):
    versionToken: VersionToken
    configuration: TableBucketReplicationConfiguration


class GetTableBucketRequest(ServiceRequest):
    tableBucketARN: TableBucketARN


class GetTableBucketResponse(TypedDict, total=False):
    arn: TableBucketARN
    name: TableBucketName
    ownerAccountId: AccountId
    createdAt: SyntheticTimestamp_date_time
    tableBucketId: TableBucketId | None
    type: TableBucketType | None


class GetTableBucketStorageClassRequest(ServiceRequest):
    tableBucketARN: TableBucketARN


class GetTableBucketStorageClassResponse(TypedDict, total=False):
    storageClassConfiguration: StorageClassConfiguration


class GetTableEncryptionRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    namespace: NamespaceName
    name: TableName


class GetTableEncryptionResponse(TypedDict, total=False):
    encryptionConfiguration: EncryptionConfiguration


class GetTableMaintenanceConfigurationRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    namespace: NamespaceName
    name: TableName


class IcebergSnapshotManagementSettings(TypedDict, total=False):
    """Contains details about the snapshot management settings for an Iceberg
    table. The oldest snapshot expires when its age exceeds the
    ``maxSnapshotAgeHours`` and the total number of snapshots exceeds the
    value for the minimum number of snapshots to keep
    ``minSnapshotsToKeep``.
    """

    minSnapshotsToKeep: PositiveInteger | None
    maxSnapshotAgeHours: PositiveInteger | None


class IcebergCompactionSettings(TypedDict, total=False):
    """Contains details about the compaction settings for an Iceberg table."""

    targetFileSizeMB: PositiveInteger | None
    strategy: IcebergCompactionStrategy | None


class TableMaintenanceSettings(TypedDict, total=False):
    """Contains details about maintenance settings for the table."""

    icebergCompaction: IcebergCompactionSettings | None
    icebergSnapshotManagement: IcebergSnapshotManagementSettings | None


class TableMaintenanceConfigurationValue(TypedDict, total=False):
    """The values that define a maintenance configuration for a table."""

    status: MaintenanceStatus | None
    settings: TableMaintenanceSettings | None


TableMaintenanceConfiguration = dict[TableMaintenanceType, TableMaintenanceConfigurationValue]


class GetTableMaintenanceConfigurationResponse(TypedDict, total=False):
    tableARN: TableARN
    configuration: TableMaintenanceConfiguration


class GetTableMaintenanceJobStatusRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    namespace: NamespaceName
    name: TableName


class TableMaintenanceJobStatusValue(TypedDict, total=False):
    """Details about the status of a maintenance job."""

    status: JobStatus
    lastRunTimestamp: SyntheticTimestamp_date_time | None
    failureMessage: String | None


TableMaintenanceJobStatus = dict[TableMaintenanceJobType, TableMaintenanceJobStatusValue]


class GetTableMaintenanceJobStatusResponse(TypedDict, total=False):
    tableARN: TableARN
    status: TableMaintenanceJobStatus


class GetTableMetadataLocationRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    namespace: NamespaceName
    name: TableName


class GetTableMetadataLocationResponse(TypedDict, total=False):
    versionToken: VersionToken
    metadataLocation: MetadataLocation | None
    warehouseLocation: WarehouseLocation


class GetTablePolicyRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    namespace: NamespaceName
    name: TableName


class GetTablePolicyResponse(TypedDict, total=False):
    resourcePolicy: ResourcePolicy


class GetTableRecordExpirationConfigurationRequest(ServiceRequest):
    tableArn: TableARN


class TableRecordExpirationSettings(TypedDict, total=False):
    """The record expiration setting that specifies when records expire and are
    automatically removed from a table.
    """

    days: PositiveInteger | None


class TableRecordExpirationConfigurationValue(TypedDict, total=False):
    """The expiration configuration settings for records in a table, and the
    status of the configuration. If the status of the configuration is
    enabled, records expire and are automatically removed after the number
    of days specified in the record expiration settings for the table.
    """

    status: TableRecordExpirationStatus | None
    settings: TableRecordExpirationSettings | None


class GetTableRecordExpirationConfigurationResponse(TypedDict, total=False):
    configuration: TableRecordExpirationConfigurationValue


class GetTableRecordExpirationJobStatusRequest(ServiceRequest):
    tableArn: TableARN


Long = int


class TableRecordExpirationJobMetrics(TypedDict, total=False):
    """Provides metrics for the record expiration job that most recently ran
    for a table. The metrics provide insight into the amount of data that
    was removed when the job ran.
    """

    deletedDataFiles: Long | None
    deletedRecords: Long | None
    removedFilesSize: Long | None


class GetTableRecordExpirationJobStatusResponse(TypedDict, total=False):
    status: TableRecordExpirationJobStatus
    lastRunTimestamp: SyntheticTimestamp_date_time | None
    failureMessage: String | None
    metrics: TableRecordExpirationJobMetrics | None


class GetTableReplicationRequest(ServiceRequest):
    tableArn: TableARN


class TableReplicationRule(TypedDict, total=False):
    """Defines a rule for replicating a table to one or more destination
    tables.
    """

    destinations: ReplicationDestinations


TableReplicationRules = list[TableReplicationRule]


class TableReplicationConfiguration(TypedDict, total=False):
    """The replication configuration for an individual table. This
    configuration defines how the table is replicated to destination tables.
    """

    role: IAMRole
    rules: TableReplicationRules


class GetTableReplicationResponse(TypedDict, total=False):
    versionToken: String
    configuration: TableReplicationConfiguration


class GetTableReplicationStatusRequest(ServiceRequest):
    tableArn: TableARN


class LastSuccessfulReplicatedUpdate(TypedDict, total=False):
    """Contains information about the most recent successful replication update
    to a destination.
    """

    metadataLocation: MetadataLocation
    timestamp: SyntheticTimestamp_date_time


class ReplicationDestinationStatusModel(TypedDict, total=False):
    """Contains status information for a replication destination, including the
    current replication state, last successful update, and any error
    messages.
    """

    replicationStatus: ReplicationStatus
    destinationTableBucketArn: TableBucketARN
    destinationTableArn: TableARN | None
    lastSuccessfulReplicatedUpdate: LastSuccessfulReplicatedUpdate | None
    failureMessage: String | None


ReplicationDestinationStatuses = list[ReplicationDestinationStatusModel]


class GetTableReplicationStatusResponse(TypedDict, total=False):
    sourceTableArn: TableARN
    destinations: ReplicationDestinationStatuses


class GetTableRequest(ServiceRequest):
    tableBucketARN: TableBucketARN | None
    namespace: NamespaceName | None
    name: TableName | None
    tableArn: TableARN | None


class ReplicationInformation(TypedDict, total=False):
    """Contains information about the source of a replicated table."""

    sourceTableARN: TableARN


class ManagedTableInformation(TypedDict, total=False):
    """Contains information about tables that are managed by S3 Tables,
    including replication information for replica tables.
    """

    replicationInformation: ReplicationInformation | None


class GetTableResponse(TypedDict, total=False):
    name: TableName
    type: TableType
    tableARN: TableARN
    namespace: NamespaceList
    namespaceId: NamespaceId | None
    versionToken: VersionToken
    metadataLocation: MetadataLocation | None
    warehouseLocation: WarehouseLocation
    createdAt: SyntheticTimestamp_date_time
    createdBy: AccountId
    managedByService: String | None
    modifiedAt: SyntheticTimestamp_date_time
    modifiedBy: AccountId
    ownerAccountId: AccountId
    format: OpenTableFormat
    tableBucketId: TableBucketId | None
    managedTableInformation: ManagedTableInformation | None


class GetTableStorageClassRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    namespace: NamespaceName
    name: TableName


class GetTableStorageClassResponse(TypedDict, total=False):
    storageClassConfiguration: StorageClassConfiguration


class ListNamespacesRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    prefix: ListNamespacesRequestPrefixString | None
    continuationToken: NextToken | None
    maxNamespaces: ListNamespacesLimit | None


class NamespaceSummary(TypedDict, total=False):
    """Contains details about a namespace."""

    namespace: NamespaceList
    createdAt: SyntheticTimestamp_date_time
    createdBy: AccountId
    ownerAccountId: AccountId
    namespaceId: NamespaceId | None
    tableBucketId: TableBucketId | None


NamespaceSummaryList = list[NamespaceSummary]


class ListNamespacesResponse(TypedDict, total=False):
    namespaces: NamespaceSummaryList
    continuationToken: NextToken | None


class ListTableBucketsRequest(TypedDict, total=False):
    prefix: ListTableBucketsRequestPrefixString | None
    continuationToken: NextToken | None
    maxBuckets: ListTableBucketsLimit | None
    type: TableBucketType | None


class TableBucketSummary(TypedDict, total=False):
    arn: TableBucketARN
    name: TableBucketName
    ownerAccountId: AccountId
    createdAt: SyntheticTimestamp_date_time
    tableBucketId: TableBucketId | None
    type: TableBucketType | None


TableBucketSummaryList = list[TableBucketSummary]


class ListTableBucketsResponse(TypedDict, total=False):
    tableBuckets: TableBucketSummaryList
    continuationToken: NextToken | None


class ListTablesRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    namespace: NamespaceName | None
    prefix: ListTablesRequestPrefixString | None
    continuationToken: NextToken | None
    maxTables: ListTablesLimit | None


class TableSummary(TypedDict, total=False):
    namespace: NamespaceList
    name: TableName
    type: TableType
    tableARN: TableARN
    createdAt: SyntheticTimestamp_date_time
    modifiedAt: SyntheticTimestamp_date_time
    managedByService: String | None
    namespaceId: NamespaceId | None
    tableBucketId: TableBucketId | None


TableSummaryList = list[TableSummary]


class ListTablesResponse(TypedDict, total=False):
    tables: TableSummaryList
    continuationToken: NextToken | None


class ListTagsForResourceRequest(ServiceRequest):
    resourceArn: ResourceArn


class ListTagsForResourceResponse(TypedDict, total=False):
    tags: Tags | None


class PutTableBucketEncryptionRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    encryptionConfiguration: EncryptionConfiguration


class PutTableBucketMaintenanceConfigurationRequest(TypedDict, total=False):
    tableBucketARN: TableBucketARN
    type: TableBucketMaintenanceType
    value: TableBucketMaintenanceConfigurationValue


class PutTableBucketMetricsConfigurationRequest(ServiceRequest):
    tableBucketARN: TableBucketARN


class PutTableBucketPolicyRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    resourcePolicy: ResourcePolicy


class PutTableBucketReplicationRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    versionToken: VersionToken | None
    configuration: TableBucketReplicationConfiguration


class PutTableBucketReplicationResponse(TypedDict, total=False):
    versionToken: VersionToken
    status: String


class PutTableBucketStorageClassRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    storageClassConfiguration: StorageClassConfiguration


class PutTableMaintenanceConfigurationRequest(TypedDict, total=False):
    tableBucketARN: TableBucketARN
    namespace: NamespaceName
    name: TableName
    type: TableMaintenanceType
    value: TableMaintenanceConfigurationValue


class PutTablePolicyRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    namespace: NamespaceName
    name: TableName
    resourcePolicy: ResourcePolicy


class PutTableRecordExpirationConfigurationRequest(ServiceRequest):
    tableArn: TableARN
    value: TableRecordExpirationConfigurationValue


class PutTableReplicationRequest(ServiceRequest):
    tableArn: TableARN
    versionToken: String | None
    configuration: TableReplicationConfiguration


class PutTableReplicationResponse(TypedDict, total=False):
    versionToken: String
    status: String


class RenameTableRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    namespace: NamespaceName
    name: TableName
    newNamespaceName: NamespaceName | None
    newName: TableName | None
    versionToken: VersionToken | None


TagKeyList = list[TagKey]


class TagResourceRequest(ServiceRequest):
    resourceArn: ResourceArn
    tags: Tags


class TagResourceResponse(TypedDict, total=False):
    pass


class UntagResourceRequest(ServiceRequest):
    resourceArn: ResourceArn
    tagKeys: TagKeyList


class UntagResourceResponse(TypedDict, total=False):
    pass


class UpdateTableMetadataLocationRequest(ServiceRequest):
    tableBucketARN: TableBucketARN
    namespace: NamespaceName
    name: TableName
    versionToken: VersionToken
    metadataLocation: MetadataLocation


class UpdateTableMetadataLocationResponse(TypedDict, total=False):
    name: TableName
    tableARN: TableARN
    namespace: NamespaceList
    versionToken: VersionToken
    metadataLocation: MetadataLocation


class S3TablesApi:
    service: str = "s3tables"
    version: str = "2018-05-10"

    @handler("CreateNamespace")
    def create_namespace(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        namespace: CreateNamespaceRequestNamespaceList,
        **kwargs,
    ) -> CreateNamespaceResponse:
        """Creates a namespace. A namespace is a logical grouping of tables within
        your table bucket, which you can use to organize tables. For more
        information, see `Create a
        namespace <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-namespace-create.html>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           You must have the ``s3tables:CreateNamespace`` permission to use this
           operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket to create the
        namespace in.
        :param namespace: A name for the namespace.
        :returns: CreateNamespaceResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("CreateTable")
    def create_table(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        namespace: NamespaceName,
        name: TableName,
        format: OpenTableFormat,
        metadata: TableMetadata | None = None,
        encryption_configuration: EncryptionConfiguration | None = None,
        storage_class_configuration: StorageClassConfiguration | None = None,
        tags: Tags | None = None,
        **kwargs,
    ) -> CreateTableResponse:
        """Creates a new table associated with the given namespace in a table
        bucket. For more information, see `Creating an Amazon S3
        table <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-create.html>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           -  You must have the ``s3tables:CreateTable`` permission to use this
              operation.

           -  If you use this operation with the optional ``metadata`` request
              parameter you must have the ``s3tables:PutTableData`` permission.

           -  If you use this operation with the optional
              ``encryptionConfiguration`` request parameter you must have the
              ``s3tables:PutTableEncryption`` permission.

           -  If you use this operation with the ``storageClassConfiguration``
              request parameter, you must have the
              ``s3tables:PutTableStorageClass`` permission.

           -  To create a table with tags, you must have the
              ``s3tables:TagResource`` permission in addition to
              ``s3tables:CreateTable`` permission.

           Additionally, If you choose SSE-KMS encryption you must grant the S3
           Tables maintenance principal access to your KMS key. For more
           information, see `Permissions requirements for S3 Tables SSE-KMS
           encryption <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-kms-permissions.html>`__.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket to create the table
        in.
        :param namespace: The namespace to associated with the table.
        :param name: The name for the table.
        :param format: The format for the table.
        :param metadata: The metadata for the table.
        :param encryption_configuration: The encryption configuration to use for the table.
        :param storage_class_configuration: The storage class configuration for the table.
        :param tags: A map of user-defined tags that you would like to apply to the table
        that you are creating.
        :returns: CreateTableResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("CreateTableBucket")
    def create_table_bucket(
        self,
        context: RequestContext,
        name: TableBucketName,
        encryption_configuration: EncryptionConfiguration | None = None,
        storage_class_configuration: StorageClassConfiguration | None = None,
        tags: Tags | None = None,
        **kwargs,
    ) -> CreateTableBucketResponse:
        """Creates a table bucket. For more information, see `Creating a table
        bucket <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-buckets-create.html>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           -  You must have the ``s3tables:CreateTableBucket`` permission to use
              this operation.

           -  If you use this operation with the optional
              ``encryptionConfiguration`` parameter you must have the
              ``s3tables:PutTableBucketEncryption`` permission.

           -  If you use this operation with the ``storageClassConfiguration``
              request parameter, you must have the
              ``s3tables:PutTableBucketStorageClass`` permission.

           -  To create a table bucket with tags, you must have the
              ``s3tables:TagResource`` permission in addition to
              ``s3tables:CreateTableBucket`` permission.

        :param name: The name for the table bucket.
        :param encryption_configuration: The encryption configuration to use for the table bucket.
        :param storage_class_configuration: The default storage class configuration for the table bucket.
        :param tags: A map of user-defined tags that you would like to apply to the table
        bucket that you are creating.
        :returns: CreateTableBucketResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("DeleteNamespace")
    def delete_namespace(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        namespace: NamespaceName,
        **kwargs,
    ) -> None:
        """Deletes a namespace. For more information, see `Delete a
        namespace <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-namespace-delete.html>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           You must have the ``s3tables:DeleteNamespace`` permission to use this
           operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket associated with the
        namespace.
        :param namespace: The name of the namespace.
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("DeleteTable")
    def delete_table(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        namespace: NamespaceName,
        name: TableName,
        version_token: VersionToken | None = None,
        **kwargs,
    ) -> None:
        """Deletes a table. For more information, see `Deleting an Amazon S3
        table <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-delete.html>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           You must have the ``s3tables:DeleteTable`` permission to use this
           operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket that contains the
        table.
        :param namespace: The namespace associated with the table.
        :param name: The name of the table.
        :param version_token: The version token of the table.
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("DeleteTableBucket")
    def delete_table_bucket(
        self, context: RequestContext, table_bucket_arn: TableBucketARN, **kwargs
    ) -> None:
        """Deletes a table bucket. For more information, see `Deleting a table
        bucket <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-buckets-delete.html>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           You must have the ``s3tables:DeleteTableBucket`` permission to use
           this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("DeleteTableBucketEncryption")
    def delete_table_bucket_encryption(
        self, context: RequestContext, table_bucket_arn: TableBucketARN, **kwargs
    ) -> None:
        """Deletes the encryption configuration for a table bucket.

        Permissions
           You must have the ``s3tables:DeleteTableBucketEncryption`` permission
           to use this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("DeleteTableBucketMetricsConfiguration")
    def delete_table_bucket_metrics_configuration(
        self, context: RequestContext, table_bucket_arn: TableBucketARN, **kwargs
    ) -> None:
        """Deletes the metrics configuration for a table bucket.

        Permissions
           You must have the ``s3tables:DeleteTableBucketMetricsConfiguration``
           permission to use this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("DeleteTableBucketPolicy")
    def delete_table_bucket_policy(
        self, context: RequestContext, table_bucket_arn: TableBucketARN, **kwargs
    ) -> None:
        """Deletes a table bucket policy. For more information, see `Deleting a
        table bucket
        policy <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-bucket-policy.html#table-bucket-policy-delete>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           You must have the ``s3tables:DeleteTableBucketPolicy`` permission to
           use this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("DeleteTableBucketReplication")
    def delete_table_bucket_replication(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        version_token: VersionToken | None = None,
        **kwargs,
    ) -> None:
        """Deletes the replication configuration for a table bucket. After
        deletion, new table updates will no longer be replicated to destination
        buckets, though existing replicated tables will remain in destination
        buckets.

        Permissions
           You must have the ``s3tables:DeleteTableBucketReplication``
           permission to use this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :param version_token: A version token from a previous GetTableBucketReplication call.
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises AccessDeniedException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("DeleteTablePolicy")
    def delete_table_policy(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        namespace: NamespaceName,
        name: TableName,
        **kwargs,
    ) -> None:
        """Deletes a table policy. For more information, see `Deleting a table
        policy <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-table-policy.html#table-policy-delete>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           You must have the ``s3tables:DeleteTablePolicy`` permission to use
           this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket that contains the
        table.
        :param namespace: The namespace associated with the table.
        :param name: The table name.
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("DeleteTableReplication")
    def delete_table_replication(
        self, context: RequestContext, table_arn: TableARN, version_token: String, **kwargs
    ) -> None:
        """Deletes the replication configuration for a specific table. After
        deletion, new updates to this table will no longer be replicated to
        destination tables, though existing replicated copies will remain in
        destination buckets.

        Permissions
           You must have the ``s3tables:DeleteTableReplication`` permission to
           use this operation.

        :param table_arn: The Amazon Resource Name (ARN) of the table.
        :param version_token: A version token from a previous GetTableReplication call.
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises AccessDeniedException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetNamespace")
    def get_namespace(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        namespace: NamespaceName,
        **kwargs,
    ) -> GetNamespaceResponse:
        """Gets details about a namespace. For more information, see `Table
        namespaces <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-namespace.html>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           You must have the ``s3tables:GetNamespace`` permission to use this
           operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :param namespace: The name of the namespace.
        :returns: GetNamespaceResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises AccessDeniedException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetTable")
    def get_table(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN | None = None,
        namespace: NamespaceName | None = None,
        name: TableName | None = None,
        table_arn: TableARN | None = None,
        **kwargs,
    ) -> GetTableResponse:
        """Gets details about a table. For more information, see `S3
        Tables <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-tables.html>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           You must have the ``s3tables:GetTable`` permission to use this
           operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket associated with the
        table.
        :param namespace: The name of the namespace the table is associated with.
        :param name: The name of the table.
        :param table_arn: The Amazon Resource Name (ARN) of the table.
        :returns: GetTableResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises AccessDeniedException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetTableBucket")
    def get_table_bucket(
        self, context: RequestContext, table_bucket_arn: TableBucketARN, **kwargs
    ) -> GetTableBucketResponse:
        """Gets details on a table bucket. For more information, see `Viewing
        details about an Amazon S3 table
        bucket <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-buckets-details.html>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           You must have the ``s3tables:GetTableBucket`` permission to use this
           operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :returns: GetTableBucketResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises AccessDeniedException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetTableBucketEncryption")
    def get_table_bucket_encryption(
        self, context: RequestContext, table_bucket_arn: TableBucketARN, **kwargs
    ) -> GetTableBucketEncryptionResponse:
        """Gets the encryption configuration for a table bucket.

        Permissions
           You must have the ``s3tables:GetTableBucketEncryption`` permission to
           use this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :returns: GetTableBucketEncryptionResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises AccessDeniedException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetTableBucketMaintenanceConfiguration")
    def get_table_bucket_maintenance_configuration(
        self, context: RequestContext, table_bucket_arn: TableBucketARN, **kwargs
    ) -> GetTableBucketMaintenanceConfigurationResponse:
        """Gets details about a maintenance configuration for a given table bucket.
        For more information, see `Amazon S3 table bucket
        maintenance <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-table-buckets-maintenance.html>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           You must have the ``s3tables:GetTableBucketMaintenanceConfiguration``
           permission to use this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket associated with the
        maintenance configuration.
        :returns: GetTableBucketMaintenanceConfigurationResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetTableBucketMetricsConfiguration")
    def get_table_bucket_metrics_configuration(
        self, context: RequestContext, table_bucket_arn: TableBucketARN, **kwargs
    ) -> GetTableBucketMetricsConfigurationResponse:
        """Gets the metrics configuration for a table bucket.

        Permissions
           You must have the ``s3tables:GetTableBucketMetricsConfiguration``
           permission to use this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :returns: GetTableBucketMetricsConfigurationResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetTableBucketPolicy")
    def get_table_bucket_policy(
        self, context: RequestContext, table_bucket_arn: TableBucketARN, **kwargs
    ) -> GetTableBucketPolicyResponse:
        """Gets details about a table bucket policy. For more information, see
        `Viewing a table bucket
        policy <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-bucket-policy.html#table-bucket-policy-get>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           You must have the ``s3tables:GetTableBucketPolicy`` permission to use
           this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :returns: GetTableBucketPolicyResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetTableBucketReplication")
    def get_table_bucket_replication(
        self, context: RequestContext, table_bucket_arn: TableBucketARN, **kwargs
    ) -> GetTableBucketReplicationResponse:
        """Retrieves the replication configuration for a table bucket.This
        operation returns the IAM role, ``versionToken``, and replication rules
        that define how tables in this bucket are replicated to other buckets.

        Permissions
           You must have the ``s3tables:GetTableBucketReplication`` permission
           to use this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :returns: GetTableBucketReplicationResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises AccessDeniedException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetTableBucketStorageClass")
    def get_table_bucket_storage_class(
        self, context: RequestContext, table_bucket_arn: TableBucketARN, **kwargs
    ) -> GetTableBucketStorageClassResponse:
        """Retrieves the storage class configuration for a specific table. This
        allows you to view the storage class settings that apply to an
        individual table, which may differ from the table bucket's default
        configuration.

        Permissions
           You must have the ``s3tables:GetTableBucketStorageClass`` permission
           to use this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :returns: GetTableBucketStorageClassResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises AccessDeniedException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetTableEncryption")
    def get_table_encryption(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        namespace: NamespaceName,
        name: TableName,
        **kwargs,
    ) -> GetTableEncryptionResponse:
        """Gets the encryption configuration for a table.

        Permissions
           You must have the ``s3tables:GetTableEncryption`` permission to use
           this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket containing the table.
        :param namespace: The namespace associated with the table.
        :param name: The name of the table.
        :returns: GetTableEncryptionResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises AccessDeniedException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetTableMaintenanceConfiguration")
    def get_table_maintenance_configuration(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        namespace: NamespaceName,
        name: TableName,
        **kwargs,
    ) -> GetTableMaintenanceConfigurationResponse:
        """Gets details about the maintenance configuration of a table. For more
        information, see `S3 Tables
        maintenance <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-maintenance.html>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           -  You must have the ``s3tables:GetTableMaintenanceConfiguration``
              permission to use this operation.

           -  You must have the ``s3tables:GetTableData`` permission to use set
              the compaction strategy to ``sort`` or ``zorder``.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :param namespace: The namespace associated with the table.
        :param name: The name of the table.
        :returns: GetTableMaintenanceConfigurationResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetTableMaintenanceJobStatus")
    def get_table_maintenance_job_status(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        namespace: NamespaceName,
        name: TableName,
        **kwargs,
    ) -> GetTableMaintenanceJobStatusResponse:
        """Gets the status of a maintenance job for a table. For more information,
        see `S3 Tables
        maintenance <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-maintenance.html>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           You must have the ``s3tables:GetTableMaintenanceJobStatus``
           permission to use this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :param namespace: The name of the namespace the table is associated with.
        :param name: The name of the table containing the maintenance job status you want to
        check.
        :returns: GetTableMaintenanceJobStatusResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetTableMetadataLocation")
    def get_table_metadata_location(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        namespace: NamespaceName,
        name: TableName,
        **kwargs,
    ) -> GetTableMetadataLocationResponse:
        """Gets the location of the table metadata.

        Permissions
           You must have the ``s3tables:GetTableMetadataLocation`` permission to
           use this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :param namespace: The namespace of the table.
        :param name: The name of the table.
        :returns: GetTableMetadataLocationResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetTablePolicy")
    def get_table_policy(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        namespace: NamespaceName,
        name: TableName,
        **kwargs,
    ) -> GetTablePolicyResponse:
        """Gets details about a table policy. For more information, see `Viewing a
        table
        policy <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-table-policy.html#table-policy-get>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           You must have the ``s3tables:GetTablePolicy`` permission to use this
           operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket that contains the
        table.
        :param namespace: The namespace associated with the table.
        :param name: The name of the table.
        :returns: GetTablePolicyResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetTableRecordExpirationConfiguration")
    def get_table_record_expiration_configuration(
        self, context: RequestContext, table_arn: TableARN, **kwargs
    ) -> GetTableRecordExpirationConfigurationResponse:
        """Retrieves the expiration configuration settings for records in a table,
        and the status of the configuration. If the status of the configuration
        is ``enabled``, records expire and are automatically removed from the
        table after the specified number of days.

        Permissions
           You must have the ``s3tables:GetTableRecordExpirationConfiguration``
           permission to use this operation.

        :param table_arn: The Amazon Resource Name (ARN) of the table.
        :returns: GetTableRecordExpirationConfigurationResponse
        :raises InternalServerErrorException:
        :raises MethodNotAllowedException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetTableRecordExpirationJobStatus")
    def get_table_record_expiration_job_status(
        self, context: RequestContext, table_arn: TableARN, **kwargs
    ) -> GetTableRecordExpirationJobStatusResponse:
        """Retrieves the status, metrics, and details of the latest record
        expiration job for a table. This includes when the job ran, and whether
        it succeeded or failed. If the job ran successfully, this also includes
        statistics about the records that were removed.

        Permissions
           You must have the ``s3tables:GetTableRecordExpirationJobStatus``
           permission to use this operation.

        :param table_arn: The Amazon Resource Name (ARN) of the table.
        :returns: GetTableRecordExpirationJobStatusResponse
        :raises InternalServerErrorException:
        :raises MethodNotAllowedException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetTableReplication")
    def get_table_replication(
        self, context: RequestContext, table_arn: TableARN, **kwargs
    ) -> GetTableReplicationResponse:
        """Retrieves the replication configuration for a specific table.

        Permissions
           You must have the ``s3tables:GetTableReplication`` permission to use
           this operation.

        :param table_arn: The Amazon Resource Name (ARN) of the table.
        :returns: GetTableReplicationResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises AccessDeniedException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetTableReplicationStatus")
    def get_table_replication_status(
        self, context: RequestContext, table_arn: TableARN, **kwargs
    ) -> GetTableReplicationStatusResponse:
        """Retrieves the replication status for a table, including the status of
        replication to each destination. This operation provides visibility into
        replication health and progress.

        Permissions
           You must have the ``s3tables:GetTableReplicationStatus`` permission
           to use this operation.

        :param table_arn: The Amazon Resource Name (ARN) of the table.
        :returns: GetTableReplicationStatusResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetTableStorageClass")
    def get_table_storage_class(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        namespace: NamespaceName,
        name: TableName,
        **kwargs,
    ) -> GetTableStorageClassResponse:
        """Retrieves the storage class configuration for a specific table. This
        allows you to view the storage class settings that apply to an
        individual table, which may differ from the table bucket's default
        configuration.

        Permissions
           You must have the ``s3tables:GetTableStorageClass`` permission to use
           this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket that contains the
        table.
        :param namespace: The namespace associated with the table.
        :param name: The name of the table.
        :returns: GetTableStorageClassResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises AccessDeniedException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("ListNamespaces")
    def list_namespaces(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        prefix: ListNamespacesRequestPrefixString | None = None,
        continuation_token: NextToken | None = None,
        max_namespaces: ListNamespacesLimit | None = None,
        **kwargs,
    ) -> ListNamespacesResponse:
        """Lists the namespaces within a table bucket. For more information, see
        `Table
        namespaces <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-namespace.html>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           You must have the ``s3tables:ListNamespaces`` permission to use this
           operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :param prefix: The prefix of the namespaces.
        :param continuation_token: ``ContinuationToken`` indicates to Amazon S3 that the list is being
        continued on this bucket with a token.
        :param max_namespaces: The maximum number of namespaces to return in the list.
        :returns: ListNamespacesResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises AccessDeniedException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("ListTableBuckets", expand=False)
    def list_table_buckets(
        self, context: RequestContext, request: ListTableBucketsRequest, **kwargs
    ) -> ListTableBucketsResponse:
        """Lists table buckets for your account. For more information, see `S3
        Table
        buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-buckets.html>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           You must have the ``s3tables:ListTableBuckets`` permission to use
           this operation.

        :param prefix: The prefix of the table buckets.
        :param continuation_token: ``ContinuationToken`` indicates to Amazon S3 that the list is being
        continued on this bucket with a token.
        :param max_buckets: The maximum number of table buckets to return in the list.
        :param type: The type of table buckets to filter by in the list.
        :returns: ListTableBucketsResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises AccessDeniedException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("ListTables")
    def list_tables(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        namespace: NamespaceName | None = None,
        prefix: ListTablesRequestPrefixString | None = None,
        continuation_token: NextToken | None = None,
        max_tables: ListTablesLimit | None = None,
        **kwargs,
    ) -> ListTablesResponse:
        """List tables in the given table bucket. For more information, see `S3
        Tables <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-tables.html>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           You must have the ``s3tables:ListTables`` permission to use this
           operation.

        :param table_bucket_arn: The Amazon resource Name (ARN) of the table bucket.
        :param namespace: The namespace of the tables.
        :param prefix: The prefix of the tables.
        :param continuation_token: ``ContinuationToken`` indicates to Amazon S3 that the list is being
        continued on this bucket with a token.
        :param max_tables: The maximum number of tables to return.
        :returns: ListTablesResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("ListTagsForResource")
    def list_tags_for_resource(
        self, context: RequestContext, resource_arn: ResourceArn, **kwargs
    ) -> ListTagsForResourceResponse:
        """Lists all of the tags applied to a specified Amazon S3 Tables resource.
        Each tag is a label consisting of a key and value pair. Tags can help
        you organize, track costs for, and control access to resources.

        For a list of S3 resources that support tagging, see `Managing tags for
        Amazon S3
        resources <https://docs.aws.amazon.com/AmazonS3/latest/userguide/tagging.html#manage-tags>`__.

        Permissions
           For tables and table buckets, you must have the
           ``s3tables:ListTagsForResource`` permission to use this operation.

        :param resource_arn: The Amazon Resource Name (ARN) of the Amazon S3 Tables resource that you
        want to list tags for.
        :returns: ListTagsForResourceResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("PutTableBucketEncryption")
    def put_table_bucket_encryption(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        encryption_configuration: EncryptionConfiguration,
        **kwargs,
    ) -> None:
        """Sets the encryption configuration for a table bucket.

        Permissions
           You must have the ``s3tables:PutTableBucketEncryption`` permission to
           use this operation.

           If you choose SSE-KMS encryption you must grant the S3 Tables
           maintenance principal access to your KMS key. For more information,
           see `Permissions requirements for S3 Tables SSE-KMS
           encryption <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-kms-permissions.html>`__
           in the *Amazon Simple Storage Service User Guide*.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :param encryption_configuration: The encryption configuration to apply to the table bucket.
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("PutTableBucketMaintenanceConfiguration", expand=False)
    def put_table_bucket_maintenance_configuration(
        self,
        context: RequestContext,
        request: PutTableBucketMaintenanceConfigurationRequest,
        **kwargs,
    ) -> None:
        """Creates a new maintenance configuration or replaces an existing
        maintenance configuration for a table bucket. For more information, see
        `Amazon S3 table bucket
        maintenance <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-table-buckets-maintenance.html>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           You must have the ``s3tables:PutTableBucketMaintenanceConfiguration``
           permission to use this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket associated with the
        maintenance configuration.
        :param type: The type of the maintenance configuration.
        :param value: Defines the values of the maintenance configuration for the table
        bucket.
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("PutTableBucketMetricsConfiguration")
    def put_table_bucket_metrics_configuration(
        self, context: RequestContext, table_bucket_arn: TableBucketARN, **kwargs
    ) -> None:
        """Sets the metrics configuration for a table bucket.

        Permissions
           You must have the ``s3tables:PutTableBucketMetricsConfiguration``
           permission to use this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("PutTableBucketPolicy")
    def put_table_bucket_policy(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        resource_policy: ResourcePolicy,
        **kwargs,
    ) -> None:
        """Creates a new table bucket policy or replaces an existing table bucket
        policy for a table bucket. For more information, see `Adding a table
        bucket
        policy <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-bucket-policy.html#table-bucket-policy-add>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           You must have the ``s3tables:PutTableBucketPolicy`` permission to use
           this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :param resource_policy: The ``JSON`` that defines the policy.
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("PutTableBucketReplication")
    def put_table_bucket_replication(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        configuration: TableBucketReplicationConfiguration,
        version_token: VersionToken | None = None,
        **kwargs,
    ) -> PutTableBucketReplicationResponse:
        """Creates or updates the replication configuration for a table bucket.
        This operation defines how tables in the source bucket are replicated to
        destination buckets. Replication helps ensure data availability and
        disaster recovery across regions or accounts.

        Permissions
           -  You must have the ``s3tables:PutTableBucketReplication``
              permission to use this operation. The IAM role specified in the
              configuration must have permissions to read from the source bucket
              and write permissions to all destination buckets.

           -  You must also have the following permissions:

              -  ``s3tables:GetTable`` permission on the source table.

              -  ``s3tables:ListTables`` permission on the bucket containing the
                 table.

              -  ``s3tables:CreateTable`` permission for the destination.

              -  ``s3tables:CreateNamespace`` permission for the destination.

              -  ``s3tables:GetTableMaintenanceConfig`` permission for the
                 source bucket.

              -  ``s3tables:PutTableMaintenanceConfig`` permission for the
                 destination bucket.

           -  You must have ``iam:PassRole`` permission with condition allowing
              roles to be passed to ``replication.s3tables.amazonaws.com``.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the source table bucket.
        :param configuration: The replication configuration to apply, including the IAM role and
        replication rules.
        :param version_token: A version token from a previous GetTableBucketReplication call.
        :returns: PutTableBucketReplicationResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises AccessDeniedException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("PutTableBucketStorageClass")
    def put_table_bucket_storage_class(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        storage_class_configuration: StorageClassConfiguration,
        **kwargs,
    ) -> None:
        """Sets or updates the storage class configuration for a table bucket. This
        configuration serves as the default storage class for all new tables
        created in the bucket, allowing you to optimize storage costs at the
        bucket level.

        Permissions
           You must have the ``s3tables:PutTableBucketStorageClass`` permission
           to use this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :param storage_class_configuration: The storage class configuration to apply to the table bucket.
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("PutTableMaintenanceConfiguration", expand=False)
    def put_table_maintenance_configuration(
        self, context: RequestContext, request: PutTableMaintenanceConfigurationRequest, **kwargs
    ) -> None:
        """Creates a new maintenance configuration or replaces an existing
        maintenance configuration for a table. For more information, see `S3
        Tables
        maintenance <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-maintenance.html>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           You must have the ``s3tables:PutTableMaintenanceConfiguration``
           permission to use this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table associated with the
        maintenance configuration.
        :param namespace: The namespace of the table.
        :param name: The name of the table.
        :param type: The type of the maintenance configuration.
        :param value: Defines the values of the maintenance configuration for the table.
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("PutTablePolicy")
    def put_table_policy(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        namespace: NamespaceName,
        name: TableName,
        resource_policy: ResourcePolicy,
        **kwargs,
    ) -> None:
        """Creates a new table policy or replaces an existing table policy for a
        table. For more information, see `Adding a table
        policy <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-table-policy.html#table-policy-add>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           You must have the ``s3tables:PutTablePolicy`` permission to use this
           operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket that contains the
        table.
        :param namespace: The namespace associated with the table.
        :param name: The name of the table.
        :param resource_policy: The ``JSON`` that defines the policy.
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("PutTableRecordExpirationConfiguration")
    def put_table_record_expiration_configuration(
        self,
        context: RequestContext,
        table_arn: TableARN,
        value: TableRecordExpirationConfigurationValue,
        **kwargs,
    ) -> None:
        """Creates or updates the expiration configuration settings for records in
        a table, including the status of the configuration. If you enable record
        expiration for a table, records expire and are automatically removed
        from the table after the number of days that you specify.

        Permissions
           You must have the ``s3tables:PutTableRecordExpirationConfiguration``
           permission to use this operation.

        :param table_arn: The Amazon Resource Name (ARN) of the table.
        :param value: The record expiration configuration to apply to the table, including the
        status (``enabled`` or ``disabled``) and retention period in days.
        :raises InternalServerErrorException:
        :raises MethodNotAllowedException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("PutTableReplication")
    def put_table_replication(
        self,
        context: RequestContext,
        table_arn: TableARN,
        configuration: TableReplicationConfiguration,
        version_token: String | None = None,
        **kwargs,
    ) -> PutTableReplicationResponse:
        """Creates or updates the replication configuration for a specific table.
        This operation allows you to define table-level replication
        independently of bucket-level replication, providing granular control
        over which tables are replicated and where.

        Permissions
           -  You must have the ``s3tables:PutTableReplication`` permission to
              use this operation. The IAM role specified in the configuration
              must have permissions to read from the source table and write to
              all destination tables.

           -  You must also have the following permissions:

              -  ``s3tables:GetTable`` permission on the source table being
                 replicated.

              -  ``s3tables:CreateTable`` permission for the destination.

              -  ``s3tables:CreateNamespace`` permission for the destination.

              -  ``s3tables:GetTableMaintenanceConfig`` permission for the
                 source table.

              -  ``s3tables:PutTableMaintenanceConfig`` permission for the
                 destination table.

           -  You must have ``iam:PassRole`` permission with condition allowing
              roles to be passed to ``replication.s3tables.amazonaws.com``.

        :param table_arn: The Amazon Resource Name (ARN) of the source table.
        :param configuration: The replication configuration to apply to the table, including the IAM
        role and replication rules.
        :param version_token: A version token from a previous GetTableReplication call.
        :returns: PutTableReplicationResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises AccessDeniedException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("RenameTable")
    def rename_table(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        namespace: NamespaceName,
        name: TableName,
        new_namespace_name: NamespaceName | None = None,
        new_name: TableName | None = None,
        version_token: VersionToken | None = None,
        **kwargs,
    ) -> None:
        """Renames a table or a namespace. For more information, see `S3
        Tables <https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-tables.html>`__
        in the *Amazon Simple Storage Service User Guide*.

        Permissions
           You must have the ``s3tables:RenameTable`` permission to use this
           operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :param namespace: The namespace associated with the table.
        :param name: The current name of the table.
        :param new_namespace_name: The new name for the namespace.
        :param new_name: The new name for the table.
        :param version_token: The version token of the table.
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("TagResource")
    def tag_resource(
        self, context: RequestContext, resource_arn: ResourceArn, tags: Tags, **kwargs
    ) -> TagResourceResponse:
        """Applies one or more user-defined tags to an Amazon S3 Tables resource or
        updates existing tags. Each tag is a label consisting of a key and value
        pair. Tags can help you organize, track costs for, and control access to
        your resources. You can add up to 50 tags for each S3 resource.

        For a list of S3 resources that support tagging, see `Managing tags for
        Amazon S3
        resources <https://docs.aws.amazon.com/AmazonS3/latest/userguide/tagging.html#manage-tags>`__.

        Permissions
           For tables and table buckets, you must have the
           ``s3tables:TagResource`` permission to use this operation.

        :param resource_arn: The Amazon Resource Name (ARN) of the Amazon S3 Tables resource that
        you're applying tags to.
        :param tags: The user-defined tag that you want to add to the specified S3 Tables
        resource.
        :returns: TagResourceResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("UntagResource")
    def untag_resource(
        self, context: RequestContext, resource_arn: ResourceArn, tag_keys: TagKeyList, **kwargs
    ) -> UntagResourceResponse:
        """Removes the specified user-defined tags from an Amazon S3 Tables
        resource. You can pass one or more tag keys.

        For a list of S3 resources that support tagging, see `Managing tags for
        Amazon S3
        resources <https://docs.aws.amazon.com/AmazonS3/latest/userguide/tagging.html#manage-tags>`__.

        Permissions
           For tables and table buckets, you must have the
           ``s3tables:UntagResource`` permission to use this operation.

        :param resource_arn: The Amazon Resource Name (ARN) of the Amazon S3 Tables resource that
        you're removing tags from.
        :param tag_keys: The array of tag keys that you're removing from the S3 Tables resource.
        :returns: UntagResourceResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("UpdateTableMetadataLocation")
    def update_table_metadata_location(
        self,
        context: RequestContext,
        table_bucket_arn: TableBucketARN,
        namespace: NamespaceName,
        name: TableName,
        version_token: VersionToken,
        metadata_location: MetadataLocation,
        **kwargs,
    ) -> UpdateTableMetadataLocationResponse:
        """Updates the metadata location for a table. The metadata location of a
        table must be an S3 URI that begins with the table's warehouse location.
        The metadata location for an Apache Iceberg table must end with
        ``.metadata.json``, or if the metadata file is Gzip-compressed,
        ``.metadata.json.gz``.

        Permissions
           You must have the ``s3tables:UpdateTableMetadataLocation`` permission
           to use this operation.

        :param table_bucket_arn: The Amazon Resource Name (ARN) of the table bucket.
        :param namespace: The namespace of the table.
        :param name: The name of the table.
        :param version_token: The version token of the table.
        :param metadata_location: The new metadata location for the table.
        :returns: UpdateTableMetadataLocationResponse
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        :raises BadRequestException:
        """
        raise NotImplementedError
