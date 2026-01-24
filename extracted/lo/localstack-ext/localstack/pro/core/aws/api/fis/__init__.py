from datetime import datetime
from enum import StrEnum
from typing import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

ActionDescription = str
ActionId = str
ActionParameterDescription = str
ActionParameterName = str
ActionParameterRequired = bool
ActionTargetName = str
ClientToken = str
CloudWatchLogGroupArn = str
ExceptionMessage = str
ExperimentActionDescription = str
ExperimentActionName = str
ExperimentActionParameter = str
ExperimentActionParameterName = str
ExperimentActionStartAfter = str
ExperimentActionStatusReason = str
ExperimentActionTargetName = str
ExperimentErrorAccountId = str
ExperimentErrorCode = str
ExperimentErrorLocation = str
ExperimentId = str
ExperimentReportErrorCode = str
ExperimentReportReason = str
ExperimentReportS3ReportArn = str
ExperimentReportS3ReportType = str
ExperimentStatusReason = str
ExperimentTargetFilterPath = str
ExperimentTargetFilterValue = str
ExperimentTargetName = str
ExperimentTargetParameterName = str
ExperimentTargetParameterValue = str
ExperimentTargetSelectionMode = str
ExperimentTemplateActionDescription = str
ExperimentTemplateActionName = str
ExperimentTemplateActionParameter = str
ExperimentTemplateActionParameterName = str
ExperimentTemplateActionStartAfter = str
ExperimentTemplateActionTargetName = str
ExperimentTemplateDescription = str
ExperimentTemplateId = str
ExperimentTemplateTargetFilterPath = str
ExperimentTemplateTargetFilterValue = str
ExperimentTemplateTargetName = str
ExperimentTemplateTargetParameterName = str
ExperimentTemplateTargetParameterValue = str
ExperimentTemplateTargetSelectionMode = str
ListActionsMaxResults = int
ListExperimentResolvedTargetsMaxResults = int
ListExperimentTemplatesMaxResults = int
ListExperimentsMaxResults = int
ListTargetAccountConfigurationsMaxResults = int
ListTargetResourceTypesMaxResults = int
LogSchemaVersion = int
NextToken = str
ReportConfigurationCloudWatchDashboardIdentifier = str
ReportConfigurationDuration = str
ReportConfigurationS3OutputPrefix = str
ResourceArn = str
RoleArn = str
S3BucketName = str
S3ObjectKey = str
SafetyLeverId = str
SafetyLeverStatusReason = str
StopConditionSource = str
StopConditionValue = str
TagKey = str
TagValue = str
TargetAccountConfigurationDescription = str
TargetAccountId = str
TargetInformationKey = str
TargetInformationValue = str
TargetName = str
TargetResourceTypeDescription = str
TargetResourceTypeId = str
TargetResourceTypeParameterDescription = str
TargetResourceTypeParameterName = str
TargetResourceTypeParameterRequired = bool


class AccountTargeting(StrEnum):
    single_account = "single-account"
    multi_account = "multi-account"


class ActionsMode(StrEnum):
    skip_all = "skip-all"
    run_all = "run-all"


class EmptyTargetResolutionMode(StrEnum):
    fail = "fail"
    skip = "skip"


class ExperimentActionStatus(StrEnum):
    pending = "pending"
    initiating = "initiating"
    running = "running"
    completed = "completed"
    cancelled = "cancelled"
    stopping = "stopping"
    stopped = "stopped"
    failed = "failed"
    skipped = "skipped"


class ExperimentReportStatus(StrEnum):
    pending = "pending"
    running = "running"
    completed = "completed"
    cancelled = "cancelled"
    failed = "failed"


class ExperimentStatus(StrEnum):
    pending = "pending"
    initiating = "initiating"
    running = "running"
    completed = "completed"
    stopping = "stopping"
    stopped = "stopped"
    failed = "failed"
    cancelled = "cancelled"


class SafetyLeverStatus(StrEnum):
    disengaged = "disengaged"
    engaged = "engaged"
    engaging = "engaging"


class SafetyLeverStatusInput(StrEnum):
    disengaged = "disengaged"
    engaged = "engaged"


class ConflictException(ServiceException):
    """The request could not be processed because of a conflict."""

    code: str = "ConflictException"
    sender_fault: bool = False
    status_code: int = 409


class ResourceNotFoundException(ServiceException):
    """The specified resource cannot be found."""

    code: str = "ResourceNotFoundException"
    sender_fault: bool = False
    status_code: int = 404


class ServiceQuotaExceededException(ServiceException):
    """You have exceeded your service quota."""

    code: str = "ServiceQuotaExceededException"
    sender_fault: bool = False
    status_code: int = 402


class ValidationException(ServiceException):
    """The specified input is not valid, or fails to satisfy the constraints
    for the request.
    """

    code: str = "ValidationException"
    sender_fault: bool = False
    status_code: int = 400


TagMap = dict[TagKey, TagValue]


class ActionTarget(TypedDict, total=False):
    """Describes a target for an action."""

    resourceType: TargetResourceTypeId | None


ActionTargetMap = dict[ActionTargetName, ActionTarget]


class ActionParameter(TypedDict, total=False):
    """Describes a parameter for an action."""

    description: ActionParameterDescription | None
    required: ActionParameterRequired | None


ActionParameterMap = dict[ActionParameterName, ActionParameter]


class Action(TypedDict, total=False):
    """Describes an action. For more information, see `FIS
    actions <https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html>`__
    in the *Fault Injection Service User Guide*.
    """

    id: ActionId | None
    arn: ResourceArn | None
    description: ActionDescription | None
    parameters: ActionParameterMap | None
    targets: ActionTargetMap | None
    tags: TagMap | None


class ActionSummary(TypedDict, total=False):
    """Provides a summary of an action."""

    id: ActionId | None
    arn: ResourceArn | None
    description: ActionDescription | None
    targets: ActionTargetMap | None
    tags: TagMap | None


ActionSummaryList = list[ActionSummary]
ExperimentTemplateActionStartAfterList = list[ExperimentTemplateActionStartAfter]
ExperimentTemplateActionTargetMap = dict[
    ExperimentTemplateActionTargetName, ExperimentTemplateTargetName
]
ExperimentTemplateActionParameterMap = dict[
    ExperimentTemplateActionParameterName, ExperimentTemplateActionParameter
]


class CreateExperimentTemplateActionInput(TypedDict, total=False):
    """Specifies an action for an experiment template.

    For more information, see
    `Actions <https://docs.aws.amazon.com/fis/latest/userguide/actions.html>`__
    in the *Fault Injection Service User Guide*.
    """

    actionId: ActionId
    description: ExperimentTemplateActionDescription | None
    parameters: ExperimentTemplateActionParameterMap | None
    targets: ExperimentTemplateActionTargetMap | None
    startAfter: ExperimentTemplateActionStartAfterList | None


