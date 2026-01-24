from datetime import datetime
from enum import StrEnum
from typing import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

ActivityBatchSize = int
ActivityName = str
AttributeName = str
BucketKeyExpression = str
BucketName = str
ChannelArn = str
ChannelName = str
ColumnDataType = str
ColumnName = str
DatasetActionName = str
DatasetArn = str
DatasetContentVersion = str
DatasetName = str
DatastoreArn = str
DatastoreName = str
DoubleValue = float
EntryName = str
ErrorCode = str
ErrorMessage = str
FilterExpression = str
GlueDatabaseName = str
GlueTableName = str
Image = str
IncludeStatisticsFlag = bool
IotEventsInputName = str
LambdaName = str
LateDataRuleName = str
LogResult = str
LoggingEnabled = bool
MathExpression = str
MaxMessages = int
MaxResults = int
MaxVersions = int
MessageId = str
NextToken = str
OffsetSeconds = int
OutputFileName = str
PartitionAttributeName = str
PipelineArn = str
PipelineName = str
PresignedURI = str
Reason = str
ReprocessingId = str
ResourceArn = str
RetentionPeriodInDays = int
RoleArn = str
S3KeyPrefix = str
S3PathChannelMessage = str
ScheduleExpression = str
SessionTimeoutInMinutes = int
SizeInBytes = float
SqlQuery = str
StringValue = str
TagKey = str
TagValue = str
TimeExpression = str
TimestampFormat = str
UnlimitedRetentionPeriod = bool
UnlimitedVersioning = bool
VariableName = str
VolumeSizeInGB = int
errorMessage = str
resourceArn = str
resourceId = str


class ChannelStatus(StrEnum):
    CREATING = "CREATING"
    ACTIVE = "ACTIVE"
    DELETING = "DELETING"


class ComputeType(StrEnum):
    ACU_1 = "ACU_1"
    ACU_2 = "ACU_2"


class DatasetActionType(StrEnum):
    QUERY = "QUERY"
    CONTAINER = "CONTAINER"


class DatasetContentState(StrEnum):
    CREATING = "CREATING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class DatasetStatus(StrEnum):
    CREATING = "CREATING"
    ACTIVE = "ACTIVE"
    DELETING = "DELETING"


class DatastoreStatus(StrEnum):
    CREATING = "CREATING"
    ACTIVE = "ACTIVE"
    DELETING = "DELETING"


class FileFormatType(StrEnum):
    JSON = "JSON"
    PARQUET = "PARQUET"


class LoggingLevel(StrEnum):
    ERROR = "ERROR"


class ReprocessingStatus(StrEnum):
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"


class InternalFailureException(ServiceException):
    """There was an internal failure."""

    code: str = "InternalFailureException"
    sender_fault: bool = False
    status_code: int = 500


class InvalidRequestException(ServiceException):
    """The request was not valid."""

    code: str = "InvalidRequestException"
    sender_fault: bool = False
    status_code: int = 400


class LimitExceededException(ServiceException):
    """The command caused an internal limit to be exceeded."""

    code: str = "LimitExceededException"
    sender_fault: bool = False
    status_code: int = 410


class ResourceAlreadyExistsException(ServiceException):
    """A resource with the same name already exists."""

    code: str = "ResourceAlreadyExistsException"
    sender_fault: bool = False
    status_code: int = 409
    resourceId: resourceId | None
    resourceArn: resourceArn | None


class ResourceNotFoundException(ServiceException):
    """A resource with the specified name could not be found."""

    code: str = "ResourceNotFoundException"
    sender_fault: bool = False
    status_code: int = 404


class ServiceUnavailableException(ServiceException):
    """The service is temporarily unavailable."""

    code: str = "ServiceUnavailableException"
    sender_fault: bool = False
    status_code: int = 503


class ThrottlingException(ServiceException):
    """The request was denied due to request throttling."""

    code: str = "ThrottlingException"
    sender_fault: bool = False
    status_code: int = 429


AttributeNameMapping = dict[AttributeName, AttributeName]


class AddAttributesActivity(TypedDict, total=False):
    """An activity that adds other attributes based on existing attributes in
    the message.
    """

    name: ActivityName
    attributes: AttributeNameMapping
    next: ActivityName | None


AttributeNames = list[AttributeName]


class BatchPutMessageErrorEntry(TypedDict, total=False):
    """Contains informations about errors."""

    messageId: MessageId | None
    errorCode: ErrorCode | None
    errorMessage: ErrorMessage | None


BatchPutMessageErrorEntries = list[BatchPutMessageErrorEntry]
MessagePayload = bytes


class Message(TypedDict, total=False):
    """Information about a message."""

    messageId: MessageId
    payload: MessagePayload


Messages = list[Message]


class BatchPutMessageRequest(ServiceRequest):
    channelName: ChannelName
    messages: Messages


class BatchPutMessageResponse(TypedDict, total=False):
    batchPutMessageErrorEntries: BatchPutMessageErrorEntries | None


class CancelPipelineReprocessingRequest(ServiceRequest):
    pipelineName: PipelineName
    reprocessingId: ReprocessingId


class CancelPipelineReprocessingResponse(TypedDict, total=False):
    pass


Timestamp = datetime


class RetentionPeriod(TypedDict, total=False):
    """How long, in days, message data is kept."""

    unlimited: UnlimitedRetentionPeriod | None
    numberOfDays: RetentionPeriodInDays | None


class CustomerManagedChannelS3Storage(TypedDict, total=False):
    """Used to store channel data in an S3 bucket that you manage. If
    customer-managed storage is selected, the ``retentionPeriod`` parameter
    is ignored. You can't change the choice of S3 storage after the data
    store is created.
    """

    bucket: BucketName
    keyPrefix: S3KeyPrefix | None
    roleArn: RoleArn


class ServiceManagedChannelS3Storage(TypedDict, total=False):
    """Used to store channel data in an S3 bucket managed by IoT Analytics. You
    can't change the choice of S3 storage after the data store is created.
    """

    pass


class ChannelStorage(TypedDict, total=False):
    """Where channel data is stored. You may choose one of
    ``serviceManagedS3``, ``customerManagedS3`` storage. If not specified,
    the default is ``serviceManagedS3``. This can't be changed after
    creation of the channel.
    """

    serviceManagedS3: ServiceManagedChannelS3Storage | None
    customerManagedS3: CustomerManagedChannelS3Storage | None


