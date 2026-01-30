from datetime import datetime
from enum import StrEnum
from typing import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

ApplicationArn = str
ApplicationId = str
ApplicationName = str
Arn = str
AttemptNumber = int
AutoStopConfigIdleTimeoutMinutesInteger = int
Boolean = bool
ClientToken = str
ConfigurationPropertyKey = str
ConfigurationPropertyValue = str
CpuSize = str
DiskSize = str
DiskType = str
Double = float
EncryptionContextKey = str
EncryptionContextValue = str
EncryptionKeyArn = str
EngineType = str
EntryPointArgument = str
EntryPointPath = str
HiveCliParameters = str
IAMRoleArn = str
IdentityCenterApplicationArn = str
IdentityCenterInstanceArn = str
ImageDigest = str
ImageUri = str
InitScriptPath = str
Integer = int
JobArn = str
JobRunId = str
JobRunType = str
ListApplicationsRequestMaxResultsInteger = int
ListJobRunAttemptsRequestMaxResultsInteger = int
ListJobRunsRequestMaxResultsInteger = int
LogGroupName = str
LogStreamNamePrefix = str
LogTypeString = str
MemorySize = str
NextToken = str
PolicyDocument = str
PrometheusUrlString = str
Query = str
ReleaseLabel = str
RequestIdentityUserArn = str
ResourceArn = str
RetryPolicyMaxFailedAttemptsPerHourInteger = int
SecurityGroupString = str
ShutdownGracePeriodInSeconds = int
SparkSubmitParameters = str
String1024 = str
String256 = str
SubnetString = str
TagKey = str
TagValue = str
UriString = str
Url = str
WorkerTypeString = str


class ApplicationState(StrEnum):
    CREATING = "CREATING"
    CREATED = "CREATED"
    STARTING = "STARTING"
    STARTED = "STARTED"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    TERMINATED = "TERMINATED"


class Architecture(StrEnum):
    ARM64 = "ARM64"
    X86_64 = "X86_64"


class JobRunMode(StrEnum):
    BATCH = "BATCH"
    STREAMING = "STREAMING"


class JobRunState(StrEnum):
    SUBMITTED = "SUBMITTED"
    PENDING = "PENDING"
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLING = "CANCELLING"
    CANCELLED = "CANCELLED"
    QUEUED = "QUEUED"


class ConflictException(ServiceException):
    """The request could not be processed because of conflict in the current
    state of the resource.
    """

    code: str = "ConflictException"
    sender_fault: bool = True
    status_code: int = 409


class InternalServerException(ServiceException):
    """Request processing failed because of an error or failure with the
    service.
    """

    code: str = "InternalServerException"
    sender_fault: bool = False
    status_code: int = 500


class ResourceNotFoundException(ServiceException):
    """The specified resource was not found."""

    code: str = "ResourceNotFoundException"
    sender_fault: bool = True
    status_code: int = 404


class ServiceQuotaExceededException(ServiceException):
    """The maximum number of resources per account has been reached."""

    code: str = "ServiceQuotaExceededException"
    sender_fault: bool = True
    status_code: int = 402


class ValidationException(ServiceException):
    """The input fails to satisfy the constraints specified by an Amazon Web
    Services service.
    """

    code: str = "ValidationException"
    sender_fault: bool = True
    status_code: int = 400


class JobLevelCostAllocationConfiguration(TypedDict, total=False):
    """The configuration object that enables job level cost allocation."""

    enabled: Boolean | None


class IdentityCenterConfiguration(TypedDict, total=False):
    """The IAM Identity Center Configuration accepts the Identity Center
    instance parameter required to enable trusted identity propagation. This
    configuration allows identity propagation between integrated services
    and the Identity Center instance.
    """

    identityCenterInstanceArn: IdentityCenterInstanceArn | None
    identityCenterApplicationArn: IdentityCenterApplicationArn | None
    userBackgroundSessionsEnabled: Boolean | None


class SchedulerConfiguration(TypedDict, total=False):
    """The scheduler configuration for batch and streaming jobs running on this
    application. Supported with release labels emr-7.0.0 and above.
    """

    queueTimeoutMinutes: Integer | None
    maxConcurrentRuns: Integer | None


class InteractiveConfiguration(TypedDict, total=False):
    """The configuration to use to enable the different types of interactive
    use cases in an application.
    """

    studioEnabled: Boolean | None
    livyEndpointEnabled: Boolean | None