CreateExperimentTemplateActionInputMap = dict[
    ExperimentTemplateActionName, CreateExperimentTemplateActionInput
]


class CreateExperimentTemplateExperimentOptionsInput(TypedDict, total=False):
    """Specifies experiment options for an experiment template."""

    accountTargeting: AccountTargeting | None
    emptyTargetResolutionMode: EmptyTargetResolutionMode | None


class ExperimentTemplateS3LogConfigurationInput(TypedDict, total=False):
    """Specifies the configuration for experiment logging to Amazon S3."""

    bucketName: S3BucketName
    prefix: S3ObjectKey | None


class ExperimentTemplateCloudWatchLogsLogConfigurationInput(TypedDict, total=False):
    """Specifies the configuration for experiment logging to Amazon CloudWatch
    Logs.
    """

    logGroupArn: CloudWatchLogGroupArn


class CreateExperimentTemplateLogConfigurationInput(TypedDict, total=False):
    """Specifies the configuration for experiment logging."""

    cloudWatchLogsConfiguration: ExperimentTemplateCloudWatchLogsLogConfigurationInput | None
    s3Configuration: ExperimentTemplateS3LogConfigurationInput | None
    logSchemaVersion: LogSchemaVersion


class ReportConfigurationCloudWatchDashboardInput(TypedDict, total=False):
    """Specifies the CloudWatch dashboard for the experiment report."""

    dashboardIdentifier: ReportConfigurationCloudWatchDashboardIdentifier | None


ReportConfigurationCloudWatchDashboardInputList = list[ReportConfigurationCloudWatchDashboardInput]


class ExperimentTemplateReportConfigurationDataSourcesInput(TypedDict, total=False):
    """Specifies the data sources for the experiment report."""

    cloudWatchDashboards: ReportConfigurationCloudWatchDashboardInputList | None


class ReportConfigurationS3OutputInput(TypedDict, total=False):
    """Specifies the S3 destination for the experiment report."""

    bucketName: S3BucketName | None
    prefix: ReportConfigurationS3OutputPrefix | None


class ExperimentTemplateReportConfigurationOutputsInput(TypedDict, total=False):
    """Specifies the outputs for the experiment templates."""

    s3Configuration: ReportConfigurationS3OutputInput | None


class CreateExperimentTemplateReportConfigurationInput(TypedDict, total=False):
    """Specifies the configuration for experiment reports."""

    outputs: ExperimentTemplateReportConfigurationOutputsInput | None
    dataSources: ExperimentTemplateReportConfigurationDataSourcesInput | None
    preExperimentDuration: ReportConfigurationDuration | None
    postExperimentDuration: ReportConfigurationDuration | None


ExperimentTemplateTargetParameterMap = dict[
    ExperimentTemplateTargetParameterName, ExperimentTemplateTargetParameterValue
]
ExperimentTemplateTargetFilterValues = list[ExperimentTemplateTargetFilterValue]


class ExperimentTemplateTargetInputFilter(TypedDict, total=False):
    """Specifies a filter used for the target resource input in an experiment
    template.

    For more information, see `Resource
    filters <https://docs.aws.amazon.com/fis/latest/userguide/targets.html#target-filters>`__
    in the *Fault Injection Service User Guide*.
    """

    path: ExperimentTemplateTargetFilterPath
    values: ExperimentTemplateTargetFilterValues


ExperimentTemplateTargetFilterInputList = list[ExperimentTemplateTargetInputFilter]
ResourceArnList = list[ResourceArn]


class CreateExperimentTemplateTargetInput(TypedDict, total=False):
    """Specifies a target for an experiment. You must specify at least one
    Amazon Resource Name (ARN) or at least one resource tag. You cannot
    specify both ARNs and tags.

    For more information, see
    `Targets <https://docs.aws.amazon.com/fis/latest/userguide/targets.html>`__
    in the *Fault Injection Service User Guide*.
    """

    resourceType: TargetResourceTypeId
    resourceArns: ResourceArnList | None
    resourceTags: TagMap | None
    filters: ExperimentTemplateTargetFilterInputList | None
    selectionMode: ExperimentTemplateTargetSelectionMode
    parameters: ExperimentTemplateTargetParameterMap | None


CreateExperimentTemplateTargetInputMap = dict[
    ExperimentTemplateTargetName, CreateExperimentTemplateTargetInput
]


class CreateExperimentTemplateStopConditionInput(TypedDict, total=False):
    """Specifies a stop condition for an experiment template."""

    source: StopConditionSource
    value: StopConditionValue | None


CreateExperimentTemplateStopConditionInputList = list[CreateExperimentTemplateStopConditionInput]


class CreateExperimentTemplateRequest(ServiceRequest):
    clientToken: ClientToken
    description: ExperimentTemplateDescription
    stopConditions: CreateExperimentTemplateStopConditionInputList
    targets: CreateExperimentTemplateTargetInputMap | None
    actions: CreateExperimentTemplateActionInputMap
    roleArn: RoleArn
    tags: TagMap | None
    logConfiguration: CreateExperimentTemplateLogConfigurationInput | None
    experimentOptions: CreateExperimentTemplateExperimentOptionsInput | None
    experimentReportConfiguration: CreateExperimentTemplateReportConfigurationInput | None


class ExperimentTemplateReportConfigurationCloudWatchDashboard(TypedDict, total=False):
    """The CloudWatch dashboards to include as data sources in the experiment
    report.
    """

    dashboardIdentifier: ReportConfigurationCloudWatchDashboardIdentifier | None


ExperimentTemplateReportConfigurationCloudWatchDashboardList = list[
    ExperimentTemplateReportConfigurationCloudWatchDashboard
]


class ExperimentTemplateReportConfigurationDataSources(TypedDict, total=False):
    """Describes the data sources for the experiment report."""

    cloudWatchDashboards: ExperimentTemplateReportConfigurationCloudWatchDashboardList | None


class ReportConfigurationS3Output(TypedDict, total=False):
    """Describes the S3 destination for the experiment report."""

    bucketName: S3BucketName | None
    prefix: ReportConfigurationS3OutputPrefix | None


class ExperimentTemplateReportConfigurationOutputs(TypedDict, total=False):
    """The output destinations of the experiment report."""

    s3Configuration: ReportConfigurationS3Output | None


