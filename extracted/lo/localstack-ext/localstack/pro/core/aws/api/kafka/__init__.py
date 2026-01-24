from datetime import datetime
from enum import StrEnum
from typing import TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

MaxResults = int
_boolean = bool
_double = float
_integer = int
_integerMin1Max15 = int
_integerMin1Max16384 = int
_integerMin1 = int
_string = str
_stringMax1024 = str
_stringMax249 = str
_stringMax256 = str
_stringMin1Max128 = str
_stringMin1Max64 = str
_stringMin5Max32 = str
_stringMin1Max128Pattern09AZaZ09AZaZ0 = str


class BrokerAZDistribution(StrEnum):
    DEFAULT = "DEFAULT"


class RebalancingStatus(StrEnum):
    PAUSED = "PAUSED"
    ACTIVE = "ACTIVE"


class ClientBroker(StrEnum):
    TLS = "TLS"
    TLS_PLAINTEXT = "TLS_PLAINTEXT"
    PLAINTEXT = "PLAINTEXT"


class ClusterState(StrEnum):
    ACTIVE = "ACTIVE"
    CREATING = "CREATING"
    DELETING = "DELETING"
    FAILED = "FAILED"
    HEALING = "HEALING"
    MAINTENANCE = "MAINTENANCE"
    REBOOTING_BROKER = "REBOOTING_BROKER"
    UPDATING = "UPDATING"


class ClusterType(StrEnum):
    PROVISIONED = "PROVISIONED"
    SERVERLESS = "SERVERLESS"


class ConfigurationState(StrEnum):
    ACTIVE = "ACTIVE"
    DELETING = "DELETING"
    DELETE_FAILED = "DELETE_FAILED"


class CustomerActionStatus(StrEnum):
    CRITICAL_ACTION_REQUIRED = "CRITICAL_ACTION_REQUIRED"
    ACTION_RECOMMENDED = "ACTION_RECOMMENDED"
    NONE = "NONE"


class EnhancedMonitoring(StrEnum):
    DEFAULT = "DEFAULT"
    PER_BROKER = "PER_BROKER"
    PER_TOPIC_PER_BROKER = "PER_TOPIC_PER_BROKER"
    PER_TOPIC_PER_PARTITION = "PER_TOPIC_PER_PARTITION"


class KafkaVersionStatus(StrEnum):
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"


class NodeType(StrEnum):
    BROKER = "BROKER"


class ReplicationStartingPositionType(StrEnum):
    LATEST = "LATEST"
    EARLIEST = "EARLIEST"


class ReplicationTopicNameConfigurationType(StrEnum):
    PREFIXED_WITH_SOURCE_CLUSTER_ALIAS = "PREFIXED_WITH_SOURCE_CLUSTER_ALIAS"
    IDENTICAL = "IDENTICAL"


class ReplicatorState(StrEnum):
    RUNNING = "RUNNING"
    CREATING = "CREATING"
    UPDATING = "UPDATING"
    DELETING = "DELETING"
    FAILED = "FAILED"


class StorageMode(StrEnum):
    LOCAL = "LOCAL"
    TIERED = "TIERED"


class TargetCompressionType(StrEnum):
    NONE = "NONE"
    GZIP = "GZIP"
    SNAPPY = "SNAPPY"
    LZ4 = "LZ4"
    ZSTD = "ZSTD"


class UserIdentityType(StrEnum):
    AWSACCOUNT = "AWSACCOUNT"
    AWSSERVICE = "AWSSERVICE"


class TopicState(StrEnum):
    CREATING = "CREATING"
    UPDATING = "UPDATING"
    DELETING = "DELETING"
    ACTIVE = "ACTIVE"


class VpcConnectionState(StrEnum):
    CREATING = "CREATING"
    AVAILABLE = "AVAILABLE"
    INACTIVE = "INACTIVE"
    DEACTIVATING = "DEACTIVATING"
    DELETING = "DELETING"
    FAILED = "FAILED"
    REJECTED = "REJECTED"
    REJECTING = "REJECTING"


class BadRequestException(ServiceException):
    """Returns information about an error."""

    code: str = "BadRequestException"
    sender_fault: bool = False
    status_code: int = 400
    InvalidParameter: _string | None


class ConflictException(ServiceException):
    """Returns information about an error."""

    code: str = "ConflictException"
    sender_fault: bool = False
    status_code: int = 409
    InvalidParameter: _string | None


class ForbiddenException(ServiceException):
    """Returns information about an error."""

    code: str = "ForbiddenException"
    sender_fault: bool = False
    status_code: int = 403
    InvalidParameter: _string | None


class InternalServerErrorException(ServiceException):
    """Returns information about an error."""

    code: str = "InternalServerErrorException"
    sender_fault: bool = False
    status_code: int = 500
    InvalidParameter: _string | None


class NotFoundException(ServiceException):
    """Returns information about an error."""

    code: str = "NotFoundException"
    sender_fault: bool = False
    status_code: int = 404
    InvalidParameter: _string | None


class ServiceUnavailableException(ServiceException):
    """Returns information about an error."""

    code: str = "ServiceUnavailableException"
    sender_fault: bool = False
    status_code: int = 503
    InvalidParameter: _string | None


class TooManyRequestsException(ServiceException):
    """Returns information about an error."""

    code: str = "TooManyRequestsException"
    sender_fault: bool = False
    status_code: int = 429
    InvalidParameter: _string | None


class UnauthorizedException(ServiceException):
    """Returns information about an error."""

    code: str = "UnauthorizedException"
    sender_fault: bool = False
    status_code: int = 401
    InvalidParameter: _string | None


class AmazonMskCluster(TypedDict, total=False):
    """Details of an Amazon MSK Cluster."""

    MskClusterArn: _string


_listOf__string = list[_string]


class BatchAssociateScramSecretRequest(ServiceRequest):
    """Associates sasl scram secrets to cluster."""

    ClusterArn: _string
    SecretArnList: _listOf__string


class UnprocessedScramSecret(TypedDict, total=False):
    """Error info for scram secret associate/disassociate failure."""

    ErrorCode: _string | None
    ErrorMessage: _string | None
    SecretArn: _string | None


_listOfUnprocessedScramSecret = list[UnprocessedScramSecret]


class BatchAssociateScramSecretResponse(TypedDict, total=False):
    ClusterArn: _string | None
    UnprocessedScramSecrets: _listOfUnprocessedScramSecret | None


_listOf__double = list[_double]


class BrokerCountUpdateInfo(TypedDict, total=False):
    """Information regarding UpdateBrokerCount."""

    CreatedBrokerIds: _listOf__double | None
    DeletedBrokerIds: _listOf__double | None


class ProvisionedThroughput(TypedDict, total=False):
    """Contains information about provisioned throughput for EBS storage
    volumes attached to kafka broker nodes.
    """

    Enabled: _boolean | None
    VolumeThroughput: _integer | None


class BrokerEBSVolumeInfo(TypedDict, total=False):
    """Specifies the EBS volume upgrade information. The broker identifier must
    be set to the keyword ALL. This means the changes apply to all the
    brokers in the cluster.
    """

    KafkaBrokerNodeId: _string
    ProvisionedThroughput: ProvisionedThroughput | None
    VolumeSizeGB: _integer | None


class S3(TypedDict, total=False):
    Bucket: _string | None
    Enabled: _boolean
    Prefix: _string | None


class Firehose(TypedDict, total=False):
    DeliveryStream: _string | None
    Enabled: _boolean


class CloudWatchLogs(TypedDict, total=False):
    Enabled: _boolean
    LogGroup: _string | None


class BrokerLogs(TypedDict, total=False):
    CloudWatchLogs: CloudWatchLogs | None
    Firehose: Firehose | None
    S3: S3 | None


class Rebalancing(TypedDict, total=False):
    """Specifies whether or not intelligent rebalancing is turned on for a
    newly created MSK Provisioned cluster with Express brokers. Intelligent
    rebalancing performs automatic partition balancing operations when you
    scale your clusters up or down. By default, intelligent rebalancing is
    ACTIVE for all new Express-based clusters.
    """

    Status: RebalancingStatus | None


class VpcConnectivityTls(TypedDict, total=False):
    """Details for TLS client authentication for VPC connectivity."""

    Enabled: _boolean | None


class VpcConnectivityIam(TypedDict, total=False):
    """Details for IAM access control for VPC connectivity."""

    Enabled: _boolean | None


class VpcConnectivityScram(TypedDict, total=False):
    """Details for SASL/SCRAM client authentication for VPC connectivity."""

    Enabled: _boolean | None


class VpcConnectivitySasl(TypedDict, total=False):
    """Details for SASL client authentication for VPC connectivity."""

    Scram: VpcConnectivityScram | None
    Iam: VpcConnectivityIam | None


class VpcConnectivityClientAuthentication(TypedDict, total=False):
    """Includes all client authentication information for VPC connectivity."""

    Sasl: VpcConnectivitySasl | None
    Tls: VpcConnectivityTls | None


class VpcConnectivity(TypedDict, total=False):
    """VPC connectivity access control for brokers."""

    ClientAuthentication: VpcConnectivityClientAuthentication | None


class PublicAccess(TypedDict, total=False):
    """Public access control for brokers."""

    Type: _string | None


class ConnectivityInfo(TypedDict, total=False):
    """Information about the broker access configuration."""

    PublicAccess: PublicAccess | None
    VpcConnectivity: VpcConnectivity | None


class EBSStorageInfo(TypedDict, total=False):
    """Contains information about the EBS storage volumes attached to Apache
    Kafka broker nodes.
    """

    ProvisionedThroughput: ProvisionedThroughput | None
    VolumeSize: _integerMin1Max16384 | None


class StorageInfo(TypedDict, total=False):
    """Contains information about storage volumes attached to MSK broker nodes."""

    EbsStorageInfo: EBSStorageInfo | None


class BrokerNodeGroupInfo(TypedDict, total=False):
    """Describes the setup to be used for Apache Kafka broker nodes in the
    cluster.
    """

    BrokerAZDistribution: BrokerAZDistribution | None
    ClientSubnets: _listOf__string
    InstanceType: _stringMin5Max32
    SecurityGroups: _listOf__string | None
    StorageInfo: StorageInfo | None
    ConnectivityInfo: ConnectivityInfo | None
    ZoneIds: _listOf__string | None