EncryptionContext = dict[EncryptionContextKey, EncryptionContextValue]


class DiskEncryptionConfiguration(TypedDict, total=False):
    """The configuration object that allows encrypting local disks."""

    encryptionContext: EncryptionContext | None
    encryptionKeyArn: EncryptionKeyArn | None


class PrometheusMonitoringConfiguration(TypedDict, total=False):
    """The monitoring configuration object you can configure to send metrics to
    Amazon Managed Service for Prometheus for a job run.
    """

    remoteWriteUrl: PrometheusUrlString | None


LogTypeList = list[LogTypeString]
LogTypeMap = dict[WorkerTypeString, LogTypeList]


class CloudWatchLoggingConfiguration(TypedDict, total=False):
    """The Amazon CloudWatch configuration for monitoring logs. You can
    configure your jobs to send log information to CloudWatch.
    """

    enabled: Boolean
    logGroupName: LogGroupName | None
    logStreamNamePrefix: LogStreamNamePrefix | None
    encryptionKeyArn: EncryptionKeyArn | None
    logTypes: LogTypeMap | None


class ManagedPersistenceMonitoringConfiguration(TypedDict, total=False):
    """The managed log persistence configuration for a job run."""

    enabled: Boolean | None
    encryptionKeyArn: EncryptionKeyArn | None


class S3MonitoringConfiguration(TypedDict, total=False):
    """The Amazon S3 configuration for monitoring log publishing. You can
    configure your jobs to send log information to Amazon S3.
    """

    logUri: UriString | None
    encryptionKeyArn: EncryptionKeyArn | None


class MonitoringConfiguration(TypedDict, total=False):
    """The configuration setting for monitoring."""

    s3MonitoringConfiguration: S3MonitoringConfiguration | None
    managedPersistenceMonitoringConfiguration: ManagedPersistenceMonitoringConfiguration | None
    cloudWatchLoggingConfiguration: CloudWatchLoggingConfiguration | None
    prometheusMonitoringConfiguration: PrometheusMonitoringConfiguration | None


ConfigurationList = list["Configuration"]
SensitivePropertiesMap = dict[ConfigurationPropertyKey, ConfigurationPropertyValue]


class Configuration(TypedDict, total=False):
    """A configuration specification to be used when provisioning an
    application. A configuration consists of a classification, properties,
    and optional nested configurations. A classification refers to an
    application-specific configuration file. Properties are the settings you
    want to change in that file.
    """

    classification: String1024
    properties: SensitivePropertiesMap | None
    configurations: ConfigurationList | None


class ImageConfiguration(TypedDict, total=False):
    """The applied image configuration."""

    imageUri: ImageUri
    resolvedImageDigest: ImageDigest | None


class WorkerTypeSpecification(TypedDict, total=False):
    """The specifications for a worker type."""

    imageConfiguration: ImageConfiguration | None


WorkerTypeSpecificationMap = dict[WorkerTypeString, WorkerTypeSpecification]
SecurityGroupIds = list[SecurityGroupString]
SubnetIds = list[SubnetString]


class NetworkConfiguration(TypedDict, total=False):
    """The network configuration for customer VPC connectivity."""

    subnetIds: SubnetIds | None
    securityGroupIds: SecurityGroupIds | None


class AutoStopConfig(TypedDict, total=False):
    """The configuration for an application to automatically stop after a
    certain amount of time being idle.
    """

    enabled: Boolean | None
    idleTimeoutMinutes: AutoStopConfigIdleTimeoutMinutesInteger | None


class AutoStartConfig(TypedDict, total=False):
    """The configuration for an application to automatically start on job
    submission.
    """

    enabled: Boolean | None


TagMap = dict[TagKey, TagValue]
Date = datetime


class MaximumAllowedResources(TypedDict, total=False):
    """The maximum allowed cumulative resources for an application. No new
    resources will be created once the limit is hit.
    """

    cpu: CpuSize
    memory: MemorySize
    disk: DiskSize | None


class WorkerResourceConfig(TypedDict, total=False):
    """The cumulative configuration requirements for every worker instance of
    the worker type.
    """

    cpu: CpuSize
    memory: MemorySize
    disk: DiskSize | None
    diskType: DiskType | None


WorkerCounts = int


class InitialCapacityConfig(TypedDict, total=False):
    """The initial capacity configuration per worker."""

    workerCount: WorkerCounts
    workerConfiguration: WorkerResourceConfig | None


InitialCapacityConfigMap = dict[WorkerTypeString, InitialCapacityConfig]