class Channel(TypedDict, total=False):
    """A collection of data from an MQTT topic. Channels archive the raw,
    unprocessed messages before publishing the data to a pipeline.
    """

    name: ChannelName | None
    storage: ChannelStorage | None
    arn: ChannelArn | None
    status: ChannelStatus | None
    retentionPeriod: RetentionPeriod | None
    creationTime: Timestamp | None
    lastUpdateTime: Timestamp | None
    lastMessageArrivalTime: Timestamp | None


class ChannelActivity(TypedDict, total=False):
    """The activity that determines the source of the messages to be processed."""

    name: ActivityName
    channelName: ChannelName
    next: ActivityName | None


S3PathChannelMessages = list[S3PathChannelMessage]


class ChannelMessages(TypedDict, total=False):
    """Specifies one or more sets of channel messages."""

    s3Paths: S3PathChannelMessages | None


class EstimatedResourceSize(TypedDict, total=False):
    """The estimated size of the resource."""

    estimatedSizeInBytes: SizeInBytes | None
    estimatedOn: Timestamp | None


class ChannelStatistics(TypedDict, total=False):
    """Statistics information about the channel."""

    size: EstimatedResourceSize | None


class CustomerManagedChannelS3StorageSummary(TypedDict, total=False):
    """Used to store channel data in an S3 bucket that you manage."""

    bucket: BucketName | None
    keyPrefix: S3KeyPrefix | None
    roleArn: RoleArn | None


class ServiceManagedChannelS3StorageSummary(TypedDict, total=False):
    """Used to store channel data in an S3 bucket managed by IoT Analytics."""

    pass


class ChannelStorageSummary(TypedDict, total=False):
    """Where channel data is stored."""

    serviceManagedS3: ServiceManagedChannelS3StorageSummary | None
    customerManagedS3: CustomerManagedChannelS3StorageSummary | None


class ChannelSummary(TypedDict, total=False):
    """A summary of information about a channel."""

    channelName: ChannelName | None
    channelStorage: ChannelStorageSummary | None
    status: ChannelStatus | None
    creationTime: Timestamp | None
    lastUpdateTime: Timestamp | None
    lastMessageArrivalTime: Timestamp | None


ChannelSummaries = list[ChannelSummary]


class Column(TypedDict, total=False):
    name: ColumnName
    type: ColumnDataType


Columns = list[Column]


class OutputFileUriValue(TypedDict, total=False):
    """The value of the variable as a structure that specifies an output file
    URI.
    """

    fileName: OutputFileName


class DatasetContentVersionValue(TypedDict, total=False):
    """The dataset whose latest contents are used as input to the notebook or
    application.
    """

    datasetName: DatasetName


class Variable(TypedDict, total=False):
    """An instance of a variable to be passed to the ``containerAction``
    execution. Each variable must have a name and a value given by one of
    ``stringValue``, ``datasetContentVersionValue``, or
    ``outputFileUriValue``.
    """

    name: VariableName
    stringValue: StringValue | None
    doubleValue: DoubleValue | None
    datasetContentVersionValue: DatasetContentVersionValue | None
    outputFileUriValue: OutputFileUriValue | None


Variables = list[Variable]


class ResourceConfiguration(TypedDict, total=False):
    """The configuration of the resource used to execute the
    ``containerAction``.
    """

    computeType: ComputeType
    volumeSizeInGB: VolumeSizeInGB


class ContainerDatasetAction(TypedDict, total=False):
    """Information required to run the ``containerAction`` to produce dataset
    contents.
    """

    image: Image
    executionRoleArn: RoleArn
    resourceConfiguration: ResourceConfiguration
    variables: Variables | None


class Tag(TypedDict, total=False):
    """A set of key-value pairs that are used to manage the resource."""

    key: TagKey
    value: TagValue


TagList = list[Tag]


class CreateChannelRequest(ServiceRequest):
    channelName: ChannelName
    channelStorage: ChannelStorage | None
    retentionPeriod: RetentionPeriod | None
    tags: TagList | None


class CreateChannelResponse(TypedDict, total=False):
    channelName: ChannelName | None
    channelArn: ChannelArn | None
    retentionPeriod: RetentionPeriod | None


class CreateDatasetContentRequest(ServiceRequest):
    datasetName: DatasetName
    versionId: DatasetContentVersion | None


class CreateDatasetContentResponse(TypedDict, total=False):
    versionId: DatasetContentVersion | None


class DeltaTimeSessionWindowConfiguration(TypedDict, total=False):
    """A structure that contains the configuration information of a delta time
    session window.

    ```DeltaTime`` <https://docs.aws.amazon.com/iotanalytics/latest/APIReference/API_DeltaTime.html>`__
    specifies a time interval. You can use ``DeltaTime`` to create dataset
    contents with data that has arrived in the data store since the last
    execution. For an example of ``DeltaTime``, see `Creating a SQL dataset
    with a delta window
    (CLI) <https://docs.aws.amazon.com/iotanalytics/latest/userguide/automate-create-dataset.html#automate-example6>`__
    in the *IoT Analytics User Guide*.
    """

    timeoutInMinutes: SessionTimeoutInMinutes


class LateDataRuleConfiguration(TypedDict, total=False):
    """The information needed to configure a delta time session window."""

    deltaTimeSessionWindowConfiguration: DeltaTimeSessionWindowConfiguration | None


class LateDataRule(TypedDict, total=False):
    """A structure that contains the name and configuration information of a
    late data rule.
    """

    ruleName: LateDataRuleName | None
    ruleConfiguration: LateDataRuleConfiguration


LateDataRules = list[LateDataRule]


class VersioningConfiguration(TypedDict, total=False):
    """Information about the versioning of dataset contents."""

    unlimited: UnlimitedVersioning | None
    maxVersions: MaxVersions | None


class GlueConfiguration(TypedDict, total=False):
    """Configuration information for coordination with Glue, a fully managed
    extract, transform and load (ETL) service.
    """

    tableName: GlueTableName
    databaseName: GlueDatabaseName


class S3DestinationConfiguration(TypedDict, total=False):
    """Configuration information for delivery of dataset contents to Amazon
    Simple Storage Service (Amazon S3).
    """

    bucket: BucketName
    key: BucketKeyExpression
    glueConfiguration: GlueConfiguration | None
    roleArn: RoleArn