class ExperimentTemplateReportConfiguration(TypedDict, total=False):
    """Describes the experiment report configuration. For more information, see
    `Experiment report configurations for AWS
    FIS <https://docs.aws.amazon.com/fis/latest/userguide/experiment-report-configuration>`__.
    """

    outputs: ExperimentTemplateReportConfigurationOutputs | None
    dataSources: ExperimentTemplateReportConfigurationDataSources | None
    preExperimentDuration: ReportConfigurationDuration | None
    postExperimentDuration: ReportConfigurationDuration | None


TargetAccountConfigurationsCount = int


class ExperimentTemplateExperimentOptions(TypedDict, total=False):
    """Describes the experiment options for an experiment template."""

    accountTargeting: AccountTargeting | None
    emptyTargetResolutionMode: EmptyTargetResolutionMode | None


class ExperimentTemplateS3LogConfiguration(TypedDict, total=False):
    """Describes the configuration for experiment logging to Amazon S3."""

    bucketName: S3BucketName | None
    prefix: S3ObjectKey | None


class ExperimentTemplateCloudWatchLogsLogConfiguration(TypedDict, total=False):
    """Describes the configuration for experiment logging to Amazon CloudWatch
    Logs.
    """

    logGroupArn: CloudWatchLogGroupArn | None


class ExperimentTemplateLogConfiguration(TypedDict, total=False):
    """Describes the configuration for experiment logging."""

    cloudWatchLogsConfiguration: ExperimentTemplateCloudWatchLogsLogConfiguration | None
    s3Configuration: ExperimentTemplateS3LogConfiguration | None
    logSchemaVersion: LogSchemaVersion | None


LastUpdateTime = datetime
CreationTime = datetime


class ExperimentTemplateStopCondition(TypedDict, total=False):
    """Describes a stop condition for an experiment template."""

    source: StopConditionSource | None
    value: StopConditionValue | None


ExperimentTemplateStopConditionList = list[ExperimentTemplateStopCondition]


class ExperimentTemplateAction(TypedDict, total=False):
    """Describes an action for an experiment template."""

    actionId: ActionId | None
    description: ExperimentTemplateActionDescription | None
    parameters: ExperimentTemplateActionParameterMap | None
    targets: ExperimentTemplateActionTargetMap | None
    startAfter: ExperimentTemplateActionStartAfterList | None


ExperimentTemplateActionMap = dict[ExperimentTemplateActionName, ExperimentTemplateAction]


class ExperimentTemplateTargetFilter(TypedDict, total=False):
    """Describes a filter used for the target resources in an experiment
    template.
    """

    path: ExperimentTemplateTargetFilterPath | None
    values: ExperimentTemplateTargetFilterValues | None


ExperimentTemplateTargetFilterList = list[ExperimentTemplateTargetFilter]


class ExperimentTemplateTarget(TypedDict, total=False):
    """Describes a target for an experiment template."""

    resourceType: TargetResourceTypeId | None
    resourceArns: ResourceArnList | None
    resourceTags: TagMap | None
    filters: ExperimentTemplateTargetFilterList | None
    selectionMode: ExperimentTemplateTargetSelectionMode | None
    parameters: ExperimentTemplateTargetParameterMap | None


ExperimentTemplateTargetMap = dict[ExperimentTemplateTargetName, ExperimentTemplateTarget]


class ExperimentTemplate(TypedDict, total=False):
    """Describes an experiment template."""

    id: ExperimentTemplateId | None
    arn: ResourceArn | None
    description: ExperimentTemplateDescription | None
    targets: ExperimentTemplateTargetMap | None
    actions: ExperimentTemplateActionMap | None
    stopConditions: ExperimentTemplateStopConditionList | None
    creationTime: CreationTime | None
    lastUpdateTime: LastUpdateTime | None
    roleArn: RoleArn | None
    tags: TagMap | None
    logConfiguration: ExperimentTemplateLogConfiguration | None
    experimentOptions: ExperimentTemplateExperimentOptions | None
    targetAccountConfigurationsCount: TargetAccountConfigurationsCount | None
    experimentReportConfiguration: ExperimentTemplateReportConfiguration | None


class CreateExperimentTemplateResponse(TypedDict, total=False):
    experimentTemplate: ExperimentTemplate | None


class CreateTargetAccountConfigurationRequest(ServiceRequest):
    clientToken: ClientToken | None
    experimentTemplateId: ExperimentTemplateId
    accountId: TargetAccountId
    roleArn: RoleArn
    description: TargetAccountConfigurationDescription | None


class TargetAccountConfiguration(TypedDict, total=False):
    """Describes a target account configuration."""

    roleArn: RoleArn | None
    accountId: TargetAccountId | None
    description: TargetAccountConfigurationDescription | None


class CreateTargetAccountConfigurationResponse(TypedDict, total=False):
    targetAccountConfiguration: TargetAccountConfiguration | None


class DeleteExperimentTemplateRequest(ServiceRequest):
    id: ExperimentTemplateId


class DeleteExperimentTemplateResponse(TypedDict, total=False):
    experimentTemplate: ExperimentTemplate | None


class DeleteTargetAccountConfigurationRequest(ServiceRequest):
    experimentTemplateId: ExperimentTemplateId
    accountId: TargetAccountId


class DeleteTargetAccountConfigurationResponse(TypedDict, total=False):
    targetAccountConfiguration: TargetAccountConfiguration | None


class ExperimentReportS3Report(TypedDict, total=False):
    """Describes the S3 destination for the report."""

    arn: ExperimentReportS3ReportArn | None
    reportType: ExperimentReportS3ReportType | None


ExperimentReportS3ReportList = list[ExperimentReportS3Report]


class ExperimentReportError(TypedDict, total=False):
    """Describes the error when experiment report generation has failed."""

    code: ExperimentReportErrorCode | None


class ExperimentReportState(TypedDict, total=False):
    """Describes the state of the experiment report generation."""

    status: ExperimentReportStatus | None
    reason: ExperimentReportReason | None
    error: ExperimentReportError | None


class ExperimentReport(TypedDict, total=False):
    """Describes the experiment report."""

    state: ExperimentReportState | None
    s3Reports: ExperimentReportS3ReportList | None


class ExperimentReportConfigurationCloudWatchDashboard(TypedDict, total=False):
    """Specifies the CloudWatch dashboard to include in the experiment report.
    The dashboard widgets will be captured as snapshot graphs within the
    report.
    """

    dashboardIdentifier: ReportConfigurationCloudWatchDashboardIdentifier | None


ExperimentReportConfigurationCloudWatchDashboardList = list[
    ExperimentReportConfigurationCloudWatchDashboard
]