class Application(TypedDict, total=False):
    applicationId: ApplicationId
    name: ApplicationName | None
    arn: ApplicationArn
    releaseLabel: ReleaseLabel
    type: EngineType
    state: ApplicationState
    stateDetails: String256 | None
    initialCapacity: InitialCapacityConfigMap | None
    maximumCapacity: MaximumAllowedResources | None
    createdAt: Date
    updatedAt: Date
    tags: TagMap | None
    autoStartConfiguration: AutoStartConfig | None
    autoStopConfiguration: AutoStopConfig | None
    networkConfiguration: NetworkConfiguration | None
    architecture: Architecture | None
    imageConfiguration: ImageConfiguration | None
    workerTypeSpecifications: WorkerTypeSpecificationMap | None
    runtimeConfiguration: ConfigurationList | None
    monitoringConfiguration: MonitoringConfiguration | None
    diskEncryptionConfiguration: DiskEncryptionConfiguration | None
    interactiveConfiguration: InteractiveConfiguration | None
    schedulerConfiguration: SchedulerConfiguration | None
    identityCenterConfiguration: IdentityCenterConfiguration | None
    jobLevelCostAllocationConfiguration: JobLevelCostAllocationConfiguration | None


class ApplicationSummary(TypedDict, total=False):
    id: ApplicationId
    name: ApplicationName | None
    arn: ApplicationArn
    releaseLabel: ReleaseLabel
    type: EngineType
    state: ApplicationState
    stateDetails: String256 | None
    createdAt: Date
    updatedAt: Date
    architecture: Architecture | None


ApplicationList = list[ApplicationSummary]
ApplicationStateSet = list[ApplicationState]


class CancelJobRunRequest(ServiceRequest):
    applicationId: ApplicationId
    jobRunId: JobRunId
    shutdownGracePeriodInSeconds: ShutdownGracePeriodInSeconds | None


class CancelJobRunResponse(TypedDict, total=False):
    applicationId: ApplicationId
    jobRunId: JobRunId


class ConfigurationOverrides(TypedDict, total=False):
    """A configuration specification to be used to override existing
    configurations.
    """

    applicationConfiguration: ConfigurationList | None
    monitoringConfiguration: MonitoringConfiguration | None
    diskEncryptionConfiguration: DiskEncryptionConfiguration | None


class IdentityCenterConfigurationInput(TypedDict, total=False):
    """The IAM Identity Center Configuration accepts the Identity Center
    instance parameter required to enable trusted identity propagation. This
    configuration allows identity propagation between integrated services
    and the Identity Center instance.
    """

    identityCenterInstanceArn: IdentityCenterInstanceArn | None
    userBackgroundSessionsEnabled: Boolean | None


class ImageConfigurationInput(TypedDict, total=False):
    """The image configuration."""

    imageUri: ImageUri | None


class WorkerTypeSpecificationInput(TypedDict, total=False):
    """The specifications for a worker type."""

    imageConfiguration: ImageConfigurationInput | None


WorkerTypeSpecificationInputMap = dict[WorkerTypeString, WorkerTypeSpecificationInput]


class CreateApplicationRequest(TypedDict, total=False):
    name: ApplicationName | None
    releaseLabel: ReleaseLabel
    type: EngineType
    clientToken: ClientToken
    initialCapacity: InitialCapacityConfigMap | None
    maximumCapacity: MaximumAllowedResources | None
    tags: TagMap | None
    autoStartConfiguration: AutoStartConfig | None
    autoStopConfiguration: AutoStopConfig | None
    networkConfiguration: NetworkConfiguration | None
    architecture: Architecture | None
    imageConfiguration: ImageConfigurationInput | None
    workerTypeSpecifications: WorkerTypeSpecificationInputMap | None
    runtimeConfiguration: ConfigurationList | None
    monitoringConfiguration: MonitoringConfiguration | None
    diskEncryptionConfiguration: DiskEncryptionConfiguration | None
    interactiveConfiguration: InteractiveConfiguration | None
    schedulerConfiguration: SchedulerConfiguration | None
    identityCenterConfiguration: IdentityCenterConfigurationInput | None
    jobLevelCostAllocationConfiguration: JobLevelCostAllocationConfiguration | None


class CreateApplicationResponse(TypedDict, total=False):
    applicationId: ApplicationId
    name: ApplicationName | None
    arn: ApplicationArn


class DeleteApplicationRequest(ServiceRequest):
    applicationId: ApplicationId


class DeleteApplicationResponse(TypedDict, total=False):
    pass


Duration = int
EntryPointArguments = list[EntryPointArgument]


class GetApplicationRequest(ServiceRequest):
    applicationId: ApplicationId


class GetApplicationResponse(TypedDict, total=False):
    application: Application


class GetDashboardForJobRunRequest(ServiceRequest):
    applicationId: ApplicationId
    jobRunId: JobRunId
    attempt: AttemptNumber | None
    accessSystemProfileLogs: Boolean | None


class GetDashboardForJobRunResponse(TypedDict, total=False):
    url: Url | None


class GetJobRunRequest(ServiceRequest):
    applicationId: ApplicationId
    jobRunId: JobRunId
    attempt: AttemptNumber | None


Long = int


class RetryPolicy(TypedDict, total=False):
    """The retry policy to use for a job run."""

    maxAttempts: AttemptNumber | None
    maxFailedAttemptsPerHour: RetryPolicyMaxFailedAttemptsPerHourInteger | None


class ResourceUtilization(TypedDict, total=False):
    """The resource utilization for memory, storage, and vCPU for jobs."""

    vCPUHour: Double | None
    memoryGBHour: Double | None
    storageGBHour: Double | None


class TotalResourceUtilization(TypedDict, total=False):
    """The aggregate vCPU, memory, and storage resources used from the time job
    start executing till the time job is terminated, rounded up to the
    nearest second.
    """

    vCPUHour: Double | None
    memoryGBHour: Double | None
    storageGBHour: Double | None


class Hive(TypedDict, total=False):
    """The configurations for the Hive job driver."""

    query: Query
    initQueryFile: InitScriptPath | None
    parameters: HiveCliParameters | None


class SparkSubmit(TypedDict, total=False):
    """The configurations for the Spark submit job driver."""

    entryPoint: EntryPointPath
    entryPointArguments: EntryPointArguments | None
    sparkSubmitParameters: SparkSubmitParameters | None


class JobDriver(TypedDict, total=False):
    """The driver that the job runs on."""

    sparkSubmit: SparkSubmit | None
    hive: Hive | None


PolicyArnList = list[Arn]


class JobRunExecutionIamPolicy(TypedDict, total=False):
    """Optional IAM policy. The resulting job IAM role permissions will be an
    intersection of the policies passed and the policy associated with your
    job execution role.
    """

    policy: PolicyDocument | None
    policyArns: PolicyArnList | None


class JobRun(TypedDict, total=False):
    """Information about a job run. A job run is a unit of work, such as a
    Spark JAR, Hive query, or SparkSQL query, that you submit to an Amazon
    EMR Serverless application.
    """

    applicationId: ApplicationId
    jobRunId: JobRunId
    name: String256 | None
    arn: JobArn
    createdBy: RequestIdentityUserArn
    createdAt: Date
    updatedAt: Date
    executionRole: IAMRoleArn
    executionIamPolicy: JobRunExecutionIamPolicy | None
    state: JobRunState
    stateDetails: String256
    releaseLabel: ReleaseLabel
    configurationOverrides: ConfigurationOverrides | None
    jobDriver: JobDriver
    tags: TagMap | None
    totalResourceUtilization: TotalResourceUtilization | None
    networkConfiguration: NetworkConfiguration | None
    totalExecutionDurationSeconds: Integer | None
    executionTimeoutMinutes: Duration | None
    billedResourceUtilization: ResourceUtilization | None
    mode: JobRunMode | None
    retryPolicy: RetryPolicy | None
    attempt: AttemptNumber | None
    attemptCreatedAt: Date | None
    attemptUpdatedAt: Date | None
    startedAt: Date | None
    endedAt: Date | None
    queuedDurationMilliseconds: Long | None


class GetJobRunResponse(TypedDict, total=False):
    jobRun: JobRun


class JobRunAttemptSummary(TypedDict, total=False):
    applicationId: ApplicationId
    id: JobRunId
    name: String256 | None
    mode: JobRunMode | None
    arn: JobArn
    createdBy: RequestIdentityUserArn
    jobCreatedAt: Date
    createdAt: Date
    updatedAt: Date
    executionRole: IAMRoleArn
    state: JobRunState
    stateDetails: String256
    releaseLabel: ReleaseLabel
    type: JobRunType | None
    attempt: AttemptNumber | None


JobRunAttempts = list[JobRunAttemptSummary]
JobRunStateSet = list[JobRunState]