class IotEventsDestinationConfiguration(TypedDict, total=False):
    """Configuration information for delivery of dataset contents to IoT
    Events.
    """

    inputName: IotEventsInputName
    roleArn: RoleArn


class DatasetContentDeliveryDestination(TypedDict, total=False):
    """The destination to which dataset contents are delivered."""

    iotEventsDestinationConfiguration: IotEventsDestinationConfiguration | None
    s3DestinationConfiguration: S3DestinationConfiguration | None


class DatasetContentDeliveryRule(TypedDict, total=False):
    """When dataset contents are created, they are delivered to destination
    specified here.
    """

    entryName: EntryName | None
    destination: DatasetContentDeliveryDestination


DatasetContentDeliveryRules = list[DatasetContentDeliveryRule]


class TriggeringDataset(TypedDict, total=False):
    """Information about the dataset whose content generation triggers the new
    dataset content generation.
    """

    name: DatasetName


class Schedule(TypedDict, total=False):
    """The schedule for when to trigger an update."""

    expression: ScheduleExpression | None


class DatasetTrigger(TypedDict, total=False):
    """The ``DatasetTrigger`` that specifies when the dataset is automatically
    updated.
    """

    schedule: Schedule | None
    dataset: TriggeringDataset | None


DatasetTriggers = list[DatasetTrigger]


class DeltaTime(TypedDict, total=False):
    """Used to limit data to that which has arrived since the last execution of
    the action.
    """

    offsetSeconds: OffsetSeconds
    timeExpression: TimeExpression


class QueryFilter(TypedDict, total=False):
    """Information that is used to filter message data, to segregate it
    according to the timeframe in which it arrives.
    """

    deltaTime: DeltaTime | None


QueryFilters = list[QueryFilter]


class SqlQueryDatasetAction(TypedDict, total=False):
    """The SQL query to modify the message."""

    sqlQuery: SqlQuery
    filters: QueryFilters | None


class DatasetAction(TypedDict, total=False):
    """A ``DatasetAction`` object that specifies how dataset contents are
    automatically created.
    """

    actionName: DatasetActionName | None
    queryAction: SqlQueryDatasetAction | None
    containerAction: ContainerDatasetAction | None


DatasetActions = list[DatasetAction]


class CreateDatasetRequest(ServiceRequest):
    datasetName: DatasetName
    actions: DatasetActions
    triggers: DatasetTriggers | None
    contentDeliveryRules: DatasetContentDeliveryRules | None
    retentionPeriod: RetentionPeriod | None
    versioningConfiguration: VersioningConfiguration | None
    tags: TagList | None
    lateDataRules: LateDataRules | None


class CreateDatasetResponse(TypedDict, total=False):
    datasetName: DatasetName | None
    datasetArn: DatasetArn | None
    retentionPeriod: RetentionPeriod | None


class TimestampPartition(TypedDict, total=False):
    """A partition dimension defined by a timestamp attribute."""

    attributeName: PartitionAttributeName
    timestampFormat: TimestampFormat | None


class Partition(TypedDict, total=False):
    """A partition dimension defined by an attribute."""

    attributeName: PartitionAttributeName


class DatastorePartition(TypedDict, total=False):
    """A single dimension to partition a data store. The dimension must be an
    ``AttributePartition`` or a ``TimestampPartition``.
    """

    attributePartition: Partition | None
    timestampPartition: TimestampPartition | None


Partitions = list[DatastorePartition]


class DatastorePartitions(TypedDict, total=False):
    """Contains information about the partition dimensions in a data store."""

    partitions: Partitions | None


class SchemaDefinition(TypedDict, total=False):
    """Information needed to define a schema."""

    columns: Columns | None


class ParquetConfiguration(TypedDict, total=False):
    """Contains the configuration information of the Parquet format."""

    schemaDefinition: SchemaDefinition | None


class JsonConfiguration(TypedDict, total=False):
    """Contains the configuration information of the JSON format."""

    pass


class FileFormatConfiguration(TypedDict, total=False):
    """Contains the configuration information of file formats. IoT Analytics
    data stores support JSON and `Parquet <https://parquet.apache.org/>`__.

    The default file format is JSON. You can specify only one format.

    You can't change the file format after you create the data store.
    """

    jsonConfiguration: JsonConfiguration | None
    parquetConfiguration: ParquetConfiguration | None


class IotSiteWiseCustomerManagedDatastoreS3Storage(TypedDict, total=False):
    """Used to store data used by IoT SiteWise in an Amazon S3 bucket that you
    manage. You can't change the choice of Amazon S3 storage after your data
    store is created.
    """

    bucket: BucketName
    keyPrefix: S3KeyPrefix | None


class DatastoreIotSiteWiseMultiLayerStorage(TypedDict, total=False):
    """Used to store data used by IoT SiteWise in an Amazon S3 bucket that you
    manage. You can't change the choice of Amazon S3 storage after your data
    store is created.
    """

    customerManagedS3Storage: IotSiteWiseCustomerManagedDatastoreS3Storage


class CustomerManagedDatastoreS3Storage(TypedDict, total=False):
    """S3-customer-managed; When you choose customer-managed storage, the
    ``retentionPeriod`` parameter is ignored. You can't change the choice of
    Amazon S3 storage after your data store is created.
    """

    bucket: BucketName
    keyPrefix: S3KeyPrefix | None
    roleArn: RoleArn


class ServiceManagedDatastoreS3Storage(TypedDict, total=False):
    """Used to store data in an Amazon S3 bucket managed by IoT Analytics. You
    can't change the choice of Amazon S3 storage after your data store is
    created.
    """

    pass


class DatastoreStorage(TypedDict, total=False):
    """Where data in a data store is stored.. You can choose
    ``serviceManagedS3`` storage, ``customerManagedS3`` storage, or
    ``iotSiteWiseMultiLayerStorage`` storage. The default is
    ``serviceManagedS3``. You can't change the choice of Amazon S3 storage
    after your data store is created.
    """

    serviceManagedS3: ServiceManagedDatastoreS3Storage | None
    customerManagedS3: CustomerManagedDatastoreS3Storage | None
    iotSiteWiseMultiLayerStorage: DatastoreIotSiteWiseMultiLayerStorage | None


