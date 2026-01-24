from datetime import datetime
from enum import StrEnum
from typing import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

MaxResults = int
_boolean = bool
_double = float
_integer = int
_integerMin5Max100 = int
_string = str


class AuthenticationStrategy(StrEnum):
    SIMPLE = "SIMPLE"
    LDAP = "LDAP"
    CONFIG_MANAGED = "CONFIG_MANAGED"


class BrokerState(StrEnum):
    CREATION_IN_PROGRESS = "CREATION_IN_PROGRESS"
    CREATION_FAILED = "CREATION_FAILED"
    DELETION_IN_PROGRESS = "DELETION_IN_PROGRESS"
    RUNNING = "RUNNING"
    REBOOT_IN_PROGRESS = "REBOOT_IN_PROGRESS"
    CRITICAL_ACTION_REQUIRED = "CRITICAL_ACTION_REQUIRED"
    REPLICA = "REPLICA"


class BrokerStorageType(StrEnum):
    EBS = "EBS"
    EFS = "EFS"


class ChangeType(StrEnum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class DataReplicationMode(StrEnum):
    NONE = "NONE"
    CRDR = "CRDR"


class DayOfWeek(StrEnum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


class DeploymentMode(StrEnum):
    SINGLE_INSTANCE = "SINGLE_INSTANCE"
    ACTIVE_STANDBY_MULTI_AZ = "ACTIVE_STANDBY_MULTI_AZ"
    CLUSTER_MULTI_AZ = "CLUSTER_MULTI_AZ"


class EngineType(StrEnum):
    ACTIVEMQ = "ACTIVEMQ"
    RABBITMQ = "RABBITMQ"


class PromoteMode(StrEnum):
    SWITCHOVER = "SWITCHOVER"
    FAILOVER = "FAILOVER"


class SanitizationWarningReason(StrEnum):
    DISALLOWED_ELEMENT_REMOVED = "DISALLOWED_ELEMENT_REMOVED"
    DISALLOWED_ATTRIBUTE_REMOVED = "DISALLOWED_ATTRIBUTE_REMOVED"
    INVALID_ATTRIBUTE_VALUE_REMOVED = "INVALID_ATTRIBUTE_VALUE_REMOVED"


class BadRequestException(ServiceException):
    """Returns information about an error."""

    code: str = "BadRequestException"
    sender_fault: bool = False
    status_code: int = 400
    ErrorAttribute: _string | None


class ConflictException(ServiceException):
    """Returns information about an error."""

    code: str = "ConflictException"
    sender_fault: bool = False
    status_code: int = 409
    ErrorAttribute: _string | None


class ForbiddenException(ServiceException):
    """Returns information about an error."""

    code: str = "ForbiddenException"
    sender_fault: bool = False
    status_code: int = 403
    ErrorAttribute: _string | None


class InternalServerErrorException(ServiceException):
    """Returns information about an error."""

    code: str = "InternalServerErrorException"
    sender_fault: bool = False
    status_code: int = 500
    ErrorAttribute: _string | None


class NotFoundException(ServiceException):
    """Returns information about an error."""

    code: str = "NotFoundException"
    sender_fault: bool = False
    status_code: int = 404
    ErrorAttribute: _string | None


class UnauthorizedException(ServiceException):
    """Returns information about an error."""

    code: str = "UnauthorizedException"
    sender_fault: bool = False
    status_code: int = 401
    ErrorAttribute: _string | None


class ActionRequired(TypedDict, total=False):
    """Action required for a broker."""

    ActionRequiredCode: _string | None
    ActionRequiredInfo: _string | None


class AvailabilityZone(TypedDict, total=False):
    """Name of the availability zone."""

    Name: _string | None


class EngineVersion(TypedDict, total=False):
    """Id of the engine version."""

    Name: _string | None


_listOfEngineVersion = list[EngineVersion]


class BrokerEngineType(TypedDict, total=False):
    """Types of broker engines."""

    EngineType: EngineType | None
    EngineVersions: _listOfEngineVersion | None


_listOfBrokerEngineType = list[BrokerEngineType]


class BrokerEngineTypeOutput(TypedDict, total=False):
    """Returns a list of broker engine type."""

    BrokerEngineTypes: _listOfBrokerEngineType | None
    MaxResults: _integerMin5Max100
    NextToken: _string | None


_listOf__string = list[_string]


class BrokerInstance(TypedDict, total=False):
    """Returns information about all brokers."""

    ConsoleURL: _string | None
    Endpoints: _listOf__string | None
    IpAddress: _string | None


_listOfDeploymentMode = list[DeploymentMode]
_listOfAvailabilityZone = list[AvailabilityZone]


class BrokerInstanceOption(TypedDict, total=False):
    """Option for host instance type."""

    AvailabilityZones: _listOfAvailabilityZone | None
    EngineType: EngineType | None
    HostInstanceType: _string | None
    StorageType: BrokerStorageType | None
    SupportedDeploymentModes: _listOfDeploymentMode | None
    SupportedEngineVersions: _listOf__string | None


_listOfBrokerInstanceOption = list[BrokerInstanceOption]


class BrokerInstanceOptionsOutput(TypedDict, total=False):
    """Returns a list of broker instance options."""

    BrokerInstanceOptions: _listOfBrokerInstanceOption | None
    MaxResults: _integerMin5Max100
    NextToken: _string | None


_timestampIso8601 = datetime


class BrokerSummary(TypedDict, total=False):
    """Returns information about all brokers."""

    BrokerArn: _string | None
    BrokerId: _string | None
    BrokerName: _string | None
    BrokerState: BrokerState | None
    Created: _timestampIso8601 | None
    DeploymentMode: DeploymentMode
    EngineType: EngineType
    HostInstanceType: _string | None


_mapOf__string = dict[_string, _string]


class ConfigurationRevision(TypedDict, total=False):
    """Returns information about the specified configuration revision."""

    Created: _timestampIso8601
    Description: _string | None
    Revision: _integer


class Configuration(TypedDict, total=False):
    """Returns information about all configurations."""

    Arn: _string
    AuthenticationStrategy: AuthenticationStrategy
    Created: _timestampIso8601
    Description: _string
    EngineType: EngineType
    EngineVersion: _string
    Id: _string
    LatestRevision: ConfigurationRevision
    Name: _string
    Tags: _mapOf__string | None


class ConfigurationId(TypedDict, total=False):
    """A list of information about the configuration."""

    Id: _string
    Revision: _integer | None


_listOfConfigurationId = list[ConfigurationId]


class Configurations(TypedDict, total=False):
    """Broker configuration information"""

    Current: ConfigurationId | None
    History: _listOfConfigurationId | None
    Pending: ConfigurationId | None


class User(TypedDict, total=False):
    """A user associated with the broker. For Amazon MQ for RabbitMQ brokers,
    one and only one administrative user is accepted and created when a
    broker is first provisioned. All subsequent broker users are created by
    making RabbitMQ API calls directly to brokers or via the RabbitMQ web
    console.
    """

    ConsoleAccess: _boolean | None
    Groups: _listOf__string | None
    Password: _string
    Username: _string
    ReplicationUser: _boolean | None


_listOfUser = list[User]


class WeeklyStartTime(TypedDict, total=False):
    """The scheduled time period relative to UTC during which Amazon MQ begins
    to apply pending updates or patches to the broker.
    """

    DayOfWeek: DayOfWeek
    TimeOfDay: _string
    TimeZone: _string | None


class Logs(TypedDict, total=False):
    """The list of information about logs to be enabled for the specified
    broker.
    """

    Audit: _boolean | None
    General: _boolean | None


class LdapServerMetadataInput(TypedDict, total=False):
    """Optional. The metadata of the LDAP server used to authenticate and
    authorize connections to the broker.

    Does not apply to RabbitMQ brokers.
    """

    Hosts: _listOf__string
    RoleBase: _string
    RoleName: _string | None
    RoleSearchMatching: _string
    RoleSearchSubtree: _boolean | None
    ServiceAccountPassword: _string
    ServiceAccountUsername: _string
    UserBase: _string
    UserRoleName: _string | None
    UserSearchMatching: _string
    UserSearchSubtree: _boolean | None


class EncryptionOptions(TypedDict, total=False):
    """Encryption options for the broker."""

    KmsKeyId: _string | None
    UseAwsOwnedKey: _boolean


class CreateBrokerInput(TypedDict, total=False):
    """Creates a broker."""

    AuthenticationStrategy: AuthenticationStrategy | None
    AutoMinorVersionUpgrade: _boolean | None
    BrokerName: _string
    Configuration: ConfigurationId | None
    CreatorRequestId: _string | None
    DeploymentMode: DeploymentMode
    DataReplicationMode: DataReplicationMode | None
    DataReplicationPrimaryBrokerArn: _string | None
    EncryptionOptions: EncryptionOptions | None
    EngineType: EngineType
    EngineVersion: _string | None
    HostInstanceType: _string
    LdapServerMetadata: LdapServerMetadataInput | None
    Logs: Logs | None
    MaintenanceWindowStartTime: WeeklyStartTime | None
    PubliclyAccessible: _boolean
    SecurityGroups: _listOf__string | None
    StorageType: BrokerStorageType | None
    SubnetIds: _listOf__string | None
    Tags: _mapOf__string | None
    Users: _listOfUser | None


class CreateBrokerOutput(TypedDict, total=False):
    """Returns information about the created broker."""

    BrokerArn: _string | None
    BrokerId: _string | None


class CreateBrokerRequest(ServiceRequest):
    """Creates a broker using the specified properties."""

    AuthenticationStrategy: AuthenticationStrategy | None
    AutoMinorVersionUpgrade: _boolean | None
    BrokerName: _string
    Configuration: ConfigurationId | None
    CreatorRequestId: _string | None
    DeploymentMode: DeploymentMode
    EncryptionOptions: EncryptionOptions | None
    EngineType: EngineType
    EngineVersion: _string | None
    HostInstanceType: _string
    LdapServerMetadata: LdapServerMetadataInput | None
    Logs: Logs | None
    MaintenanceWindowStartTime: WeeklyStartTime | None
    PubliclyAccessible: _boolean
    SecurityGroups: _listOf__string | None
    StorageType: BrokerStorageType | None
    SubnetIds: _listOf__string | None
    Tags: _mapOf__string | None
    Users: _listOfUser | None
    DataReplicationMode: DataReplicationMode | None
    DataReplicationPrimaryBrokerArn: _string | None


class CreateBrokerResponse(TypedDict, total=False):
    BrokerArn: _string | None
    BrokerId: _string | None


class CreateConfigurationInput(TypedDict, total=False):
    """Creates a new configuration for the specified configuration name. Amazon
    MQ uses the default configuration (the engine type and version).
    """

    AuthenticationStrategy: AuthenticationStrategy | None
    EngineType: EngineType
    EngineVersion: _string | None
    Name: _string
    Tags: _mapOf__string | None


class CreateConfigurationOutput(TypedDict, total=False):
    """Returns information about the created configuration."""

    Arn: _string
    AuthenticationStrategy: AuthenticationStrategy
    Created: _timestampIso8601
    Id: _string
    LatestRevision: ConfigurationRevision | None
    Name: _string


class CreateConfigurationRequest(ServiceRequest):
    """Creates a new configuration for the specified configuration name. Amazon
    MQ uses the default configuration (the engine type and version).
    """

    AuthenticationStrategy: AuthenticationStrategy | None
    EngineType: EngineType
    EngineVersion: _string | None
    Name: _string
    Tags: _mapOf__string | None


class CreateConfigurationResponse(TypedDict, total=False):
    Arn: _string | None
    AuthenticationStrategy: AuthenticationStrategy | None
    Created: _timestampIso8601 | None
    Id: _string | None
    LatestRevision: ConfigurationRevision | None
    Name: _string | None


class CreateTagsRequest(ServiceRequest):
    """A map of the key-value pairs for the resource tag."""

    ResourceArn: _string
    Tags: _mapOf__string | None


class CreateUserInput(TypedDict, total=False):
    """Creates a new ActiveMQ user."""

    ConsoleAccess: _boolean | None
    Groups: _listOf__string | None
    Password: _string
    ReplicationUser: _boolean | None


class CreateUserRequest(ServiceRequest):
    """Creates a new ActiveMQ user."""

    BrokerId: _string
    ConsoleAccess: _boolean | None
    Groups: _listOf__string | None
    Password: _string
    Username: _string
    ReplicationUser: _boolean | None


class CreateUserResponse(TypedDict, total=False):
    pass


class DataReplicationCounterpart(TypedDict, total=False):
    """Specifies a broker in a data replication pair."""

    BrokerId: _string
    Region: _string


class DataReplicationMetadataOutput(TypedDict, total=False):
    """The replication details of the data replication-enabled broker. Only
    returned if dataReplicationMode or pendingDataReplicationMode is set to
    CRDR.
    """

    DataReplicationCounterpart: DataReplicationCounterpart | None
    DataReplicationRole: _string


class DeleteBrokerOutput(TypedDict, total=False):
    """Returns information about the deleted broker."""

    BrokerId: _string | None


class DeleteBrokerRequest(ServiceRequest):
    BrokerId: _string


class DeleteBrokerResponse(TypedDict, total=False):
    BrokerId: _string | None


class DeleteConfigurationOutput(TypedDict, total=False):
    """Returns information about the deleted configuration."""

    ConfigurationId: _string | None


class DeleteConfigurationRequest(ServiceRequest):
    ConfigurationId: _string


class DeleteConfigurationResponse(TypedDict, total=False):
    ConfigurationId: _string | None


class DeleteTagsRequest(ServiceRequest):
    ResourceArn: _string
    TagKeys: _listOf__string


class DeleteUserRequest(ServiceRequest):
    BrokerId: _string
    Username: _string


class DeleteUserResponse(TypedDict, total=False):
    pass


class DescribeBrokerEngineTypesRequest(ServiceRequest):
    EngineType: _string | None
    MaxResults: MaxResults | None
    NextToken: _string | None


class DescribeBrokerEngineTypesResponse(TypedDict, total=False):
    BrokerEngineTypes: _listOfBrokerEngineType | None
    MaxResults: _integerMin5Max100 | None
    NextToken: _string | None


class DescribeBrokerInstanceOptionsRequest(ServiceRequest):
    EngineType: _string | None
    HostInstanceType: _string | None
    MaxResults: MaxResults | None
    NextToken: _string | None
    StorageType: _string | None


class DescribeBrokerInstanceOptionsResponse(TypedDict, total=False):
    BrokerInstanceOptions: _listOfBrokerInstanceOption | None
    MaxResults: _integerMin5Max100 | None
    NextToken: _string | None


class UserSummary(TypedDict, total=False):
    """Returns a list of all broker users. Does not apply to RabbitMQ brokers."""

    PendingChange: ChangeType | None
    Username: _string


_listOfUserSummary = list[UserSummary]


class LdapServerMetadataOutput(TypedDict, total=False):
    """Optional. The metadata of the LDAP server used to authenticate and
    authorize connections to the broker.
    """

    Hosts: _listOf__string
    RoleBase: _string
    RoleName: _string | None
    RoleSearchMatching: _string
    RoleSearchSubtree: _boolean | None
    ServiceAccountUsername: _string
    UserBase: _string
    UserRoleName: _string | None
    UserSearchMatching: _string
    UserSearchSubtree: _boolean | None


class PendingLogs(TypedDict, total=False):
    """The list of information about logs to be enabled for the specified
    broker.
    """

    Audit: _boolean | None
    General: _boolean | None


class LogsSummary(TypedDict, total=False):
    """The list of information about logs currently enabled and pending to be
    deployed for the specified broker.
    """

    Audit: _boolean | None
    AuditLogGroup: _string | None
    General: _boolean
    GeneralLogGroup: _string
    Pending: PendingLogs | None


_listOfBrokerInstance = list[BrokerInstance]
_listOfActionRequired = list[ActionRequired]


class DescribeBrokerOutput(TypedDict, total=False):
    """Returns information about the specified broker."""

    ActionsRequired: _listOfActionRequired | None
    AuthenticationStrategy: AuthenticationStrategy | None
    AutoMinorVersionUpgrade: _boolean
    BrokerArn: _string | None
    BrokerId: _string | None
    BrokerInstances: _listOfBrokerInstance | None
    BrokerName: _string | None
    BrokerState: BrokerState | None
    Configurations: Configurations | None
    Created: _timestampIso8601 | None
    DeploymentMode: DeploymentMode
    DataReplicationMetadata: DataReplicationMetadataOutput | None
    DataReplicationMode: DataReplicationMode | None
    EncryptionOptions: EncryptionOptions | None
    EngineType: EngineType
    EngineVersion: _string | None
    HostInstanceType: _string | None
    LdapServerMetadata: LdapServerMetadataOutput | None
    Logs: LogsSummary | None
    MaintenanceWindowStartTime: WeeklyStartTime | None
    PendingAuthenticationStrategy: AuthenticationStrategy | None
    PendingDataReplicationMetadata: DataReplicationMetadataOutput | None
    PendingDataReplicationMode: DataReplicationMode | None
    PendingEngineVersion: _string | None
    PendingHostInstanceType: _string | None
    PendingLdapServerMetadata: LdapServerMetadataOutput | None
    PendingSecurityGroups: _listOf__string | None
    PubliclyAccessible: _boolean
    SecurityGroups: _listOf__string | None
    StorageType: BrokerStorageType | None
    SubnetIds: _listOf__string | None
    Tags: _mapOf__string | None
    Users: _listOfUserSummary | None


class DescribeBrokerRequest(ServiceRequest):
    BrokerId: _string


class DescribeBrokerResponse(TypedDict, total=False):
    ActionsRequired: _listOfActionRequired | None
    AuthenticationStrategy: AuthenticationStrategy | None
    AutoMinorVersionUpgrade: _boolean | None
    BrokerArn: _string | None
    BrokerId: _string | None
    BrokerInstances: _listOfBrokerInstance | None
    BrokerName: _string | None
    BrokerState: BrokerState | None
    Configurations: Configurations | None
    Created: _timestampIso8601 | None
    DeploymentMode: DeploymentMode | None
    EncryptionOptions: EncryptionOptions | None
    EngineType: EngineType | None
    EngineVersion: _string | None
    HostInstanceType: _string | None
    LdapServerMetadata: LdapServerMetadataOutput | None
    Logs: LogsSummary | None
    MaintenanceWindowStartTime: WeeklyStartTime | None
    PendingAuthenticationStrategy: AuthenticationStrategy | None
    PendingEngineVersion: _string | None
    PendingHostInstanceType: _string | None
    PendingLdapServerMetadata: LdapServerMetadataOutput | None
    PendingSecurityGroups: _listOf__string | None
    PubliclyAccessible: _boolean | None
    SecurityGroups: _listOf__string | None
    StorageType: BrokerStorageType | None
    SubnetIds: _listOf__string | None
    Tags: _mapOf__string | None
    Users: _listOfUserSummary | None
    DataReplicationMetadata: DataReplicationMetadataOutput | None
    DataReplicationMode: DataReplicationMode | None
    PendingDataReplicationMetadata: DataReplicationMetadataOutput | None
    PendingDataReplicationMode: DataReplicationMode | None


class DescribeConfigurationRequest(ServiceRequest):
    ConfigurationId: _string


class DescribeConfigurationResponse(TypedDict, total=False):
    Arn: _string | None
    AuthenticationStrategy: AuthenticationStrategy | None
    Created: _timestampIso8601 | None
    Description: _string | None
    EngineType: EngineType | None
    EngineVersion: _string | None
    Id: _string | None
    LatestRevision: ConfigurationRevision | None
    Name: _string | None
    Tags: _mapOf__string | None


class DescribeConfigurationRevisionOutput(TypedDict, total=False):
    """Returns the specified configuration revision for the specified
    configuration.
    """

    ConfigurationId: _string
    Created: _timestampIso8601
    Data: _string
    Description: _string | None


class DescribeConfigurationRevisionRequest(ServiceRequest):
    ConfigurationId: _string
    ConfigurationRevision: _string


class DescribeConfigurationRevisionResponse(TypedDict, total=False):
    ConfigurationId: _string | None
    Created: _timestampIso8601 | None
    Data: _string | None
    Description: _string | None


class UserPendingChanges(TypedDict, total=False):
    """Returns information about the status of the changes pending for the
    ActiveMQ user.
    """

    ConsoleAccess: _boolean | None
    Groups: _listOf__string | None
    PendingChange: ChangeType


class DescribeUserOutput(TypedDict, total=False):
    """Returns information about an ActiveMQ user."""

    BrokerId: _string
    ConsoleAccess: _boolean | None
    Groups: _listOf__string | None
    Pending: UserPendingChanges | None
    ReplicationUser: _boolean | None
    Username: _string


class DescribeUserRequest(ServiceRequest):
    BrokerId: _string
    Username: _string


class DescribeUserResponse(TypedDict, total=False):
    BrokerId: _string | None
    ConsoleAccess: _boolean | None
    Groups: _listOf__string | None
    Pending: UserPendingChanges | None
    Username: _string | None
    ReplicationUser: _boolean | None


class Error(TypedDict, total=False):
    """Returns information about an error."""

    ErrorAttribute: _string | None
    Message: _string | None


_listOfBrokerSummary = list[BrokerSummary]


class ListBrokersOutput(TypedDict, total=False):
    """A list of information about all brokers."""

    BrokerSummaries: _listOfBrokerSummary | None
    NextToken: _string | None


class ListBrokersRequest(ServiceRequest):
    MaxResults: MaxResults | None
    NextToken: _string | None


class ListBrokersResponse(TypedDict, total=False):
    BrokerSummaries: _listOfBrokerSummary | None
    NextToken: _string | None


_listOfConfigurationRevision = list[ConfigurationRevision]


class ListConfigurationRevisionsOutput(TypedDict, total=False):
    """Returns a list of all revisions for the specified configuration."""

    ConfigurationId: _string | None
    MaxResults: _integer | None
    NextToken: _string | None
    Revisions: _listOfConfigurationRevision | None


class ListConfigurationRevisionsRequest(ServiceRequest):
    ConfigurationId: _string
    MaxResults: MaxResults | None
    NextToken: _string | None


class ListConfigurationRevisionsResponse(TypedDict, total=False):
    ConfigurationId: _string | None
    MaxResults: _integer | None
    NextToken: _string | None
    Revisions: _listOfConfigurationRevision | None


_listOfConfiguration = list[Configuration]


class ListConfigurationsOutput(TypedDict, total=False):
    """Returns a list of all configurations."""

    Configurations: _listOfConfiguration | None
    MaxResults: _integer | None
    NextToken: _string | None


class ListConfigurationsRequest(ServiceRequest):
    MaxResults: MaxResults | None
    NextToken: _string | None


class ListConfigurationsResponse(TypedDict, total=False):
    Configurations: _listOfConfiguration | None
    MaxResults: _integer | None
    NextToken: _string | None


class ListTagsRequest(ServiceRequest):
    ResourceArn: _string


class ListTagsResponse(TypedDict, total=False):
    Tags: _mapOf__string | None


class ListUsersOutput(TypedDict, total=False):
    """Returns a list of all ActiveMQ users."""

    BrokerId: _string
    MaxResults: _integerMin5Max100
    NextToken: _string | None
    Users: _listOfUserSummary


class ListUsersRequest(ServiceRequest):
    BrokerId: _string
    MaxResults: MaxResults | None
    NextToken: _string | None


class ListUsersResponse(TypedDict, total=False):
    BrokerId: _string | None
    MaxResults: _integerMin5Max100 | None
    NextToken: _string | None
    Users: _listOfUserSummary | None


class PromoteInput(TypedDict, total=False):
    """Creates a Promote request with the properties specified."""

    Mode: PromoteMode


class PromoteOutput(TypedDict, total=False):
    """Returns information about the updated broker."""

    BrokerId: _string | None


class PromoteRequest(ServiceRequest):
    """Promotes a data replication replica broker to the primary broker role."""

    BrokerId: _string
    Mode: PromoteMode


class PromoteResponse(TypedDict, total=False):
    BrokerId: _string | None


class RebootBrokerRequest(ServiceRequest):
    BrokerId: _string


class RebootBrokerResponse(TypedDict, total=False):
    pass


class SanitizationWarning(TypedDict, total=False):
    """Returns information about the configuration element or attribute that
    was sanitized in the configuration.
    """

    AttributeName: _string | None
    ElementName: _string | None
    Reason: SanitizationWarningReason


class Tags(TypedDict, total=False):
    """A map of the key-value pairs for the resource tag."""

    Tags: _mapOf__string | None


class UpdateBrokerInput(TypedDict, total=False):
    """Updates the broker using the specified properties."""

    AuthenticationStrategy: AuthenticationStrategy | None
    AutoMinorVersionUpgrade: _boolean | None
    Configuration: ConfigurationId | None
    DataReplicationMode: DataReplicationMode | None
    EngineVersion: _string | None
    HostInstanceType: _string | None
    LdapServerMetadata: LdapServerMetadataInput | None
    Logs: Logs | None
    MaintenanceWindowStartTime: WeeklyStartTime | None
    SecurityGroups: _listOf__string | None


class UpdateBrokerOutput(TypedDict, total=False):
    """Returns information about the updated broker."""

    AuthenticationStrategy: AuthenticationStrategy | None
    AutoMinorVersionUpgrade: _boolean | None
    BrokerId: _string
    Configuration: ConfigurationId | None
    DataReplicationMetadata: DataReplicationMetadataOutput | None
    DataReplicationMode: DataReplicationMode | None
    EngineVersion: _string | None
    HostInstanceType: _string | None
    LdapServerMetadata: LdapServerMetadataOutput | None
    Logs: Logs | None
    MaintenanceWindowStartTime: WeeklyStartTime | None
    PendingDataReplicationMetadata: DataReplicationMetadataOutput | None
    PendingDataReplicationMode: DataReplicationMode | None
    SecurityGroups: _listOf__string | None


class UpdateBrokerRequest(ServiceRequest):
    """Updates the broker using the specified properties."""

    AuthenticationStrategy: AuthenticationStrategy | None
    AutoMinorVersionUpgrade: _boolean | None
    BrokerId: _string
    Configuration: ConfigurationId | None
    EngineVersion: _string | None
    HostInstanceType: _string | None
    LdapServerMetadata: LdapServerMetadataInput | None
    Logs: Logs | None
    MaintenanceWindowStartTime: WeeklyStartTime | None
    SecurityGroups: _listOf__string | None
    DataReplicationMode: DataReplicationMode | None


class UpdateBrokerResponse(TypedDict, total=False):
    AuthenticationStrategy: AuthenticationStrategy | None
    AutoMinorVersionUpgrade: _boolean | None
    BrokerId: _string | None
    Configuration: ConfigurationId | None
    EngineVersion: _string | None
    HostInstanceType: _string | None
    LdapServerMetadata: LdapServerMetadataOutput | None
    Logs: Logs | None
    MaintenanceWindowStartTime: WeeklyStartTime | None
    SecurityGroups: _listOf__string | None
    DataReplicationMetadata: DataReplicationMetadataOutput | None
    DataReplicationMode: DataReplicationMode | None
    PendingDataReplicationMetadata: DataReplicationMetadataOutput | None
    PendingDataReplicationMode: DataReplicationMode | None


class UpdateConfigurationInput(TypedDict, total=False):
    """Updates the specified configuration."""

    Data: _string
    Description: _string | None


_listOfSanitizationWarning = list[SanitizationWarning]


class UpdateConfigurationOutput(TypedDict, total=False):
    """Returns information about the updated configuration."""

    Arn: _string
    Created: _timestampIso8601
    Id: _string
    LatestRevision: ConfigurationRevision | None
    Name: _string
    Warnings: _listOfSanitizationWarning | None


class UpdateConfigurationRequest(ServiceRequest):
    """Updates the specified configuration."""

    ConfigurationId: _string
    Data: _string
    Description: _string | None


class UpdateConfigurationResponse(TypedDict, total=False):
    Arn: _string | None
    Created: _timestampIso8601 | None
    Id: _string | None
    LatestRevision: ConfigurationRevision | None
    Name: _string | None
    Warnings: _listOfSanitizationWarning | None


class UpdateUserInput(TypedDict, total=False):
    """Updates the information for an ActiveMQ user."""

    ConsoleAccess: _boolean | None
    Groups: _listOf__string | None
    Password: _string | None
    ReplicationUser: _boolean | None


class UpdateUserRequest(ServiceRequest):
    """Updates the information for an ActiveMQ user."""

    BrokerId: _string
    ConsoleAccess: _boolean | None
    Groups: _listOf__string | None
    Password: _string | None
    Username: _string
    ReplicationUser: _boolean | None


class UpdateUserResponse(TypedDict, total=False):
    pass


_long = int
_timestampUnix = datetime


class MqApi:
    service: str = "mq"
    version: str = "2017-11-27"

    @handler("CreateBroker")
    def create_broker(
        self,
        context: RequestContext,
        host_instance_type: _string,
        broker_name: _string,
        deployment_mode: DeploymentMode,
        engine_type: EngineType,
        publicly_accessible: _boolean,
        authentication_strategy: AuthenticationStrategy | None = None,
        auto_minor_version_upgrade: _boolean | None = None,
        configuration: ConfigurationId | None = None,
        creator_request_id: _string | None = None,
        encryption_options: EncryptionOptions | None = None,
        engine_version: _string | None = None,
        ldap_server_metadata: LdapServerMetadataInput | None = None,
        logs: Logs | None = None,
        maintenance_window_start_time: WeeklyStartTime | None = None,
        security_groups: _listOf__string | None = None,
        storage_type: BrokerStorageType | None = None,
        subnet_ids: _listOf__string | None = None,
        tags: _mapOf__string | None = None,
        users: _listOfUser | None = None,
        data_replication_mode: DataReplicationMode | None = None,
        data_replication_primary_broker_arn: _string | None = None,
        **kwargs,
    ) -> CreateBrokerResponse:
        """Creates a broker. Note: This API is asynchronous.

        To create a broker, you must either use the AmazonMQFullAccess IAM
        policy or include the following EC2 permissions in your IAM policy.

        -  ec2:CreateNetworkInterface

           This permission is required to allow Amazon MQ to create an elastic
           network interface (ENI) on behalf of your account.

        -  ec2:CreateNetworkInterfacePermission

           This permission is required to attach the ENI to the broker instance.

        -  ec2:DeleteNetworkInterface

        -  ec2:DeleteNetworkInterfacePermission

        -  ec2:DetachNetworkInterface

        -  ec2:DescribeInternetGateways

        -  ec2:DescribeNetworkInterfaces

        -  ec2:DescribeNetworkInterfacePermissions

        -  ec2:DescribeRouteTables

        -  ec2:DescribeSecurityGroups

        -  ec2:DescribeSubnets

        -  ec2:DescribeVpcs

        For more information, see `Create an IAM User and Get Your Amazon Web
        Services
        Credentials <https://docs.aws.amazon.com//amazon-mq/latest/developer-guide/amazon-mq-setting-up.html#create-iam-user>`__
        and `Never Modify or Delete the Amazon MQ Elastic Network
        Interface <https://docs.aws.amazon.com//amazon-mq/latest/developer-guide/connecting-to-amazon-mq.html#never-modify-delete-elastic-network-interface>`__
        in the *Amazon MQ Developer Guide*.

        :param host_instance_type: Required.
        :param broker_name: Required.
        :param deployment_mode: Required.
        :param engine_type: Required.
        :param publicly_accessible: Enables connections from applications outside of the VPC that hosts the
        broker's subnets.
        :param authentication_strategy: Optional.
        :param auto_minor_version_upgrade: Enables automatic upgrades to new patch versions for brokers as new
        versions are released and supported by Amazon MQ.
        :param configuration: A list of information about the configuration.
        :param creator_request_id: The unique ID that the requester receives for the created broker.
        :param encryption_options: Encryption options for the broker.
        :param engine_version: The broker engine version.
        :param ldap_server_metadata: Optional.
        :param logs: Enables Amazon CloudWatch logging for brokers.
        :param maintenance_window_start_time: The parameters that determine the WeeklyStartTime.
        :param security_groups: The list of rules (1 minimum, 125 maximum) that authorize connections to
        brokers.
        :param storage_type: The broker's storage type.
        :param subnet_ids: The list of groups that define which subnets and IP ranges the broker
        can use from different Availability Zones.
        :param tags: Create tags when creating the broker.
        :param users: The list of broker users (persons or applications) who can access queues
        and topics.
        :param data_replication_mode: Defines whether this broker is a part of a data replication pair.
        :param data_replication_primary_broker_arn: The Amazon Resource Name (ARN) of the primary broker that is used to
        replicate data from in a data replication pair, and is applied to the
        replica broker.
        :returns: CreateBrokerResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ConflictException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("CreateConfiguration")
    def create_configuration(
        self,
        context: RequestContext,
        engine_type: EngineType,
        name: _string,
        authentication_strategy: AuthenticationStrategy | None = None,
        engine_version: _string | None = None,
        tags: _mapOf__string | None = None,
        **kwargs,
    ) -> CreateConfigurationResponse:
        """Creates a new configuration for the specified configuration name. Amazon
        MQ uses the default configuration (the engine type and version).

        :param engine_type: Required.
        :param name: Required.
        :param authentication_strategy: Optional.
        :param engine_version: The broker engine version.
        :param tags: Create tags when creating the configuration.
        :returns: CreateConfigurationResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ConflictException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("CreateTags")
    def create_tags(
        self,
        context: RequestContext,
        resource_arn: _string,
        tags: _mapOf__string | None = None,
        **kwargs,
    ) -> None:
        """Add a tag to a resource.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource tag.
        :param tags: The key-value pair for the resource tag.
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("CreateUser")
    def create_user(
        self,
        context: RequestContext,
        username: _string,
        broker_id: _string,
        password: _string,
        console_access: _boolean | None = None,
        groups: _listOf__string | None = None,
        replication_user: _boolean | None = None,
        **kwargs,
    ) -> CreateUserResponse:
        """Creates an ActiveMQ user.

        Do not add personally identifiable information (PII) or other
        confidential or sensitive information in broker usernames. Broker
        usernames are accessible to other Amazon Web Services services,
        including CloudWatch Logs. Broker usernames are not intended to be used
        for private or sensitive data.

        :param username: The username of the ActiveMQ user.
        :param broker_id: The unique ID that Amazon MQ generates for the broker.
        :param password: Required.
        :param console_access: Enables access to the ActiveMQ Web Console for the ActiveMQ user.
        :param groups: The list of groups (20 maximum) to which the ActiveMQ user belongs.
        :param replication_user: Defines if this user is intended for CRDR replication purposes.
        :returns: CreateUserResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ConflictException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("DeleteBroker")
    def delete_broker(
        self, context: RequestContext, broker_id: _string, **kwargs
    ) -> DeleteBrokerResponse:
        """Deletes a broker. Note: This API is asynchronous.

        :param broker_id: The unique ID that Amazon MQ generates for the broker.
        :returns: DeleteBrokerResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("DeleteConfiguration")
    def delete_configuration(
        self, context: RequestContext, configuration_id: _string, **kwargs
    ) -> DeleteConfigurationResponse:
        """Deletes the specified configuration.

        :param configuration_id: The unique ID that Amazon MQ generates for the configuration.
        :returns: DeleteConfigurationResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ConflictException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("DeleteTags")
    def delete_tags(
        self, context: RequestContext, tag_keys: _listOf__string, resource_arn: _string, **kwargs
    ) -> None:
        """Removes a tag from a resource.

        :param tag_keys: An array of tag keys to delete.
        :param resource_arn: The Amazon Resource Name (ARN) of the resource tag.
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("DeleteUser")
    def delete_user(
        self, context: RequestContext, username: _string, broker_id: _string, **kwargs
    ) -> DeleteUserResponse:
        """Deletes an ActiveMQ user.

        :param username: The username of the ActiveMQ user.
        :param broker_id: The unique ID that Amazon MQ generates for the broker.
        :returns: DeleteUserResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("DescribeBroker")
    def describe_broker(
        self, context: RequestContext, broker_id: _string, **kwargs
    ) -> DescribeBrokerResponse:
        """Returns information about the specified broker.

        :param broker_id: The unique ID that Amazon MQ generates for the broker.
        :returns: DescribeBrokerResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("DescribeBrokerEngineTypes")
    def describe_broker_engine_types(
        self,
        context: RequestContext,
        engine_type: _string | None = None,
        max_results: MaxResults | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> DescribeBrokerEngineTypesResponse:
        """Describe available engine types and versions.

        :param engine_type: Filter response by engine type.
        :param max_results: The maximum number of brokers that Amazon MQ can return per page (20 by
        default).
        :param next_token: The token that specifies the next page of results Amazon MQ should
        return.
        :returns: DescribeBrokerEngineTypesResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("DescribeBrokerInstanceOptions")
    def describe_broker_instance_options(
        self,
        context: RequestContext,
        engine_type: _string | None = None,
        host_instance_type: _string | None = None,
        max_results: MaxResults | None = None,
        next_token: _string | None = None,
        storage_type: _string | None = None,
        **kwargs,
    ) -> DescribeBrokerInstanceOptionsResponse:
        """Describe available broker instance options.

        :param engine_type: Filter response by engine type.
        :param host_instance_type: Filter response by host instance type.
        :param max_results: The maximum number of brokers that Amazon MQ can return per page (20 by
        default).
        :param next_token: The token that specifies the next page of results Amazon MQ should
        return.
        :param storage_type: Filter response by storage type.
        :returns: DescribeBrokerInstanceOptionsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("DescribeConfiguration")
    def describe_configuration(
        self, context: RequestContext, configuration_id: _string, **kwargs
    ) -> DescribeConfigurationResponse:
        """Returns information about the specified configuration.

        :param configuration_id: The unique ID that Amazon MQ generates for the configuration.
        :returns: DescribeConfigurationResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("DescribeConfigurationRevision")
    def describe_configuration_revision(
        self,
        context: RequestContext,
        configuration_revision: _string,
        configuration_id: _string,
        **kwargs,
    ) -> DescribeConfigurationRevisionResponse:
        """Returns the specified configuration revision for the specified
        configuration.

        :param configuration_revision: The revision of the configuration.
        :param configuration_id: The unique ID that Amazon MQ generates for the configuration.
        :returns: DescribeConfigurationRevisionResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("DescribeUser")
    def describe_user(
        self, context: RequestContext, username: _string, broker_id: _string, **kwargs
    ) -> DescribeUserResponse:
        """Returns information about an ActiveMQ user.

        :param username: The username of the ActiveMQ user.
        :param broker_id: The unique ID that Amazon MQ generates for the broker.
        :returns: DescribeUserResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ListBrokers")
    def list_brokers(
        self,
        context: RequestContext,
        max_results: MaxResults | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> ListBrokersResponse:
        """Returns a list of all brokers.

        :param max_results: The maximum number of brokers that Amazon MQ can return per page (20 by
        default).
        :param next_token: The token that specifies the next page of results Amazon MQ should
        return.
        :returns: ListBrokersResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ListConfigurationRevisions")
    def list_configuration_revisions(
        self,
        context: RequestContext,
        configuration_id: _string,
        max_results: MaxResults | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> ListConfigurationRevisionsResponse:
        """Returns a list of all revisions for the specified configuration.

        :param configuration_id: The unique ID that Amazon MQ generates for the configuration.
        :param max_results: The maximum number of brokers that Amazon MQ can return per page (20 by
        default).
        :param next_token: The token that specifies the next page of results Amazon MQ should
        return.
        :returns: ListConfigurationRevisionsResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ListConfigurations")
    def list_configurations(
        self,
        context: RequestContext,
        max_results: MaxResults | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> ListConfigurationsResponse:
        """Returns a list of all configurations.

        :param max_results: The maximum number of brokers that Amazon MQ can return per page (20 by
        default).
        :param next_token: The token that specifies the next page of results Amazon MQ should
        return.
        :returns: ListConfigurationsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ListTags")
    def list_tags(
        self, context: RequestContext, resource_arn: _string, **kwargs
    ) -> ListTagsResponse:
        """Lists tags for a resource.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource tag.
        :returns: ListTagsResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ListUsers")
    def list_users(
        self,
        context: RequestContext,
        broker_id: _string,
        max_results: MaxResults | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> ListUsersResponse:
        """Returns a list of all ActiveMQ users.

        :param broker_id: The unique ID that Amazon MQ generates for the broker.
        :param max_results: The maximum number of brokers that Amazon MQ can return per page (20 by
        default).
        :param next_token: The token that specifies the next page of results Amazon MQ should
        return.
        :returns: ListUsersResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("Promote")
    def promote(
        self, context: RequestContext, broker_id: _string, mode: PromoteMode, **kwargs
    ) -> PromoteResponse:
        """Promotes a data replication replica broker to the primary broker role.

        :param broker_id: The unique ID that Amazon MQ generates for the broker.
        :param mode: The Promote mode requested.
        :returns: PromoteResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("RebootBroker")
    def reboot_broker(
        self, context: RequestContext, broker_id: _string, **kwargs
    ) -> RebootBrokerResponse:
        """Reboots a broker. Note: This API is asynchronous.

        :param broker_id: The unique ID that Amazon MQ generates for the broker.
        :returns: RebootBrokerResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("UpdateBroker")
    def update_broker(
        self,
        context: RequestContext,
        broker_id: _string,
        authentication_strategy: AuthenticationStrategy | None = None,
        auto_minor_version_upgrade: _boolean | None = None,
        configuration: ConfigurationId | None = None,
        engine_version: _string | None = None,
        host_instance_type: _string | None = None,
        ldap_server_metadata: LdapServerMetadataInput | None = None,
        logs: Logs | None = None,
        maintenance_window_start_time: WeeklyStartTime | None = None,
        security_groups: _listOf__string | None = None,
        data_replication_mode: DataReplicationMode | None = None,
        **kwargs,
    ) -> UpdateBrokerResponse:
        """Adds a pending configuration change to a broker.

        :param broker_id: The unique ID that Amazon MQ generates for the broker.
        :param authentication_strategy: Optional.
        :param auto_minor_version_upgrade: Enables automatic upgrades to new patch versions for brokers as new
        versions are released and supported by Amazon MQ.
        :param configuration: A list of information about the configuration.
        :param engine_version: The broker engine version.
        :param host_instance_type: The broker's host instance type to upgrade to.
        :param ldap_server_metadata: Optional.
        :param logs: Enables Amazon CloudWatch logging for brokers.
        :param maintenance_window_start_time: The parameters that determine the WeeklyStartTime.
        :param security_groups: The list of security groups (1 minimum, 5 maximum) that authorizes
        connections to brokers.
        :param data_replication_mode: Defines whether this broker is a part of a data replication pair.
        :returns: UpdateBrokerResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ConflictException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("UpdateConfiguration")
    def update_configuration(
        self,
        context: RequestContext,
        configuration_id: _string,
        data: _string,
        description: _string | None = None,
        **kwargs,
    ) -> UpdateConfigurationResponse:
        """Updates the specified configuration.

        :param configuration_id: The unique ID that Amazon MQ generates for the configuration.
        :param data: Amazon MQ for Active MQ: The base64-encoded XML configuration.
        :param description: The description of the configuration.
        :returns: UpdateConfigurationResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ConflictException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("UpdateUser")
    def update_user(
        self,
        context: RequestContext,
        username: _string,
        broker_id: _string,
        console_access: _boolean | None = None,
        groups: _listOf__string | None = None,
        password: _string | None = None,
        replication_user: _boolean | None = None,
        **kwargs,
    ) -> UpdateUserResponse:
        """Updates the information for an ActiveMQ user.

        :param username: The username of the ActiveMQ user.
        :param broker_id: The unique ID that Amazon MQ generates for the broker.
        :param console_access: Enables access to the the ActiveMQ Web Console for the ActiveMQ user.
        :param groups: The list of groups (20 maximum) to which the ActiveMQ user belongs.
        :param password: The password of the user.
        :param replication_user: Defines whether the user is intended for data replication.
        :returns: UpdateUserResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ConflictException:
        :raises ForbiddenException:
        """
        raise NotImplementedError
