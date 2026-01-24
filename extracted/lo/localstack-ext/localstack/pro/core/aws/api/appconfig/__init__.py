from collections.abc import Iterable
from datetime import datetime
from enum import StrEnum
from typing import IO, TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

Arn = str
Boolean = bool
ConfigurationProfileType = str
DeletionProtectionDuration = int
DeploymentStrategyId = str
Description = str
DynamicParameterKey = str
ExtensionOrParameterName = str
Float = float
GrowthFactor = float
Id = str
Identifier = str
Integer = int
KmsKeyIdentifier = str
KmsKeyIdentifierOrEmpty = str
LongName = str
MaxResults = int
MinutesBetween0And24Hours = int
Name = str
NextToken = str
Percentage = float
QueryName = str
RoleArn = str
String = str
StringWithLengthBetween0And32768 = str
StringWithLengthBetween1And2048 = str
StringWithLengthBetween1And255 = str
StringWithLengthBetween1And64 = str
TagKey = str
TagValue = str
Uri = str
Version = str
VersionLabel = str


class ActionPoint(StrEnum):
    PRE_CREATE_HOSTED_CONFIGURATION_VERSION = "PRE_CREATE_HOSTED_CONFIGURATION_VERSION"
    PRE_START_DEPLOYMENT = "PRE_START_DEPLOYMENT"
    AT_DEPLOYMENT_TICK = "AT_DEPLOYMENT_TICK"
    ON_DEPLOYMENT_START = "ON_DEPLOYMENT_START"
    ON_DEPLOYMENT_STEP = "ON_DEPLOYMENT_STEP"
    ON_DEPLOYMENT_BAKING = "ON_DEPLOYMENT_BAKING"
    ON_DEPLOYMENT_COMPLETE = "ON_DEPLOYMENT_COMPLETE"
    ON_DEPLOYMENT_ROLLED_BACK = "ON_DEPLOYMENT_ROLLED_BACK"


class BadRequestReason(StrEnum):
    InvalidConfiguration = "InvalidConfiguration"


class BytesMeasure(StrEnum):
    KILOBYTES = "KILOBYTES"


class DeletionProtectionCheck(StrEnum):
    ACCOUNT_DEFAULT = "ACCOUNT_DEFAULT"
    APPLY = "APPLY"
    BYPASS = "BYPASS"


class DeploymentEventType(StrEnum):
    PERCENTAGE_UPDATED = "PERCENTAGE_UPDATED"
    ROLLBACK_STARTED = "ROLLBACK_STARTED"
    ROLLBACK_COMPLETED = "ROLLBACK_COMPLETED"
    BAKE_TIME_STARTED = "BAKE_TIME_STARTED"
    DEPLOYMENT_STARTED = "DEPLOYMENT_STARTED"
    DEPLOYMENT_COMPLETED = "DEPLOYMENT_COMPLETED"
    REVERT_COMPLETED = "REVERT_COMPLETED"


class DeploymentState(StrEnum):
    BAKING = "BAKING"
    VALIDATING = "VALIDATING"
    DEPLOYING = "DEPLOYING"
    COMPLETE = "COMPLETE"
    ROLLING_BACK = "ROLLING_BACK"
    ROLLED_BACK = "ROLLED_BACK"
    REVERTED = "REVERTED"


class EnvironmentState(StrEnum):
    READY_FOR_DEPLOYMENT = "READY_FOR_DEPLOYMENT"
    DEPLOYING = "DEPLOYING"
    ROLLING_BACK = "ROLLING_BACK"
    ROLLED_BACK = "ROLLED_BACK"
    REVERTED = "REVERTED"


class GrowthType(StrEnum):
    LINEAR = "LINEAR"
    EXPONENTIAL = "EXPONENTIAL"


class ReplicateTo(StrEnum):
    NONE = "NONE"
    SSM_DOCUMENT = "SSM_DOCUMENT"


class TriggeredBy(StrEnum):
    USER = "USER"
    APPCONFIG = "APPCONFIG"
    CLOUDWATCH_ALARM = "CLOUDWATCH_ALARM"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class ValidatorType(StrEnum):
    JSON_SCHEMA = "JSON_SCHEMA"
    LAMBDA = "LAMBDA"


class InvalidConfigurationDetail(TypedDict, total=False):
    """Detailed information about the bad request exception error when creating
    a hosted configuration version.
    """

    Constraint: String | None
    Location: String | None
    Reason: String | None
    Type: String | None
    Value: String | None


InvalidConfigurationDetailList = list[InvalidConfigurationDetail]


class BadRequestDetails(TypedDict, total=False):
    """Detailed information about the input that failed to satisfy the
    constraints specified by a call.
    """

    InvalidConfiguration: InvalidConfigurationDetailList | None


class BadRequestException(ServiceException):
    """The input fails to satisfy the constraints specified by an Amazon Web
    Services service.
    """

    code: str = "BadRequestException"
    sender_fault: bool = False
    status_code: int = 400
    Reason: BadRequestReason | None
    Details: BadRequestDetails | None


class ConflictException(ServiceException):
    """The request could not be processed because of conflict in the current
    state of the resource.
    """

    code: str = "ConflictException"
    sender_fault: bool = False
    status_code: int = 409


class InternalServerException(ServiceException):
    """There was an internal failure in the AppConfig service."""

    code: str = "InternalServerException"
    sender_fault: bool = False
    status_code: int = 500


class PayloadTooLargeException(ServiceException):
    """The configuration size is too large."""

    code: str = "PayloadTooLargeException"
    sender_fault: bool = False
    status_code: int = 413
    Measure: BytesMeasure | None
    Limit: Float | None
    Size: Float | None


class ResourceNotFoundException(ServiceException):
    """The requested resource could not be found."""

    code: str = "ResourceNotFoundException"
    sender_fault: bool = False
    status_code: int = 404
    ResourceName: String | None


class ServiceQuotaExceededException(ServiceException):
    """The number of one more AppConfig resources exceeds the maximum allowed.
    Verify that your environment doesn't exceed the following service
    quotas:

    Applications: 100 max

    Deployment strategies: 20 max

    Configuration profiles: 100 max per application

    Environments: 20 max per application

    To resolve this issue, you can delete one or more resources and try
    again. Or, you can request a quota increase. For more information about
    quotas and to request an increase, see `Service quotas for
    AppConfig <https://docs.aws.amazon.com/general/latest/gr/appconfig.html#limits_appconfig>`__
    in the Amazon Web Services General Reference.
    """

    code: str = "ServiceQuotaExceededException"
    sender_fault: bool = False
    status_code: int = 402


class DeletionProtectionSettings(TypedDict, total=False):
    """A parameter to configure deletion protection. Deletion protection
    prevents a user from deleting a configuration profile or an environment
    if AppConfig has called either
    `GetLatestConfiguration <https://docs.aws.amazon.com/appconfig/2019-10-09/APIReference/API_appconfigdata_GetLatestConfiguration.html>`__
    or for the configuration profile or from the environment during the
    specified interval.

    The default interval specified by ``ProtectionPeriodInMinutes`` is 60.
    ``DeletionProtectionCheck`` skips configuration profiles and
    environments that were created in the past hour.
    """

    Enabled: Boolean | None
    ProtectionPeriodInMinutes: DeletionProtectionDuration | None