class CreateDatastoreRequest(ServiceRequest):
    datastoreName: DatastoreName
    datastoreStorage: DatastoreStorage | None
    retentionPeriod: RetentionPeriod | None
    tags: TagList | None
    fileFormatConfiguration: FileFormatConfiguration | None
    datastorePartitions: DatastorePartitions | None


class CreateDatastoreResponse(TypedDict, total=False):
    datastoreName: DatastoreName | None
    datastoreArn: DatastoreArn | None
    retentionPeriod: RetentionPeriod | None


class DeviceShadowEnrichActivity(TypedDict, total=False):
    """An activity that adds information from the IoT Device Shadow service to
    a message.
    """

    name: ActivityName
    attribute: AttributeName
    thingName: AttributeName
    roleArn: RoleArn
    next: ActivityName | None


class DeviceRegistryEnrichActivity(TypedDict, total=False):
    """An activity that adds data from the IoT device registry to your message."""

    name: ActivityName
    attribute: AttributeName
    thingName: AttributeName
    roleArn: RoleArn
    next: ActivityName | None


class MathActivity(TypedDict, total=False):
    """An activity that computes an arithmetic expression using the message's
    attributes.
    """

    name: ActivityName
    attribute: AttributeName
    math: MathExpression
    next: ActivityName | None


class FilterActivity(TypedDict, total=False):
    """An activity that filters a message based on its attributes."""

    name: ActivityName
    filter: FilterExpression
    next: ActivityName | None


class SelectAttributesActivity(TypedDict, total=False):
    """Used to create a new message using only the specified attributes from
    the original message.
    """

    name: ActivityName
    attributes: AttributeNames
    next: ActivityName | None


class RemoveAttributesActivity(TypedDict, total=False):
    """An activity that removes attributes from a message."""

    name: ActivityName
    attributes: AttributeNames
    next: ActivityName | None


class DatastoreActivity(TypedDict, total=False):
    """The datastore activity that specifies where to store the processed data."""

    name: ActivityName
    datastoreName: DatastoreName


class LambdaActivity(TypedDict, total=False):
    """An activity that runs a Lambda function to modify the message."""

    name: ActivityName
    lambdaName: LambdaName
    batchSize: ActivityBatchSize
    next: ActivityName | None


PipelineActivity = TypedDict(
    "PipelineActivity",
    {
        "channel": ChannelActivity | None,
        "lambda": LambdaActivity | None,
        "datastore": DatastoreActivity | None,
        "addAttributes": AddAttributesActivity | None,
        "removeAttributes": RemoveAttributesActivity | None,
        "selectAttributes": SelectAttributesActivity | None,
        "filter": FilterActivity | None,
        "math": MathActivity | None,
        "deviceRegistryEnrich": DeviceRegistryEnrichActivity | None,
        "deviceShadowEnrich": DeviceShadowEnrichActivity | None,
    },
    total=False,
)
PipelineActivities = list[PipelineActivity]


class CreatePipelineRequest(ServiceRequest):
    pipelineName: PipelineName
    pipelineActivities: PipelineActivities
    tags: TagList | None


class CreatePipelineResponse(TypedDict, total=False):
    pipelineName: PipelineName | None
    pipelineArn: PipelineArn | None


class CustomerManagedDatastoreS3StorageSummary(TypedDict, total=False):
    """Contains information about the data store that you manage."""

    bucket: BucketName | None
    keyPrefix: S3KeyPrefix | None
    roleArn: RoleArn | None


class Dataset(TypedDict, total=False):
    """Information about a dataset."""

    name: DatasetName | None
    arn: DatasetArn | None
    actions: DatasetActions | None
    triggers: DatasetTriggers | None
    contentDeliveryRules: DatasetContentDeliveryRules | None
    status: DatasetStatus | None
    creationTime: Timestamp | None
    lastUpdateTime: Timestamp | None
    retentionPeriod: RetentionPeriod | None
    versioningConfiguration: VersioningConfiguration | None
    lateDataRules: LateDataRules | None


class DatasetActionSummary(TypedDict, total=False):
    """Information about the action that automatically creates the dataset's
    contents.
    """

    actionName: DatasetActionName | None
    actionType: DatasetActionType | None


DatasetActionSummaries = list[DatasetActionSummary]


class DatasetContentStatus(TypedDict, total=False):
    """The state of the dataset contents and the reason they are in this state."""

    state: DatasetContentState | None
    reason: Reason | None


class DatasetContentSummary(TypedDict, total=False):
    """Summary information about dataset contents."""

    version: DatasetContentVersion | None
    status: DatasetContentStatus | None
    creationTime: Timestamp | None
    scheduleTime: Timestamp | None
    completionTime: Timestamp | None


DatasetContentSummaries = list[DatasetContentSummary]


class DatasetEntry(TypedDict, total=False):
    """The reference to a dataset entry."""

    entryName: EntryName | None
    dataURI: PresignedURI | None


DatasetEntries = list[DatasetEntry]


class DatasetSummary(TypedDict, total=False):
    """A summary of information about a dataset."""

    datasetName: DatasetName | None
    status: DatasetStatus | None
    creationTime: Timestamp | None
    lastUpdateTime: Timestamp | None
    triggers: DatasetTriggers | None
    actions: DatasetActionSummaries | None


DatasetSummaries = list[DatasetSummary]


class Datastore(TypedDict, total=False):
    """Information about a data store."""

    name: DatastoreName | None
    storage: DatastoreStorage | None
    arn: DatastoreArn | None
    status: DatastoreStatus | None
    retentionPeriod: RetentionPeriod | None
    creationTime: Timestamp | None
    lastUpdateTime: Timestamp | None
    lastMessageArrivalTime: Timestamp | None
    fileFormatConfiguration: FileFormatConfiguration | None
    datastorePartitions: DatastorePartitions | None


class IotSiteWiseCustomerManagedDatastoreS3StorageSummary(TypedDict, total=False):
    """Contains information about the data store that you manage, which stores
    data used by IoT SiteWise.
    """

    bucket: BucketName | None
    keyPrefix: S3KeyPrefix | None


class DatastoreIotSiteWiseMultiLayerStorageSummary(TypedDict, total=False):
    """Contains information about the data store that you manage, which stores
    data used by IoT SiteWise.
    """

    customerManagedS3Storage: IotSiteWiseCustomerManagedDatastoreS3StorageSummary | None


class DatastoreStatistics(TypedDict, total=False):
    """Statistical information about the data store."""

    size: EstimatedResourceSize | None