_long = int


class BrokerSoftwareInfo(TypedDict, total=False):
    """Information about the current software installed on the cluster."""

    ConfigurationArn: _string | None
    ConfigurationRevision: _long | None
    KafkaVersion: _string | None


class BrokerNodeInfo(TypedDict, total=False):
    """BrokerNodeInfo"""

    AttachedENIId: _string | None
    BrokerId: _double | None
    ClientSubnet: _string | None
    ClientVpcIpAddress: _string | None
    CurrentBrokerSoftwareInfo: BrokerSoftwareInfo | None
    Endpoints: _listOf__string | None


class Unauthenticated(TypedDict, total=False):
    Enabled: _boolean | None


class Tls(TypedDict, total=False):
    """Details for client authentication using TLS."""

    CertificateAuthorityArnList: _listOf__string | None
    Enabled: _boolean | None


class Iam(TypedDict, total=False):
    """Details for IAM access control."""

    Enabled: _boolean | None


class Scram(TypedDict, total=False):
    """Details for SASL/SCRAM client authentication."""

    Enabled: _boolean | None


class Sasl(TypedDict, total=False):
    """Details for client authentication using SASL."""

    Scram: Scram | None
    Iam: Iam | None


class ClientAuthentication(TypedDict, total=False):
    """Includes all client authentication information."""

    Sasl: Sasl | None
    Tls: Tls | None
    Unauthenticated: Unauthenticated | None


class ServerlessSasl(TypedDict, total=False):
    """Details for client authentication using SASL."""

    Iam: Iam | None


class ServerlessClientAuthentication(TypedDict, total=False):
    """Includes all client authentication information."""

    Sasl: ServerlessSasl | None


_mapOf__string = dict[_string, _string]


class StateInfo(TypedDict, total=False):
    Code: _string | None
    Message: _string | None


class LoggingInfo(TypedDict, total=False):
    BrokerLogs: BrokerLogs


class NodeExporter(TypedDict, total=False):
    """Indicates whether you want to turn on or turn off the Node Exporter."""

    EnabledInBroker: _boolean


class JmxExporter(TypedDict, total=False):
    """Indicates whether you want to turn on or turn off the JMX Exporter."""

    EnabledInBroker: _boolean


class Prometheus(TypedDict, total=False):
    """Prometheus settings."""

    JmxExporter: JmxExporter | None
    NodeExporter: NodeExporter | None


class OpenMonitoring(TypedDict, total=False):
    """JMX and Node monitoring for the MSK cluster."""

    Prometheus: Prometheus


class EncryptionInTransit(TypedDict, total=False):
    """The settings for encrypting data in transit."""

    ClientBroker: ClientBroker | None
    InCluster: _boolean | None


class EncryptionAtRest(TypedDict, total=False):
    """The data-volume encryption details."""

    DataVolumeKMSKeyId: _string


class EncryptionInfo(TypedDict, total=False):
    """Includes encryption-related information, such as the AWS KMS key used
    for encrypting data at rest and whether you want MSK to encrypt your
    data in transit.
    """

    EncryptionAtRest: EncryptionAtRest | None
    EncryptionInTransit: EncryptionInTransit | None


_timestampIso8601 = datetime


class ClusterInfo(TypedDict, total=False):
    """Returns information about a cluster."""

    ActiveOperationArn: _string | None
    BrokerNodeGroupInfo: BrokerNodeGroupInfo | None
    Rebalancing: Rebalancing | None
    ClientAuthentication: ClientAuthentication | None
    ClusterArn: _string | None
    ClusterName: _string | None
    CreationTime: _timestampIso8601 | None
    CurrentBrokerSoftwareInfo: BrokerSoftwareInfo | None
    CurrentVersion: _string | None
    EncryptionInfo: EncryptionInfo | None
    EnhancedMonitoring: EnhancedMonitoring | None
    OpenMonitoring: OpenMonitoring | None
    LoggingInfo: LoggingInfo | None
    NumberOfBrokerNodes: _integer | None
    State: ClusterState | None
    StateInfo: StateInfo | None
    Tags: _mapOf__string | None
    ZookeeperConnectString: _string | None
    ZookeeperConnectStringTls: _string | None
    StorageMode: StorageMode | None
    CustomerActionStatus: CustomerActionStatus | None


class VpcConfig(TypedDict, total=False):
    """The configuration of the Amazon VPCs for the cluster."""

    SubnetIds: _listOf__string
    SecurityGroupIds: _listOf__string | None


_listOfVpcConfig = list[VpcConfig]


class Serverless(TypedDict, total=False):
    """Serverless cluster."""

    VpcConfigs: _listOfVpcConfig
    ClientAuthentication: ServerlessClientAuthentication | None


class NodeExporterInfo(TypedDict, total=False):
    """Indicates whether you want to turn on or turn off the Node Exporter."""

    EnabledInBroker: _boolean


class JmxExporterInfo(TypedDict, total=False):
    """Indicates whether you want to turn on or turn off the JMX Exporter."""

    EnabledInBroker: _boolean


class PrometheusInfo(TypedDict, total=False):
    """Prometheus settings."""

    JmxExporter: JmxExporterInfo | None
    NodeExporter: NodeExporterInfo | None


class OpenMonitoringInfo(TypedDict, total=False):
    """JMX and Node monitoring for the MSK cluster."""

    Prometheus: PrometheusInfo


class Provisioned(TypedDict, total=False):
    """Provisioned cluster."""

    BrokerNodeGroupInfo: BrokerNodeGroupInfo
    Rebalancing: Rebalancing | None
    CurrentBrokerSoftwareInfo: BrokerSoftwareInfo | None
    ClientAuthentication: ClientAuthentication | None
    EncryptionInfo: EncryptionInfo | None
    EnhancedMonitoring: EnhancedMonitoring | None
    OpenMonitoring: OpenMonitoringInfo | None
    LoggingInfo: LoggingInfo | None
    NumberOfBrokerNodes: _integerMin1Max15
    ZookeeperConnectString: _string | None
    ZookeeperConnectStringTls: _string | None
    StorageMode: StorageMode | None
    CustomerActionStatus: CustomerActionStatus | None


class Cluster(TypedDict, total=False):
    """Returns information about a cluster."""

    ActiveOperationArn: _string | None
    ClusterType: ClusterType | None
    ClusterArn: _string | None
    ClusterName: _string | None
    CreationTime: _timestampIso8601 | None
    CurrentVersion: _string | None
    State: ClusterState | None
    StateInfo: StateInfo | None
    Tags: _mapOf__string | None
    Provisioned: Provisioned | None
    Serverless: Serverless | None


class UserIdentity(TypedDict, total=False):
    """Description of the requester that calls the API operation."""

    Type: UserIdentityType | None
    PrincipalId: _string | None


class VpcConnectionInfo(TypedDict, total=False):
    """Description of the VPC connection."""

    VpcConnectionArn: _string | None
    Owner: _string | None
    UserIdentity: UserIdentity | None
    CreationTime: _timestampIso8601 | None


class ConfigurationInfo(TypedDict, total=False):
    """Specifies the configuration to use for the brokers."""

    Arn: _string
    Revision: _long


_listOfBrokerEBSVolumeInfo = list[BrokerEBSVolumeInfo]


class MutableClusterInfo(TypedDict, total=False):
    """Information about cluster attributes that can be updated via update
    APIs.
    """

    BrokerEBSVolumeInfo: _listOfBrokerEBSVolumeInfo | None
    ConfigurationInfo: ConfigurationInfo | None
    NumberOfBrokerNodes: _integer | None
    EnhancedMonitoring: EnhancedMonitoring | None
    OpenMonitoring: OpenMonitoring | None
    KafkaVersion: _string | None
    LoggingInfo: LoggingInfo | None
    InstanceType: _stringMin5Max32 | None
    ClientAuthentication: ClientAuthentication | None
    EncryptionInfo: EncryptionInfo | None
    ConnectivityInfo: ConnectivityInfo | None
    StorageMode: StorageMode | None
    BrokerCountUpdateInfo: BrokerCountUpdateInfo | None
    Rebalancing: Rebalancing | None


class ClusterOperationStepInfo(TypedDict, total=False):
    """State information about the operation step."""

    StepStatus: _string | None


class ClusterOperationStep(TypedDict, total=False):
    """Step taken during a cluster operation."""

    StepInfo: ClusterOperationStepInfo | None
    StepName: _string | None


_listOfClusterOperationStep = list[ClusterOperationStep]


class ErrorInfo(TypedDict, total=False):
    """Returns information about an error state of the cluster."""

    ErrorCode: _string | None
    ErrorString: _string | None


class ClusterOperationInfo(TypedDict, total=False):
    """Returns information about a cluster operation."""

    ClientRequestId: _string | None
    ClusterArn: _string | None
    CreationTime: _timestampIso8601 | None
    EndTime: _timestampIso8601 | None
    ErrorInfo: ErrorInfo | None
    OperationArn: _string | None
    OperationState: _string | None
    OperationSteps: _listOfClusterOperationStep | None
    OperationType: _string | None
    SourceClusterInfo: MutableClusterInfo | None
    TargetClusterInfo: MutableClusterInfo | None
    VpcConnectionInfo: VpcConnectionInfo | None


class ProvisionedRequest(TypedDict, total=False):
    """Provisioned cluster request."""

    BrokerNodeGroupInfo: BrokerNodeGroupInfo
    Rebalancing: Rebalancing | None
    ClientAuthentication: ClientAuthentication | None
    ConfigurationInfo: ConfigurationInfo | None
    EncryptionInfo: EncryptionInfo | None
    EnhancedMonitoring: EnhancedMonitoring | None
    OpenMonitoring: OpenMonitoringInfo | None
    KafkaVersion: _stringMin1Max128
    LoggingInfo: LoggingInfo | None
    NumberOfBrokerNodes: _integerMin1Max15
    StorageMode: StorageMode | None