class AccountSettings(TypedDict, total=False):
    DeletionProtection: DeletionProtectionSettings | None


class Action(TypedDict, total=False):
    """An action defines the tasks that the extension performs during the
    AppConfig workflow. Each action includes an action point, as shown in
    the following list:

    -  ``PRE_CREATE_HOSTED_CONFIGURATION_VERSION``

    -  ``PRE_START_DEPLOYMENT``

    -  ``AT_DEPLOYMENT_TICK``

    -  ``ON_DEPLOYMENT_START``

    -  ``ON_DEPLOYMENT_STEP``

    -  ``ON_DEPLOYMENT_BAKING``

    -  ``ON_DEPLOYMENT_COMPLETE``

    -  ``ON_DEPLOYMENT_ROLLED_BACK``

    Each action also includes a name, a URI to an Lambda function, and an
    Amazon Resource Name (ARN) for an Identity and Access Management assume
    role. You specify the name, URI, and ARN for each *action point* defined
    in the extension.
    """

    Name: Name | None
    Description: Description | None
    Uri: Uri | None
    RoleArn: Arn | None


class ActionInvocation(TypedDict, total=False):
    """An extension that was invoked as part of a deployment event."""

    ExtensionIdentifier: Identifier | None
    ActionName: Name | None
    Uri: Uri | None
    RoleArn: Arn | None
    ErrorMessage: String | None
    ErrorCode: String | None
    InvocationId: Id | None


ActionInvocations = list[ActionInvocation]
ActionList = list[Action]
ActionsMap = dict[ActionPoint, ActionList]


class Application(TypedDict, total=False):
    Id: Id | None
    Name: Name | None
    Description: Description | None


ApplicationList = list[Application]


class Applications(TypedDict, total=False):
    Items: ApplicationList | None
    NextToken: NextToken | None


ParameterValueMap = dict[ExtensionOrParameterName, StringWithLengthBetween1And2048]


class AppliedExtension(TypedDict, total=False):
    """An extension that was invoked during a deployment."""

    ExtensionId: Id | None
    ExtensionAssociationId: Id | None
    VersionNumber: Integer | None
    Parameters: ParameterValueMap | None


AppliedExtensions = list[AppliedExtension]
Blob = bytes


class Configuration(TypedDict, total=False):
    Content: Blob | IO[Blob] | Iterable[Blob] | None
    ConfigurationVersion: Version | None
    ContentType: String | None


class Validator(TypedDict, total=False):
    """A validator provides a syntactic or semantic check to ensure the
    configuration that you want to deploy functions as intended. To validate
    your application configuration data, you provide a schema or an Amazon
    Web Services Lambda function that runs against the configuration. The
    configuration deployment or update can only proceed when the
    configuration data is valid. For more information, see `About
    validators <https://docs.aws.amazon.com/appconfig/latest/userguide/appconfig-creating-configuration-profile.html#appconfig-creating-configuration-and-profile-validators>`__
    in the *AppConfig User Guide*.
    """

    Type: ValidatorType
    Content: StringWithLengthBetween0And32768


ValidatorList = list[Validator]


class ConfigurationProfile(TypedDict, total=False):
    ApplicationId: Id | None
    Id: Id | None
    Name: LongName | None
    Description: Description | None
    LocationUri: Uri | None
    RetrievalRoleArn: RoleArn | None
    Validators: ValidatorList | None
    Type: ConfigurationProfileType | None
    KmsKeyArn: Arn | None
    KmsKeyIdentifier: KmsKeyIdentifier | None


ValidatorTypeList = list[ValidatorType]


class ConfigurationProfileSummary(TypedDict, total=False):
    """A summary of a configuration profile."""

    ApplicationId: Id | None
    Id: Id | None
    Name: LongName | None
    LocationUri: Uri | None
    ValidatorTypes: ValidatorTypeList | None
    Type: ConfigurationProfileType | None


ConfigurationProfileSummaryList = list[ConfigurationProfileSummary]


class ConfigurationProfiles(TypedDict, total=False):
    Items: ConfigurationProfileSummaryList | None
    NextToken: NextToken | None


TagMap = dict[TagKey, TagValue]


class CreateApplicationRequest(ServiceRequest):
    Name: Name
    Description: Description | None
    Tags: TagMap | None


class CreateConfigurationProfileRequest(ServiceRequest):
    ApplicationId: Id
    Name: LongName
    Description: Description | None
    LocationUri: Uri
    RetrievalRoleArn: RoleArn | None
    Validators: ValidatorList | None
    Tags: TagMap | None
    Type: ConfigurationProfileType | None
    KmsKeyIdentifier: KmsKeyIdentifier | None


class CreateDeploymentStrategyRequest(ServiceRequest):
    Name: Name
    Description: Description | None
    DeploymentDurationInMinutes: MinutesBetween0And24Hours
    FinalBakeTimeInMinutes: MinutesBetween0And24Hours | None
    GrowthFactor: GrowthFactor
    GrowthType: GrowthType | None
    ReplicateTo: ReplicateTo | None
    Tags: TagMap | None


class Monitor(TypedDict, total=False):
    """Amazon CloudWatch alarms to monitor during the deployment process."""

    AlarmArn: StringWithLengthBetween1And2048
    AlarmRoleArn: RoleArn | None


MonitorList = list[Monitor]


class CreateEnvironmentRequest(ServiceRequest):
    ApplicationId: Id
    Name: Name
    Description: Description | None
    Monitors: MonitorList | None
    Tags: TagMap | None


class CreateExtensionAssociationRequest(ServiceRequest):
    ExtensionIdentifier: Identifier
    ExtensionVersionNumber: Integer | None
    ResourceIdentifier: Identifier
    Parameters: ParameterValueMap | None
    Tags: TagMap | None


class Parameter(TypedDict, total=False):
    """A value such as an Amazon Resource Name (ARN) or an Amazon Simple
    Notification Service topic entered in an extension when invoked.
    Parameter values are specified in an extension association. For more
    information about extensions, see `Extending
    workflows <https://docs.aws.amazon.com/appconfig/latest/userguide/working-with-appconfig-extensions.html>`__
    in the *AppConfig User Guide*.
    """

    Description: Description | None
    Required: Boolean | None
    Dynamic: Boolean | None


ParameterMap = dict[ExtensionOrParameterName, Parameter]


class CreateExtensionRequest(ServiceRequest):
    Name: ExtensionOrParameterName
    Description: Description | None
    Actions: ActionsMap
    Parameters: ParameterMap | None
    Tags: TagMap | None
    LatestVersionNumber: Integer | None


class CreateHostedConfigurationVersionRequest(ServiceRequest):
    Content: IO[Blob]
    ApplicationId: Id
    ConfigurationProfileId: Id
    Description: Description | None
    ContentType: StringWithLengthBetween1And255
    LatestVersionNumber: Integer | None
    VersionLabel: VersionLabel | None


class DeleteApplicationRequest(ServiceRequest):
    ApplicationId: Id


class DeleteConfigurationProfileRequest(ServiceRequest):
    ApplicationId: Id
    ConfigurationProfileId: Id
    DeletionProtectionCheck: DeletionProtectionCheck | None


