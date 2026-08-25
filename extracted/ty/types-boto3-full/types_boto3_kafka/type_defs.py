"""
Type annotations for kafka service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kafka/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_kafka.type_defs import AmazonMskClusterTypeDef

    data: AmazonMskClusterTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import IO, Any, Union

from botocore.response import StreamingBody

from .literals import (
    ChannelDestinationTypeType,
    ChannelStatusType,
    ClientBrokerType,
    ClusterStateType,
    ClusterTypeType,
    ConfigurationStateType,
    ConsumerGroupOffsetSyncModeType,
    CustomerActionStatusType,
    EnhancedMonitoringType,
    IcebergCompressionTypeType,
    JwtSigningAlgorithmType,
    KafkaClusterSaslScramMechanismType,
    KafkaVersionStatusType,
    NetworkTypeType,
    RebalancingStatusType,
    ReplicationStartingPositionTypeType,
    ReplicationTopicNameConfigurationTypeType,
    ReplicatorStateType,
    S3CompressionTypeType,
    S3StorageClassType,
    StorageModeType,
    TargetCompressionTypeType,
    TokenEndpointAuthenticationMethodType,
    TopicStateType,
    UserIdentityTypeType,
    ValueConverterType,
    VpcConnectionStateType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AmazonMskClusterTypeDef",
    "ApacheKafkaClusterTypeDef",
    "AuthorizerLogsTypeDef",
    "BatchAssociateScramSecretRequestTypeDef",
    "BatchAssociateScramSecretResponseTypeDef",
    "BatchDisassociateScramSecretRequestTypeDef",
    "BatchDisassociateScramSecretResponseTypeDef",
    "BlobTypeDef",
    "BrokerCountUpdateInfoTypeDef",
    "BrokerEBSVolumeInfoTypeDef",
    "BrokerLogsTypeDef",
    "BrokerNodeGroupInfoOutputTypeDef",
    "BrokerNodeGroupInfoTypeDef",
    "BrokerNodeGroupInfoUnionTypeDef",
    "BrokerNodeInfoTypeDef",
    "BrokerSoftwareInfoTypeDef",
    "CatalogTypeDef",
    "ChannelInfoTypeDef",
    "ChannelLoggingInfoTypeDef",
    "ChannelStateInfoTypeDef",
    "ClientAuthenticationOutputTypeDef",
    "ClientAuthenticationTypeDef",
    "ClientAuthenticationUnionTypeDef",
    "ClientVpcConnectionTypeDef",
    "CloudWatchLogsTypeDef",
    "ClusterInfoTypeDef",
    "ClusterOperationInfoTypeDef",
    "ClusterOperationStepInfoTypeDef",
    "ClusterOperationStepTypeDef",
    "ClusterOperationV2ProvisionedTypeDef",
    "ClusterOperationV2ServerlessTypeDef",
    "ClusterOperationV2SummaryTypeDef",
    "ClusterOperationV2TypeDef",
    "ClusterTypeDef",
    "CompatibleKafkaVersionTypeDef",
    "ConfigurationInfoTypeDef",
    "ConfigurationRevisionTypeDef",
    "ConfigurationTypeDef",
    "ConnectivityInfoTypeDef",
    "ConsumerGroupReplicationOutputTypeDef",
    "ConsumerGroupReplicationTypeDef",
    "ConsumerGroupReplicationUnionTypeDef",
    "ConsumerGroupReplicationUpdateTypeDef",
    "ControllerNodeInfoTypeDef",
    "CreateChannelRequestTypeDef",
    "CreateChannelResponseTypeDef",
    "CreateClusterRequestTypeDef",
    "CreateClusterResponseTypeDef",
    "CreateClusterV2RequestTypeDef",
    "CreateClusterV2ResponseTypeDef",
    "CreateConfigurationRequestTypeDef",
    "CreateConfigurationResponseTypeDef",
    "CreateReplicatorRequestTypeDef",
    "CreateReplicatorResponseTypeDef",
    "CreateTopicRequestTypeDef",
    "CreateTopicResponseTypeDef",
    "CreateVpcConnectionRequestTypeDef",
    "CreateVpcConnectionResponseTypeDef",
    "DeadLetterQueueS3TypeDef",
    "DeleteChannelRequestTypeDef",
    "DeleteChannelResponseTypeDef",
    "DeleteClusterPolicyRequestTypeDef",
    "DeleteClusterRequestTypeDef",
    "DeleteClusterResponseTypeDef",
    "DeleteConfigurationRequestTypeDef",
    "DeleteConfigurationResponseTypeDef",
    "DeleteReplicatorRequestTypeDef",
    "DeleteReplicatorResponseTypeDef",
    "DeleteTopicRequestTypeDef",
    "DeleteTopicResponseTypeDef",
    "DeleteVpcConnectionRequestTypeDef",
    "DeleteVpcConnectionResponseTypeDef",
    "DescribeChannelRequestTypeDef",
    "DescribeChannelResponseTypeDef",
    "DescribeClusterOperationRequestTypeDef",
    "DescribeClusterOperationResponseTypeDef",
    "DescribeClusterOperationV2RequestTypeDef",
    "DescribeClusterOperationV2ResponseTypeDef",
    "DescribeClusterRequestTypeDef",
    "DescribeClusterResponseTypeDef",
    "DescribeClusterV2RequestTypeDef",
    "DescribeClusterV2ResponseTypeDef",
    "DescribeConfigurationRequestTypeDef",
    "DescribeConfigurationResponseTypeDef",
    "DescribeConfigurationRevisionRequestTypeDef",
    "DescribeConfigurationRevisionResponseTypeDef",
    "DescribeReplicatorRequestTypeDef",
    "DescribeReplicatorResponseTypeDef",
    "DescribeTopicPartitionsRequestPaginateTypeDef",
    "DescribeTopicPartitionsRequestTypeDef",
    "DescribeTopicPartitionsResponseTypeDef",
    "DescribeTopicRequestTypeDef",
    "DescribeTopicResponseTypeDef",
    "DescribeVpcConnectionRequestTypeDef",
    "DescribeVpcConnectionResponseTypeDef",
    "DestinationTableOutputTypeDef",
    "DestinationTableTypeDef",
    "EBSStorageInfoTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EncryptionAtRestTypeDef",
    "EncryptionConfigurationTypeDef",
    "EncryptionInTransitTypeDef",
    "EncryptionInfoTypeDef",
    "ErrorInfoTypeDef",
    "FirehoseTypeDef",
    "GetBootstrapBrokersRequestTypeDef",
    "GetBootstrapBrokersResponseTypeDef",
    "GetClusterPolicyRequestTypeDef",
    "GetClusterPolicyResponseTypeDef",
    "GetCompatibleKafkaVersionsRequestTypeDef",
    "GetCompatibleKafkaVersionsResponseTypeDef",
    "IamTypeDef",
    "IcebergDestinationConfigurationOutputTypeDef",
    "IcebergDestinationConfigurationTypeDef",
    "IcebergDestinationConfigurationUnionTypeDef",
    "IcebergDestinationUpdateTypeDef",
    "JmxExporterInfoTypeDef",
    "JmxExporterTypeDef",
    "KafkaClusterClientAuthenticationTypeDef",
    "KafkaClusterClientVpcConfigOutputTypeDef",
    "KafkaClusterClientVpcConfigTypeDef",
    "KafkaClusterClientVpcConfigUnionTypeDef",
    "KafkaClusterDescriptionTypeDef",
    "KafkaClusterEncryptionInTransitTypeDef",
    "KafkaClusterMTLSAuthenticationTypeDef",
    "KafkaClusterOAuthClientCredentialsAssertionTypeDef",
    "KafkaClusterOAuthClientCredentialsTypeDef",
    "KafkaClusterOAuthIamJwtBearerTypeDef",
    "KafkaClusterSaslOAuthBearerAuthenticationTypeDef",
    "KafkaClusterSaslScramAuthenticationTypeDef",
    "KafkaClusterSummaryTypeDef",
    "KafkaClusterTypeDef",
    "KafkaVersionTypeDef",
    "ListChannelsRequestTypeDef",
    "ListChannelsResponseTypeDef",
    "ListClientVpcConnectionsRequestPaginateTypeDef",
    "ListClientVpcConnectionsRequestTypeDef",
    "ListClientVpcConnectionsResponseTypeDef",
    "ListClusterOperationsRequestPaginateTypeDef",
    "ListClusterOperationsRequestTypeDef",
    "ListClusterOperationsResponseTypeDef",
    "ListClusterOperationsV2RequestPaginateTypeDef",
    "ListClusterOperationsV2RequestTypeDef",
    "ListClusterOperationsV2ResponseTypeDef",
    "ListClustersRequestPaginateTypeDef",
    "ListClustersRequestTypeDef",
    "ListClustersResponseTypeDef",
    "ListClustersV2RequestPaginateTypeDef",
    "ListClustersV2RequestTypeDef",
    "ListClustersV2ResponseTypeDef",
    "ListConfigurationRevisionsRequestPaginateTypeDef",
    "ListConfigurationRevisionsRequestTypeDef",
    "ListConfigurationRevisionsResponseTypeDef",
    "ListConfigurationsRequestPaginateTypeDef",
    "ListConfigurationsRequestTypeDef",
    "ListConfigurationsResponseTypeDef",
    "ListKafkaVersionsRequestPaginateTypeDef",
    "ListKafkaVersionsRequestTypeDef",
    "ListKafkaVersionsResponseTypeDef",
    "ListNodesRequestPaginateTypeDef",
    "ListNodesRequestTypeDef",
    "ListNodesResponseTypeDef",
    "ListReplicatorsRequestPaginateTypeDef",
    "ListReplicatorsRequestTypeDef",
    "ListReplicatorsResponseTypeDef",
    "ListScramSecretsRequestPaginateTypeDef",
    "ListScramSecretsRequestTypeDef",
    "ListScramSecretsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTopicsRequestPaginateTypeDef",
    "ListTopicsRequestTypeDef",
    "ListTopicsResponseTypeDef",
    "ListVpcConnectionsRequestPaginateTypeDef",
    "ListVpcConnectionsRequestTypeDef",
    "ListVpcConnectionsResponseTypeDef",
    "LogDeliveryTypeDef",
    "LoggingInfoTypeDef",
    "MutableClusterInfoTypeDef",
    "NodeExporterInfoTypeDef",
    "NodeExporterTypeDef",
    "NodeInfoTypeDef",
    "OpenMonitoringInfoTypeDef",
    "OpenMonitoringTypeDef",
    "PaginatorConfigTypeDef",
    "PartitionSourceTypeDef",
    "PartitionSpecOutputTypeDef",
    "PartitionSpecTypeDef",
    "PrometheusInfoTypeDef",
    "PrometheusTypeDef",
    "ProvisionedRequestTypeDef",
    "ProvisionedThroughputTypeDef",
    "ProvisionedTypeDef",
    "PublicAccessTypeDef",
    "PutClusterPolicyRequestTypeDef",
    "PutClusterPolicyResponseTypeDef",
    "RebalancingTypeDef",
    "RebootBrokerRequestTypeDef",
    "RebootBrokerResponseTypeDef",
    "RecordConverterTypeDef",
    "RecordSchemaTypeDef",
    "RejectClientVpcConnectionRequestTypeDef",
    "ReplicationInfoDescriptionTypeDef",
    "ReplicationInfoSummaryTypeDef",
    "ReplicationInfoTypeDef",
    "ReplicationStartingPositionTypeDef",
    "ReplicationStateInfoTypeDef",
    "ReplicationTopicNameConfigurationTypeDef",
    "ReplicatorCloudWatchLogsTypeDef",
    "ReplicatorFirehoseTypeDef",
    "ReplicatorLogDeliveryTypeDef",
    "ReplicatorS3TypeDef",
    "ReplicatorSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "S3DestinationConfigurationTypeDef",
    "S3DestinationUpdateTypeDef",
    "S3StorageTypeDef",
    "S3TypeDef",
    "SaslTypeDef",
    "SchemaEvolutionTypeDef",
    "ScramTypeDef",
    "ServerlessClientAuthenticationTypeDef",
    "ServerlessConnectivityInfoTypeDef",
    "ServerlessRequestTypeDef",
    "ServerlessSaslTypeDef",
    "ServerlessTypeDef",
    "StateInfoTypeDef",
    "StorageInfoTypeDef",
    "TableCreationTypeDef",
    "TagResourceRequestTypeDef",
    "TlsOutputTypeDef",
    "TlsTypeDef",
    "TlsUnionTypeDef",
    "TopicConfigurationTypeDef",
    "TopicInfoTypeDef",
    "TopicPartitionInfoTypeDef",
    "TopicReplicationOutputTypeDef",
    "TopicReplicationTypeDef",
    "TopicReplicationUnionTypeDef",
    "TopicReplicationUpdateTypeDef",
    "UnauthenticatedTypeDef",
    "UnprocessedScramSecretTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateBrokerCountRequestTypeDef",
    "UpdateBrokerCountResponseTypeDef",
    "UpdateBrokerStorageRequestTypeDef",
    "UpdateBrokerStorageResponseTypeDef",
    "UpdateBrokerTypeRequestTypeDef",
    "UpdateBrokerTypeResponseTypeDef",
    "UpdateChannelRequestTypeDef",
    "UpdateChannelResponseTypeDef",
    "UpdateClusterConfigurationRequestTypeDef",
    "UpdateClusterConfigurationResponseTypeDef",
    "UpdateClusterKafkaVersionRequestTypeDef",
    "UpdateClusterKafkaVersionResponseTypeDef",
    "UpdateConfigurationRequestTypeDef",
    "UpdateConfigurationResponseTypeDef",
    "UpdateConnectivityRequestTypeDef",
    "UpdateConnectivityResponseTypeDef",
    "UpdateMonitoringRequestTypeDef",
    "UpdateMonitoringResponseTypeDef",
    "UpdateRebalancingRequestTypeDef",
    "UpdateRebalancingResponseTypeDef",
    "UpdateReplicationInfoRequestTypeDef",
    "UpdateReplicationInfoResponseTypeDef",
    "UpdateSecurityRequestTypeDef",
    "UpdateSecurityResponseTypeDef",
    "UpdateStorageRequestTypeDef",
    "UpdateStorageResponseTypeDef",
    "UpdateTopicRequestTypeDef",
    "UpdateTopicResponseTypeDef",
    "UserIdentityTypeDef",
    "VpcConfigOutputTypeDef",
    "VpcConfigTypeDef",
    "VpcConfigUnionTypeDef",
    "VpcConnectionInfoServerlessTypeDef",
    "VpcConnectionInfoTypeDef",
    "VpcConnectionTypeDef",
    "VpcConnectivityClientAuthenticationTypeDef",
    "VpcConnectivityIamTypeDef",
    "VpcConnectivitySaslTypeDef",
    "VpcConnectivityScramTypeDef",
    "VpcConnectivityTlsTypeDef",
    "VpcConnectivityTypeDef",
    "ZookeeperAccessTypeDef",
    "ZookeeperNodeInfoTypeDef",
)


class AmazonMskClusterTypeDef(TypedDict):
    MskClusterArn: str


class ApacheKafkaClusterTypeDef(TypedDict):
    ApacheKafkaClusterId: str
    BootstrapBrokerString: str


class CloudWatchLogsTypeDef(TypedDict):
    Enabled: bool
    LogGroup: NotRequired[str]


class FirehoseTypeDef(TypedDict):
    Enabled: bool
    DeliveryStream: NotRequired[str]


class S3TypeDef(TypedDict):
    Enabled: bool
    Bucket: NotRequired[str]
    Prefix: NotRequired[str]


class BatchAssociateScramSecretRequestTypeDef(TypedDict):
    ClusterArn: str
    SecretArnList: Sequence[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class UnprocessedScramSecretTypeDef(TypedDict):
    ErrorCode: NotRequired[str]
    ErrorMessage: NotRequired[str]
    SecretArn: NotRequired[str]


class BatchDisassociateScramSecretRequestTypeDef(TypedDict):
    ClusterArn: str
    SecretArnList: Sequence[str]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class BrokerCountUpdateInfoTypeDef(TypedDict):
    CreatedBrokerIds: NotRequired[list[float]]
    DeletedBrokerIds: NotRequired[list[float]]


class ProvisionedThroughputTypeDef(TypedDict):
    Enabled: NotRequired[bool]
    VolumeThroughput: NotRequired[int]


class BrokerSoftwareInfoTypeDef(TypedDict):
    ConfigurationArn: NotRequired[str]
    ConfigurationRevision: NotRequired[int]
    KafkaVersion: NotRequired[str]


class CatalogTypeDef(TypedDict):
    CatalogArn: NotRequired[str]
    WarehouseLocation: NotRequired[str]


class ChannelInfoTypeDef(TypedDict):
    ChannelArn: str
    ChannelName: str
    Status: ChannelStatusType
    CreationTime: datetime
    DestinationType: ChannelDestinationTypeType
    ClusterOperationArn: NotRequired[str]


class ChannelStateInfoTypeDef(TypedDict):
    Code: NotRequired[str]
    Message: NotRequired[str]


class TlsOutputTypeDef(TypedDict):
    CertificateAuthorityArnList: NotRequired[list[str]]
    Enabled: NotRequired[bool]


class UnauthenticatedTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class ClientVpcConnectionTypeDef(TypedDict):
    VpcConnectionArn: str
    Authentication: NotRequired[str]
    CreationTime: NotRequired[datetime]
    State: NotRequired[VpcConnectionStateType]
    Owner: NotRequired[str]


class RebalancingTypeDef(TypedDict):
    Status: NotRequired[RebalancingStatusType]


class StateInfoTypeDef(TypedDict):
    Code: NotRequired[str]
    Message: NotRequired[str]


class ErrorInfoTypeDef(TypedDict):
    ErrorCode: NotRequired[str]
    ErrorString: NotRequired[str]


class ClusterOperationStepInfoTypeDef(TypedDict):
    StepStatus: NotRequired[str]


class ServerlessConnectivityInfoTypeDef(TypedDict):
    NetworkType: NotRequired[NetworkTypeType]


class ClusterOperationV2SummaryTypeDef(TypedDict):
    ClusterArn: NotRequired[str]
    ClusterType: NotRequired[ClusterTypeType]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    OperationArn: NotRequired[str]
    OperationState: NotRequired[str]
    OperationType: NotRequired[str]


class CompatibleKafkaVersionTypeDef(TypedDict):
    SourceVersion: NotRequired[str]
    TargetVersions: NotRequired[list[str]]


class ConfigurationInfoTypeDef(TypedDict):
    Arn: str
    Revision: int


class ConfigurationRevisionTypeDef(TypedDict):
    CreationTime: datetime
    Revision: int
    Description: NotRequired[str]


PublicAccessTypeDef = TypedDict(
    "PublicAccessTypeDef",
    {
        "Type": NotRequired[str],
    },
)


class ConsumerGroupReplicationOutputTypeDef(TypedDict):
    ConsumerGroupsToReplicate: list[str]
    ConsumerGroupsToExclude: NotRequired[list[str]]
    DetectAndCopyNewConsumerGroups: NotRequired[bool]
    SynchroniseConsumerGroupOffsets: NotRequired[bool]
    ConsumerGroupOffsetSyncMode: NotRequired[ConsumerGroupOffsetSyncModeType]


class ConsumerGroupReplicationTypeDef(TypedDict):
    ConsumerGroupsToReplicate: Sequence[str]
    ConsumerGroupsToExclude: NotRequired[Sequence[str]]
    DetectAndCopyNewConsumerGroups: NotRequired[bool]
    SynchroniseConsumerGroupOffsets: NotRequired[bool]
    ConsumerGroupOffsetSyncMode: NotRequired[ConsumerGroupOffsetSyncModeType]


class ConsumerGroupReplicationUpdateTypeDef(TypedDict):
    ConsumerGroupsToExclude: Sequence[str]
    ConsumerGroupsToReplicate: Sequence[str]
    DetectAndCopyNewConsumerGroups: bool
    SynchroniseConsumerGroupOffsets: bool


class ControllerNodeInfoTypeDef(TypedDict):
    Endpoints: NotRequired[list[str]]


class EncryptionConfigurationTypeDef(TypedDict):
    KmsKeyArn: str


class CreateTopicRequestTypeDef(TypedDict):
    ClusterArn: str
    TopicName: str
    PartitionCount: int
    ReplicationFactor: int
    Configs: NotRequired[str]


class CreateVpcConnectionRequestTypeDef(TypedDict):
    TargetClusterArn: str
    Authentication: str
    VpcId: str
    ClientSubnets: Sequence[str]
    SecurityGroups: Sequence[str]
    Tags: NotRequired[Mapping[str, str]]


class DeadLetterQueueS3TypeDef(TypedDict):
    BucketArn: str
    ErrorOutputPrefix: NotRequired[str]
    ExpectedBucketOwner: NotRequired[str]


class DeleteChannelRequestTypeDef(TypedDict):
    ChannelArn: str
    ClusterArn: str


class DeleteClusterPolicyRequestTypeDef(TypedDict):
    ClusterArn: str


class DeleteClusterRequestTypeDef(TypedDict):
    ClusterArn: str
    CurrentVersion: NotRequired[str]


class DeleteConfigurationRequestTypeDef(TypedDict):
    Arn: str


class DeleteReplicatorRequestTypeDef(TypedDict):
    ReplicatorArn: str
    CurrentVersion: NotRequired[str]


class DeleteTopicRequestTypeDef(TypedDict):
    ClusterArn: str
    TopicName: str


class DeleteVpcConnectionRequestTypeDef(TypedDict):
    Arn: str


class DescribeChannelRequestTypeDef(TypedDict):
    ChannelArn: str
    ClusterArn: str


class DescribeClusterOperationRequestTypeDef(TypedDict):
    ClusterOperationArn: str


class DescribeClusterOperationV2RequestTypeDef(TypedDict):
    ClusterOperationArn: str


class DescribeClusterRequestTypeDef(TypedDict):
    ClusterArn: str


class DescribeClusterV2RequestTypeDef(TypedDict):
    ClusterArn: str


class DescribeConfigurationRequestTypeDef(TypedDict):
    Arn: str


class DescribeConfigurationRevisionRequestTypeDef(TypedDict):
    Arn: str
    Revision: int


class DescribeReplicatorRequestTypeDef(TypedDict):
    ReplicatorArn: str


class ReplicationStateInfoTypeDef(TypedDict):
    Code: NotRequired[str]
    Message: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeTopicPartitionsRequestTypeDef(TypedDict):
    ClusterArn: str
    TopicName: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class TopicPartitionInfoTypeDef(TypedDict):
    Partition: NotRequired[int]
    Leader: NotRequired[int]
    Replicas: NotRequired[list[int]]
    Isr: NotRequired[list[int]]


class DescribeTopicRequestTypeDef(TypedDict):
    ClusterArn: str
    TopicName: str


class DescribeVpcConnectionRequestTypeDef(TypedDict):
    Arn: str


class EncryptionAtRestTypeDef(TypedDict):
    DataVolumeKMSKeyId: str


class EncryptionInTransitTypeDef(TypedDict):
    ClientBroker: NotRequired[ClientBrokerType]
    InCluster: NotRequired[bool]


class GetBootstrapBrokersRequestTypeDef(TypedDict):
    ClusterArn: str


class GetClusterPolicyRequestTypeDef(TypedDict):
    ClusterArn: str


class GetCompatibleKafkaVersionsRequestTypeDef(TypedDict):
    ClusterArn: NotRequired[str]


class IamTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class SchemaEvolutionTypeDef(TypedDict):
    EnableSchemaEvolution: NotRequired[bool]


class TableCreationTypeDef(TypedDict):
    EnableTableCreation: NotRequired[bool]


class IcebergDestinationUpdateTypeDef(TypedDict):
    DataFreshnessInSeconds: int


class JmxExporterInfoTypeDef(TypedDict):
    EnabledInBroker: bool


class JmxExporterTypeDef(TypedDict):
    EnabledInBroker: bool


class KafkaClusterMTLSAuthenticationTypeDef(TypedDict):
    SecretArn: str


class KafkaClusterSaslScramAuthenticationTypeDef(TypedDict):
    Mechanism: KafkaClusterSaslScramMechanismType
    SecretArn: str


class KafkaClusterClientVpcConfigOutputTypeDef(TypedDict):
    SubnetIds: list[str]
    SecurityGroupIds: NotRequired[list[str]]


class KafkaClusterClientVpcConfigTypeDef(TypedDict):
    SubnetIds: Sequence[str]
    SecurityGroupIds: NotRequired[Sequence[str]]


class KafkaClusterEncryptionInTransitTypeDef(TypedDict):
    EncryptionType: Literal["TLS"]
    RootCaCertificate: NotRequired[str]


class KafkaClusterOAuthClientCredentialsAssertionTypeDef(TypedDict):
    Audience: str
    SigningAlgorithm: JwtSigningAlgorithmType
    TokenRequestSecretArn: NotRequired[str]


class KafkaClusterOAuthClientCredentialsTypeDef(TypedDict):
    TokenRequestSecretArn: str


class KafkaClusterOAuthIamJwtBearerTypeDef(TypedDict):
    Audience: str
    SigningAlgorithm: JwtSigningAlgorithmType
    TokenRequestSecretArn: NotRequired[str]


class KafkaVersionTypeDef(TypedDict):
    Version: NotRequired[str]
    Status: NotRequired[KafkaVersionStatusType]


class ListChannelsRequestTypeDef(TypedDict):
    ClusterArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    TopicNameFilter: NotRequired[str]


class ListClientVpcConnectionsRequestTypeDef(TypedDict):
    ClusterArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListClusterOperationsRequestTypeDef(TypedDict):
    ClusterArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListClusterOperationsV2RequestTypeDef(TypedDict):
    ClusterArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListClustersRequestTypeDef(TypedDict):
    ClusterNameFilter: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListClustersV2RequestTypeDef(TypedDict):
    ClusterNameFilter: NotRequired[str]
    ClusterTypeFilter: NotRequired[str]
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListConfigurationRevisionsRequestTypeDef(TypedDict):
    Arn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListConfigurationsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListKafkaVersionsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListNodesRequestTypeDef(TypedDict):
    ClusterArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListReplicatorsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    ReplicatorNameFilter: NotRequired[str]


class ListScramSecretsRequestTypeDef(TypedDict):
    ClusterArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceArn: str


class ListTopicsRequestTypeDef(TypedDict):
    ClusterArn: str
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]
    TopicNameFilter: NotRequired[str]


class TopicInfoTypeDef(TypedDict):
    TopicArn: NotRequired[str]
    TopicName: NotRequired[str]
    ReplicationFactor: NotRequired[int]
    PartitionCount: NotRequired[int]
    OutOfSyncReplicaCount: NotRequired[int]


class ListVpcConnectionsRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]


class VpcConnectionTypeDef(TypedDict):
    VpcConnectionArn: str
    TargetClusterArn: str
    CreationTime: NotRequired[datetime]
    Authentication: NotRequired[str]
    VpcId: NotRequired[str]
    State: NotRequired[VpcConnectionStateType]


class ZookeeperAccessTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class NodeExporterInfoTypeDef(TypedDict):
    EnabledInBroker: bool


class NodeExporterTypeDef(TypedDict):
    EnabledInBroker: bool


class ZookeeperNodeInfoTypeDef(TypedDict):
    AttachedENIId: NotRequired[str]
    ClientVpcIpAddress: NotRequired[str]
    Endpoints: NotRequired[list[str]]
    ZookeeperId: NotRequired[float]
    ZookeeperVersion: NotRequired[str]


class PartitionSourceTypeDef(TypedDict):
    SourceName: NotRequired[str]


class PutClusterPolicyRequestTypeDef(TypedDict):
    ClusterArn: str
    Policy: str
    CurrentVersion: NotRequired[str]


class RebootBrokerRequestTypeDef(TypedDict):
    BrokerIds: Sequence[str]
    ClusterArn: str


class RecordConverterTypeDef(TypedDict):
    ValueConverter: ValueConverterType


class RecordSchemaTypeDef(TypedDict):
    GsrArn: str


class RejectClientVpcConnectionRequestTypeDef(TypedDict):
    ClusterArn: str
    VpcConnectionArn: str


class ReplicationInfoSummaryTypeDef(TypedDict):
    SourceKafkaClusterAlias: NotRequired[str]
    TargetKafkaClusterAlias: NotRequired[str]


ReplicationStartingPositionTypeDef = TypedDict(
    "ReplicationStartingPositionTypeDef",
    {
        "Type": NotRequired[ReplicationStartingPositionTypeType],
    },
)
ReplicationTopicNameConfigurationTypeDef = TypedDict(
    "ReplicationTopicNameConfigurationTypeDef",
    {
        "Type": NotRequired[ReplicationTopicNameConfigurationTypeType],
    },
)


class ReplicatorCloudWatchLogsTypeDef(TypedDict):
    Enabled: bool
    LogGroup: NotRequired[str]


class ReplicatorFirehoseTypeDef(TypedDict):
    Enabled: bool
    DeliveryStream: NotRequired[str]


class ReplicatorS3TypeDef(TypedDict):
    Enabled: bool
    Bucket: NotRequired[str]
    Prefix: NotRequired[str]


class S3StorageTypeDef(TypedDict):
    BucketArn: str
    CompressionType: S3CompressionTypeType
    StorageClass: S3StorageClassType
    OutputPrefix: NotRequired[str]
    OutputKeyTemplate: NotRequired[str]
    ExpectedBucketOwner: NotRequired[str]


class S3DestinationUpdateTypeDef(TypedDict):
    DataFreshnessInSeconds: int


class ScramTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class VpcConfigOutputTypeDef(TypedDict):
    SubnetIds: list[str]
    SecurityGroupIds: NotRequired[list[str]]


class TagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Mapping[str, str]


class TlsTypeDef(TypedDict):
    CertificateAuthorityArnList: NotRequired[Sequence[str]]
    Enabled: NotRequired[bool]


class TopicReplicationUpdateTypeDef(TypedDict):
    CopyAccessControlListsForTopics: bool
    CopyTopicConfigurations: bool
    DetectAndCopyNewTopics: bool
    TopicsToExclude: Sequence[str]
    TopicsToReplicate: Sequence[str]


class UntagResourceRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class UpdateBrokerCountRequestTypeDef(TypedDict):
    ClusterArn: str
    CurrentVersion: str
    TargetNumberOfBrokerNodes: int


class UpdateBrokerTypeRequestTypeDef(TypedDict):
    ClusterArn: str
    CurrentVersion: str
    TargetInstanceType: str


class UpdateTopicRequestTypeDef(TypedDict):
    ClusterArn: str
    TopicName: str
    Configs: NotRequired[str]
    PartitionCount: NotRequired[int]


UserIdentityTypeDef = TypedDict(
    "UserIdentityTypeDef",
    {
        "Type": NotRequired[UserIdentityTypeType],
        "PrincipalId": NotRequired[str],
    },
)


class VpcConfigTypeDef(TypedDict):
    SubnetIds: Sequence[str]
    SecurityGroupIds: NotRequired[Sequence[str]]


class VpcConnectivityTlsTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class VpcConnectivityIamTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class VpcConnectivityScramTypeDef(TypedDict):
    Enabled: NotRequired[bool]


class KafkaClusterSummaryTypeDef(TypedDict):
    AmazonMskCluster: NotRequired[AmazonMskClusterTypeDef]
    ApacheKafkaCluster: NotRequired[ApacheKafkaClusterTypeDef]
    KafkaClusterAlias: NotRequired[str]


class AuthorizerLogsTypeDef(TypedDict):
    CloudWatchLogs: NotRequired[CloudWatchLogsTypeDef]
    Firehose: NotRequired[FirehoseTypeDef]
    S3: NotRequired[S3TypeDef]


class BrokerLogsTypeDef(TypedDict):
    CloudWatchLogs: NotRequired[CloudWatchLogsTypeDef]
    Firehose: NotRequired[FirehoseTypeDef]
    S3: NotRequired[S3TypeDef]


class ChannelLoggingInfoTypeDef(TypedDict):
    CloudWatchLogs: NotRequired[CloudWatchLogsTypeDef]
    Firehose: NotRequired[FirehoseTypeDef]
    S3: NotRequired[S3TypeDef]


class CreateChannelResponseTypeDef(TypedDict):
    ChannelArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateClusterResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterName: str
    State: ClusterStateType
    ResponseMetadata: ResponseMetadataTypeDef


class CreateClusterV2ResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterName: str
    State: ClusterStateType
    ClusterType: ClusterTypeType
    ResponseMetadata: ResponseMetadataTypeDef


class CreateReplicatorResponseTypeDef(TypedDict):
    ReplicatorArn: str
    ReplicatorName: str
    ReplicatorState: ReplicatorStateType
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTopicResponseTypeDef(TypedDict):
    TopicArn: str
    TopicName: str
    Status: TopicStateType
    ResponseMetadata: ResponseMetadataTypeDef


class CreateVpcConnectionResponseTypeDef(TypedDict):
    VpcConnectionArn: str
    State: VpcConnectionStateType
    Authentication: str
    VpcId: str
    ClientSubnets: list[str]
    SecurityGroups: list[str]
    CreationTime: datetime
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteChannelResponseTypeDef(TypedDict):
    ChannelArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteClusterResponseTypeDef(TypedDict):
    ClusterArn: str
    State: ClusterStateType
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteConfigurationResponseTypeDef(TypedDict):
    Arn: str
    State: ConfigurationStateType
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteReplicatorResponseTypeDef(TypedDict):
    ReplicatorArn: str
    ReplicatorState: ReplicatorStateType
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteTopicResponseTypeDef(TypedDict):
    TopicArn: str
    TopicName: str
    Status: TopicStateType
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVpcConnectionResponseTypeDef(TypedDict):
    VpcConnectionArn: str
    State: VpcConnectionStateType
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeConfigurationRevisionResponseTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    Description: str
    Revision: int
    ServerProperties: bytes
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTopicResponseTypeDef(TypedDict):
    TopicArn: str
    TopicName: str
    ReplicationFactor: int
    PartitionCount: int
    Configs: str
    Status: TopicStateType
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeVpcConnectionResponseTypeDef(TypedDict):
    VpcConnectionArn: str
    TargetClusterArn: str
    State: VpcConnectionStateType
    Authentication: str
    VpcId: str
    Subnets: list[str]
    SecurityGroups: list[str]
    CreationTime: datetime
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class GetBootstrapBrokersResponseTypeDef(TypedDict):
    BootstrapBrokerString: str
    BootstrapBrokerStringTls: str
    BootstrapBrokerStringSaslScram: str
    BootstrapBrokerStringSaslIam: str
    BootstrapBrokerStringPublicTls: str
    BootstrapBrokerStringPublicSaslScram: str
    BootstrapBrokerStringPublicSaslIam: str
    BootstrapBrokerStringVpcConnectivityTls: str
    BootstrapBrokerStringVpcConnectivitySaslScram: str
    BootstrapBrokerStringVpcConnectivitySaslIam: str
    BootstrapBrokerStringIpv6: str
    BootstrapBrokerStringTlsIpv6: str
    BootstrapBrokerStringSaslScramIpv6: str
    BootstrapBrokerStringSaslIamIpv6: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetClusterPolicyResponseTypeDef(TypedDict):
    CurrentVersion: str
    Policy: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListScramSecretsResponseTypeDef(TypedDict):
    SecretArnList: list[str]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class PutClusterPolicyResponseTypeDef(TypedDict):
    CurrentVersion: str
    ResponseMetadata: ResponseMetadataTypeDef


class RebootBrokerResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBrokerCountResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBrokerStorageResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateBrokerTypeResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateChannelResponseTypeDef(TypedDict):
    ChannelArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateClusterConfigurationResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateClusterKafkaVersionResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateConnectivityResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateMonitoringResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateRebalancingResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateReplicationInfoResponseTypeDef(TypedDict):
    ReplicatorArn: str
    ReplicatorState: ReplicatorStateType
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSecurityResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateStorageResponseTypeDef(TypedDict):
    ClusterArn: str
    ClusterOperationArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTopicResponseTypeDef(TypedDict):
    TopicArn: str
    TopicName: str
    Status: TopicStateType
    ResponseMetadata: ResponseMetadataTypeDef


class BatchAssociateScramSecretResponseTypeDef(TypedDict):
    ClusterArn: str
    UnprocessedScramSecrets: list[UnprocessedScramSecretTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchDisassociateScramSecretResponseTypeDef(TypedDict):
    ClusterArn: str
    UnprocessedScramSecrets: list[UnprocessedScramSecretTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateConfigurationRequestTypeDef(TypedDict):
    Name: str
    ServerProperties: BlobTypeDef
    Description: NotRequired[str]
    KafkaVersions: NotRequired[Sequence[str]]


class UpdateConfigurationRequestTypeDef(TypedDict):
    Arn: str
    ServerProperties: BlobTypeDef
    Description: NotRequired[str]


class BrokerEBSVolumeInfoTypeDef(TypedDict):
    KafkaBrokerNodeId: str
    ProvisionedThroughput: NotRequired[ProvisionedThroughputTypeDef]
    VolumeSizeGB: NotRequired[int]


class EBSStorageInfoTypeDef(TypedDict):
    ProvisionedThroughput: NotRequired[ProvisionedThroughputTypeDef]
    VolumeSize: NotRequired[int]


class UpdateStorageRequestTypeDef(TypedDict):
    ClusterArn: str
    CurrentVersion: str
    ProvisionedThroughput: NotRequired[ProvisionedThroughputTypeDef]
    StorageMode: NotRequired[StorageModeType]
    VolumeSizeGB: NotRequired[int]


class BrokerNodeInfoTypeDef(TypedDict):
    AttachedENIId: NotRequired[str]
    BrokerId: NotRequired[float]
    ClientSubnet: NotRequired[str]
    ClientVpcIpAddress: NotRequired[str]
    CurrentBrokerSoftwareInfo: NotRequired[BrokerSoftwareInfoTypeDef]
    Endpoints: NotRequired[list[str]]


class ListChannelsResponseTypeDef(TypedDict):
    Channels: list[ChannelInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListClientVpcConnectionsResponseTypeDef(TypedDict):
    ClientVpcConnections: list[ClientVpcConnectionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateRebalancingRequestTypeDef(TypedDict):
    ClusterArn: str
    CurrentVersion: str
    Rebalancing: RebalancingTypeDef


class ClusterOperationStepTypeDef(TypedDict):
    StepInfo: NotRequired[ClusterOperationStepInfoTypeDef]
    StepName: NotRequired[str]


class ListClusterOperationsV2ResponseTypeDef(TypedDict):
    ClusterOperationInfoList: list[ClusterOperationV2SummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GetCompatibleKafkaVersionsResponseTypeDef(TypedDict):
    CompatibleKafkaVersions: list[CompatibleKafkaVersionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateClusterConfigurationRequestTypeDef(TypedDict):
    ClusterArn: str
    ConfigurationInfo: ConfigurationInfoTypeDef
    CurrentVersion: str


class UpdateClusterKafkaVersionRequestTypeDef(TypedDict):
    ClusterArn: str
    CurrentVersion: str
    TargetKafkaVersion: str
    ConfigurationInfo: NotRequired[ConfigurationInfoTypeDef]


class ConfigurationTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    Description: str
    KafkaVersions: list[str]
    LatestRevision: ConfigurationRevisionTypeDef
    Name: str
    State: ConfigurationStateType


class CreateConfigurationResponseTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    LatestRevision: ConfigurationRevisionTypeDef
    Name: str
    State: ConfigurationStateType
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeConfigurationResponseTypeDef(TypedDict):
    Arn: str
    CreationTime: datetime
    Description: str
    KafkaVersions: list[str]
    LatestRevision: ConfigurationRevisionTypeDef
    Name: str
    State: ConfigurationStateType
    ResponseMetadata: ResponseMetadataTypeDef


class ListConfigurationRevisionsResponseTypeDef(TypedDict):
    Revisions: list[ConfigurationRevisionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class UpdateConfigurationResponseTypeDef(TypedDict):
    Arn: str
    LatestRevision: ConfigurationRevisionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


ConsumerGroupReplicationUnionTypeDef = Union[
    ConsumerGroupReplicationTypeDef, ConsumerGroupReplicationOutputTypeDef
]


class DescribeTopicPartitionsRequestPaginateTypeDef(TypedDict):
    ClusterArn: str
    TopicName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListClientVpcConnectionsRequestPaginateTypeDef(TypedDict):
    ClusterArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListClusterOperationsRequestPaginateTypeDef(TypedDict):
    ClusterArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListClusterOperationsV2RequestPaginateTypeDef(TypedDict):
    ClusterArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListClustersRequestPaginateTypeDef(TypedDict):
    ClusterNameFilter: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListClustersV2RequestPaginateTypeDef(TypedDict):
    ClusterNameFilter: NotRequired[str]
    ClusterTypeFilter: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListConfigurationRevisionsRequestPaginateTypeDef(TypedDict):
    Arn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListConfigurationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListKafkaVersionsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListNodesRequestPaginateTypeDef(TypedDict):
    ClusterArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListReplicatorsRequestPaginateTypeDef(TypedDict):
    ReplicatorNameFilter: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListScramSecretsRequestPaginateTypeDef(TypedDict):
    ClusterArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTopicsRequestPaginateTypeDef(TypedDict):
    ClusterArn: str
    TopicNameFilter: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListVpcConnectionsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTopicPartitionsResponseTypeDef(TypedDict):
    Partitions: list[TopicPartitionInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class EncryptionInfoTypeDef(TypedDict):
    EncryptionAtRest: NotRequired[EncryptionAtRestTypeDef]
    EncryptionInTransit: NotRequired[EncryptionInTransitTypeDef]


class ServerlessSaslTypeDef(TypedDict):
    Iam: NotRequired[IamTypeDef]


KafkaClusterClientVpcConfigUnionTypeDef = Union[
    KafkaClusterClientVpcConfigTypeDef, KafkaClusterClientVpcConfigOutputTypeDef
]


class KafkaClusterSaslOAuthBearerAuthenticationTypeDef(TypedDict):
    TokenEndpointUrl: str
    TokenEndpointAuthenticationMethod: TokenEndpointAuthenticationMethodType
    ClientCredentials: NotRequired[KafkaClusterOAuthClientCredentialsTypeDef]
    IamJwtBearer: NotRequired[KafkaClusterOAuthIamJwtBearerTypeDef]
    ClientCredentialsAssertion: NotRequired[KafkaClusterOAuthClientCredentialsAssertionTypeDef]
    Scope: NotRequired[str]
    TokenEndpointTlsCertificateArn: NotRequired[str]


class ListKafkaVersionsResponseTypeDef(TypedDict):
    KafkaVersions: list[KafkaVersionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTopicsResponseTypeDef(TypedDict):
    Topics: list[TopicInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListVpcConnectionsResponseTypeDef(TypedDict):
    VpcConnections: list[VpcConnectionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class PrometheusInfoTypeDef(TypedDict):
    JmxExporter: NotRequired[JmxExporterInfoTypeDef]
    NodeExporter: NotRequired[NodeExporterInfoTypeDef]


class PrometheusTypeDef(TypedDict):
    JmxExporter: NotRequired[JmxExporterTypeDef]
    NodeExporter: NotRequired[NodeExporterTypeDef]


class PartitionSpecOutputTypeDef(TypedDict):
    PartitionStrategy: Literal["TIME_HOUR"]
    SourceList: NotRequired[list[PartitionSourceTypeDef]]


class PartitionSpecTypeDef(TypedDict):
    PartitionStrategy: Literal["TIME_HOUR"]
    SourceList: NotRequired[Sequence[PartitionSourceTypeDef]]


class TopicConfigurationTypeDef(TypedDict):
    RecordConverter: RecordConverterTypeDef
    TopicArn: str
    RecordSchema: NotRequired[RecordSchemaTypeDef]


class TopicReplicationOutputTypeDef(TypedDict):
    TopicsToReplicate: list[str]
    CopyAccessControlListsForTopics: NotRequired[bool]
    CopyTopicConfigurations: NotRequired[bool]
    DetectAndCopyNewTopics: NotRequired[bool]
    StartingPosition: NotRequired[ReplicationStartingPositionTypeDef]
    TopicNameConfiguration: NotRequired[ReplicationTopicNameConfigurationTypeDef]
    TopicsToExclude: NotRequired[list[str]]


class TopicReplicationTypeDef(TypedDict):
    TopicsToReplicate: Sequence[str]
    CopyAccessControlListsForTopics: NotRequired[bool]
    CopyTopicConfigurations: NotRequired[bool]
    DetectAndCopyNewTopics: NotRequired[bool]
    StartingPosition: NotRequired[ReplicationStartingPositionTypeDef]
    TopicNameConfiguration: NotRequired[ReplicationTopicNameConfigurationTypeDef]
    TopicsToExclude: NotRequired[Sequence[str]]


class ReplicatorLogDeliveryTypeDef(TypedDict):
    CloudWatchLogs: NotRequired[ReplicatorCloudWatchLogsTypeDef]
    Firehose: NotRequired[ReplicatorFirehoseTypeDef]
    S3: NotRequired[ReplicatorS3TypeDef]


class S3DestinationConfigurationTypeDef(TypedDict):
    DeadLetterQueueS3: DeadLetterQueueS3TypeDef
    ServiceExecutionRoleArn: str
    Storage: S3StorageTypeDef
    DataFreshnessInSeconds: NotRequired[int]


class UpdateChannelRequestTypeDef(TypedDict):
    ChannelArn: str
    ClusterArn: str
    IcebergDestinationUpdate: NotRequired[IcebergDestinationUpdateTypeDef]
    S3DestinationUpdate: NotRequired[S3DestinationUpdateTypeDef]


class SaslTypeDef(TypedDict):
    Scram: NotRequired[ScramTypeDef]
    Iam: NotRequired[IamTypeDef]


TlsUnionTypeDef = Union[TlsTypeDef, TlsOutputTypeDef]


class VpcConnectionInfoServerlessTypeDef(TypedDict):
    CreationTime: NotRequired[datetime]
    Owner: NotRequired[str]
    UserIdentity: NotRequired[UserIdentityTypeDef]
    VpcConnectionArn: NotRequired[str]


class VpcConnectionInfoTypeDef(TypedDict):
    VpcConnectionArn: NotRequired[str]
    Owner: NotRequired[str]
    UserIdentity: NotRequired[UserIdentityTypeDef]
    CreationTime: NotRequired[datetime]


VpcConfigUnionTypeDef = Union[VpcConfigTypeDef, VpcConfigOutputTypeDef]


class VpcConnectivitySaslTypeDef(TypedDict):
    Scram: NotRequired[VpcConnectivityScramTypeDef]
    Iam: NotRequired[VpcConnectivityIamTypeDef]


class ReplicatorSummaryTypeDef(TypedDict):
    CreationTime: NotRequired[datetime]
    CurrentVersion: NotRequired[str]
    IsReplicatorReference: NotRequired[bool]
    KafkaClustersSummary: NotRequired[list[KafkaClusterSummaryTypeDef]]
    ReplicationInfoSummaryList: NotRequired[list[ReplicationInfoSummaryTypeDef]]
    ReplicatorArn: NotRequired[str]
    ReplicatorName: NotRequired[str]
    ReplicatorResourceArn: NotRequired[str]
    ReplicatorState: NotRequired[ReplicatorStateType]


class LoggingInfoTypeDef(TypedDict):
    BrokerLogs: BrokerLogsTypeDef
    AuthorizerLogs: NotRequired[AuthorizerLogsTypeDef]


class UpdateBrokerStorageRequestTypeDef(TypedDict):
    ClusterArn: str
    CurrentVersion: str
    TargetBrokerEBSVolumeInfo: Sequence[BrokerEBSVolumeInfoTypeDef]


class StorageInfoTypeDef(TypedDict):
    EbsStorageInfo: NotRequired[EBSStorageInfoTypeDef]


class NodeInfoTypeDef(TypedDict):
    AddedToClusterTime: NotRequired[str]
    BrokerNodeInfo: NotRequired[BrokerNodeInfoTypeDef]
    ControllerNodeInfo: NotRequired[ControllerNodeInfoTypeDef]
    InstanceType: NotRequired[str]
    NodeARN: NotRequired[str]
    NodeType: NotRequired[Literal["BROKER"]]
    ZookeeperNodeInfo: NotRequired[ZookeeperNodeInfoTypeDef]


class ListConfigurationsResponseTypeDef(TypedDict):
    Configurations: list[ConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ServerlessClientAuthenticationTypeDef(TypedDict):
    Sasl: NotRequired[ServerlessSaslTypeDef]


class KafkaClusterClientAuthenticationTypeDef(TypedDict):
    SaslScram: NotRequired[KafkaClusterSaslScramAuthenticationTypeDef]
    MTLS: NotRequired[KafkaClusterMTLSAuthenticationTypeDef]
    SaslOAuthBearer: NotRequired[KafkaClusterSaslOAuthBearerAuthenticationTypeDef]


class OpenMonitoringInfoTypeDef(TypedDict):
    Prometheus: PrometheusInfoTypeDef


class OpenMonitoringTypeDef(TypedDict):
    Prometheus: PrometheusTypeDef


class DestinationTableOutputTypeDef(TypedDict):
    DestinationDatabaseName: NotRequired[str]
    DestinationTableName: NotRequired[str]
    PartitionSpec: NotRequired[PartitionSpecOutputTypeDef]


class DestinationTableTypeDef(TypedDict):
    DestinationDatabaseName: NotRequired[str]
    DestinationTableName: NotRequired[str]
    PartitionSpec: NotRequired[PartitionSpecTypeDef]


class ReplicationInfoDescriptionTypeDef(TypedDict):
    ConsumerGroupReplication: NotRequired[ConsumerGroupReplicationOutputTypeDef]
    SourceKafkaClusterAlias: NotRequired[str]
    TargetCompressionType: NotRequired[TargetCompressionTypeType]
    TargetKafkaClusterAlias: NotRequired[str]
    TopicReplication: NotRequired[TopicReplicationOutputTypeDef]


TopicReplicationUnionTypeDef = Union[TopicReplicationTypeDef, TopicReplicationOutputTypeDef]


class LogDeliveryTypeDef(TypedDict):
    ReplicatorLogDelivery: NotRequired[ReplicatorLogDeliveryTypeDef]


class ClientAuthenticationOutputTypeDef(TypedDict):
    Sasl: NotRequired[SaslTypeDef]
    Tls: NotRequired[TlsOutputTypeDef]
    Unauthenticated: NotRequired[UnauthenticatedTypeDef]


class ClientAuthenticationTypeDef(TypedDict):
    Sasl: NotRequired[SaslTypeDef]
    Tls: NotRequired[TlsUnionTypeDef]
    Unauthenticated: NotRequired[UnauthenticatedTypeDef]


class ClusterOperationV2ServerlessTypeDef(TypedDict):
    SourceClusterInfo: NotRequired[ServerlessConnectivityInfoTypeDef]
    TargetClusterInfo: NotRequired[ServerlessConnectivityInfoTypeDef]
    VpcConnectionInfo: NotRequired[VpcConnectionInfoServerlessTypeDef]


class VpcConnectivityClientAuthenticationTypeDef(TypedDict):
    Sasl: NotRequired[VpcConnectivitySaslTypeDef]
    Tls: NotRequired[VpcConnectivityTlsTypeDef]


class ListReplicatorsResponseTypeDef(TypedDict):
    Replicators: list[ReplicatorSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListNodesResponseTypeDef(TypedDict):
    NodeInfoList: list[NodeInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ServerlessRequestTypeDef(TypedDict):
    VpcConfigs: Sequence[VpcConfigUnionTypeDef]
    ClientAuthentication: NotRequired[ServerlessClientAuthenticationTypeDef]


class ServerlessTypeDef(TypedDict):
    VpcConfigs: list[VpcConfigOutputTypeDef]
    ClientAuthentication: NotRequired[ServerlessClientAuthenticationTypeDef]
    ConnectivityInfo: NotRequired[ServerlessConnectivityInfoTypeDef]


class KafkaClusterDescriptionTypeDef(TypedDict):
    AmazonMskCluster: NotRequired[AmazonMskClusterTypeDef]
    ApacheKafkaCluster: NotRequired[ApacheKafkaClusterTypeDef]
    KafkaClusterAlias: NotRequired[str]
    VpcConfig: NotRequired[KafkaClusterClientVpcConfigOutputTypeDef]
    ClientAuthentication: NotRequired[KafkaClusterClientAuthenticationTypeDef]
    EncryptionInTransit: NotRequired[KafkaClusterEncryptionInTransitTypeDef]


class KafkaClusterTypeDef(TypedDict):
    AmazonMskCluster: NotRequired[AmazonMskClusterTypeDef]
    ApacheKafkaCluster: NotRequired[ApacheKafkaClusterTypeDef]
    VpcConfig: NotRequired[KafkaClusterClientVpcConfigUnionTypeDef]
    ClientAuthentication: NotRequired[KafkaClusterClientAuthenticationTypeDef]
    EncryptionInTransit: NotRequired[KafkaClusterEncryptionInTransitTypeDef]


class UpdateMonitoringRequestTypeDef(TypedDict):
    ClusterArn: str
    CurrentVersion: str
    EnhancedMonitoring: NotRequired[EnhancedMonitoringType]
    OpenMonitoring: NotRequired[OpenMonitoringInfoTypeDef]
    LoggingInfo: NotRequired[LoggingInfoTypeDef]


class IcebergDestinationConfigurationOutputTypeDef(TypedDict):
    AppendOnly: bool
    DeadLetterQueueS3: DeadLetterQueueS3TypeDef
    DestinationTableList: list[DestinationTableOutputTypeDef]
    SchemaEvolution: SchemaEvolutionTypeDef
    ServiceExecutionRoleArn: str
    TableCreation: TableCreationTypeDef
    Catalog: NotRequired[CatalogTypeDef]
    DataFreshnessInSeconds: NotRequired[int]
    CompressionType: NotRequired[IcebergCompressionTypeType]


class IcebergDestinationConfigurationTypeDef(TypedDict):
    AppendOnly: bool
    DeadLetterQueueS3: DeadLetterQueueS3TypeDef
    DestinationTableList: Sequence[DestinationTableTypeDef]
    SchemaEvolution: SchemaEvolutionTypeDef
    ServiceExecutionRoleArn: str
    TableCreation: TableCreationTypeDef
    Catalog: NotRequired[CatalogTypeDef]
    DataFreshnessInSeconds: NotRequired[int]
    CompressionType: NotRequired[IcebergCompressionTypeType]


class ReplicationInfoTypeDef(TypedDict):
    ConsumerGroupReplication: ConsumerGroupReplicationUnionTypeDef
    TargetCompressionType: TargetCompressionTypeType
    TopicReplication: TopicReplicationUnionTypeDef
    SourceKafkaClusterArn: NotRequired[str]
    SourceKafkaClusterId: NotRequired[str]
    TargetKafkaClusterArn: NotRequired[str]
    TargetKafkaClusterId: NotRequired[str]


class UpdateReplicationInfoRequestTypeDef(TypedDict):
    CurrentVersion: str
    ReplicatorArn: str
    ConsumerGroupReplication: NotRequired[ConsumerGroupReplicationUpdateTypeDef]
    SourceKafkaClusterArn: NotRequired[str]
    SourceKafkaClusterId: NotRequired[str]
    TargetKafkaClusterArn: NotRequired[str]
    TargetKafkaClusterId: NotRequired[str]
    TopicReplication: NotRequired[TopicReplicationUpdateTypeDef]
    LogDelivery: NotRequired[LogDeliveryTypeDef]


ClientAuthenticationUnionTypeDef = Union[
    ClientAuthenticationTypeDef, ClientAuthenticationOutputTypeDef
]


class VpcConnectivityTypeDef(TypedDict):
    ClientAuthentication: NotRequired[VpcConnectivityClientAuthenticationTypeDef]


class DescribeReplicatorResponseTypeDef(TypedDict):
    CreationTime: datetime
    CurrentVersion: str
    IsReplicatorReference: bool
    KafkaClusters: list[KafkaClusterDescriptionTypeDef]
    ReplicationInfoList: list[ReplicationInfoDescriptionTypeDef]
    ReplicatorArn: str
    ReplicatorDescription: str
    ReplicatorName: str
    ReplicatorResourceArn: str
    ReplicatorState: ReplicatorStateType
    ServiceExecutionRoleArn: str
    StateInfo: ReplicationStateInfoTypeDef
    Tags: dict[str, str]
    LogDelivery: LogDeliveryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeChannelResponseTypeDef(TypedDict):
    ChannelArn: str
    ChannelName: str
    EncryptionConfiguration: EncryptionConfigurationTypeDef
    IcebergDestinationConfiguration: IcebergDestinationConfigurationOutputTypeDef
    S3DestinationConfiguration: S3DestinationConfigurationTypeDef
    Status: ChannelStatusType
    DestinationType: ChannelDestinationTypeType
    CreationTime: datetime
    TopicConfigurationList: list[TopicConfigurationTypeDef]
    LoggingInfo: ChannelLoggingInfoTypeDef
    StateInfo: ChannelStateInfoTypeDef
    ClusterOperationArn: str
    Tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


IcebergDestinationConfigurationUnionTypeDef = Union[
    IcebergDestinationConfigurationTypeDef, IcebergDestinationConfigurationOutputTypeDef
]


class CreateReplicatorRequestTypeDef(TypedDict):
    KafkaClusters: Sequence[KafkaClusterTypeDef]
    ReplicationInfoList: Sequence[ReplicationInfoTypeDef]
    ReplicatorName: str
    ServiceExecutionRoleArn: str
    Description: NotRequired[str]
    Tags: NotRequired[Mapping[str, str]]
    LogDelivery: NotRequired[LogDeliveryTypeDef]


class UpdateSecurityRequestTypeDef(TypedDict):
    ClusterArn: str
    CurrentVersion: str
    ClientAuthentication: NotRequired[ClientAuthenticationUnionTypeDef]
    EncryptionInfo: NotRequired[EncryptionInfoTypeDef]


class ConnectivityInfoTypeDef(TypedDict):
    PublicAccess: NotRequired[PublicAccessTypeDef]
    VpcConnectivity: NotRequired[VpcConnectivityTypeDef]
    NetworkType: NotRequired[NetworkTypeType]


class CreateChannelRequestTypeDef(TypedDict):
    ChannelName: str
    ClusterArn: str
    TopicConfigurationList: Sequence[TopicConfigurationTypeDef]
    EncryptionConfiguration: NotRequired[EncryptionConfigurationTypeDef]
    IcebergDestinationConfiguration: NotRequired[IcebergDestinationConfigurationUnionTypeDef]
    S3DestinationConfiguration: NotRequired[S3DestinationConfigurationTypeDef]
    Tags: NotRequired[Mapping[str, str]]
    LoggingInfo: NotRequired[ChannelLoggingInfoTypeDef]


class BrokerNodeGroupInfoOutputTypeDef(TypedDict):
    ClientSubnets: list[str]
    InstanceType: str
    BrokerAZDistribution: NotRequired[Literal["DEFAULT"]]
    SecurityGroups: NotRequired[list[str]]
    StorageInfo: NotRequired[StorageInfoTypeDef]
    ConnectivityInfo: NotRequired[ConnectivityInfoTypeDef]
    ZoneIds: NotRequired[list[str]]


class BrokerNodeGroupInfoTypeDef(TypedDict):
    ClientSubnets: Sequence[str]
    InstanceType: str
    BrokerAZDistribution: NotRequired[Literal["DEFAULT"]]
    SecurityGroups: NotRequired[Sequence[str]]
    StorageInfo: NotRequired[StorageInfoTypeDef]
    ConnectivityInfo: NotRequired[ConnectivityInfoTypeDef]
    ZoneIds: NotRequired[Sequence[str]]


class MutableClusterInfoTypeDef(TypedDict):
    BrokerEBSVolumeInfo: NotRequired[list[BrokerEBSVolumeInfoTypeDef]]
    ConfigurationInfo: NotRequired[ConfigurationInfoTypeDef]
    NumberOfBrokerNodes: NotRequired[int]
    EnhancedMonitoring: NotRequired[EnhancedMonitoringType]
    OpenMonitoring: NotRequired[OpenMonitoringTypeDef]
    ZookeeperAccess: NotRequired[ZookeeperAccessTypeDef]
    KafkaVersion: NotRequired[str]
    LoggingInfo: NotRequired[LoggingInfoTypeDef]
    InstanceType: NotRequired[str]
    ClientAuthentication: NotRequired[ClientAuthenticationOutputTypeDef]
    EncryptionInfo: NotRequired[EncryptionInfoTypeDef]
    ConnectivityInfo: NotRequired[ConnectivityInfoTypeDef]
    StorageMode: NotRequired[StorageModeType]
    BrokerCountUpdateInfo: NotRequired[BrokerCountUpdateInfoTypeDef]
    Rebalancing: NotRequired[RebalancingTypeDef]


class UpdateConnectivityRequestTypeDef(TypedDict):
    ClusterArn: str
    CurrentVersion: str
    ConnectivityInfo: NotRequired[ConnectivityInfoTypeDef]
    ZookeeperAccess: NotRequired[ZookeeperAccessTypeDef]


class ClusterInfoTypeDef(TypedDict):
    ActiveOperationArn: NotRequired[str]
    BrokerNodeGroupInfo: NotRequired[BrokerNodeGroupInfoOutputTypeDef]
    Rebalancing: NotRequired[RebalancingTypeDef]
    ClientAuthentication: NotRequired[ClientAuthenticationOutputTypeDef]
    ClusterArn: NotRequired[str]
    ClusterName: NotRequired[str]
    CreationTime: NotRequired[datetime]
    CurrentBrokerSoftwareInfo: NotRequired[BrokerSoftwareInfoTypeDef]
    CurrentVersion: NotRequired[str]
    EncryptionInfo: NotRequired[EncryptionInfoTypeDef]
    EnhancedMonitoring: NotRequired[EnhancedMonitoringType]
    OpenMonitoring: NotRequired[OpenMonitoringTypeDef]
    LoggingInfo: NotRequired[LoggingInfoTypeDef]
    NumberOfBrokerNodes: NotRequired[int]
    State: NotRequired[ClusterStateType]
    StateInfo: NotRequired[StateInfoTypeDef]
    Tags: NotRequired[dict[str, str]]
    ZookeeperConnectString: NotRequired[str]
    ZookeeperConnectStringTls: NotRequired[str]
    StorageMode: NotRequired[StorageModeType]
    CustomerActionStatus: NotRequired[CustomerActionStatusType]


class ProvisionedTypeDef(TypedDict):
    BrokerNodeGroupInfo: BrokerNodeGroupInfoOutputTypeDef
    NumberOfBrokerNodes: int
    Rebalancing: NotRequired[RebalancingTypeDef]
    CurrentBrokerSoftwareInfo: NotRequired[BrokerSoftwareInfoTypeDef]
    ClientAuthentication: NotRequired[ClientAuthenticationOutputTypeDef]
    EncryptionInfo: NotRequired[EncryptionInfoTypeDef]
    EnhancedMonitoring: NotRequired[EnhancedMonitoringType]
    OpenMonitoring: NotRequired[OpenMonitoringInfoTypeDef]
    LoggingInfo: NotRequired[LoggingInfoTypeDef]
    ZookeeperConnectString: NotRequired[str]
    ZookeeperConnectStringTls: NotRequired[str]
    StorageMode: NotRequired[StorageModeType]
    CustomerActionStatus: NotRequired[CustomerActionStatusType]


BrokerNodeGroupInfoUnionTypeDef = Union[
    BrokerNodeGroupInfoTypeDef, BrokerNodeGroupInfoOutputTypeDef
]


class ClusterOperationInfoTypeDef(TypedDict):
    ClientRequestId: NotRequired[str]
    ClusterArn: NotRequired[str]
    CreationTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    ErrorInfo: NotRequired[ErrorInfoTypeDef]
    OperationArn: NotRequired[str]
    OperationState: NotRequired[str]
    OperationSteps: NotRequired[list[ClusterOperationStepTypeDef]]
    OperationType: NotRequired[str]
    SourceClusterInfo: NotRequired[MutableClusterInfoTypeDef]
    TargetClusterInfo: NotRequired[MutableClusterInfoTypeDef]
    VpcConnectionInfo: NotRequired[VpcConnectionInfoTypeDef]


class ClusterOperationV2ProvisionedTypeDef(TypedDict):
    OperationSteps: NotRequired[list[ClusterOperationStepTypeDef]]
    SourceClusterInfo: NotRequired[MutableClusterInfoTypeDef]
    TargetClusterInfo: NotRequired[MutableClusterInfoTypeDef]
    VpcConnectionInfo: NotRequired[VpcConnectionInfoTypeDef]


class DescribeClusterResponseTypeDef(TypedDict):
    ClusterInfo: ClusterInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListClustersResponseTypeDef(TypedDict):
    ClusterInfoList: list[ClusterInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ClusterTypeDef(TypedDict):
    ActiveOperationArn: NotRequired[str]
    ClusterType: NotRequired[ClusterTypeType]
    ClusterArn: NotRequired[str]
    ClusterName: NotRequired[str]
    CreationTime: NotRequired[datetime]
    CurrentVersion: NotRequired[str]
    State: NotRequired[ClusterStateType]
    StateInfo: NotRequired[StateInfoTypeDef]
    Tags: NotRequired[dict[str, str]]
    Provisioned: NotRequired[ProvisionedTypeDef]
    Serverless: NotRequired[ServerlessTypeDef]


class CreateClusterRequestTypeDef(TypedDict):
    BrokerNodeGroupInfo: BrokerNodeGroupInfoUnionTypeDef
    ClusterName: str
    KafkaVersion: str
    NumberOfBrokerNodes: int
    Rebalancing: NotRequired[RebalancingTypeDef]
    ClientAuthentication: NotRequired[ClientAuthenticationUnionTypeDef]
    ConfigurationInfo: NotRequired[ConfigurationInfoTypeDef]
    EncryptionInfo: NotRequired[EncryptionInfoTypeDef]
    EnhancedMonitoring: NotRequired[EnhancedMonitoringType]
    OpenMonitoring: NotRequired[OpenMonitoringInfoTypeDef]
    LoggingInfo: NotRequired[LoggingInfoTypeDef]
    Tags: NotRequired[Mapping[str, str]]
    StorageMode: NotRequired[StorageModeType]


class ProvisionedRequestTypeDef(TypedDict):
    BrokerNodeGroupInfo: BrokerNodeGroupInfoUnionTypeDef
    KafkaVersion: str
    NumberOfBrokerNodes: int
    Rebalancing: NotRequired[RebalancingTypeDef]
    ClientAuthentication: NotRequired[ClientAuthenticationUnionTypeDef]
    ConfigurationInfo: NotRequired[ConfigurationInfoTypeDef]
    EncryptionInfo: NotRequired[EncryptionInfoTypeDef]
    EnhancedMonitoring: NotRequired[EnhancedMonitoringType]
    OpenMonitoring: NotRequired[OpenMonitoringInfoTypeDef]
    LoggingInfo: NotRequired[LoggingInfoTypeDef]
    StorageMode: NotRequired[StorageModeType]


class DescribeClusterOperationResponseTypeDef(TypedDict):
    ClusterOperationInfo: ClusterOperationInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListClusterOperationsResponseTypeDef(TypedDict):
    ClusterOperationInfoList: list[ClusterOperationInfoTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ClusterOperationV2TypeDef(TypedDict):
    ClusterArn: NotRequired[str]
    ClusterType: NotRequired[ClusterTypeType]
    StartTime: NotRequired[datetime]
    EndTime: NotRequired[datetime]
    ErrorInfo: NotRequired[ErrorInfoTypeDef]
    OperationArn: NotRequired[str]
    OperationState: NotRequired[str]
    OperationType: NotRequired[str]
    Provisioned: NotRequired[ClusterOperationV2ProvisionedTypeDef]
    Serverless: NotRequired[ClusterOperationV2ServerlessTypeDef]


class DescribeClusterV2ResponseTypeDef(TypedDict):
    ClusterInfo: ClusterTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListClustersV2ResponseTypeDef(TypedDict):
    ClusterInfoList: list[ClusterTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateClusterV2RequestTypeDef(TypedDict):
    ClusterName: str
    Tags: NotRequired[Mapping[str, str]]
    Provisioned: NotRequired[ProvisionedRequestTypeDef]
    Serverless: NotRequired[ServerlessRequestTypeDef]


class DescribeClusterOperationV2ResponseTypeDef(TypedDict):
    ClusterOperationInfo: ClusterOperationV2TypeDef
    ResponseMetadata: ResponseMetadataTypeDef