class ExperimentReportConfigurationDataSources(TypedDict, total=False):
    """Describes the data sources for the experiment report."""

    cloudWatchDashboards: ExperimentReportConfigurationCloudWatchDashboardList | None


class ExperimentReportConfigurationOutputsS3Configuration(TypedDict, total=False):
    """Specifies the S3 destination for the experiment report."""

    bucketName: S3BucketName | None
    prefix: ReportConfigurationS3OutputPrefix | None


class ExperimentReportConfigurationOutputs(TypedDict, total=False):
    """Describes the output destinations of the experiment report."""

    s3Configuration: ExperimentReportConfigurationOutputsS3Configuration | None


class ExperimentReportConfiguration(TypedDict, total=False):
    """Describes the report configuration for the experiment. For more
    information, see `Experiment report configurations for AWS
    FIS <https://docs.aws.amazon.com/fis/latest/userguide/experiment-report-configuration>`__.
    """

    outputs: ExperimentReportConfigurationOutputs | None
    dataSources: ExperimentReportConfigurationDataSources | None
    preExperimentDuration: ReportConfigurationDuration | None
    postExperimentDuration: ReportConfigurationDuration | None


class ExperimentOptions(TypedDict, total=False):
    """Describes the options for an experiment."""

    accountTargeting: AccountTargeting | None
    emptyTargetResolutionMode: EmptyTargetResolutionMode | None
    actionsMode: ActionsMode | None


class ExperimentS3LogConfiguration(TypedDict, total=False):
    """Describes the configuration for experiment logging to Amazon S3."""

    bucketName: S3BucketName | None
    prefix: S3ObjectKey | None


class ExperimentCloudWatchLogsLogConfiguration(TypedDict, total=False):
    """Describes the configuration for experiment logging to Amazon CloudWatch
    Logs.
    """

    logGroupArn: CloudWatchLogGroupArn | None


class ExperimentLogConfiguration(TypedDict, total=False):
    """Describes the configuration for experiment logging."""

    cloudWatchLogsConfiguration: ExperimentCloudWatchLogsLogConfiguration | None
    s3Configuration: ExperimentS3LogConfiguration | None
    logSchemaVersion: LogSchemaVersion | None


ExperimentEndTime = datetime
ExperimentStartTime = datetime


class ExperimentStopCondition(TypedDict, total=False):
    """Describes the stop condition for an experiment."""

    source: StopConditionSource | None
    value: StopConditionValue | None


ExperimentStopConditionList = list[ExperimentStopCondition]
ExperimentActionEndTime = datetime
ExperimentActionStartTime = datetime


class ExperimentActionState(TypedDict, total=False):
    """Describes the state of an action."""

    status: ExperimentActionStatus | None
    reason: ExperimentActionStatusReason | None


ExperimentActionStartAfterList = list[ExperimentActionStartAfter]
ExperimentActionTargetMap = dict[ExperimentActionTargetName, ExperimentTargetName]
ExperimentActionParameterMap = dict[ExperimentActionParameterName, ExperimentActionParameter]


class ExperimentAction(TypedDict, total=False):
    """Describes the action for an experiment."""

    actionId: ActionId | None
    description: ExperimentActionDescription | None
    parameters: ExperimentActionParameterMap | None
    targets: ExperimentActionTargetMap | None
    startAfter: ExperimentActionStartAfterList | None
    state: ExperimentActionState | None
    startTime: ExperimentActionStartTime | None
    endTime: ExperimentActionEndTime | None


ExperimentActionMap = dict[ExperimentActionName, ExperimentAction]
ExperimentTargetParameterMap = dict[ExperimentTargetParameterName, ExperimentTargetParameterValue]
ExperimentTargetFilterValues = list[ExperimentTargetFilterValue]


class ExperimentTargetFilter(TypedDict, total=False):
    """Describes a filter used for the target resources in an experiment."""

    path: ExperimentTargetFilterPath | None
    values: ExperimentTargetFilterValues | None


ExperimentTargetFilterList = list[ExperimentTargetFilter]


class ExperimentTarget(TypedDict, total=False):
    """Describes a target for an experiment."""

    resourceType: TargetResourceTypeId | None
    resourceArns: ResourceArnList | None
    resourceTags: TagMap | None
    filters: ExperimentTargetFilterList | None
    selectionMode: ExperimentTargetSelectionMode | None
    parameters: ExperimentTargetParameterMap | None


ExperimentTargetMap = dict[ExperimentTargetName, ExperimentTarget]


class ExperimentError(TypedDict, total=False):
    """Describes the error when an experiment has ``failed``."""

    accountId: ExperimentErrorAccountId | None
    code: ExperimentErrorCode | None
    location: ExperimentErrorLocation | None


class ExperimentState(TypedDict, total=False):
    """Describes the state of an experiment."""

    status: ExperimentStatus | None
    reason: ExperimentStatusReason | None
    error: ExperimentError | None


class Experiment(TypedDict, total=False):
    """Describes an experiment."""

    id: ExperimentId | None
    arn: ResourceArn | None
    experimentTemplateId: ExperimentTemplateId | None
    roleArn: RoleArn | None
    state: ExperimentState | None
    targets: ExperimentTargetMap | None
    actions: ExperimentActionMap | None
    stopConditions: ExperimentStopConditionList | None
    creationTime: CreationTime | None
    startTime: ExperimentStartTime | None
    endTime: ExperimentEndTime | None
    tags: TagMap | None
    logConfiguration: ExperimentLogConfiguration | None
    experimentOptions: ExperimentOptions | None
    targetAccountConfigurationsCount: TargetAccountConfigurationsCount | None
    experimentReportConfiguration: ExperimentReportConfiguration | None
    experimentReport: ExperimentReport | None


class ExperimentSummary(TypedDict, total=False):
    """Provides a summary of an experiment."""

    id: ExperimentId | None
    arn: ResourceArn | None
    experimentTemplateId: ExperimentTemplateId | None
    state: ExperimentState | None
    creationTime: CreationTime | None
    tags: TagMap | None
    experimentOptions: ExperimentOptions | None


ExperimentSummaryList = list[ExperimentSummary]


class ExperimentTargetAccountConfiguration(TypedDict, total=False):
    """Describes a target account configuration for an experiment."""

    roleArn: RoleArn | None
    accountId: TargetAccountId | None
    description: TargetAccountConfigurationDescription | None


class ExperimentTargetAccountConfigurationSummary(TypedDict, total=False):
    """Provides a summary of a target account configuration."""

    roleArn: RoleArn | None
    accountId: TargetAccountId | None
    description: TargetAccountConfigurationDescription | None


ExperimentTargetAccountConfigurationList = list[ExperimentTargetAccountConfigurationSummary]