class DeleteDeploymentStrategyRequest(ServiceRequest):
    DeploymentStrategyId: DeploymentStrategyId


class DeleteEnvironmentRequest(ServiceRequest):
    EnvironmentId: Id
    ApplicationId: Id
    DeletionProtectionCheck: DeletionProtectionCheck | None


class DeleteExtensionAssociationRequest(ServiceRequest):
    ExtensionAssociationId: Id


class DeleteExtensionRequest(ServiceRequest):
    ExtensionIdentifier: Identifier
    VersionNumber: Integer | None


class DeleteHostedConfigurationVersionRequest(ServiceRequest):
    ApplicationId: Id
    ConfigurationProfileId: Id
    VersionNumber: Integer


Iso8601DateTime = datetime


class DeploymentEvent(TypedDict, total=False):
    """An object that describes a deployment event."""

    EventType: DeploymentEventType | None
    TriggeredBy: TriggeredBy | None
    Description: Description | None
    ActionInvocations: ActionInvocations | None
    OccurredAt: Iso8601DateTime | None


DeploymentEvents = list[DeploymentEvent]


class Deployment(TypedDict, total=False):
    ApplicationId: Id | None
    EnvironmentId: Id | None
    DeploymentStrategyId: Id | None
    ConfigurationProfileId: Id | None
    DeploymentNumber: Integer | None
    ConfigurationName: Name | None
    ConfigurationLocationUri: Uri | None
    ConfigurationVersion: Version | None
    Description: Description | None
    DeploymentDurationInMinutes: MinutesBetween0And24Hours | None
    GrowthType: GrowthType | None
    GrowthFactor: Percentage | None
    FinalBakeTimeInMinutes: MinutesBetween0And24Hours | None
    State: DeploymentState | None
    EventLog: DeploymentEvents | None
    PercentageComplete: Percentage | None
    StartedAt: Iso8601DateTime | None
    CompletedAt: Iso8601DateTime | None
    AppliedExtensions: AppliedExtensions | None
    KmsKeyArn: Arn | None
    KmsKeyIdentifier: KmsKeyIdentifier | None
    VersionLabel: VersionLabel | None


class DeploymentSummary(TypedDict, total=False):
    """Information about the deployment."""

    DeploymentNumber: Integer | None
    ConfigurationName: Name | None
    ConfigurationVersion: Version | None
    DeploymentDurationInMinutes: MinutesBetween0And24Hours | None
    GrowthType: GrowthType | None
    GrowthFactor: Percentage | None
    FinalBakeTimeInMinutes: MinutesBetween0And24Hours | None
    State: DeploymentState | None
    PercentageComplete: Percentage | None
    StartedAt: Iso8601DateTime | None
    CompletedAt: Iso8601DateTime | None
    VersionLabel: VersionLabel | None


DeploymentList = list[DeploymentSummary]


class DeploymentStrategy(TypedDict, total=False):
    Id: Id | None
    Name: Name | None
    Description: Description | None
    DeploymentDurationInMinutes: MinutesBetween0And24Hours | None
    GrowthType: GrowthType | None
    GrowthFactor: Percentage | None
    FinalBakeTimeInMinutes: MinutesBetween0And24Hours | None
    ReplicateTo: ReplicateTo | None


DeploymentStrategyList = list[DeploymentStrategy]


class DeploymentStrategies(TypedDict, total=False):
    Items: DeploymentStrategyList | None
    NextToken: NextToken | None


class Deployments(TypedDict, total=False):
    Items: DeploymentList | None
    NextToken: NextToken | None


DynamicParameterMap = dict[DynamicParameterKey, StringWithLengthBetween1And2048]


class Environment(TypedDict, total=False):
    ApplicationId: Id | None
    Id: Id | None
    Name: Name | None
    Description: Description | None
    State: EnvironmentState | None
    Monitors: MonitorList | None


EnvironmentList = list[Environment]


class Environments(TypedDict, total=False):
    Items: EnvironmentList | None
    NextToken: NextToken | None


class Extension(TypedDict, total=False):
    Id: Id | None
    Name: Name | None
    VersionNumber: Integer | None
    Arn: Arn | None
    Description: Description | None
    Actions: ActionsMap | None
    Parameters: ParameterMap | None


class ExtensionAssociation(TypedDict, total=False):
    Id: Identifier | None
    ExtensionArn: Arn | None
    ResourceArn: Arn | None
    Arn: Arn | None
    Parameters: ParameterValueMap | None
    ExtensionVersionNumber: Integer | None


class ExtensionAssociationSummary(TypedDict, total=False):
    """Information about an association between an extension and an AppConfig
    resource such as an application, environment, or configuration profile.
    Call ``GetExtensionAssociation`` to get more information about an
    association.
    """

    Id: Identifier | None
    ExtensionArn: Arn | None
    ResourceArn: Arn | None


ExtensionAssociationSummaries = list[ExtensionAssociationSummary]


class ExtensionAssociations(TypedDict, total=False):
    Items: ExtensionAssociationSummaries | None
    NextToken: NextToken | None


class ExtensionSummary(TypedDict, total=False):
    """Information about an extension. Call ``GetExtension`` to get more
    information about an extension.
    """

    Id: Id | None
    Name: Name | None
    VersionNumber: Integer | None
    Arn: Arn | None
    Description: Description | None


ExtensionSummaries = list[ExtensionSummary]


class Extensions(TypedDict, total=False):
    Items: ExtensionSummaries | None
    NextToken: NextToken | None


class GetApplicationRequest(ServiceRequest):
    ApplicationId: Id


class GetConfigurationProfileRequest(ServiceRequest):
    ApplicationId: Id
    ConfigurationProfileId: Id


class GetConfigurationRequest(ServiceRequest):
    Application: StringWithLengthBetween1And64
    Environment: StringWithLengthBetween1And64
    Configuration: StringWithLengthBetween1And64
    ClientId: StringWithLengthBetween1And64
    ClientConfigurationVersion: Version | None


class GetDeploymentRequest(ServiceRequest):
    ApplicationId: Id
    EnvironmentId: Id
    DeploymentNumber: Integer


class GetDeploymentStrategyRequest(ServiceRequest):
    DeploymentStrategyId: DeploymentStrategyId


class GetEnvironmentRequest(ServiceRequest):
    ApplicationId: Id
    EnvironmentId: Id


class GetExtensionAssociationRequest(ServiceRequest):
    ExtensionAssociationId: Id


class GetExtensionRequest(ServiceRequest):
    ExtensionIdentifier: Identifier
    VersionNumber: Integer | None


class GetHostedConfigurationVersionRequest(ServiceRequest):
    ApplicationId: Id
    ConfigurationProfileId: Id
    VersionNumber: Integer


class HostedConfigurationVersion(TypedDict, total=False):
    Content: Blob | IO[Blob] | Iterable[Blob] | None
    ApplicationId: Id | None
    ConfigurationProfileId: Id | None
    VersionNumber: Integer | None
    Description: Description | None
    ContentType: StringWithLengthBetween1And255 | None
    VersionLabel: VersionLabel | None
    KmsKeyArn: Arn | None