class ServerlessRequest(TypedDict, total=False):
    """Serverless cluster request."""

    VpcConfigs: _listOfVpcConfig
    ClientAuthentication: ServerlessClientAuthentication | None


class ClientVpcConnection(TypedDict, total=False):
    """The client VPC connection object."""

    Authentication: _string | None
    CreationTime: _timestampIso8601 | None
    State: VpcConnectionState | None
    VpcConnectionArn: _string
    Owner: _string | None


class VpcConnection(TypedDict, total=False):
    """The VPC connection object."""

    VpcConnectionArn: _string
    TargetClusterArn: _string
    CreationTime: _timestampIso8601 | None
    Authentication: _string | None
    VpcId: _string | None
    State: VpcConnectionState | None


class CompatibleKafkaVersion(TypedDict, total=False):
    """Contains source Apache Kafka versions and compatible target Apache Kafka
    versions.
    """

    SourceVersion: _string | None
    TargetVersions: _listOf__string | None


class ConfigurationRevision(TypedDict, total=False):
    """Describes a configuration revision."""

    CreationTime: _timestampIso8601
    Description: _string | None
    Revision: _long


class Configuration(TypedDict, total=False):
    """Represents an MSK Configuration."""

    Arn: _string
    CreationTime: _timestampIso8601
    Description: _string
    KafkaVersions: _listOf__string
    LatestRevision: ConfigurationRevision
    Name: _string
    State: ConfigurationState


_listOf__stringMax256 = list[_stringMax256]


class ConsumerGroupReplication(TypedDict, total=False):
    """Details about consumer group replication."""

    ConsumerGroupsToExclude: _listOf__stringMax256 | None
    ConsumerGroupsToReplicate: _listOf__stringMax256
    DetectAndCopyNewConsumerGroups: _boolean | None
    SynchroniseConsumerGroupOffsets: _boolean | None


class ConsumerGroupReplicationUpdate(TypedDict, total=False):
    """Details about consumer group replication."""

    ConsumerGroupsToExclude: _listOf__stringMax256
    ConsumerGroupsToReplicate: _listOf__stringMax256
    DetectAndCopyNewConsumerGroups: _boolean
    SynchroniseConsumerGroupOffsets: _boolean


class CreateClusterV2Request(ServiceRequest):
    ClusterName: _stringMin1Max64
    Tags: _mapOf__string | None
    Provisioned: ProvisionedRequest | None
    Serverless: ServerlessRequest | None


class CreateClusterRequest(ServiceRequest):
    BrokerNodeGroupInfo: BrokerNodeGroupInfo
    Rebalancing: Rebalancing | None
    ClientAuthentication: ClientAuthentication | None
    ClusterName: _stringMin1Max64
    ConfigurationInfo: ConfigurationInfo | None
    EncryptionInfo: EncryptionInfo | None
    EnhancedMonitoring: EnhancedMonitoring | None
    OpenMonitoring: OpenMonitoringInfo | None
    KafkaVersion: _stringMin1Max128
    LoggingInfo: LoggingInfo | None
    NumberOfBrokerNodes: _integerMin1Max15
    Tags: _mapOf__string | None
    StorageMode: StorageMode | None


class CreateClusterResponse(TypedDict, total=False):
    ClusterArn: _string | None
    ClusterName: _string | None
    State: ClusterState | None


class CreateClusterV2Response(TypedDict, total=False):
    ClusterArn: _string | None
    ClusterName: _string | None
    State: ClusterState | None
    ClusterType: ClusterType | None


_blob = bytes


class CreateConfigurationRequest(ServiceRequest):
    Description: _string | None
    KafkaVersions: _listOf__string | None
    Name: _string
    ServerProperties: _blob


class CreateConfigurationResponse(TypedDict, total=False):
    Arn: _string | None
    CreationTime: _timestampIso8601 | None
    LatestRevision: ConfigurationRevision | None
    Name: _string | None
    State: ConfigurationState | None


_listOf__stringMax249 = list[_stringMax249]


class ReplicationTopicNameConfiguration(TypedDict, total=False):
    """Configuration for specifying replicated topic names should be the same
    as their corresponding upstream topics or prefixed with source cluster
    alias.
    """

    Type: ReplicationTopicNameConfigurationType | None


class ReplicationStartingPosition(TypedDict, total=False):
    """Configuration for specifying the position in the topics to start
    replicating from.
    """

    Type: ReplicationStartingPositionType | None


class TopicReplication(TypedDict, total=False):
    """Details about topic replication."""

    CopyAccessControlListsForTopics: _boolean | None
    CopyTopicConfigurations: _boolean | None
    DetectAndCopyNewTopics: _boolean | None
    StartingPosition: ReplicationStartingPosition | None
    TopicNameConfiguration: ReplicationTopicNameConfiguration | None
    TopicsToExclude: _listOf__stringMax249 | None
    TopicsToReplicate: _listOf__stringMax249


class ReplicationInfo(TypedDict, total=False):
    """Specifies configuration for replication between a source and target
    Kafka cluster.
    """

    ConsumerGroupReplication: ConsumerGroupReplication
    SourceKafkaClusterArn: _string
    TargetCompressionType: TargetCompressionType
    TargetKafkaClusterArn: _string
    TopicReplication: TopicReplication


_listOfReplicationInfo = list[ReplicationInfo]


class KafkaClusterClientVpcConfig(TypedDict, total=False):
    """Details of an Amazon VPC which has network connectivity to the Apache
    Kafka cluster.
    """

    SecurityGroupIds: _listOf__string | None
    SubnetIds: _listOf__string


class KafkaCluster(TypedDict, total=False):
    """Information about Kafka Cluster to be used as source / target for
    replication.
    """

    AmazonMskCluster: AmazonMskCluster
    VpcConfig: KafkaClusterClientVpcConfig


_listOfKafkaCluster = list[KafkaCluster]


class CreateReplicatorRequest(ServiceRequest):
    """Creates a replicator using the specified configuration."""

    Description: _stringMax1024 | None
    KafkaClusters: _listOfKafkaCluster
    ReplicationInfoList: _listOfReplicationInfo
    ReplicatorName: _stringMin1Max128Pattern09AZaZ09AZaZ0
    ServiceExecutionRoleArn: _string
    Tags: _mapOf__string | None


class CreateReplicatorResponse(TypedDict, total=False):
    ReplicatorArn: _string | None
    ReplicatorName: _string | None
    ReplicatorState: ReplicatorState | None


class CreateVpcConnectionRequest(ServiceRequest):
    TargetClusterArn: _string
    Authentication: _string
    VpcId: _string
    ClientSubnets: _listOf__string
    SecurityGroups: _listOf__string
    Tags: _mapOf__string | None


class CreateVpcConnectionResponse(TypedDict, total=False):
    VpcConnectionArn: _string | None
    State: VpcConnectionState | None
    Authentication: _string | None
    VpcId: _string | None
    ClientSubnets: _listOf__string | None
    SecurityGroups: _listOf__string | None
    CreationTime: _timestampIso8601 | None
    Tags: _mapOf__string | None


class VpcConnectionInfoServerless(TypedDict, total=False):
    """Description of the VPC connection."""

    CreationTime: _timestampIso8601 | None
    Owner: _string | None
    UserIdentity: UserIdentity | None
    VpcConnectionArn: _string | None


class ClusterOperationV2Serverless(TypedDict, total=False):
    """Returns information about a serverless cluster operation."""

    VpcConnectionInfo: VpcConnectionInfoServerless | None


class ClusterOperationV2Provisioned(TypedDict, total=False):
    """Returns information about a provisioned cluster operation."""

    OperationSteps: _listOfClusterOperationStep | None
    SourceClusterInfo: MutableClusterInfo | None
    TargetClusterInfo: MutableClusterInfo | None
    VpcConnectionInfo: VpcConnectionInfo | None


class ClusterOperationV2(TypedDict, total=False):
    """Returns information about a cluster operation."""

    ClusterArn: _string | None
    ClusterType: ClusterType | None
    StartTime: _timestampIso8601 | None
    EndTime: _timestampIso8601 | None
    ErrorInfo: ErrorInfo | None
    OperationArn: _string | None
    OperationState: _string | None
    OperationType: _string | None
    Provisioned: ClusterOperationV2Provisioned | None
    Serverless: ClusterOperationV2Serverless | None


class ClusterOperationV2Summary(TypedDict, total=False):
    """Returns information about a cluster operation."""

    ClusterArn: _string | None
    ClusterType: ClusterType | None
    StartTime: _timestampIso8601 | None
    EndTime: _timestampIso8601 | None
    OperationArn: _string | None
    OperationState: _string | None
    OperationType: _string | None


class ControllerNodeInfo(TypedDict, total=False):
    """Controller node information."""

    Endpoints: _listOf__string | None


class DeleteClusterRequest(ServiceRequest):
    ClusterArn: _string
    CurrentVersion: _string | None


class DeleteClusterResponse(TypedDict, total=False):
    ClusterArn: _string | None
    State: ClusterState | None


class DeleteClusterPolicyRequest(ServiceRequest):
    ClusterArn: _string


class DeleteClusterPolicyResponse(TypedDict, total=False):
    pass


class DeleteConfigurationRequest(ServiceRequest):
    Arn: _string


class DeleteConfigurationResponse(TypedDict, total=False):
    Arn: _string | None
    State: ConfigurationState | None


class DeleteReplicatorRequest(ServiceRequest):
    CurrentVersion: _string | None
    ReplicatorArn: _string


class DeleteReplicatorResponse(TypedDict, total=False):
    ReplicatorArn: _string | None
    ReplicatorState: ReplicatorState | None


class DeleteVpcConnectionRequest(ServiceRequest):
    Arn: _string


class DeleteVpcConnectionResponse(TypedDict, total=False):
    VpcConnectionArn: _string | None
    State: VpcConnectionState | None


class DescribeClusterOperationRequest(ServiceRequest):
    ClusterOperationArn: _string


class DescribeClusterOperationV2Request(ServiceRequest):
    ClusterOperationArn: _string


class DescribeClusterOperationResponse(TypedDict, total=False):
    ClusterOperationInfo: ClusterOperationInfo | None