class ServiceManagedDatastoreS3StorageSummary(TypedDict, total=False):
    """Contains information about the data store that is managed by IoT
    Analytics.
    """

    pass


class DatastoreStorageSummary(TypedDict, total=False):
    """Contains information about your data store."""

    serviceManagedS3: ServiceManagedDatastoreS3StorageSummary | None
    customerManagedS3: CustomerManagedDatastoreS3StorageSummary | None
    iotSiteWiseMultiLayerStorage: DatastoreIotSiteWiseMultiLayerStorageSummary | None


class DatastoreSummary(TypedDict, total=False):
    """A summary of information about a data store."""

    datastoreName: DatastoreName | None
    datastoreStorage: DatastoreStorageSummary | None
    status: DatastoreStatus | None
    creationTime: Timestamp | None
    lastUpdateTime: Timestamp | None
    lastMessageArrivalTime: Timestamp | None
    fileFormatType: FileFormatType | None
    datastorePartitions: DatastorePartitions | None


DatastoreSummaries = list[DatastoreSummary]


class DeleteChannelRequest(ServiceRequest):
    channelName: ChannelName


class DeleteDatasetContentRequest(ServiceRequest):
    datasetName: DatasetName
    versionId: DatasetContentVersion | None


class DeleteDatasetRequest(ServiceRequest):
    datasetName: DatasetName


class DeleteDatastoreRequest(ServiceRequest):
    datastoreName: DatastoreName


class DeletePipelineRequest(ServiceRequest):
    pipelineName: PipelineName


class DescribeChannelRequest(ServiceRequest):
    channelName: ChannelName
    includeStatistics: IncludeStatisticsFlag | None


class DescribeChannelResponse(TypedDict, total=False):
    channel: Channel | None
    statistics: ChannelStatistics | None


class DescribeDatasetRequest(ServiceRequest):
    datasetName: DatasetName


class DescribeDatasetResponse(TypedDict, total=False):
    dataset: Dataset | None


class DescribeDatastoreRequest(ServiceRequest):
    datastoreName: DatastoreName
    includeStatistics: IncludeStatisticsFlag | None


class DescribeDatastoreResponse(TypedDict, total=False):
    datastore: Datastore | None
    statistics: DatastoreStatistics | None


class DescribeLoggingOptionsRequest(ServiceRequest):
    pass


class LoggingOptions(TypedDict, total=False):
    """Information about logging options."""

    roleArn: RoleArn
    level: LoggingLevel
    enabled: LoggingEnabled


class DescribeLoggingOptionsResponse(TypedDict, total=False):
    loggingOptions: LoggingOptions | None


class DescribePipelineRequest(ServiceRequest):
    pipelineName: PipelineName


class ReprocessingSummary(TypedDict, total=False):
    """Information about pipeline reprocessing."""

    id: ReprocessingId | None
    status: ReprocessingStatus | None
    creationTime: Timestamp | None


ReprocessingSummaries = list[ReprocessingSummary]


class Pipeline(TypedDict, total=False):
    """Contains information about a pipeline."""

    name: PipelineName | None
    arn: PipelineArn | None
    activities: PipelineActivities | None
    reprocessingSummaries: ReprocessingSummaries | None
    creationTime: Timestamp | None
    lastUpdateTime: Timestamp | None


class DescribePipelineResponse(TypedDict, total=False):
    pipeline: Pipeline | None


EndTime = datetime


class GetDatasetContentRequest(ServiceRequest):
    datasetName: DatasetName
    versionId: DatasetContentVersion | None


class GetDatasetContentResponse(TypedDict, total=False):
    entries: DatasetEntries | None
    timestamp: Timestamp | None
    status: DatasetContentStatus | None


class ListChannelsRequest(ServiceRequest):
    nextToken: NextToken | None
    maxResults: MaxResults | None


class ListChannelsResponse(TypedDict, total=False):
    channelSummaries: ChannelSummaries | None
    nextToken: NextToken | None


class ListDatasetContentsRequest(ServiceRequest):
    datasetName: DatasetName
    nextToken: NextToken | None
    maxResults: MaxResults | None
    scheduledOnOrAfter: Timestamp | None
    scheduledBefore: Timestamp | None


class ListDatasetContentsResponse(TypedDict, total=False):
    datasetContentSummaries: DatasetContentSummaries | None
    nextToken: NextToken | None


class ListDatasetsRequest(ServiceRequest):
    nextToken: NextToken | None
    maxResults: MaxResults | None


class ListDatasetsResponse(TypedDict, total=False):
    datasetSummaries: DatasetSummaries | None
    nextToken: NextToken | None


class ListDatastoresRequest(ServiceRequest):
    nextToken: NextToken | None
    maxResults: MaxResults | None


class ListDatastoresResponse(TypedDict, total=False):
    datastoreSummaries: DatastoreSummaries | None
    nextToken: NextToken | None


class ListPipelinesRequest(ServiceRequest):
    nextToken: NextToken | None
    maxResults: MaxResults | None


class PipelineSummary(TypedDict, total=False):
    """A summary of information about a pipeline."""

    pipelineName: PipelineName | None
    reprocessingSummaries: ReprocessingSummaries | None
    creationTime: Timestamp | None
    lastUpdateTime: Timestamp | None


PipelineSummaries = list[PipelineSummary]


class ListPipelinesResponse(TypedDict, total=False):
    pipelineSummaries: PipelineSummaries | None
    nextToken: NextToken | None


class ListTagsForResourceRequest(ServiceRequest):
    resourceArn: ResourceArn


class ListTagsForResourceResponse(TypedDict, total=False):
    tags: TagList | None


MessagePayloads = list[MessagePayload]


class PutLoggingOptionsRequest(ServiceRequest):
    loggingOptions: LoggingOptions


class RunPipelineActivityRequest(ServiceRequest):
    pipelineActivity: PipelineActivity
    payloads: MessagePayloads


class RunPipelineActivityResponse(TypedDict, total=False):
    payloads: MessagePayloads | None
    logResult: LogResult | None


StartTime = datetime


class SampleChannelDataRequest(ServiceRequest):
    channelName: ChannelName
    maxMessages: MaxMessages | None
    startTime: StartTime | None
    endTime: EndTime | None


class SampleChannelDataResponse(TypedDict, total=False):
    payloads: MessagePayloads | None


