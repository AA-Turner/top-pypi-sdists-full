from datetime import datetime
from enum import StrEnum
from typing import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

AbortThresholdPercentage = float
AcmCertificateArn = str
AggregationField = str
AggregationTypeValue = str
AlarmName = str
AlertTargetArn = str
AllowAuthorizerOverride = bool
AllowAutoRegistration = bool
AscendingOrder = bool
AssetId = str
AssetPropertyAlias = str
AssetPropertyBooleanValue = str
AssetPropertyDoubleValue = str
AssetPropertyEntryId = str
AssetPropertyId = str
AssetPropertyIntegerValue = str
AssetPropertyOffsetInNanos = str
AssetPropertyQuality = str
AssetPropertyStringValue = str
AssetPropertyTimeInSeconds = str
AttributeKey = str
AttributeName = str
AttributeValue = str
AuditCheckName = str
AuditDescription = str
AuditTaskId = str
AuthorizerArn = str
AuthorizerFunctionArn = str
AuthorizerName = str
Average = float
AwsAccountId = str
AwsArn = str
AwsIotJobArn = str
AwsIotJobId = str
AwsIotSqlVersion = str
AwsJobAbortCriteriaAbortThresholdPercentage = float
AwsJobAbortCriteriaMinimumNumberOfExecutedThings = int
AwsJobRateIncreaseCriteriaNumberOfThings = int
AwsJobRolloutIncrementFactor = float
AwsJobRolloutRatePerMinute = int
BatchMode = bool
BeforeSubstitutionFlag = bool
BehaviorMetric = str
BehaviorName = str
BillingGroupArn = str
BillingGroupDescription = str
BillingGroupId = str
BillingGroupName = str
Boolean = bool
BooleanCommandExecutionResult = bool
BooleanKey = bool
BooleanParameterValue = bool
BooleanWrapperObject = bool
BucketKeyValue = str
BucketName = str
CanceledChecksCount = int
CanceledThings = int
CertificateArn = str
CertificateId = str
CertificateName = str
CertificatePathOnDevice = str
CertificatePem = str
CertificateProviderArn = str
CertificateProviderFunctionArn = str
CertificateProviderName = str
CertificateSigningRequest = str
ChannelName = str
CheckCompliant = bool
Cidr = str
ClientCertificateCallbackArn = str
ClientId = str
ClientRequestToken = str
ClientToken = str
Code = str
CognitoIdentityPoolId = str
CommandArn = str
CommandDescription = str
CommandExecutionId = str
CommandExecutionResultName = str
CommandId = str
CommandMaxResults = int
CommandParameterDescription = str
CommandParameterName = str
Comment = str
CompliantChecksCount = int
ConfigValue = str
ConfirmationToken = str
ConnectionAttributeName = str
ConnectivityApiThingName = str
ConsecutiveDatapointsToAlarm = int
ConsecutiveDatapointsToClear = int
ContentType = str
CorrelationData = str
Count = int
CredentialDurationSeconds = int
CronExpression = str
CustomMetricArn = str
CustomMetricDisplayName = str
CustomerVersion = int
DataCollectionPercentage = float
DayOfMonth = str
DeleteAdditionalMetricsToRetain = bool
DeleteAlertTargets = bool
DeleteBehaviors = bool
DeleteMetricsExportConfig = bool
DeleteScheduledAudits = bool
DeleteStream = bool
DeliveryStreamName = str
DeprecationFlag = bool
Description = str
DetailsKey = str
DetailsValue = str
DetectMitigationActionExecutionErrorCode = str
DeviceDefenderThingName = str
DimensionArn = str
DimensionName = str
DimensionStringValue = str
DisableAllLogs = bool
DisconnectReason = str
DisplayName = str
DomainConfigurationArn = str
DomainConfigurationName = str
DomainName = str
DoubleParameterValue = float
DurationInMinutes = int
DurationSeconds = int
DynamoOperation = str
ElasticsearchEndpoint = str
ElasticsearchId = str
ElasticsearchIndex = str
ElasticsearchType = str
EnableCachingForHttp = bool
EnableOCSPCheck = bool
Enabled = bool
EnabledBoolean = bool
EndpointAddress = str
EndpointType = str
Environment = str
ErrorCode = str
ErrorMessage = str
EvaluationStatistic = str
Example = str
ExecutionNamePrefix = str
ExportMetric = bool
FailedChecksCount = int
FailedThings = int
FieldName = str
FileId = int
FileName = str
FileType = int
FindingId = str
FirehoseSeparator = str
Flag = bool
FleetMetricArn = str
FleetMetricDescription = str
FleetMetricName = str
FleetMetricPeriod = int
ForceDelete = bool
ForceDeleteAWSJob = bool
ForceFlag = bool
Forced = bool
FunctionArn = str
GenerationId = str
HashAlgorithm = str
HashKeyField = str
HashKeyValue = str
HeaderKey = str
HeaderValue = str
HttpHeaderName = str
HttpHeaderValue = str
HttpQueryString = str
InProgressChecksCount = int
InProgressThings = int
IncrementFactor = float
IndexName = str
IndexSchema = str
InlineDocument = str
InputName = str
IntegerParameterValue = int
IsAuthenticated = bool
IsDefaultVersion = bool
IsDisabled = bool
IsSuppressed = bool
IssuerCertificateSerialNumber = str
IssuerCertificateSubject = str
IssuerId = str
JobArn = str
JobDescription = str
JobDocument = str
JobDocumentSource = str
JobId = str
JobTemplateArn = str
JobTemplateId = str
JsonDocument = str
KafkaHeaderKey = str
KafkaHeaderValue = str
Key = str
KeyName = str
KeyValue = str
KmsAccessRoleArn = str
KmsKeyArn = str
LaserMaxResults = int
ListSuppressedAlerts = bool
ListSuppressedFindings = bool
LogGroupName = str
LogTargetName = str
ManagedJobTemplateName = str
ManagedTemplateVersion = str
Marker = str
MaxBuckets = int
MaxJobExecutionsPerMin = int
MaxResults = int
Maximum = float
MaximumPerMinute = int
Message = str
MessageExpiry = str
MessageId = str
MetricName = str
MimeType = str
Minimum = float
MinimumNumberOfExecutedThings = int
MissingContextValue = str
MitigationActionArn = str
MitigationActionId = str
MitigationActionName = str
MitigationActionsTaskId = str
MqttClientId = str
MqttTopic = str
MqttUsername = str
NamespaceId = str
NextToken = str
NonCompliantChecksCount = int
NullableBoolean = bool
Number = float
NumberOfRetries = int
NumberOfThings = int
OCSPLambdaArn = str
OTAUpdateArn = str
OTAUpdateDescription = str
OTAUpdateErrorMessage = str
OTAUpdateFileVersion = str
OTAUpdateId = str
Optional_ = bool
OverrideDynamicGroups = bool
PackageArn = str
PackageCatalogMaxResults = int
PackageName = str
PackageVersionArn = str
PackageVersionErrorReason = str
PackageVersionRecipe = str
PageSize = int
Parameter = str
ParameterKey = str
ParameterValue = str
PartitionKey = str
PayloadField = str
PayloadFormatIndicator = str
PayloadVersion = str
Percent = float
PercentValue = float
Percentage = int
Platform = str
PolicyArn = str
PolicyDocument = str
PolicyName = str
PolicyTarget = str
PolicyVersionId = str
Port = int
Prefix = str
PrimitiveBoolean = bool
Principal = str
PrincipalArn = str
PrincipalId = str
PrivateKey = str
ProcessingTargetName = str
PublicKey = str
Qos = int
QueryMaxResults = int
QueryString = str
QueryVersion = str
QueueUrl = str
QueuedThings = int
RangeKeyField = str
RangeKeyValue = str
ReasonCode = str
ReasonForNonCompliance = str
ReasonForNonComplianceCode = str
Recursive = bool
RecursiveWithoutDefault = bool
Regex = str
RegistrationCode = str
RegistryMaxResults = int
RegistryS3BucketName = str
RegistryS3KeyName = str
RejectedThings = int
RemoveAuthorizerConfig = bool
RemoveAutoRegistration = bool
RemoveHook = bool
RemoveThingType = bool
RemovedThings = int
ReservedDomainConfigurationName = str
Resource = str
ResourceArn = str
ResourceAttributeKey = str
ResourceAttributeValue = str
ResourceDescription = str
ResourceLogicalId = str
ResponseTopic = str
RetryAttempt = int
RoleAlias = str
RoleAliasArn = str
RoleArn = str
RolloutRatePerMinute = int
RuleArn = str
RuleName = str
S3Bucket = str
S3FileUrl = str
S3Key = str
S3Version = str
SQL = str
SalesforceEndpoint = str
SalesforceToken = str
SbomValidationErrorMessage = str
ScheduledAuditArn = str
ScheduledAuditName = str
SearchQueryMaxResults = int
Seconds = int
SecurityGroupId = str
SecurityPolicy = str
SecurityProfileArn = str
SecurityProfileDescription = str
SecurityProfileName = str
SecurityProfileTargetArn = str
ServerCertificateStatusDetail = str
ServerName = str
ServiceName = str
SetAsActive = bool
SetAsActiveFlag = bool
SetAsDefault = bool
ShadowName = str
SignatureAlgorithm = str
SigningJobId = str
SigningProfileName = str
SigningRegion = str
SkyfallMaxResults = int
SnsTopicArn = str
StateMachineName = str
StateReason = str
StateValue = str
StatusCode = int
StatusReasonCode = str
StatusReasonDescription = str
StdDeviation = float
StreamArn = str
StreamDescription = str
StreamId = str
StreamName = str
StreamVersion = int
String = str
StringCommandExecutionResult = str
StringDateTime = str
StringParameterValue = str
SubnetId = str
SucceededThings = int
Sum = float
SumOfSquares = float
SuppressAlerts = bool
SuppressIndefinitely = bool
TableName = str
TagKey = str
TagValue = str
Target = str
TargetArn = str
TargetFieldName = str
TaskId = str
TemplateArn = str
TemplateBody = str
TemplateDescription = str
TemplateName = str
TemplateVersionId = int
ThingArn = str
ThingGroupArn = str
ThingGroupDescription = str
ThingGroupId = str
ThingGroupName = str
ThingId = str
ThingName = str
ThingTypeArn = str
ThingTypeDescription = str
ThingTypeId = str
ThingTypeName = str
TimedOutThings = int
TimestreamDatabaseName = str
TimestreamDimensionName = str
TimestreamDimensionValue = str
TimestreamTableName = str
TimestreamTimestampUnit = str
TimestreamTimestampValue = str
TinyMaxResults = int
Token = str
TokenKeyName = str
TokenSignature = str
Topic = str
TopicPattern = str
TopicRuleDestinationMaxResults = int
TopicRuleMaxResults = int
TotalChecksCount = int
UndoDeprecate = bool
UnsetDefaultVersion = bool
UnsignedLongParameterValue = str
Url = str
UseBase64 = bool
UserPropertyKey = str
UserPropertyKeyName = str
UserPropertyValue = str
Valid = bool
Value = str
Variance = float
VerificationStateDescription = str
VersionName = str
ViolationId = str
VpcId = str
WaitingForDataCollectionChecksCount = int
errorMessage = str
resourceArn = str
resourceId = str
stringValue = str
usePrefixAttributeValue = bool


class AbortAction(StrEnum):
    CANCEL = "CANCEL"


class ActionType(StrEnum):
    PUBLISH = "PUBLISH"
    SUBSCRIBE = "SUBSCRIBE"
    RECEIVE = "RECEIVE"
    CONNECT = "CONNECT"


class AggregationTypeName(StrEnum):
    Statistics = "Statistics"
    Percentiles = "Percentiles"
    Cardinality = "Cardinality"


class AlertTargetType(StrEnum):
    SNS = "SNS"


class ApplicationProtocol(StrEnum):
    SECURE_MQTT = "SECURE_MQTT"
    MQTT_WSS = "MQTT_WSS"
    HTTPS = "HTTPS"
    DEFAULT = "DEFAULT"


class AuditCheckRunStatus(StrEnum):
    IN_PROGRESS = "IN_PROGRESS"
    WAITING_FOR_DATA_COLLECTION = "WAITING_FOR_DATA_COLLECTION"
    CANCELED = "CANCELED"
    COMPLETED_COMPLIANT = "COMPLETED_COMPLIANT"
    COMPLETED_NON_COMPLIANT = "COMPLETED_NON_COMPLIANT"
    FAILED = "FAILED"


class AuditFindingSeverity(StrEnum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class AuditFrequency(StrEnum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    BIWEEKLY = "BIWEEKLY"
    MONTHLY = "MONTHLY"


class AuditMitigationActionsExecutionStatus(StrEnum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"
    SKIPPED = "SKIPPED"
    PENDING = "PENDING"


class AuditMitigationActionsTaskStatus(StrEnum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"


class AuditNotificationType(StrEnum):
    SNS = "SNS"


class AuditTaskStatus(StrEnum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"


class AuditTaskType(StrEnum):
    ON_DEMAND_AUDIT_TASK = "ON_DEMAND_AUDIT_TASK"
    SCHEDULED_AUDIT_TASK = "SCHEDULED_AUDIT_TASK"


class AuthDecision(StrEnum):
    ALLOWED = "ALLOWED"
    EXPLICIT_DENY = "EXPLICIT_DENY"
    IMPLICIT_DENY = "IMPLICIT_DENY"


class AuthenticationType(StrEnum):
    CUSTOM_AUTH_X509 = "CUSTOM_AUTH_X509"
    CUSTOM_AUTH = "CUSTOM_AUTH"
    AWS_X509 = "AWS_X509"
    AWS_SIGV4 = "AWS_SIGV4"
    DEFAULT = "DEFAULT"


class AuthorizerStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class AutoRegistrationStatus(StrEnum):
    ENABLE = "ENABLE"
    DISABLE = "DISABLE"


class AwsJobAbortCriteriaAbortAction(StrEnum):
    CANCEL = "CANCEL"


class AwsJobAbortCriteriaFailureType(StrEnum):
    FAILED = "FAILED"
    REJECTED = "REJECTED"
    TIMED_OUT = "TIMED_OUT"
    ALL = "ALL"


class BehaviorCriteriaType(StrEnum):
    STATIC = "STATIC"
    STATISTICAL = "STATISTICAL"
    MACHINE_LEARNING = "MACHINE_LEARNING"


class CACertificateStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class CACertificateUpdateAction(StrEnum):
    DEACTIVATE = "DEACTIVATE"


class CannedAccessControlList(StrEnum):
    private = "private"
    public_read = "public-read"
    public_read_write = "public-read-write"
    aws_exec_read = "aws-exec-read"
    authenticated_read = "authenticated-read"
    bucket_owner_read = "bucket-owner-read"
    bucket_owner_full_control = "bucket-owner-full-control"
    log_delivery_write = "log-delivery-write"


class CertificateMode(StrEnum):
    DEFAULT = "DEFAULT"
    SNI_ONLY = "SNI_ONLY"


class CertificateProviderOperation(StrEnum):
    CreateCertificateFromCsr = "CreateCertificateFromCsr"


class CertificateStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    REVOKED = "REVOKED"
    PENDING_TRANSFER = "PENDING_TRANSFER"
    REGISTER_INACTIVE = "REGISTER_INACTIVE"
    PENDING_ACTIVATION = "PENDING_ACTIVATION"


class CommandExecutionStatus(StrEnum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    REJECTED = "REJECTED"
    TIMED_OUT = "TIMED_OUT"


class CommandNamespace(StrEnum):
    AWS_IoT = "AWS-IoT"
    AWS_IoT_FleetWise = "AWS-IoT-FleetWise"


class ComparisonOperator(StrEnum):
    less_than = "less-than"
    less_than_equals = "less-than-equals"
    greater_than = "greater-than"
    greater_than_equals = "greater-than-equals"
    in_cidr_set = "in-cidr-set"
    not_in_cidr_set = "not-in-cidr-set"
    in_port_set = "in-port-set"
    not_in_port_set = "not-in-port-set"
    in_set = "in-set"
    not_in_set = "not-in-set"


class ConfidenceLevel(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ConfigName(StrEnum):
    CERT_AGE_THRESHOLD_IN_DAYS = "CERT_AGE_THRESHOLD_IN_DAYS"
    CERT_EXPIRATION_THRESHOLD_IN_DAYS = "CERT_EXPIRATION_THRESHOLD_IN_DAYS"


class ConfigurationStatus(StrEnum):
    HEALTHY = "HEALTHY"
    UNHEALTHY = "UNHEALTHY"


class CustomMetricType(StrEnum):
    string_list = "string-list"
    ip_address_list = "ip-address-list"
    number_list = "number-list"
    number = "number"


class DayOfWeek(StrEnum):
    SUN = "SUN"
    MON = "MON"
    TUE = "TUE"
    WED = "WED"
    THU = "THU"
    FRI = "FRI"
    SAT = "SAT"


class DetectMitigationActionExecutionStatus(StrEnum):
    IN_PROGRESS = "IN_PROGRESS"
    SUCCESSFUL = "SUCCESSFUL"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class DetectMitigationActionsTaskStatus(StrEnum):
    IN_PROGRESS = "IN_PROGRESS"
    SUCCESSFUL = "SUCCESSFUL"
    FAILED = "FAILED"
    CANCELED = "CANCELED"


class DeviceCertificateUpdateAction(StrEnum):
    DEACTIVATE = "DEACTIVATE"


class DeviceDefenderIndexingMode(StrEnum):
    OFF = "OFF"
    VIOLATIONS = "VIOLATIONS"


class DimensionType(StrEnum):
    TOPIC_FILTER = "TOPIC_FILTER"


class DimensionValueOperator(StrEnum):
    IN = "IN"
    NOT_IN = "NOT_IN"


class DisconnectReasonValue(StrEnum):
    AUTH_ERROR = "AUTH_ERROR"
    CLIENT_INITIATED_DISCONNECT = "CLIENT_INITIATED_DISCONNECT"
    CLIENT_ERROR = "CLIENT_ERROR"
    CONNECTION_LOST = "CONNECTION_LOST"
    DUPLICATE_CLIENTID = "DUPLICATE_CLIENTID"
    FORBIDDEN_ACCESS = "FORBIDDEN_ACCESS"
    MQTT_KEEP_ALIVE_TIMEOUT = "MQTT_KEEP_ALIVE_TIMEOUT"
    SERVER_ERROR = "SERVER_ERROR"
    SERVER_INITIATED_DISCONNECT = "SERVER_INITIATED_DISCONNECT"
    THROTTLED = "THROTTLED"
    WEBSOCKET_TTL_EXPIRATION = "WEBSOCKET_TTL_EXPIRATION"
    CUSTOMAUTH_TTL_EXPIRATION = "CUSTOMAUTH_TTL_EXPIRATION"
    UNKNOWN = "UNKNOWN"
    NONE = "NONE"


class DomainConfigurationStatus(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class DomainType(StrEnum):
    ENDPOINT = "ENDPOINT"
    AWS_MANAGED = "AWS_MANAGED"
    CUSTOMER_MANAGED = "CUSTOMER_MANAGED"


class DynamicGroupStatus(StrEnum):
    ACTIVE = "ACTIVE"
    BUILDING = "BUILDING"
    REBUILDING = "REBUILDING"


class DynamoKeyType(StrEnum):
    STRING = "STRING"
    NUMBER = "NUMBER"


class EncryptionType(StrEnum):
    CUSTOMER_MANAGED_KMS_KEY = "CUSTOMER_MANAGED_KMS_KEY"
    AWS_OWNED_KMS_KEY = "AWS_OWNED_KMS_KEY"


class EventType(StrEnum):
    THING = "THING"
    THING_GROUP = "THING_GROUP"
    THING_TYPE = "THING_TYPE"
    THING_GROUP_MEMBERSHIP = "THING_GROUP_MEMBERSHIP"
    THING_GROUP_HIERARCHY = "THING_GROUP_HIERARCHY"
    THING_TYPE_ASSOCIATION = "THING_TYPE_ASSOCIATION"
    JOB = "JOB"
    JOB_EXECUTION = "JOB_EXECUTION"
    POLICY = "POLICY"
    CERTIFICATE = "CERTIFICATE"
    CA_CERTIFICATE = "CA_CERTIFICATE"


class FieldType(StrEnum):
    Number = "Number"
    String = "String"
    Boolean = "Boolean"


class FleetMetricUnit(StrEnum):
    Seconds = "Seconds"
    Microseconds = "Microseconds"
    Milliseconds = "Milliseconds"
    Bytes = "Bytes"
    Kilobytes = "Kilobytes"
    Megabytes = "Megabytes"
    Gigabytes = "Gigabytes"
    Terabytes = "Terabytes"
    Bits = "Bits"
    Kilobits = "Kilobits"
    Megabits = "Megabits"
    Gigabits = "Gigabits"
    Terabits = "Terabits"
    Percent = "Percent"
    Count = "Count"
    Bytes_Second = "Bytes/Second"
    Kilobytes_Second = "Kilobytes/Second"
    Megabytes_Second = "Megabytes/Second"
    Gigabytes_Second = "Gigabytes/Second"
    Terabytes_Second = "Terabytes/Second"
    Bits_Second = "Bits/Second"
    Kilobits_Second = "Kilobits/Second"
    Megabits_Second = "Megabits/Second"
    Gigabits_Second = "Gigabits/Second"
    Terabits_Second = "Terabits/Second"
    Count_Second = "Count/Second"
    None_ = "None"


class IndexStatus(StrEnum):
    ACTIVE = "ACTIVE"
    BUILDING = "BUILDING"
    REBUILDING = "REBUILDING"


class JobEndBehavior(StrEnum):
    STOP_ROLLOUT = "STOP_ROLLOUT"
    CANCEL = "CANCEL"
    FORCE_CANCEL = "FORCE_CANCEL"


class JobExecutionFailureType(StrEnum):
    FAILED = "FAILED"
    REJECTED = "REJECTED"
    TIMED_OUT = "TIMED_OUT"
    ALL = "ALL"


class JobExecutionStatus(StrEnum):
    QUEUED = "QUEUED"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    TIMED_OUT = "TIMED_OUT"
    REJECTED = "REJECTED"
    REMOVED = "REMOVED"
    CANCELED = "CANCELED"


class JobStatus(StrEnum):
    IN_PROGRESS = "IN_PROGRESS"
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"
    DELETION_IN_PROGRESS = "DELETION_IN_PROGRESS"
    SCHEDULED = "SCHEDULED"


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    ERROR = "ERROR"
    WARN = "WARN"
    DISABLED = "DISABLED"


class LogTargetType(StrEnum):
    DEFAULT = "DEFAULT"
    THING_GROUP = "THING_GROUP"
    CLIENT_ID = "CLIENT_ID"
    SOURCE_IP = "SOURCE_IP"
    PRINCIPAL_ID = "PRINCIPAL_ID"


class MessageFormat(StrEnum):
    RAW = "RAW"
    JSON = "JSON"


class MitigationActionType(StrEnum):
    UPDATE_DEVICE_CERTIFICATE = "UPDATE_DEVICE_CERTIFICATE"
    UPDATE_CA_CERTIFICATE = "UPDATE_CA_CERTIFICATE"
    ADD_THINGS_TO_THING_GROUP = "ADD_THINGS_TO_THING_GROUP"
    REPLACE_DEFAULT_POLICY_VERSION = "REPLACE_DEFAULT_POLICY_VERSION"
    ENABLE_IOT_LOGGING = "ENABLE_IOT_LOGGING"
    PUBLISH_FINDING_TO_SNS = "PUBLISH_FINDING_TO_SNS"


class ModelStatus(StrEnum):
    PENDING_BUILD = "PENDING_BUILD"
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"


class NamedShadowIndexingMode(StrEnum):
    OFF = "OFF"
    ON = "ON"


class OTAUpdateStatus(StrEnum):
    CREATE_PENDING = "CREATE_PENDING"
    CREATE_IN_PROGRESS = "CREATE_IN_PROGRESS"
    CREATE_COMPLETE = "CREATE_COMPLETE"
    CREATE_FAILED = "CREATE_FAILED"
    DELETE_IN_PROGRESS = "DELETE_IN_PROGRESS"
    DELETE_FAILED = "DELETE_FAILED"


class PackageVersionAction(StrEnum):
    PUBLISH = "PUBLISH"
    DEPRECATE = "DEPRECATE"


class PackageVersionStatus(StrEnum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    DEPRECATED = "DEPRECATED"


class PolicyTemplateName(StrEnum):
    BLANK_POLICY = "BLANK_POLICY"


class Protocol(StrEnum):
    MQTT = "MQTT"
    HTTP = "HTTP"


class ReportType(StrEnum):
    ERRORS = "ERRORS"
    RESULTS = "RESULTS"


class ResourceType(StrEnum):
    DEVICE_CERTIFICATE = "DEVICE_CERTIFICATE"
    CA_CERTIFICATE = "CA_CERTIFICATE"
    IOT_POLICY = "IOT_POLICY"
    COGNITO_IDENTITY_POOL = "COGNITO_IDENTITY_POOL"
    CLIENT_ID = "CLIENT_ID"
    ACCOUNT_SETTINGS = "ACCOUNT_SETTINGS"
    ROLE_ALIAS = "ROLE_ALIAS"
    IAM_ROLE = "IAM_ROLE"
    ISSUER_CERTIFICATE = "ISSUER_CERTIFICATE"


class RetryableFailureType(StrEnum):
    FAILED = "FAILED"
    TIMED_OUT = "TIMED_OUT"
    ALL = "ALL"


class SbomValidationErrorCode(StrEnum):
    INCOMPATIBLE_FORMAT = "INCOMPATIBLE_FORMAT"
    FILE_SIZE_LIMIT_EXCEEDED = "FILE_SIZE_LIMIT_EXCEEDED"


class SbomValidationResult(StrEnum):
    FAILED = "FAILED"
    SUCCEEDED = "SUCCEEDED"


class SbomValidationStatus(StrEnum):
    IN_PROGRESS = "IN_PROGRESS"
    FAILED = "FAILED"
    SUCCEEDED = "SUCCEEDED"


class ServerCertificateStatus(StrEnum):
    INVALID = "INVALID"
    VALID = "VALID"


class ServiceType(StrEnum):
    DATA = "DATA"
    CREDENTIAL_PROVIDER = "CREDENTIAL_PROVIDER"
    JOBS = "JOBS"


class SortOrder(StrEnum):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


class Status(StrEnum):
    InProgress = "InProgress"
    Completed = "Completed"
    Failed = "Failed"
    Cancelled = "Cancelled"
    Cancelling = "Cancelling"


class TargetFieldOrder(StrEnum):
    LatLon = "LatLon"
    LonLat = "LonLat"


class TargetSelection(StrEnum):
    CONTINUOUS = "CONTINUOUS"
    SNAPSHOT = "SNAPSHOT"


class TemplateType(StrEnum):
    FLEET_PROVISIONING = "FLEET_PROVISIONING"
    JITP = "JITP"


class ThingConnectivityIndexingMode(StrEnum):
    OFF = "OFF"
    STATUS = "STATUS"


class ThingGroupIndexingMode(StrEnum):
    OFF = "OFF"
    ON = "ON"


class ThingIndexingMode(StrEnum):
    OFF = "OFF"
    REGISTRY = "REGISTRY"
    REGISTRY_AND_SHADOW = "REGISTRY_AND_SHADOW"


class ThingPrincipalType(StrEnum):
    EXCLUSIVE_THING = "EXCLUSIVE_THING"
    NON_EXCLUSIVE_THING = "NON_EXCLUSIVE_THING"


class TopicRuleDestinationStatus(StrEnum):
    ENABLED = "ENABLED"
    IN_PROGRESS = "IN_PROGRESS"
    DISABLED = "DISABLED"
    ERROR = "ERROR"
    DELETING = "DELETING"


class VerificationState(StrEnum):
    FALSE_POSITIVE = "FALSE_POSITIVE"
    BENIGN_POSITIVE = "BENIGN_POSITIVE"
    TRUE_POSITIVE = "TRUE_POSITIVE"
    UNKNOWN = "UNKNOWN"


class ViolationEventType(StrEnum):
    in_alarm = "in-alarm"
    alarm_cleared = "alarm-cleared"
    alarm_invalidated = "alarm-invalidated"


class CertificateConflictException(ServiceException):
    """Unable to verify the CA certificate used to sign the device certificate
    you are attempting to register. This is happens when you have registered
    more than one CA certificate that has the same subject field and public
    key.
    """

    code: str = "CertificateConflictException"
    sender_fault: bool = False
    status_code: int = 409


class CertificateStateException(ServiceException):
    """The certificate operation is not allowed."""

    code: str = "CertificateStateException"
    sender_fault: bool = False
    status_code: int = 406


class CertificateValidationException(ServiceException):
    """The certificate is invalid."""

    code: str = "CertificateValidationException"
    sender_fault: bool = False
    status_code: int = 400


class ConflictException(ServiceException):
    """The request conflicts with the current state of the resource."""

    code: str = "ConflictException"
    sender_fault: bool = False
    status_code: int = 409
    resourceId: resourceId | None


class ConflictingResourceUpdateException(ServiceException):
    """A conflicting resource update exception. This exception is thrown when
    two pending updates cause a conflict.
    """

    code: str = "ConflictingResourceUpdateException"
    sender_fault: bool = False
    status_code: int = 409


class DeleteConflictException(ServiceException):
    """You can't delete the resource because it is attached to one or more
    resources.
    """

    code: str = "DeleteConflictException"
    sender_fault: bool = False
    status_code: int = 409


class IndexNotReadyException(ServiceException):
    """The index is not ready."""

    code: str = "IndexNotReadyException"
    sender_fault: bool = False
    status_code: int = 400


class InternalException(ServiceException):
    """An unexpected error has occurred."""

    code: str = "InternalException"
    sender_fault: bool = False
    status_code: int = 500


class InternalFailureException(ServiceException):
    """An unexpected error has occurred."""

    code: str = "InternalFailureException"
    sender_fault: bool = False
    status_code: int = 500


class InternalServerException(ServiceException):
    """Internal error from the service that indicates an unexpected error or
    that the service is unavailable.
    """

    code: str = "InternalServerException"
    sender_fault: bool = False
    status_code: int = 500


class InvalidAggregationException(ServiceException):
    """The aggregation is invalid."""

    code: str = "InvalidAggregationException"
    sender_fault: bool = False
    status_code: int = 400


class InvalidQueryException(ServiceException):
    """The query is invalid."""

    code: str = "InvalidQueryException"
    sender_fault: bool = False
    status_code: int = 400


class InvalidRequestException(ServiceException):
    """The request is not valid."""

    code: str = "InvalidRequestException"
    sender_fault: bool = False
    status_code: int = 400


class InvalidResponseException(ServiceException):
    """The response is invalid."""

    code: str = "InvalidResponseException"
    sender_fault: bool = False
    status_code: int = 400


class InvalidStateTransitionException(ServiceException):
    """An attempt was made to change to an invalid state, for example by
    deleting a job or a job execution which is "IN_PROGRESS" without setting
    the ``force`` parameter.
    """

    code: str = "InvalidStateTransitionException"
    sender_fault: bool = False
    status_code: int = 409


class LimitExceededException(ServiceException):
    """A limit has been exceeded."""

    code: str = "LimitExceededException"
    sender_fault: bool = False
    status_code: int = 410


class MalformedPolicyException(ServiceException):
    """The policy documentation is not valid."""

    code: str = "MalformedPolicyException"
    sender_fault: bool = False
    status_code: int = 400


class NotConfiguredException(ServiceException):
    """The resource is not configured."""

    code: str = "NotConfiguredException"
    sender_fault: bool = False
    status_code: int = 404


class RegistrationCodeValidationException(ServiceException):
    """The registration code is invalid."""

    code: str = "RegistrationCodeValidationException"
    sender_fault: bool = False
    status_code: int = 400


class ResourceAlreadyExistsException(ServiceException):
    """The resource already exists."""

    code: str = "ResourceAlreadyExistsException"
    sender_fault: bool = False
    status_code: int = 409
    resourceId: resourceId | None
    resourceArn: resourceArn | None


class ResourceNotFoundException(ServiceException):
    """The specified resource does not exist."""

    code: str = "ResourceNotFoundException"
    sender_fault: bool = False
    status_code: int = 404


class ResourceRegistrationFailureException(ServiceException):
    """The resource registration failed."""

    code: str = "ResourceRegistrationFailureException"
    sender_fault: bool = False
    status_code: int = 400


class ServiceQuotaExceededException(ServiceException):
    """Service quota has been exceeded."""

    code: str = "ServiceQuotaExceededException"
    sender_fault: bool = False
    status_code: int = 402


class ServiceUnavailableException(ServiceException):
    """The service is temporarily unavailable."""

    code: str = "ServiceUnavailableException"
    sender_fault: bool = False
    status_code: int = 503


class SqlParseException(ServiceException):
    """The Rule-SQL expression can't be parsed correctly."""

    code: str = "SqlParseException"
    sender_fault: bool = False
    status_code: int = 400


class TaskAlreadyExistsException(ServiceException):
    """This exception occurs if you attempt to start a task with the same
    task-id as an existing task but with a different clientRequestToken.
    """

    code: str = "TaskAlreadyExistsException"
    sender_fault: bool = False
    status_code: int = 400


class ThrottlingException(ServiceException):
    """The rate exceeds the limit."""

    code: str = "ThrottlingException"
    sender_fault: bool = False
    status_code: int = 400


class TransferAlreadyCompletedException(ServiceException):
    """You can't revert the certificate transfer because the transfer is
    already complete.
    """

    code: str = "TransferAlreadyCompletedException"
    sender_fault: bool = False
    status_code: int = 410


class TransferConflictException(ServiceException):
    """You can't transfer the certificate because authorization policies are
    still attached.
    """

    code: str = "TransferConflictException"
    sender_fault: bool = False
    status_code: int = 409


class UnauthorizedException(ServiceException):
    """You are not authorized to perform this operation."""

    code: str = "UnauthorizedException"
    sender_fault: bool = False
    status_code: int = 401


class ValidationException(ServiceException):
    """The request is not valid."""

    code: str = "ValidationException"
    sender_fault: bool = False
    status_code: int = 400


class VersionConflictException(ServiceException):
    """An exception thrown when the version of an entity specified with the
    ``expectedVersion`` parameter does not match the latest version in the
    system.
    """

    code: str = "VersionConflictException"
    sender_fault: bool = False
    status_code: int = 409


class VersionsLimitExceededException(ServiceException):
    """The number of policy versions exceeds the limit."""

    code: str = "VersionsLimitExceededException"
    sender_fault: bool = False
    status_code: int = 409


class AbortCriteria(TypedDict, total=False):
    """The criteria that determine when and how a job abort takes place."""

    failureType: JobExecutionFailureType
    action: AbortAction
    thresholdPercentage: AbortThresholdPercentage
    minNumberOfExecutedThings: MinimumNumberOfExecutedThings


AbortCriteriaList = list[AbortCriteria]


class AbortConfig(TypedDict, total=False):
    """The criteria that determine when and how a job abort takes place."""

    criteriaList: AbortCriteriaList


class AcceptCertificateTransferRequest(ServiceRequest):
    """The input for the AcceptCertificateTransfer operation."""

    certificateId: CertificateId
    setAsActive: SetAsActive | None


class LocationTimestamp(TypedDict, total=False):
    """Describes how to interpret an application-defined timestamp value from
    an MQTT message payload and the precision of that value.
    """

    value: String
    unit: String | None


class LocationAction(TypedDict, total=False):
    """The Amazon Location rule action sends device location updates from an
    MQTT message to an Amazon Location tracker resource.
    """

    roleArn: AwsArn
    trackerName: String
    deviceId: String
    timestamp: LocationTimestamp | None
    latitude: String
    longitude: String


class OpenSearchAction(TypedDict, total=False):
    roleArn: AwsArn
    endpoint: ElasticsearchEndpoint
    index: ElasticsearchIndex
    type: ElasticsearchType
    id: ElasticsearchId


class KafkaActionHeader(TypedDict, total=False):
    """Specifies a Kafka header using key-value pairs when you create a Rule’s
    Kafka Action. You can use these headers to route data from IoT clients
    to downstream Kafka clusters without modifying your message payload.

    For more information about Rule's Kafka action, see `Apache
    Kafka <https://docs.aws.amazon.com/iot/latest/developerguide/apache-kafka-rule-action.html>`__.
    """

    key: KafkaHeaderKey
    value: KafkaHeaderValue


KafkaHeaders = list[KafkaActionHeader]
ClientProperties = dict[String, String]


class KafkaAction(TypedDict, total=False):
    """Send messages to an Amazon Managed Streaming for Apache Kafka (Amazon
    MSK) or self-managed Apache Kafka cluster.
    """

    destinationArn: AwsArn
    topic: String
    key: String | None
    partition: String | None
    clientProperties: ClientProperties
    headers: KafkaHeaders | None


class SigV4Authorization(TypedDict, total=False):
    """For more information, see `Signature Version 4 signing
    process <https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html>`__.
    """

    signingRegion: SigningRegion
    serviceName: ServiceName
    roleArn: AwsArn


class HttpAuthorization(TypedDict, total=False):
    """The authorization method used to send messages."""

    sigv4: SigV4Authorization | None


class HttpActionHeader(TypedDict, total=False):
    """The HTTP action header."""

    key: HeaderKey
    value: HeaderValue


HeaderList = list[HttpActionHeader]


class HttpAction(TypedDict, total=False):
    """Send data to an HTTPS endpoint."""

    url: Url
    confirmationUrl: Url | None
    headers: HeaderList | None
    auth: HttpAuthorization | None


class TimestreamTimestamp(TypedDict, total=False):
    """Describes how to interpret an application-defined timestamp value from
    an MQTT message payload and the precision of that value.
    """

    value: TimestreamTimestampValue
    unit: TimestreamTimestampUnit


class TimestreamDimension(TypedDict, total=False):
    """Metadata attributes of the time series that are written in each measure
    record.
    """

    name: TimestreamDimensionName
    value: TimestreamDimensionValue


TimestreamDimensionList = list[TimestreamDimension]


class TimestreamAction(TypedDict, total=False):
    """The Timestream rule action writes attributes (measures) from an MQTT
    message into an Amazon Timestream table. For more information, see the
    `Timestream <https://docs.aws.amazon.com/iot/latest/developerguide/timestream-rule-action.html>`__
    topic rule action documentation.
    """

    roleArn: AwsArn
    databaseName: TimestreamDatabaseName
    tableName: TimestreamTableName
    dimensions: TimestreamDimensionList
    timestamp: TimestreamTimestamp | None


class StepFunctionsAction(TypedDict, total=False):
    """Starts execution of a Step Functions state machine."""

    executionNamePrefix: ExecutionNamePrefix | None
    stateMachineName: StateMachineName
    roleArn: AwsArn


class AssetPropertyTimestamp(TypedDict, total=False):
    """An asset property timestamp entry containing the following information."""

    timeInSeconds: AssetPropertyTimeInSeconds
    offsetInNanos: AssetPropertyOffsetInNanos | None


class AssetPropertyVariant(TypedDict, total=False):
    """Contains an asset property value (of a single type)."""

    stringValue: AssetPropertyStringValue | None
    integerValue: AssetPropertyIntegerValue | None
    doubleValue: AssetPropertyDoubleValue | None
    booleanValue: AssetPropertyBooleanValue | None


class AssetPropertyValue(TypedDict, total=False):
    """An asset property value entry containing the following information."""

    value: AssetPropertyVariant
    timestamp: AssetPropertyTimestamp
    quality: AssetPropertyQuality | None


AssetPropertyValueList = list[AssetPropertyValue]


class PutAssetPropertyValueEntry(TypedDict, total=False):
    """An asset property value entry containing the following information."""

    entryId: AssetPropertyEntryId | None
    assetId: AssetId | None
    propertyId: AssetPropertyId | None
    propertyAlias: AssetPropertyAlias | None
    propertyValues: AssetPropertyValueList


PutAssetPropertyValueEntryList = list[PutAssetPropertyValueEntry]


class IotSiteWiseAction(TypedDict, total=False):
    """Describes an action to send data from an MQTT message that triggered the
    rule to IoT SiteWise asset properties.
    """

    putAssetPropertyValueEntries: PutAssetPropertyValueEntryList
    roleArn: AwsArn


class IotEventsAction(TypedDict, total=False):
    """Sends an input to an IoT Events detector."""

    inputName: InputName
    messageId: MessageId | None
    batchMode: BatchMode | None
    roleArn: AwsArn


class IotAnalyticsAction(TypedDict, total=False):
    """Sends message data to an IoT Analytics channel."""

    channelArn: AwsArn | None
    channelName: ChannelName | None
    batchMode: BatchMode | None
    roleArn: AwsArn | None


class SalesforceAction(TypedDict, total=False):
    """Describes an action to write a message to a Salesforce IoT Cloud Input
    Stream.
    """

    token: SalesforceToken
    url: SalesforceEndpoint


class ElasticsearchAction(TypedDict, total=False):
    roleArn: AwsArn
    endpoint: ElasticsearchEndpoint
    index: ElasticsearchIndex
    type: ElasticsearchType
    id: ElasticsearchId


class CloudwatchLogsAction(TypedDict, total=False):
    """Describes an action that sends data to CloudWatch Logs."""

    roleArn: AwsArn
    logGroupName: LogGroupName
    batchMode: BatchMode | None


class CloudwatchAlarmAction(TypedDict, total=False):
    """Describes an action that updates a CloudWatch alarm."""

    roleArn: AwsArn
    alarmName: AlarmName
    stateReason: StateReason
    stateValue: StateValue


class CloudwatchMetricAction(TypedDict, total=False):
    """Describes an action that captures a CloudWatch metric."""

    roleArn: AwsArn
    metricNamespace: String
    metricName: String
    metricValue: String
    metricUnit: String
    metricTimestamp: String | None


class FirehoseAction(TypedDict, total=False):
    """Describes an action that writes data to an Amazon Kinesis Firehose
    stream.
    """

    roleArn: AwsArn
    deliveryStreamName: DeliveryStreamName
    separator: FirehoseSeparator | None
    batchMode: BatchMode | None


class S3Action(TypedDict, total=False):
    """Describes an action to write data to an Amazon S3 bucket."""

    roleArn: AwsArn
    bucketName: BucketName
    key: Key
    cannedAcl: CannedAccessControlList | None


class UserProperty(TypedDict, total=False):
    """A key-value pair that you define in the header. Both the key and the
    value are either literal strings or valid `substitution
    templates <https://docs.aws.amazon.com/iot/latest/developerguide/iot-substitution-templates.html>`__.
    """

    key: UserPropertyKey
    value: UserPropertyValue


UserProperties = list[UserProperty]


class MqttHeaders(TypedDict, total=False):
    """Specifies MQTT Version 5.0 headers information. For more information,
    see
    `MQTT <https://docs.aws.amazon.com/iot/latest/developerguide/mqtt.html>`__
    from Amazon Web Services IoT Core Developer Guide.
    """

    payloadFormatIndicator: PayloadFormatIndicator | None
    contentType: ContentType | None
    responseTopic: ResponseTopic | None
    correlationData: CorrelationData | None
    messageExpiry: MessageExpiry | None
    userProperties: UserProperties | None


class RepublishAction(TypedDict, total=False):
    """Describes an action to republish to another topic."""

    roleArn: AwsArn
    topic: TopicPattern
    qos: Qos | None
    headers: MqttHeaders | None


class KinesisAction(TypedDict, total=False):
    """Describes an action to write data to an Amazon Kinesis stream."""

    roleArn: AwsArn
    streamName: StreamName
    partitionKey: PartitionKey | None


class SqsAction(TypedDict, total=False):
    """Describes an action to publish data to an Amazon SQS queue."""

    roleArn: AwsArn
    queueUrl: QueueUrl
    useBase64: UseBase64 | None


class SnsAction(TypedDict, total=False):
    """Describes an action to publish to an Amazon SNS topic."""

    targetArn: AwsArn
    roleArn: AwsArn
    messageFormat: MessageFormat | None


class LambdaAction(TypedDict, total=False):
    """Describes an action to invoke a Lambda function."""

    functionArn: FunctionArn


class PutItemInput(TypedDict, total=False):
    """The input for the DynamoActionVS action that specifies the DynamoDB
    table to which the message data will be written.
    """

    tableName: TableName


class DynamoDBv2Action(TypedDict, total=False):
    """Describes an action to write to a DynamoDB table.

    This DynamoDB action writes each attribute in the message payload into
    it's own column in the DynamoDB table.
    """

    roleArn: AwsArn
    putItem: PutItemInput


class DynamoDBAction(TypedDict, total=False):
    """Describes an action to write to a DynamoDB table.

    The ``tableName``, ``hashKeyField``, and ``rangeKeyField`` values must
    match the values used when you created the table.

    The ``hashKeyValue`` and ``rangeKeyvalue`` fields use a substitution
    template syntax. These templates provide data at runtime. The syntax is
    as follows: ${*sql-expression*}.

    You can specify any valid expression in a WHERE or SELECT clause,
    including JSON properties, comparisons, calculations, and functions. For
    example, the following field uses the third level of the topic:

    ``"hashKeyValue": "${topic(3)}"``

    The following field uses the timestamp:

    ``"rangeKeyValue": "${timestamp()}"``
    """

    tableName: TableName
    roleArn: AwsArn
    operation: DynamoOperation | None
    hashKeyField: HashKeyField
    hashKeyValue: HashKeyValue
    hashKeyType: DynamoKeyType | None
    rangeKeyField: RangeKeyField | None
    rangeKeyValue: RangeKeyValue | None
    rangeKeyType: DynamoKeyType | None
    payloadField: PayloadField | None


Action = TypedDict(
    "Action",
    {
        "dynamoDB": DynamoDBAction | None,
        "dynamoDBv2": DynamoDBv2Action | None,
        "lambda": LambdaAction | None,
        "sns": SnsAction | None,
        "sqs": SqsAction | None,
        "kinesis": KinesisAction | None,
        "republish": RepublishAction | None,
        "s3": S3Action | None,
        "firehose": FirehoseAction | None,
        "cloudwatchMetric": CloudwatchMetricAction | None,
        "cloudwatchAlarm": CloudwatchAlarmAction | None,
        "cloudwatchLogs": CloudwatchLogsAction | None,
        "elasticsearch": ElasticsearchAction | None,
        "salesforce": SalesforceAction | None,
        "iotAnalytics": IotAnalyticsAction | None,
        "iotEvents": IotEventsAction | None,
        "iotSiteWise": IotSiteWiseAction | None,
        "stepFunctions": StepFunctionsAction | None,
        "timestream": TimestreamAction | None,
        "http": HttpAction | None,
        "kafka": KafkaAction | None,
        "openSearch": OpenSearchAction | None,
        "location": LocationAction | None,
    },
    total=False,
)
ActionList = list[Action]
Timestamp = datetime


class ViolationEventAdditionalInfo(TypedDict, total=False):
    """The details of a violation event."""

    confidenceLevel: ConfidenceLevel | None


StringList = list[stringValue]
NumberList = list[Number]
Ports = list[Port]
Cidrs = list[Cidr]
UnsignedLong = int


class MetricValue(TypedDict, total=False):
    """The value to be compared with the ``metric``."""

    count: UnsignedLong | None
    cidrs: Cidrs | None
    ports: Ports | None
    number: Number | None
    numbers: NumberList | None
    strings: StringList | None


class MachineLearningDetectionConfig(TypedDict, total=False):
    """The configuration of an ML Detect Security Profile."""

    confidenceLevel: ConfidenceLevel


class StatisticalThreshold(TypedDict, total=False):
    """A statistical ranking (percentile) that indicates a threshold value by
    which a behavior is determined to be in compliance or in violation of
    the behavior.
    """

    statistic: EvaluationStatistic | None


class BehaviorCriteria(TypedDict, total=False):
    """The criteria by which the behavior is determined to be normal."""

    comparisonOperator: ComparisonOperator | None
    value: MetricValue | None
    durationSeconds: DurationSeconds | None
    consecutiveDatapointsToAlarm: ConsecutiveDatapointsToAlarm | None
    consecutiveDatapointsToClear: ConsecutiveDatapointsToClear | None
    statisticalThreshold: StatisticalThreshold | None
    mlDetectionConfig: MachineLearningDetectionConfig | None


class MetricDimension(TypedDict, total=False):
    """The dimension of a metric."""

    dimensionName: DimensionName
    operator: DimensionValueOperator | None


class Behavior(TypedDict, total=False):
    """A Device Defender security profile behavior."""

    name: BehaviorName
    metric: BehaviorMetric | None
    metricDimension: MetricDimension | None
    criteria: BehaviorCriteria | None
    suppressAlerts: SuppressAlerts | None
    exportMetric: ExportMetric | None


class ActiveViolation(TypedDict, total=False):
    """Information about an active Device Defender security profile behavior
    violation.
    """

    violationId: ViolationId | None
    thingName: DeviceDefenderThingName | None
    securityProfileName: SecurityProfileName | None
    behavior: Behavior | None
    lastViolationValue: MetricValue | None
    violationEventAdditionalInfo: ViolationEventAdditionalInfo | None
    verificationState: VerificationState | None
    verificationStateDescription: VerificationStateDescription | None
    lastViolationTime: Timestamp | None
    violationStartTime: Timestamp | None


ActiveViolations = list[ActiveViolation]


class AddThingToBillingGroupRequest(ServiceRequest):
    billingGroupName: BillingGroupName | None
    billingGroupArn: BillingGroupArn | None
    thingName: ThingName | None
    thingArn: ThingArn | None


class AddThingToBillingGroupResponse(TypedDict, total=False):
    pass


class AddThingToThingGroupRequest(ServiceRequest):
    thingGroupName: ThingGroupName | None
    thingGroupArn: ThingGroupArn | None
    thingName: ThingName | None
    thingArn: ThingArn | None
    overrideDynamicGroups: OverrideDynamicGroups | None


class AddThingToThingGroupResponse(TypedDict, total=False):
    pass


ThingGroupNames = list[ThingGroupName]


class AddThingsToThingGroupParams(TypedDict, total=False):
    """Parameters used when defining a mitigation action that move a set of
    things to a thing group.
    """

    thingGroupNames: ThingGroupNames
    overrideDynamicGroups: NullableBoolean | None


AdditionalMetricsToRetainList = list[BehaviorMetric]


class MetricToRetain(TypedDict, total=False):
    """The metric you want to retain. Dimensions are optional."""

    metric: BehaviorMetric
    metricDimension: MetricDimension | None
    exportMetric: ExportMetric | None


AdditionalMetricsToRetainV2List = list[MetricToRetain]
AdditionalParameterMap = dict[AttributeKey, Value]
AggregationTypeValues = list[AggregationTypeValue]


class AggregationType(TypedDict, total=False):
    """The type of aggregation queries."""

    name: AggregationTypeName
    values: AggregationTypeValues | None


class AlertTarget(TypedDict, total=False):
    """A structure containing the alert target ARN and the role ARN."""

    alertTargetArn: AlertTargetArn
    roleArn: RoleArn


AlertTargets = dict[AlertTargetType, AlertTarget]


class Policy(TypedDict, total=False):
    """Describes an IoT policy."""

    policyName: PolicyName | None
    policyArn: PolicyArn | None


Policies = list[Policy]


class Allowed(TypedDict, total=False):
    """Contains information that allowed the authorization."""

    policies: Policies | None


ApproximateSecondsBeforeTimedOut = int


class S3Location(TypedDict, total=False):
    """The S3 location."""

    bucket: S3Bucket | None
    key: S3Key | None
    version: S3Version | None


class Sbom(TypedDict, total=False):
    """A specific software bill of matrerials associated with a software
    package version.
    """

    s3Location: S3Location | None


class AssociateSbomWithPackageVersionRequest(ServiceRequest):
    packageName: PackageName
    versionName: VersionName
    sbom: Sbom
    clientToken: ClientToken | None


class AssociateSbomWithPackageVersionResponse(TypedDict, total=False):
    packageName: PackageName | None
    versionName: VersionName | None
    sbom: Sbom | None
    sbomValidationStatus: SbomValidationStatus | None


JobTargets = list[TargetArn]


class AssociateTargetsWithJobRequest(ServiceRequest):
    targets: JobTargets
    jobId: JobId
    comment: Comment | None
    namespaceId: NamespaceId | None


class AssociateTargetsWithJobResponse(TypedDict, total=False):
    jobArn: JobArn | None
    jobId: JobId | None
    description: JobDescription | None


class AttachPolicyRequest(ServiceRequest):
    policyName: PolicyName
    target: PolicyTarget


class AttachPrincipalPolicyRequest(ServiceRequest):
    """The input for the AttachPrincipalPolicy operation."""

    policyName: PolicyName
    principal: Principal


class AttachSecurityProfileRequest(ServiceRequest):
    securityProfileName: SecurityProfileName
    securityProfileTargetArn: SecurityProfileTargetArn


class AttachSecurityProfileResponse(TypedDict, total=False):
    pass


class AttachThingPrincipalRequest(ServiceRequest):
    """The input for the AttachThingPrincipal operation."""

    thingName: ThingName
    principal: Principal
    thingPrincipalType: ThingPrincipalType | None


class AttachThingPrincipalResponse(TypedDict, total=False):
    """The output from the AttachThingPrincipal operation."""

    pass


Attributes = dict[AttributeName, AttributeValue]


class AttributePayload(TypedDict, total=False):
    """The attribute payload."""

    attributes: Attributes | None
    merge: Flag | None


AttributesMap = dict[AttributeKey, Value]
CheckCustomConfiguration = dict[ConfigName, ConfigValue]


class AuditCheckConfiguration(TypedDict, total=False):
    """Which audit checks are enabled and disabled for this account."""

    enabled: Enabled | None
    configuration: CheckCustomConfiguration | None


AuditCheckConfigurations = dict[AuditCheckName, AuditCheckConfiguration]
SuppressedNonCompliantResourcesCount = int
NonCompliantResourcesCount = int
TotalResourcesCount = int


class AuditCheckDetails(TypedDict, total=False):
    """Information about the audit check."""

    checkRunStatus: AuditCheckRunStatus | None
    checkCompliant: CheckCompliant | None
    totalResourcesCount: TotalResourcesCount | None
    nonCompliantResourcesCount: NonCompliantResourcesCount | None
    suppressedNonCompliantResourcesCount: SuppressedNonCompliantResourcesCount | None
    errorCode: ErrorCode | None
    message: ErrorMessage | None


MitigationActionNameList = list[MitigationActionName]
AuditCheckToActionsMapping = dict[AuditCheckName, MitigationActionNameList]
ReasonForNonComplianceCodes = list[ReasonForNonComplianceCode]
AuditCheckToReasonCodeFilter = dict[AuditCheckName, ReasonForNonComplianceCodes]
AuditDetails = dict[AuditCheckName, AuditCheckDetails]
StringMap = dict[String, String]


class IssuerCertificateIdentifier(TypedDict, total=False):
    """The certificate issuer indentifier."""

    issuerCertificateSubject: IssuerCertificateSubject | None
    issuerId: IssuerId | None
    issuerCertificateSerialNumber: IssuerCertificateSerialNumber | None


class PolicyVersionIdentifier(TypedDict, total=False):
    """Information about the version of the policy associated with the
    resource.
    """

    policyName: PolicyName | None
    policyVersionId: PolicyVersionId | None


class ResourceIdentifier(TypedDict, total=False):
    """Information that identifies the noncompliant resource."""

    deviceCertificateId: CertificateId | None
    caCertificateId: CertificateId | None
    cognitoIdentityPoolId: CognitoIdentityPoolId | None
    clientId: ClientId | None
    policyVersionIdentifier: PolicyVersionIdentifier | None
    account: AwsAccountId | None
    iamRoleArn: RoleArn | None
    roleAliasArn: RoleAliasArn | None
    issuerCertificateIdentifier: IssuerCertificateIdentifier | None
    deviceCertificateArn: CertificateArn | None


class RelatedResource(TypedDict, total=False):
    """Information about a related resource."""

    resourceType: ResourceType | None
    resourceIdentifier: ResourceIdentifier | None
    additionalInfo: StringMap | None


RelatedResources = list[RelatedResource]


class NonCompliantResource(TypedDict, total=False):
    """Information about the resource that was noncompliant with the audit
    check.
    """

    resourceType: ResourceType | None
    resourceIdentifier: ResourceIdentifier | None
    additionalInfo: StringMap | None


class AuditFinding(TypedDict, total=False):
    """The findings (results) of the audit."""

    findingId: FindingId | None
    taskId: AuditTaskId | None
    checkName: AuditCheckName | None
    taskStartTime: Timestamp | None
    findingTime: Timestamp | None
    severity: AuditFindingSeverity | None
    nonCompliantResource: NonCompliantResource | None
    relatedResources: RelatedResources | None
    reasonForNonCompliance: ReasonForNonCompliance | None
    reasonForNonComplianceCode: ReasonForNonComplianceCode | None
    isSuppressed: IsSuppressed | None


AuditFindings = list[AuditFinding]


class AuditMitigationActionExecutionMetadata(TypedDict, total=False):
    """Returned by ListAuditMitigationActionsTask, this object contains
    information that describes a mitigation action that has been started.
    """

    taskId: MitigationActionsTaskId | None
    findingId: FindingId | None
    actionName: MitigationActionName | None
    actionId: MitigationActionId | None
    status: AuditMitigationActionsExecutionStatus | None
    startTime: Timestamp | None
    endTime: Timestamp | None
    errorCode: ErrorCode | None
    message: ErrorMessage | None


AuditMitigationActionExecutionMetadataList = list[AuditMitigationActionExecutionMetadata]


class AuditMitigationActionsTaskMetadata(TypedDict, total=False):
    """Information about an audit mitigation actions task that is returned by
    ``ListAuditMitigationActionsTasks``.
    """

    taskId: MitigationActionsTaskId | None
    startTime: Timestamp | None
    taskStatus: AuditMitigationActionsTaskStatus | None


AuditMitigationActionsTaskMetadataList = list[AuditMitigationActionsTaskMetadata]
CanceledFindingsCount = int
SkippedFindingsCount = int
SucceededFindingsCount = int
FailedFindingsCount = int
TotalFindingsCount = int


class TaskStatisticsForAuditCheck(TypedDict, total=False):
    """Provides summary counts of how many tasks for findings are in a
    particular state. This information is included in the response from
    DescribeAuditMitigationActionsTask.
    """

    totalFindingsCount: TotalFindingsCount | None
    failedFindingsCount: FailedFindingsCount | None
    succeededFindingsCount: SucceededFindingsCount | None
    skippedFindingsCount: SkippedFindingsCount | None
    canceledFindingsCount: CanceledFindingsCount | None


AuditMitigationActionsTaskStatistics = dict[AuditCheckName, TaskStatisticsForAuditCheck]
FindingIds = list[FindingId]


class AuditMitigationActionsTaskTarget(TypedDict, total=False):
    """Used in MitigationActionParams, this information identifies the target
    findings to which the mitigation actions are applied. Only one entry
    appears.
    """

    auditTaskId: AuditTaskId | None
    findingIds: FindingIds | None
    auditCheckToReasonCodeFilter: AuditCheckToReasonCodeFilter | None


class AuditNotificationTarget(TypedDict, total=False):
    """Information about the targets to which audit notifications are sent."""

    targetArn: TargetArn | None
    roleArn: RoleArn | None
    enabled: Enabled | None


AuditNotificationTargetConfigurations = dict[AuditNotificationType, AuditNotificationTarget]


class AuditSuppression(TypedDict, total=False):
    """Filters out specific findings of a Device Defender audit."""

    checkName: AuditCheckName
    resourceIdentifier: ResourceIdentifier
    expirationDate: Timestamp | None
    suppressIndefinitely: SuppressIndefinitely | None
    description: AuditDescription | None


AuditSuppressionList = list[AuditSuppression]


class AuditTaskMetadata(TypedDict, total=False):
    """The audits that were performed."""

    taskId: AuditTaskId | None
    taskStatus: AuditTaskStatus | None
    taskType: AuditTaskType | None


AuditTaskMetadataList = list[AuditTaskMetadata]
Resources = list[Resource]


class AuthInfo(TypedDict, total=False):
    """A collection of authorization information."""

    actionType: ActionType | None
    resources: Resources


AuthInfos = list[AuthInfo]
MissingContextValues = list[MissingContextValue]


class ExplicitDeny(TypedDict, total=False):
    """Information that explicitly denies authorization."""

    policies: Policies | None


class ImplicitDeny(TypedDict, total=False):
    """Information that implicitly denies authorization. When policy doesn't
    explicitly deny or allow an action on a resource it is considered an
    implicit deny.
    """

    policies: Policies | None


class Denied(TypedDict, total=False):
    """Contains information that denied the authorization."""

    implicitDeny: ImplicitDeny | None
    explicitDeny: ExplicitDeny | None


class AuthResult(TypedDict, total=False):
    """The authorizer result."""

    authInfo: AuthInfo | None
    allowed: Allowed | None
    denied: Denied | None
    authDecision: AuthDecision | None
    missingContextValues: MissingContextValues | None


AuthResults = list[AuthResult]


class AuthorizerConfig(TypedDict, total=False):
    """An object that specifies the authorization service for a domain."""

    defaultAuthorizerName: AuthorizerName | None
    allowAuthorizerOverride: AllowAuthorizerOverride | None


DateType = datetime
PublicKeyMap = dict[KeyName, KeyValue]


class AuthorizerDescription(TypedDict, total=False):
    """The authorizer description."""

    authorizerName: AuthorizerName | None
    authorizerArn: AuthorizerArn | None
    authorizerFunctionArn: AuthorizerFunctionArn | None
    tokenKeyName: TokenKeyName | None
    tokenSigningPublicKeys: PublicKeyMap | None
    status: AuthorizerStatus | None
    creationDate: DateType | None
    lastModifiedDate: DateType | None
    signingDisabled: BooleanKey | None
    enableCachingForHttp: EnableCachingForHttp | None


class AuthorizerSummary(TypedDict, total=False):
    """The authorizer summary."""

    authorizerName: AuthorizerName | None
    authorizerArn: AuthorizerArn | None


Authorizers = list[AuthorizerSummary]


class AwsJobAbortCriteria(TypedDict, total=False):
    """The criteria that determine when and how a job abort takes place."""

    failureType: AwsJobAbortCriteriaFailureType
    action: AwsJobAbortCriteriaAbortAction
    thresholdPercentage: AwsJobAbortCriteriaAbortThresholdPercentage
    minNumberOfExecutedThings: AwsJobAbortCriteriaMinimumNumberOfExecutedThings


AwsJobAbortCriteriaList = list[AwsJobAbortCriteria]


class AwsJobAbortConfig(TypedDict, total=False):
    """The criteria that determine when and how a job abort takes place."""

    abortCriteriaList: AwsJobAbortCriteriaList


class AwsJobRateIncreaseCriteria(TypedDict, total=False):
    """The criteria to initiate the increase in rate of rollout for a job."""

    numberOfNotifiedThings: AwsJobRateIncreaseCriteriaNumberOfThings | None
    numberOfSucceededThings: AwsJobRateIncreaseCriteriaNumberOfThings | None


class AwsJobExponentialRolloutRate(TypedDict, total=False):
    """The rate of increase for a job rollout. This parameter allows you to
    define an exponential rate increase for a job rollout.
    """

    baseRatePerMinute: AwsJobRolloutRatePerMinute
    incrementFactor: AwsJobRolloutIncrementFactor
    rateIncreaseCriteria: AwsJobRateIncreaseCriteria


class AwsJobExecutionsRolloutConfig(TypedDict, total=False):
    """Configuration for the rollout of OTA updates."""

    maximumPerMinute: MaximumPerMinute | None
    exponentialRate: AwsJobExponentialRolloutRate | None


ExpiresInSeconds = int


class AwsJobPresignedUrlConfig(TypedDict, total=False):
    """Configuration information for pre-signed URLs. Valid when ``protocols``
    contains HTTP.
    """

    expiresInSec: ExpiresInSeconds | None


AwsJobTimeoutInProgressTimeoutInMinutes = int


class AwsJobTimeoutConfig(TypedDict, total=False):
    """Specifies the amount of time each device has to finish its execution of
    the job. A timer is started when the job execution status is set to
    ``IN_PROGRESS``. If the job execution status is not set to another
    terminal state before the timer expires, it will be automatically set to
    ``TIMED_OUT``.
    """

    inProgressTimeoutInMinutes: AwsJobTimeoutInProgressTimeoutInMinutes | None


class BehaviorModelTrainingSummary(TypedDict, total=False):
    """The summary of an ML Detect behavior model."""

    securityProfileName: SecurityProfileName | None
    behaviorName: BehaviorName | None
    trainingDataCollectionStartDate: Timestamp | None
    modelStatus: ModelStatus | None
    datapointsCollectionPercentage: DataCollectionPercentage | None
    lastModelRefreshDate: Timestamp | None


BehaviorModelTrainingSummaries = list[BehaviorModelTrainingSummary]
Behaviors = list[Behavior]
CreationDate = datetime


class BillingGroupMetadata(TypedDict, total=False):
    """Additional information about the billing group."""

    creationDate: CreationDate | None


class GroupNameAndArn(TypedDict, total=False):
    """The name and ARN of a group."""

    groupName: ThingGroupName | None
    groupArn: ThingGroupArn | None


BillingGroupNameAndArnList = list[GroupNameAndArn]


class BillingGroupProperties(TypedDict, total=False):
    """The properties of a billing group."""

    billingGroupDescription: BillingGroupDescription | None


BinaryCommandExecutionResult = bytes
BinaryParameterValue = bytes


class Bucket(TypedDict, total=False):
    """A count of documents that meets a specific aggregation criteria."""

    keyValue: BucketKeyValue | None
    count: Count | None


Buckets = list[Bucket]


class TermsAggregation(TypedDict, total=False):
    """Performs an aggregation that will return a list of buckets. The list of
    buckets is a ranked list of the number of occurrences of an aggregation
    field value.
    """

    maxBuckets: MaxBuckets | None


class BucketsAggregationType(TypedDict, total=False):
    """The type of bucketed aggregation performed."""

    termsAggregation: TermsAggregation | None


class CACertificate(TypedDict, total=False):
    """A CA certificate."""

    certificateArn: CertificateArn | None
    certificateId: CertificateId | None
    status: CACertificateStatus | None
    creationDate: DateType | None


class CertificateValidity(TypedDict, total=False):
    """When the certificate is valid."""

    notBefore: DateType | None
    notAfter: DateType | None


class CACertificateDescription(TypedDict, total=False):
    """Describes a CA certificate."""

    certificateArn: CertificateArn | None
    certificateId: CertificateId | None
    status: CACertificateStatus | None
    certificatePem: CertificatePem | None
    ownedBy: AwsAccountId | None
    creationDate: DateType | None
    autoRegistrationStatus: AutoRegistrationStatus | None
    lastModifiedDate: DateType | None
    customerVersion: CustomerVersion | None
    generationId: GenerationId | None
    validity: CertificateValidity | None
    certificateMode: CertificateMode | None


CACertificates = list[CACertificate]


class CancelAuditMitigationActionsTaskRequest(ServiceRequest):
    taskId: MitigationActionsTaskId


class CancelAuditMitigationActionsTaskResponse(TypedDict, total=False):
    pass


class CancelAuditTaskRequest(ServiceRequest):
    taskId: AuditTaskId


class CancelAuditTaskResponse(TypedDict, total=False):
    pass


class CancelCertificateTransferRequest(ServiceRequest):
    """The input for the CancelCertificateTransfer operation."""

    certificateId: CertificateId


class CancelDetectMitigationActionsTaskRequest(ServiceRequest):
    taskId: MitigationActionsTaskId


class CancelDetectMitigationActionsTaskResponse(TypedDict, total=False):
    pass


DetailsMap = dict[DetailsKey, DetailsValue]
ExpectedVersion = int


class CancelJobExecutionRequest(ServiceRequest):
    jobId: JobId
    thingName: ThingName
    force: ForceFlag | None
    expectedVersion: ExpectedVersion | None
    statusDetails: DetailsMap | None


class CancelJobRequest(ServiceRequest):
    jobId: JobId
    reasonCode: ReasonCode | None
    comment: Comment | None
    force: ForceFlag | None


class CancelJobResponse(TypedDict, total=False):
    jobArn: JobArn | None
    jobId: JobId | None
    description: JobDescription | None


class Certificate(TypedDict, total=False):
    """Information about a certificate."""

    certificateArn: CertificateArn | None
    certificateId: CertificateId | None
    status: CertificateStatus | None
    certificateMode: CertificateMode | None
    creationDate: DateType | None


class TransferData(TypedDict, total=False):
    """Data used to transfer a certificate to an Amazon Web Services account."""

    transferMessage: Message | None
    rejectReason: Message | None
    transferDate: DateType | None
    acceptDate: DateType | None
    rejectDate: DateType | None


class CertificateDescription(TypedDict, total=False):
    """Describes a certificate."""

    certificateArn: CertificateArn | None
    certificateId: CertificateId | None
    caCertificateId: CertificateId | None
    status: CertificateStatus | None
    certificatePem: CertificatePem | None
    ownedBy: AwsAccountId | None
    previousOwnedBy: AwsAccountId | None
    creationDate: DateType | None
    lastModifiedDate: DateType | None
    customerVersion: CustomerVersion | None
    transferData: TransferData | None
    generationId: GenerationId | None
    validity: CertificateValidity | None
    certificateMode: CertificateMode | None


CertificateProviderAccountDefaultForOperations = list[CertificateProviderOperation]


class CertificateProviderSummary(TypedDict, total=False):
    """The certificate provider summary."""

    certificateProviderName: CertificateProviderName | None
    certificateProviderArn: CertificateProviderArn | None


CertificateProviders = list[CertificateProviderSummary]
Certificates = list[Certificate]


class ClearDefaultAuthorizerRequest(ServiceRequest):
    pass


class ClearDefaultAuthorizerResponse(TypedDict, total=False):
    pass


class ClientCertificateConfig(TypedDict, total=False):
    """An object that speciﬁes the client certificate conﬁguration for a
    domain.
    """

    clientCertificateCallbackArn: ClientCertificateCallbackArn | None


class CodeSigningCertificateChain(TypedDict, total=False):
    """Describes the certificate chain being used when code signing a file."""

    certificateName: CertificateName | None
    inlineDocument: InlineDocument | None


Signature = bytes


class CodeSigningSignature(TypedDict, total=False):
    """Describes the signature for a file."""

    inlineDocument: Signature | None


class CustomCodeSigning(TypedDict, total=False):
    """Describes a custom method used to code sign a file."""

    signature: CodeSigningSignature | None
    certificateChain: CodeSigningCertificateChain | None
    hashAlgorithm: HashAlgorithm | None
    signatureAlgorithm: SignatureAlgorithm | None


class S3Destination(TypedDict, total=False):
    """Describes the location of updated firmware in S3."""

    bucket: S3Bucket | None
    prefix: Prefix | None


class Destination(TypedDict, total=False):
    """Describes the location of the updated firmware."""

    s3Destination: S3Destination | None


class SigningProfileParameter(TypedDict, total=False):
    """Describes the code-signing profile."""

    certificateArn: CertificateArn | None
    platform: Platform | None
    certificatePathOnDevice: CertificatePathOnDevice | None


class StartSigningJobParameter(TypedDict, total=False):
    """Information required to start a signing job."""

    signingProfileParameter: SigningProfileParameter | None
    signingProfileName: SigningProfileName | None
    destination: Destination | None


class CodeSigning(TypedDict, total=False):
    """Describes the method to use when code signing a file."""

    awsSignerJobId: SigningJobId | None
    startSigningJobParameter: StartSigningJobParameter | None
    customCodeSigning: CustomCodeSigning | None


LongParameterValue = int


class CommandParameterValue(TypedDict, total=False):
    """The range of possible values that's used to describe a specific command
    parameter.

    The ``commandParameterValue`` can only have one of the below fields
    listed.
    """

    S: StringParameterValue | None
    B: BooleanParameterValue | None
    I: IntegerParameterValue | None
    L: LongParameterValue | None
    D: DoubleParameterValue | None
    BIN: BinaryParameterValue | None
    UL: UnsignedLongParameterValue | None


CommandExecutionParameterMap = dict[CommandParameterName, CommandParameterValue]


class CommandExecutionResult(TypedDict, total=False):
    """The result value of the command execution. The device can use the result
    field to share additional details about the execution such as a return
    value of a remote function call.

    This field is not applicable if you use the ``AWS-IoT-FleetWise``
    namespace.
    """

    S: StringCommandExecutionResult | None
    B: BooleanCommandExecutionResult | None
    BIN: BinaryCommandExecutionResult | None


CommandExecutionResultMap = dict[CommandExecutionResultName, CommandExecutionResult]


class CommandExecutionSummary(TypedDict, total=False):
    """Summary information about a particular command execution."""

    commandArn: CommandArn | None
    executionId: CommandExecutionId | None
    targetArn: TargetArn | None
    status: CommandExecutionStatus | None
    createdAt: DateType | None
    startedAt: DateType | None
    completedAt: DateType | None


CommandExecutionSummaryList = list[CommandExecutionSummary]
CommandExecutionTimeoutInSeconds = int


class CommandParameter(TypedDict, total=False):
    """A map of key-value pairs that describe the command."""

    name: CommandParameterName
    value: CommandParameterValue | None
    defaultValue: CommandParameterValue | None
    description: CommandParameterDescription | None


CommandParameterList = list[CommandParameter]
CommandPayloadBlob = bytes


class CommandPayload(TypedDict, total=False):
    """The command payload object that contains the instructions for the device
    to process.
    """

    content: CommandPayloadBlob | None
    contentType: MimeType | None


class CommandSummary(TypedDict, total=False):
    """Summary information about a particular command resource."""

    commandArn: CommandArn | None
    commandId: CommandId | None
    displayName: DisplayName | None
    deprecated: DeprecationFlag | None
    createdAt: DateType | None
    lastUpdatedAt: DateType | None
    pendingDeletion: BooleanWrapperObject | None


CommandSummaryList = list[CommandSummary]


class Configuration(TypedDict, total=False):
    """Configuration."""

    Enabled: Enabled | None


class ConfigurationDetails(TypedDict, total=False):
    """The encryption configuration details that include the status information
    of the Amazon Web Services Key Management Service (KMS) key and the KMS
    access role.
    """

    configurationStatus: ConfigurationStatus | None
    errorCode: ErrorCode | None
    errorMessage: ErrorMessage | None


class ConfirmTopicRuleDestinationRequest(ServiceRequest):
    confirmationToken: ConfirmationToken


class ConfirmTopicRuleDestinationResponse(TypedDict, total=False):
    pass


ConnectivityTimestamp = int


class CreateAuditSuppressionRequest(ServiceRequest):
    checkName: AuditCheckName
    resourceIdentifier: ResourceIdentifier
    expirationDate: Timestamp | None
    suppressIndefinitely: SuppressIndefinitely | None
    description: AuditDescription | None
    clientRequestToken: ClientRequestToken


class CreateAuditSuppressionResponse(TypedDict, total=False):
    pass


class Tag(TypedDict, total=False):
    """A set of key/value pairs that are used to manage the resource."""

    Key: TagKey
    Value: TagValue | None


TagList = list[Tag]


class CreateAuthorizerRequest(ServiceRequest):
    authorizerName: AuthorizerName
    authorizerFunctionArn: AuthorizerFunctionArn
    tokenKeyName: TokenKeyName | None
    tokenSigningPublicKeys: PublicKeyMap | None
    status: AuthorizerStatus | None
    tags: TagList | None
    signingDisabled: BooleanKey | None
    enableCachingForHttp: EnableCachingForHttp | None


class CreateAuthorizerResponse(TypedDict, total=False):
    authorizerName: AuthorizerName | None
    authorizerArn: AuthorizerArn | None


class CreateBillingGroupRequest(ServiceRequest):
    billingGroupName: BillingGroupName
    billingGroupProperties: BillingGroupProperties | None
    tags: TagList | None


class CreateBillingGroupResponse(TypedDict, total=False):
    billingGroupName: BillingGroupName | None
    billingGroupArn: BillingGroupArn | None
    billingGroupId: BillingGroupId | None


class CreateCertificateFromCsrRequest(ServiceRequest):
    """The input for the CreateCertificateFromCsr operation."""

    certificateSigningRequest: CertificateSigningRequest
    setAsActive: SetAsActive | None


class CreateCertificateFromCsrResponse(TypedDict, total=False):
    """The output from the CreateCertificateFromCsr operation."""

    certificateArn: CertificateArn | None
    certificateId: CertificateId | None
    certificatePem: CertificatePem | None


class CreateCertificateProviderRequest(ServiceRequest):
    certificateProviderName: CertificateProviderName
    lambdaFunctionArn: CertificateProviderFunctionArn
    accountDefaultForOperations: CertificateProviderAccountDefaultForOperations
    clientToken: ClientToken | None
    tags: TagList | None


class CreateCertificateProviderResponse(TypedDict, total=False):
    certificateProviderName: CertificateProviderName | None
    certificateProviderArn: CertificateProviderArn | None


class CreateCommandRequest(ServiceRequest):
    commandId: CommandId
    namespace: CommandNamespace | None
    displayName: DisplayName | None
    description: CommandDescription | None
    payload: CommandPayload | None
    mandatoryParameters: CommandParameterList | None
    roleArn: RoleArn | None
    tags: TagList | None


class CreateCommandResponse(TypedDict, total=False):
    commandId: CommandId | None
    commandArn: CommandArn | None


class CreateCustomMetricRequest(ServiceRequest):
    metricName: MetricName
    displayName: CustomMetricDisplayName | None
    metricType: CustomMetricType
    tags: TagList | None
    clientRequestToken: ClientRequestToken


class CreateCustomMetricResponse(TypedDict, total=False):
    metricName: MetricName | None
    metricArn: CustomMetricArn | None


DimensionStringValues = list[DimensionStringValue]


class CreateDimensionRequest(TypedDict, total=False):
    name: DimensionName
    type: DimensionType
    stringValues: DimensionStringValues
    tags: TagList | None
    clientRequestToken: ClientRequestToken


class CreateDimensionResponse(TypedDict, total=False):
    name: DimensionName | None
    arn: DimensionArn | None


class ServerCertificateConfig(TypedDict, total=False):
    """The server certificate configuration."""

    enableOCSPCheck: EnableOCSPCheck | None
    ocspLambdaArn: OCSPLambdaArn | None
    ocspAuthorizedResponderArn: AcmCertificateArn | None


class TlsConfig(TypedDict, total=False):
    """An object that specifies the TLS configuration for a domain."""

    securityPolicy: SecurityPolicy | None


ServerCertificateArns = list[AcmCertificateArn]


class CreateDomainConfigurationRequest(ServiceRequest):
    domainConfigurationName: DomainConfigurationName
    domainName: DomainName | None
    serverCertificateArns: ServerCertificateArns | None
    validationCertificateArn: AcmCertificateArn | None
    authorizerConfig: AuthorizerConfig | None
    serviceType: ServiceType | None
    tags: TagList | None
    tlsConfig: TlsConfig | None
    serverCertificateConfig: ServerCertificateConfig | None
    authenticationType: AuthenticationType | None
    applicationProtocol: ApplicationProtocol | None
    clientCertificateConfig: ClientCertificateConfig | None


class CreateDomainConfigurationResponse(TypedDict, total=False):
    domainConfigurationName: DomainConfigurationName | None
    domainConfigurationArn: DomainConfigurationArn | None


class ThingGroupProperties(TypedDict, total=False):
    """Thing group properties."""

    thingGroupDescription: ThingGroupDescription | None
    attributePayload: AttributePayload | None


class CreateDynamicThingGroupRequest(ServiceRequest):
    thingGroupName: ThingGroupName
    thingGroupProperties: ThingGroupProperties | None
    indexName: IndexName | None
    queryString: QueryString
    queryVersion: QueryVersion | None
    tags: TagList | None


class CreateDynamicThingGroupResponse(TypedDict, total=False):
    thingGroupName: ThingGroupName | None
    thingGroupArn: ThingGroupArn | None
    thingGroupId: ThingGroupId | None
    indexName: IndexName | None
    queryString: QueryString | None
    queryVersion: QueryVersion | None


class CreateFleetMetricRequest(ServiceRequest):
    metricName: FleetMetricName
    queryString: QueryString
    aggregationType: AggregationType
    period: FleetMetricPeriod
    aggregationField: AggregationField
    description: FleetMetricDescription | None
    queryVersion: QueryVersion | None
    indexName: IndexName | None
    unit: FleetMetricUnit | None
    tags: TagList | None


class CreateFleetMetricResponse(TypedDict, total=False):
    metricName: FleetMetricName | None
    metricArn: FleetMetricArn | None


DestinationPackageVersions = list[PackageVersionArn]


class MaintenanceWindow(TypedDict, total=False):
    """An optional configuration within the ``SchedulingConfig`` to setup a
    recurring maintenance window with a predetermined start time and
    duration for the rollout of a job document to all devices in a target
    group for a job.
    """

    startTime: CronExpression
    durationInMinutes: DurationInMinutes


MaintenanceWindows = list[MaintenanceWindow]


class SchedulingConfig(TypedDict, total=False):
    """Specifies the date and time that a job will begin the rollout of the job
    document to all devices in the target group. Additionally, you can
    specify the end behavior for each job execution when it reaches the
    scheduled end time.
    """

    startTime: StringDateTime | None
    endTime: StringDateTime | None
    endBehavior: JobEndBehavior | None
    maintenanceWindows: MaintenanceWindows | None


ParameterMap = dict[ParameterKey, ParameterValue]


class RetryCriteria(TypedDict, total=False):
    """The criteria that determines how many retries are allowed for each
    failure type for a job.
    """

    failureType: RetryableFailureType
    numberOfRetries: NumberOfRetries


RetryCriteriaList = list[RetryCriteria]


class JobExecutionsRetryConfig(TypedDict, total=False):
    """The configuration that determines how many retries are allowed for each
    failure type for a job.
    """

    criteriaList: RetryCriteriaList


InProgressTimeoutInMinutes = int


class TimeoutConfig(TypedDict, total=False):
    """Specifies the amount of time each device has to finish its execution of
    the job. A timer is started when the job execution status is set to
    ``IN_PROGRESS``. If the job execution status is not set to another
    terminal state before the timer expires, it will be automatically set to
    ``TIMED_OUT``.
    """

    inProgressTimeoutInMinutes: InProgressTimeoutInMinutes | None


class RateIncreaseCriteria(TypedDict, total=False):
    """Allows you to define a criteria to initiate the increase in rate of
    rollout for a job.
    """

    numberOfNotifiedThings: NumberOfThings | None
    numberOfSucceededThings: NumberOfThings | None


class ExponentialRolloutRate(TypedDict, total=False):
    """Allows you to create an exponential rate of rollout for a job."""

    baseRatePerMinute: RolloutRatePerMinute
    incrementFactor: IncrementFactor
    rateIncreaseCriteria: RateIncreaseCriteria


class JobExecutionsRolloutConfig(TypedDict, total=False):
    """Allows you to create a staged rollout of a job."""

    maximumPerMinute: MaxJobExecutionsPerMin | None
    exponentialRate: ExponentialRolloutRate | None


ExpiresInSec = int


class PresignedUrlConfig(TypedDict, total=False):
    """Configuration for pre-signed S3 URLs."""

    roleArn: RoleArn | None
    expiresInSec: ExpiresInSec | None


class CreateJobRequest(ServiceRequest):
    jobId: JobId
    targets: JobTargets
    documentSource: JobDocumentSource | None
    document: JobDocument | None
    description: JobDescription | None
    presignedUrlConfig: PresignedUrlConfig | None
    targetSelection: TargetSelection | None
    jobExecutionsRolloutConfig: JobExecutionsRolloutConfig | None
    abortConfig: AbortConfig | None
    timeoutConfig: TimeoutConfig | None
    tags: TagList | None
    namespaceId: NamespaceId | None
    jobTemplateArn: JobTemplateArn | None
    jobExecutionsRetryConfig: JobExecutionsRetryConfig | None
    documentParameters: ParameterMap | None
    schedulingConfig: SchedulingConfig | None
    destinationPackageVersions: DestinationPackageVersions | None


class CreateJobResponse(TypedDict, total=False):
    jobArn: JobArn | None
    jobId: JobId | None
    description: JobDescription | None


class CreateJobTemplateRequest(ServiceRequest):
    jobTemplateId: JobTemplateId
    jobArn: JobArn | None
    documentSource: JobDocumentSource | None
    document: JobDocument | None
    description: JobDescription
    presignedUrlConfig: PresignedUrlConfig | None
    jobExecutionsRolloutConfig: JobExecutionsRolloutConfig | None
    abortConfig: AbortConfig | None
    timeoutConfig: TimeoutConfig | None
    tags: TagList | None
    jobExecutionsRetryConfig: JobExecutionsRetryConfig | None
    maintenanceWindows: MaintenanceWindows | None
    destinationPackageVersions: DestinationPackageVersions | None


class CreateJobTemplateResponse(TypedDict, total=False):
    jobTemplateArn: JobTemplateArn | None
    jobTemplateId: JobTemplateId | None


class CreateKeysAndCertificateRequest(ServiceRequest):
    """The input for the CreateKeysAndCertificate operation.

    Requires permission to access the
    `CreateKeysAndCertificateRequest <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
    action.
    """

    setAsActive: SetAsActive | None


class KeyPair(TypedDict, total=False):
    """Describes a key pair."""

    PublicKey: PublicKey | None
    PrivateKey: PrivateKey | None


class CreateKeysAndCertificateResponse(TypedDict, total=False):
    """The output of the CreateKeysAndCertificate operation."""

    certificateArn: CertificateArn | None
    certificateId: CertificateId | None
    certificatePem: CertificatePem | None
    keyPair: KeyPair | None


class PublishFindingToSnsParams(TypedDict, total=False):
    """Parameters to define a mitigation action that publishes findings to
    Amazon SNS. You can implement your own custom actions in response to the
    Amazon SNS messages.
    """

    topicArn: SnsTopicArn


class EnableIoTLoggingParams(TypedDict, total=False):
    """Parameters used when defining a mitigation action that enable Amazon Web
    Services IoT Core logging.
    """

    roleArnForLogging: RoleArn
    logLevel: LogLevel


class ReplaceDefaultPolicyVersionParams(TypedDict, total=False):
    """Parameters to define a mitigation action that adds a blank policy to
    restrict permissions.
    """

    templateName: PolicyTemplateName


class UpdateCACertificateParams(TypedDict, total=False):
    """Parameters to define a mitigation action that changes the state of the
    CA certificate to inactive.
    """

    action: CACertificateUpdateAction


class UpdateDeviceCertificateParams(TypedDict, total=False):
    """Parameters to define a mitigation action that changes the state of the
    device certificate to inactive.
    """

    action: DeviceCertificateUpdateAction


class MitigationActionParams(TypedDict, total=False):
    """The set of parameters for this mitigation action. You can specify only
    one type of parameter (in other words, you can apply only one action for
    each defined mitigation action).
    """

    updateDeviceCertificateParams: UpdateDeviceCertificateParams | None
    updateCACertificateParams: UpdateCACertificateParams | None
    addThingsToThingGroupParams: AddThingsToThingGroupParams | None
    replaceDefaultPolicyVersionParams: ReplaceDefaultPolicyVersionParams | None
    enableIoTLoggingParams: EnableIoTLoggingParams | None
    publishFindingToSnsParams: PublishFindingToSnsParams | None


class CreateMitigationActionRequest(ServiceRequest):
    actionName: MitigationActionName
    roleArn: RoleArn
    actionParams: MitigationActionParams
    tags: TagList | None


class CreateMitigationActionResponse(TypedDict, total=False):
    actionArn: MitigationActionArn | None
    actionId: MitigationActionId | None


class Stream(TypedDict, total=False):
    """Describes a group of files that can be streamed."""

    streamId: StreamId | None
    fileId: FileId | None


class FileLocation(TypedDict, total=False):
    """The location of the OTA update."""

    stream: Stream | None
    s3Location: S3Location | None


class OTAUpdateFile(TypedDict, total=False):
    """Describes a file to be associated with an OTA update."""

    fileName: FileName | None
    fileType: FileType | None
    fileVersion: OTAUpdateFileVersion | None
    fileLocation: FileLocation | None
    codeSigning: CodeSigning | None
    attributes: AttributesMap | None


OTAUpdateFiles = list[OTAUpdateFile]
Protocols = list[Protocol]
Targets = list[Target]


class CreateOTAUpdateRequest(ServiceRequest):
    otaUpdateId: OTAUpdateId
    description: OTAUpdateDescription | None
    targets: Targets
    protocols: Protocols | None
    targetSelection: TargetSelection | None
    awsJobExecutionsRolloutConfig: AwsJobExecutionsRolloutConfig | None
    awsJobPresignedUrlConfig: AwsJobPresignedUrlConfig | None
    awsJobAbortConfig: AwsJobAbortConfig | None
    awsJobTimeoutConfig: AwsJobTimeoutConfig | None
    files: OTAUpdateFiles
    roleArn: RoleArn
    additionalParameters: AdditionalParameterMap | None
    tags: TagList | None


class CreateOTAUpdateResponse(TypedDict, total=False):
    otaUpdateId: OTAUpdateId | None
    awsIotJobId: AwsIotJobId | None
    otaUpdateArn: OTAUpdateArn | None
    awsIotJobArn: AwsIotJobArn | None
    otaUpdateStatus: OTAUpdateStatus | None


TagMap = dict[TagKey, TagValue]


class CreatePackageRequest(ServiceRequest):
    packageName: PackageName
    description: ResourceDescription | None
    tags: TagMap | None
    clientToken: ClientToken | None


class CreatePackageResponse(TypedDict, total=False):
    packageName: PackageName | None
    packageArn: PackageArn | None
    description: ResourceDescription | None


class PackageVersionArtifact(TypedDict, total=False):
    """A specific package version artifact associated with a software package
    version.
    """

    s3Location: S3Location | None


ResourceAttributes = dict[ResourceAttributeKey, ResourceAttributeValue]


class CreatePackageVersionRequest(ServiceRequest):
    packageName: PackageName
    versionName: VersionName
    description: ResourceDescription | None
    attributes: ResourceAttributes | None
    artifact: PackageVersionArtifact | None
    recipe: PackageVersionRecipe | None
    tags: TagMap | None
    clientToken: ClientToken | None


class CreatePackageVersionResponse(TypedDict, total=False):
    packageVersionArn: PackageVersionArn | None
    packageName: PackageName | None
    versionName: VersionName | None
    description: ResourceDescription | None
    attributes: ResourceAttributes | None
    status: PackageVersionStatus | None
    errorReason: PackageVersionErrorReason | None


class CreatePolicyRequest(ServiceRequest):
    """The input for the CreatePolicy operation."""

    policyName: PolicyName
    policyDocument: PolicyDocument
    tags: TagList | None


class CreatePolicyResponse(TypedDict, total=False):
    """The output from the CreatePolicy operation."""

    policyName: PolicyName | None
    policyArn: PolicyArn | None
    policyDocument: PolicyDocument | None
    policyVersionId: PolicyVersionId | None


class CreatePolicyVersionRequest(ServiceRequest):
    """The input for the CreatePolicyVersion operation."""

    policyName: PolicyName
    policyDocument: PolicyDocument
    setAsDefault: SetAsDefault | None


class CreatePolicyVersionResponse(TypedDict, total=False):
    """The output of the CreatePolicyVersion operation."""

    policyArn: PolicyArn | None
    policyDocument: PolicyDocument | None
    policyVersionId: PolicyVersionId | None
    isDefaultVersion: IsDefaultVersion | None


class CreateProvisioningClaimRequest(ServiceRequest):
    templateName: TemplateName


class CreateProvisioningClaimResponse(TypedDict, total=False):
    certificateId: CertificateId | None
    certificatePem: CertificatePem | None
    keyPair: KeyPair | None
    expiration: DateType | None


class ProvisioningHook(TypedDict, total=False):
    """Structure that contains ``payloadVersion`` and ``targetArn``."""

    payloadVersion: PayloadVersion | None
    targetArn: TargetArn


class CreateProvisioningTemplateRequest(TypedDict, total=False):
    templateName: TemplateName
    description: TemplateDescription | None
    templateBody: TemplateBody
    enabled: Enabled | None
    provisioningRoleArn: RoleArn
    preProvisioningHook: ProvisioningHook | None
    tags: TagList | None
    type: TemplateType | None


class CreateProvisioningTemplateResponse(TypedDict, total=False):
    templateArn: TemplateArn | None
    templateName: TemplateName | None
    defaultVersionId: TemplateVersionId | None


class CreateProvisioningTemplateVersionRequest(ServiceRequest):
    templateName: TemplateName
    templateBody: TemplateBody
    setAsDefault: SetAsDefault | None


class CreateProvisioningTemplateVersionResponse(TypedDict, total=False):
    templateArn: TemplateArn | None
    templateName: TemplateName | None
    versionId: TemplateVersionId | None
    isDefaultVersion: IsDefaultVersion | None


class CreateRoleAliasRequest(ServiceRequest):
    roleAlias: RoleAlias
    roleArn: RoleArn
    credentialDurationSeconds: CredentialDurationSeconds | None
    tags: TagList | None


class CreateRoleAliasResponse(TypedDict, total=False):
    roleAlias: RoleAlias | None
    roleAliasArn: RoleAliasArn | None


TargetAuditCheckNames = list[AuditCheckName]


class CreateScheduledAuditRequest(ServiceRequest):
    frequency: AuditFrequency
    dayOfMonth: DayOfMonth | None
    dayOfWeek: DayOfWeek | None
    targetCheckNames: TargetAuditCheckNames
    scheduledAuditName: ScheduledAuditName
    tags: TagList | None


class CreateScheduledAuditResponse(TypedDict, total=False):
    scheduledAuditArn: ScheduledAuditArn | None


class MetricsExportConfig(TypedDict, total=False):
    """Set configurations for metrics export."""

    mqttTopic: MqttTopic
    roleArn: RoleArn


class CreateSecurityProfileRequest(ServiceRequest):
    securityProfileName: SecurityProfileName
    securityProfileDescription: SecurityProfileDescription | None
    behaviors: Behaviors | None
    alertTargets: AlertTargets | None
    additionalMetricsToRetain: AdditionalMetricsToRetainList | None
    additionalMetricsToRetainV2: AdditionalMetricsToRetainV2List | None
    tags: TagList | None
    metricsExportConfig: MetricsExportConfig | None


class CreateSecurityProfileResponse(TypedDict, total=False):
    securityProfileName: SecurityProfileName | None
    securityProfileArn: SecurityProfileArn | None


class StreamFile(TypedDict, total=False):
    """Represents a file to stream."""

    fileId: FileId | None
    s3Location: S3Location | None


StreamFiles = list[StreamFile]


class CreateStreamRequest(ServiceRequest):
    streamId: StreamId
    description: StreamDescription | None
    files: StreamFiles
    roleArn: RoleArn
    tags: TagList | None


class CreateStreamResponse(TypedDict, total=False):
    streamId: StreamId | None
    streamArn: StreamArn | None
    description: StreamDescription | None
    streamVersion: StreamVersion | None


class CreateThingGroupRequest(ServiceRequest):
    thingGroupName: ThingGroupName
    parentGroupName: ThingGroupName | None
    thingGroupProperties: ThingGroupProperties | None
    tags: TagList | None


class CreateThingGroupResponse(TypedDict, total=False):
    thingGroupName: ThingGroupName | None
    thingGroupArn: ThingGroupArn | None
    thingGroupId: ThingGroupId | None


class CreateThingRequest(ServiceRequest):
    """The input for the CreateThing operation."""

    thingName: ThingName
    thingTypeName: ThingTypeName | None
    attributePayload: AttributePayload | None
    billingGroupName: BillingGroupName | None


class CreateThingResponse(TypedDict, total=False):
    """The output of the CreateThing operation."""

    thingName: ThingName | None
    thingArn: ThingArn | None
    thingId: ThingId | None


class PropagatingAttribute(TypedDict, total=False):
    """An object that represents the connection attribute, thing attribute, and
    the user property key.
    """

    userPropertyKey: UserPropertyKeyName | None
    thingAttribute: AttributeName | None
    connectionAttribute: ConnectionAttributeName | None


PropagatingAttributeList = list[PropagatingAttribute]


class Mqtt5Configuration(TypedDict, total=False):
    """The configuration to add user-defined properties to enrich MQTT 5
    messages.
    """

    propagatingAttributes: PropagatingAttributeList | None


SearchableAttributes = list[AttributeName]


class ThingTypeProperties(TypedDict, total=False):
    """The ThingTypeProperties contains information about the thing type
    including: a thing type description, and a list of searchable thing
    attribute names.
    """

    thingTypeDescription: ThingTypeDescription | None
    searchableAttributes: SearchableAttributes | None
    mqtt5Configuration: Mqtt5Configuration | None


class CreateThingTypeRequest(ServiceRequest):
    """The input for the CreateThingType operation."""

    thingTypeName: ThingTypeName
    thingTypeProperties: ThingTypeProperties | None
    tags: TagList | None


class CreateThingTypeResponse(TypedDict, total=False):
    """The output of the CreateThingType operation."""

    thingTypeName: ThingTypeName | None
    thingTypeArn: ThingTypeArn | None
    thingTypeId: ThingTypeId | None


SecurityGroupList = list[SecurityGroupId]
SubnetIdList = list[SubnetId]


class VpcDestinationConfiguration(TypedDict, total=False):
    """The configuration information for a virtual private cloud (VPC)
    destination.
    """

    subnetIds: SubnetIdList
    securityGroups: SecurityGroupList | None
    vpcId: VpcId
    roleArn: AwsArn


class HttpUrlDestinationConfiguration(TypedDict, total=False):
    """HTTP URL destination configuration used by the topic rule's HTTP action."""

    confirmationUrl: Url


class TopicRuleDestinationConfiguration(TypedDict, total=False):
    """Configuration of the topic rule destination."""

    httpUrlConfiguration: HttpUrlDestinationConfiguration | None
    vpcConfiguration: VpcDestinationConfiguration | None


class CreateTopicRuleDestinationRequest(ServiceRequest):
    destinationConfiguration: TopicRuleDestinationConfiguration


class VpcDestinationProperties(TypedDict, total=False):
    """The properties of a virtual private cloud (VPC) destination."""

    subnetIds: SubnetIdList | None
    securityGroups: SecurityGroupList | None
    vpcId: VpcId | None
    roleArn: AwsArn | None


class HttpUrlDestinationProperties(TypedDict, total=False):
    """HTTP URL destination properties."""

    confirmationUrl: Url | None


LastUpdatedAtDate = datetime
CreatedAtDate = datetime


class TopicRuleDestination(TypedDict, total=False):
    """A topic rule destination."""

    arn: AwsArn | None
    status: TopicRuleDestinationStatus | None
    createdAt: CreatedAtDate | None
    lastUpdatedAt: LastUpdatedAtDate | None
    statusReason: String | None
    httpUrlProperties: HttpUrlDestinationProperties | None
    vpcProperties: VpcDestinationProperties | None


class CreateTopicRuleDestinationResponse(TypedDict, total=False):
    topicRuleDestination: TopicRuleDestination | None


class TopicRulePayload(TypedDict, total=False):
    """Describes a rule."""

    sql: SQL
    description: Description | None
    actions: ActionList
    ruleDisabled: IsDisabled | None
    awsIotSqlVersion: AwsIotSqlVersion | None
    errorAction: Action | None


class CreateTopicRuleRequest(ServiceRequest):
    """The input for the CreateTopicRule operation."""

    ruleName: RuleName
    topicRulePayload: TopicRulePayload
    tags: String | None


class DeleteAccountAuditConfigurationRequest(ServiceRequest):
    deleteScheduledAudits: DeleteScheduledAudits | None


class DeleteAccountAuditConfigurationResponse(TypedDict, total=False):
    pass


class DeleteAuditSuppressionRequest(ServiceRequest):
    checkName: AuditCheckName
    resourceIdentifier: ResourceIdentifier


class DeleteAuditSuppressionResponse(TypedDict, total=False):
    pass


class DeleteAuthorizerRequest(ServiceRequest):
    authorizerName: AuthorizerName


class DeleteAuthorizerResponse(TypedDict, total=False):
    pass


OptionalVersion = int


class DeleteBillingGroupRequest(ServiceRequest):
    billingGroupName: BillingGroupName
    expectedVersion: OptionalVersion | None


class DeleteBillingGroupResponse(TypedDict, total=False):
    pass


class DeleteCACertificateRequest(ServiceRequest):
    """Input for the DeleteCACertificate operation."""

    certificateId: CertificateId


class DeleteCACertificateResponse(TypedDict, total=False):
    """The output for the DeleteCACertificate operation."""

    pass


class DeleteCertificateProviderRequest(ServiceRequest):
    certificateProviderName: CertificateProviderName


class DeleteCertificateProviderResponse(TypedDict, total=False):
    pass


class DeleteCertificateRequest(ServiceRequest):
    """The input for the DeleteCertificate operation."""

    certificateId: CertificateId
    forceDelete: ForceDelete | None


class DeleteCommandExecutionRequest(ServiceRequest):
    executionId: CommandExecutionId
    targetArn: TargetArn


class DeleteCommandExecutionResponse(TypedDict, total=False):
    pass


class DeleteCommandRequest(ServiceRequest):
    commandId: CommandId


class DeleteCommandResponse(TypedDict, total=False):
    statusCode: StatusCode | None


class DeleteCustomMetricRequest(ServiceRequest):
    metricName: MetricName


class DeleteCustomMetricResponse(TypedDict, total=False):
    pass


class DeleteDimensionRequest(ServiceRequest):
    name: DimensionName


class DeleteDimensionResponse(TypedDict, total=False):
    pass


class DeleteDomainConfigurationRequest(ServiceRequest):
    domainConfigurationName: DomainConfigurationName


class DeleteDomainConfigurationResponse(TypedDict, total=False):
    pass


class DeleteDynamicThingGroupRequest(ServiceRequest):
    thingGroupName: ThingGroupName
    expectedVersion: OptionalVersion | None


class DeleteDynamicThingGroupResponse(TypedDict, total=False):
    pass


class DeleteFleetMetricRequest(ServiceRequest):
    metricName: FleetMetricName
    expectedVersion: OptionalVersion | None


ExecutionNumber = int


class DeleteJobExecutionRequest(ServiceRequest):
    jobId: JobId
    thingName: ThingName
    executionNumber: ExecutionNumber
    force: ForceFlag | None
    namespaceId: NamespaceId | None


class DeleteJobRequest(ServiceRequest):
    jobId: JobId
    force: ForceFlag | None
    namespaceId: NamespaceId | None


class DeleteJobTemplateRequest(ServiceRequest):
    jobTemplateId: JobTemplateId


class DeleteMitigationActionRequest(ServiceRequest):
    actionName: MitigationActionName


class DeleteMitigationActionResponse(TypedDict, total=False):
    pass


class DeleteOTAUpdateRequest(ServiceRequest):
    otaUpdateId: OTAUpdateId
    deleteStream: DeleteStream | None
    forceDeleteAWSJob: ForceDeleteAWSJob | None


class DeleteOTAUpdateResponse(TypedDict, total=False):
    pass


class DeletePackageRequest(ServiceRequest):
    packageName: PackageName
    clientToken: ClientToken | None


class DeletePackageResponse(TypedDict, total=False):
    pass


class DeletePackageVersionRequest(ServiceRequest):
    packageName: PackageName
    versionName: VersionName
    clientToken: ClientToken | None


class DeletePackageVersionResponse(TypedDict, total=False):
    pass


class DeletePolicyRequest(ServiceRequest):
    """The input for the DeletePolicy operation."""

    policyName: PolicyName


class DeletePolicyVersionRequest(ServiceRequest):
    """The input for the DeletePolicyVersion operation."""

    policyName: PolicyName
    policyVersionId: PolicyVersionId


class DeleteProvisioningTemplateRequest(ServiceRequest):
    templateName: TemplateName


class DeleteProvisioningTemplateResponse(TypedDict, total=False):
    pass


class DeleteProvisioningTemplateVersionRequest(ServiceRequest):
    templateName: TemplateName
    versionId: TemplateVersionId


class DeleteProvisioningTemplateVersionResponse(TypedDict, total=False):
    pass


class DeleteRegistrationCodeRequest(ServiceRequest):
    """The input for the DeleteRegistrationCode operation."""

    pass


class DeleteRegistrationCodeResponse(TypedDict, total=False):
    """The output for the DeleteRegistrationCode operation."""

    pass


class DeleteRoleAliasRequest(ServiceRequest):
    roleAlias: RoleAlias


class DeleteRoleAliasResponse(TypedDict, total=False):
    pass


class DeleteScheduledAuditRequest(ServiceRequest):
    scheduledAuditName: ScheduledAuditName


class DeleteScheduledAuditResponse(TypedDict, total=False):
    pass


class DeleteSecurityProfileRequest(ServiceRequest):
    securityProfileName: SecurityProfileName
    expectedVersion: OptionalVersion | None


class DeleteSecurityProfileResponse(TypedDict, total=False):
    pass


class DeleteStreamRequest(ServiceRequest):
    streamId: StreamId


class DeleteStreamResponse(TypedDict, total=False):
    pass


class DeleteThingGroupRequest(ServiceRequest):
    thingGroupName: ThingGroupName
    expectedVersion: OptionalVersion | None


class DeleteThingGroupResponse(TypedDict, total=False):
    pass


class DeleteThingRequest(ServiceRequest):
    """The input for the DeleteThing operation."""

    thingName: ThingName
    expectedVersion: OptionalVersion | None


class DeleteThingResponse(TypedDict, total=False):
    """The output of the DeleteThing operation."""

    pass


class DeleteThingTypeRequest(ServiceRequest):
    """The input for the DeleteThingType operation."""

    thingTypeName: ThingTypeName


class DeleteThingTypeResponse(TypedDict, total=False):
    """The output for the DeleteThingType operation."""

    pass


class DeleteTopicRuleDestinationRequest(ServiceRequest):
    arn: AwsArn


class DeleteTopicRuleDestinationResponse(TypedDict, total=False):
    pass


class DeleteTopicRuleRequest(ServiceRequest):
    """The input for the DeleteTopicRule operation."""

    ruleName: RuleName


class DeleteV2LoggingLevelRequest(ServiceRequest):
    targetType: LogTargetType
    targetName: LogTargetName


class DeprecateThingTypeRequest(ServiceRequest):
    """The input for the DeprecateThingType operation."""

    thingTypeName: ThingTypeName
    undoDeprecate: UndoDeprecate | None


class DeprecateThingTypeResponse(TypedDict, total=False):
    """The output for the DeprecateThingType operation."""

    pass


DeprecationDate = datetime


class DescribeAccountAuditConfigurationRequest(ServiceRequest):
    pass


class DescribeAccountAuditConfigurationResponse(TypedDict, total=False):
    roleArn: RoleArn | None
    auditNotificationTargetConfigurations: AuditNotificationTargetConfigurations | None
    auditCheckConfigurations: AuditCheckConfigurations | None


class DescribeAuditFindingRequest(ServiceRequest):
    findingId: FindingId


class DescribeAuditFindingResponse(TypedDict, total=False):
    finding: AuditFinding | None


class DescribeAuditMitigationActionsTaskRequest(ServiceRequest):
    taskId: MitigationActionsTaskId


class MitigationAction(TypedDict, total=False):
    """Describes which changes should be applied as part of a mitigation
    action.
    """

    name: MitigationActionName | None
    id: MitigationActionId | None
    roleArn: RoleArn | None
    actionParams: MitigationActionParams | None


MitigationActionList = list[MitigationAction]


class DescribeAuditMitigationActionsTaskResponse(TypedDict, total=False):
    taskStatus: AuditMitigationActionsTaskStatus | None
    startTime: Timestamp | None
    endTime: Timestamp | None
    taskStatistics: AuditMitigationActionsTaskStatistics | None
    target: AuditMitigationActionsTaskTarget | None
    auditCheckToActionsMapping: AuditCheckToActionsMapping | None
    actionsDefinition: MitigationActionList | None


class DescribeAuditSuppressionRequest(ServiceRequest):
    checkName: AuditCheckName
    resourceIdentifier: ResourceIdentifier


class DescribeAuditSuppressionResponse(TypedDict, total=False):
    checkName: AuditCheckName | None
    resourceIdentifier: ResourceIdentifier | None
    expirationDate: Timestamp | None
    suppressIndefinitely: SuppressIndefinitely | None
    description: AuditDescription | None


class DescribeAuditTaskRequest(ServiceRequest):
    taskId: AuditTaskId


class TaskStatistics(TypedDict, total=False):
    """Statistics for the checks performed during the audit."""

    totalChecks: TotalChecksCount | None
    inProgressChecks: InProgressChecksCount | None
    waitingForDataCollectionChecks: WaitingForDataCollectionChecksCount | None
    compliantChecks: CompliantChecksCount | None
    nonCompliantChecks: NonCompliantChecksCount | None
    failedChecks: FailedChecksCount | None
    canceledChecks: CanceledChecksCount | None


class DescribeAuditTaskResponse(TypedDict, total=False):
    taskStatus: AuditTaskStatus | None
    taskType: AuditTaskType | None
    taskStartTime: Timestamp | None
    taskStatistics: TaskStatistics | None
    scheduledAuditName: ScheduledAuditName | None
    auditDetails: AuditDetails | None


class DescribeAuthorizerRequest(ServiceRequest):
    authorizerName: AuthorizerName


class DescribeAuthorizerResponse(TypedDict, total=False):
    authorizerDescription: AuthorizerDescription | None


class DescribeBillingGroupRequest(ServiceRequest):
    billingGroupName: BillingGroupName


Version = int


class DescribeBillingGroupResponse(TypedDict, total=False):
    billingGroupName: BillingGroupName | None
    billingGroupId: BillingGroupId | None
    billingGroupArn: BillingGroupArn | None
    version: Version | None
    billingGroupProperties: BillingGroupProperties | None
    billingGroupMetadata: BillingGroupMetadata | None


class DescribeCACertificateRequest(ServiceRequest):
    """The input for the DescribeCACertificate operation."""

    certificateId: CertificateId


class RegistrationConfig(TypedDict, total=False):
    """The registration configuration."""

    templateBody: TemplateBody | None
    roleArn: RoleArn | None
    templateName: TemplateName | None


class DescribeCACertificateResponse(TypedDict, total=False):
    """The output from the DescribeCACertificate operation."""

    certificateDescription: CACertificateDescription | None
    registrationConfig: RegistrationConfig | None


class DescribeCertificateProviderRequest(ServiceRequest):
    certificateProviderName: CertificateProviderName


class DescribeCertificateProviderResponse(TypedDict, total=False):
    certificateProviderName: CertificateProviderName | None
    certificateProviderArn: CertificateProviderArn | None
    lambdaFunctionArn: CertificateProviderFunctionArn | None
    accountDefaultForOperations: CertificateProviderAccountDefaultForOperations | None
    creationDate: DateType | None
    lastModifiedDate: DateType | None


class DescribeCertificateRequest(ServiceRequest):
    """The input for the DescribeCertificate operation."""

    certificateId: CertificateId


class DescribeCertificateResponse(TypedDict, total=False):
    """The output of the DescribeCertificate operation."""

    certificateDescription: CertificateDescription | None


class DescribeCustomMetricRequest(ServiceRequest):
    metricName: MetricName


class DescribeCustomMetricResponse(TypedDict, total=False):
    metricName: MetricName | None
    metricArn: CustomMetricArn | None
    metricType: CustomMetricType | None
    displayName: CustomMetricDisplayName | None
    creationDate: Timestamp | None
    lastModifiedDate: Timestamp | None


class DescribeDefaultAuthorizerRequest(ServiceRequest):
    pass


class DescribeDefaultAuthorizerResponse(TypedDict, total=False):
    authorizerDescription: AuthorizerDescription | None


class DescribeDetectMitigationActionsTaskRequest(ServiceRequest):
    taskId: MitigationActionsTaskId


GenericLongValue = int


class DetectMitigationActionsTaskStatistics(TypedDict, total=False):
    """The statistics of a mitigation action task."""

    actionsExecuted: GenericLongValue | None
    actionsSkipped: GenericLongValue | None
    actionsFailed: GenericLongValue | None


class ViolationEventOccurrenceRange(TypedDict, total=False):
    """Specifies the time period of which violation events occurred between."""

    startTime: Timestamp
    endTime: Timestamp


TargetViolationIdsForDetectMitigationActions = list[ViolationId]


class DetectMitigationActionsTaskTarget(TypedDict, total=False):
    """The target of a mitigation action task."""

    violationIds: TargetViolationIdsForDetectMitigationActions | None
    securityProfileName: SecurityProfileName | None
    behaviorName: BehaviorName | None


class DetectMitigationActionsTaskSummary(TypedDict, total=False):
    """The summary of the mitigation action tasks."""

    taskId: MitigationActionsTaskId | None
    taskStatus: DetectMitigationActionsTaskStatus | None
    taskStartTime: Timestamp | None
    taskEndTime: Timestamp | None
    target: DetectMitigationActionsTaskTarget | None
    violationEventOccurrenceRange: ViolationEventOccurrenceRange | None
    onlyActiveViolationsIncluded: PrimitiveBoolean | None
    suppressedAlertsIncluded: PrimitiveBoolean | None
    actionsDefinition: MitigationActionList | None
    taskStatistics: DetectMitigationActionsTaskStatistics | None


class DescribeDetectMitigationActionsTaskResponse(TypedDict, total=False):
    taskSummary: DetectMitigationActionsTaskSummary | None


class DescribeDimensionRequest(ServiceRequest):
    name: DimensionName


class DescribeDimensionResponse(TypedDict, total=False):
    name: DimensionName | None
    arn: DimensionArn | None
    type: DimensionType | None
    stringValues: DimensionStringValues | None
    creationDate: Timestamp | None
    lastModifiedDate: Timestamp | None


class DescribeDomainConfigurationRequest(ServiceRequest):
    domainConfigurationName: ReservedDomainConfigurationName


class ServerCertificateSummary(TypedDict, total=False):
    """An object that contains information about a server certificate."""

    serverCertificateArn: AcmCertificateArn | None
    serverCertificateStatus: ServerCertificateStatus | None
    serverCertificateStatusDetail: ServerCertificateStatusDetail | None


ServerCertificates = list[ServerCertificateSummary]


class DescribeDomainConfigurationResponse(TypedDict, total=False):
    domainConfigurationName: ReservedDomainConfigurationName | None
    domainConfigurationArn: DomainConfigurationArn | None
    domainName: DomainName | None
    serverCertificates: ServerCertificates | None
    authorizerConfig: AuthorizerConfig | None
    domainConfigurationStatus: DomainConfigurationStatus | None
    serviceType: ServiceType | None
    domainType: DomainType | None
    lastStatusChangeDate: DateType | None
    tlsConfig: TlsConfig | None
    serverCertificateConfig: ServerCertificateConfig | None
    authenticationType: AuthenticationType | None
    applicationProtocol: ApplicationProtocol | None
    clientCertificateConfig: ClientCertificateConfig | None


class DescribeEncryptionConfigurationRequest(ServiceRequest):
    pass


class DescribeEncryptionConfigurationResponse(TypedDict, total=False):
    encryptionType: EncryptionType | None
    kmsKeyArn: KmsKeyArn | None
    kmsAccessRoleArn: KmsAccessRoleArn | None
    configurationDetails: ConfigurationDetails | None
    lastModifiedDate: DateType | None


class DescribeEndpointRequest(ServiceRequest):
    """The input for the DescribeEndpoint operation."""

    endpointType: EndpointType | None


class DescribeEndpointResponse(TypedDict, total=False):
    """The output from the DescribeEndpoint operation."""

    endpointAddress: EndpointAddress | None


class DescribeEventConfigurationsRequest(ServiceRequest):
    pass


LastModifiedDate = datetime
EventConfigurations = dict[EventType, Configuration]


class DescribeEventConfigurationsResponse(TypedDict, total=False):
    eventConfigurations: EventConfigurations | None
    creationDate: CreationDate | None
    lastModifiedDate: LastModifiedDate | None


class DescribeFleetMetricRequest(ServiceRequest):
    metricName: FleetMetricName


class DescribeFleetMetricResponse(TypedDict, total=False):
    metricName: FleetMetricName | None
    queryString: QueryString | None
    aggregationType: AggregationType | None
    period: FleetMetricPeriod | None
    aggregationField: AggregationField | None
    description: FleetMetricDescription | None
    queryVersion: QueryVersion | None
    indexName: IndexName | None
    creationDate: CreationDate | None
    lastModifiedDate: LastModifiedDate | None
    unit: FleetMetricUnit | None
    version: Version | None
    metricArn: FleetMetricArn | None


class DescribeIndexRequest(ServiceRequest):
    indexName: IndexName


class DescribeIndexResponse(TypedDict, total=False):
    indexName: IndexName | None
    indexStatus: IndexStatus | None
    schema: IndexSchema | None


class DescribeJobExecutionRequest(ServiceRequest):
    jobId: JobId
    thingName: ThingName
    executionNumber: ExecutionNumber | None


VersionNumber = int


class JobExecutionStatusDetails(TypedDict, total=False):
    """Details of the job execution status."""

    detailsMap: DetailsMap | None


class JobExecution(TypedDict, total=False):
    """The job execution object represents the execution of a job on a
    particular device.
    """

    jobId: JobId | None
    status: JobExecutionStatus | None
    forceCanceled: Forced | None
    statusDetails: JobExecutionStatusDetails | None
    thingArn: ThingArn | None
    queuedAt: DateType | None
    startedAt: DateType | None
    lastUpdatedAt: DateType | None
    executionNumber: ExecutionNumber | None
    versionNumber: VersionNumber | None
    approximateSecondsBeforeTimedOut: ApproximateSecondsBeforeTimedOut | None


class DescribeJobExecutionResponse(TypedDict, total=False):
    execution: JobExecution | None


class DescribeJobRequest(ServiceRequest):
    jobId: JobId
    beforeSubstitution: BeforeSubstitutionFlag | None


class ScheduledJobRollout(TypedDict, total=False):
    """Displays the next seven maintenance window occurrences and their start
    times.
    """

    startTime: StringDateTime | None


ScheduledJobRolloutList = list[ScheduledJobRollout]
ProcessingTargetNameList = list[ProcessingTargetName]


class JobProcessDetails(TypedDict, total=False):
    """The job process details."""

    processingTargets: ProcessingTargetNameList | None
    numberOfCanceledThings: CanceledThings | None
    numberOfSucceededThings: SucceededThings | None
    numberOfFailedThings: FailedThings | None
    numberOfRejectedThings: RejectedThings | None
    numberOfQueuedThings: QueuedThings | None
    numberOfInProgressThings: InProgressThings | None
    numberOfRemovedThings: RemovedThings | None
    numberOfTimedOutThings: TimedOutThings | None


class Job(TypedDict, total=False):
    """The ``Job`` object contains details about a job."""

    jobArn: JobArn | None
    jobId: JobId | None
    targetSelection: TargetSelection | None
    status: JobStatus | None
    forceCanceled: Forced | None
    reasonCode: ReasonCode | None
    comment: Comment | None
    targets: JobTargets | None
    description: JobDescription | None
    presignedUrlConfig: PresignedUrlConfig | None
    jobExecutionsRolloutConfig: JobExecutionsRolloutConfig | None
    abortConfig: AbortConfig | None
    createdAt: DateType | None
    lastUpdatedAt: DateType | None
    completedAt: DateType | None
    jobProcessDetails: JobProcessDetails | None
    timeoutConfig: TimeoutConfig | None
    namespaceId: NamespaceId | None
    jobTemplateArn: JobTemplateArn | None
    jobExecutionsRetryConfig: JobExecutionsRetryConfig | None
    documentParameters: ParameterMap | None
    isConcurrent: BooleanWrapperObject | None
    schedulingConfig: SchedulingConfig | None
    scheduledJobRollouts: ScheduledJobRolloutList | None
    destinationPackageVersions: DestinationPackageVersions | None


class DescribeJobResponse(TypedDict, total=False):
    documentSource: JobDocumentSource | None
    job: Job | None


class DescribeJobTemplateRequest(ServiceRequest):
    jobTemplateId: JobTemplateId


class DescribeJobTemplateResponse(TypedDict, total=False):
    jobTemplateArn: JobTemplateArn | None
    jobTemplateId: JobTemplateId | None
    description: JobDescription | None
    documentSource: JobDocumentSource | None
    document: JobDocument | None
    createdAt: DateType | None
    presignedUrlConfig: PresignedUrlConfig | None
    jobExecutionsRolloutConfig: JobExecutionsRolloutConfig | None
    abortConfig: AbortConfig | None
    timeoutConfig: TimeoutConfig | None
    jobExecutionsRetryConfig: JobExecutionsRetryConfig | None
    maintenanceWindows: MaintenanceWindows | None
    destinationPackageVersions: DestinationPackageVersions | None


class DescribeManagedJobTemplateRequest(ServiceRequest):
    templateName: ManagedJobTemplateName
    templateVersion: ManagedTemplateVersion | None


class DocumentParameter(TypedDict, total=False):
    """A map of key-value pairs containing the patterns that need to be
    replaced in a managed template job document schema. You can use the
    description of each key as a guidance to specify the inputs during
    runtime when creating a job.

    ``documentParameters`` can only be used when creating jobs from Amazon
    Web Services managed templates. This parameter can't be used with custom
    job templates or to create jobs from them.
    """

    key: ParameterKey | None
    description: JobDescription | None
    regex: Regex | None
    example: Example | None
    optional: Optional_ | None


DocumentParameters = list[DocumentParameter]
Environments = list[Environment]


class DescribeManagedJobTemplateResponse(TypedDict, total=False):
    templateName: ManagedJobTemplateName | None
    templateArn: JobTemplateArn | None
    description: JobDescription | None
    templateVersion: ManagedTemplateVersion | None
    environments: Environments | None
    documentParameters: DocumentParameters | None
    document: JobDocument | None


class DescribeMitigationActionRequest(ServiceRequest):
    actionName: MitigationActionName


class DescribeMitigationActionResponse(TypedDict, total=False):
    actionName: MitigationActionName | None
    actionType: MitigationActionType | None
    actionArn: MitigationActionArn | None
    actionId: MitigationActionId | None
    roleArn: RoleArn | None
    actionParams: MitigationActionParams | None
    creationDate: Timestamp | None
    lastModifiedDate: Timestamp | None


class DescribeProvisioningTemplateRequest(ServiceRequest):
    templateName: TemplateName


class DescribeProvisioningTemplateResponse(TypedDict, total=False):
    templateArn: TemplateArn | None
    templateName: TemplateName | None
    description: TemplateDescription | None
    creationDate: DateType | None
    lastModifiedDate: DateType | None
    defaultVersionId: TemplateVersionId | None
    templateBody: TemplateBody | None
    enabled: Enabled | None
    provisioningRoleArn: RoleArn | None
    preProvisioningHook: ProvisioningHook | None
    type: TemplateType | None


class DescribeProvisioningTemplateVersionRequest(ServiceRequest):
    templateName: TemplateName
    versionId: TemplateVersionId


class DescribeProvisioningTemplateVersionResponse(TypedDict, total=False):
    versionId: TemplateVersionId | None
    creationDate: DateType | None
    templateBody: TemplateBody | None
    isDefaultVersion: IsDefaultVersion | None


class DescribeRoleAliasRequest(ServiceRequest):
    roleAlias: RoleAlias


class RoleAliasDescription(TypedDict, total=False):
    """Role alias description."""

    roleAlias: RoleAlias | None
    roleAliasArn: RoleAliasArn | None
    roleArn: RoleArn | None
    owner: AwsAccountId | None
    credentialDurationSeconds: CredentialDurationSeconds | None
    creationDate: DateType | None
    lastModifiedDate: DateType | None


class DescribeRoleAliasResponse(TypedDict, total=False):
    roleAliasDescription: RoleAliasDescription | None


class DescribeScheduledAuditRequest(ServiceRequest):
    scheduledAuditName: ScheduledAuditName


class DescribeScheduledAuditResponse(TypedDict, total=False):
    frequency: AuditFrequency | None
    dayOfMonth: DayOfMonth | None
    dayOfWeek: DayOfWeek | None
    targetCheckNames: TargetAuditCheckNames | None
    scheduledAuditName: ScheduledAuditName | None
    scheduledAuditArn: ScheduledAuditArn | None


class DescribeSecurityProfileRequest(ServiceRequest):
    securityProfileName: SecurityProfileName


class DescribeSecurityProfileResponse(TypedDict, total=False):
    securityProfileName: SecurityProfileName | None
    securityProfileArn: SecurityProfileArn | None
    securityProfileDescription: SecurityProfileDescription | None
    behaviors: Behaviors | None
    alertTargets: AlertTargets | None
    additionalMetricsToRetain: AdditionalMetricsToRetainList | None
    additionalMetricsToRetainV2: AdditionalMetricsToRetainV2List | None
    version: Version | None
    creationDate: Timestamp | None
    lastModifiedDate: Timestamp | None
    metricsExportConfig: MetricsExportConfig | None


class DescribeStreamRequest(ServiceRequest):
    streamId: StreamId


class StreamInfo(TypedDict, total=False):
    """Information about a stream."""

    streamId: StreamId | None
    streamArn: StreamArn | None
    streamVersion: StreamVersion | None
    description: StreamDescription | None
    files: StreamFiles | None
    createdAt: DateType | None
    lastUpdatedAt: DateType | None
    roleArn: RoleArn | None


class DescribeStreamResponse(TypedDict, total=False):
    streamInfo: StreamInfo | None


class DescribeThingGroupRequest(ServiceRequest):
    thingGroupName: ThingGroupName


ThingGroupNameAndArnList = list[GroupNameAndArn]


class ThingGroupMetadata(TypedDict, total=False):
    """Thing group metadata."""

    parentGroupName: ThingGroupName | None
    rootToParentThingGroups: ThingGroupNameAndArnList | None
    creationDate: CreationDate | None


class DescribeThingGroupResponse(TypedDict, total=False):
    thingGroupName: ThingGroupName | None
    thingGroupId: ThingGroupId | None
    thingGroupArn: ThingGroupArn | None
    version: Version | None
    thingGroupProperties: ThingGroupProperties | None
    thingGroupMetadata: ThingGroupMetadata | None
    indexName: IndexName | None
    queryString: QueryString | None
    queryVersion: QueryVersion | None
    status: DynamicGroupStatus | None


class DescribeThingRegistrationTaskRequest(ServiceRequest):
    taskId: TaskId


class DescribeThingRegistrationTaskResponse(TypedDict, total=False):
    taskId: TaskId | None
    creationDate: CreationDate | None
    lastModifiedDate: LastModifiedDate | None
    templateBody: TemplateBody | None
    inputFileBucket: RegistryS3BucketName | None
    inputFileKey: RegistryS3KeyName | None
    roleArn: RoleArn | None
    status: Status | None
    message: ErrorMessage | None
    successCount: Count | None
    failureCount: Count | None
    percentageProgress: Percentage | None


class DescribeThingRequest(ServiceRequest):
    """The input for the DescribeThing operation."""

    thingName: ThingName


class DescribeThingResponse(TypedDict, total=False):
    """The output from the DescribeThing operation."""

    defaultClientId: ClientId | None
    thingName: ThingName | None
    thingId: ThingId | None
    thingArn: ThingArn | None
    thingTypeName: ThingTypeName | None
    attributes: Attributes | None
    version: Version | None
    billingGroupName: BillingGroupName | None


class DescribeThingTypeRequest(ServiceRequest):
    """The input for the DescribeThingType operation."""

    thingTypeName: ThingTypeName


class ThingTypeMetadata(TypedDict, total=False):
    """The ThingTypeMetadata contains additional information about the thing
    type including: creation date and time, a value indicating whether the
    thing type is deprecated, and a date and time when time was deprecated.
    """

    deprecated: Boolean | None
    deprecationDate: DeprecationDate | None
    creationDate: CreationDate | None


class DescribeThingTypeResponse(TypedDict, total=False):
    """The output for the DescribeThingType operation."""

    thingTypeName: ThingTypeName | None
    thingTypeId: ThingTypeId | None
    thingTypeArn: ThingTypeArn | None
    thingTypeProperties: ThingTypeProperties | None
    thingTypeMetadata: ThingTypeMetadata | None


class DetachPolicyRequest(ServiceRequest):
    policyName: PolicyName
    target: PolicyTarget


class DetachPrincipalPolicyRequest(ServiceRequest):
    """The input for the DetachPrincipalPolicy operation."""

    policyName: PolicyName
    principal: Principal


class DetachSecurityProfileRequest(ServiceRequest):
    securityProfileName: SecurityProfileName
    securityProfileTargetArn: SecurityProfileTargetArn


class DetachSecurityProfileResponse(TypedDict, total=False):
    pass


class DetachThingPrincipalRequest(ServiceRequest):
    """The input for the DetachThingPrincipal operation."""

    thingName: ThingName
    principal: Principal


class DetachThingPrincipalResponse(TypedDict, total=False):
    """The output from the DetachThingPrincipal operation."""

    pass


class DetectMitigationActionExecution(TypedDict, total=False):
    """Describes which mitigation actions should be executed."""

    taskId: MitigationActionsTaskId | None
    violationId: ViolationId | None
    actionName: MitigationActionName | None
    thingName: DeviceDefenderThingName | None
    executionStartDate: Timestamp | None
    executionEndDate: Timestamp | None
    status: DetectMitigationActionExecutionStatus | None
    errorCode: DetectMitigationActionExecutionErrorCode | None
    message: ErrorMessage | None


DetectMitigationActionExecutionList = list[DetectMitigationActionExecution]
DetectMitigationActionsTaskSummaryList = list[DetectMitigationActionsTaskSummary]
DetectMitigationActionsToExecuteList = list[MitigationActionName]
DimensionNames = list[DimensionName]


class DisableTopicRuleRequest(ServiceRequest):
    """The input for the DisableTopicRuleRequest operation."""

    ruleName: RuleName


class DisassociateSbomFromPackageVersionRequest(ServiceRequest):
    packageName: PackageName
    versionName: VersionName
    clientToken: ClientToken | None


class DisassociateSbomFromPackageVersionResponse(TypedDict, total=False):
    pass


class DomainConfigurationSummary(TypedDict, total=False):
    """The summary of a domain configuration. A domain configuration specifies
    custom IoT-specific information about a domain. A domain configuration
    can be associated with an Amazon Web Services-managed domain (for
    example, dbc123defghijk.iot.us-west-2.amazonaws.com), a customer managed
    domain, or a default endpoint.

    -  Data

    -  Jobs

    -  CredentialProvider
    """

    domainConfigurationName: ReservedDomainConfigurationName | None
    domainConfigurationArn: DomainConfigurationArn | None
    serviceType: ServiceType | None


DomainConfigurations = list[DomainConfigurationSummary]


class EffectivePolicy(TypedDict, total=False):
    """The policy that has the effect on the authorization results."""

    policyName: PolicyName | None
    policyArn: PolicyArn | None
    policyDocument: PolicyDocument | None


EffectivePolicies = list[EffectivePolicy]


class EnableTopicRuleRequest(ServiceRequest):
    """The input for the EnableTopicRuleRequest operation."""

    ruleName: RuleName


class ErrorInfo(TypedDict, total=False):
    """Error information."""

    code: Code | None
    message: OTAUpdateErrorMessage | None


class Field(TypedDict, total=False):
    name: FieldName | None
    type: FieldType | None


Fields = list[Field]


class FleetMetricNameAndArn(TypedDict, total=False):
    """The name and ARN of a fleet metric."""

    metricName: FleetMetricName | None
    metricArn: FleetMetricArn | None


FleetMetricNameAndArnList = list[FleetMetricNameAndArn]


class GeoLocationTarget(TypedDict, total=False):
    """A geolocation target that you select to index. Each geolocation target
    contains a ``name`` and ``order`` key-value pair that specifies the
    geolocation target fields.
    """

    name: TargetFieldName | None
    order: TargetFieldOrder | None


GeoLocationsFilter = list[GeoLocationTarget]


class GetBehaviorModelTrainingSummariesRequest(ServiceRequest):
    securityProfileName: SecurityProfileName | None
    maxResults: TinyMaxResults | None
    nextToken: NextToken | None


class GetBehaviorModelTrainingSummariesResponse(TypedDict, total=False):
    summaries: BehaviorModelTrainingSummaries | None
    nextToken: NextToken | None


class GetBucketsAggregationRequest(ServiceRequest):
    indexName: IndexName | None
    queryString: QueryString
    aggregationField: AggregationField
    queryVersion: QueryVersion | None
    bucketsAggregationType: BucketsAggregationType


class GetBucketsAggregationResponse(TypedDict, total=False):
    totalCount: Count | None
    buckets: Buckets | None


class GetCardinalityRequest(ServiceRequest):
    indexName: IndexName | None
    queryString: QueryString
    aggregationField: AggregationField | None
    queryVersion: QueryVersion | None


class GetCardinalityResponse(TypedDict, total=False):
    cardinality: Count | None


class GetCommandExecutionRequest(ServiceRequest):
    executionId: CommandExecutionId
    targetArn: TargetArn
    includeResult: BooleanWrapperObject | None


class StatusReason(TypedDict, total=False):
    """Provide additional context about the status of a command execution using
    a reason code and description.
    """

    reasonCode: StatusReasonCode
    reasonDescription: StatusReasonDescription | None


class GetCommandExecutionResponse(TypedDict, total=False):
    executionId: CommandExecutionId | None
    commandArn: CommandArn | None
    targetArn: TargetArn | None
    status: CommandExecutionStatus | None
    statusReason: StatusReason | None
    result: CommandExecutionResultMap | None
    parameters: CommandExecutionParameterMap | None
    executionTimeoutSeconds: CommandExecutionTimeoutInSeconds | None
    createdAt: DateType | None
    lastUpdatedAt: DateType | None
    startedAt: DateType | None
    completedAt: DateType | None
    timeToLive: DateType | None


class GetCommandRequest(ServiceRequest):
    commandId: CommandId


class GetCommandResponse(TypedDict, total=False):
    commandId: CommandId | None
    commandArn: CommandArn | None
    namespace: CommandNamespace | None
    displayName: DisplayName | None
    description: CommandDescription | None
    mandatoryParameters: CommandParameterList | None
    payload: CommandPayload | None
    roleArn: RoleArn | None
    createdAt: DateType | None
    lastUpdatedAt: DateType | None
    deprecated: DeprecationFlag | None
    pendingDeletion: BooleanWrapperObject | None


class GetEffectivePoliciesRequest(ServiceRequest):
    principal: Principal | None
    cognitoIdentityPoolId: CognitoIdentityPoolId | None
    thingName: ThingName | None


class GetEffectivePoliciesResponse(TypedDict, total=False):
    effectivePolicies: EffectivePolicies | None


class GetIndexingConfigurationRequest(ServiceRequest):
    pass


class ThingGroupIndexingConfiguration(TypedDict, total=False):
    """Thing group indexing configuration."""

    thingGroupIndexingMode: ThingGroupIndexingMode
    managedFields: Fields | None
    customFields: Fields | None


NamedShadowNamesFilter = list[ShadowName]


class IndexingFilter(TypedDict, total=False):
    """Provides additional selections for named shadows and geolocation data.

    To add named shadows to your fleet indexing configuration, set
    ``namedShadowIndexingMode`` to be ON and specify your shadow names in
    ``namedShadowNames`` filter.

    To add geolocation data to your fleet indexing configuration:

    -  If you store geolocation data in a class/unnamed shadow, set
       ``thingIndexingMode`` to be ``REGISTRY_AND_SHADOW`` and specify your
       geolocation data in ``geoLocations`` filter.

    -  If you store geolocation data in a named shadow, set
       ``namedShadowIndexingMode`` to be ``ON``, add the shadow name in
       ``namedShadowNames`` filter, and specify your geolocation data in
       ``geoLocations`` filter. For more information, see `Managing fleet
       indexing <https://docs.aws.amazon.com/iot/latest/developerguide/managing-fleet-index.html>`__.
    """

    namedShadowNames: NamedShadowNamesFilter | None
    geoLocations: GeoLocationsFilter | None


class ThingIndexingConfiguration(TypedDict, total=False):
    """The thing indexing configuration. For more information, see `Managing
    Thing
    Indexing <https://docs.aws.amazon.com/iot/latest/developerguide/managing-index.html>`__.
    """

    thingIndexingMode: ThingIndexingMode
    thingConnectivityIndexingMode: ThingConnectivityIndexingMode | None
    deviceDefenderIndexingMode: DeviceDefenderIndexingMode | None
    namedShadowIndexingMode: NamedShadowIndexingMode | None
    managedFields: Fields | None
    customFields: Fields | None
    filter: IndexingFilter | None


class GetIndexingConfigurationResponse(TypedDict, total=False):
    thingIndexingConfiguration: ThingIndexingConfiguration | None
    thingGroupIndexingConfiguration: ThingGroupIndexingConfiguration | None


class GetJobDocumentRequest(ServiceRequest):
    jobId: JobId
    beforeSubstitution: BeforeSubstitutionFlag | None


class GetJobDocumentResponse(TypedDict, total=False):
    document: JobDocument | None


class GetLoggingOptionsRequest(ServiceRequest):
    """The input for the GetLoggingOptions operation."""

    pass


class GetLoggingOptionsResponse(TypedDict, total=False):
    """The output from the GetLoggingOptions operation."""

    roleArn: AwsArn | None
    logLevel: LogLevel | None


class GetOTAUpdateRequest(ServiceRequest):
    otaUpdateId: OTAUpdateId


class OTAUpdateInfo(TypedDict, total=False):
    """Information about an OTA update."""

    otaUpdateId: OTAUpdateId | None
    otaUpdateArn: OTAUpdateArn | None
    creationDate: DateType | None
    lastModifiedDate: DateType | None
    description: OTAUpdateDescription | None
    targets: Targets | None
    protocols: Protocols | None
    awsJobExecutionsRolloutConfig: AwsJobExecutionsRolloutConfig | None
    awsJobPresignedUrlConfig: AwsJobPresignedUrlConfig | None
    targetSelection: TargetSelection | None
    otaUpdateFiles: OTAUpdateFiles | None
    otaUpdateStatus: OTAUpdateStatus | None
    awsIotJobId: AwsIotJobId | None
    awsIotJobArn: AwsIotJobArn | None
    errorInfo: ErrorInfo | None
    additionalParameters: AdditionalParameterMap | None


class GetOTAUpdateResponse(TypedDict, total=False):
    otaUpdateInfo: OTAUpdateInfo | None


class GetPackageConfigurationRequest(ServiceRequest):
    pass


class VersionUpdateByJobsConfig(TypedDict, total=False):
    """Configuration to manage IoT Job's package version reporting. If
    configured, Jobs updates the thing's reserved named shadow with the
    package version information up on successful job completion.

    **Note:** For each job, the destinationPackageVersions attribute has to
    be set with the correct data for Jobs to report to the thing shadow.
    """

    enabled: EnabledBoolean | None
    roleArn: RoleArn | None


class GetPackageConfigurationResponse(TypedDict, total=False):
    versionUpdateByJobsConfig: VersionUpdateByJobsConfig | None


class GetPackageRequest(ServiceRequest):
    packageName: PackageName


class GetPackageResponse(TypedDict, total=False):
    packageName: PackageName | None
    packageArn: PackageArn | None
    description: ResourceDescription | None
    defaultVersionName: VersionName | None
    creationDate: CreationDate | None
    lastModifiedDate: LastModifiedDate | None


class GetPackageVersionRequest(ServiceRequest):
    packageName: PackageName
    versionName: VersionName


class GetPackageVersionResponse(TypedDict, total=False):
    packageVersionArn: PackageVersionArn | None
    packageName: PackageName | None
    versionName: VersionName | None
    description: ResourceDescription | None
    attributes: ResourceAttributes | None
    artifact: PackageVersionArtifact | None
    status: PackageVersionStatus | None
    errorReason: PackageVersionErrorReason | None
    creationDate: CreationDate | None
    lastModifiedDate: LastModifiedDate | None
    sbom: Sbom | None
    sbomValidationStatus: SbomValidationStatus | None
    recipe: PackageVersionRecipe | None


PercentList = list[Percent]


class GetPercentilesRequest(ServiceRequest):
    indexName: IndexName | None
    queryString: QueryString
    aggregationField: AggregationField | None
    queryVersion: QueryVersion | None
    percents: PercentList | None


class PercentPair(TypedDict, total=False):
    """Describes the percentile and percentile value."""

    percent: Percent | None
    value: PercentValue | None


Percentiles = list[PercentPair]


class GetPercentilesResponse(TypedDict, total=False):
    percentiles: Percentiles | None


class GetPolicyRequest(ServiceRequest):
    """The input for the GetPolicy operation."""

    policyName: PolicyName


class GetPolicyResponse(TypedDict, total=False):
    """The output from the GetPolicy operation."""

    policyName: PolicyName | None
    policyArn: PolicyArn | None
    policyDocument: PolicyDocument | None
    defaultVersionId: PolicyVersionId | None
    creationDate: DateType | None
    lastModifiedDate: DateType | None
    generationId: GenerationId | None


class GetPolicyVersionRequest(ServiceRequest):
    """The input for the GetPolicyVersion operation."""

    policyName: PolicyName
    policyVersionId: PolicyVersionId


class GetPolicyVersionResponse(TypedDict, total=False):
    """The output from the GetPolicyVersion operation."""

    policyArn: PolicyArn | None
    policyName: PolicyName | None
    policyDocument: PolicyDocument | None
    policyVersionId: PolicyVersionId | None
    isDefaultVersion: IsDefaultVersion | None
    creationDate: DateType | None
    lastModifiedDate: DateType | None
    generationId: GenerationId | None


class GetRegistrationCodeRequest(ServiceRequest):
    """The input to the GetRegistrationCode operation."""

    pass


class GetRegistrationCodeResponse(TypedDict, total=False):
    """The output from the GetRegistrationCode operation."""

    registrationCode: RegistrationCode | None


class GetStatisticsRequest(ServiceRequest):
    indexName: IndexName | None
    queryString: QueryString
    aggregationField: AggregationField | None
    queryVersion: QueryVersion | None


class Statistics(TypedDict, total=False):
    """A map of key-value pairs for all supported statistics. For issues with
    missing or unexpected values for this API, consult `Fleet indexing
    troubleshooting
    guide <https://docs.aws.amazon.com/iot/latest/developerguide/fleet-indexing-troubleshooting.html>`__.
    """

    count: Count | None
    average: Average | None
    sum: Sum | None
    minimum: Minimum | None
    maximum: Maximum | None
    sumOfSquares: SumOfSquares | None
    variance: Variance | None
    stdDeviation: StdDeviation | None


class GetStatisticsResponse(TypedDict, total=False):
    statistics: Statistics | None


class GetThingConnectivityDataRequest(ServiceRequest):
    thingName: ConnectivityApiThingName


class GetThingConnectivityDataResponse(TypedDict, total=False):
    thingName: ConnectivityApiThingName | None
    connected: Boolean | None
    timestamp: Timestamp | None
    disconnectReason: DisconnectReasonValue | None


class GetTopicRuleDestinationRequest(ServiceRequest):
    arn: AwsArn


class GetTopicRuleDestinationResponse(TypedDict, total=False):
    topicRuleDestination: TopicRuleDestination | None


class GetTopicRuleRequest(ServiceRequest):
    """The input for the GetTopicRule operation."""

    ruleName: RuleName


class TopicRule(TypedDict, total=False):
    """Describes a rule."""

    ruleName: RuleName | None
    sql: SQL | None
    description: Description | None
    createdAt: CreatedAtDate | None
    actions: ActionList | None
    ruleDisabled: IsDisabled | None
    awsIotSqlVersion: AwsIotSqlVersion | None
    errorAction: Action | None


class GetTopicRuleResponse(TypedDict, total=False):
    """The output from the GetTopicRule operation."""

    ruleArn: RuleArn | None
    rule: TopicRule | None


class GetV2LoggingOptionsRequest(ServiceRequest):
    pass


class GetV2LoggingOptionsResponse(TypedDict, total=False):
    roleArn: AwsArn | None
    defaultLogLevel: LogLevel | None
    disableAllLogs: DisableAllLogs | None


HttpHeaders = dict[HttpHeaderName, HttpHeaderValue]


class HttpContext(TypedDict, total=False):
    """Specifies the HTTP context to use for the test authorizer request."""

    headers: HttpHeaders | None
    queryString: HttpQueryString | None


class HttpUrlDestinationSummary(TypedDict, total=False):
    """Information about an HTTP URL destination."""

    confirmationUrl: Url | None


IndexNamesList = list[IndexName]


class JobExecutionSummary(TypedDict, total=False):
    """The job execution summary."""

    status: JobExecutionStatus | None
    queuedAt: DateType | None
    startedAt: DateType | None
    lastUpdatedAt: DateType | None
    executionNumber: ExecutionNumber | None
    retryAttempt: RetryAttempt | None


class JobExecutionSummaryForJob(TypedDict, total=False):
    """Contains a summary of information about job executions for a specific
    job.
    """

    thingArn: ThingArn | None
    jobExecutionSummary: JobExecutionSummary | None


JobExecutionSummaryForJobList = list[JobExecutionSummaryForJob]


class JobExecutionSummaryForThing(TypedDict, total=False):
    """The job execution summary for a thing."""

    jobId: JobId | None
    jobExecutionSummary: JobExecutionSummary | None


JobExecutionSummaryForThingList = list[JobExecutionSummaryForThing]


class JobSummary(TypedDict, total=False):
    """The job summary."""

    jobArn: JobArn | None
    jobId: JobId | None
    thingGroupId: ThingGroupId | None
    targetSelection: TargetSelection | None
    status: JobStatus | None
    createdAt: DateType | None
    lastUpdatedAt: DateType | None
    completedAt: DateType | None
    isConcurrent: BooleanWrapperObject | None


JobSummaryList = list[JobSummary]


class JobTemplateSummary(TypedDict, total=False):
    """An object that contains information about the job template."""

    jobTemplateArn: JobTemplateArn | None
    jobTemplateId: JobTemplateId | None
    description: JobDescription | None
    createdAt: DateType | None


JobTemplateSummaryList = list[JobTemplateSummary]


class ListActiveViolationsRequest(ServiceRequest):
    thingName: DeviceDefenderThingName | None
    securityProfileName: SecurityProfileName | None
    behaviorCriteriaType: BehaviorCriteriaType | None
    listSuppressedAlerts: ListSuppressedAlerts | None
    verificationState: VerificationState | None
    nextToken: NextToken | None
    maxResults: MaxResults | None


class ListActiveViolationsResponse(TypedDict, total=False):
    activeViolations: ActiveViolations | None
    nextToken: NextToken | None


class ListAttachedPoliciesRequest(ServiceRequest):
    target: PolicyTarget
    recursive: Recursive | None
    marker: Marker | None
    pageSize: PageSize | None


class ListAttachedPoliciesResponse(TypedDict, total=False):
    policies: Policies | None
    nextMarker: Marker | None


class ListAuditFindingsRequest(ServiceRequest):
    taskId: AuditTaskId | None
    checkName: AuditCheckName | None
    resourceIdentifier: ResourceIdentifier | None
    maxResults: MaxResults | None
    nextToken: NextToken | None
    startTime: Timestamp | None
    endTime: Timestamp | None
    listSuppressedFindings: ListSuppressedFindings | None


class ListAuditFindingsResponse(TypedDict, total=False):
    findings: AuditFindings | None
    nextToken: NextToken | None


class ListAuditMitigationActionsExecutionsRequest(ServiceRequest):
    taskId: MitigationActionsTaskId
    actionStatus: AuditMitigationActionsExecutionStatus | None
    findingId: FindingId
    maxResults: MaxResults | None
    nextToken: NextToken | None


class ListAuditMitigationActionsExecutionsResponse(TypedDict, total=False):
    actionsExecutions: AuditMitigationActionExecutionMetadataList | None
    nextToken: NextToken | None


class ListAuditMitigationActionsTasksRequest(ServiceRequest):
    auditTaskId: AuditTaskId | None
    findingId: FindingId | None
    taskStatus: AuditMitigationActionsTaskStatus | None
    maxResults: MaxResults | None
    nextToken: NextToken | None
    startTime: Timestamp
    endTime: Timestamp


class ListAuditMitigationActionsTasksResponse(TypedDict, total=False):
    tasks: AuditMitigationActionsTaskMetadataList | None
    nextToken: NextToken | None


class ListAuditSuppressionsRequest(ServiceRequest):
    checkName: AuditCheckName | None
    resourceIdentifier: ResourceIdentifier | None
    ascendingOrder: AscendingOrder | None
    nextToken: NextToken | None
    maxResults: MaxResults | None


class ListAuditSuppressionsResponse(TypedDict, total=False):
    suppressions: AuditSuppressionList | None
    nextToken: NextToken | None


class ListAuditTasksRequest(ServiceRequest):
    startTime: Timestamp
    endTime: Timestamp
    taskType: AuditTaskType | None
    taskStatus: AuditTaskStatus | None
    nextToken: NextToken | None
    maxResults: MaxResults | None


class ListAuditTasksResponse(TypedDict, total=False):
    tasks: AuditTaskMetadataList | None
    nextToken: NextToken | None


class ListAuthorizersRequest(ServiceRequest):
    pageSize: PageSize | None
    marker: Marker | None
    ascendingOrder: AscendingOrder | None
    status: AuthorizerStatus | None


class ListAuthorizersResponse(TypedDict, total=False):
    authorizers: Authorizers | None
    nextMarker: Marker | None


class ListBillingGroupsRequest(ServiceRequest):
    nextToken: NextToken | None
    maxResults: RegistryMaxResults | None
    namePrefixFilter: BillingGroupName | None


class ListBillingGroupsResponse(TypedDict, total=False):
    billingGroups: BillingGroupNameAndArnList | None
    nextToken: NextToken | None


class ListCACertificatesRequest(ServiceRequest):
    """Input for the ListCACertificates operation."""

    pageSize: PageSize | None
    marker: Marker | None
    ascendingOrder: AscendingOrder | None
    templateName: TemplateName | None


class ListCACertificatesResponse(TypedDict, total=False):
    """The output from the ListCACertificates operation."""

    certificates: CACertificates | None
    nextMarker: Marker | None


class ListCertificateProvidersRequest(ServiceRequest):
    nextToken: Marker | None
    ascendingOrder: AscendingOrder | None


class ListCertificateProvidersResponse(TypedDict, total=False):
    certificateProviders: CertificateProviders | None
    nextToken: Marker | None


class ListCertificatesByCARequest(ServiceRequest):
    """The input to the ListCertificatesByCA operation."""

    caCertificateId: CertificateId
    pageSize: PageSize | None
    marker: Marker | None
    ascendingOrder: AscendingOrder | None


class ListCertificatesByCAResponse(TypedDict, total=False):
    """The output of the ListCertificatesByCA operation."""

    certificates: Certificates | None
    nextMarker: Marker | None


class ListCertificatesRequest(ServiceRequest):
    """The input for the ListCertificates operation."""

    pageSize: PageSize | None
    marker: Marker | None
    ascendingOrder: AscendingOrder | None


class ListCertificatesResponse(TypedDict, total=False):
    """The output of the ListCertificates operation."""

    certificates: Certificates | None
    nextMarker: Marker | None


class TimeFilter(TypedDict, total=False):
    """A filter that can be used to list command executions for a device that
    started or completed before or after a particular date and time.
    """

    after: StringDateTime | None
    before: StringDateTime | None


class ListCommandExecutionsRequest(ServiceRequest):
    maxResults: CommandMaxResults | None
    nextToken: NextToken | None
    namespace: CommandNamespace | None
    status: CommandExecutionStatus | None
    sortOrder: SortOrder | None
    startedTimeFilter: TimeFilter | None
    completedTimeFilter: TimeFilter | None
    targetArn: TargetArn | None
    commandArn: CommandArn | None


class ListCommandExecutionsResponse(TypedDict, total=False):
    commandExecutions: CommandExecutionSummaryList | None
    nextToken: NextToken | None


class ListCommandsRequest(ServiceRequest):
    maxResults: CommandMaxResults | None
    nextToken: NextToken | None
    namespace: CommandNamespace | None
    commandParameterName: CommandParameterName | None
    sortOrder: SortOrder | None


class ListCommandsResponse(TypedDict, total=False):
    commands: CommandSummaryList | None
    nextToken: NextToken | None


class ListCustomMetricsRequest(ServiceRequest):
    nextToken: NextToken | None
    maxResults: MaxResults | None


MetricNames = list[MetricName]


class ListCustomMetricsResponse(TypedDict, total=False):
    metricNames: MetricNames | None
    nextToken: NextToken | None


class ListDetectMitigationActionsExecutionsRequest(ServiceRequest):
    taskId: MitigationActionsTaskId | None
    violationId: ViolationId | None
    thingName: DeviceDefenderThingName | None
    startTime: Timestamp | None
    endTime: Timestamp | None
    maxResults: MaxResults | None
    nextToken: NextToken | None


class ListDetectMitigationActionsExecutionsResponse(TypedDict, total=False):
    actionsExecutions: DetectMitigationActionExecutionList | None
    nextToken: NextToken | None


class ListDetectMitigationActionsTasksRequest(ServiceRequest):
    maxResults: MaxResults | None
    nextToken: NextToken | None
    startTime: Timestamp
    endTime: Timestamp


class ListDetectMitigationActionsTasksResponse(TypedDict, total=False):
    tasks: DetectMitigationActionsTaskSummaryList | None
    nextToken: NextToken | None


class ListDimensionsRequest(ServiceRequest):
    nextToken: NextToken | None
    maxResults: MaxResults | None


class ListDimensionsResponse(TypedDict, total=False):
    dimensionNames: DimensionNames | None
    nextToken: NextToken | None


class ListDomainConfigurationsRequest(ServiceRequest):
    marker: Marker | None
    pageSize: PageSize | None
    serviceType: ServiceType | None


class ListDomainConfigurationsResponse(TypedDict, total=False):
    domainConfigurations: DomainConfigurations | None
    nextMarker: Marker | None


class ListFleetMetricsRequest(ServiceRequest):
    nextToken: NextToken | None
    maxResults: MaxResults | None


class ListFleetMetricsResponse(TypedDict, total=False):
    fleetMetrics: FleetMetricNameAndArnList | None
    nextToken: NextToken | None


class ListIndicesRequest(ServiceRequest):
    nextToken: NextToken | None
    maxResults: QueryMaxResults | None


class ListIndicesResponse(TypedDict, total=False):
    indexNames: IndexNamesList | None
    nextToken: NextToken | None


class ListJobExecutionsForJobRequest(ServiceRequest):
    jobId: JobId
    status: JobExecutionStatus | None
    maxResults: LaserMaxResults | None
    nextToken: NextToken | None


class ListJobExecutionsForJobResponse(TypedDict, total=False):
    executionSummaries: JobExecutionSummaryForJobList | None
    nextToken: NextToken | None


class ListJobExecutionsForThingRequest(ServiceRequest):
    thingName: ThingName
    status: JobExecutionStatus | None
    namespaceId: NamespaceId | None
    maxResults: LaserMaxResults | None
    nextToken: NextToken | None
    jobId: JobId | None


class ListJobExecutionsForThingResponse(TypedDict, total=False):
    executionSummaries: JobExecutionSummaryForThingList | None
    nextToken: NextToken | None


class ListJobTemplatesRequest(ServiceRequest):
    maxResults: LaserMaxResults | None
    nextToken: NextToken | None


class ListJobTemplatesResponse(TypedDict, total=False):
    jobTemplates: JobTemplateSummaryList | None
    nextToken: NextToken | None


class ListJobsRequest(ServiceRequest):
    status: JobStatus | None
    targetSelection: TargetSelection | None
    maxResults: LaserMaxResults | None
    nextToken: NextToken | None
    thingGroupName: ThingGroupName | None
    thingGroupId: ThingGroupId | None
    namespaceId: NamespaceId | None


class ListJobsResponse(TypedDict, total=False):
    jobs: JobSummaryList | None
    nextToken: NextToken | None


class ListManagedJobTemplatesRequest(ServiceRequest):
    templateName: ManagedJobTemplateName | None
    maxResults: LaserMaxResults | None
    nextToken: NextToken | None


class ManagedJobTemplateSummary(TypedDict, total=False):
    """An object that contains information about the managed template."""

    templateArn: JobTemplateArn | None
    templateName: ManagedJobTemplateName | None
    description: JobDescription | None
    environments: Environments | None
    templateVersion: ManagedTemplateVersion | None


ManagedJobTemplatesSummaryList = list[ManagedJobTemplateSummary]


class ListManagedJobTemplatesResponse(TypedDict, total=False):
    managedJobTemplates: ManagedJobTemplatesSummaryList | None
    nextToken: NextToken | None


class ListMetricValuesRequest(ServiceRequest):
    thingName: DeviceDefenderThingName
    metricName: BehaviorMetric
    dimensionName: DimensionName | None
    dimensionValueOperator: DimensionValueOperator | None
    startTime: Timestamp
    endTime: Timestamp
    maxResults: MaxResults | None
    nextToken: NextToken | None


class MetricDatum(TypedDict, total=False):
    """A metric."""

    timestamp: Timestamp | None
    value: MetricValue | None


MetricDatumList = list[MetricDatum]


class ListMetricValuesResponse(TypedDict, total=False):
    metricDatumList: MetricDatumList | None
    nextToken: NextToken | None


class ListMitigationActionsRequest(ServiceRequest):
    actionType: MitigationActionType | None
    maxResults: MaxResults | None
    nextToken: NextToken | None


class MitigationActionIdentifier(TypedDict, total=False):
    """Information that identifies a mitigation action. This information is
    returned by ListMitigationActions.
    """

    actionName: MitigationActionName | None
    actionArn: MitigationActionArn | None
    creationDate: Timestamp | None


MitigationActionIdentifierList = list[MitigationActionIdentifier]


class ListMitigationActionsResponse(TypedDict, total=False):
    actionIdentifiers: MitigationActionIdentifierList | None
    nextToken: NextToken | None


class ListOTAUpdatesRequest(ServiceRequest):
    maxResults: MaxResults | None
    nextToken: NextToken | None
    otaUpdateStatus: OTAUpdateStatus | None


class OTAUpdateSummary(TypedDict, total=False):
    """An OTA update summary."""

    otaUpdateId: OTAUpdateId | None
    otaUpdateArn: OTAUpdateArn | None
    creationDate: DateType | None


OTAUpdatesSummary = list[OTAUpdateSummary]


class ListOTAUpdatesResponse(TypedDict, total=False):
    otaUpdates: OTAUpdatesSummary | None
    nextToken: NextToken | None


class ListOutgoingCertificatesRequest(ServiceRequest):
    """The input to the ListOutgoingCertificates operation."""

    pageSize: PageSize | None
    marker: Marker | None
    ascendingOrder: AscendingOrder | None


class OutgoingCertificate(TypedDict, total=False):
    """A certificate that has been transferred but not yet accepted."""

    certificateArn: CertificateArn | None
    certificateId: CertificateId | None
    transferredTo: AwsAccountId | None
    transferDate: DateType | None
    transferMessage: Message | None
    creationDate: DateType | None


OutgoingCertificates = list[OutgoingCertificate]


class ListOutgoingCertificatesResponse(TypedDict, total=False):
    """The output from the ListOutgoingCertificates operation."""

    outgoingCertificates: OutgoingCertificates | None
    nextMarker: Marker | None


class ListPackageVersionsRequest(ServiceRequest):
    packageName: PackageName
    status: PackageVersionStatus | None
    maxResults: PackageCatalogMaxResults | None
    nextToken: NextToken | None


class PackageVersionSummary(TypedDict, total=False):
    """A summary of information about a package version."""

    packageName: PackageName | None
    versionName: VersionName | None
    status: PackageVersionStatus | None
    creationDate: CreationDate | None
    lastModifiedDate: LastModifiedDate | None


PackageVersionSummaryList = list[PackageVersionSummary]


class ListPackageVersionsResponse(TypedDict, total=False):
    packageVersionSummaries: PackageVersionSummaryList | None
    nextToken: NextToken | None


class ListPackagesRequest(ServiceRequest):
    maxResults: PackageCatalogMaxResults | None
    nextToken: NextToken | None


class PackageSummary(TypedDict, total=False):
    """A summary of information about a software package."""

    packageName: PackageName | None
    defaultVersionName: VersionName | None
    creationDate: CreationDate | None
    lastModifiedDate: LastModifiedDate | None


PackageSummaryList = list[PackageSummary]


class ListPackagesResponse(TypedDict, total=False):
    packageSummaries: PackageSummaryList | None
    nextToken: NextToken | None


class ListPoliciesRequest(ServiceRequest):
    """The input for the ListPolicies operation."""

    marker: Marker | None
    pageSize: PageSize | None
    ascendingOrder: AscendingOrder | None


class ListPoliciesResponse(TypedDict, total=False):
    """The output from the ListPolicies operation."""

    policies: Policies | None
    nextMarker: Marker | None


class ListPolicyPrincipalsRequest(ServiceRequest):
    """The input for the ListPolicyPrincipals operation."""

    policyName: PolicyName
    marker: Marker | None
    pageSize: PageSize | None
    ascendingOrder: AscendingOrder | None


Principals = list[PrincipalArn]


class ListPolicyPrincipalsResponse(TypedDict, total=False):
    """The output from the ListPolicyPrincipals operation."""

    principals: Principals | None
    nextMarker: Marker | None


class ListPolicyVersionsRequest(ServiceRequest):
    """The input for the ListPolicyVersions operation."""

    policyName: PolicyName


class PolicyVersion(TypedDict, total=False):
    """Describes a policy version."""

    versionId: PolicyVersionId | None
    isDefaultVersion: IsDefaultVersion | None
    createDate: DateType | None


PolicyVersions = list[PolicyVersion]


class ListPolicyVersionsResponse(TypedDict, total=False):
    """The output from the ListPolicyVersions operation."""

    policyVersions: PolicyVersions | None


class ListPrincipalPoliciesRequest(ServiceRequest):
    """The input for the ListPrincipalPolicies operation."""

    principal: Principal
    marker: Marker | None
    pageSize: PageSize | None
    ascendingOrder: AscendingOrder | None


class ListPrincipalPoliciesResponse(TypedDict, total=False):
    """The output from the ListPrincipalPolicies operation."""

    policies: Policies | None
    nextMarker: Marker | None


class ListPrincipalThingsRequest(ServiceRequest):
    """The input for the ListPrincipalThings operation."""

    nextToken: NextToken | None
    maxResults: RegistryMaxResults | None
    principal: Principal


ThingNameList = list[ThingName]


class ListPrincipalThingsResponse(TypedDict, total=False):
    """The output from the ListPrincipalThings operation."""

    things: ThingNameList | None
    nextToken: NextToken | None


class ListPrincipalThingsV2Request(ServiceRequest):
    nextToken: NextToken | None
    maxResults: RegistryMaxResults | None
    principal: Principal
    thingPrincipalType: ThingPrincipalType | None


class PrincipalThingObject(TypedDict, total=False):
    """An object that represents the thing and the type of relation it has with
    the principal.
    """

    thingName: ThingName
    thingPrincipalType: ThingPrincipalType | None


PrincipalThingObjects = list[PrincipalThingObject]


class ListPrincipalThingsV2Response(TypedDict, total=False):
    principalThingObjects: PrincipalThingObjects | None
    nextToken: NextToken | None


class ListProvisioningTemplateVersionsRequest(ServiceRequest):
    templateName: TemplateName
    maxResults: MaxResults | None
    nextToken: NextToken | None


class ProvisioningTemplateVersionSummary(TypedDict, total=False):
    """A summary of information about a fleet provision template version."""

    versionId: TemplateVersionId | None
    creationDate: DateType | None
    isDefaultVersion: IsDefaultVersion | None


ProvisioningTemplateVersionListing = list[ProvisioningTemplateVersionSummary]


class ListProvisioningTemplateVersionsResponse(TypedDict, total=False):
    versions: ProvisioningTemplateVersionListing | None
    nextToken: NextToken | None


class ListProvisioningTemplatesRequest(ServiceRequest):
    maxResults: MaxResults | None
    nextToken: NextToken | None


class ProvisioningTemplateSummary(TypedDict, total=False):
    templateArn: TemplateArn | None
    templateName: TemplateName | None
    description: TemplateDescription | None
    creationDate: DateType | None
    lastModifiedDate: DateType | None
    enabled: Enabled | None
    type: TemplateType | None


ProvisioningTemplateListing = list[ProvisioningTemplateSummary]


class ListProvisioningTemplatesResponse(TypedDict, total=False):
    templates: ProvisioningTemplateListing | None
    nextToken: NextToken | None


class ListRelatedResourcesForAuditFindingRequest(ServiceRequest):
    findingId: FindingId
    nextToken: NextToken | None
    maxResults: MaxResults | None


class ListRelatedResourcesForAuditFindingResponse(TypedDict, total=False):
    relatedResources: RelatedResources | None
    nextToken: NextToken | None


class ListRoleAliasesRequest(ServiceRequest):
    pageSize: PageSize | None
    marker: Marker | None
    ascendingOrder: AscendingOrder | None


RoleAliases = list[RoleAlias]


class ListRoleAliasesResponse(TypedDict, total=False):
    roleAliases: RoleAliases | None
    nextMarker: Marker | None


class ListSbomValidationResultsRequest(ServiceRequest):
    packageName: PackageName
    versionName: VersionName
    validationResult: SbomValidationResult | None
    maxResults: PackageCatalogMaxResults | None
    nextToken: NextToken | None


class SbomValidationResultSummary(TypedDict, total=False):
    """A summary of the validation results for a specific software bill of
    materials (SBOM) attached to a software package version.
    """

    fileName: FileName | None
    validationResult: SbomValidationResult | None
    errorCode: SbomValidationErrorCode | None
    errorMessage: SbomValidationErrorMessage | None


SbomValidationResultSummaryList = list[SbomValidationResultSummary]


class ListSbomValidationResultsResponse(TypedDict, total=False):
    validationResultSummaries: SbomValidationResultSummaryList | None
    nextToken: NextToken | None


class ListScheduledAuditsRequest(ServiceRequest):
    nextToken: NextToken | None
    maxResults: MaxResults | None


class ScheduledAuditMetadata(TypedDict, total=False):
    """Information about the scheduled audit."""

    scheduledAuditName: ScheduledAuditName | None
    scheduledAuditArn: ScheduledAuditArn | None
    frequency: AuditFrequency | None
    dayOfMonth: DayOfMonth | None
    dayOfWeek: DayOfWeek | None


ScheduledAuditMetadataList = list[ScheduledAuditMetadata]


class ListScheduledAuditsResponse(TypedDict, total=False):
    scheduledAudits: ScheduledAuditMetadataList | None
    nextToken: NextToken | None


class ListSecurityProfilesForTargetRequest(ServiceRequest):
    nextToken: NextToken | None
    maxResults: MaxResults | None
    recursive: Recursive | None
    securityProfileTargetArn: SecurityProfileTargetArn


class SecurityProfileTarget(TypedDict, total=False):
    """A target to which an alert is sent when a security profile behavior is
    violated.
    """

    arn: SecurityProfileTargetArn


class SecurityProfileIdentifier(TypedDict, total=False):
    """Identifying information for a Device Defender security profile."""

    name: SecurityProfileName
    arn: SecurityProfileArn


class SecurityProfileTargetMapping(TypedDict, total=False):
    """Information about a security profile and the target associated with it."""

    securityProfileIdentifier: SecurityProfileIdentifier | None
    target: SecurityProfileTarget | None


SecurityProfileTargetMappings = list[SecurityProfileTargetMapping]


class ListSecurityProfilesForTargetResponse(TypedDict, total=False):
    securityProfileTargetMappings: SecurityProfileTargetMappings | None
    nextToken: NextToken | None


class ListSecurityProfilesRequest(ServiceRequest):
    nextToken: NextToken | None
    maxResults: MaxResults | None
    dimensionName: DimensionName | None
    metricName: MetricName | None


SecurityProfileIdentifiers = list[SecurityProfileIdentifier]


class ListSecurityProfilesResponse(TypedDict, total=False):
    securityProfileIdentifiers: SecurityProfileIdentifiers | None
    nextToken: NextToken | None


class ListStreamsRequest(ServiceRequest):
    maxResults: MaxResults | None
    nextToken: NextToken | None
    ascendingOrder: AscendingOrder | None


class StreamSummary(TypedDict, total=False):
    """A summary of a stream."""

    streamId: StreamId | None
    streamArn: StreamArn | None
    streamVersion: StreamVersion | None
    description: StreamDescription | None


StreamsSummary = list[StreamSummary]


class ListStreamsResponse(TypedDict, total=False):
    streams: StreamsSummary | None
    nextToken: NextToken | None


class ListTagsForResourceRequest(ServiceRequest):
    resourceArn: ResourceArn
    nextToken: NextToken | None


class ListTagsForResourceResponse(TypedDict, total=False):
    tags: TagList | None
    nextToken: NextToken | None


class ListTargetsForPolicyRequest(ServiceRequest):
    policyName: PolicyName
    marker: Marker | None
    pageSize: PageSize | None


PolicyTargets = list[PolicyTarget]


class ListTargetsForPolicyResponse(TypedDict, total=False):
    targets: PolicyTargets | None
    nextMarker: Marker | None


class ListTargetsForSecurityProfileRequest(ServiceRequest):
    securityProfileName: SecurityProfileName
    nextToken: NextToken | None
    maxResults: MaxResults | None


SecurityProfileTargets = list[SecurityProfileTarget]


class ListTargetsForSecurityProfileResponse(TypedDict, total=False):
    securityProfileTargets: SecurityProfileTargets | None
    nextToken: NextToken | None


class ListThingGroupsForThingRequest(ServiceRequest):
    thingName: ThingName
    nextToken: NextToken | None
    maxResults: RegistryMaxResults | None


class ListThingGroupsForThingResponse(TypedDict, total=False):
    thingGroups: ThingGroupNameAndArnList | None
    nextToken: NextToken | None


class ListThingGroupsRequest(ServiceRequest):
    nextToken: NextToken | None
    maxResults: RegistryMaxResults | None
    parentGroup: ThingGroupName | None
    namePrefixFilter: ThingGroupName | None
    recursive: RecursiveWithoutDefault | None


class ListThingGroupsResponse(TypedDict, total=False):
    thingGroups: ThingGroupNameAndArnList | None
    nextToken: NextToken | None


class ListThingPrincipalsRequest(ServiceRequest):
    """The input for the ListThingPrincipal operation."""

    nextToken: NextToken | None
    maxResults: RegistryMaxResults | None
    thingName: ThingName


class ListThingPrincipalsResponse(TypedDict, total=False):
    """The output from the ListThingPrincipals operation."""

    principals: Principals | None
    nextToken: NextToken | None


class ListThingPrincipalsV2Request(ServiceRequest):
    nextToken: NextToken | None
    maxResults: RegistryMaxResults | None
    thingName: ThingName
    thingPrincipalType: ThingPrincipalType | None


class ThingPrincipalObject(TypedDict, total=False):
    """An object that represents the principal and the type of relation it has
    with the thing.
    """

    principal: Principal
    thingPrincipalType: ThingPrincipalType | None


ThingPrincipalObjects = list[ThingPrincipalObject]


class ListThingPrincipalsV2Response(TypedDict, total=False):
    thingPrincipalObjects: ThingPrincipalObjects | None
    nextToken: NextToken | None


class ListThingRegistrationTaskReportsRequest(ServiceRequest):
    taskId: TaskId
    reportType: ReportType
    nextToken: NextToken | None
    maxResults: RegistryMaxResults | None


S3FileUrlList = list[S3FileUrl]


class ListThingRegistrationTaskReportsResponse(TypedDict, total=False):
    resourceLinks: S3FileUrlList | None
    reportType: ReportType | None
    nextToken: NextToken | None


class ListThingRegistrationTasksRequest(ServiceRequest):
    nextToken: NextToken | None
    maxResults: RegistryMaxResults | None
    status: Status | None


TaskIdList = list[TaskId]


class ListThingRegistrationTasksResponse(TypedDict, total=False):
    taskIds: TaskIdList | None
    nextToken: NextToken | None


class ListThingTypesRequest(ServiceRequest):
    """The input for the ListThingTypes operation."""

    nextToken: NextToken | None
    maxResults: RegistryMaxResults | None
    thingTypeName: ThingTypeName | None


class ThingTypeDefinition(TypedDict, total=False):
    """The definition of the thing type, including thing type name and
    description.
    """

    thingTypeName: ThingTypeName | None
    thingTypeArn: ThingTypeArn | None
    thingTypeProperties: ThingTypeProperties | None
    thingTypeMetadata: ThingTypeMetadata | None


ThingTypeList = list[ThingTypeDefinition]


class ListThingTypesResponse(TypedDict, total=False):
    """The output for the ListThingTypes operation."""

    thingTypes: ThingTypeList | None
    nextToken: NextToken | None


class ListThingsInBillingGroupRequest(ServiceRequest):
    billingGroupName: BillingGroupName
    nextToken: NextToken | None
    maxResults: RegistryMaxResults | None


class ListThingsInBillingGroupResponse(TypedDict, total=False):
    things: ThingNameList | None
    nextToken: NextToken | None


class ListThingsInThingGroupRequest(ServiceRequest):
    thingGroupName: ThingGroupName
    recursive: Recursive | None
    nextToken: NextToken | None
    maxResults: RegistryMaxResults | None


class ListThingsInThingGroupResponse(TypedDict, total=False):
    things: ThingNameList | None
    nextToken: NextToken | None


class ListThingsRequest(ServiceRequest):
    """The input for the ListThings operation."""

    nextToken: NextToken | None
    maxResults: RegistryMaxResults | None
    attributeName: AttributeName | None
    attributeValue: AttributeValue | None
    thingTypeName: ThingTypeName | None
    usePrefixAttributeValue: usePrefixAttributeValue | None


class ThingAttribute(TypedDict, total=False):
    """The properties of the thing, including thing name, thing type name, and
    a list of thing attributes.
    """

    thingName: ThingName | None
    thingTypeName: ThingTypeName | None
    thingArn: ThingArn | None
    attributes: Attributes | None
    version: Version | None


ThingAttributeList = list[ThingAttribute]


class ListThingsResponse(TypedDict, total=False):
    """The output from the ListThings operation."""

    things: ThingAttributeList | None
    nextToken: NextToken | None


class ListTopicRuleDestinationsRequest(ServiceRequest):
    maxResults: TopicRuleDestinationMaxResults | None
    nextToken: NextToken | None


class VpcDestinationSummary(TypedDict, total=False):
    """The summary of a virtual private cloud (VPC) destination."""

    subnetIds: SubnetIdList | None
    securityGroups: SecurityGroupList | None
    vpcId: VpcId | None
    roleArn: AwsArn | None


class TopicRuleDestinationSummary(TypedDict, total=False):
    """Information about the topic rule destination."""

    arn: AwsArn | None
    status: TopicRuleDestinationStatus | None
    createdAt: CreatedAtDate | None
    lastUpdatedAt: LastUpdatedAtDate | None
    statusReason: String | None
    httpUrlSummary: HttpUrlDestinationSummary | None
    vpcDestinationSummary: VpcDestinationSummary | None


TopicRuleDestinationSummaries = list[TopicRuleDestinationSummary]


class ListTopicRuleDestinationsResponse(TypedDict, total=False):
    destinationSummaries: TopicRuleDestinationSummaries | None
    nextToken: NextToken | None


class ListTopicRulesRequest(ServiceRequest):
    """The input for the ListTopicRules operation."""

    topic: Topic | None
    maxResults: TopicRuleMaxResults | None
    nextToken: NextToken | None
    ruleDisabled: IsDisabled | None


class TopicRuleListItem(TypedDict, total=False):
    """Describes a rule."""

    ruleArn: RuleArn | None
    ruleName: RuleName | None
    topicPattern: TopicPattern | None
    createdAt: CreatedAtDate | None
    ruleDisabled: IsDisabled | None


TopicRuleList = list[TopicRuleListItem]


class ListTopicRulesResponse(TypedDict, total=False):
    """The output from the ListTopicRules operation."""

    rules: TopicRuleList | None
    nextToken: NextToken | None


class ListV2LoggingLevelsRequest(ServiceRequest):
    targetType: LogTargetType | None
    nextToken: NextToken | None
    maxResults: SkyfallMaxResults | None


class LogTarget(TypedDict, total=False):
    """A log target."""

    targetType: LogTargetType
    targetName: LogTargetName | None


class LogTargetConfiguration(TypedDict, total=False):
    """The target configuration."""

    logTarget: LogTarget | None
    logLevel: LogLevel | None


LogTargetConfigurations = list[LogTargetConfiguration]


class ListV2LoggingLevelsResponse(TypedDict, total=False):
    logTargetConfigurations: LogTargetConfigurations | None
    nextToken: NextToken | None


class ListViolationEventsRequest(ServiceRequest):
    startTime: Timestamp
    endTime: Timestamp
    thingName: DeviceDefenderThingName | None
    securityProfileName: SecurityProfileName | None
    behaviorCriteriaType: BehaviorCriteriaType | None
    listSuppressedAlerts: ListSuppressedAlerts | None
    verificationState: VerificationState | None
    nextToken: NextToken | None
    maxResults: MaxResults | None


class ViolationEvent(TypedDict, total=False):
    """Information about a Device Defender security profile behavior violation."""

    violationId: ViolationId | None
    thingName: DeviceDefenderThingName | None
    securityProfileName: SecurityProfileName | None
    behavior: Behavior | None
    metricValue: MetricValue | None
    violationEventAdditionalInfo: ViolationEventAdditionalInfo | None
    violationEventType: ViolationEventType | None
    verificationState: VerificationState | None
    verificationStateDescription: VerificationStateDescription | None
    violationEventTime: Timestamp | None


ViolationEvents = list[ViolationEvent]


class ListViolationEventsResponse(TypedDict, total=False):
    violationEvents: ViolationEvents | None
    nextToken: NextToken | None


class LoggingOptionsPayload(TypedDict, total=False):
    """Describes the logging options payload."""

    roleArn: AwsArn
    logLevel: LogLevel | None


MqttPassword = bytes


class MqttContext(TypedDict, total=False):
    """Specifies the MQTT context to use for the test authorizer request"""

    username: MqttUsername | None
    password: MqttPassword | None
    clientId: MqttClientId | None


Parameters = dict[Parameter, Value]
PolicyDocuments = list[PolicyDocument]
PolicyNames = list[PolicyName]


class PutVerificationStateOnViolationRequest(ServiceRequest):
    violationId: ViolationId
    verificationState: VerificationState
    verificationStateDescription: VerificationStateDescription | None


class PutVerificationStateOnViolationResponse(TypedDict, total=False):
    pass


class RegisterCACertificateRequest(ServiceRequest):
    """The input to the RegisterCACertificate operation."""

    caCertificate: CertificatePem
    verificationCertificate: CertificatePem | None
    setAsActive: SetAsActive | None
    allowAutoRegistration: AllowAutoRegistration | None
    registrationConfig: RegistrationConfig | None
    tags: TagList | None
    certificateMode: CertificateMode | None


class RegisterCACertificateResponse(TypedDict, total=False):
    """The output from the RegisterCACertificateResponse operation."""

    certificateArn: CertificateArn | None
    certificateId: CertificateId | None


class RegisterCertificateRequest(ServiceRequest):
    """The input to the RegisterCertificate operation."""

    certificatePem: CertificatePem
    caCertificatePem: CertificatePem | None
    setAsActive: SetAsActiveFlag | None
    status: CertificateStatus | None


class RegisterCertificateResponse(TypedDict, total=False):
    """The output from the RegisterCertificate operation."""

    certificateArn: CertificateArn | None
    certificateId: CertificateId | None


class RegisterCertificateWithoutCARequest(ServiceRequest):
    certificatePem: CertificatePem
    status: CertificateStatus | None


class RegisterCertificateWithoutCAResponse(TypedDict, total=False):
    certificateArn: CertificateArn | None
    certificateId: CertificateId | None


class RegisterThingRequest(ServiceRequest):
    templateBody: TemplateBody
    parameters: Parameters | None


ResourceArns = dict[ResourceLogicalId, ResourceArn]


class RegisterThingResponse(TypedDict, total=False):
    certificatePem: CertificatePem | None
    resourceArns: ResourceArns | None


class RejectCertificateTransferRequest(ServiceRequest):
    """The input for the RejectCertificateTransfer operation."""

    certificateId: CertificateId
    rejectReason: Message | None


class RemoveThingFromBillingGroupRequest(ServiceRequest):
    billingGroupName: BillingGroupName | None
    billingGroupArn: BillingGroupArn | None
    thingName: ThingName | None
    thingArn: ThingArn | None


class RemoveThingFromBillingGroupResponse(TypedDict, total=False):
    pass


class RemoveThingFromThingGroupRequest(ServiceRequest):
    thingGroupName: ThingGroupName | None
    thingGroupArn: ThingGroupArn | None
    thingName: ThingName | None
    thingArn: ThingArn | None


class RemoveThingFromThingGroupResponse(TypedDict, total=False):
    pass


class ReplaceTopicRuleRequest(ServiceRequest):
    """The input for the ReplaceTopicRule operation."""

    ruleName: RuleName
    topicRulePayload: TopicRulePayload


class SearchIndexRequest(ServiceRequest):
    indexName: IndexName | None
    queryString: QueryString
    nextToken: NextToken | None
    maxResults: SearchQueryMaxResults | None
    queryVersion: QueryVersion | None


ThingGroupNameList = list[ThingGroupName]


class ThingGroupDocument(TypedDict, total=False):
    """The thing group search index document."""

    thingGroupName: ThingGroupName | None
    thingGroupId: ThingGroupId | None
    thingGroupDescription: ThingGroupDescription | None
    attributes: Attributes | None
    parentGroupNames: ThingGroupNameList | None


ThingGroupDocumentList = list[ThingGroupDocument]


class ThingConnectivity(TypedDict, total=False):
    """The connectivity status of the thing."""

    connected: Boolean | None
    timestamp: ConnectivityTimestamp | None
    disconnectReason: DisconnectReason | None


class ThingDocument(TypedDict, total=False):
    """The thing search index document."""

    thingName: ThingName | None
    thingId: ThingId | None
    thingTypeName: ThingTypeName | None
    thingGroupNames: ThingGroupNameList | None
    attributes: Attributes | None
    shadow: JsonDocument | None
    deviceDefender: JsonDocument | None
    connectivity: ThingConnectivity | None


ThingDocumentList = list[ThingDocument]


class SearchIndexResponse(TypedDict, total=False):
    nextToken: NextToken | None
    things: ThingDocumentList | None
    thingGroups: ThingGroupDocumentList | None


class SetDefaultAuthorizerRequest(ServiceRequest):
    authorizerName: AuthorizerName


class SetDefaultAuthorizerResponse(TypedDict, total=False):
    authorizerName: AuthorizerName | None
    authorizerArn: AuthorizerArn | None


class SetDefaultPolicyVersionRequest(ServiceRequest):
    """The input for the SetDefaultPolicyVersion operation."""

    policyName: PolicyName
    policyVersionId: PolicyVersionId


class SetLoggingOptionsRequest(ServiceRequest):
    """The input for the SetLoggingOptions operation."""

    loggingOptionsPayload: LoggingOptionsPayload


class SetV2LoggingLevelRequest(ServiceRequest):
    logTarget: LogTarget
    logLevel: LogLevel


class SetV2LoggingOptionsRequest(ServiceRequest):
    roleArn: AwsArn | None
    defaultLogLevel: LogLevel | None
    disableAllLogs: DisableAllLogs | None


class StartAuditMitigationActionsTaskRequest(ServiceRequest):
    taskId: MitigationActionsTaskId
    target: AuditMitigationActionsTaskTarget
    auditCheckToActionsMapping: AuditCheckToActionsMapping
    clientRequestToken: ClientRequestToken


class StartAuditMitigationActionsTaskResponse(TypedDict, total=False):
    taskId: MitigationActionsTaskId | None


class StartDetectMitigationActionsTaskRequest(ServiceRequest):
    taskId: MitigationActionsTaskId
    target: DetectMitigationActionsTaskTarget
    actions: DetectMitigationActionsToExecuteList
    violationEventOccurrenceRange: ViolationEventOccurrenceRange | None
    includeOnlyActiveViolations: NullableBoolean | None
    includeSuppressedAlerts: NullableBoolean | None
    clientRequestToken: ClientRequestToken


class StartDetectMitigationActionsTaskResponse(TypedDict, total=False):
    taskId: MitigationActionsTaskId | None


class StartOnDemandAuditTaskRequest(ServiceRequest):
    targetCheckNames: TargetAuditCheckNames


class StartOnDemandAuditTaskResponse(TypedDict, total=False):
    taskId: AuditTaskId | None


class StartThingRegistrationTaskRequest(ServiceRequest):
    templateBody: TemplateBody
    inputFileBucket: RegistryS3BucketName
    inputFileKey: RegistryS3KeyName
    roleArn: RoleArn


class StartThingRegistrationTaskResponse(TypedDict, total=False):
    taskId: TaskId | None


class StopThingRegistrationTaskRequest(ServiceRequest):
    taskId: TaskId


class StopThingRegistrationTaskResponse(TypedDict, total=False):
    pass


TagKeyList = list[TagKey]


class TagResourceRequest(ServiceRequest):
    resourceArn: ResourceArn
    tags: TagList


class TagResourceResponse(TypedDict, total=False):
    pass


class TestAuthorizationRequest(ServiceRequest):
    principal: Principal | None
    cognitoIdentityPoolId: CognitoIdentityPoolId | None
    authInfos: AuthInfos
    clientId: ClientId | None
    policyNamesToAdd: PolicyNames | None
    policyNamesToSkip: PolicyNames | None


class TestAuthorizationResponse(TypedDict, total=False):
    authResults: AuthResults | None


class TlsContext(TypedDict, total=False):
    """Specifies the TLS context to use for the test authorizer request."""

    serverName: ServerName | None


class TestInvokeAuthorizerRequest(ServiceRequest):
    authorizerName: AuthorizerName
    token: Token | None
    tokenSignature: TokenSignature | None
    httpContext: HttpContext | None
    mqttContext: MqttContext | None
    tlsContext: TlsContext | None


class TestInvokeAuthorizerResponse(TypedDict, total=False):
    isAuthenticated: IsAuthenticated | None
    principalId: PrincipalId | None
    policyDocuments: PolicyDocuments | None
    refreshAfterInSeconds: Seconds | None
    disconnectAfterInSeconds: Seconds | None


ThingGroupList = list[ThingGroupName]


class TransferCertificateRequest(ServiceRequest):
    """The input for the TransferCertificate operation."""

    certificateId: CertificateId
    targetAwsAccount: AwsAccountId
    transferMessage: Message | None


class TransferCertificateResponse(TypedDict, total=False):
    """The output from the TransferCertificate operation."""

    transferredCertificateArn: CertificateArn | None


class UntagResourceRequest(ServiceRequest):
    resourceArn: ResourceArn
    tagKeys: TagKeyList


class UntagResourceResponse(TypedDict, total=False):
    pass


class UpdateAccountAuditConfigurationRequest(ServiceRequest):
    roleArn: RoleArn | None
    auditNotificationTargetConfigurations: AuditNotificationTargetConfigurations | None
    auditCheckConfigurations: AuditCheckConfigurations | None


class UpdateAccountAuditConfigurationResponse(TypedDict, total=False):
    pass


class UpdateAuditSuppressionRequest(ServiceRequest):
    checkName: AuditCheckName
    resourceIdentifier: ResourceIdentifier
    expirationDate: Timestamp | None
    suppressIndefinitely: SuppressIndefinitely | None
    description: AuditDescription | None


class UpdateAuditSuppressionResponse(TypedDict, total=False):
    pass


class UpdateAuthorizerRequest(ServiceRequest):
    authorizerName: AuthorizerName
    authorizerFunctionArn: AuthorizerFunctionArn | None
    tokenKeyName: TokenKeyName | None
    tokenSigningPublicKeys: PublicKeyMap | None
    status: AuthorizerStatus | None
    enableCachingForHttp: EnableCachingForHttp | None


class UpdateAuthorizerResponse(TypedDict, total=False):
    authorizerName: AuthorizerName | None
    authorizerArn: AuthorizerArn | None


class UpdateBillingGroupRequest(ServiceRequest):
    billingGroupName: BillingGroupName
    billingGroupProperties: BillingGroupProperties
    expectedVersion: OptionalVersion | None


class UpdateBillingGroupResponse(TypedDict, total=False):
    version: Version | None


class UpdateCACertificateRequest(ServiceRequest):
    """The input to the UpdateCACertificate operation."""

    certificateId: CertificateId
    newStatus: CACertificateStatus | None
    newAutoRegistrationStatus: AutoRegistrationStatus | None
    registrationConfig: RegistrationConfig | None
    removeAutoRegistration: RemoveAutoRegistration | None


class UpdateCertificateProviderRequest(ServiceRequest):
    certificateProviderName: CertificateProviderName
    lambdaFunctionArn: CertificateProviderFunctionArn | None
    accountDefaultForOperations: CertificateProviderAccountDefaultForOperations | None


class UpdateCertificateProviderResponse(TypedDict, total=False):
    certificateProviderName: CertificateProviderName | None
    certificateProviderArn: CertificateProviderArn | None


class UpdateCertificateRequest(ServiceRequest):
    """The input for the UpdateCertificate operation."""

    certificateId: CertificateId
    newStatus: CertificateStatus


class UpdateCommandRequest(ServiceRequest):
    commandId: CommandId
    displayName: DisplayName | None
    description: CommandDescription | None
    deprecated: DeprecationFlag | None


class UpdateCommandResponse(TypedDict, total=False):
    commandId: CommandId | None
    displayName: DisplayName | None
    description: CommandDescription | None
    deprecated: DeprecationFlag | None
    lastUpdatedAt: DateType | None


class UpdateCustomMetricRequest(ServiceRequest):
    metricName: MetricName
    displayName: CustomMetricDisplayName


class UpdateCustomMetricResponse(TypedDict, total=False):
    metricName: MetricName | None
    metricArn: CustomMetricArn | None
    metricType: CustomMetricType | None
    displayName: CustomMetricDisplayName | None
    creationDate: Timestamp | None
    lastModifiedDate: Timestamp | None


class UpdateDimensionRequest(ServiceRequest):
    name: DimensionName
    stringValues: DimensionStringValues


class UpdateDimensionResponse(TypedDict, total=False):
    name: DimensionName | None
    arn: DimensionArn | None
    type: DimensionType | None
    stringValues: DimensionStringValues | None
    creationDate: Timestamp | None
    lastModifiedDate: Timestamp | None


class UpdateDomainConfigurationRequest(ServiceRequest):
    domainConfigurationName: ReservedDomainConfigurationName
    authorizerConfig: AuthorizerConfig | None
    domainConfigurationStatus: DomainConfigurationStatus | None
    removeAuthorizerConfig: RemoveAuthorizerConfig | None
    tlsConfig: TlsConfig | None
    serverCertificateConfig: ServerCertificateConfig | None
    authenticationType: AuthenticationType | None
    applicationProtocol: ApplicationProtocol | None
    clientCertificateConfig: ClientCertificateConfig | None


class UpdateDomainConfigurationResponse(TypedDict, total=False):
    domainConfigurationName: ReservedDomainConfigurationName | None
    domainConfigurationArn: DomainConfigurationArn | None


class UpdateDynamicThingGroupRequest(ServiceRequest):
    thingGroupName: ThingGroupName
    thingGroupProperties: ThingGroupProperties
    expectedVersion: OptionalVersion | None
    indexName: IndexName | None
    queryString: QueryString | None
    queryVersion: QueryVersion | None


class UpdateDynamicThingGroupResponse(TypedDict, total=False):
    version: Version | None


class UpdateEncryptionConfigurationRequest(ServiceRequest):
    encryptionType: EncryptionType
    kmsKeyArn: KmsKeyArn | None
    kmsAccessRoleArn: KmsAccessRoleArn | None


class UpdateEncryptionConfigurationResponse(TypedDict, total=False):
    pass


class UpdateEventConfigurationsRequest(ServiceRequest):
    eventConfigurations: EventConfigurations | None


class UpdateEventConfigurationsResponse(TypedDict, total=False):
    pass


class UpdateFleetMetricRequest(ServiceRequest):
    metricName: FleetMetricName
    queryString: QueryString | None
    aggregationType: AggregationType | None
    period: FleetMetricPeriod | None
    aggregationField: AggregationField | None
    description: FleetMetricDescription | None
    queryVersion: QueryVersion | None
    indexName: IndexName
    unit: FleetMetricUnit | None
    expectedVersion: OptionalVersion | None


class UpdateIndexingConfigurationRequest(ServiceRequest):
    thingIndexingConfiguration: ThingIndexingConfiguration | None
    thingGroupIndexingConfiguration: ThingGroupIndexingConfiguration | None


class UpdateIndexingConfigurationResponse(TypedDict, total=False):
    pass


class UpdateJobRequest(ServiceRequest):
    jobId: JobId
    description: JobDescription | None
    presignedUrlConfig: PresignedUrlConfig | None
    jobExecutionsRolloutConfig: JobExecutionsRolloutConfig | None
    abortConfig: AbortConfig | None
    timeoutConfig: TimeoutConfig | None
    namespaceId: NamespaceId | None
    jobExecutionsRetryConfig: JobExecutionsRetryConfig | None


class UpdateMitigationActionRequest(ServiceRequest):
    actionName: MitigationActionName
    roleArn: RoleArn | None
    actionParams: MitigationActionParams | None


class UpdateMitigationActionResponse(TypedDict, total=False):
    actionArn: MitigationActionArn | None
    actionId: MitigationActionId | None


class UpdatePackageConfigurationRequest(ServiceRequest):
    versionUpdateByJobsConfig: VersionUpdateByJobsConfig | None
    clientToken: ClientToken | None


class UpdatePackageConfigurationResponse(TypedDict, total=False):
    pass


class UpdatePackageRequest(ServiceRequest):
    packageName: PackageName
    description: ResourceDescription | None
    defaultVersionName: VersionName | None
    unsetDefaultVersion: UnsetDefaultVersion | None
    clientToken: ClientToken | None


class UpdatePackageResponse(TypedDict, total=False):
    pass


class UpdatePackageVersionRequest(ServiceRequest):
    packageName: PackageName
    versionName: VersionName
    description: ResourceDescription | None
    attributes: ResourceAttributes | None
    artifact: PackageVersionArtifact | None
    action: PackageVersionAction | None
    recipe: PackageVersionRecipe | None
    clientToken: ClientToken | None


class UpdatePackageVersionResponse(TypedDict, total=False):
    pass


class UpdateProvisioningTemplateRequest(ServiceRequest):
    templateName: TemplateName
    description: TemplateDescription | None
    enabled: Enabled | None
    defaultVersionId: TemplateVersionId | None
    provisioningRoleArn: RoleArn | None
    preProvisioningHook: ProvisioningHook | None
    removePreProvisioningHook: RemoveHook | None


class UpdateProvisioningTemplateResponse(TypedDict, total=False):
    pass


class UpdateRoleAliasRequest(ServiceRequest):
    roleAlias: RoleAlias
    roleArn: RoleArn | None
    credentialDurationSeconds: CredentialDurationSeconds | None


class UpdateRoleAliasResponse(TypedDict, total=False):
    roleAlias: RoleAlias | None
    roleAliasArn: RoleAliasArn | None


class UpdateScheduledAuditRequest(ServiceRequest):
    frequency: AuditFrequency | None
    dayOfMonth: DayOfMonth | None
    dayOfWeek: DayOfWeek | None
    targetCheckNames: TargetAuditCheckNames | None
    scheduledAuditName: ScheduledAuditName


class UpdateScheduledAuditResponse(TypedDict, total=False):
    scheduledAuditArn: ScheduledAuditArn | None


class UpdateSecurityProfileRequest(ServiceRequest):
    securityProfileName: SecurityProfileName
    securityProfileDescription: SecurityProfileDescription | None
    behaviors: Behaviors | None
    alertTargets: AlertTargets | None
    additionalMetricsToRetain: AdditionalMetricsToRetainList | None
    additionalMetricsToRetainV2: AdditionalMetricsToRetainV2List | None
    deleteBehaviors: DeleteBehaviors | None
    deleteAlertTargets: DeleteAlertTargets | None
    deleteAdditionalMetricsToRetain: DeleteAdditionalMetricsToRetain | None
    expectedVersion: OptionalVersion | None
    metricsExportConfig: MetricsExportConfig | None
    deleteMetricsExportConfig: DeleteMetricsExportConfig | None


class UpdateSecurityProfileResponse(TypedDict, total=False):
    securityProfileName: SecurityProfileName | None
    securityProfileArn: SecurityProfileArn | None
    securityProfileDescription: SecurityProfileDescription | None
    behaviors: Behaviors | None
    alertTargets: AlertTargets | None
    additionalMetricsToRetain: AdditionalMetricsToRetainList | None
    additionalMetricsToRetainV2: AdditionalMetricsToRetainV2List | None
    version: Version | None
    creationDate: Timestamp | None
    lastModifiedDate: Timestamp | None
    metricsExportConfig: MetricsExportConfig | None


class UpdateStreamRequest(ServiceRequest):
    streamId: StreamId
    description: StreamDescription | None
    files: StreamFiles | None
    roleArn: RoleArn | None


class UpdateStreamResponse(TypedDict, total=False):
    streamId: StreamId | None
    streamArn: StreamArn | None
    description: StreamDescription | None
    streamVersion: StreamVersion | None


class UpdateThingGroupRequest(ServiceRequest):
    thingGroupName: ThingGroupName
    thingGroupProperties: ThingGroupProperties
    expectedVersion: OptionalVersion | None


class UpdateThingGroupResponse(TypedDict, total=False):
    version: Version | None


class UpdateThingGroupsForThingRequest(ServiceRequest):
    thingName: ThingName | None
    thingGroupsToAdd: ThingGroupList | None
    thingGroupsToRemove: ThingGroupList | None
    overrideDynamicGroups: OverrideDynamicGroups | None


class UpdateThingGroupsForThingResponse(TypedDict, total=False):
    pass


class UpdateThingRequest(ServiceRequest):
    """The input for the UpdateThing operation."""

    thingName: ThingName
    thingTypeName: ThingTypeName | None
    attributePayload: AttributePayload | None
    expectedVersion: OptionalVersion | None
    removeThingType: RemoveThingType | None


class UpdateThingResponse(TypedDict, total=False):
    """The output from the UpdateThing operation."""

    pass


class UpdateThingTypeRequest(ServiceRequest):
    thingTypeName: ThingTypeName
    thingTypeProperties: ThingTypeProperties | None


class UpdateThingTypeResponse(TypedDict, total=False):
    pass


class UpdateTopicRuleDestinationRequest(ServiceRequest):
    arn: AwsArn
    status: TopicRuleDestinationStatus


class UpdateTopicRuleDestinationResponse(TypedDict, total=False):
    pass


class ValidateSecurityProfileBehaviorsRequest(ServiceRequest):
    behaviors: Behaviors


class ValidationError(TypedDict, total=False):
    """Information about an error found in a behavior specification."""

    errorMessage: ErrorMessage | None


ValidationErrors = list[ValidationError]


class ValidateSecurityProfileBehaviorsResponse(TypedDict, total=False):
    valid: Valid | None
    validationErrors: ValidationErrors | None


class IotApi:
    service: str = "iot"
    version: str = "2015-05-28"

    @handler("AcceptCertificateTransfer")
    def accept_certificate_transfer(
        self,
        context: RequestContext,
        certificate_id: CertificateId,
        set_as_active: SetAsActive | None = None,
        **kwargs,
    ) -> None:
        """Accepts a pending certificate transfer. The default state of the
        certificate is INACTIVE.

        To check for pending certificate transfers, call ListCertificates to
        enumerate your certificates.

        Requires permission to access the
        `AcceptCertificateTransfer <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param certificate_id: The ID of the certificate.
        :param set_as_active: Specifies whether the certificate is active.
        :raises ResourceNotFoundException:
        :raises TransferAlreadyCompletedException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("AddThingToBillingGroup")
    def add_thing_to_billing_group(
        self,
        context: RequestContext,
        billing_group_name: BillingGroupName | None = None,
        billing_group_arn: BillingGroupArn | None = None,
        thing_name: ThingName | None = None,
        thing_arn: ThingArn | None = None,
        **kwargs,
    ) -> AddThingToBillingGroupResponse:
        """Adds a thing to a billing group.

        Requires permission to access the
        `AddThingToBillingGroup <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param billing_group_name: The name of the billing group.
        :param billing_group_arn: The ARN of the billing group.
        :param thing_name: The name of the thing to be added to the billing group.
        :param thing_arn: The ARN of the thing to be added to the billing group.
        :returns: AddThingToBillingGroupResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("AddThingToThingGroup")
    def add_thing_to_thing_group(
        self,
        context: RequestContext,
        thing_group_name: ThingGroupName | None = None,
        thing_group_arn: ThingGroupArn | None = None,
        thing_name: ThingName | None = None,
        thing_arn: ThingArn | None = None,
        override_dynamic_groups: OverrideDynamicGroups | None = None,
        **kwargs,
    ) -> AddThingToThingGroupResponse:
        """Adds a thing to a thing group.

        Requires permission to access the
        `AddThingToThingGroup <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_group_name: The name of the group to which you are adding a thing.
        :param thing_group_arn: The ARN of the group to which you are adding a thing.
        :param thing_name: The name of the thing to add to a group.
        :param thing_arn: The ARN of the thing to add to a group.
        :param override_dynamic_groups: Override dynamic thing groups with static thing groups when 10-group
        limit is reached.
        :returns: AddThingToThingGroupResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("AssociateSbomWithPackageVersion")
    def associate_sbom_with_package_version(
        self,
        context: RequestContext,
        package_name: PackageName,
        version_name: VersionName,
        sbom: Sbom,
        client_token: ClientToken | None = None,
        **kwargs,
    ) -> AssociateSbomWithPackageVersionResponse:
        """Associates the selected software bill of materials (SBOM) with a
        specific software package version.

        Requires permission to access the
        `AssociateSbomWithPackageVersion <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param package_name: The name of the new software package.
        :param version_name: The name of the new package version.
        :param sbom: A specific software bill of matrerials associated with a software
        package version.
        :param client_token: A unique case-sensitive identifier that you can provide to ensure the
        idempotency of the request.
        :returns: AssociateSbomWithPackageVersionResponse
        :raises ThrottlingException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ValidationException:
        :raises ServiceQuotaExceededException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("AssociateTargetsWithJob")
    def associate_targets_with_job(
        self,
        context: RequestContext,
        targets: JobTargets,
        job_id: JobId,
        comment: Comment | None = None,
        namespace_id: NamespaceId | None = None,
        **kwargs,
    ) -> AssociateTargetsWithJobResponse:
        """Associates a group with a continuous job. The following criteria must be
        met:

        -  The job must have been created with the ``targetSelection`` field set
           to "CONTINUOUS".

        -  The job status must currently be "IN_PROGRESS".

        -  The total number of targets associated with a job must not exceed
           100.

        Requires permission to access the
        `AssociateTargetsWithJob <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param targets: A list of thing group ARNs that define the targets of the job.
        :param job_id: The unique identifier you assigned to this job when it was created.
        :param comment: An optional comment string describing why the job was associated with
        the targets.
        :param namespace_id: The namespace used to indicate that a job is a customer-managed job.
        :returns: AssociateTargetsWithJobResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises LimitExceededException:
        :raises ThrottlingException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("AttachPolicy")
    def attach_policy(
        self, context: RequestContext, policy_name: PolicyName, target: PolicyTarget, **kwargs
    ) -> None:
        """Attaches the specified policy to the specified principal (certificate or
        other credential).

        Requires permission to access the
        `AttachPolicy <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param policy_name: The name of the policy to attach.
        :param target: The
        `identity <https://docs.
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("AttachPrincipalPolicy")
    def attach_principal_policy(
        self, context: RequestContext, policy_name: PolicyName, principal: Principal, **kwargs
    ) -> None:
        """Attaches the specified policy to the specified principal (certificate or
        other credential).

        **Note:** This action is deprecated and works as expected for backward
        compatibility, but we won't add enhancements. Use AttachPolicy instead.

        Requires permission to access the
        `AttachPrincipalPolicy <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param policy_name: The policy name.
        :param principal: The principal, which can be a certificate ARN (as returned from the
        CreateCertificate operation) or an Amazon Cognito ID.
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("AttachSecurityProfile")
    def attach_security_profile(
        self,
        context: RequestContext,
        security_profile_name: SecurityProfileName,
        security_profile_target_arn: SecurityProfileTargetArn,
        **kwargs,
    ) -> AttachSecurityProfileResponse:
        """Associates a Device Defender security profile with a thing group or this
        account. Each thing group or account can have up to five security
        profiles associated with it.

        Requires permission to access the
        `AttachSecurityProfile <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param security_profile_name: The security profile that is attached.
        :param security_profile_target_arn: The ARN of the target (thing group) to which the security profile is
        attached.
        :returns: AttachSecurityProfileResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises LimitExceededException:
        :raises VersionConflictException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("AttachThingPrincipal")
    def attach_thing_principal(
        self,
        context: RequestContext,
        thing_name: ThingName,
        principal: Principal,
        thing_principal_type: ThingPrincipalType | None = None,
        **kwargs,
    ) -> AttachThingPrincipalResponse:
        """Attaches the specified principal to the specified thing. A principal can
        be X.509 certificates, Amazon Cognito identities or federated
        identities.

        Requires permission to access the
        `AttachThingPrincipal <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_name: The name of the thing.
        :param principal: The principal, which can be a certificate ARN (as returned from the
        CreateCertificate operation) or an Amazon Cognito ID.
        :param thing_principal_type: The type of the relation you want to specify when you attach a principal
        to a thing.
        :returns: AttachThingPrincipalResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("CancelAuditMitigationActionsTask")
    def cancel_audit_mitigation_actions_task(
        self, context: RequestContext, task_id: MitigationActionsTaskId, **kwargs
    ) -> CancelAuditMitigationActionsTaskResponse:
        """Cancels a mitigation action task that is in progress. If the task is not
        in progress, an InvalidRequestException occurs.

        Requires permission to access the
        `CancelAuditMitigationActionsTask <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param task_id: The unique identifier for the task that you want to cancel.
        :returns: CancelAuditMitigationActionsTaskResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("CancelAuditTask")
    def cancel_audit_task(
        self, context: RequestContext, task_id: AuditTaskId, **kwargs
    ) -> CancelAuditTaskResponse:
        """Cancels an audit that is in progress. The audit can be either scheduled
        or on demand. If the audit isn't in progress, an
        "InvalidRequestException" occurs.

        Requires permission to access the
        `CancelAuditTask <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param task_id: The ID of the audit you want to cancel.
        :returns: CancelAuditTaskResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("CancelCertificateTransfer")
    def cancel_certificate_transfer(
        self, context: RequestContext, certificate_id: CertificateId, **kwargs
    ) -> None:
        """Cancels a pending transfer for the specified certificate.

        **Note** Only the transfer source account can use this operation to
        cancel a transfer. (Transfer destinations can use
        RejectCertificateTransfer instead.) After transfer, IoT returns the
        certificate to the source account in the INACTIVE state. After the
        destination account has accepted the transfer, the transfer cannot be
        cancelled.

        After a certificate transfer is cancelled, the status of the certificate
        changes from PENDING_TRANSFER to INACTIVE.

        Requires permission to access the
        `CancelCertificateTransfer <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param certificate_id: The ID of the certificate.
        :raises ResourceNotFoundException:
        :raises TransferAlreadyCompletedException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("CancelDetectMitigationActionsTask")
    def cancel_detect_mitigation_actions_task(
        self, context: RequestContext, task_id: MitigationActionsTaskId, **kwargs
    ) -> CancelDetectMitigationActionsTaskResponse:
        """Cancels a Device Defender ML Detect mitigation action.

        Requires permission to access the
        `CancelDetectMitigationActionsTask <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param task_id: The unique identifier of the task.
        :returns: CancelDetectMitigationActionsTaskResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("CancelJob")
    def cancel_job(
        self,
        context: RequestContext,
        job_id: JobId,
        reason_code: ReasonCode | None = None,
        comment: Comment | None = None,
        force: ForceFlag | None = None,
        **kwargs,
    ) -> CancelJobResponse:
        """Cancels a job.

        Requires permission to access the
        `CancelJob <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param job_id: The unique identifier you assigned to this job when it was created.
        :param reason_code: (Optional)A reason code string that explains why the job was canceled.
        :param comment: An optional comment string describing why the job was canceled.
        :param force: (Optional) If ``true`` job executions with status "IN_PROGRESS" and
        "QUEUED" are canceled, otherwise only job executions with status
        "QUEUED" are canceled.
        :returns: CancelJobResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ServiceUnavailableException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("CancelJobExecution")
    def cancel_job_execution(
        self,
        context: RequestContext,
        job_id: JobId,
        thing_name: ThingName,
        force: ForceFlag | None = None,
        expected_version: ExpectedVersion | None = None,
        status_details: DetailsMap | None = None,
        **kwargs,
    ) -> None:
        """Cancels the execution of a job for a given thing.

        Requires permission to access the
        `CancelJobExecution <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param job_id: The ID of the job to be canceled.
        :param thing_name: The name of the thing whose execution of the job will be canceled.
        :param force: (Optional) If ``true`` the job execution will be canceled if it has
        status IN_PROGRESS or QUEUED, otherwise the job execution will be
        canceled only if it has status QUEUED.
        :param expected_version: (Optional) The expected current version of the job execution.
        :param status_details: A collection of name/value pairs that describe the status of the job
        execution.
        :raises InvalidRequestException:
        :raises InvalidStateTransitionException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ServiceUnavailableException:
        :raises VersionConflictException:
        """
        raise NotImplementedError

    @handler("ClearDefaultAuthorizer")
    def clear_default_authorizer(
        self, context: RequestContext, **kwargs
    ) -> ClearDefaultAuthorizerResponse:
        """Clears the default authorizer.

        Requires permission to access the
        `ClearDefaultAuthorizer <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :returns: ClearDefaultAuthorizerResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ConfirmTopicRuleDestination")
    def confirm_topic_rule_destination(
        self, context: RequestContext, confirmation_token: ConfirmationToken, **kwargs
    ) -> ConfirmTopicRuleDestinationResponse:
        """Confirms a topic rule destination. When you create a rule requiring a
        destination, IoT sends a confirmation message to the endpoint or base
        address you specify. The message includes a token which you pass back
        when calling ``ConfirmTopicRuleDestination`` to confirm that you own or
        have access to the endpoint.

        Requires permission to access the
        `ConfirmTopicRuleDestination <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param confirmation_token: The token used to confirm ownership or access to the topic rule
        confirmation URL.
        :returns: ConfirmTopicRuleDestinationResponse
        :raises InternalException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        :raises UnauthorizedException:
        :raises ConflictingResourceUpdateException:
        """
        raise NotImplementedError

    @handler("CreateAuditSuppression")
    def create_audit_suppression(
        self,
        context: RequestContext,
        check_name: AuditCheckName,
        resource_identifier: ResourceIdentifier,
        client_request_token: ClientRequestToken,
        expiration_date: Timestamp | None = None,
        suppress_indefinitely: SuppressIndefinitely | None = None,
        description: AuditDescription | None = None,
        **kwargs,
    ) -> CreateAuditSuppressionResponse:
        """Creates a Device Defender audit suppression.

        Requires permission to access the
        `CreateAuditSuppression <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param check_name: An audit check name.
        :param resource_identifier: Information that identifies the noncompliant resource.
        :param client_request_token: Each audit supression must have a unique client request token.
        :param expiration_date: The epoch timestamp in seconds at which this suppression expires.
        :param suppress_indefinitely: Indicates whether a suppression should exist indefinitely or not.
        :param description: The description of the audit suppression.
        :returns: CreateAuditSuppressionResponse
        :raises InvalidRequestException:
        :raises ResourceAlreadyExistsException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("CreateAuthorizer")
    def create_authorizer(
        self,
        context: RequestContext,
        authorizer_name: AuthorizerName,
        authorizer_function_arn: AuthorizerFunctionArn,
        token_key_name: TokenKeyName | None = None,
        token_signing_public_keys: PublicKeyMap | None = None,
        status: AuthorizerStatus | None = None,
        tags: TagList | None = None,
        signing_disabled: BooleanKey | None = None,
        enable_caching_for_http: EnableCachingForHttp | None = None,
        **kwargs,
    ) -> CreateAuthorizerResponse:
        """Creates an authorizer.

        Requires permission to access the
        `CreateAuthorizer <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param authorizer_name: The authorizer name.
        :param authorizer_function_arn: The ARN of the authorizer's Lambda function.
        :param token_key_name: The name of the token key used to extract the token from the HTTP
        headers.
        :param token_signing_public_keys: The public keys used to verify the digital signature returned by your
        custom authentication service.
        :param status: The status of the create authorizer request.
        :param tags: Metadata which can be used to manage the custom authorizer.
        :param signing_disabled: Specifies whether IoT validates the token signature in an authorization
        request.
        :param enable_caching_for_http: When ``true``, the result from the authorizer’s Lambda function is
        cached for clients that use persistent HTTP connections.
        :returns: CreateAuthorizerResponse
        :raises ResourceAlreadyExistsException:
        :raises InvalidRequestException:
        :raises LimitExceededException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("CreateBillingGroup")
    def create_billing_group(
        self,
        context: RequestContext,
        billing_group_name: BillingGroupName,
        billing_group_properties: BillingGroupProperties | None = None,
        tags: TagList | None = None,
        **kwargs,
    ) -> CreateBillingGroupResponse:
        """Creates a billing group. If this call is made multiple times using the
        same billing group name and configuration, the call will succeed. If
        this call is made with the same billing group name but different
        configuration a ``ResourceAlreadyExistsException`` is thrown.

        Requires permission to access the
        `CreateBillingGroup <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param billing_group_name: The name you wish to give to the billing group.
        :param billing_group_properties: The properties of the billing group.
        :param tags: Metadata which can be used to manage the billing group.
        :returns: CreateBillingGroupResponse
        :raises InvalidRequestException:
        :raises ResourceAlreadyExistsException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("CreateCertificateFromCsr")
    def create_certificate_from_csr(
        self,
        context: RequestContext,
        certificate_signing_request: CertificateSigningRequest,
        set_as_active: SetAsActive | None = None,
        **kwargs,
    ) -> CreateCertificateFromCsrResponse:
        """Creates an X.509 certificate using the specified certificate signing
        request.

        Requires permission to access the
        `CreateCertificateFromCsr <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        The CSR must include a public key that is either an RSA key with a
        length of at least 2048 bits or an ECC key from NIST P-256, NIST P-384,
        or NIST P-521 curves. For supported certificates, consult `Certificate
        signing algorithms supported by
        IoT <https://docs.aws.amazon.com/iot/latest/developerguide/x509-client-certs.html#x509-cert-algorithms>`__.

        Reusing the same certificate signing request (CSR) results in a distinct
        certificate.

        You can create multiple certificates in a batch by creating a directory,
        copying multiple ``.csr`` files into that directory, and then specifying
        that directory on the command line. The following commands show how to
        create a batch of certificates given a batch of CSRs. In the following
        commands, we assume that a set of CSRs are located inside of the
        directory my-csr-directory:

        On Linux and OS X, the command is:

        ``$ ls my-csr-directory/ | xargs -I {} aws iot create-certificate-from-csr --certificate-signing-request file://my-csr-directory/{}``

        This command lists all of the CSRs in my-csr-directory and pipes each
        CSR file name to the ``aws iot create-certificate-from-csr`` Amazon Web
        Services CLI command to create a certificate for the corresponding CSR.

        You can also run the ``aws iot create-certificate-from-csr`` part of the
        command in parallel to speed up the certificate creation process:

        ``$ ls my-csr-directory/ | xargs -P 10 -I {} aws iot create-certificate-from-csr --certificate-signing-request file://my-csr-directory/{}``

        On Windows PowerShell, the command to create certificates for all CSRs
        in my-csr-directory is:

        ``> ls -Name my-csr-directory | %{aws iot create-certificate-from-csr --certificate-signing-request file://my-csr-directory/$_}``

        On a Windows command prompt, the command to create certificates for all
        CSRs in my-csr-directory is:

        ``> forfiles /p my-csr-directory /c "cmd /c aws iot create-certificate-from-csr --certificate-signing-request file://@path"``

        :param certificate_signing_request: The certificate signing request (CSR).
        :param set_as_active: Specifies whether the certificate is active.
        :returns: CreateCertificateFromCsrResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("CreateCertificateProvider")
    def create_certificate_provider(
        self,
        context: RequestContext,
        certificate_provider_name: CertificateProviderName,
        lambda_function_arn: CertificateProviderFunctionArn,
        account_default_for_operations: CertificateProviderAccountDefaultForOperations,
        client_token: ClientToken | None = None,
        tags: TagList | None = None,
        **kwargs,
    ) -> CreateCertificateProviderResponse:
        """Creates an Amazon Web Services IoT Core certificate provider. You can
        use Amazon Web Services IoT Core certificate provider to customize how
        to sign a certificate signing request (CSR) in IoT fleet provisioning.
        For more information, see `Customizing certificate signing using Amazon
        Web Services IoT Core certificate
        provider <https://docs.aws.amazon.com/iot/latest/developerguide/provisioning-cert-provider.html>`__
        from *Amazon Web Services IoT Core Developer Guide*.

        Requires permission to access the
        `CreateCertificateProvider <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        After you create a certificate provider, the behavior of
        ```CreateCertificateFromCsr`` API for fleet
        provisioning <https://docs.aws.amazon.com/iot/latest/developerguide/fleet-provision-api.html#create-cert-csr>`__
        will change and all API calls to ``CreateCertificateFromCsr`` will
        invoke the certificate provider to create the certificates. It can take
        up to a few minutes for this behavior to change after a certificate
        provider is created.

        :param certificate_provider_name: The name of the certificate provider.
        :param lambda_function_arn: The ARN of the Lambda function that defines the authentication logic.
        :param account_default_for_operations: A list of the operations that the certificate provider will use to
        generate certificates.
        :param client_token: A string that you can optionally pass in the
        ``CreateCertificateProvider`` request to make sure the request is
        idempotent.
        :param tags: Metadata which can be used to manage the certificate provider.
        :returns: CreateCertificateProviderResponse
        :raises LimitExceededException:
        :raises ResourceAlreadyExistsException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("CreateCommand")
    def create_command(
        self,
        context: RequestContext,
        command_id: CommandId,
        namespace: CommandNamespace | None = None,
        display_name: DisplayName | None = None,
        description: CommandDescription | None = None,
        payload: CommandPayload | None = None,
        mandatory_parameters: CommandParameterList | None = None,
        role_arn: RoleArn | None = None,
        tags: TagList | None = None,
        **kwargs,
    ) -> CreateCommandResponse:
        """Creates a command. A command contains reusable configurations that can
        be applied before they are sent to the devices.

        :param command_id: A unique identifier for the command.
        :param namespace: The namespace of the command.
        :param display_name: The user-friendly name in the console for the command.
        :param description: A short text decription of the command.
        :param payload: The payload object for the command.
        :param mandatory_parameters: A list of parameters that are required by the ``StartCommandExecution``
        API.
        :param role_arn: The IAM role that you must provide when using the ``AWS-IoT-FleetWise``
        namespace.
        :param tags: Name-value pairs that are used as metadata to manage a command.
        :returns: CreateCommandResponse
        :raises ValidationException:
        :raises ConflictException:
        :raises ServiceQuotaExceededException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("CreateCustomMetric")
    def create_custom_metric(
        self,
        context: RequestContext,
        metric_name: MetricName,
        metric_type: CustomMetricType,
        client_request_token: ClientRequestToken,
        display_name: CustomMetricDisplayName | None = None,
        tags: TagList | None = None,
        **kwargs,
    ) -> CreateCustomMetricResponse:
        """Use this API to define a Custom Metric published by your devices to
        Device Defender.

        Requires permission to access the
        `CreateCustomMetric <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param metric_name: The name of the custom metric.
        :param metric_type: The type of the custom metric.
        :param client_request_token: Each custom metric must have a unique client request token.
        :param display_name: The friendly name in the console for the custom metric.
        :param tags: Metadata that can be used to manage the custom metric.
        :returns: CreateCustomMetricResponse
        :raises InvalidRequestException:
        :raises LimitExceededException:
        :raises ResourceAlreadyExistsException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("CreateDimension", expand=False)
    def create_dimension(
        self, context: RequestContext, request: CreateDimensionRequest, **kwargs
    ) -> CreateDimensionResponse:
        """Create a dimension that you can use to limit the scope of a metric used
        in a security profile for IoT Device Defender. For example, using a
        ``TOPIC_FILTER`` dimension, you can narrow down the scope of the metric
        only to MQTT topics whose name match the pattern specified in the
        dimension.

        Requires permission to access the
        `CreateDimension <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param name: A unique identifier for the dimension.
        :param type: Specifies the type of dimension.
        :param string_values: Specifies the value or list of values for the dimension.
        :param client_request_token: Each dimension must have a unique client request token.
        :param tags: Metadata that can be used to manage the dimension.
        :returns: CreateDimensionResponse
        :raises InternalFailureException:
        :raises InvalidRequestException:
        :raises LimitExceededException:
        :raises ResourceAlreadyExistsException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateDomainConfiguration")
    def create_domain_configuration(
        self,
        context: RequestContext,
        domain_configuration_name: DomainConfigurationName,
        domain_name: DomainName | None = None,
        server_certificate_arns: ServerCertificateArns | None = None,
        validation_certificate_arn: AcmCertificateArn | None = None,
        authorizer_config: AuthorizerConfig | None = None,
        service_type: ServiceType | None = None,
        tags: TagList | None = None,
        tls_config: TlsConfig | None = None,
        server_certificate_config: ServerCertificateConfig | None = None,
        authentication_type: AuthenticationType | None = None,
        application_protocol: ApplicationProtocol | None = None,
        client_certificate_config: ClientCertificateConfig | None = None,
        **kwargs,
    ) -> CreateDomainConfigurationResponse:
        """Creates a domain configuration.

        Requires permission to access the
        `CreateDomainConfiguration <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param domain_configuration_name: The name of the domain configuration.
        :param domain_name: The name of the domain.
        :param server_certificate_arns: The ARNs of the certificates that IoT passes to the device during the
        TLS handshake.
        :param validation_certificate_arn: The certificate used to validate the server certificate and prove domain
        name ownership.
        :param authorizer_config: An object that specifies the authorization service for a domain.
        :param service_type: The type of service delivered by the endpoint.
        :param tags: Metadata which can be used to manage the domain configuration.
        :param tls_config: An object that specifies the TLS configuration for a domain.
        :param server_certificate_config: The server certificate configuration.
        :param authentication_type: An enumerated string that speciﬁes the authentication type.
        :param application_protocol: An enumerated string that speciﬁes the application-layer protocol.
        :param client_certificate_config: An object that speciﬁes the client certificate conﬁguration for a
        domain.
        :returns: CreateDomainConfigurationResponse
        :raises LimitExceededException:
        :raises CertificateValidationException:
        :raises ResourceAlreadyExistsException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises InvalidRequestException:
        :raises UnauthorizedException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateDynamicThingGroup")
    def create_dynamic_thing_group(
        self,
        context: RequestContext,
        thing_group_name: ThingGroupName,
        query_string: QueryString,
        thing_group_properties: ThingGroupProperties | None = None,
        index_name: IndexName | None = None,
        query_version: QueryVersion | None = None,
        tags: TagList | None = None,
        **kwargs,
    ) -> CreateDynamicThingGroupResponse:
        """Creates a dynamic thing group.

        Requires permission to access the
        `CreateDynamicThingGroup <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_group_name: The dynamic thing group name to create.
        :param query_string: The dynamic thing group search query string.
        :param thing_group_properties: The dynamic thing group properties.
        :param index_name: The dynamic thing group index name.
        :param query_version: The dynamic thing group query version.
        :param tags: Metadata which can be used to manage the dynamic thing group.
        :returns: CreateDynamicThingGroupResponse
        :raises InvalidRequestException:
        :raises ResourceAlreadyExistsException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        :raises InvalidQueryException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("CreateFleetMetric")
    def create_fleet_metric(
        self,
        context: RequestContext,
        metric_name: FleetMetricName,
        query_string: QueryString,
        aggregation_type: AggregationType,
        period: FleetMetricPeriod,
        aggregation_field: AggregationField,
        description: FleetMetricDescription | None = None,
        query_version: QueryVersion | None = None,
        index_name: IndexName | None = None,
        unit: FleetMetricUnit | None = None,
        tags: TagList | None = None,
        **kwargs,
    ) -> CreateFleetMetricResponse:
        """Creates a fleet metric.

        Requires permission to access the
        `CreateFleetMetric <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param metric_name: The name of the fleet metric to create.
        :param query_string: The search query string.
        :param aggregation_type: The type of the aggregation query.
        :param period: The time in seconds between fleet metric emissions.
        :param aggregation_field: The field to aggregate.
        :param description: The fleet metric description.
        :param query_version: The query version.
        :param index_name: The name of the index to search.
        :param unit: Used to support unit transformation such as milliseconds to seconds.
        :param tags: Metadata, which can be used to manage the fleet metric.
        :returns: CreateFleetMetricResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises LimitExceededException:
        :raises ResourceAlreadyExistsException:
        :raises ResourceNotFoundException:
        :raises InvalidQueryException:
        :raises InvalidAggregationException:
        :raises IndexNotReadyException:
        """
        raise NotImplementedError

    @handler("CreateJob")
    def create_job(
        self,
        context: RequestContext,
        job_id: JobId,
        targets: JobTargets,
        document_source: JobDocumentSource | None = None,
        document: JobDocument | None = None,
        description: JobDescription | None = None,
        presigned_url_config: PresignedUrlConfig | None = None,
        target_selection: TargetSelection | None = None,
        job_executions_rollout_config: JobExecutionsRolloutConfig | None = None,
        abort_config: AbortConfig | None = None,
        timeout_config: TimeoutConfig | None = None,
        tags: TagList | None = None,
        namespace_id: NamespaceId | None = None,
        job_template_arn: JobTemplateArn | None = None,
        job_executions_retry_config: JobExecutionsRetryConfig | None = None,
        document_parameters: ParameterMap | None = None,
        scheduling_config: SchedulingConfig | None = None,
        destination_package_versions: DestinationPackageVersions | None = None,
        **kwargs,
    ) -> CreateJobResponse:
        """Creates a job.

        Requires permission to access the
        `CreateJob <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param job_id: A job identifier which must be unique for your account.
        :param targets: A list of things and thing groups to which the job should be sent.
        :param document_source: An S3 link, or S3 object URL, to the job document.
        :param document: The job document.
        :param description: A short text description of the job.
        :param presigned_url_config: Configuration information for pre-signed S3 URLs.
        :param target_selection: Specifies whether the job will continue to run (CONTINUOUS), or will be
        complete after all those things specified as targets have completed the
        job (SNAPSHOT).
        :param job_executions_rollout_config: Allows you to create a staged rollout of the job.
        :param abort_config: Allows you to create the criteria to abort a job.
        :param timeout_config: Specifies the amount of time each device has to finish its execution of
        the job.
        :param tags: Metadata which can be used to manage the job.
        :param namespace_id: The namespace used to indicate that a job is a customer-managed job.
        :param job_template_arn: The ARN of the job template used to create the job.
        :param job_executions_retry_config: Allows you to create the criteria to retry a job.
        :param document_parameters: Parameters of an Amazon Web Services managed template that you can
        specify to create the job document.
        :param scheduling_config: The configuration that allows you to schedule a job for a future date
        and time in addition to specifying the end behavior for each job
        execution.
        :param destination_package_versions: The package version Amazon Resource Names (ARNs) that are installed on
        the device when the job successfully completes.
        :returns: CreateJobResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ResourceAlreadyExistsException:
        :raises LimitExceededException:
        :raises ThrottlingException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("CreateJobTemplate")
    def create_job_template(
        self,
        context: RequestContext,
        job_template_id: JobTemplateId,
        description: JobDescription,
        job_arn: JobArn | None = None,
        document_source: JobDocumentSource | None = None,
        document: JobDocument | None = None,
        presigned_url_config: PresignedUrlConfig | None = None,
        job_executions_rollout_config: JobExecutionsRolloutConfig | None = None,
        abort_config: AbortConfig | None = None,
        timeout_config: TimeoutConfig | None = None,
        tags: TagList | None = None,
        job_executions_retry_config: JobExecutionsRetryConfig | None = None,
        maintenance_windows: MaintenanceWindows | None = None,
        destination_package_versions: DestinationPackageVersions | None = None,
        **kwargs,
    ) -> CreateJobTemplateResponse:
        """Creates a job template.

        Requires permission to access the
        `CreateJobTemplate <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param job_template_id: A unique identifier for the job template.
        :param description: A description of the job document.
        :param job_arn: The ARN of the job to use as the basis for the job template.
        :param document_source: An S3 link, or S3 object URL, to the job document.
        :param document: The job document.
        :param presigned_url_config: Configuration for pre-signed S3 URLs.
        :param job_executions_rollout_config: Allows you to create a staged rollout of a job.
        :param abort_config: The criteria that determine when and how a job abort takes place.
        :param timeout_config: Specifies the amount of time each device has to finish its execution of
        the job.
        :param tags: Metadata that can be used to manage the job template.
        :param job_executions_retry_config: Allows you to create the criteria to retry a job.
        :param maintenance_windows: Allows you to configure an optional maintenance window for the rollout
        of a job document to all devices in the target group for a job.
        :param destination_package_versions: The package version Amazon Resource Names (ARNs) that are installed on
        the device when the job successfully completes.
        :returns: CreateJobTemplateResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises LimitExceededException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("CreateKeysAndCertificate")
    def create_keys_and_certificate(
        self, context: RequestContext, set_as_active: SetAsActive | None = None, **kwargs
    ) -> CreateKeysAndCertificateResponse:
        """Creates a 2048-bit RSA key pair and issues an X.509 certificate using
        the issued public key. You can also call ``CreateKeysAndCertificate``
        over MQTT from a device, for more information, see `Provisioning MQTT
        API <https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html#provision-mqtt-api>`__.

        **Note** This is the only time IoT issues the private key for this
        certificate, so it is important to keep it in a secure location.

        Requires permission to access the
        `CreateKeysAndCertificate <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param set_as_active: Specifies whether the certificate is active.
        :returns: CreateKeysAndCertificateResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("CreateMitigationAction")
    def create_mitigation_action(
        self,
        context: RequestContext,
        action_name: MitigationActionName,
        role_arn: RoleArn,
        action_params: MitigationActionParams,
        tags: TagList | None = None,
        **kwargs,
    ) -> CreateMitigationActionResponse:
        """Defines an action that can be applied to audit findings by using
        StartAuditMitigationActionsTask. Only certain types of mitigation
        actions can be applied to specific check names. For more information,
        see `Mitigation
        actions <https://docs.aws.amazon.com/iot/latest/developerguide/device-defender-mitigation-actions.html>`__.
        Each mitigation action can apply only one type of change.

        Requires permission to access the
        `CreateMitigationAction <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param action_name: A friendly name for the action.
        :param role_arn: The ARN of the IAM role that is used to apply the mitigation action.
        :param action_params: Defines the type of action and the parameters for that action.
        :param tags: Metadata that can be used to manage the mitigation action.
        :returns: CreateMitigationActionResponse
        :raises InvalidRequestException:
        :raises ResourceAlreadyExistsException:
        :raises LimitExceededException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("CreateOTAUpdate")
    def create_ota_update(
        self,
        context: RequestContext,
        ota_update_id: OTAUpdateId,
        targets: Targets,
        files: OTAUpdateFiles,
        role_arn: RoleArn,
        description: OTAUpdateDescription | None = None,
        protocols: Protocols | None = None,
        target_selection: TargetSelection | None = None,
        aws_job_executions_rollout_config: AwsJobExecutionsRolloutConfig | None = None,
        aws_job_presigned_url_config: AwsJobPresignedUrlConfig | None = None,
        aws_job_abort_config: AwsJobAbortConfig | None = None,
        aws_job_timeout_config: AwsJobTimeoutConfig | None = None,
        additional_parameters: AdditionalParameterMap | None = None,
        tags: TagList | None = None,
        **kwargs,
    ) -> CreateOTAUpdateResponse:
        """Creates an IoT OTA update on a target group of things or groups.

        Requires permission to access the
        `CreateOTAUpdate <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param ota_update_id: The ID of the OTA update to be created.
        :param targets: The devices targeted to receive OTA updates.
        :param files: The files to be streamed by the OTA update.
        :param role_arn: The IAM role that grants Amazon Web Services IoT Core access to the
        Amazon S3, IoT jobs and Amazon Web Services Code Signing resources to
        create an OTA update job.
        :param description: The description of the OTA update.
        :param protocols: The protocol used to transfer the OTA update image.
        :param target_selection: Specifies whether the update will continue to run (CONTINUOUS), or will
        be complete after all the things specified as targets have completed the
        update (SNAPSHOT).
        :param aws_job_executions_rollout_config: Configuration for the rollout of OTA updates.
        :param aws_job_presigned_url_config: Configuration information for pre-signed URLs.
        :param aws_job_abort_config: The criteria that determine when and how a job abort takes place.
        :param aws_job_timeout_config: Specifies the amount of time each device has to finish its execution of
        the job.
        :param additional_parameters: A list of additional OTA update parameters, which are name-value pairs.
        :param tags: Metadata which can be used to manage updates.
        :returns: CreateOTAUpdateResponse
        :raises InvalidRequestException:
        :raises LimitExceededException:
        :raises ResourceNotFoundException:
        :raises ResourceAlreadyExistsException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("CreatePackage")
    def create_package(
        self,
        context: RequestContext,
        package_name: PackageName,
        description: ResourceDescription | None = None,
        tags: TagMap | None = None,
        client_token: ClientToken | None = None,
        **kwargs,
    ) -> CreatePackageResponse:
        """Creates an IoT software package that can be deployed to your fleet.

        Requires permission to access the
        `CreatePackage <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        and
        `GetIndexingConfiguration <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        actions.

        :param package_name: The name of the new software package.
        :param description: A summary of the package being created.
        :param tags: Metadata that can be used to manage the package.
        :param client_token: A unique case-sensitive identifier that you can provide to ensure the
        idempotency of the request.
        :returns: CreatePackageResponse
        :raises ThrottlingException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ValidationException:
        :raises ServiceQuotaExceededException:
        """
        raise NotImplementedError

    @handler("CreatePackageVersion")
    def create_package_version(
        self,
        context: RequestContext,
        package_name: PackageName,
        version_name: VersionName,
        description: ResourceDescription | None = None,
        attributes: ResourceAttributes | None = None,
        artifact: PackageVersionArtifact | None = None,
        recipe: PackageVersionRecipe | None = None,
        tags: TagMap | None = None,
        client_token: ClientToken | None = None,
        **kwargs,
    ) -> CreatePackageVersionResponse:
        """Creates a new version for an existing IoT software package.

        Requires permission to access the
        `CreatePackageVersion <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        and
        `GetIndexingConfiguration <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        actions.

        :param package_name: The name of the associated software package.
        :param version_name: The name of the new package version.
        :param description: A summary of the package version being created.
        :param attributes: Metadata that can be used to define a package version’s configuration.
        :param artifact: The various build components created during the build process such as
        libraries and configuration files that make up a software package
        version.
        :param recipe: The inline job document associated with a software package version used
        for a quick job deployment.
        :param tags: Metadata that can be used to manage the package version.
        :param client_token: A unique case-sensitive identifier that you can provide to ensure the
        idempotency of the request.
        :returns: CreatePackageVersionResponse
        :raises ThrottlingException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ValidationException:
        :raises ServiceQuotaExceededException:
        """
        raise NotImplementedError

    @handler("CreatePolicy")
    def create_policy(
        self,
        context: RequestContext,
        policy_name: PolicyName,
        policy_document: PolicyDocument,
        tags: TagList | None = None,
        **kwargs,
    ) -> CreatePolicyResponse:
        """Creates an IoT policy.

        The created policy is the default version for the policy. This operation
        creates a policy version with a version identifier of **1** and sets
        **1** as the policy's default version.

        Requires permission to access the
        `CreatePolicy <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param policy_name: The policy name.
        :param policy_document: The JSON document that describes the policy.
        :param tags: Metadata which can be used to manage the policy.
        :returns: CreatePolicyResponse
        :raises ResourceAlreadyExistsException:
        :raises MalformedPolicyException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("CreatePolicyVersion")
    def create_policy_version(
        self,
        context: RequestContext,
        policy_name: PolicyName,
        policy_document: PolicyDocument,
        set_as_default: SetAsDefault | None = None,
        **kwargs,
    ) -> CreatePolicyVersionResponse:
        """Creates a new version of the specified IoT policy. To update a policy,
        create a new policy version. A managed policy can have up to five
        versions. If the policy has five versions, you must use
        DeletePolicyVersion to delete an existing version before you create a
        new one.

        Optionally, you can set the new version as the policy's default version.
        The default version is the operative version (that is, the version that
        is in effect for the certificates to which the policy is attached).

        Requires permission to access the
        `CreatePolicyVersion <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param policy_name: The policy name.
        :param policy_document: The JSON document that describes the policy.
        :param set_as_default: Specifies whether the policy version is set as the default.
        :returns: CreatePolicyVersionResponse
        :raises ResourceNotFoundException:
        :raises MalformedPolicyException:
        :raises VersionsLimitExceededException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("CreateProvisioningClaim")
    def create_provisioning_claim(
        self, context: RequestContext, template_name: TemplateName, **kwargs
    ) -> CreateProvisioningClaimResponse:
        """Creates a provisioning claim.

        Requires permission to access the
        `CreateProvisioningClaim <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param template_name: The name of the provisioning template to use.
        :returns: CreateProvisioningClaimResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("CreateProvisioningTemplate", expand=False)
    def create_provisioning_template(
        self, context: RequestContext, request: CreateProvisioningTemplateRequest, **kwargs
    ) -> CreateProvisioningTemplateResponse:
        """Creates a provisioning template.

        Requires permission to access the
        `CreateProvisioningTemplate <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param template_name: The name of the provisioning template.
        :param template_body: The JSON formatted contents of the provisioning template.
        :param provisioning_role_arn: The role ARN for the role associated with the provisioning template.
        :param description: The description of the provisioning template.
        :param enabled: True to enable the provisioning template, otherwise false.
        :param pre_provisioning_hook: Creates a pre-provisioning hook template.
        :param tags: Metadata which can be used to manage the provisioning template.
        :param type: The type you define in a provisioning template.
        :returns: CreateProvisioningTemplateResponse
        :raises InternalFailureException:
        :raises InvalidRequestException:
        :raises LimitExceededException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ResourceAlreadyExistsException:
        """
        raise NotImplementedError

    @handler("CreateProvisioningTemplateVersion")
    def create_provisioning_template_version(
        self,
        context: RequestContext,
        template_name: TemplateName,
        template_body: TemplateBody,
        set_as_default: SetAsDefault | None = None,
        **kwargs,
    ) -> CreateProvisioningTemplateVersionResponse:
        """Creates a new version of a provisioning template.

        Requires permission to access the
        `CreateProvisioningTemplateVersion <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param template_name: The name of the provisioning template.
        :param template_body: The JSON formatted contents of the provisioning template.
        :param set_as_default: Sets a fleet provision template version as the default version.
        :returns: CreateProvisioningTemplateVersionResponse
        :raises VersionsLimitExceededException:
        :raises InternalFailureException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises ResourceNotFoundException:
        :raises UnauthorizedException:
        :raises ConflictingResourceUpdateException:
        """
        raise NotImplementedError

    @handler("CreateRoleAlias")
    def create_role_alias(
        self,
        context: RequestContext,
        role_alias: RoleAlias,
        role_arn: RoleArn,
        credential_duration_seconds: CredentialDurationSeconds | None = None,
        tags: TagList | None = None,
        **kwargs,
    ) -> CreateRoleAliasResponse:
        """Creates a role alias.

        Requires permission to access the
        `CreateRoleAlias <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        The value of
        ```credentialDurationSeconds`` <https://docs.aws.amazon.com/iot/latest/apireference/API_CreateRoleAlias.html#iot-CreateRoleAlias-request-credentialDurationSeconds>`__
        must be less than or equal to the maximum session duration of the IAM
        role that the role alias references. For more information, see
        `Modifying a role maximum session duration (Amazon Web Services
        API) <https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-managingrole-editing-api.html#roles-modify_max-session-duration-api>`__
        from the Amazon Web Services Identity and Access Management User Guide.

        :param role_alias: The role alias that points to a role ARN.
        :param role_arn: The role ARN.
        :param credential_duration_seconds: How long (in seconds) the credentials will be valid.
        :param tags: Metadata which can be used to manage the role alias.
        :returns: CreateRoleAliasResponse
        :raises ResourceAlreadyExistsException:
        :raises InvalidRequestException:
        :raises LimitExceededException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("CreateScheduledAudit")
    def create_scheduled_audit(
        self,
        context: RequestContext,
        frequency: AuditFrequency,
        target_check_names: TargetAuditCheckNames,
        scheduled_audit_name: ScheduledAuditName,
        day_of_month: DayOfMonth | None = None,
        day_of_week: DayOfWeek | None = None,
        tags: TagList | None = None,
        **kwargs,
    ) -> CreateScheduledAuditResponse:
        """Creates a scheduled audit that is run at a specified time interval.

        Requires permission to access the
        `CreateScheduledAudit <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param frequency: How often the scheduled audit takes place, either ``DAILY``, ``WEEKLY``,
        ``BIWEEKLY`` or ``MONTHLY``.
        :param target_check_names: Which checks are performed during the scheduled audit.
        :param scheduled_audit_name: The name you want to give to the scheduled audit.
        :param day_of_month: The day of the month on which the scheduled audit takes place.
        :param day_of_week: The day of the week on which the scheduled audit takes place, either
        ``SUN``, ``MON``, ``TUE``, ``WED``, ``THU``, ``FRI``, or ``SAT``.
        :param tags: Metadata that can be used to manage the scheduled audit.
        :returns: CreateScheduledAuditResponse
        :raises InvalidRequestException:
        :raises ResourceAlreadyExistsException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("CreateSecurityProfile")
    def create_security_profile(
        self,
        context: RequestContext,
        security_profile_name: SecurityProfileName,
        security_profile_description: SecurityProfileDescription | None = None,
        behaviors: Behaviors | None = None,
        alert_targets: AlertTargets | None = None,
        additional_metrics_to_retain: AdditionalMetricsToRetainList | None = None,
        additional_metrics_to_retain_v2: AdditionalMetricsToRetainV2List | None = None,
        tags: TagList | None = None,
        metrics_export_config: MetricsExportConfig | None = None,
        **kwargs,
    ) -> CreateSecurityProfileResponse:
        """Creates a Device Defender security profile.

        Requires permission to access the
        `CreateSecurityProfile <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param security_profile_name: The name you are giving to the security profile.
        :param security_profile_description: A description of the security profile.
        :param behaviors: Specifies the behaviors that, when violated by a device (thing), cause
        an alert.
        :param alert_targets: Specifies the destinations to which alerts are sent.
        :param additional_metrics_to_retain: *Please use CreateSecurityProfileRequest$additionalMetricsToRetainV2
        instead.
        :param additional_metrics_to_retain_v2: A list of metrics whose data is retained (stored).
        :param tags: Metadata that can be used to manage the security profile.
        :param metrics_export_config: Specifies the MQTT topic and role ARN required for metric export.
        :returns: CreateSecurityProfileResponse
        :raises InvalidRequestException:
        :raises ResourceAlreadyExistsException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("CreateStream")
    def create_stream(
        self,
        context: RequestContext,
        stream_id: StreamId,
        files: StreamFiles,
        role_arn: RoleArn,
        description: StreamDescription | None = None,
        tags: TagList | None = None,
        **kwargs,
    ) -> CreateStreamResponse:
        """Creates a stream for delivering one or more large files in chunks over
        MQTT. A stream transports data bytes in chunks or blocks packaged as
        MQTT messages from a source like S3. You can have one or more files
        associated with a stream.

        Requires permission to access the
        `CreateStream <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param stream_id: The stream ID.
        :param files: The files to stream.
        :param role_arn: An IAM role that allows the IoT service principal to access your S3
        files.
        :param description: A description of the stream.
        :param tags: Metadata which can be used to manage streams.
        :returns: CreateStreamResponse
        :raises InvalidRequestException:
        :raises LimitExceededException:
        :raises ResourceNotFoundException:
        :raises ResourceAlreadyExistsException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("CreateThing")
    def create_thing(
        self,
        context: RequestContext,
        thing_name: ThingName,
        thing_type_name: ThingTypeName | None = None,
        attribute_payload: AttributePayload | None = None,
        billing_group_name: BillingGroupName | None = None,
        **kwargs,
    ) -> CreateThingResponse:
        """Creates a thing record in the registry. If this call is made multiple
        times using the same thing name and configuration, the call will
        succeed. If this call is made with the same thing name but different
        configuration a ``ResourceAlreadyExistsException`` is thrown.

        This is a control plane operation. See
        `Authorization <https://docs.aws.amazon.com/iot/latest/developerguide/iot-authorization.html>`__
        for information about authorizing control plane actions.

        Requires permission to access the
        `CreateThing <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_name: The name of the thing to create.
        :param thing_type_name: The name of the thing type associated with the new thing.
        :param attribute_payload: The attribute payload, which consists of up to three name/value pairs in
        a JSON document.
        :param billing_group_name: The name of the billing group the thing will be added to.
        :returns: CreateThingResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceAlreadyExistsException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("CreateThingGroup")
    def create_thing_group(
        self,
        context: RequestContext,
        thing_group_name: ThingGroupName,
        parent_group_name: ThingGroupName | None = None,
        thing_group_properties: ThingGroupProperties | None = None,
        tags: TagList | None = None,
        **kwargs,
    ) -> CreateThingGroupResponse:
        """Create a thing group.

        This is a control plane operation. See
        `Authorization <https://docs.aws.amazon.com/iot/latest/developerguide/iot-authorization.html>`__
        for information about authorizing control plane actions.

        If the ``ThingGroup`` that you create has the exact same attributes as
        an existing ``ThingGroup``, you will get a 200 success response.

        Requires permission to access the
        `CreateThingGroup <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_group_name: The thing group name to create.
        :param parent_group_name: The name of the parent thing group.
        :param thing_group_properties: The thing group properties.
        :param tags: Metadata which can be used to manage the thing group.
        :returns: CreateThingGroupResponse
        :raises InvalidRequestException:
        :raises ResourceAlreadyExistsException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("CreateThingType")
    def create_thing_type(
        self,
        context: RequestContext,
        thing_type_name: ThingTypeName,
        thing_type_properties: ThingTypeProperties | None = None,
        tags: TagList | None = None,
        **kwargs,
    ) -> CreateThingTypeResponse:
        """Creates a new thing type. If this call is made multiple times using the
        same thing type name and configuration, the call will succeed. If this
        call is made with the same thing type name but different configuration a
        ``ResourceAlreadyExistsException`` is thrown.

        Requires permission to access the
        `CreateThingType <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_type_name: The name of the thing type.
        :param thing_type_properties: The ThingTypeProperties for the thing type to create.
        :param tags: Metadata which can be used to manage the thing type.
        :returns: CreateThingTypeResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceAlreadyExistsException:
        """
        raise NotImplementedError

    @handler("CreateTopicRule")
    def create_topic_rule(
        self,
        context: RequestContext,
        rule_name: RuleName,
        topic_rule_payload: TopicRulePayload,
        tags: String | None = None,
        **kwargs,
    ) -> None:
        """Creates a rule. Creating rules is an administrator-level action. Any
        user who has permission to create rules will be able to access data
        processed by the rule.

        Requires permission to access the
        `CreateTopicRule <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param rule_name: The name of the rule.
        :param topic_rule_payload: The rule payload.
        :param tags: Metadata which can be used to manage the topic rule.
        :raises SqlParseException:
        :raises InternalException:
        :raises InvalidRequestException:
        :raises ResourceAlreadyExistsException:
        :raises ServiceUnavailableException:
        :raises ConflictingResourceUpdateException:
        :raises UnauthorizedException:
        """
        raise NotImplementedError

    @handler("CreateTopicRuleDestination")
    def create_topic_rule_destination(
        self,
        context: RequestContext,
        destination_configuration: TopicRuleDestinationConfiguration,
        **kwargs,
    ) -> CreateTopicRuleDestinationResponse:
        """Creates a topic rule destination. The destination must be confirmed
        prior to use.

        Requires permission to access the
        `CreateTopicRuleDestination <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param destination_configuration: The topic rule destination configuration.
        :returns: CreateTopicRuleDestinationResponse
        :raises InternalException:
        :raises InvalidRequestException:
        :raises ResourceAlreadyExistsException:
        :raises ServiceUnavailableException:
        :raises ConflictingResourceUpdateException:
        :raises UnauthorizedException:
        """
        raise NotImplementedError

    @handler("DeleteAccountAuditConfiguration")
    def delete_account_audit_configuration(
        self,
        context: RequestContext,
        delete_scheduled_audits: DeleteScheduledAudits | None = None,
        **kwargs,
    ) -> DeleteAccountAuditConfigurationResponse:
        """Restores the default settings for Device Defender audits for this
        account. Any configuration data you entered is deleted and all audit
        checks are reset to disabled.

        Requires permission to access the
        `DeleteAccountAuditConfiguration <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param delete_scheduled_audits: If true, all scheduled audits are deleted.
        :returns: DeleteAccountAuditConfigurationResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DeleteAuditSuppression")
    def delete_audit_suppression(
        self,
        context: RequestContext,
        check_name: AuditCheckName,
        resource_identifier: ResourceIdentifier,
        **kwargs,
    ) -> DeleteAuditSuppressionResponse:
        """Deletes a Device Defender audit suppression.

        Requires permission to access the
        `DeleteAuditSuppression <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param check_name: An audit check name.
        :param resource_identifier: Information that identifies the noncompliant resource.
        :returns: DeleteAuditSuppressionResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DeleteAuthorizer")
    def delete_authorizer(
        self, context: RequestContext, authorizer_name: AuthorizerName, **kwargs
    ) -> DeleteAuthorizerResponse:
        """Deletes an authorizer.

        Requires permission to access the
        `DeleteAuthorizer <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param authorizer_name: The name of the authorizer to delete.
        :returns: DeleteAuthorizerResponse
        :raises DeleteConflictException:
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DeleteBillingGroup")
    def delete_billing_group(
        self,
        context: RequestContext,
        billing_group_name: BillingGroupName,
        expected_version: OptionalVersion | None = None,
        **kwargs,
    ) -> DeleteBillingGroupResponse:
        """Deletes the billing group.

        Requires permission to access the
        `DeleteBillingGroup <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param billing_group_name: The name of the billing group.
        :param expected_version: The expected version of the billing group.
        :returns: DeleteBillingGroupResponse
        :raises InvalidRequestException:
        :raises VersionConflictException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DeleteCACertificate")
    def delete_ca_certificate(
        self, context: RequestContext, certificate_id: CertificateId, **kwargs
    ) -> DeleteCACertificateResponse:
        """Deletes a registered CA certificate.

        Requires permission to access the
        `DeleteCACertificate <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param certificate_id: The ID of the certificate to delete.
        :returns: DeleteCACertificateResponse
        :raises InvalidRequestException:
        :raises CertificateStateException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("DeleteCertificate")
    def delete_certificate(
        self,
        context: RequestContext,
        certificate_id: CertificateId,
        force_delete: ForceDelete | None = None,
        **kwargs,
    ) -> None:
        """Deletes the specified certificate.

        A certificate cannot be deleted if it has a policy or IoT thing attached
        to it or if its status is set to ACTIVE. To delete a certificate, first
        use the DetachPolicy action to detach all policies. Next, use the
        UpdateCertificate action to set the certificate to the INACTIVE status.

        Requires permission to access the
        `DeleteCertificate <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param certificate_id: The ID of the certificate.
        :param force_delete: Forces the deletion of a certificate if it is inactive and is not
        attached to an IoT thing.
        :raises CertificateStateException:
        :raises DeleteConflictException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("DeleteCertificateProvider")
    def delete_certificate_provider(
        self, context: RequestContext, certificate_provider_name: CertificateProviderName, **kwargs
    ) -> DeleteCertificateProviderResponse:
        """Deletes a certificate provider.

        Requires permission to access the
        `DeleteCertificateProvider <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        If you delete the certificate provider resource, the behavior of
        ``CreateCertificateFromCsr`` will resume, and IoT will create
        certificates signed by IoT from a certificate signing request (CSR).

        :param certificate_provider_name: The name of the certificate provider.
        :returns: DeleteCertificateProviderResponse
        :raises DeleteConflictException:
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DeleteCommand")
    def delete_command(
        self, context: RequestContext, command_id: CommandId, **kwargs
    ) -> DeleteCommandResponse:
        """Delete a command resource.

        :param command_id: The unique identifier of the command to be deleted.
        :returns: DeleteCommandResponse
        :raises ValidationException:
        :raises ConflictException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("DeleteCommandExecution")
    def delete_command_execution(
        self,
        context: RequestContext,
        execution_id: CommandExecutionId,
        target_arn: TargetArn,
        **kwargs,
    ) -> DeleteCommandExecutionResponse:
        """Delete a command execution.

        Only command executions that enter a terminal state can be deleted from
        your account.

        :param execution_id: The unique identifier of the command execution that you want to delete
        from your account.
        :param target_arn: The Amazon Resource Number (ARN) of the target device for which you want
        to delete command executions.
        :returns: DeleteCommandExecutionResponse
        :raises ConflictException:
        :raises ValidationException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("DeleteCustomMetric")
    def delete_custom_metric(
        self, context: RequestContext, metric_name: MetricName, **kwargs
    ) -> DeleteCustomMetricResponse:
        """Deletes a Device Defender detect custom metric.

        Requires permission to access the
        `DeleteCustomMetric <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        Before you can delete a custom metric, you must first remove the custom
        metric from all security profiles it's a part of. The security profile
        associated with the custom metric can be found using the
        `ListSecurityProfiles <https://docs.aws.amazon.com/iot/latest/apireference/API_ListSecurityProfiles.html>`__
        API with ``metricName`` set to your custom metric name.

        :param metric_name: The name of the custom metric.
        :returns: DeleteCustomMetricResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DeleteDimension")
    def delete_dimension(
        self, context: RequestContext, name: DimensionName, **kwargs
    ) -> DeleteDimensionResponse:
        """Removes the specified dimension from your Amazon Web Services accounts.

        Requires permission to access the
        `DeleteDimension <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param name: The unique identifier for the dimension that you want to delete.
        :returns: DeleteDimensionResponse
        :raises InternalFailureException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeleteDomainConfiguration")
    def delete_domain_configuration(
        self, context: RequestContext, domain_configuration_name: DomainConfigurationName, **kwargs
    ) -> DeleteDomainConfigurationResponse:
        """Deletes the specified domain configuration.

        Requires permission to access the
        `DeleteDomainConfiguration <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param domain_configuration_name: The name of the domain configuration to be deleted.
        :returns: DeleteDomainConfigurationResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("DeleteDynamicThingGroup")
    def delete_dynamic_thing_group(
        self,
        context: RequestContext,
        thing_group_name: ThingGroupName,
        expected_version: OptionalVersion | None = None,
        **kwargs,
    ) -> DeleteDynamicThingGroupResponse:
        """Deletes a dynamic thing group.

        Requires permission to access the
        `DeleteDynamicThingGroup <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_group_name: The name of the dynamic thing group to delete.
        :param expected_version: The expected version of the dynamic thing group to delete.
        :returns: DeleteDynamicThingGroupResponse
        :raises InvalidRequestException:
        :raises VersionConflictException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DeleteFleetMetric")
    def delete_fleet_metric(
        self,
        context: RequestContext,
        metric_name: FleetMetricName,
        expected_version: OptionalVersion | None = None,
        **kwargs,
    ) -> None:
        """Deletes the specified fleet metric. Returns successfully with no error
        if the deletion is successful or you specify a fleet metric that doesn't
        exist.

        Requires permission to access the
        `DeleteFleetMetric <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param metric_name: The name of the fleet metric to delete.
        :param expected_version: The expected version of the fleet metric to delete.
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises VersionConflictException:
        """
        raise NotImplementedError

    @handler("DeleteJob")
    def delete_job(
        self,
        context: RequestContext,
        job_id: JobId,
        force: ForceFlag | None = None,
        namespace_id: NamespaceId | None = None,
        **kwargs,
    ) -> None:
        """Deletes a job and its related job executions.

        Deleting a job may take time, depending on the number of job executions
        created for the job and various other factors. While the job is being
        deleted, the status of the job will be shown as "DELETION_IN_PROGRESS".
        Attempting to delete or cancel a job whose status is already
        "DELETION_IN_PROGRESS" will result in an error.

        Only 10 jobs may have status "DELETION_IN_PROGRESS" at the same time, or
        a LimitExceededException will occur.

        Requires permission to access the
        `DeleteJob <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param job_id: The ID of the job to be deleted.
        :param force: (Optional) When true, you can delete a job which is "IN_PROGRESS".
        :param namespace_id: The namespace used to indicate that a job is a customer-managed job.
        :raises InvalidRequestException:
        :raises InvalidStateTransitionException:
        :raises ResourceNotFoundException:
        :raises LimitExceededException:
        :raises ThrottlingException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DeleteJobExecution")
    def delete_job_execution(
        self,
        context: RequestContext,
        job_id: JobId,
        thing_name: ThingName,
        execution_number: ExecutionNumber,
        force: ForceFlag | None = None,
        namespace_id: NamespaceId | None = None,
        **kwargs,
    ) -> None:
        """Deletes a job execution.

        Requires permission to access the
        `DeleteJobExecution <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param job_id: The ID of the job whose execution on a particular device will be
        deleted.
        :param thing_name: The name of the thing whose job execution will be deleted.
        :param execution_number: The ID of the job execution to be deleted.
        :param force: (Optional) When true, you can delete a job execution which is
        "IN_PROGRESS".
        :param namespace_id: The namespace used to indicate that a job is a customer-managed job.
        :raises InvalidRequestException:
        :raises InvalidStateTransitionException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DeleteJobTemplate")
    def delete_job_template(
        self, context: RequestContext, job_template_id: JobTemplateId, **kwargs
    ) -> None:
        """Deletes the specified job template.

        :param job_template_id: The unique identifier of the job template to delete.
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DeleteMitigationAction")
    def delete_mitigation_action(
        self, context: RequestContext, action_name: MitigationActionName, **kwargs
    ) -> DeleteMitigationActionResponse:
        """Deletes a defined mitigation action from your Amazon Web Services
        accounts.

        Requires permission to access the
        `DeleteMitigationAction <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param action_name: The name of the mitigation action that you want to delete.
        :returns: DeleteMitigationActionResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DeleteOTAUpdate")
    def delete_ota_update(
        self,
        context: RequestContext,
        ota_update_id: OTAUpdateId,
        delete_stream: DeleteStream | None = None,
        force_delete_aws_job: ForceDeleteAWSJob | None = None,
        **kwargs,
    ) -> DeleteOTAUpdateResponse:
        """Delete an OTA update.

        Requires permission to access the
        `DeleteOTAUpdate <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param ota_update_id: The ID of the OTA update to delete.
        :param delete_stream: When true, the stream created by the OTAUpdate process is deleted when
        the OTA update is deleted.
        :param force_delete_aws_job: When true, deletes the IoT job created by the OTAUpdate process even if
        it is "IN_PROGRESS".
        :returns: DeleteOTAUpdateResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises VersionConflictException:
        """
        raise NotImplementedError

    @handler("DeletePackage")
    def delete_package(
        self,
        context: RequestContext,
        package_name: PackageName,
        client_token: ClientToken | None = None,
        **kwargs,
    ) -> DeletePackageResponse:
        """Deletes a specific version from a software package.

        **Note:** All package versions must be deleted before deleting the
        software package.

        Requires permission to access the
        `DeletePackageVersion <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param package_name: The name of the target software package.
        :param client_token: A unique case-sensitive identifier that you can provide to ensure the
        idempotency of the request.
        :returns: DeletePackageResponse
        :raises ThrottlingException:
        :raises InternalServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("DeletePackageVersion")
    def delete_package_version(
        self,
        context: RequestContext,
        package_name: PackageName,
        version_name: VersionName,
        client_token: ClientToken | None = None,
        **kwargs,
    ) -> DeletePackageVersionResponse:
        """Deletes a specific version from a software package.

        **Note:** If a package version is designated as default, you must remove
        the designation from the software package using the UpdatePackage
        action.

        :param package_name: The name of the associated software package.
        :param version_name: The name of the target package version.
        :param client_token: A unique case-sensitive identifier that you can provide to ensure the
        idempotency of the request.
        :returns: DeletePackageVersionResponse
        :raises ThrottlingException:
        :raises InternalServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("DeletePolicy")
    def delete_policy(self, context: RequestContext, policy_name: PolicyName, **kwargs) -> None:
        """Deletes the specified policy.

        A policy cannot be deleted if it has non-default versions or it is
        attached to any certificate.

        To delete a policy, use the DeletePolicyVersion action to delete all
        non-default versions of the policy; use the DetachPolicy action to
        detach the policy from any certificate; and then use the DeletePolicy
        action to delete the policy.

        When a policy is deleted using DeletePolicy, its default version is
        deleted with it.

        Because of the distributed nature of Amazon Web Services, it can take up
        to five minutes after a policy is detached before it's ready to be
        deleted.

        Requires permission to access the
        `DeletePolicy <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param policy_name: The name of the policy to delete.
        :raises DeleteConflictException:
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DeletePolicyVersion")
    def delete_policy_version(
        self,
        context: RequestContext,
        policy_name: PolicyName,
        policy_version_id: PolicyVersionId,
        **kwargs,
    ) -> None:
        """Deletes the specified version of the specified policy. You cannot delete
        the default version of a policy using this action. To delete the default
        version of a policy, use DeletePolicy. To find out which version of a
        policy is marked as the default version, use ListPolicyVersions.

        Requires permission to access the
        `DeletePolicyVersion <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param policy_name: The name of the policy.
        :param policy_version_id: The policy version ID.
        :raises DeleteConflictException:
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DeleteProvisioningTemplate")
    def delete_provisioning_template(
        self, context: RequestContext, template_name: TemplateName, **kwargs
    ) -> DeleteProvisioningTemplateResponse:
        """Deletes a provisioning template.

        Requires permission to access the
        `DeleteProvisioningTemplate <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param template_name: The name of the fleet provision template to delete.
        :returns: DeleteProvisioningTemplateResponse
        :raises InternalFailureException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises DeleteConflictException:
        :raises ThrottlingException:
        :raises ConflictingResourceUpdateException:
        :raises UnauthorizedException:
        """
        raise NotImplementedError

    @handler("DeleteProvisioningTemplateVersion")
    def delete_provisioning_template_version(
        self,
        context: RequestContext,
        template_name: TemplateName,
        version_id: TemplateVersionId,
        **kwargs,
    ) -> DeleteProvisioningTemplateVersionResponse:
        """Deletes a provisioning template version.

        Requires permission to access the
        `DeleteProvisioningTemplateVersion <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param template_name: The name of the provisioning template version to delete.
        :param version_id: The provisioning template version ID to delete.
        :returns: DeleteProvisioningTemplateVersionResponse
        :raises InternalFailureException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises ResourceNotFoundException:
        :raises UnauthorizedException:
        :raises ConflictingResourceUpdateException:
        :raises DeleteConflictException:
        """
        raise NotImplementedError

    @handler("DeleteRegistrationCode")
    def delete_registration_code(
        self, context: RequestContext, **kwargs
    ) -> DeleteRegistrationCodeResponse:
        """Deletes a CA certificate registration code.

        Requires permission to access the
        `DeleteRegistrationCode <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :returns: DeleteRegistrationCodeResponse
        :raises ThrottlingException:
        :raises ResourceNotFoundException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DeleteRoleAlias")
    def delete_role_alias(
        self, context: RequestContext, role_alias: RoleAlias, **kwargs
    ) -> DeleteRoleAliasResponse:
        """Deletes a role alias

        Requires permission to access the
        `DeleteRoleAlias <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param role_alias: The role alias to delete.
        :returns: DeleteRoleAliasResponse
        :raises DeleteConflictException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("DeleteScheduledAudit")
    def delete_scheduled_audit(
        self, context: RequestContext, scheduled_audit_name: ScheduledAuditName, **kwargs
    ) -> DeleteScheduledAuditResponse:
        """Deletes a scheduled audit.

        Requires permission to access the
        `DeleteScheduledAudit <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param scheduled_audit_name: The name of the scheduled audit you want to delete.
        :returns: DeleteScheduledAuditResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DeleteSecurityProfile")
    def delete_security_profile(
        self,
        context: RequestContext,
        security_profile_name: SecurityProfileName,
        expected_version: OptionalVersion | None = None,
        **kwargs,
    ) -> DeleteSecurityProfileResponse:
        """Deletes a Device Defender security profile.

        Requires permission to access the
        `DeleteSecurityProfile <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param security_profile_name: The name of the security profile to be deleted.
        :param expected_version: The expected version of the security profile.
        :returns: DeleteSecurityProfileResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        :raises VersionConflictException:
        """
        raise NotImplementedError

    @handler("DeleteStream")
    def delete_stream(
        self, context: RequestContext, stream_id: StreamId, **kwargs
    ) -> DeleteStreamResponse:
        """Deletes a stream.

        Requires permission to access the
        `DeleteStream <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param stream_id: The stream ID.
        :returns: DeleteStreamResponse
        :raises ResourceNotFoundException:
        :raises DeleteConflictException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DeleteThing")
    def delete_thing(
        self,
        context: RequestContext,
        thing_name: ThingName,
        expected_version: OptionalVersion | None = None,
        **kwargs,
    ) -> DeleteThingResponse:
        """Deletes the specified thing. Returns successfully with no error if the
        deletion is successful or you specify a thing that doesn't exist.

        Requires permission to access the
        `DeleteThing <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_name: The name of the thing to delete.
        :param expected_version: The expected version of the thing record in the registry.
        :returns: DeleteThingResponse
        :raises ResourceNotFoundException:
        :raises VersionConflictException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DeleteThingGroup")
    def delete_thing_group(
        self,
        context: RequestContext,
        thing_group_name: ThingGroupName,
        expected_version: OptionalVersion | None = None,
        **kwargs,
    ) -> DeleteThingGroupResponse:
        """Deletes a thing group.

        Requires permission to access the
        `DeleteThingGroup <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_group_name: The name of the thing group to delete.
        :param expected_version: The expected version of the thing group to delete.
        :returns: DeleteThingGroupResponse
        :raises InvalidRequestException:
        :raises VersionConflictException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DeleteThingType")
    def delete_thing_type(
        self, context: RequestContext, thing_type_name: ThingTypeName, **kwargs
    ) -> DeleteThingTypeResponse:
        """Deletes the specified thing type. You cannot delete a thing type if it
        has things associated with it. To delete a thing type, first mark it as
        deprecated by calling DeprecateThingType, then remove any associated
        things by calling UpdateThing to change the thing type on any associated
        thing, and finally use DeleteThingType to delete the thing type.

        Requires permission to access the
        `DeleteThingType <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_type_name: The name of the thing type.
        :returns: DeleteThingTypeResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DeleteTopicRule")
    def delete_topic_rule(self, context: RequestContext, rule_name: RuleName, **kwargs) -> None:
        """Deletes the rule.

        Requires permission to access the
        `DeleteTopicRule <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param rule_name: The name of the rule.
        :raises InternalException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        :raises UnauthorizedException:
        :raises ConflictingResourceUpdateException:
        """
        raise NotImplementedError

    @handler("DeleteTopicRuleDestination")
    def delete_topic_rule_destination(
        self, context: RequestContext, arn: AwsArn, **kwargs
    ) -> DeleteTopicRuleDestinationResponse:
        """Deletes a topic rule destination.

        Requires permission to access the
        `DeleteTopicRuleDestination <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param arn: The ARN of the topic rule destination to delete.
        :returns: DeleteTopicRuleDestinationResponse
        :raises InternalException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        :raises UnauthorizedException:
        :raises ConflictingResourceUpdateException:
        """
        raise NotImplementedError

    @handler("DeleteV2LoggingLevel")
    def delete_v2_logging_level(
        self,
        context: RequestContext,
        target_type: LogTargetType,
        target_name: LogTargetName,
        **kwargs,
    ) -> None:
        """Deletes a logging level.

        Requires permission to access the
        `DeleteV2LoggingLevel <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param target_type: The type of resource for which you are configuring logging.
        :param target_name: The name of the resource for which you are configuring logging.
        :raises InternalException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DeprecateThingType")
    def deprecate_thing_type(
        self,
        context: RequestContext,
        thing_type_name: ThingTypeName,
        undo_deprecate: UndoDeprecate | None = None,
        **kwargs,
    ) -> DeprecateThingTypeResponse:
        """Deprecates a thing type. You can not associate new things with
        deprecated thing type.

        Requires permission to access the
        `DeprecateThingType <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_type_name: The name of the thing type to deprecate.
        :param undo_deprecate: Whether to undeprecate a deprecated thing type.
        :returns: DeprecateThingTypeResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DescribeAccountAuditConfiguration")
    def describe_account_audit_configuration(
        self, context: RequestContext, **kwargs
    ) -> DescribeAccountAuditConfigurationResponse:
        """Gets information about the Device Defender audit settings for this
        account. Settings include how audit notifications are sent and which
        audit checks are enabled or disabled.

        Requires permission to access the
        `DescribeAccountAuditConfiguration <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :returns: DescribeAccountAuditConfigurationResponse
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DescribeAuditFinding")
    def describe_audit_finding(
        self, context: RequestContext, finding_id: FindingId, **kwargs
    ) -> DescribeAuditFindingResponse:
        """Gets information about a single audit finding. Properties include the
        reason for noncompliance, the severity of the issue, and the start time
        when the audit that returned the finding.

        Requires permission to access the
        `DescribeAuditFinding <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param finding_id: A unique identifier for a single audit finding.
        :returns: DescribeAuditFindingResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DescribeAuditMitigationActionsTask")
    def describe_audit_mitigation_actions_task(
        self, context: RequestContext, task_id: MitigationActionsTaskId, **kwargs
    ) -> DescribeAuditMitigationActionsTaskResponse:
        """Gets information about an audit mitigation task that is used to apply
        mitigation actions to a set of audit findings. Properties include the
        actions being applied, the audit checks to which they're being applied,
        the task status, and aggregated task statistics.

        :param task_id: The unique identifier for the audit mitigation task.
        :returns: DescribeAuditMitigationActionsTaskResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DescribeAuditSuppression")
    def describe_audit_suppression(
        self,
        context: RequestContext,
        check_name: AuditCheckName,
        resource_identifier: ResourceIdentifier,
        **kwargs,
    ) -> DescribeAuditSuppressionResponse:
        """Gets information about a Device Defender audit suppression.

        :param check_name: An audit check name.
        :param resource_identifier: Information that identifies the noncompliant resource.
        :returns: DescribeAuditSuppressionResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DescribeAuditTask")
    def describe_audit_task(
        self, context: RequestContext, task_id: AuditTaskId, **kwargs
    ) -> DescribeAuditTaskResponse:
        """Gets information about a Device Defender audit.

        Requires permission to access the
        `DescribeAuditTask <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param task_id: The ID of the audit whose information you want to get.
        :returns: DescribeAuditTaskResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DescribeAuthorizer")
    def describe_authorizer(
        self, context: RequestContext, authorizer_name: AuthorizerName, **kwargs
    ) -> DescribeAuthorizerResponse:
        """Describes an authorizer.

        Requires permission to access the
        `DescribeAuthorizer <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param authorizer_name: The name of the authorizer to describe.
        :returns: DescribeAuthorizerResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DescribeBillingGroup")
    def describe_billing_group(
        self, context: RequestContext, billing_group_name: BillingGroupName, **kwargs
    ) -> DescribeBillingGroupResponse:
        """Returns information about a billing group.

        Requires permission to access the
        `DescribeBillingGroup <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param billing_group_name: The name of the billing group.
        :returns: DescribeBillingGroupResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeCACertificate")
    def describe_ca_certificate(
        self, context: RequestContext, certificate_id: CertificateId, **kwargs
    ) -> DescribeCACertificateResponse:
        """Describes a registered CA certificate.

        Requires permission to access the
        `DescribeCACertificate <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param certificate_id: The CA certificate identifier.
        :returns: DescribeCACertificateResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeCertificate")
    def describe_certificate(
        self, context: RequestContext, certificate_id: CertificateId, **kwargs
    ) -> DescribeCertificateResponse:
        """Gets information about the specified certificate.

        Requires permission to access the
        `DescribeCertificate <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param certificate_id: The ID of the certificate.
        :returns: DescribeCertificateResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeCertificateProvider")
    def describe_certificate_provider(
        self, context: RequestContext, certificate_provider_name: CertificateProviderName, **kwargs
    ) -> DescribeCertificateProviderResponse:
        """Describes a certificate provider.

        Requires permission to access the
        `DescribeCertificateProvider <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param certificate_provider_name: The name of the certificate provider.
        :returns: DescribeCertificateProviderResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DescribeCustomMetric")
    def describe_custom_metric(
        self, context: RequestContext, metric_name: MetricName, **kwargs
    ) -> DescribeCustomMetricResponse:
        """Gets information about a Device Defender detect custom metric.

        Requires permission to access the
        `DescribeCustomMetric <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param metric_name: The name of the custom metric.
        :returns: DescribeCustomMetricResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DescribeDefaultAuthorizer")
    def describe_default_authorizer(
        self, context: RequestContext, **kwargs
    ) -> DescribeDefaultAuthorizerResponse:
        """Describes the default authorizer.

        Requires permission to access the
        `DescribeDefaultAuthorizer <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :returns: DescribeDefaultAuthorizerResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DescribeDetectMitigationActionsTask")
    def describe_detect_mitigation_actions_task(
        self, context: RequestContext, task_id: MitigationActionsTaskId, **kwargs
    ) -> DescribeDetectMitigationActionsTaskResponse:
        """Gets information about a Device Defender ML Detect mitigation action.

        Requires permission to access the
        `DescribeDetectMitigationActionsTask <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param task_id: The unique identifier of the task.
        :returns: DescribeDetectMitigationActionsTaskResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DescribeDimension")
    def describe_dimension(
        self, context: RequestContext, name: DimensionName, **kwargs
    ) -> DescribeDimensionResponse:
        """Provides details about a dimension that is defined in your Amazon Web
        Services accounts.

        Requires permission to access the
        `DescribeDimension <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param name: The unique identifier for the dimension.
        :returns: DescribeDimensionResponse
        :raises InternalFailureException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DescribeDomainConfiguration")
    def describe_domain_configuration(
        self,
        context: RequestContext,
        domain_configuration_name: ReservedDomainConfigurationName,
        **kwargs,
    ) -> DescribeDomainConfigurationResponse:
        """Gets summary information about a domain configuration.

        Requires permission to access the
        `DescribeDomainConfiguration <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param domain_configuration_name: The name of the domain configuration.
        :returns: DescribeDomainConfigurationResponse
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InvalidRequestException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DescribeEncryptionConfiguration")
    def describe_encryption_configuration(
        self, context: RequestContext, **kwargs
    ) -> DescribeEncryptionConfigurationResponse:
        """Retrieves the encryption configuration for resources and data of your
        Amazon Web Services account in Amazon Web Services IoT Core. For more
        information, see `Key management in
        IoT <https://docs.aws.amazon.com/iot/latest/developerguide/key-management.html>`__
        from the *Amazon Web Services IoT Core Developer Guide*.

        :returns: DescribeEncryptionConfigurationResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DescribeEndpoint")
    def describe_endpoint(
        self, context: RequestContext, endpoint_type: EndpointType | None = None, **kwargs
    ) -> DescribeEndpointResponse:
        """Returns or creates a unique endpoint specific to the Amazon Web Services
        account making the call.

        The first time ``DescribeEndpoint`` is called, an endpoint is created.
        All subsequent calls to ``DescribeEndpoint`` return the same endpoint.

        Requires permission to access the
        `DescribeEndpoint <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param endpoint_type: The endpoint type.
        :returns: DescribeEndpointResponse
        :raises InternalFailureException:
        :raises InvalidRequestException:
        :raises UnauthorizedException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DescribeEventConfigurations")
    def describe_event_configurations(
        self, context: RequestContext, **kwargs
    ) -> DescribeEventConfigurationsResponse:
        """Describes event configurations.

        Requires permission to access the
        `DescribeEventConfigurations <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :returns: DescribeEventConfigurationsResponse
        :raises InternalFailureException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DescribeFleetMetric")
    def describe_fleet_metric(
        self, context: RequestContext, metric_name: FleetMetricName, **kwargs
    ) -> DescribeFleetMetricResponse:
        """Gets information about the specified fleet metric.

        Requires permission to access the
        `DescribeFleetMetric <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param metric_name: The name of the fleet metric to describe.
        :returns: DescribeFleetMetricResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeIndex")
    def describe_index(
        self, context: RequestContext, index_name: IndexName, **kwargs
    ) -> DescribeIndexResponse:
        """Describes a search index.

        Requires permission to access the
        `DescribeIndex <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param index_name: The index name.
        :returns: DescribeIndexResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeJob")
    def describe_job(
        self,
        context: RequestContext,
        job_id: JobId,
        before_substitution: BeforeSubstitutionFlag | None = None,
        **kwargs,
    ) -> DescribeJobResponse:
        """Describes a job.

        Requires permission to access the
        `DescribeJob <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param job_id: The unique identifier you assigned to this job when it was created.
        :param before_substitution: Provides a view of the job document before and after the substitution
        parameters have been resolved with their exact values.
        :returns: DescribeJobResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DescribeJobExecution")
    def describe_job_execution(
        self,
        context: RequestContext,
        job_id: JobId,
        thing_name: ThingName,
        execution_number: ExecutionNumber | None = None,
        **kwargs,
    ) -> DescribeJobExecutionResponse:
        """Describes a job execution.

        Requires permission to access the
        `DescribeJobExecution <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param job_id: The unique identifier you assigned to this job when it was created.
        :param thing_name: The name of the thing on which the job execution is running.
        :param execution_number: A string (consisting of the digits "0" through "9" which is used to
        specify a particular job execution on a particular device.
        :returns: DescribeJobExecutionResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DescribeJobTemplate")
    def describe_job_template(
        self, context: RequestContext, job_template_id: JobTemplateId, **kwargs
    ) -> DescribeJobTemplateResponse:
        """Returns information about a job template.

        :param job_template_id: The unique identifier of the job template.
        :returns: DescribeJobTemplateResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DescribeManagedJobTemplate")
    def describe_managed_job_template(
        self,
        context: RequestContext,
        template_name: ManagedJobTemplateName,
        template_version: ManagedTemplateVersion | None = None,
        **kwargs,
    ) -> DescribeManagedJobTemplateResponse:
        """View details of a managed job template.

        :param template_name: The unique name of a managed job template, which is required.
        :param template_version: An optional parameter to specify version of a managed template.
        :returns: DescribeManagedJobTemplateResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("DescribeMitigationAction")
    def describe_mitigation_action(
        self, context: RequestContext, action_name: MitigationActionName, **kwargs
    ) -> DescribeMitigationActionResponse:
        """Gets information about a mitigation action.

        Requires permission to access the
        `DescribeMitigationAction <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param action_name: The friendly name that uniquely identifies the mitigation action.
        :returns: DescribeMitigationActionResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DescribeProvisioningTemplate")
    def describe_provisioning_template(
        self, context: RequestContext, template_name: TemplateName, **kwargs
    ) -> DescribeProvisioningTemplateResponse:
        """Returns information about a provisioning template.

        Requires permission to access the
        `DescribeProvisioningTemplate <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param template_name: The name of the provisioning template.
        :returns: DescribeProvisioningTemplateResponse
        :raises InternalFailureException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        """
        raise NotImplementedError

    @handler("DescribeProvisioningTemplateVersion")
    def describe_provisioning_template_version(
        self,
        context: RequestContext,
        template_name: TemplateName,
        version_id: TemplateVersionId,
        **kwargs,
    ) -> DescribeProvisioningTemplateVersionResponse:
        """Returns information about a provisioning template version.

        Requires permission to access the
        `DescribeProvisioningTemplateVersion <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param template_name: The template name.
        :param version_id: The provisioning template version ID.
        :returns: DescribeProvisioningTemplateVersionResponse
        :raises InternalFailureException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises ResourceNotFoundException:
        :raises UnauthorizedException:
        """
        raise NotImplementedError

    @handler("DescribeRoleAlias")
    def describe_role_alias(
        self, context: RequestContext, role_alias: RoleAlias, **kwargs
    ) -> DescribeRoleAliasResponse:
        """Describes a role alias.

        Requires permission to access the
        `DescribeRoleAlias <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param role_alias: The role alias to describe.
        :returns: DescribeRoleAliasResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeScheduledAudit")
    def describe_scheduled_audit(
        self, context: RequestContext, scheduled_audit_name: ScheduledAuditName, **kwargs
    ) -> DescribeScheduledAuditResponse:
        """Gets information about a scheduled audit.

        Requires permission to access the
        `DescribeScheduledAudit <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param scheduled_audit_name: The name of the scheduled audit whose information you want to get.
        :returns: DescribeScheduledAuditResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DescribeSecurityProfile")
    def describe_security_profile(
        self, context: RequestContext, security_profile_name: SecurityProfileName, **kwargs
    ) -> DescribeSecurityProfileResponse:
        """Gets information about a Device Defender security profile.

        Requires permission to access the
        `DescribeSecurityProfile <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param security_profile_name: The name of the security profile whose information you want to get.
        :returns: DescribeSecurityProfileResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DescribeStream")
    def describe_stream(
        self, context: RequestContext, stream_id: StreamId, **kwargs
    ) -> DescribeStreamResponse:
        """Gets information about a stream.

        Requires permission to access the
        `DescribeStream <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param stream_id: The stream ID.
        :returns: DescribeStreamResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DescribeThing")
    def describe_thing(
        self, context: RequestContext, thing_name: ThingName, **kwargs
    ) -> DescribeThingResponse:
        """Gets information about the specified thing.

        Requires permission to access the
        `DescribeThing <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_name: The name of the thing.
        :returns: DescribeThingResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DescribeThingGroup")
    def describe_thing_group(
        self, context: RequestContext, thing_group_name: ThingGroupName, **kwargs
    ) -> DescribeThingGroupResponse:
        """Describe a thing group.

        Requires permission to access the
        `DescribeThingGroup <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_group_name: The name of the thing group.
        :returns: DescribeThingGroupResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeThingRegistrationTask")
    def describe_thing_registration_task(
        self, context: RequestContext, task_id: TaskId, **kwargs
    ) -> DescribeThingRegistrationTaskResponse:
        """Describes a bulk thing provisioning task.

        Requires permission to access the
        `DescribeThingRegistrationTask <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param task_id: The task ID.
        :returns: DescribeThingRegistrationTaskResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeThingType")
    def describe_thing_type(
        self, context: RequestContext, thing_type_name: ThingTypeName, **kwargs
    ) -> DescribeThingTypeResponse:
        """Gets information about the specified thing type.

        Requires permission to access the
        `DescribeThingType <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_type_name: The name of the thing type.
        :returns: DescribeThingTypeResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DetachPolicy")
    def detach_policy(
        self, context: RequestContext, policy_name: PolicyName, target: PolicyTarget, **kwargs
    ) -> None:
        """Detaches a policy from the specified target.

        Because of the distributed nature of Amazon Web Services, it can take up
        to five minutes after a policy is detached before it's ready to be
        deleted.

        Requires permission to access the
        `DetachPolicy <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param policy_name: The policy to detach.
        :param target: The target from which the policy will be detached.
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("DetachPrincipalPolicy")
    def detach_principal_policy(
        self, context: RequestContext, policy_name: PolicyName, principal: Principal, **kwargs
    ) -> None:
        """Removes the specified policy from the specified certificate.

        **Note:** This action is deprecated and works as expected for backward
        compatibility, but we won't add enhancements. Use DetachPolicy instead.

        Requires permission to access the
        `DetachPrincipalPolicy <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param policy_name: The name of the policy to detach.
        :param principal: The principal.
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DetachSecurityProfile")
    def detach_security_profile(
        self,
        context: RequestContext,
        security_profile_name: SecurityProfileName,
        security_profile_target_arn: SecurityProfileTargetArn,
        **kwargs,
    ) -> DetachSecurityProfileResponse:
        """Disassociates a Device Defender security profile from a thing group or
        from this account.

        Requires permission to access the
        `DetachSecurityProfile <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param security_profile_name: The security profile that is detached.
        :param security_profile_target_arn: The ARN of the thing group from which the security profile is detached.
        :returns: DetachSecurityProfileResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DetachThingPrincipal")
    def detach_thing_principal(
        self, context: RequestContext, thing_name: ThingName, principal: Principal, **kwargs
    ) -> DetachThingPrincipalResponse:
        """Detaches the specified principal from the specified thing. A principal
        can be X.509 certificates, IAM users, groups, and roles, Amazon Cognito
        identities or federated identities.

        This call is asynchronous. It might take several seconds for the
        detachment to propagate.

        Requires permission to access the
        `DetachThingPrincipal <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_name: The name of the thing.
        :param principal: If the principal is a certificate, this value must be ARN of the
        certificate.
        :returns: DetachThingPrincipalResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("DisableTopicRule")
    def disable_topic_rule(self, context: RequestContext, rule_name: RuleName, **kwargs) -> None:
        """Disables the rule.

        Requires permission to access the
        `DisableTopicRule <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param rule_name: The name of the rule to disable.
        :raises InternalException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        :raises UnauthorizedException:
        :raises ConflictingResourceUpdateException:
        """
        raise NotImplementedError

    @handler("DisassociateSbomFromPackageVersion")
    def disassociate_sbom_from_package_version(
        self,
        context: RequestContext,
        package_name: PackageName,
        version_name: VersionName,
        client_token: ClientToken | None = None,
        **kwargs,
    ) -> DisassociateSbomFromPackageVersionResponse:
        """Disassociates the selected software bill of materials (SBOM) from a
        specific software package version.

        Requires permission to access the
        `DisassociateSbomWithPackageVersion <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param package_name: The name of the new software package.
        :param version_name: The name of the new package version.
        :param client_token: A unique case-sensitive identifier that you can provide to ensure the
        idempotency of the request.
        :returns: DisassociateSbomFromPackageVersionResponse
        :raises ThrottlingException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ValidationException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("EnableTopicRule")
    def enable_topic_rule(self, context: RequestContext, rule_name: RuleName, **kwargs) -> None:
        """Enables the rule.

        Requires permission to access the
        `EnableTopicRule <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param rule_name: The name of the topic rule to enable.
        :raises InternalException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        :raises UnauthorizedException:
        :raises ConflictingResourceUpdateException:
        """
        raise NotImplementedError

    @handler("GetBehaviorModelTrainingSummaries")
    def get_behavior_model_training_summaries(
        self,
        context: RequestContext,
        security_profile_name: SecurityProfileName | None = None,
        max_results: TinyMaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> GetBehaviorModelTrainingSummariesResponse:
        """Returns a Device Defender's ML Detect Security Profile training model's
        status.

        Requires permission to access the
        `GetBehaviorModelTrainingSummaries <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param security_profile_name: The name of the security profile.
        :param max_results: The maximum number of results to return at one time.
        :param next_token: The token for the next set of results.
        :returns: GetBehaviorModelTrainingSummariesResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetBucketsAggregation")
    def get_buckets_aggregation(
        self,
        context: RequestContext,
        query_string: QueryString,
        aggregation_field: AggregationField,
        buckets_aggregation_type: BucketsAggregationType,
        index_name: IndexName | None = None,
        query_version: QueryVersion | None = None,
        **kwargs,
    ) -> GetBucketsAggregationResponse:
        """Aggregates on indexed data with search queries pertaining to particular
        fields.

        Requires permission to access the
        `GetBucketsAggregation <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param query_string: The search query string.
        :param aggregation_field: The aggregation field.
        :param buckets_aggregation_type: The basic control of the response shape and the bucket aggregation type
        to perform.
        :param index_name: The name of the index to search.
        :param query_version: The version of the query.
        :returns: GetBucketsAggregationResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        :raises InvalidQueryException:
        :raises InvalidAggregationException:
        :raises IndexNotReadyException:
        """
        raise NotImplementedError

    @handler("GetCardinality")
    def get_cardinality(
        self,
        context: RequestContext,
        query_string: QueryString,
        index_name: IndexName | None = None,
        aggregation_field: AggregationField | None = None,
        query_version: QueryVersion | None = None,
        **kwargs,
    ) -> GetCardinalityResponse:
        """Returns the approximate count of unique values that match the query.

        Requires permission to access the
        `GetCardinality <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param query_string: The search query string.
        :param index_name: The name of the index to search.
        :param aggregation_field: The field to aggregate.
        :param query_version: The query version.
        :returns: GetCardinalityResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        :raises InvalidQueryException:
        :raises InvalidAggregationException:
        :raises IndexNotReadyException:
        """
        raise NotImplementedError

    @handler("GetCommand")
    def get_command(
        self, context: RequestContext, command_id: CommandId, **kwargs
    ) -> GetCommandResponse:
        """Gets information about the specified command.

        :param command_id: The unique identifier of the command for which you want to retrieve
        information.
        :returns: GetCommandResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("GetCommandExecution")
    def get_command_execution(
        self,
        context: RequestContext,
        execution_id: CommandExecutionId,
        target_arn: TargetArn,
        include_result: BooleanWrapperObject | None = None,
        **kwargs,
    ) -> GetCommandExecutionResponse:
        """Gets information about the specific command execution on a single
        device.

        :param execution_id: The unique identifier for the command execution.
        :param target_arn: The Amazon Resource Number (ARN) of the device on which the command
        execution is being performed.
        :param include_result: Can be used to specify whether to include the result of the command
        execution in the ``GetCommandExecution`` API response.
        :returns: GetCommandExecutionResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("GetEffectivePolicies")
    def get_effective_policies(
        self,
        context: RequestContext,
        principal: Principal | None = None,
        cognito_identity_pool_id: CognitoIdentityPoolId | None = None,
        thing_name: ThingName | None = None,
        **kwargs,
    ) -> GetEffectivePoliciesResponse:
        """Gets a list of the policies that have an effect on the authorization
        behavior of the specified device when it connects to the IoT device
        gateway.

        Requires permission to access the
        `GetEffectivePolicies <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param principal: The principal.
        :param cognito_identity_pool_id: The Cognito identity pool ID.
        :param thing_name: The thing name.
        :returns: GetEffectivePoliciesResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("GetIndexingConfiguration")
    def get_indexing_configuration(
        self, context: RequestContext, **kwargs
    ) -> GetIndexingConfigurationResponse:
        """Gets the indexing configuration.

        Requires permission to access the
        `GetIndexingConfiguration <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :returns: GetIndexingConfigurationResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("GetJobDocument")
    def get_job_document(
        self,
        context: RequestContext,
        job_id: JobId,
        before_substitution: BeforeSubstitutionFlag | None = None,
        **kwargs,
    ) -> GetJobDocumentResponse:
        """Gets a job document.

        Requires permission to access the
        `GetJobDocument <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param job_id: The unique identifier you assigned to this job when it was created.
        :param before_substitution: Provides a view of the job document before and after the substitution
        parameters have been resolved with their exact values.
        :returns: GetJobDocumentResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("GetLoggingOptions")
    def get_logging_options(self, context: RequestContext, **kwargs) -> GetLoggingOptionsResponse:
        """Gets the logging options.

        NOTE: use of this command is not recommended. Use
        ``GetV2LoggingOptions`` instead.

        Requires permission to access the
        `GetLoggingOptions <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :returns: GetLoggingOptionsResponse
        :raises InternalException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("GetOTAUpdate")
    def get_ota_update(
        self, context: RequestContext, ota_update_id: OTAUpdateId, **kwargs
    ) -> GetOTAUpdateResponse:
        """Gets an OTA update.

        Requires permission to access the
        `GetOTAUpdate <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param ota_update_id: The OTA update ID.
        :returns: GetOTAUpdateResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetPackage")
    def get_package(
        self, context: RequestContext, package_name: PackageName, **kwargs
    ) -> GetPackageResponse:
        """Gets information about the specified software package.

        Requires permission to access the
        `GetPackage <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param package_name: The name of the target software package.
        :returns: GetPackageResponse
        :raises ThrottlingException:
        :raises InternalServerException:
        :raises ValidationException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetPackageConfiguration")
    def get_package_configuration(
        self, context: RequestContext, **kwargs
    ) -> GetPackageConfigurationResponse:
        """Gets information about the specified software package's configuration.

        Requires permission to access the
        `GetPackageConfiguration <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :returns: GetPackageConfigurationResponse
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("GetPackageVersion")
    def get_package_version(
        self,
        context: RequestContext,
        package_name: PackageName,
        version_name: VersionName,
        **kwargs,
    ) -> GetPackageVersionResponse:
        """Gets information about the specified package version.

        Requires permission to access the
        `GetPackageVersion <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param package_name: The name of the associated package.
        :param version_name: The name of the target package version.
        :returns: GetPackageVersionResponse
        :raises ThrottlingException:
        :raises InternalServerException:
        :raises ValidationException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetPercentiles")
    def get_percentiles(
        self,
        context: RequestContext,
        query_string: QueryString,
        index_name: IndexName | None = None,
        aggregation_field: AggregationField | None = None,
        query_version: QueryVersion | None = None,
        percents: PercentList | None = None,
        **kwargs,
    ) -> GetPercentilesResponse:
        """Groups the aggregated values that match the query into percentile
        groupings. The default percentile groupings are: 1,5,25,50,75,95,99,
        although you can specify your own when you call ``GetPercentiles``. This
        function returns a value for each percentile group specified (or the
        default percentile groupings). The percentile group "1" contains the
        aggregated field value that occurs in approximately one percent of the
        values that match the query. The percentile group "5" contains the
        aggregated field value that occurs in approximately five percent of the
        values that match the query, and so on. The result is an approximation,
        the more values that match the query, the more accurate the percentile
        values.

        Requires permission to access the
        `GetPercentiles <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param query_string: The search query string.
        :param index_name: The name of the index to search.
        :param aggregation_field: The field to aggregate.
        :param query_version: The query version.
        :param percents: The percentile groups returned.
        :returns: GetPercentilesResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        :raises InvalidQueryException:
        :raises InvalidAggregationException:
        :raises IndexNotReadyException:
        """
        raise NotImplementedError

    @handler("GetPolicy")
    def get_policy(
        self, context: RequestContext, policy_name: PolicyName, **kwargs
    ) -> GetPolicyResponse:
        """Gets information about the specified policy with the policy document of
        the default version.

        Requires permission to access the
        `GetPolicy <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param policy_name: The name of the policy.
        :returns: GetPolicyResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("GetPolicyVersion")
    def get_policy_version(
        self,
        context: RequestContext,
        policy_name: PolicyName,
        policy_version_id: PolicyVersionId,
        **kwargs,
    ) -> GetPolicyVersionResponse:
        """Gets information about the specified policy version.

        Requires permission to access the
        `GetPolicyVersion <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param policy_name: The name of the policy.
        :param policy_version_id: The policy version ID.
        :returns: GetPolicyVersionResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("GetRegistrationCode")
    def get_registration_code(
        self, context: RequestContext, **kwargs
    ) -> GetRegistrationCodeResponse:
        """Gets a registration code used to register a CA certificate with IoT.

        IoT will create a registration code as part of this API call if the
        registration code doesn't exist or has been deleted. If you already have
        a registration code, this API call will return the same registration
        code.

        Requires permission to access the
        `GetRegistrationCode <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :returns: GetRegistrationCodeResponse
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("GetStatistics")
    def get_statistics(
        self,
        context: RequestContext,
        query_string: QueryString,
        index_name: IndexName | None = None,
        aggregation_field: AggregationField | None = None,
        query_version: QueryVersion | None = None,
        **kwargs,
    ) -> GetStatisticsResponse:
        """Returns the count, average, sum, minimum, maximum, sum of squares,
        variance, and standard deviation for the specified aggregated field. If
        the aggregation field is of type ``String``, only the count statistic is
        returned.

        Requires permission to access the
        `GetStatistics <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param query_string: The query used to search.
        :param index_name: The name of the index to search.
        :param aggregation_field: The aggregation field name.
        :param query_version: The version of the query used to search.
        :returns: GetStatisticsResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        :raises InvalidQueryException:
        :raises InvalidAggregationException:
        :raises IndexNotReadyException:
        """
        raise NotImplementedError

    @handler("GetThingConnectivityData")
    def get_thing_connectivity_data(
        self, context: RequestContext, thing_name: ConnectivityApiThingName, **kwargs
    ) -> GetThingConnectivityDataResponse:
        """Retrieves the live connectivity status per device.

        :param thing_name: The name of your IoT thing.
        :returns: GetThingConnectivityDataResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        :raises IndexNotReadyException:
        """
        raise NotImplementedError

    @handler("GetTopicRule")
    def get_topic_rule(
        self, context: RequestContext, rule_name: RuleName, **kwargs
    ) -> GetTopicRuleResponse:
        """Gets information about the rule.

        Requires permission to access the
        `GetTopicRule <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param rule_name: The name of the rule.
        :returns: GetTopicRuleResponse
        :raises InternalException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        :raises UnauthorizedException:
        """
        raise NotImplementedError

    @handler("GetTopicRuleDestination")
    def get_topic_rule_destination(
        self, context: RequestContext, arn: AwsArn, **kwargs
    ) -> GetTopicRuleDestinationResponse:
        """Gets information about a topic rule destination.

        Requires permission to access the
        `GetTopicRuleDestination <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param arn: The ARN of the topic rule destination.
        :returns: GetTopicRuleDestinationResponse
        :raises InternalException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        :raises UnauthorizedException:
        """
        raise NotImplementedError

    @handler("GetV2LoggingOptions")
    def get_v2_logging_options(
        self, context: RequestContext, **kwargs
    ) -> GetV2LoggingOptionsResponse:
        """Gets the fine grained logging options.

        Requires permission to access the
        `GetV2LoggingOptions <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :returns: GetV2LoggingOptionsResponse
        :raises InternalException:
        :raises NotConfiguredException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListActiveViolations")
    def list_active_violations(
        self,
        context: RequestContext,
        thing_name: DeviceDefenderThingName | None = None,
        security_profile_name: SecurityProfileName | None = None,
        behavior_criteria_type: BehaviorCriteriaType | None = None,
        list_suppressed_alerts: ListSuppressedAlerts | None = None,
        verification_state: VerificationState | None = None,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListActiveViolationsResponse:
        """Lists the active violations for a given Device Defender security
        profile.

        Requires permission to access the
        `ListActiveViolations <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_name: The name of the thing whose active violations are listed.
        :param security_profile_name: The name of the Device Defender security profile for which violations
        are listed.
        :param behavior_criteria_type: The criteria for a behavior.
        :param list_suppressed_alerts: A list of all suppressed alerts.
        :param verification_state: The verification state of the violation (detect alarm).
        :param next_token: The token for the next set of results.
        :param max_results: The maximum number of results to return at one time.
        :returns: ListActiveViolationsResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListAttachedPolicies")
    def list_attached_policies(
        self,
        context: RequestContext,
        target: PolicyTarget,
        recursive: Recursive | None = None,
        marker: Marker | None = None,
        page_size: PageSize | None = None,
        **kwargs,
    ) -> ListAttachedPoliciesResponse:
        """Lists the policies attached to the specified thing group.

        Requires permission to access the
        `ListAttachedPolicies <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param target: The group or principal for which the policies will be listed.
        :param recursive: When true, recursively list attached policies.
        :param marker: The token to retrieve the next set of results.
        :param page_size: The maximum number of results to be returned per request.
        :returns: ListAttachedPoliciesResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("ListAuditFindings")
    def list_audit_findings(
        self,
        context: RequestContext,
        task_id: AuditTaskId | None = None,
        check_name: AuditCheckName | None = None,
        resource_identifier: ResourceIdentifier | None = None,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        start_time: Timestamp | None = None,
        end_time: Timestamp | None = None,
        list_suppressed_findings: ListSuppressedFindings | None = None,
        **kwargs,
    ) -> ListAuditFindingsResponse:
        """Lists the findings (results) of a Device Defender audit or of the audits
        performed during a specified time period. (Findings are retained for 90
        days.)

        Requires permission to access the
        `ListAuditFindings <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param task_id: A filter to limit results to the audit with the specified ID.
        :param check_name: A filter to limit results to the findings for the specified audit check.
        :param resource_identifier: Information identifying the noncompliant resource.
        :param max_results: The maximum number of results to return at one time.
        :param next_token: The token for the next set of results.
        :param start_time: A filter to limit results to those found after the specified time.
        :param end_time: A filter to limit results to those found before the specified time.
        :param list_suppressed_findings: Boolean flag indicating whether only the suppressed findings or the
        unsuppressed findings should be listed.
        :returns: ListAuditFindingsResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListAuditMitigationActionsExecutions")
    def list_audit_mitigation_actions_executions(
        self,
        context: RequestContext,
        task_id: MitigationActionsTaskId,
        finding_id: FindingId,
        action_status: AuditMitigationActionsExecutionStatus | None = None,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListAuditMitigationActionsExecutionsResponse:
        """Gets the status of audit mitigation action tasks that were executed.

        Requires permission to access the
        `ListAuditMitigationActionsExecutions <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param task_id: Specify this filter to limit results to actions for a specific audit
        mitigation actions task.
        :param finding_id: Specify this filter to limit results to those that were applied to a
        specific audit finding.
        :param action_status: Specify this filter to limit results to those with a specific status.
        :param max_results: The maximum number of results to return at one time.
        :param next_token: The token for the next set of results.
        :returns: ListAuditMitigationActionsExecutionsResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListAuditMitigationActionsTasks")
    def list_audit_mitigation_actions_tasks(
        self,
        context: RequestContext,
        start_time: Timestamp,
        end_time: Timestamp,
        audit_task_id: AuditTaskId | None = None,
        finding_id: FindingId | None = None,
        task_status: AuditMitigationActionsTaskStatus | None = None,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListAuditMitigationActionsTasksResponse:
        """Gets a list of audit mitigation action tasks that match the specified
        filters.

        Requires permission to access the
        `ListAuditMitigationActionsTasks <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param start_time: Specify this filter to limit results to tasks that began on or after a
        specific date and time.
        :param end_time: Specify this filter to limit results to tasks that were completed or
        canceled on or before a specific date and time.
        :param audit_task_id: Specify this filter to limit results to tasks that were applied to
        results for a specific audit.
        :param finding_id: Specify this filter to limit results to tasks that were applied to a
        specific audit finding.
        :param task_status: Specify this filter to limit results to tasks that are in a specific
        state.
        :param max_results: The maximum number of results to return at one time.
        :param next_token: The token for the next set of results.
        :returns: ListAuditMitigationActionsTasksResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListAuditSuppressions")
    def list_audit_suppressions(
        self,
        context: RequestContext,
        check_name: AuditCheckName | None = None,
        resource_identifier: ResourceIdentifier | None = None,
        ascending_order: AscendingOrder | None = None,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListAuditSuppressionsResponse:
        """Lists your Device Defender audit listings.

        Requires permission to access the
        `ListAuditSuppressions <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param check_name: An audit check name.
        :param resource_identifier: Information that identifies the noncompliant resource.
        :param ascending_order: Determines whether suppressions are listed in ascending order by
        expiration date or not.
        :param next_token: The token for the next set of results.
        :param max_results: The maximum number of results to return at one time.
        :returns: ListAuditSuppressionsResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListAuditTasks")
    def list_audit_tasks(
        self,
        context: RequestContext,
        start_time: Timestamp,
        end_time: Timestamp,
        task_type: AuditTaskType | None = None,
        task_status: AuditTaskStatus | None = None,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListAuditTasksResponse:
        """Lists the Device Defender audits that have been performed during a given
        time period.

        Requires permission to access the
        `ListAuditTasks <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param start_time: The beginning of the time period.
        :param end_time: The end of the time period.
        :param task_type: A filter to limit the output to the specified type of audit: can be one
        of "ON_DEMAND_AUDIT_TASK" or "SCHEDULED__AUDIT_TASK".
        :param task_status: A filter to limit the output to audits with the specified completion
        status: can be one of "IN_PROGRESS", "COMPLETED", "FAILED", or
        "CANCELED".
        :param next_token: The token for the next set of results.
        :param max_results: The maximum number of results to return at one time.
        :returns: ListAuditTasksResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListAuthorizers")
    def list_authorizers(
        self,
        context: RequestContext,
        page_size: PageSize | None = None,
        marker: Marker | None = None,
        ascending_order: AscendingOrder | None = None,
        status: AuthorizerStatus | None = None,
        **kwargs,
    ) -> ListAuthorizersResponse:
        """Lists the authorizers registered in your account.

        Requires permission to access the
        `ListAuthorizers <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param page_size: The maximum number of results to return at one time.
        :param marker: A marker used to get the next set of results.
        :param ascending_order: Return the list of authorizers in ascending alphabetical order.
        :param status: The status of the list authorizers request.
        :returns: ListAuthorizersResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListBillingGroups")
    def list_billing_groups(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: RegistryMaxResults | None = None,
        name_prefix_filter: BillingGroupName | None = None,
        **kwargs,
    ) -> ListBillingGroupsResponse:
        """Lists the billing groups you have created.

        Requires permission to access the
        `ListBillingGroups <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return per request.
        :param name_prefix_filter: Limit the results to billing groups whose names have the given prefix.
        :returns: ListBillingGroupsResponse
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListCACertificates")
    def list_ca_certificates(
        self,
        context: RequestContext,
        page_size: PageSize | None = None,
        marker: Marker | None = None,
        ascending_order: AscendingOrder | None = None,
        template_name: TemplateName | None = None,
        **kwargs,
    ) -> ListCACertificatesResponse:
        """Lists the CA certificates registered for your Amazon Web Services
        account.

        The results are paginated with a default page size of 25. You can use
        the returned marker to retrieve additional results.

        Requires permission to access the
        `ListCACertificates <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param page_size: The result page size.
        :param marker: The marker for the next set of results.
        :param ascending_order: Determines the order of the results.
        :param template_name: The name of the provisioning template.
        :returns: ListCACertificatesResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListCertificateProviders")
    def list_certificate_providers(
        self,
        context: RequestContext,
        next_token: Marker | None = None,
        ascending_order: AscendingOrder | None = None,
        **kwargs,
    ) -> ListCertificateProvidersResponse:
        """Lists all your certificate providers in your Amazon Web Services
        account.

        Requires permission to access the
        `ListCertificateProviders <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param next_token: The token for the next set of results, or ``null`` if there are no more
        results.
        :param ascending_order: Returns the list of certificate providers in ascending alphabetical
        order.
        :returns: ListCertificateProvidersResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListCertificates")
    def list_certificates(
        self,
        context: RequestContext,
        page_size: PageSize | None = None,
        marker: Marker | None = None,
        ascending_order: AscendingOrder | None = None,
        **kwargs,
    ) -> ListCertificatesResponse:
        """Lists the certificates registered in your Amazon Web Services account.

        The results are paginated with a default page size of 25. You can use
        the returned marker to retrieve additional results.

        Requires permission to access the
        `ListCertificates <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param page_size: The result page size.
        :param marker: The marker for the next set of results.
        :param ascending_order: Specifies the order for results.
        :returns: ListCertificatesResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListCertificatesByCA")
    def list_certificates_by_ca(
        self,
        context: RequestContext,
        ca_certificate_id: CertificateId,
        page_size: PageSize | None = None,
        marker: Marker | None = None,
        ascending_order: AscendingOrder | None = None,
        **kwargs,
    ) -> ListCertificatesByCAResponse:
        """List the device certificates signed by the specified CA certificate.

        Requires permission to access the
        `ListCertificatesByCA <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param ca_certificate_id: The ID of the CA certificate.
        :param page_size: The result page size.
        :param marker: The marker for the next set of results.
        :param ascending_order: Specifies the order for results.
        :returns: ListCertificatesByCAResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListCommandExecutions")
    def list_command_executions(
        self,
        context: RequestContext,
        max_results: CommandMaxResults | None = None,
        next_token: NextToken | None = None,
        namespace: CommandNamespace | None = None,
        status: CommandExecutionStatus | None = None,
        sort_order: SortOrder | None = None,
        started_time_filter: TimeFilter | None = None,
        completed_time_filter: TimeFilter | None = None,
        target_arn: TargetArn | None = None,
        command_arn: CommandArn | None = None,
        **kwargs,
    ) -> ListCommandExecutionsResponse:
        """List all command executions.

        -  You must provide only the ``startedTimeFilter`` or the
           ``completedTimeFilter`` information. If you provide both time
           filters, the API will generate an error. You can use this information
           to retrieve a list of command executions within a specific timeframe.

        -  You must provide only the ``commandArn`` or the ``thingArn``
           information depending on whether you want to list executions for a
           specific command or an IoT thing. If you provide both fields, the API
           will generate an error.

        For more information about considerations for using this API, see `List
        command executions in your account
        (CLI) <https://docs.aws.amazon.com/iot/latest/developerguide/iot-remote-command-execution-start-monitor.html#iot-remote-command-execution-list-cli>`__.

        :param max_results: The maximum number of results to return in this operation.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise ``null`` to receive the first set of
        results.
        :param namespace: The namespace of the command.
        :param status: List all command executions for the device that have a particular
        status.
        :param sort_order: Specify whether to list the command executions that were created in the
        ascending or descending order.
        :param started_time_filter: List all command executions that started any time before or after the
        date and time that you specify.
        :param completed_time_filter: List all command executions that completed any time before or after the
        date and time that you specify.
        :param target_arn: The Amazon Resource Number (ARN) of the target device.
        :param command_arn: The Amazon Resource Number (ARN) of the command.
        :returns: ListCommandExecutionsResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("ListCommands")
    def list_commands(
        self,
        context: RequestContext,
        max_results: CommandMaxResults | None = None,
        next_token: NextToken | None = None,
        namespace: CommandNamespace | None = None,
        command_parameter_name: CommandParameterName | None = None,
        sort_order: SortOrder | None = None,
        **kwargs,
    ) -> ListCommandsResponse:
        """List all commands in your account.

        :param max_results: The maximum number of results to return in this operation.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise ``null`` to receive the first set of
        results.
        :param namespace: The namespace of the command.
        :param command_parameter_name: A filter that can be used to display the list of commands that have a
        specific command parameter name.
        :param sort_order: Specify whether to list the commands that you have created in the
        ascending or descending order.
        :returns: ListCommandsResponse
        :raises ValidationException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("ListCustomMetrics")
    def list_custom_metrics(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListCustomMetricsResponse:
        """Lists your Device Defender detect custom metrics.

        Requires permission to access the
        `ListCustomMetrics <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param next_token: The token for the next set of results.
        :param max_results: The maximum number of results to return at one time.
        :returns: ListCustomMetricsResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListDetectMitigationActionsExecutions")
    def list_detect_mitigation_actions_executions(
        self,
        context: RequestContext,
        task_id: MitigationActionsTaskId | None = None,
        violation_id: ViolationId | None = None,
        thing_name: DeviceDefenderThingName | None = None,
        start_time: Timestamp | None = None,
        end_time: Timestamp | None = None,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListDetectMitigationActionsExecutionsResponse:
        """Lists mitigation actions executions for a Device Defender ML Detect
        Security Profile.

        Requires permission to access the
        `ListDetectMitigationActionsExecutions <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param task_id: The unique identifier of the task.
        :param violation_id: The unique identifier of the violation.
        :param thing_name: The name of the thing whose mitigation actions are listed.
        :param start_time: A filter to limit results to those found after the specified time.
        :param end_time: The end of the time period for which ML Detect mitigation actions
        executions are returned.
        :param max_results: The maximum number of results to return at one time.
        :param next_token: The token for the next set of results.
        :returns: ListDetectMitigationActionsExecutionsResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListDetectMitigationActionsTasks")
    def list_detect_mitigation_actions_tasks(
        self,
        context: RequestContext,
        start_time: Timestamp,
        end_time: Timestamp,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListDetectMitigationActionsTasksResponse:
        """List of Device Defender ML Detect mitigation actions tasks.

        Requires permission to access the
        `ListDetectMitigationActionsTasks <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param start_time: A filter to limit results to those found after the specified time.
        :param end_time: The end of the time period for which ML Detect mitigation actions tasks
        are returned.
        :param max_results: The maximum number of results to return at one time.
        :param next_token: The token for the next set of results.
        :returns: ListDetectMitigationActionsTasksResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListDimensions")
    def list_dimensions(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListDimensionsResponse:
        """List the set of dimensions that are defined for your Amazon Web Services
        accounts.

        Requires permission to access the
        `ListDimensions <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param next_token: The token for the next set of results.
        :param max_results: The maximum number of results to retrieve at one time.
        :returns: ListDimensionsResponse
        :raises InternalFailureException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListDomainConfigurations")
    def list_domain_configurations(
        self,
        context: RequestContext,
        marker: Marker | None = None,
        page_size: PageSize | None = None,
        service_type: ServiceType | None = None,
        **kwargs,
    ) -> ListDomainConfigurationsResponse:
        """Gets a list of domain configurations for the user. This list is sorted
        alphabetically by domain configuration name.

        Requires permission to access the
        `ListDomainConfigurations <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param marker: The marker for the next set of results.
        :param page_size: The result page size.
        :param service_type: The type of service delivered by the endpoint.
        :returns: ListDomainConfigurationsResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListFleetMetrics")
    def list_fleet_metrics(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListFleetMetricsResponse:
        """Lists all your fleet metrics.

        Requires permission to access the
        `ListFleetMetrics <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise ``null`` to receive the first set of
        results.
        :param max_results: The maximum number of results to return in this operation.
        :returns: ListFleetMetricsResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListIndices")
    def list_indices(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: QueryMaxResults | None = None,
        **kwargs,
    ) -> ListIndicesResponse:
        """Lists the search indices.

        Requires permission to access the
        `ListIndices <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param next_token: The token used to get the next set of results, or ``null`` if there are
        no additional results.
        :param max_results: The maximum number of results to return at one time.
        :returns: ListIndicesResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListJobExecutionsForJob")
    def list_job_executions_for_job(
        self,
        context: RequestContext,
        job_id: JobId,
        status: JobExecutionStatus | None = None,
        max_results: LaserMaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListJobExecutionsForJobResponse:
        """Lists the job executions for a job.

        Requires permission to access the
        `ListJobExecutionsForJob <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param job_id: The unique identifier you assigned to this job when it was created.
        :param status: The status of the job.
        :param max_results: The maximum number of results to be returned per request.
        :param next_token: The token to retrieve the next set of results.
        :returns: ListJobExecutionsForJobResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListJobExecutionsForThing")
    def list_job_executions_for_thing(
        self,
        context: RequestContext,
        thing_name: ThingName,
        status: JobExecutionStatus | None = None,
        namespace_id: NamespaceId | None = None,
        max_results: LaserMaxResults | None = None,
        next_token: NextToken | None = None,
        job_id: JobId | None = None,
        **kwargs,
    ) -> ListJobExecutionsForThingResponse:
        """Lists the job executions for the specified thing.

        Requires permission to access the
        `ListJobExecutionsForThing <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_name: The thing name.
        :param status: An optional filter that lets you search for jobs that have the specified
        status.
        :param namespace_id: The namespace used to indicate that a job is a customer-managed job.
        :param max_results: The maximum number of results to be returned per request.
        :param next_token: The token to retrieve the next set of results.
        :param job_id: The unique identifier you assigned to this job when it was created.
        :returns: ListJobExecutionsForThingResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListJobTemplates")
    def list_job_templates(
        self,
        context: RequestContext,
        max_results: LaserMaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListJobTemplatesResponse:
        """Returns a list of job templates.

        Requires permission to access the
        `ListJobTemplates <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param max_results: The maximum number of results to return in the list.
        :param next_token: The token to use to return the next set of results in the list.
        :returns: ListJobTemplatesResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListJobs")
    def list_jobs(
        self,
        context: RequestContext,
        status: JobStatus | None = None,
        target_selection: TargetSelection | None = None,
        max_results: LaserMaxResults | None = None,
        next_token: NextToken | None = None,
        thing_group_name: ThingGroupName | None = None,
        thing_group_id: ThingGroupId | None = None,
        namespace_id: NamespaceId | None = None,
        **kwargs,
    ) -> ListJobsResponse:
        """Lists jobs.

        Requires permission to access the
        `ListJobs <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param status: An optional filter that lets you search for jobs that have the specified
        status.
        :param target_selection: Specifies whether the job will continue to run (CONTINUOUS), or will be
        complete after all those things specified as targets have completed the
        job (SNAPSHOT).
        :param max_results: The maximum number of results to return per request.
        :param next_token: The token to retrieve the next set of results.
        :param thing_group_name: A filter that limits the returned jobs to those for the specified group.
        :param thing_group_id: A filter that limits the returned jobs to those for the specified group.
        :param namespace_id: The namespace used to indicate that a job is a customer-managed job.
        :returns: ListJobsResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListManagedJobTemplates")
    def list_managed_job_templates(
        self,
        context: RequestContext,
        template_name: ManagedJobTemplateName | None = None,
        max_results: LaserMaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListManagedJobTemplatesResponse:
        """Returns a list of managed job templates.

        :param template_name: An optional parameter for template name.
        :param max_results: Maximum number of entries that can be returned.
        :param next_token: The token to retrieve the next set of results.
        :returns: ListManagedJobTemplatesResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("ListMetricValues")
    def list_metric_values(
        self,
        context: RequestContext,
        thing_name: DeviceDefenderThingName,
        metric_name: BehaviorMetric,
        start_time: Timestamp,
        end_time: Timestamp,
        dimension_name: DimensionName | None = None,
        dimension_value_operator: DimensionValueOperator | None = None,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListMetricValuesResponse:
        """Lists the values reported for an IoT Device Defender metric (device-side
        metric, cloud-side metric, or custom metric) by the given thing during
        the specified time period.

        :param thing_name: The name of the thing for which security profile metric values are
        returned.
        :param metric_name: The name of the security profile metric for which values are returned.
        :param start_time: The start of the time period for which metric values are returned.
        :param end_time: The end of the time period for which metric values are returned.
        :param dimension_name: The dimension name.
        :param dimension_value_operator: The dimension value operator.
        :param max_results: The maximum number of results to return at one time.
        :param next_token: The token for the next set of results.
        :returns: ListMetricValuesResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListMitigationActions")
    def list_mitigation_actions(
        self,
        context: RequestContext,
        action_type: MitigationActionType | None = None,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListMitigationActionsResponse:
        """Gets a list of all mitigation actions that match the specified filter
        criteria.

        Requires permission to access the
        `ListMitigationActions <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param action_type: Specify a value to limit the result to mitigation actions with a
        specific action type.
        :param max_results: The maximum number of results to return at one time.
        :param next_token: The token for the next set of results.
        :returns: ListMitigationActionsResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListOTAUpdates")
    def list_ota_updates(
        self,
        context: RequestContext,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        ota_update_status: OTAUpdateStatus | None = None,
        **kwargs,
    ) -> ListOTAUpdatesResponse:
        """Lists OTA updates.

        Requires permission to access the
        `ListOTAUpdates <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param max_results: The maximum number of results to return at one time.
        :param next_token: A token used to retrieve the next set of results.
        :param ota_update_status: The OTA update job status.
        :returns: ListOTAUpdatesResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListOutgoingCertificates")
    def list_outgoing_certificates(
        self,
        context: RequestContext,
        page_size: PageSize | None = None,
        marker: Marker | None = None,
        ascending_order: AscendingOrder | None = None,
        **kwargs,
    ) -> ListOutgoingCertificatesResponse:
        """Lists certificates that are being transferred but not yet accepted.

        Requires permission to access the
        `ListOutgoingCertificates <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param page_size: The result page size.
        :param marker: The marker for the next set of results.
        :param ascending_order: Specifies the order for results.
        :returns: ListOutgoingCertificatesResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListPackageVersions")
    def list_package_versions(
        self,
        context: RequestContext,
        package_name: PackageName,
        status: PackageVersionStatus | None = None,
        max_results: PackageCatalogMaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListPackageVersionsResponse:
        """Lists the software package versions associated to the account.

        Requires permission to access the
        `ListPackageVersions <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param package_name: The name of the target software package.
        :param status: The status of the package version.
        :param max_results: The maximum number of results to return at one time.
        :param next_token: The token for the next set of results.
        :returns: ListPackageVersionsResponse
        :raises ThrottlingException:
        :raises InternalServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("ListPackages")
    def list_packages(
        self,
        context: RequestContext,
        max_results: PackageCatalogMaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListPackagesResponse:
        """Lists the software packages associated to the account.

        Requires permission to access the
        `ListPackages <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param max_results: The maximum number of results returned at one time.
        :param next_token: The token for the next set of results.
        :returns: ListPackagesResponse
        :raises ThrottlingException:
        :raises InternalServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("ListPolicies")
    def list_policies(
        self,
        context: RequestContext,
        marker: Marker | None = None,
        page_size: PageSize | None = None,
        ascending_order: AscendingOrder | None = None,
        **kwargs,
    ) -> ListPoliciesResponse:
        """Lists your policies.

        Requires permission to access the
        `ListPolicies <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param marker: The marker for the next set of results.
        :param page_size: The result page size.
        :param ascending_order: Specifies the order for results.
        :returns: ListPoliciesResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListPolicyPrincipals")
    def list_policy_principals(
        self,
        context: RequestContext,
        policy_name: PolicyName,
        marker: Marker | None = None,
        page_size: PageSize | None = None,
        ascending_order: AscendingOrder | None = None,
        **kwargs,
    ) -> ListPolicyPrincipalsResponse:
        """Lists the principals associated with the specified policy.

        **Note:** This action is deprecated and works as expected for backward
        compatibility, but we won't add enhancements. Use ListTargetsForPolicy
        instead.

        Requires permission to access the
        `ListPolicyPrincipals <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param policy_name: The policy name.
        :param marker: The marker for the next set of results.
        :param page_size: The result page size.
        :param ascending_order: Specifies the order for results.
        :returns: ListPolicyPrincipalsResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListPolicyVersions")
    def list_policy_versions(
        self, context: RequestContext, policy_name: PolicyName, **kwargs
    ) -> ListPolicyVersionsResponse:
        """Lists the versions of the specified policy and identifies the default
        version.

        Requires permission to access the
        `ListPolicyVersions <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param policy_name: The policy name.
        :returns: ListPolicyVersionsResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListPrincipalPolicies")
    def list_principal_policies(
        self,
        context: RequestContext,
        principal: Principal,
        marker: Marker | None = None,
        page_size: PageSize | None = None,
        ascending_order: AscendingOrder | None = None,
        **kwargs,
    ) -> ListPrincipalPoliciesResponse:
        """Lists the policies attached to the specified principal. If you use an
        Cognito identity, the ID must be in `AmazonCognito Identity
        format <https://docs.aws.amazon.com/cognitoidentity/latest/APIReference/API_GetCredentialsForIdentity.html#API_GetCredentialsForIdentity_RequestSyntax>`__.

        **Note:** This action is deprecated and works as expected for backward
        compatibility, but we won't add enhancements. Use ListAttachedPolicies
        instead.

        Requires permission to access the
        `ListPrincipalPolicies <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param principal: The principal.
        :param marker: The marker for the next set of results.
        :param page_size: The result page size.
        :param ascending_order: Specifies the order for results.
        :returns: ListPrincipalPoliciesResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListPrincipalThings")
    def list_principal_things(
        self,
        context: RequestContext,
        principal: Principal,
        next_token: NextToken | None = None,
        max_results: RegistryMaxResults | None = None,
        **kwargs,
    ) -> ListPrincipalThingsResponse:
        """Lists the things associated with the specified principal. A principal
        can be X.509 certificates, IAM users, groups, and roles, Amazon Cognito
        identities or federated identities.

        Requires permission to access the
        `ListPrincipalThings <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param principal: The principal.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return in this operation.
        :returns: ListPrincipalThingsResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListPrincipalThingsV2")
    def list_principal_things_v2(
        self,
        context: RequestContext,
        principal: Principal,
        next_token: NextToken | None = None,
        max_results: RegistryMaxResults | None = None,
        thing_principal_type: ThingPrincipalType | None = None,
        **kwargs,
    ) -> ListPrincipalThingsV2Response:
        """Lists the things associated with the specified principal. A principal
        can be an X.509 certificate or an Amazon Cognito ID.

        Requires permission to access the
        `ListPrincipalThings <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param principal: The principal.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return in this operation.
        :param thing_principal_type: The type of the relation you want to filter in the response.
        :returns: ListPrincipalThingsV2Response
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListProvisioningTemplateVersions")
    def list_provisioning_template_versions(
        self,
        context: RequestContext,
        template_name: TemplateName,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListProvisioningTemplateVersionsResponse:
        """A list of provisioning template versions.

        Requires permission to access the
        `ListProvisioningTemplateVersions <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param template_name: The name of the provisioning template.
        :param max_results: The maximum number of results to return at one time.
        :param next_token: A token to retrieve the next set of results.
        :returns: ListProvisioningTemplateVersionsResponse
        :raises InternalFailureException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises ResourceNotFoundException:
        :raises UnauthorizedException:
        """
        raise NotImplementedError

    @handler("ListProvisioningTemplates")
    def list_provisioning_templates(
        self,
        context: RequestContext,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListProvisioningTemplatesResponse:
        """Lists the provisioning templates in your Amazon Web Services account.

        Requires permission to access the
        `ListProvisioningTemplates <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param max_results: The maximum number of results to return at one time.
        :param next_token: A token to retrieve the next set of results.
        :returns: ListProvisioningTemplatesResponse
        :raises InternalFailureException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        """
        raise NotImplementedError

    @handler("ListRelatedResourcesForAuditFinding")
    def list_related_resources_for_audit_finding(
        self,
        context: RequestContext,
        finding_id: FindingId,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListRelatedResourcesForAuditFindingResponse:
        """The related resources of an Audit finding. The following resources can
        be returned from calling this API:

        -  DEVICE_CERTIFICATE

        -  CA_CERTIFICATE

        -  IOT_POLICY

        -  COGNITO_IDENTITY_POOL

        -  CLIENT_ID

        -  ACCOUNT_SETTINGS

        -  ROLE_ALIAS

        -  IAM_ROLE

        -  ISSUER_CERTIFICATE

        This API is similar to DescribeAuditFinding's
        `RelatedResources <https://docs.aws.amazon.com/iot/latest/apireference/API_DescribeAuditFinding.html>`__
        but provides pagination and is not limited to 10 resources. When calling
        `DescribeAuditFinding <https://docs.aws.amazon.com/iot/latest/apireference/API_DescribeAuditFinding.html>`__
        for the intermediate CA revoked for active device certificates check,
        RelatedResources will not be populated. You must use this API,
        ListRelatedResourcesForAuditFinding, to list the certificates.

        :param finding_id: The finding Id.
        :param next_token: A token that can be used to retrieve the next set of results, or
        ``null`` if there are no additional results.
        :param max_results: The maximum number of results to return at one time.
        :returns: ListRelatedResourcesForAuditFindingResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListRoleAliases")
    def list_role_aliases(
        self,
        context: RequestContext,
        page_size: PageSize | None = None,
        marker: Marker | None = None,
        ascending_order: AscendingOrder | None = None,
        **kwargs,
    ) -> ListRoleAliasesResponse:
        """Lists the role aliases registered in your account.

        Requires permission to access the
        `ListRoleAliases <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param page_size: The maximum number of results to return at one time.
        :param marker: A marker used to get the next set of results.
        :param ascending_order: Return the list of role aliases in ascending alphabetical order.
        :returns: ListRoleAliasesResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListSbomValidationResults")
    def list_sbom_validation_results(
        self,
        context: RequestContext,
        package_name: PackageName,
        version_name: VersionName,
        validation_result: SbomValidationResult | None = None,
        max_results: PackageCatalogMaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListSbomValidationResultsResponse:
        """The validation results for all software bill of materials (SBOM)
        attached to a specific software package version.

        Requires permission to access the
        `ListSbomValidationResults <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param package_name: The name of the new software package.
        :param version_name: The name of the new package version.
        :param validation_result: The end result of the.
        :param max_results: The maximum number of results to return at one time.
        :param next_token: A token that can be used to retrieve the next set of results, or null if
        there are no additional results.
        :returns: ListSbomValidationResultsResponse
        :raises ThrottlingException:
        :raises InternalServerException:
        :raises ValidationException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListScheduledAudits")
    def list_scheduled_audits(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListScheduledAuditsResponse:
        """Lists all of your scheduled audits.

        Requires permission to access the
        `ListScheduledAudits <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param next_token: The token for the next set of results.
        :param max_results: The maximum number of results to return at one time.
        :returns: ListScheduledAuditsResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListSecurityProfiles")
    def list_security_profiles(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        dimension_name: DimensionName | None = None,
        metric_name: MetricName | None = None,
        **kwargs,
    ) -> ListSecurityProfilesResponse:
        """Lists the Device Defender security profiles you've created. You can
        filter security profiles by dimension or custom metric.

        Requires permission to access the
        `ListSecurityProfiles <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        ``dimensionName`` and ``metricName`` cannot be used in the same request.

        :param next_token: The token for the next set of results.
        :param max_results: The maximum number of results to return at one time.
        :param dimension_name: A filter to limit results to the security profiles that use the defined
        dimension.
        :param metric_name: The name of the custom metric.
        :returns: ListSecurityProfilesResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListSecurityProfilesForTarget")
    def list_security_profiles_for_target(
        self,
        context: RequestContext,
        security_profile_target_arn: SecurityProfileTargetArn,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        recursive: Recursive | None = None,
        **kwargs,
    ) -> ListSecurityProfilesForTargetResponse:
        """Lists the Device Defender security profiles attached to a target (thing
        group).

        Requires permission to access the
        `ListSecurityProfilesForTarget <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param security_profile_target_arn: The ARN of the target (thing group) whose attached security profiles you
        want to get.
        :param next_token: The token for the next set of results.
        :param max_results: The maximum number of results to return at one time.
        :param recursive: If true, return child groups too.
        :returns: ListSecurityProfilesForTargetResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListStreams")
    def list_streams(
        self,
        context: RequestContext,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        ascending_order: AscendingOrder | None = None,
        **kwargs,
    ) -> ListStreamsResponse:
        """Lists all of the streams in your Amazon Web Services account.

        Requires permission to access the
        `ListStreams <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param max_results: The maximum number of results to return at a time.
        :param next_token: A token used to get the next set of results.
        :param ascending_order: Set to true to return the list of streams in ascending order.
        :returns: ListStreamsResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListTagsForResource")
    def list_tags_for_resource(
        self,
        context: RequestContext,
        resource_arn: ResourceArn,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListTagsForResourceResponse:
        """Lists the tags (metadata) you have assigned to the resource.

        Requires permission to access the
        `ListTagsForResource <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param resource_arn: The ARN of the resource.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :returns: ListTagsForResourceResponse
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListTargetsForPolicy")
    def list_targets_for_policy(
        self,
        context: RequestContext,
        policy_name: PolicyName,
        marker: Marker | None = None,
        page_size: PageSize | None = None,
        **kwargs,
    ) -> ListTargetsForPolicyResponse:
        """List targets for the specified policy.

        Requires permission to access the
        `ListTargetsForPolicy <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param policy_name: The policy name.
        :param marker: A marker used to get the next set of results.
        :param page_size: The maximum number of results to return at one time.
        :returns: ListTargetsForPolicyResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("ListTargetsForSecurityProfile")
    def list_targets_for_security_profile(
        self,
        context: RequestContext,
        security_profile_name: SecurityProfileName,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListTargetsForSecurityProfileResponse:
        """Lists the targets (thing groups) associated with a given Device Defender
        security profile.

        Requires permission to access the
        `ListTargetsForSecurityProfile <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param security_profile_name: The security profile.
        :param next_token: The token for the next set of results.
        :param max_results: The maximum number of results to return at one time.
        :returns: ListTargetsForSecurityProfileResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListThingGroups")
    def list_thing_groups(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: RegistryMaxResults | None = None,
        parent_group: ThingGroupName | None = None,
        name_prefix_filter: ThingGroupName | None = None,
        recursive: RecursiveWithoutDefault | None = None,
        **kwargs,
    ) -> ListThingGroupsResponse:
        """List the thing groups in your account.

        Requires permission to access the
        `ListThingGroups <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return at one time.
        :param parent_group: A filter that limits the results to those with the specified parent
        group.
        :param name_prefix_filter: A filter that limits the results to those with the specified name
        prefix.
        :param recursive: If true, return child groups as well.
        :returns: ListThingGroupsResponse
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListThingGroupsForThing")
    def list_thing_groups_for_thing(
        self,
        context: RequestContext,
        thing_name: ThingName,
        next_token: NextToken | None = None,
        max_results: RegistryMaxResults | None = None,
        **kwargs,
    ) -> ListThingGroupsForThingResponse:
        """List the thing groups to which the specified thing belongs.

        Requires permission to access the
        `ListThingGroupsForThing <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_name: The thing name.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return at one time.
        :returns: ListThingGroupsForThingResponse
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListThingPrincipals")
    def list_thing_principals(
        self,
        context: RequestContext,
        thing_name: ThingName,
        next_token: NextToken | None = None,
        max_results: RegistryMaxResults | None = None,
        **kwargs,
    ) -> ListThingPrincipalsResponse:
        """Lists the principals associated with the specified thing. A principal
        can be X.509 certificates, IAM users, groups, and roles, Amazon Cognito
        identities or federated identities.

        Requires permission to access the
        `ListThingPrincipals <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_name: The name of the thing.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return in this operation.
        :returns: ListThingPrincipalsResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListThingPrincipalsV2")
    def list_thing_principals_v2(
        self,
        context: RequestContext,
        thing_name: ThingName,
        next_token: NextToken | None = None,
        max_results: RegistryMaxResults | None = None,
        thing_principal_type: ThingPrincipalType | None = None,
        **kwargs,
    ) -> ListThingPrincipalsV2Response:
        """Lists the principals associated with the specified thing. A principal
        can be an X.509 certificate or an Amazon Cognito ID.

        Requires permission to access the
        `ListThingPrincipals <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_name: The name of the thing.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return in this operation.
        :param thing_principal_type: The type of the relation you want to filter in the response.
        :returns: ListThingPrincipalsV2Response
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListThingRegistrationTaskReports")
    def list_thing_registration_task_reports(
        self,
        context: RequestContext,
        task_id: TaskId,
        report_type: ReportType,
        next_token: NextToken | None = None,
        max_results: RegistryMaxResults | None = None,
        **kwargs,
    ) -> ListThingRegistrationTaskReportsResponse:
        """Information about the thing registration tasks.

        :param task_id: The id of the task.
        :param report_type: The type of task report.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return per request.
        :returns: ListThingRegistrationTaskReportsResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListThingRegistrationTasks")
    def list_thing_registration_tasks(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: RegistryMaxResults | None = None,
        status: Status | None = None,
        **kwargs,
    ) -> ListThingRegistrationTasksResponse:
        """List bulk thing provisioning tasks.

        Requires permission to access the
        `ListThingRegistrationTasks <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return at one time.
        :param status: The status of the bulk thing provisioning task.
        :returns: ListThingRegistrationTasksResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListThingTypes")
    def list_thing_types(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: RegistryMaxResults | None = None,
        thing_type_name: ThingTypeName | None = None,
        **kwargs,
    ) -> ListThingTypesResponse:
        """Lists the existing thing types.

        Requires permission to access the
        `ListThingTypes <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return in this operation.
        :param thing_type_name: The name of the thing type.
        :returns: ListThingTypesResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListThings")
    def list_things(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: RegistryMaxResults | None = None,
        attribute_name: AttributeName | None = None,
        attribute_value: AttributeValue | None = None,
        thing_type_name: ThingTypeName | None = None,
        use_prefix_attribute_value: usePrefixAttributeValue | None = None,
        **kwargs,
    ) -> ListThingsResponse:
        """Lists your things. Use the **attributeName** and **attributeValue**
        parameters to filter your things. For example, calling ``ListThings``
        with attributeName=Color and attributeValue=Red retrieves all things in
        the registry that contain an attribute **Color** with the value **Red**.
        For more information, see `List
        Things <https://docs.aws.amazon.com/iot/latest/developerguide/thing-registry.html#list-things>`__
        from the *Amazon Web Services IoT Core Developer Guide*.

        Requires permission to access the
        `ListThings <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        You will not be charged for calling this API if an ``Access denied``
        error is returned. You will also not be charged if no attributes or
        pagination token was provided in request and no pagination token and no
        results were returned.

        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return in this operation.
        :param attribute_name: The attribute name used to search for things.
        :param attribute_value: The attribute value used to search for things.
        :param thing_type_name: The name of the thing type used to search for things.
        :param use_prefix_attribute_value: When ``true``, the action returns the thing resources with attribute
        values that start with the ``attributeValue`` provided.
        :returns: ListThingsResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("ListThingsInBillingGroup")
    def list_things_in_billing_group(
        self,
        context: RequestContext,
        billing_group_name: BillingGroupName,
        next_token: NextToken | None = None,
        max_results: RegistryMaxResults | None = None,
        **kwargs,
    ) -> ListThingsInBillingGroupResponse:
        """Lists the things you have added to the given billing group.

        Requires permission to access the
        `ListThingsInBillingGroup <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param billing_group_name: The name of the billing group.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return per request.
        :returns: ListThingsInBillingGroupResponse
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListThingsInThingGroup")
    def list_things_in_thing_group(
        self,
        context: RequestContext,
        thing_group_name: ThingGroupName,
        recursive: Recursive | None = None,
        next_token: NextToken | None = None,
        max_results: RegistryMaxResults | None = None,
        **kwargs,
    ) -> ListThingsInThingGroupResponse:
        """Lists the things in the specified group.

        Requires permission to access the
        `ListThingsInThingGroup <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_group_name: The thing group name.
        :param recursive: When true, list things in this thing group and in all child groups as
        well.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return at one time.
        :returns: ListThingsInThingGroupResponse
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListTopicRuleDestinations")
    def list_topic_rule_destinations(
        self,
        context: RequestContext,
        max_results: TopicRuleDestinationMaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListTopicRuleDestinationsResponse:
        """Lists all the topic rule destinations in your Amazon Web Services
        account.

        Requires permission to access the
        `ListTopicRuleDestinations <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param max_results: The maximum number of results to return at one time.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :returns: ListTopicRuleDestinationsResponse
        :raises InternalException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        :raises UnauthorizedException:
        """
        raise NotImplementedError

    @handler("ListTopicRules")
    def list_topic_rules(
        self,
        context: RequestContext,
        topic: Topic | None = None,
        max_results: TopicRuleMaxResults | None = None,
        next_token: NextToken | None = None,
        rule_disabled: IsDisabled | None = None,
        **kwargs,
    ) -> ListTopicRulesResponse:
        """Lists the rules for the specific topic.

        Requires permission to access the
        `ListTopicRules <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param topic: The topic.
        :param max_results: The maximum number of results to return.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param rule_disabled: Specifies whether the rule is disabled.
        :returns: ListTopicRulesResponse
        :raises InternalException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        :raises UnauthorizedException:
        """
        raise NotImplementedError

    @handler("ListV2LoggingLevels")
    def list_v2_logging_levels(
        self,
        context: RequestContext,
        target_type: LogTargetType | None = None,
        next_token: NextToken | None = None,
        max_results: SkyfallMaxResults | None = None,
        **kwargs,
    ) -> ListV2LoggingLevelsResponse:
        """Lists logging levels.

        Requires permission to access the
        `ListV2LoggingLevels <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param target_type: The type of resource for which you are configuring logging.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return at one time.
        :returns: ListV2LoggingLevelsResponse
        :raises InternalException:
        :raises NotConfiguredException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListViolationEvents")
    def list_violation_events(
        self,
        context: RequestContext,
        start_time: Timestamp,
        end_time: Timestamp,
        thing_name: DeviceDefenderThingName | None = None,
        security_profile_name: SecurityProfileName | None = None,
        behavior_criteria_type: BehaviorCriteriaType | None = None,
        list_suppressed_alerts: ListSuppressedAlerts | None = None,
        verification_state: VerificationState | None = None,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListViolationEventsResponse:
        """Lists the Device Defender security profile violations discovered during
        the given time period. You can use filters to limit the results to those
        alerts issued for a particular security profile, behavior, or thing
        (device).

        Requires permission to access the
        `ListViolationEvents <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param start_time: The start time for the alerts to be listed.
        :param end_time: The end time for the alerts to be listed.
        :param thing_name: A filter to limit results to those alerts caused by the specified thing.
        :param security_profile_name: A filter to limit results to those alerts generated by the specified
        security profile.
        :param behavior_criteria_type: The criteria for a behavior.
        :param list_suppressed_alerts: A list of all suppressed alerts.
        :param verification_state: The verification state of the violation (detect alarm).
        :param next_token: The token for the next set of results.
        :param max_results: The maximum number of results to return at one time.
        :returns: ListViolationEventsResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("PutVerificationStateOnViolation")
    def put_verification_state_on_violation(
        self,
        context: RequestContext,
        violation_id: ViolationId,
        verification_state: VerificationState,
        verification_state_description: VerificationStateDescription | None = None,
        **kwargs,
    ) -> PutVerificationStateOnViolationResponse:
        """Set a verification state and provide a description of that verification
        state on a violation (detect alarm).

        :param violation_id: The violation ID.
        :param verification_state: The verification state of the violation.
        :param verification_state_description: The description of the verification state of the violation (detect
        alarm).
        :returns: PutVerificationStateOnViolationResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("RegisterCACertificate")
    def register_ca_certificate(
        self,
        context: RequestContext,
        ca_certificate: CertificatePem,
        verification_certificate: CertificatePem | None = None,
        set_as_active: SetAsActive | None = None,
        allow_auto_registration: AllowAutoRegistration | None = None,
        registration_config: RegistrationConfig | None = None,
        tags: TagList | None = None,
        certificate_mode: CertificateMode | None = None,
        **kwargs,
    ) -> RegisterCACertificateResponse:
        """Registers a CA certificate with Amazon Web Services IoT Core. There is
        no limit to the number of CA certificates you can register in your
        Amazon Web Services account. You can register up to 10 CA certificates
        with the same ``CA subject field`` per Amazon Web Services account.

        Requires permission to access the
        `RegisterCACertificate <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param ca_certificate: The CA certificate.
        :param verification_certificate: The private key verification certificate.
        :param set_as_active: A boolean value that specifies if the CA certificate is set to active.
        :param allow_auto_registration: Allows this CA certificate to be used for auto registration of device
        certificates.
        :param registration_config: Information about the registration configuration.
        :param tags: Metadata which can be used to manage the CA certificate.
        :param certificate_mode: Describes the certificate mode in which the Certificate Authority (CA)
        will be registered.
        :returns: RegisterCACertificateResponse
        :raises ResourceNotFoundException:
        :raises ResourceAlreadyExistsException:
        :raises RegistrationCodeValidationException:
        :raises InvalidRequestException:
        :raises CertificateValidationException:
        :raises ThrottlingException:
        :raises LimitExceededException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("RegisterCertificate")
    def register_certificate(
        self,
        context: RequestContext,
        certificate_pem: CertificatePem,
        ca_certificate_pem: CertificatePem | None = None,
        set_as_active: SetAsActiveFlag | None = None,
        status: CertificateStatus | None = None,
        **kwargs,
    ) -> RegisterCertificateResponse:
        """Registers a device certificate with IoT in the same `certificate
        mode <https://docs.aws.amazon.com/iot/latest/apireference/API_CertificateDescription.html#iot-Type-CertificateDescription-certificateMode>`__
        as the signing CA. If you have more than one CA certificate that has the
        same subject field, you must specify the CA certificate that was used to
        sign the device certificate being registered.

        Requires permission to access the
        `RegisterCertificate <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param certificate_pem: The certificate data, in PEM format.
        :param ca_certificate_pem: The CA certificate used to sign the device certificate being registered.
        :param set_as_active: A boolean value that specifies if the certificate is set to active.
        :param status: The status of the register certificate request.
        :returns: RegisterCertificateResponse
        :raises ResourceAlreadyExistsException:
        :raises InvalidRequestException:
        :raises CertificateValidationException:
        :raises CertificateStateException:
        :raises CertificateConflictException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("RegisterCertificateWithoutCA")
    def register_certificate_without_ca(
        self,
        context: RequestContext,
        certificate_pem: CertificatePem,
        status: CertificateStatus | None = None,
        **kwargs,
    ) -> RegisterCertificateWithoutCAResponse:
        """Register a certificate that does not have a certificate authority (CA).
        For supported certificates, consult `Certificate signing algorithms
        supported by
        IoT <https://docs.aws.amazon.com/iot/latest/developerguide/x509-client-certs.html#x509-cert-algorithms>`__.

        :param certificate_pem: The certificate data, in PEM format.
        :param status: The status of the register certificate request.
        :returns: RegisterCertificateWithoutCAResponse
        :raises ResourceAlreadyExistsException:
        :raises InvalidRequestException:
        :raises CertificateStateException:
        :raises CertificateValidationException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("RegisterThing")
    def register_thing(
        self,
        context: RequestContext,
        template_body: TemplateBody,
        parameters: Parameters | None = None,
        **kwargs,
    ) -> RegisterThingResponse:
        """Provisions a thing in the device registry. RegisterThing calls other IoT
        control plane APIs. These calls might exceed your account level `IoT
        Throttling
        Limits <https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html#limits_iot>`__
        and cause throttle errors. Please contact `Amazon Web Services Customer
        Support <https://console.aws.amazon.com/support/home>`__ to raise your
        throttling limits if necessary.

        Requires permission to access the
        `RegisterThing <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param template_body: The provisioning template.
        :param parameters: The parameters for provisioning a thing.
        :returns: RegisterThingResponse
        :raises InternalFailureException:
        :raises ServiceUnavailableException:
        :raises InvalidRequestException:
        :raises UnauthorizedException:
        :raises ThrottlingException:
        :raises ConflictingResourceUpdateException:
        :raises ResourceRegistrationFailureException:
        """
        raise NotImplementedError

    @handler("RejectCertificateTransfer")
    def reject_certificate_transfer(
        self,
        context: RequestContext,
        certificate_id: CertificateId,
        reject_reason: Message | None = None,
        **kwargs,
    ) -> None:
        """Rejects a pending certificate transfer. After IoT rejects a certificate
        transfer, the certificate status changes from **PENDING_TRANSFER** to
        **INACTIVE**.

        To check for pending certificate transfers, call ListCertificates to
        enumerate your certificates.

        This operation can only be called by the transfer destination. After it
        is called, the certificate will be returned to the source's account in
        the INACTIVE state.

        Requires permission to access the
        `RejectCertificateTransfer <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param certificate_id: The ID of the certificate.
        :param reject_reason: The reason the certificate transfer was rejected.
        :raises ResourceNotFoundException:
        :raises TransferAlreadyCompletedException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("RemoveThingFromBillingGroup")
    def remove_thing_from_billing_group(
        self,
        context: RequestContext,
        billing_group_name: BillingGroupName | None = None,
        billing_group_arn: BillingGroupArn | None = None,
        thing_name: ThingName | None = None,
        thing_arn: ThingArn | None = None,
        **kwargs,
    ) -> RemoveThingFromBillingGroupResponse:
        """Removes the given thing from the billing group.

        Requires permission to access the
        `RemoveThingFromBillingGroup <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        This call is asynchronous. It might take several seconds for the
        detachment to propagate.

        :param billing_group_name: The name of the billing group.
        :param billing_group_arn: The ARN of the billing group.
        :param thing_name: The name of the thing to be removed from the billing group.
        :param thing_arn: The ARN of the thing to be removed from the billing group.
        :returns: RemoveThingFromBillingGroupResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("RemoveThingFromThingGroup")
    def remove_thing_from_thing_group(
        self,
        context: RequestContext,
        thing_group_name: ThingGroupName | None = None,
        thing_group_arn: ThingGroupArn | None = None,
        thing_name: ThingName | None = None,
        thing_arn: ThingArn | None = None,
        **kwargs,
    ) -> RemoveThingFromThingGroupResponse:
        """Remove the specified thing from the specified group.

        You must specify either a ``thingGroupArn`` or a ``thingGroupName`` to
        identify the thing group and either a ``thingArn`` or a ``thingName`` to
        identify the thing to remove from the thing group.

        Requires permission to access the
        `RemoveThingFromThingGroup <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_group_name: The group name.
        :param thing_group_arn: The group ARN.
        :param thing_name: The name of the thing to remove from the group.
        :param thing_arn: The ARN of the thing to remove from the group.
        :returns: RemoveThingFromThingGroupResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ReplaceTopicRule")
    def replace_topic_rule(
        self,
        context: RequestContext,
        rule_name: RuleName,
        topic_rule_payload: TopicRulePayload,
        **kwargs,
    ) -> None:
        """Replaces the rule. You must specify all parameters for the new rule.
        Creating rules is an administrator-level action. Any user who has
        permission to create rules will be able to access data processed by the
        rule.

        Requires permission to access the
        `ReplaceTopicRule <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param rule_name: The name of the rule.
        :param topic_rule_payload: The rule payload.
        :raises SqlParseException:
        :raises InternalException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        :raises UnauthorizedException:
        :raises ConflictingResourceUpdateException:
        """
        raise NotImplementedError

    @handler("SearchIndex")
    def search_index(
        self,
        context: RequestContext,
        query_string: QueryString,
        index_name: IndexName | None = None,
        next_token: NextToken | None = None,
        max_results: SearchQueryMaxResults | None = None,
        query_version: QueryVersion | None = None,
        **kwargs,
    ) -> SearchIndexResponse:
        """The query search index.

        Requires permission to access the
        `SearchIndex <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param query_string: The search query string.
        :param index_name: The search index name.
        :param next_token: The token used to get the next set of results, or ``null`` if there are
        no additional results.
        :param max_results: The maximum number of results to return per page at one time.
        :param query_version: The query version.
        :returns: SearchIndexResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        :raises InvalidQueryException:
        :raises IndexNotReadyException:
        """
        raise NotImplementedError

    @handler("SetDefaultAuthorizer")
    def set_default_authorizer(
        self, context: RequestContext, authorizer_name: AuthorizerName, **kwargs
    ) -> SetDefaultAuthorizerResponse:
        """Sets the default authorizer. This will be used if a websocket connection
        is made without specifying an authorizer.

        Requires permission to access the
        `SetDefaultAuthorizer <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param authorizer_name: The authorizer name.
        :returns: SetDefaultAuthorizerResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceAlreadyExistsException:
        """
        raise NotImplementedError

    @handler("SetDefaultPolicyVersion")
    def set_default_policy_version(
        self,
        context: RequestContext,
        policy_name: PolicyName,
        policy_version_id: PolicyVersionId,
        **kwargs,
    ) -> None:
        """Sets the specified version of the specified policy as the policy's
        default (operative) version. This action affects all certificates to
        which the policy is attached. To list the principals the policy is
        attached to, use the ListPrincipalPolicies action.

        Requires permission to access the
        `SetDefaultPolicyVersion <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param policy_name: The policy name.
        :param policy_version_id: The policy version ID.
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("SetLoggingOptions")
    def set_logging_options(
        self, context: RequestContext, logging_options_payload: LoggingOptionsPayload, **kwargs
    ) -> None:
        """Sets the logging options.

        NOTE: use of this command is not recommended. Use
        ``SetV2LoggingOptions`` instead.

        Requires permission to access the
        `SetLoggingOptions <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param logging_options_payload: The logging options payload.
        :raises InternalException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("SetV2LoggingLevel")
    def set_v2_logging_level(
        self, context: RequestContext, log_target: LogTarget, log_level: LogLevel, **kwargs
    ) -> None:
        """Sets the logging level.

        Requires permission to access the
        `SetV2LoggingLevel <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param log_target: The log target.
        :param log_level: The log level.
        :raises InternalException:
        :raises NotConfiguredException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("SetV2LoggingOptions")
    def set_v2_logging_options(
        self,
        context: RequestContext,
        role_arn: AwsArn | None = None,
        default_log_level: LogLevel | None = None,
        disable_all_logs: DisableAllLogs | None = None,
        **kwargs,
    ) -> None:
        """Sets the logging options for the V2 logging service.

        Requires permission to access the
        `SetV2LoggingOptions <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param role_arn: The ARN of the role that allows IoT to write to Cloudwatch logs.
        :param default_log_level: The default logging level.
        :param disable_all_logs: If true all logs are disabled.
        :raises InternalException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("StartAuditMitigationActionsTask")
    def start_audit_mitigation_actions_task(
        self,
        context: RequestContext,
        task_id: MitigationActionsTaskId,
        target: AuditMitigationActionsTaskTarget,
        audit_check_to_actions_mapping: AuditCheckToActionsMapping,
        client_request_token: ClientRequestToken,
        **kwargs,
    ) -> StartAuditMitigationActionsTaskResponse:
        """Starts a task that applies a set of mitigation actions to the specified
        target.

        Requires permission to access the
        `StartAuditMitigationActionsTask <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param task_id: A unique identifier for the task.
        :param target: Specifies the audit findings to which the mitigation actions are
        applied.
        :param audit_check_to_actions_mapping: For an audit check, specifies which mitigation actions to apply.
        :param client_request_token: Each audit mitigation task must have a unique client request token.
        :returns: StartAuditMitigationActionsTaskResponse
        :raises InvalidRequestException:
        :raises TaskAlreadyExistsException:
        :raises LimitExceededException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("StartDetectMitigationActionsTask")
    def start_detect_mitigation_actions_task(
        self,
        context: RequestContext,
        task_id: MitigationActionsTaskId,
        target: DetectMitigationActionsTaskTarget,
        actions: DetectMitigationActionsToExecuteList,
        client_request_token: ClientRequestToken,
        violation_event_occurrence_range: ViolationEventOccurrenceRange | None = None,
        include_only_active_violations: NullableBoolean | None = None,
        include_suppressed_alerts: NullableBoolean | None = None,
        **kwargs,
    ) -> StartDetectMitigationActionsTaskResponse:
        """Starts a Device Defender ML Detect mitigation actions task.

        Requires permission to access the
        `StartDetectMitigationActionsTask <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param task_id: The unique identifier of the task.
        :param target: Specifies the ML Detect findings to which the mitigation actions are
        applied.
        :param actions: The actions to be performed when a device has unexpected behavior.
        :param client_request_token: Each mitigation action task must have a unique client request token.
        :param violation_event_occurrence_range: Specifies the time period of which violation events occurred between.
        :param include_only_active_violations: Specifies to list only active violations.
        :param include_suppressed_alerts: Specifies to include suppressed alerts.
        :returns: StartDetectMitigationActionsTaskResponse
        :raises InvalidRequestException:
        :raises TaskAlreadyExistsException:
        :raises LimitExceededException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("StartOnDemandAuditTask")
    def start_on_demand_audit_task(
        self, context: RequestContext, target_check_names: TargetAuditCheckNames, **kwargs
    ) -> StartOnDemandAuditTaskResponse:
        """Starts an on-demand Device Defender audit.

        Requires permission to access the
        `StartOnDemandAuditTask <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param target_check_names: Which checks are performed during the audit.
        :returns: StartOnDemandAuditTaskResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("StartThingRegistrationTask")
    def start_thing_registration_task(
        self,
        context: RequestContext,
        template_body: TemplateBody,
        input_file_bucket: RegistryS3BucketName,
        input_file_key: RegistryS3KeyName,
        role_arn: RoleArn,
        **kwargs,
    ) -> StartThingRegistrationTaskResponse:
        """Creates a bulk thing provisioning task.

        Requires permission to access the
        `StartThingRegistrationTask <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param template_body: The provisioning template.
        :param input_file_bucket: The S3 bucket that contains the input file.
        :param input_file_key: The name of input file within the S3 bucket.
        :param role_arn: The IAM role ARN that grants permission the input file.
        :returns: StartThingRegistrationTaskResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("StopThingRegistrationTask")
    def stop_thing_registration_task(
        self, context: RequestContext, task_id: TaskId, **kwargs
    ) -> StopThingRegistrationTaskResponse:
        """Cancels a bulk thing provisioning task.

        Requires permission to access the
        `StopThingRegistrationTask <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param task_id: The bulk thing provisioning task ID.
        :returns: StopThingRegistrationTaskResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("TagResource")
    def tag_resource(
        self, context: RequestContext, resource_arn: ResourceArn, tags: TagList, **kwargs
    ) -> TagResourceResponse:
        """Adds to or modifies the tags of the given resource. Tags are metadata
        which can be used to manage a resource.

        Requires permission to access the
        `TagResource <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param resource_arn: The ARN of the resource.
        :param tags: The new or modified tags for the resource.
        :returns: TagResourceResponse
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("TestAuthorization")
    def test_authorization(
        self,
        context: RequestContext,
        auth_infos: AuthInfos,
        principal: Principal | None = None,
        cognito_identity_pool_id: CognitoIdentityPoolId | None = None,
        client_id: ClientId | None = None,
        policy_names_to_add: PolicyNames | None = None,
        policy_names_to_skip: PolicyNames | None = None,
        **kwargs,
    ) -> TestAuthorizationResponse:
        """Tests if a specified principal is authorized to perform an IoT action on
        a specified resource. Use this to test and debug the authorization
        behavior of devices that connect to the IoT device gateway.

        Requires permission to access the
        `TestAuthorization <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param auth_infos: A list of authorization info objects.
        :param principal: The principal.
        :param cognito_identity_pool_id: The Cognito identity pool ID.
        :param client_id: The MQTT client ID.
        :param policy_names_to_add: When testing custom authorization, the policies specified here are
        treated as if they are attached to the principal being authorized.
        :param policy_names_to_skip: When testing custom authorization, the policies specified here are
        treated as if they are not attached to the principal being authorized.
        :returns: TestAuthorizationResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("TestInvokeAuthorizer")
    def test_invoke_authorizer(
        self,
        context: RequestContext,
        authorizer_name: AuthorizerName,
        token: Token | None = None,
        token_signature: TokenSignature | None = None,
        http_context: HttpContext | None = None,
        mqtt_context: MqttContext | None = None,
        tls_context: TlsContext | None = None,
        **kwargs,
    ) -> TestInvokeAuthorizerResponse:
        """Tests a custom authorization behavior by invoking a specified custom
        authorizer. Use this to test and debug the custom authorization behavior
        of devices that connect to the IoT device gateway.

        Requires permission to access the
        `TestInvokeAuthorizer <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param authorizer_name: The custom authorizer name.
        :param token: The token returned by your custom authentication service.
        :param token_signature: The signature made with the token and your custom authentication
        service's private key.
        :param http_context: Specifies a test HTTP authorization request.
        :param mqtt_context: Specifies a test MQTT authorization request.
        :param tls_context: Specifies a test TLS authorization request.
        :returns: TestInvokeAuthorizerResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises InvalidResponseException:
        """
        raise NotImplementedError

    @handler("TransferCertificate")
    def transfer_certificate(
        self,
        context: RequestContext,
        certificate_id: CertificateId,
        target_aws_account: AwsAccountId,
        transfer_message: Message | None = None,
        **kwargs,
    ) -> TransferCertificateResponse:
        """Transfers the specified certificate to the specified Amazon Web Services
        account.

        Requires permission to access the
        `TransferCertificate <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        You can cancel the transfer until it is acknowledged by the recipient.

        No notification is sent to the transfer destination's account. It's up
        to the caller to notify the transfer target.

        The certificate being transferred must not be in the ``ACTIVE`` state.
        You can use the UpdateCertificate action to deactivate it.

        The certificate must not have any policies attached to it. You can use
        the DetachPolicy action to detach them.

        **Customer managed key behavior:** When you use a customer managed key
        to secure your data and then transfer the key to a customer in a
        different account using the TransferCertificate operation, the
        certificates will no longer be protected by their customer managed key
        configuration. During the transfer process, certificates are encrypted
        using IoT owned keys.

        While a certificate is in the **PENDING_TRANSFER** state, it's always
        protected by IoT owned keys, regardless of the customer managed key
        configuration of either the source or destination account.

        Once the transfer is completed through AcceptCertificateTransfer,
        RejectCertificateTransfer, or CancelCertificateTransfer, the certificate
        will be protected by the customer managed key configuration of the
        account that owns the certificate after the transfer operation:

        -  If the transfer is accepted: The certificate is protected by the
           destination account's customer managed key configuration.

        -  If the transfer is rejected or cancelled: The certificate is
           protected by the source account's customer managed key configuration.

        :param certificate_id: The ID of the certificate.
        :param target_aws_account: The Amazon Web Services account.
        :param transfer_message: The transfer message.
        :returns: TransferCertificateResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises CertificateStateException:
        :raises TransferConflictException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("UntagResource")
    def untag_resource(
        self, context: RequestContext, resource_arn: ResourceArn, tag_keys: TagKeyList, **kwargs
    ) -> UntagResourceResponse:
        """Removes the given tags (metadata) from the resource.

        Requires permission to access the
        `UntagResource <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param resource_arn: The ARN of the resource.
        :param tag_keys: A list of the keys of the tags to be removed from the resource.
        :returns: UntagResourceResponse
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("UpdateAccountAuditConfiguration")
    def update_account_audit_configuration(
        self,
        context: RequestContext,
        role_arn: RoleArn | None = None,
        audit_notification_target_configurations: AuditNotificationTargetConfigurations
        | None = None,
        audit_check_configurations: AuditCheckConfigurations | None = None,
        **kwargs,
    ) -> UpdateAccountAuditConfigurationResponse:
        """Configures or reconfigures the Device Defender audit settings for this
        account. Settings include how audit notifications are sent and which
        audit checks are enabled or disabled.

        Requires permission to access the
        `UpdateAccountAuditConfiguration <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param role_arn: The Amazon Resource Name (ARN) of the role that grants permission to IoT
        to access information about your devices, policies, certificates, and
        other items as required when performing an audit.
        :param audit_notification_target_configurations: Information about the targets to which audit notifications are sent.
        :param audit_check_configurations: Specifies which audit checks are enabled and disabled for this account.
        :returns: UpdateAccountAuditConfigurationResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("UpdateAuditSuppression")
    def update_audit_suppression(
        self,
        context: RequestContext,
        check_name: AuditCheckName,
        resource_identifier: ResourceIdentifier,
        expiration_date: Timestamp | None = None,
        suppress_indefinitely: SuppressIndefinitely | None = None,
        description: AuditDescription | None = None,
        **kwargs,
    ) -> UpdateAuditSuppressionResponse:
        """Updates a Device Defender audit suppression.

        :param check_name: An audit check name.
        :param resource_identifier: Information that identifies the noncompliant resource.
        :param expiration_date: The expiration date (epoch timestamp in seconds) that you want the
        suppression to adhere to.
        :param suppress_indefinitely: Indicates whether a suppression should exist indefinitely or not.
        :param description: The description of the audit suppression.
        :returns: UpdateAuditSuppressionResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("UpdateAuthorizer")
    def update_authorizer(
        self,
        context: RequestContext,
        authorizer_name: AuthorizerName,
        authorizer_function_arn: AuthorizerFunctionArn | None = None,
        token_key_name: TokenKeyName | None = None,
        token_signing_public_keys: PublicKeyMap | None = None,
        status: AuthorizerStatus | None = None,
        enable_caching_for_http: EnableCachingForHttp | None = None,
        **kwargs,
    ) -> UpdateAuthorizerResponse:
        """Updates an authorizer.

        Requires permission to access the
        `UpdateAuthorizer <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param authorizer_name: The authorizer name.
        :param authorizer_function_arn: The ARN of the authorizer's Lambda function.
        :param token_key_name: The key used to extract the token from the HTTP headers.
        :param token_signing_public_keys: The public keys used to verify the token signature.
        :param status: The status of the update authorizer request.
        :param enable_caching_for_http: When ``true``, the result from the authorizer’s Lambda function is
        cached for the time specified in ``refreshAfterInSeconds``.
        :returns: UpdateAuthorizerResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises LimitExceededException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("UpdateBillingGroup")
    def update_billing_group(
        self,
        context: RequestContext,
        billing_group_name: BillingGroupName,
        billing_group_properties: BillingGroupProperties,
        expected_version: OptionalVersion | None = None,
        **kwargs,
    ) -> UpdateBillingGroupResponse:
        """Updates information about the billing group.

        Requires permission to access the
        `UpdateBillingGroup <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param billing_group_name: The name of the billing group.
        :param billing_group_properties: The properties of the billing group.
        :param expected_version: The expected version of the billing group.
        :returns: UpdateBillingGroupResponse
        :raises InvalidRequestException:
        :raises VersionConflictException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("UpdateCACertificate")
    def update_ca_certificate(
        self,
        context: RequestContext,
        certificate_id: CertificateId,
        new_status: CACertificateStatus | None = None,
        new_auto_registration_status: AutoRegistrationStatus | None = None,
        registration_config: RegistrationConfig | None = None,
        remove_auto_registration: RemoveAutoRegistration | None = None,
        **kwargs,
    ) -> None:
        """Updates a registered CA certificate.

        Requires permission to access the
        `UpdateCACertificate <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param certificate_id: The CA certificate identifier.
        :param new_status: The updated status of the CA certificate.
        :param new_auto_registration_status: The new value for the auto registration status.
        :param registration_config: Information about the registration configuration.
        :param remove_auto_registration: If true, removes auto registration.
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("UpdateCertificate")
    def update_certificate(
        self,
        context: RequestContext,
        certificate_id: CertificateId,
        new_status: CertificateStatus,
        **kwargs,
    ) -> None:
        """Updates the status of the specified certificate. This operation is
        idempotent.

        Requires permission to access the
        `UpdateCertificate <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        Certificates must be in the ACTIVE state to authenticate devices that
        use a certificate to connect to IoT.

        Within a few minutes of updating a certificate from the ACTIVE state to
        any other state, IoT disconnects all devices that used that certificate
        to connect. Devices cannot use a certificate that is not in the ACTIVE
        state to reconnect.

        :param certificate_id: The ID of the certificate.
        :param new_status: The new status.
        :raises ResourceNotFoundException:
        :raises CertificateStateException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("UpdateCertificateProvider")
    def update_certificate_provider(
        self,
        context: RequestContext,
        certificate_provider_name: CertificateProviderName,
        lambda_function_arn: CertificateProviderFunctionArn | None = None,
        account_default_for_operations: CertificateProviderAccountDefaultForOperations
        | None = None,
        **kwargs,
    ) -> UpdateCertificateProviderResponse:
        """Updates a certificate provider.

        Requires permission to access the
        `UpdateCertificateProvider <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param certificate_provider_name: The name of the certificate provider.
        :param lambda_function_arn: The Lambda function ARN that's associated with the certificate provider.
        :param account_default_for_operations: A list of the operations that the certificate provider will use to
        generate certificates.
        :returns: UpdateCertificateProviderResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("UpdateCommand")
    def update_command(
        self,
        context: RequestContext,
        command_id: CommandId,
        display_name: DisplayName | None = None,
        description: CommandDescription | None = None,
        deprecated: DeprecationFlag | None = None,
        **kwargs,
    ) -> UpdateCommandResponse:
        """Update information about a command or mark a command for deprecation.

        :param command_id: The unique identifier of the command to be updated.
        :param display_name: The new user-friendly name to use in the console for the command.
        :param description: A short text description of the command.
        :param deprecated: A boolean that you can use to specify whether to deprecate a command.
        :returns: UpdateCommandResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("UpdateCustomMetric")
    def update_custom_metric(
        self,
        context: RequestContext,
        metric_name: MetricName,
        display_name: CustomMetricDisplayName,
        **kwargs,
    ) -> UpdateCustomMetricResponse:
        """Updates a Device Defender detect custom metric.

        Requires permission to access the
        `UpdateCustomMetric <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param metric_name: The name of the custom metric.
        :param display_name: Field represents a friendly name in the console for the custom metric,
        it doesn't have to be unique.
        :returns: UpdateCustomMetricResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("UpdateDimension")
    def update_dimension(
        self,
        context: RequestContext,
        name: DimensionName,
        string_values: DimensionStringValues,
        **kwargs,
    ) -> UpdateDimensionResponse:
        """Updates the definition for a dimension. You cannot change the type of a
        dimension after it is created (you can delete it and recreate it).

        Requires permission to access the
        `UpdateDimension <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param name: A unique identifier for the dimension.
        :param string_values: Specifies the value or list of values for the dimension.
        :returns: UpdateDimensionResponse
        :raises InternalFailureException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("UpdateDomainConfiguration")
    def update_domain_configuration(
        self,
        context: RequestContext,
        domain_configuration_name: ReservedDomainConfigurationName,
        authorizer_config: AuthorizerConfig | None = None,
        domain_configuration_status: DomainConfigurationStatus | None = None,
        remove_authorizer_config: RemoveAuthorizerConfig | None = None,
        tls_config: TlsConfig | None = None,
        server_certificate_config: ServerCertificateConfig | None = None,
        authentication_type: AuthenticationType | None = None,
        application_protocol: ApplicationProtocol | None = None,
        client_certificate_config: ClientCertificateConfig | None = None,
        **kwargs,
    ) -> UpdateDomainConfigurationResponse:
        """Updates values stored in the domain configuration. Domain configurations
        for default endpoints can't be updated.

        Requires permission to access the
        `UpdateDomainConfiguration <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param domain_configuration_name: The name of the domain configuration to be updated.
        :param authorizer_config: An object that specifies the authorization service for a domain.
        :param domain_configuration_status: The status to which the domain configuration should be updated.
        :param remove_authorizer_config: Removes the authorization configuration from a domain.
        :param tls_config: An object that specifies the TLS configuration for a domain.
        :param server_certificate_config: The server certificate configuration.
        :param authentication_type: An enumerated string that speciﬁes the authentication type.
        :param application_protocol: An enumerated string that speciﬁes the application-layer protocol.
        :param client_certificate_config: An object that speciﬁes the client certificate conﬁguration for a
        domain.
        :returns: UpdateDomainConfigurationResponse
        :raises ResourceNotFoundException:
        :raises CertificateValidationException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("UpdateDynamicThingGroup")
    def update_dynamic_thing_group(
        self,
        context: RequestContext,
        thing_group_name: ThingGroupName,
        thing_group_properties: ThingGroupProperties,
        expected_version: OptionalVersion | None = None,
        index_name: IndexName | None = None,
        query_string: QueryString | None = None,
        query_version: QueryVersion | None = None,
        **kwargs,
    ) -> UpdateDynamicThingGroupResponse:
        """Updates a dynamic thing group.

        Requires permission to access the
        `UpdateDynamicThingGroup <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_group_name: The name of the dynamic thing group to update.
        :param thing_group_properties: The dynamic thing group properties to update.
        :param expected_version: The expected version of the dynamic thing group to update.
        :param index_name: The dynamic thing group index to update.
        :param query_string: The dynamic thing group search query string to update.
        :param query_version: The dynamic thing group query version to update.
        :returns: UpdateDynamicThingGroupResponse
        :raises InvalidRequestException:
        :raises VersionConflictException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        :raises InvalidQueryException:
        """
        raise NotImplementedError

    @handler("UpdateEncryptionConfiguration")
    def update_encryption_configuration(
        self,
        context: RequestContext,
        encryption_type: EncryptionType,
        kms_key_arn: KmsKeyArn | None = None,
        kms_access_role_arn: KmsAccessRoleArn | None = None,
        **kwargs,
    ) -> UpdateEncryptionConfigurationResponse:
        """Updates the encryption configuration. By default, all Amazon Web
        Services IoT Core data at rest is encrypted using Amazon Web Services
        owned keys. Amazon Web Services IoT Core also supports symmetric
        customer managed keys from Amazon Web Services Key Management Service
        (KMS). With customer managed keys, you create, own, and manage the KMS
        keys in your Amazon Web Services account. For more information, see
        `Data
        encryption <https://docs.aws.amazon.com/iot/latest/developerguide/data-encryption.html>`__
        in the *Amazon Web Services IoT Core Developer Guide*.

        :param encryption_type: The type of the Amazon Web Services Key Management Service (KMS) key.
        :param kms_key_arn: The ARN of the customer-managed KMS key.
        :param kms_access_role_arn: The Amazon Resource Name (ARN) of the IAM role assumed by Amazon Web
        Services IoT Core to call KMS on behalf of the customer.
        :returns: UpdateEncryptionConfigurationResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("UpdateEventConfigurations")
    def update_event_configurations(
        self,
        context: RequestContext,
        event_configurations: EventConfigurations | None = None,
        **kwargs,
    ) -> UpdateEventConfigurationsResponse:
        """Updates the event configurations.

        Requires permission to access the
        `UpdateEventConfigurations <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param event_configurations: The new event configuration values.
        :returns: UpdateEventConfigurationsResponse
        :raises InvalidRequestException:
        :raises InternalFailureException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("UpdateFleetMetric")
    def update_fleet_metric(
        self,
        context: RequestContext,
        metric_name: FleetMetricName,
        index_name: IndexName,
        query_string: QueryString | None = None,
        aggregation_type: AggregationType | None = None,
        period: FleetMetricPeriod | None = None,
        aggregation_field: AggregationField | None = None,
        description: FleetMetricDescription | None = None,
        query_version: QueryVersion | None = None,
        unit: FleetMetricUnit | None = None,
        expected_version: OptionalVersion | None = None,
        **kwargs,
    ) -> None:
        """Updates the data for a fleet metric.

        Requires permission to access the
        `UpdateFleetMetric <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param metric_name: The name of the fleet metric to update.
        :param index_name: The name of the index to search.
        :param query_string: The search query string.
        :param aggregation_type: The type of the aggregation query.
        :param period: The time in seconds between fleet metric emissions.
        :param aggregation_field: The field to aggregate.
        :param description: The description of the fleet metric.
        :param query_version: The version of the query.
        :param unit: Used to support unit transformation such as milliseconds to seconds.
        :param expected_version: The expected version of the fleet metric record in the registry.
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        :raises InvalidQueryException:
        :raises InvalidAggregationException:
        :raises VersionConflictException:
        :raises IndexNotReadyException:
        """
        raise NotImplementedError

    @handler("UpdateIndexingConfiguration")
    def update_indexing_configuration(
        self,
        context: RequestContext,
        thing_indexing_configuration: ThingIndexingConfiguration | None = None,
        thing_group_indexing_configuration: ThingGroupIndexingConfiguration | None = None,
        **kwargs,
    ) -> UpdateIndexingConfigurationResponse:
        """Updates the search configuration.

        Requires permission to access the
        `UpdateIndexingConfiguration <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_indexing_configuration: Thing indexing configuration.
        :param thing_group_indexing_configuration: Thing group indexing configuration.
        :returns: UpdateIndexingConfigurationResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("UpdateJob")
    def update_job(
        self,
        context: RequestContext,
        job_id: JobId,
        description: JobDescription | None = None,
        presigned_url_config: PresignedUrlConfig | None = None,
        job_executions_rollout_config: JobExecutionsRolloutConfig | None = None,
        abort_config: AbortConfig | None = None,
        timeout_config: TimeoutConfig | None = None,
        namespace_id: NamespaceId | None = None,
        job_executions_retry_config: JobExecutionsRetryConfig | None = None,
        **kwargs,
    ) -> None:
        """Updates supported fields of the specified job.

        Requires permission to access the
        `UpdateJob <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param job_id: The ID of the job to be updated.
        :param description: A short text description of the job.
        :param presigned_url_config: Configuration information for pre-signed S3 URLs.
        :param job_executions_rollout_config: Allows you to create a staged rollout of the job.
        :param abort_config: Allows you to create criteria to abort a job.
        :param timeout_config: Specifies the amount of time each device has to finish its execution of
        the job.
        :param namespace_id: The namespace used to indicate that a job is a customer-managed job.
        :param job_executions_retry_config: Allows you to create the criteria to retry a job.
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("UpdateMitigationAction")
    def update_mitigation_action(
        self,
        context: RequestContext,
        action_name: MitigationActionName,
        role_arn: RoleArn | None = None,
        action_params: MitigationActionParams | None = None,
        **kwargs,
    ) -> UpdateMitigationActionResponse:
        """Updates the definition for the specified mitigation action.

        Requires permission to access the
        `UpdateMitigationAction <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param action_name: The friendly name for the mitigation action.
        :param role_arn: The ARN of the IAM role that is used to apply the mitigation action.
        :param action_params: Defines the type of action and the parameters for that action.
        :returns: UpdateMitigationActionResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("UpdatePackage")
    def update_package(
        self,
        context: RequestContext,
        package_name: PackageName,
        description: ResourceDescription | None = None,
        default_version_name: VersionName | None = None,
        unset_default_version: UnsetDefaultVersion | None = None,
        client_token: ClientToken | None = None,
        **kwargs,
    ) -> UpdatePackageResponse:
        """Updates the supported fields for a specific software package.

        Requires permission to access the
        `UpdatePackage <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        and
        `GetIndexingConfiguration <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        actions.

        :param package_name: The name of the target software package.
        :param description: The package description.
        :param default_version_name: The name of the default package version.
        :param unset_default_version: Indicates whether you want to remove the named default package version
        from the software package.
        :param client_token: A unique case-sensitive identifier that you can provide to ensure the
        idempotency of the request.
        :returns: UpdatePackageResponse
        :raises ThrottlingException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ValidationException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("UpdatePackageConfiguration")
    def update_package_configuration(
        self,
        context: RequestContext,
        version_update_by_jobs_config: VersionUpdateByJobsConfig | None = None,
        client_token: ClientToken | None = None,
        **kwargs,
    ) -> UpdatePackageConfigurationResponse:
        """Updates the software package configuration.

        Requires permission to access the
        `UpdatePackageConfiguration <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        and
        `iam:PassRole <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html>`__
        actions.

        :param version_update_by_jobs_config: Configuration to manage job's package version reporting.
        :param client_token: A unique case-sensitive identifier that you can provide to ensure the
        idempotency of the request.
        :returns: UpdatePackageConfigurationResponse
        :raises ThrottlingException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("UpdatePackageVersion")
    def update_package_version(
        self,
        context: RequestContext,
        package_name: PackageName,
        version_name: VersionName,
        description: ResourceDescription | None = None,
        attributes: ResourceAttributes | None = None,
        artifact: PackageVersionArtifact | None = None,
        action: PackageVersionAction | None = None,
        recipe: PackageVersionRecipe | None = None,
        client_token: ClientToken | None = None,
        **kwargs,
    ) -> UpdatePackageVersionResponse:
        """Updates the supported fields for a specific package version.

        Requires permission to access the
        `UpdatePackageVersion <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        and
        `GetIndexingConfiguration <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        actions.

        :param package_name: The name of the associated software package.
        :param version_name: The name of the target package version.
        :param description: The package version description.
        :param attributes: Metadata that can be used to define a package version’s configuration.
        :param artifact: The various components that make up a software package version.
        :param action: The status that the package version should be assigned.
        :param recipe: The inline job document associated with a software package version used
        for a quick job deployment.
        :param client_token: A unique case-sensitive identifier that you can provide to ensure the
        idempotency of the request.
        :returns: UpdatePackageVersionResponse
        :raises ThrottlingException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ValidationException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("UpdateProvisioningTemplate")
    def update_provisioning_template(
        self,
        context: RequestContext,
        template_name: TemplateName,
        description: TemplateDescription | None = None,
        enabled: Enabled | None = None,
        default_version_id: TemplateVersionId | None = None,
        provisioning_role_arn: RoleArn | None = None,
        pre_provisioning_hook: ProvisioningHook | None = None,
        remove_pre_provisioning_hook: RemoveHook | None = None,
        **kwargs,
    ) -> UpdateProvisioningTemplateResponse:
        """Updates a provisioning template.

        Requires permission to access the
        `UpdateProvisioningTemplate <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param template_name: The name of the provisioning template.
        :param description: The description of the provisioning template.
        :param enabled: True to enable the provisioning template, otherwise false.
        :param default_version_id: The ID of the default provisioning template version.
        :param provisioning_role_arn: The ARN of the role associated with the provisioning template.
        :param pre_provisioning_hook: Updates the pre-provisioning hook template.
        :param remove_pre_provisioning_hook: Removes pre-provisioning hook template.
        :returns: UpdateProvisioningTemplateResponse
        :raises InternalFailureException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises UnauthorizedException:
        :raises ConflictingResourceUpdateException:
        """
        raise NotImplementedError

    @handler("UpdateRoleAlias")
    def update_role_alias(
        self,
        context: RequestContext,
        role_alias: RoleAlias,
        role_arn: RoleArn | None = None,
        credential_duration_seconds: CredentialDurationSeconds | None = None,
        **kwargs,
    ) -> UpdateRoleAliasResponse:
        """Updates a role alias.

        Requires permission to access the
        `UpdateRoleAlias <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        The value of
        ```credentialDurationSeconds`` <https://docs.aws.amazon.com/iot/latest/apireference/API_UpdateRoleAlias.html#iot-UpdateRoleAlias-request-credentialDurationSeconds>`__
        must be less than or equal to the maximum session duration of the IAM
        role that the role alias references. For more information, see
        `Modifying a role maximum session duration (Amazon Web Services
        API) <https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-managingrole-editing-api.html#roles-modify_max-session-duration-api>`__
        from the Amazon Web Services Identity and Access Management User Guide.

        :param role_alias: The role alias to update.
        :param role_arn: The role ARN.
        :param credential_duration_seconds: The number of seconds the credential will be valid.
        :returns: UpdateRoleAliasResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("UpdateScheduledAudit")
    def update_scheduled_audit(
        self,
        context: RequestContext,
        scheduled_audit_name: ScheduledAuditName,
        frequency: AuditFrequency | None = None,
        day_of_month: DayOfMonth | None = None,
        day_of_week: DayOfWeek | None = None,
        target_check_names: TargetAuditCheckNames | None = None,
        **kwargs,
    ) -> UpdateScheduledAuditResponse:
        """Updates a scheduled audit, including which checks are performed and how
        often the audit takes place.

        Requires permission to access the
        `UpdateScheduledAudit <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param scheduled_audit_name: The name of the scheduled audit.
        :param frequency: How often the scheduled audit takes place, either ``DAILY``, ``WEEKLY``,
        ``BIWEEKLY``, or ``MONTHLY``.
        :param day_of_month: The day of the month on which the scheduled audit takes place.
        :param day_of_week: The day of the week on which the scheduled audit takes place.
        :param target_check_names: Which checks are performed during the scheduled audit.
        :returns: UpdateScheduledAuditResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("UpdateSecurityProfile")
    def update_security_profile(
        self,
        context: RequestContext,
        security_profile_name: SecurityProfileName,
        security_profile_description: SecurityProfileDescription | None = None,
        behaviors: Behaviors | None = None,
        alert_targets: AlertTargets | None = None,
        additional_metrics_to_retain: AdditionalMetricsToRetainList | None = None,
        additional_metrics_to_retain_v2: AdditionalMetricsToRetainV2List | None = None,
        delete_behaviors: DeleteBehaviors | None = None,
        delete_alert_targets: DeleteAlertTargets | None = None,
        delete_additional_metrics_to_retain: DeleteAdditionalMetricsToRetain | None = None,
        expected_version: OptionalVersion | None = None,
        metrics_export_config: MetricsExportConfig | None = None,
        delete_metrics_export_config: DeleteMetricsExportConfig | None = None,
        **kwargs,
    ) -> UpdateSecurityProfileResponse:
        """Updates a Device Defender security profile.

        Requires permission to access the
        `UpdateSecurityProfile <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param security_profile_name: The name of the security profile you want to update.
        :param security_profile_description: A description of the security profile.
        :param behaviors: Specifies the behaviors that, when violated by a device (thing), cause
        an alert.
        :param alert_targets: Where the alerts are sent.
        :param additional_metrics_to_retain: *Please use UpdateSecurityProfileRequest$additionalMetricsToRetainV2
        instead.
        :param additional_metrics_to_retain_v2: A list of metrics whose data is retained (stored).
        :param delete_behaviors: If true, delete all ``behaviors`` defined for this security profile.
        :param delete_alert_targets: If true, delete all ``alertTargets`` defined for this security profile.
        :param delete_additional_metrics_to_retain: If true, delete all ``additionalMetricsToRetain`` defined for this
        security profile.
        :param expected_version: The expected version of the security profile.
        :param metrics_export_config: Specifies the MQTT topic and role ARN required for metric export.
        :param delete_metrics_export_config: Set the value as true to delete metrics export related configurations.
        :returns: UpdateSecurityProfileResponse
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises VersionConflictException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("UpdateStream")
    def update_stream(
        self,
        context: RequestContext,
        stream_id: StreamId,
        description: StreamDescription | None = None,
        files: StreamFiles | None = None,
        role_arn: RoleArn | None = None,
        **kwargs,
    ) -> UpdateStreamResponse:
        """Updates an existing stream. The stream version will be incremented by
        one.

        Requires permission to access the
        `UpdateStream <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param stream_id: The stream ID.
        :param description: The description of the stream.
        :param files: The files associated with the stream.
        :param role_arn: An IAM role that allows the IoT service principal assumes to access your
        S3 files.
        :returns: UpdateStreamResponse
        :raises InvalidRequestException:
        :raises LimitExceededException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("UpdateThing")
    def update_thing(
        self,
        context: RequestContext,
        thing_name: ThingName,
        thing_type_name: ThingTypeName | None = None,
        attribute_payload: AttributePayload | None = None,
        expected_version: OptionalVersion | None = None,
        remove_thing_type: RemoveThingType | None = None,
        **kwargs,
    ) -> UpdateThingResponse:
        """Updates the data for a thing.

        Requires permission to access the
        `UpdateThing <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_name: The name of the thing to update.
        :param thing_type_name: The name of the thing type.
        :param attribute_payload: A list of thing attributes, a JSON string containing name-value pairs.
        :param expected_version: The expected version of the thing record in the registry.
        :param remove_thing_type: Remove a thing type association.
        :returns: UpdateThingResponse
        :raises InvalidRequestException:
        :raises VersionConflictException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("UpdateThingGroup")
    def update_thing_group(
        self,
        context: RequestContext,
        thing_group_name: ThingGroupName,
        thing_group_properties: ThingGroupProperties,
        expected_version: OptionalVersion | None = None,
        **kwargs,
    ) -> UpdateThingGroupResponse:
        """Update a thing group.

        Requires permission to access the
        `UpdateThingGroup <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_group_name: The thing group to update.
        :param thing_group_properties: The thing group properties.
        :param expected_version: The expected version of the thing group.
        :returns: UpdateThingGroupResponse
        :raises InvalidRequestException:
        :raises VersionConflictException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("UpdateThingGroupsForThing")
    def update_thing_groups_for_thing(
        self,
        context: RequestContext,
        thing_name: ThingName | None = None,
        thing_groups_to_add: ThingGroupList | None = None,
        thing_groups_to_remove: ThingGroupList | None = None,
        override_dynamic_groups: OverrideDynamicGroups | None = None,
        **kwargs,
    ) -> UpdateThingGroupsForThingResponse:
        """Updates the groups to which the thing belongs.

        Requires permission to access the
        `UpdateThingGroupsForThing <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param thing_name: The thing whose group memberships will be updated.
        :param thing_groups_to_add: The groups to which the thing will be added.
        :param thing_groups_to_remove: The groups from which the thing will be removed.
        :param override_dynamic_groups: Override dynamic thing groups with static thing groups when 10-group
        limit is reached.
        :returns: UpdateThingGroupsForThingResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("UpdateThingType")
    def update_thing_type(
        self,
        context: RequestContext,
        thing_type_name: ThingTypeName,
        thing_type_properties: ThingTypeProperties | None = None,
        **kwargs,
    ) -> UpdateThingTypeResponse:
        """Updates a thing type.

        :param thing_type_name: The name of a thing type.
        :param thing_type_properties: The ThingTypeProperties contains information about the thing type
        including: a thing type description, and a list of searchable thing
        attribute names.
        :returns: UpdateThingTypeResponse
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises UnauthorizedException:
        :raises ServiceUnavailableException:
        :raises InternalFailureException:
        """
        raise NotImplementedError

    @handler("UpdateTopicRuleDestination")
    def update_topic_rule_destination(
        self, context: RequestContext, arn: AwsArn, status: TopicRuleDestinationStatus, **kwargs
    ) -> UpdateTopicRuleDestinationResponse:
        """Updates a topic rule destination. You use this to change the status,
        endpoint URL, or confirmation URL of the destination.

        Requires permission to access the
        `UpdateTopicRuleDestination <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param arn: The ARN of the topic rule destination.
        :param status: The status of the topic rule destination.
        :returns: UpdateTopicRuleDestinationResponse
        :raises InternalException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        :raises UnauthorizedException:
        :raises ConflictingResourceUpdateException:
        """
        raise NotImplementedError

    @handler("ValidateSecurityProfileBehaviors")
    def validate_security_profile_behaviors(
        self, context: RequestContext, behaviors: Behaviors, **kwargs
    ) -> ValidateSecurityProfileBehaviorsResponse:
        """Validates a Device Defender security profile behaviors specification.

        Requires permission to access the
        `ValidateSecurityProfileBehaviors <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsiot.html#awsiot-actions-as-permissions>`__
        action.

        :param behaviors: Specifies the behaviors that, when violated by a device (thing), cause
        an alert.
        :returns: ValidateSecurityProfileBehaviorsResponse
        :raises InvalidRequestException:
        :raises ThrottlingException:
        :raises InternalFailureException:
        """
        raise NotImplementedError