class DescribeClusterOperationV2Response(TypedDict, total=False):
    ClusterOperationInfo: ClusterOperationV2 | None


class DescribeClusterRequest(ServiceRequest):
    ClusterArn: _string


class DescribeClusterV2Request(ServiceRequest):
    ClusterArn: _string


class DescribeClusterResponse(TypedDict, total=False):
    ClusterInfo: ClusterInfo | None


class DescribeClusterV2Response(TypedDict, total=False):
    ClusterInfo: Cluster | None


class DescribeConfigurationRequest(ServiceRequest):
    Arn: _string


class DescribeConfigurationResponse(TypedDict, total=False):
    Arn: _string | None
    CreationTime: _timestampIso8601 | None
    Description: _string | None
    KafkaVersions: _listOf__string | None
    LatestRevision: ConfigurationRevision | None
    Name: _string | None
    State: ConfigurationState | None


class DescribeConfigurationRevisionRequest(ServiceRequest):
    Arn: _string
    Revision: _long


class DescribeConfigurationRevisionResponse(TypedDict, total=False):
    Arn: _string | None
    CreationTime: _timestampIso8601 | None
    Description: _string | None
    Revision: _long | None
    ServerProperties: _blob | None


class DescribeTopicRequest(ServiceRequest):
    ClusterArn: _string
    TopicName: _string


class DescribeTopicPartitionsRequest(ServiceRequest):
    ClusterArn: _string
    TopicName: _string
    MaxResults: MaxResults | None
    NextToken: _string | None


class DescribeTopicResponse(TypedDict, total=False):
    TopicArn: _string | None
    TopicName: _string | None
    ReplicationFactor: _integer | None
    PartitionCount: _integer | None
    Configs: _string | None
    Status: TopicState | None


_listOf__integer = list[_integer]


class TopicPartitionInfo(TypedDict, total=False):
    """Contains information about a topic partition."""

    Partition: _integer | None
    Leader: _integer | None
    Replicas: _listOf__integer | None
    Isr: _listOf__integer | None


_listOfTopicPartitionInfo = list[TopicPartitionInfo]


class DescribeTopicPartitionsResponse(TypedDict, total=False):
    Partitions: _listOfTopicPartitionInfo | None
    NextToken: _string | None


class DescribeVpcConnectionRequest(ServiceRequest):
    Arn: _string


class DescribeReplicatorRequest(ServiceRequest):
    ReplicatorArn: _string


class ReplicationStateInfo(TypedDict, total=False):
    """Details about the state of a replicator"""

    Code: _string | None
    Message: _string | None


class ReplicationInfoDescription(TypedDict, total=False):
    """Specifies configuration for replication between a source and target
    Kafka cluster (sourceKafkaClusterAlias -> targetKafkaClusterAlias)
    """

    ConsumerGroupReplication: ConsumerGroupReplication | None
    SourceKafkaClusterAlias: _string | None
    TargetCompressionType: TargetCompressionType | None
    TargetKafkaClusterAlias: _string | None
    TopicReplication: TopicReplication | None


_listOfReplicationInfoDescription = list[ReplicationInfoDescription]


class KafkaClusterDescription(TypedDict, total=False):
    """Information about Kafka Cluster used as source / target for replication."""

    AmazonMskCluster: AmazonMskCluster | None
    KafkaClusterAlias: _string | None
    VpcConfig: KafkaClusterClientVpcConfig | None


_listOfKafkaClusterDescription = list[KafkaClusterDescription]


class DescribeReplicatorResponse(TypedDict, total=False):
    CreationTime: _timestampIso8601 | None
    CurrentVersion: _string | None
    IsReplicatorReference: _boolean | None
    KafkaClusters: _listOfKafkaClusterDescription | None
    ReplicationInfoList: _listOfReplicationInfoDescription | None
    ReplicatorArn: _string | None
    ReplicatorDescription: _string | None
    ReplicatorName: _string | None
    ReplicatorResourceArn: _string | None
    ReplicatorState: ReplicatorState | None
    ServiceExecutionRoleArn: _string | None
    StateInfo: ReplicationStateInfo | None
    Tags: _mapOf__string | None


class DescribeVpcConnectionResponse(TypedDict, total=False):
    VpcConnectionArn: _string | None
    TargetClusterArn: _string | None
    State: VpcConnectionState | None
    Authentication: _string | None
    VpcId: _string | None
    Subnets: _listOf__string | None
    SecurityGroups: _listOf__string | None
    CreationTime: _timestampIso8601 | None
    Tags: _mapOf__string | None


class BatchDisassociateScramSecretRequest(ServiceRequest):
    """Disassociates sasl scram secrets to cluster."""

    ClusterArn: _string
    SecretArnList: _listOf__string


class BatchDisassociateScramSecretResponse(TypedDict, total=False):
    ClusterArn: _string | None
    UnprocessedScramSecrets: _listOfUnprocessedScramSecret | None


class Error(TypedDict, total=False):
    """Returns information about an error."""

    InvalidParameter: _string | None
    Message: _string | None


class GetBootstrapBrokersRequest(ServiceRequest):
    ClusterArn: _string


class GetBootstrapBrokersResponse(TypedDict, total=False):
    BootstrapBrokerString: _string | None
    BootstrapBrokerStringTls: _string | None
    BootstrapBrokerStringSaslScram: _string | None
    BootstrapBrokerStringSaslIam: _string | None
    BootstrapBrokerStringPublicTls: _string | None
    BootstrapBrokerStringPublicSaslScram: _string | None
    BootstrapBrokerStringPublicSaslIam: _string | None
    BootstrapBrokerStringVpcConnectivityTls: _string | None
    BootstrapBrokerStringVpcConnectivitySaslScram: _string | None
    BootstrapBrokerStringVpcConnectivitySaslIam: _string | None


class GetCompatibleKafkaVersionsRequest(ServiceRequest):
    ClusterArn: _string | None


_listOfCompatibleKafkaVersion = list[CompatibleKafkaVersion]


class GetCompatibleKafkaVersionsResponse(TypedDict, total=False):
    CompatibleKafkaVersions: _listOfCompatibleKafkaVersion | None


class GetClusterPolicyRequest(ServiceRequest):
    ClusterArn: _string


class GetClusterPolicyResponse(TypedDict, total=False):
    CurrentVersion: _string | None
    Policy: _string | None


class KafkaClusterSummary(TypedDict, total=False):
    """Summarized information about Kafka Cluster used as source / target for
    replication.
    """

    AmazonMskCluster: AmazonMskCluster | None
    KafkaClusterAlias: _string | None


class KafkaVersion(TypedDict, total=False):
    Version: _string | None
    Status: KafkaVersionStatus | None


class ListClusterOperationsRequest(ServiceRequest):
    ClusterArn: _string
    MaxResults: MaxResults | None
    NextToken: _string | None


class ListClusterOperationsV2Request(ServiceRequest):
    ClusterArn: _string
    MaxResults: MaxResults | None
    NextToken: _string | None


_listOfClusterOperationInfo = list[ClusterOperationInfo]


class ListClusterOperationsResponse(TypedDict, total=False):
    ClusterOperationInfoList: _listOfClusterOperationInfo | None
    NextToken: _string | None


_listOfClusterOperationV2Summary = list[ClusterOperationV2Summary]


class ListClusterOperationsV2Response(TypedDict, total=False):
    ClusterOperationInfoList: _listOfClusterOperationV2Summary | None
    NextToken: _string | None


class ListClustersRequest(ServiceRequest):
    ClusterNameFilter: _string | None
    MaxResults: MaxResults | None
    NextToken: _string | None


class ListClustersV2Request(ServiceRequest):
    ClusterNameFilter: _string | None
    ClusterTypeFilter: _string | None
    MaxResults: MaxResults | None
    NextToken: _string | None


_listOfClusterInfo = list[ClusterInfo]


class ListClustersResponse(TypedDict, total=False):
    ClusterInfoList: _listOfClusterInfo | None
    NextToken: _string | None


_listOfCluster = list[Cluster]


class ListClustersV2Response(TypedDict, total=False):
    ClusterInfoList: _listOfCluster | None
    NextToken: _string | None


class ListConfigurationRevisionsRequest(ServiceRequest):
    Arn: _string
    MaxResults: MaxResults | None
    NextToken: _string | None


_listOfConfigurationRevision = list[ConfigurationRevision]


class ListConfigurationRevisionsResponse(TypedDict, total=False):
    NextToken: _string | None
    Revisions: _listOfConfigurationRevision | None


class ListConfigurationsRequest(ServiceRequest):
    MaxResults: MaxResults | None
    NextToken: _string | None


_listOfConfiguration = list[Configuration]


class ListConfigurationsResponse(TypedDict, total=False):
    Configurations: _listOfConfiguration | None
    NextToken: _string | None


class ListKafkaVersionsRequest(ServiceRequest):
    MaxResults: MaxResults | None
    NextToken: _string | None


_listOfKafkaVersion = list[KafkaVersion]


class ListKafkaVersionsResponse(TypedDict, total=False):
    KafkaVersions: _listOfKafkaVersion | None
    NextToken: _string | None


class ListNodesRequest(ServiceRequest):
    ClusterArn: _string
    MaxResults: MaxResults | None
    NextToken: _string | None


class ZookeeperNodeInfo(TypedDict, total=False):
    """Zookeeper node information."""

    AttachedENIId: _string | None
    ClientVpcIpAddress: _string | None
    Endpoints: _listOf__string | None
    ZookeeperId: _double | None
    ZookeeperVersion: _string | None


class NodeInfo(TypedDict, total=False):
    """The node information object."""

    AddedToClusterTime: _string | None
    BrokerNodeInfo: BrokerNodeInfo | None
    ControllerNodeInfo: ControllerNodeInfo | None
    InstanceType: _string | None
    NodeARN: _string | None
    NodeType: NodeType | None
    ZookeeperNodeInfo: ZookeeperNodeInfo | None


_listOfNodeInfo = list[NodeInfo]


class ListNodesResponse(TypedDict, total=False):
    NextToken: _string | None
    NodeInfoList: _listOfNodeInfo | None


