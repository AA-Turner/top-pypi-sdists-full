from datetime import datetime
from enum import StrEnum
from typing import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

ARN = str
AccountId = str
BackupOptionKey = str
BackupOptionValue = str
BackupPlanName = str
BackupRuleName = str
BackupSelectionName = str
BackupVaultName = str
BackupVaultNameOrWildcard = str
Boolean = bool
ConditionKey = str
ConditionValue = str
ControlName = str
CreatorRequestId = str
CronExpression = str
FrameworkDescription = str
FrameworkName = str
GlobalSettingsName = str
GlobalSettingsValue = str
IAMPolicy = str
IAMRoleArn = str
IsEnabled = bool
ListRestoreTestingPlansInputMaxResultsInteger = int
ListRestoreTestingSelectionsInputMaxResultsInteger = int
ListScanJobsInputMaxResultsInteger = int
MaxFrameworkInputs = int
MaxResults = int
MaxScheduledRunsPreview = int
MessageCategory = str
MetadataKey = str
MetadataValue = str
ParameterName = str
ParameterValue = str
Region = str
ReportJobId = str
ReportPlanDescription = str
ReportPlanName = str
RequesterComment = str
ResourceType = str
RestoreJobId = str
String = str
TagKey = str
TagValue = str
TieringConfigurationName = str
TieringDownSettingsInDays = int
Timezone = str
boolean = bool
integer = int
string = str


class AggregationPeriod(StrEnum):
    ONE_DAY = "ONE_DAY"
    SEVEN_DAYS = "SEVEN_DAYS"
    FOURTEEN_DAYS = "FOURTEEN_DAYS"


class BackupJobState(StrEnum):
    CREATED = "CREATED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    ABORTING = "ABORTING"
    ABORTED = "ABORTED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"
    PARTIAL = "PARTIAL"


class BackupJobStatus(StrEnum):
    CREATED = "CREATED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    ABORTING = "ABORTING"
    ABORTED = "ABORTED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"
    PARTIAL = "PARTIAL"
    AGGREGATE_ALL = "AGGREGATE_ALL"
    ANY = "ANY"


class BackupVaultEvent(StrEnum):
    BACKUP_JOB_STARTED = "BACKUP_JOB_STARTED"
    BACKUP_JOB_COMPLETED = "BACKUP_JOB_COMPLETED"
    BACKUP_JOB_SUCCESSFUL = "BACKUP_JOB_SUCCESSFUL"
    BACKUP_JOB_FAILED = "BACKUP_JOB_FAILED"
    BACKUP_JOB_EXPIRED = "BACKUP_JOB_EXPIRED"
    RESTORE_JOB_STARTED = "RESTORE_JOB_STARTED"
    RESTORE_JOB_COMPLETED = "RESTORE_JOB_COMPLETED"
    RESTORE_JOB_SUCCESSFUL = "RESTORE_JOB_SUCCESSFUL"
    RESTORE_JOB_FAILED = "RESTORE_JOB_FAILED"
    COPY_JOB_STARTED = "COPY_JOB_STARTED"
    COPY_JOB_SUCCESSFUL = "COPY_JOB_SUCCESSFUL"
    COPY_JOB_FAILED = "COPY_JOB_FAILED"
    RECOVERY_POINT_MODIFIED = "RECOVERY_POINT_MODIFIED"
    BACKUP_PLAN_CREATED = "BACKUP_PLAN_CREATED"
    BACKUP_PLAN_MODIFIED = "BACKUP_PLAN_MODIFIED"
    S3_BACKUP_OBJECT_FAILED = "S3_BACKUP_OBJECT_FAILED"
    S3_RESTORE_OBJECT_FAILED = "S3_RESTORE_OBJECT_FAILED"
    CONTINUOUS_BACKUP_INTERRUPTED = "CONTINUOUS_BACKUP_INTERRUPTED"
    RECOVERY_POINT_INDEX_COMPLETED = "RECOVERY_POINT_INDEX_COMPLETED"
    RECOVERY_POINT_INDEX_DELETED = "RECOVERY_POINT_INDEX_DELETED"
    RECOVERY_POINT_INDEXING_FAILED = "RECOVERY_POINT_INDEXING_FAILED"


class ConditionType(StrEnum):
    STRINGEQUALS = "STRINGEQUALS"


