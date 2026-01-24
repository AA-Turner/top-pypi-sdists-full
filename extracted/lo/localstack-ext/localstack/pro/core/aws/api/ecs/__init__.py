from datetime import datetime
from enum import StrEnum
from typing import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

AllowedInstanceType = str
Boolean = bool
BoxedBoolean = bool
BoxedDouble = float
BoxedInteger = int
CapacityProviderStrategyItemBase = int
CapacityProviderStrategyItemWeight = int
Double = float
Duration = int
EBSKMSKeyId = str
EBSSnapshotId = str
EBSVolumeType = str
ECSVolumeName = str
ExcludedInstanceType = str
IAMRoleArn = str
Integer = int
ManagedScalingInstanceWarmupPeriod = int
ManagedScalingStepSize = int
ManagedScalingTargetCapacity = int
PortNumber = int
SensitiveString = str
String = str
TagKey = str
TagValue = str
TaskVolumeStorageGiB = int


class AcceleratorManufacturer(StrEnum):
    amazon_web_services = "amazon-web-services"
    amd = "amd"
    nvidia = "nvidia"
    xilinx = "xilinx"
    habana = "habana"


class AcceleratorName(StrEnum):
    a100 = "a100"
    inferentia = "inferentia"
    k520 = "k520"
    k80 = "k80"
    m60 = "m60"
    radeon_pro_v520 = "radeon-pro-v520"
    t4 = "t4"
    vu9p = "vu9p"
    v100 = "v100"
    a10g = "a10g"
    h100 = "h100"
    t4g = "t4g"


class AcceleratorType(StrEnum):
    gpu = "gpu"
    fpga = "fpga"
    inference = "inference"


class AccessType(StrEnum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


class AgentUpdateStatus(StrEnum):
    PENDING = "PENDING"
    STAGING = "STAGING"
    STAGED = "STAGED"
    UPDATING = "UPDATING"
    UPDATED = "UPDATED"
    FAILED = "FAILED"


class ApplicationProtocol(StrEnum):
    http = "http"
    http2 = "http2"
    grpc = "grpc"


class AssignPublicIp(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class AvailabilityZoneRebalancing(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class BareMetal(StrEnum):
    included = "included"
    required = "required"
    excluded = "excluded"


class BurstablePerformance(StrEnum):
    included = "included"
    required = "required"
    excluded = "excluded"


class CPUArchitecture(StrEnum):
    X86_64 = "X86_64"
    ARM64 = "ARM64"


class CapacityProviderField(StrEnum):
    TAGS = "TAGS"


class CapacityProviderStatus(StrEnum):
    PROVISIONING = "PROVISIONING"
    ACTIVE = "ACTIVE"
    DEPROVISIONING = "DEPROVISIONING"
    INACTIVE = "INACTIVE"


class CapacityProviderType(StrEnum):
    EC2_AUTOSCALING = "EC2_AUTOSCALING"
    MANAGED_INSTANCES = "MANAGED_INSTANCES"
    FARGATE = "FARGATE"
    FARGATE_SPOT = "FARGATE_SPOT"


class CapacityProviderUpdateStatus(StrEnum):
    CREATE_IN_PROGRESS = "CREATE_IN_PROGRESS"
    CREATE_COMPLETE = "CREATE_COMPLETE"
    CREATE_FAILED = "CREATE_FAILED"
    DELETE_IN_PROGRESS = "DELETE_IN_PROGRESS"
    DELETE_COMPLETE = "DELETE_COMPLETE"
    DELETE_FAILED = "DELETE_FAILED"
    UPDATE_IN_PROGRESS = "UPDATE_IN_PROGRESS"
    UPDATE_COMPLETE = "UPDATE_COMPLETE"
    UPDATE_FAILED = "UPDATE_FAILED"


class ClusterField(StrEnum):
    ATTACHMENTS = "ATTACHMENTS"
    CONFIGURATIONS = "CONFIGURATIONS"
    SETTINGS = "SETTINGS"
    STATISTICS = "STATISTICS"
    TAGS = "TAGS"


class ClusterSettingName(StrEnum):
    containerInsights = "containerInsights"


class Compatibility(StrEnum):
    EC2 = "EC2"
    FARGATE = "FARGATE"
    EXTERNAL = "EXTERNAL"
    MANAGED_INSTANCES = "MANAGED_INSTANCES"


class Connectivity(StrEnum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"


class ContainerCondition(StrEnum):
    START = "START"
    COMPLETE = "COMPLETE"
    SUCCESS = "SUCCESS"
    HEALTHY = "HEALTHY"


class ContainerInstanceField(StrEnum):
    TAGS = "TAGS"
    CONTAINER_INSTANCE_HEALTH = "CONTAINER_INSTANCE_HEALTH"


class ContainerInstanceStatus(StrEnum):
    ACTIVE = "ACTIVE"
    DRAINING = "DRAINING"
    REGISTERING = "REGISTERING"
    DEREGISTERING = "DEREGISTERING"
    REGISTRATION_FAILED = "REGISTRATION_FAILED"


class CpuManufacturer(StrEnum):
    intel = "intel"
    amd = "amd"
    amazon_web_services = "amazon-web-services"


class DeploymentControllerType(StrEnum):
    ECS = "ECS"
    CODE_DEPLOY = "CODE_DEPLOY"
    EXTERNAL = "EXTERNAL"


class DeploymentLifecycleHookStage(StrEnum):
    RECONCILE_SERVICE = "RECONCILE_SERVICE"
    PRE_SCALE_UP = "PRE_SCALE_UP"
    POST_SCALE_UP = "POST_SCALE_UP"
    TEST_TRAFFIC_SHIFT = "TEST_TRAFFIC_SHIFT"
    POST_TEST_TRAFFIC_SHIFT = "POST_TEST_TRAFFIC_SHIFT"
    PRODUCTION_TRAFFIC_SHIFT = "PRODUCTION_TRAFFIC_SHIFT"
    POST_PRODUCTION_TRAFFIC_SHIFT = "POST_PRODUCTION_TRAFFIC_SHIFT"


class DeploymentRolloutState(StrEnum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    IN_PROGRESS = "IN_PROGRESS"


class DeploymentStrategy(StrEnum):
    ROLLING = "ROLLING"
    BLUE_GREEN = "BLUE_GREEN"
    LINEAR = "LINEAR"
    CANARY = "CANARY"


class DesiredStatus(StrEnum):
    RUNNING = "RUNNING"
    PENDING = "PENDING"
    STOPPED = "STOPPED"


class DeviceCgroupPermission(StrEnum):
    read = "read"
    write = "write"
    mknod = "mknod"


class EBSResourceType(StrEnum):
    volume = "volume"


class EFSAuthorizationConfigIAM(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class EFSTransitEncryption(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class EnvironmentFileType(StrEnum):
    s3 = "s3"


class ExecuteCommandLogging(StrEnum):
    NONE = "NONE"
    DEFAULT = "DEFAULT"
    OVERRIDE = "OVERRIDE"


class ExpressGatewayServiceInclude(StrEnum):
    TAGS = "TAGS"


class ExpressGatewayServiceScalingMetric(StrEnum):
    AVERAGE_CPU = "AVERAGE_CPU"
    AVERAGE_MEMORY = "AVERAGE_MEMORY"
    REQUEST_COUNT_PER_TARGET = "REQUEST_COUNT_PER_TARGET"


class ExpressGatewayServiceStatusCode(StrEnum):
    ACTIVE = "ACTIVE"
    DRAINING = "DRAINING"
    INACTIVE = "INACTIVE"


class FirelensConfigurationType(StrEnum):
    fluentd = "fluentd"
    fluentbit = "fluentbit"


class HealthStatus(StrEnum):
    HEALTHY = "HEALTHY"
    UNHEALTHY = "UNHEALTHY"
    UNKNOWN = "UNKNOWN"


class InstanceGeneration(StrEnum):
    current = "current"
    previous = "previous"


class InstanceHealthCheckState(StrEnum):
    OK = "OK"
    IMPAIRED = "IMPAIRED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    INITIALIZING = "INITIALIZING"


class InstanceHealthCheckType(StrEnum):
    CONTAINER_RUNTIME = "CONTAINER_RUNTIME"


class IpcMode(StrEnum):
    host = "host"
    task = "task"
    none = "none"


class LaunchType(StrEnum):
    EC2 = "EC2"
    FARGATE = "FARGATE"
    EXTERNAL = "EXTERNAL"
    MANAGED_INSTANCES = "MANAGED_INSTANCES"


class LocalStorage(StrEnum):
    included = "included"
    required = "required"
    excluded = "excluded"


class LocalStorageType(StrEnum):
    hdd = "hdd"
    ssd = "ssd"


class LogDriver(StrEnum):
    json_file = "json-file"
    syslog = "syslog"
    journald = "journald"
    gelf = "gelf"
    fluentd = "fluentd"
    awslogs = "awslogs"
    splunk = "splunk"
    awsfirelens = "awsfirelens"


class ManagedAgentName(StrEnum):
    ExecuteCommandAgent = "ExecuteCommandAgent"


class ManagedDraining(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class ManagedInstancesMonitoringOptions(StrEnum):
    BASIC = "BASIC"
    DETAILED = "DETAILED"


class ManagedResourceStatus(StrEnum):
    PROVISIONING = "PROVISIONING"
    ACTIVE = "ACTIVE"
    DEPROVISIONING = "DEPROVISIONING"
    DELETED = "DELETED"
    FAILED = "FAILED"


class ManagedScalingStatus(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class ManagedTerminationProtection(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class NetworkMode(StrEnum):
    bridge = "bridge"
    host = "host"
    awsvpc = "awsvpc"
    none = "none"


class OSFamily(StrEnum):
    WINDOWS_SERVER_2019_FULL = "WINDOWS_SERVER_2019_FULL"
    WINDOWS_SERVER_2019_CORE = "WINDOWS_SERVER_2019_CORE"
    WINDOWS_SERVER_2016_FULL = "WINDOWS_SERVER_2016_FULL"
    WINDOWS_SERVER_2004_CORE = "WINDOWS_SERVER_2004_CORE"
    WINDOWS_SERVER_2022_CORE = "WINDOWS_SERVER_2022_CORE"
    WINDOWS_SERVER_2022_FULL = "WINDOWS_SERVER_2022_FULL"
    WINDOWS_SERVER_2025_CORE = "WINDOWS_SERVER_2025_CORE"
    WINDOWS_SERVER_2025_FULL = "WINDOWS_SERVER_2025_FULL"
    WINDOWS_SERVER_20H2_CORE = "WINDOWS_SERVER_20H2_CORE"
    LINUX = "LINUX"


class PidMode(StrEnum):
    host = "host"
    task = "task"


class PlacementConstraintType(StrEnum):
    distinctInstance = "distinctInstance"
    memberOf = "memberOf"


class PlacementStrategyType(StrEnum):
    random = "random"
    spread = "spread"
    binpack = "binpack"


class PlatformDeviceType(StrEnum):
    GPU = "GPU"


class PropagateMITags(StrEnum):
    CAPACITY_PROVIDER = "CAPACITY_PROVIDER"
    NONE = "NONE"


class PropagateTags(StrEnum):
    TASK_DEFINITION = "TASK_DEFINITION"
    SERVICE = "SERVICE"
    NONE = "NONE"


class ProxyConfigurationType(StrEnum):
    APPMESH = "APPMESH"


class ResourceManagementType(StrEnum):
    CUSTOMER = "CUSTOMER"
    ECS = "ECS"


class ResourceType(StrEnum):
    GPU = "GPU"
    InferenceAccelerator = "InferenceAccelerator"


class ScaleUnit(StrEnum):
    PERCENT = "PERCENT"


class SchedulingStrategy(StrEnum):
    REPLICA = "REPLICA"
    DAEMON = "DAEMON"


class Scope(StrEnum):
    task = "task"
    shared = "shared"


class ServiceConnectAccessLoggingFormat(StrEnum):
    TEXT = "TEXT"
    JSON = "JSON"


class ServiceConnectIncludeQueryParameters(StrEnum):
    DISABLED = "DISABLED"
    ENABLED = "ENABLED"


class ServiceDeploymentLifecycleStage(StrEnum):
    RECONCILE_SERVICE = "RECONCILE_SERVICE"
    PRE_SCALE_UP = "PRE_SCALE_UP"
    SCALE_UP = "SCALE_UP"
    POST_SCALE_UP = "POST_SCALE_UP"
    TEST_TRAFFIC_SHIFT = "TEST_TRAFFIC_SHIFT"
    POST_TEST_TRAFFIC_SHIFT = "POST_TEST_TRAFFIC_SHIFT"
    PRODUCTION_TRAFFIC_SHIFT = "PRODUCTION_TRAFFIC_SHIFT"
    POST_PRODUCTION_TRAFFIC_SHIFT = "POST_PRODUCTION_TRAFFIC_SHIFT"
    BAKE_TIME = "BAKE_TIME"
    CLEAN_UP = "CLEAN_UP"


class ServiceDeploymentRollbackMonitorsStatus(StrEnum):
    TRIGGERED = "TRIGGERED"
    MONITORING = "MONITORING"
    MONITORING_COMPLETE = "MONITORING_COMPLETE"
    DISABLED = "DISABLED"


class ServiceDeploymentStatus(StrEnum):
    PENDING = "PENDING"
    SUCCESSFUL = "SUCCESSFUL"
    STOPPED = "STOPPED"
    STOP_REQUESTED = "STOP_REQUESTED"
    IN_PROGRESS = "IN_PROGRESS"
    ROLLBACK_REQUESTED = "ROLLBACK_REQUESTED"
    ROLLBACK_IN_PROGRESS = "ROLLBACK_IN_PROGRESS"
    ROLLBACK_SUCCESSFUL = "ROLLBACK_SUCCESSFUL"
    ROLLBACK_FAILED = "ROLLBACK_FAILED"


class ServiceField(StrEnum):
    TAGS = "TAGS"


class SettingName(StrEnum):
    serviceLongArnFormat = "serviceLongArnFormat"
    taskLongArnFormat = "taskLongArnFormat"
    containerInstanceLongArnFormat = "containerInstanceLongArnFormat"
    awsvpcTrunking = "awsvpcTrunking"
    containerInsights = "containerInsights"
    fargateFIPSMode = "fargateFIPSMode"
    tagResourceAuthorization = "tagResourceAuthorization"
    fargateTaskRetirementWaitPeriod = "fargateTaskRetirementWaitPeriod"
    guardDutyActivate = "guardDutyActivate"
    defaultLogDriverMode = "defaultLogDriverMode"


class SettingType(StrEnum):
    user = "user"
    aws_managed = "aws_managed"


class SortOrder(StrEnum):
    ASC = "ASC"
    DESC = "DESC"


class StabilityStatus(StrEnum):
    STEADY_STATE = "STEADY_STATE"
    STABILIZING = "STABILIZING"


class StopServiceDeploymentStopType(StrEnum):
    ABORT = "ABORT"
    ROLLBACK = "ROLLBACK"


class TargetType(StrEnum):
    container_instance = "container-instance"


class TaskDefinitionFamilyStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ALL = "ALL"


class TaskDefinitionField(StrEnum):
    TAGS = "TAGS"


class TaskDefinitionPlacementConstraintType(StrEnum):
    memberOf = "memberOf"


class TaskDefinitionStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETE_IN_PROGRESS = "DELETE_IN_PROGRESS"


class TaskField(StrEnum):
    TAGS = "TAGS"


class TaskFilesystemType(StrEnum):
    ext3 = "ext3"
    ext4 = "ext4"
    xfs = "xfs"
    ntfs = "ntfs"


class TaskSetField(StrEnum):
    TAGS = "TAGS"


class TaskStopCode(StrEnum):
    TaskFailedToStart = "TaskFailedToStart"
    EssentialContainerExited = "EssentialContainerExited"
    UserInitiated = "UserInitiated"
    ServiceSchedulerInitiated = "ServiceSchedulerInitiated"
    SpotInterruption = "SpotInterruption"
    TerminationNotice = "TerminationNotice"


class TransportProtocol(StrEnum):
    tcp = "tcp"
    udp = "udp"


class UlimitName(StrEnum):
    core = "core"
    cpu = "cpu"
    data = "data"
    fsize = "fsize"
    locks = "locks"
    memlock = "memlock"
    msgqueue = "msgqueue"
    nice = "nice"
    nofile = "nofile"
    nproc = "nproc"
    rss = "rss"
    rtprio = "rtprio"
    rttime = "rttime"
    sigpending = "sigpending"
    stack = "stack"


class VersionConsistency(StrEnum):
    enabled = "enabled"
    disabled = "disabled"


class AccessDeniedException(ServiceException):
    """You don't have authorization to perform the requested action."""

    code: str = "AccessDeniedException"
    sender_fault: bool = False
    status_code: int = 400


class AttributeLimitExceededException(ServiceException):
    """You can apply up to 10 custom attributes for each resource. You can view
    the attributes of a resource with
    `ListAttributes <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ListAttributes.html>`__.
    You can remove existing attributes on a resource with
    `DeleteAttributes <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_DeleteAttributes.html>`__.
    """

    code: str = "AttributeLimitExceededException"
    sender_fault: bool = False
    status_code: int = 400


class BlockedException(ServiceException):
    """Your Amazon Web Services account was blocked. For more information,
    contact `Amazon Web Services
    Support <http://aws.amazon.com/contact-us/>`__.
    """

    code: str = "BlockedException"
    sender_fault: bool = False
    status_code: int = 400


class ClientException(ServiceException):
    """These errors are usually caused by a client action. This client action
    might be using an action or resource on behalf of a user that doesn't
    have permissions to use the action or resource. Or, it might be
    specifying an identifier that isn't valid.
    """

    code: str = "ClientException"
    sender_fault: bool = False
    status_code: int = 400


class ClusterContainsCapacityProviderException(ServiceException):
    """The cluster contains one or more capacity providers that prevent the
    requested operation. This exception occurs when you try to delete a
    cluster that still has active capacity providers, including Amazon ECS
    Managed Instances capacity providers. You must first delete all capacity
    providers from the cluster before you can delete the cluster itself.
    """

    code: str = "ClusterContainsCapacityProviderException"
    sender_fault: bool = False
    status_code: int = 400


class ClusterContainsContainerInstancesException(ServiceException):
    """You can't delete a cluster that has registered container instances.
    First, deregister the container instances before you can delete the
    cluster. For more information, see
    `DeregisterContainerInstance <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_DeregisterContainerInstance.html>`__.
    """

    code: str = "ClusterContainsContainerInstancesException"
    sender_fault: bool = False
    status_code: int = 400


class ClusterContainsServicesException(ServiceException):
    """You can't delete a cluster that contains services. First, update the
    service to reduce its desired task count to 0, and then delete the
    service. For more information, see
    `UpdateService <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_UpdateService.html>`__
    and
    `DeleteService <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_DeleteService.html>`__.
    """

    code: str = "ClusterContainsServicesException"
    sender_fault: bool = False
    status_code: int = 400


class ClusterContainsTasksException(ServiceException):
    """You can't delete a cluster that has active tasks."""

    code: str = "ClusterContainsTasksException"
    sender_fault: bool = False
    status_code: int = 400


class ClusterNotFoundException(ServiceException):
    """The specified cluster wasn't found. You can view your available clusters
    with
    `ListClusters <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ListClusters.html>`__.
    Amazon ECS clusters are Region specific.
    """

    code: str = "ClusterNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


ResourceIds = list[String]


class ConflictException(ServiceException):
    """The request could not be processed because of conflict in the current
    state of the resource.
    """

    code: str = "ConflictException"
    sender_fault: bool = False
    status_code: int = 400
    resourceIds: ResourceIds | None


class InvalidParameterException(ServiceException):
    """The specified parameter isn't valid. Review the available parameters for
    the API request.

    For more information about service event errors, see `Amazon ECS service
    event
    messages <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-event-messages-list.html>`__.
    """

    code: str = "InvalidParameterException"
    sender_fault: bool = False
    status_code: int = 400


class LimitExceededException(ServiceException):
    """The limit for the resource was exceeded."""

    code: str = "LimitExceededException"
    sender_fault: bool = False
    status_code: int = 400


class MissingVersionException(ServiceException):
    """Amazon ECS can't determine the current version of the Amazon ECS
    container agent on the container instance and doesn't have enough
    information to proceed with an update. This could be because the agent
    running on the container instance is a previous or custom version that
    doesn't use our version information.
    """

    code: str = "MissingVersionException"
    sender_fault: bool = False
    status_code: int = 400


class NamespaceNotFoundException(ServiceException):
    """The specified namespace wasn't found."""

    code: str = "NamespaceNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class NoUpdateAvailableException(ServiceException):
    """There's no update available for this Amazon ECS container agent. This
    might be because the agent is already running the latest version or
    because it's so old that there's no update path to the current version.
    """

    code: str = "NoUpdateAvailableException"
    sender_fault: bool = False
    status_code: int = 400


class PlatformTaskDefinitionIncompatibilityException(ServiceException):
    """The specified platform version doesn't satisfy the required capabilities
    of the task definition.
    """

    code: str = "PlatformTaskDefinitionIncompatibilityException"
    sender_fault: bool = False
    status_code: int = 400


class PlatformUnknownException(ServiceException):
    """The specified platform version doesn't exist."""

    code: str = "PlatformUnknownException"
    sender_fault: bool = False
    status_code: int = 400


class ResourceInUseException(ServiceException):
    """The specified resource is in-use and can't be removed."""

    code: str = "ResourceInUseException"
    sender_fault: bool = False
    status_code: int = 400


class ResourceNotFoundException(ServiceException):
    """The specified resource wasn't found."""

    code: str = "ResourceNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class ServerException(ServiceException):
    """These errors are usually caused by a server issue."""

    code: str = "ServerException"
    sender_fault: bool = False
    status_code: int = 400


class ServiceDeploymentNotFoundException(ServiceException):
    """The service deploy ARN that you specified in the
    ``StopServiceDeployment`` doesn't exist. You can use
    ``ListServiceDeployments`` to retrieve the service deployment ARNs.
    """

    code: str = "ServiceDeploymentNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class ServiceNotActiveException(ServiceException):
    """The specified service isn't active. You can't update a service that's
    inactive. If you have previously deleted a service, you can re-create it
    with
    `CreateService <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_CreateService.html>`__.
    """

    code: str = "ServiceNotActiveException"
    sender_fault: bool = False
    status_code: int = 400


class ServiceNotFoundException(ServiceException):
    """The specified service wasn't found. You can view your available services
    with
    `ListServices <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ListServices.html>`__.
    Amazon ECS services are cluster specific and Region specific.
    """

    code: str = "ServiceNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class TargetNotConnectedException(ServiceException):
    """The execute command cannot run. This error can be caused by any of the
    following configuration issues:

    -  Incorrect IAM permissions

    -  The SSM agent is not installed or is not running

    -  There is an interface Amazon VPC endpoint for Amazon ECS, but there
       is not one for Systems Manager Session Manager

    For information about how to troubleshoot the issues, see
    `Troubleshooting issues with ECS
    Exec <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-exec.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    code: str = "TargetNotConnectedException"
    sender_fault: bool = False
    status_code: int = 400


class TargetNotFoundException(ServiceException):
    """The specified target wasn't found. You can view your available container
    instances with
    `ListContainerInstances <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ListContainerInstances.html>`__.
    Amazon ECS container instances are cluster-specific and Region-specific.
    """

    code: str = "TargetNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class TaskSetNotFoundException(ServiceException):
    """The specified task set wasn't found. You can view your available task
    sets with
    `DescribeTaskSets <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_DescribeTaskSets.html>`__.
    Task sets are specific to each cluster, service and Region.
    """

    code: str = "TaskSetNotFoundException"
    sender_fault: bool = False
    status_code: int = 400


class UnsupportedFeatureException(ServiceException):
    """The specified task isn't supported in this Region."""

    code: str = "UnsupportedFeatureException"
    sender_fault: bool = False
    status_code: int = 400


class UpdateInProgressException(ServiceException):
    """There's already a current Amazon ECS container agent update in progress
    on the container instance that's specified. If the container agent
    becomes disconnected while it's in a transitional stage, such as
    ``PENDING`` or ``STAGING``, the update process can get stuck in that
    state. However, when the agent reconnects, it resumes where it stopped
    previously.
    """

    code: str = "UpdateInProgressException"
    sender_fault: bool = False
    status_code: int = 400


class AcceleratorCountRequest(TypedDict, total=False):
    """The minimum and maximum number of accelerators (such as GPUs) for
    instance type selection. This is used for workloads that require
    specific numbers of accelerators.
    """

    min: BoxedInteger | None
    max: BoxedInteger | None


AcceleratorManufacturerSet = list[AcceleratorManufacturer]
AcceleratorNameSet = list[AcceleratorName]


class AcceleratorTotalMemoryMiBRequest(TypedDict, total=False):
    """The minimum and maximum total accelerator memory in mebibytes (MiB) for
    instance type selection. This is important for GPU workloads that
    require specific amounts of video memory.
    """

    min: BoxedInteger | None
    max: BoxedInteger | None


AcceleratorTypeSet = list[AcceleratorType]


class AdvancedConfiguration(TypedDict, total=False):
    """The advanced settings for a load balancer used in blue/green
    deployments. Specify the alternate target group, listener rules, and IAM
    role required for traffic shifting during blue/green deployments. For
    more information, see `Required resources for Amazon ECS blue/green
    deployments <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/blue-green-deployment-implementation.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    alternateTargetGroupArn: String | None
    productionListenerRule: String | None
    testListenerRule: String | None
    roleArn: String | None


AllowedInstanceTypeSet = list[AllowedInstanceType]


class KeyValuePair(TypedDict, total=False):
    """A key-value pair object."""

    name: String | None
    value: String | None


AttachmentDetails = list[KeyValuePair]


class Attachment(TypedDict, total=False):
    id: String | None
    type: String | None
    status: String | None
    details: AttachmentDetails | None


class AttachmentStateChange(TypedDict, total=False):
    """An object representing a change in state for a task attachment."""

    attachmentArn: String
    status: String


AttachmentStateChanges = list[AttachmentStateChange]
Attachments = list[Attachment]


class Attribute(TypedDict, total=False):
    """An attribute is a name-value pair that's associated with an Amazon ECS
    object. Use attributes to extend the Amazon ECS data model by adding
    custom metadata to your resources. For more information, see
    `Attributes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html#attributes>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    name: String
    value: String | None
    targetType: TargetType | None
    targetId: String | None


Attributes = list[Attribute]


class ManagedScaling(TypedDict, total=False):
    """The managed scaling settings for the Auto Scaling group capacity
    provider.

    When managed scaling is turned on, Amazon ECS manages the scale-in and
    scale-out actions of the Auto Scaling group. Amazon ECS manages a target
    tracking scaling policy using an Amazon ECS managed CloudWatch metric
    with the specified ``targetCapacity`` value as the target value for the
    metric. For more information, see `Using managed
    scaling <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/asg-capacity-providers.html#asg-capacity-providers-managed-scaling>`__
    in the *Amazon Elastic Container Service Developer Guide*.

    If managed scaling is off, the user must manage the scaling of the Auto
    Scaling group.
    """

    status: ManagedScalingStatus | None
    targetCapacity: ManagedScalingTargetCapacity | None
    minimumScalingStepSize: ManagedScalingStepSize | None
    maximumScalingStepSize: ManagedScalingStepSize | None
    instanceWarmupPeriod: ManagedScalingInstanceWarmupPeriod | None


class AutoScalingGroupProvider(TypedDict, total=False):
    """The details of the Auto Scaling group for the capacity provider."""

    autoScalingGroupArn: String
    managedScaling: ManagedScaling | None
    managedTerminationProtection: ManagedTerminationProtection | None
    managedDraining: ManagedDraining | None


class AutoScalingGroupProviderUpdate(TypedDict, total=False):
    """The details of the Auto Scaling group capacity provider to update."""

    managedScaling: ManagedScaling | None
    managedTerminationProtection: ManagedTerminationProtection | None
    managedDraining: ManagedDraining | None


StringList = list[String]


class AwsVpcConfiguration(TypedDict, total=False):
    """An object representing the networking details for a task or service. For
    example
    ``awsVpcConfiguration={subnets=["subnet-12344321"],securityGroups=["sg-12344321"]}``.
    """

    subnets: StringList
    securityGroups: StringList | None
    assignPublicIp: AssignPublicIp | None


class BaselineEbsBandwidthMbpsRequest(TypedDict, total=False):
    """The minimum and maximum baseline Amazon EBS bandwidth in megabits per
    second (Mbps) for instance type selection. This is important for
    workloads with high storage I/O requirements.
    """

    min: BoxedInteger | None
    max: BoxedInteger | None


class CanaryConfiguration(TypedDict, total=False):
    """Configuration for a canary deployment strategy that shifts a fixed
    percentage of traffic to the new service revision, waits for a specified
    bake time, then shifts the remaining traffic.

    This is only valid when you run ``CreateService`` or ``UpdateService``
    with ``deploymentController`` set to ``ECS`` and a
    ``deploymentConfiguration`` with a strategy set to ``CANARY``.
    """

    canaryPercent: Double | None
    canaryBakeTimeInMinutes: Integer | None


class Tag(TypedDict, total=False):
    """The metadata that you apply to a resource to help you categorize and
    organize them. Each tag consists of a key and an optional value. You
    define them.

    The following basic restrictions apply to tags:

    -  Maximum number of tags per resource - 50

    -  For each resource, each tag key must be unique, and each tag key can
       have only one value.

    -  Maximum key length - 128 Unicode characters in UTF-8

    -  Maximum value length - 256 Unicode characters in UTF-8

    -  If your tagging schema is used across multiple services and
       resources, remember that other services may have restrictions on
       allowed characters. Generally allowed characters are: letters,
       numbers, and spaces representable in UTF-8, and the following
       characters: + - = . _ : / @.

    -  Tag keys and values are case-sensitive.

    -  Do not use ``aws:``, ``AWS:``, or any upper or lowercase combination
       of such as a prefix for either keys or values as it is reserved for
       Amazon Web Services use. You cannot edit or delete tag keys or values
       with this prefix. Tags with this prefix do not count against your
       tags per resource limit.
    """

    key: TagKey | None
    value: TagValue | None


Tags = list[Tag]


class InfrastructureOptimization(TypedDict, total=False):
    """The configuration that controls how Amazon ECS optimizes your
    infrastructure.
    """

    scaleInAfter: BoxedInteger | None


class NetworkBandwidthGbpsRequest(TypedDict, total=False):
    """The minimum and maximum network bandwidth in gigabits per second (Gbps)
    for instance type selection. This is important for network-intensive
    workloads.
    """

    min: BoxedDouble | None
    max: BoxedDouble | None


class TotalLocalStorageGBRequest(TypedDict, total=False):
    """The minimum and maximum total local storage in gigabytes (GB) for
    instance types with local storage. This is useful for workloads that
    require local storage for temporary data or caching.
    """

    min: BoxedDouble | None
    max: BoxedDouble | None


LocalStorageTypeSet = list[LocalStorageType]


class NetworkInterfaceCountRequest(TypedDict, total=False):
    """The minimum and maximum number of network interfaces for instance type
    selection. This is useful for workloads that require multiple network
    interfaces.
    """

    min: BoxedInteger | None
    max: BoxedInteger | None


InstanceGenerationSet = list[InstanceGeneration]
ExcludedInstanceTypeSet = list[ExcludedInstanceType]


class MemoryGiBPerVCpuRequest(TypedDict, total=False):
    """The minimum and maximum amount of memory per vCPU in gibibytes (GiB).
    This helps ensure that instance types have the appropriate memory-to-CPU
    ratio for your workloads.
    """

    min: BoxedDouble | None
    max: BoxedDouble | None


CpuManufacturerSet = list[CpuManufacturer]


class MemoryMiBRequest(TypedDict, total=False):
    """The minimum and maximum amount of memory in mebibytes (MiB) for instance
    type selection. This ensures that selected instance types have adequate
    memory for your workloads.
    """

    min: BoxedInteger
    max: BoxedInteger | None


class VCpuCountRangeRequest(TypedDict, total=False):
    """The minimum and maximum number of vCPUs for instance type selection.
    This allows you to specify a range of vCPU counts that meet your
    workload requirements.
    """

    min: BoxedInteger
    max: BoxedInteger | None


class InstanceRequirementsRequest(TypedDict, total=False):
    """The instance requirements for attribute-based instance type selection.
    Instead of specifying exact instance types, you define requirements such
    as vCPU count, memory size, network performance, and accelerator
    specifications. Amazon ECS automatically selects Amazon EC2 instance
    types that match these requirements, providing flexibility and helping
    to mitigate capacity constraints.
    """

    vCpuCount: VCpuCountRangeRequest
    memoryMiB: MemoryMiBRequest
    cpuManufacturers: CpuManufacturerSet | None
    memoryGiBPerVCpu: MemoryGiBPerVCpuRequest | None
    excludedInstanceTypes: ExcludedInstanceTypeSet | None
    instanceGenerations: InstanceGenerationSet | None
    spotMaxPricePercentageOverLowestPrice: BoxedInteger | None
    onDemandMaxPricePercentageOverLowestPrice: BoxedInteger | None
    bareMetal: BareMetal | None
    burstablePerformance: BurstablePerformance | None
    requireHibernateSupport: BoxedBoolean | None
    networkInterfaceCount: NetworkInterfaceCountRequest | None
    localStorage: LocalStorage | None
    localStorageTypes: LocalStorageTypeSet | None
    totalLocalStorageGB: TotalLocalStorageGBRequest | None
    baselineEbsBandwidthMbps: BaselineEbsBandwidthMbpsRequest | None
    acceleratorTypes: AcceleratorTypeSet | None
    acceleratorCount: AcceleratorCountRequest | None
    acceleratorManufacturers: AcceleratorManufacturerSet | None
    acceleratorNames: AcceleratorNameSet | None
    acceleratorTotalMemoryMiB: AcceleratorTotalMemoryMiBRequest | None
    networkBandwidthGbps: NetworkBandwidthGbpsRequest | None
    allowedInstanceTypes: AllowedInstanceTypeSet | None
    maxSpotPriceAsPercentageOfOptimalOnDemandPrice: BoxedInteger | None


class ManagedInstancesStorageConfiguration(TypedDict, total=False):
    """The storage configuration for Amazon ECS Managed Instances. This defines
    the root volume configuration for the instances.
    """

    storageSizeGiB: TaskVolumeStorageGiB | None


class ManagedInstancesNetworkConfiguration(TypedDict, total=False):
    """The network configuration for Amazon ECS Managed Instances. This
    specifies the VPC subnets and security groups that instances use for
    network connectivity. Amazon ECS Managed Instances support multiple
    network modes including ``awsvpc`` (instances receive ENIs for task
    isolation), ``host`` (instances share network namespace with tasks), and
    ``none`` (no external network connectivity), ensuring backward
    compatibility for migrating workloads from Fargate or Amazon EC2.
    """

    subnets: StringList | None
    securityGroups: StringList | None


class InstanceLaunchTemplate(TypedDict, total=False):
    """The launch template configuration for Amazon ECS Managed Instances. This
    defines how Amazon ECS launches Amazon EC2 instances, including the
    instance profile for your tasks, network and storage configuration,
    capacity options, and instance requirements for flexible instance type
    selection.
    """

    ec2InstanceProfileArn: String
    networkConfiguration: ManagedInstancesNetworkConfiguration
    storageConfiguration: ManagedInstancesStorageConfiguration | None
    monitoring: ManagedInstancesMonitoringOptions | None
    instanceRequirements: InstanceRequirementsRequest | None


class ManagedInstancesProvider(TypedDict, total=False):
    """The configuration for a Amazon ECS Managed Instances provider. Amazon
    ECS uses this configuration to automatically launch, manage, and
    terminate Amazon EC2 instances on your behalf. Managed instances provide
    access to the full range of Amazon EC2 instance types and features while
    offloading infrastructure management to Amazon Web Services.
    """

    infrastructureRoleArn: String | None
    instanceLaunchTemplate: InstanceLaunchTemplate | None
    propagateTags: PropagateMITags | None
    infrastructureOptimization: InfrastructureOptimization | None


class CapacityProvider(TypedDict, total=False):
    capacityProviderArn: String | None
    name: String | None
    cluster: String | None
    status: CapacityProviderStatus | None
    autoScalingGroupProvider: AutoScalingGroupProvider | None
    managedInstancesProvider: ManagedInstancesProvider | None
    updateStatus: CapacityProviderUpdateStatus | None
    updateStatusReason: String | None
    tags: Tags | None
    type: CapacityProviderType | None


CapacityProviderFieldList = list[CapacityProviderField]


class CapacityProviderStrategyItem(TypedDict, total=False):
    """The details of a capacity provider strategy. A capacity provider
    strategy can be set when using the
    `RunTask <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RunTask.html>`__ or
    `CreateCluster <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_CreateCluster.html>`__
    APIs or as the default capacity provider strategy for a cluster with the
    ``CreateCluster`` API.

    Only capacity providers that are already associated with a cluster and
    have an ``ACTIVE`` or ``UPDATING`` status can be used in a capacity
    provider strategy. The
    `PutClusterCapacityProviders <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PutClusterCapacityProviders.html>`__
    API is used to associate a capacity provider with a cluster.

    If specifying a capacity provider that uses an Auto Scaling group, the
    capacity provider must already be created. New Auto Scaling group
    capacity providers can be created with the
    `CreateClusterCapacityProvider <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_CreateClusterCapacityProvider.html>`__
    API operation.

    To use a Fargate capacity provider, specify either the ``FARGATE`` or
    ``FARGATE_SPOT`` capacity providers. The Fargate capacity providers are
    available to all accounts and only need to be associated with a cluster
    to be used in a capacity provider strategy.

    With ``FARGATE_SPOT``, you can run interruption tolerant tasks at a rate
    that's discounted compared to the ``FARGATE`` price. ``FARGATE_SPOT``
    runs tasks on spare compute capacity. When Amazon Web Services needs the
    capacity back, your tasks are interrupted with a two-minute warning.
    ``FARGATE_SPOT`` supports Linux tasks with the X86_64 architecture on
    platform version 1.3.0 or later. ``FARGATE_SPOT`` supports Linux tasks
    with the ARM64 architecture on platform version 1.4.0 or later.

    A capacity provider strategy can contain a maximum of 20 capacity
    providers.
    """

    capacityProvider: String
    weight: CapacityProviderStrategyItemWeight | None
    base: CapacityProviderStrategyItemBase | None


CapacityProviderStrategy = list[CapacityProviderStrategyItem]
CapacityProviders = list[CapacityProvider]


class ClusterServiceConnectDefaults(TypedDict, total=False):
    """Use this parameter to set a default Service Connect namespace. After you
    set a default Service Connect namespace, any new services with Service
    Connect turned on that are created in the cluster are added as client
    services in the namespace. This setting only applies to new services
    that set the ``enabled`` parameter to ``true`` in the
    ``ServiceConnectConfiguration``. You can set the namespace of each
    service individually in the ``ServiceConnectConfiguration`` to override
    this default parameter.

    Tasks that run in a namespace can use short names to connect to services
    in the namespace. Tasks can connect to services across all of the
    clusters in the namespace. Tasks connect through a managed proxy
    container that collects logs and metrics for increased visibility. Only
    the tasks that Amazon ECS services create are supported with Service
    Connect. For more information, see `Service
    Connect <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-connect.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    namespace: String | None


class ClusterSetting(TypedDict, total=False):
    """The settings to use when creating a cluster. This parameter is used to
    turn on CloudWatch Container Insights with enhanced observability or
    CloudWatch Container Insights for a cluster.

    Container Insights with enhanced observability provides all the
    Container Insights metrics, plus additional task and container metrics.
    This version supports enhanced observability for Amazon ECS clusters
    using the Amazon EC2 and Fargate launch types. After you configure
    Container Insights with enhanced observability on Amazon ECS, Container
    Insights auto-collects detailed infrastructure telemetry from the
    cluster level down to the container level in your environment and
    displays these critical performance data in curated dashboards removing
    the heavy lifting in observability set-up.

    For more information, see `Monitor Amazon ECS containers using Container
    Insights with enhanced
    observability <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cloudwatch-container-insights.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    name: ClusterSettingName | None
    value: String | None


ClusterSettings = list[ClusterSetting]
Statistics = list[KeyValuePair]


class ManagedStorageConfiguration(TypedDict, total=False):
    """The managed storage configuration for the cluster."""

    kmsKeyId: String | None
    fargateEphemeralStorageKmsKeyId: String | None


class ExecuteCommandLogConfiguration(TypedDict, total=False):
    """The log configuration for the results of the execute command actions.
    The logs can be sent to CloudWatch Logs or an Amazon S3 bucket.
    """

    cloudWatchLogGroupName: String | None
    cloudWatchEncryptionEnabled: Boolean | None
    s3BucketName: String | None
    s3EncryptionEnabled: Boolean | None
    s3KeyPrefix: String | None


class ExecuteCommandConfiguration(TypedDict, total=False):
    """The details of the execute command configuration."""

    kmsKeyId: String | None
    logging: ExecuteCommandLogging | None
    logConfiguration: ExecuteCommandLogConfiguration | None


class ClusterConfiguration(TypedDict, total=False):
    """The execute command and managed storage configuration for the cluster."""

    executeCommandConfiguration: ExecuteCommandConfiguration | None
    managedStorageConfiguration: ManagedStorageConfiguration | None


class Cluster(TypedDict, total=False):
    """A regional grouping of one or more container instances where you can run
    task requests. Each account receives a default cluster the first time
    you use the Amazon ECS service, but you may also create other clusters.
    Clusters may contain more than one instance type simultaneously.
    """

    clusterArn: String | None
    clusterName: String | None
    configuration: ClusterConfiguration | None
    status: String | None
    registeredContainerInstancesCount: Integer | None
    runningTasksCount: Integer | None
    pendingTasksCount: Integer | None
    activeServicesCount: Integer | None
    statistics: Statistics | None
    tags: Tags | None
    settings: ClusterSettings | None
    capacityProviders: StringList | None
    defaultCapacityProviderStrategy: CapacityProviderStrategy | None
    attachments: Attachments | None
    attachmentsStatus: String | None
    serviceConnectDefaults: ClusterServiceConnectDefaults | None


ClusterFieldList = list[ClusterField]


class ClusterServiceConnectDefaultsRequest(TypedDict, total=False):
    """Use this parameter to set a default Service Connect namespace. After you
    set a default Service Connect namespace, any new services with Service
    Connect turned on that are created in the cluster are added as client
    services in the namespace. This setting only applies to new services
    that set the ``enabled`` parameter to ``true`` in the
    ``ServiceConnectConfiguration``. You can set the namespace of each
    service individually in the ``ServiceConnectConfiguration`` to override
    this default parameter.

    Tasks that run in a namespace can use short names to connect to services
    in the namespace. Tasks can connect to services across all of the
    clusters in the namespace. Tasks connect through a managed proxy
    container that collects logs and metrics for increased visibility. Only
    the tasks that Amazon ECS services create are supported with Service
    Connect. For more information, see `Service
    Connect <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-connect.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    namespace: String


Clusters = list[Cluster]
CompatibilityList = list[Compatibility]
GpuIds = list[String]
Timestamp = datetime


class ManagedAgent(TypedDict, total=False):
    """Details about the managed agent status for the container."""

    lastStartedAt: Timestamp | None
    name: ManagedAgentName | None
    reason: String | None
    lastStatus: String | None


ManagedAgents = list[ManagedAgent]


class NetworkInterface(TypedDict, total=False):
    """An object representing the elastic network interface for tasks that use
    the ``awsvpc`` network mode.
    """

    attachmentId: String | None
    privateIpv4Address: String | None
    ipv6Address: String | None


NetworkInterfaces = list[NetworkInterface]


class NetworkBinding(TypedDict, total=False):
    """Details on the network bindings between a container and its host
    container instance. After a task reaches the ``RUNNING`` status, manual
    and automatic host and container port assignments are visible in the
    ``networkBindings`` section of
    `DescribeTasks <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_DescribeTasks.html>`__
    API responses.
    """

    bindIP: String | None
    containerPort: BoxedInteger | None
    hostPort: BoxedInteger | None
    protocol: TransportProtocol | None
    containerPortRange: String | None
    hostPortRange: String | None


NetworkBindings = list[NetworkBinding]


class Container(TypedDict, total=False):
    """A Docker container that's part of a task."""

    containerArn: String | None
    taskArn: String | None
    name: String | None
    image: String | None
    imageDigest: String | None
    runtimeId: String | None
    lastStatus: String | None
    exitCode: BoxedInteger | None
    reason: String | None
    networkBindings: NetworkBindings | None
    networkInterfaces: NetworkInterfaces | None
    healthStatus: HealthStatus | None
    managedAgents: ManagedAgents | None
    cpu: String | None
    memory: String | None
    memoryReservation: String | None
    gpuIds: GpuIds | None


FirelensConfigurationOptionsMap = dict[String, String]


class FirelensConfiguration(TypedDict, total=False):
    type: FirelensConfigurationType
    options: FirelensConfigurationOptionsMap | None


class ResourceRequirement(TypedDict, total=False):
    value: String
    type: ResourceType


ResourceRequirements = list[ResourceRequirement]


class SystemControl(TypedDict, total=False):
    """A list of namespaced kernel parameters to set in the container. This
    parameter maps to ``Sysctls`` in the docker container create command and
    the ``--sysctl`` option to docker run. For example, you can configure
    ``net.ipv4.tcp_keepalive_time`` setting to maintain longer lived
    connections.

    We don't recommend that you specify network-related ``systemControls``
    parameters for multiple containers in a single task that also uses
    either the ``awsvpc`` or ``host`` network mode. Doing this has the
    following disadvantages:

    -  For tasks that use the ``awsvpc`` network mode including Fargate, if
       you set ``systemControls`` for any container, it applies to all
       containers in the task. If you set different ``systemControls`` for
       multiple containers in a single task, the container that's started
       last determines which ``systemControls`` take effect.

    -  For tasks that use the ``host`` network mode, the network namespace
       ``systemControls`` aren't supported.

    If you're setting an IPC resource namespace to use for the containers in
    the task, the following conditions apply to your system controls. For
    more information, see `IPC
    mode <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html#task_definition_ipcmode>`__.

    -  For tasks that use the ``host`` IPC mode, IPC namespace
       ``systemControls`` aren't supported.

    -  For tasks that use the ``task`` IPC mode, IPC namespace
       ``systemControls`` values apply to all containers within a task.

    This parameter is not supported for Windows containers.

    This parameter is only supported for tasks that are hosted on Fargate if
    the tasks are using platform version ``1.4.0`` or later (Linux). This
    isn't supported for Windows containers on Fargate.
    """

    namespace: String | None
    value: String | None


SystemControls = list[SystemControl]


class HealthCheck(TypedDict, total=False):
    """An object representing a container health check. Health check parameters
    that are specified in a container definition override any Docker health
    checks that exist in the container image (such as those specified in a
    parent image or from the image's Dockerfile). This configuration maps to
    the ``HEALTHCHECK`` parameter of docker run.

    The Amazon ECS container agent only monitors and reports on the health
    checks specified in the task definition. Amazon ECS does not monitor
    Docker health checks that are embedded in a container image and not
    specified in the container definition. Health check parameters that are
    specified in a container definition override any Docker health checks
    that exist in the container image.

    You can view the health status of both individual containers and a task
    with the DescribeTasks API operation or when viewing the task details in
    the console.

    The health check is designed to make sure that your containers survive
    agent restarts, upgrades, or temporary unavailability.

    Amazon ECS performs health checks on containers with the default that
    launched the container instance or the task.

    The following describes the possible ``healthStatus`` values for a
    container:

    -  ``HEALTHY``-The container health check has passed successfully.

    -  ``UNHEALTHY``-The container health check has failed.

    -  ``UNKNOWN``-The container health check is being evaluated, there's no
       container health check defined, or Amazon ECS doesn't have the health
       status of the container.

    The following describes the possible ``healthStatus`` values based on
    the container health checker status of essential containers in the task
    with the following priority order (high to low):

    -  ``UNHEALTHY``-One or more essential containers have failed their
       health check.

    -  ``UNKNOWN``-Any essential container running within the task is in an
       ``UNKNOWN`` state and no other essential containers have an
       ``UNHEALTHY`` state.

    -  ``HEALTHY``-All essential containers within the task have passed
       their health checks.

    Consider the following task health example with 2 containers.

    -  If Container1 is ``UNHEALTHY`` and Container2 is ``UNKNOWN``, the
       task health is ``UNHEALTHY``.

    -  If Container1 is ``UNHEALTHY`` and Container2 is ``HEALTHY``, the
       task health is ``UNHEALTHY``.

    -  If Container1 is ``HEALTHY`` and Container2 is ``UNKNOWN``, the task
       health is ``UNKNOWN``.

    -  If Container1 is ``HEALTHY`` and Container2 is ``HEALTHY``, the task
       health is ``HEALTHY``.

    Consider the following task health example with 3 containers.

    -  If Container1 is ``UNHEALTHY`` and Container2 is ``UNKNOWN``, and
       Container3 is ``UNKNOWN``, the task health is ``UNHEALTHY``.

    -  If Container1 is ``UNHEALTHY`` and Container2 is ``UNKNOWN``, and
       Container3 is ``HEALTHY``, the task health is ``UNHEALTHY``.

    -  If Container1 is ``UNHEALTHY`` and Container2 is ``HEALTHY``, and
       Container3 is ``HEALTHY``, the task health is ``UNHEALTHY``.

    -  If Container1 is ``HEALTHY`` and Container2 is ``UNKNOWN``, and
       Container3 is ``HEALTHY``, the task health is ``UNKNOWN``.

    -  If Container1 is ``HEALTHY`` and Container2 is ``UNKNOWN``, and
       Container3 is ``UNKNOWN``, the task health is ``UNKNOWN``.

    -  If Container1 is ``HEALTHY`` and Container2 is ``HEALTHY``, and
       Container3 is ``HEALTHY``, the task health is ``HEALTHY``.

    If a task is run manually, and not as part of a service, the task will
    continue its lifecycle regardless of its health status. For tasks that
    are part of a service, if the task reports as unhealthy then the task
    will be stopped and the service scheduler will replace it.

    When a container health check fails for a task that is part of a
    service, the following process occurs:

    #. The task is marked as ``UNHEALTHY``.

    #. The unhealthy task will be stopped, and during the stopping process,
       it will go through the following states:

       -  ``DEACTIVATING`` - In this state, Amazon ECS performs additional
          steps before stopping the task. For example, for tasks that are
          part of services configured to use Elastic Load Balancing target
          groups, target groups will be deregistered in this state.

       -  ``STOPPING`` - The task is in the process of being stopped.

       -  ``DEPROVISIONING`` - Resources associated with the task are being
          cleaned up.

       -  ``STOPPED`` - The task has been completely stopped.

    #. After the old task stops, a new task will be launched to ensure
       service operation, and the new task will go through the following
       lifecycle:

       -  ``PROVISIONING`` - Resources required for the task are being
          provisioned.

       -  ``PENDING`` - The task is waiting to be placed on a container
          instance.

       -  ``ACTIVATING`` - In this state, Amazon ECS pulls container images,
          creates containers, configures task networking, registers load
          balancer target groups, and configures service discovery status.

       -  ``RUNNING`` - The task is running and performing its work.

    For more detailed information about task lifecycle states, see `Task
    lifecycle <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-lifecycle-explanation.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.

    The following are notes about container health check support:

    -  If the Amazon ECS container agent becomes disconnected from the
       Amazon ECS service, this won't cause a container to transition to an
       ``UNHEALTHY`` status. This is by design, to ensure that containers
       remain running during agent restarts or temporary unavailability. The
       health check status is the "last heard from" response from the Amazon
       ECS agent, so if the container was considered ``HEALTHY`` prior to
       the disconnect, that status will remain until the agent reconnects
       and another health check occurs. There are no assumptions made about
       the status of the container health checks.

    -  Container health checks require version ``1.17.0`` or greater of the
       Amazon ECS container agent. For more information, see `Updating the
       Amazon ECS container
       agent <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-agent-update.html>`__.

    -  Container health checks are supported for Fargate tasks if you're
       using platform version ``1.1.0`` or greater. For more information,
       see `Fargate platform
       versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`__.

    -  Container health checks aren't supported for tasks that are part of a
       service that's configured to use a Classic Load Balancer.

    For an example of how to specify a task definition with multiple
    containers where container dependency is specified, see `Container
    dependency <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/example_task_definitions.html#example_task_definition-containerdependency>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    command: StringList
    interval: BoxedInteger | None
    timeout: BoxedInteger | None
    retries: BoxedInteger | None
    startPeriod: BoxedInteger | None


class Secret(TypedDict, total=False):
    """An object representing the secret to expose to your container. Secrets
    can be exposed to a container in the following ways:

    -  To inject sensitive data into your containers as environment
       variables, use the ``secrets`` container definition parameter.

    -  To reference sensitive information in the log configuration of a
       container, use the ``secretOptions`` container definition parameter.

    For more information, see `Specifying sensitive
    data <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/specifying-sensitive-data.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    name: String
    valueFrom: String


SecretList = list[Secret]
LogConfigurationOptionsMap = dict[String, String]


class LogConfiguration(TypedDict, total=False):
    """The log configuration for the container. This parameter maps to
    ``LogConfig`` in the docker container create command and the
    ``--log-driver`` option to docker run.

    By default, containers use the same logging driver that the Docker
    daemon uses. However, the container might use a different logging driver
    than the Docker daemon by specifying a log driver configuration in the
    container definition.

    Understand the following when specifying a log configuration for your
    containers.

    -  Amazon ECS currently supports a subset of the logging drivers
       available to the Docker daemon. Additional log drivers may be
       available in future releases of the Amazon ECS container agent.

       For tasks on Fargate, the supported log drivers are ``awslogs``,
       ``splunk``, and ``awsfirelens``.

       For tasks hosted on Amazon EC2 instances, the supported log drivers
       are ``awslogs``, ``fluentd``, ``gelf``, ``json-file``,
       ``journald``, ``syslog``, ``splunk``, and ``awsfirelens``.

    -  This parameter requires version 1.18 of the Docker Remote API or
       greater on your container instance.

    -  For tasks that are hosted on Amazon EC2 instances, the Amazon ECS
       container agent must register the available logging drivers with the
       ``ECS_AVAILABLE_LOGGING_DRIVERS`` environment variable before
       containers placed on that instance can use these log configuration
       options. For more information, see `Amazon ECS container agent
       configuration <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-agent-config.html>`__
       in the *Amazon Elastic Container Service Developer Guide*.

    -  For tasks that are on Fargate, because you don't have access to the
       underlying infrastructure your tasks are hosted on, any additional
       software needed must be installed outside of the task. For example,
       the Fluentd output aggregators or a remote host running Logstash to
       send Gelf logs to.
    """

    logDriver: LogDriver
    options: LogConfigurationOptionsMap | None
    secretOptions: SecretList | None


class Ulimit(TypedDict, total=False):
    """The ``ulimit`` settings to pass to the container.

    Amazon ECS tasks hosted on Fargate use the default resource limit values
    set by the operating system with the exception of the ``nofile``
    resource limit parameter which Fargate overrides. The ``nofile``
    resource limit sets a restriction on the number of open files that a
    container can use. The default ``nofile`` soft limit is ``65535`` and
    the default hard limit is ``65535``.

    You can specify the ``ulimit`` settings for a container in a task
    definition.
    """

    name: UlimitName
    softLimit: Integer
    hardLimit: Integer


UlimitList = list[Ulimit]
DockerLabelsMap = dict[String, String]


class HostEntry(TypedDict, total=False):
    """Hostnames and IP address entries that are added to the ``/etc/hosts``
    file of a container via the ``extraHosts`` parameter of its
    `ContainerDefinition <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ContainerDefinition.html>`__.
    """

    hostname: String
    ipAddress: String


HostEntryList = list[HostEntry]


class ContainerDependency(TypedDict, total=False):
    """The dependencies defined for container startup and shutdown. A container
    can contain multiple dependencies. When a dependency is defined for
    container startup, for container shutdown it is reversed.

    Your Amazon ECS container instances require at least version 1.26.0 of
    the container agent to use container dependencies. However, we recommend
    using the latest container agent version. For information about checking
    your agent version and updating to the latest version, see `Updating the
    Amazon ECS Container
    Agent <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-agent-update.html>`__
    in the *Amazon Elastic Container Service Developer Guide*. If you're
    using an Amazon ECS-optimized Linux AMI, your instance needs at least
    version 1.26.0-1 of the ``ecs-init`` package. If your container
    instances are launched from version ``20190301`` or later, then they
    contain the required versions of the container agent and ``ecs-init``.
    For more information, see `Amazon ECS-optimized Linux
    AMI <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.

    For tasks that use the Fargate launch type, the task or service requires
    the following platforms:

    -  Linux platform version ``1.3.0`` or later.

    -  Windows platform version ``1.0.0`` or later.

    For more information about how to create a container dependency, see
    `Container
    dependency <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/example_task_definitions.html#example_task_definition-containerdependency>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    containerName: String
    condition: ContainerCondition


ContainerDependencies = list[ContainerDependency]


class Tmpfs(TypedDict, total=False):
    """The container path, mount options, and size of the tmpfs mount."""

    containerPath: String
    size: Integer
    mountOptions: StringList | None


TmpfsList = list[Tmpfs]
DeviceCgroupPermissions = list[DeviceCgroupPermission]


class Device(TypedDict, total=False):
    """An object representing a container instance host device."""

    hostPath: String
    containerPath: String | None
    permissions: DeviceCgroupPermissions | None


DevicesList = list[Device]


class KernelCapabilities(TypedDict, total=False):
    """The Linux capabilities to add or remove from the default Docker
    configuration for a container defined in the task definition. For more
    detailed information about these Linux capabilities, see the
    `capabilities(7) <http://man7.org/linux/man-pages/man7/capabilities.7.html>`__
    Linux manual page.

    The following describes how Docker processes the Linux capabilities
    specified in the ``add`` and ``drop`` request parameters. For
    information about the latest behavior, see `Docker Compose: order of
    cap_drop and
    cap_add <https://forums.docker.com/t/docker-compose-order-of-cap-drop-and-cap-add/97136/1>`__
    in the Docker Community Forum.

    -  When the container is a privleged container, the container
       capabilities are all of the default Docker capabilities. The
       capabilities specified in the ``add`` request parameter, and the
       ``drop`` request parameter are ignored.

    -  When the ``add`` request parameter is set to ALL, the container
       capabilities are all of the default Docker capabilities, excluding
       those specified in the ``drop`` request parameter.

    -  When the ``drop`` request parameter is set to ALL, the container
       capabilities are the capabilities specified in the ``add`` request
       parameter.

    -  When the ``add`` request parameter and the ``drop`` request parameter
       are both empty, the capabilities the container capabilities are all
       of the default Docker capabilities.

    -  The default is to first drop the capabilities specified in the
       ``drop`` request parameter, and then add the capabilities specified
       in the ``add`` request parameter.
    """

    add: StringList | None
    drop: StringList | None


class LinuxParameters(TypedDict, total=False):
    """The Linux-specific options that are applied to the container, such as
    Linux
    `KernelCapabilities <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_KernelCapabilities.html>`__.
    """

    capabilities: KernelCapabilities | None
    devices: DevicesList | None
    initProcessEnabled: BoxedBoolean | None
    sharedMemorySize: BoxedInteger | None
    tmpfs: TmpfsList | None
    maxSwap: BoxedInteger | None
    swappiness: BoxedInteger | None


class VolumeFrom(TypedDict, total=False):
    """Details on a data volume from another container in the same task
    definition.
    """

    sourceContainer: String | None
    readOnly: BoxedBoolean | None


VolumeFromList = list[VolumeFrom]


class MountPoint(TypedDict, total=False):
    """The details for a volume mount point that's used in a container
    definition.
    """

    sourceVolume: String | None
    containerPath: String | None
    readOnly: BoxedBoolean | None


MountPointList = list[MountPoint]


class EnvironmentFile(TypedDict, total=False):
    value: String
    type: EnvironmentFileType


EnvironmentFiles = list[EnvironmentFile]
EnvironmentVariables = list[KeyValuePair]
IntegerList = list[BoxedInteger]


class ContainerRestartPolicy(TypedDict, total=False):
    """You can enable a restart policy for each container defined in your task
    definition, to overcome transient failures faster and maintain task
    availability. When you enable a restart policy for a container, Amazon
    ECS can restart the container if it exits, without needing to replace
    the task. For more information, see `Restart individual containers in
    Amazon ECS tasks with container restart
    policies <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-restart-policy.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    enabled: BoxedBoolean
    ignoredExitCodes: IntegerList | None
    restartAttemptPeriod: BoxedInteger | None


class PortMapping(TypedDict, total=False):
    """Port mappings allow containers to access ports on the host container
    instance to send or receive traffic. Port mappings are specified as part
    of the container definition.

    If you use containers in a task with the ``awsvpc`` or ``host`` network
    mode, specify the exposed ports using ``containerPort``. The
    ``hostPort`` can be left blank or it must be the same value as the
    ``containerPort``.

    Most fields of this parameter (``containerPort``, ``hostPort``,
    ``protocol``) maps to ``PortBindings`` in the docker container create
    command and the ``--publish`` option to ``docker run``. If the network
    mode of a task definition is set to ``host``, host ports must either be
    undefined or match the container port in the port mapping.

    You can't expose the same container port for multiple protocols. If you
    attempt this, an error is returned.

    After a task reaches the ``RUNNING`` status, manual and automatic host
    and container port assignments are visible in the ``networkBindings``
    section of
    `DescribeTasks <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_DescribeTasks.html>`__
    API responses.
    """

    containerPort: BoxedInteger | None
    hostPort: BoxedInteger | None
    protocol: TransportProtocol | None
    name: String | None
    appProtocol: ApplicationProtocol | None
    containerPortRange: String | None


PortMappingList = list[PortMapping]


class RepositoryCredentials(TypedDict, total=False):
    """The repository credentials for private registry authentication."""

    credentialsParameter: String


class ContainerDefinition(TypedDict, total=False):
    """Container definitions are used in task definitions to describe the
    different containers that are launched as part of a task.
    """

    name: String | None
    image: String | None
    repositoryCredentials: RepositoryCredentials | None
    cpu: Integer | None
    memory: BoxedInteger | None
    memoryReservation: BoxedInteger | None
    links: StringList | None
    portMappings: PortMappingList | None
    essential: BoxedBoolean | None
    restartPolicy: ContainerRestartPolicy | None
    entryPoint: StringList | None
    command: StringList | None
    environment: EnvironmentVariables | None
    environmentFiles: EnvironmentFiles | None
    mountPoints: MountPointList | None
    volumesFrom: VolumeFromList | None
    linuxParameters: LinuxParameters | None
    secrets: SecretList | None
    dependsOn: ContainerDependencies | None
    startTimeout: BoxedInteger | None
    stopTimeout: BoxedInteger | None
    versionConsistency: VersionConsistency | None
    hostname: String | None
    user: String | None
    workingDirectory: String | None
    disableNetworking: BoxedBoolean | None
    privileged: BoxedBoolean | None
    readonlyRootFilesystem: BoxedBoolean | None
    dnsServers: StringList | None
    dnsSearchDomains: StringList | None
    extraHosts: HostEntryList | None
    dockerSecurityOptions: StringList | None
    interactive: BoxedBoolean | None
    pseudoTerminal: BoxedBoolean | None
    dockerLabels: DockerLabelsMap | None
    ulimits: UlimitList | None
    logConfiguration: LogConfiguration | None
    healthCheck: HealthCheck | None
    systemControls: SystemControls | None
    resourceRequirements: ResourceRequirements | None
    firelensConfiguration: FirelensConfiguration | None
    credentialSpecs: StringList | None


ContainerDefinitions = list[ContainerDefinition]


class ContainerImage(TypedDict, total=False):
    """The details about the container image a service revision uses.

    To ensure that all tasks in a service use the same container image,
    Amazon ECS resolves container image names and any image tags specified
    in the task definition to container image digests.

    After the container image digest has been established, Amazon ECS uses
    the digest to start any other desired tasks, and for any future service
    and service revision updates. This leads to all tasks in a service
    always running identical container images, resulting in version
    consistency for your software. For more information, see `Container
    image
    resolution <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-ecs.html#deployment-container-image-stability>`__
    in the Amazon ECS Developer Guide.
    """

    containerName: String | None
    imageDigest: String | None
    image: String | None


ContainerImages = list[ContainerImage]


class InstanceHealthCheckResult(TypedDict, total=False):
    type: InstanceHealthCheckType | None
    status: InstanceHealthCheckState | None
    lastUpdated: Timestamp | None
    lastStatusChange: Timestamp | None


InstanceHealthCheckResultList = list[InstanceHealthCheckResult]


class ContainerInstanceHealthStatus(TypedDict, total=False):
    """An object representing the health status of the container instance."""

    overallStatus: InstanceHealthCheckState | None
    details: InstanceHealthCheckResultList | None


Long = int


class Resource(TypedDict, total=False):
    name: String | None
    type: String | None
    doubleValue: Double | None
    longValue: Long | None
    integerValue: Integer | None
    stringSetValue: StringList | None


Resources = list[Resource]


class VersionInfo(TypedDict, total=False):
    """The Docker and Amazon ECS container agent version information about a
    container instance.
    """

    agentVersion: String | None
    agentHash: String | None
    dockerVersion: String | None


class ContainerInstance(TypedDict, total=False):
    """An Amazon EC2 or External instance that's running the Amazon ECS agent
    and has been registered with a cluster.
    """

    containerInstanceArn: String | None
    ec2InstanceId: String | None
    capacityProviderName: String | None
    version: Long | None
    versionInfo: VersionInfo | None
    remainingResources: Resources | None
    registeredResources: Resources | None
    status: String | None
    statusReason: String | None
    agentConnected: Boolean | None
    runningTasksCount: Integer | None
    pendingTasksCount: Integer | None
    agentUpdateStatus: AgentUpdateStatus | None
    attributes: Attributes | None
    registeredAt: Timestamp | None
    attachments: Attachments | None
    tags: Tags | None
    healthStatus: ContainerInstanceHealthStatus | None


ContainerInstanceFieldList = list[ContainerInstanceField]
ContainerInstances = list[ContainerInstance]


class ContainerOverride(TypedDict, total=False):
    """The overrides that are sent to a container. An empty container override
    can be passed in. An example of an empty container override is
    ``{"containerOverrides": [ ] }``. If a non-empty container override is
    specified, the ``name`` parameter must be included.

    You can use Secrets Manager or Amazon Web Services Systems Manager
    Parameter Store to store the sensitive data. For more information, see
    `Retrieve secrets through environment
    variables <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/secrets-envvar.html>`__
    in the Amazon ECS Developer Guide.
    """

    name: String | None
    command: StringList | None
    environment: EnvironmentVariables | None
    environmentFiles: EnvironmentFiles | None
    cpu: BoxedInteger | None
    memory: BoxedInteger | None
    memoryReservation: BoxedInteger | None
    resourceRequirements: ResourceRequirements | None


ContainerOverrides = list[ContainerOverride]


class ContainerStateChange(TypedDict, total=False):
    """An object that represents a change in state for a container."""

    containerName: String | None
    imageDigest: String | None
    runtimeId: String | None
    exitCode: BoxedInteger | None
    networkBindings: NetworkBindings | None
    reason: String | None
    status: String | None


ContainerStateChanges = list[ContainerStateChange]
Containers = list[Container]


class CreateManagedInstancesProviderConfiguration(TypedDict, total=False):
    """The configuration for creating a Amazon ECS Managed Instances provider.
    This specifies how Amazon ECS should manage Amazon EC2 instances,
    including the infrastructure role, instance launch template, and whether
    to propagate tags from the capacity provider to the instances.
    """

    infrastructureRoleArn: String
    instanceLaunchTemplate: InstanceLaunchTemplate
    propagateTags: PropagateMITags | None
    infrastructureOptimization: InfrastructureOptimization | None


class CreateCapacityProviderRequest(ServiceRequest):
    name: String
    cluster: String | None
    autoScalingGroupProvider: AutoScalingGroupProvider | None
    managedInstancesProvider: CreateManagedInstancesProviderConfiguration | None
    tags: Tags | None


class CreateCapacityProviderResponse(TypedDict, total=False):
    capacityProvider: CapacityProvider | None


class CreateClusterRequest(ServiceRequest):
    clusterName: String | None
    tags: Tags | None
    settings: ClusterSettings | None
    configuration: ClusterConfiguration | None
    capacityProviders: StringList | None
    defaultCapacityProviderStrategy: CapacityProviderStrategy | None
    serviceConnectDefaults: ClusterServiceConnectDefaultsRequest | None


class CreateClusterResponse(TypedDict, total=False):
    cluster: Cluster | None


class ExpressGatewayScalingTarget(TypedDict, total=False):
    """Defines the auto-scaling configuration for an Express service. This
    determines how the service automatically adjusts the number of running
    tasks based on demand metrics such as CPU utilization, memory
    utilization, or request count per target.

    Auto-scaling helps ensure your application can handle varying levels of
    traffic while optimizing costs by scaling down during low-demand
    periods. You can specify the minimum and maximum number of tasks, the
    scaling metric, and the target value for that metric.
    """

    minTaskCount: BoxedInteger | None
    maxTaskCount: BoxedInteger | None
    autoScalingMetric: ExpressGatewayServiceScalingMetric | None
    autoScalingTargetValue: BoxedInteger | None


class ExpressGatewayServiceNetworkConfiguration(TypedDict, total=False):
    """The network configuration for an Express service. By default, an Express
    service utilizes subnets and security groups associated with the default
    VPC.
    """

    securityGroups: StringList | None
    subnets: StringList | None


class ExpressGatewayRepositoryCredentials(TypedDict, total=False):
    """The repository credentials for private registry authentication to pass
    to the container.
    """

    credentialsParameter: String | None


class ExpressGatewayServiceAwsLogsConfiguration(TypedDict, total=False):
    """Specifies the Amazon CloudWatch Logs configuration for the Express
    service container.
    """

    logGroup: String
    logStreamPrefix: String


class ExpressGatewayContainer(TypedDict, total=False):
    """Defines the configuration for the primary container in an Express
    service. This container receives traffic from the Application Load
    Balancer and runs your application code.

    The container configuration includes the container image, port mapping,
    logging settings, environment variables, and secrets. The container
    image is the only required parameter, with sensible defaults provided
    for other settings.
    """

    image: String
    containerPort: BoxedInteger | None
    awsLogsConfiguration: ExpressGatewayServiceAwsLogsConfiguration | None
    repositoryCredentials: ExpressGatewayRepositoryCredentials | None
    command: StringList | None
    environment: EnvironmentVariables | None
    secrets: SecretList | None


class CreateExpressGatewayServiceRequest(ServiceRequest):
    executionRoleArn: String
    infrastructureRoleArn: String
    serviceName: String | None
    cluster: String | None
    healthCheckPath: String | None
    primaryContainer: ExpressGatewayContainer
    taskRoleArn: String | None
    networkConfiguration: ExpressGatewayServiceNetworkConfiguration | None
    cpu: String | None
    memory: String | None
    scalingTarget: ExpressGatewayScalingTarget | None
    tags: Tags | None


class IngressPathSummary(TypedDict, total=False):
    """The entry point into an Express service."""

    accessType: AccessType
    endpoint: String


IngressPathSummaries = list[IngressPathSummary]


class ExpressGatewayServiceConfiguration(TypedDict, total=False):
    """Represents a specific configuration revision of an Express service,
    containing all the settings and parameters for that revision.
    """

    serviceRevisionArn: String | None
    executionRoleArn: String | None
    taskRoleArn: String | None
    cpu: String | None
    memory: String | None
    networkConfiguration: ExpressGatewayServiceNetworkConfiguration | None
    healthCheckPath: String | None
    primaryContainer: ExpressGatewayContainer | None
    scalingTarget: ExpressGatewayScalingTarget | None
    ingressPaths: IngressPathSummaries | None
    createdAt: Timestamp | None


ExpressGatewayServiceConfigurations = list[ExpressGatewayServiceConfiguration]


class ExpressGatewayServiceStatus(TypedDict, total=False):
    """An object that defines the status of Express service creation and
    information about the status of the service.
    """

    statusCode: ExpressGatewayServiceStatusCode | None
    statusReason: String | None


class ECSExpressGatewayService(TypedDict, total=False):
    """Represents an Express service, which provides a simplified way to deploy
    containerized web applications on Amazon ECS with managed Amazon Web
    Services infrastructure. An Express service automatically provisions and
    manages Application Load Balancers, target groups, security groups, and
    auto-scaling policies.

    Express services use a service revision architecture where each service
    can have multiple active configurations, enabling blue-green deployments
    and gradual rollouts. The service maintains a list of active
    configurations and manages the lifecycle of the underlying Amazon Web
    Services resources.
    """

    cluster: String | None
    serviceName: String | None
    serviceArn: String | None
    infrastructureRoleArn: String | None
    status: ExpressGatewayServiceStatus | None
    currentDeployment: String | None
    activeConfigurations: ExpressGatewayServiceConfigurations | None
    tags: Tags | None
    createdAt: Timestamp | None
    updatedAt: Timestamp | None


class CreateExpressGatewayServiceResponse(TypedDict, total=False):
    service: ECSExpressGatewayService | None


class VpcLatticeConfiguration(TypedDict, total=False):
    """The VPC Lattice configuration for your service that holds the
    information for the target group(s) Amazon ECS tasks will be registered
    to.
    """

    roleArn: IAMRoleArn
    targetGroupArn: String
    portName: String


VpcLatticeConfigurations = list[VpcLatticeConfiguration]


class EBSTagSpecification(TypedDict, total=False):
    """The tag specifications of an Amazon EBS volume."""

    resourceType: EBSResourceType
    tags: Tags | None
    propagateTags: PropagateTags | None


EBSTagSpecifications = list[EBSTagSpecification]


class ServiceManagedEBSVolumeConfiguration(TypedDict, total=False):
    """The configuration for the Amazon EBS volume that Amazon ECS creates and
    manages on your behalf. These settings are used to create each Amazon
    EBS volume, with one volume created for each task in the service. For
    information about the supported launch types and operating systems, see
    `Supported operating systems and launch
    types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ebs-volumes.html#ebs-volumes-configuration>`__
    in the *Amazon Elastic Container Service Developer Guide*.

    Many of these parameters map 1:1 with the Amazon EBS ``CreateVolume``
    API request parameters.
    """

    encrypted: BoxedBoolean | None
    kmsKeyId: EBSKMSKeyId | None
    volumeType: EBSVolumeType | None
    sizeInGiB: BoxedInteger | None
    snapshotId: EBSSnapshotId | None
    volumeInitializationRate: BoxedInteger | None
    iops: BoxedInteger | None
    throughput: BoxedInteger | None
    tagSpecifications: EBSTagSpecifications | None
    roleArn: IAMRoleArn
    filesystemType: TaskFilesystemType | None


class ServiceVolumeConfiguration(TypedDict, total=False):
    """The configuration for a volume specified in the task definition as a
    volume that is configured at launch time. Currently, the only supported
    volume type is an Amazon EBS volume.
    """

    name: ECSVolumeName
    managedEBSVolume: ServiceManagedEBSVolumeConfiguration | None


ServiceVolumeConfigurations = list[ServiceVolumeConfiguration]


class ServiceConnectAccessLogConfiguration(TypedDict, total=False):
    """Configuration for Service Connect access logging. Access logs provide
    detailed information about requests made to your service, including
    request patterns, response codes, and timing data for debugging and
    monitoring purposes.

    To enable access logs, you must also specify a ``logConfiguration`` in
    the ``serviceConnectConfiguration``.
    """

    format: ServiceConnectAccessLoggingFormat
    includeQueryParameters: ServiceConnectIncludeQueryParameters | None


class ServiceConnectTlsCertificateAuthority(TypedDict, total=False):
    """The certificate root authority that secures your service."""

    awsPcaAuthorityArn: String | None


class ServiceConnectTlsConfiguration(TypedDict, total=False):
    """The key that encrypts and decrypts your resources for Service Connect
    TLS.
    """

    issuerCertificateAuthority: ServiceConnectTlsCertificateAuthority
    kmsKey: String | None
    roleArn: String | None


class TimeoutConfiguration(TypedDict, total=False):
    """An object that represents the timeout configurations for Service
    Connect.

    If ``idleTimeout`` is set to a time that is less than
    ``perRequestTimeout``, the connection will close when the
    ``idleTimeout`` is reached and not the ``perRequestTimeout``.
    """

    idleTimeoutSeconds: Duration | None
    perRequestTimeoutSeconds: Duration | None


class ServiceConnectTestTrafficHeaderMatchRules(TypedDict, total=False):
    """The header matching rules for test traffic routing in Amazon ECS
    blue/green deployments. These rules determine how incoming requests are
    matched based on HTTP headers to route test traffic to the new service
    revision.
    """

    exact: String


class ServiceConnectTestTrafficHeaderRules(TypedDict, total=False):
    """The HTTP header rules used to identify and route test traffic during
    Amazon ECS blue/green deployments. These rules specify which HTTP
    headers to examine and what values to match for routing decisions.

    For more information, see `Service Connect for Amazon ECS blue/green
    deployments <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-connect-blue-green.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    name: String
    value: ServiceConnectTestTrafficHeaderMatchRules | None


class ServiceConnectTestTrafficRules(TypedDict, total=False):
    """The test traffic routing configuration for Amazon ECS blue/green
    deployments. This configuration allows you to define rules for routing
    specific traffic to the new service revision during the deployment
    process, allowing for safe testing before full production traffic shift.

    For more information, see `Service Connect for Amazon ECS blue/green
    deployments <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-connect-blue-green.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    header: ServiceConnectTestTrafficHeaderRules


class ServiceConnectClientAlias(TypedDict, total=False):
    """Each alias ("endpoint") is a fully-qualified name and port number that
    other tasks ("clients") can use to connect to this service.

    Each name and port mapping must be unique within the namespace.

    Tasks that run in a namespace can use short names to connect to services
    in the namespace. Tasks can connect to services across all of the
    clusters in the namespace. Tasks connect through a managed proxy
    container that collects logs and metrics for increased visibility. Only
    the tasks that Amazon ECS services create are supported with Service
    Connect. For more information, see `Service
    Connect <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-connect.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    port: PortNumber
    dnsName: String | None
    testTrafficRules: ServiceConnectTestTrafficRules | None


ServiceConnectClientAliasList = list[ServiceConnectClientAlias]


class ServiceConnectService(TypedDict, total=False):
    """The Service Connect service object configuration. For more information,
    see `Service
    Connect <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-connect.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    portName: String
    discoveryName: String | None
    clientAliases: ServiceConnectClientAliasList | None
    ingressPortOverride: PortNumber | None
    timeout: TimeoutConfiguration | None
    tls: ServiceConnectTlsConfiguration | None


ServiceConnectServiceList = list[ServiceConnectService]


class ServiceConnectConfiguration(TypedDict, total=False):
    """The Service Connect configuration of your Amazon ECS service. The
    configuration for this service to discover and connect to services, and
    be discovered by, and connected from, other services within a namespace.

    Tasks that run in a namespace can use short names to connect to services
    in the namespace. Tasks can connect to services across all of the
    clusters in the namespace. Tasks connect through a managed proxy
    container that collects logs and metrics for increased visibility. Only
    the tasks that Amazon ECS services create are supported with Service
    Connect. For more information, see `Service
    Connect <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-connect.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    enabled: Boolean
    namespace: String | None
    services: ServiceConnectServiceList | None
    logConfiguration: LogConfiguration | None
    accessLogConfiguration: ServiceConnectAccessLogConfiguration | None


class DeploymentController(TypedDict, total=False):
    type: DeploymentControllerType


class NetworkConfiguration(TypedDict, total=False):
    """The network configuration for a task or service."""

    awsvpcConfiguration: AwsVpcConfiguration | None


class PlacementStrategy(TypedDict, total=False):
    type: PlacementStrategyType | None
    field: String | None


PlacementStrategies = list[PlacementStrategy]


class PlacementConstraint(TypedDict, total=False):
    type: PlacementConstraintType | None
    expression: String | None


PlacementConstraints = list[PlacementConstraint]


class LinearConfiguration(TypedDict, total=False):
    """Configuration for linear deployment strategy that shifts production
    traffic in equal percentage increments with configurable wait times
    between each step until 100% of traffic is shifted to the new service
    revision. This is only valid when you run ``CreateService`` or
    ``UpdateService`` with ``deploymentController`` set to ``ECS`` and a
    ``deploymentConfiguration`` with a strategy set to ``LINEAR``.
    """

    stepPercent: Double | None
    stepBakeTimeInMinutes: Integer | None


class HookDetails(TypedDict, total=False):
    pass


DeploymentLifecycleHookStageList = list[DeploymentLifecycleHookStage]


class DeploymentLifecycleHook(TypedDict, total=False):
    """A deployment lifecycle hook runs custom logic at specific stages of the
    deployment process. Currently, you can use Lambda functions as hook
    targets.

    For more information, see `Lifecycle hooks for Amazon ECS service
    deployments <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-lifecycle-hooks.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    hookTargetArn: String | None
    roleArn: IAMRoleArn | None
    lifecycleStages: DeploymentLifecycleHookStageList | None
    hookDetails: HookDetails | None


DeploymentLifecycleHookList = list[DeploymentLifecycleHook]


class DeploymentAlarms(TypedDict, total=False):
    """One of the methods which provide a way for you to quickly identify when
    a deployment has failed, and then to optionally roll back the failure to
    the last working deployment.

    When the alarms are generated, Amazon ECS sets the service deployment to
    failed. Set the rollback parameter to have Amazon ECS to roll back your
    service to the last completed deployment after a failure.

    You can only use the ``DeploymentAlarms`` method to detect failures when
    the ``DeploymentController`` is set to ``ECS``.

    For more information, see `Rolling
    update <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-ecs.html>`__
    in the *Amazon Elastic Container Service Developer Guide* .
    """

    alarmNames: StringList
    rollback: Boolean
    enable: Boolean


class DeploymentCircuitBreaker(TypedDict, total=False):
    """The deployment circuit breaker can only be used for services using the
    rolling update (``ECS``) deployment type.

    The **deployment circuit breaker** determines whether a service
    deployment will fail if the service can't reach a steady state. If it is
    turned on, a service deployment will transition to a failed state and
    stop launching new tasks. You can also configure Amazon ECS to roll back
    your service to the last completed deployment after a failure. For more
    information, see `Rolling
    update <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-ecs.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.

    For more information about API failure reasons, see `API failure
    reasons <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/api_failures_messages.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    enable: Boolean
    rollback: Boolean


class DeploymentConfiguration(TypedDict, total=False):
    """Optional deployment parameters that control how many tasks run during a
    deployment and the ordering of stopping and starting tasks.
    """

    deploymentCircuitBreaker: DeploymentCircuitBreaker | None
    maximumPercent: BoxedInteger | None
    minimumHealthyPercent: BoxedInteger | None
    alarms: DeploymentAlarms | None
    strategy: DeploymentStrategy | None
    bakeTimeInMinutes: BoxedInteger | None
    lifecycleHooks: DeploymentLifecycleHookList | None
    linearConfiguration: LinearConfiguration | None
    canaryConfiguration: CanaryConfiguration | None


class ServiceRegistry(TypedDict, total=False):
    """The details for the service registry.

    Each service may be associated with one service registry. Multiple
    service registries for each service are not supported.

    When you add, update, or remove the service registries configuration,
    Amazon ECS starts a new deployment. New tasks are registered and
    deregistered to the updated service registry configuration.
    """

    registryArn: String | None
    port: BoxedInteger | None
    containerName: String | None
    containerPort: BoxedInteger | None


ServiceRegistries = list[ServiceRegistry]


class LoadBalancer(TypedDict, total=False):
    """The load balancer configuration to use with a service or task set.

    When you add, update, or remove a load balancer configuration, Amazon
    ECS starts a new deployment with the updated Elastic Load Balancing
    configuration. This causes tasks to register to and deregister from load
    balancers.

    We recommend that you verify this on a test environment before you
    update the Elastic Load Balancing configuration.

    A service-linked role is required for services that use multiple target
    groups. For more information, see `Using service-linked
    roles <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using-service-linked-roles.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    targetGroupArn: String | None
    loadBalancerName: String | None
    containerName: String | None
    containerPort: BoxedInteger | None
    advancedConfiguration: AdvancedConfiguration | None


LoadBalancers = list[LoadBalancer]


class CreateServiceRequest(ServiceRequest):
    cluster: String | None
    serviceName: String
    taskDefinition: String | None
    availabilityZoneRebalancing: AvailabilityZoneRebalancing | None
    loadBalancers: LoadBalancers | None
    serviceRegistries: ServiceRegistries | None
    desiredCount: BoxedInteger | None
    clientToken: String | None
    launchType: LaunchType | None
    capacityProviderStrategy: CapacityProviderStrategy | None
    platformVersion: String | None
    role: String | None
    deploymentConfiguration: DeploymentConfiguration | None
    placementConstraints: PlacementConstraints | None
    placementStrategy: PlacementStrategies | None
    networkConfiguration: NetworkConfiguration | None
    healthCheckGracePeriodSeconds: BoxedInteger | None
    schedulingStrategy: SchedulingStrategy | None
    deploymentController: DeploymentController | None
    tags: Tags | None
    enableECSManagedTags: Boolean | None
    propagateTags: PropagateTags | None
    enableExecuteCommand: Boolean | None
    serviceConnectConfiguration: ServiceConnectConfiguration | None
    volumeConfigurations: ServiceVolumeConfigurations | None
    vpcLatticeConfigurations: VpcLatticeConfigurations | None


class ServiceCurrentRevisionSummary(TypedDict, total=False):
    """The summary of the current service revision configuration"""

    arn: String | None
    requestedTaskCount: Integer | None
    runningTaskCount: Integer | None
    pendingTaskCount: Integer | None


ServiceCurrentRevisionSummaryList = list[ServiceCurrentRevisionSummary]


class ServiceEvent(TypedDict, total=False):
    """The details for an event that's associated with a service."""

    id: String | None
    createdAt: Timestamp | None
    message: String | None


ServiceEvents = list[ServiceEvent]


class DeploymentEphemeralStorage(TypedDict, total=False):
    """The amount of ephemeral storage to allocate for the deployment."""

    kmsKeyId: String | None


class ServiceConnectServiceResource(TypedDict, total=False):
    """The Service Connect resource. Each configuration maps a discovery name
    to a Cloud Map service name. The data is stored in Cloud Map as part of
    the Service Connect configuration for each discovery name of this Amazon
    ECS service.

    A task can resolve the ``dnsName`` for each of the ``clientAliases`` of
    a service. However a task can't resolve the discovery names. If you want
    to connect to a service, refer to the ``ServiceConnectConfiguration`` of
    that service for the list of ``clientAliases`` that you can use.
    """

    discoveryName: String | None
    discoveryArn: String | None


ServiceConnectServiceResourceList = list[ServiceConnectServiceResource]


class Deployment(TypedDict, total=False):
    """The details of an Amazon ECS service deployment. This is used only when
    a service uses the ``ECS`` deployment controller type.
    """

    id: String | None
    status: String | None
    taskDefinition: String | None
    desiredCount: Integer | None
    pendingCount: Integer | None
    runningCount: Integer | None
    failedTasks: Integer | None
    createdAt: Timestamp | None
    updatedAt: Timestamp | None
    capacityProviderStrategy: CapacityProviderStrategy | None
    launchType: LaunchType | None
    platformVersion: String | None
    platformFamily: String | None
    networkConfiguration: NetworkConfiguration | None
    rolloutState: DeploymentRolloutState | None
    rolloutStateReason: String | None
    serviceConnectConfiguration: ServiceConnectConfiguration | None
    serviceConnectResources: ServiceConnectServiceResourceList | None
    volumeConfigurations: ServiceVolumeConfigurations | None
    fargateEphemeralStorage: DeploymentEphemeralStorage | None
    vpcLatticeConfigurations: VpcLatticeConfigurations | None


Deployments = list[Deployment]


class Scale(TypedDict, total=False):
    """A floating-point percentage of the desired number of tasks to place and
    keep running in the task set.
    """

    value: Double | None
    unit: ScaleUnit | None


class TaskSet(TypedDict, total=False):
    """Information about a set of Amazon ECS tasks in either an CodeDeploy or
    an ``EXTERNAL`` deployment. An Amazon ECS task set includes details such
    as the desired number of tasks, how many tasks are running, and whether
    the task set serves production traffic.
    """

    id: String | None
    taskSetArn: String | None
    serviceArn: String | None
    clusterArn: String | None
    startedBy: String | None
    externalId: String | None
    status: String | None
    taskDefinition: String | None
    computedDesiredCount: Integer | None
    pendingCount: Integer | None
    runningCount: Integer | None
    createdAt: Timestamp | None
    updatedAt: Timestamp | None
    launchType: LaunchType | None
    capacityProviderStrategy: CapacityProviderStrategy | None
    platformVersion: String | None
    platformFamily: String | None
    networkConfiguration: NetworkConfiguration | None
    loadBalancers: LoadBalancers | None
    serviceRegistries: ServiceRegistries | None
    scale: Scale | None
    stabilityStatus: StabilityStatus | None
    stabilityStatusAt: Timestamp | None
    tags: Tags | None
    fargateEphemeralStorage: DeploymentEphemeralStorage | None


TaskSets = list[TaskSet]


class Service(TypedDict, total=False):
    """Details on a service within a cluster."""

    serviceArn: String | None
    serviceName: String | None
    clusterArn: String | None
    loadBalancers: LoadBalancers | None
    serviceRegistries: ServiceRegistries | None
    status: String | None
    desiredCount: Integer | None
    runningCount: Integer | None
    pendingCount: Integer | None
    launchType: LaunchType | None
    capacityProviderStrategy: CapacityProviderStrategy | None
    platformVersion: String | None
    platformFamily: String | None
    taskDefinition: String | None
    deploymentConfiguration: DeploymentConfiguration | None
    taskSets: TaskSets | None
    deployments: Deployments | None
    roleArn: String | None
    events: ServiceEvents | None
    createdAt: Timestamp | None
    currentServiceDeployment: String | None
    currentServiceRevisions: ServiceCurrentRevisionSummaryList | None
    placementConstraints: PlacementConstraints | None
    placementStrategy: PlacementStrategies | None
    networkConfiguration: NetworkConfiguration | None
    healthCheckGracePeriodSeconds: BoxedInteger | None
    schedulingStrategy: SchedulingStrategy | None
    deploymentController: DeploymentController | None
    tags: Tags | None
    createdBy: String | None
    enableECSManagedTags: Boolean | None
    propagateTags: PropagateTags | None
    enableExecuteCommand: Boolean | None
    availabilityZoneRebalancing: AvailabilityZoneRebalancing | None
    resourceManagementType: ResourceManagementType | None


class CreateServiceResponse(TypedDict, total=False):
    service: Service | None


class CreateTaskSetRequest(ServiceRequest):
    service: String
    cluster: String
    externalId: String | None
    taskDefinition: String
    networkConfiguration: NetworkConfiguration | None
    loadBalancers: LoadBalancers | None
    serviceRegistries: ServiceRegistries | None
    launchType: LaunchType | None
    capacityProviderStrategy: CapacityProviderStrategy | None
    platformVersion: String | None
    scale: Scale | None
    clientToken: String | None
    tags: Tags | None


class CreateTaskSetResponse(TypedDict, total=False):
    taskSet: TaskSet | None


class CreatedAt(TypedDict, total=False):
    """The optional filter to narrow the ``ListServiceDeployment`` results.

    If you do not specify a value, service deployments that were created
    before the current time are included in the result.
    """

    before: Timestamp | None
    after: Timestamp | None


class DeleteAccountSettingRequest(ServiceRequest):
    name: SettingName
    principalArn: String | None


class Setting(TypedDict, total=False):
    name: SettingName | None
    value: String | None
    principalArn: String | None
    type: SettingType | None


class DeleteAccountSettingResponse(TypedDict, total=False):
    setting: Setting | None


class DeleteAttributesRequest(ServiceRequest):
    cluster: String | None
    attributes: Attributes


class DeleteAttributesResponse(TypedDict, total=False):
    attributes: Attributes | None


class DeleteCapacityProviderRequest(ServiceRequest):
    capacityProvider: String
    cluster: String | None


class DeleteCapacityProviderResponse(TypedDict, total=False):
    capacityProvider: CapacityProvider | None


class DeleteClusterRequest(ServiceRequest):
    cluster: String


class DeleteClusterResponse(TypedDict, total=False):
    cluster: Cluster | None


class DeleteExpressGatewayServiceRequest(ServiceRequest):
    serviceArn: String


class DeleteExpressGatewayServiceResponse(TypedDict, total=False):
    service: ECSExpressGatewayService | None


class DeleteServiceRequest(ServiceRequest):
    cluster: String | None
    service: String
    force: BoxedBoolean | None


class DeleteServiceResponse(TypedDict, total=False):
    service: Service | None


class DeleteTaskDefinitionsRequest(ServiceRequest):
    taskDefinitions: StringList


class Failure(TypedDict, total=False):
    """A failed resource. For a list of common causes, see `API failure
    reasons <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/api_failures_messages.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    arn: String | None
    reason: String | None
    detail: String | None


Failures = list[Failure]


class EphemeralStorage(TypedDict, total=False):
    """The amount of ephemeral storage to allocate for the task. This parameter
    is used to expand the total amount of ephemeral storage available,
    beyond the default amount, for tasks hosted on Fargate. For more
    information, see `Using data volumes in
    tasks <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_data_volumes.html>`__
    in the *Amazon ECS Developer Guide;*.

    For tasks using the Fargate launch type, the task requires the following
    platforms:

    -  Linux platform version ``1.4.0`` or later.

    -  Windows platform version ``1.0.0`` or later.
    """

    sizeInGiB: Integer


ProxyConfigurationProperties = list[KeyValuePair]


class ProxyConfiguration(TypedDict, total=False):
    type: ProxyConfigurationType | None
    containerName: String
    properties: ProxyConfigurationProperties | None


class InferenceAccelerator(TypedDict, total=False):
    """Details on an Elastic Inference accelerator. For more information, see
    `Working with Amazon Elastic Inference on Amazon
    ECS <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-inference.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    deviceName: String
    deviceType: String


InferenceAccelerators = list[InferenceAccelerator]


class RuntimePlatform(TypedDict, total=False):
    """Information about the platform for the Amazon ECS service or task.

    For more information about ``RuntimePlatform``, see
    `RuntimePlatform <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html#runtime-platform>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    cpuArchitecture: CPUArchitecture | None
    operatingSystemFamily: OSFamily | None


class TaskDefinitionPlacementConstraint(TypedDict, total=False):
    type: TaskDefinitionPlacementConstraintType | None
    expression: String | None


TaskDefinitionPlacementConstraints = list[TaskDefinitionPlacementConstraint]
RequiresAttributes = list[Attribute]


class FSxWindowsFileServerAuthorizationConfig(TypedDict, total=False):
    """The authorization configuration details for Amazon FSx for Windows File
    Server file system. See
    `FSxWindowsFileServerVolumeConfiguration <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_FSxWindowsFileServerVolumeConfiguration.html>`__
    in the *Amazon ECS API Reference*.

    For more information and the input format, see `Amazon FSx for Windows
    File Server
    Volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/wfsx-volumes.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    credentialsParameter: String
    domain: String


class FSxWindowsFileServerVolumeConfiguration(TypedDict, total=False):
    """This parameter is specified when you're using `Amazon FSx for Windows
    File
    Server <https://docs.aws.amazon.com/fsx/latest/WindowsGuide/what-is.html>`__
    file system for task storage.

    For more information and the input format, see `Amazon FSx for Windows
    File Server
    volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/wfsx-volumes.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    fileSystemId: String
    rootDirectory: String
    authorizationConfig: FSxWindowsFileServerAuthorizationConfig


class EFSAuthorizationConfig(TypedDict, total=False):
    """The authorization configuration details for the Amazon EFS file system."""

    accessPointId: String | None
    iam: EFSAuthorizationConfigIAM | None


class EFSVolumeConfiguration(TypedDict, total=False):
    """This parameter is specified when you're using an Amazon Elastic File
    System file system for task storage. For more information, see `Amazon
    EFS
    volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/efs-volumes.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    fileSystemId: String
    rootDirectory: String | None
    transitEncryption: EFSTransitEncryption | None
    transitEncryptionPort: BoxedInteger | None
    authorizationConfig: EFSAuthorizationConfig | None


StringMap = dict[String, String]


class DockerVolumeConfiguration(TypedDict, total=False):
    """This parameter is specified when you're using Docker volumes. Docker
    volumes are only supported when you're using the EC2 launch type.
    Windows containers only support the use of the ``local`` driver. To use
    bind mounts, specify a ``host`` instead.
    """

    scope: Scope | None
    autoprovision: BoxedBoolean | None
    driver: String | None
    driverOpts: StringMap | None
    labels: StringMap | None


class HostVolumeProperties(TypedDict, total=False):
    """Details on a container instance bind mount host volume."""

    sourcePath: String | None


class Volume(TypedDict, total=False):
    """The data volume configuration for tasks launched using this task
    definition. Specifying a volume configuration in a task definition is
    optional. The volume configuration may contain multiple volumes but only
    one volume configured at launch is supported. Each volume defined in the
    volume configuration may only specify a ``name`` and one of either
    ``configuredAtLaunch``, ``dockerVolumeConfiguration``,
    ``efsVolumeConfiguration``, ``fsxWindowsFileServerVolumeConfiguration``,
    or ``host``. If an empty volume configuration is specified, by default
    Amazon ECS uses a host volume. For more information, see `Using data
    volumes in
    tasks <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_data_volumes.html>`__.
    """

    name: String | None
    host: HostVolumeProperties | None
    dockerVolumeConfiguration: DockerVolumeConfiguration | None
    efsVolumeConfiguration: EFSVolumeConfiguration | None
    fsxWindowsFileServerVolumeConfiguration: FSxWindowsFileServerVolumeConfiguration | None
    configuredAtLaunch: BoxedBoolean | None


VolumeList = list[Volume]


class TaskDefinition(TypedDict, total=False):
    """The details of a task definition which describes the container and
    volume definitions of an Amazon Elastic Container Service task. You can
    specify which Docker images to use, the required resources, and other
    configurations related to launching the task definition through an
    Amazon ECS service or task.
    """

    taskDefinitionArn: String | None
    containerDefinitions: ContainerDefinitions | None
    family: String | None
    taskRoleArn: String | None
    executionRoleArn: String | None
    networkMode: NetworkMode | None
    revision: Integer | None
    volumes: VolumeList | None
    status: TaskDefinitionStatus | None
    requiresAttributes: RequiresAttributes | None
    placementConstraints: TaskDefinitionPlacementConstraints | None
    compatibilities: CompatibilityList | None
    runtimePlatform: RuntimePlatform | None
    requiresCompatibilities: CompatibilityList | None
    cpu: String | None
    memory: String | None
    inferenceAccelerators: InferenceAccelerators | None
    pidMode: PidMode | None
    ipcMode: IpcMode | None
    proxyConfiguration: ProxyConfiguration | None
    registeredAt: Timestamp | None
    deregisteredAt: Timestamp | None
    registeredBy: String | None
    ephemeralStorage: EphemeralStorage | None
    enableFaultInjection: BoxedBoolean | None


TaskDefinitionList = list[TaskDefinition]


class DeleteTaskDefinitionsResponse(TypedDict, total=False):
    taskDefinitions: TaskDefinitionList | None
    failures: Failures | None


class DeleteTaskSetRequest(ServiceRequest):
    cluster: String
    service: String
    taskSet: String
    force: BoxedBoolean | None


class DeleteTaskSetResponse(TypedDict, total=False):
    taskSet: TaskSet | None


class DeregisterContainerInstanceRequest(ServiceRequest):
    cluster: String | None
    containerInstance: String
    force: BoxedBoolean | None


class DeregisterContainerInstanceResponse(TypedDict, total=False):
    containerInstance: ContainerInstance | None


class DeregisterTaskDefinitionRequest(ServiceRequest):
    taskDefinition: String


class DeregisterTaskDefinitionResponse(TypedDict, total=False):
    taskDefinition: TaskDefinition | None


class DescribeCapacityProvidersRequest(ServiceRequest):
    capacityProviders: StringList | None
    cluster: String | None
    include: CapacityProviderFieldList | None
    maxResults: BoxedInteger | None
    nextToken: String | None


class DescribeCapacityProvidersResponse(TypedDict, total=False):
    capacityProviders: CapacityProviders | None
    failures: Failures | None
    nextToken: String | None


class DescribeClustersRequest(ServiceRequest):
    clusters: StringList | None
    include: ClusterFieldList | None


class DescribeClustersResponse(TypedDict, total=False):
    clusters: Clusters | None
    failures: Failures | None


class DescribeContainerInstancesRequest(ServiceRequest):
    cluster: String | None
    containerInstances: StringList
    include: ContainerInstanceFieldList | None


class DescribeContainerInstancesResponse(TypedDict, total=False):
    containerInstances: ContainerInstances | None
    failures: Failures | None


ExpressGatewayServiceIncludeList = list[ExpressGatewayServiceInclude]


class DescribeExpressGatewayServiceRequest(ServiceRequest):
    serviceArn: String
    include: ExpressGatewayServiceIncludeList | None


class DescribeExpressGatewayServiceResponse(TypedDict, total=False):
    service: ECSExpressGatewayService | None


class DescribeServiceDeploymentsRequest(ServiceRequest):
    serviceDeploymentArns: StringList


class ServiceDeploymentAlarms(TypedDict, total=False):
    """The CloudWatch alarms used to determine a service deployment failed.

    Amazon ECS considers the service deployment as failed when any of the
    alarms move to the ``ALARM`` state. For more information, see `How
    CloudWatch alarms detect Amazon ECS deployment
    failures <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-alarm-failure.html>`__
    in the Amazon ECS Developer Guide.
    """

    status: ServiceDeploymentRollbackMonitorsStatus | None
    alarmNames: StringList | None
    triggeredAlarmNames: StringList | None


class ServiceDeploymentCircuitBreaker(TypedDict, total=False):
    """Information about the circuit breaker used to determine when a service
    deployment has failed.

    The deployment circuit breaker is the rolling update mechanism that
    determines if the tasks reach a steady state. The deployment circuit
    breaker has an option that will automatically roll back a failed
    deployment to the last cpompleted service revision. For more
    information, see `How the Amazon ECS deployment circuit breaker detects
    failures <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-circuit-breaker.html>`__
    in the *Amazon ECS Developer Guide*.
    """

    status: ServiceDeploymentRollbackMonitorsStatus | None
    failureCount: Integer | None
    threshold: Integer | None


class Rollback(TypedDict, total=False):
    """Information about the service deployment rollback."""

    reason: String | None
    startedAt: Timestamp | None
    serviceRevisionArn: String | None


class ServiceRevisionSummary(TypedDict, total=False):
    """The information about the number of requested, pending, and running
    tasks for a service revision.
    """

    arn: String | None
    requestedTaskCount: Integer | None
    runningTaskCount: Integer | None
    pendingTaskCount: Integer | None
    requestedTestTrafficWeight: Double | None
    requestedProductionTrafficWeight: Double | None


ServiceRevisionsSummaryList = list[ServiceRevisionSummary]


class ServiceDeployment(TypedDict, total=False):
    """Information about the service deployment.

    Service deployments provide a comprehensive view of your deployments.
    For information about service deployments, see `View service history
    using Amazon ECS service
    deployments <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-deployment.html>`__
    in the *Amazon Elastic Container Service Developer Guide* .
    """

    serviceDeploymentArn: String | None
    serviceArn: String | None
    clusterArn: String | None
    createdAt: Timestamp | None
    startedAt: Timestamp | None
    finishedAt: Timestamp | None
    stoppedAt: Timestamp | None
    updatedAt: Timestamp | None
    sourceServiceRevisions: ServiceRevisionsSummaryList | None
    targetServiceRevision: ServiceRevisionSummary | None
    status: ServiceDeploymentStatus | None
    statusReason: String | None
    lifecycleStage: ServiceDeploymentLifecycleStage | None
    deploymentConfiguration: DeploymentConfiguration | None
    rollback: Rollback | None
    deploymentCircuitBreaker: ServiceDeploymentCircuitBreaker | None
    alarms: ServiceDeploymentAlarms | None


ServiceDeployments = list[ServiceDeployment]


class DescribeServiceDeploymentsResponse(TypedDict, total=False):
    serviceDeployments: ServiceDeployments | None
    failures: Failures | None


class DescribeServiceRevisionsRequest(ServiceRequest):
    serviceRevisionArns: StringList


class ManagedLogGroup(TypedDict, total=False):
    """The Cloudwatch Log Group created by Amazon ECS for an Express service."""

    arn: String | None
    status: ManagedResourceStatus
    statusReason: String | None
    updatedAt: Timestamp
    logGroupName: String


ManagedLogGroups = list[ManagedLogGroup]


class ManagedSecurityGroup(TypedDict, total=False):
    """A security group associated with the Express service."""

    arn: String | None
    status: ManagedResourceStatus
    statusReason: String | None
    updatedAt: Timestamp


ManagedSecurityGroups = list[ManagedSecurityGroup]


class ManagedMetricAlarm(TypedDict, total=False):
    """The CloudWatch metric alarm associated with the Express service's
    scaling policy.
    """

    arn: String | None
    status: ManagedResourceStatus
    statusReason: String | None
    updatedAt: Timestamp


ManagedMetricAlarms = list[ManagedMetricAlarm]


class ManagedApplicationAutoScalingPolicy(TypedDict, total=False):
    """The Application Auto Scaling policy created by Amazon ECS when you
    create an Express service.
    """

    arn: String | None
    status: ManagedResourceStatus
    statusReason: String | None
    updatedAt: Timestamp
    policyType: String
    targetValue: Double
    metric: String


ManagedApplicationAutoScalingPolicies = list[ManagedApplicationAutoScalingPolicy]


class ManagedScalableTarget(TypedDict, total=False):
    """Represents a scalable target."""

    arn: String | None
    status: ManagedResourceStatus
    statusReason: String | None
    updatedAt: Timestamp
    minCapacity: Integer
    maxCapacity: Integer


class ManagedAutoScaling(TypedDict, total=False):
    """The auto scaling configuration created by Amazon ECS for an Express
    service.
    """

    scalableTarget: ManagedScalableTarget | None
    applicationAutoScalingPolicies: ManagedApplicationAutoScalingPolicies | None


class ManagedTargetGroup(TypedDict, total=False):
    """The target group associated with the Express service's Application Load
    Balancer. For more information about load balancer target groups, see
    `CreateTargetGroup <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_CreateTargetGroup.html>`__
    in the *Elastic Load Balancing API Reference*
    """

    arn: String | None
    status: ManagedResourceStatus
    statusReason: String | None
    updatedAt: Timestamp
    healthCheckPath: String
    healthCheckPort: Integer
    port: Integer


ManagedTargetGroups = list[ManagedTargetGroup]


class ManagedListenerRule(TypedDict, total=False):
    """The listener rule associated with the Express service's Application Load
    Balancer.
    """

    arn: String | None
    status: ManagedResourceStatus
    statusReason: String | None
    updatedAt: Timestamp


class ManagedListener(TypedDict, total=False):
    """The listeners associated with the Express service's Application Load
    Balancer.
    """

    arn: String | None
    status: ManagedResourceStatus
    statusReason: String | None
    updatedAt: Timestamp


class ManagedCertificate(TypedDict, total=False):
    """The ACM certificate associated with the HTTPS domain created for the
    Express service.
    """

    arn: String | None
    status: ManagedResourceStatus
    statusReason: String | None
    updatedAt: Timestamp
    domainName: String


class ManagedLoadBalancer(TypedDict, total=False):
    """The Application Load Balancer associated with the Express service."""

    arn: String | None
    status: ManagedResourceStatus
    statusReason: String | None
    updatedAt: Timestamp
    scheme: String
    subnetIds: StringList | None
    securityGroupIds: StringList | None


class ManagedIngressPath(TypedDict, total=False):
    """The entry point into the Express service."""

    accessType: AccessType
    endpoint: String
    loadBalancer: ManagedLoadBalancer | None
    loadBalancerSecurityGroups: ManagedSecurityGroups | None
    certificate: ManagedCertificate | None
    listener: ManagedListener | None
    rule: ManagedListenerRule | None
    targetGroups: ManagedTargetGroups | None


ManagedIngressPaths = list[ManagedIngressPath]


class ECSManagedResources(TypedDict, total=False):
    """Represents the Amazon Web Services resources managed by Amazon ECS for
    an Express service, including ingress paths, auto-scaling policies,
    metric alarms, and security groups.
    """

    ingressPaths: ManagedIngressPaths | None
    autoScaling: ManagedAutoScaling | None
    metricAlarms: ManagedMetricAlarms | None
    serviceSecurityGroups: ManagedSecurityGroups | None
    logGroups: ManagedLogGroups | None


class ServiceRevisionLoadBalancer(TypedDict, total=False):
    """The resolved load balancer configuration for a service revision. This
    includes information about which target groups serve traffic and which
    listener rules direct traffic to them.
    """

    targetGroupArn: String | None
    productionListenerRule: String | None


ServiceRevisionLoadBalancers = list[ServiceRevisionLoadBalancer]


class ResolvedConfiguration(TypedDict, total=False):
    """The resolved configuration for a service revision, which contains the
    actual resources your service revision uses, such as which target groups
    serve traffic.
    """

    loadBalancers: ServiceRevisionLoadBalancers | None


class ServiceRevision(TypedDict, total=False):
    """Information about the service revision.

    A service revision contains a record of the workload configuration
    Amazon ECS is attempting to deploy. Whenever you create or deploy a
    service, Amazon ECS automatically creates and captures the configuration
    that you're trying to deploy in the service revision. For information
    about service revisions, see `Amazon ECS service
    revisions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-revision.html>`__
    in the *Amazon Elastic Container Service Developer Guide* .
    """

    serviceRevisionArn: String | None
    serviceArn: String | None
    clusterArn: String | None
    taskDefinition: String | None
    capacityProviderStrategy: CapacityProviderStrategy | None
    launchType: LaunchType | None
    platformVersion: String | None
    platformFamily: String | None
    loadBalancers: LoadBalancers | None
    serviceRegistries: ServiceRegistries | None
    networkConfiguration: NetworkConfiguration | None
    containerImages: ContainerImages | None
    guardDutyEnabled: Boolean | None
    serviceConnectConfiguration: ServiceConnectConfiguration | None
    volumeConfigurations: ServiceVolumeConfigurations | None
    fargateEphemeralStorage: DeploymentEphemeralStorage | None
    createdAt: Timestamp | None
    vpcLatticeConfigurations: VpcLatticeConfigurations | None
    resolvedConfiguration: ResolvedConfiguration | None
    ecsManagedResources: ECSManagedResources | None


ServiceRevisions = list[ServiceRevision]


class DescribeServiceRevisionsResponse(TypedDict, total=False):
    serviceRevisions: ServiceRevisions | None
    failures: Failures | None


ServiceFieldList = list[ServiceField]


class DescribeServicesRequest(ServiceRequest):
    cluster: String | None
    services: StringList
    include: ServiceFieldList | None


Services = list[Service]


class DescribeServicesResponse(TypedDict, total=False):
    services: Services | None
    failures: Failures | None


TaskDefinitionFieldList = list[TaskDefinitionField]


class DescribeTaskDefinitionRequest(ServiceRequest):
    taskDefinition: String
    include: TaskDefinitionFieldList | None


class DescribeTaskDefinitionResponse(TypedDict, total=False):
    taskDefinition: TaskDefinition | None
    tags: Tags | None


TaskSetFieldList = list[TaskSetField]


class DescribeTaskSetsRequest(ServiceRequest):
    cluster: String
    service: String
    taskSets: StringList | None
    include: TaskSetFieldList | None


class DescribeTaskSetsResponse(TypedDict, total=False):
    taskSets: TaskSets | None
    failures: Failures | None


TaskFieldList = list[TaskField]


class DescribeTasksRequest(ServiceRequest):
    cluster: String | None
    tasks: StringList
    include: TaskFieldList | None


class TaskEphemeralStorage(TypedDict, total=False):
    """The amount of ephemeral storage to allocate for the task."""

    sizeInGiB: Integer | None
    kmsKeyId: String | None


class InferenceAcceleratorOverride(TypedDict, total=False):
    """Details on an Elastic Inference accelerator task override. This
    parameter is used to override the Elastic Inference accelerator
    specified in the task definition. For more information, see `Working
    with Amazon Elastic Inference on Amazon
    ECS <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-inference.html>`__
    in the *Amazon Elastic Container Service Developer Guide*.
    """

    deviceName: String | None
    deviceType: String | None


InferenceAcceleratorOverrides = list[InferenceAcceleratorOverride]


class TaskOverride(TypedDict, total=False):
    """The overrides that are associated with a task."""

    containerOverrides: ContainerOverrides | None
    cpu: String | None
    inferenceAcceleratorOverrides: InferenceAcceleratorOverrides | None
    executionRoleArn: String | None
    memory: String | None
    taskRoleArn: String | None
    ephemeralStorage: EphemeralStorage | None


class Task(TypedDict, total=False):
    """Details on a task in a cluster."""

    attachments: Attachments | None
    attributes: Attributes | None
    availabilityZone: String | None
    capacityProviderName: String | None
    clusterArn: String | None
    connectivity: Connectivity | None
    connectivityAt: Timestamp | None
    containerInstanceArn: String | None
    containers: Containers | None
    cpu: String | None
    createdAt: Timestamp | None
    desiredStatus: String | None
    enableExecuteCommand: Boolean | None
    executionStoppedAt: Timestamp | None
    group: String | None
    healthStatus: HealthStatus | None
    inferenceAccelerators: InferenceAccelerators | None
    lastStatus: String | None
    launchType: LaunchType | None
    memory: String | None
    overrides: TaskOverride | None
    platformVersion: String | None
    platformFamily: String | None
    pullStartedAt: Timestamp | None
    pullStoppedAt: Timestamp | None
    startedAt: Timestamp | None
    startedBy: String | None
    stopCode: TaskStopCode | None
    stoppedAt: Timestamp | None
    stoppedReason: String | None
    stoppingAt: Timestamp | None
    tags: Tags | None
    taskArn: String | None
    taskDefinitionArn: String | None
    version: Long | None
    ephemeralStorage: EphemeralStorage | None
    fargateEphemeralStorage: TaskEphemeralStorage | None


Tasks = list[Task]


class DescribeTasksResponse(TypedDict, total=False):
    tasks: Tasks | None
    failures: Failures | None


class DiscoverPollEndpointRequest(ServiceRequest):
    containerInstance: String | None
    cluster: String | None


class DiscoverPollEndpointResponse(TypedDict, total=False):
    endpoint: String | None
    telemetryEndpoint: String | None
    serviceConnectEndpoint: String | None


class ExecuteCommandRequest(ServiceRequest):
    cluster: String | None
    container: String | None
    command: String
    interactive: Boolean
    task: String


class Session(TypedDict, total=False):
    """The details for the execute command session."""

    sessionId: String | None
    streamUrl: String | None
    tokenValue: SensitiveString | None


class ExecuteCommandResponse(TypedDict, total=False):
    clusterArn: String | None
    containerArn: String | None
    containerName: String | None
    interactive: Boolean | None
    session: Session | None
    taskArn: String | None


class GetTaskProtectionRequest(ServiceRequest):
    cluster: String
    tasks: StringList | None


class ProtectedTask(TypedDict, total=False):
    """An object representing the protection status details for a task. You can
    set the protection status with the
    `UpdateTaskProtection <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_UpdateTaskProtection.html>`__
    API and get the status of tasks with the
    `GetTaskProtection <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_GetTaskProtection.html>`__
    API.
    """

    taskArn: String | None
    protectionEnabled: Boolean | None
    expirationDate: Timestamp | None


ProtectedTasks = list[ProtectedTask]


class GetTaskProtectionResponse(TypedDict, total=False):
    protectedTasks: ProtectedTasks | None
    failures: Failures | None


class InstanceLaunchTemplateUpdate(TypedDict, total=False):
    """The updated launch template configuration for Amazon ECS Managed
    Instances. You can modify the instance profile, network configuration,
    storage settings, and instance requirements. Changes apply to new
    instances launched after the update.

    For more information, see `Store instance launch parameters in Amazon
    EC2 launch
    templates <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-launch-templates.html>`__
    in the *Amazon EC2 User Guide*.
    """

    ec2InstanceProfileArn: String | None
    networkConfiguration: ManagedInstancesNetworkConfiguration | None
    storageConfiguration: ManagedInstancesStorageConfiguration | None
    monitoring: ManagedInstancesMonitoringOptions | None
    instanceRequirements: InstanceRequirementsRequest | None


class ListAccountSettingsRequest(ServiceRequest):
    name: SettingName | None
    value: String | None
    principalArn: String | None
    effectiveSettings: Boolean | None
    nextToken: String | None
    maxResults: Integer | None


Settings = list[Setting]


class ListAccountSettingsResponse(TypedDict, total=False):
    settings: Settings | None
    nextToken: String | None


class ListAttributesRequest(ServiceRequest):
    cluster: String | None
    targetType: TargetType
    attributeName: String | None
    attributeValue: String | None
    nextToken: String | None
    maxResults: BoxedInteger | None


class ListAttributesResponse(TypedDict, total=False):
    attributes: Attributes | None
    nextToken: String | None


class ListClustersRequest(ServiceRequest):
    nextToken: String | None
    maxResults: BoxedInteger | None


class ListClustersResponse(TypedDict, total=False):
    clusterArns: StringList | None
    nextToken: String | None


class ListContainerInstancesRequest(ServiceRequest):
    cluster: String | None
    filter: String | None
    nextToken: String | None
    maxResults: BoxedInteger | None
    status: ContainerInstanceStatus | None


class ListContainerInstancesResponse(TypedDict, total=False):
    containerInstanceArns: StringList | None
    nextToken: String | None


ServiceDeploymentStatusList = list[ServiceDeploymentStatus]


class ListServiceDeploymentsRequest(ServiceRequest):
    service: String
    cluster: String | None
    status: ServiceDeploymentStatusList | None
    createdAt: CreatedAt | None
    nextToken: String | None
    maxResults: BoxedInteger | None


class ServiceDeploymentBrief(TypedDict, total=False):
    """The service deployment properties that are retured when you call
    ``ListServiceDeployments``.

    This provides a high-level overview of the service deployment.
    """

    serviceDeploymentArn: String | None
    serviceArn: String | None
    clusterArn: String | None
    startedAt: Timestamp | None
    createdAt: Timestamp | None
    finishedAt: Timestamp | None
    targetServiceRevisionArn: String | None
    status: ServiceDeploymentStatus | None
    statusReason: String | None


ServiceDeploymentsBrief = list[ServiceDeploymentBrief]


class ListServiceDeploymentsResponse(TypedDict, total=False):
    serviceDeployments: ServiceDeploymentsBrief | None
    nextToken: String | None


class ListServicesByNamespaceRequest(ServiceRequest):
    namespace: String
    nextToken: String | None
    maxResults: BoxedInteger | None


class ListServicesByNamespaceResponse(TypedDict, total=False):
    serviceArns: StringList | None
    nextToken: String | None


class ListServicesRequest(ServiceRequest):
    cluster: String | None
    nextToken: String | None
    maxResults: BoxedInteger | None
    launchType: LaunchType | None
    schedulingStrategy: SchedulingStrategy | None
    resourceManagementType: ResourceManagementType | None


class ListServicesResponse(TypedDict, total=False):
    serviceArns: StringList | None
    nextToken: String | None


class ListTagsForResourceRequest(ServiceRequest):
    resourceArn: String


class ListTagsForResourceResponse(TypedDict, total=False):
    tags: Tags | None


class ListTaskDefinitionFamiliesRequest(ServiceRequest):
    familyPrefix: String | None
    status: TaskDefinitionFamilyStatus | None
    nextToken: String | None
    maxResults: BoxedInteger | None


class ListTaskDefinitionFamiliesResponse(TypedDict, total=False):
    families: StringList | None
    nextToken: String | None


class ListTaskDefinitionsRequest(ServiceRequest):
    familyPrefix: String | None
    status: TaskDefinitionStatus | None
    sort: SortOrder | None
    nextToken: String | None
    maxResults: BoxedInteger | None


class ListTaskDefinitionsResponse(TypedDict, total=False):
    taskDefinitionArns: StringList | None
    nextToken: String | None


class ListTasksRequest(ServiceRequest):
    cluster: String | None
    containerInstance: String | None
    family: String | None
    nextToken: String | None
    maxResults: BoxedInteger | None
    startedBy: String | None
    serviceName: String | None
    desiredStatus: DesiredStatus | None
    launchType: LaunchType | None


class ListTasksResponse(TypedDict, total=False):
    taskArns: StringList | None
    nextToken: String | None


class ManagedAgentStateChange(TypedDict, total=False):
    """An object representing a change in state for a managed agent."""

    containerName: String
    managedAgentName: ManagedAgentName
    status: String
    reason: String | None


ManagedAgentStateChanges = list[ManagedAgentStateChange]


class PlatformDevice(TypedDict, total=False):
    id: String
    type: PlatformDeviceType


PlatformDevices = list[PlatformDevice]


class PutAccountSettingDefaultRequest(ServiceRequest):
    name: SettingName
    value: String


class PutAccountSettingDefaultResponse(TypedDict, total=False):
    setting: Setting | None


class PutAccountSettingRequest(ServiceRequest):
    name: SettingName
    value: String
    principalArn: String | None


class PutAccountSettingResponse(TypedDict, total=False):
    setting: Setting | None


class PutAttributesRequest(ServiceRequest):
    cluster: String | None
    attributes: Attributes


class PutAttributesResponse(TypedDict, total=False):
    attributes: Attributes | None


class PutClusterCapacityProvidersRequest(ServiceRequest):
    cluster: String
    capacityProviders: StringList
    defaultCapacityProviderStrategy: CapacityProviderStrategy


class PutClusterCapacityProvidersResponse(TypedDict, total=False):
    cluster: Cluster | None


class RegisterContainerInstanceRequest(ServiceRequest):
    cluster: String | None
    instanceIdentityDocument: String | None
    instanceIdentityDocumentSignature: String | None
    totalResources: Resources | None
    versionInfo: VersionInfo | None
    containerInstanceArn: String | None
    attributes: Attributes | None
    platformDevices: PlatformDevices | None
    tags: Tags | None


class RegisterContainerInstanceResponse(TypedDict, total=False):
    containerInstance: ContainerInstance | None


class RegisterTaskDefinitionRequest(ServiceRequest):
    family: String
    taskRoleArn: String | None
    executionRoleArn: String | None
    networkMode: NetworkMode | None
    containerDefinitions: ContainerDefinitions
    volumes: VolumeList | None
    placementConstraints: TaskDefinitionPlacementConstraints | None
    requiresCompatibilities: CompatibilityList | None
    cpu: String | None
    memory: String | None
    tags: Tags | None
    pidMode: PidMode | None
    ipcMode: IpcMode | None
    proxyConfiguration: ProxyConfiguration | None
    inferenceAccelerators: InferenceAccelerators | None
    ephemeralStorage: EphemeralStorage | None
    runtimePlatform: RuntimePlatform | None
    enableFaultInjection: BoxedBoolean | None


class RegisterTaskDefinitionResponse(TypedDict, total=False):
    taskDefinition: TaskDefinition | None
    tags: Tags | None


class TaskManagedEBSVolumeTerminationPolicy(TypedDict, total=False):
    """The termination policy for the Amazon EBS volume when the task exits.
    For more information, see `Amazon ECS volume termination
    policy <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ebs-volumes.html#ebs-volume-types>`__.
    """

    deleteOnTermination: BoxedBoolean


class TaskManagedEBSVolumeConfiguration(TypedDict, total=False):
    """The configuration for the Amazon EBS volume that Amazon ECS creates and
    manages on your behalf. These settings are used to create each Amazon
    EBS volume, with one volume created for each task.
    """

    encrypted: BoxedBoolean | None
    kmsKeyId: EBSKMSKeyId | None
    volumeType: EBSVolumeType | None
    sizeInGiB: BoxedInteger | None
    snapshotId: EBSSnapshotId | None
    volumeInitializationRate: BoxedInteger | None
    iops: BoxedInteger | None
    throughput: BoxedInteger | None
    tagSpecifications: EBSTagSpecifications | None
    roleArn: IAMRoleArn
    terminationPolicy: TaskManagedEBSVolumeTerminationPolicy | None
    filesystemType: TaskFilesystemType | None


class TaskVolumeConfiguration(TypedDict, total=False):
    """Configuration settings for the task volume that was
    ``configuredAtLaunch`` that weren't set during ``RegisterTaskDef``.
    """

    name: ECSVolumeName
    managedEBSVolume: TaskManagedEBSVolumeConfiguration | None


TaskVolumeConfigurations = list[TaskVolumeConfiguration]


class RunTaskRequest(ServiceRequest):
    capacityProviderStrategy: CapacityProviderStrategy | None
    cluster: String | None
    count: BoxedInteger | None
    enableECSManagedTags: Boolean | None
    enableExecuteCommand: Boolean | None
    group: String | None
    launchType: LaunchType | None
    networkConfiguration: NetworkConfiguration | None
    overrides: TaskOverride | None
    placementConstraints: PlacementConstraints | None
    placementStrategy: PlacementStrategies | None
    platformVersion: String | None
    propagateTags: PropagateTags | None
    referenceId: String | None
    startedBy: String | None
    tags: Tags | None
    taskDefinition: String
    clientToken: String | None
    volumeConfigurations: TaskVolumeConfigurations | None


class RunTaskResponse(TypedDict, total=False):
    tasks: Tasks | None
    failures: Failures | None


class StartTaskRequest(ServiceRequest):
    cluster: String | None
    containerInstances: StringList
    enableECSManagedTags: Boolean | None
    enableExecuteCommand: Boolean | None
    group: String | None
    networkConfiguration: NetworkConfiguration | None
    overrides: TaskOverride | None
    propagateTags: PropagateTags | None
    referenceId: String | None
    startedBy: String | None
    tags: Tags | None
    taskDefinition: String
    volumeConfigurations: TaskVolumeConfigurations | None


class StartTaskResponse(TypedDict, total=False):
    tasks: Tasks | None
    failures: Failures | None


class StopServiceDeploymentRequest(ServiceRequest):
    serviceDeploymentArn: String
    stopType: StopServiceDeploymentStopType | None


class StopServiceDeploymentResponse(TypedDict, total=False):
    serviceDeploymentArn: String | None


class StopTaskRequest(ServiceRequest):
    cluster: String | None
    task: String
    reason: String | None


class StopTaskResponse(TypedDict, total=False):
    task: Task | None


class SubmitAttachmentStateChangesRequest(ServiceRequest):
    cluster: String | None
    attachments: AttachmentStateChanges


class SubmitAttachmentStateChangesResponse(TypedDict, total=False):
    acknowledgment: String | None


class SubmitContainerStateChangeRequest(ServiceRequest):
    cluster: String | None
    task: String | None
    containerName: String | None
    runtimeId: String | None
    status: String | None
    exitCode: BoxedInteger | None
    reason: String | None
    networkBindings: NetworkBindings | None


class SubmitContainerStateChangeResponse(TypedDict, total=False):
    acknowledgment: String | None


class SubmitTaskStateChangeRequest(ServiceRequest):
    cluster: String | None
    task: String | None
    status: String | None
    reason: String | None
    containers: ContainerStateChanges | None
    attachments: AttachmentStateChanges | None
    managedAgents: ManagedAgentStateChanges | None
    pullStartedAt: Timestamp | None
    pullStoppedAt: Timestamp | None
    executionStoppedAt: Timestamp | None


class SubmitTaskStateChangeResponse(TypedDict, total=False):
    acknowledgment: String | None


TagKeys = list[TagKey]


class TagResourceRequest(ServiceRequest):
    resourceArn: String
    tags: Tags


class TagResourceResponse(TypedDict, total=False):
    pass


class UntagResourceRequest(ServiceRequest):
    resourceArn: String
    tagKeys: TagKeys


class UntagResourceResponse(TypedDict, total=False):
    pass


class UpdateManagedInstancesProviderConfiguration(TypedDict, total=False):
    """The updated configuration for a Amazon ECS Managed Instances provider.
    You can modify the infrastructure role, instance launch template, and
    tag propagation settings. Changes apply to new instances launched after
    the update.
    """

    infrastructureRoleArn: String
    instanceLaunchTemplate: InstanceLaunchTemplateUpdate
    propagateTags: PropagateMITags | None
    infrastructureOptimization: InfrastructureOptimization | None


class UpdateCapacityProviderRequest(ServiceRequest):
    name: String
    cluster: String | None
    autoScalingGroupProvider: AutoScalingGroupProviderUpdate | None
    managedInstancesProvider: UpdateManagedInstancesProviderConfiguration | None


class UpdateCapacityProviderResponse(TypedDict, total=False):
    capacityProvider: CapacityProvider | None


class UpdateClusterRequest(ServiceRequest):
    cluster: String
    settings: ClusterSettings | None
    configuration: ClusterConfiguration | None
    serviceConnectDefaults: ClusterServiceConnectDefaultsRequest | None


class UpdateClusterResponse(TypedDict, total=False):
    cluster: Cluster | None


class UpdateClusterSettingsRequest(ServiceRequest):
    cluster: String
    settings: ClusterSettings


class UpdateClusterSettingsResponse(TypedDict, total=False):
    cluster: Cluster | None


class UpdateContainerAgentRequest(ServiceRequest):
    cluster: String | None
    containerInstance: String


class UpdateContainerAgentResponse(TypedDict, total=False):
    containerInstance: ContainerInstance | None


class UpdateContainerInstancesStateRequest(ServiceRequest):
    cluster: String | None
    containerInstances: StringList
    status: ContainerInstanceStatus


class UpdateContainerInstancesStateResponse(TypedDict, total=False):
    containerInstances: ContainerInstances | None
    failures: Failures | None


class UpdateExpressGatewayServiceRequest(ServiceRequest):
    serviceArn: String
    executionRoleArn: String | None
    healthCheckPath: String | None
    primaryContainer: ExpressGatewayContainer | None
    taskRoleArn: String | None
    networkConfiguration: ExpressGatewayServiceNetworkConfiguration | None
    cpu: String | None
    memory: String | None
    scalingTarget: ExpressGatewayScalingTarget | None


class UpdatedExpressGatewayService(TypedDict, total=False):
    """An object that describes an Express service to be updated."""

    serviceArn: String | None
    cluster: String | None
    serviceName: String | None
    status: ExpressGatewayServiceStatus | None
    targetConfiguration: ExpressGatewayServiceConfiguration | None
    createdAt: Timestamp | None
    updatedAt: Timestamp | None


class UpdateExpressGatewayServiceResponse(TypedDict, total=False):
    service: UpdatedExpressGatewayService | None


class UpdateServicePrimaryTaskSetRequest(ServiceRequest):
    cluster: String
    service: String
    primaryTaskSet: String


class UpdateServicePrimaryTaskSetResponse(TypedDict, total=False):
    taskSet: TaskSet | None


class UpdateServiceRequest(ServiceRequest):
    cluster: String | None
    service: String
    desiredCount: BoxedInteger | None
    taskDefinition: String | None
    capacityProviderStrategy: CapacityProviderStrategy | None
    deploymentConfiguration: DeploymentConfiguration | None
    availabilityZoneRebalancing: AvailabilityZoneRebalancing | None
    networkConfiguration: NetworkConfiguration | None
    placementConstraints: PlacementConstraints | None
    placementStrategy: PlacementStrategies | None
    platformVersion: String | None
    forceNewDeployment: Boolean | None
    healthCheckGracePeriodSeconds: BoxedInteger | None
    deploymentController: DeploymentController | None
    enableExecuteCommand: BoxedBoolean | None
    enableECSManagedTags: BoxedBoolean | None
    loadBalancers: LoadBalancers | None
    propagateTags: PropagateTags | None
    serviceRegistries: ServiceRegistries | None
    serviceConnectConfiguration: ServiceConnectConfiguration | None
    volumeConfigurations: ServiceVolumeConfigurations | None
    vpcLatticeConfigurations: VpcLatticeConfigurations | None


class UpdateServiceResponse(TypedDict, total=False):
    service: Service | None


class UpdateTaskProtectionRequest(ServiceRequest):
    cluster: String
    tasks: StringList
    protectionEnabled: Boolean
    expiresInMinutes: BoxedInteger | None


class UpdateTaskProtectionResponse(TypedDict, total=False):
    protectedTasks: ProtectedTasks | None
    failures: Failures | None


class UpdateTaskSetRequest(ServiceRequest):
    cluster: String
    service: String
    taskSet: String
    scale: Scale


class UpdateTaskSetResponse(TypedDict, total=False):
    taskSet: TaskSet | None


class EcsApi:
    service: str = "ecs"
    version: str = "2014-11-13"

    @handler("CreateCapacityProvider")
    def create_capacity_provider(
        self,
        context: RequestContext,
        name: String,
        cluster: String | None = None,
        auto_scaling_group_provider: AutoScalingGroupProvider | None = None,
        managed_instances_provider: CreateManagedInstancesProviderConfiguration | None = None,
        tags: Tags | None = None,
        **kwargs,
    ) -> CreateCapacityProviderResponse:
        """Creates a capacity provider. Capacity providers are associated with a
        cluster and are used in capacity provider strategies to facilitate
        cluster auto scaling. You can create capacity providers for Amazon ECS
        Managed Instances and EC2 instances. Fargate has the predefined
        ``FARGATE`` and ``FARGATE_SPOT`` capacity providers.

        :param name: The name of the capacity provider.
        :param cluster: The name of the cluster to associate with the capacity provider.
        :param auto_scaling_group_provider: The details of the Auto Scaling group for the capacity provider.
        :param managed_instances_provider: The configuration for the Amazon ECS Managed Instances provider.
        :param tags: The metadata that you apply to the capacity provider to categorize and
        organize them more conveniently.
        :returns: CreateCapacityProviderResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises LimitExceededException:
        :raises UpdateInProgressException:
        :raises UnsupportedFeatureException:
        :raises ClusterNotFoundException:
        """
        raise NotImplementedError

    @handler("CreateCluster")
    def create_cluster(
        self,
        context: RequestContext,
        cluster_name: String | None = None,
        tags: Tags | None = None,
        settings: ClusterSettings | None = None,
        configuration: ClusterConfiguration | None = None,
        capacity_providers: StringList | None = None,
        default_capacity_provider_strategy: CapacityProviderStrategy | None = None,
        service_connect_defaults: ClusterServiceConnectDefaultsRequest | None = None,
        **kwargs,
    ) -> CreateClusterResponse:
        """Creates a new Amazon ECS cluster. By default, your account receives a
        ``default`` cluster when you launch your first container instance.
        However, you can create your own cluster with a unique name.

        When you call the
        `CreateCluster <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_CreateCluster.html>`__
        API operation, Amazon ECS attempts to create the Amazon ECS
        service-linked role for your account. This is so that it can manage
        required resources in other Amazon Web Services services on your behalf.
        However, if the user that makes the call doesn't have permissions to
        create the service-linked role, it isn't created. For more information,
        see `Using service-linked roles for Amazon
        ECS <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using-service-linked-roles.html>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        :param cluster_name: The name of your cluster.
        :param tags: The metadata that you apply to the cluster to help you categorize and
        organize them.
        :param settings: The setting to use when creating a cluster.
        :param configuration: The ``execute`` command configuration for the cluster.
        :param capacity_providers: The short name of one or more capacity providers to associate with the
        cluster.
        :param default_capacity_provider_strategy: The capacity provider strategy to set as the default for the cluster.
        :param service_connect_defaults: Use this parameter to set a default Service Connect namespace.
        :returns: CreateClusterResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises NamespaceNotFoundException:
        """
        raise NotImplementedError

    @handler("CreateExpressGatewayService")
    def create_express_gateway_service(
        self,
        context: RequestContext,
        execution_role_arn: String,
        infrastructure_role_arn: String,
        primary_container: ExpressGatewayContainer,
        service_name: String | None = None,
        cluster: String | None = None,
        health_check_path: String | None = None,
        task_role_arn: String | None = None,
        network_configuration: ExpressGatewayServiceNetworkConfiguration | None = None,
        cpu: String | None = None,
        memory: String | None = None,
        scaling_target: ExpressGatewayScalingTarget | None = None,
        tags: Tags | None = None,
        **kwargs,
    ) -> CreateExpressGatewayServiceResponse:
        """Creates an Express service that simplifies deploying containerized web
        applications on Amazon ECS with managed Amazon Web Services
        infrastructure. This operation provisions and configures Application
        Load Balancers, target groups, security groups, and auto-scaling
        policies automatically.

        Specify a primary container configuration with your application image
        and basic settings. Amazon ECS creates the necessary Amazon Web Services
        resources for traffic distribution, health monitoring, network access
        control, and capacity management.

        Provide an execution role for task operations and an infrastructure role
        for managing Amazon Web Services resources on your behalf.

        :param execution_role_arn: The Amazon Resource Name (ARN) of the task execution role that grants
        the Amazon ECS container agent permission to make Amazon Web Services
        API calls on your behalf.
        :param infrastructure_role_arn: The Amazon Resource Name (ARN) of the infrastructure role that grants
        Amazon ECS permission to create and manage Amazon Web Services resources
        on your behalf for the Express service.
        :param primary_container: The primary container configuration for the Express service.
        :param service_name: The name of the Express service.
        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster on
        which to create the Express service.
        :param health_check_path: The path on the container that the Application Load Balancer uses for
        health checks.
        :param task_role_arn: The Amazon Resource Name (ARN) of the IAM role that containers in this
        task can assume.
        :param network_configuration: The network configuration for the Express service tasks.
        :param cpu: The number of CPU units used by the task.
        :param memory: The amount of memory (in MiB) used by the task.
        :param scaling_target: The auto-scaling configuration for the Express service.
        :param tags: The metadata that you apply to the Express service to help categorize
        and organize it.
        :returns: CreateExpressGatewayServiceResponse
        :raises AccessDeniedException:
        :raises ClientException:
        :raises ClusterNotFoundException:
        :raises InvalidParameterException:
        :raises PlatformUnknownException:
        :raises PlatformTaskDefinitionIncompatibilityException:
        :raises ServerException:
        :raises UnsupportedFeatureException:
        """
        raise NotImplementedError

    @handler("CreateService")
    def create_service(
        self,
        context: RequestContext,
        service_name: String,
        cluster: String | None = None,
        task_definition: String | None = None,
        availability_zone_rebalancing: AvailabilityZoneRebalancing | None = None,
        load_balancers: LoadBalancers | None = None,
        service_registries: ServiceRegistries | None = None,
        desired_count: BoxedInteger | None = None,
        client_token: String | None = None,
        launch_type: LaunchType | None = None,
        capacity_provider_strategy: CapacityProviderStrategy | None = None,
        platform_version: String | None = None,
        role: String | None = None,
        deployment_configuration: DeploymentConfiguration | None = None,
        placement_constraints: PlacementConstraints | None = None,
        placement_strategy: PlacementStrategies | None = None,
        network_configuration: NetworkConfiguration | None = None,
        health_check_grace_period_seconds: BoxedInteger | None = None,
        scheduling_strategy: SchedulingStrategy | None = None,
        deployment_controller: DeploymentController | None = None,
        tags: Tags | None = None,
        enable_ecs_managed_tags: Boolean | None = None,
        propagate_tags: PropagateTags | None = None,
        enable_execute_command: Boolean | None = None,
        service_connect_configuration: ServiceConnectConfiguration | None = None,
        volume_configurations: ServiceVolumeConfigurations | None = None,
        vpc_lattice_configurations: VpcLatticeConfigurations | None = None,
        **kwargs,
    ) -> CreateServiceResponse:
        """Runs and maintains your desired number of tasks from a specified task
        definition. If the number of tasks running in a service drops below the
        ``desiredCount``, Amazon ECS runs another copy of the task in the
        specified cluster. To update an existing service, use
        `UpdateService <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_UpdateService.html>`__.

        On March 21, 2024, a change was made to resolve the task definition
        revision before authorization. When a task definition revision is not
        specified, authorization will occur using the latest revision of a task
        definition.

        Amazon Elastic Inference (EI) is no longer available to customers.

        In addition to maintaining the desired count of tasks in your service,
        you can optionally run your service behind one or more load balancers.
        The load balancers distribute traffic across the tasks that are
        associated with the service. For more information, see `Service load
        balancing <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-load-balancing.html>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        You can attach Amazon EBS volumes to Amazon ECS tasks by configuring the
        volume when creating or updating a service. ``volumeConfigurations`` is
        only supported for REPLICA service and not DAEMON service. For more
        information, see `Amazon EBS
        volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ebs-volumes.html#ebs-volume-types>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        Tasks for services that don't use a load balancer are considered healthy
        if they're in the ``RUNNING`` state. Tasks for services that use a load
        balancer are considered healthy if they're in the ``RUNNING`` state and
        are reported as healthy by the load balancer.

        There are two service scheduler strategies available:

        -  ``REPLICA`` - The replica scheduling strategy places and maintains
           your desired number of tasks across your cluster. By default, the
           service scheduler spreads tasks across Availability Zones. You can
           use task placement strategies and constraints to customize task
           placement decisions. For more information, see `Service scheduler
           concepts <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_services.html>`__
           in the *Amazon Elastic Container Service Developer Guide*.

        -  ``DAEMON`` - The daemon scheduling strategy deploys exactly one task
           on each active container instance that meets all of the task
           placement constraints that you specify in your cluster. The service
           scheduler also evaluates the task placement constraints for running
           tasks. It also stops tasks that don't meet the placement constraints.
           When using this strategy, you don't need to specify a desired number
           of tasks, a task placement strategy, or use Service Auto Scaling
           policies. For more information, see `Amazon ECS
           services <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_services.html>`__
           in the *Amazon Elastic Container Service Developer Guide*.

        The deployment controller is the mechanism that determines how tasks are
        deployed for your service. The valid options are:

        -  ECS

           When you create a service which uses the ``ECS`` deployment
           controller, you can choose between the following deployment
           strategies (which you can set in the “ ``strategy`` ” field in
           “ ``deploymentConfiguration`` ”): :

           -  ``ROLLING``: When you create a service which uses the *rolling
              update* (``ROLLING``) deployment strategy, the Amazon ECS service
              scheduler replaces the currently running tasks with new tasks. The
              number of tasks that Amazon ECS adds or removes from the service
              during a rolling update is controlled by the service deployment
              configuration. For more information, see `Deploy Amazon ECS
              services by replacing
              tasks <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-ecs.html>`__
              in the *Amazon Elastic Container Service Developer Guide*.

              Rolling update deployments are best suited for the following
              scenarios:

              -  Gradual service updates: You need to update your service
                 incrementally without taking the entire service offline at
                 once.

              -  Limited resource requirements: You want to avoid the additional
                 resource costs of running two complete environments
                 simultaneously (as required by blue/green deployments).

              -  Acceptable deployment time: Your application can tolerate a
                 longer deployment process, as rolling updates replace tasks one
                 by one.

              -  No need for instant roll back: Your service can tolerate a
                 rollback process that takes minutes rather than seconds.

              -  Simple deployment process: You prefer a straightforward
                 deployment approach without the complexity of managing multiple
                 environments, target groups, and listeners.

              -  No load balancer requirement: Your service doesn't use or
                 require a load balancer, Application Load Balancer, Network
                 Load Balancer, or Service Connect (which are required for
                 blue/green deployments).

              -  Stateful applications: Your application maintains state that
                 makes it difficult to run two parallel environments.

              -  Cost sensitivity: You want to minimize deployment costs by not
                 running duplicate environments during deployment.

              Rolling updates are the default deployment strategy for services
              and provide a balance between deployment safety and resource
              efficiency for many common application scenarios.

           -  ``BLUE_GREEN``: A *blue/green* deployment strategy
              (``BLUE_GREEN``) is a release methodology that reduces downtime
              and risk by running two identical production environments called
              blue and green. With Amazon ECS blue/green deployments, you can
              validate new service revisions before directing production traffic
              to them. This approach provides a safer way to deploy changes with
              the ability to quickly roll back if needed. For more information,
              see `Amazon ECS blue/green
              deployments <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-blue-green.html>`__
              in the *Amazon Elastic Container Service Developer Guide*.

              Amazon ECS blue/green deployments are best suited for the
              following scenarios:

              -  Service validation: When you need to validate new service
                 revisions before directing production traffic to them

              -  Zero downtime: When your service requires zero-downtime
                 deployments

              -  Instant roll back: When you need the ability to quickly roll
                 back if issues are detected

              -  Load balancer requirement: When your service uses Application
                 Load Balancer, Network Load Balancer, or Service Connect

           -  ``LINEAR``: A *linear* deployment strategy (``LINEAR``) gradually
              shifts traffic from the current production environment to a new
              environment in equal percentage increments. With Amazon ECS linear
              deployments, you can control the pace of traffic shifting and
              validate new service revisions with increasing amounts of
              production traffic.

              Linear deployments are best suited for the following scenarios:

              -  Gradual validation: When you want to gradually validate your
                 new service version with increasing traffic

              -  Performance monitoring: When you need time to monitor metrics
                 and performance during the deployment

              -  Risk minimization: When you want to minimize risk by exposing
                 the new version to production traffic incrementally

              -  Load balancer requirement: When your service uses Application
                 Load Balancer or Service Connect

           -  ``CANARY``: A *canary* deployment strategy (``CANARY``) shifts a
              small percentage of traffic to the new service revision first,
              then shifts the remaining traffic all at once after a specified
              time period. This allows you to test the new version with a subset
              of users before full deployment.

              Canary deployments are best suited for the following scenarios:

              -  Feature testing: When you want to test new features with a
                 small subset of users before full rollout

              -  Production validation: When you need to validate performance
                 and functionality with real production traffic

              -  Blast radius control: When you want to minimize blast radius if
                 issues are discovered in the new version

              -  Load balancer requirement: When your service uses Application
                 Load Balancer or Service Connect

        -  External

           Use a third-party deployment controller.

        -  Blue/green deployment (powered by CodeDeploy)

           CodeDeploy installs an updated version of the application as a new
           replacement task set and reroutes production traffic from the
           original application task set to the replacement task set. The
           original task set is terminated after a successful deployment. Use
           this deployment controller to verify a new deployment of a service
           before sending production traffic to it.

        When creating a service that uses the ``EXTERNAL`` deployment
        controller, you can specify only parameters that aren't controlled at
        the task set level. The only required parameter is the service name. You
        control your services using the
        `CreateTaskSet <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_CreateTaskSet.html>`__.
        For more information, see `Amazon ECS deployment
        types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        When the service scheduler launches new tasks, it determines task
        placement. For information about task placement and task placement
        strategies, see `Amazon ECS task
        placement <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement.html>`__
        in the *Amazon Elastic Container Service Developer Guide*

        :param service_name: The name of your service.
        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster that
        you run your service on.
        :param task_definition: The ``family`` and ``revision`` (``family:revision``) or full ARN of the
        task definition to run in your service.
        :param availability_zone_rebalancing: Indicates whether to use Availability Zone rebalancing for the service.
        :param load_balancers: A load balancer object representing the load balancers to use with your
        service.
        :param service_registries: The details of the service discovery registry to associate with this
        service.
        :param desired_count: The number of instantiations of the specified task definition to place
        and keep running in your service.
        :param client_token: An identifier that you provide to ensure the idempotency of the request.
        :param launch_type: The infrastructure that you run your service on.
        :param capacity_provider_strategy: The capacity provider strategy to use for the service.
        :param platform_version: The platform version that your tasks in the service are running on.
        :param role: The name or full Amazon Resource Name (ARN) of the IAM role that allows
        Amazon ECS to make calls to your load balancer on your behalf.
        :param deployment_configuration: Optional deployment parameters that control how many tasks run during
        the deployment and the ordering of stopping and starting tasks.
        :param placement_constraints: An array of placement constraint objects to use for tasks in your
        service.
        :param placement_strategy: The placement strategy objects to use for tasks in your service.
        :param network_configuration: The network configuration for the service.
        :param health_check_grace_period_seconds: The period of time, in seconds, that the Amazon ECS service scheduler
        ignores unhealthy Elastic Load Balancing, VPC Lattice, and container
        health checks after a task has first started.
        :param scheduling_strategy: The scheduling strategy to use for the service.
        :param deployment_controller: The deployment controller to use for the service.
        :param tags: The metadata that you apply to the service to help you categorize and
        organize them.
        :param enable_ecs_managed_tags: Specifies whether to turn on Amazon ECS managed tags for the tasks
        within the service.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition to the
        task.
        :param enable_execute_command: Determines whether the execute command functionality is turned on for
        the service.
        :param service_connect_configuration: The configuration for this service to discover and connect to services,
        and be discovered by, and connected from, other services within a
        namespace.
        :param volume_configurations: The configuration for a volume specified in the task definition as a
        volume that is configured at launch time.
        :param vpc_lattice_configurations: The VPC Lattice configuration for the service being created.
        :returns: CreateServiceResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        :raises UnsupportedFeatureException:
        :raises PlatformUnknownException:
        :raises PlatformTaskDefinitionIncompatibilityException:
        :raises AccessDeniedException:
        :raises NamespaceNotFoundException:
        """
        raise NotImplementedError

    @handler("CreateTaskSet")
    def create_task_set(
        self,
        context: RequestContext,
        service: String,
        cluster: String,
        task_definition: String,
        external_id: String | None = None,
        network_configuration: NetworkConfiguration | None = None,
        load_balancers: LoadBalancers | None = None,
        service_registries: ServiceRegistries | None = None,
        launch_type: LaunchType | None = None,
        capacity_provider_strategy: CapacityProviderStrategy | None = None,
        platform_version: String | None = None,
        scale: Scale | None = None,
        client_token: String | None = None,
        tags: Tags | None = None,
        **kwargs,
    ) -> CreateTaskSetResponse:
        """Create a task set in the specified cluster and service. This is used
        when a service uses the ``EXTERNAL`` deployment controller type. For
        more information, see `Amazon ECS deployment
        types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        On March 21, 2024, a change was made to resolve the task definition
        revision before authorization. When a task definition revision is not
        specified, authorization will occur using the latest revision of a task
        definition.

        For information about the maximum number of task sets and other quotas,
        see `Amazon ECS service
        quotas <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-quotas.html>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        :param service: The short name or full Amazon Resource Name (ARN) of the service to
        create the task set in.
        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster that
        hosts the service to create the task set in.
        :param task_definition: The task definition for the tasks in the task set to use.
        :param external_id: An optional non-unique tag that identifies this task set in external
        systems.
        :param network_configuration: An object representing the network configuration for a task set.
        :param load_balancers: A load balancer object representing the load balancer to use with the
        task set.
        :param service_registries: The details of the service discovery registries to assign to this task
        set.
        :param launch_type: The launch type that new tasks in the task set uses.
        :param capacity_provider_strategy: The capacity provider strategy to use for the task set.
        :param platform_version: The platform version that the tasks in the task set uses.
        :param scale: A floating-point percentage of the desired number of tasks to place and
        keep running in the task set.
        :param client_token: An identifier that you provide to ensure the idempotency of the request.
        :param tags: The metadata that you apply to the task set to help you categorize and
        organize them.
        :returns: CreateTaskSetResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        :raises UnsupportedFeatureException:
        :raises PlatformUnknownException:
        :raises PlatformTaskDefinitionIncompatibilityException:
        :raises AccessDeniedException:
        :raises ServiceNotFoundException:
        :raises ServiceNotActiveException:
        :raises NamespaceNotFoundException:
        """
        raise NotImplementedError

    @handler("DeleteAccountSetting")
    def delete_account_setting(
        self,
        context: RequestContext,
        name: SettingName,
        principal_arn: String | None = None,
        **kwargs,
    ) -> DeleteAccountSettingResponse:
        """Disables an account setting for a specified user, role, or the root user
        for an account.

        :param name: The resource name to disable the account setting for.
        :param principal_arn: The Amazon Resource Name (ARN) of the principal.
        :returns: DeleteAccountSettingResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("DeleteAttributes")
    def delete_attributes(
        self,
        context: RequestContext,
        attributes: Attributes,
        cluster: String | None = None,
        **kwargs,
    ) -> DeleteAttributesResponse:
        """Deletes one or more custom attributes from an Amazon ECS resource.

        :param attributes: The attributes to delete from your resource.
        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster that
        contains the resource to delete attributes.
        :returns: DeleteAttributesResponse
        :raises ClusterNotFoundException:
        :raises TargetNotFoundException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("DeleteCapacityProvider")
    def delete_capacity_provider(
        self,
        context: RequestContext,
        capacity_provider: String,
        cluster: String | None = None,
        **kwargs,
    ) -> DeleteCapacityProviderResponse:
        """Deletes the specified capacity provider.

        The ``FARGATE`` and ``FARGATE_SPOT`` capacity providers are reserved and
        can't be deleted. You can disassociate them from a cluster using either
        `PutClusterCapacityProviders <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PutClusterCapacityProviders.html>`__
        or by deleting the cluster.

        Prior to a capacity provider being deleted, the capacity provider must
        be removed from the capacity provider strategy from all services. The
        `UpdateService <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_UpdateService.html>`__
        API can be used to remove a capacity provider from a service's capacity
        provider strategy. When updating a service, the ``forceNewDeployment``
        option can be used to ensure that any tasks using the Amazon EC2
        instance capacity provided by the capacity provider are transitioned to
        use the capacity from the remaining capacity providers. Only capacity
        providers that aren't associated with a cluster can be deleted. To
        remove a capacity provider from a cluster, you can either use
        `PutClusterCapacityProviders <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PutClusterCapacityProviders.html>`__
        or delete the cluster.

        :param capacity_provider: The short name or full Amazon Resource Name (ARN) of the capacity
        provider to delete.
        :param cluster: The name of the cluster that contains the capacity provider to delete.
        :returns: DeleteCapacityProviderResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises UnsupportedFeatureException:
        :raises ClusterNotFoundException:
        """
        raise NotImplementedError

    @handler("DeleteCluster")
    def delete_cluster(
        self, context: RequestContext, cluster: String, **kwargs
    ) -> DeleteClusterResponse:
        """Deletes the specified cluster. The cluster transitions to the
        ``INACTIVE`` state. Clusters with an ``INACTIVE`` status might remain
        discoverable in your account for a period of time. However, this
        behavior is subject to change in the future. We don't recommend that you
        rely on ``INACTIVE`` clusters persisting.

        You must deregister all container instances from this cluster before you
        may delete it. You can list the container instances in a cluster with
        `ListContainerInstances <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ListContainerInstances.html>`__
        and deregister them with
        `DeregisterContainerInstance <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_DeregisterContainerInstance.html>`__.

        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster to
        delete.
        :returns: DeleteClusterResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        :raises ClusterContainsCapacityProviderException:
        :raises ClusterContainsContainerInstancesException:
        :raises ClusterContainsServicesException:
        :raises ClusterContainsTasksException:
        :raises UpdateInProgressException:
        """
        raise NotImplementedError

    @handler("DeleteExpressGatewayService")
    def delete_express_gateway_service(
        self, context: RequestContext, service_arn: String, **kwargs
    ) -> DeleteExpressGatewayServiceResponse:
        """Deletes an Express service and removes all associated Amazon Web
        Services resources. This operation stops service tasks, removes the
        Application Load Balancer, target groups, security groups, auto-scaling
        policies, and other managed infrastructure components.

        The service enters a ``DRAINING`` state where existing tasks complete
        current requests without starting new tasks. After all tasks stop, the
        service and infrastructure are permanently removed.

        This operation cannot be reversed. Back up important data and verify the
        service is no longer needed before deletion.

        :param service_arn: The Amazon Resource Name (ARN) of the Express service to delete.
        :returns: DeleteExpressGatewayServiceResponse
        :raises AccessDeniedException:
        :raises ClientException:
        :raises ClusterNotFoundException:
        :raises InvalidParameterException:
        :raises ServerException:
        :raises ServiceNotFoundException:
        :raises ServiceNotActiveException:
        :raises UnsupportedFeatureException:
        """
        raise NotImplementedError

    @handler("DeleteService")
    def delete_service(
        self,
        context: RequestContext,
        service: String,
        cluster: String | None = None,
        force: BoxedBoolean | None = None,
        **kwargs,
    ) -> DeleteServiceResponse:
        """Deletes a specified service within a cluster. You can delete a service
        if you have no running tasks in it and the desired task count is zero.
        If the service is actively maintaining tasks, you can't delete it, and
        you must update the service to a desired task count of zero. For more
        information, see
        `UpdateService <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_UpdateService.html>`__.

        When you delete a service, if there are still running tasks that require
        cleanup, the service status moves from ``ACTIVE`` to ``DRAINING``, and
        the service is no longer visible in the console or in the
        `ListServices <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ListServices.html>`__
        API operation. After all tasks have transitioned to either ``STOPPING``
        or ``STOPPED`` status, the service status moves from ``DRAINING`` to
        ``INACTIVE``. Services in the ``DRAINING`` or ``INACTIVE`` status can
        still be viewed with the
        `DescribeServices <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_DescribeServices.html>`__
        API operation. However, in the future, ``INACTIVE`` services may be
        cleaned up and purged from Amazon ECS record keeping, and
        `DescribeServices <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_DescribeServices.html>`__
        calls on those services return a ``ServiceNotFoundException`` error.

        If you attempt to create a new service with the same name as an existing
        service in either ``ACTIVE`` or ``DRAINING`` status, you receive an
        error.

        :param service: The name of the service to delete.
        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster that
        hosts the service to delete.
        :param force: If ``true``, allows you to delete a service even if it wasn't scaled
        down to zero tasks.
        :returns: DeleteServiceResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        :raises ServiceNotFoundException:
        """
        raise NotImplementedError

    @handler("DeleteTaskDefinitions")
    def delete_task_definitions(
        self, context: RequestContext, task_definitions: StringList, **kwargs
    ) -> DeleteTaskDefinitionsResponse:
        """Deletes one or more task definitions.

        You must deregister a task definition revision before you delete it. For
        more information, see
        `DeregisterTaskDefinition <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_DeregisterTaskDefinition.html>`__.

        When you delete a task definition revision, it is immediately
        transitions from the ``INACTIVE`` to ``DELETE_IN_PROGRESS``. Existing
        tasks and services that reference a ``DELETE_IN_PROGRESS`` task
        definition revision continue to run without disruption. Existing
        services that reference a ``DELETE_IN_PROGRESS`` task definition
        revision can still scale up or down by modifying the service's desired
        count.

        You can't use a ``DELETE_IN_PROGRESS`` task definition revision to run
        new tasks or create new services. You also can't update an existing
        service to reference a ``DELETE_IN_PROGRESS`` task definition revision.

        A task definition revision will stay in ``DELETE_IN_PROGRESS`` status
        until all the associated tasks and services have been terminated.

        When you delete all ``INACTIVE`` task definition revisions, the task
        definition name is not displayed in the console and not returned in the
        API. If a task definition revisions are in the ``DELETE_IN_PROGRESS``
        state, the task definition name is displayed in the console and returned
        in the API. The task definition name is retained by Amazon ECS and the
        revision is incremented the next time you create a task definition with
        that name.

        :param task_definitions: The ``family`` and ``revision`` (``family:revision``) or full Amazon
        Resource Name (ARN) of the task definition to delete.
        :returns: DeleteTaskDefinitionsResponse
        :raises AccessDeniedException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ServerException:
        """
        raise NotImplementedError

    @handler("DeleteTaskSet")
    def delete_task_set(
        self,
        context: RequestContext,
        cluster: String,
        service: String,
        task_set: String,
        force: BoxedBoolean | None = None,
        **kwargs,
    ) -> DeleteTaskSetResponse:
        """Deletes a specified task set within a service. This is used when a
        service uses the ``EXTERNAL`` deployment controller type. For more
        information, see `Amazon ECS deployment
        types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster that
        hosts the service that the task set found in to delete.
        :param service: The short name or full Amazon Resource Name (ARN) of the service that
        hosts the task set to delete.
        :param task_set: The task set ID or full Amazon Resource Name (ARN) of the task set to
        delete.
        :param force: If ``true``, you can delete a task set even if it hasn't been scaled
        down to zero.
        :returns: DeleteTaskSetResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        :raises UnsupportedFeatureException:
        :raises AccessDeniedException:
        :raises ServiceNotFoundException:
        :raises ServiceNotActiveException:
        :raises TaskSetNotFoundException:
        """
        raise NotImplementedError

    @handler("DeregisterContainerInstance")
    def deregister_container_instance(
        self,
        context: RequestContext,
        container_instance: String,
        cluster: String | None = None,
        force: BoxedBoolean | None = None,
        **kwargs,
    ) -> DeregisterContainerInstanceResponse:
        """Deregisters an Amazon ECS container instance from the specified cluster.
        This instance is no longer available to run tasks.

        If you intend to use the container instance for some other purpose after
        deregistration, we recommend that you stop all of the tasks running on
        the container instance before deregistration. That prevents any orphaned
        tasks from consuming resources.

        Deregistering a container instance removes the instance from a cluster,
        but it doesn't terminate the EC2 instance. If you are finished using the
        instance, be sure to terminate it in the Amazon EC2 console to stop
        billing.

        If you terminate a running container instance, Amazon ECS automatically
        deregisters the instance from your cluster (stopped container instances
        or instances with disconnected agents aren't automatically deregistered
        when terminated).

        :param container_instance: The container instance ID or full ARN of the container instance to
        deregister.
        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster that
        hosts the container instance to deregister.
        :param force: Forces the container instance to be deregistered.
        :returns: DeregisterContainerInstanceResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        """
        raise NotImplementedError

    @handler("DeregisterTaskDefinition")
    def deregister_task_definition(
        self, context: RequestContext, task_definition: String, **kwargs
    ) -> DeregisterTaskDefinitionResponse:
        """Deregisters the specified task definition by family and revision. Upon
        deregistration, the task definition is marked as ``INACTIVE``. Existing
        tasks and services that reference an ``INACTIVE`` task definition
        continue to run without disruption. Existing services that reference an
        ``INACTIVE`` task definition can still scale up or down by modifying the
        service's desired count. If you want to delete a task definition
        revision, you must first deregister the task definition revision.

        You can't use an ``INACTIVE`` task definition to run new tasks or create
        new services, and you can't update an existing service to reference an
        ``INACTIVE`` task definition. However, there may be up to a 10-minute
        window following deregistration where these restrictions have not yet
        taken effect.

        At this time, ``INACTIVE`` task definitions remain discoverable in your
        account indefinitely. However, this behavior is subject to change in the
        future. We don't recommend that you rely on ``INACTIVE`` task
        definitions persisting beyond the lifecycle of any associated tasks and
        services.

        You must deregister a task definition revision before you delete it. For
        more information, see
        `DeleteTaskDefinitions <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_DeleteTaskDefinitions.html>`__.

        :param task_definition: The ``family`` and ``revision`` (``family:revision``) or full Amazon
        Resource Name (ARN) of the task definition to deregister.
        :returns: DeregisterTaskDefinitionResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("DescribeCapacityProviders")
    def describe_capacity_providers(
        self,
        context: RequestContext,
        capacity_providers: StringList | None = None,
        cluster: String | None = None,
        include: CapacityProviderFieldList | None = None,
        max_results: BoxedInteger | None = None,
        next_token: String | None = None,
        **kwargs,
    ) -> DescribeCapacityProvidersResponse:
        """Describes one or more of your capacity providers.

        :param capacity_providers: The short name or full Amazon Resource Name (ARN) of one or more
        capacity providers.
        :param cluster: The name of the cluster to describe capacity providers for.
        :param include: Specifies whether or not you want to see the resource tags for the
        capacity provider.
        :param max_results: The maximum number of account setting results returned by
        ``DescribeCapacityProviders`` in paginated output.
        :param next_token: The ``nextToken`` value returned from a previous paginated
        ``DescribeCapacityProviders`` request where ``maxResults`` was used and
        the results exceeded the value of that parameter.
        :returns: DescribeCapacityProvidersResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises UnsupportedFeatureException:
        :raises ClusterNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeClusters")
    def describe_clusters(
        self,
        context: RequestContext,
        clusters: StringList | None = None,
        include: ClusterFieldList | None = None,
        **kwargs,
    ) -> DescribeClustersResponse:
        """Describes one or more of your clusters.

        For CLI examples, see
        `describe-clusters.rst <https://github.com/aws/aws-cli/blob/develop/awscli/examples/ecs/describe-clusters.rst>`__
        on GitHub.

        :param clusters: A list of up to 100 cluster names or full cluster Amazon Resource Name
        (ARN) entries.
        :param include: Determines whether to include additional information about the clusters
        in the response.
        :returns: DescribeClustersResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("DescribeContainerInstances")
    def describe_container_instances(
        self,
        context: RequestContext,
        container_instances: StringList,
        cluster: String | None = None,
        include: ContainerInstanceFieldList | None = None,
        **kwargs,
    ) -> DescribeContainerInstancesResponse:
        """Describes one or more container instances. Returns metadata about each
        container instance requested.

        :param container_instances: A list of up to 100 container instance IDs or full Amazon Resource Name
        (ARN) entries.
        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster that
        hosts the container instances to describe.
        :param include: Specifies whether you want to see the resource tags for the container
        instance.
        :returns: DescribeContainerInstancesResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeExpressGatewayService")
    def describe_express_gateway_service(
        self,
        context: RequestContext,
        service_arn: String,
        include: ExpressGatewayServiceIncludeList | None = None,
        **kwargs,
    ) -> DescribeExpressGatewayServiceResponse:
        """Retrieves detailed information about an Express service, including
        current status, configuration, managed infrastructure, and service
        revisions.

        Returns comprehensive service details, active service revisions, ingress
        paths with endpoints, and managed Amazon Web Services resource status
        including load balancers and auto-scaling policies.

        Use the ``include`` parameter to retrieve additional information such as
        resource tags.

        :param service_arn: The Amazon Resource Name (ARN) of the Express service to describe.
        :param include: Specifies additional information to include in the response.
        :returns: DescribeExpressGatewayServiceResponse
        :raises AccessDeniedException:
        :raises ClientException:
        :raises ClusterNotFoundException:
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises ServerException:
        :raises UnsupportedFeatureException:
        """
        raise NotImplementedError

    @handler("DescribeServiceDeployments")
    def describe_service_deployments(
        self, context: RequestContext, service_deployment_arns: StringList, **kwargs
    ) -> DescribeServiceDeploymentsResponse:
        """Describes one or more of your service deployments.

        A service deployment happens when you release a software update for the
        service. For more information, see `View service history using Amazon
        ECS service
        deployments <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-deployment.html>`__.

        :param service_deployment_arns: The ARN of the service deployment.
        :returns: DescribeServiceDeploymentsResponse
        :raises AccessDeniedException:
        :raises ClientException:
        :raises ClusterNotFoundException:
        :raises InvalidParameterException:
        :raises ServerException:
        :raises ServiceNotFoundException:
        :raises UnsupportedFeatureException:
        """
        raise NotImplementedError

    @handler("DescribeServiceRevisions")
    def describe_service_revisions(
        self, context: RequestContext, service_revision_arns: StringList, **kwargs
    ) -> DescribeServiceRevisionsResponse:
        """Describes one or more service revisions.

        A service revision is a version of the service that includes the values
        for the Amazon ECS resources (for example, task definition) and the
        environment resources (for example, load balancers, subnets, and
        security groups). For more information, see `Amazon ECS service
        revisions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-revision.html>`__.

        You can't describe a service revision that was created before October
        25, 2024.

        :param service_revision_arns: The ARN of the service revision.
        :returns: DescribeServiceRevisionsResponse
        :raises AccessDeniedException:
        :raises ClientException:
        :raises ClusterNotFoundException:
        :raises InvalidParameterException:
        :raises ServerException:
        :raises ServiceNotFoundException:
        :raises UnsupportedFeatureException:
        """
        raise NotImplementedError

    @handler("DescribeServices")
    def describe_services(
        self,
        context: RequestContext,
        services: StringList,
        cluster: String | None = None,
        include: ServiceFieldList | None = None,
        **kwargs,
    ) -> DescribeServicesResponse:
        """Describes the specified services running in your cluster.

        :param services: A list of services to describe.
        :param cluster: The short name or full Amazon Resource Name (ARN)the cluster that hosts
        the service to describe.
        :param include: Determines whether you want to see the resource tags for the service.
        :returns: DescribeServicesResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeTaskDefinition")
    def describe_task_definition(
        self,
        context: RequestContext,
        task_definition: String,
        include: TaskDefinitionFieldList | None = None,
        **kwargs,
    ) -> DescribeTaskDefinitionResponse:
        """Describes a task definition. You can specify a ``family`` and
        ``revision`` to find information about a specific task definition, or
        you can simply specify the family to find the latest ``ACTIVE`` revision
        in that family.

        You can only describe ``INACTIVE`` task definitions while an active task
        or service references them.

        :param task_definition: The ``family`` for the latest ``ACTIVE`` revision, ``family`` and
        ``revision`` (``family:revision``) for a specific revision in the
        family, or full Amazon Resource Name (ARN) of the task definition to
        describe.
        :param include: Determines whether to see the resource tags for the task definition.
        :returns: DescribeTaskDefinitionResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("DescribeTaskSets")
    def describe_task_sets(
        self,
        context: RequestContext,
        cluster: String,
        service: String,
        task_sets: StringList | None = None,
        include: TaskSetFieldList | None = None,
        **kwargs,
    ) -> DescribeTaskSetsResponse:
        """Describes the task sets in the specified cluster and service. This is
        used when a service uses the ``EXTERNAL`` deployment controller type.
        For more information, see `Amazon ECS Deployment
        Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster that
        hosts the service that the task sets exist in.
        :param service: The short name or full Amazon Resource Name (ARN) of the service that
        the task sets exist in.
        :param task_sets: The ID or full Amazon Resource Name (ARN) of task sets to describe.
        :param include: Specifies whether to see the resource tags for the task set.
        :returns: DescribeTaskSetsResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        :raises UnsupportedFeatureException:
        :raises AccessDeniedException:
        :raises ServiceNotFoundException:
        :raises ServiceNotActiveException:
        """
        raise NotImplementedError

    @handler("DescribeTasks")
    def describe_tasks(
        self,
        context: RequestContext,
        tasks: StringList,
        cluster: String | None = None,
        include: TaskFieldList | None = None,
        **kwargs,
    ) -> DescribeTasksResponse:
        """Describes a specified task or tasks.

        Currently, stopped tasks appear in the returned results for at least one
        hour.

        If you have tasks with tags, and then delete the cluster, the tagged
        tasks are returned in the response. If you create a new cluster with the
        same name as the deleted cluster, the tagged tasks are not included in
        the response.

        :param tasks: A list of up to 100 task IDs or full ARN entries.
        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster that
        hosts the task or tasks to describe.
        :param include: Specifies whether you want to see the resource tags for the task.
        :returns: DescribeTasksResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        """
        raise NotImplementedError

    @handler("DiscoverPollEndpoint")
    def discover_poll_endpoint(
        self,
        context: RequestContext,
        container_instance: String | None = None,
        cluster: String | None = None,
        **kwargs,
    ) -> DiscoverPollEndpointResponse:
        """This action is only used by the Amazon ECS agent, and it is not intended
        for use outside of the agent.

        Returns an endpoint for the Amazon ECS agent to poll for updates.

        :param container_instance: The container instance ID or full ARN of the container instance.
        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster that
        the container instance belongs to.
        :returns: DiscoverPollEndpointResponse
        :raises ServerException:
        :raises ClientException:
        """
        raise NotImplementedError

    @handler("ExecuteCommand")
    def execute_command(
        self,
        context: RequestContext,
        command: String,
        interactive: Boolean,
        task: String,
        cluster: String | None = None,
        container: String | None = None,
        **kwargs,
    ) -> ExecuteCommandResponse:
        """Runs a command remotely on a container within a task.

        If you use a condition key in your IAM policy to refine the conditions
        for the policy statement, for example limit the actions to a specific
        cluster, you receive an ``AccessDeniedException`` when there is a
        mismatch between the condition key value and the corresponding parameter
        value.

        For information about required permissions and considerations, see
        `Using Amazon ECS Exec for
        debugging <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-exec.html>`__
        in the *Amazon ECS Developer Guide*.

        :param command: The command to run on the container.
        :param interactive: Use this flag to run your command in interactive mode.
        :param task: The Amazon Resource Name (ARN) or ID of the task the container is part
        of.
        :param cluster: The Amazon Resource Name (ARN) or short name of the cluster the task is
        running in.
        :param container: The name of the container to execute the command on.
        :returns: ExecuteCommandResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises AccessDeniedException:
        :raises ClusterNotFoundException:
        :raises TargetNotConnectedException:
        """
        raise NotImplementedError

    @handler("GetTaskProtection")
    def get_task_protection(
        self, context: RequestContext, cluster: String, tasks: StringList | None = None, **kwargs
    ) -> GetTaskProtectionResponse:
        """Retrieves the protection status of tasks in an Amazon ECS service.

        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster that
        hosts the service that the task sets exist in.
        :param tasks: A list of up to 100 task IDs or full ARN entries.
        :returns: GetTaskProtectionResponse
        :raises AccessDeniedException:
        :raises ClientException:
        :raises ClusterNotFoundException:
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises ServerException:
        :raises UnsupportedFeatureException:
        """
        raise NotImplementedError

    @handler("ListAccountSettings")
    def list_account_settings(
        self,
        context: RequestContext,
        name: SettingName | None = None,
        value: String | None = None,
        principal_arn: String | None = None,
        effective_settings: Boolean | None = None,
        next_token: String | None = None,
        max_results: Integer | None = None,
        **kwargs,
    ) -> ListAccountSettingsResponse:
        """Lists the account settings for a specified principal.

        :param name: The name of the account setting you want to list the settings for.
        :param value: The value of the account settings to filter results with.
        :param principal_arn: The ARN of the principal, which can be a user, role, or the root user.
        :param effective_settings: Determines whether to return the effective settings.
        :param next_token: The ``nextToken`` value returned from a ``ListAccountSettings`` request
        indicating that more results are available to fulfill the request and
        further calls will be needed.
        :param max_results: The maximum number of account setting results returned by
        ``ListAccountSettings`` in paginated output.
        :returns: ListAccountSettingsResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("ListAttributes")
    def list_attributes(
        self,
        context: RequestContext,
        target_type: TargetType,
        cluster: String | None = None,
        attribute_name: String | None = None,
        attribute_value: String | None = None,
        next_token: String | None = None,
        max_results: BoxedInteger | None = None,
        **kwargs,
    ) -> ListAttributesResponse:
        """Lists the attributes for Amazon ECS resources within a specified target
        type and cluster. When you specify a target type and cluster,
        ``ListAttributes`` returns a list of attribute objects, one for each
        attribute on each resource. You can filter the list of results to a
        single attribute name to only return results that have that name. You
        can also filter the results by attribute name and value. You can do
        this, for example, to see which container instances in a cluster are
        running a Linux AMI (``ecs.os-type=linux``).

        :param target_type: The type of the target to list attributes with.
        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster to list
        attributes.
        :param attribute_name: The name of the attribute to filter the results with.
        :param attribute_value: The value of the attribute to filter results with.
        :param next_token: The ``nextToken`` value returned from a ``ListAttributes`` request
        indicating that more results are available to fulfill the request and
        further calls are needed.
        :param max_results: The maximum number of cluster results that ``ListAttributes`` returned
        in paginated output.
        :returns: ListAttributesResponse
        :raises ClusterNotFoundException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("ListClusters")
    def list_clusters(
        self,
        context: RequestContext,
        next_token: String | None = None,
        max_results: BoxedInteger | None = None,
        **kwargs,
    ) -> ListClustersResponse:
        """Returns a list of existing clusters.

        :param next_token: The ``nextToken`` value returned from a ``ListClusters`` request
        indicating that more results are available to fulfill the request and
        further calls are needed.
        :param max_results: The maximum number of cluster results that ``ListClusters`` returned in
        paginated output.
        :returns: ListClustersResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("ListContainerInstances")
    def list_container_instances(
        self,
        context: RequestContext,
        cluster: String | None = None,
        filter: String | None = None,
        next_token: String | None = None,
        max_results: BoxedInteger | None = None,
        status: ContainerInstanceStatus | None = None,
        **kwargs,
    ) -> ListContainerInstancesResponse:
        """Returns a list of container instances in a specified cluster. You can
        filter the results of a ``ListContainerInstances`` operation with
        cluster query language statements inside the ``filter`` parameter. For
        more information, see `Cluster Query
        Language <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-query-language.html>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster that
        hosts the container instances to list.
        :param filter: You can filter the results of a ``ListContainerInstances`` operation
        with cluster query language statements.
        :param next_token: The ``nextToken`` value returned from a ``ListContainerInstances``
        request indicating that more results are available to fulfill the
        request and further calls are needed.
        :param max_results: The maximum number of container instance results that
        ``ListContainerInstances`` returned in paginated output.
        :param status: Filters the container instances by status.
        :returns: ListContainerInstancesResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        """
        raise NotImplementedError

    @handler("ListServiceDeployments")
    def list_service_deployments(
        self,
        context: RequestContext,
        service: String,
        cluster: String | None = None,
        status: ServiceDeploymentStatusList | None = None,
        created_at: CreatedAt | None = None,
        next_token: String | None = None,
        max_results: BoxedInteger | None = None,
        **kwargs,
    ) -> ListServiceDeploymentsResponse:
        """This operation lists all the service deployments that meet the specified
        filter criteria.

        A service deployment happens when you release a software update for the
        service. You route traffic from the running service revisions to the new
        service revison and control the number of running tasks.

        This API returns the values that you use for the request parameters in
        `DescribeServiceRevisions <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_DescribeServiceRevisions.html>`__.

        :param service: The ARN or name of the service.
        :param cluster: The cluster that hosts the service.
        :param status: An optional filter you can use to narrow the results.
        :param created_at: An optional filter you can use to narrow the results by the service
        creation date.
        :param next_token: The ``nextToken`` value returned from a ``ListServiceDeployments``
        request indicating that more results are available to fulfill the
        request and further calls are needed.
        :param max_results: The maximum number of service deployment results that
        ``ListServiceDeployments`` returned in paginated output.
        :returns: ListServiceDeploymentsResponse
        :raises AccessDeniedException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ServerException:
        :raises ServiceNotFoundException:
        :raises UnsupportedFeatureException:
        """
        raise NotImplementedError

    @handler("ListServices")
    def list_services(
        self,
        context: RequestContext,
        cluster: String | None = None,
        next_token: String | None = None,
        max_results: BoxedInteger | None = None,
        launch_type: LaunchType | None = None,
        scheduling_strategy: SchedulingStrategy | None = None,
        resource_management_type: ResourceManagementType | None = None,
        **kwargs,
    ) -> ListServicesResponse:
        """Returns a list of services. You can filter the results by cluster,
        launch type, and scheduling strategy.

        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster to use
        when filtering the ``ListServices`` results.
        :param next_token: The ``nextToken`` value returned from a ``ListServices`` request
        indicating that more results are available to fulfill the request and
        further calls will be needed.
        :param max_results: The maximum number of service results that ``ListServices`` returned in
        paginated output.
        :param launch_type: The launch type to use when filtering the ``ListServices`` results.
        :param scheduling_strategy: The scheduling strategy to use when filtering the ``ListServices``
        results.
        :param resource_management_type: The resourceManagementType type to use when filtering the
        ``ListServices`` results.
        :returns: ListServicesResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        """
        raise NotImplementedError

    @handler("ListServicesByNamespace")
    def list_services_by_namespace(
        self,
        context: RequestContext,
        namespace: String,
        next_token: String | None = None,
        max_results: BoxedInteger | None = None,
        **kwargs,
    ) -> ListServicesByNamespaceResponse:
        """This operation lists all of the services that are associated with a
        Cloud Map namespace. This list might include services in different
        clusters. In contrast, ``ListServices`` can only list services in one
        cluster at a time. If you need to filter the list of services in a
        single cluster by various parameters, use ``ListServices``. For more
        information, see `Service
        Connect <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-connect.html>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        :param namespace: The namespace name or full Amazon Resource Name (ARN) of the Cloud Map
        namespace to list the services in.
        :param next_token: The ``nextToken`` value that's returned from a
        ``ListServicesByNamespace`` request.
        :param max_results: The maximum number of service results that ``ListServicesByNamespace``
        returns in paginated output.
        :returns: ListServicesByNamespaceResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises NamespaceNotFoundException:
        """
        raise NotImplementedError

    @handler("ListTagsForResource")
    def list_tags_for_resource(
        self, context: RequestContext, resource_arn: String, **kwargs
    ) -> ListTagsForResourceResponse:
        """List the tags for an Amazon ECS resource.

        :param resource_arn: The Amazon Resource Name (ARN) that identifies the resource to list the
        tags for.
        :returns: ListTagsForResourceResponse
        :raises ServerException:
        :raises ClientException:
        :raises ClusterNotFoundException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("ListTaskDefinitionFamilies")
    def list_task_definition_families(
        self,
        context: RequestContext,
        family_prefix: String | None = None,
        status: TaskDefinitionFamilyStatus | None = None,
        next_token: String | None = None,
        max_results: BoxedInteger | None = None,
        **kwargs,
    ) -> ListTaskDefinitionFamiliesResponse:
        """Returns a list of task definition families that are registered to your
        account. This list includes task definition families that no longer have
        any ``ACTIVE`` task definition revisions.

        You can filter out task definition families that don't contain any
        ``ACTIVE`` task definition revisions by setting the ``status`` parameter
        to ``ACTIVE``. You can also filter the results with the ``familyPrefix``
        parameter.

        :param family_prefix: The ``familyPrefix`` is a string that's used to filter the results of
        ``ListTaskDefinitionFamilies``.
        :param status: The task definition family status to filter the
        ``ListTaskDefinitionFamilies`` results with.
        :param next_token: The ``nextToken`` value returned from a ``ListTaskDefinitionFamilies``
        request indicating that more results are available to fulfill the
        request and further calls will be needed.
        :param max_results: The maximum number of task definition family results that
        ``ListTaskDefinitionFamilies`` returned in paginated output.
        :returns: ListTaskDefinitionFamiliesResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("ListTaskDefinitions")
    def list_task_definitions(
        self,
        context: RequestContext,
        family_prefix: String | None = None,
        status: TaskDefinitionStatus | None = None,
        sort: SortOrder | None = None,
        next_token: String | None = None,
        max_results: BoxedInteger | None = None,
        **kwargs,
    ) -> ListTaskDefinitionsResponse:
        """Returns a list of task definitions that are registered to your account.
        You can filter the results by family name with the ``familyPrefix``
        parameter or by status with the ``status`` parameter.

        :param family_prefix: The full family name to filter the ``ListTaskDefinitions`` results with.
        :param status: The task definition status to filter the ``ListTaskDefinitions`` results
        with.
        :param sort: The order to sort the results in.
        :param next_token: The ``nextToken`` value returned from a ``ListTaskDefinitions`` request
        indicating that more results are available to fulfill the request and
        further calls will be needed.
        :param max_results: The maximum number of task definition results that
        ``ListTaskDefinitions`` returned in paginated output.
        :returns: ListTaskDefinitionsResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("ListTasks")
    def list_tasks(
        self,
        context: RequestContext,
        cluster: String | None = None,
        container_instance: String | None = None,
        family: String | None = None,
        next_token: String | None = None,
        max_results: BoxedInteger | None = None,
        started_by: String | None = None,
        service_name: String | None = None,
        desired_status: DesiredStatus | None = None,
        launch_type: LaunchType | None = None,
        **kwargs,
    ) -> ListTasksResponse:
        """Returns a list of tasks. You can filter the results by cluster, task
        definition family, container instance, launch type, what IAM principal
        started the task, or by the desired status of the task.

        Recently stopped tasks might appear in the returned results.

        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster to use
        when filtering the ``ListTasks`` results.
        :param container_instance: The container instance ID or full ARN of the container instance to use
        when filtering the ``ListTasks`` results.
        :param family: The name of the task definition family to use when filtering the
        ``ListTasks`` results.
        :param next_token: The ``nextToken`` value returned from a ``ListTasks`` request indicating
        that more results are available to fulfill the request and further calls
        will be needed.
        :param max_results: The maximum number of task results that ``ListTasks`` returned in
        paginated output.
        :param started_by: The ``startedBy`` value to filter the task results with.
        :param service_name: The name of the service to use when filtering the ``ListTasks`` results.
        :param desired_status: The task desired status to use when filtering the ``ListTasks`` results.
        :param launch_type: The launch type to use when filtering the ``ListTasks`` results.
        :returns: ListTasksResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        :raises ServiceNotFoundException:
        """
        raise NotImplementedError

    @handler("PutAccountSetting")
    def put_account_setting(
        self,
        context: RequestContext,
        name: SettingName,
        value: String,
        principal_arn: String | None = None,
        **kwargs,
    ) -> PutAccountSettingResponse:
        """Modifies an account setting. Account settings are set on a per-Region
        basis.

        If you change the root user account setting, the default settings are
        reset for users and roles that do not have specified individual account
        settings. For more information, see `Account
        Settings <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-account-settings.html>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        :param name: The Amazon ECS account setting name to modify.
        :param value: The account setting value for the specified principal ARN.
        :param principal_arn: The ARN of the principal, which can be a user, role, or the root user.
        :returns: PutAccountSettingResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("PutAccountSettingDefault")
    def put_account_setting_default(
        self, context: RequestContext, name: SettingName, value: String, **kwargs
    ) -> PutAccountSettingDefaultResponse:
        """Modifies an account setting for all users on an account for whom no
        individual account setting has been specified. Account settings are set
        on a per-Region basis.

        :param name: The resource name for which to modify the account setting.
        :param value: The account setting value for the specified principal ARN.
        :returns: PutAccountSettingDefaultResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("PutAttributes")
    def put_attributes(
        self,
        context: RequestContext,
        attributes: Attributes,
        cluster: String | None = None,
        **kwargs,
    ) -> PutAttributesResponse:
        """Create or update an attribute on an Amazon ECS resource. If the
        attribute doesn't exist, it's created. If the attribute exists, its
        value is replaced with the specified value. To delete an attribute, use
        `DeleteAttributes <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_DeleteAttributes.html>`__.
        For more information, see
        `Attributes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement-constraints.html#attributes>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        :param attributes: The attributes to apply to your resource.
        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster that
        contains the resource to apply attributes.
        :returns: PutAttributesResponse
        :raises ClusterNotFoundException:
        :raises TargetNotFoundException:
        :raises AttributeLimitExceededException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("PutClusterCapacityProviders")
    def put_cluster_capacity_providers(
        self,
        context: RequestContext,
        cluster: String,
        capacity_providers: StringList,
        default_capacity_provider_strategy: CapacityProviderStrategy,
        **kwargs,
    ) -> PutClusterCapacityProvidersResponse:
        """Modifies the available capacity providers and the default capacity
        provider strategy for a cluster.

        You must specify both the available capacity providers and a default
        capacity provider strategy for the cluster. If the specified cluster has
        existing capacity providers associated with it, you must specify all
        existing capacity providers in addition to any new ones you want to add.
        Any existing capacity providers that are associated with a cluster that
        are omitted from a
        `PutClusterCapacityProviders <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PutClusterCapacityProviders.html>`__
        API call will be disassociated with the cluster. You can only
        disassociate an existing capacity provider from a cluster if it's not
        being used by any existing tasks.

        When creating a service or running a task on a cluster, if no capacity
        provider or launch type is specified, then the cluster's default
        capacity provider strategy is used. We recommend that you define a
        default capacity provider strategy for your cluster. However, you must
        specify an empty array (``[]``) to bypass defining a default strategy.

        Amazon ECS Managed Instances doesn't support this, because when you
        create a capacity provider with Amazon ECS Managed Instances, it becomes
        available only within the specified cluster.

        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster to
        modify the capacity provider settings for.
        :param capacity_providers: The name of one or more capacity providers to associate with the
        cluster.
        :param default_capacity_provider_strategy: The capacity provider strategy to use by default for the cluster.
        :returns: PutClusterCapacityProvidersResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        :raises ResourceInUseException:
        :raises UpdateInProgressException:
        """
        raise NotImplementedError

    @handler("RegisterContainerInstance")
    def register_container_instance(
        self,
        context: RequestContext,
        cluster: String | None = None,
        instance_identity_document: String | None = None,
        instance_identity_document_signature: String | None = None,
        total_resources: Resources | None = None,
        version_info: VersionInfo | None = None,
        container_instance_arn: String | None = None,
        attributes: Attributes | None = None,
        platform_devices: PlatformDevices | None = None,
        tags: Tags | None = None,
        **kwargs,
    ) -> RegisterContainerInstanceResponse:
        """This action is only used by the Amazon ECS agent, and it is not intended
        for use outside of the agent.

        Registers an EC2 instance into the specified cluster. This instance
        becomes available to place containers on.

        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster to
        register your container instance with.
        :param instance_identity_document: The instance identity document for the EC2 instance to register.
        :param instance_identity_document_signature: The instance identity document signature for the EC2 instance to
        register.
        :param total_resources: The resources available on the instance.
        :param version_info: The version information for the Amazon ECS container agent and Docker
        daemon that runs on the container instance.
        :param container_instance_arn: The ARN of the container instance (if it was previously registered).
        :param attributes: The container instance attributes that this container instance supports.
        :param platform_devices: The devices that are available on the container instance.
        :param tags: The metadata that you apply to the container instance to help you
        categorize and organize them.
        :returns: RegisterContainerInstanceResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("RegisterTaskDefinition")
    def register_task_definition(
        self,
        context: RequestContext,
        family: String,
        container_definitions: ContainerDefinitions,
        task_role_arn: String | None = None,
        execution_role_arn: String | None = None,
        network_mode: NetworkMode | None = None,
        volumes: VolumeList | None = None,
        placement_constraints: TaskDefinitionPlacementConstraints | None = None,
        requires_compatibilities: CompatibilityList | None = None,
        cpu: String | None = None,
        memory: String | None = None,
        tags: Tags | None = None,
        pid_mode: PidMode | None = None,
        ipc_mode: IpcMode | None = None,
        proxy_configuration: ProxyConfiguration | None = None,
        inference_accelerators: InferenceAccelerators | None = None,
        ephemeral_storage: EphemeralStorage | None = None,
        runtime_platform: RuntimePlatform | None = None,
        enable_fault_injection: BoxedBoolean | None = None,
        **kwargs,
    ) -> RegisterTaskDefinitionResponse:
        """Registers a new task definition from the supplied ``family`` and
        ``containerDefinitions``. Optionally, you can add data volumes to your
        containers with the ``volumes`` parameter. For more information about
        task definition parameters and defaults, see `Amazon ECS Task
        Definitions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_defintions.html>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        You can specify a role for your task with the ``taskRoleArn`` parameter.
        When you specify a role for a task, its containers can then use the
        latest versions of the CLI or SDKs to make API requests to the Amazon
        Web Services services that are specified in the policy that's associated
        with the role. For more information, see `IAM Roles for
        Tasks <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        You can specify a Docker networking mode for the containers in your task
        definition with the ``networkMode`` parameter. If you specify the
        ``awsvpc`` network mode, the task is allocated an elastic network
        interface, and you must specify a
        `NetworkConfiguration <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_NetworkConfiguration.html>`__
        when you create a service or run a task with the task definition. For
        more information, see `Task
        Networking <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-networking.html>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        :param family: You must specify a ``family`` for a task definition.
        :param container_definitions: A list of container definitions in JSON format that describe the
        different containers that make up your task.
        :param task_role_arn: The short name or full Amazon Resource Name (ARN) of the IAM role that
        containers in this task can assume.
        :param execution_role_arn: The Amazon Resource Name (ARN) of the task execution role that grants
        the Amazon ECS container agent permission to make Amazon Web Services
        API calls on your behalf.
        :param network_mode: The Docker networking mode to use for the containers in the task.
        :param volumes: A list of volume definitions in JSON format that containers in your task
        might use.
        :param placement_constraints: An array of placement constraint objects to use for the task.
        :param requires_compatibilities: The task launch type that Amazon ECS validates the task definition
        against.
        :param cpu: The number of CPU units used by the task.
        :param memory: The amount of memory (in MiB) used by the task.
        :param tags: The metadata that you apply to the task definition to help you
        categorize and organize them.
        :param pid_mode: The process namespace to use for the containers in the task.
        :param ipc_mode: The IPC resource namespace to use for the containers in the task.
        :param proxy_configuration: The configuration details for the App Mesh proxy.
        :param inference_accelerators: The Elastic Inference accelerators to use for the containers in the
        task.
        :param ephemeral_storage: The amount of ephemeral storage to allocate for the task.
        :param runtime_platform: The operating system that your tasks definitions run on.
        :param enable_fault_injection: Enables fault injection when you register your task definition and
        allows for fault injection requests to be accepted from the task's
        containers.
        :returns: RegisterTaskDefinitionResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("RunTask")
    def run_task(
        self,
        context: RequestContext,
        task_definition: String,
        capacity_provider_strategy: CapacityProviderStrategy | None = None,
        cluster: String | None = None,
        count: BoxedInteger | None = None,
        enable_ecs_managed_tags: Boolean | None = None,
        enable_execute_command: Boolean | None = None,
        group: String | None = None,
        launch_type: LaunchType | None = None,
        network_configuration: NetworkConfiguration | None = None,
        overrides: TaskOverride | None = None,
        placement_constraints: PlacementConstraints | None = None,
        placement_strategy: PlacementStrategies | None = None,
        platform_version: String | None = None,
        propagate_tags: PropagateTags | None = None,
        reference_id: String | None = None,
        started_by: String | None = None,
        tags: Tags | None = None,
        client_token: String | None = None,
        volume_configurations: TaskVolumeConfigurations | None = None,
        **kwargs,
    ) -> RunTaskResponse:
        """Starts a new task using the specified task definition.

        On March 21, 2024, a change was made to resolve the task definition
        revision before authorization. When a task definition revision is not
        specified, authorization will occur using the latest revision of a task
        definition.

        Amazon Elastic Inference (EI) is no longer available to customers.

        You can allow Amazon ECS to place tasks for you, or you can customize
        how Amazon ECS places tasks using placement constraints and placement
        strategies. For more information, see `Scheduling
        Tasks <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/scheduling_tasks.html>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        Alternatively, you can use ``StartTask`` to use your own scheduler or
        place tasks manually on specific container instances.

        You can attach Amazon EBS volumes to Amazon ECS tasks by configuring the
        volume when creating or updating a service. For more information, see
        `Amazon EBS
        volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ebs-volumes.html#ebs-volume-types>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        The Amazon ECS API follows an eventual consistency model. This is
        because of the distributed nature of the system supporting the API. This
        means that the result of an API command you run that affects your Amazon
        ECS resources might not be immediately visible to all subsequent
        commands you run. Keep this in mind when you carry out an API command
        that immediately follows a previous API command.

        To manage eventual consistency, you can do the following:

        -  Confirm the state of the resource before you run a command to modify
           it. Run the DescribeTasks command using an exponential backoff
           algorithm to ensure that you allow enough time for the previous
           command to propagate through the system. To do this, run the
           DescribeTasks command repeatedly, starting with a couple of seconds
           of wait time and increasing gradually up to five minutes of wait
           time.

        -  Add wait time between subsequent commands, even if the DescribeTasks
           command returns an accurate response. Apply an exponential backoff
           algorithm starting with a couple of seconds of wait time, and
           increase gradually up to about five minutes of wait time.

        If you get a ``ConflictException`` error, the ``RunTask`` request could
        not be processed due to conflicts. The provided ``clientToken`` is
        already in use with a different ``RunTask`` request. The ``resourceIds``
        are the existing task ARNs which are already associated with the
        ``clientToken``.

        To fix this issue:

        -  Run ``RunTask`` with a unique ``clientToken``.

        -  Run ``RunTask`` with the ``clientToken`` and the original set of
           parameters

        If you get a ``ClientException`` error, the ``RunTask`` could not be
        processed because you use managed scaling and there is a capacity error
        because the quota of tasks in the ``PROVISIONING`` per cluster has been
        reached. For information about the service quotas, see `Amazon ECS
        service
        quotas <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-quotas.html>`__.

        :param task_definition: The ``family`` and ``revision`` (``family:revision``) or full ARN of the
        task definition to run.
        :param capacity_provider_strategy: The capacity provider strategy to use for the task.
        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster to run
        your task on.
        :param count: The number of instantiations of the specified task to place on your
        cluster.
        :param enable_ecs_managed_tags: Specifies whether to use Amazon ECS managed tags for the task.
        :param enable_execute_command: Determines whether to use the execute command functionality for the
        containers in this task.
        :param group: The name of the task group to associate with the task.
        :param launch_type: The infrastructure to run your standalone task on.
        :param network_configuration: The network configuration for the task.
        :param overrides: A list of container overrides in JSON format that specify the name of a
        container in the specified task definition and the overrides it should
        receive.
        :param placement_constraints: An array of placement constraint objects to use for the task.
        :param placement_strategy: The placement strategy objects to use for the task.
        :param platform_version: The platform version the task uses.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition to the
        task.
        :param reference_id: This parameter is only used by Amazon ECS.
        :param started_by: An optional tag specified when a task is started.
        :param tags: The metadata that you apply to the task to help you categorize and
        organize them.
        :param client_token: An identifier that you provide to ensure the idempotency of the request.
        :param volume_configurations: The details of the volume that was ``configuredAtLaunch``.
        :returns: RunTaskResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        :raises UnsupportedFeatureException:
        :raises PlatformUnknownException:
        :raises PlatformTaskDefinitionIncompatibilityException:
        :raises AccessDeniedException:
        :raises BlockedException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("StartTask")
    def start_task(
        self,
        context: RequestContext,
        container_instances: StringList,
        task_definition: String,
        cluster: String | None = None,
        enable_ecs_managed_tags: Boolean | None = None,
        enable_execute_command: Boolean | None = None,
        group: String | None = None,
        network_configuration: NetworkConfiguration | None = None,
        overrides: TaskOverride | None = None,
        propagate_tags: PropagateTags | None = None,
        reference_id: String | None = None,
        started_by: String | None = None,
        tags: Tags | None = None,
        volume_configurations: TaskVolumeConfigurations | None = None,
        **kwargs,
    ) -> StartTaskResponse:
        """Starts a new task from the specified task definition on the specified
        container instance or instances.

        On March 21, 2024, a change was made to resolve the task definition
        revision before authorization. When a task definition revision is not
        specified, authorization will occur using the latest revision of a task
        definition.

        Amazon Elastic Inference (EI) is no longer available to customers.

        Alternatively, you can use ``RunTask`` to place tasks for you. For more
        information, see `Scheduling
        Tasks <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/scheduling_tasks.html>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        You can attach Amazon EBS volumes to Amazon ECS tasks by configuring the
        volume when creating or updating a service. For more information, see
        `Amazon EBS
        volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ebs-volumes.html#ebs-volume-types>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        :param container_instances: The container instance IDs or full ARN entries for the container
        instances where you would like to place your task.
        :param task_definition: The ``family`` and ``revision`` (``family:revision``) or full ARN of the
        task definition to start.
        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster where
        to start your task.
        :param enable_ecs_managed_tags: Specifies whether to use Amazon ECS managed tags for the task.
        :param enable_execute_command: Whether or not the execute command functionality is turned on for the
        task.
        :param group: The name of the task group to associate with the task.
        :param network_configuration: The VPC subnet and security group configuration for tasks that receive
        their own elastic network interface by using the ``awsvpc`` networking
        mode.
        :param overrides: A list of container overrides in JSON format that specify the name of a
        container in the specified task definition and the overrides it
        receives.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the
        service to the task.
        :param reference_id: This parameter is only used by Amazon ECS.
        :param started_by: An optional tag specified when a task is started.
        :param tags: The metadata that you apply to the task to help you categorize and
        organize them.
        :param volume_configurations: The details of the volume that was ``configuredAtLaunch``.
        :returns: StartTaskResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        :raises UnsupportedFeatureException:
        """
        raise NotImplementedError

    @handler("StopServiceDeployment")
    def stop_service_deployment(
        self,
        context: RequestContext,
        service_deployment_arn: String,
        stop_type: StopServiceDeploymentStopType | None = None,
        **kwargs,
    ) -> StopServiceDeploymentResponse:
        """Stops an ongoing service deployment.

        The following stop types are avaiable:

        -  ROLLBACK - This option rolls back the service deployment to the
           previous service revision.

           You can use this option even if you didn't configure the service
           deployment for the rollback option.

        For more information, see `Stopping Amazon ECS service
        deployments <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/stop-service-deployment.html>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        :param service_deployment_arn: The ARN of the service deployment that you want to stop.
        :param stop_type: How you want Amazon ECS to stop the service.
        :returns: StopServiceDeploymentResponse
        :raises AccessDeniedException:
        :raises ClientException:
        :raises ConflictException:
        :raises InvalidParameterException:
        :raises ServerException:
        :raises ServiceDeploymentNotFoundException:
        :raises UnsupportedFeatureException:
        """
        raise NotImplementedError

    @handler("StopTask")
    def stop_task(
        self,
        context: RequestContext,
        task: String,
        cluster: String | None = None,
        reason: String | None = None,
        **kwargs,
    ) -> StopTaskResponse:
        """Stops a running task. Any tags associated with the task will be deleted.

        When you call ``StopTask`` on a task, the equivalent of ``docker stop``
        is issued to the containers running in the task. This results in a stop
        signal value and a default 30-second timeout, after which the
        ``SIGKILL`` value is sent and the containers are forcibly stopped. This
        signal can be defined in your container image with the ``STOPSIGNAL``
        instruction and will default to ``SIGTERM``. If the container handles
        the ``SIGTERM`` value gracefully and exits within 30 seconds from
        receiving it, no ``SIGKILL`` value is sent.

        For Windows containers, POSIX signals do not work and runtime stops the
        container by sending a ``CTRL_SHUTDOWN_EVENT``. For more information,
        see `Unable to react to graceful shutdown of (Windows) container
        #25982 <https://github.com/moby/moby/issues/25982>`__ on GitHub.

        The default 30-second timeout can be configured on the Amazon ECS
        container agent with the ``ECS_CONTAINER_STOP_TIMEOUT`` variable. For
        more information, see `Amazon ECS Container Agent
        Configuration <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-agent-config.html>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        :param task: Thefull Amazon Resource Name (ARN) of the task.
        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster that
        hosts the task to stop.
        :param reason: An optional message specified when a task is stopped.
        :returns: StopTaskResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        """
        raise NotImplementedError

    @handler("SubmitAttachmentStateChanges")
    def submit_attachment_state_changes(
        self,
        context: RequestContext,
        attachments: AttachmentStateChanges,
        cluster: String | None = None,
        **kwargs,
    ) -> SubmitAttachmentStateChangesResponse:
        """This action is only used by the Amazon ECS agent, and it is not intended
        for use outside of the agent.

        Sent to acknowledge that an attachment changed states.

        :param attachments: Any attachments associated with the state change request.
        :param cluster: The short name or full ARN of the cluster that hosts the container
        instance the attachment belongs to.
        :returns: SubmitAttachmentStateChangesResponse
        :raises ServerException:
        :raises ClientException:
        :raises AccessDeniedException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("SubmitContainerStateChange")
    def submit_container_state_change(
        self,
        context: RequestContext,
        cluster: String | None = None,
        task: String | None = None,
        container_name: String | None = None,
        runtime_id: String | None = None,
        status: String | None = None,
        exit_code: BoxedInteger | None = None,
        reason: String | None = None,
        network_bindings: NetworkBindings | None = None,
        **kwargs,
    ) -> SubmitContainerStateChangeResponse:
        """This action is only used by the Amazon ECS agent, and it is not intended
        for use outside of the agent.

        Sent to acknowledge that a container changed states.

        :param cluster: The short name or full ARN of the cluster that hosts the container.
        :param task: The task ID or full Amazon Resource Name (ARN) of the task that hosts
        the container.
        :param container_name: The name of the container.
        :param runtime_id: The ID of the Docker container.
        :param status: The status of the state change request.
        :param exit_code: The exit code that's returned for the state change request.
        :param reason: The reason for the state change request.
        :param network_bindings: The network bindings of the container.
        :returns: SubmitContainerStateChangeResponse
        :raises ServerException:
        :raises ClientException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("SubmitTaskStateChange")
    def submit_task_state_change(
        self,
        context: RequestContext,
        cluster: String | None = None,
        task: String | None = None,
        status: String | None = None,
        reason: String | None = None,
        containers: ContainerStateChanges | None = None,
        attachments: AttachmentStateChanges | None = None,
        managed_agents: ManagedAgentStateChanges | None = None,
        pull_started_at: Timestamp | None = None,
        pull_stopped_at: Timestamp | None = None,
        execution_stopped_at: Timestamp | None = None,
        **kwargs,
    ) -> SubmitTaskStateChangeResponse:
        """This action is only used by the Amazon ECS agent, and it is not intended
        for use outside of the agent.

        Sent to acknowledge that a task changed states.

        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster that
        hosts the task.
        :param task: The task ID or full ARN of the task in the state change request.
        :param status: The status of the state change request.
        :param reason: The reason for the state change request.
        :param containers: Any containers that's associated with the state change request.
        :param attachments: Any attachments associated with the state change request.
        :param managed_agents: The details for the managed agent that's associated with the task.
        :param pull_started_at: The Unix timestamp for the time when the container image pull started.
        :param pull_stopped_at: The Unix timestamp for the time when the container image pull completed.
        :param execution_stopped_at: The Unix timestamp for the time when the task execution stopped.
        :returns: SubmitTaskStateChangeResponse
        :raises ServerException:
        :raises ClientException:
        :raises AccessDeniedException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("TagResource")
    def tag_resource(
        self, context: RequestContext, resource_arn: String, tags: Tags, **kwargs
    ) -> TagResourceResponse:
        """Associates the specified tags to a resource with the specified
        ``resourceArn``. If existing tags on a resource aren't specified in the
        request parameters, they aren't changed. When a resource is deleted, the
        tags that are associated with that resource are deleted as well.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource to add tags to.
        :param tags: The tags to add to the resource.
        :returns: TagResourceResponse
        :raises ServerException:
        :raises ClientException:
        :raises ClusterNotFoundException:
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("UntagResource")
    def untag_resource(
        self, context: RequestContext, resource_arn: String, tag_keys: TagKeys, **kwargs
    ) -> UntagResourceResponse:
        """Deletes specified tags from a resource.

        :param resource_arn: The Amazon Resource Name (ARN) of the resource to delete tags from.
        :param tag_keys: The keys of the tags to be removed.
        :returns: UntagResourceResponse
        :raises ServerException:
        :raises ClientException:
        :raises ClusterNotFoundException:
        :raises ResourceNotFoundException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("UpdateCapacityProvider")
    def update_capacity_provider(
        self,
        context: RequestContext,
        name: String,
        cluster: String | None = None,
        auto_scaling_group_provider: AutoScalingGroupProviderUpdate | None = None,
        managed_instances_provider: UpdateManagedInstancesProviderConfiguration | None = None,
        **kwargs,
    ) -> UpdateCapacityProviderResponse:
        """Modifies the parameters for a capacity provider.

        These changes only apply to new Amazon ECS Managed Instances, or EC2
        instances, not existing ones.

        :param name: The name of the capacity provider to update.
        :param cluster: The name of the cluster that contains the capacity provider to update.
        :param auto_scaling_group_provider: An object that represent the parameters to update for the Auto Scaling
        group capacity provider.
        :param managed_instances_provider: The updated configuration for the Amazon ECS Managed Instances provider.
        :returns: UpdateCapacityProviderResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises UnsupportedFeatureException:
        :raises ClusterNotFoundException:
        """
        raise NotImplementedError

    @handler("UpdateCluster")
    def update_cluster(
        self,
        context: RequestContext,
        cluster: String,
        settings: ClusterSettings | None = None,
        configuration: ClusterConfiguration | None = None,
        service_connect_defaults: ClusterServiceConnectDefaultsRequest | None = None,
        **kwargs,
    ) -> UpdateClusterResponse:
        """Updates the cluster.

        :param cluster: The name of the cluster to modify the settings for.
        :param settings: The cluster settings for your cluster.
        :param configuration: The execute command configuration for the cluster.
        :param service_connect_defaults: Use this parameter to set a default Service Connect namespace.
        :returns: UpdateClusterResponse
        :raises ServerException:
        :raises ClientException:
        :raises ClusterNotFoundException:
        :raises InvalidParameterException:
        :raises NamespaceNotFoundException:
        """
        raise NotImplementedError

    @handler("UpdateClusterSettings")
    def update_cluster_settings(
        self, context: RequestContext, cluster: String, settings: ClusterSettings, **kwargs
    ) -> UpdateClusterSettingsResponse:
        """Modifies the settings to use for a cluster.

        :param cluster: The name of the cluster to modify the settings for.
        :param settings: The setting to use by default for a cluster.
        :returns: UpdateClusterSettingsResponse
        :raises ServerException:
        :raises ClientException:
        :raises ClusterNotFoundException:
        :raises InvalidParameterException:
        """
        raise NotImplementedError

    @handler("UpdateContainerAgent")
    def update_container_agent(
        self,
        context: RequestContext,
        container_instance: String,
        cluster: String | None = None,
        **kwargs,
    ) -> UpdateContainerAgentResponse:
        """Updates the Amazon ECS container agent on a specified container
        instance. Updating the Amazon ECS container agent doesn't interrupt
        running tasks or services on the container instance. The process for
        updating the agent differs depending on whether your container instance
        was launched with the Amazon ECS-optimized AMI or another operating
        system.

        The ``UpdateContainerAgent`` API isn't supported for container instances
        using the Amazon ECS-optimized Amazon Linux 2 (arm64) AMI. To update the
        container agent, you can update the ``ecs-init`` package. This updates
        the agent. For more information, see `Updating the Amazon ECS container
        agent <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/agent-update-ecs-ami.html>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        Agent updates with the ``UpdateContainerAgent`` API operation do not
        apply to Windows container instances. We recommend that you launch new
        container instances to update the agent version in your Windows
        clusters.

        The ``UpdateContainerAgent`` API requires an Amazon ECS-optimized AMI or
        Amazon Linux AMI with the ``ecs-init`` service installed and running.
        For help updating the Amazon ECS container agent on other operating
        systems, see `Manually updating the Amazon ECS container
        agent <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-agent-update.html#manually_update_agent>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        :param container_instance: The container instance ID or full ARN entries for the container instance
        where you would like to update the Amazon ECS container agent.
        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster that
        your container instance is running on.
        :returns: UpdateContainerAgentResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        :raises UpdateInProgressException:
        :raises NoUpdateAvailableException:
        :raises MissingVersionException:
        """
        raise NotImplementedError

    @handler("UpdateContainerInstancesState")
    def update_container_instances_state(
        self,
        context: RequestContext,
        container_instances: StringList,
        status: ContainerInstanceStatus,
        cluster: String | None = None,
        **kwargs,
    ) -> UpdateContainerInstancesStateResponse:
        """Modifies the status of an Amazon ECS container instance.

        Once a container instance has reached an ``ACTIVE`` state, you can
        change the status of a container instance to ``DRAINING`` to manually
        remove an instance from a cluster, for example to perform system
        updates, update the Docker daemon, or scale down the cluster size.

        A container instance can't be changed to ``DRAINING`` until it has
        reached an ``ACTIVE`` status. If the instance is in any other status, an
        error will be received.

        When you set a container instance to ``DRAINING``, Amazon ECS prevents
        new tasks from being scheduled for placement on the container instance
        and replacement service tasks are started on other container instances
        in the cluster if the resources are available. Service tasks on the
        container instance that are in the ``PENDING`` state are stopped
        immediately.

        Service tasks on the container instance that are in the ``RUNNING``
        state are stopped and replaced according to the service's deployment
        configuration parameters, ``minimumHealthyPercent`` and
        ``maximumPercent``. You can change the deployment configuration of your
        service using
        `UpdateService <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_UpdateService.html>`__.

        -  If ``minimumHealthyPercent`` is below 100%, the scheduler can ignore
           ``desiredCount`` temporarily during task replacement. For example,
           ``desiredCount`` is four tasks, a minimum of 50% allows the scheduler
           to stop two existing tasks before starting two new tasks. If the
           minimum is 100%, the service scheduler can't remove existing tasks
           until the replacement tasks are considered healthy. Tasks for
           services that do not use a load balancer are considered healthy if
           they're in the ``RUNNING`` state. Tasks for services that use a load
           balancer are considered healthy if they're in the ``RUNNING`` state
           and are reported as healthy by the load balancer.

        -  The ``maximumPercent`` parameter represents an upper limit on the
           number of running tasks during task replacement. You can use this to
           define the replacement batch size. For example, if ``desiredCount``
           is four tasks, a maximum of 200% starts four new tasks before
           stopping the four tasks to be drained, provided that the cluster
           resources required to do this are available. If the maximum is 100%,
           then replacement tasks can't start until the draining tasks have
           stopped.

        Any ``PENDING`` or ``RUNNING`` tasks that do not belong to a service
        aren't affected. You must wait for them to finish or stop them manually.

        A container instance has completed draining when it has no more
        ``RUNNING`` tasks. You can verify this using
        `ListTasks <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ListTasks.html>`__.

        When a container instance has been drained, you can set a container
        instance to ``ACTIVE`` status and once it has reached that status the
        Amazon ECS scheduler can begin scheduling tasks on the instance again.

        :param container_instances: A list of up to 10 container instance IDs or full ARN entries.
        :param status: The container instance state to update the container instance with.
        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster that
        hosts the container instance to update.
        :returns: UpdateContainerInstancesStateResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        """
        raise NotImplementedError

    @handler("UpdateExpressGatewayService")
    def update_express_gateway_service(
        self,
        context: RequestContext,
        service_arn: String,
        execution_role_arn: String | None = None,
        health_check_path: String | None = None,
        primary_container: ExpressGatewayContainer | None = None,
        task_role_arn: String | None = None,
        network_configuration: ExpressGatewayServiceNetworkConfiguration | None = None,
        cpu: String | None = None,
        memory: String | None = None,
        scaling_target: ExpressGatewayScalingTarget | None = None,
        **kwargs,
    ) -> UpdateExpressGatewayServiceResponse:
        """Updates an existing Express service configuration. Modifies container
        settings, resource allocation, auto-scaling configuration, and other
        service parameters without recreating the service.

        Amazon ECS creates a new service revision with updated configuration and
        performs a rolling deployment to replace existing tasks. The service
        remains available during updates, ensuring zero-downtime deployments.

        Some parameters like the infrastructure role cannot be modified after
        service creation and require creating a new service.

        :param service_arn: The Amazon Resource Name (ARN) of the Express service to update.
        :param execution_role_arn: The Amazon Resource Name (ARN) of the task execution role for the
        Express service.
        :param health_check_path: The path on the container for Application Load Balancer health checks.
        :param primary_container: The primary container configuration for the Express service.
        :param task_role_arn: The Amazon Resource Name (ARN) of the IAM role for containers in this
        task.
        :param network_configuration: The network configuration for the Express service tasks.
        :param cpu: The number of CPU units used by the task.
        :param memory: The amount of memory (in MiB) used by the task.
        :param scaling_target: The auto-scaling configuration for the Express service.
        :returns: UpdateExpressGatewayServiceResponse
        :raises AccessDeniedException:
        :raises ClientException:
        :raises ClusterNotFoundException:
        :raises InvalidParameterException:
        :raises ServerException:
        :raises ServiceNotFoundException:
        :raises ServiceNotActiveException:
        :raises UnsupportedFeatureException:
        """
        raise NotImplementedError

    @handler("UpdateService")
    def update_service(
        self,
        context: RequestContext,
        service: String,
        cluster: String | None = None,
        desired_count: BoxedInteger | None = None,
        task_definition: String | None = None,
        capacity_provider_strategy: CapacityProviderStrategy | None = None,
        deployment_configuration: DeploymentConfiguration | None = None,
        availability_zone_rebalancing: AvailabilityZoneRebalancing | None = None,
        network_configuration: NetworkConfiguration | None = None,
        placement_constraints: PlacementConstraints | None = None,
        placement_strategy: PlacementStrategies | None = None,
        platform_version: String | None = None,
        force_new_deployment: Boolean | None = None,
        health_check_grace_period_seconds: BoxedInteger | None = None,
        deployment_controller: DeploymentController | None = None,
        enable_execute_command: BoxedBoolean | None = None,
        enable_ecs_managed_tags: BoxedBoolean | None = None,
        load_balancers: LoadBalancers | None = None,
        propagate_tags: PropagateTags | None = None,
        service_registries: ServiceRegistries | None = None,
        service_connect_configuration: ServiceConnectConfiguration | None = None,
        volume_configurations: ServiceVolumeConfigurations | None = None,
        vpc_lattice_configurations: VpcLatticeConfigurations | None = None,
        **kwargs,
    ) -> UpdateServiceResponse:
        """Modifies the parameters of a service.

        On March 21, 2024, a change was made to resolve the task definition
        revision before authorization. When a task definition revision is not
        specified, authorization will occur using the latest revision of a task
        definition.

        For services using the rolling update (``ECS``) you can update the
        desired count, deployment configuration, network configuration, load
        balancers, service registries, enable ECS managed tags option, propagate
        tags option, task placement constraints and strategies, and task
        definition. When you update any of these parameters, Amazon ECS starts
        new tasks with the new configuration.

        You can attach Amazon EBS volumes to Amazon ECS tasks by configuring the
        volume when starting or running a task, or when creating or updating a
        service. For more information, see `Amazon EBS
        volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ebs-volumes.html#ebs-volume-types>`__
        in the *Amazon Elastic Container Service Developer Guide*. You can
        update your volume configurations and trigger a new deployment.
        ``volumeConfigurations`` is only supported for REPLICA service and not
        DAEMON service. If you leave ``volumeConfigurations`` ``null``, it
        doesn't trigger a new deployment. For more information on volumes, see
        `Amazon EBS
        volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ebs-volumes.html#ebs-volume-types>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        For services using the blue/green (``CODE_DEPLOY``) deployment
        controller, only the desired count, deployment configuration, health
        check grace period, task placement constraints and strategies, enable
        ECS managed tags option, and propagate tags can be updated using this
        API. If the network configuration, platform version, task definition, or
        load balancer need to be updated, create a new CodeDeploy deployment.
        For more information, see
        `CreateDeployment <https://docs.aws.amazon.com/codedeploy/latest/APIReference/API_CreateDeployment.html>`__
        in the *CodeDeploy API Reference*.

        For services using an external deployment controller, you can update
        only the desired count, task placement constraints and strategies,
        health check grace period, enable ECS managed tags option, and propagate
        tags option, using this API. If the launch type, load balancer, network
        configuration, platform version, or task definition need to be updated,
        create a new task set For more information, see
        `CreateTaskSet <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_CreateTaskSet.html>`__.

        You can add to or subtract from the number of instantiations of a task
        definition in a service by specifying the cluster that the service is
        running in and a new ``desiredCount`` parameter.

        You can attach Amazon EBS volumes to Amazon ECS tasks by configuring the
        volume when starting or running a task, or when creating or updating a
        service. For more information, see `Amazon EBS
        volumes <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ebs-volumes.html#ebs-volume-types>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        If you have updated the container image of your application, you can
        create a new task definition with that image and deploy it to your
        service. The service scheduler uses the minimum healthy percent and
        maximum percent parameters (in the service's deployment configuration)
        to determine the deployment strategy.

        If your updated Docker image uses the same tag as what is in the
        existing task definition for your service (for example,
        ``my_image:latest``), you don't need to create a new revision of your
        task definition. You can update the service using the
        ``forceNewDeployment`` option. The new tasks launched by the deployment
        pull the current image/tag combination from your repository when they
        start.

        You can also update the deployment configuration of a service. When a
        deployment is triggered by updating the task definition of a service,
        the service scheduler uses the deployment configuration parameters,
        ``minimumHealthyPercent`` and ``maximumPercent``, to determine the
        deployment strategy.

        -  If ``minimumHealthyPercent`` is below 100%, the scheduler can ignore
           ``desiredCount`` temporarily during a deployment. For example, if
           ``desiredCount`` is four tasks, a minimum of 50% allows the scheduler
           to stop two existing tasks before starting two new tasks. Tasks for
           services that don't use a load balancer are considered healthy if
           they're in the ``RUNNING`` state. Tasks for services that use a load
           balancer are considered healthy if they're in the ``RUNNING`` state
           and are reported as healthy by the load balancer.

        -  The ``maximumPercent`` parameter represents an upper limit on the
           number of running tasks during a deployment. You can use it to define
           the deployment batch size. For example, if ``desiredCount`` is four
           tasks, a maximum of 200% starts four new tasks before stopping the
           four older tasks (provided that the cluster resources required to do
           this are available).

        When
        `UpdateService <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_UpdateService.html>`__
        stops a task during a deployment, the equivalent of ``docker stop`` is
        issued to the containers running in the task. This results in a
        ``SIGTERM`` and a 30-second timeout. After this, ``SIGKILL`` is sent and
        the containers are forcibly stopped. If the container handles the
        ``SIGTERM`` gracefully and exits within 30 seconds from receiving it, no
        ``SIGKILL`` is sent.

        When the service scheduler launches new tasks, it determines task
        placement in your cluster with the following logic.

        -  Determine which of the container instances in your cluster can
           support your service's task definition. For example, they have the
           required CPU, memory, ports, and container instance attributes.

        -  By default, the service scheduler attempts to balance tasks across
           Availability Zones in this manner even though you can choose a
           different placement strategy.

           -  Sort the valid container instances by the fewest number of running
              tasks for this service in the same Availability Zone as the
              instance. For example, if zone A has one running service task and
              zones B and C each have zero, valid container instances in either
              zone B or C are considered optimal for placement.

           -  Place the new service task on a valid container instance in an
              optimal Availability Zone (based on the previous steps), favoring
              container instances with the fewest number of running tasks for
              this service.

        When the service scheduler stops running tasks, it attempts to maintain
        balance across the Availability Zones in your cluster using the
        following logic:

        -  Sort the container instances by the largest number of running tasks
           for this service in the same Availability Zone as the instance. For
           example, if zone A has one running service task and zones B and C
           each have two, container instances in either zone B or C are
           considered optimal for termination.

        -  Stop the task on a container instance in an optimal Availability Zone
           (based on the previous steps), favoring container instances with the
           largest number of running tasks for this service.

        :param service: The name of the service to update.
        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster that
        your service runs on.
        :param desired_count: The number of instantiations of the task to place and keep running in
        your service.
        :param task_definition: The ``family`` and ``revision`` (``family:revision``) or full ARN of the
        task definition to run in your service.
        :param capacity_provider_strategy: The details of a capacity provider strategy.
        :param deployment_configuration: Optional deployment parameters that control how many tasks run during
        the deployment and the ordering of stopping and starting tasks.
        :param availability_zone_rebalancing: Indicates whether to use Availability Zone rebalancing for the service.
        :param network_configuration: An object representing the network configuration for the service.
        :param placement_constraints: An array of task placement constraint objects to update the service to
        use.
        :param placement_strategy: The task placement strategy objects to update the service to use.
        :param platform_version: The platform version that your tasks in the service run on.
        :param force_new_deployment: Determines whether to force a new deployment of the service.
        :param health_check_grace_period_seconds: The period of time, in seconds, that the Amazon ECS service scheduler
        ignores unhealthy Elastic Load Balancing, VPC Lattice, and container
        health checks after a task has first started.
        :param deployment_controller: The deployment controller to use for the service.
        :param enable_execute_command: If ``true``, this enables execute command functionality on all task
        containers.
        :param enable_ecs_managed_tags: Determines whether to turn on Amazon ECS managed tags for the tasks in
        the service.
        :param load_balancers: You must have a service-linked role when you update this property

        A list of Elastic Load Balancing load balancer objects.
        :param propagate_tags: Determines whether to propagate the tags from the task definition or the
        service to the task.
        :param service_registries: You must have a service-linked role when you update this property.
        :param service_connect_configuration: The configuration for this service to discover and connect to services,
        and be discovered by, and connected from, other services within a
        namespace.
        :param volume_configurations: The details of the volume that was ``configuredAtLaunch``.
        :param vpc_lattice_configurations: An object representing the VPC Lattice configuration for the service
        being updated.
        :returns: UpdateServiceResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        :raises ServiceNotFoundException:
        :raises ServiceNotActiveException:
        :raises PlatformUnknownException:
        :raises PlatformTaskDefinitionIncompatibilityException:
        :raises AccessDeniedException:
        :raises NamespaceNotFoundException:
        :raises UnsupportedFeatureException:
        """
        raise NotImplementedError

    @handler("UpdateServicePrimaryTaskSet")
    def update_service_primary_task_set(
        self,
        context: RequestContext,
        cluster: String,
        service: String,
        primary_task_set: String,
        **kwargs,
    ) -> UpdateServicePrimaryTaskSetResponse:
        """Modifies which task set in a service is the primary task set. Any
        parameters that are updated on the primary task set in a service will
        transition to the service. This is used when a service uses the
        ``EXTERNAL`` deployment controller type. For more information, see
        `Amazon ECS Deployment
        Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster that
        hosts the service that the task set exists in.
        :param service: The short name or full Amazon Resource Name (ARN) of the service that
        the task set exists in.
        :param primary_task_set: The short name or full Amazon Resource Name (ARN) of the task set to set
        as the primary task set in the deployment.
        :returns: UpdateServicePrimaryTaskSetResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        :raises UnsupportedFeatureException:
        :raises ServiceNotFoundException:
        :raises ServiceNotActiveException:
        :raises TaskSetNotFoundException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("UpdateTaskProtection")
    def update_task_protection(
        self,
        context: RequestContext,
        cluster: String,
        tasks: StringList,
        protection_enabled: Boolean,
        expires_in_minutes: BoxedInteger | None = None,
        **kwargs,
    ) -> UpdateTaskProtectionResponse:
        """Updates the protection status of a task. You can set
        ``protectionEnabled`` to ``true`` to protect your task from termination
        during scale-in events from `Service
        Autoscaling <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-auto-scaling.html>`__
        or
        `deployments <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`__.

        Task-protection, by default, expires after 2 hours at which point Amazon
        ECS clears the ``protectionEnabled`` property making the task eligible
        for termination by a subsequent scale-in event.

        You can specify a custom expiration period for task protection from 1
        minute to up to 2,880 minutes (48 hours). To specify the custom
        expiration period, set the ``expiresInMinutes`` property. The
        ``expiresInMinutes`` property is always reset when you invoke this
        operation for a task that already has ``protectionEnabled`` set to
        ``true``. You can keep extending the protection expiration period of a
        task by invoking this operation repeatedly.

        To learn more about Amazon ECS task protection, see `Task scale-in
        protection <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-scale-in-protection.html>`__
        in the *Amazon Elastic Container Service Developer Guide* .

        This operation is only supported for tasks belonging to an Amazon ECS
        service. Invoking this operation for a standalone task will result in an
        ``TASK_NOT_VALID`` failure. For more information, see `API failure
        reasons <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/api_failures_messages.html>`__.

        If you prefer to set task protection from within the container, we
        recommend using the `Task scale-in protection
        endpoint <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-scale-in-protection-endpoint.html>`__.

        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster that
        hosts the service that the task sets exist in.
        :param tasks: A list of up to 10 task IDs or full ARN entries.
        :param protection_enabled: Specify ``true`` to mark a task for protection and ``false`` to unset
        protection, making it eligible for termination.
        :param expires_in_minutes: If you set ``protectionEnabled`` to ``true``, you can specify the
        duration for task protection in minutes.
        :returns: UpdateTaskProtectionResponse
        :raises AccessDeniedException:
        :raises ClientException:
        :raises ClusterNotFoundException:
        :raises InvalidParameterException:
        :raises ResourceNotFoundException:
        :raises ServerException:
        :raises UnsupportedFeatureException:
        """
        raise NotImplementedError

    @handler("UpdateTaskSet")
    def update_task_set(
        self,
        context: RequestContext,
        cluster: String,
        service: String,
        task_set: String,
        scale: Scale,
        **kwargs,
    ) -> UpdateTaskSetResponse:
        """Modifies a task set. This is used when a service uses the ``EXTERNAL``
        deployment controller type. For more information, see `Amazon ECS
        Deployment
        Types <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html>`__
        in the *Amazon Elastic Container Service Developer Guide*.

        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster that
        hosts the service that the task set is found in.
        :param service: The short name or full Amazon Resource Name (ARN) of the service that
        the task set is found in.
        :param task_set: The short name or full Amazon Resource Name (ARN) of the task set to
        update.
        :param scale: A floating-point percentage of the desired number of tasks to place and
        keep running in the task set.
        :returns: UpdateTaskSetResponse
        :raises ServerException:
        :raises ClientException:
        :raises InvalidParameterException:
        :raises ClusterNotFoundException:
        :raises UnsupportedFeatureException:
        :raises AccessDeniedException:
        :raises ServiceNotFoundException:
        :raises ServiceNotActiveException:
        :raises TaskSetNotFoundException:
        """
        raise NotImplementedError