class ListReplicatorsRequest(ServiceRequest):
    MaxResults: MaxResults | None
    NextToken: _string | None
    ReplicatorNameFilter: _string | None


class ReplicationInfoSummary(TypedDict, total=False):
    """Summarized information of replication between clusters."""

    SourceKafkaClusterAlias: _string | None
    TargetKafkaClusterAlias: _string | None


_listOfReplicationInfoSummary = list[ReplicationInfoSummary]
_listOfKafkaClusterSummary = list[KafkaClusterSummary]


class ReplicatorSummary(TypedDict, total=False):
    """Information about a replicator."""

    CreationTime: _timestampIso8601 | None
    CurrentVersion: _string | None
    IsReplicatorReference: _boolean | None
    KafkaClustersSummary: _listOfKafkaClusterSummary | None
    ReplicationInfoSummaryList: _listOfReplicationInfoSummary | None
    ReplicatorArn: _string | None
    ReplicatorName: _string | None
    ReplicatorResourceArn: _string | None
    ReplicatorState: ReplicatorState | None


_listOfReplicatorSummary = list[ReplicatorSummary]


class ListReplicatorsResponse(TypedDict, total=False):
    NextToken: _string | None
    Replicators: _listOfReplicatorSummary | None


class ListScramSecretsRequest(ServiceRequest):
    ClusterArn: _string
    MaxResults: MaxResults | None
    NextToken: _string | None


class ListScramSecretsResponse(TypedDict, total=False):
    NextToken: _string | None
    SecretArnList: _listOf__string | None


class ListTagsForResourceRequest(ServiceRequest):
    ResourceArn: _string


class ListTagsForResourceResponse(TypedDict, total=False):
    Tags: _mapOf__string | None


class ListClientVpcConnectionsRequest(ServiceRequest):
    ClusterArn: _string
    MaxResults: MaxResults | None
    NextToken: _string | None


_listOfClientVpcConnection = list[ClientVpcConnection]


class ListClientVpcConnectionsResponse(TypedDict, total=False):
    ClientVpcConnections: _listOfClientVpcConnection | None
    NextToken: _string | None


class ListTopicsRequest(ServiceRequest):
    ClusterArn: _string
    MaxResults: MaxResults | None
    NextToken: _string | None
    TopicNameFilter: _string | None


class TopicInfo(TypedDict, total=False):
    """Includes identification info about the topic."""

    TopicArn: _string | None
    TopicName: _string | None
    ReplicationFactor: _integer | None
    PartitionCount: _integer | None
    OutOfSyncReplicaCount: _integer | None


_listOfTopicInfo = list[TopicInfo]


class ListTopicsResponse(TypedDict, total=False):
    Topics: _listOfTopicInfo | None
    NextToken: _string | None


class ListVpcConnectionsRequest(ServiceRequest):
    MaxResults: MaxResults | None
    NextToken: _string | None


_listOfVpcConnection = list[VpcConnection]


class ListVpcConnectionsResponse(TypedDict, total=False):
    VpcConnections: _listOfVpcConnection | None
    NextToken: _string | None


class RejectClientVpcConnectionRequest(ServiceRequest):
    ClusterArn: _string
    VpcConnectionArn: _string


class RejectClientVpcConnectionResponse(TypedDict, total=False):
    pass


class PutClusterPolicyRequest(ServiceRequest):
    ClusterArn: _string
    CurrentVersion: _string | None
    Policy: _string


class PutClusterPolicyResponse(TypedDict, total=False):
    CurrentVersion: _string | None


class RebootBrokerRequest(ServiceRequest):
    """Reboots a node."""

    BrokerIds: _listOf__string
    ClusterArn: _string


class RebootBrokerResponse(TypedDict, total=False):
    ClusterArn: _string | None
    ClusterOperationArn: _string | None


class TagResourceRequest(ServiceRequest):
    ResourceArn: _string
    Tags: _mapOf__string


class TopicReplicationUpdate(TypedDict, total=False):
    """Details for updating the topic replication of a replicator."""

    CopyAccessControlListsForTopics: _boolean
    CopyTopicConfigurations: _boolean
    DetectAndCopyNewTopics: _boolean
    TopicsToExclude: _listOf__stringMax249
    TopicsToReplicate: _listOf__stringMax249


class UntagResourceRequest(ServiceRequest):
    ResourceArn: _string
    TagKeys: _listOf__string


class UpdateBrokerCountRequest(ServiceRequest):
    ClusterArn: _string
    CurrentVersion: _string
    TargetNumberOfBrokerNodes: _integerMin1Max15


class UpdateBrokerCountResponse(TypedDict, total=False):
    ClusterArn: _string | None
    ClusterOperationArn: _string | None


class UpdateBrokerTypeRequest(ServiceRequest):
    ClusterArn: _string
    CurrentVersion: _string
    TargetInstanceType: _string


class UpdateBrokerTypeResponse(TypedDict, total=False):
    ClusterArn: _string | None
    ClusterOperationArn: _string | None


class UpdateBrokerStorageRequest(ServiceRequest):
    ClusterArn: _string
    CurrentVersion: _string
    TargetBrokerEBSVolumeInfo: _listOfBrokerEBSVolumeInfo


class UpdateBrokerStorageResponse(TypedDict, total=False):
    ClusterArn: _string | None
    ClusterOperationArn: _string | None


class UpdateClusterConfigurationRequest(ServiceRequest):
    ClusterArn: _string
    ConfigurationInfo: ConfigurationInfo
    CurrentVersion: _string


class UpdateClusterConfigurationResponse(TypedDict, total=False):
    ClusterArn: _string | None
    ClusterOperationArn: _string | None


class UpdateClusterKafkaVersionRequest(ServiceRequest):
    ClusterArn: _string
    ConfigurationInfo: ConfigurationInfo | None
    CurrentVersion: _string
    TargetKafkaVersion: _string


class UpdateClusterKafkaVersionResponse(TypedDict, total=False):
    ClusterArn: _string | None
    ClusterOperationArn: _string | None


class UpdateMonitoringRequest(ServiceRequest):
    """Request body for UpdateMonitoring."""

    ClusterArn: _string
    CurrentVersion: _string
    EnhancedMonitoring: EnhancedMonitoring | None
    OpenMonitoring: OpenMonitoringInfo | None
    LoggingInfo: LoggingInfo | None


class UpdateMonitoringResponse(TypedDict, total=False):
    ClusterArn: _string | None
    ClusterOperationArn: _string | None


class UpdateRebalancingRequest(ServiceRequest):
    ClusterArn: _string
    CurrentVersion: _string
    Rebalancing: Rebalancing


class UpdateRebalancingResponse(TypedDict, total=False):
    ClusterArn: _string | None
    ClusterOperationArn: _string | None


class UpdateReplicationInfoRequest(ServiceRequest):
    """Update information relating to replication between a given source and
    target Kafka cluster.
    """

    ConsumerGroupReplication: ConsumerGroupReplicationUpdate | None
    CurrentVersion: _string
    ReplicatorArn: _string
    SourceKafkaClusterArn: _string
    TargetKafkaClusterArn: _string
    TopicReplication: TopicReplicationUpdate | None


class UpdateReplicationInfoResponse(TypedDict, total=False):
    ReplicatorArn: _string | None
    ReplicatorState: ReplicatorState | None


class UpdateSecurityRequest(ServiceRequest):
    ClientAuthentication: ClientAuthentication | None
    ClusterArn: _string
    CurrentVersion: _string
    EncryptionInfo: EncryptionInfo | None


class UpdateSecurityResponse(TypedDict, total=False):
    ClusterArn: _string | None
    ClusterOperationArn: _string | None


class UpdateStorageRequest(ServiceRequest):
    """Request object for UpdateStorage api. Its used to update the storage
    attributes for the cluster.
    """

    ClusterArn: _string
    CurrentVersion: _string
    ProvisionedThroughput: ProvisionedThroughput | None
    StorageMode: StorageMode | None
    VolumeSizeGB: _integer | None


class UpdateStorageResponse(TypedDict, total=False):
    ClusterArn: _string | None
    ClusterOperationArn: _string | None


class UpdateConfigurationRequest(ServiceRequest):
    Arn: _string
    Description: _string | None
    ServerProperties: _blob


class UpdateConfigurationResponse(TypedDict, total=False):
    Arn: _string | None
    LatestRevision: ConfigurationRevision | None


class UpdateConnectivityRequest(ServiceRequest):
    """Request body for UpdateConnectivity."""

    ClusterArn: _string
    ConnectivityInfo: ConnectivityInfo
    CurrentVersion: _string


class UpdateConnectivityResponse(TypedDict, total=False):
    ClusterArn: _string | None
    ClusterOperationArn: _string | None


_timestampUnix = datetime


class KafkaApi:
    service: str = "kafka"
    version: str = "2018-11-14"

    @handler("BatchAssociateScramSecret")
    def batch_associate_scram_secret(
        self,
        context: RequestContext,
        cluster_arn: _string,
        secret_arn_list: _listOf__string,
        **kwargs,
    ) -> BatchAssociateScramSecretResponse:
        """Associates one or more Scram Secrets with an Amazon MSK cluster.

        :param cluster_arn: The Amazon Resource Name (ARN) of the cluster to be updated.
        :param secret_arn_list: List of AWS Secrets Manager secret ARNs.
        :returns: BatchAssociateScramSecretResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("CreateCluster")
    def create_cluster(
        self,
        context: RequestContext,
        broker_node_group_info: BrokerNodeGroupInfo,
        kafka_version: _stringMin1Max128,
        number_of_broker_nodes: _integerMin1Max15,
        cluster_name: _stringMin1Max64,
        rebalancing: Rebalancing | None = None,
        client_authentication: ClientAuthentication | None = None,
        configuration_info: ConfigurationInfo | None = None,
        encryption_info: EncryptionInfo | None = None,
        enhanced_monitoring: EnhancedMonitoring | None = None,
        open_monitoring: OpenMonitoringInfo | None = None,
        logging_info: LoggingInfo | None = None,
        tags: _mapOf__string | None = None,
        storage_mode: StorageMode | None = None,
        **kwargs,
    ) -> CreateClusterResponse:
        """Creates a new MSK cluster.

        :param broker_node_group_info: Information about the broker nodes in the cluster.
        :param kafka_version: The version of Apache Kafka.
        :param number_of_broker_nodes: The number of broker nodes in the cluster.
        :param cluster_name: The name of the cluster.
        :param rebalancing: Specifies if intelligent rebalancing should be turned on for the new MSK
        Provisioned cluster with Express brokers.
        :param client_authentication: Includes all client authentication related information.
        :param configuration_info: Represents the configuration that you want MSK to use for the brokers in
        a cluster.
        :param encryption_info: Includes all encryption-related information.
        :param enhanced_monitoring: Specifies the level of monitoring for the MSK cluster.
        :param open_monitoring: The settings for open monitoring.
        :param logging_info: .
        :param tags: Create tags when creating the cluster.
        :param storage_mode: This controls storage mode for supported storage tiers.
        :returns: CreateClusterResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises UnauthorizedException:
        :raises ForbiddenException:
        :raises ServiceUnavailableException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("CreateClusterV2")
    def create_cluster_v2(
        self,
        context: RequestContext,
        cluster_name: _stringMin1Max64,
        tags: _mapOf__string | None = None,
        provisioned: ProvisionedRequest | None = None,
        serverless: ServerlessRequest | None = None,
        **kwargs,
    ) -> CreateClusterV2Response:
        """Creates a new MSK cluster.

        :param cluster_name: The name of the cluster.
        :param tags: A map of tags that you want the cluster to have.
        :param provisioned: Information about the provisioned cluster.
        :param serverless: Information about the serverless cluster.
        :returns: CreateClusterV2Response
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises UnauthorizedException:
        :raises ForbiddenException:
        :raises ServiceUnavailableException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("CreateConfiguration")
    def create_configuration(
        self,
        context: RequestContext,
        server_properties: _blob,
        name: _string,
        description: _string | None = None,
        kafka_versions: _listOf__string | None = None,
        **kwargs,
    ) -> CreateConfigurationResponse:
        """Creates a new MSK configuration.

        :param server_properties: Contents of the server.
        :param name: The name of the configuration.
        :param description: The description of the configuration.
        :param kafka_versions: The versions of Apache Kafka with which you can use this MSK
        configuration.
        :returns: CreateConfigurationResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises UnauthorizedException:
        :raises ForbiddenException:
        :raises ServiceUnavailableException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("CreateReplicator")
    def create_replicator(
        self,
        context: RequestContext,
        service_execution_role_arn: _string,
        replicator_name: _stringMin1Max128Pattern09AZaZ09AZaZ0,
        replication_info_list: _listOfReplicationInfo,
        kafka_clusters: _listOfKafkaCluster,
        description: _stringMax1024 | None = None,
        tags: _mapOf__string | None = None,
        **kwargs,
    ) -> CreateReplicatorResponse:
        """Creates the replicator.

        :param service_execution_role_arn: The ARN of the IAM role used by the replicator to access resources in
        the customer's account (e.
        :param replicator_name: The name of the replicator.
        :param replication_info_list: A list of replication configurations, where each configuration targets a
        given source cluster to target cluster replication flow.
        :param kafka_clusters: Kafka Clusters to use in setting up sources / targets for replication.
        :param description: A summary description of the replicator.
        :param tags: List of tags to attach to created Replicator.
        :returns: CreateReplicatorResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        :raises TooManyRequestsException:
        :raises ConflictException:
        """
        raise NotImplementedError

    @handler("CreateVpcConnection")
    def create_vpc_connection(
        self,
        context: RequestContext,
        target_cluster_arn: _string,
        authentication: _string,
        vpc_id: _string,
        client_subnets: _listOf__string,
        security_groups: _listOf__string,
        tags: _mapOf__string | None = None,
        **kwargs,
    ) -> CreateVpcConnectionResponse:
        """Creates a new MSK VPC connection.

        :param target_cluster_arn: The cluster Amazon Resource Name (ARN) for the VPC connection.
        :param authentication: The authentication type of VPC connection.
        :param vpc_id: The VPC ID of VPC connection.
        :param client_subnets: The list of client subnets.
        :param security_groups: The list of security groups.
        :param tags: A map of tags for the VPC connection.
        :returns: CreateVpcConnectionResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises UnauthorizedException:
        :raises ForbiddenException:
        :raises ServiceUnavailableException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteCluster")
    def delete_cluster(
        self,
        context: RequestContext,
        cluster_arn: _string,
        current_version: _string | None = None,
        **kwargs,
    ) -> DeleteClusterResponse:
        """Deletes the MSK cluster specified by the Amazon Resource Name (ARN) in
        the request.

        :param cluster_arn: The Amazon Resource Name (ARN) that uniquely identifies the cluster.
        :param current_version: The current version of the MSK cluster.
        :returns: DeleteClusterResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("DeleteClusterPolicy")
    def delete_cluster_policy(
        self, context: RequestContext, cluster_arn: _string, **kwargs
    ) -> DeleteClusterPolicyResponse:
        """Deletes the MSK cluster policy specified by the Amazon Resource Name
        (ARN) in the request.

        :param cluster_arn: The Amazon Resource Name (ARN) of the cluster.
        :returns: DeleteClusterPolicyResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("DeleteConfiguration")
    def delete_configuration(
        self, context: RequestContext, arn: _string, **kwargs
    ) -> DeleteConfigurationResponse:
        """Deletes an MSK Configuration.

        :param arn: The Amazon Resource Name (ARN) that uniquely identifies an MSK
        configuration.
        :returns: DeleteConfigurationResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("DeleteReplicator")
    def delete_replicator(
        self,
        context: RequestContext,
        replicator_arn: _string,
        current_version: _string | None = None,
        **kwargs,
    ) -> DeleteReplicatorResponse:
        """Deletes a replicator.

        :param replicator_arn: The Amazon Resource Name (ARN) of the replicator to be deleted.
        :param current_version: The current version of the replicator.
        :returns: DeleteReplicatorResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DeleteVpcConnection")
    def delete_vpc_connection(
        self, context: RequestContext, arn: _string, **kwargs
    ) -> DeleteVpcConnectionResponse:
        """Deletes a MSK VPC connection.

        :param arn: The Amazon Resource Name (ARN) that uniquely identifies an MSK VPC
        connection.
        :returns: DeleteVpcConnectionResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("DescribeCluster")
    def describe_cluster(
        self, context: RequestContext, cluster_arn: _string, **kwargs
    ) -> DescribeClusterResponse:
        """Returns a description of the MSK cluster whose Amazon Resource Name
        (ARN) is specified in the request.

        :param cluster_arn: The Amazon Resource Name (ARN) that uniquely identifies the cluster.
        :returns: DescribeClusterResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("DescribeClusterV2")
    def describe_cluster_v2(
        self, context: RequestContext, cluster_arn: _string, **kwargs
    ) -> DescribeClusterV2Response:
        """Returns a description of the MSK cluster whose Amazon Resource Name
        (ARN) is specified in the request.

        :param cluster_arn: The Amazon Resource Name (ARN) that uniquely identifies the cluster.
        :returns: DescribeClusterV2Response
        :raises NotFoundException:
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("DescribeClusterOperation")
    def describe_cluster_operation(
        self, context: RequestContext, cluster_operation_arn: _string, **kwargs
    ) -> DescribeClusterOperationResponse:
        """Returns a description of the cluster operation specified by the ARN.

        :param cluster_operation_arn: The Amazon Resource Name (ARN) that uniquely identifies the MSK cluster
        operation.
        :returns: DescribeClusterOperationResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("DescribeClusterOperationV2")
    def describe_cluster_operation_v2(
        self, context: RequestContext, cluster_operation_arn: _string, **kwargs
    ) -> DescribeClusterOperationV2Response:
        """Returns a description of the cluster operation specified by the ARN.

        :param cluster_operation_arn: ARN of the cluster operation to describe.
        :returns: DescribeClusterOperationV2Response
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DescribeConfiguration")
    def describe_configuration(
        self, context: RequestContext, arn: _string, **kwargs
    ) -> DescribeConfigurationResponse:
        """Returns a description of this MSK configuration.

        :param arn: The Amazon Resource Name (ARN) that uniquely identifies an MSK
        configuration and all of its revisions.
        :returns: DescribeConfigurationResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DescribeConfigurationRevision")
    def describe_configuration_revision(
        self, context: RequestContext, revision: _long, arn: _string, **kwargs
    ) -> DescribeConfigurationRevisionResponse:
        """Returns a description of this revision of the configuration.

        :param revision: A string that uniquely identifies a revision of an MSK configuration.
        :param arn: The Amazon Resource Name (ARN) that uniquely identifies an MSK
        configuration and all of its revisions.
        :returns: DescribeConfigurationRevisionResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("DescribeReplicator")
    def describe_replicator(
        self, context: RequestContext, replicator_arn: _string, **kwargs
    ) -> DescribeReplicatorResponse:
        """Describes a replicator.

        :param replicator_arn: The Amazon Resource Name (ARN) of the replicator to be described.
        :returns: DescribeReplicatorResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("DescribeTopic")
    def describe_topic(
        self, context: RequestContext, cluster_arn: _string, topic_name: _string, **kwargs
    ) -> DescribeTopicResponse:
        """Returns topic details of this topic on a MSK cluster.

        :param cluster_arn: The Amazon Resource Name (ARN) that uniquely identifies the cluster.
        :param topic_name: The Kafka topic name that uniquely identifies the topic.
        :returns: DescribeTopicResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeTopicPartitions")
    def describe_topic_partitions(
        self,
        context: RequestContext,
        cluster_arn: _string,
        topic_name: _string,
        max_results: MaxResults | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> DescribeTopicPartitionsResponse:
        """Returns partition details of this topic on a MSK cluster.

        :param cluster_arn: The Amazon Resource Name (ARN) that uniquely identifies the cluster.
        :param topic_name: The Kafka topic name that uniquely identifies the topic.
        :param max_results: The maximum number of results to return in the response.
        :param next_token: The paginated results marker.
        :returns: DescribeTopicPartitionsResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        """
        raise NotImplementedError

    @handler("DescribeVpcConnection")
    def describe_vpc_connection(
        self, context: RequestContext, arn: _string, **kwargs
    ) -> DescribeVpcConnectionResponse:
        """Returns a description of this MSK VPC connection.

        :param arn: The Amazon Resource Name (ARN) that uniquely identifies a MSK VPC
        connection.
        :returns: DescribeVpcConnectionResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("BatchDisassociateScramSecret")
    def batch_disassociate_scram_secret(
        self,
        context: RequestContext,
        cluster_arn: _string,
        secret_arn_list: _listOf__string,
        **kwargs,
    ) -> BatchDisassociateScramSecretResponse:
        """Disassociates one or more Scram Secrets from an Amazon MSK cluster.

        :param cluster_arn: The Amazon Resource Name (ARN) of the cluster to be updated.
        :param secret_arn_list: List of AWS Secrets Manager secret ARNs.
        :returns: BatchDisassociateScramSecretResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetBootstrapBrokers")
    def get_bootstrap_brokers(
        self, context: RequestContext, cluster_arn: _string, **kwargs
    ) -> GetBootstrapBrokersResponse:
        """A list of brokers that a client application can use to bootstrap. This
        list doesn't necessarily include all of the brokers in the cluster. The
        following Python 3.6 example shows how you can use the Amazon Resource
        Name (ARN) of a cluster to get its bootstrap brokers. If you don't know
        the ARN of your cluster, you can use the ``ListClusters`` operation to
        get the ARNs of all the clusters in this account and Region.

        :param cluster_arn: The Amazon Resource Name (ARN) that uniquely identifies the cluster.
        :returns: GetBootstrapBrokersResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ConflictException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("GetCompatibleKafkaVersions")
    def get_compatible_kafka_versions(
        self, context: RequestContext, cluster_arn: _string | None = None, **kwargs
    ) -> GetCompatibleKafkaVersionsResponse:
        """Gets the Apache Kafka versions to which you can update the MSK cluster.

        :param cluster_arn: The Amazon Resource Name (ARN) of the cluster check.
        :returns: GetCompatibleKafkaVersionsResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("GetClusterPolicy")
    def get_cluster_policy(
        self, context: RequestContext, cluster_arn: _string, **kwargs
    ) -> GetClusterPolicyResponse:
        """Get the MSK cluster policy specified by the Amazon Resource Name (ARN)
        in the request.

        :param cluster_arn: The Amazon Resource Name (ARN) of the cluster.
        :returns: GetClusterPolicyResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ListClusterOperations")
    def list_cluster_operations(
        self,
        context: RequestContext,
        cluster_arn: _string,
        max_results: MaxResults | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> ListClusterOperationsResponse:
        """Returns a list of all the operations that have been performed on the
        specified MSK cluster.

        :param cluster_arn: The Amazon Resource Name (ARN) that uniquely identifies the cluster.
        :param max_results: The maximum number of results to return in the response.
        :param next_token: The paginated results marker.
        :returns: ListClusterOperationsResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises UnauthorizedException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ListClusterOperationsV2")
    def list_cluster_operations_v2(
        self,
        context: RequestContext,
        cluster_arn: _string,
        max_results: MaxResults | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> ListClusterOperationsV2Response:
        """Returns a list of all the operations that have been performed on the
        specified MSK cluster.

        :param cluster_arn: The arn of the cluster whose operations are being requested.
        :param max_results: The maxResults of the query.
        :param next_token: The nextToken of the query.
        :returns: ListClusterOperationsV2Response
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("ListClusters")
    def list_clusters(
        self,
        context: RequestContext,
        cluster_name_filter: _string | None = None,
        max_results: MaxResults | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> ListClustersResponse:
        """Returns a list of all the MSK clusters in the current Region.

        :param cluster_name_filter: Specify a prefix of the name of the clusters that you want to list.
        :param max_results: The maximum number of results to return in the response.
        :param next_token: The paginated results marker.
        :returns: ListClustersResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises UnauthorizedException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ListClustersV2")
    def list_clusters_v2(
        self,
        context: RequestContext,
        cluster_name_filter: _string | None = None,
        cluster_type_filter: _string | None = None,
        max_results: MaxResults | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> ListClustersV2Response:
        """Returns a list of all the MSK clusters in the current Region.

        :param cluster_name_filter: Specify a prefix of the names of the clusters that you want to list.
        :param cluster_type_filter: Specify either PROVISIONED or SERVERLESS.
        :param max_results: The maximum number of results to return in the response.
        :param next_token: The paginated results marker.
        :returns: ListClustersV2Response
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises UnauthorizedException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ListConfigurationRevisions")
    def list_configuration_revisions(
        self,
        context: RequestContext,
        arn: _string,
        max_results: MaxResults | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> ListConfigurationRevisionsResponse:
        """Returns a list of all the MSK configurations in this Region.

        :param arn: The Amazon Resource Name (ARN) that uniquely identifies an MSK
        configuration and all of its revisions.
        :param max_results: The maximum number of results to return in the response.
        :param next_token: The paginated results marker.
        :returns: ListConfigurationRevisionsResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
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
        """Returns a list of all the MSK configurations in this Region.

        :param max_results: The maximum number of results to return in the response.
        :param next_token: The paginated results marker.
        :returns: ListConfigurationsResponse
        :raises ServiceUnavailableException:
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ListKafkaVersions")
    def list_kafka_versions(
        self,
        context: RequestContext,
        max_results: MaxResults | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> ListKafkaVersionsResponse:
        """Returns a list of Apache Kafka versions.

        :param max_results: The maximum number of results to return in the response.
        :param next_token: The paginated results marker.
        :returns: ListKafkaVersionsResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ListNodes")
    def list_nodes(
        self,
        context: RequestContext,
        cluster_arn: _string,
        max_results: MaxResults | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> ListNodesResponse:
        """Returns a list of the broker nodes in the cluster.

        :param cluster_arn: The Amazon Resource Name (ARN) that uniquely identifies the cluster.
        :param max_results: The maximum number of results to return in the response.
        :param next_token: The paginated results marker.
        :returns: ListNodesResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ListReplicators")
    def list_replicators(
        self,
        context: RequestContext,
        max_results: MaxResults | None = None,
        next_token: _string | None = None,
        replicator_name_filter: _string | None = None,
        **kwargs,
    ) -> ListReplicatorsResponse:
        """Lists the replicators.

        :param max_results: The maximum number of results to return in the response.
        :param next_token: If the response of ListReplicators is truncated, it returns a NextToken
        in the response.
        :param replicator_name_filter: Returns replicators starting with given name.
        :returns: ListReplicatorsResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("ListScramSecrets")
    def list_scram_secrets(
        self,
        context: RequestContext,
        cluster_arn: _string,
        max_results: MaxResults | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> ListScramSecretsResponse:
        """Returns a list of the Scram Secrets associated with an Amazon MSK
        cluster.

        :param cluster_arn: The arn of the cluster.
        :param max_results: The maxResults of the query.
        :param next_token: The nextToken of the query.
        :returns: ListScramSecretsResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("ListTagsForResource")
    def list_tags_for_resource(
        self, context: RequestContext, resource_arn: _string, **kwargs
    ) -> ListTagsForResourceResponse:
        """Returns a list of the tags associated with the specified resource.

        :param resource_arn: The Amazon Resource Name (ARN) that uniquely identifies the resource
        that's associated with the tags.
        :returns: ListTagsForResourceResponse
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        """
        raise NotImplementedError

    @handler("ListClientVpcConnections")
    def list_client_vpc_connections(
        self,
        context: RequestContext,
        cluster_arn: _string,
        max_results: MaxResults | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> ListClientVpcConnectionsResponse:
        """Returns a list of all the VPC connections in this Region.

        :param cluster_arn: The Amazon Resource Name (ARN) of the cluster.
        :param max_results: The maximum number of results to return in the response.
        :param next_token: The paginated results marker.
        :returns: ListClientVpcConnectionsResponse
        :raises ServiceUnavailableException:
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ListTopics")
    def list_topics(
        self,
        context: RequestContext,
        cluster_arn: _string,
        max_results: MaxResults | None = None,
        next_token: _string | None = None,
        topic_name_filter: _string | None = None,
        **kwargs,
    ) -> ListTopicsResponse:
        """List topics in a MSK cluster.

        :param cluster_arn: The Amazon Resource Name (ARN) that uniquely identifies the cluster.
        :param max_results: The maximum number of results to return in the response.
        :param next_token: The paginated results marker.
        :param topic_name_filter: Returns topics starting with given name.
        :returns: ListTopicsResponse
        :raises ServiceUnavailableException:
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("ListVpcConnections")
    def list_vpc_connections(
        self,
        context: RequestContext,
        max_results: MaxResults | None = None,
        next_token: _string | None = None,
        **kwargs,
    ) -> ListVpcConnectionsResponse:
        """Returns a list of all the VPC connections in this Region.

        :param max_results: The maximum number of results to return in the response.
        :param next_token: The paginated results marker.
        :returns: ListVpcConnectionsResponse
        :raises ServiceUnavailableException:
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("RejectClientVpcConnection")
    def reject_client_vpc_connection(
        self, context: RequestContext, vpc_connection_arn: _string, cluster_arn: _string, **kwargs
    ) -> RejectClientVpcConnectionResponse:
        """Returns empty response.

        :param vpc_connection_arn: The VPC connection ARN.
        :param cluster_arn: The Amazon Resource Name (ARN) of the cluster.
        :returns: RejectClientVpcConnectionResponse
        :raises ServiceUnavailableException:
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("PutClusterPolicy")
    def put_cluster_policy(
        self,
        context: RequestContext,
        cluster_arn: _string,
        policy: _string,
        current_version: _string | None = None,
        **kwargs,
    ) -> PutClusterPolicyResponse:
        """Creates or updates the MSK cluster policy specified by the cluster
        Amazon Resource Name (ARN) in the request.

        :param cluster_arn: The Amazon Resource Name (ARN) of the cluster.
        :param policy: The policy.
        :param current_version: The policy version.
        :returns: PutClusterPolicyResponse
        :raises BadRequestException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("RebootBroker")
    def reboot_broker(
        self, context: RequestContext, cluster_arn: _string, broker_ids: _listOf__string, **kwargs
    ) -> RebootBrokerResponse:
        """Reboots brokers.

        :param cluster_arn: The Amazon Resource Name (ARN) of the cluster to be updated.
        :param broker_ids: The list of broker IDs to be rebooted.
        :returns: RebootBrokerResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("TagResource")
    def tag_resource(
        self, context: RequestContext, resource_arn: _string, tags: _mapOf__string, **kwargs
    ) -> None:
        """Adds tags to the specified MSK resource.

        :param resource_arn: The Amazon Resource Name (ARN) that uniquely identifies the resource
        that's associated with the tags.
        :param tags: The key-value pair for the resource tag.
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        """
        raise NotImplementedError

    @handler("UntagResource")
    def untag_resource(
        self, context: RequestContext, tag_keys: _listOf__string, resource_arn: _string, **kwargs
    ) -> None:
        """Removes the tags associated with the keys that are provided in the
        query.

        :param tag_keys: Tag keys must be unique for a given cluster.
        :param resource_arn: The Amazon Resource Name (ARN) that uniquely identifies the resource
        that's associated with the tags.
        :raises NotFoundException:
        :raises BadRequestException:
        :raises InternalServerErrorException:
        """
        raise NotImplementedError

    @handler("UpdateBrokerCount")
    def update_broker_count(
        self,
        context: RequestContext,
        cluster_arn: _string,
        current_version: _string,
        target_number_of_broker_nodes: _integerMin1Max15,
        **kwargs,
    ) -> UpdateBrokerCountResponse:
        """Updates the number of broker nodes in the cluster.

        :param cluster_arn: The Amazon Resource Name (ARN) that uniquely identifies the cluster.
        :param current_version: The version of cluster to update from.
        :param target_number_of_broker_nodes: The number of broker nodes that you want the cluster to have after this
        operation completes successfully.
        :returns: UpdateBrokerCountResponse
        :raises ServiceUnavailableException:
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("UpdateBrokerType")
    def update_broker_type(
        self,
        context: RequestContext,
        cluster_arn: _string,
        current_version: _string,
        target_instance_type: _string,
        **kwargs,
    ) -> UpdateBrokerTypeResponse:
        """Updates EC2 instance type.

        :param cluster_arn: The Amazon Resource Name (ARN) that uniquely identifies the cluster.
        :param current_version: The cluster version that you want to change.
        :param target_instance_type: The Amazon MSK broker type that you want all of the brokers in this
        cluster to be.
        :returns: UpdateBrokerTypeResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateBrokerStorage")
    def update_broker_storage(
        self,
        context: RequestContext,
        cluster_arn: _string,
        target_broker_ebs_volume_info: _listOfBrokerEBSVolumeInfo,
        current_version: _string,
        **kwargs,
    ) -> UpdateBrokerStorageResponse:
        """Updates the EBS storage associated with MSK brokers.

        :param cluster_arn: The Amazon Resource Name (ARN) that uniquely identifies the cluster.
        :param target_broker_ebs_volume_info: Describes the target volume size and the ID of the broker to apply the
        update to.
        :param current_version: The version of cluster to update from.
        :returns: UpdateBrokerStorageResponse
        :raises ServiceUnavailableException:
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("UpdateConfiguration")
    def update_configuration(
        self,
        context: RequestContext,
        arn: _string,
        server_properties: _blob,
        description: _string | None = None,
        **kwargs,
    ) -> UpdateConfigurationResponse:
        """Updates an MSK configuration.

        :param arn: The Amazon Resource Name (ARN) of the configuration.
        :param server_properties: Contents of the server.
        :param description: The description of the configuration revision.
        :returns: UpdateConfigurationResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("UpdateConnectivity")
    def update_connectivity(
        self,
        context: RequestContext,
        cluster_arn: _string,
        connectivity_info: ConnectivityInfo,
        current_version: _string,
        **kwargs,
    ) -> UpdateConnectivityResponse:
        """Updates the cluster's connectivity configuration.

        :param cluster_arn: The Amazon Resource Name (ARN) of the configuration.
        :param connectivity_info: Information about the broker access configuration.
        :param current_version: The version of the MSK cluster to update.
        :returns: UpdateConnectivityResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("UpdateClusterConfiguration")
    def update_cluster_configuration(
        self,
        context: RequestContext,
        cluster_arn: _string,
        current_version: _string,
        configuration_info: ConfigurationInfo,
        **kwargs,
    ) -> UpdateClusterConfigurationResponse:
        """Updates the cluster with the configuration that is specified in the
        request body.

        :param cluster_arn: The Amazon Resource Name (ARN) that uniquely identifies the cluster.
        :param current_version: The version of the cluster that needs to be updated.
        :param configuration_info: Represents the configuration that you want MSK to use for the brokers in
        a cluster.
        :returns: UpdateClusterConfigurationResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        """
        raise NotImplementedError

    @handler("UpdateClusterKafkaVersion")
    def update_cluster_kafka_version(
        self,
        context: RequestContext,
        cluster_arn: _string,
        target_kafka_version: _string,
        current_version: _string,
        configuration_info: ConfigurationInfo | None = None,
        **kwargs,
    ) -> UpdateClusterKafkaVersionResponse:
        """Updates the Apache Kafka version for the cluster.

        :param cluster_arn: The Amazon Resource Name (ARN) of the cluster to be updated.
        :param target_kafka_version: Target Kafka version.
        :param current_version: Current cluster version.
        :param configuration_info: The custom configuration that should be applied on the new version of
        cluster.
        :returns: UpdateClusterKafkaVersionResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateMonitoring")
    def update_monitoring(
        self,
        context: RequestContext,
        cluster_arn: _string,
        current_version: _string,
        enhanced_monitoring: EnhancedMonitoring | None = None,
        open_monitoring: OpenMonitoringInfo | None = None,
        logging_info: LoggingInfo | None = None,
        **kwargs,
    ) -> UpdateMonitoringResponse:
        """Updates the monitoring settings for the cluster. You can use this
        operation to specify which Apache Kafka metrics you want Amazon MSK to
        send to Amazon CloudWatch. You can also specify settings for open
        monitoring with Prometheus.

        :param cluster_arn: The Amazon Resource Name (ARN) that uniquely identifies the cluster.
        :param current_version: The version of the MSK cluster to update.
        :param enhanced_monitoring: Specifies which Apache Kafka metrics Amazon MSK gathers and sends to
        Amazon CloudWatch for this cluster.
        :param open_monitoring: The settings for open monitoring.
        :param logging_info: .
        :returns: UpdateMonitoringResponse
        :raises ServiceUnavailableException:
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        """
        raise NotImplementedError

    @handler("UpdateRebalancing")
    def update_rebalancing(
        self,
        context: RequestContext,
        cluster_arn: _string,
        current_version: _string,
        rebalancing: Rebalancing,
        **kwargs,
    ) -> UpdateRebalancingResponse:
        """Use this resource to update the intelligent rebalancing status of an
        Amazon MSK Provisioned cluster with Express brokers.

        :param cluster_arn: The Amazon Resource Name (ARN) of the cluster.
        :param current_version: The current version of the cluster.
        :param rebalancing: Specifies if intelligent rebalancing should be turned on for your
        cluster.
        :returns: UpdateRebalancingResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateReplicationInfo")
    def update_replication_info(
        self,
        context: RequestContext,
        replicator_arn: _string,
        source_kafka_cluster_arn: _string,
        current_version: _string,
        target_kafka_cluster_arn: _string,
        consumer_group_replication: ConsumerGroupReplicationUpdate | None = None,
        topic_replication: TopicReplicationUpdate | None = None,
        **kwargs,
    ) -> UpdateReplicationInfoResponse:
        """Updates replication info of a replicator.

        :param replicator_arn: The Amazon Resource Name (ARN) of the replicator to be updated.
        :param source_kafka_cluster_arn: The ARN of the source Kafka cluster.
        :param current_version: Current replicator version.
        :param target_kafka_cluster_arn: The ARN of the target Kafka cluster.
        :param consumer_group_replication: Updated consumer group replication information.
        :param topic_replication: Updated topic replication information.
        :returns: UpdateReplicationInfoResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateSecurity")
    def update_security(
        self,
        context: RequestContext,
        cluster_arn: _string,
        current_version: _string,
        client_authentication: ClientAuthentication | None = None,
        encryption_info: EncryptionInfo | None = None,
        **kwargs,
    ) -> UpdateSecurityResponse:
        """Updates the security settings for the cluster. You can use this
        operation to specify encryption and authentication on existing clusters.

        :param cluster_arn: The Amazon Resource Name (ARN) that uniquely identifies the cluster.
        :param current_version: The version of the MSK cluster to update.
        :param client_authentication: Includes all client authentication related information.
        :param encryption_info: Includes all encryption-related information.
        :returns: UpdateSecurityResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError

    @handler("UpdateStorage")
    def update_storage(
        self,
        context: RequestContext,
        cluster_arn: _string,
        current_version: _string,
        provisioned_throughput: ProvisionedThroughput | None = None,
        storage_mode: StorageMode | None = None,
        volume_size_gb: _integer | None = None,
        **kwargs,
    ) -> UpdateStorageResponse:
        """Updates cluster broker volume size (or) sets cluster storage mode to
        TIERED.

        :param cluster_arn: The Amazon Resource Name (ARN) of the cluster to be updated.
        :param current_version: The version of cluster to update from.
        :param provisioned_throughput: EBS volume provisioned throughput information.
        :param storage_mode: Controls storage mode for supported storage tiers.
        :param volume_size_gb: size of the EBS volume to update.
        :returns: UpdateStorageResponse
        :raises BadRequestException:
        :raises UnauthorizedException:
        :raises InternalServerErrorException:
        :raises ForbiddenException:
        :raises NotFoundException:
        :raises ServiceUnavailableException:
        :raises TooManyRequestsException:
        """
        raise NotImplementedError