class HostedConfigurationVersionSummary(TypedDict, total=False):
    """Information about the configuration."""

    ApplicationId: Id | None
    ConfigurationProfileId: Id | None
    VersionNumber: Integer | None
    Description: Description | None
    ContentType: StringWithLengthBetween1And255 | None
    VersionLabel: VersionLabel | None
    KmsKeyArn: Arn | None


HostedConfigurationVersionSummaryList = list[HostedConfigurationVersionSummary]


class HostedConfigurationVersions(TypedDict, total=False):
    Items: HostedConfigurationVersionSummaryList | None
    NextToken: NextToken | None


class ListApplicationsRequest(ServiceRequest):
    MaxResults: MaxResults | None
    NextToken: NextToken | None


class ListConfigurationProfilesRequest(ServiceRequest):
    ApplicationId: Id
    MaxResults: MaxResults | None
    NextToken: NextToken | None
    Type: ConfigurationProfileType | None


class ListDeploymentStrategiesRequest(ServiceRequest):
    MaxResults: MaxResults | None
    NextToken: NextToken | None


class ListDeploymentsRequest(ServiceRequest):
    ApplicationId: Id
    EnvironmentId: Id
    MaxResults: MaxResults | None
    NextToken: NextToken | None


class ListEnvironmentsRequest(ServiceRequest):
    ApplicationId: Id
    MaxResults: MaxResults | None
    NextToken: NextToken | None


class ListExtensionAssociationsRequest(ServiceRequest):
    ResourceIdentifier: Arn | None
    ExtensionIdentifier: Identifier | None
    ExtensionVersionNumber: Integer | None
    MaxResults: MaxResults | None
    NextToken: NextToken | None


class ListExtensionsRequest(ServiceRequest):
    MaxResults: MaxResults | None
    NextToken: NextToken | None
    Name: QueryName | None


class ListHostedConfigurationVersionsRequest(ServiceRequest):
    ApplicationId: Id
    ConfigurationProfileId: Id
    MaxResults: MaxResults | None
    NextToken: NextToken | None
    VersionLabel: QueryName | None


class ListTagsForResourceRequest(ServiceRequest):
    ResourceArn: Arn


class ResourceTags(TypedDict, total=False):
    Tags: TagMap | None


class StartDeploymentRequest(ServiceRequest):
    ApplicationId: Id
    EnvironmentId: Id
    DeploymentStrategyId: DeploymentStrategyId
    ConfigurationProfileId: Id
    ConfigurationVersion: Version
    Description: Description | None
    Tags: TagMap | None
    KmsKeyIdentifier: KmsKeyIdentifier | None
    DynamicExtensionParameters: DynamicParameterMap | None


class StopDeploymentRequest(ServiceRequest):
    ApplicationId: Id
    EnvironmentId: Id
    DeploymentNumber: Integer
    AllowRevert: Boolean | None


TagKeyList = list[TagKey]


class TagResourceRequest(ServiceRequest):
    ResourceArn: Arn
    Tags: TagMap


class UntagResourceRequest(ServiceRequest):
    ResourceArn: Arn
    TagKeys: TagKeyList


class UpdateAccountSettingsRequest(ServiceRequest):
    DeletionProtection: DeletionProtectionSettings | None


class UpdateApplicationRequest(ServiceRequest):
    ApplicationId: Id
    Name: Name | None
    Description: Description | None


class UpdateConfigurationProfileRequest(ServiceRequest):
    ApplicationId: Id
    ConfigurationProfileId: Id
    Name: LongName | None
    Description: Description | None
    RetrievalRoleArn: RoleArn | None
    Validators: ValidatorList | None
    KmsKeyIdentifier: KmsKeyIdentifierOrEmpty | None


class UpdateDeploymentStrategyRequest(ServiceRequest):
    DeploymentStrategyId: DeploymentStrategyId
    Description: Description | None
    DeploymentDurationInMinutes: MinutesBetween0And24Hours | None
    FinalBakeTimeInMinutes: MinutesBetween0And24Hours | None
    GrowthFactor: GrowthFactor | None
    GrowthType: GrowthType | None


class UpdateEnvironmentRequest(ServiceRequest):
    ApplicationId: Id
    EnvironmentId: Id
    Name: Name | None
    Description: Description | None
    Monitors: MonitorList | None


class UpdateExtensionAssociationRequest(ServiceRequest):
    ExtensionAssociationId: Id
    Parameters: ParameterValueMap | None


class UpdateExtensionRequest(ServiceRequest):
    ExtensionIdentifier: Identifier
    Description: Description | None
    Actions: ActionsMap | None
    Parameters: ParameterMap | None
    VersionNumber: Integer | None


class ValidateConfigurationRequest(ServiceRequest):
    ApplicationId: Id
    ConfigurationProfileId: Id
    ConfigurationVersion: Version


class AppconfigApi:
    service: str = "appconfig"
    version: str = "2019-10-09"

    @handler("CreateApplication")
    def create_application(
        self,
        context: RequestContext,
        name: Name,
        description: Description | None = None,
        tags: TagMap | None = None,
        **kwargs,
    ) -> Application:
        """Creates an application. In AppConfig, an application is simply an
        organizational construct like a folder. This organizational construct
        has a relationship with some unit of executable code. For example, you
        could create an application called MyMobileApp to organize and manage
        configuration data for a mobile application installed by your users.

        :param name: A name for the application.
        :param description: A description of the application.
        :param tags: Metadata to assign to the application.
        :returns: Application
        :raises BadRequestException:
        :raises ServiceQuotaExceededException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("CreateConfigurationProfile", expand=False)
    def create_configuration_profile(
        self, context: RequestContext, request: CreateConfigurationProfileRequest, **kwargs
    ) -> ConfigurationProfile:
        """Creates a configuration profile, which is information that enables
        AppConfig to access the configuration source. Valid configuration
        sources include the following:

        -  Configuration data in YAML, JSON, and other formats stored in the
           AppConfig hosted configuration store

        -  Configuration data stored as objects in an Amazon Simple Storage
           Service (Amazon S3) bucket

        -  Pipelines stored in CodePipeline

        -  Secrets stored in Secrets Manager

        -  Standard and secure string parameters stored in Amazon Web Services
           Systems Manager Parameter Store

        -  Configuration data in SSM documents stored in the Systems Manager
           document store

        A configuration profile includes the following information:

        -  The URI location of the configuration data.

        -  The Identity and Access Management (IAM) role that provides access to
           the configuration data.

        -  A validator for the configuration data. Available validators include
           either a JSON Schema or an Amazon Web Services Lambda function.

        For more information, see `Create a Configuration and a Configuration
        Profile <http://docs.aws.amazon.com/appconfig/latest/userguide/appconfig-creating-configuration-and-profile.html>`__
        in the *AppConfig User Guide*.

        :param application_id: The application ID.
        :param name: A name for the configuration profile.
        :param location_uri: A URI to locate the configuration.
        :param description: A description of the configuration profile.
        :param retrieval_role_arn: The ARN of an IAM role with permission to access the configuration at
        the specified ``LocationUri``.
        :param validators: A list of methods for validating the configuration.
        :param tags: Metadata to assign to the configuration profile.
        :param type: The type of configurations contained in the profile.
        :param kms_key_identifier: The identifier for an Key Management Service key to encrypt new
        configuration data versions in the AppConfig hosted configuration store.
        :returns: ConfigurationProfile
        :raises BadRequestException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ServiceQuotaExceededException:
        """
        raise NotImplementedError

    @handler("CreateDeploymentStrategy")
    def create_deployment_strategy(
        self,
        context: RequestContext,
        name: Name,
        deployment_duration_in_minutes: MinutesBetween0And24Hours,
        growth_factor: GrowthFactor,
        description: Description | None = None,
        final_bake_time_in_minutes: MinutesBetween0And24Hours | None = None,
        growth_type: GrowthType | None = None,
        replicate_to: ReplicateTo | None = None,
        tags: TagMap | None = None,
        **kwargs,
    ) -> DeploymentStrategy:
        """Creates a deployment strategy that defines important criteria for
        rolling out your configuration to the designated targets. A deployment
        strategy includes the overall duration required, a percentage of targets
        to receive the deployment during each interval, an algorithm that
        defines how percentage grows, and bake time.

        :param name: A name for the deployment strategy.
        :param deployment_duration_in_minutes: Total amount of time for a deployment to last.
        :param growth_factor: The percentage of targets to receive a deployed configuration during
        each interval.
        :param description: A description of the deployment strategy.
        :param final_bake_time_in_minutes: Specifies the amount of time AppConfig monitors for Amazon CloudWatch
        alarms after the configuration has been deployed to 100% of its targets,
        before considering the deployment to be complete.
        :param growth_type: The algorithm used to define how percentage grows over time.
        :param replicate_to: Save the deployment strategy to a Systems Manager (SSM) document.
        :param tags: Metadata to assign to the deployment strategy.
        :returns: DeploymentStrategy
        :raises InternalServerException:
        :raises ServiceQuotaExceededException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("CreateEnvironment")
    def create_environment(
        self,
        context: RequestContext,
        application_id: Id,
        name: Name,
        description: Description | None = None,
        monitors: MonitorList | None = None,
        tags: TagMap | None = None,
        **kwargs,
    ) -> Environment:
        """Creates an environment. For each application, you define one or more
        environments. An environment is a deployment group of AppConfig targets,
        such as applications in a ``Beta`` or ``Production`` environment. You
        can also define environments for application subcomponents such as the
        ``Web``, ``Mobile`` and ``Back-end`` components for your application.
        You can configure Amazon CloudWatch alarms for each environment. The
        system monitors alarms during a configuration deployment. If an alarm is
        triggered, the system rolls back the configuration.

        :param application_id: The application ID.
        :param name: A name for the environment.
        :param description: A description of the environment.
        :param monitors: Amazon CloudWatch alarms to monitor during the deployment process.
        :param tags: Metadata to assign to the environment.
        :returns: Environment
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        :raises BadRequestException:
        :raises ServiceQuotaExceededException:
        """
        raise NotImplementedError

    @handler("CreateExtension")
    def create_extension(
        self,
        context: RequestContext,
        name: ExtensionOrParameterName,
        actions: ActionsMap,
        description: Description | None = None,
        parameters: ParameterMap | None = None,
        tags: TagMap | None = None,
        latest_version_number: Integer | None = None,
        **kwargs,
    ) -> Extension:
        """Creates an AppConfig extension. An extension augments your ability to
        inject logic or behavior at different points during the AppConfig
        workflow of creating or deploying a configuration.

        You can create your own extensions or use the Amazon Web Services
        authored extensions provided by AppConfig. For an AppConfig extension
        that uses Lambda, you must create a Lambda function to perform any
        computation and processing defined in the extension. If you plan to
        create custom versions of the Amazon Web Services authored notification
        extensions, you only need to specify an Amazon Resource Name (ARN) in
        the ``Uri`` field for the new extension version.

        -  For a custom EventBridge notification extension, enter the ARN of the
           EventBridge default events in the ``Uri`` field.

        -  For a custom Amazon SNS notification extension, enter the ARN of an
           Amazon SNS topic in the ``Uri`` field.

        -  For a custom Amazon SQS notification extension, enter the ARN of an
           Amazon SQS message queue in the ``Uri`` field.

        For more information about extensions, see `Extending
        workflows <https://docs.aws.amazon.com/appconfig/latest/userguide/working-with-appconfig-extensions.html>`__
        in the *AppConfig User Guide*.

        :param name: A name for the extension.
        :param actions: The actions defined in the extension.
        :param description: Information about the extension.
        :param parameters: The parameters accepted by the extension.
        :param tags: Adds one or more tags for the specified extension.
        :param latest_version_number: You can omit this field when you create an extension.
        :returns: Extension
        :raises BadRequestException:
        :raises ConflictException:
        :raises ServiceQuotaExceededException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("CreateExtensionAssociation")
    def create_extension_association(
        self,
        context: RequestContext,
        extension_identifier: Identifier,
        resource_identifier: Identifier,
        extension_version_number: Integer | None = None,
        parameters: ParameterValueMap | None = None,
        tags: TagMap | None = None,
        **kwargs,
    ) -> ExtensionAssociation:
        """When you create an extension or configure an Amazon Web Services
        authored extension, you associate the extension with an AppConfig
        application, environment, or configuration profile. For example, you can
        choose to run the ``AppConfig deployment events to Amazon SNS`` Amazon
        Web Services authored extension and receive notifications on an Amazon
        SNS topic anytime a configuration deployment is started for a specific
        application. Defining which extension to associate with an AppConfig
        resource is called an *extension association*. An extension association
        is a specified relationship between an extension and an AppConfig
        resource, such as an application or a configuration profile. For more
        information about extensions and associations, see `Extending
        workflows <https://docs.aws.amazon.com/appconfig/latest/userguide/working-with-appconfig-extensions.html>`__
        in the *AppConfig User Guide*.

        :param extension_identifier: The name, the ID, or the Amazon Resource Name (ARN) of the extension.
        :param resource_identifier: The ARN of an application, configuration profile, or environment.
        :param extension_version_number: The version number of the extension.
        :param parameters: The parameter names and values defined in the extensions.
        :param tags: Adds one or more tags for the specified extension association.
        :returns: ExtensionAssociation
        :raises BadRequestException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ServiceQuotaExceededException:
        """
        raise NotImplementedError

    @handler("CreateHostedConfigurationVersion")
    def create_hosted_configuration_version(
        self,
        context: RequestContext,
        application_id: Id,
        configuration_profile_id: Id,
        content: IO[Blob],
        content_type: StringWithLengthBetween1And255,
        description: Description | None = None,
        latest_version_number: Integer | None = None,
        version_label: VersionLabel | None = None,
        **kwargs,
    ) -> HostedConfigurationVersion:
        """Creates a new configuration in the AppConfig hosted configuration store.
        If you're creating a feature flag, we recommend you familiarize yourself
        with the JSON schema for feature flag data. For more information, see
        `Type reference for
        AWS.AppConfig.FeatureFlags <https://docs.aws.amazon.com/appconfig/latest/userguide/appconfig-creating-configuration-and-profile-feature-flags.html#appconfig-type-reference-feature-flags>`__
        in the *AppConfig User Guide*.

        :param application_id: The application ID.
        :param configuration_profile_id: The configuration profile ID.
        :param content: The configuration data, as bytes.
        :param content_type: A standard MIME type describing the format of the configuration content.
        :param description: A description of the configuration.
        :param latest_version_number: An optional locking token used to prevent race conditions from
        overwriting configuration updates when creating a new version.
        :param version_label: An optional, user-defined label for the AppConfig hosted configuration
        version.
        :returns: HostedConfigurationVersion
        :raises BadRequestException:
        :raises ServiceQuotaExceededException:
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises PayloadTooLargeException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("DeleteApplication")
    def delete_application(self, context: RequestContext, application_id: Id, **kwargs) -> None:
        """Deletes an application.

        :param application_id: The ID of the application to delete.
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("DeleteConfigurationProfile")
    def delete_configuration_profile(
        self,
        context: RequestContext,
        application_id: Id,
        configuration_profile_id: Id,
        deletion_protection_check: DeletionProtectionCheck | None = None,
        **kwargs,
    ) -> None:
        """Deletes a configuration profile.

        To prevent users from unintentionally deleting actively-used
        configuration profiles, enable `deletion
        protection <https://docs.aws.amazon.com/appconfig/latest/userguide/deletion-protection.html>`__.

        :param application_id: The application ID that includes the configuration profile you want to
        delete.
        :param configuration_profile_id: The ID of the configuration profile you want to delete.
        :param deletion_protection_check: A parameter to configure deletion protection.
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("DeleteDeploymentStrategy")
    def delete_deployment_strategy(
        self, context: RequestContext, deployment_strategy_id: DeploymentStrategyId, **kwargs
    ) -> None:
        """Deletes a deployment strategy.

        :param deployment_strategy_id: The ID of the deployment strategy you want to delete.
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("DeleteEnvironment")
    def delete_environment(
        self,
        context: RequestContext,
        environment_id: Id,
        application_id: Id,
        deletion_protection_check: DeletionProtectionCheck | None = None,
        **kwargs,
    ) -> None:
        """Deletes an environment.

        To prevent users from unintentionally deleting actively-used
        environments, enable `deletion
        protection <https://docs.aws.amazon.com/appconfig/latest/userguide/deletion-protection.html>`__.

        :param environment_id: The ID of the environment that you want to delete.
        :param application_id: The application ID that includes the environment that you want to
        delete.
        :param deletion_protection_check: A parameter to configure deletion protection.
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("DeleteExtension")
    def delete_extension(
        self,
        context: RequestContext,
        extension_identifier: Identifier,
        version_number: Integer | None = None,
        **kwargs,
    ) -> None:
        """Deletes an AppConfig extension. You must delete all associations to an
        extension before you delete the extension.

        :param extension_identifier: The name, ID, or Amazon Resource Name (ARN) of the extension you want to
        delete.
        :param version_number: A specific version of an extension to delete.
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("DeleteExtensionAssociation")
    def delete_extension_association(
        self, context: RequestContext, extension_association_id: Id, **kwargs
    ) -> None:
        """Deletes an extension association. This action doesn't delete extensions
        defined in the association.

        :param extension_association_id: The ID of the extension association to delete.
        :raises BadRequestException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("DeleteHostedConfigurationVersion")
    def delete_hosted_configuration_version(
        self,
        context: RequestContext,
        application_id: Id,
        configuration_profile_id: Id,
        version_number: Integer,
        **kwargs,
    ) -> None:
        """Deletes a version of a configuration from the AppConfig hosted
        configuration store.

        :param application_id: The application ID.
        :param configuration_profile_id: The configuration profile ID.
        :param version_number: The versions number to delete.
        :raises BadRequestException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("GetAccountSettings")
    def get_account_settings(self, context: RequestContext, **kwargs) -> AccountSettings:
        """Returns information about the status of the ``DeletionProtection``
        parameter.

        :returns: AccountSettings
        :raises InternalServerException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetApplication")
    def get_application(self, context: RequestContext, application_id: Id, **kwargs) -> Application:
        """Retrieves information about an application.

        :param application_id: The ID of the application you want to get.
        :returns: Application
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetConfiguration")
    def get_configuration(
        self,
        context: RequestContext,
        application: StringWithLengthBetween1And64,
        environment: StringWithLengthBetween1And64,
        configuration: StringWithLengthBetween1And64,
        client_id: StringWithLengthBetween1And64,
        client_configuration_version: Version | None = None,
        **kwargs,
    ) -> Configuration:
        """(Deprecated) Retrieves the latest deployed configuration.

        Note the following important information.

        -  This API action is deprecated. Calls to receive configuration data
           should use the
           `StartConfigurationSession <https://docs.aws.amazon.com/appconfig/2019-10-09/APIReference/API_appconfigdata_StartConfigurationSession.html>`__
           and
           `GetLatestConfiguration <https://docs.aws.amazon.com/appconfig/2019-10-09/APIReference/API_appconfigdata_GetLatestConfiguration.html>`__
           APIs instead.

        -  GetConfiguration is a priced call. For more information, see
           `Pricing <https://aws.amazon.com/systems-manager/pricing/>`__.

        :param application: The application to get.
        :param environment: The environment to get.
        :param configuration: The configuration to get.
        :param client_id: The clientId parameter in the following command is a unique,
        user-specified ID to identify the client for the configuration.
        :param client_configuration_version: The configuration version returned in the most recent GetConfiguration
        response.
        :returns: Configuration
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetConfigurationProfile")
    def get_configuration_profile(
        self, context: RequestContext, application_id: Id, configuration_profile_id: Id, **kwargs
    ) -> ConfigurationProfile:
        """Retrieves information about a configuration profile.

        :param application_id: The ID of the application that includes the configuration profile you
        want to get.
        :param configuration_profile_id: The ID of the configuration profile that you want to get.
        :returns: ConfigurationProfile
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetDeployment")
    def get_deployment(
        self,
        context: RequestContext,
        application_id: Id,
        environment_id: Id,
        deployment_number: Integer,
        **kwargs,
    ) -> Deployment:
        """Retrieves information about a configuration deployment.

        :param application_id: The ID of the application that includes the deployment you want to get.
        :param environment_id: The ID of the environment that includes the deployment you want to get.
        :param deployment_number: The sequence number of the deployment.
        :returns: Deployment
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetDeploymentStrategy")
    def get_deployment_strategy(
        self, context: RequestContext, deployment_strategy_id: DeploymentStrategyId, **kwargs
    ) -> DeploymentStrategy:
        """Retrieves information about a deployment strategy. A deployment strategy
        defines important criteria for rolling out your configuration to the
        designated targets. A deployment strategy includes the overall duration
        required, a percentage of targets to receive the deployment during each
        interval, an algorithm that defines how percentage grows, and bake time.

        :param deployment_strategy_id: The ID of the deployment strategy to get.
        :returns: DeploymentStrategy
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetEnvironment")
    def get_environment(
        self, context: RequestContext, application_id: Id, environment_id: Id, **kwargs
    ) -> Environment:
        """Retrieves information about an environment. An environment is a
        deployment group of AppConfig applications, such as applications in a
        ``Production`` environment or in an ``EU_Region`` environment. Each
        configuration deployment targets an environment. You can enable one or
        more Amazon CloudWatch alarms for an environment. If an alarm is
        triggered during a deployment, AppConfig roles back the configuration.

        :param application_id: The ID of the application that includes the environment you want to get.
        :param environment_id: The ID of the environment that you want to get.
        :returns: Environment
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetExtension")
    def get_extension(
        self,
        context: RequestContext,
        extension_identifier: Identifier,
        version_number: Integer | None = None,
        **kwargs,
    ) -> Extension:
        """Returns information about an AppConfig extension.

        :param extension_identifier: The name, the ID, or the Amazon Resource Name (ARN) of the extension.
        :param version_number: The extension version number.
        :returns: Extension
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("GetExtensionAssociation")
    def get_extension_association(
        self, context: RequestContext, extension_association_id: Id, **kwargs
    ) -> ExtensionAssociation:
        """Returns information about an AppConfig extension association. For more
        information about extensions and associations, see `Extending
        workflows <https://docs.aws.amazon.com/appconfig/latest/userguide/working-with-appconfig-extensions.html>`__
        in the *AppConfig User Guide*.

        :param extension_association_id: The extension association ID to get.
        :returns: ExtensionAssociation
        :raises BadRequestException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("GetHostedConfigurationVersion")
    def get_hosted_configuration_version(
        self,
        context: RequestContext,
        application_id: Id,
        configuration_profile_id: Id,
        version_number: Integer,
        **kwargs,
    ) -> HostedConfigurationVersion:
        """Retrieves information about a specific configuration version.

        :param application_id: The application ID.
        :param configuration_profile_id: The configuration profile ID.
        :param version_number: The version.
        :returns: HostedConfigurationVersion
        :raises BadRequestException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("ListApplications")
    def list_applications(
        self,
        context: RequestContext,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> Applications:
        """Lists all applications in your Amazon Web Services account.

        :param max_results: The maximum number of items to return for this call.
        :param next_token: A token to start the list.
        :returns: Applications
        :raises InternalServerException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("ListConfigurationProfiles", expand=False)
    def list_configuration_profiles(
        self, context: RequestContext, request: ListConfigurationProfilesRequest, **kwargs
    ) -> ConfigurationProfiles:
        """Lists the configuration profiles for an application.

        :param application_id: The application ID.
        :param max_results: The maximum number of items to return for this call.
        :param next_token: A token to start the list.
        :param type: A filter based on the type of configurations that the configuration
        profile contains.
        :returns: ConfigurationProfiles
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("ListDeploymentStrategies")
    def list_deployment_strategies(
        self,
        context: RequestContext,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> DeploymentStrategies:
        """Lists deployment strategies.

        :param max_results: The maximum number of items to return for this call.
        :param next_token: A token to start the list.
        :returns: DeploymentStrategies
        :raises InternalServerException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("ListDeployments")
    def list_deployments(
        self,
        context: RequestContext,
        application_id: Id,
        environment_id: Id,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> Deployments:
        """Lists the deployments for an environment in descending deployment number
        order.

        :param application_id: The application ID.
        :param environment_id: The environment ID.
        :param max_results: The maximum number of items that may be returned for this call.
        :param next_token: The token returned by a prior call to this operation indicating the next
        set of results to be returned.
        :returns: Deployments
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("ListEnvironments")
    def list_environments(
        self,
        context: RequestContext,
        application_id: Id,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> Environments:
        """Lists the environments for an application.

        :param application_id: The application ID.
        :param max_results: The maximum number of items to return for this call.
        :param next_token: A token to start the list.
        :returns: Environments
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("ListExtensionAssociations")
    def list_extension_associations(
        self,
        context: RequestContext,
        resource_identifier: Arn | None = None,
        extension_identifier: Identifier | None = None,
        extension_version_number: Integer | None = None,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ExtensionAssociations:
        """Lists all AppConfig extension associations in the account. For more
        information about extensions and associations, see `Extending
        workflows <https://docs.aws.amazon.com/appconfig/latest/userguide/working-with-appconfig-extensions.html>`__
        in the *AppConfig User Guide*.

        :param resource_identifier: The ARN of an application, configuration profile, or environment.
        :param extension_identifier: The name, the ID, or the Amazon Resource Name (ARN) of the extension.
        :param extension_version_number: The version number for the extension defined in the association.
        :param max_results: The maximum number of items to return for this call.
        :param next_token: A token to start the list.
        :returns: ExtensionAssociations
        :raises InternalServerException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("ListExtensions")
    def list_extensions(
        self,
        context: RequestContext,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        name: QueryName | None = None,
        **kwargs,
    ) -> Extensions:
        """Lists all custom and Amazon Web Services authored AppConfig extensions
        in the account. For more information about extensions, see `Extending
        workflows <https://docs.aws.amazon.com/appconfig/latest/userguide/working-with-appconfig-extensions.html>`__
        in the *AppConfig User Guide*.

        :param max_results: The maximum number of items to return for this call.
        :param next_token: A token to start the list.
        :param name: The extension name.
        :returns: Extensions
        :raises InternalServerException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("ListHostedConfigurationVersions")
    def list_hosted_configuration_versions(
        self,
        context: RequestContext,
        application_id: Id,
        configuration_profile_id: Id,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        version_label: QueryName | None = None,
        **kwargs,
    ) -> HostedConfigurationVersions:
        """Lists configurations stored in the AppConfig hosted configuration store
        by version.

        :param application_id: The application ID.
        :param configuration_profile_id: The configuration profile ID.
        :param max_results: The maximum number of items to return for this call.
        :param next_token: A token to start the list.
        :param version_label: An optional filter that can be used to specify the version label of an
        AppConfig hosted configuration version.
        :returns: HostedConfigurationVersions
        :raises BadRequestException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("ListTagsForResource")
    def list_tags_for_resource(
        self, context: RequestContext, resource_arn: Arn, **kwargs
    ) -> ResourceTags:
        """Retrieves the list of key-value tags assigned to the resource.

        :param resource_arn: The resource ARN.
        :returns: ResourceTags
        :raises ResourceNotFoundException:
        :raises BadRequestException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("StartDeployment")
    def start_deployment(
        self,
        context: RequestContext,
        application_id: Id,
        environment_id: Id,
        deployment_strategy_id: DeploymentStrategyId,
        configuration_profile_id: Id,
        configuration_version: Version,
        description: Description | None = None,
        tags: TagMap | None = None,
        kms_key_identifier: KmsKeyIdentifier | None = None,
        dynamic_extension_parameters: DynamicParameterMap | None = None,
        **kwargs,
    ) -> Deployment:
        """Starts a deployment.

        :param application_id: The application ID.
        :param environment_id: The environment ID.
        :param deployment_strategy_id: The deployment strategy ID.
        :param configuration_profile_id: The configuration profile ID.
        :param configuration_version: The configuration version to deploy.
        :param description: A description of the deployment.
        :param tags: Metadata to assign to the deployment.
        :param kms_key_identifier: The KMS key identifier (key ID, key alias, or key ARN).
        :param dynamic_extension_parameters: A map of dynamic extension parameter names to values to pass to
        associated extensions with ``PRE_START_DEPLOYMENT`` actions.
        :returns: Deployment
        :raises BadRequestException:
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("StopDeployment")
    def stop_deployment(
        self,
        context: RequestContext,
        application_id: Id,
        environment_id: Id,
        deployment_number: Integer,
        allow_revert: Boolean | None = None,
        **kwargs,
    ) -> Deployment:
        """Stops a deployment. This API action works only on deployments that have
        a status of ``DEPLOYING``, unless an ``AllowRevert`` parameter is
        supplied. If the ``AllowRevert`` parameter is supplied, the status of an
        in-progress deployment will be ``ROLLED_BACK``. The status of a
        completed deployment will be ``REVERTED``. AppConfig only allows a
        revert within 72 hours of deployment completion.

        :param application_id: The application ID.
        :param environment_id: The environment ID.
        :param deployment_number: The sequence number of the deployment.
        :param allow_revert: A Boolean that enables AppConfig to rollback a ``COMPLETED`` deployment
        to the previous configuration version.
        :returns: Deployment
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises BadRequestException:
        """
        raise NotImplementedError

    @handler("TagResource")
    def tag_resource(
        self, context: RequestContext, resource_arn: Arn, tags: TagMap, **kwargs
    ) -> None:
        """Assigns metadata to an AppConfig resource. Tags help organize and
        categorize your AppConfig resources. Each tag consists of a key and an
        optional value, both of which you define. You can specify a maximum of
        50 tags for a resource.

        :param resource_arn: The ARN of the resource for which to retrieve tags.
        :param tags: The key-value string map.
        :raises ResourceNotFoundException:
        :raises BadRequestException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("UntagResource")
    def untag_resource(
        self, context: RequestContext, resource_arn: Arn, tag_keys: TagKeyList, **kwargs
    ) -> None:
        """Deletes a tag key and value from an AppConfig resource.

        :param resource_arn: The ARN of the resource for which to remove tags.
        :param tag_keys: The tag keys to delete.
        :raises ResourceNotFoundException:
        :raises BadRequestException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("UpdateAccountSettings")
    def update_account_settings(
        self,
        context: RequestContext,
        deletion_protection: DeletionProtectionSettings | None = None,
        **kwargs,
    ) -> AccountSettings:
        """Updates the value of the ``DeletionProtection`` parameter.

        :param deletion_protection: A parameter to configure deletion protection.
        :returns: AccountSettings
        :raises BadRequestException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("UpdateApplication")
    def update_application(
        self,
        context: RequestContext,
        application_id: Id,
        name: Name | None = None,
        description: Description | None = None,
        **kwargs,
    ) -> Application:
        """Updates an application.

        :param application_id: The application ID.
        :param name: The name of the application.
        :param description: A description of the application.
        :returns: Application
        :raises BadRequestException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("UpdateConfigurationProfile")
    def update_configuration_profile(
        self,
        context: RequestContext,
        application_id: Id,
        configuration_profile_id: Id,
        name: LongName | None = None,
        description: Description | None = None,
        retrieval_role_arn: RoleArn | None = None,
        validators: ValidatorList | None = None,
        kms_key_identifier: KmsKeyIdentifierOrEmpty | None = None,
        **kwargs,
    ) -> ConfigurationProfile:
        """Updates a configuration profile.

        :param application_id: The application ID.
        :param configuration_profile_id: The ID of the configuration profile.
        :param name: The name of the configuration profile.
        :param description: A description of the configuration profile.
        :param retrieval_role_arn: The ARN of an IAM role with permission to access the configuration at
        the specified ``LocationUri``.
        :param validators: A list of methods for validating the configuration.
        :param kms_key_identifier: The identifier for a Key Management Service key to encrypt new
        configuration data versions in the AppConfig hosted configuration store.
        :returns: ConfigurationProfile
        :raises BadRequestException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("UpdateDeploymentStrategy")
    def update_deployment_strategy(
        self,
        context: RequestContext,
        deployment_strategy_id: DeploymentStrategyId,
        description: Description | None = None,
        deployment_duration_in_minutes: MinutesBetween0And24Hours | None = None,
        final_bake_time_in_minutes: MinutesBetween0And24Hours | None = None,
        growth_factor: GrowthFactor | None = None,
        growth_type: GrowthType | None = None,
        **kwargs,
    ) -> DeploymentStrategy:
        """Updates a deployment strategy.

        :param deployment_strategy_id: The deployment strategy ID.
        :param description: A description of the deployment strategy.
        :param deployment_duration_in_minutes: Total amount of time for a deployment to last.
        :param final_bake_time_in_minutes: The amount of time that AppConfig monitors for alarms before considering
        the deployment to be complete and no longer eligible for automatic
        rollback.
        :param growth_factor: The percentage of targets to receive a deployed configuration during
        each interval.
        :param growth_type: The algorithm used to define how percentage grows over time.
        :returns: DeploymentStrategy
        :raises BadRequestException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("UpdateEnvironment")
    def update_environment(
        self,
        context: RequestContext,
        application_id: Id,
        environment_id: Id,
        name: Name | None = None,
        description: Description | None = None,
        monitors: MonitorList | None = None,
        **kwargs,
    ) -> Environment:
        """Updates an environment.

        :param application_id: The application ID.
        :param environment_id: The environment ID.
        :param name: The name of the environment.
        :param description: A description of the environment.
        :param monitors: Amazon CloudWatch alarms to monitor during the deployment process.
        :returns: Environment
        :raises BadRequestException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("UpdateExtension")
    def update_extension(
        self,
        context: RequestContext,
        extension_identifier: Identifier,
        description: Description | None = None,
        actions: ActionsMap | None = None,
        parameters: ParameterMap | None = None,
        version_number: Integer | None = None,
        **kwargs,
    ) -> Extension:
        """Updates an AppConfig extension. For more information about extensions,
        see `Extending
        workflows <https://docs.aws.amazon.com/appconfig/latest/userguide/working-with-appconfig-extensions.html>`__
        in the *AppConfig User Guide*.

        :param extension_identifier: The name, the ID, or the Amazon Resource Name (ARN) of the extension.
        :param description: Information about the extension.
        :param actions: The actions defined in the extension.
        :param parameters: One or more parameters for the actions called by the extension.
        :param version_number: The extension version number.
        :returns: Extension
        :raises BadRequestException:
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("UpdateExtensionAssociation")
    def update_extension_association(
        self,
        context: RequestContext,
        extension_association_id: Id,
        parameters: ParameterValueMap | None = None,
        **kwargs,
    ) -> ExtensionAssociation:
        """Updates an association. For more information about extensions and
        associations, see `Extending
        workflows <https://docs.aws.amazon.com/appconfig/latest/userguide/working-with-appconfig-extensions.html>`__
        in the *AppConfig User Guide*.

        :param extension_association_id: The system-generated ID for the association.
        :param parameters: The parameter names and values defined in the extension.
        :returns: ExtensionAssociation
        :raises BadRequestException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("ValidateConfiguration")
    def validate_configuration(
        self,
        context: RequestContext,
        application_id: Id,
        configuration_profile_id: Id,
        configuration_version: Version,
        **kwargs,
    ) -> None:
        """Uses the validators in a configuration profile to validate a
        configuration.

        :param application_id: The application ID.
        :param configuration_profile_id: The configuration profile ID.
        :param configuration_version: The version of the configuration to validate.
        :raises BadRequestException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        """
        raise NotImplementedError