class JobRunSummary(TypedDict, total=False):
    applicationId: ApplicationId
    id: JobRunId
    name: String256 | None
    mode: JobRunMode | None
    arn: JobArn
    createdBy: RequestIdentityUserArn
    createdAt: Date
    updatedAt: Date
    executionRole: IAMRoleArn
    state: JobRunState
    stateDetails: String256
    releaseLabel: ReleaseLabel
    type: JobRunType | None
    attempt: AttemptNumber | None
    attemptCreatedAt: Date | None
    attemptUpdatedAt: Date | None


JobRuns = list[JobRunSummary]


class ListApplicationsRequest(ServiceRequest):
    nextToken: NextToken | None
    maxResults: ListApplicationsRequestMaxResultsInteger | None
    states: ApplicationStateSet | None


class ListApplicationsResponse(TypedDict, total=False):
    applications: ApplicationList
    nextToken: NextToken | None


class ListJobRunAttemptsRequest(ServiceRequest):
    applicationId: ApplicationId
    jobRunId: JobRunId
    nextToken: NextToken | None
    maxResults: ListJobRunAttemptsRequestMaxResultsInteger | None


class ListJobRunAttemptsResponse(TypedDict, total=False):
    jobRunAttempts: JobRunAttempts
    nextToken: NextToken | None


class ListJobRunsRequest(ServiceRequest):
    applicationId: ApplicationId
    nextToken: NextToken | None
    maxResults: ListJobRunsRequestMaxResultsInteger | None
    createdAtAfter: Date | None
    createdAtBefore: Date | None
    states: JobRunStateSet | None
    mode: JobRunMode | None


class ListJobRunsResponse(TypedDict, total=False):
    jobRuns: JobRuns
    nextToken: NextToken | None


class ListTagsForResourceRequest(ServiceRequest):
    resourceArn: ResourceArn


class ListTagsForResourceResponse(TypedDict, total=False):
    tags: TagMap | None


class StartApplicationRequest(ServiceRequest):
    applicationId: ApplicationId


class StartApplicationResponse(TypedDict, total=False):
    pass


class StartJobRunRequest(ServiceRequest):
    applicationId: ApplicationId
    clientToken: ClientToken
    executionRoleArn: IAMRoleArn
    executionIamPolicy: JobRunExecutionIamPolicy | None
    jobDriver: JobDriver | None
    configurationOverrides: ConfigurationOverrides | None
    tags: TagMap | None
    executionTimeoutMinutes: Duration | None
    name: String256 | None
    mode: JobRunMode | None
    retryPolicy: RetryPolicy | None


class StartJobRunResponse(TypedDict, total=False):
    applicationId: ApplicationId
    jobRunId: JobRunId
    arn: JobArn


class StopApplicationRequest(ServiceRequest):
    applicationId: ApplicationId


class StopApplicationResponse(TypedDict, total=False):
    pass


TagKeyList = list[TagKey]


class TagResourceRequest(ServiceRequest):
    resourceArn: ResourceArn
    tags: TagMap


class TagResourceResponse(TypedDict, total=False):
    pass


class UntagResourceRequest(ServiceRequest):
    resourceArn: ResourceArn
    tagKeys: TagKeyList


class UntagResourceResponse(TypedDict, total=False):
    pass


class UpdateApplicationRequest(ServiceRequest):
    applicationId: ApplicationId
    clientToken: ClientToken
    initialCapacity: InitialCapacityConfigMap | None
    maximumCapacity: MaximumAllowedResources | None
    autoStartConfiguration: AutoStartConfig | None
    autoStopConfiguration: AutoStopConfig | None
    networkConfiguration: NetworkConfiguration | None
    architecture: Architecture | None
    imageConfiguration: ImageConfigurationInput | None
    workerTypeSpecifications: WorkerTypeSpecificationInputMap | None
    interactiveConfiguration: InteractiveConfiguration | None
    releaseLabel: ReleaseLabel | None
    runtimeConfiguration: ConfigurationList | None
    monitoringConfiguration: MonitoringConfiguration | None
    diskEncryptionConfiguration: DiskEncryptionConfiguration | None
    schedulerConfiguration: SchedulerConfiguration | None
    identityCenterConfiguration: IdentityCenterConfigurationInput | None
    jobLevelCostAllocationConfiguration: JobLevelCostAllocationConfiguration | None


class UpdateApplicationResponse(TypedDict, total=False):
    application: Application