class ExperimentTemplateSummary(TypedDict, total=False):
    """Provides a summary of an experiment template."""

    id: ExperimentTemplateId | None
    arn: ResourceArn | None
    description: ExperimentTemplateDescription | None
    creationTime: CreationTime | None
    lastUpdateTime: LastUpdateTime | None
    tags: TagMap | None


ExperimentTemplateSummaryList = list[ExperimentTemplateSummary]


class GetActionRequest(ServiceRequest):
    id: ActionId


class GetActionResponse(TypedDict, total=False):
    action: Action | None


class GetExperimentRequest(ServiceRequest):
    id: ExperimentId


class GetExperimentResponse(TypedDict, total=False):
    experiment: Experiment | None


class GetExperimentTargetAccountConfigurationRequest(ServiceRequest):
    experimentId: ExperimentId
    accountId: TargetAccountId


class GetExperimentTargetAccountConfigurationResponse(TypedDict, total=False):
    targetAccountConfiguration: ExperimentTargetAccountConfiguration | None


class GetExperimentTemplateRequest(ServiceRequest):
    id: ExperimentTemplateId


class GetExperimentTemplateResponse(TypedDict, total=False):
    experimentTemplate: ExperimentTemplate | None


class GetSafetyLeverRequest(ServiceRequest):
    id: SafetyLeverId


class SafetyLeverState(TypedDict, total=False):
    """Describes the state of the safety lever."""

    status: SafetyLeverStatus | None
    reason: SafetyLeverStatusReason | None


class SafetyLever(TypedDict, total=False):
    """Describes a safety lever."""

    id: SafetyLeverId | None
    arn: ResourceArn | None
    state: SafetyLeverState | None


class GetSafetyLeverResponse(TypedDict, total=False):
    safetyLever: SafetyLever | None


class GetTargetAccountConfigurationRequest(ServiceRequest):
    experimentTemplateId: ExperimentTemplateId
    accountId: TargetAccountId


class GetTargetAccountConfigurationResponse(TypedDict, total=False):
    targetAccountConfiguration: TargetAccountConfiguration | None


class GetTargetResourceTypeRequest(ServiceRequest):
    resourceType: TargetResourceTypeId


class TargetResourceTypeParameter(TypedDict, total=False):
    """Describes the parameters for a resource type. Use parameters to
    determine which tasks are identified during target resolution.
    """

    description: TargetResourceTypeParameterDescription | None
    required: TargetResourceTypeParameterRequired | None


TargetResourceTypeParameterMap = dict[TargetResourceTypeParameterName, TargetResourceTypeParameter]


class TargetResourceType(TypedDict, total=False):
    """Describes a resource type."""

    resourceType: TargetResourceTypeId | None
    description: TargetResourceTypeDescription | None
    parameters: TargetResourceTypeParameterMap | None


class GetTargetResourceTypeResponse(TypedDict, total=False):
    targetResourceType: TargetResourceType | None


class ListActionsRequest(ServiceRequest):
    maxResults: ListActionsMaxResults | None
    nextToken: NextToken | None


class ListActionsResponse(TypedDict, total=False):
    actions: ActionSummaryList | None
    nextToken: NextToken | None


class ListExperimentResolvedTargetsRequest(ServiceRequest):
    experimentId: ExperimentId
    maxResults: ListExperimentResolvedTargetsMaxResults | None
    nextToken: NextToken | None
    targetName: TargetName | None


TargetInformationMap = dict[TargetInformationKey, TargetInformationValue]


class ResolvedTarget(TypedDict, total=False):
    """Describes a resolved target."""

    resourceType: TargetResourceTypeId | None
    targetName: TargetName | None
    targetInformation: TargetInformationMap | None


ResolvedTargetList = list[ResolvedTarget]


class ListExperimentResolvedTargetsResponse(TypedDict, total=False):
    resolvedTargets: ResolvedTargetList | None
    nextToken: NextToken | None


class ListExperimentTargetAccountConfigurationsRequest(ServiceRequest):
    experimentId: ExperimentId
    nextToken: NextToken | None


class ListExperimentTargetAccountConfigurationsResponse(TypedDict, total=False):
    targetAccountConfigurations: ExperimentTargetAccountConfigurationList | None
    nextToken: NextToken | None


class ListExperimentTemplatesRequest(ServiceRequest):
    maxResults: ListExperimentTemplatesMaxResults | None
    nextToken: NextToken | None


class ListExperimentTemplatesResponse(TypedDict, total=False):
    experimentTemplates: ExperimentTemplateSummaryList | None
    nextToken: NextToken | None


class ListExperimentsRequest(ServiceRequest):
    maxResults: ListExperimentsMaxResults | None
    nextToken: NextToken | None
    experimentTemplateId: ExperimentTemplateId | None


class ListExperimentsResponse(TypedDict, total=False):
    experiments: ExperimentSummaryList | None
    nextToken: NextToken | None


class ListTagsForResourceRequest(ServiceRequest):
    resourceArn: ResourceArn


class ListTagsForResourceResponse(TypedDict, total=False):
    tags: TagMap | None


class ListTargetAccountConfigurationsRequest(ServiceRequest):
    experimentTemplateId: ExperimentTemplateId
    maxResults: ListTargetAccountConfigurationsMaxResults | None
    nextToken: NextToken | None


class TargetAccountConfigurationSummary(TypedDict, total=False):
    """Provides a summary of a target account configuration."""

    roleArn: RoleArn | None
    accountId: TargetAccountId | None
    description: TargetAccountConfigurationDescription | None


TargetAccountConfigurationList = list[TargetAccountConfigurationSummary]


class ListTargetAccountConfigurationsResponse(TypedDict, total=False):
    targetAccountConfigurations: TargetAccountConfigurationList | None
    nextToken: NextToken | None


class ListTargetResourceTypesRequest(ServiceRequest):
    maxResults: ListTargetResourceTypesMaxResults | None
    nextToken: NextToken | None


class TargetResourceTypeSummary(TypedDict, total=False):
    """Describes a resource type."""

    resourceType: TargetResourceTypeId | None
    description: TargetResourceTypeDescription | None


TargetResourceTypeSummaryList = list[TargetResourceTypeSummary]


class ListTargetResourceTypesResponse(TypedDict, total=False):
    targetResourceTypes: TargetResourceTypeSummaryList | None
    nextToken: NextToken | None


class StartExperimentExperimentOptionsInput(TypedDict, total=False):
    """Specifies experiment options for running an experiment."""

    actionsMode: ActionsMode | None