class StartPipelineReprocessingRequest(ServiceRequest):
    pipelineName: PipelineName
    startTime: StartTime | None
    endTime: EndTime | None
    channelMessages: ChannelMessages | None


class StartPipelineReprocessingResponse(TypedDict, total=False):
    reprocessingId: ReprocessingId | None


TagKeyList = list[TagKey]


class TagResourceRequest(ServiceRequest):
    resourceArn: ResourceArn
    tags: TagList


class TagResourceResponse(TypedDict, total=False):
    pass


class UntagResourceRequest(ServiceRequest):
    resourceArn: ResourceArn
    tagKeys: TagKeyList


class UntagResourceResponse(TypedDict, total=False):
    pass


class UpdateChannelRequest(ServiceRequest):
    channelName: ChannelName
    channelStorage: ChannelStorage | None
    retentionPeriod: RetentionPeriod | None


class UpdateDatasetRequest(ServiceRequest):
    datasetName: DatasetName
    actions: DatasetActions
    triggers: DatasetTriggers | None
    contentDeliveryRules: DatasetContentDeliveryRules | None
    retentionPeriod: RetentionPeriod | None
    versioningConfiguration: VersioningConfiguration | None
    lateDataRules: LateDataRules | None


class UpdateDatastoreRequest(ServiceRequest):
    datastoreName: DatastoreName
    retentionPeriod: RetentionPeriod | None
    datastoreStorage: DatastoreStorage | None
    fileFormatConfiguration: FileFormatConfiguration | None


class UpdatePipelineRequest(ServiceRequest):
    pipelineName: PipelineName
    pipelineActivities: PipelineActivities


class IotanalyticsApi:
    service: str = "iotanalytics"
    version: str = "2017-11-27"

    @handler("BatchPutMessage")
    def batch_put_message(
        self, context: RequestContext, channel_name: ChannelName, messages: Messages, **kwargs
    ) -> BatchPutMessageResponse:
        """Sends messages to a channel.

        :param channel_name: The name of the channel where the messages are sent.
        :param messages: The list of messages to be sent.
        :returns: BatchPutMessageResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CancelPipelineReprocessing")
    def cancel_pipeline_reprocessing(
        self,
        context: RequestContext,
        pipeline_name: PipelineName,
        reprocessing_id: ReprocessingId,
        **kwargs,
    ) -> CancelPipelineReprocessingResponse:
        """Cancels the reprocessing of data through the pipeline.

        :param pipeline_name: The name of pipeline for which data reprocessing is canceled.
        :param reprocessing_id: The ID of the reprocessing task (returned by
        ``StartPipelineReprocessing``).
        :returns: CancelPipelineReprocessingResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateChannel")
    def create_channel(
        self,
        context: RequestContext,
        channel_name: ChannelName,
        channel_storage: ChannelStorage | None = None,
        retention_period: RetentionPeriod | None = None,
        tags: TagList | None = None,
        **kwargs,
    ) -> CreateChannelResponse:
        """Used to create a channel. A channel collects data from an MQTT topic and
        archives the raw, unprocessed messages before publishing the data to a
        pipeline.

        :param channel_name: The name of the channel.
        :param channel_storage: Where channel data is stored.
        :param retention_period: How long, in days, message data is kept for the channel.
        :param tags: Metadata which can be used to manage the channel.
        :returns: CreateChannelResponse
        :raises InvalidRequestException:
        :raises ResourceAlreadyExistsException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("CreateDataset")
    def create_dataset(
        self,
        context: RequestContext,
        dataset_name: DatasetName,
        actions: DatasetActions,
        triggers: DatasetTriggers | None = None,
        content_delivery_rules: DatasetContentDeliveryRules | None = None,
        retention_period: RetentionPeriod | None = None,
        versioning_configuration: VersioningConfiguration | None = None,
        tags: TagList | None = None,
        late_data_rules: LateDataRules | None = None,
        **kwargs,
    ) -> CreateDatasetResponse:
        """Used to create a dataset. A dataset stores data retrieved from a data
        store by applying a ``queryAction`` (a SQL query) or a
        ``containerAction`` (executing a containerized application). This
        operation creates the skeleton of a dataset. The dataset can be
        populated manually by calling ``CreateDatasetContent`` or automatically
        according to a trigger you specify.

        :param dataset_name: The name of the dataset.
        :param actions: A list of actions that create the dataset contents.
        :param triggers: A list of triggers.
        :param content_delivery_rules: When dataset contents are created, they are delivered to destinations
        specified here.
        :param retention_period: Optional.
        :param versioning_configuration: Optional.
        :param tags: Metadata which can be used to manage the dataset.
        :param late_data_rules: A list of data rules that send notifications to CloudWatch, when data
        arrives late.
        :returns: CreateDatasetResponse
        :raises InvalidRequestException:
        :raises ResourceAlreadyExistsException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("CreateDatasetContent")
    def create_dataset_content(
        self,
        context: RequestContext,
        dataset_name: DatasetName,
        version_id: DatasetContentVersion | None = None,
        **kwargs,
    ) -> CreateDatasetContentResponse:
        """Creates the content of a dataset by applying a ``queryAction`` (a SQL
        query) or a ``containerAction`` (executing a containerized application).

        :param dataset_name: The name of the dataset.
        :param version_id: The version ID of the dataset content.
        :returns: CreateDatasetContentResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateDatastore")
    def create_datastore(
        self,
        context: RequestContext,
        datastore_name: DatastoreName,
        datastore_storage: DatastoreStorage | None = None,
        retention_period: RetentionPeriod | None = None,
        tags: TagList | None = None,
        file_format_configuration: FileFormatConfiguration | None = None,
        datastore_partitions: DatastorePartitions | None = None,
        **kwargs,
    ) -> CreateDatastoreResponse:
        """Creates a data store, which is a repository for messages.

        :param datastore_name: The name of the data store.
        :param datastore_storage: Where data in a data store is stored.
        :param retention_period: How long, in days, message data is kept for the data store.
        :param tags: Metadata which can be used to manage the data store.
        :param file_format_configuration: Contains the configuration information of file formats.
        :param datastore_partitions: Contains information about the partition dimensions in a data store.
        :returns: CreateDatastoreResponse
        :raises InvalidRequestException:
        :raises ResourceAlreadyExistsException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("CreatePipeline")
    def create_pipeline(
        self,
        context: RequestContext,
        pipeline_name: PipelineName,
        pipeline_activities: PipelineActivities,
        tags: TagList | None = None,
        **kwargs,
    ) -> CreatePipelineResponse:
        """Creates a pipeline. A pipeline consumes messages from a channel and
        allows you to process the messages before storing them in a data store.
        You must specify both a ``channel`` and a ``datastore`` activity and,
        optionally, as many as 23 additional activities in the
        ``pipelineActivities`` array.

        :param pipeline_name: The name of the pipeline.
        :param pipeline_activities: A list of ``PipelineActivity`` objects.
        :param tags: Metadata which can be used to manage the pipeline.
        :returns: CreatePipelineResponse
        :raises InvalidRequestException:
        :raises ResourceAlreadyExistsException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("DeleteChannel")
    def delete_channel(self, context: RequestContext, channel_name: ChannelName, **kwargs) -> None:
        """Deletes the specified channel.

        :param channel_name: The name of the channel to delete.
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeleteDataset")
    def delete_dataset(self, context: RequestContext, dataset_name: DatasetName, **kwargs) -> None:
        """Deletes the specified dataset.

        You do not have to delete the content of the dataset before you perform
        this operation.

        :param dataset_name: The name of the dataset to delete.
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeleteDatasetContent")
    def delete_dataset_content(
        self,
        context: RequestContext,
        dataset_name: DatasetName,
        version_id: DatasetContentVersion | None = None,
        **kwargs,
    ) -> None:
        """Deletes the content of the specified dataset.

        :param dataset_name: The name of the dataset whose content is deleted.
        :param version_id: The version of the dataset whose content is deleted.
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeleteDatastore")
    def delete_datastore(
        self, context: RequestContext, datastore_name: DatastoreName, **kwargs
    ) -> None:
        """Deletes the specified data store.

        :param datastore_name: The name of the data store to delete.
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeletePipeline")
    def delete_pipeline(
        self, context: RequestContext, pipeline_name: PipelineName, **kwargs
    ) -> None:
        """Deletes the specified pipeline.

        :param pipeline_name: The name of the pipeline to delete.
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DescribeChannel")
    def describe_channel(
        self,
        context: RequestContext,
        channel_name: ChannelName,
        include_statistics: IncludeStatisticsFlag | None = None,
        **kwargs,
    ) -> DescribeChannelResponse:
        """Retrieves information about a channel.

        :param channel_name: The name of the channel whose information is retrieved.
        :param include_statistics: If true, additional statistical information about the channel is
        included in the response.
        :returns: DescribeChannelResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DescribeDataset")
    def describe_dataset(
        self, context: RequestContext, dataset_name: DatasetName, **kwargs
    ) -> DescribeDatasetResponse:
        """Retrieves information about a dataset.

        :param dataset_name: The name of the dataset whose information is retrieved.
        :returns: DescribeDatasetResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DescribeDatastore")
    def describe_datastore(
        self,
        context: RequestContext,
        datastore_name: DatastoreName,
        include_statistics: IncludeStatisticsFlag | None = None,
        **kwargs,
    ) -> DescribeDatastoreResponse:
        """Retrieves information about a data store.

        :param datastore_name: The name of the data store.
        :param include_statistics: If true, additional statistical information about the data store is
        included in the response.
        :returns: DescribeDatastoreResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DescribeLoggingOptions")
    def describe_logging_options(
        self, context: RequestContext, **kwargs
    ) -> DescribeLoggingOptionsResponse:
        """Retrieves the current settings of the IoT Analytics logging options.

        :returns: DescribeLoggingOptionsResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DescribePipeline")
    def describe_pipeline(
        self, context: RequestContext, pipeline_name: PipelineName, **kwargs
    ) -> DescribePipelineResponse:
        """Retrieves information about a pipeline.

        :param pipeline_name: The name of the pipeline whose information is retrieved.
        :returns: DescribePipelineResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetDatasetContent")
    def get_dataset_content(
        self,
        context: RequestContext,
        dataset_name: DatasetName,
        version_id: DatasetContentVersion | None = None,
        **kwargs,
    ) -> GetDatasetContentResponse:
        """Retrieves the contents of a dataset as presigned URIs.

        :param dataset_name: The name of the dataset whose contents are retrieved.
        :param version_id: The version of the dataset whose contents are retrieved.
        :returns: GetDatasetContentResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListChannels")
    def list_channels(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListChannelsResponse:
        """Retrieves a list of channels.

        :param next_token: The token for the next set of results.
        :param max_results: The maximum number of results to return in this request.
        :returns: ListChannelsResponse
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListDatasetContents")
    def list_dataset_contents(
        self,
        context: RequestContext,
        dataset_name: DatasetName,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        scheduled_on_or_after: Timestamp | None = None,
        scheduled_before: Timestamp | None = None,
        **kwargs,
    ) -> ListDatasetContentsResponse:
        """Lists information about dataset contents that have been created.

        :param dataset_name: The name of the dataset whose contents information you want to list.
        :param next_token: The token for the next set of results.
        :param max_results: The maximum number of results to return in this request.
        :param scheduled_on_or_after: A filter to limit results to those dataset contents whose creation is
        scheduled on or after the given time.
        :param scheduled_before: A filter to limit results to those dataset contents whose creation is
        scheduled before the given time.
        :returns: ListDatasetContentsResponse
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListDatasets")
    def list_datasets(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListDatasetsResponse:
        """Retrieves information about datasets.

        :param next_token: The token for the next set of results.
        :param max_results: The maximum number of results to return in this request.
        :returns: ListDatasetsResponse
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListDatastores")
    def list_datastores(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListDatastoresResponse:
        """Retrieves a list of data stores.

        :param next_token: The token for the next set of results.
        :param max_results: The maximum number of results to return in this request.
        :returns: ListDatastoresResponse
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListPipelines")
    def list_pipelines(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListPipelinesResponse:
        """Retrieves a list of pipelines.

        :param next_token: The token for the next set of results.
        :param max_results: The maximum number of results to return in this request.
        :returns: ListPipelinesResponse
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListTagsForResource")
    def list_tags_for_resource(
        self, context: RequestContext, resource_arn: ResourceArn, **kwargs
    ) -> ListTagsForResourceResponse:
        """Lists the tags (metadata) that you have assigned to the resource.

        :param resource_arn: The ARN of the resource whose tags you want to list.
        :returns: ListTagsForResourceResponse
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        :raises LimitExceededException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("PutLoggingOptions")
    def put_logging_options(
        self, context: RequestContext, logging_options: LoggingOptions, **kwargs
    ) -> None:
        """Sets or updates the IoT Analytics logging options.

        If you update the value of any ``loggingOptions`` field, it takes up to
        one minute for the change to take effect. Also, if you change the policy
        attached to the role you specified in the ``roleArn`` field (for
        example, to correct an invalid policy), it takes up to five minutes for
        that change to take effect.

        :param logging_options: The new values of the IoT Analytics logging options.
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("RunPipelineActivity")
    def run_pipeline_activity(
        self,
        context: RequestContext,
        pipeline_activity: PipelineActivity,
        payloads: MessagePayloads,
        **kwargs,
    ) -> RunPipelineActivityResponse:
        """Simulates the results of running a pipeline activity on a message
        payload.

        :param pipeline_activity: The pipeline activity that is run.
        :param payloads: The sample message payloads on which the pipeline activity is run.
        :returns: RunPipelineActivityResponse
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("SampleChannelData")
    def sample_channel_data(
        self,
        context: RequestContext,
        channel_name: ChannelName,
        max_messages: MaxMessages | None = None,
        start_time: StartTime | None = None,
        end_time: EndTime | None = None,
        **kwargs,
    ) -> SampleChannelDataResponse:
        """Retrieves a sample of messages from the specified channel ingested
        during the specified timeframe. Up to 10 messages can be retrieved.

        :param channel_name: The name of the channel whose message samples are retrieved.
        :param max_messages: The number of sample messages to be retrieved.
        :param start_time: The start of the time window from which sample messages are retrieved.
        :param end_time: The end of the time window from which sample messages are retrieved.
        :returns: SampleChannelDataResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("StartPipelineReprocessing")
    def start_pipeline_reprocessing(
        self,
        context: RequestContext,
        pipeline_name: PipelineName,
        start_time: StartTime | None = None,
        end_time: EndTime | None = None,
        channel_messages: ChannelMessages | None = None,
        **kwargs,
    ) -> StartPipelineReprocessingResponse:
        """Starts the reprocessing of raw message data through the pipeline.

        :param pipeline_name: The name of the pipeline on which to start reprocessing.
        :param start_time: The start time (inclusive) of raw message data that is reprocessed.
        :param end_time: The end time (exclusive) of raw message data that is reprocessed.
        :param channel_messages: Specifies one or more sets of channel messages that you want to
        reprocess.
        :returns: StartPipelineReprocessingResponse
        :raises ResourceNotFoundException:
        :raises ResourceAlreadyExistsException:
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("TagResource")
    def tag_resource(
        self, context: RequestContext, resource_arn: ResourceArn, tags: TagList, **kwargs
    ) -> TagResourceResponse:
        """Adds to or modifies the tags of the given resource. Tags are metadata
        that can be used to manage a resource.

        :param resource_arn: The ARN of the resource whose tags you want to modify.
        :param tags: The new or modified tags for the resource.
        :returns: TagResourceResponse
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        :raises LimitExceededException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("UntagResource")
    def untag_resource(
        self, context: RequestContext, resource_arn: ResourceArn, tag_keys: TagKeyList, **kwargs
    ) -> UntagResourceResponse:
        """Removes the given tags (metadata) from the resource.

        :param resource_arn: The ARN of the resource whose tags you want to remove.
        :param tag_keys: The keys of those tags which you want to remove.
        :returns: UntagResourceResponse
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        :raises LimitExceededException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("UpdateChannel")
    def update_channel(
        self,
        context: RequestContext,
        channel_name: ChannelName,
        channel_storage: ChannelStorage | None = None,
        retention_period: RetentionPeriod | None = None,
        **kwargs,
    ) -> None:
        """Used to update the settings of a channel.

        :param channel_name: The name of the channel to be updated.
        :param channel_storage: Where channel data is stored.
        :param retention_period: How long, in days, message data is kept for the channel.
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("UpdateDataset")
    def update_dataset(
        self,
        context: RequestContext,
        dataset_name: DatasetName,
        actions: DatasetActions,
        triggers: DatasetTriggers | None = None,
        content_delivery_rules: DatasetContentDeliveryRules | None = None,
        retention_period: RetentionPeriod | None = None,
        versioning_configuration: VersioningConfiguration | None = None,
        late_data_rules: LateDataRules | None = None,
        **kwargs,
    ) -> None:
        """Updates the settings of a dataset.

        :param dataset_name: The name of the dataset to update.
        :param actions: A list of ``DatasetAction`` objects.
        :param triggers: A list of ``DatasetTrigger`` objects.
        :param content_delivery_rules: When dataset contents are created, they are delivered to destinations
        specified here.
        :param retention_period: How long, in days, dataset contents are kept for the dataset.
        :param versioning_configuration: Optional.
        :param late_data_rules: A list of data rules that send notifications to CloudWatch, when data
        arrives late.
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("UpdateDatastore")
    def update_datastore(
        self,
        context: RequestContext,
        datastore_name: DatastoreName,
        retention_period: RetentionPeriod | None = None,
        datastore_storage: DatastoreStorage | None = None,
        file_format_configuration: FileFormatConfiguration | None = None,
        **kwargs,
    ) -> None:
        """Used to update the settings of a data store.

        :param datastore_name: The name of the data store to be updated.
        :param retention_period: How long, in days, message data is kept for the data store.
        :param datastore_storage: Where data in a data store is stored.
        :param file_format_configuration: Contains the configuration information of file formats.
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("UpdatePipeline")
    def update_pipeline(
        self,
        context: RequestContext,
        pipeline_name: PipelineName,
        pipeline_activities: PipelineActivities,
        **kwargs,
    ) -> None:
        """Updates the settings of a pipeline. You must specify both a ``channel``
        and a ``datastore`` activity and, optionally, as many as 23 additional
        activities in the ``pipelineActivities`` array.

        :param pipeline_name: The name of the pipeline to update.
        :param pipeline_activities: A list of ``PipelineActivity`` objects.
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ThrottlingException:
        :raises LimitExceededException:
        """
        raise NotImplementedError