class CopyJobState(StrEnum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    PARTIAL = "PARTIAL"


class CopyJobStatus(StrEnum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    ABORTING = "ABORTING"
    ABORTED = "ABORTED"
    COMPLETING = "COMPLETING"
    COMPLETED = "COMPLETED"
    FAILING = "FAILING"
    FAILED = "FAILED"
    PARTIAL = "PARTIAL"
    AGGREGATE_ALL = "AGGREGATE_ALL"
    ANY = "ANY"


class EncryptionKeyType(StrEnum):
    AWS_OWNED_KMS_KEY = "AWS_OWNED_KMS_KEY"
    CUSTOMER_MANAGED_KMS_KEY = "CUSTOMER_MANAGED_KMS_KEY"


class Index(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class IndexStatus(StrEnum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    FAILED = "FAILED"
    DELETING = "DELETING"


class LegalHoldStatus(StrEnum):
    CREATING = "CREATING"
    ACTIVE = "ACTIVE"
    CANCELING = "CANCELING"
    CANCELED = "CANCELED"


class LifecycleDeleteAfterEvent(StrEnum):
    DELETE_AFTER_COPY = "DELETE_AFTER_COPY"


class MalwareScanner(StrEnum):
    GUARDDUTY = "GUARDDUTY"


class MpaRevokeSessionStatus(StrEnum):
    PENDING = "PENDING"
    FAILED = "FAILED"


class MpaSessionStatus(StrEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    FAILED = "FAILED"


class RecoveryPointStatus(StrEnum):
    COMPLETED = "COMPLETED"
    PARTIAL = "PARTIAL"
    DELETING = "DELETING"
    EXPIRED = "EXPIRED"
    AVAILABLE = "AVAILABLE"
    STOPPED = "STOPPED"
    CREATING = "CREATING"


class RestoreDeletionStatus(StrEnum):
    DELETING = "DELETING"
    FAILED = "FAILED"
    SUCCESSFUL = "SUCCESSFUL"


class RestoreJobState(StrEnum):
    CREATED = "CREATED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    ABORTED = "ABORTED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    AGGREGATE_ALL = "AGGREGATE_ALL"
    ANY = "ANY"


class RestoreJobStatus(StrEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    ABORTED = "ABORTED"
    FAILED = "FAILED"


class RestoreTestingRecoveryPointSelectionAlgorithm(StrEnum):
    LATEST_WITHIN_WINDOW = "LATEST_WITHIN_WINDOW"
    RANDOM_WITHIN_WINDOW = "RANDOM_WITHIN_WINDOW"


class RestoreTestingRecoveryPointType(StrEnum):
    CONTINUOUS = "CONTINUOUS"
    SNAPSHOT = "SNAPSHOT"


class RestoreValidationStatus(StrEnum):
    FAILED = "FAILED"
    SUCCESSFUL = "SUCCESSFUL"
    TIMED_OUT = "TIMED_OUT"
    VALIDATING = "VALIDATING"


class RuleExecutionType(StrEnum):
    CONTINUOUS = "CONTINUOUS"
    SNAPSHOTS = "SNAPSHOTS"
    CONTINUOUS_AND_SNAPSHOTS = "CONTINUOUS_AND_SNAPSHOTS"


class ScanFinding(StrEnum):
    MALWARE = "MALWARE"


class ScanJobState(StrEnum):
    COMPLETED = "COMPLETED"
    COMPLETED_WITH_ISSUES = "COMPLETED_WITH_ISSUES"
    FAILED = "FAILED"
    CANCELED = "CANCELED"


class ScanJobStatus(StrEnum):
    CREATED = "CREATED"
    COMPLETED = "COMPLETED"
    COMPLETED_WITH_ISSUES = "COMPLETED_WITH_ISSUES"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    CANCELED = "CANCELED"
    AGGREGATE_ALL = "AGGREGATE_ALL"
    ANY = "ANY"


class ScanMode(StrEnum):
    FULL_SCAN = "FULL_SCAN"
    INCREMENTAL_SCAN = "INCREMENTAL_SCAN"


class ScanResourceType(StrEnum):
    EBS = "EBS"
    EC2 = "EC2"
    S3 = "S3"


class ScanResultStatus(StrEnum):
    NO_THREATS_FOUND = "NO_THREATS_FOUND"
    THREATS_FOUND = "THREATS_FOUND"


class ScanState(StrEnum):
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"
    COMPLETED_WITH_ISSUES = "COMPLETED_WITH_ISSUES"
    CREATED = "CREATED"
    FAILED = "FAILED"
    RUNNING = "RUNNING"


class StorageClass(StrEnum):
    WARM = "WARM"
    COLD = "COLD"
    DELETED = "DELETED"


class VaultState(StrEnum):
    CREATING = "CREATING"
    AVAILABLE = "AVAILABLE"
    FAILED = "FAILED"


class VaultType(StrEnum):
    BACKUP_VAULT = "BACKUP_VAULT"
    LOGICALLY_AIR_GAPPED_BACKUP_VAULT = "LOGICALLY_AIR_GAPPED_BACKUP_VAULT"
    RESTORE_ACCESS_BACKUP_VAULT = "RESTORE_ACCESS_BACKUP_VAULT"


class AlreadyExistsException(ServiceException):
    """The required resource already exists."""

    code: str = "AlreadyExistsException"
    sender_fault: bool = False
    status_code: int = 400
    CreatorRequestId: string | None
    Arn: string | None
    Type: string | None
    Context: string | None


class ConflictException(ServiceException):
    """Backup can't perform the action that you requested until it finishes
    performing a previous action. Try again later.
    """

    code: str = "ConflictException"
    sender_fault: bool = False
    status_code: int = 400
    Type: string | None
    Context: string | None


class DependencyFailureException(ServiceException):
    """A dependent Amazon Web Services service or resource returned an error to
    the Backup service, and the action cannot be completed.
    """

    code: str = "DependencyFailureException"
    sender_fault: bool = False
    status_code: int = 400
    Type: string | None
    Context: string | None


class InvalidParameterValueException(ServiceException):
    """Indicates that something is wrong with a parameter's value. For example,
    the value is out of range.
    """

    code: str = "InvalidParameterValueException"
    sender_fault: bool = False
    status_code: int = 400
    Type: string | None
    Context: string | None


class InvalidRequestException(ServiceException):
    """Indicates that something is wrong with the input to the request. For
    example, a parameter is of the wrong type.
    """

    code: str = "InvalidRequestException"
    sender_fault: bool = False
    status_code: int = 400
    Type: string | None
    Context: string | None


class InvalidResourceStateException(ServiceException):
    """Backup is already performing an action on this recovery point. It can't
    perform the action you requested until the first action finishes. Try
    again later.
    """

    code: str = "InvalidResourceStateException"
    sender_fault: bool = False
    status_code: int = 400
    Type: string | None
    Context: string | None


class LimitExceededException(ServiceException):
    """A limit in the request has been exceeded; for example, a maximum number
    of items allowed in a request.
    """

    code: str = "LimitExceededException"
    sender_fault: bool = False
    status_code: int = 400
    Type: string | None
    Context: string | None


class MissingParameterValueException(ServiceException):
    """Indicates that a required parameter is missing."""

    code: str = "MissingParameterValueException"
    sender_fault: bool = False
    status_code: int = 400
    Type: string | None
    Context: string | None


class ResourceNotFoundException(ServiceException):
    """A resource that is required for the action doesn't exist."""

    code: str = "ResourceNotFoundException"
    sender_fault: bool = False
    status_code: int = 400
    Type: string | None
    Context: string | None


class ServiceUnavailableException(ServiceException):
    """The request failed due to a temporary failure of the server."""

    code: str = "ServiceUnavailableException"
    sender_fault: bool = False
    status_code: int = 400
    Type: string | None
    Context: string | None


BackupOptions = dict[BackupOptionKey, BackupOptionValue]


class AdvancedBackupSetting(TypedDict, total=False):
    """The backup options for each resource type."""

    ResourceType: ResourceType | None
    BackupOptions: BackupOptions | None


AdvancedBackupSettings = list[AdvancedBackupSetting]
timestamp = datetime
ScanFindings = list[ScanFinding]


class AggregatedScanResult(TypedDict, total=False):
    """Contains aggregated scan results across multiple scan operations,
    providing a summary of scan status and findings.
    """

    FailedScan: Boolean | None
    Findings: ScanFindings | None
    LastComputed: timestamp | None


class AssociateBackupVaultMpaApprovalTeamInput(ServiceRequest):
    BackupVaultName: BackupVaultName
    MpaApprovalTeamArn: ARN
    RequesterComment: RequesterComment | None


Long = int


class RecoveryPointCreator(TypedDict, total=False):
    """Contains information about the backup plan and rule that Backup used to
    initiate the recovery point backup.
    """

    BackupPlanId: string | None
    BackupPlanArn: ARN | None
    BackupPlanName: string | None
    BackupPlanVersion: string | None
    BackupRuleId: string | None
    BackupRuleName: string | None
    BackupRuleCron: string | None
    BackupRuleTimezone: string | None


class Lifecycle(TypedDict, total=False):
    """Specifies the time period, in days, before a recovery point transitions
    to cold storage or is deleted.

    Backups transitioned to cold storage must be stored in cold storage for
    a minimum of 90 days. Therefore, on the console, the retention setting
    must be 90 days greater than the transition to cold after days setting.
    The transition to cold after days setting can't be changed after a
    backup has been transitioned to cold.

    Resource types that can transition to cold storage are listed in the
    `Feature availability by
    resource <https://docs.aws.amazon.com/aws-backup/latest/devguide/backup-feature-availability.html#features-by-resource>`__
    table. Backup ignores this expression for other resource types.

    To remove the existing lifecycle and retention periods and keep your
    recovery points indefinitely, specify -1 for
    ``MoveToColdStorageAfterDays`` and ``DeleteAfterDays``.
    """

    MoveToColdStorageAfterDays: Long | None
    DeleteAfterDays: Long | None
    OptInToArchiveForSupportedResources: Boolean | None
    DeleteAfterEvent: LifecycleDeleteAfterEvent | None


class BackupJob(TypedDict, total=False):
    """Contains detailed information about a backup job."""

    AccountId: AccountId | None
    BackupJobId: string | None
    BackupVaultName: BackupVaultName | None
    BackupVaultArn: ARN | None
    VaultType: string | None
    VaultLockState: string | None
    RecoveryPointArn: ARN | None
    RecoveryPointLifecycle: Lifecycle | None
    EncryptionKeyArn: ARN | None
    IsEncrypted: boolean | None
    ResourceArn: ARN | None
    CreationDate: timestamp | None
    CompletionDate: timestamp | None
    State: BackupJobState | None
    StatusMessage: string | None
    PercentDone: string | None
    BackupSizeInBytes: Long | None
    IamRoleArn: IAMRoleArn | None
    CreatedBy: RecoveryPointCreator | None
    ExpectedCompletionDate: timestamp | None
    StartBy: timestamp | None
    ResourceType: ResourceType | None
    BytesTransferred: Long | None
    BackupOptions: BackupOptions | None
    BackupType: string | None
    ParentJobId: string | None
    IsParent: boolean | None
    ResourceName: string | None
    InitiationDate: timestamp | None
    MessageCategory: string | None


BackupJobChildJobsInState = dict[BackupJobState, Long]


class BackupJobSummary(TypedDict, total=False):
    """This is a summary of jobs created or running within the most recent 30
    days.

    The returned summary may contain the following: Region, Account, State,
    RestourceType, MessageCategory, StartTime, EndTime, and Count of
    included jobs.
    """

    Region: Region | None
    AccountId: AccountId | None
    State: BackupJobStatus | None
    ResourceType: ResourceType | None
    MessageCategory: MessageCategory | None
    Count: integer | None
    StartTime: timestamp | None
    EndTime: timestamp | None


BackupJobSummaryList = list[BackupJobSummary]
BackupJobsList = list[BackupJob]
ResourceTypes = list[ResourceType]


class ScanSetting(TypedDict, total=False):
    """Contains configuration settings for malware scanning, including the
    scanner type, target resource types, and scanner role.
    """

    MalwareScanner: MalwareScanner | None
    ResourceTypes: ResourceTypes | None
    ScannerRoleArn: IAMRoleArn | None


ScanSettings = list[ScanSetting]


class ScanAction(TypedDict, total=False):
    """Defines a scanning action that specifies the malware scanner and scan
    mode to use.
    """

    MalwareScanner: MalwareScanner | None
    ScanMode: ScanMode | None


ScanActions = list[ScanAction]


class IndexAction(TypedDict, total=False):
    """This is an optional array within a BackupRule.

    IndexAction consists of one ResourceTypes.
    """

    ResourceTypes: ResourceTypes | None


IndexActions = list[IndexAction]


class CopyAction(TypedDict, total=False):
    """The details of the copy operation."""

    Lifecycle: Lifecycle | None
    DestinationBackupVaultArn: ARN


CopyActions = list[CopyAction]
Tags = dict[TagKey, TagValue]
WindowMinutes = int


class BackupRule(TypedDict, total=False):
    """Specifies a scheduled task used to back up a selection of resources."""

    RuleName: BackupRuleName
    TargetBackupVaultName: BackupVaultName
    TargetLogicallyAirGappedBackupVaultArn: ARN | None
    ScheduleExpression: CronExpression | None
    StartWindowMinutes: WindowMinutes | None
    CompletionWindowMinutes: WindowMinutes | None
    Lifecycle: Lifecycle | None
    RecoveryPointTags: Tags | None
    RuleId: string | None
    CopyActions: CopyActions | None
    EnableContinuousBackup: Boolean | None
    ScheduleExpressionTimezone: Timezone | None
    IndexActions: IndexActions | None
    ScanActions: ScanActions | None


BackupRules = list[BackupRule]


class BackupPlan(TypedDict, total=False):
    """Contains an optional backup plan display name and an array of
    ``BackupRule`` objects, each of which specifies a backup rule. Each rule
    in a backup plan is a separate scheduled task and can back up a
    different selection of Amazon Web Services resources.
    """

    BackupPlanName: BackupPlanName
    Rules: BackupRules
    AdvancedBackupSettings: AdvancedBackupSettings | None
    ScanSettings: ScanSettings | None


class BackupRuleInput(TypedDict, total=False):
    """Specifies a scheduled task used to back up a selection of resources."""

    RuleName: BackupRuleName
    TargetBackupVaultName: BackupVaultName
    TargetLogicallyAirGappedBackupVaultArn: ARN | None
    ScheduleExpression: CronExpression | None
    StartWindowMinutes: WindowMinutes | None
    CompletionWindowMinutes: WindowMinutes | None
    Lifecycle: Lifecycle | None
    RecoveryPointTags: Tags | None
    CopyActions: CopyActions | None
    EnableContinuousBackup: Boolean | None
    ScheduleExpressionTimezone: Timezone | None
    IndexActions: IndexActions | None
    ScanActions: ScanActions | None


BackupRulesInput = list[BackupRuleInput]


class BackupPlanInput(TypedDict, total=False):
    """Contains an optional backup plan display name and an array of
    ``BackupRule`` objects, each of which specifies a backup rule. Each rule
    in a backup plan is a separate scheduled task.
    """

    BackupPlanName: BackupPlanName
    Rules: BackupRulesInput
    AdvancedBackupSettings: AdvancedBackupSettings | None
    ScanSettings: ScanSettings | None


class BackupPlanTemplatesListMember(TypedDict, total=False):
    """An object specifying metadata associated with a backup plan template."""

    BackupPlanTemplateId: string | None
    BackupPlanTemplateName: string | None


BackupPlanTemplatesList = list[BackupPlanTemplatesListMember]


class BackupPlansListMember(TypedDict, total=False):
    """Contains metadata about a backup plan."""

    BackupPlanArn: ARN | None
    BackupPlanId: string | None
    CreationDate: timestamp | None
    DeletionDate: timestamp | None
    VersionId: string | None
    BackupPlanName: BackupPlanName | None
    CreatorRequestId: string | None
    LastExecutionDate: timestamp | None
    AdvancedBackupSettings: AdvancedBackupSettings | None


BackupPlanVersionsList = list[BackupPlansListMember]
BackupPlansList = list[BackupPlansListMember]


class ConditionParameter(TypedDict, total=False):
    """Includes information about tags you define to assign tagged resources to
    a backup plan.

    Include the prefix ``aws:ResourceTag`` in your tags. For example,
    ``"aws:ResourceTag/TagKey1": "Value1"``.
    """

    ConditionKey: ConditionKey | None
    ConditionValue: ConditionValue | None


ConditionParameters = list[ConditionParameter]


class Conditions(TypedDict, total=False):
    """Contains information about which resources to include or exclude from a
    backup plan using their tags. Conditions are case sensitive.
    """

    StringEquals: ConditionParameters | None
    StringNotEquals: ConditionParameters | None
    StringLike: ConditionParameters | None
    StringNotLike: ConditionParameters | None


ResourceArns = list[ARN]


class Condition(TypedDict, total=False):
    """Contains an array of triplets made up of a condition type (such as
    ``StringEquals``), a key, and a value. Used to filter resources using
    their tags and assign them to a backup plan. Case sensitive.
    """

    ConditionType: ConditionType
    ConditionKey: ConditionKey
    ConditionValue: ConditionValue


ListOfTags = list[Condition]


class BackupSelection(TypedDict, total=False):
    """Used to specify a set of resources to a backup plan.

    We recommend that you specify conditions, tags, or resources to include
    or exclude. Otherwise, Backup attempts to select all supported and
    opted-in storage resources, which could have unintended cost
    implications.

    For more information, see `Assigning resources
    programmatically <https://docs.aws.amazon.com/aws-backup/latest/devguide/assigning-resources.html#assigning-resources-json>`__.
    """

    SelectionName: BackupSelectionName
    IamRoleArn: IAMRoleArn
    Resources: ResourceArns | None
    ListOfTags: ListOfTags | None
    NotResources: ResourceArns | None
    Conditions: Conditions | None


class BackupSelectionsListMember(TypedDict, total=False):
    """Contains metadata about a ``BackupSelection`` object."""

    SelectionId: string | None
    SelectionName: BackupSelectionName | None
    BackupPlanId: string | None
    CreationDate: timestamp | None
    CreatorRequestId: string | None
    IamRoleArn: IAMRoleArn | None


BackupSelectionsList = list[BackupSelectionsListMember]
BackupVaultEvents = list[BackupVaultEvent]
long = int


class BackupVaultListMember(TypedDict, total=False):
    """Contains metadata about a backup vault."""

    BackupVaultName: BackupVaultName | None
    BackupVaultArn: ARN | None
    VaultType: VaultType | None
    VaultState: VaultState | None
    CreationDate: timestamp | None
    EncryptionKeyArn: ARN | None
    CreatorRequestId: string | None
    NumberOfRecoveryPoints: long | None
    Locked: Boolean | None
    MinRetentionDays: Long | None
    MaxRetentionDays: Long | None
    LockDate: timestamp | None
    EncryptionKeyType: EncryptionKeyType | None


BackupVaultList = list[BackupVaultListMember]


class CalculatedLifecycle(TypedDict, total=False):
    """Contains ``DeleteAt`` and ``MoveToColdStorageAt`` timestamps, which are
    used to specify a lifecycle for a recovery point.

    The lifecycle defines when a protected resource is transitioned to cold
    storage and when it expires. Backup transitions and expires backups
    automatically according to the lifecycle that you define.

    Backups transitioned to cold storage must be stored in cold storage for
    a minimum of 90 days. Therefore, the “retention” setting must be 90 days
    greater than the “transition to cold after days” setting. The
    “transition to cold after days” setting cannot be changed after a backup
    has been transitioned to cold.

    Resource types that can transition to cold storage are listed in the
    `Feature availability by
    resource <https://docs.aws.amazon.com/aws-backup/latest/devguide/backup-feature-availability.html#features-by-resource>`__
    table. Backup ignores this expression for other resource types.
    """

    MoveToColdStorageAt: timestamp | None
    DeleteAt: timestamp | None


class CancelLegalHoldInput(ServiceRequest):
    LegalHoldId: string
    CancelDescription: string
    RetainRecordInDays: Long | None


class CancelLegalHoldOutput(TypedDict, total=False):
    pass


ComplianceResourceIdList = list[string]


class ControlInputParameter(TypedDict, total=False):
    """The parameters for a control. A control can have zero, one, or more than
    one parameter. An example of a control with two parameters is: "backup
    plan frequency is at least ``daily`` and the retention period is at
    least ``1 year``". The first parameter is ``daily``. The second
    parameter is ``1 year``.
    """

    ParameterName: ParameterName | None
    ParameterValue: ParameterValue | None


ControlInputParameters = list[ControlInputParameter]
stringMap = dict[string, string]
ResourceTypeList = list[ARN]


class ControlScope(TypedDict, total=False):
    """A framework consists of one or more controls. Each control has its own
    control scope. The control scope can include one or more resource types,
    a combination of a tag key and value, or a combination of one resource
    type and one resource ID. If no scope is specified, evaluations for the
    rule are triggered when any resource in your recording group changes in
    configuration.

    To set a control scope that includes all of a particular resource, leave
    the ``ControlScope`` empty or do not pass it when calling
    ``CreateFramework``.
    """

    ComplianceResourceIds: ComplianceResourceIdList | None
    ComplianceResourceTypes: ResourceTypeList | None
    Tags: stringMap | None


CopyJobChildJobsInState = dict[CopyJobState, Long]


class CopyJob(TypedDict, total=False):
    """Contains detailed information about a copy job."""

    AccountId: AccountId | None
    CopyJobId: string | None
    SourceBackupVaultArn: ARN | None
    SourceRecoveryPointArn: ARN | None
    DestinationBackupVaultArn: ARN | None
    DestinationVaultType: string | None
    DestinationVaultLockState: string | None
    DestinationRecoveryPointArn: ARN | None
    DestinationEncryptionKeyArn: ARN | None
    DestinationRecoveryPointLifecycle: Lifecycle | None
    ResourceArn: ARN | None
    CreationDate: timestamp | None
    CompletionDate: timestamp | None
    State: CopyJobState | None
    StatusMessage: string | None
    BackupSizeInBytes: Long | None
    IamRoleArn: IAMRoleArn | None
    CreatedBy: RecoveryPointCreator | None
    CreatedByBackupJobId: string | None
    ResourceType: ResourceType | None
    ParentJobId: string | None
    IsParent: boolean | None
    CompositeMemberIdentifier: string | None
    NumberOfChildJobs: Long | None
    ChildJobsInState: CopyJobChildJobsInState | None
    ResourceName: string | None
    MessageCategory: string | None


class CopyJobSummary(TypedDict, total=False):
    """This is a summary of copy jobs created or running within the most recent
    30 days.

    The returned summary may contain the following: Region, Account, State,
    RestourceType, MessageCategory, StartTime, EndTime, and Count of
    included jobs.
    """

    Region: Region | None
    AccountId: AccountId | None
    State: CopyJobStatus | None
    ResourceType: ResourceType | None
    MessageCategory: MessageCategory | None
    Count: integer | None
    StartTime: timestamp | None
    EndTime: timestamp | None


CopyJobSummaryList = list[CopyJobSummary]
CopyJobsList = list[CopyJob]


class CreateBackupPlanInput(ServiceRequest):
    BackupPlan: BackupPlanInput
    BackupPlanTags: Tags | None
    CreatorRequestId: string | None


class CreateBackupPlanOutput(TypedDict, total=False):
    BackupPlanId: string | None
    BackupPlanArn: ARN | None
    CreationDate: timestamp | None
    VersionId: string | None
    AdvancedBackupSettings: AdvancedBackupSettings | None


class CreateBackupSelectionInput(ServiceRequest):
    BackupPlanId: string
    BackupSelection: BackupSelection
    CreatorRequestId: string | None


class CreateBackupSelectionOutput(TypedDict, total=False):
    SelectionId: string | None
    BackupPlanId: string | None
    CreationDate: timestamp | None


class CreateBackupVaultInput(ServiceRequest):
    BackupVaultName: BackupVaultName
    BackupVaultTags: Tags | None
    EncryptionKeyArn: ARN | None
    CreatorRequestId: string | None


class CreateBackupVaultOutput(TypedDict, total=False):
    BackupVaultName: BackupVaultName | None
    BackupVaultArn: ARN | None
    CreationDate: timestamp | None


class FrameworkControl(TypedDict, total=False):
    """Contains detailed information about all of the controls of a framework.
    Each framework must contain at least one control.
    """

    ControlName: ControlName
    ControlInputParameters: ControlInputParameters | None
    ControlScope: ControlScope | None


FrameworkControls = list[FrameworkControl]


class CreateFrameworkInput(ServiceRequest):
    FrameworkName: FrameworkName
    FrameworkDescription: FrameworkDescription | None
    FrameworkControls: FrameworkControls
    IdempotencyToken: string | None
    FrameworkTags: stringMap | None


class CreateFrameworkOutput(TypedDict, total=False):
    FrameworkName: FrameworkName | None
    FrameworkArn: ARN | None


class DateRange(TypedDict, total=False):
    """This is a resource filter containing FromDate: DateTime and ToDate:
    DateTime. Both values are required. Future DateTime values are not
    permitted.

    The date and time are in Unix format and Coordinated Universal Time
    (UTC), and it is accurate to milliseconds ((milliseconds are optional).
    For example, the value 1516925490.087 represents Friday, January 26,
    2018 12:11:30.087 AM.
    """

    FromDate: timestamp
    ToDate: timestamp


ResourceIdentifiers = list[string]
VaultNames = list[string]


class RecoveryPointSelection(TypedDict, total=False):
    """This specifies criteria to assign a set of resources, such as resource
    types or backup vaults.
    """

    VaultNames: VaultNames | None
    ResourceIdentifiers: ResourceIdentifiers | None
    DateRange: DateRange | None


class CreateLegalHoldInput(ServiceRequest):
    Title: string
    Description: string
    IdempotencyToken: string | None
    RecoveryPointSelection: RecoveryPointSelection | None
    Tags: Tags | None


class CreateLegalHoldOutput(TypedDict, total=False):
    Title: string | None
    Status: LegalHoldStatus | None
    Description: string | None
    LegalHoldId: string | None
    LegalHoldArn: ARN | None
    CreationDate: timestamp | None
    RecoveryPointSelection: RecoveryPointSelection | None


class CreateLogicallyAirGappedBackupVaultInput(ServiceRequest):
    BackupVaultName: BackupVaultName
    BackupVaultTags: Tags | None
    CreatorRequestId: string | None
    MinRetentionDays: Long
    MaxRetentionDays: Long
    EncryptionKeyArn: ARN | None


class CreateLogicallyAirGappedBackupVaultOutput(TypedDict, total=False):
    BackupVaultName: BackupVaultName | None
    BackupVaultArn: ARN | None
    CreationDate: timestamp | None
    VaultState: VaultState | None


stringList = list[string]


class ReportSetting(TypedDict, total=False):
    """Contains detailed information about a report setting."""

    ReportTemplate: string
    FrameworkArns: stringList | None
    NumberOfFrameworks: integer | None
    Accounts: stringList | None
    OrganizationUnits: stringList | None
    Regions: stringList | None


FormatList = list[string]


class ReportDeliveryChannel(TypedDict, total=False):
    """Contains information from your report plan about where to deliver your
    reports, specifically your Amazon S3 bucket name, S3 key prefix, and the
    formats of your reports.
    """

    S3BucketName: string
    S3KeyPrefix: string | None
    Formats: FormatList | None


class CreateReportPlanInput(ServiceRequest):
    ReportPlanName: ReportPlanName
    ReportPlanDescription: ReportPlanDescription | None
    ReportDeliveryChannel: ReportDeliveryChannel
    ReportSetting: ReportSetting
    ReportPlanTags: stringMap | None
    IdempotencyToken: string | None


class CreateReportPlanOutput(TypedDict, total=False):
    ReportPlanName: ReportPlanName | None
    ReportPlanArn: ARN | None
    CreationTime: timestamp | None


class CreateRestoreAccessBackupVaultInput(ServiceRequest):
    SourceBackupVaultArn: ARN
    BackupVaultName: BackupVaultName | None
    BackupVaultTags: Tags | None
    CreatorRequestId: string | None
    RequesterComment: RequesterComment | None


class CreateRestoreAccessBackupVaultOutput(TypedDict, total=False):
    RestoreAccessBackupVaultArn: ARN | None
    VaultState: VaultState | None
    RestoreAccessBackupVaultName: BackupVaultName | None
    CreationDate: timestamp | None


SensitiveStringMap = dict[String, String]
RestoreTestingRecoveryPointTypeList = list[RestoreTestingRecoveryPointType]


class RestoreTestingRecoveryPointSelection(TypedDict, total=False):
    """``RecoveryPointSelection`` has five parameters (three required and two
    optional). The values you specify determine which recovery point is
    included in the restore test. You must indicate with ``Algorithm`` if
    you want the latest recovery point within your ``SelectionWindowDays``
    or if you want a random recovery point, and you must indicate through
    ``IncludeVaults`` from which vaults the recovery points can be chosen.

    ``Algorithm`` (*required*) Valid values: "``LATEST_WITHIN_WINDOW``" or
    "``RANDOM_WITHIN_WINDOW``".

    ``Recovery point types`` (*required*) Valid values: "``SNAPSHOT``"
    and/or "``CONTINUOUS``". Include ``SNAPSHOT`` to restore only snapshot
    recovery points; include ``CONTINUOUS`` to restore continuous recovery
    points (point in time restore / PITR); use both to restore either a
    snapshot or a continuous recovery point. The recovery point will be
    determined by the value for ``Algorithm``.

    ``IncludeVaults`` (*required*). You must include one or more backup
    vaults. Use the wildcard ["*"] or specific ARNs.

    ``SelectionWindowDays`` (*optional*) Value must be an integer (in days)
    from 1 to 365. If not included, the value defaults to ``30``.

    ``ExcludeVaults`` (*optional*). You can choose to input one or more
    specific backup vault ARNs to exclude those vaults' contents from
    restore eligibility. Or, you can include a list of selectors. If this
    parameter and its value are not included, it defaults to empty list.
    """

    Algorithm: RestoreTestingRecoveryPointSelectionAlgorithm | None
    ExcludeVaults: stringList | None
    IncludeVaults: stringList | None
    RecoveryPointTypes: RestoreTestingRecoveryPointTypeList | None
    SelectionWindowDays: integer | None


class RestoreTestingPlanForCreate(TypedDict, total=False):
    """This contains metadata about a restore testing plan."""

    RecoveryPointSelection: RestoreTestingRecoveryPointSelection
    RestoreTestingPlanName: String
    ScheduleExpression: String
    ScheduleExpressionTimezone: String | None
    StartWindowHours: integer | None


class CreateRestoreTestingPlanInput(ServiceRequest):
    CreatorRequestId: String | None
    RestoreTestingPlan: RestoreTestingPlanForCreate
    Tags: SensitiveStringMap | None


Timestamp = datetime


class CreateRestoreTestingPlanOutput(TypedDict, total=False):
    CreationTime: Timestamp
    RestoreTestingPlanArn: String
    RestoreTestingPlanName: String


class KeyValue(TypedDict, total=False):
    """Pair of two related strings. Allowed characters are letters, white
    space, and numbers that can be represented in UTF-8 and the following
    characters: ``+ - = . _ : /``
    """

    Key: String
    Value: String


KeyValueList = list[KeyValue]


class ProtectedResourceConditions(TypedDict, total=False):
    """The conditions that you define for resources in your restore testing
    plan using tags.
    """

    StringEquals: KeyValueList | None
    StringNotEquals: KeyValueList | None


class RestoreTestingSelectionForCreate(TypedDict, total=False):
    """This contains metadata about a specific restore testing selection.

    ProtectedResourceType is required, such as Amazon EBS or Amazon EC2.

    This consists of ``RestoreTestingSelectionName``,
    ``ProtectedResourceType``, and one of the following:

    -  ``ProtectedResourceArns``

    -  ``ProtectedResourceConditions``

    Each protected resource type can have one single value.

    A restore testing selection can include a wildcard value ("*") for
    ``ProtectedResourceArns`` along with ``ProtectedResourceConditions``.
    Alternatively, you can include up to 30 specific protected resource ARNs
    in ``ProtectedResourceArns``.

    ``ProtectedResourceConditions`` examples include as ``StringEquals`` and
    ``StringNotEquals``.
    """

    IamRoleArn: String
    ProtectedResourceArns: stringList | None
    ProtectedResourceConditions: ProtectedResourceConditions | None
    ProtectedResourceType: String
    RestoreMetadataOverrides: SensitiveStringMap | None
    RestoreTestingSelectionName: String
    ValidationWindowHours: integer | None


class CreateRestoreTestingSelectionInput(ServiceRequest):
    CreatorRequestId: String | None
    RestoreTestingPlanName: String
    RestoreTestingSelection: RestoreTestingSelectionForCreate


class CreateRestoreTestingSelectionOutput(TypedDict, total=False):
    CreationTime: Timestamp
    RestoreTestingPlanArn: String
    RestoreTestingPlanName: String
    RestoreTestingSelectionName: String


class ResourceSelection(TypedDict, total=False):
    """This contains metadata about resource selection for tiering
    configurations.

    You can specify up to 5 different resource selections per tiering
    configuration. Data moved to lower-cost tier remains there until
    deletion (one-way transition).
    """

    Resources: ResourceArns
    TieringDownSettingsInDays: TieringDownSettingsInDays
    ResourceType: ResourceType


ResourceSelections = list[ResourceSelection]


class TieringConfigurationInputForCreate(TypedDict, total=False):
    """This contains metadata about a tiering configuration for create
    operations.
    """

    TieringConfigurationName: TieringConfigurationName
    BackupVaultName: BackupVaultNameOrWildcard
    ResourceSelection: ResourceSelections


class CreateTieringConfigurationInput(ServiceRequest):
    TieringConfiguration: TieringConfigurationInputForCreate
    TieringConfigurationTags: Tags | None
    CreatorRequestId: CreatorRequestId | None


class CreateTieringConfigurationOutput(TypedDict, total=False):
    TieringConfigurationArn: ARN | None
    TieringConfigurationName: string | None
    CreationTime: timestamp | None


class DeleteBackupPlanInput(ServiceRequest):
    BackupPlanId: string


class DeleteBackupPlanOutput(TypedDict, total=False):
    BackupPlanId: string | None
    BackupPlanArn: ARN | None
    DeletionDate: timestamp | None
    VersionId: string | None


class DeleteBackupSelectionInput(ServiceRequest):
    BackupPlanId: string
    SelectionId: string


class DeleteBackupVaultAccessPolicyInput(ServiceRequest):
    BackupVaultName: BackupVaultName


class DeleteBackupVaultInput(ServiceRequest):
    BackupVaultName: string


class DeleteBackupVaultLockConfigurationInput(ServiceRequest):
    BackupVaultName: BackupVaultName


class DeleteBackupVaultNotificationsInput(ServiceRequest):
    BackupVaultName: BackupVaultName


class DeleteFrameworkInput(ServiceRequest):
    FrameworkName: FrameworkName


class DeleteRecoveryPointInput(ServiceRequest):
    BackupVaultName: BackupVaultName
    RecoveryPointArn: ARN


class DeleteReportPlanInput(ServiceRequest):
    ReportPlanName: ReportPlanName


class DeleteRestoreTestingPlanInput(ServiceRequest):
    RestoreTestingPlanName: String


class DeleteRestoreTestingSelectionInput(ServiceRequest):
    RestoreTestingPlanName: String
    RestoreTestingSelectionName: String


class DeleteTieringConfigurationInput(ServiceRequest):
    TieringConfigurationName: TieringConfigurationName


class DeleteTieringConfigurationOutput(TypedDict, total=False):
    pass


class DescribeBackupJobInput(ServiceRequest):
    BackupJobId: string


class DescribeBackupJobOutput(TypedDict, total=False):
    AccountId: AccountId | None
    BackupJobId: string | None
    BackupVaultName: BackupVaultName | None
    RecoveryPointLifecycle: Lifecycle | None
    BackupVaultArn: ARN | None
    VaultType: string | None
    VaultLockState: string | None
    RecoveryPointArn: ARN | None
    EncryptionKeyArn: ARN | None
    IsEncrypted: boolean | None
    ResourceArn: ARN | None
    CreationDate: timestamp | None
    CompletionDate: timestamp | None
    State: BackupJobState | None
    StatusMessage: string | None
    PercentDone: string | None
    BackupSizeInBytes: Long | None
    IamRoleArn: IAMRoleArn | None
    CreatedBy: RecoveryPointCreator | None
    ResourceType: ResourceType | None
    BytesTransferred: Long | None
    ExpectedCompletionDate: timestamp | None
    StartBy: timestamp | None
    BackupOptions: BackupOptions | None
    BackupType: string | None
    ParentJobId: string | None
    IsParent: boolean | None
    NumberOfChildJobs: Long | None
    ChildJobsInState: BackupJobChildJobsInState | None
    ResourceName: string | None
    InitiationDate: timestamp | None
    MessageCategory: string | None


class DescribeBackupVaultInput(ServiceRequest):
    BackupVaultName: string
    BackupVaultAccountId: string | None


class LatestMpaApprovalTeamUpdate(TypedDict, total=False):
    """Contains information about the latest update to an MPA approval team
    association.
    """

    MpaSessionArn: ARN | None
    Status: MpaSessionStatus | None
    StatusMessage: string | None
    InitiationDate: timestamp | None
    ExpiryDate: timestamp | None


class DescribeBackupVaultOutput(TypedDict, total=False):
    BackupVaultName: string | None
    BackupVaultArn: ARN | None
    VaultType: VaultType | None
    VaultState: VaultState | None
    EncryptionKeyArn: ARN | None
    CreationDate: timestamp | None
    CreatorRequestId: string | None
    NumberOfRecoveryPoints: long | None
    Locked: Boolean | None
    MinRetentionDays: Long | None
    MaxRetentionDays: Long | None
    LockDate: timestamp | None
    SourceBackupVaultArn: ARN | None
    MpaApprovalTeamArn: ARN | None
    MpaSessionArn: ARN | None
    LatestMpaApprovalTeamUpdate: LatestMpaApprovalTeamUpdate | None
    EncryptionKeyType: EncryptionKeyType | None


class DescribeCopyJobInput(ServiceRequest):
    CopyJobId: string


class DescribeCopyJobOutput(TypedDict, total=False):
    CopyJob: CopyJob | None


class DescribeFrameworkInput(ServiceRequest):
    FrameworkName: FrameworkName


class DescribeFrameworkOutput(TypedDict, total=False):
    FrameworkName: FrameworkName | None
    FrameworkArn: ARN | None
    FrameworkDescription: FrameworkDescription | None
    FrameworkControls: FrameworkControls | None
    CreationTime: timestamp | None
    DeploymentStatus: string | None
    FrameworkStatus: string | None
    IdempotencyToken: string | None


class DescribeGlobalSettingsInput(ServiceRequest):
    pass


GlobalSettings = dict[GlobalSettingsName, GlobalSettingsValue]


class DescribeGlobalSettingsOutput(TypedDict, total=False):
    GlobalSettings: GlobalSettings | None
    LastUpdateTime: timestamp | None


class DescribeProtectedResourceInput(ServiceRequest):
    ResourceArn: ARN


class DescribeProtectedResourceOutput(TypedDict, total=False):
    ResourceArn: ARN | None
    ResourceType: ResourceType | None
    LastBackupTime: timestamp | None
    ResourceName: string | None
    LastBackupVaultArn: ARN | None
    LastRecoveryPointArn: ARN | None
    LatestRestoreExecutionTimeMinutes: Long | None
    LatestRestoreJobCreationDate: timestamp | None
    LatestRestoreRecoveryPointCreationDate: timestamp | None


class DescribeRecoveryPointInput(ServiceRequest):
    BackupVaultName: BackupVaultName
    RecoveryPointArn: ARN
    BackupVaultAccountId: AccountId | None


class ScanResult(TypedDict, total=False):
    """Contains the results of a security scan, including scanner information,
    scan state, and any findings discovered.
    """

    MalwareScanner: MalwareScanner | None
    ScanJobState: ScanJobState | None
    LastScanTimestamp: timestamp | None
    Findings: ScanFindings | None


ScanResults = list[ScanResult]


class DescribeRecoveryPointOutput(TypedDict, total=False):
    RecoveryPointArn: ARN | None
    BackupVaultName: BackupVaultName | None
    BackupVaultArn: ARN | None
    SourceBackupVaultArn: ARN | None
    ResourceArn: ARN | None
    ResourceType: ResourceType | None
    CreatedBy: RecoveryPointCreator | None
    IamRoleArn: IAMRoleArn | None
    Status: RecoveryPointStatus | None
    StatusMessage: string | None
    CreationDate: timestamp | None
    InitiationDate: timestamp | None
    CompletionDate: timestamp | None
    BackupSizeInBytes: Long | None
    CalculatedLifecycle: CalculatedLifecycle | None
    Lifecycle: Lifecycle | None
    EncryptionKeyArn: ARN | None
    IsEncrypted: boolean | None
    StorageClass: StorageClass | None
    LastRestoreTime: timestamp | None
    ParentRecoveryPointArn: ARN | None
    CompositeMemberIdentifier: string | None
    IsParent: boolean | None
    ResourceName: string | None
    VaultType: VaultType | None
    IndexStatus: IndexStatus | None
    IndexStatusMessage: string | None
    EncryptionKeyType: EncryptionKeyType | None
    ScanResults: ScanResults | None


class DescribeRegionSettingsInput(ServiceRequest):
    pass


ResourceTypeManagementPreference = dict[ResourceType, IsEnabled]
ResourceTypeOptInPreference = dict[ResourceType, IsEnabled]


class DescribeRegionSettingsOutput(TypedDict, total=False):
    ResourceTypeOptInPreference: ResourceTypeOptInPreference | None
    ResourceTypeManagementPreference: ResourceTypeManagementPreference | None


class DescribeReportJobInput(ServiceRequest):
    ReportJobId: ReportJobId


class ReportDestination(TypedDict, total=False):
    """Contains information from your report job about your report destination."""

    S3BucketName: string | None
    S3Keys: stringList | None


class ReportJob(TypedDict, total=False):
    """Contains detailed information about a report job. A report job compiles
    a report based on a report plan and publishes it to Amazon S3.
    """

    ReportJobId: ReportJobId | None
    ReportPlanArn: ARN | None
    ReportTemplate: string | None
    CreationTime: timestamp | None
    CompletionTime: timestamp | None
    Status: string | None
    StatusMessage: string | None
    ReportDestination: ReportDestination | None


class DescribeReportJobOutput(TypedDict, total=False):
    ReportJob: ReportJob | None


class DescribeReportPlanInput(ServiceRequest):
    ReportPlanName: ReportPlanName


class ReportPlan(TypedDict, total=False):
    """Contains detailed information about a report plan."""

    ReportPlanArn: ARN | None
    ReportPlanName: ReportPlanName | None
    ReportPlanDescription: ReportPlanDescription | None
    ReportSetting: ReportSetting | None
    ReportDeliveryChannel: ReportDeliveryChannel | None
    DeploymentStatus: string | None
    CreationTime: timestamp | None
    LastAttemptedExecutionTime: timestamp | None
    LastSuccessfulExecutionTime: timestamp | None


class DescribeReportPlanOutput(TypedDict, total=False):
    ReportPlan: ReportPlan | None


class DescribeRestoreJobInput(ServiceRequest):
    RestoreJobId: RestoreJobId


class RestoreJobCreator(TypedDict, total=False):
    """Contains information about the restore testing plan that Backup used to
    initiate the restore job.
    """

    RestoreTestingPlanArn: ARN | None


class DescribeRestoreJobOutput(TypedDict, total=False):
    AccountId: AccountId | None
    RestoreJobId: string | None
    RecoveryPointArn: ARN | None
    SourceResourceArn: ARN | None
    BackupVaultArn: ARN | None
    CreationDate: timestamp | None
    CompletionDate: timestamp | None
    Status: RestoreJobStatus | None
    StatusMessage: string | None
    PercentDone: string | None
    BackupSizeInBytes: Long | None
    IamRoleArn: IAMRoleArn | None
    ExpectedCompletionTimeMinutes: Long | None
    CreatedResourceArn: ARN | None
    ResourceType: ResourceType | None
    RecoveryPointCreationDate: timestamp | None
    CreatedBy: RestoreJobCreator | None
    ValidationStatus: RestoreValidationStatus | None
    ValidationStatusMessage: string | None
    DeletionStatus: RestoreDeletionStatus | None
    DeletionStatusMessage: string | None
    IsParent: boolean | None
    ParentJobId: string | None


class DescribeScanJobInput(ServiceRequest):
    ScanJobId: String


class ScanResultInfo(TypedDict, total=False):
    """Contains information about the results of a scan job."""

    ScanResultStatus: ScanResultStatus


class ScanJobCreator(TypedDict, total=False):
    """Contains identifying information about the creation of a scan job,
    including the backup plan and rule that initiated the scan.
    """

    BackupPlanArn: String
    BackupPlanId: String
    BackupPlanVersion: String
    BackupRuleId: String


class DescribeScanJobOutput(TypedDict, total=False):
    AccountId: String
    BackupVaultArn: String
    BackupVaultName: String
    CompletionDate: Timestamp | None
    CreatedBy: ScanJobCreator
    CreationDate: Timestamp
    IamRoleArn: String
    MalwareScanner: MalwareScanner
    RecoveryPointArn: String
    ResourceArn: String
    ResourceName: String
    ResourceType: ScanResourceType
    ScanBaseRecoveryPointArn: String | None
    ScanId: String | None
    ScanJobId: String
    ScanMode: ScanMode
    ScanResult: ScanResultInfo | None
    ScannerRoleArn: String
    State: ScanState
    StatusMessage: String | None


class DisassociateBackupVaultMpaApprovalTeamInput(ServiceRequest):
    BackupVaultName: BackupVaultName
    RequesterComment: RequesterComment | None


class DisassociateRecoveryPointFromParentInput(ServiceRequest):
    BackupVaultName: BackupVaultName
    RecoveryPointArn: ARN


class DisassociateRecoveryPointInput(ServiceRequest):
    BackupVaultName: BackupVaultName
    RecoveryPointArn: ARN


class ExportBackupPlanTemplateInput(ServiceRequest):
    BackupPlanId: string


class ExportBackupPlanTemplateOutput(TypedDict, total=False):
    BackupPlanTemplateJson: string | None


class Framework(TypedDict, total=False):
    """Contains detailed information about a framework. Frameworks contain
    controls, which evaluate and report on your backup events and resources.
    Frameworks generate daily compliance results.
    """

    FrameworkName: FrameworkName | None
    FrameworkArn: ARN | None
    FrameworkDescription: FrameworkDescription | None
    NumberOfControls: integer | None
    CreationTime: timestamp | None
    DeploymentStatus: string | None


FrameworkList = list[Framework]


class GetBackupPlanFromJSONInput(ServiceRequest):
    BackupPlanTemplateJson: string


class GetBackupPlanFromJSONOutput(TypedDict, total=False):
    BackupPlan: BackupPlan | None


class GetBackupPlanFromTemplateInput(ServiceRequest):
    BackupPlanTemplateId: string


class GetBackupPlanFromTemplateOutput(TypedDict, total=False):
    BackupPlanDocument: BackupPlan | None


class GetBackupPlanInput(ServiceRequest):
    BackupPlanId: string
    VersionId: string | None
    MaxScheduledRunsPreview: MaxScheduledRunsPreview | None


class ScheduledPlanExecutionMember(TypedDict, total=False):
    """Contains information about a scheduled backup plan execution, including
    the execution time, rule type, and associated rule identifier.
    """

    ExecutionTime: timestamp | None
    RuleId: string | None
    RuleExecutionType: RuleExecutionType | None


ScheduledRunsPreview = list[ScheduledPlanExecutionMember]


class GetBackupPlanOutput(TypedDict, total=False):
    BackupPlan: BackupPlan | None
    BackupPlanId: string | None
    BackupPlanArn: ARN | None
    VersionId: string | None
    CreatorRequestId: string | None
    CreationDate: timestamp | None
    DeletionDate: timestamp | None
    LastExecutionDate: timestamp | None
    AdvancedBackupSettings: AdvancedBackupSettings | None
    ScheduledRunsPreview: ScheduledRunsPreview | None


class GetBackupSelectionInput(ServiceRequest):
    BackupPlanId: string
    SelectionId: string


class GetBackupSelectionOutput(TypedDict, total=False):
    BackupSelection: BackupSelection | None
    SelectionId: string | None
    BackupPlanId: string | None
    CreationDate: timestamp | None
    CreatorRequestId: string | None


class GetBackupVaultAccessPolicyInput(ServiceRequest):
    BackupVaultName: BackupVaultName


class GetBackupVaultAccessPolicyOutput(TypedDict, total=False):
    BackupVaultName: BackupVaultName | None
    BackupVaultArn: ARN | None
    Policy: IAMPolicy | None


class GetBackupVaultNotificationsInput(ServiceRequest):
    BackupVaultName: BackupVaultName


class GetBackupVaultNotificationsOutput(TypedDict, total=False):
    BackupVaultName: BackupVaultName | None
    BackupVaultArn: ARN | None
    SNSTopicArn: ARN | None
    BackupVaultEvents: BackupVaultEvents | None


class GetLegalHoldInput(ServiceRequest):
    LegalHoldId: string


class GetLegalHoldOutput(TypedDict, total=False):
    Title: string | None
    Status: LegalHoldStatus | None
    Description: string | None
    CancelDescription: string | None
    LegalHoldId: string | None
    LegalHoldArn: ARN | None
    CreationDate: timestamp | None
    CancellationDate: timestamp | None
    RetainRecordUntil: timestamp | None
    RecoveryPointSelection: RecoveryPointSelection | None


class GetRecoveryPointIndexDetailsInput(ServiceRequest):
    BackupVaultName: BackupVaultName
    RecoveryPointArn: ARN


class GetRecoveryPointIndexDetailsOutput(TypedDict, total=False):
    RecoveryPointArn: ARN | None
    BackupVaultArn: ARN | None
    SourceResourceArn: ARN | None
    IndexCreationDate: timestamp | None
    IndexDeletionDate: timestamp | None
    IndexCompletionDate: timestamp | None
    IndexStatus: IndexStatus | None
    IndexStatusMessage: string | None
    TotalItemsIndexed: Long | None


class GetRecoveryPointRestoreMetadataInput(ServiceRequest):
    BackupVaultName: BackupVaultName
    RecoveryPointArn: ARN
    BackupVaultAccountId: AccountId | None


Metadata = dict[MetadataKey, MetadataValue]


class GetRecoveryPointRestoreMetadataOutput(TypedDict, total=False):
    BackupVaultArn: ARN | None
    RecoveryPointArn: ARN | None
    RestoreMetadata: Metadata | None
    ResourceType: ResourceType | None


class GetRestoreJobMetadataInput(ServiceRequest):
    RestoreJobId: RestoreJobId


class GetRestoreJobMetadataOutput(TypedDict, total=False):
    RestoreJobId: RestoreJobId | None
    Metadata: Metadata | None


class GetRestoreTestingInferredMetadataInput(ServiceRequest):
    BackupVaultAccountId: String | None
    BackupVaultName: String
    RecoveryPointArn: String


class GetRestoreTestingInferredMetadataOutput(TypedDict, total=False):
    InferredMetadata: stringMap


class GetRestoreTestingPlanInput(ServiceRequest):
    RestoreTestingPlanName: String


class RestoreTestingPlanForGet(TypedDict, total=False):
    """This contains metadata about a restore testing plan."""

    CreationTime: Timestamp
    CreatorRequestId: String | None
    LastExecutionTime: Timestamp | None
    LastUpdateTime: Timestamp | None
    RecoveryPointSelection: RestoreTestingRecoveryPointSelection
    RestoreTestingPlanArn: String
    RestoreTestingPlanName: String
    ScheduleExpression: String
    ScheduleExpressionTimezone: String | None
    StartWindowHours: integer | None


class GetRestoreTestingPlanOutput(TypedDict, total=False):
    RestoreTestingPlan: RestoreTestingPlanForGet


class GetRestoreTestingSelectionInput(ServiceRequest):
    RestoreTestingPlanName: String
    RestoreTestingSelectionName: String


class RestoreTestingSelectionForGet(TypedDict, total=False):
    """This contains metadata about a restore testing selection."""

    CreationTime: Timestamp
    CreatorRequestId: String | None
    IamRoleArn: String
    ProtectedResourceArns: stringList | None
    ProtectedResourceConditions: ProtectedResourceConditions | None
    ProtectedResourceType: String
    RestoreMetadataOverrides: SensitiveStringMap | None
    RestoreTestingPlanName: String
    RestoreTestingSelectionName: String
    ValidationWindowHours: integer | None


class GetRestoreTestingSelectionOutput(TypedDict, total=False):
    RestoreTestingSelection: RestoreTestingSelectionForGet


class GetSupportedResourceTypesOutput(TypedDict, total=False):
    ResourceTypes: ResourceTypes | None


class GetTieringConfigurationInput(ServiceRequest):
    TieringConfigurationName: TieringConfigurationName


class TieringConfiguration(TypedDict, total=False):
    """This contains metadata about a tiering configuration."""

    TieringConfigurationName: TieringConfigurationName
    TieringConfigurationArn: ARN | None
    BackupVaultName: BackupVaultNameOrWildcard
    ResourceSelection: ResourceSelections
    CreatorRequestId: CreatorRequestId | None
    CreationTime: timestamp | None
    LastUpdatedTime: timestamp | None


class GetTieringConfigurationOutput(TypedDict, total=False):
    TieringConfiguration: TieringConfiguration | None


class IndexedRecoveryPoint(TypedDict, total=False):
    """This is a recovery point that has an associated backup index.

    Only recovery points with a backup index can be included in a search.
    """

    RecoveryPointArn: ARN | None
    SourceResourceArn: ARN | None
    IamRoleArn: ARN | None
    BackupCreationDate: timestamp | None
    ResourceType: ResourceType | None
    IndexCreationDate: timestamp | None
    IndexStatus: IndexStatus | None
    IndexStatusMessage: string | None
    BackupVaultArn: ARN | None


IndexedRecoveryPointList = list[IndexedRecoveryPoint]


class LatestRevokeRequest(TypedDict, total=False):
    """Contains information about the latest request to revoke access to a
    backup vault.
    """

    MpaSessionArn: string | None
    Status: MpaRevokeSessionStatus | None
    StatusMessage: string | None
    InitiationDate: timestamp | None
    ExpiryDate: timestamp | None


class LegalHold(TypedDict, total=False):
    """A legal hold is an administrative tool that helps prevent backups from
    being deleted while under a hold. While the hold is in place, backups
    under a hold cannot be deleted and lifecycle policies that would alter
    the backup status (such as transition to cold storage) are delayed until
    the legal hold is removed. A backup can have more than one legal hold.
    Legal holds are applied to one or more backups (also known as recovery
    points). These backups can be filtered by resource types and by resource
    IDs.
    """

    Title: string | None
    Status: LegalHoldStatus | None
    Description: string | None
    LegalHoldId: string | None
    LegalHoldArn: ARN | None
    CreationDate: timestamp | None
    CancellationDate: timestamp | None


LegalHoldsList = list[LegalHold]


class ListBackupJobSummariesInput(ServiceRequest):
    AccountId: AccountId | None
    State: BackupJobStatus | None
    ResourceType: ResourceType | None
    MessageCategory: MessageCategory | None
    AggregationPeriod: AggregationPeriod | None
    MaxResults: MaxResults | None
    NextToken: string | None


class ListBackupJobSummariesOutput(TypedDict, total=False):
    BackupJobSummaries: BackupJobSummaryList | None
    AggregationPeriod: string | None
    NextToken: string | None


class ListBackupJobsInput(ServiceRequest):
    NextToken: string | None
    MaxResults: MaxResults | None
    ByResourceArn: ARN | None
    ByState: BackupJobState | None
    ByBackupVaultName: BackupVaultName | None
    ByCreatedBefore: timestamp | None
    ByCreatedAfter: timestamp | None
    ByResourceType: ResourceType | None
    ByAccountId: AccountId | None
    ByCompleteAfter: timestamp | None
    ByCompleteBefore: timestamp | None
    ByParentJobId: string | None
    ByMessageCategory: string | None


class ListBackupJobsOutput(TypedDict, total=False):
    BackupJobs: BackupJobsList | None
    NextToken: string | None


class ListBackupPlanTemplatesInput(ServiceRequest):
    NextToken: string | None
    MaxResults: MaxResults | None


class ListBackupPlanTemplatesOutput(TypedDict, total=False):
    NextToken: string | None
    BackupPlanTemplatesList: BackupPlanTemplatesList | None


class ListBackupPlanVersionsInput(ServiceRequest):
    BackupPlanId: string
    NextToken: string | None
    MaxResults: MaxResults | None


class ListBackupPlanVersionsOutput(TypedDict, total=False):
    NextToken: string | None
    BackupPlanVersionsList: BackupPlanVersionsList | None


class ListBackupPlansInput(ServiceRequest):
    NextToken: string | None
    MaxResults: MaxResults | None
    IncludeDeleted: Boolean | None


class ListBackupPlansOutput(TypedDict, total=False):
    NextToken: string | None
    BackupPlansList: BackupPlansList | None


class ListBackupSelectionsInput(ServiceRequest):
    BackupPlanId: string
    NextToken: string | None
    MaxResults: MaxResults | None


class ListBackupSelectionsOutput(TypedDict, total=False):
    NextToken: string | None
    BackupSelectionsList: BackupSelectionsList | None


class ListBackupVaultsInput(ServiceRequest):
    ByVaultType: VaultType | None
    ByShared: boolean | None
    NextToken: string | None
    MaxResults: MaxResults | None


class ListBackupVaultsOutput(TypedDict, total=False):
    BackupVaultList: BackupVaultList | None
    NextToken: string | None


class ListCopyJobSummariesInput(ServiceRequest):
    AccountId: AccountId | None
    State: CopyJobStatus | None
    ResourceType: ResourceType | None
    MessageCategory: MessageCategory | None
    AggregationPeriod: AggregationPeriod | None
    MaxResults: MaxResults | None
    NextToken: string | None


class ListCopyJobSummariesOutput(TypedDict, total=False):
    CopyJobSummaries: CopyJobSummaryList | None
    AggregationPeriod: string | None
    NextToken: string | None


class ListCopyJobsInput(ServiceRequest):
    NextToken: string | None
    MaxResults: MaxResults | None
    ByResourceArn: ARN | None
    ByState: CopyJobState | None
    ByCreatedBefore: timestamp | None
    ByCreatedAfter: timestamp | None
    ByResourceType: ResourceType | None
    ByDestinationVaultArn: string | None
    ByAccountId: AccountId | None
    ByCompleteBefore: timestamp | None
    ByCompleteAfter: timestamp | None
    ByParentJobId: string | None
    ByMessageCategory: string | None
    BySourceRecoveryPointArn: string | None


class ListCopyJobsOutput(TypedDict, total=False):
    CopyJobs: CopyJobsList | None
    NextToken: string | None


class ListFrameworksInput(ServiceRequest):
    MaxResults: MaxFrameworkInputs | None
    NextToken: string | None


class ListFrameworksOutput(TypedDict, total=False):
    Frameworks: FrameworkList | None
    NextToken: string | None


class ListIndexedRecoveryPointsInput(ServiceRequest):
    NextToken: string | None
    MaxResults: MaxResults | None
    SourceResourceArn: ARN | None
    CreatedBefore: timestamp | None
    CreatedAfter: timestamp | None
    ResourceType: ResourceType | None
    IndexStatus: IndexStatus | None


class ListIndexedRecoveryPointsOutput(TypedDict, total=False):
    IndexedRecoveryPoints: IndexedRecoveryPointList | None
    NextToken: string | None


class ListLegalHoldsInput(ServiceRequest):
    NextToken: string | None
    MaxResults: MaxResults | None


class ListLegalHoldsOutput(TypedDict, total=False):
    NextToken: string | None
    LegalHolds: LegalHoldsList | None


class ListProtectedResourcesByBackupVaultInput(ServiceRequest):
    BackupVaultName: BackupVaultName
    BackupVaultAccountId: AccountId | None
    NextToken: string | None
    MaxResults: MaxResults | None


class ProtectedResource(TypedDict, total=False):
    """A structure that contains information about a backed-up resource."""

    ResourceArn: ARN | None
    ResourceType: ResourceType | None
    LastBackupTime: timestamp | None
    ResourceName: string | None
    LastBackupVaultArn: ARN | None
    LastRecoveryPointArn: ARN | None


ProtectedResourcesList = list[ProtectedResource]


class ListProtectedResourcesByBackupVaultOutput(TypedDict, total=False):
    Results: ProtectedResourcesList | None
    NextToken: string | None


class ListProtectedResourcesInput(ServiceRequest):
    NextToken: string | None
    MaxResults: MaxResults | None


class ListProtectedResourcesOutput(TypedDict, total=False):
    Results: ProtectedResourcesList | None
    NextToken: string | None


class ListRecoveryPointsByBackupVaultInput(ServiceRequest):
    BackupVaultName: BackupVaultName
    BackupVaultAccountId: AccountId | None
    NextToken: string | None
    MaxResults: MaxResults | None
    ByResourceArn: ARN | None
    ByResourceType: ResourceType | None
    ByBackupPlanId: string | None
    ByCreatedBefore: timestamp | None
    ByCreatedAfter: timestamp | None
    ByParentRecoveryPointArn: ARN | None


class RecoveryPointByBackupVault(TypedDict, total=False):
    """Contains detailed information about the recovery points stored in a
    backup vault.
    """

    RecoveryPointArn: ARN | None
    BackupVaultName: BackupVaultName | None
    BackupVaultArn: ARN | None
    SourceBackupVaultArn: ARN | None
    ResourceArn: ARN | None
    ResourceType: ResourceType | None
    CreatedBy: RecoveryPointCreator | None
    IamRoleArn: IAMRoleArn | None
    Status: RecoveryPointStatus | None
    StatusMessage: string | None
    CreationDate: timestamp | None
    InitiationDate: timestamp | None
    CompletionDate: timestamp | None
    BackupSizeInBytes: Long | None
    CalculatedLifecycle: CalculatedLifecycle | None
    Lifecycle: Lifecycle | None
    EncryptionKeyArn: ARN | None
    IsEncrypted: boolean | None
    LastRestoreTime: timestamp | None
    ParentRecoveryPointArn: ARN | None
    CompositeMemberIdentifier: string | None
    IsParent: boolean | None
    ResourceName: string | None
    VaultType: VaultType | None
    IndexStatus: IndexStatus | None
    IndexStatusMessage: string | None
    EncryptionKeyType: EncryptionKeyType | None
    AggregatedScanResult: AggregatedScanResult | None


RecoveryPointByBackupVaultList = list[RecoveryPointByBackupVault]


class ListRecoveryPointsByBackupVaultOutput(TypedDict, total=False):
    NextToken: string | None
    RecoveryPoints: RecoveryPointByBackupVaultList | None


class ListRecoveryPointsByLegalHoldInput(ServiceRequest):
    LegalHoldId: string
    NextToken: string | None
    MaxResults: MaxResults | None


class RecoveryPointMember(TypedDict, total=False):
    """This is a recovery point which is a child (nested) recovery point of a
    parent (composite) recovery point. These recovery points can be
    disassociated from their parent (composite) recovery point, in which
    case they will no longer be a member.
    """

    RecoveryPointArn: ARN | None
    ResourceArn: ARN | None
    ResourceType: ResourceType | None
    BackupVaultName: BackupVaultName | None


RecoveryPointsList = list[RecoveryPointMember]


class ListRecoveryPointsByLegalHoldOutput(TypedDict, total=False):
    RecoveryPoints: RecoveryPointsList | None
    NextToken: string | None


class ListRecoveryPointsByResourceInput(ServiceRequest):
    ResourceArn: ARN
    NextToken: string | None
    MaxResults: MaxResults | None
    ManagedByAWSBackupOnly: boolean | None


class RecoveryPointByResource(TypedDict, total=False):
    """Contains detailed information about a saved recovery point."""

    RecoveryPointArn: ARN | None
    CreationDate: timestamp | None
    Status: RecoveryPointStatus | None
    StatusMessage: string | None
    EncryptionKeyArn: ARN | None
    BackupSizeBytes: Long | None
    BackupVaultName: BackupVaultName | None
    IsParent: boolean | None
    ParentRecoveryPointArn: ARN | None
    ResourceName: string | None
    VaultType: VaultType | None
    IndexStatus: IndexStatus | None
    IndexStatusMessage: string | None
    EncryptionKeyType: EncryptionKeyType | None
    AggregatedScanResult: AggregatedScanResult | None


RecoveryPointByResourceList = list[RecoveryPointByResource]


class ListRecoveryPointsByResourceOutput(TypedDict, total=False):
    NextToken: string | None
    RecoveryPoints: RecoveryPointByResourceList | None


class ListReportJobsInput(ServiceRequest):
    ByReportPlanName: ReportPlanName | None
    ByCreationBefore: timestamp | None
    ByCreationAfter: timestamp | None
    ByStatus: string | None
    MaxResults: MaxResults | None
    NextToken: string | None


ReportJobList = list[ReportJob]


class ListReportJobsOutput(TypedDict, total=False):
    ReportJobs: ReportJobList | None
    NextToken: string | None


class ListReportPlansInput(ServiceRequest):
    MaxResults: MaxResults | None
    NextToken: string | None


ReportPlanList = list[ReportPlan]


class ListReportPlansOutput(TypedDict, total=False):
    ReportPlans: ReportPlanList | None
    NextToken: string | None


class ListRestoreAccessBackupVaultsInput(ServiceRequest):
    BackupVaultName: BackupVaultName
    NextToken: string | None
    MaxResults: MaxResults | None


class RestoreAccessBackupVaultListMember(TypedDict, total=False):
    """Contains information about a restore access backup vault."""

    RestoreAccessBackupVaultArn: ARN | None
    CreationDate: timestamp | None
    ApprovalDate: timestamp | None
    VaultState: VaultState | None
    LatestRevokeRequest: LatestRevokeRequest | None


RestoreAccessBackupVaultList = list[RestoreAccessBackupVaultListMember]


class ListRestoreAccessBackupVaultsOutput(TypedDict, total=False):
    NextToken: string | None
    RestoreAccessBackupVaults: RestoreAccessBackupVaultList | None


class ListRestoreJobSummariesInput(ServiceRequest):
    AccountId: AccountId | None
    State: RestoreJobState | None
    ResourceType: ResourceType | None
    AggregationPeriod: AggregationPeriod | None
    MaxResults: MaxResults | None
    NextToken: string | None


class RestoreJobSummary(TypedDict, total=False):
    """This is a summary of restore jobs created or running within the most
    recent 30 days.

    The returned summary may contain the following: Region, Account, State,
    ResourceType, MessageCategory, StartTime, EndTime, and Count of included
    jobs.
    """

    Region: Region | None
    AccountId: AccountId | None
    State: RestoreJobState | None
    ResourceType: ResourceType | None
    Count: integer | None
    StartTime: timestamp | None
    EndTime: timestamp | None


RestoreJobSummaryList = list[RestoreJobSummary]


class ListRestoreJobSummariesOutput(TypedDict, total=False):
    RestoreJobSummaries: RestoreJobSummaryList | None
    AggregationPeriod: string | None
    NextToken: string | None


class ListRestoreJobsByProtectedResourceInput(ServiceRequest):
    ResourceArn: ARN
    ByStatus: RestoreJobStatus | None
    ByRecoveryPointCreationDateAfter: timestamp | None
    ByRecoveryPointCreationDateBefore: timestamp | None
    NextToken: string | None
    MaxResults: MaxResults | None


class RestoreJobsListMember(TypedDict, total=False):
    """Contains metadata about a restore job."""

    AccountId: AccountId | None
    RestoreJobId: string | None
    RecoveryPointArn: ARN | None
    SourceResourceArn: ARN | None
    BackupVaultArn: ARN | None
    CreationDate: timestamp | None
    CompletionDate: timestamp | None
    Status: RestoreJobStatus | None
    StatusMessage: string | None
    PercentDone: string | None
    BackupSizeInBytes: Long | None
    IamRoleArn: IAMRoleArn | None
    ExpectedCompletionTimeMinutes: Long | None
    CreatedResourceArn: ARN | None
    ResourceType: ResourceType | None
    RecoveryPointCreationDate: timestamp | None
    IsParent: boolean | None
    ParentJobId: string | None
    CreatedBy: RestoreJobCreator | None
    ValidationStatus: RestoreValidationStatus | None
    ValidationStatusMessage: string | None
    DeletionStatus: RestoreDeletionStatus | None
    DeletionStatusMessage: string | None


RestoreJobsList = list[RestoreJobsListMember]


class ListRestoreJobsByProtectedResourceOutput(TypedDict, total=False):
    RestoreJobs: RestoreJobsList | None
    NextToken: string | None


class ListRestoreJobsInput(ServiceRequest):
    NextToken: string | None
    MaxResults: MaxResults | None
    ByAccountId: AccountId | None
    ByResourceType: ResourceType | None
    ByCreatedBefore: timestamp | None
    ByCreatedAfter: timestamp | None
    ByStatus: RestoreJobStatus | None
    ByCompleteBefore: timestamp | None
    ByCompleteAfter: timestamp | None
    ByRestoreTestingPlanArn: ARN | None
    ByParentJobId: string | None


class ListRestoreJobsOutput(TypedDict, total=False):
    RestoreJobs: RestoreJobsList | None
    NextToken: string | None


class ListRestoreTestingPlansInput(ServiceRequest):
    MaxResults: ListRestoreTestingPlansInputMaxResultsInteger | None
    NextToken: String | None


class RestoreTestingPlanForList(TypedDict, total=False):
    """This contains metadata about a restore testing plan."""

    CreationTime: Timestamp
    LastExecutionTime: Timestamp | None
    LastUpdateTime: Timestamp | None
    RestoreTestingPlanArn: String
    RestoreTestingPlanName: String
    ScheduleExpression: String
    ScheduleExpressionTimezone: String | None
    StartWindowHours: integer | None


RestoreTestingPlans = list[RestoreTestingPlanForList]


class ListRestoreTestingPlansOutput(TypedDict, total=False):
    NextToken: String | None
    RestoreTestingPlans: RestoreTestingPlans


class ListRestoreTestingSelectionsInput(ServiceRequest):
    MaxResults: ListRestoreTestingSelectionsInputMaxResultsInteger | None
    NextToken: String | None
    RestoreTestingPlanName: String


class RestoreTestingSelectionForList(TypedDict, total=False):
    """This contains metadata about a restore testing selection."""

    CreationTime: Timestamp
    IamRoleArn: String
    ProtectedResourceType: String
    RestoreTestingPlanName: String
    RestoreTestingSelectionName: String
    ValidationWindowHours: integer | None


RestoreTestingSelections = list[RestoreTestingSelectionForList]


class ListRestoreTestingSelectionsOutput(TypedDict, total=False):
    NextToken: String | None
    RestoreTestingSelections: RestoreTestingSelections


class ListScanJobSummariesInput(ServiceRequest):
    AccountId: AccountId | None
    ResourceType: ResourceType | None
    MalwareScanner: MalwareScanner | None
    ScanResultStatus: ScanResultStatus | None
    State: ScanJobStatus | None
    AggregationPeriod: AggregationPeriod | None
    MaxResults: MaxResults | None
    NextToken: string | None


class ScanJobSummary(TypedDict, total=False):
    """Contains summary information about scan jobs, including counts and
    metadata for a specific time period and criteria.
    """

    Region: Region | None
    AccountId: AccountId | None
    State: ScanJobStatus | None
    ResourceType: ResourceType | None
    Count: integer | None
    StartTime: timestamp | None
    EndTime: timestamp | None
    MalwareScanner: MalwareScanner | None
    ScanResultStatus: ScanResultStatus | None


ScanJobSummaryList = list[ScanJobSummary]


class ListScanJobSummariesOutput(TypedDict, total=False):
    ScanJobSummaries: ScanJobSummaryList | None
    AggregationPeriod: string | None
    NextToken: string | None


class ListScanJobsInput(ServiceRequest):
    ByAccountId: String | None
    ByBackupVaultName: String | None
    ByCompleteAfter: Timestamp | None
    ByCompleteBefore: Timestamp | None
    ByMalwareScanner: MalwareScanner | None
    ByRecoveryPointArn: String | None
    ByResourceArn: String | None
    ByResourceType: ScanResourceType | None
    ByScanResultStatus: ScanResultStatus | None
    ByState: ScanState | None
    MaxResults: ListScanJobsInputMaxResultsInteger | None
    NextToken: String | None


class ScanJob(TypedDict, total=False):
    """Contains metadata about a scan job, including information about the
    scanning process, results, and associated resources.
    """

    AccountId: String
    BackupVaultArn: String
    BackupVaultName: String
    CompletionDate: Timestamp | None
    CreatedBy: ScanJobCreator
    CreationDate: Timestamp
    IamRoleArn: String
    MalwareScanner: MalwareScanner
    RecoveryPointArn: String
    ResourceArn: String
    ResourceName: String
    ResourceType: ScanResourceType
    ScanBaseRecoveryPointArn: String | None
    ScanId: String | None
    ScanJobId: String
    ScanMode: ScanMode
    ScanResult: ScanResultInfo | None
    ScannerRoleArn: String
    State: ScanState | None
    StatusMessage: String | None


ScanJobs = list[ScanJob]


class ListScanJobsOutput(TypedDict, total=False):
    NextToken: String | None
    ScanJobs: ScanJobs


class ListTagsInput(ServiceRequest):
    ResourceArn: ARN
    NextToken: string | None
    MaxResults: MaxResults | None


class ListTagsOutput(TypedDict, total=False):
    NextToken: string | None
    Tags: Tags | None


class ListTieringConfigurationsInput(ServiceRequest):
    MaxResults: MaxResults | None
    NextToken: string | None


class TieringConfigurationsListMember(TypedDict, total=False):
    """This contains metadata about a tiering configuration returned in a list."""

    TieringConfigurationArn: ARN | None
    TieringConfigurationName: TieringConfigurationName | None
    BackupVaultName: BackupVaultNameOrWildcard | None
    CreationTime: timestamp | None
    LastUpdatedTime: timestamp | None


TieringConfigurationsList = list[TieringConfigurationsListMember]


class ListTieringConfigurationsOutput(TypedDict, total=False):
    TieringConfigurations: TieringConfigurationsList | None
    NextToken: string | None


class PutBackupVaultAccessPolicyInput(ServiceRequest):
    BackupVaultName: BackupVaultName
    Policy: IAMPolicy | None


class PutBackupVaultLockConfigurationInput(ServiceRequest):
    BackupVaultName: BackupVaultName
    MinRetentionDays: Long | None
    MaxRetentionDays: Long | None
    ChangeableForDays: Long | None


class PutBackupVaultNotificationsInput(ServiceRequest):
    BackupVaultName: BackupVaultName
    SNSTopicArn: ARN
    BackupVaultEvents: BackupVaultEvents


class PutRestoreValidationResultInput(ServiceRequest):
    RestoreJobId: RestoreJobId
    ValidationStatus: RestoreValidationStatus
    ValidationStatusMessage: string | None


class RestoreTestingPlanForUpdate(TypedDict, total=False):
    """This contains metadata about a restore testing plan."""

    RecoveryPointSelection: RestoreTestingRecoveryPointSelection | None
    ScheduleExpression: String | None
    ScheduleExpressionTimezone: String | None
    StartWindowHours: integer | None


class RestoreTestingSelectionForUpdate(TypedDict, total=False):
    """This contains metadata about a restore testing selection."""

    IamRoleArn: String | None
    ProtectedResourceArns: stringList | None
    ProtectedResourceConditions: ProtectedResourceConditions | None
    RestoreMetadataOverrides: SensitiveStringMap | None
    ValidationWindowHours: integer | None


class RevokeRestoreAccessBackupVaultInput(ServiceRequest):
    BackupVaultName: BackupVaultName
    RestoreAccessBackupVaultArn: ARN
    RequesterComment: RequesterComment | None


class StartBackupJobInput(ServiceRequest):
    BackupVaultName: BackupVaultName
    LogicallyAirGappedBackupVaultArn: ARN | None
    ResourceArn: ARN
    IamRoleArn: IAMRoleArn
    IdempotencyToken: string | None
    StartWindowMinutes: WindowMinutes | None
    CompleteWindowMinutes: WindowMinutes | None
    Lifecycle: Lifecycle | None
    RecoveryPointTags: Tags | None
    BackupOptions: BackupOptions | None
    Index: Index | None


class StartBackupJobOutput(TypedDict, total=False):
    BackupJobId: string | None
    RecoveryPointArn: ARN | None
    CreationDate: timestamp | None
    IsParent: boolean | None


class StartCopyJobInput(ServiceRequest):
    RecoveryPointArn: ARN
    SourceBackupVaultName: BackupVaultName
    DestinationBackupVaultArn: ARN
    IamRoleArn: IAMRoleArn
    IdempotencyToken: string | None
    Lifecycle: Lifecycle | None


class StartCopyJobOutput(TypedDict, total=False):
    CopyJobId: string | None
    CreationDate: timestamp | None
    IsParent: boolean | None


class StartReportJobInput(ServiceRequest):
    ReportPlanName: ReportPlanName
    IdempotencyToken: string | None


class StartReportJobOutput(TypedDict, total=False):
    ReportJobId: ReportJobId | None


class StartRestoreJobInput(ServiceRequest):
    RecoveryPointArn: ARN
    Metadata: Metadata
    IamRoleArn: IAMRoleArn | None
    IdempotencyToken: string | None
    ResourceType: ResourceType | None
    CopySourceTagsToRestoredResource: boolean | None


class StartRestoreJobOutput(TypedDict, total=False):
    RestoreJobId: RestoreJobId | None


class StartScanJobInput(ServiceRequest):
    BackupVaultName: String
    IamRoleArn: String
    IdempotencyToken: String | None
    MalwareScanner: MalwareScanner
    RecoveryPointArn: String
    ScanBaseRecoveryPointArn: String | None
    ScanMode: ScanMode
    ScannerRoleArn: String


class StartScanJobOutput(TypedDict, total=False):
    CreationDate: Timestamp
    ScanJobId: String


class StopBackupJobInput(ServiceRequest):
    BackupJobId: string


TagKeyList = list[string]


class TagResourceInput(ServiceRequest):
    ResourceArn: ARN
    Tags: Tags


class TieringConfigurationInputForUpdate(TypedDict, total=False):
    """This contains metadata about a tiering configuration for update
    operations.
    """

    ResourceSelection: ResourceSelections
    BackupVaultName: BackupVaultNameOrWildcard


class UntagResourceInput(ServiceRequest):
    ResourceArn: ARN
    TagKeyList: TagKeyList


class UpdateBackupPlanInput(ServiceRequest):
    BackupPlanId: string
    BackupPlan: BackupPlanInput


class UpdateBackupPlanOutput(TypedDict, total=False):
    BackupPlanId: string | None
    BackupPlanArn: ARN | None
    CreationDate: timestamp | None
    VersionId: string | None
    AdvancedBackupSettings: AdvancedBackupSettings | None
    ScanSettings: ScanSettings | None


class UpdateFrameworkInput(ServiceRequest):
    FrameworkName: FrameworkName
    FrameworkDescription: FrameworkDescription | None
    FrameworkControls: FrameworkControls | None
    IdempotencyToken: string | None


class UpdateFrameworkOutput(TypedDict, total=False):
    FrameworkName: FrameworkName | None
    FrameworkArn: ARN | None
    CreationTime: timestamp | None


class UpdateGlobalSettingsInput(ServiceRequest):
    GlobalSettings: GlobalSettings | None


class UpdateRecoveryPointIndexSettingsInput(ServiceRequest):
    BackupVaultName: BackupVaultName
    RecoveryPointArn: ARN
    IamRoleArn: IAMRoleArn | None
    Index: Index


class UpdateRecoveryPointIndexSettingsOutput(TypedDict, total=False):
    BackupVaultName: BackupVaultName | None
    RecoveryPointArn: ARN | None
    IndexStatus: IndexStatus | None
    Index: Index | None


class UpdateRecoveryPointLifecycleInput(ServiceRequest):
    BackupVaultName: BackupVaultName
    RecoveryPointArn: ARN
    Lifecycle: Lifecycle | None


class UpdateRecoveryPointLifecycleOutput(TypedDict, total=False):
    BackupVaultArn: ARN | None
    RecoveryPointArn: ARN | None
    Lifecycle: Lifecycle | None
    CalculatedLifecycle: CalculatedLifecycle | None


class UpdateRegionSettingsInput(ServiceRequest):
    ResourceTypeOptInPreference: ResourceTypeOptInPreference | None
    ResourceTypeManagementPreference: ResourceTypeManagementPreference | None


class UpdateReportPlanInput(ServiceRequest):
    ReportPlanName: ReportPlanName
    ReportPlanDescription: ReportPlanDescription | None
    ReportDeliveryChannel: ReportDeliveryChannel | None
    ReportSetting: ReportSetting | None
    IdempotencyToken: string | None


class UpdateReportPlanOutput(TypedDict, total=False):
    ReportPlanName: ReportPlanName | None
    ReportPlanArn: ARN | None
    CreationTime: timestamp | None


class UpdateRestoreTestingPlanInput(ServiceRequest):
    RestoreTestingPlan: RestoreTestingPlanForUpdate
    RestoreTestingPlanName: String


class UpdateRestoreTestingPlanOutput(TypedDict, total=False):
    CreationTime: Timestamp
    RestoreTestingPlanArn: String
    RestoreTestingPlanName: String
    UpdateTime: Timestamp


class UpdateRestoreTestingSelectionInput(ServiceRequest):
    RestoreTestingPlanName: String
    RestoreTestingSelection: RestoreTestingSelectionForUpdate
    RestoreTestingSelectionName: String


class UpdateRestoreTestingSelectionOutput(TypedDict, total=False):
    CreationTime: Timestamp
    RestoreTestingPlanArn: String
    RestoreTestingPlanName: String
    RestoreTestingSelectionName: String
    UpdateTime: Timestamp


class UpdateTieringConfigurationInput(ServiceRequest):
    TieringConfigurationName: TieringConfigurationName
    TieringConfiguration: TieringConfigurationInputForUpdate


class UpdateTieringConfigurationOutput(TypedDict, total=False):
    TieringConfigurationArn: ARN | None
    TieringConfigurationName: TieringConfigurationName | None
    CreationTime: timestamp | None
    LastUpdatedTime: timestamp | None


class BackupApi:
    service: str = "backup"
    version: str = "2018-11-15"

    @handler("AssociateBackupVaultMpaApprovalTeam")
    def associate_backup_vault_mpa_approval_team(
        self,
        context: RequestContext,
        backup_vault_name: BackupVaultName,
        mpa_approval_team_arn: ARN,
        requester_comment: RequesterComment | None = None,
        **kwargs,
    ) -> None:
        """Associates an MPA approval team with a backup vault.

        :param backup_vault_name: The name of the backup vault to associate with the MPA approval team.
        :param mpa_approval_team_arn: The Amazon Resource Name (ARN) of the MPA approval team to associate
        with the backup vault.
        :param requester_comment: A comment provided by the requester explaining the association request.
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("CancelLegalHold")
    def cancel_legal_hold(
        self,
        context: RequestContext,
        legal_hold_id: string,
        cancel_description: string,
        retain_record_in_days: Long | None = None,
        **kwargs,
    ) -> CancelLegalHoldOutput:
        """Removes the specified legal hold on a recovery point. This action can
        only be performed by a user with sufficient permissions.

        :param legal_hold_id: The ID of the legal hold.
        :param cancel_description: A string the describes the reason for removing the legal hold.
        :param retain_record_in_days: The integer amount, in days, after which to remove legal hold.
        :returns: CancelLegalHoldOutput
        :raises InvalidParameterValueException:
        :raises InvalidResourceStateException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("CreateBackupPlan")
    def create_backup_plan(
        self,
        context: RequestContext,
        backup_plan: BackupPlanInput,
        backup_plan_tags: Tags | None = None,
        creator_request_id: string | None = None,
        **kwargs,
    ) -> CreateBackupPlanOutput:
        """Creates a backup plan using a backup plan name and backup rules. A
        backup plan is a document that contains information that Backup uses to
        schedule tasks that create recovery points for resources.

        If you call ``CreateBackupPlan`` with a plan that already exists, you
        receive an ``AlreadyExistsException`` exception.

        :param backup_plan: The body of a backup plan.
        :param backup_plan_tags: The tags to assign to the backup plan.
        :param creator_request_id: Identifies the request and allows failed requests to be retried without
        the risk of running the operation twice.
        :returns: CreateBackupPlanOutput
        :raises LimitExceededException:
        :raises AlreadyExistsException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("CreateBackupSelection")
    def create_backup_selection(
        self,
        context: RequestContext,
        backup_plan_id: string,
        backup_selection: BackupSelection,
        creator_request_id: string | None = None,
        **kwargs,
    ) -> CreateBackupSelectionOutput:
        """Creates a JSON document that specifies a set of resources to assign to a
        backup plan. For examples, see `Assigning resources
        programmatically <https://docs.aws.amazon.com/aws-backup/latest/devguide/assigning-resources.html#assigning-resources-json>`__.

        :param backup_plan_id: The ID of the backup plan.
        :param backup_selection: The body of a request to assign a set of resources to a backup plan.
        :param creator_request_id: A unique string that identifies the request and allows failed requests
        to be retried without the risk of running the operation twice.
        :returns: CreateBackupSelectionOutput
        :raises LimitExceededException:
        :raises AlreadyExistsException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("CreateBackupVault")
    def create_backup_vault(
        self,
        context: RequestContext,
        backup_vault_name: BackupVaultName,
        backup_vault_tags: Tags | None = None,
        encryption_key_arn: ARN | None = None,
        creator_request_id: string | None = None,
        **kwargs,
    ) -> CreateBackupVaultOutput:
        """Creates a logical container where backups are stored. A
        ``CreateBackupVault`` request includes a name, optionally one or more
        resource tags, an encryption key, and a request ID.

        Do not include sensitive data, such as passport numbers, in the name of
        a backup vault.

        :param backup_vault_name: The name of a logical container where backups are stored.
        :param backup_vault_tags: The tags to assign to the backup vault.
        :param encryption_key_arn: The server-side encryption key that is used to protect your backups; for
        example,
        ``arn:aws:kms:us-west-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab``.
        :param creator_request_id: A unique string that identifies the request and allows failed requests
        to be retried without the risk of running the operation twice.
        :returns: CreateBackupVaultOutput
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        :raises LimitExceededException:
        :raises AlreadyExistsException:
        """
        raise NotImplementedError

    @handler("CreateFramework")
    def create_framework(
        self,
        context: RequestContext,
        framework_name: FrameworkName,
        framework_controls: FrameworkControls,
        framework_description: FrameworkDescription | None = None,
        idempotency_token: string | None = None,
        framework_tags: stringMap | None = None,
        **kwargs,
    ) -> CreateFrameworkOutput:
        """Creates a framework with one or more controls. A framework is a
        collection of controls that you can use to evaluate your backup
        practices. By using pre-built customizable controls to define your
        policies, you can evaluate whether your backup practices comply with
        your policies and which resources are not yet in compliance.

        :param framework_name: The unique name of the framework.
        :param framework_controls: The controls that make up the framework.
        :param framework_description: An optional description of the framework with a maximum of 1,024
        characters.
        :param idempotency_token: A customer-chosen string that you can use to distinguish between
        otherwise identical calls to ``CreateFrameworkInput``.
        :param framework_tags: The tags to assign to the framework.
        :returns: CreateFrameworkOutput
        :raises AlreadyExistsException:
        :raises LimitExceededException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("CreateLegalHold")
    def create_legal_hold(
        self,
        context: RequestContext,
        title: string,
        description: string,
        idempotency_token: string | None = None,
        recovery_point_selection: RecoveryPointSelection | None = None,
        tags: Tags | None = None,
        **kwargs,
    ) -> CreateLegalHoldOutput:
        """Creates a legal hold on a recovery point (backup). A legal hold is a
        restraint on altering or deleting a backup until an authorized user
        cancels the legal hold. Any actions to delete or disassociate a recovery
        point will fail with an error if one or more active legal holds are on
        the recovery point.

        :param title: The title of the legal hold.
        :param description: The description of the legal hold.
        :param idempotency_token: This is a user-chosen string used to distinguish between otherwise
        identical calls.
        :param recovery_point_selection: The criteria to assign a set of resources, such as resource types or
        backup vaults.
        :param tags: Optional tags to include.
        :returns: CreateLegalHoldOutput
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("CreateLogicallyAirGappedBackupVault")
    def create_logically_air_gapped_backup_vault(
        self,
        context: RequestContext,
        backup_vault_name: BackupVaultName,
        min_retention_days: Long,
        max_retention_days: Long,
        backup_vault_tags: Tags | None = None,
        creator_request_id: string | None = None,
        encryption_key_arn: ARN | None = None,
        **kwargs,
    ) -> CreateLogicallyAirGappedBackupVaultOutput:
        """Creates a logical container to where backups may be copied.

        This request includes a name, the Region, the maximum number of
        retention days, the minimum number of retention days, and optionally can
        include tags and a creator request ID.

        Do not include sensitive data, such as passport numbers, in the name of
        a backup vault.

        :param backup_vault_name: The name of a logical container where backups are stored.
        :param min_retention_days: This setting specifies the minimum retention period that the vault
        retains its recovery points.
        :param max_retention_days: The maximum retention period that the vault retains its recovery points.
        :param backup_vault_tags: The tags to assign to the vault.
        :param creator_request_id: The ID of the creation request.
        :param encryption_key_arn: The ARN of the customer-managed KMS key to use for encrypting the
        logically air-gapped backup vault.
        :returns: CreateLogicallyAirGappedBackupVaultOutput
        :raises AlreadyExistsException:
        :raises InvalidParameterValueException:
        :raises LimitExceededException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("CreateReportPlan")
    def create_report_plan(
        self,
        context: RequestContext,
        report_plan_name: ReportPlanName,
        report_delivery_channel: ReportDeliveryChannel,
        report_setting: ReportSetting,
        report_plan_description: ReportPlanDescription | None = None,
        report_plan_tags: stringMap | None = None,
        idempotency_token: string | None = None,
        **kwargs,
    ) -> CreateReportPlanOutput:
        """Creates a report plan. A report plan is a document that contains
        information about the contents of the report and where Backup will
        deliver it.

        If you call ``CreateReportPlan`` with a plan that already exists, you
        receive an ``AlreadyExistsException`` exception.

        :param report_plan_name: The unique name of the report plan.
        :param report_delivery_channel: A structure that contains information about where and how to deliver
        your reports, specifically your Amazon S3 bucket name, S3 key prefix,
        and the formats of your reports.
        :param report_setting: Identifies the report template for the report.
        :param report_plan_description: An optional description of the report plan with a maximum of 1,024
        characters.
        :param report_plan_tags: The tags to assign to the report plan.
        :param idempotency_token: A customer-chosen string that you can use to distinguish between
        otherwise identical calls to ``CreateReportPlanInput``.
        :returns: CreateReportPlanOutput
        :raises AlreadyExistsException:
        :raises LimitExceededException:
        :raises InvalidParameterValueException:
        :raises ServiceUnavailableException:
        :raises MissingParameterValueException:
        """
        raise NotImplementedError

    @handler("CreateRestoreAccessBackupVault")
    def create_restore_access_backup_vault(
        self,
        context: RequestContext,
        source_backup_vault_arn: ARN,
        backup_vault_name: BackupVaultName | None = None,
        backup_vault_tags: Tags | None = None,
        creator_request_id: string | None = None,
        requester_comment: RequesterComment | None = None,
        **kwargs,
    ) -> CreateRestoreAccessBackupVaultOutput:
        """Creates a restore access backup vault that provides temporary access to
        recovery points in a logically air-gapped backup vault, subject to MPA
        approval.

        :param source_backup_vault_arn: The ARN of the source backup vault containing the recovery points to
        which temporary access is requested.
        :param backup_vault_name: The name of the backup vault to associate with an MPA approval team.
        :param backup_vault_tags: Optional tags to assign to the restore access backup vault.
        :param creator_request_id: A unique string that identifies the request and allows failed requests
        to be retried without the risk of executing the operation twice.
        :param requester_comment: A comment explaining the reason for requesting restore access to the
        backup vault.
        :returns: CreateRestoreAccessBackupVaultOutput
        :raises AlreadyExistsException:
        :raises InvalidParameterValueException:
        :raises LimitExceededException:
        :raises MissingParameterValueException:
        :raises ResourceNotFoundException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("CreateRestoreTestingPlan")
    def create_restore_testing_plan(
        self,
        context: RequestContext,
        restore_testing_plan: RestoreTestingPlanForCreate,
        creator_request_id: String | None = None,
        tags: SensitiveStringMap | None = None,
        **kwargs,
    ) -> CreateRestoreTestingPlanOutput:
        """Creates a restore testing plan.

        The first of two steps to create a restore testing plan. After this
        request is successful, finish the procedure using
        CreateRestoreTestingSelection.

        :param restore_testing_plan: A restore testing plan must contain a unique ``RestoreTestingPlanName``
        string you create and must contain a ``ScheduleExpression`` cron.
        :param creator_request_id: This is a unique string that identifies the request and allows failed
        requests to be retriedwithout the risk of running the operation twice.
        :param tags: The tags to assign to the restore testing plan.
        :returns: CreateRestoreTestingPlanOutput
        :raises AlreadyExistsException:
        :raises ConflictException:
        :raises InvalidParameterValueException:
        :raises LimitExceededException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("CreateRestoreTestingSelection")
    def create_restore_testing_selection(
        self,
        context: RequestContext,
        restore_testing_plan_name: String,
        restore_testing_selection: RestoreTestingSelectionForCreate,
        creator_request_id: String | None = None,
        **kwargs,
    ) -> CreateRestoreTestingSelectionOutput:
        """This request can be sent after CreateRestoreTestingPlan request returns
        successfully. This is the second part of creating a resource testing
        plan, and it must be completed sequentially.

        This consists of ``RestoreTestingSelectionName``,
        ``ProtectedResourceType``, and one of the following:

        -  ``ProtectedResourceArns``

        -  ``ProtectedResourceConditions``

        Each protected resource type can have one single value.

        A restore testing selection can include a wildcard value ("*") for
        ``ProtectedResourceArns`` along with ``ProtectedResourceConditions``.
        Alternatively, you can include up to 30 specific protected resource ARNs
        in ``ProtectedResourceArns``.

        Cannot select by both protected resource types AND specific ARNs.
        Request will fail if both are included.

        :param restore_testing_plan_name: Input the restore testing plan name that was returned from the related
        CreateRestoreTestingPlan request.
        :param restore_testing_selection: This consists of ``RestoreTestingSelectionName``,
        ``ProtectedResourceType``, and one of the following:

        -  ``ProtectedResourceArns``

        -  ``ProtectedResourceConditions``

        Each protected resource type can have one single value.
        :param creator_request_id: This is an optional unique string that identifies the request and allows
        failed requests to be retried without the risk of running the operation
        twice.
        :returns: CreateRestoreTestingSelectionOutput
        :raises AlreadyExistsException:
        :raises InvalidParameterValueException:
        :raises LimitExceededException:
        :raises MissingParameterValueException:
        :raises ResourceNotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("CreateTieringConfiguration")
    def create_tiering_configuration(
        self,
        context: RequestContext,
        tiering_configuration: TieringConfigurationInputForCreate,
        tiering_configuration_tags: Tags | None = None,
        creator_request_id: CreatorRequestId | None = None,
        **kwargs,
    ) -> CreateTieringConfigurationOutput:
        """Creates a tiering configuration.

        A tiering configuration enables automatic movement of backup data to a
        lower-cost storage tier based on the age of backed-up objects in the
        backup vault.

        Each vault can only have one vault-specific tiering configuration, in
        addition to any global configuration that applies to all vaults.

        :param tiering_configuration: A tiering configuration must contain a unique
        ``TieringConfigurationName`` string you create and must contain a
        ``BackupVaultName`` and ``ResourceSelection``.
        :param tiering_configuration_tags: The tags to assign to the tiering configuration.
        :param creator_request_id: This is a unique string that identifies the request and allows failed
        requests to be retried without the risk of running the operation twice.
        :returns: CreateTieringConfigurationOutput
        :raises AlreadyExistsException:
        :raises ConflictException:
        :raises InvalidParameterValueException:
        :raises LimitExceededException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DeleteBackupPlan")
    def delete_backup_plan(
        self, context: RequestContext, backup_plan_id: string, **kwargs
    ) -> DeleteBackupPlanOutput:
        """Deletes a backup plan. A backup plan can only be deleted after all
        associated selections of resources have been deleted. Deleting a backup
        plan deletes the current version of a backup plan. Previous versions, if
        any, will still exist.

        :param backup_plan_id: Uniquely identifies a backup plan.
        :returns: DeleteBackupPlanOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("DeleteBackupSelection")
    def delete_backup_selection(
        self, context: RequestContext, backup_plan_id: string, selection_id: string, **kwargs
    ) -> None:
        """Deletes the resource selection associated with a backup plan that is
        specified by the ``SelectionId``.

        :param backup_plan_id: Uniquely identifies a backup plan.
        :param selection_id: Uniquely identifies the body of a request to assign a set of resources
        to a backup plan.
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DeleteBackupVault")
    def delete_backup_vault(
        self, context: RequestContext, backup_vault_name: string, **kwargs
    ) -> None:
        """Deletes the backup vault identified by its name. A vault can be deleted
        only if it is empty.

        :param backup_vault_name: The name of a logical container where backups are stored.
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("DeleteBackupVaultAccessPolicy")
    def delete_backup_vault_access_policy(
        self, context: RequestContext, backup_vault_name: BackupVaultName, **kwargs
    ) -> None:
        """Deletes the policy document that manages permissions on a backup vault.

        :param backup_vault_name: The name of a logical container where backups are stored.
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DeleteBackupVaultLockConfiguration")
    def delete_backup_vault_lock_configuration(
        self, context: RequestContext, backup_vault_name: BackupVaultName, **kwargs
    ) -> None:
        """Deletes Backup Vault Lock from a backup vault specified by a backup
        vault name.

        If the Vault Lock configuration is immutable, then you cannot delete
        Vault Lock using API operations, and you will receive an
        ``InvalidRequestException`` if you attempt to do so. For more
        information, see `Vault
        Lock <https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html>`__
        in the *Backup Developer Guide*.

        :param backup_vault_name: The name of the backup vault from which to delete Backup Vault Lock.
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DeleteBackupVaultNotifications")
    def delete_backup_vault_notifications(
        self, context: RequestContext, backup_vault_name: BackupVaultName, **kwargs
    ) -> None:
        """Deletes event notifications for the specified backup vault.

        :param backup_vault_name: The name of a logical container where backups are stored.
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DeleteFramework")
    def delete_framework(
        self, context: RequestContext, framework_name: FrameworkName, **kwargs
    ) -> None:
        """Deletes the framework specified by a framework name.

        :param framework_name: The unique name of a framework.
        :raises MissingParameterValueException:
        :raises InvalidParameterValueException:
        :raises ServiceUnavailableException:
        :raises ConflictException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("DeleteRecoveryPoint")
    def delete_recovery_point(
        self,
        context: RequestContext,
        backup_vault_name: BackupVaultName,
        recovery_point_arn: ARN,
        **kwargs,
    ) -> None:
        """Deletes the recovery point specified by a recovery point ID.

        If the recovery point ID belongs to a continuous backup, calling this
        endpoint deletes the existing continuous backup and stops future
        continuous backup.

        When an IAM role's permissions are insufficient to call this API, the
        service sends back an HTTP 200 response with an empty HTTP body, but the
        recovery point is not deleted. Instead, it enters an ``EXPIRED`` state.

        ``EXPIRED`` recovery points can be deleted with this API once the IAM
        role has the ``iam:CreateServiceLinkedRole`` action. To learn more about
        adding this role, see `Troubleshooting manual
        deletions <https://docs.aws.amazon.com/aws-backup/latest/devguide/deleting-backups.html#deleting-backups-troubleshooting>`__.

        If the user or role is deleted or the permission within the role is
        removed, the deletion will not be successful and will enter an
        ``EXPIRED`` state.

        :param backup_vault_name: The name of a logical container where backups are stored.
        :param recovery_point_arn: An Amazon Resource Name (ARN) that uniquely identifies a recovery point;
        for example,
        ``arn:aws:backup:us-east-1:123456789012:recovery-point:1EB3B5E7-9EB0-435A-A80B-108B488B0D45``.
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises InvalidResourceStateException:
        :raises ServiceUnavailableException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("DeleteReportPlan")
    def delete_report_plan(
        self, context: RequestContext, report_plan_name: ReportPlanName, **kwargs
    ) -> None:
        """Deletes the report plan specified by a report plan name.

        :param report_plan_name: The unique name of a report plan.
        :raises MissingParameterValueException:
        :raises InvalidParameterValueException:
        :raises ConflictException:
        :raises ServiceUnavailableException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("DeleteRestoreTestingPlan")
    def delete_restore_testing_plan(
        self, context: RequestContext, restore_testing_plan_name: String, **kwargs
    ) -> None:
        """This request deletes the specified restore testing plan.

        Deletion can only successfully occur if all associated restore testing
        selections are deleted first.

        :param restore_testing_plan_name: Required unique name of the restore testing plan you wish to delete.
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DeleteRestoreTestingSelection")
    def delete_restore_testing_selection(
        self,
        context: RequestContext,
        restore_testing_plan_name: String,
        restore_testing_selection_name: String,
        **kwargs,
    ) -> None:
        """Input the Restore Testing Plan name and Restore Testing Selection name.

        All testing selections associated with a restore testing plan must be
        deleted before the restore testing plan can be deleted.

        :param restore_testing_plan_name: Required unique name of the restore testing plan that contains the
        restore testing selection you wish to delete.
        :param restore_testing_selection_name: Required unique name of the restore testing selection you wish to
        delete.
        :raises ResourceNotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DeleteTieringConfiguration")
    def delete_tiering_configuration(
        self,
        context: RequestContext,
        tiering_configuration_name: TieringConfigurationName,
        **kwargs,
    ) -> DeleteTieringConfigurationOutput:
        """Deletes the tiering configuration specified by a tiering configuration
        name.

        :param tiering_configuration_name: The unique name of a tiering configuration.
        :returns: DeleteTieringConfigurationOutput
        :raises MissingParameterValueException:
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DescribeBackupJob")
    def describe_backup_job(
        self, context: RequestContext, backup_job_id: string, **kwargs
    ) -> DescribeBackupJobOutput:
        """Returns backup job details for the specified ``BackupJobId``.

        :param backup_job_id: Uniquely identifies a request to Backup to back up a resource.
        :returns: DescribeBackupJobOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        :raises DependencyFailureException:
        """
        raise NotImplementedError

    @handler("DescribeBackupVault")
    def describe_backup_vault(
        self,
        context: RequestContext,
        backup_vault_name: string,
        backup_vault_account_id: string | None = None,
        **kwargs,
    ) -> DescribeBackupVaultOutput:
        """Returns metadata about a backup vault specified by its name.

        :param backup_vault_name: The name of a logical container where backups are stored.
        :param backup_vault_account_id: The account ID of the specified backup vault.
        :returns: DescribeBackupVaultOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DescribeCopyJob")
    def describe_copy_job(
        self, context: RequestContext, copy_job_id: string, **kwargs
    ) -> DescribeCopyJobOutput:
        """Returns metadata associated with creating a copy of a resource.

        :param copy_job_id: Uniquely identifies a copy job.
        :returns: DescribeCopyJobOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DescribeFramework")
    def describe_framework(
        self, context: RequestContext, framework_name: FrameworkName, **kwargs
    ) -> DescribeFrameworkOutput:
        """Returns the framework details for the specified ``FrameworkName``.

        :param framework_name: The unique name of a framework.
        :returns: DescribeFrameworkOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DescribeGlobalSettings")
    def describe_global_settings(
        self, context: RequestContext, **kwargs
    ) -> DescribeGlobalSettingsOutput:
        """Describes whether the Amazon Web Services account is opted in to
        cross-account backup. Returns an error if the account is not a member of
        an Organizations organization. Example:
        ``describe-global-settings --region us-west-2``

        :returns: DescribeGlobalSettingsOutput
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DescribeProtectedResource")
    def describe_protected_resource(
        self, context: RequestContext, resource_arn: ARN, **kwargs
    ) -> DescribeProtectedResourceOutput:
        """Returns information about a saved resource, including the last time it
        was backed up, its Amazon Resource Name (ARN), and the Amazon Web
        Services service type of the saved resource.

        :param resource_arn: An Amazon Resource Name (ARN) that uniquely identifies a resource.
        :returns: DescribeProtectedResourceOutput
        :raises MissingParameterValueException:
        :raises InvalidParameterValueException:
        :raises ServiceUnavailableException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeRecoveryPoint")
    def describe_recovery_point(
        self,
        context: RequestContext,
        backup_vault_name: BackupVaultName,
        recovery_point_arn: ARN,
        backup_vault_account_id: AccountId | None = None,
        **kwargs,
    ) -> DescribeRecoveryPointOutput:
        """Returns metadata associated with a recovery point, including ID, status,
        encryption, and lifecycle.

        :param backup_vault_name: The name of a logical container where backups are stored.
        :param recovery_point_arn: An Amazon Resource Name (ARN) that uniquely identifies a recovery point;
        for example,
        ``arn:aws:backup:us-east-1:123456789012:recovery-point:1EB3B5E7-9EB0-435A-A80B-108B488B0D45``.
        :param backup_vault_account_id: The account ID of the specified backup vault.
        :returns: DescribeRecoveryPointOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DescribeRegionSettings")
    def describe_region_settings(
        self, context: RequestContext, **kwargs
    ) -> DescribeRegionSettingsOutput:
        """Returns the current service opt-in settings for the Region. If service
        opt-in is enabled for a service, Backup tries to protect that service's
        resources in this Region, when the resource is included in an on-demand
        backup or scheduled backup plan. Otherwise, Backup does not try to
        protect that service's resources in this Region.

        :returns: DescribeRegionSettingsOutput
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DescribeReportJob")
    def describe_report_job(
        self, context: RequestContext, report_job_id: ReportJobId, **kwargs
    ) -> DescribeReportJobOutput:
        """Returns the details associated with creating a report as specified by
        its ``ReportJobId``.

        :param report_job_id: The identifier of the report job.
        :returns: DescribeReportJobOutput
        :raises ServiceUnavailableException:
        :raises MissingParameterValueException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeReportPlan")
    def describe_report_plan(
        self, context: RequestContext, report_plan_name: ReportPlanName, **kwargs
    ) -> DescribeReportPlanOutput:
        """Returns a list of all report plans for an Amazon Web Services account
        and Amazon Web Services Region.

        :param report_plan_name: The unique name of a report plan.
        :returns: DescribeReportPlanOutput
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ResourceNotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DescribeRestoreJob")
    def describe_restore_job(
        self, context: RequestContext, restore_job_id: RestoreJobId, **kwargs
    ) -> DescribeRestoreJobOutput:
        """Returns metadata associated with a restore job that is specified by a
        job ID.

        :param restore_job_id: Uniquely identifies the job that restores a recovery point.
        :returns: DescribeRestoreJobOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        :raises DependencyFailureException:
        """
        raise NotImplementedError

    @handler("DescribeScanJob")
    def describe_scan_job(
        self, context: RequestContext, scan_job_id: String, **kwargs
    ) -> DescribeScanJobOutput:
        """Returns scan job details for the specified ScanJobID.

        :param scan_job_id: Uniquely identifies a request to Backup to scan a resource.
        :returns: DescribeScanJobOutput
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ResourceNotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DisassociateBackupVaultMpaApprovalTeam")
    def disassociate_backup_vault_mpa_approval_team(
        self,
        context: RequestContext,
        backup_vault_name: BackupVaultName,
        requester_comment: RequesterComment | None = None,
        **kwargs,
    ) -> None:
        """Removes the association between an MPA approval team and a backup vault,
        disabling the MPA approval workflow for restore operations.

        :param backup_vault_name: The name of the backup vault from which to disassociate the MPA approval
        team.
        :param requester_comment: An optional comment explaining the reason for disassociating the MPA
        approval team from the backup vault.
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DisassociateRecoveryPoint")
    def disassociate_recovery_point(
        self,
        context: RequestContext,
        backup_vault_name: BackupVaultName,
        recovery_point_arn: ARN,
        **kwargs,
    ) -> None:
        """Deletes the specified continuous backup recovery point from Backup and
        releases control of that continuous backup to the source service, such
        as Amazon RDS. The source service will continue to create and retain
        continuous backups using the lifecycle that you specified in your
        original backup plan.

        Does not support snapshot backup recovery points.

        :param backup_vault_name: The unique name of an Backup vault.
        :param recovery_point_arn: An Amazon Resource Name (ARN) that uniquely identifies an Backup
        recovery point.
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises InvalidResourceStateException:
        :raises ServiceUnavailableException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("DisassociateRecoveryPointFromParent")
    def disassociate_recovery_point_from_parent(
        self,
        context: RequestContext,
        backup_vault_name: BackupVaultName,
        recovery_point_arn: ARN,
        **kwargs,
    ) -> None:
        """This action to a specific child (nested) recovery point removes the
        relationship between the specified recovery point and its parent
        (composite) recovery point.

        :param backup_vault_name: The name of a logical container where the child (nested) recovery point
        is stored.
        :param recovery_point_arn: The Amazon Resource Name (ARN) that uniquely identifies the child
        (nested) recovery point; for example,
        ``arn:aws:backup:us-east-1:123456789012:recovery-point:1EB3B5E7-9EB0-435A-A80B-108B488B0D45.
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("ExportBackupPlanTemplate")
    def export_backup_plan_template(
        self, context: RequestContext, backup_plan_id: string, **kwargs
    ) -> ExportBackupPlanTemplateOutput:
        """Returns the backup plan that is specified by the plan ID as a backup
        template.

        :param backup_plan_id: Uniquely identifies a backup plan.
        :returns: ExportBackupPlanTemplateOutput
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetBackupPlan")
    def get_backup_plan(
        self,
        context: RequestContext,
        backup_plan_id: string,
        version_id: string | None = None,
        max_scheduled_runs_preview: MaxScheduledRunsPreview | None = None,
        **kwargs,
    ) -> GetBackupPlanOutput:
        """Returns ``BackupPlan`` details for the specified ``BackupPlanId``. The
        details are the body of a backup plan in JSON format, in addition to
        plan metadata.

        :param backup_plan_id: Uniquely identifies a backup plan.
        :param version_id: Unique, randomly generated, Unicode, UTF-8 encoded strings that are at
        most 1,024 bytes long.
        :param max_scheduled_runs_preview: Number of future scheduled backup runs to preview.
        :returns: GetBackupPlanOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("GetBackupPlanFromJSON")
    def get_backup_plan_from_json(
        self, context: RequestContext, backup_plan_template_json: string, **kwargs
    ) -> GetBackupPlanFromJSONOutput:
        """Returns a valid JSON document specifying a backup plan or an error.

        :param backup_plan_template_json: A customer-supplied backup plan document in JSON format.
        :returns: GetBackupPlanFromJSONOutput
        :raises LimitExceededException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("GetBackupPlanFromTemplate")
    def get_backup_plan_from_template(
        self, context: RequestContext, backup_plan_template_id: string, **kwargs
    ) -> GetBackupPlanFromTemplateOutput:
        """Returns the template specified by its ``templateId`` as a backup plan.

        :param backup_plan_template_id: Uniquely identifies a stored backup plan template.
        :returns: GetBackupPlanFromTemplateOutput
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetBackupSelection")
    def get_backup_selection(
        self, context: RequestContext, backup_plan_id: string, selection_id: string, **kwargs
    ) -> GetBackupSelectionOutput:
        """Returns selection metadata and a document in JSON format that specifies
        a list of resources that are associated with a backup plan.

        :param backup_plan_id: Uniquely identifies a backup plan.
        :param selection_id: Uniquely identifies the body of a request to assign a set of resources
        to a backup plan.
        :returns: GetBackupSelectionOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("GetBackupVaultAccessPolicy")
    def get_backup_vault_access_policy(
        self, context: RequestContext, backup_vault_name: BackupVaultName, **kwargs
    ) -> GetBackupVaultAccessPolicyOutput:
        """Returns the access policy document that is associated with the named
        backup vault.

        :param backup_vault_name: The name of a logical container where backups are stored.
        :returns: GetBackupVaultAccessPolicyOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("GetBackupVaultNotifications")
    def get_backup_vault_notifications(
        self, context: RequestContext, backup_vault_name: BackupVaultName, **kwargs
    ) -> GetBackupVaultNotificationsOutput:
        """Returns event notifications for the specified backup vault.

        :param backup_vault_name: The name of a logical container where backups are stored.
        :returns: GetBackupVaultNotificationsOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("GetLegalHold")
    def get_legal_hold(
        self, context: RequestContext, legal_hold_id: string, **kwargs
    ) -> GetLegalHoldOutput:
        """This action returns details for a specified legal hold. The details are
        the body of a legal hold in JSON format, in addition to metadata.

        :param legal_hold_id: The ID of the legal hold.
        :returns: GetLegalHoldOutput
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetRecoveryPointIndexDetails")
    def get_recovery_point_index_details(
        self,
        context: RequestContext,
        backup_vault_name: BackupVaultName,
        recovery_point_arn: ARN,
        **kwargs,
    ) -> GetRecoveryPointIndexDetailsOutput:
        """This operation returns the metadata and details specific to the backup
        index associated with the specified recovery point.

        :param backup_vault_name: The name of a logical container where backups are stored.
        :param recovery_point_arn: An ARN that uniquely identifies a recovery point; for example,
        ``arn:aws:backup:us-east-1:123456789012:recovery-point:1EB3B5E7-9EB0-435A-A80B-108B488B0D45``.
        :returns: GetRecoveryPointIndexDetailsOutput
        :raises MissingParameterValueException:
        :raises InvalidParameterValueException:
        :raises ResourceNotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("GetRecoveryPointRestoreMetadata")
    def get_recovery_point_restore_metadata(
        self,
        context: RequestContext,
        backup_vault_name: BackupVaultName,
        recovery_point_arn: ARN,
        backup_vault_account_id: AccountId | None = None,
        **kwargs,
    ) -> GetRecoveryPointRestoreMetadataOutput:
        """Returns a set of metadata key-value pairs that were used to create the
        backup.

        :param backup_vault_name: The name of a logical container where backups are stored.
        :param recovery_point_arn: An Amazon Resource Name (ARN) that uniquely identifies a recovery point;
        for example,
        ``arn:aws:backup:us-east-1:123456789012:recovery-point:1EB3B5E7-9EB0-435A-A80B-108B488B0D45``.
        :param backup_vault_account_id: The account ID of the specified backup vault.
        :returns: GetRecoveryPointRestoreMetadataOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("GetRestoreJobMetadata")
    def get_restore_job_metadata(
        self, context: RequestContext, restore_job_id: RestoreJobId, **kwargs
    ) -> GetRestoreJobMetadataOutput:
        """This request returns the metadata for the specified restore job.

        :param restore_job_id: This is a unique identifier of a restore job within Backup.
        :returns: GetRestoreJobMetadataOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("GetRestoreTestingInferredMetadata")
    def get_restore_testing_inferred_metadata(
        self,
        context: RequestContext,
        backup_vault_name: String,
        recovery_point_arn: String,
        backup_vault_account_id: String | None = None,
        **kwargs,
    ) -> GetRestoreTestingInferredMetadataOutput:
        """This request returns the minimal required set of metadata needed to
        start a restore job with secure default settings. ``BackupVaultName``
        and ``RecoveryPointArn`` are required parameters.
        ``BackupVaultAccountId`` is an optional parameter.

        :param backup_vault_name: The name of a logical container where backups are stored.
        :param recovery_point_arn: An Amazon Resource Name (ARN) that uniquely identifies a recovery point;
        for example,
        ``arn:aws:backup:us-east-1:123456789012:recovery-point:1EB3B5E7-9EB0-435A-A80B-108B488B0D45``.
        :param backup_vault_account_id: The account ID of the specified backup vault.
        :returns: GetRestoreTestingInferredMetadataOutput
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ResourceNotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("GetRestoreTestingPlan")
    def get_restore_testing_plan(
        self, context: RequestContext, restore_testing_plan_name: String, **kwargs
    ) -> GetRestoreTestingPlanOutput:
        """Returns ``RestoreTestingPlan`` details for the specified
        ``RestoreTestingPlanName``. The details are the body of a restore
        testing plan in JSON format, in addition to plan metadata.

        :param restore_testing_plan_name: Required unique name of the restore testing plan.
        :returns: GetRestoreTestingPlanOutput
        :raises ResourceNotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("GetRestoreTestingSelection")
    def get_restore_testing_selection(
        self,
        context: RequestContext,
        restore_testing_plan_name: String,
        restore_testing_selection_name: String,
        **kwargs,
    ) -> GetRestoreTestingSelectionOutput:
        """Returns RestoreTestingSelection, which displays resources and elements
        of the restore testing plan.

        :param restore_testing_plan_name: Required unique name of the restore testing plan.
        :param restore_testing_selection_name: Required unique name of the restore testing selection.
        :returns: GetRestoreTestingSelectionOutput
        :raises ResourceNotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("GetSupportedResourceTypes")
    def get_supported_resource_types(
        self, context: RequestContext, **kwargs
    ) -> GetSupportedResourceTypesOutput:
        """Returns the Amazon Web Services resource types supported by Backup.

        :returns: GetSupportedResourceTypesOutput
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("GetTieringConfiguration")
    def get_tiering_configuration(
        self,
        context: RequestContext,
        tiering_configuration_name: TieringConfigurationName,
        **kwargs,
    ) -> GetTieringConfigurationOutput:
        """Returns ``TieringConfiguration`` details for the specified
        ``TieringConfigurationName``. The details are the body of a tiering
        configuration in JSON format, in addition to configuration metadata.

        :param tiering_configuration_name: The unique name of a tiering configuration.
        :returns: GetTieringConfigurationOutput
        :raises MissingParameterValueException:
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListBackupJobSummaries")
    def list_backup_job_summaries(
        self,
        context: RequestContext,
        account_id: AccountId | None = None,
        state: BackupJobStatus | None = None,
        resource_type: ResourceType | None = None,
        message_category: MessageCategory | None = None,
        aggregation_period: AggregationPeriod | None = None,
        max_results: MaxResults | None = None,
        next_token: string | None = None,
        **kwargs,
    ) -> ListBackupJobSummariesOutput:
        """This is a request for a summary of backup jobs created or running within
        the most recent 30 days. You can include parameters AccountID, State,
        ResourceType, MessageCategory, AggregationPeriod, MaxResults, or
        NextToken to filter results.

        This request returns a summary that contains Region, Account, State,
        ResourceType, MessageCategory, StartTime, EndTime, and Count of included
        jobs.

        :param account_id: Returns the job count for the specified account.
        :param state: This parameter returns the job count for jobs with the specified state.
        :param resource_type: Returns the job count for the specified resource type.
        :param message_category: This parameter returns the job count for the specified message category.
        :param aggregation_period: The period for the returned results.
        :param max_results: The maximum number of items to be returned.
        :param next_token: The next item following a partial list of returned resources.
        :returns: ListBackupJobSummariesOutput
        :raises InvalidParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListBackupJobs")
    def list_backup_jobs(
        self,
        context: RequestContext,
        next_token: string | None = None,
        max_results: MaxResults | None = None,
        by_resource_arn: ARN | None = None,
        by_state: BackupJobState | None = None,
        by_backup_vault_name: BackupVaultName | None = None,
        by_created_before: timestamp | None = None,
        by_created_after: timestamp | None = None,
        by_resource_type: ResourceType | None = None,
        by_account_id: AccountId | None = None,
        by_complete_after: timestamp | None = None,
        by_complete_before: timestamp | None = None,
        by_parent_job_id: string | None = None,
        by_message_category: string | None = None,
        **kwargs,
    ) -> ListBackupJobsOutput:
        """Returns a list of existing backup jobs for an authenticated account for
        the last 30 days. For a longer period of time, consider using these
        `monitoring
        tools <https://docs.aws.amazon.com/aws-backup/latest/devguide/monitoring.html>`__.

        :param next_token: The next item following a partial list of returned items.
        :param max_results: The maximum number of items to be returned.
        :param by_resource_arn: Returns only backup jobs that match the specified resource Amazon
        Resource Name (ARN).
        :param by_state: Returns only backup jobs that are in the specified state.
        :param by_backup_vault_name: Returns only backup jobs that will be stored in the specified backup
        vault.
        :param by_created_before: Returns only backup jobs that were created before the specified date.
        :param by_created_after: Returns only backup jobs that were created after the specified date.
        :param by_resource_type: Returns only backup jobs for the specified resources:

        -  ``Aurora`` for Amazon Aurora

        -  ``CloudFormation`` for CloudFormation

        -  ``DocumentDB`` for Amazon DocumentDB (with MongoDB compatibility)

        -  ``DynamoDB`` for Amazon DynamoDB

        -  ``EBS`` for Amazon Elastic Block Store

        -  ``EC2`` for Amazon Elastic Compute Cloud

        -  ``EFS`` for Amazon Elastic File System

        -  ``FSx`` for Amazon FSx

        -  ``Neptune`` for Amazon Neptune

        -  ``RDS`` for Amazon Relational Database Service

        -  ``Redshift`` for Amazon Redshift

        -  ``S3`` for Amazon Simple Storage Service (Amazon S3)

        -  ``SAP HANA on Amazon EC2`` for SAP HANA databases on Amazon Elastic
           Compute Cloud instances

        -  ``Storage Gateway`` for Storage Gateway

        -  ``Timestream`` for Amazon Timestream

        -  ``VirtualMachine`` for VMware virtual machines.
        :param by_account_id: The account ID to list the jobs from.
        :param by_complete_after: Returns only backup jobs completed after a date expressed in Unix format
        and Coordinated Universal Time (UTC).
        :param by_complete_before: Returns only backup jobs completed before a date expressed in Unix
        format and Coordinated Universal Time (UTC).
        :param by_parent_job_id: This is a filter to list child (nested) jobs based on parent job ID.
        :param by_message_category: This is an optional parameter that can be used to filter out jobs with a
        MessageCategory which matches the value you input.
        :returns: ListBackupJobsOutput
        :raises InvalidParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListBackupPlanTemplates")
    def list_backup_plan_templates(
        self,
        context: RequestContext,
        next_token: string | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListBackupPlanTemplatesOutput:
        """Lists the backup plan templates.

        :param next_token: The next item following a partial list of returned items.
        :param max_results: The maximum number of items to return.
        :returns: ListBackupPlanTemplatesOutput
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListBackupPlanVersions")
    def list_backup_plan_versions(
        self,
        context: RequestContext,
        backup_plan_id: string,
        next_token: string | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListBackupPlanVersionsOutput:
        """Returns version metadata of your backup plans, including Amazon Resource
        Names (ARNs), backup plan IDs, creation and deletion dates, plan names,
        and version IDs.

        :param backup_plan_id: Uniquely identifies a backup plan.
        :param next_token: The next item following a partial list of returned items.
        :param max_results: The maximum number of items to be returned.
        :returns: ListBackupPlanVersionsOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListBackupPlans")
    def list_backup_plans(
        self,
        context: RequestContext,
        next_token: string | None = None,
        max_results: MaxResults | None = None,
        include_deleted: Boolean | None = None,
        **kwargs,
    ) -> ListBackupPlansOutput:
        """Lists the active backup plans for the account.

        :param next_token: The next item following a partial list of returned items.
        :param max_results: The maximum number of items to be returned.
        :param include_deleted: A Boolean value with a default value of ``FALSE`` that returns deleted
        backup plans when set to ``TRUE``.
        :returns: ListBackupPlansOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListBackupSelections")
    def list_backup_selections(
        self,
        context: RequestContext,
        backup_plan_id: string,
        next_token: string | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListBackupSelectionsOutput:
        """Returns an array containing metadata of the resources associated with
        the target backup plan.

        :param backup_plan_id: Uniquely identifies a backup plan.
        :param next_token: The next item following a partial list of returned items.
        :param max_results: The maximum number of items to be returned.
        :returns: ListBackupSelectionsOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListBackupVaults")
    def list_backup_vaults(
        self,
        context: RequestContext,
        by_vault_type: VaultType | None = None,
        by_shared: boolean | None = None,
        next_token: string | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListBackupVaultsOutput:
        """Returns a list of recovery point storage containers along with
        information about them.

        :param by_vault_type: This parameter will sort the list of vaults by vault type.
        :param by_shared: This parameter will sort the list of vaults by shared vaults.
        :param next_token: The next item following a partial list of returned items.
        :param max_results: The maximum number of items to be returned.
        :returns: ListBackupVaultsOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListCopyJobSummaries")
    def list_copy_job_summaries(
        self,
        context: RequestContext,
        account_id: AccountId | None = None,
        state: CopyJobStatus | None = None,
        resource_type: ResourceType | None = None,
        message_category: MessageCategory | None = None,
        aggregation_period: AggregationPeriod | None = None,
        max_results: MaxResults | None = None,
        next_token: string | None = None,
        **kwargs,
    ) -> ListCopyJobSummariesOutput:
        """This request obtains a list of copy jobs created or running within the
        the most recent 30 days. You can include parameters AccountID, State,
        ResourceType, MessageCategory, AggregationPeriod, MaxResults, or
        NextToken to filter results.

        This request returns a summary that contains Region, Account, State,
        RestourceType, MessageCategory, StartTime, EndTime, and Count of
        included jobs.

        :param account_id: Returns the job count for the specified account.
        :param state: This parameter returns the job count for jobs with the specified state.
        :param resource_type: Returns the job count for the specified resource type.
        :param message_category: This parameter returns the job count for the specified message category.
        :param aggregation_period: The period for the returned results.
        :param max_results: This parameter sets the maximum number of items to be returned.
        :param next_token: The next item following a partial list of returned resources.
        :returns: ListCopyJobSummariesOutput
        :raises InvalidParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListCopyJobs")
    def list_copy_jobs(
        self,
        context: RequestContext,
        next_token: string | None = None,
        max_results: MaxResults | None = None,
        by_resource_arn: ARN | None = None,
        by_state: CopyJobState | None = None,
        by_created_before: timestamp | None = None,
        by_created_after: timestamp | None = None,
        by_resource_type: ResourceType | None = None,
        by_destination_vault_arn: string | None = None,
        by_account_id: AccountId | None = None,
        by_complete_before: timestamp | None = None,
        by_complete_after: timestamp | None = None,
        by_parent_job_id: string | None = None,
        by_message_category: string | None = None,
        by_source_recovery_point_arn: string | None = None,
        **kwargs,
    ) -> ListCopyJobsOutput:
        """Returns metadata about your copy jobs.

        :param next_token: The next item following a partial list of returned items.
        :param max_results: The maximum number of items to be returned.
        :param by_resource_arn: Returns only copy jobs that match the specified resource Amazon Resource
        Name (ARN).
        :param by_state: Returns only copy jobs that are in the specified state.
        :param by_created_before: Returns only copy jobs that were created before the specified date.
        :param by_created_after: Returns only copy jobs that were created after the specified date.
        :param by_resource_type: Returns only backup jobs for the specified resources:

        -  ``Aurora`` for Amazon Aurora

        -  ``CloudFormation`` for CloudFormation

        -  ``DocumentDB`` for Amazon DocumentDB (with MongoDB compatibility)

        -  ``DynamoDB`` for Amazon DynamoDB

        -  ``EBS`` for Amazon Elastic Block Store

        -  ``EC2`` for Amazon Elastic Compute Cloud

        -  ``EFS`` for Amazon Elastic File System

        -  ``FSx`` for Amazon FSx

        -  ``Neptune`` for Amazon Neptune

        -  ``RDS`` for Amazon Relational Database Service

        -  ``Redshift`` for Amazon Redshift

        -  ``S3`` for Amazon Simple Storage Service (Amazon S3)

        -  ``SAP HANA on Amazon EC2`` for SAP HANA databases on Amazon Elastic
           Compute Cloud instances

        -  ``Storage Gateway`` for Storage Gateway

        -  ``Timestream`` for Amazon Timestream

        -  ``VirtualMachine`` for VMware virtual machines.
        :param by_destination_vault_arn: An Amazon Resource Name (ARN) that uniquely identifies a source backup
        vault to copy from; for example,
        ``arn:aws:backup:us-east-1:123456789012:backup-vault:aBackupVault``.
        :param by_account_id: The account ID to list the jobs from.
        :param by_complete_before: Returns only copy jobs completed before a date expressed in Unix format
        and Coordinated Universal Time (UTC).
        :param by_complete_after: Returns only copy jobs completed after a date expressed in Unix format
        and Coordinated Universal Time (UTC).
        :param by_parent_job_id: This is a filter to list child (nested) jobs based on parent job ID.
        :param by_message_category: This is an optional parameter that can be used to filter out jobs with a
        MessageCategory which matches the value you input.
        :param by_source_recovery_point_arn: Filters copy jobs by the specified source recovery point ARN.
        :returns: ListCopyJobsOutput
        :raises InvalidParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListFrameworks")
    def list_frameworks(
        self,
        context: RequestContext,
        max_results: MaxFrameworkInputs | None = None,
        next_token: string | None = None,
        **kwargs,
    ) -> ListFrameworksOutput:
        """Returns a list of all frameworks for an Amazon Web Services account and
        Amazon Web Services Region.

        :param max_results: The number of desired results from 1 to 1000.
        :param next_token: An identifier that was returned from the previous call to this
        operation, which can be used to return the next set of items in the
        list.
        :returns: ListFrameworksOutput
        :raises InvalidParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListIndexedRecoveryPoints")
    def list_indexed_recovery_points(
        self,
        context: RequestContext,
        next_token: string | None = None,
        max_results: MaxResults | None = None,
        source_resource_arn: ARN | None = None,
        created_before: timestamp | None = None,
        created_after: timestamp | None = None,
        resource_type: ResourceType | None = None,
        index_status: IndexStatus | None = None,
        **kwargs,
    ) -> ListIndexedRecoveryPointsOutput:
        """This operation returns a list of recovery points that have an associated
        index, belonging to the specified account.

        Optional parameters you can include are: MaxResults; NextToken;
        SourceResourceArns; CreatedBefore; CreatedAfter; and ResourceType.

        :param next_token: The next item following a partial list of returned recovery points.
        :param max_results: The maximum number of resource list items to be returned.
        :param source_resource_arn: A string of the Amazon Resource Name (ARN) that uniquely identifies the
        source resource.
        :param created_before: Returns only indexed recovery points that were created before the
        specified date.
        :param created_after: Returns only indexed recovery points that were created after the
        specified date.
        :param resource_type: Returns a list of indexed recovery points for the specified resource
        type(s).
        :param index_status: Include this parameter to filter the returned list by the indicated
        statuses.
        :returns: ListIndexedRecoveryPointsOutput
        :raises InvalidParameterValueException:
        :raises ResourceNotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListLegalHolds")
    def list_legal_holds(
        self,
        context: RequestContext,
        next_token: string | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListLegalHoldsOutput:
        """This action returns metadata about active and previous legal holds.

        :param next_token: The next item following a partial list of returned resources.
        :param max_results: The maximum number of resource list items to be returned.
        :returns: ListLegalHoldsOutput
        :raises InvalidParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListProtectedResources")
    def list_protected_resources(
        self,
        context: RequestContext,
        next_token: string | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListProtectedResourcesOutput:
        """Returns an array of resources successfully backed up by Backup,
        including the time the resource was saved, an Amazon Resource Name (ARN)
        of the resource, and a resource type.

        :param next_token: The next item following a partial list of returned items.
        :param max_results: The maximum number of items to be returned.
        :returns: ListProtectedResourcesOutput
        :raises InvalidParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListProtectedResourcesByBackupVault")
    def list_protected_resources_by_backup_vault(
        self,
        context: RequestContext,
        backup_vault_name: BackupVaultName,
        backup_vault_account_id: AccountId | None = None,
        next_token: string | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListProtectedResourcesByBackupVaultOutput:
        """This request lists the protected resources corresponding to each backup
        vault.

        :param backup_vault_name: The list of protected resources by backup vault within the vault(s) you
        specify by name.
        :param backup_vault_account_id: The list of protected resources by backup vault within the vault(s) you
        specify by account ID.
        :param next_token: The next item following a partial list of returned items.
        :param max_results: The maximum number of items to be returned.
        :returns: ListProtectedResourcesByBackupVaultOutput
        :raises InvalidParameterValueException:
        :raises ResourceNotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListRecoveryPointsByBackupVault")
    def list_recovery_points_by_backup_vault(
        self,
        context: RequestContext,
        backup_vault_name: BackupVaultName,
        backup_vault_account_id: AccountId | None = None,
        next_token: string | None = None,
        max_results: MaxResults | None = None,
        by_resource_arn: ARN | None = None,
        by_resource_type: ResourceType | None = None,
        by_backup_plan_id: string | None = None,
        by_created_before: timestamp | None = None,
        by_created_after: timestamp | None = None,
        by_parent_recovery_point_arn: ARN | None = None,
        **kwargs,
    ) -> ListRecoveryPointsByBackupVaultOutput:
        """Returns detailed information about the recovery points stored in a
        backup vault.

        :param backup_vault_name: The name of a logical container where backups are stored.
        :param backup_vault_account_id: This parameter will sort the list of recovery points by account ID.
        :param next_token: The next item following a partial list of returned items.
        :param max_results: The maximum number of items to be returned.
        :param by_resource_arn: Returns only recovery points that match the specified resource Amazon
        Resource Name (ARN).
        :param by_resource_type: Returns only recovery points that match the specified resource type(s):

        -  ``Aurora`` for Amazon Aurora

        -  ``CloudFormation`` for CloudFormation

        -  ``DocumentDB`` for Amazon DocumentDB (with MongoDB compatibility)

        -  ``DynamoDB`` for Amazon DynamoDB

        -  ``EBS`` for Amazon Elastic Block Store

        -  ``EC2`` for Amazon Elastic Compute Cloud

        -  ``EFS`` for Amazon Elastic File System

        -  ``FSx`` for Amazon FSx

        -  ``Neptune`` for Amazon Neptune

        -  ``RDS`` for Amazon Relational Database Service

        -  ``Redshift`` for Amazon Redshift

        -  ``S3`` for Amazon Simple Storage Service (Amazon S3)

        -  ``SAP HANA on Amazon EC2`` for SAP HANA databases on Amazon Elastic
           Compute Cloud instances

        -  ``Storage Gateway`` for Storage Gateway

        -  ``Timestream`` for Amazon Timestream

        -  ``VirtualMachine`` for VMware virtual machines.
        :param by_backup_plan_id: Returns only recovery points that match the specified backup plan ID.
        :param by_created_before: Returns only recovery points that were created before the specified
        timestamp.
        :param by_created_after: Returns only recovery points that were created after the specified
        timestamp.
        :param by_parent_recovery_point_arn: This returns only recovery points that match the specified parent
        (composite) recovery point Amazon Resource Name (ARN).
        :returns: ListRecoveryPointsByBackupVaultOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListRecoveryPointsByLegalHold")
    def list_recovery_points_by_legal_hold(
        self,
        context: RequestContext,
        legal_hold_id: string,
        next_token: string | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListRecoveryPointsByLegalHoldOutput:
        """This action returns recovery point ARNs (Amazon Resource Names) of the
        specified legal hold.

        :param legal_hold_id: The ID of the legal hold.
        :param next_token: The next item following a partial list of returned resources.
        :param max_results: The maximum number of resource list items to be returned.
        :returns: ListRecoveryPointsByLegalHoldOutput
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListRecoveryPointsByResource")
    def list_recovery_points_by_resource(
        self,
        context: RequestContext,
        resource_arn: ARN,
        next_token: string | None = None,
        max_results: MaxResults | None = None,
        managed_by_aws_backup_only: boolean | None = None,
        **kwargs,
    ) -> ListRecoveryPointsByResourceOutput:
        """The information about the recovery points of the type specified by a
        resource Amazon Resource Name (ARN).

        For Amazon EFS and Amazon EC2, this action only lists recovery points
        created by Backup.

        :param resource_arn: An ARN that uniquely identifies a resource.
        :param next_token: The next item following a partial list of returned items.
        :param max_results: The maximum number of items to be returned.
        :param managed_by_aws_backup_only: This attribute filters recovery points based on ownership.
        :returns: ListRecoveryPointsByResourceOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListReportJobs")
    def list_report_jobs(
        self,
        context: RequestContext,
        by_report_plan_name: ReportPlanName | None = None,
        by_creation_before: timestamp | None = None,
        by_creation_after: timestamp | None = None,
        by_status: string | None = None,
        max_results: MaxResults | None = None,
        next_token: string | None = None,
        **kwargs,
    ) -> ListReportJobsOutput:
        """Returns details about your report jobs.

        :param by_report_plan_name: Returns only report jobs with the specified report plan name.
        :param by_creation_before: Returns only report jobs that were created before the date and time
        specified in Unix format and Coordinated Universal Time (UTC).
        :param by_creation_after: Returns only report jobs that were created after the date and time
        specified in Unix format and Coordinated Universal Time (UTC).
        :param by_status: Returns only report jobs that are in the specified status.
        :param max_results: The number of desired results from 1 to 1000.
        :param next_token: An identifier that was returned from the previous call to this
        operation, which can be used to return the next set of items in the
        list.
        :returns: ListReportJobsOutput
        :raises InvalidParameterValueException:
        :raises ServiceUnavailableException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListReportPlans")
    def list_report_plans(
        self,
        context: RequestContext,
        max_results: MaxResults | None = None,
        next_token: string | None = None,
        **kwargs,
    ) -> ListReportPlansOutput:
        """Returns a list of your report plans. For detailed information about a
        single report plan, use ``DescribeReportPlan``.

        :param max_results: The number of desired results from 1 to 1000.
        :param next_token: An identifier that was returned from the previous call to this
        operation, which can be used to return the next set of items in the
        list.
        :returns: ListReportPlansOutput
        :raises InvalidParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListRestoreAccessBackupVaults")
    def list_restore_access_backup_vaults(
        self,
        context: RequestContext,
        backup_vault_name: BackupVaultName,
        next_token: string | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListRestoreAccessBackupVaultsOutput:
        """Returns a list of restore access backup vaults associated with a
        specified backup vault.

        :param backup_vault_name: The name of the backup vault for which to list associated restore access
        backup vaults.
        :param next_token: The pagination token from a previous request to retrieve the next set of
        results.
        :param max_results: The maximum number of items to return in the response.
        :returns: ListRestoreAccessBackupVaultsOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListRestoreJobSummaries")
    def list_restore_job_summaries(
        self,
        context: RequestContext,
        account_id: AccountId | None = None,
        state: RestoreJobState | None = None,
        resource_type: ResourceType | None = None,
        aggregation_period: AggregationPeriod | None = None,
        max_results: MaxResults | None = None,
        next_token: string | None = None,
        **kwargs,
    ) -> ListRestoreJobSummariesOutput:
        """This request obtains a summary of restore jobs created or running within
        the the most recent 30 days. You can include parameters AccountID,
        State, ResourceType, AggregationPeriod, MaxResults, or NextToken to
        filter results.

        This request returns a summary that contains Region, Account, State,
        RestourceType, MessageCategory, StartTime, EndTime, and Count of
        included jobs.

        :param account_id: Returns the job count for the specified account.
        :param state: This parameter returns the job count for jobs with the specified state.
        :param resource_type: Returns the job count for the specified resource type.
        :param aggregation_period: The period for the returned results.
        :param max_results: This parameter sets the maximum number of items to be returned.
        :param next_token: The next item following a partial list of returned resources.
        :returns: ListRestoreJobSummariesOutput
        :raises InvalidParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListRestoreJobs")
    def list_restore_jobs(
        self,
        context: RequestContext,
        next_token: string | None = None,
        max_results: MaxResults | None = None,
        by_account_id: AccountId | None = None,
        by_resource_type: ResourceType | None = None,
        by_created_before: timestamp | None = None,
        by_created_after: timestamp | None = None,
        by_status: RestoreJobStatus | None = None,
        by_complete_before: timestamp | None = None,
        by_complete_after: timestamp | None = None,
        by_restore_testing_plan_arn: ARN | None = None,
        by_parent_job_id: string | None = None,
        **kwargs,
    ) -> ListRestoreJobsOutput:
        """Returns a list of jobs that Backup initiated to restore a saved
        resource, including details about the recovery process.

        :param next_token: The next item following a partial list of returned items.
        :param max_results: The maximum number of items to be returned.
        :param by_account_id: The account ID to list the jobs from.
        :param by_resource_type: Include this parameter to return only restore jobs for the specified
        resources:

        -  ``Aurora`` for Amazon Aurora

        -  ``CloudFormation`` for CloudFormation

        -  ``DocumentDB`` for Amazon DocumentDB (with MongoDB compatibility)

        -  ``DynamoDB`` for Amazon DynamoDB

        -  ``EBS`` for Amazon Elastic Block Store

        -  ``EC2`` for Amazon Elastic Compute Cloud

        -  ``EFS`` for Amazon Elastic File System

        -  ``FSx`` for Amazon FSx

        -  ``Neptune`` for Amazon Neptune

        -  ``RDS`` for Amazon Relational Database Service

        -  ``Redshift`` for Amazon Redshift

        -  ``S3`` for Amazon Simple Storage Service (Amazon S3)

        -  ``SAP HANA on Amazon EC2`` for SAP HANA databases on Amazon Elastic
           Compute Cloud instances

        -  ``Storage Gateway`` for Storage Gateway

        -  ``Timestream`` for Amazon Timestream

        -  ``VirtualMachine`` for VMware virtual machines.
        :param by_created_before: Returns only restore jobs that were created before the specified date.
        :param by_created_after: Returns only restore jobs that were created after the specified date.
        :param by_status: Returns only restore jobs associated with the specified job status.
        :param by_complete_before: Returns only copy jobs completed before a date expressed in Unix format
        and Coordinated Universal Time (UTC).
        :param by_complete_after: Returns only copy jobs completed after a date expressed in Unix format
        and Coordinated Universal Time (UTC).
        :param by_restore_testing_plan_arn: This returns only restore testing jobs that match the specified resource
        Amazon Resource Name (ARN).
        :param by_parent_job_id: This is a filter to list child (nested) restore jobs based on parent
        restore job ID.
        :returns: ListRestoreJobsOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListRestoreJobsByProtectedResource")
    def list_restore_jobs_by_protected_resource(
        self,
        context: RequestContext,
        resource_arn: ARN,
        by_status: RestoreJobStatus | None = None,
        by_recovery_point_creation_date_after: timestamp | None = None,
        by_recovery_point_creation_date_before: timestamp | None = None,
        next_token: string | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListRestoreJobsByProtectedResourceOutput:
        """This returns restore jobs that contain the specified protected resource.

        You must include ``ResourceArn``. You can optionally include
        ``NextToken``, ``ByStatus``, ``MaxResults``,
        ``ByRecoveryPointCreationDateAfter`` , and
        ``ByRecoveryPointCreationDateBefore``.

        :param resource_arn: Returns only restore jobs that match the specified resource Amazon
        Resource Name (ARN).
        :param by_status: Returns only restore jobs associated with the specified job status.
        :param by_recovery_point_creation_date_after: Returns only restore jobs of recovery points that were created after the
        specified date.
        :param by_recovery_point_creation_date_before: Returns only restore jobs of recovery points that were created before
        the specified date.
        :param next_token: The next item following a partial list of returned items.
        :param max_results: The maximum number of items to be returned.
        :returns: ListRestoreJobsByProtectedResourceOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListRestoreTestingPlans")
    def list_restore_testing_plans(
        self,
        context: RequestContext,
        max_results: ListRestoreTestingPlansInputMaxResultsInteger | None = None,
        next_token: String | None = None,
        **kwargs,
    ) -> ListRestoreTestingPlansOutput:
        """Returns a list of restore testing plans.

        :param max_results: The maximum number of items to be returned.
        :param next_token: The next item following a partial list of returned items.
        :returns: ListRestoreTestingPlansOutput
        :raises InvalidParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListRestoreTestingSelections")
    def list_restore_testing_selections(
        self,
        context: RequestContext,
        restore_testing_plan_name: String,
        max_results: ListRestoreTestingSelectionsInputMaxResultsInteger | None = None,
        next_token: String | None = None,
        **kwargs,
    ) -> ListRestoreTestingSelectionsOutput:
        """Returns a list of restore testing selections. Can be filtered by
        ``MaxResults`` and ``RestoreTestingPlanName``.

        :param restore_testing_plan_name: Returns restore testing selections by the specified restore testing plan
        name.
        :param max_results: The maximum number of items to be returned.
        :param next_token: The next item following a partial list of returned items.
        :returns: ListRestoreTestingSelectionsOutput
        :raises InvalidParameterValueException:
        :raises ResourceNotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListScanJobSummaries")
    def list_scan_job_summaries(
        self,
        context: RequestContext,
        account_id: AccountId | None = None,
        resource_type: ResourceType | None = None,
        malware_scanner: MalwareScanner | None = None,
        scan_result_status: ScanResultStatus | None = None,
        state: ScanJobStatus | None = None,
        aggregation_period: AggregationPeriod | None = None,
        max_results: MaxResults | None = None,
        next_token: string | None = None,
        **kwargs,
    ) -> ListScanJobSummariesOutput:
        """This is a request for a summary of scan jobs created or running within
        the most recent 30 days.

        :param account_id: Returns the job count for the specified account.
        :param resource_type: Returns the job count for the specified resource type.
        :param malware_scanner: Returns only the scan jobs for the specified malware scanner.
        :param scan_result_status: Returns only the scan jobs for the specified scan results.
        :param state: Returns only the scan jobs for the specified scanning job state.
        :param aggregation_period: The period for the returned results.
        :param max_results: The maximum number of items to be returned.
        :param next_token: The next item following a partial list of returned items.
        :returns: ListScanJobSummariesOutput
        :raises InvalidParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListScanJobs")
    def list_scan_jobs(
        self,
        context: RequestContext,
        by_account_id: String | None = None,
        by_backup_vault_name: String | None = None,
        by_complete_after: Timestamp | None = None,
        by_complete_before: Timestamp | None = None,
        by_malware_scanner: MalwareScanner | None = None,
        by_recovery_point_arn: String | None = None,
        by_resource_arn: String | None = None,
        by_resource_type: ScanResourceType | None = None,
        by_scan_result_status: ScanResultStatus | None = None,
        by_state: ScanState | None = None,
        max_results: ListScanJobsInputMaxResultsInteger | None = None,
        next_token: String | None = None,
        **kwargs,
    ) -> ListScanJobsOutput:
        """Returns a list of existing scan jobs for an authenticated account for
        the last 30 days.

        :param by_account_id: The account ID to list the jobs from.
        :param by_backup_vault_name: Returns only scan jobs that will be stored in the specified backup
        vault.
        :param by_complete_after: Returns only scan jobs completed after a date expressed in Unix format
        and Coordinated Universal Time (UTC).
        :param by_complete_before: Returns only backup jobs completed before a date expressed in Unix
        format and Coordinated Universal Time (UTC).
        :param by_malware_scanner: Returns only the scan jobs for the specified malware scanner.
        :param by_recovery_point_arn: Returns only the scan jobs that are ran against the specified recovery
        point.
        :param by_resource_arn: Returns only scan jobs that match the specified resource Amazon Resource
        Name (ARN).
        :param by_resource_type: Returns restore testing selections by the specified restore testing plan
        name.
        :param by_scan_result_status: Returns only the scan jobs for the specified scan results:

        -  ``THREATS_FOUND``

        -  ``NO_THREATS_FOUND``.
        :param by_state: Returns only the scan jobs for the specified scanning job state.
        :param max_results: The maximum number of items to be returned.
        :param next_token: The next item following a partial list of returned items.
        :returns: ListScanJobsOutput
        :raises InvalidParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListTags")
    def list_tags(
        self,
        context: RequestContext,
        resource_arn: ARN,
        next_token: string | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListTagsOutput:
        """Returns the tags assigned to the resource, such as a target recovery
        point, backup plan, or backup vault.

        This operation returns results depending on the resource type used in
        the value for ``resourceArn``. For example, recovery points of Amazon
        DynamoDB with Advanced Settings have an ARN (Amazon Resource Name) that
        begins with ``arn:aws:backup``. Recovery points (backups) of DynamoDB
        without Advanced Settings enabled have an ARN that begins with
        ``arn:aws:dynamodb``.

        When this operation is called and when you include values of
        ``resourceArn`` that have an ARN other than ``arn:aws:backup``, it may
        return one of the exceptions listed below. To prevent this exception,
        include only values representing resource types that are fully managed
        by Backup. These have an ARN that begins ``arn:aws:backup`` and they are
        noted in the `Feature availability by
        resource <https://docs.aws.amazon.com/aws-backup/latest/devguide/backup-feature-availability.html#features-by-resource>`__
        table.

        :param resource_arn: An Amazon Resource Name (ARN) that uniquely identifies a resource.
        :param next_token: The next item following a partial list of returned items.
        :param max_results: The maximum number of items to be returned.
        :returns: ListTagsOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("ListTieringConfigurations")
    def list_tiering_configurations(
        self,
        context: RequestContext,
        max_results: MaxResults | None = None,
        next_token: string | None = None,
        **kwargs,
    ) -> ListTieringConfigurationsOutput:
        """Returns a list of tiering configurations.

        :param max_results: The maximum number of items to be returned.
        :param next_token: The next item following a partial list of returned items.
        :returns: ListTieringConfigurationsOutput
        :raises InvalidParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("PutBackupVaultAccessPolicy")
    def put_backup_vault_access_policy(
        self,
        context: RequestContext,
        backup_vault_name: BackupVaultName,
        policy: IAMPolicy | None = None,
        **kwargs,
    ) -> None:
        """Sets a resource-based policy that is used to manage access permissions
        on the target backup vault. Requires a backup vault name and an access
        policy document in JSON format.

        :param backup_vault_name: The name of a logical container where backups are stored.
        :param policy: The backup vault access policy document in JSON format.
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("PutBackupVaultLockConfiguration")
    def put_backup_vault_lock_configuration(
        self,
        context: RequestContext,
        backup_vault_name: BackupVaultName,
        min_retention_days: Long | None = None,
        max_retention_days: Long | None = None,
        changeable_for_days: Long | None = None,
        **kwargs,
    ) -> None:
        """Applies Backup Vault Lock to a backup vault, preventing attempts to
        delete any recovery point stored in or created in a backup vault. Vault
        Lock also prevents attempts to update the lifecycle policy that controls
        the retention period of any recovery point currently stored in a backup
        vault. If specified, Vault Lock enforces a minimum and maximum retention
        period for future backup and copy jobs that target a backup vault.

        Backup Vault Lock has been assessed by Cohasset Associates for use in
        environments that are subject to SEC 17a-4, CFTC, and FINRA regulations.
        For more information about how Backup Vault Lock relates to these
        regulations, see the `Cohasset Associates Compliance
        Assessment. <https://docs.aws.amazon.com/aws-backup/latest/devguide/samples/cohassetreport.zip>`__

        For more information, see `Backup Vault
        Lock <https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html>`__.

        :param backup_vault_name: The Backup Vault Lock configuration that specifies the name of the
        backup vault it protects.
        :param min_retention_days: The Backup Vault Lock configuration that specifies the minimum retention
        period that the vault retains its recovery points.
        :param max_retention_days: The Backup Vault Lock configuration that specifies the maximum retention
        period that the vault retains its recovery points.
        :param changeable_for_days: The Backup Vault Lock configuration that specifies the number of days
        before the lock date.
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("PutBackupVaultNotifications")
    def put_backup_vault_notifications(
        self,
        context: RequestContext,
        backup_vault_name: BackupVaultName,
        sns_topic_arn: ARN,
        backup_vault_events: BackupVaultEvents,
        **kwargs,
    ) -> None:
        """Turns on notifications on a backup vault for the specified topic and
        events.

        :param backup_vault_name: The name of a logical container where backups are stored.
        :param sns_topic_arn: The Amazon Resource Name (ARN) that specifies the topic for a backup
        vault’s events; for example,
        ``arn:aws:sns:us-west-2:111122223333:MyVaultTopic``.
        :param backup_vault_events: An array of events that indicate the status of jobs to back up resources
        to the backup vault.
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("PutRestoreValidationResult")
    def put_restore_validation_result(
        self,
        context: RequestContext,
        restore_job_id: RestoreJobId,
        validation_status: RestoreValidationStatus,
        validation_status_message: string | None = None,
        **kwargs,
    ) -> None:
        """This request allows you to send your independent self-run restore test
        validation results. ``RestoreJobId`` and ``ValidationStatus`` are
        required. Optionally, you can input a ``ValidationStatusMessage``.

        :param restore_job_id: This is a unique identifier of a restore job within Backup.
        :param validation_status: The status of your restore validation.
        :param validation_status_message: This is an optional message string you can input to describe the
        validation status for the restore test validation.
        :raises InvalidParameterValueException:
        :raises InvalidRequestException:
        :raises MissingParameterValueException:
        :raises ResourceNotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("RevokeRestoreAccessBackupVault")
    def revoke_restore_access_backup_vault(
        self,
        context: RequestContext,
        backup_vault_name: BackupVaultName,
        restore_access_backup_vault_arn: ARN,
        requester_comment: RequesterComment | None = None,
        **kwargs,
    ) -> None:
        """Revokes access to a restore access backup vault, removing the ability to
        restore from its recovery points and permanently deleting the vault.

        :param backup_vault_name: The name of the source backup vault associated with the restore access
        backup vault to be revoked.
        :param restore_access_backup_vault_arn: The ARN of the restore access backup vault to revoke.
        :param requester_comment: A comment explaining the reason for revoking access to the restore
        access backup vault.
        :raises ResourceNotFoundException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        :raises InvalidParameterValueException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("StartBackupJob")
    def start_backup_job(
        self,
        context: RequestContext,
        backup_vault_name: BackupVaultName,
        resource_arn: ARN,
        iam_role_arn: IAMRoleArn,
        logically_air_gapped_backup_vault_arn: ARN | None = None,
        idempotency_token: string | None = None,
        start_window_minutes: WindowMinutes | None = None,
        complete_window_minutes: WindowMinutes | None = None,
        lifecycle: Lifecycle | None = None,
        recovery_point_tags: Tags | None = None,
        backup_options: BackupOptions | None = None,
        index: Index | None = None,
        **kwargs,
    ) -> StartBackupJobOutput:
        """Starts an on-demand backup job for the specified resource.

        :param backup_vault_name: The name of a logical container where backups are stored.
        :param resource_arn: An Amazon Resource Name (ARN) that uniquely identifies a resource.
        :param iam_role_arn: Specifies the IAM role ARN used to create the target recovery point; for
        example, ``arn:aws:iam::123456789012:role/S3Access``.
        :param logically_air_gapped_backup_vault_arn: The ARN of a logically air-gapped vault.
        :param idempotency_token: A customer-chosen string that you can use to distinguish between
        otherwise identical calls to ``StartBackupJob``.
        :param start_window_minutes: A value in minutes after a backup is scheduled before a job will be
        canceled if it doesn't start successfully.
        :param complete_window_minutes: A value in minutes during which a successfully started backup must
        complete, or else Backup will cancel the job.
        :param lifecycle: The lifecycle defines when a protected resource is transitioned to cold
        storage and when it expires.
        :param recovery_point_tags: The tags to assign to the resources.
        :param backup_options: The backup option for a selected resource.
        :param index: Include this parameter to enable index creation if your backup job has a
        resource type that supports backup indexes.
        :returns: StartBackupJobOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("StartCopyJob")
    def start_copy_job(
        self,
        context: RequestContext,
        recovery_point_arn: ARN,
        source_backup_vault_name: BackupVaultName,
        destination_backup_vault_arn: ARN,
        iam_role_arn: IAMRoleArn,
        idempotency_token: string | None = None,
        lifecycle: Lifecycle | None = None,
        **kwargs,
    ) -> StartCopyJobOutput:
        """Starts a job to create a one-time copy of the specified resource.

        Does not support continuous backups.

        See `Copy job
        retry <https://docs.aws.amazon.com/aws-backup/latest/devguide/recov-point-create-a-copy.html#backup-copy-retry>`__
        for information on how Backup retries copy job operations.

        :param recovery_point_arn: An ARN that uniquely identifies a recovery point to use for the copy
        job; for example,
        arn:aws:backup:us-east-1:123456789012:recovery-point:1EB3B5E7-9EB0-435A-A80B-108B488B0D45.
        :param source_backup_vault_name: The name of a logical source container where backups are stored.
        :param destination_backup_vault_arn: An Amazon Resource Name (ARN) that uniquely identifies a destination
        backup vault to copy to; for example,
        ``arn:aws:backup:us-east-1:123456789012:backup-vault:aBackupVault``.
        :param iam_role_arn: Specifies the IAM role ARN used to copy the target recovery point; for
        example, ``arn:aws:iam::123456789012:role/S3Access``.
        :param idempotency_token: A customer-chosen string that you can use to distinguish between
        otherwise identical calls to ``StartCopyJob``.
        :param lifecycle: Specifies the time period, in days, before a recovery point transitions
        to cold storage or is deleted.
        :returns: StartCopyJobOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        :raises LimitExceededException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("StartReportJob")
    def start_report_job(
        self,
        context: RequestContext,
        report_plan_name: ReportPlanName,
        idempotency_token: string | None = None,
        **kwargs,
    ) -> StartReportJobOutput:
        """Starts an on-demand report job for the specified report plan.

        :param report_plan_name: The unique name of a report plan.
        :param idempotency_token: A customer-chosen string that you can use to distinguish between
        otherwise identical calls to ``StartReportJobInput``.
        :returns: StartReportJobOutput
        :raises InvalidParameterValueException:
        :raises ServiceUnavailableException:
        :raises MissingParameterValueException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("StartRestoreJob")
    def start_restore_job(
        self,
        context: RequestContext,
        recovery_point_arn: ARN,
        metadata: Metadata,
        iam_role_arn: IAMRoleArn | None = None,
        idempotency_token: string | None = None,
        resource_type: ResourceType | None = None,
        copy_source_tags_to_restored_resource: boolean | None = None,
        **kwargs,
    ) -> StartRestoreJobOutput:
        """Recovers the saved resource identified by an Amazon Resource Name (ARN).

        :param recovery_point_arn: An ARN that uniquely identifies a recovery point; for example,
        ``arn:aws:backup:us-east-1:123456789012:recovery-point:1EB3B5E7-9EB0-435A-A80B-108B488B0D45``.
        :param metadata: A set of metadata key-value pairs.
        :param iam_role_arn: The Amazon Resource Name (ARN) of the IAM role that Backup uses to
        create the target resource; for example:
        ``arn:aws:iam::123456789012:role/S3Access``.
        :param idempotency_token: A customer-chosen string that you can use to distinguish between
        otherwise identical calls to ``StartRestoreJob``.
        :param resource_type: Starts a job to restore a recovery point for one of the following
        resources:

        -  ``Aurora`` - Amazon Aurora

        -  ``DocumentDB`` - Amazon DocumentDB

        -  ``CloudFormation`` - CloudFormation

        -  ``DynamoDB`` - Amazon DynamoDB

        -  ``EBS`` - Amazon Elastic Block Store

        -  ``EC2`` - Amazon Elastic Compute Cloud

        -  ``EFS`` - Amazon Elastic File System

        -  ``FSx`` - Amazon FSx

        -  ``Neptune`` - Amazon Neptune

        -  ``RDS`` - Amazon Relational Database Service

        -  ``Redshift`` - Amazon Redshift

        -  ``Storage Gateway`` - Storage Gateway

        -  ``S3`` - Amazon Simple Storage Service

        -  ``Timestream`` - Amazon Timestream

        -  ``VirtualMachine`` - Virtual machines.
        :param copy_source_tags_to_restored_resource: This is an optional parameter.
        :returns: StartRestoreJobOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("StartScanJob")
    def start_scan_job(
        self,
        context: RequestContext,
        backup_vault_name: String,
        iam_role_arn: String,
        malware_scanner: MalwareScanner,
        recovery_point_arn: String,
        scan_mode: ScanMode,
        scanner_role_arn: String,
        idempotency_token: String | None = None,
        scan_base_recovery_point_arn: String | None = None,
        **kwargs,
    ) -> StartScanJobOutput:
        """Starts scanning jobs for specific resources.

        :param backup_vault_name: The name of a logical container where backups are stored.
        :param iam_role_arn: Specifies the IAM role ARN used to create the target recovery point; for
        example, ``arn:aws:iam::123456789012:role/S3Access``.
        :param malware_scanner: Specifies the malware scanner used during the scan job.
        :param recovery_point_arn: An Amazon Resource Name (ARN) that uniquely identifies a recovery point.
        :param scan_mode: Specifies the scan type use for the scan job.
        :param scanner_role_arn: Specified the IAM scanner role ARN.
        :param idempotency_token: A customer-chosen string that you can use to distinguish between
        otherwise identical calls to ``StartScanJob``.
        :param scan_base_recovery_point_arn: An ARN that uniquely identifies the base recovery point to be used for
        incremental scanning.
        :returns: StartScanJobOutput
        :raises InvalidParameterValueException:
        :raises InvalidRequestException:
        :raises LimitExceededException:
        :raises MissingParameterValueException:
        :raises ResourceNotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("StopBackupJob")
    def stop_backup_job(self, context: RequestContext, backup_job_id: string, **kwargs) -> None:
        """Attempts to cancel a job to create a one-time backup of a resource.

        This action is not supported for the following services:

        -  Amazon Aurora

        -  Amazon DocumentDB (with MongoDB compatibility)

        -  Amazon FSx for Lustre

        -  Amazon FSx for NetApp ONTAP

        -  Amazon FSx for OpenZFS

        -  Amazon FSx for Windows File Server

        -  Amazon Neptune

        -  SAP HANA databases on Amazon EC2 instances

        -  Amazon RDS

        :param backup_job_id: Uniquely identifies a request to Backup to back up a resource.
        :raises MissingParameterValueException:
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises InvalidRequestException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("TagResource")
    def tag_resource(
        self, context: RequestContext, resource_arn: ARN, tags: Tags, **kwargs
    ) -> None:
        """Assigns a set of key-value pairs to a resource.

        :param resource_arn: The ARN that uniquely identifies the resource.
        :param tags: Key-value pairs that are used to help organize your resources.
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        :raises LimitExceededException:
        """
        raise NotImplementedError

    @handler("UntagResource")
    def untag_resource(
        self, context: RequestContext, resource_arn: ARN, tag_key_list: TagKeyList, **kwargs
    ) -> None:
        """Removes a set of key-value pairs from a recovery point, backup plan, or
        backup vault identified by an Amazon Resource Name (ARN)

        This API is not supported for recovery points for resource types
        including Aurora, Amazon DocumentDB. Amazon EBS, Amazon FSx, Neptune,
        and Amazon RDS.

        :param resource_arn: An ARN that uniquely identifies a resource.
        :param tag_key_list: The keys to identify which key-value tags to remove from a resource.
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("UpdateBackupPlan")
    def update_backup_plan(
        self,
        context: RequestContext,
        backup_plan_id: string,
        backup_plan: BackupPlanInput,
        **kwargs,
    ) -> UpdateBackupPlanOutput:
        """Updates the specified backup plan. The new version is uniquely
        identified by its ID.

        :param backup_plan_id: The ID of the backup plan.
        :param backup_plan: The body of a backup plan.
        :returns: UpdateBackupPlanOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("UpdateFramework")
    def update_framework(
        self,
        context: RequestContext,
        framework_name: FrameworkName,
        framework_description: FrameworkDescription | None = None,
        framework_controls: FrameworkControls | None = None,
        idempotency_token: string | None = None,
        **kwargs,
    ) -> UpdateFrameworkOutput:
        """Updates the specified framework.

        :param framework_name: The unique name of a framework.
        :param framework_description: An optional description of the framework with a maximum 1,024
        characters.
        :param framework_controls: The controls that make up the framework.
        :param idempotency_token: A customer-chosen string that you can use to distinguish between
        otherwise identical calls to ``UpdateFrameworkInput``.
        :returns: UpdateFrameworkOutput
        :raises AlreadyExistsException:
        :raises ResourceNotFoundException:
        :raises LimitExceededException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ConflictException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("UpdateGlobalSettings")
    def update_global_settings(
        self, context: RequestContext, global_settings: GlobalSettings | None = None, **kwargs
    ) -> None:
        """Updates whether the Amazon Web Services account is opted in to
        cross-account backup. Returns an error if the account is not an
        Organizations management account. Use the ``DescribeGlobalSettings`` API
        to determine the current settings.

        :param global_settings: Inputs can include:

        A value for ``isCrossAccountBackupEnabled`` and a Region.
        :raises ServiceUnavailableException:
        :raises MissingParameterValueException:
        :raises InvalidParameterValueException:
        :raises InvalidRequestException:
        """
        raise NotImplementedError

    @handler("UpdateRecoveryPointIndexSettings")
    def update_recovery_point_index_settings(
        self,
        context: RequestContext,
        backup_vault_name: BackupVaultName,
        recovery_point_arn: ARN,
        index: Index,
        iam_role_arn: IAMRoleArn | None = None,
        **kwargs,
    ) -> UpdateRecoveryPointIndexSettingsOutput:
        """This operation updates the settings of a recovery point index.

        Required: BackupVaultName, RecoveryPointArn, and IAMRoleArn

        :param backup_vault_name: The name of a logical container where backups are stored.
        :param recovery_point_arn: An ARN that uniquely identifies a recovery point; for example,
        ``arn:aws:backup:us-east-1:123456789012:recovery-point:1EB3B5E7-9EB0-435A-A80B-108B488B0D45``.
        :param index: Index can have 1 of 2 possible values, either ``ENABLED`` or
        ``DISABLED``.
        :param iam_role_arn: This specifies the IAM role ARN used for this operation.
        :returns: UpdateRecoveryPointIndexSettingsOutput
        :raises MissingParameterValueException:
        :raises InvalidParameterValueException:
        :raises InvalidRequestException:
        :raises ResourceNotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("UpdateRecoveryPointLifecycle")
    def update_recovery_point_lifecycle(
        self,
        context: RequestContext,
        backup_vault_name: BackupVaultName,
        recovery_point_arn: ARN,
        lifecycle: Lifecycle | None = None,
        **kwargs,
    ) -> UpdateRecoveryPointLifecycleOutput:
        """Sets the transition lifecycle of a recovery point.

        The lifecycle defines when a protected resource is transitioned to cold
        storage and when it expires. Backup transitions and expires backups
        automatically according to the lifecycle that you define.

        Resource types that can transition to cold storage are listed in the
        `Feature availability by
        resource <https://docs.aws.amazon.com/aws-backup/latest/devguide/backup-feature-availability.html#features-by-resource>`__
        table. Backup ignores this expression for other resource types.

        Backups transitioned to cold storage must be stored in cold storage for
        a minimum of 90 days. Therefore, the “retention” setting must be 90 days
        greater than the “transition to cold after days” setting. The
        “transition to cold after days” setting cannot be changed after a backup
        has been transitioned to cold.

        If your lifecycle currently uses the parameters ``DeleteAfterDays`` and
        ``MoveToColdStorageAfterDays``, include these parameters and their
        values when you call this operation. Not including them may result in
        your plan updating with null values.

        This operation does not support continuous backups.

        :param backup_vault_name: The name of a logical container where backups are stored.
        :param recovery_point_arn: An Amazon Resource Name (ARN) that uniquely identifies a recovery point;
        for example,
        ``arn:aws:backup:us-east-1:123456789012:recovery-point:1EB3B5E7-9EB0-435A-A80B-108B488B0D45``.
        :param lifecycle: The lifecycle defines when a protected resource is transitioned to cold
        storage and when it expires.
        :returns: UpdateRecoveryPointLifecycleOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises InvalidRequestException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("UpdateRegionSettings")
    def update_region_settings(
        self,
        context: RequestContext,
        resource_type_opt_in_preference: ResourceTypeOptInPreference | None = None,
        resource_type_management_preference: ResourceTypeManagementPreference | None = None,
        **kwargs,
    ) -> None:
        """Updates the current service opt-in settings for the Region.

        Use the ``DescribeRegionSettings`` API to determine the resource types
        that are supported.

        :param resource_type_opt_in_preference: Updates the list of services along with the opt-in preferences for the
        Region.
        :param resource_type_management_preference: Enables or disables full Backup management of backups for a resource
        type.
        :raises ServiceUnavailableException:
        :raises MissingParameterValueException:
        :raises InvalidParameterValueException:
        """
        raise NotImplementedError

    @handler("UpdateReportPlan")
    def update_report_plan(
        self,
        context: RequestContext,
        report_plan_name: ReportPlanName,
        report_plan_description: ReportPlanDescription | None = None,
        report_delivery_channel: ReportDeliveryChannel | None = None,
        report_setting: ReportSetting | None = None,
        idempotency_token: string | None = None,
        **kwargs,
    ) -> UpdateReportPlanOutput:
        """Updates the specified report plan.

        :param report_plan_name: The unique name of the report plan.
        :param report_plan_description: An optional description of the report plan with a maximum 1,024
        characters.
        :param report_delivery_channel: The information about where to deliver your reports, specifically your
        Amazon S3 bucket name, S3 key prefix, and the formats of your reports.
        :param report_setting: The report template for the report.
        :param idempotency_token: A customer-chosen string that you can use to distinguish between
        otherwise identical calls to ``UpdateReportPlanInput``.
        :returns: UpdateReportPlanOutput
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises ServiceUnavailableException:
        :raises MissingParameterValueException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("UpdateRestoreTestingPlan")
    def update_restore_testing_plan(
        self,
        context: RequestContext,
        restore_testing_plan: RestoreTestingPlanForUpdate,
        restore_testing_plan_name: String,
        **kwargs,
    ) -> UpdateRestoreTestingPlanOutput:
        """This request will send changes to your specified restore testing plan.
        ``RestoreTestingPlanName`` cannot be updated after it is created.

        ``RecoveryPointSelection`` can contain:

        -  ``Algorithm``

        -  ``ExcludeVaults``

        -  ``IncludeVaults``

        -  ``RecoveryPointTypes``

        -  ``SelectionWindowDays``

        :param restore_testing_plan: Specifies the body of a restore testing plan.
        :param restore_testing_plan_name: The name of the restore testing plan name.
        :returns: UpdateRestoreTestingPlanOutput
        :raises ConflictException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ResourceNotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("UpdateRestoreTestingSelection")
    def update_restore_testing_selection(
        self,
        context: RequestContext,
        restore_testing_plan_name: String,
        restore_testing_selection: RestoreTestingSelectionForUpdate,
        restore_testing_selection_name: String,
        **kwargs,
    ) -> UpdateRestoreTestingSelectionOutput:
        """Updates the specified restore testing selection.

        Most elements except the ``RestoreTestingSelectionName`` can be updated
        with this request.

        You can use either protected resource ARNs or conditions, but not both.

        :param restore_testing_plan_name: The restore testing plan name is required to update the indicated
        testing plan.
        :param restore_testing_selection: To update your restore testing selection, you can use either protected
        resource ARNs or conditions, but not both.
        :param restore_testing_selection_name: The required restore testing selection name of the restore testing
        selection you wish to update.
        :returns: UpdateRestoreTestingSelectionOutput
        :raises ConflictException:
        :raises InvalidParameterValueException:
        :raises MissingParameterValueException:
        :raises ResourceNotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("UpdateTieringConfiguration")
    def update_tiering_configuration(
        self,
        context: RequestContext,
        tiering_configuration_name: TieringConfigurationName,
        tiering_configuration: TieringConfigurationInputForUpdate,
        **kwargs,
    ) -> UpdateTieringConfigurationOutput:
        """This request will send changes to your specified tiering configuration.
        ``TieringConfigurationName`` cannot be updated after it is created.

        ``ResourceSelection`` can contain:

        -  ``Resources``

        -  ``TieringDownSettingsInDays``

        -  ``ResourceType``

        :param tiering_configuration_name: The name of a tiering configuration to update.
        :param tiering_configuration: Specifies the body of a tiering configuration.
        :returns: UpdateTieringConfigurationOutput
        :raises AlreadyExistsException:
        :raises ConflictException:
        :raises ResourceNotFoundException:
        :raises InvalidParameterValueException:
        :raises LimitExceededException:
        :raises MissingParameterValueException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError
