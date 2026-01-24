"""
Type annotations for lightsail service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lightsail/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_lightsail.type_defs import AccessKeyLastUsedTypeDef

    data: AccessKeyLastUsedTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    AccessDirectionType,
    AccessTypeType,
    AccountLevelBpaSyncStatusType,
    AddOnTypeType,
    AlarmStateType,
    AutoMountStatusType,
    AutoSnapshotStatusType,
    BehaviorEnumType,
    BlueprintTypeType,
    BPAStatusMessageType,
    BucketMetricNameType,
    CertificateDomainValidationStatusType,
    CertificateStatusType,
    ComparisonOperatorType,
    ContactMethodStatusType,
    ContactProtocolType,
    ContainerServiceDeploymentStateType,
    ContainerServiceMetricNameType,
    ContainerServicePowerNameType,
    ContainerServiceProtocolType,
    ContainerServiceStateDetailCodeType,
    ContainerServiceStateType,
    DiskSnapshotStateType,
    DiskStateType,
    DistributionMetricNameType,
    DnsRecordCreationStateCodeType,
    ExportSnapshotRecordSourceTypeType,
    ForwardValuesType,
    HeaderEnumType,
    HttpEndpointType,
    HttpProtocolIpv6Type,
    HttpTokensType,
    InstanceAccessProtocolType,
    InstanceHealthReasonType,
    InstanceHealthStateType,
    InstanceMetadataStateType,
    InstanceMetricNameType,
    InstancePlatformType,
    InstanceSnapshotStateType,
    IpAddressTypeType,
    LoadBalancerAttributeNameType,
    LoadBalancerMetricNameType,
    LoadBalancerProtocolType,
    LoadBalancerStateType,
    LoadBalancerTlsCertificateDnsRecordCreationStateCodeType,
    LoadBalancerTlsCertificateDomainStatusType,
    LoadBalancerTlsCertificateFailureReasonType,
    LoadBalancerTlsCertificateRenewalStatusType,
    LoadBalancerTlsCertificateRevocationReasonType,
    LoadBalancerTlsCertificateStatusType,
    MetricNameType,
    MetricStatisticType,
    MetricUnitType,
    NameServersUpdateStateCodeType,
    NetworkProtocolType,
    OperationStatusType,
    OperationTypeType,
    OriginProtocolPolicyEnumType,
    PortAccessTypeType,
    PortInfoSourceTypeType,
    PortStateType,
    PricingUnitType,
    R53HostedZoneDeletionStateCodeType,
    RecordStateType,
    RegionNameType,
    RelationalDatabaseMetricNameType,
    RelationalDatabasePasswordVersionType,
    RenewalStatusType,
    ResourceBucketAccessType,
    ResourceTypeType,
    SetupStatusType,
    StatusType,
    StatusTypeType,
    TreatMissingDataType,
    ViewerMinimumTlsProtocolVersionEnumType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AccessKeyLastUsedTypeDef",
    "AccessKeyTypeDef",
    "AccessRulesTypeDef",
    "AccountLevelBpaSyncTypeDef",
    "AddOnRequestTypeDef",
    "AddOnTypeDef",
    "AlarmTypeDef",
    "AllocateStaticIpRequestTypeDef",
    "AllocateStaticIpResultTypeDef",
    "AttachCertificateToDistributionRequestTypeDef",
    "AttachCertificateToDistributionResultTypeDef",
    "AttachDiskRequestTypeDef",
    "AttachDiskResultTypeDef",
    "AttachInstancesToLoadBalancerRequestTypeDef",
    "AttachInstancesToLoadBalancerResultTypeDef",
    "AttachLoadBalancerTlsCertificateRequestTypeDef",
    "AttachLoadBalancerTlsCertificateResultTypeDef",
    "AttachStaticIpRequestTypeDef",
    "AttachStaticIpResultTypeDef",
    "AttachedDiskTypeDef",
    "AutoSnapshotAddOnRequestTypeDef",
    "AutoSnapshotDetailsTypeDef",
    "AvailabilityZoneTypeDef",
    "BlueprintTypeDef",
    "BucketAccessLogConfigTypeDef",
    "BucketBundleTypeDef",
    "BucketCorsConfigOutputTypeDef",
    "BucketCorsConfigTypeDef",
    "BucketCorsConfigUnionTypeDef",
    "BucketCorsRuleOutputTypeDef",
    "BucketCorsRuleTypeDef",
    "BucketStateTypeDef",
    "BucketTypeDef",
    "BundleTypeDef",
    "CacheBehaviorPerPathTypeDef",
    "CacheBehaviorTypeDef",
    "CacheSettingsOutputTypeDef",
    "CacheSettingsTypeDef",
    "CacheSettingsUnionTypeDef",
    "CertificateSummaryTypeDef",
    "CertificateTypeDef",
    "CloseInstancePublicPortsRequestTypeDef",
    "CloseInstancePublicPortsResultTypeDef",
    "CloudFormationStackRecordSourceInfoTypeDef",
    "CloudFormationStackRecordTypeDef",
    "ContactMethodTypeDef",
    "ContainerImageTypeDef",
    "ContainerOutputTypeDef",
    "ContainerServiceDeploymentRequestTypeDef",
    "ContainerServiceDeploymentTypeDef",
    "ContainerServiceECRImagePullerRoleRequestTypeDef",
    "ContainerServiceECRImagePullerRoleTypeDef",
    "ContainerServiceEndpointTypeDef",
    "ContainerServiceHealthCheckConfigTypeDef",
    "ContainerServiceLogEventTypeDef",
    "ContainerServicePowerTypeDef",
    "ContainerServiceRegistryLoginTypeDef",
    "ContainerServiceStateDetailTypeDef",
    "ContainerServiceTypeDef",
    "ContainerServicesListResultTypeDef",
    "ContainerTypeDef",
    "ContainerUnionTypeDef",
    "CookieObjectOutputTypeDef",
    "CookieObjectTypeDef",
    "CopySnapshotRequestTypeDef",
    "CopySnapshotResultTypeDef",
    "CostEstimateTypeDef",
    "CreateBucketAccessKeyRequestTypeDef",
    "CreateBucketAccessKeyResultTypeDef",
    "CreateBucketRequestTypeDef",
    "CreateBucketResultTypeDef",
    "CreateCertificateRequestTypeDef",
    "CreateCertificateResultTypeDef",
    "CreateCloudFormationStackRequestTypeDef",
    "CreateCloudFormationStackResultTypeDef",
    "CreateContactMethodRequestTypeDef",
    "CreateContactMethodResultTypeDef",
    "CreateContainerServiceDeploymentRequestTypeDef",
    "CreateContainerServiceDeploymentResultTypeDef",
    "CreateContainerServiceRegistryLoginResultTypeDef",
    "CreateContainerServiceRequestTypeDef",
    "CreateContainerServiceResultTypeDef",
    "CreateDiskFromSnapshotRequestTypeDef",
    "CreateDiskFromSnapshotResultTypeDef",
    "CreateDiskRequestTypeDef",
    "CreateDiskResultTypeDef",
    "CreateDiskSnapshotRequestTypeDef",
    "CreateDiskSnapshotResultTypeDef",
    "CreateDistributionRequestTypeDef",
    "CreateDistributionResultTypeDef",
    "CreateDomainEntryRequestTypeDef",
    "CreateDomainEntryResultTypeDef",
    "CreateDomainRequestTypeDef",
    "CreateDomainResultTypeDef",
    "CreateGUISessionAccessDetailsRequestTypeDef",
    "CreateGUISessionAccessDetailsResultTypeDef",
    "CreateInstanceSnapshotRequestTypeDef",
    "CreateInstanceSnapshotResultTypeDef",
    "CreateInstancesFromSnapshotRequestTypeDef",
    "CreateInstancesFromSnapshotResultTypeDef",
    "CreateInstancesRequestTypeDef",
    "CreateInstancesResultTypeDef",
    "CreateKeyPairRequestTypeDef",
    "CreateKeyPairResultTypeDef",
    "CreateLoadBalancerRequestTypeDef",
    "CreateLoadBalancerResultTypeDef",
    "CreateLoadBalancerTlsCertificateRequestTypeDef",
    "CreateLoadBalancerTlsCertificateResultTypeDef",
    "CreateRelationalDatabaseFromSnapshotRequestTypeDef",
    "CreateRelationalDatabaseFromSnapshotResultTypeDef",
    "CreateRelationalDatabaseRequestTypeDef",
    "CreateRelationalDatabaseResultTypeDef",
    "CreateRelationalDatabaseSnapshotRequestTypeDef",
    "CreateRelationalDatabaseSnapshotResultTypeDef",
    "DeleteAlarmRequestTypeDef",
    "DeleteAlarmResultTypeDef",
    "DeleteAutoSnapshotRequestTypeDef",
    "DeleteAutoSnapshotResultTypeDef",
    "DeleteBucketAccessKeyRequestTypeDef",
    "DeleteBucketAccessKeyResultTypeDef",
    "DeleteBucketRequestTypeDef",
    "DeleteBucketResultTypeDef",
    "DeleteCertificateRequestTypeDef",
    "DeleteCertificateResultTypeDef",
    "DeleteContactMethodRequestTypeDef",
    "DeleteContactMethodResultTypeDef",
    "DeleteContainerImageRequestTypeDef",
    "DeleteContainerServiceRequestTypeDef",
    "DeleteDiskRequestTypeDef",
    "DeleteDiskResultTypeDef",
    "DeleteDiskSnapshotRequestTypeDef",
    "DeleteDiskSnapshotResultTypeDef",
    "DeleteDistributionRequestTypeDef",
    "DeleteDistributionResultTypeDef",
    "DeleteDomainEntryRequestTypeDef",
    "DeleteDomainEntryResultTypeDef",
    "DeleteDomainRequestTypeDef",
    "DeleteDomainResultTypeDef",
    "DeleteInstanceRequestTypeDef",
    "DeleteInstanceResultTypeDef",
    "DeleteInstanceSnapshotRequestTypeDef",
    "DeleteInstanceSnapshotResultTypeDef",
    "DeleteKeyPairRequestTypeDef",
    "DeleteKeyPairResultTypeDef",
    "DeleteKnownHostKeysRequestTypeDef",
    "DeleteKnownHostKeysResultTypeDef",
    "DeleteLoadBalancerRequestTypeDef",
    "DeleteLoadBalancerResultTypeDef",
    "DeleteLoadBalancerTlsCertificateRequestTypeDef",
    "DeleteLoadBalancerTlsCertificateResultTypeDef",
    "DeleteRelationalDatabaseRequestTypeDef",
    "DeleteRelationalDatabaseResultTypeDef",
    "DeleteRelationalDatabaseSnapshotRequestTypeDef",
    "DeleteRelationalDatabaseSnapshotResultTypeDef",
    "DestinationInfoTypeDef",
    "DetachCertificateFromDistributionRequestTypeDef",
    "DetachCertificateFromDistributionResultTypeDef",
    "DetachDiskRequestTypeDef",
    "DetachDiskResultTypeDef",
    "DetachInstancesFromLoadBalancerRequestTypeDef",
    "DetachInstancesFromLoadBalancerResultTypeDef",
    "DetachStaticIpRequestTypeDef",
    "DetachStaticIpResultTypeDef",
    "DisableAddOnRequestTypeDef",
    "DisableAddOnResultTypeDef",
    "DiskInfoTypeDef",
    "DiskMapTypeDef",
    "DiskSnapshotInfoTypeDef",
    "DiskSnapshotTypeDef",
    "DiskTypeDef",
    "DistributionBundleTypeDef",
    "DnsRecordCreationStateTypeDef",
    "DomainEntryOutputTypeDef",
    "DomainEntryTypeDef",
    "DomainEntryUnionTypeDef",
    "DomainTypeDef",
    "DomainValidationRecordTypeDef",
    "DownloadDefaultKeyPairResultTypeDef",
    "EnableAddOnRequestTypeDef",
    "EnableAddOnResultTypeDef",
    "EndpointRequestTypeDef",
    "EstimateByTimeTypeDef",
    "ExportSnapshotRecordSourceInfoTypeDef",
    "ExportSnapshotRecordTypeDef",
    "ExportSnapshotRequestTypeDef",
    "ExportSnapshotResultTypeDef",
    "GetActiveNamesRequestPaginateTypeDef",
    "GetActiveNamesRequestTypeDef",
    "GetActiveNamesResultTypeDef",
    "GetAlarmsRequestTypeDef",
    "GetAlarmsResultTypeDef",
    "GetAutoSnapshotsRequestTypeDef",
    "GetAutoSnapshotsResultTypeDef",
    "GetBlueprintsRequestPaginateTypeDef",
    "GetBlueprintsRequestTypeDef",
    "GetBlueprintsResultTypeDef",
    "GetBucketAccessKeysRequestTypeDef",
    "GetBucketAccessKeysResultTypeDef",
    "GetBucketBundlesRequestTypeDef",
    "GetBucketBundlesResultTypeDef",
    "GetBucketMetricDataRequestTypeDef",
    "GetBucketMetricDataResultTypeDef",
    "GetBucketsRequestTypeDef",
    "GetBucketsResultTypeDef",
    "GetBundlesRequestPaginateTypeDef",
    "GetBundlesRequestTypeDef",
    "GetBundlesResultTypeDef",
    "GetCertificatesRequestTypeDef",
    "GetCertificatesResultTypeDef",
    "GetCloudFormationStackRecordsRequestPaginateTypeDef",
    "GetCloudFormationStackRecordsRequestTypeDef",
    "GetCloudFormationStackRecordsResultTypeDef",
    "GetContactMethodsRequestTypeDef",
    "GetContactMethodsResultTypeDef",
    "GetContainerAPIMetadataResultTypeDef",
    "GetContainerImagesRequestTypeDef",
    "GetContainerImagesResultTypeDef",
    "GetContainerLogRequestTypeDef",
    "GetContainerLogResultTypeDef",
    "GetContainerServiceDeploymentsRequestTypeDef",
    "GetContainerServiceDeploymentsResultTypeDef",
    "GetContainerServiceMetricDataRequestTypeDef",
    "GetContainerServiceMetricDataResultTypeDef",
    "GetContainerServicePowersResultTypeDef",
    "GetContainerServicesRequestTypeDef",
    "GetCostEstimateRequestTypeDef",
    "GetCostEstimateResultTypeDef",
    "GetDiskRequestTypeDef",
    "GetDiskResultTypeDef",
    "GetDiskSnapshotRequestTypeDef",
    "GetDiskSnapshotResultTypeDef",
    "GetDiskSnapshotsRequestPaginateTypeDef",
    "GetDiskSnapshotsRequestTypeDef",
    "GetDiskSnapshotsResultTypeDef",
    "GetDisksRequestPaginateTypeDef",
    "GetDisksRequestTypeDef",
    "GetDisksResultTypeDef",
    "GetDistributionBundlesResultTypeDef",
    "GetDistributionLatestCacheResetRequestTypeDef",
    "GetDistributionLatestCacheResetResultTypeDef",
    "GetDistributionMetricDataRequestTypeDef",
    "GetDistributionMetricDataResultTypeDef",
    "GetDistributionsRequestTypeDef",
    "GetDistributionsResultTypeDef",
    "GetDomainRequestTypeDef",
    "GetDomainResultTypeDef",
    "GetDomainsRequestPaginateTypeDef",
    "GetDomainsRequestTypeDef",
    "GetDomainsResultTypeDef",
    "GetExportSnapshotRecordsRequestPaginateTypeDef",
    "GetExportSnapshotRecordsRequestTypeDef",
    "GetExportSnapshotRecordsResultTypeDef",
    "GetInstanceAccessDetailsRequestTypeDef",
    "GetInstanceAccessDetailsResultTypeDef",
    "GetInstanceMetricDataRequestTypeDef",
    "GetInstanceMetricDataResultTypeDef",
    "GetInstancePortStatesRequestTypeDef",
    "GetInstancePortStatesResultTypeDef",
    "GetInstanceRequestTypeDef",
    "GetInstanceResultTypeDef",
    "GetInstanceSnapshotRequestTypeDef",
    "GetInstanceSnapshotResultTypeDef",
    "GetInstanceSnapshotsRequestPaginateTypeDef",
    "GetInstanceSnapshotsRequestTypeDef",
    "GetInstanceSnapshotsResultTypeDef",
    "GetInstanceStateRequestTypeDef",
    "GetInstanceStateResultTypeDef",
    "GetInstancesRequestPaginateTypeDef",
    "GetInstancesRequestTypeDef",
    "GetInstancesResultTypeDef",
    "GetKeyPairRequestTypeDef",
    "GetKeyPairResultTypeDef",
    "GetKeyPairsRequestPaginateTypeDef",
    "GetKeyPairsRequestTypeDef",
    "GetKeyPairsResultTypeDef",
    "GetLoadBalancerMetricDataRequestTypeDef",
    "GetLoadBalancerMetricDataResultTypeDef",
    "GetLoadBalancerRequestTypeDef",
    "GetLoadBalancerResultTypeDef",
    "GetLoadBalancerTlsCertificatesRequestTypeDef",
    "GetLoadBalancerTlsCertificatesResultTypeDef",
    "GetLoadBalancerTlsPoliciesRequestTypeDef",
    "GetLoadBalancerTlsPoliciesResultTypeDef",
    "GetLoadBalancersRequestPaginateTypeDef",
    "GetLoadBalancersRequestTypeDef",
    "GetLoadBalancersResultTypeDef",
    "GetOperationRequestTypeDef",
    "GetOperationResultTypeDef",
    "GetOperationsForResourceRequestTypeDef",
    "GetOperationsForResourceResultTypeDef",
    "GetOperationsRequestPaginateTypeDef",
    "GetOperationsRequestTypeDef",
    "GetOperationsResultTypeDef",
    "GetRegionsRequestTypeDef",
    "GetRegionsResultTypeDef",
    "GetRelationalDatabaseBlueprintsRequestPaginateTypeDef",
    "GetRelationalDatabaseBlueprintsRequestTypeDef",
    "GetRelationalDatabaseBlueprintsResultTypeDef",
    "GetRelationalDatabaseBundlesRequestPaginateTypeDef",
    "GetRelationalDatabaseBundlesRequestTypeDef",
    "GetRelationalDatabaseBundlesResultTypeDef",
    "GetRelationalDatabaseEventsRequestPaginateTypeDef",
    "GetRelationalDatabaseEventsRequestTypeDef",
    "GetRelationalDatabaseEventsResultTypeDef",
    "GetRelationalDatabaseLogEventsRequestTypeDef",
    "GetRelationalDatabaseLogEventsResultTypeDef",
    "GetRelationalDatabaseLogStreamsRequestTypeDef",
    "GetRelationalDatabaseLogStreamsResultTypeDef",
    "GetRelationalDatabaseMasterUserPasswordRequestTypeDef",
    "GetRelationalDatabaseMasterUserPasswordResultTypeDef",
    "GetRelationalDatabaseMetricDataRequestTypeDef",
    "GetRelationalDatabaseMetricDataResultTypeDef",
    "GetRelationalDatabaseParametersRequestPaginateTypeDef",
    "GetRelationalDatabaseParametersRequestTypeDef",
    "GetRelationalDatabaseParametersResultTypeDef",
    "GetRelationalDatabaseRequestTypeDef",
    "GetRelationalDatabaseResultTypeDef",
    "GetRelationalDatabaseSnapshotRequestTypeDef",
    "GetRelationalDatabaseSnapshotResultTypeDef",
    "GetRelationalDatabaseSnapshotsRequestPaginateTypeDef",
    "GetRelationalDatabaseSnapshotsRequestTypeDef",
    "GetRelationalDatabaseSnapshotsResultTypeDef",
    "GetRelationalDatabasesRequestPaginateTypeDef",
    "GetRelationalDatabasesRequestTypeDef",
    "GetRelationalDatabasesResultTypeDef",
    "GetSetupHistoryRequestTypeDef",
    "GetSetupHistoryResultTypeDef",
    "GetStaticIpRequestTypeDef",
    "GetStaticIpResultTypeDef",
    "GetStaticIpsRequestPaginateTypeDef",
    "GetStaticIpsRequestTypeDef",
    "GetStaticIpsResultTypeDef",
    "HeaderObjectOutputTypeDef",
    "HeaderObjectTypeDef",
    "HostKeyAttributesTypeDef",
    "ImportKeyPairRequestTypeDef",
    "ImportKeyPairResultTypeDef",
    "InputOriginTypeDef",
    "InstanceAccessDetailsTypeDef",
    "InstanceEntryTypeDef",
    "InstanceHardwareTypeDef",
    "InstanceHealthSummaryTypeDef",
    "InstanceMetadataOptionsTypeDef",
    "InstanceNetworkingTypeDef",
    "InstancePortInfoTypeDef",
    "InstancePortStateTypeDef",
    "InstanceSnapshotInfoTypeDef",
    "InstanceSnapshotTypeDef",
    "InstanceStateTypeDef",
    "InstanceTypeDef",
    "IsVpcPeeredResultTypeDef",
    "KeyPairTypeDef",
    "LightsailDistributionTypeDef",
    "LoadBalancerTlsCertificateDnsRecordCreationStateTypeDef",
    "LoadBalancerTlsCertificateDomainValidationOptionTypeDef",
    "LoadBalancerTlsCertificateDomainValidationRecordTypeDef",
    "LoadBalancerTlsCertificateRenewalSummaryTypeDef",
    "LoadBalancerTlsCertificateSummaryTypeDef",
    "LoadBalancerTlsCertificateTypeDef",
    "LoadBalancerTlsPolicyTypeDef",
    "LoadBalancerTypeDef",
    "LogEventTypeDef",
    "MetricDatapointTypeDef",
    "MonitoredResourceInfoTypeDef",
    "MonthlyTransferTypeDef",
    "NameServersUpdateStateTypeDef",
    "OpenInstancePublicPortsRequestTypeDef",
    "OpenInstancePublicPortsResultTypeDef",
    "OperationTypeDef",
    "OriginTypeDef",
    "PaginatorConfigTypeDef",
    "PasswordDataTypeDef",
    "PeerVpcResultTypeDef",
    "PendingMaintenanceActionTypeDef",
    "PendingModifiedRelationalDatabaseValuesTypeDef",
    "PortInfoTypeDef",
    "PrivateRegistryAccessRequestTypeDef",
    "PrivateRegistryAccessTypeDef",
    "PutAlarmRequestTypeDef",
    "PutAlarmResultTypeDef",
    "PutInstancePublicPortsRequestTypeDef",
    "PutInstancePublicPortsResultTypeDef",
    "QueryStringObjectOutputTypeDef",
    "QueryStringObjectTypeDef",
    "R53HostedZoneDeletionStateTypeDef",
    "RebootInstanceRequestTypeDef",
    "RebootInstanceResultTypeDef",
    "RebootRelationalDatabaseRequestTypeDef",
    "RebootRelationalDatabaseResultTypeDef",
    "RegionTypeDef",
    "RegisterContainerImageRequestTypeDef",
    "RegisterContainerImageResultTypeDef",
    "RegisteredDomainDelegationInfoTypeDef",
    "RelationalDatabaseBlueprintTypeDef",
    "RelationalDatabaseBundleTypeDef",
    "RelationalDatabaseEndpointTypeDef",
    "RelationalDatabaseEventTypeDef",
    "RelationalDatabaseHardwareTypeDef",
    "RelationalDatabaseParameterTypeDef",
    "RelationalDatabaseSnapshotTypeDef",
    "RelationalDatabaseTypeDef",
    "ReleaseStaticIpRequestTypeDef",
    "ReleaseStaticIpResultTypeDef",
    "RenewalSummaryTypeDef",
    "ResetDistributionCacheRequestTypeDef",
    "ResetDistributionCacheResultTypeDef",
    "ResourceBudgetEstimateTypeDef",
    "ResourceLocationTypeDef",
    "ResourceReceivingAccessTypeDef",
    "ResourceRecordTypeDef",
    "ResponseMetadataTypeDef",
    "SendContactMethodVerificationRequestTypeDef",
    "SendContactMethodVerificationResultTypeDef",
    "SessionTypeDef",
    "SetIpAddressTypeRequestTypeDef",
    "SetIpAddressTypeResultTypeDef",
    "SetResourceAccessForBucketRequestTypeDef",
    "SetResourceAccessForBucketResultTypeDef",
    "SetupExecutionDetailsTypeDef",
    "SetupHistoryResourceTypeDef",
    "SetupHistoryTypeDef",
    "SetupInstanceHttpsRequestTypeDef",
    "SetupInstanceHttpsResultTypeDef",
    "SetupRequestTypeDef",
    "StartGUISessionRequestTypeDef",
    "StartGUISessionResultTypeDef",
    "StartInstanceRequestTypeDef",
    "StartInstanceResultTypeDef",
    "StartRelationalDatabaseRequestTypeDef",
    "StartRelationalDatabaseResultTypeDef",
    "StaticIpTypeDef",
    "StopGUISessionRequestTypeDef",
    "StopGUISessionResultTypeDef",
    "StopInstanceOnIdleRequestTypeDef",
    "StopInstanceRequestTypeDef",
    "StopInstanceResultTypeDef",
    "StopRelationalDatabaseRequestTypeDef",
    "StopRelationalDatabaseResultTypeDef",
    "TagResourceRequestTypeDef",
    "TagResourceResultTypeDef",
    "TagTypeDef",
    "TestAlarmRequestTypeDef",
    "TestAlarmResultTypeDef",
    "TimePeriodTypeDef",
    "TimestampTypeDef",
    "UnpeerVpcResultTypeDef",
    "UntagResourceRequestTypeDef",
    "UntagResourceResultTypeDef",
    "UpdateBucketBundleRequestTypeDef",
    "UpdateBucketBundleResultTypeDef",
    "UpdateBucketRequestTypeDef",
    "UpdateBucketResultTypeDef",
    "UpdateContainerServiceRequestTypeDef",
    "UpdateContainerServiceResultTypeDef",
    "UpdateDistributionBundleRequestTypeDef",
    "UpdateDistributionBundleResultTypeDef",
    "UpdateDistributionRequestTypeDef",
    "UpdateDistributionResultTypeDef",
    "UpdateDomainEntryRequestTypeDef",
    "UpdateDomainEntryResultTypeDef",
    "UpdateInstanceMetadataOptionsRequestTypeDef",
    "UpdateInstanceMetadataOptionsResultTypeDef",
    "UpdateLoadBalancerAttributeRequestTypeDef",
    "UpdateLoadBalancerAttributeResultTypeDef",
    "UpdateRelationalDatabaseParametersRequestTypeDef",
    "UpdateRelationalDatabaseParametersResultTypeDef",
    "UpdateRelationalDatabaseRequestTypeDef",
    "UpdateRelationalDatabaseResultTypeDef",
)

class AccessKeyLastUsedTypeDef(TypedDict):
    lastUsedDate: NotRequired[datetime]
    region: NotRequired[str]
    serviceName: NotRequired[str]

class AccessRulesTypeDef(TypedDict):
    getObject: NotRequired[AccessTypeType]
    allowPublicOverrides: NotRequired[bool]

class AccountLevelBpaSyncTypeDef(TypedDict):
    status: NotRequired[AccountLevelBpaSyncStatusType]
    lastSyncedAt: NotRequired[datetime]
    message: NotRequired[BPAStatusMessageType]
    bpaImpactsLightsail: NotRequired[bool]

class AutoSnapshotAddOnRequestTypeDef(TypedDict):
    snapshotTimeOfDay: NotRequired[str]

class StopInstanceOnIdleRequestTypeDef(TypedDict):
    threshold: NotRequired[str]
    duration: NotRequired[str]

class AddOnTypeDef(TypedDict):
    name: NotRequired[str]
    status: NotRequired[str]
    snapshotTimeOfDay: NotRequired[str]
    nextSnapshotTimeOfDay: NotRequired[str]
    threshold: NotRequired[str]
    duration: NotRequired[str]

class MonitoredResourceInfoTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    resourceType: NotRequired[ResourceTypeType]

class ResourceLocationTypeDef(TypedDict):
    availabilityZone: NotRequired[str]
    regionName: NotRequired[RegionNameType]

class AllocateStaticIpRequestTypeDef(TypedDict):
    staticIpName: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class AttachCertificateToDistributionRequestTypeDef(TypedDict):
    distributionName: str
    certificateName: str

class AttachDiskRequestTypeDef(TypedDict):
    diskName: str
    instanceName: str
    diskPath: str
    autoMounting: NotRequired[bool]

class AttachInstancesToLoadBalancerRequestTypeDef(TypedDict):
    loadBalancerName: str
    instanceNames: Sequence[str]

class AttachLoadBalancerTlsCertificateRequestTypeDef(TypedDict):
    loadBalancerName: str
    certificateName: str

class AttachStaticIpRequestTypeDef(TypedDict):
    staticIpName: str
    instanceName: str

class AttachedDiskTypeDef(TypedDict):
    path: NotRequired[str]
    sizeInGb: NotRequired[int]

class AvailabilityZoneTypeDef(TypedDict):
    zoneName: NotRequired[str]
    state: NotRequired[str]

BlueprintTypeDef = TypedDict(
    "BlueprintTypeDef",
    {
        "blueprintId": NotRequired[str],
        "name": NotRequired[str],
        "group": NotRequired[str],
        "type": NotRequired[BlueprintTypeType],
        "description": NotRequired[str],
        "isActive": NotRequired[bool],
        "minPower": NotRequired[int],
        "version": NotRequired[str],
        "versionCode": NotRequired[str],
        "productUrl": NotRequired[str],
        "licenseUrl": NotRequired[str],
        "platform": NotRequired[InstancePlatformType],
        "appCategory": NotRequired[Literal["LfR"]],
    },
)

class BucketAccessLogConfigTypeDef(TypedDict):
    enabled: bool
    destination: NotRequired[str]
    prefix: NotRequired[str]

class BucketBundleTypeDef(TypedDict):
    bundleId: NotRequired[str]
    name: NotRequired[str]
    price: NotRequired[float]
    storagePerMonthInGb: NotRequired[int]
    transferPerMonthInGb: NotRequired[int]
    isActive: NotRequired[bool]

BucketCorsRuleOutputTypeDef = TypedDict(
    "BucketCorsRuleOutputTypeDef",
    {
        "allowedMethods": list[str],
        "allowedOrigins": list[str],
        "id": NotRequired[str],
        "allowedHeaders": NotRequired[list[str]],
        "exposeHeaders": NotRequired[list[str]],
        "maxAgeSeconds": NotRequired[int],
    },
)
BucketCorsRuleTypeDef = TypedDict(
    "BucketCorsRuleTypeDef",
    {
        "allowedMethods": Sequence[str],
        "allowedOrigins": Sequence[str],
        "id": NotRequired[str],
        "allowedHeaders": NotRequired[Sequence[str]],
        "exposeHeaders": NotRequired[Sequence[str]],
        "maxAgeSeconds": NotRequired[int],
    },
)

class BucketStateTypeDef(TypedDict):
    code: NotRequired[str]
    message: NotRequired[str]

class ResourceReceivingAccessTypeDef(TypedDict):
    name: NotRequired[str]
    resourceType: NotRequired[str]

class TagTypeDef(TypedDict):
    key: NotRequired[str]
    value: NotRequired[str]

class BundleTypeDef(TypedDict):
    price: NotRequired[float]
    cpuCount: NotRequired[int]
    diskSizeInGb: NotRequired[int]
    bundleId: NotRequired[str]
    instanceType: NotRequired[str]
    isActive: NotRequired[bool]
    name: NotRequired[str]
    power: NotRequired[int]
    ramSizeInGb: NotRequired[float]
    transferPerMonthInGb: NotRequired[int]
    supportedPlatforms: NotRequired[list[InstancePlatformType]]
    supportedAppCategories: NotRequired[list[Literal["LfR"]]]
    publicIpv4AddressCount: NotRequired[int]

class CacheBehaviorPerPathTypeDef(TypedDict):
    path: NotRequired[str]
    behavior: NotRequired[BehaviorEnumType]

class CacheBehaviorTypeDef(TypedDict):
    behavior: NotRequired[BehaviorEnumType]

class CookieObjectOutputTypeDef(TypedDict):
    option: NotRequired[ForwardValuesType]
    cookiesAllowList: NotRequired[list[str]]

class HeaderObjectOutputTypeDef(TypedDict):
    option: NotRequired[ForwardValuesType]
    headersAllowList: NotRequired[list[HeaderEnumType]]

class QueryStringObjectOutputTypeDef(TypedDict):
    option: NotRequired[bool]
    queryStringsAllowList: NotRequired[list[str]]

class CookieObjectTypeDef(TypedDict):
    option: NotRequired[ForwardValuesType]
    cookiesAllowList: NotRequired[Sequence[str]]

class HeaderObjectTypeDef(TypedDict):
    option: NotRequired[ForwardValuesType]
    headersAllowList: NotRequired[Sequence[HeaderEnumType]]

class QueryStringObjectTypeDef(TypedDict):
    option: NotRequired[bool]
    queryStringsAllowList: NotRequired[Sequence[str]]

class PortInfoTypeDef(TypedDict):
    fromPort: NotRequired[int]
    toPort: NotRequired[int]
    protocol: NotRequired[NetworkProtocolType]
    cidrs: NotRequired[Sequence[str]]
    ipv6Cidrs: NotRequired[Sequence[str]]
    cidrListAliases: NotRequired[Sequence[str]]

class CloudFormationStackRecordSourceInfoTypeDef(TypedDict):
    resourceType: NotRequired[Literal["ExportSnapshotRecord"]]
    name: NotRequired[str]
    arn: NotRequired[str]

DestinationInfoTypeDef = TypedDict(
    "DestinationInfoTypeDef",
    {
        "id": NotRequired[str],
        "service": NotRequired[str],
    },
)

class ContainerImageTypeDef(TypedDict):
    image: NotRequired[str]
    digest: NotRequired[str]
    createdAt: NotRequired[datetime]

class ContainerOutputTypeDef(TypedDict):
    image: NotRequired[str]
    command: NotRequired[list[str]]
    environment: NotRequired[dict[str, str]]
    ports: NotRequired[dict[str, ContainerServiceProtocolType]]

class ContainerServiceECRImagePullerRoleRequestTypeDef(TypedDict):
    isActive: NotRequired[bool]

class ContainerServiceECRImagePullerRoleTypeDef(TypedDict):
    isActive: NotRequired[bool]
    principalArn: NotRequired[str]

class ContainerServiceHealthCheckConfigTypeDef(TypedDict):
    healthyThreshold: NotRequired[int]
    unhealthyThreshold: NotRequired[int]
    timeoutSeconds: NotRequired[int]
    intervalSeconds: NotRequired[int]
    path: NotRequired[str]
    successCodes: NotRequired[str]

class ContainerServiceLogEventTypeDef(TypedDict):
    createdAt: NotRequired[datetime]
    message: NotRequired[str]

class ContainerServicePowerTypeDef(TypedDict):
    powerId: NotRequired[str]
    price: NotRequired[float]
    cpuCount: NotRequired[float]
    ramSizeInGb: NotRequired[float]
    name: NotRequired[str]
    isActive: NotRequired[bool]

class ContainerServiceRegistryLoginTypeDef(TypedDict):
    username: NotRequired[str]
    password: NotRequired[str]
    expiresAt: NotRequired[datetime]
    registry: NotRequired[str]

class ContainerServiceStateDetailTypeDef(TypedDict):
    code: NotRequired[ContainerServiceStateDetailCodeType]
    message: NotRequired[str]

class ContainerTypeDef(TypedDict):
    image: NotRequired[str]
    command: NotRequired[Sequence[str]]
    environment: NotRequired[Mapping[str, str]]
    ports: NotRequired[Mapping[str, ContainerServiceProtocolType]]

class CopySnapshotRequestTypeDef(TypedDict):
    targetSnapshotName: str
    sourceRegion: RegionNameType
    sourceSnapshotName: NotRequired[str]
    sourceResourceName: NotRequired[str]
    restoreDate: NotRequired[str]
    useLatestRestorableAutoSnapshot: NotRequired[bool]

class CreateBucketAccessKeyRequestTypeDef(TypedDict):
    bucketName: str

class InstanceEntryTypeDef(TypedDict):
    sourceName: str
    instanceType: str
    portInfoSource: PortInfoSourceTypeType
    availabilityZone: str
    userData: NotRequired[str]

class CreateContactMethodRequestTypeDef(TypedDict):
    protocol: ContactProtocolType
    contactEndpoint: str

class InputOriginTypeDef(TypedDict):
    name: NotRequired[str]
    regionName: NotRequired[RegionNameType]
    protocolPolicy: NotRequired[OriginProtocolPolicyEnumType]
    responseTimeout: NotRequired[int]

class CreateGUISessionAccessDetailsRequestTypeDef(TypedDict):
    resourceName: str

class SessionTypeDef(TypedDict):
    name: NotRequired[str]
    url: NotRequired[str]
    isPrimary: NotRequired[bool]

class DiskMapTypeDef(TypedDict):
    originalDiskPath: NotRequired[str]
    newDiskName: NotRequired[str]

TimestampTypeDef = Union[datetime, str]

class DeleteAlarmRequestTypeDef(TypedDict):
    alarmName: str

class DeleteAutoSnapshotRequestTypeDef(TypedDict):
    resourceName: str
    date: str

class DeleteBucketAccessKeyRequestTypeDef(TypedDict):
    bucketName: str
    accessKeyId: str

class DeleteBucketRequestTypeDef(TypedDict):
    bucketName: str
    forceDelete: NotRequired[bool]

class DeleteCertificateRequestTypeDef(TypedDict):
    certificateName: str

class DeleteContactMethodRequestTypeDef(TypedDict):
    protocol: ContactProtocolType

class DeleteContainerImageRequestTypeDef(TypedDict):
    serviceName: str
    image: str

class DeleteContainerServiceRequestTypeDef(TypedDict):
    serviceName: str

class DeleteDiskRequestTypeDef(TypedDict):
    diskName: str
    forceDeleteAddOns: NotRequired[bool]

class DeleteDiskSnapshotRequestTypeDef(TypedDict):
    diskSnapshotName: str

class DeleteDistributionRequestTypeDef(TypedDict):
    distributionName: NotRequired[str]

class DeleteDomainRequestTypeDef(TypedDict):
    domainName: str

class DeleteInstanceRequestTypeDef(TypedDict):
    instanceName: str
    forceDeleteAddOns: NotRequired[bool]

class DeleteInstanceSnapshotRequestTypeDef(TypedDict):
    instanceSnapshotName: str

class DeleteKeyPairRequestTypeDef(TypedDict):
    keyPairName: str
    expectedFingerprint: NotRequired[str]

class DeleteKnownHostKeysRequestTypeDef(TypedDict):
    instanceName: str

class DeleteLoadBalancerRequestTypeDef(TypedDict):
    loadBalancerName: str

class DeleteLoadBalancerTlsCertificateRequestTypeDef(TypedDict):
    loadBalancerName: str
    certificateName: str
    force: NotRequired[bool]

class DeleteRelationalDatabaseRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    skipFinalSnapshot: NotRequired[bool]
    finalRelationalDatabaseSnapshotName: NotRequired[str]

class DeleteRelationalDatabaseSnapshotRequestTypeDef(TypedDict):
    relationalDatabaseSnapshotName: str

class DetachCertificateFromDistributionRequestTypeDef(TypedDict):
    distributionName: str

class DetachDiskRequestTypeDef(TypedDict):
    diskName: str

class DetachInstancesFromLoadBalancerRequestTypeDef(TypedDict):
    loadBalancerName: str
    instanceNames: Sequence[str]

class DetachStaticIpRequestTypeDef(TypedDict):
    staticIpName: str

class DisableAddOnRequestTypeDef(TypedDict):
    addOnType: AddOnTypeType
    resourceName: str

class DiskInfoTypeDef(TypedDict):
    name: NotRequired[str]
    path: NotRequired[str]
    sizeInGb: NotRequired[int]
    isSystemDisk: NotRequired[bool]

class DiskSnapshotInfoTypeDef(TypedDict):
    sizeInGb: NotRequired[int]

class DistributionBundleTypeDef(TypedDict):
    bundleId: NotRequired[str]
    name: NotRequired[str]
    price: NotRequired[float]
    transferPerMonthInGb: NotRequired[int]
    isActive: NotRequired[bool]

class DnsRecordCreationStateTypeDef(TypedDict):
    code: NotRequired[DnsRecordCreationStateCodeType]
    message: NotRequired[str]

DomainEntryOutputTypeDef = TypedDict(
    "DomainEntryOutputTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "target": NotRequired[str],
        "isAlias": NotRequired[bool],
        "type": NotRequired[str],
        "options": NotRequired[dict[str, str]],
    },
)
DomainEntryTypeDef = TypedDict(
    "DomainEntryTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "target": NotRequired[str],
        "isAlias": NotRequired[bool],
        "type": NotRequired[str],
        "options": NotRequired[Mapping[str, str]],
    },
)
ResourceRecordTypeDef = TypedDict(
    "ResourceRecordTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "value": NotRequired[str],
    },
)

class TimePeriodTypeDef(TypedDict):
    start: NotRequired[datetime]
    end: NotRequired[datetime]

class ExportSnapshotRequestTypeDef(TypedDict):
    sourceSnapshotName: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class GetActiveNamesRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]

class GetAlarmsRequestTypeDef(TypedDict):
    alarmName: NotRequired[str]
    pageToken: NotRequired[str]
    monitoredResourceName: NotRequired[str]

class GetAutoSnapshotsRequestTypeDef(TypedDict):
    resourceName: str

class GetBlueprintsRequestTypeDef(TypedDict):
    includeInactive: NotRequired[bool]
    pageToken: NotRequired[str]
    appCategory: NotRequired[Literal["LfR"]]

class GetBucketAccessKeysRequestTypeDef(TypedDict):
    bucketName: str

class GetBucketBundlesRequestTypeDef(TypedDict):
    includeInactive: NotRequired[bool]

MetricDatapointTypeDef = TypedDict(
    "MetricDatapointTypeDef",
    {
        "average": NotRequired[float],
        "maximum": NotRequired[float],
        "minimum": NotRequired[float],
        "sampleCount": NotRequired[float],
        "sum": NotRequired[float],
        "timestamp": NotRequired[datetime],
        "unit": NotRequired[MetricUnitType],
    },
)

class GetBucketsRequestTypeDef(TypedDict):
    bucketName: NotRequired[str]
    pageToken: NotRequired[str]
    includeConnectedResources: NotRequired[bool]
    includeCors: NotRequired[bool]

class GetBundlesRequestTypeDef(TypedDict):
    includeInactive: NotRequired[bool]
    pageToken: NotRequired[str]
    appCategory: NotRequired[Literal["LfR"]]

class GetCertificatesRequestTypeDef(TypedDict):
    certificateStatuses: NotRequired[Sequence[CertificateStatusType]]
    includeCertificateDetails: NotRequired[bool]
    certificateName: NotRequired[str]
    pageToken: NotRequired[str]

class GetCloudFormationStackRecordsRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]

class GetContactMethodsRequestTypeDef(TypedDict):
    protocols: NotRequired[Sequence[ContactProtocolType]]

class GetContainerImagesRequestTypeDef(TypedDict):
    serviceName: str

class GetContainerServiceDeploymentsRequestTypeDef(TypedDict):
    serviceName: str

class GetContainerServicesRequestTypeDef(TypedDict):
    serviceName: NotRequired[str]

class GetDiskRequestTypeDef(TypedDict):
    diskName: str

class GetDiskSnapshotRequestTypeDef(TypedDict):
    diskSnapshotName: str

class GetDiskSnapshotsRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]

class GetDisksRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]

class GetDistributionLatestCacheResetRequestTypeDef(TypedDict):
    distributionName: NotRequired[str]

class GetDistributionsRequestTypeDef(TypedDict):
    distributionName: NotRequired[str]
    pageToken: NotRequired[str]

class GetDomainRequestTypeDef(TypedDict):
    domainName: str

class GetDomainsRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]

class GetExportSnapshotRecordsRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]

class GetInstanceAccessDetailsRequestTypeDef(TypedDict):
    instanceName: str
    protocol: NotRequired[InstanceAccessProtocolType]

class GetInstancePortStatesRequestTypeDef(TypedDict):
    instanceName: str

class InstancePortStateTypeDef(TypedDict):
    fromPort: NotRequired[int]
    toPort: NotRequired[int]
    protocol: NotRequired[NetworkProtocolType]
    state: NotRequired[PortStateType]
    cidrs: NotRequired[list[str]]
    ipv6Cidrs: NotRequired[list[str]]
    cidrListAliases: NotRequired[list[str]]

class GetInstanceRequestTypeDef(TypedDict):
    instanceName: str

class GetInstanceSnapshotRequestTypeDef(TypedDict):
    instanceSnapshotName: str

class GetInstanceSnapshotsRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]

class GetInstanceStateRequestTypeDef(TypedDict):
    instanceName: str

class InstanceStateTypeDef(TypedDict):
    code: NotRequired[int]
    name: NotRequired[str]

class GetInstancesRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]

class GetKeyPairRequestTypeDef(TypedDict):
    keyPairName: str

class GetKeyPairsRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]
    includeDefaultKeyPair: NotRequired[bool]

class GetLoadBalancerRequestTypeDef(TypedDict):
    loadBalancerName: str

class GetLoadBalancerTlsCertificatesRequestTypeDef(TypedDict):
    loadBalancerName: str

class GetLoadBalancerTlsPoliciesRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]

class LoadBalancerTlsPolicyTypeDef(TypedDict):
    name: NotRequired[str]
    isDefault: NotRequired[bool]
    description: NotRequired[str]
    protocols: NotRequired[list[str]]
    ciphers: NotRequired[list[str]]

class GetLoadBalancersRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]

class GetOperationRequestTypeDef(TypedDict):
    operationId: str

class GetOperationsForResourceRequestTypeDef(TypedDict):
    resourceName: str
    pageToken: NotRequired[str]

class GetOperationsRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]

class GetRegionsRequestTypeDef(TypedDict):
    includeAvailabilityZones: NotRequired[bool]
    includeRelationalDatabaseAvailabilityZones: NotRequired[bool]

class GetRelationalDatabaseBlueprintsRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]

class RelationalDatabaseBlueprintTypeDef(TypedDict):
    blueprintId: NotRequired[str]
    engine: NotRequired[Literal["mysql"]]
    engineVersion: NotRequired[str]
    engineDescription: NotRequired[str]
    engineVersionDescription: NotRequired[str]
    isEngineDefault: NotRequired[bool]

class GetRelationalDatabaseBundlesRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]
    includeInactive: NotRequired[bool]

class RelationalDatabaseBundleTypeDef(TypedDict):
    bundleId: NotRequired[str]
    name: NotRequired[str]
    price: NotRequired[float]
    ramSizeInGb: NotRequired[float]
    diskSizeInGb: NotRequired[int]
    transferPerMonthInGb: NotRequired[int]
    cpuCount: NotRequired[int]
    isEncrypted: NotRequired[bool]
    isActive: NotRequired[bool]

class GetRelationalDatabaseEventsRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    durationInMinutes: NotRequired[int]
    pageToken: NotRequired[str]

class RelationalDatabaseEventTypeDef(TypedDict):
    resource: NotRequired[str]
    createdAt: NotRequired[datetime]
    message: NotRequired[str]
    eventCategories: NotRequired[list[str]]

class LogEventTypeDef(TypedDict):
    createdAt: NotRequired[datetime]
    message: NotRequired[str]

class GetRelationalDatabaseLogStreamsRequestTypeDef(TypedDict):
    relationalDatabaseName: str

class GetRelationalDatabaseMasterUserPasswordRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    passwordVersion: NotRequired[RelationalDatabasePasswordVersionType]

class GetRelationalDatabaseParametersRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    pageToken: NotRequired[str]

class RelationalDatabaseParameterTypeDef(TypedDict):
    allowedValues: NotRequired[str]
    applyMethod: NotRequired[str]
    applyType: NotRequired[str]
    dataType: NotRequired[str]
    description: NotRequired[str]
    isModifiable: NotRequired[bool]
    parameterName: NotRequired[str]
    parameterValue: NotRequired[str]

class GetRelationalDatabaseRequestTypeDef(TypedDict):
    relationalDatabaseName: str

class GetRelationalDatabaseSnapshotRequestTypeDef(TypedDict):
    relationalDatabaseSnapshotName: str

class GetRelationalDatabaseSnapshotsRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]

class GetRelationalDatabasesRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]

class GetSetupHistoryRequestTypeDef(TypedDict):
    resourceName: str
    pageToken: NotRequired[str]

class GetStaticIpRequestTypeDef(TypedDict):
    staticIpName: str

class GetStaticIpsRequestTypeDef(TypedDict):
    pageToken: NotRequired[str]

class HostKeyAttributesTypeDef(TypedDict):
    algorithm: NotRequired[str]
    publicKey: NotRequired[str]
    witnessedAt: NotRequired[datetime]
    fingerprintSHA1: NotRequired[str]
    fingerprintSHA256: NotRequired[str]
    notValidBefore: NotRequired[datetime]
    notValidAfter: NotRequired[datetime]

class ImportKeyPairRequestTypeDef(TypedDict):
    keyPairName: str
    publicKeyBase64: str

class PasswordDataTypeDef(TypedDict):
    ciphertext: NotRequired[str]
    keyPairName: NotRequired[str]

class InstanceHealthSummaryTypeDef(TypedDict):
    instanceName: NotRequired[str]
    instanceHealth: NotRequired[InstanceHealthStateType]
    instanceHealthReason: NotRequired[InstanceHealthReasonType]

class InstanceMetadataOptionsTypeDef(TypedDict):
    state: NotRequired[InstanceMetadataStateType]
    httpTokens: NotRequired[HttpTokensType]
    httpEndpoint: NotRequired[HttpEndpointType]
    httpPutResponseHopLimit: NotRequired[int]
    httpProtocolIpv6: NotRequired[HttpProtocolIpv6Type]

class InstancePortInfoTypeDef(TypedDict):
    fromPort: NotRequired[int]
    toPort: NotRequired[int]
    protocol: NotRequired[NetworkProtocolType]
    accessFrom: NotRequired[str]
    accessType: NotRequired[PortAccessTypeType]
    commonName: NotRequired[str]
    accessDirection: NotRequired[AccessDirectionType]
    cidrs: NotRequired[list[str]]
    ipv6Cidrs: NotRequired[list[str]]
    cidrListAliases: NotRequired[list[str]]

class MonthlyTransferTypeDef(TypedDict):
    gbPerMonthAllocated: NotRequired[int]

class OriginTypeDef(TypedDict):
    name: NotRequired[str]
    resourceType: NotRequired[ResourceTypeType]
    regionName: NotRequired[RegionNameType]
    protocolPolicy: NotRequired[OriginProtocolPolicyEnumType]
    responseTimeout: NotRequired[int]

class LoadBalancerTlsCertificateDnsRecordCreationStateTypeDef(TypedDict):
    code: NotRequired[LoadBalancerTlsCertificateDnsRecordCreationStateCodeType]
    message: NotRequired[str]

class LoadBalancerTlsCertificateDomainValidationOptionTypeDef(TypedDict):
    domainName: NotRequired[str]
    validationStatus: NotRequired[LoadBalancerTlsCertificateDomainStatusType]

class LoadBalancerTlsCertificateSummaryTypeDef(TypedDict):
    name: NotRequired[str]
    isAttached: NotRequired[bool]

class NameServersUpdateStateTypeDef(TypedDict):
    code: NotRequired[NameServersUpdateStateCodeType]
    message: NotRequired[str]

class PendingMaintenanceActionTypeDef(TypedDict):
    action: NotRequired[str]
    description: NotRequired[str]
    currentApplyDate: NotRequired[datetime]

class PendingModifiedRelationalDatabaseValuesTypeDef(TypedDict):
    masterUserPassword: NotRequired[str]
    engineVersion: NotRequired[str]
    backupRetentionEnabled: NotRequired[bool]

class PutAlarmRequestTypeDef(TypedDict):
    alarmName: str
    metricName: MetricNameType
    monitoredResourceName: str
    comparisonOperator: ComparisonOperatorType
    threshold: float
    evaluationPeriods: int
    datapointsToAlarm: NotRequired[int]
    treatMissingData: NotRequired[TreatMissingDataType]
    contactProtocols: NotRequired[Sequence[ContactProtocolType]]
    notificationTriggers: NotRequired[Sequence[AlarmStateType]]
    notificationEnabled: NotRequired[bool]

class R53HostedZoneDeletionStateTypeDef(TypedDict):
    code: NotRequired[R53HostedZoneDeletionStateCodeType]
    message: NotRequired[str]

class RebootInstanceRequestTypeDef(TypedDict):
    instanceName: str

class RebootRelationalDatabaseRequestTypeDef(TypedDict):
    relationalDatabaseName: str

class RegisterContainerImageRequestTypeDef(TypedDict):
    serviceName: str
    label: str
    digest: str

class RelationalDatabaseEndpointTypeDef(TypedDict):
    port: NotRequired[int]
    address: NotRequired[str]

class RelationalDatabaseHardwareTypeDef(TypedDict):
    cpuCount: NotRequired[int]
    diskSizeInGb: NotRequired[int]
    ramSizeInGb: NotRequired[float]

class ReleaseStaticIpRequestTypeDef(TypedDict):
    staticIpName: str

class ResetDistributionCacheRequestTypeDef(TypedDict):
    distributionName: NotRequired[str]

class SendContactMethodVerificationRequestTypeDef(TypedDict):
    protocol: Literal["Email"]

class SetIpAddressTypeRequestTypeDef(TypedDict):
    resourceType: ResourceTypeType
    resourceName: str
    ipAddressType: IpAddressTypeType
    acceptBundleUpdate: NotRequired[bool]

class SetResourceAccessForBucketRequestTypeDef(TypedDict):
    resourceName: str
    bucketName: str
    access: ResourceBucketAccessType

class SetupExecutionDetailsTypeDef(TypedDict):
    command: NotRequired[str]
    dateTime: NotRequired[datetime]
    name: NotRequired[str]
    status: NotRequired[SetupStatusType]
    standardError: NotRequired[str]
    standardOutput: NotRequired[str]
    version: NotRequired[str]

class SetupRequestTypeDef(TypedDict):
    instanceName: NotRequired[str]
    domainNames: NotRequired[list[str]]
    certificateProvider: NotRequired[Literal["LetsEncrypt"]]

class SetupInstanceHttpsRequestTypeDef(TypedDict):
    instanceName: str
    emailAddress: str
    domainNames: Sequence[str]
    certificateProvider: Literal["LetsEncrypt"]

class StartGUISessionRequestTypeDef(TypedDict):
    resourceName: str

class StartInstanceRequestTypeDef(TypedDict):
    instanceName: str

class StartRelationalDatabaseRequestTypeDef(TypedDict):
    relationalDatabaseName: str

class StopGUISessionRequestTypeDef(TypedDict):
    resourceName: str

class StopInstanceRequestTypeDef(TypedDict):
    instanceName: str
    force: NotRequired[bool]

class StopRelationalDatabaseRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    relationalDatabaseSnapshotName: NotRequired[str]

class TestAlarmRequestTypeDef(TypedDict):
    alarmName: str
    state: AlarmStateType

class UntagResourceRequestTypeDef(TypedDict):
    resourceName: str
    tagKeys: Sequence[str]
    resourceArn: NotRequired[str]

class UpdateBucketBundleRequestTypeDef(TypedDict):
    bucketName: str
    bundleId: str

class UpdateDistributionBundleRequestTypeDef(TypedDict):
    distributionName: NotRequired[str]
    bundleId: NotRequired[str]

class UpdateInstanceMetadataOptionsRequestTypeDef(TypedDict):
    instanceName: str
    httpTokens: NotRequired[HttpTokensType]
    httpEndpoint: NotRequired[HttpEndpointType]
    httpPutResponseHopLimit: NotRequired[int]
    httpProtocolIpv6: NotRequired[HttpProtocolIpv6Type]

class UpdateLoadBalancerAttributeRequestTypeDef(TypedDict):
    loadBalancerName: str
    attributeName: LoadBalancerAttributeNameType
    attributeValue: str

class UpdateRelationalDatabaseRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    masterUserPassword: NotRequired[str]
    rotateMasterUserPassword: NotRequired[bool]
    preferredBackupWindow: NotRequired[str]
    preferredMaintenanceWindow: NotRequired[str]
    enableBackupRetention: NotRequired[bool]
    disableBackupRetention: NotRequired[bool]
    publiclyAccessible: NotRequired[bool]
    applyImmediately: NotRequired[bool]
    caCertificateIdentifier: NotRequired[str]
    relationalDatabaseBlueprintId: NotRequired[str]

class AccessKeyTypeDef(TypedDict):
    accessKeyId: NotRequired[str]
    secretAccessKey: NotRequired[str]
    status: NotRequired[StatusTypeType]
    createdAt: NotRequired[datetime]
    lastUsed: NotRequired[AccessKeyLastUsedTypeDef]

class AddOnRequestTypeDef(TypedDict):
    addOnType: AddOnTypeType
    autoSnapshotAddOnRequest: NotRequired[AutoSnapshotAddOnRequestTypeDef]
    stopInstanceOnIdleRequest: NotRequired[StopInstanceOnIdleRequestTypeDef]

class AlarmTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    supportCode: NotRequired[str]
    monitoredResourceInfo: NotRequired[MonitoredResourceInfoTypeDef]
    comparisonOperator: NotRequired[ComparisonOperatorType]
    evaluationPeriods: NotRequired[int]
    period: NotRequired[int]
    threshold: NotRequired[float]
    datapointsToAlarm: NotRequired[int]
    treatMissingData: NotRequired[TreatMissingDataType]
    statistic: NotRequired[MetricStatisticType]
    metricName: NotRequired[MetricNameType]
    state: NotRequired[AlarmStateType]
    unit: NotRequired[MetricUnitType]
    contactProtocols: NotRequired[list[ContactProtocolType]]
    notificationTriggers: NotRequired[list[AlarmStateType]]
    notificationEnabled: NotRequired[bool]

class ContactMethodTypeDef(TypedDict):
    contactEndpoint: NotRequired[str]
    status: NotRequired[ContactMethodStatusType]
    protocol: NotRequired[ContactProtocolType]
    name: NotRequired[str]
    arn: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    supportCode: NotRequired[str]

OperationTypeDef = TypedDict(
    "OperationTypeDef",
    {
        "id": NotRequired[str],
        "resourceName": NotRequired[str],
        "resourceType": NotRequired[ResourceTypeType],
        "createdAt": NotRequired[datetime],
        "location": NotRequired[ResourceLocationTypeDef],
        "isTerminal": NotRequired[bool],
        "operationDetails": NotRequired[str],
        "operationType": NotRequired[OperationTypeType],
        "status": NotRequired[OperationStatusType],
        "statusChangedAt": NotRequired[datetime],
        "errorCode": NotRequired[str],
        "errorDetails": NotRequired[str],
    },
)

class SetupHistoryResourceTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]

class StaticIpTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    ipAddress: NotRequired[str]
    attachedTo: NotRequired[str]
    isAttached: NotRequired[bool]

class DownloadDefaultKeyPairResultTypeDef(TypedDict):
    publicKeyBase64: str
    privateKeyBase64: str
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetActiveNamesResultTypeDef(TypedDict):
    activeNames: list[str]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetContainerAPIMetadataResultTypeDef(TypedDict):
    metadata: list[dict[str, str]]
    ResponseMetadata: ResponseMetadataTypeDef

class GetDistributionLatestCacheResetResultTypeDef(TypedDict):
    status: str
    createTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetRelationalDatabaseLogStreamsResultTypeDef(TypedDict):
    logStreams: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetRelationalDatabaseMasterUserPasswordResultTypeDef(TypedDict):
    masterUserPassword: str
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class IsVpcPeeredResultTypeDef(TypedDict):
    isPeered: bool
    ResponseMetadata: ResponseMetadataTypeDef

class AutoSnapshotDetailsTypeDef(TypedDict):
    date: NotRequired[str]
    createdAt: NotRequired[datetime]
    status: NotRequired[AutoSnapshotStatusType]
    fromAttachedDisks: NotRequired[list[AttachedDiskTypeDef]]

class RegionTypeDef(TypedDict):
    continentCode: NotRequired[str]
    description: NotRequired[str]
    displayName: NotRequired[str]
    name: NotRequired[RegionNameType]
    availabilityZones: NotRequired[list[AvailabilityZoneTypeDef]]
    relationalDatabaseAvailabilityZones: NotRequired[list[AvailabilityZoneTypeDef]]

class GetBlueprintsResultTypeDef(TypedDict):
    blueprints: list[BlueprintTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetBucketBundlesResultTypeDef(TypedDict):
    bundles: list[BucketBundleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BucketCorsConfigOutputTypeDef(TypedDict):
    rules: NotRequired[list[BucketCorsRuleOutputTypeDef]]

class BucketCorsConfigTypeDef(TypedDict):
    rules: NotRequired[Sequence[BucketCorsRuleTypeDef]]

class CreateBucketRequestTypeDef(TypedDict):
    bucketName: str
    bundleId: str
    tags: NotRequired[Sequence[TagTypeDef]]
    enableObjectVersioning: NotRequired[bool]

class CreateCertificateRequestTypeDef(TypedDict):
    certificateName: str
    domainName: str
    subjectAlternativeNames: NotRequired[Sequence[str]]
    tags: NotRequired[Sequence[TagTypeDef]]

class CreateDiskSnapshotRequestTypeDef(TypedDict):
    diskSnapshotName: str
    diskName: NotRequired[str]
    instanceName: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]

class CreateDomainRequestTypeDef(TypedDict):
    domainName: str
    tags: NotRequired[Sequence[TagTypeDef]]

class CreateInstanceSnapshotRequestTypeDef(TypedDict):
    instanceSnapshotName: str
    instanceName: str
    tags: NotRequired[Sequence[TagTypeDef]]

class CreateKeyPairRequestTypeDef(TypedDict):
    keyPairName: str
    tags: NotRequired[Sequence[TagTypeDef]]

class CreateLoadBalancerRequestTypeDef(TypedDict):
    loadBalancerName: str
    instancePort: int
    healthCheckPath: NotRequired[str]
    certificateName: NotRequired[str]
    certificateDomainName: NotRequired[str]
    certificateAlternativeNames: NotRequired[Sequence[str]]
    tags: NotRequired[Sequence[TagTypeDef]]
    ipAddressType: NotRequired[IpAddressTypeType]
    tlsPolicyName: NotRequired[str]

class CreateLoadBalancerTlsCertificateRequestTypeDef(TypedDict):
    loadBalancerName: str
    certificateName: str
    certificateDomainName: str
    certificateAlternativeNames: NotRequired[Sequence[str]]
    tags: NotRequired[Sequence[TagTypeDef]]

class CreateRelationalDatabaseRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    relationalDatabaseBlueprintId: str
    relationalDatabaseBundleId: str
    masterDatabaseName: str
    masterUsername: str
    availabilityZone: NotRequired[str]
    masterUserPassword: NotRequired[str]
    preferredBackupWindow: NotRequired[str]
    preferredMaintenanceWindow: NotRequired[str]
    publiclyAccessible: NotRequired[bool]
    tags: NotRequired[Sequence[TagTypeDef]]

class CreateRelationalDatabaseSnapshotRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    relationalDatabaseSnapshotName: str
    tags: NotRequired[Sequence[TagTypeDef]]

class DiskSnapshotTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[list[TagTypeDef]]
    sizeInGb: NotRequired[int]
    state: NotRequired[DiskSnapshotStateType]
    progress: NotRequired[str]
    fromDiskName: NotRequired[str]
    fromDiskArn: NotRequired[str]
    fromInstanceName: NotRequired[str]
    fromInstanceArn: NotRequired[str]
    isFromAutoSnapshot: NotRequired[bool]

class DiskTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[list[TagTypeDef]]
    addOns: NotRequired[list[AddOnTypeDef]]
    sizeInGb: NotRequired[int]
    isSystemDisk: NotRequired[bool]
    iops: NotRequired[int]
    path: NotRequired[str]
    state: NotRequired[DiskStateType]
    attachedTo: NotRequired[str]
    isAttached: NotRequired[bool]
    attachmentState: NotRequired[str]
    gbInUse: NotRequired[int]
    autoMountStatus: NotRequired[AutoMountStatusType]

class KeyPairTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[list[TagTypeDef]]
    fingerprint: NotRequired[str]

class RelationalDatabaseSnapshotTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[list[TagTypeDef]]
    engine: NotRequired[str]
    engineVersion: NotRequired[str]
    sizeInGb: NotRequired[int]
    state: NotRequired[str]
    fromRelationalDatabaseName: NotRequired[str]
    fromRelationalDatabaseArn: NotRequired[str]
    fromRelationalDatabaseBundleId: NotRequired[str]
    fromRelationalDatabaseBlueprintId: NotRequired[str]

class TagResourceRequestTypeDef(TypedDict):
    resourceName: str
    tags: Sequence[TagTypeDef]
    resourceArn: NotRequired[str]

class GetBundlesResultTypeDef(TypedDict):
    bundles: list[BundleTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class CacheSettingsOutputTypeDef(TypedDict):
    defaultTTL: NotRequired[int]
    minimumTTL: NotRequired[int]
    maximumTTL: NotRequired[int]
    allowedHTTPMethods: NotRequired[str]
    cachedHTTPMethods: NotRequired[str]
    forwardedCookies: NotRequired[CookieObjectOutputTypeDef]
    forwardedHeaders: NotRequired[HeaderObjectOutputTypeDef]
    forwardedQueryStrings: NotRequired[QueryStringObjectOutputTypeDef]

class CacheSettingsTypeDef(TypedDict):
    defaultTTL: NotRequired[int]
    minimumTTL: NotRequired[int]
    maximumTTL: NotRequired[int]
    allowedHTTPMethods: NotRequired[str]
    cachedHTTPMethods: NotRequired[str]
    forwardedCookies: NotRequired[CookieObjectTypeDef]
    forwardedHeaders: NotRequired[HeaderObjectTypeDef]
    forwardedQueryStrings: NotRequired[QueryStringObjectTypeDef]

class CloseInstancePublicPortsRequestTypeDef(TypedDict):
    portInfo: PortInfoTypeDef
    instanceName: str

class OpenInstancePublicPortsRequestTypeDef(TypedDict):
    portInfo: PortInfoTypeDef
    instanceName: str

class PutInstancePublicPortsRequestTypeDef(TypedDict):
    portInfos: Sequence[PortInfoTypeDef]
    instanceName: str

class CloudFormationStackRecordTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    state: NotRequired[RecordStateType]
    sourceInfo: NotRequired[list[CloudFormationStackRecordSourceInfoTypeDef]]
    destinationInfo: NotRequired[DestinationInfoTypeDef]

class GetContainerImagesResultTypeDef(TypedDict):
    containerImages: list[ContainerImageTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class RegisterContainerImageResultTypeDef(TypedDict):
    containerImage: ContainerImageTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PrivateRegistryAccessRequestTypeDef(TypedDict):
    ecrImagePullerRole: NotRequired[ContainerServiceECRImagePullerRoleRequestTypeDef]

class PrivateRegistryAccessTypeDef(TypedDict):
    ecrImagePullerRole: NotRequired[ContainerServiceECRImagePullerRoleTypeDef]

class ContainerServiceEndpointTypeDef(TypedDict):
    containerName: NotRequired[str]
    containerPort: NotRequired[int]
    healthCheck: NotRequired[ContainerServiceHealthCheckConfigTypeDef]

class EndpointRequestTypeDef(TypedDict):
    containerName: str
    containerPort: int
    healthCheck: NotRequired[ContainerServiceHealthCheckConfigTypeDef]

class GetContainerLogResultTypeDef(TypedDict):
    logEvents: list[ContainerServiceLogEventTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetContainerServicePowersResultTypeDef(TypedDict):
    powers: list[ContainerServicePowerTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateContainerServiceRegistryLoginResultTypeDef(TypedDict):
    registryLogin: ContainerServiceRegistryLoginTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

ContainerUnionTypeDef = Union[ContainerTypeDef, ContainerOutputTypeDef]

class CreateCloudFormationStackRequestTypeDef(TypedDict):
    instances: Sequence[InstanceEntryTypeDef]

class CreateGUISessionAccessDetailsResultTypeDef(TypedDict):
    resourceName: str
    status: StatusType
    percentageComplete: int
    failureReason: str
    sessions: list[SessionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRelationalDatabaseFromSnapshotRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    availabilityZone: NotRequired[str]
    publiclyAccessible: NotRequired[bool]
    relationalDatabaseSnapshotName: NotRequired[str]
    relationalDatabaseBundleId: NotRequired[str]
    sourceRelationalDatabaseName: NotRequired[str]
    restoreTime: NotRequired[TimestampTypeDef]
    useLatestRestorableTime: NotRequired[bool]
    tags: NotRequired[Sequence[TagTypeDef]]

class GetBucketMetricDataRequestTypeDef(TypedDict):
    bucketName: str
    metricName: BucketMetricNameType
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    period: int
    statistics: Sequence[MetricStatisticType]
    unit: MetricUnitType

class GetContainerLogRequestTypeDef(TypedDict):
    serviceName: str
    containerName: str
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]
    filterPattern: NotRequired[str]
    pageToken: NotRequired[str]

class GetContainerServiceMetricDataRequestTypeDef(TypedDict):
    serviceName: str
    metricName: ContainerServiceMetricNameType
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    period: int
    statistics: Sequence[MetricStatisticType]

class GetCostEstimateRequestTypeDef(TypedDict):
    resourceName: str
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef

class GetDistributionMetricDataRequestTypeDef(TypedDict):
    distributionName: str
    metricName: DistributionMetricNameType
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    period: int
    unit: MetricUnitType
    statistics: Sequence[MetricStatisticType]

class GetInstanceMetricDataRequestTypeDef(TypedDict):
    instanceName: str
    metricName: InstanceMetricNameType
    period: int
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    unit: MetricUnitType
    statistics: Sequence[MetricStatisticType]

class GetLoadBalancerMetricDataRequestTypeDef(TypedDict):
    loadBalancerName: str
    metricName: LoadBalancerMetricNameType
    period: int
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    unit: MetricUnitType
    statistics: Sequence[MetricStatisticType]

class GetRelationalDatabaseLogEventsRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    logStreamName: str
    startTime: NotRequired[TimestampTypeDef]
    endTime: NotRequired[TimestampTypeDef]
    startFromHead: NotRequired[bool]
    pageToken: NotRequired[str]

class GetRelationalDatabaseMetricDataRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    metricName: RelationalDatabaseMetricNameType
    period: int
    startTime: TimestampTypeDef
    endTime: TimestampTypeDef
    unit: MetricUnitType
    statistics: Sequence[MetricStatisticType]

class InstanceSnapshotInfoTypeDef(TypedDict):
    fromBundleId: NotRequired[str]
    fromBlueprintId: NotRequired[str]
    fromDiskInfo: NotRequired[list[DiskInfoTypeDef]]

class GetDistributionBundlesResultTypeDef(TypedDict):
    bundles: list[DistributionBundleTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

DomainEntryUnionTypeDef = Union[DomainEntryTypeDef, DomainEntryOutputTypeDef]

class DomainValidationRecordTypeDef(TypedDict):
    domainName: NotRequired[str]
    resourceRecord: NotRequired[ResourceRecordTypeDef]
    dnsRecordCreationState: NotRequired[DnsRecordCreationStateTypeDef]
    validationStatus: NotRequired[CertificateDomainValidationStatusType]

class EstimateByTimeTypeDef(TypedDict):
    usageCost: NotRequired[float]
    pricingUnit: NotRequired[PricingUnitType]
    unit: NotRequired[float]
    currency: NotRequired[Literal["USD"]]
    timePeriod: NotRequired[TimePeriodTypeDef]

class GetActiveNamesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetBlueprintsRequestPaginateTypeDef(TypedDict):
    includeInactive: NotRequired[bool]
    appCategory: NotRequired[Literal["LfR"]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetBundlesRequestPaginateTypeDef(TypedDict):
    includeInactive: NotRequired[bool]
    appCategory: NotRequired[Literal["LfR"]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetCloudFormationStackRecordsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetDiskSnapshotsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetDisksRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetDomainsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetExportSnapshotRecordsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetInstanceSnapshotsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetInstancesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetKeyPairsRequestPaginateTypeDef(TypedDict):
    includeDefaultKeyPair: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetLoadBalancersRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetOperationsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetRelationalDatabaseBlueprintsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetRelationalDatabaseBundlesRequestPaginateTypeDef(TypedDict):
    includeInactive: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetRelationalDatabaseEventsRequestPaginateTypeDef(TypedDict):
    relationalDatabaseName: str
    durationInMinutes: NotRequired[int]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetRelationalDatabaseParametersRequestPaginateTypeDef(TypedDict):
    relationalDatabaseName: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetRelationalDatabaseSnapshotsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetRelationalDatabasesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetStaticIpsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class GetBucketMetricDataResultTypeDef(TypedDict):
    metricName: BucketMetricNameType
    metricData: list[MetricDatapointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetContainerServiceMetricDataResultTypeDef(TypedDict):
    metricName: ContainerServiceMetricNameType
    metricData: list[MetricDatapointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetDistributionMetricDataResultTypeDef(TypedDict):
    metricName: DistributionMetricNameType
    metricData: list[MetricDatapointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetInstanceMetricDataResultTypeDef(TypedDict):
    metricName: InstanceMetricNameType
    metricData: list[MetricDatapointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetLoadBalancerMetricDataResultTypeDef(TypedDict):
    metricName: LoadBalancerMetricNameType
    metricData: list[MetricDatapointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetRelationalDatabaseMetricDataResultTypeDef(TypedDict):
    metricName: RelationalDatabaseMetricNameType
    metricData: list[MetricDatapointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetInstancePortStatesResultTypeDef(TypedDict):
    portStates: list[InstancePortStateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetInstanceStateResultTypeDef(TypedDict):
    state: InstanceStateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetLoadBalancerTlsPoliciesResultTypeDef(TypedDict):
    tlsPolicies: list[LoadBalancerTlsPolicyTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetRelationalDatabaseBlueprintsResultTypeDef(TypedDict):
    blueprints: list[RelationalDatabaseBlueprintTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetRelationalDatabaseBundlesResultTypeDef(TypedDict):
    bundles: list[RelationalDatabaseBundleTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetRelationalDatabaseEventsResultTypeDef(TypedDict):
    relationalDatabaseEvents: list[RelationalDatabaseEventTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetRelationalDatabaseLogEventsResultTypeDef(TypedDict):
    resourceLogEvents: list[LogEventTypeDef]
    nextBackwardToken: str
    nextForwardToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetRelationalDatabaseParametersResultTypeDef(TypedDict):
    parameters: list[RelationalDatabaseParameterTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRelationalDatabaseParametersRequestTypeDef(TypedDict):
    relationalDatabaseName: str
    parameters: Sequence[RelationalDatabaseParameterTypeDef]

class InstanceAccessDetailsTypeDef(TypedDict):
    certKey: NotRequired[str]
    expiresAt: NotRequired[datetime]
    ipAddress: NotRequired[str]
    ipv6Addresses: NotRequired[list[str]]
    password: NotRequired[str]
    passwordData: NotRequired[PasswordDataTypeDef]
    privateKey: NotRequired[str]
    protocol: NotRequired[InstanceAccessProtocolType]
    instanceName: NotRequired[str]
    username: NotRequired[str]
    hostKeys: NotRequired[list[HostKeyAttributesTypeDef]]

class InstanceNetworkingTypeDef(TypedDict):
    monthlyTransfer: NotRequired[MonthlyTransferTypeDef]
    ports: NotRequired[list[InstancePortInfoTypeDef]]

LoadBalancerTlsCertificateDomainValidationRecordTypeDef = TypedDict(
    "LoadBalancerTlsCertificateDomainValidationRecordTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[str],
        "value": NotRequired[str],
        "validationStatus": NotRequired[LoadBalancerTlsCertificateDomainStatusType],
        "domainName": NotRequired[str],
        "dnsRecordCreationState": NotRequired[
            LoadBalancerTlsCertificateDnsRecordCreationStateTypeDef
        ],
    },
)

class LoadBalancerTlsCertificateRenewalSummaryTypeDef(TypedDict):
    renewalStatus: NotRequired[LoadBalancerTlsCertificateRenewalStatusType]
    domainValidationOptions: NotRequired[
        list[LoadBalancerTlsCertificateDomainValidationOptionTypeDef]
    ]

class LoadBalancerTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[list[TagTypeDef]]
    dnsName: NotRequired[str]
    state: NotRequired[LoadBalancerStateType]
    protocol: NotRequired[LoadBalancerProtocolType]
    publicPorts: NotRequired[list[int]]
    healthCheckPath: NotRequired[str]
    instancePort: NotRequired[int]
    instanceHealthSummary: NotRequired[list[InstanceHealthSummaryTypeDef]]
    tlsCertificateSummaries: NotRequired[list[LoadBalancerTlsCertificateSummaryTypeDef]]
    configurationOptions: NotRequired[dict[LoadBalancerAttributeNameType, str]]
    ipAddressType: NotRequired[IpAddressTypeType]
    httpsRedirectionEnabled: NotRequired[bool]
    tlsPolicyName: NotRequired[str]

class RegisteredDomainDelegationInfoTypeDef(TypedDict):
    nameServersUpdateState: NotRequired[NameServersUpdateStateTypeDef]
    r53HostedZoneDeletionState: NotRequired[R53HostedZoneDeletionStateTypeDef]

class RelationalDatabaseTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[list[TagTypeDef]]
    relationalDatabaseBlueprintId: NotRequired[str]
    relationalDatabaseBundleId: NotRequired[str]
    masterDatabaseName: NotRequired[str]
    hardware: NotRequired[RelationalDatabaseHardwareTypeDef]
    state: NotRequired[str]
    secondaryAvailabilityZone: NotRequired[str]
    backupRetentionEnabled: NotRequired[bool]
    pendingModifiedValues: NotRequired[PendingModifiedRelationalDatabaseValuesTypeDef]
    engine: NotRequired[str]
    engineVersion: NotRequired[str]
    latestRestorableTime: NotRequired[datetime]
    masterUsername: NotRequired[str]
    parameterApplyStatus: NotRequired[str]
    preferredBackupWindow: NotRequired[str]
    preferredMaintenanceWindow: NotRequired[str]
    publiclyAccessible: NotRequired[bool]
    masterEndpoint: NotRequired[RelationalDatabaseEndpointTypeDef]
    pendingMaintenanceActions: NotRequired[list[PendingMaintenanceActionTypeDef]]
    caCertificateIdentifier: NotRequired[str]

class GetBucketAccessKeysResultTypeDef(TypedDict):
    accessKeys: list[AccessKeyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDiskFromSnapshotRequestTypeDef(TypedDict):
    diskName: str
    availabilityZone: str
    sizeInGb: int
    diskSnapshotName: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    addOns: NotRequired[Sequence[AddOnRequestTypeDef]]
    sourceDiskName: NotRequired[str]
    restoreDate: NotRequired[str]
    useLatestRestorableAutoSnapshot: NotRequired[bool]

class CreateDiskRequestTypeDef(TypedDict):
    diskName: str
    availabilityZone: str
    sizeInGb: int
    tags: NotRequired[Sequence[TagTypeDef]]
    addOns: NotRequired[Sequence[AddOnRequestTypeDef]]

class CreateInstancesFromSnapshotRequestTypeDef(TypedDict):
    instanceNames: Sequence[str]
    availabilityZone: str
    bundleId: str
    attachedDiskMapping: NotRequired[Mapping[str, Sequence[DiskMapTypeDef]]]
    instanceSnapshotName: NotRequired[str]
    userData: NotRequired[str]
    keyPairName: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    addOns: NotRequired[Sequence[AddOnRequestTypeDef]]
    ipAddressType: NotRequired[IpAddressTypeType]
    sourceInstanceName: NotRequired[str]
    restoreDate: NotRequired[str]
    useLatestRestorableAutoSnapshot: NotRequired[bool]

class CreateInstancesRequestTypeDef(TypedDict):
    instanceNames: Sequence[str]
    availabilityZone: str
    blueprintId: str
    bundleId: str
    customImageName: NotRequired[str]
    userData: NotRequired[str]
    keyPairName: NotRequired[str]
    tags: NotRequired[Sequence[TagTypeDef]]
    addOns: NotRequired[Sequence[AddOnRequestTypeDef]]
    ipAddressType: NotRequired[IpAddressTypeType]

class EnableAddOnRequestTypeDef(TypedDict):
    resourceName: str
    addOnRequest: AddOnRequestTypeDef

class GetAlarmsResultTypeDef(TypedDict):
    alarms: list[AlarmTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetContactMethodsResultTypeDef(TypedDict):
    contactMethods: list[ContactMethodTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class AllocateStaticIpResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class AttachCertificateToDistributionResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class AttachDiskResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class AttachInstancesToLoadBalancerResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class AttachLoadBalancerTlsCertificateResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class AttachStaticIpResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CloseInstancePublicPortsResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CopySnapshotResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateBucketAccessKeyResultTypeDef(TypedDict):
    accessKey: AccessKeyTypeDef
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCloudFormationStackResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateContactMethodResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDiskFromSnapshotResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDiskResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDiskSnapshotResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDomainEntryResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDomainResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateInstanceSnapshotResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateInstancesFromSnapshotResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateInstancesResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateLoadBalancerResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateLoadBalancerTlsCertificateResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRelationalDatabaseFromSnapshotResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRelationalDatabaseResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRelationalDatabaseSnapshotResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAlarmResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAutoSnapshotResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteBucketAccessKeyResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteBucketResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteCertificateResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteContactMethodResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDiskResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDiskSnapshotResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDistributionResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDomainEntryResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteDomainResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteInstanceResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteInstanceSnapshotResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteKeyPairResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteKnownHostKeysResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteLoadBalancerResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteLoadBalancerTlsCertificateResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteRelationalDatabaseResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteRelationalDatabaseSnapshotResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DetachCertificateFromDistributionResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DetachDiskResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DetachInstancesFromLoadBalancerResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DetachStaticIpResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class DisableAddOnResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class EnableAddOnResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ExportSnapshotResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetOperationResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetOperationsForResourceResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    nextPageCount: str
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetOperationsResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ImportKeyPairResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class OpenInstancePublicPortsResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PeerVpcResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class PutAlarmResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class PutInstancePublicPortsResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class RebootInstanceResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class RebootRelationalDatabaseResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ReleaseStaticIpResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class ResetDistributionCacheResultTypeDef(TypedDict):
    status: str
    createTime: datetime
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class SendContactMethodVerificationResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class SetIpAddressTypeResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class SetResourceAccessForBucketResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class SetupInstanceHttpsResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class StartGUISessionResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class StartInstanceResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class StartRelationalDatabaseResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class StopGUISessionResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class StopInstanceResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class StopRelationalDatabaseResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TestAlarmResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UnpeerVpcResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UntagResourceResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateBucketBundleResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateDistributionBundleResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateDistributionResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateDomainEntryResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateInstanceMetadataOptionsResultTypeDef(TypedDict):
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateLoadBalancerAttributeResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRelationalDatabaseParametersResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRelationalDatabaseResultTypeDef(TypedDict):
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class SetupHistoryTypeDef(TypedDict):
    operationId: NotRequired[str]
    request: NotRequired[SetupRequestTypeDef]
    resource: NotRequired[SetupHistoryResourceTypeDef]
    executionDetails: NotRequired[list[SetupExecutionDetailsTypeDef]]
    status: NotRequired[SetupStatusType]

class GetStaticIpResultTypeDef(TypedDict):
    staticIp: StaticIpTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetStaticIpsResultTypeDef(TypedDict):
    staticIps: list[StaticIpTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetAutoSnapshotsResultTypeDef(TypedDict):
    resourceName: str
    resourceType: ResourceTypeType
    autoSnapshots: list[AutoSnapshotDetailsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetRegionsResultTypeDef(TypedDict):
    regions: list[RegionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class BucketTypeDef(TypedDict):
    resourceType: NotRequired[str]
    accessRules: NotRequired[AccessRulesTypeDef]
    arn: NotRequired[str]
    bundleId: NotRequired[str]
    createdAt: NotRequired[datetime]
    url: NotRequired[str]
    location: NotRequired[ResourceLocationTypeDef]
    name: NotRequired[str]
    supportCode: NotRequired[str]
    tags: NotRequired[list[TagTypeDef]]
    objectVersioning: NotRequired[str]
    ableToUpdateBundle: NotRequired[bool]
    readonlyAccessAccounts: NotRequired[list[str]]
    resourcesReceivingAccess: NotRequired[list[ResourceReceivingAccessTypeDef]]
    state: NotRequired[BucketStateTypeDef]
    accessLogConfig: NotRequired[BucketAccessLogConfigTypeDef]
    cors: NotRequired[BucketCorsConfigOutputTypeDef]

BucketCorsConfigUnionTypeDef = Union[BucketCorsConfigTypeDef, BucketCorsConfigOutputTypeDef]

class GetDiskSnapshotResultTypeDef(TypedDict):
    diskSnapshot: DiskSnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetDiskSnapshotsResultTypeDef(TypedDict):
    diskSnapshots: list[DiskSnapshotTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetDiskResultTypeDef(TypedDict):
    disk: DiskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetDisksResultTypeDef(TypedDict):
    disks: list[DiskTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class InstanceHardwareTypeDef(TypedDict):
    cpuCount: NotRequired[int]
    disks: NotRequired[list[DiskTypeDef]]
    ramSizeInGb: NotRequired[float]

class InstanceSnapshotTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[list[TagTypeDef]]
    state: NotRequired[InstanceSnapshotStateType]
    progress: NotRequired[str]
    fromAttachedDisks: NotRequired[list[DiskTypeDef]]
    fromInstanceName: NotRequired[str]
    fromInstanceArn: NotRequired[str]
    fromBlueprintId: NotRequired[str]
    fromBundleId: NotRequired[str]
    isFromAutoSnapshot: NotRequired[bool]
    sizeInGb: NotRequired[int]

class CreateKeyPairResultTypeDef(TypedDict):
    keyPair: KeyPairTypeDef
    publicKeyBase64: str
    privateKeyBase64: str
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetKeyPairResultTypeDef(TypedDict):
    keyPair: KeyPairTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetKeyPairsResultTypeDef(TypedDict):
    keyPairs: list[KeyPairTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetRelationalDatabaseSnapshotResultTypeDef(TypedDict):
    relationalDatabaseSnapshot: RelationalDatabaseSnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetRelationalDatabaseSnapshotsResultTypeDef(TypedDict):
    relationalDatabaseSnapshots: list[RelationalDatabaseSnapshotTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class LightsailDistributionTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    alternativeDomainNames: NotRequired[list[str]]
    status: NotRequired[str]
    isEnabled: NotRequired[bool]
    domainName: NotRequired[str]
    bundleId: NotRequired[str]
    certificateName: NotRequired[str]
    origin: NotRequired[OriginTypeDef]
    originPublicDNS: NotRequired[str]
    defaultCacheBehavior: NotRequired[CacheBehaviorTypeDef]
    cacheBehaviorSettings: NotRequired[CacheSettingsOutputTypeDef]
    cacheBehaviors: NotRequired[list[CacheBehaviorPerPathTypeDef]]
    ableToUpdateBundle: NotRequired[bool]
    ipAddressType: NotRequired[IpAddressTypeType]
    tags: NotRequired[list[TagTypeDef]]
    viewerMinimumTlsProtocolVersion: NotRequired[str]

CacheSettingsUnionTypeDef = Union[CacheSettingsTypeDef, CacheSettingsOutputTypeDef]

class GetCloudFormationStackRecordsResultTypeDef(TypedDict):
    cloudFormationStackRecords: list[CloudFormationStackRecordTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateContainerServiceRequestTypeDef(TypedDict):
    serviceName: str
    power: NotRequired[ContainerServicePowerNameType]
    scale: NotRequired[int]
    isDisabled: NotRequired[bool]
    publicDomainNames: NotRequired[Mapping[str, Sequence[str]]]
    privateRegistryAccess: NotRequired[PrivateRegistryAccessRequestTypeDef]

class ContainerServiceDeploymentTypeDef(TypedDict):
    version: NotRequired[int]
    state: NotRequired[ContainerServiceDeploymentStateType]
    containers: NotRequired[dict[str, ContainerOutputTypeDef]]
    publicEndpoint: NotRequired[ContainerServiceEndpointTypeDef]
    createdAt: NotRequired[datetime]

class ContainerServiceDeploymentRequestTypeDef(TypedDict):
    containers: NotRequired[Mapping[str, ContainerUnionTypeDef]]
    publicEndpoint: NotRequired[EndpointRequestTypeDef]

class CreateContainerServiceDeploymentRequestTypeDef(TypedDict):
    serviceName: str
    containers: NotRequired[Mapping[str, ContainerUnionTypeDef]]
    publicEndpoint: NotRequired[EndpointRequestTypeDef]

class ExportSnapshotRecordSourceInfoTypeDef(TypedDict):
    resourceType: NotRequired[ExportSnapshotRecordSourceTypeType]
    createdAt: NotRequired[datetime]
    name: NotRequired[str]
    arn: NotRequired[str]
    fromResourceName: NotRequired[str]
    fromResourceArn: NotRequired[str]
    instanceSnapshotInfo: NotRequired[InstanceSnapshotInfoTypeDef]
    diskSnapshotInfo: NotRequired[DiskSnapshotInfoTypeDef]

class CreateDomainEntryRequestTypeDef(TypedDict):
    domainName: str
    domainEntry: DomainEntryUnionTypeDef

class DeleteDomainEntryRequestTypeDef(TypedDict):
    domainName: str
    domainEntry: DomainEntryUnionTypeDef

class UpdateDomainEntryRequestTypeDef(TypedDict):
    domainName: str
    domainEntry: DomainEntryUnionTypeDef

class RenewalSummaryTypeDef(TypedDict):
    domainValidationRecords: NotRequired[list[DomainValidationRecordTypeDef]]
    renewalStatus: NotRequired[RenewalStatusType]
    renewalStatusReason: NotRequired[str]
    updatedAt: NotRequired[datetime]

class CostEstimateTypeDef(TypedDict):
    usageType: NotRequired[str]
    resultsByTime: NotRequired[list[EstimateByTimeTypeDef]]

class GetInstanceAccessDetailsResultTypeDef(TypedDict):
    accessDetails: InstanceAccessDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class LoadBalancerTlsCertificateTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[list[TagTypeDef]]
    loadBalancerName: NotRequired[str]
    isAttached: NotRequired[bool]
    status: NotRequired[LoadBalancerTlsCertificateStatusType]
    domainName: NotRequired[str]
    domainValidationRecords: NotRequired[
        list[LoadBalancerTlsCertificateDomainValidationRecordTypeDef]
    ]
    failureReason: NotRequired[LoadBalancerTlsCertificateFailureReasonType]
    issuedAt: NotRequired[datetime]
    issuer: NotRequired[str]
    keyAlgorithm: NotRequired[str]
    notAfter: NotRequired[datetime]
    notBefore: NotRequired[datetime]
    renewalSummary: NotRequired[LoadBalancerTlsCertificateRenewalSummaryTypeDef]
    revocationReason: NotRequired[LoadBalancerTlsCertificateRevocationReasonType]
    revokedAt: NotRequired[datetime]
    serial: NotRequired[str]
    signatureAlgorithm: NotRequired[str]
    subject: NotRequired[str]
    subjectAlternativeNames: NotRequired[list[str]]

class GetLoadBalancerResultTypeDef(TypedDict):
    loadBalancer: LoadBalancerTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetLoadBalancersResultTypeDef(TypedDict):
    loadBalancers: list[LoadBalancerTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class DomainTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[list[TagTypeDef]]
    domainEntries: NotRequired[list[DomainEntryOutputTypeDef]]
    registeredDomainDelegationInfo: NotRequired[RegisteredDomainDelegationInfoTypeDef]

class GetRelationalDatabaseResultTypeDef(TypedDict):
    relationalDatabase: RelationalDatabaseTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetRelationalDatabasesResultTypeDef(TypedDict):
    relationalDatabases: list[RelationalDatabaseTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetSetupHistoryResultTypeDef(TypedDict):
    setupHistory: list[SetupHistoryTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateBucketResultTypeDef(TypedDict):
    bucket: BucketTypeDef
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetBucketsResultTypeDef(TypedDict):
    buckets: list[BucketTypeDef]
    nextPageToken: str
    accountLevelBpaSync: AccountLevelBpaSyncTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateBucketResultTypeDef(TypedDict):
    bucket: BucketTypeDef
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateBucketRequestTypeDef(TypedDict):
    bucketName: str
    accessRules: NotRequired[AccessRulesTypeDef]
    versioning: NotRequired[str]
    readonlyAccessAccounts: NotRequired[Sequence[str]]
    accessLogConfig: NotRequired[BucketAccessLogConfigTypeDef]
    cors: NotRequired[BucketCorsConfigUnionTypeDef]

class InstanceTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    supportCode: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[list[TagTypeDef]]
    blueprintId: NotRequired[str]
    blueprintName: NotRequired[str]
    bundleId: NotRequired[str]
    addOns: NotRequired[list[AddOnTypeDef]]
    isStaticIp: NotRequired[bool]
    privateIpAddress: NotRequired[str]
    publicIpAddress: NotRequired[str]
    ipv6Addresses: NotRequired[list[str]]
    ipAddressType: NotRequired[IpAddressTypeType]
    hardware: NotRequired[InstanceHardwareTypeDef]
    networking: NotRequired[InstanceNetworkingTypeDef]
    state: NotRequired[InstanceStateTypeDef]
    username: NotRequired[str]
    sshKeyName: NotRequired[str]
    metadataOptions: NotRequired[InstanceMetadataOptionsTypeDef]

class GetInstanceSnapshotResultTypeDef(TypedDict):
    instanceSnapshot: InstanceSnapshotTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetInstanceSnapshotsResultTypeDef(TypedDict):
    instanceSnapshots: list[InstanceSnapshotTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDistributionResultTypeDef(TypedDict):
    distribution: LightsailDistributionTypeDef
    operation: OperationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetDistributionsResultTypeDef(TypedDict):
    distributions: list[LightsailDistributionTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateDistributionRequestTypeDef(TypedDict):
    distributionName: str
    origin: InputOriginTypeDef
    defaultCacheBehavior: CacheBehaviorTypeDef
    bundleId: str
    cacheBehaviorSettings: NotRequired[CacheSettingsUnionTypeDef]
    cacheBehaviors: NotRequired[Sequence[CacheBehaviorPerPathTypeDef]]
    ipAddressType: NotRequired[IpAddressTypeType]
    tags: NotRequired[Sequence[TagTypeDef]]
    certificateName: NotRequired[str]
    viewerMinimumTlsProtocolVersion: NotRequired[ViewerMinimumTlsProtocolVersionEnumType]

class UpdateDistributionRequestTypeDef(TypedDict):
    distributionName: str
    origin: NotRequired[InputOriginTypeDef]
    defaultCacheBehavior: NotRequired[CacheBehaviorTypeDef]
    cacheBehaviorSettings: NotRequired[CacheSettingsUnionTypeDef]
    cacheBehaviors: NotRequired[Sequence[CacheBehaviorPerPathTypeDef]]
    isEnabled: NotRequired[bool]
    viewerMinimumTlsProtocolVersion: NotRequired[ViewerMinimumTlsProtocolVersionEnumType]
    certificateName: NotRequired[str]
    useDefaultCertificate: NotRequired[bool]

class ContainerServiceTypeDef(TypedDict):
    containerServiceName: NotRequired[str]
    arn: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    tags: NotRequired[list[TagTypeDef]]
    power: NotRequired[ContainerServicePowerNameType]
    powerId: NotRequired[str]
    state: NotRequired[ContainerServiceStateType]
    stateDetail: NotRequired[ContainerServiceStateDetailTypeDef]
    scale: NotRequired[int]
    currentDeployment: NotRequired[ContainerServiceDeploymentTypeDef]
    nextDeployment: NotRequired[ContainerServiceDeploymentTypeDef]
    isDisabled: NotRequired[bool]
    principalArn: NotRequired[str]
    privateDomainName: NotRequired[str]
    publicDomainNames: NotRequired[dict[str, list[str]]]
    url: NotRequired[str]
    privateRegistryAccess: NotRequired[PrivateRegistryAccessTypeDef]

class GetContainerServiceDeploymentsResultTypeDef(TypedDict):
    deployments: list[ContainerServiceDeploymentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateContainerServiceRequestTypeDef(TypedDict):
    serviceName: str
    power: ContainerServicePowerNameType
    scale: int
    tags: NotRequired[Sequence[TagTypeDef]]
    publicDomainNames: NotRequired[Mapping[str, Sequence[str]]]
    deployment: NotRequired[ContainerServiceDeploymentRequestTypeDef]
    privateRegistryAccess: NotRequired[PrivateRegistryAccessRequestTypeDef]

class ExportSnapshotRecordTypeDef(TypedDict):
    name: NotRequired[str]
    arn: NotRequired[str]
    createdAt: NotRequired[datetime]
    location: NotRequired[ResourceLocationTypeDef]
    resourceType: NotRequired[ResourceTypeType]
    state: NotRequired[RecordStateType]
    sourceInfo: NotRequired[ExportSnapshotRecordSourceInfoTypeDef]
    destinationInfo: NotRequired[DestinationInfoTypeDef]

class CertificateTypeDef(TypedDict):
    arn: NotRequired[str]
    name: NotRequired[str]
    domainName: NotRequired[str]
    status: NotRequired[CertificateStatusType]
    serialNumber: NotRequired[str]
    subjectAlternativeNames: NotRequired[list[str]]
    domainValidationRecords: NotRequired[list[DomainValidationRecordTypeDef]]
    requestFailureReason: NotRequired[str]
    inUseResourceCount: NotRequired[int]
    keyAlgorithm: NotRequired[str]
    createdAt: NotRequired[datetime]
    issuedAt: NotRequired[datetime]
    issuerCA: NotRequired[str]
    notBefore: NotRequired[datetime]
    notAfter: NotRequired[datetime]
    eligibleToRenew: NotRequired[str]
    renewalSummary: NotRequired[RenewalSummaryTypeDef]
    revokedAt: NotRequired[datetime]
    revocationReason: NotRequired[str]
    tags: NotRequired[list[TagTypeDef]]
    supportCode: NotRequired[str]

class ResourceBudgetEstimateTypeDef(TypedDict):
    resourceName: NotRequired[str]
    resourceType: NotRequired[ResourceTypeType]
    costEstimates: NotRequired[list[CostEstimateTypeDef]]
    startTime: NotRequired[datetime]
    endTime: NotRequired[datetime]

class GetLoadBalancerTlsCertificatesResultTypeDef(TypedDict):
    tlsCertificates: list[LoadBalancerTlsCertificateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetDomainResultTypeDef(TypedDict):
    domain: DomainTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetDomainsResultTypeDef(TypedDict):
    domains: list[DomainTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetInstanceResultTypeDef(TypedDict):
    instance: InstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetInstancesResultTypeDef(TypedDict):
    instances: list[InstanceTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class ContainerServicesListResultTypeDef(TypedDict):
    containerServices: list[ContainerServiceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateContainerServiceDeploymentResultTypeDef(TypedDict):
    containerService: ContainerServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateContainerServiceResultTypeDef(TypedDict):
    containerService: ContainerServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateContainerServiceResultTypeDef(TypedDict):
    containerService: ContainerServiceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetExportSnapshotRecordsResultTypeDef(TypedDict):
    exportSnapshotRecords: list[ExportSnapshotRecordTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef

class CertificateSummaryTypeDef(TypedDict):
    certificateArn: NotRequired[str]
    certificateName: NotRequired[str]
    domainName: NotRequired[str]
    certificateDetail: NotRequired[CertificateTypeDef]
    tags: NotRequired[list[TagTypeDef]]

class GetCostEstimateResultTypeDef(TypedDict):
    resourcesBudgetEstimate: list[ResourceBudgetEstimateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCertificateResultTypeDef(TypedDict):
    certificate: CertificateSummaryTypeDef
    operations: list[OperationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetCertificatesResultTypeDef(TypedDict):
    certificates: list[CertificateSummaryTypeDef]
    nextPageToken: str
    ResponseMetadata: ResponseMetadataTypeDef