class EmrServerlessApi:
    service: str = "emr-serverless"
    version: str = "2021-07-13"

    @handler("CancelJobRun")
    def cancel_job_run(
        self,
        context: RequestContext,
        application_id: ApplicationId,
        job_run_id: JobRunId,
        shutdown_grace_period_in_seconds: ShutdownGracePeriodInSeconds | None = None,
        **kwargs,
    ) -> CancelJobRunResponse:
        """Cancels a job run.

        :param application_id: The ID of the application on which the job run will be canceled.
        :param job_run_id: The ID of the job run to cancel.
        :param shutdown_grace_period_in_seconds: The duration in seconds to wait before forcefully terminating the job
        after cancellation is requested.
        :returns: CancelJobRunResponse
        :raises ValidationException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("CreateApplication", expand=False)
    def create_application(
        self, context: RequestContext, request: CreateApplicationRequest, **kwargs
    ) -> CreateApplicationResponse:
        """Creates an application.

        :param release_label: The Amazon EMR release associated with the application.
        :param type: The type of application you want to start, such as Spark or Hive.
        :param client_token: The client idempotency token of the application to create.
        :param name: The name of the application.
        :param initial_capacity: The capacity to initialize when the application is created.
        :param maximum_capacity: The maximum capacity to allocate when the application is created.
        :param tags: The tags assigned to the application.
        :param auto_start_configuration: The configuration for an application to automatically start on job
        submission.
        :param auto_stop_configuration: The configuration for an application to automatically stop after a
        certain amount of time being idle.
        :param network_configuration: The network configuration for customer VPC connectivity.
        :param architecture: The CPU architecture of an application.
        :param image_configuration: The image configuration for all worker types.
        :param worker_type_specifications: The key-value pairs that specify worker type to
        ``WorkerTypeSpecificationInput``.
        :param runtime_configuration: The
        `Configuration <https://docs.
        :param monitoring_configuration: The configuration setting for monitoring.
        :param disk_encryption_configuration: The configuration object that allows encrypting local disks.
        :param interactive_configuration: The interactive configuration object that enables the interactive use
        cases to use when running an application.
        :param scheduler_configuration: The scheduler configuration for batch and streaming jobs running on this
        application.
        :param identity_center_configuration: The IAM Identity Center Configuration accepts the Identity Center
        instance parameter required to enable trusted identity propagation.
        :param job_level_cost_allocation_configuration: The configuration object that enables job level cost allocation.
        :returns: CreateApplicationResponse
        :raises ValidationException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("DeleteApplication")
    def delete_application(
        self, context: RequestContext, application_id: ApplicationId, **kwargs
    ) -> DeleteApplicationResponse:
        """Deletes an application. An application has to be in a stopped or created
        state in order to be deleted.

        :param application_id: The ID of the application that will be deleted.
        :returns: DeleteApplicationResponse
        :raises ValidationException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetApplication")
    def get_application(
        self, context: RequestContext, application_id: ApplicationId, **kwargs
    ) -> GetApplicationResponse:
        """Displays detailed information about a specified application.

        :param application_id: The ID of the application that will be described.
        :returns: GetApplicationResponse
        :raises ValidationException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("GetDashboardForJobRun")
    def get_dashboard_for_job_run(
        self,
        context: RequestContext,
        application_id: ApplicationId,
        job_run_id: JobRunId,
        attempt: AttemptNumber | None = None,
        access_system_profile_logs: Boolean | None = None,
        **kwargs,
    ) -> GetDashboardForJobRunResponse:
        """Creates and returns a URL that you can use to access the application UIs
        for a job run.

        For jobs in a running state, the application UI is a live user interface
        such as the Spark or Tez web UI. For completed jobs, the application UI
        is a persistent application user interface such as the Spark History
        Server or persistent Tez UI.

        The URL is valid for one hour after you generate it. To access the
        application UI after that hour elapses, you must invoke the API again to
        generate a new URL.

        :param application_id: The ID of the application.
        :param job_run_id: The ID of the job run.
        :param attempt: An optimal parameter that indicates the amount of attempts for the job.
        :param access_system_profile_logs: Allows access to system profile logs for Lake Formation-enabled jobs.
        :returns: GetDashboardForJobRunResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("GetJobRun")
    def get_job_run(
        self,
        context: RequestContext,
        application_id: ApplicationId,
        job_run_id: JobRunId,
        attempt: AttemptNumber | None = None,
        **kwargs,
    ) -> GetJobRunResponse:
        """Displays detailed information about a job run.

        :param application_id: The ID of the application on which the job run is submitted.
        :param job_run_id: The ID of the job run.
        :param attempt: An optimal parameter that indicates the amount of attempts for the job.
        :returns: GetJobRunResponse
        :raises ValidationException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListApplications")
    def list_applications(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: ListApplicationsRequestMaxResultsInteger | None = None,
        states: ApplicationStateSet | None = None,
        **kwargs,
    ) -> ListApplicationsResponse:
        """Lists applications based on a set of parameters.

        :param next_token: The token for the next set of application results.
        :param max_results: The maximum number of applications that can be listed.
        :param states: An optional filter for application states.
        :returns: ListApplicationsResponse
        :raises ValidationException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("ListJobRunAttempts")
    def list_job_run_attempts(
        self,
        context: RequestContext,
        application_id: ApplicationId,
        job_run_id: JobRunId,
        next_token: NextToken | None = None,
        max_results: ListJobRunAttemptsRequestMaxResultsInteger | None = None,
        **kwargs,
    ) -> ListJobRunAttemptsResponse:
        """Lists all attempt of a job run.

        :param application_id: The ID of the application for which to list job runs.
        :param job_run_id: The ID of the job run to list.
        :param next_token: The token for the next set of job run attempt results.
        :param max_results: The maximum number of job run attempts to list.
        :returns: ListJobRunAttemptsResponse
        :raises ValidationException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListJobRuns")
    def list_job_runs(
        self,
        context: RequestContext,
        application_id: ApplicationId,
        next_token: NextToken | None = None,
        max_results: ListJobRunsRequestMaxResultsInteger | None = None,
        created_at_after: Date | None = None,
        created_at_before: Date | None = None,
        states: JobRunStateSet | None = None,
        mode: JobRunMode | None = None,
        **kwargs,
    ) -> ListJobRunsResponse:
        """Lists job runs based on a set of parameters.

        :param application_id: The ID of the application for which to list the job run.
        :param next_token: The token for the next set of job run results.
        :param max_results: The maximum number of job runs that can be listed.
        :param created_at_after: The lower bound of the option to filter by creation date and time.
        :param created_at_before: The upper bound of the option to filter by creation date and time.
        :param states: An optional filter for job run states.
        :param mode: The mode of the job runs to list.
        :returns: ListJobRunsResponse
        :raises ValidationException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("ListTagsForResource")
    def list_tags_for_resource(
        self, context: RequestContext, resource_arn: ResourceArn, **kwargs
    ) -> ListTagsForResourceResponse:
        """Lists the tags assigned to the resources.

        :param resource_arn: The Amazon Resource Name (ARN) that identifies the resource to list the
        tags for.
        :returns: ListTagsForResourceResponse
        :raises ValidationException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("StartApplication")
    def start_application(
        self, context: RequestContext, application_id: ApplicationId, **kwargs
    ) -> StartApplicationResponse:
        """Starts a specified application and initializes initial capacity if
        configured.

        :param application_id: The ID of the application to start.
        :returns: StartApplicationResponse
        :raises ValidationException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        :raises ServiceQuotaExceededException:
        """
        raise NotImplementedError

    @handler("StartJobRun")
    def start_job_run(
        self,
        context: RequestContext,
        application_id: ApplicationId,
        client_token: ClientToken,
        execution_role_arn: IAMRoleArn,
        execution_iam_policy: JobRunExecutionIamPolicy | None = None,
        job_driver: JobDriver | None = None,
        configuration_overrides: ConfigurationOverrides | None = None,
        tags: TagMap | None = None,
        execution_timeout_minutes: Duration | None = None,
        name: String256 | None = None,
        mode: JobRunMode | None = None,
        retry_policy: RetryPolicy | None = None,
        **kwargs,
    ) -> StartJobRunResponse:
        """Starts a job run.

        :param application_id: The ID of the application on which to run the job.
        :param client_token: The client idempotency token of the job run to start.
        :param execution_role_arn: The execution role ARN for the job run.
        :param execution_iam_policy: You can pass an optional IAM policy.
        :param job_driver: The job driver for the job run.
        :param configuration_overrides: The configuration overrides for the job run.
        :param tags: The tags assigned to the job run.
        :param execution_timeout_minutes: The maximum duration for the job run to run.
        :param name: The optional job run name.
        :param mode: The mode of the job run when it starts.
        :param retry_policy: The retry policy when job run starts.
        :returns: StartJobRunResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("StopApplication")
    def stop_application(
        self, context: RequestContext, application_id: ApplicationId, **kwargs
    ) -> StopApplicationResponse:
        """Stops a specified application and releases initial capacity if
        configured. All scheduled and running jobs must be completed or
        cancelled before stopping an application.

        :param application_id: The ID of the application to stop.
        :returns: StopApplicationResponse
        :raises ValidationException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("TagResource")
    def tag_resource(
        self, context: RequestContext, resource_arn: ResourceArn, tags: TagMap, **kwargs
    ) -> TagResourceResponse:
        """Assigns tags to resources. A tag is a label that you assign to an Amazon
        Web Services resource. Each tag consists of a key and an optional value,
        both of which you define. Tags enable you to categorize your Amazon Web
        Services resources by attributes such as purpose, owner, or environment.
        When you have many resources of the same type, you can quickly identify
        a specific resource based on the tags you've assigned to it.

        :param resource_arn: The Amazon Resource Name (ARN) that identifies the resource to list the
        tags for.
        :param tags: The tags to add to the resource.
        :returns: TagResourceResponse
        :raises ValidationException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("UntagResource")
    def untag_resource(
        self, context: RequestContext, resource_arn: ResourceArn, tag_keys: TagKeyList, **kwargs
    ) -> UntagResourceResponse:
        """Removes tags from resources.

        :param resource_arn: The Amazon Resource Name (ARN) that identifies the resource to list the
        tags for.
        :param tag_keys: The keys of the tags to be removed.
        :returns: UntagResourceResponse
        :raises ValidationException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError

    @handler("UpdateApplication")
    def update_application(
        self,
        context: RequestContext,
        application_id: ApplicationId,
        client_token: ClientToken,
        initial_capacity: InitialCapacityConfigMap | None = None,
        maximum_capacity: MaximumAllowedResources | None = None,
        auto_start_configuration: AutoStartConfig | None = None,
        auto_stop_configuration: AutoStopConfig | None = None,
        network_configuration: NetworkConfiguration | None = None,
        architecture: Architecture | None = None,
        image_configuration: ImageConfigurationInput | None = None,
        worker_type_specifications: WorkerTypeSpecificationInputMap | None = None,
        interactive_configuration: InteractiveConfiguration | None = None,
        release_label: ReleaseLabel | None = None,
        runtime_configuration: ConfigurationList | None = None,
        monitoring_configuration: MonitoringConfiguration | None = None,
        disk_encryption_configuration: DiskEncryptionConfiguration | None = None,
        scheduler_configuration: SchedulerConfiguration | None = None,
        identity_center_configuration: IdentityCenterConfigurationInput | None = None,
        job_level_cost_allocation_configuration: JobLevelCostAllocationConfiguration | None = None,
        **kwargs,
    ) -> UpdateApplicationResponse:
        """Updates a specified application. An application has to be in a stopped
        or created state in order to be updated.

        :param application_id: The ID of the application to update.
        :param client_token: The client idempotency token of the application to update.
        :param initial_capacity: The capacity to initialize when the application is updated.
        :param maximum_capacity: The maximum capacity to allocate when the application is updated.
        :param auto_start_configuration: The configuration for an application to automatically start on job
        submission.
        :param auto_stop_configuration: The configuration for an application to automatically stop after a
        certain amount of time being idle.
        :param network_configuration: The network configuration for customer VPC connectivity.
        :param architecture: The CPU architecture of an application.
        :param image_configuration: The image configuration to be used for all worker types.
        :param worker_type_specifications: The key-value pairs that specify worker type to
        ``WorkerTypeSpecificationInput``.
        :param interactive_configuration: The interactive configuration object that contains new interactive use
        cases when the application is updated.
        :param release_label: The Amazon EMR release label for the application.
        :param runtime_configuration: The
        `Configuration <https://docs.
        :param monitoring_configuration: The configuration setting for monitoring.
        :param disk_encryption_configuration: The configuration object that allows encrypting local disks.
        :param scheduler_configuration: The scheduler configuration for batch and streaming jobs running on this
        application.
        :param identity_center_configuration: Specifies the IAM Identity Center configuration used to enable or
        disable trusted identity propagation.
        :param job_level_cost_allocation_configuration: The configuration object that enables job level cost allocation.
        :returns: UpdateApplicationResponse
        :raises ValidationException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        """
        raise NotImplementedError