class StartExperimentRequest(ServiceRequest):
    clientToken: ClientToken
    experimentTemplateId: ExperimentTemplateId
    experimentOptions: StartExperimentExperimentOptionsInput | None
    tags: TagMap | None


class StartExperimentResponse(TypedDict, total=False):
    experiment: Experiment | None


class StopExperimentRequest(ServiceRequest):
    id: ExperimentId


class StopExperimentResponse(TypedDict, total=False):
    experiment: Experiment | None


TagKeyList = list[TagKey]


class TagResourceRequest(ServiceRequest):
    resourceArn: ResourceArn
    tags: TagMap


class TagResourceResponse(TypedDict, total=False):
    pass


class UntagResourceRequest(ServiceRequest):
    resourceArn: ResourceArn
    tagKeys: TagKeyList | None


class UntagResourceResponse(TypedDict, total=False):
    pass


class UpdateExperimentTemplateActionInputItem(TypedDict, total=False):
    """Specifies an action for an experiment template."""

    actionId: ActionId | None
    description: ExperimentTemplateActionDescription | None
    parameters: ExperimentTemplateActionParameterMap | None
    targets: ExperimentTemplateActionTargetMap | None
    startAfter: ExperimentTemplateActionStartAfterList | None


UpdateExperimentTemplateActionInputMap = dict[
    ExperimentTemplateActionName, UpdateExperimentTemplateActionInputItem
]


class UpdateExperimentTemplateExperimentOptionsInput(TypedDict, total=False):
    """Specifies an experiment option for an experiment template."""

    emptyTargetResolutionMode: EmptyTargetResolutionMode | None


class UpdateExperimentTemplateLogConfigurationInput(TypedDict, total=False):
    """Specifies the configuration for experiment logging."""

    cloudWatchLogsConfiguration: ExperimentTemplateCloudWatchLogsLogConfigurationInput | None
    s3Configuration: ExperimentTemplateS3LogConfigurationInput | None
    logSchemaVersion: LogSchemaVersion | None


class UpdateExperimentTemplateReportConfigurationInput(TypedDict, total=False):
    """Specifies the input for the experiment report configuration."""

    outputs: ExperimentTemplateReportConfigurationOutputsInput | None
    dataSources: ExperimentTemplateReportConfigurationDataSourcesInput | None
    preExperimentDuration: ReportConfigurationDuration | None
    postExperimentDuration: ReportConfigurationDuration | None


class UpdateExperimentTemplateTargetInput(TypedDict, total=False):
    """Specifies a target for an experiment. You must specify at least one
    Amazon Resource Name (ARN) or at least one resource tag. You cannot
    specify both.
    """

    resourceType: TargetResourceTypeId
    resourceArns: ResourceArnList | None
    resourceTags: TagMap | None
    filters: ExperimentTemplateTargetFilterInputList | None
    selectionMode: ExperimentTemplateTargetSelectionMode
    parameters: ExperimentTemplateTargetParameterMap | None


UpdateExperimentTemplateTargetInputMap = dict[
    ExperimentTemplateTargetName, UpdateExperimentTemplateTargetInput
]


class UpdateExperimentTemplateStopConditionInput(TypedDict, total=False):
    """Specifies a stop condition for an experiment. You can define a stop
    condition as a CloudWatch alarm.
    """

    source: StopConditionSource
    value: StopConditionValue | None


UpdateExperimentTemplateStopConditionInputList = list[UpdateExperimentTemplateStopConditionInput]


class UpdateExperimentTemplateRequest(ServiceRequest):
    id: ExperimentTemplateId
    description: ExperimentTemplateDescription | None
    stopConditions: UpdateExperimentTemplateStopConditionInputList | None
    targets: UpdateExperimentTemplateTargetInputMap | None
    actions: UpdateExperimentTemplateActionInputMap | None
    roleArn: RoleArn | None
    logConfiguration: UpdateExperimentTemplateLogConfigurationInput | None
    experimentOptions: UpdateExperimentTemplateExperimentOptionsInput | None
    experimentReportConfiguration: UpdateExperimentTemplateReportConfigurationInput | None


class UpdateExperimentTemplateResponse(TypedDict, total=False):
    experimentTemplate: ExperimentTemplate | None


class UpdateSafetyLeverStateInput(TypedDict, total=False):
    """Specifies a state for a safety lever."""

    status: SafetyLeverStatusInput
    reason: SafetyLeverStatusReason


class UpdateSafetyLeverStateRequest(ServiceRequest):
    id: SafetyLeverId
    state: UpdateSafetyLeverStateInput


class UpdateSafetyLeverStateResponse(TypedDict, total=False):
    safetyLever: SafetyLever | None


class UpdateTargetAccountConfigurationRequest(ServiceRequest):
    experimentTemplateId: ExperimentTemplateId
    accountId: TargetAccountId
    roleArn: RoleArn | None
    description: TargetAccountConfigurationDescription | None


class UpdateTargetAccountConfigurationResponse(TypedDict, total=False):
    targetAccountConfiguration: TargetAccountConfiguration | None


class FisApi:
    service: str = "fis"
    version: str = "2020-12-01"

    @handler("CreateExperimentTemplate")
    def create_experiment_template(
        self,
        context: RequestContext,
        client_token: ClientToken,
        description: ExperimentTemplateDescription,
        stop_conditions: CreateExperimentTemplateStopConditionInputList,
        actions: CreateExperimentTemplateActionInputMap,
        role_arn: RoleArn,
        targets: CreateExperimentTemplateTargetInputMap | None = None,
        tags: TagMap | None = None,
        log_configuration: CreateExperimentTemplateLogConfigurationInput | None = None,
        experiment_options: CreateExperimentTemplateExperimentOptionsInput | None = None,
        experiment_report_configuration: CreateExperimentTemplateReportConfigurationInput
        | None = None,
        **kwargs,
    ) -> CreateExperimentTemplateResponse:
        """Creates an experiment template.

        An experiment template includes the following components:

        -  **Targets**: A target can be a specific resource in your Amazon Web
           Services environment, or one or more resources that match criteria
           that you specify, for example, resources that have specific tags.

        -  **Actions**: The actions to carry out on the target. You can specify
           multiple actions, the duration of each action, and when to start each
           action during an experiment.

        -  **Stop conditions**: If a stop condition is triggered while an
           experiment is running, the experiment is automatically stopped. You
           can define a stop condition as a CloudWatch alarm.

        For more information, see `experiment
        templates <https://docs.aws.amazon.com/fis/latest/userguide/experiment-templates.html>`__
        in the *Fault Injection Service User Guide*.

        :param client_token: Unique, case-sensitive identifier that you provide to ensure the
        idempotency of the request.
        :param description: A description for the experiment template.
        :param stop_conditions: The stop conditions.
        :param actions: The actions for the experiment.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM role that grants the FIS
        service permission to perform service actions on your behalf.
        :param targets: The targets for the experiment.
        :param tags: The tags to apply to the experiment template.
        :param log_configuration: The configuration for experiment logging.
        :param experiment_options: The experiment options for the experiment template.
        :param experiment_report_configuration: The experiment report configuration for the experiment template.
        :returns: CreateExperimentTemplateResponse
        :raises ValidationException:
        :raises ConflictException:
        :raises ResourceNotFoundException:
        :raises ServiceQuotaExceededException:
        """
        raise NotImplementedError

    @handler("CreateTargetAccountConfiguration")
    def create_target_account_configuration(
        self,
        context: RequestContext,
        experiment_template_id: ExperimentTemplateId,
        account_id: TargetAccountId,
        role_arn: RoleArn,
        client_token: ClientToken | None = None,
        description: TargetAccountConfigurationDescription | None = None,
        **kwargs,
    ) -> CreateTargetAccountConfigurationResponse:
        """Creates a target account configuration for the experiment template. A
        target account configuration is required when ``accountTargeting`` of
        ``experimentOptions`` is set to ``multi-account``. For more information,
        see `experiment
        options <https://docs.aws.amazon.com/fis/latest/userguide/experiment-options.html>`__
        in the *Fault Injection Service User Guide*.

        :param experiment_template_id: The experiment template ID.
        :param account_id: The Amazon Web Services account ID of the target account.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM role for the target account.
        :param client_token: Unique, case-sensitive identifier that you provide to ensure the
        idempotency of the request.
        :param description: The description of the target account.
        :returns: CreateTargetAccountConfigurationResponse
        :raises ValidationException:
        :raises ConflictException:
        :raises ResourceNotFoundException:
        :raises ServiceQuotaExceededException:
        """
        raise NotImplementedError

    @handler("DeleteExperimentTemplate")
    def delete_experiment_template(
        self, context: RequestContext, id: ExperimentTemplateId, **kwargs
    ) -> DeleteExperimentTemplateResponse:
        """Deletes the specified experiment template.

        :param id: The ID of the experiment template.
        :returns: DeleteExperimentTemplateResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("DeleteTargetAccountConfiguration")
    def delete_target_account_configuration(
        self,
        context: RequestContext,
        experiment_template_id: ExperimentTemplateId,
        account_id: TargetAccountId,
        **kwargs,
    ) -> DeleteTargetAccountConfigurationResponse:
        """Deletes the specified target account configuration of the experiment
        template.

        :param experiment_template_id: The ID of the experiment template.
        :param account_id: The Amazon Web Services account ID of the target account.
        :returns: DeleteTargetAccountConfigurationResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetAction")
    def get_action(self, context: RequestContext, id: ActionId, **kwargs) -> GetActionResponse:
        """Gets information about the specified FIS action.

        :param id: The ID of the action.
        :returns: GetActionResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetExperiment")
    def get_experiment(
        self, context: RequestContext, id: ExperimentId, **kwargs
    ) -> GetExperimentResponse:
        """Gets information about the specified experiment.

        :param id: The ID of the experiment.
        :returns: GetExperimentResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetExperimentTargetAccountConfiguration")
    def get_experiment_target_account_configuration(
        self,
        context: RequestContext,
        experiment_id: ExperimentId,
        account_id: TargetAccountId,
        **kwargs,
    ) -> GetExperimentTargetAccountConfigurationResponse:
        """Gets information about the specified target account configuration of the
        experiment.

        :param experiment_id: The ID of the experiment.
        :param account_id: The Amazon Web Services account ID of the target account.
        :returns: GetExperimentTargetAccountConfigurationResponse
        :raises ResourceNotFoundException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("GetExperimentTemplate")
    def get_experiment_template(
        self, context: RequestContext, id: ExperimentTemplateId, **kwargs
    ) -> GetExperimentTemplateResponse:
        """Gets information about the specified experiment template.

        :param id: The ID of the experiment template.
        :returns: GetExperimentTemplateResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetSafetyLever")
    def get_safety_lever(
        self, context: RequestContext, id: SafetyLeverId, **kwargs
    ) -> GetSafetyLeverResponse:
        """Gets information about the specified safety lever.

        :param id: The ID of the safety lever.
        :returns: GetSafetyLeverResponse
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetTargetAccountConfiguration")
    def get_target_account_configuration(
        self,
        context: RequestContext,
        experiment_template_id: ExperimentTemplateId,
        account_id: TargetAccountId,
        **kwargs,
    ) -> GetTargetAccountConfigurationResponse:
        """Gets information about the specified target account configuration of the
        experiment template.

        :param experiment_template_id: The ID of the experiment template.
        :param account_id: The Amazon Web Services account ID of the target account.
        :returns: GetTargetAccountConfigurationResponse
        :raises ResourceNotFoundException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("GetTargetResourceType")
    def get_target_resource_type(
        self, context: RequestContext, resource_type: TargetResourceTypeId, **kwargs
    ) -> GetTargetResourceTypeResponse:
        """Gets information about the specified resource type.

        :param resource_type: The resource type.
        :returns: GetTargetResourceTypeResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListActions")
    def list_actions(
        self,
        context: RequestContext,
        max_results: ListActionsMaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListActionsResponse:
        """Lists the available FIS actions.

        :param max_results: The maximum number of results to return with a single call.
        :param next_token: The token for the next page of results.
        :returns: ListActionsResponse
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("ListExperimentResolvedTargets")
    def list_experiment_resolved_targets(
        self,
        context: RequestContext,
        experiment_id: ExperimentId,
        max_results: ListExperimentResolvedTargetsMaxResults | None = None,
        next_token: NextToken | None = None,
        target_name: TargetName | None = None,
        **kwargs,
    ) -> ListExperimentResolvedTargetsResponse:
        """Lists the resolved targets information of the specified experiment.

        :param experiment_id: The ID of the experiment.
        :param max_results: The maximum number of results to return with a single call.
        :param next_token: The token for the next page of results.
        :param target_name: The name of the target.
        :returns: ListExperimentResolvedTargetsResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListExperimentTargetAccountConfigurations")
    def list_experiment_target_account_configurations(
        self,
        context: RequestContext,
        experiment_id: ExperimentId,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListExperimentTargetAccountConfigurationsResponse:
        """Lists the target account configurations of the specified experiment.

        :param experiment_id: The ID of the experiment.
        :param next_token: The token for the next page of results.
        :returns: ListExperimentTargetAccountConfigurationsResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListExperimentTemplates")
    def list_experiment_templates(
        self,
        context: RequestContext,
        max_results: ListExperimentTemplatesMaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListExperimentTemplatesResponse:
        """Lists your experiment templates.

        :param max_results: The maximum number of results to return with a single call.
        :param next_token: The token for the next page of results.
        :returns: ListExperimentTemplatesResponse
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("ListExperiments")
    def list_experiments(
        self,
        context: RequestContext,
        max_results: ListExperimentsMaxResults | None = None,
        next_token: NextToken | None = None,
        experiment_template_id: ExperimentTemplateId | None = None,
        **kwargs,
    ) -> ListExperimentsResponse:
        """Lists your experiments.

        :param max_results: The maximum number of results to return with a single call.
        :param next_token: The token for the next page of results.
        :param experiment_template_id: The ID of the experiment template.
        :returns: ListExperimentsResponse
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("ListTagsForResource")
    def list_tags_for_resource(
        self, context: RequestContext, resource_arn: ResourceArn, **kwargs
    ) -> ListTagsForResourceResponse:
        """Lists the tags for the specified resource.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource.
        :returns: ListTagsForResourceResponse
        """
        raise NotImplementedError

    @handler("ListTargetAccountConfigurations")
    def list_target_account_configurations(
        self,
        context: RequestContext,
        experiment_template_id: ExperimentTemplateId,
        max_results: ListTargetAccountConfigurationsMaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListTargetAccountConfigurationsResponse:
        """Lists the target account configurations of the specified experiment
        template.

        :param experiment_template_id: The ID of the experiment template.
        :param max_results: The maximum number of results to return with a single call.
        :param next_token: The token for the next page of results.
        :returns: ListTargetAccountConfigurationsResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListTargetResourceTypes")
    def list_target_resource_types(
        self,
        context: RequestContext,
        max_results: ListTargetResourceTypesMaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListTargetResourceTypesResponse:
        """Lists the target resource types.

        :param max_results: The maximum number of results to return with a single call.
        :param next_token: The token for the next page of results.
        :returns: ListTargetResourceTypesResponse
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("StartExperiment")
    def start_experiment(
        self,
        context: RequestContext,
        client_token: ClientToken,
        experiment_template_id: ExperimentTemplateId,
        experiment_options: StartExperimentExperimentOptionsInput | None = None,
        tags: TagMap | None = None,
        **kwargs,
    ) -> StartExperimentResponse:
        """Starts running an experiment from the specified experiment template.

        :param client_token: Unique, case-sensitive identifier that you provide to ensure the
        idempotency of the request.
        :param experiment_template_id: The ID of the experiment template.
        :param experiment_options: The experiment options for running the experiment.
        :param tags: The tags to apply to the experiment.
        :returns: StartExperimentResponse
        :raises ValidationException:
        :raises ConflictException:
        :raises ResourceNotFoundException:
        :raises ServiceQuotaExceededException:
        """
        raise NotImplementedError

    @handler("StopExperiment")
    def stop_experiment(
        self, context: RequestContext, id: ExperimentId, **kwargs
    ) -> StopExperimentResponse:
        """Stops the specified experiment.

        :param id: The ID of the experiment.
        :returns: StopExperimentResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("TagResource")
    def tag_resource(
        self, context: RequestContext, resource_arn: ResourceArn, tags: TagMap, **kwargs
    ) -> TagResourceResponse:
        """Applies the specified tags to the specified resource.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource.
        :param tags: The tags for the resource.
        :returns: TagResourceResponse
        """
        raise NotImplementedError

    @handler("UntagResource")
    def untag_resource(
        self,
        context: RequestContext,
        resource_arn: ResourceArn,
        tag_keys: TagKeyList | None = None,
        **kwargs,
    ) -> UntagResourceResponse:
        """Removes the specified tags from the specified resource.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource.
        :param tag_keys: The tag keys to remove.
        :returns: UntagResourceResponse
        """
        raise NotImplementedError

    @handler("UpdateExperimentTemplate")
    def update_experiment_template(
        self,
        context: RequestContext,
        id: ExperimentTemplateId,
        description: ExperimentTemplateDescription | None = None,
        stop_conditions: UpdateExperimentTemplateStopConditionInputList | None = None,
        targets: UpdateExperimentTemplateTargetInputMap | None = None,
        actions: UpdateExperimentTemplateActionInputMap | None = None,
        role_arn: RoleArn | None = None,
        log_configuration: UpdateExperimentTemplateLogConfigurationInput | None = None,
        experiment_options: UpdateExperimentTemplateExperimentOptionsInput | None = None,
        experiment_report_configuration: UpdateExperimentTemplateReportConfigurationInput
        | None = None,
        **kwargs,
    ) -> UpdateExperimentTemplateResponse:
        """Updates the specified experiment template.

        :param id: The ID of the experiment template.
        :param description: A description for the template.
        :param stop_conditions: The stop conditions for the experiment.
        :param targets: The targets for the experiment.
        :param actions: The actions for the experiment.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM role that grants the FIS
        service permission to perform service actions on your behalf.
        :param log_configuration: The configuration for experiment logging.
        :param experiment_options: The experiment options for the experiment template.
        :param experiment_report_configuration: The experiment report configuration for the experiment template.
        :returns: UpdateExperimentTemplateResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises ServiceQuotaExceededException:
        """
        raise NotImplementedError

    @handler("UpdateSafetyLeverState")
    def update_safety_lever_state(
        self,
        context: RequestContext,
        id: SafetyLeverId,
        state: UpdateSafetyLeverStateInput,
        **kwargs,
    ) -> UpdateSafetyLeverStateResponse:
        """Updates the specified safety lever state.

        :param id: The ID of the safety lever.
        :param state: The state of the safety lever.
        :returns: UpdateSafetyLeverStateResponse
        :raises ValidationException:
        :raises ConflictException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("UpdateTargetAccountConfiguration")
    def update_target_account_configuration(
        self,
        context: RequestContext,
        experiment_template_id: ExperimentTemplateId,
        account_id: TargetAccountId,
        role_arn: RoleArn | None = None,
        description: TargetAccountConfigurationDescription | None = None,
        **kwargs,
    ) -> UpdateTargetAccountConfigurationResponse:
        """Updates the target account configuration for the specified experiment
        template.

        :param experiment_template_id: The ID of the experiment template.
        :param account_id: The Amazon Web Services account ID of the target account.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM role for the target account.
        :param description: The description of the target account.
        :returns: UpdateTargetAccountConfigurationResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError
