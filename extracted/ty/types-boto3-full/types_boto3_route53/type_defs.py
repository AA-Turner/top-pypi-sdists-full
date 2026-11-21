"""
Type annotations for route53 service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_route53/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_route53.type_defs import AZAffinityTypeDef

    data: AZAffinityTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from datetime import datetime
from typing import Union

from .literals import (
    AcceleratedRecoveryStatusType,
    AccountLimitTypeType,
    AZAffinityLocationTypeType,
    ChangeActionType,
    ChangeGuardrailNameType,
    ChangeGuardrailStatusType,
    ChangeHistoryOperationType,
    ChangeHistorySortOrderType,
    ChangeStatusType,
    CidrCollectionChangeActionType,
    CloudWatchRegionType,
    ComparisonOperatorType,
    EndpointTypeType,
    FeatureEnablementType,
    FeatureStatusType,
    HealthCheckRegionType,
    HealthCheckSourceStatusReasonCodeType,
    HealthCheckSourceStatusType,
    HealthCheckTypeType,
    HostedZoneLimitTypeType,
    HostedZoneTierType,
    InsufficientDataHealthStatusType,
    ResettableElementNameType,
    ResourceRecordSetFailoverType,
    ResourceRecordSetRegionType,
    RRTypeType,
    StatisticType,
    TagResourceTypeType,
    VPCRegionType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AZAffinityTypeDef",
    "AccountLimitTypeDef",
    "ActivateKeySigningKeyRequestTypeDef",
    "ActivateKeySigningKeyResponseTypeDef",
    "AlarmIdentifierTypeDef",
    "AliasTargetTypeDef",
    "AssociateVPCWithHostedZoneRequestTypeDef",
    "AssociateVPCWithHostedZoneResponseTypeDef",
    "ChangeBatchOutputTypeDef",
    "ChangeBatchSummaryTypeDef",
    "ChangeBatchTypeDef",
    "ChangeBatchUnionTypeDef",
    "ChangeCidrCollectionRequestTypeDef",
    "ChangeCidrCollectionResponseTypeDef",
    "ChangeGuardrailTypeDef",
    "ChangeHistoryFeatureTypeDef",
    "ChangeInfoTypeDef",
    "ChangeOutputTypeDef",
    "ChangeResourceRecordSetsRequestTypeDef",
    "ChangeResourceRecordSetsResponseTypeDef",
    "ChangeTagsForResourceRequestTypeDef",
    "ChangeTypeDef",
    "CidrBlockSummaryTypeDef",
    "CidrCollectionChangeTypeDef",
    "CidrCollectionTypeDef",
    "CidrRoutingConfigTypeDef",
    "CloudWatchAlarmConfigurationTypeDef",
    "CollectionSummaryTypeDef",
    "CoordinatesTypeDef",
    "CreateCidrCollectionRequestTypeDef",
    "CreateCidrCollectionResponseTypeDef",
    "CreateHealthCheckRequestTypeDef",
    "CreateHealthCheckResponseTypeDef",
    "CreateHealthCheckSourceRequestTypeDef",
    "CreateHealthCheckSourceResponseTypeDef",
    "CreateHostedZoneRequestTypeDef",
    "CreateHostedZoneResponseTypeDef",
    "CreateKeySigningKeyRequestTypeDef",
    "CreateKeySigningKeyResponseTypeDef",
    "CreateQueryLoggingConfigRequestTypeDef",
    "CreateQueryLoggingConfigResponseTypeDef",
    "CreateResourceRecordSetProtectionsRequestTypeDef",
    "CreateReusableDelegationSetRequestTypeDef",
    "CreateReusableDelegationSetResponseTypeDef",
    "CreateTrafficPolicyInstanceRequestTypeDef",
    "CreateTrafficPolicyInstanceResponseTypeDef",
    "CreateTrafficPolicyRequestTypeDef",
    "CreateTrafficPolicyResponseTypeDef",
    "CreateTrafficPolicyVersionRequestTypeDef",
    "CreateTrafficPolicyVersionResponseTypeDef",
    "CreateVPCAssociationAuthorizationRequestTypeDef",
    "CreateVPCAssociationAuthorizationResponseTypeDef",
    "DNSSECStatusTypeDef",
    "DeactivateKeySigningKeyRequestTypeDef",
    "DeactivateKeySigningKeyResponseTypeDef",
    "DelegationSetTypeDef",
    "DeleteCidrCollectionRequestTypeDef",
    "DeleteHealthCheckRequestTypeDef",
    "DeleteHealthCheckSourceRequestTypeDef",
    "DeleteHealthCheckSourceResponseTypeDef",
    "DeleteHostedZoneRequestTypeDef",
    "DeleteHostedZoneResponseTypeDef",
    "DeleteKeySigningKeyRequestTypeDef",
    "DeleteKeySigningKeyResponseTypeDef",
    "DeleteQueryLoggingConfigRequestTypeDef",
    "DeleteResourceRecordSetProtectionsRequestTypeDef",
    "DeleteReusableDelegationSetRequestTypeDef",
    "DeleteTrafficPolicyInstanceRequestTypeDef",
    "DeleteTrafficPolicyRequestTypeDef",
    "DeleteVPCAssociationAuthorizationRequestTypeDef",
    "DimensionTypeDef",
    "DisableHostedZoneDNSSECRequestTypeDef",
    "DisableHostedZoneDNSSECResponseTypeDef",
    "DisassociateVPCFromHostedZoneRequestTypeDef",
    "DisassociateVPCFromHostedZoneResponseTypeDef",
    "EnableHostedZoneDNSSECRequestTypeDef",
    "EnableHostedZoneDNSSECResponseTypeDef",
    "GeoLocationDetailsTypeDef",
    "GeoLocationTypeDef",
    "GeoProximityLocationTypeDef",
    "GetAccountLimitRequestTypeDef",
    "GetAccountLimitResponseTypeDef",
    "GetChangeRequestTypeDef",
    "GetChangeRequestWaitTypeDef",
    "GetChangeResponseTypeDef",
    "GetCheckerIpRangesResponseTypeDef",
    "GetDNSSECRequestTypeDef",
    "GetDNSSECResponseTypeDef",
    "GetGeoLocationRequestTypeDef",
    "GetGeoLocationResponseTypeDef",
    "GetHealthCheckCountResponseTypeDef",
    "GetHealthCheckLastFailureReasonRequestTypeDef",
    "GetHealthCheckLastFailureReasonResponseTypeDef",
    "GetHealthCheckRequestTypeDef",
    "GetHealthCheckResponseTypeDef",
    "GetHealthCheckSourceRequestTypeDef",
    "GetHealthCheckSourceRequestWaitExtraTypeDef",
    "GetHealthCheckSourceRequestWaitTypeDef",
    "GetHealthCheckSourceResponseTypeDef",
    "GetHealthCheckStatusRequestTypeDef",
    "GetHealthCheckStatusResponseTypeDef",
    "GetHostedZoneChangeBatchRequestTypeDef",
    "GetHostedZoneChangeBatchResponseTypeDef",
    "GetHostedZoneCountResponseTypeDef",
    "GetHostedZoneLimitRequestTypeDef",
    "GetHostedZoneLimitResponseTypeDef",
    "GetHostedZoneRequestTypeDef",
    "GetHostedZoneResponseTypeDef",
    "GetQueryLoggingConfigRequestTypeDef",
    "GetQueryLoggingConfigResponseTypeDef",
    "GetReusableDelegationSetLimitRequestTypeDef",
    "GetReusableDelegationSetLimitResponseTypeDef",
    "GetReusableDelegationSetRequestTypeDef",
    "GetReusableDelegationSetResponseTypeDef",
    "GetTrafficPolicyInstanceCountResponseTypeDef",
    "GetTrafficPolicyInstanceRequestTypeDef",
    "GetTrafficPolicyInstanceResponseTypeDef",
    "GetTrafficPolicyRequestTypeDef",
    "GetTrafficPolicyResponseTypeDef",
    "HealthCheckConfigOutputTypeDef",
    "HealthCheckConfigTypeDef",
    "HealthCheckConfigUnionTypeDef",
    "HealthCheckObservationTypeDef",
    "HealthCheckSourceConfigOutputTypeDef",
    "HealthCheckSourceConfigTypeDef",
    "HealthCheckSourceConfigUnionTypeDef",
    "HealthCheckSourceTypeDef",
    "HealthCheckTypeDef",
    "HostedZoneConfigTypeDef",
    "HostedZoneFailureReasonsTypeDef",
    "HostedZoneFeaturesTypeDef",
    "HostedZoneLimitTypeDef",
    "HostedZoneOwnerTypeDef",
    "HostedZoneSummaryTypeDef",
    "HostedZoneTypeDef",
    "KeySigningKeyTypeDef",
    "LinkedServiceTypeDef",
    "ListCidrBlocksRequestPaginateTypeDef",
    "ListCidrBlocksRequestTypeDef",
    "ListCidrBlocksResponseTypeDef",
    "ListCidrCollectionsRequestPaginateTypeDef",
    "ListCidrCollectionsRequestTypeDef",
    "ListCidrCollectionsResponseTypeDef",
    "ListCidrLocationsRequestPaginateTypeDef",
    "ListCidrLocationsRequestTypeDef",
    "ListCidrLocationsResponseTypeDef",
    "ListGeoLocationsRequestTypeDef",
    "ListGeoLocationsResponseTypeDef",
    "ListHealthCheckSourcesRequestPaginateTypeDef",
    "ListHealthCheckSourcesRequestTypeDef",
    "ListHealthCheckSourcesResponseTypeDef",
    "ListHealthChecksBySourceRequestPaginateTypeDef",
    "ListHealthChecksBySourceRequestTypeDef",
    "ListHealthChecksBySourceResponseTypeDef",
    "ListHealthChecksRequestPaginateTypeDef",
    "ListHealthChecksRequestTypeDef",
    "ListHealthChecksResponseTypeDef",
    "ListHostedZoneChangeBatchesRequestPaginateTypeDef",
    "ListHostedZoneChangeBatchesRequestTypeDef",
    "ListHostedZoneChangeBatchesResponseTypeDef",
    "ListHostedZonesByNameRequestTypeDef",
    "ListHostedZonesByNameResponseTypeDef",
    "ListHostedZonesByVPCRequestTypeDef",
    "ListHostedZonesByVPCResponseTypeDef",
    "ListHostedZonesRequestPaginateTypeDef",
    "ListHostedZonesRequestTypeDef",
    "ListHostedZonesResponseTypeDef",
    "ListQueryLoggingConfigsRequestPaginateTypeDef",
    "ListQueryLoggingConfigsRequestTypeDef",
    "ListQueryLoggingConfigsResponseTypeDef",
    "ListResourceRecordSetChangesRequestPaginateTypeDef",
    "ListResourceRecordSetChangesRequestTypeDef",
    "ListResourceRecordSetChangesResponseTypeDef",
    "ListResourceRecordSetProtectionsRequestPaginateTypeDef",
    "ListResourceRecordSetProtectionsRequestTypeDef",
    "ListResourceRecordSetProtectionsResponseTypeDef",
    "ListResourceRecordSetsRequestPaginateTypeDef",
    "ListResourceRecordSetsRequestTypeDef",
    "ListResourceRecordSetsResponseTypeDef",
    "ListReusableDelegationSetsRequestTypeDef",
    "ListReusableDelegationSetsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTagsForResourcesRequestTypeDef",
    "ListTagsForResourcesResponseTypeDef",
    "ListTrafficPoliciesRequestTypeDef",
    "ListTrafficPoliciesResponseTypeDef",
    "ListTrafficPolicyInstancesByHostedZoneRequestTypeDef",
    "ListTrafficPolicyInstancesByHostedZoneResponseTypeDef",
    "ListTrafficPolicyInstancesByPolicyRequestTypeDef",
    "ListTrafficPolicyInstancesByPolicyResponseTypeDef",
    "ListTrafficPolicyInstancesRequestTypeDef",
    "ListTrafficPolicyInstancesResponseTypeDef",
    "ListTrafficPolicyVersionsRequestTypeDef",
    "ListTrafficPolicyVersionsResponseTypeDef",
    "ListVPCAssociationAuthorizationsRequestPaginateTypeDef",
    "ListVPCAssociationAuthorizationsRequestTypeDef",
    "ListVPCAssociationAuthorizationsResponseTypeDef",
    "LocationSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "QueryLoggingConfigTypeDef",
    "ResourceRecordSetChangeTypeDef",
    "ResourceRecordSetOutputTypeDef",
    "ResourceRecordSetProtectionConfigTypeDef",
    "ResourceRecordSetProtectionKeyTypeDef",
    "ResourceRecordSetProtectionTypeDef",
    "ResourceRecordSetTypeDef",
    "ResourceRecordTypeDef",
    "ResourceTagSetTypeDef",
    "ResponseMetadataTypeDef",
    "ReusableDelegationSetLimitTypeDef",
    "StatusReportTypeDef",
    "SubnetConfigurationOutputTypeDef",
    "SubnetConfigurationTypeDef",
    "TagTypeDef",
    "TestDNSAnswerRequestTypeDef",
    "TestDNSAnswerResponseTypeDef",
    "TrafficPolicyInstanceTypeDef",
    "TrafficPolicySummaryTypeDef",
    "TrafficPolicyTypeDef",
    "UpdateHealthCheckRequestTypeDef",
    "UpdateHealthCheckResponseTypeDef",
    "UpdateHostedZoneCommentRequestTypeDef",
    "UpdateHostedZoneCommentResponseTypeDef",
    "UpdateHostedZoneFeaturesRequestTypeDef",
    "UpdateHostedZoneTierRequestTypeDef",
    "UpdateTrafficPolicyCommentRequestTypeDef",
    "UpdateTrafficPolicyCommentResponseTypeDef",
    "UpdateTrafficPolicyInstanceRequestTypeDef",
    "UpdateTrafficPolicyInstanceResponseTypeDef",
    "VPCTypeDef",
    "WaiterConfigTypeDef",
)


class AZAffinityTypeDef(TypedDict):
    LocationType: NotRequired[AZAffinityLocationTypeType]
    LocationId: NotRequired[str]


AccountLimitTypeDef = TypedDict(
    "AccountLimitTypeDef",
    {
        "Type": AccountLimitTypeType,
        "Value": int,
    },
)


class ActivateKeySigningKeyRequestTypeDef(TypedDict):
    HostedZoneId: str
    Name: str


class ChangeInfoTypeDef(TypedDict):
    Id: str
    Status: ChangeStatusType
    SubmittedAt: datetime
    Comment: NotRequired[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AlarmIdentifierTypeDef(TypedDict):
    Region: CloudWatchRegionType
    Name: str


class AliasTargetTypeDef(TypedDict):
    HostedZoneId: str
    DNSName: str
    EvaluateTargetHealth: bool


class VPCTypeDef(TypedDict):
    VPCRegion: NotRequired[VPCRegionType]
    VPCId: NotRequired[str]


class ChangeBatchSummaryTypeDef(TypedDict):
    ChangeId: str
    Operation: ChangeHistoryOperationType
    SubmittedAt: datetime
    ChangeCount: int
    SubmittedBy: NotRequired[str]
    RequestId: NotRequired[str]
    Comment: NotRequired[str]


class CidrCollectionChangeTypeDef(TypedDict):
    LocationName: str
    Action: CidrCollectionChangeActionType
    CidrList: Sequence[str]


class ChangeGuardrailTypeDef(TypedDict):
    Name: ChangeGuardrailNameType
    Status: ChangeGuardrailStatusType


class ChangeHistoryFeatureTypeDef(TypedDict):
    Status: NotRequired[FeatureEnablementType]
    RetentionStartsAt: NotRequired[datetime]


class TagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class CidrBlockSummaryTypeDef(TypedDict):
    CidrBlock: NotRequired[str]
    LocationName: NotRequired[str]


class CidrCollectionTypeDef(TypedDict):
    Arn: NotRequired[str]
    Id: NotRequired[str]
    Name: NotRequired[str]
    Version: NotRequired[int]


class CidrRoutingConfigTypeDef(TypedDict):
    CollectionId: str
    LocationName: str


class DimensionTypeDef(TypedDict):
    Name: str
    Value: str


class CollectionSummaryTypeDef(TypedDict):
    Arn: NotRequired[str]
    Id: NotRequired[str]
    Name: NotRequired[str]
    Version: NotRequired[int]


class CoordinatesTypeDef(TypedDict):
    Latitude: str
    Longitude: str


class CreateCidrCollectionRequestTypeDef(TypedDict):
    Name: str
    CallerReference: str


class HostedZoneConfigTypeDef(TypedDict):
    Comment: NotRequired[str]
    PrivateZone: NotRequired[bool]
    HostedZoneTier: NotRequired[HostedZoneTierType]


class DelegationSetTypeDef(TypedDict):
    NameServers: list[str]
    Id: NotRequired[str]
    CallerReference: NotRequired[str]


class CreateKeySigningKeyRequestTypeDef(TypedDict):
    CallerReference: str
    HostedZoneId: str
    KeyManagementServiceArn: str
    Name: str
    Status: str


class KeySigningKeyTypeDef(TypedDict):
    Name: NotRequired[str]
    KmsArn: NotRequired[str]
    Flag: NotRequired[int]
    SigningAlgorithmMnemonic: NotRequired[str]
    SigningAlgorithmType: NotRequired[int]
    DigestAlgorithmMnemonic: NotRequired[str]
    DigestAlgorithmType: NotRequired[int]
    KeyTag: NotRequired[int]
    DigestValue: NotRequired[str]
    PublicKey: NotRequired[str]
    DSRecord: NotRequired[str]
    DNSKEYRecord: NotRequired[str]
    Status: NotRequired[str]
    StatusMessage: NotRequired[str]
    CreatedDate: NotRequired[datetime]
    LastModifiedDate: NotRequired[datetime]


class CreateQueryLoggingConfigRequestTypeDef(TypedDict):
    HostedZoneId: str
    CloudWatchLogsLogGroupArn: str


class QueryLoggingConfigTypeDef(TypedDict):
    Id: str
    HostedZoneId: str
    CloudWatchLogsLogGroupArn: str


class ResourceRecordSetProtectionConfigTypeDef(TypedDict):
    RecordName: str
    RecordType: RRTypeType
    Comment: NotRequired[str]


class CreateReusableDelegationSetRequestTypeDef(TypedDict):
    CallerReference: str
    HostedZoneId: NotRequired[str]


class CreateTrafficPolicyInstanceRequestTypeDef(TypedDict):
    HostedZoneId: str
    Name: str
    TTL: int
    TrafficPolicyId: str
    TrafficPolicyVersion: int


class TrafficPolicyInstanceTypeDef(TypedDict):
    Id: str
    HostedZoneId: str
    Name: str
    TTL: int
    State: str
    Message: str
    TrafficPolicyId: str
    TrafficPolicyVersion: int
    TrafficPolicyType: RRTypeType


class CreateTrafficPolicyRequestTypeDef(TypedDict):
    Name: str
    Document: str
    Comment: NotRequired[str]


TrafficPolicyTypeDef = TypedDict(
    "TrafficPolicyTypeDef",
    {
        "Id": str,
        "Version": int,
        "Name": str,
        "Type": RRTypeType,
        "Document": str,
        "Comment": NotRequired[str],
    },
)


class CreateTrafficPolicyVersionRequestTypeDef(TypedDict):
    Id: str
    Document: str
    Comment: NotRequired[str]


class DNSSECStatusTypeDef(TypedDict):
    ServeSignature: NotRequired[str]
    StatusMessage: NotRequired[str]


class DeactivateKeySigningKeyRequestTypeDef(TypedDict):
    HostedZoneId: str
    Name: str


class DeleteCidrCollectionRequestTypeDef(TypedDict):
    Id: str


class DeleteHealthCheckRequestTypeDef(TypedDict):
    HealthCheckId: str


class DeleteHealthCheckSourceRequestTypeDef(TypedDict):
    HealthCheckSourceId: str


class DeleteHostedZoneRequestTypeDef(TypedDict):
    Id: str


class DeleteKeySigningKeyRequestTypeDef(TypedDict):
    HostedZoneId: str
    Name: str


class DeleteQueryLoggingConfigRequestTypeDef(TypedDict):
    Id: str


class ResourceRecordSetProtectionKeyTypeDef(TypedDict):
    RecordName: str
    RecordType: RRTypeType


class DeleteReusableDelegationSetRequestTypeDef(TypedDict):
    Id: str


class DeleteTrafficPolicyInstanceRequestTypeDef(TypedDict):
    Id: str


class DeleteTrafficPolicyRequestTypeDef(TypedDict):
    Id: str
    Version: int


class DisableHostedZoneDNSSECRequestTypeDef(TypedDict):
    HostedZoneId: str


class EnableHostedZoneDNSSECRequestTypeDef(TypedDict):
    HostedZoneId: str


class GeoLocationDetailsTypeDef(TypedDict):
    ContinentCode: NotRequired[str]
    ContinentName: NotRequired[str]
    CountryCode: NotRequired[str]
    CountryName: NotRequired[str]
    SubdivisionCode: NotRequired[str]
    SubdivisionName: NotRequired[str]


class GeoLocationTypeDef(TypedDict):
    ContinentCode: NotRequired[str]
    CountryCode: NotRequired[str]
    SubdivisionCode: NotRequired[str]


GetAccountLimitRequestTypeDef = TypedDict(
    "GetAccountLimitRequestTypeDef",
    {
        "Type": AccountLimitTypeType,
    },
)


class GetChangeRequestTypeDef(TypedDict):
    Id: str


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class GetDNSSECRequestTypeDef(TypedDict):
    HostedZoneId: str


class GetGeoLocationRequestTypeDef(TypedDict):
    ContinentCode: NotRequired[str]
    CountryCode: NotRequired[str]
    SubdivisionCode: NotRequired[str]


class GetHealthCheckLastFailureReasonRequestTypeDef(TypedDict):
    HealthCheckId: str


class GetHealthCheckRequestTypeDef(TypedDict):
    HealthCheckId: str


class GetHealthCheckSourceRequestTypeDef(TypedDict):
    HealthCheckSourceId: str


class GetHealthCheckStatusRequestTypeDef(TypedDict):
    HealthCheckId: str


class GetHostedZoneChangeBatchRequestTypeDef(TypedDict):
    HostedZoneId: str
    ChangeId: str


GetHostedZoneLimitRequestTypeDef = TypedDict(
    "GetHostedZoneLimitRequestTypeDef",
    {
        "Type": HostedZoneLimitTypeType,
        "HostedZoneId": str,
    },
)
HostedZoneLimitTypeDef = TypedDict(
    "HostedZoneLimitTypeDef",
    {
        "Type": HostedZoneLimitTypeType,
        "Value": int,
    },
)


class GetHostedZoneRequestTypeDef(TypedDict):
    Id: str


class GetQueryLoggingConfigRequestTypeDef(TypedDict):
    Id: str


GetReusableDelegationSetLimitRequestTypeDef = TypedDict(
    "GetReusableDelegationSetLimitRequestTypeDef",
    {
        "Type": Literal["MAX_ZONES_BY_REUSABLE_DELEGATION_SET"],
        "DelegationSetId": str,
    },
)
ReusableDelegationSetLimitTypeDef = TypedDict(
    "ReusableDelegationSetLimitTypeDef",
    {
        "Type": Literal["MAX_ZONES_BY_REUSABLE_DELEGATION_SET"],
        "Value": int,
    },
)


class GetReusableDelegationSetRequestTypeDef(TypedDict):
    Id: str


class GetTrafficPolicyInstanceRequestTypeDef(TypedDict):
    Id: str


class GetTrafficPolicyRequestTypeDef(TypedDict):
    Id: str
    Version: int


class StatusReportTypeDef(TypedDict):
    Status: NotRequired[str]
    CheckedTime: NotRequired[datetime]


class SubnetConfigurationOutputTypeDef(TypedDict):
    SubnetId: str
    AvailabilityZoneId: str
    SecurityGroupIdList: list[str]


class SubnetConfigurationTypeDef(TypedDict):
    SubnetId: str
    AvailabilityZoneId: str
    SecurityGroupIdList: Sequence[str]


class LinkedServiceTypeDef(TypedDict):
    ServicePrincipal: NotRequired[str]
    Description: NotRequired[str]


class HostedZoneFailureReasonsTypeDef(TypedDict):
    AcceleratedRecovery: NotRequired[str]


class HostedZoneOwnerTypeDef(TypedDict):
    OwningAccount: NotRequired[str]
    OwningService: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListCidrBlocksRequestTypeDef(TypedDict):
    CollectionId: str
    LocationName: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[str]


class ListCidrCollectionsRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[str]


class ListCidrLocationsRequestTypeDef(TypedDict):
    CollectionId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[str]


class LocationSummaryTypeDef(TypedDict):
    LocationName: NotRequired[str]


class ListGeoLocationsRequestTypeDef(TypedDict):
    StartContinentCode: NotRequired[str]
    StartCountryCode: NotRequired[str]
    StartSubdivisionCode: NotRequired[str]
    MaxItems: NotRequired[str]


class ListHealthCheckSourcesRequestTypeDef(TypedDict):
    NextToken: NotRequired[str]
    MaxResults: NotRequired[str]


class ListHealthChecksBySourceRequestTypeDef(TypedDict):
    HealthCheckSourceId: str
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]


class ListHealthChecksRequestTypeDef(TypedDict):
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]


class ListHostedZoneChangeBatchesRequestTypeDef(TypedDict):
    HostedZoneId: str
    SubmittedAfter: NotRequired[str]
    SubmittedBefore: NotRequired[str]
    StartAfterChangeId: NotRequired[str]
    SortOrder: NotRequired[ChangeHistorySortOrderType]
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]


class ListHostedZonesByNameRequestTypeDef(TypedDict):
    DNSName: NotRequired[str]
    HostedZoneId: NotRequired[str]
    MaxItems: NotRequired[str]


class ListHostedZonesByVPCRequestTypeDef(TypedDict):
    VPCId: str
    VPCRegion: VPCRegionType
    MaxItems: NotRequired[str]
    NextToken: NotRequired[str]


class ListHostedZonesRequestTypeDef(TypedDict):
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]
    DelegationSetId: NotRequired[str]
    HostedZoneType: NotRequired[Literal["PrivateHostedZone"]]


class ListQueryLoggingConfigsRequestTypeDef(TypedDict):
    HostedZoneId: NotRequired[str]
    NextToken: NotRequired[str]
    MaxResults: NotRequired[str]


class ListResourceRecordSetChangesRequestTypeDef(TypedDict):
    HostedZoneId: str
    RecordName: NotRequired[str]
    RecordType: NotRequired[RRTypeType]
    SubmittedAfter: NotRequired[str]
    SubmittedBefore: NotRequired[str]
    SortOrder: NotRequired[ChangeHistorySortOrderType]
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]


class ListResourceRecordSetProtectionsRequestTypeDef(TypedDict):
    HostedZoneId: str
    StartRecordName: NotRequired[str]
    StartRecordType: NotRequired[RRTypeType]
    MaxResults: NotRequired[str]
    NextToken: NotRequired[str]


class ResourceRecordSetProtectionTypeDef(TypedDict):
    RecordName: str
    RecordType: RRTypeType
    Comment: NotRequired[str]


class ListResourceRecordSetsRequestTypeDef(TypedDict):
    HostedZoneId: str
    StartRecordName: NotRequired[str]
    StartRecordType: NotRequired[RRTypeType]
    StartRecordIdentifier: NotRequired[str]
    MaxItems: NotRequired[str]


class ListReusableDelegationSetsRequestTypeDef(TypedDict):
    Marker: NotRequired[str]
    MaxItems: NotRequired[str]


class ListTagsForResourceRequestTypeDef(TypedDict):
    ResourceType: TagResourceTypeType
    ResourceId: str


class ListTagsForResourcesRequestTypeDef(TypedDict):
    ResourceType: TagResourceTypeType
    ResourceIds: Sequence[str]


class ListTrafficPoliciesRequestTypeDef(TypedDict):
    TrafficPolicyIdMarker: NotRequired[str]
    MaxItems: NotRequired[str]


TrafficPolicySummaryTypeDef = TypedDict(
    "TrafficPolicySummaryTypeDef",
    {
        "Id": str,
        "Name": str,
        "Type": RRTypeType,
        "LatestVersion": int,
        "TrafficPolicyCount": int,
    },
)


class ListTrafficPolicyInstancesByHostedZoneRequestTypeDef(TypedDict):
    HostedZoneId: str
    TrafficPolicyInstanceNameMarker: NotRequired[str]
    TrafficPolicyInstanceTypeMarker: NotRequired[RRTypeType]
    MaxItems: NotRequired[str]


class ListTrafficPolicyInstancesByPolicyRequestTypeDef(TypedDict):
    TrafficPolicyId: str
    TrafficPolicyVersion: int
    HostedZoneIdMarker: NotRequired[str]
    TrafficPolicyInstanceNameMarker: NotRequired[str]
    TrafficPolicyInstanceTypeMarker: NotRequired[RRTypeType]
    MaxItems: NotRequired[str]


class ListTrafficPolicyInstancesRequestTypeDef(TypedDict):
    HostedZoneIdMarker: NotRequired[str]
    TrafficPolicyInstanceNameMarker: NotRequired[str]
    TrafficPolicyInstanceTypeMarker: NotRequired[RRTypeType]
    MaxItems: NotRequired[str]


class ListTrafficPolicyVersionsRequestTypeDef(TypedDict):
    Id: str
    TrafficPolicyVersionMarker: NotRequired[str]
    MaxItems: NotRequired[str]


class ListVPCAssociationAuthorizationsRequestTypeDef(TypedDict):
    HostedZoneId: str
    NextToken: NotRequired[str]
    MaxResults: NotRequired[str]


class ResourceRecordTypeDef(TypedDict):
    Value: str


class TestDNSAnswerRequestTypeDef(TypedDict):
    HostedZoneId: str
    RecordName: str
    RecordType: RRTypeType
    ResolverIP: NotRequired[str]
    EDNS0ClientSubnetIP: NotRequired[str]
    EDNS0ClientSubnetMask: NotRequired[str]


class UpdateHostedZoneCommentRequestTypeDef(TypedDict):
    Id: str
    Comment: NotRequired[str]


class UpdateHostedZoneTierRequestTypeDef(TypedDict):
    HostedZoneId: str
    HostedZoneTier: HostedZoneTierType
    DryRun: NotRequired[bool]


class UpdateTrafficPolicyCommentRequestTypeDef(TypedDict):
    Id: str
    Version: int
    Comment: str


class UpdateTrafficPolicyInstanceRequestTypeDef(TypedDict):
    Id: str
    TTL: int
    TrafficPolicyId: str
    TrafficPolicyVersion: int


class ActivateKeySigningKeyResponseTypeDef(TypedDict):
    ChangeInfo: ChangeInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class AssociateVPCWithHostedZoneResponseTypeDef(TypedDict):
    ChangeInfo: ChangeInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ChangeCidrCollectionResponseTypeDef(TypedDict):
    Id: str
    ResponseMetadata: ResponseMetadataTypeDef


class ChangeResourceRecordSetsResponseTypeDef(TypedDict):
    ChangeInfo: ChangeInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateHealthCheckSourceResponseTypeDef(TypedDict):
    HealthCheckSourceId: str
    HealthCheckSourceStatus: HealthCheckSourceStatusType
    Location: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeactivateKeySigningKeyResponseTypeDef(TypedDict):
    ChangeInfo: ChangeInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteHealthCheckSourceResponseTypeDef(TypedDict):
    HealthCheckSourceId: str
    HealthCheckSourceStatus: HealthCheckSourceStatusType
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteHostedZoneResponseTypeDef(TypedDict):
    ChangeInfo: ChangeInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteKeySigningKeyResponseTypeDef(TypedDict):
    ChangeInfo: ChangeInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisableHostedZoneDNSSECResponseTypeDef(TypedDict):
    ChangeInfo: ChangeInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DisassociateVPCFromHostedZoneResponseTypeDef(TypedDict):
    ChangeInfo: ChangeInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class EnableHostedZoneDNSSECResponseTypeDef(TypedDict):
    ChangeInfo: ChangeInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetAccountLimitResponseTypeDef(TypedDict):
    Limit: AccountLimitTypeDef
    Count: int
    ResponseMetadata: ResponseMetadataTypeDef


class GetChangeResponseTypeDef(TypedDict):
    ChangeInfo: ChangeInfoTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetCheckerIpRangesResponseTypeDef(TypedDict):
    CheckerIpRanges: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetHealthCheckCountResponseTypeDef(TypedDict):
    HealthCheckCount: int
    ResponseMetadata: ResponseMetadataTypeDef


class GetHostedZoneCountResponseTypeDef(TypedDict):
    HostedZoneCount: int
    ResponseMetadata: ResponseMetadataTypeDef


class GetTrafficPolicyInstanceCountResponseTypeDef(TypedDict):
    TrafficPolicyInstanceCount: int
    ResponseMetadata: ResponseMetadataTypeDef


TestDNSAnswerResponseTypeDef = TypedDict(
    "TestDNSAnswerResponseTypeDef",
    {
        "Nameserver": str,
        "RecordName": str,
        "RecordType": RRTypeType,
        "RecordData": list[str],
        "ResponseCode": str,
        "Protocol": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
HealthCheckConfigOutputTypeDef = TypedDict(
    "HealthCheckConfigOutputTypeDef",
    {
        "Type": HealthCheckTypeType,
        "IPAddress": NotRequired[str],
        "Port": NotRequired[int],
        "ResourcePath": NotRequired[str],
        "FullyQualifiedDomainName": NotRequired[str],
        "SearchString": NotRequired[str],
        "RequestInterval": NotRequired[int],
        "FailureThreshold": NotRequired[int],
        "MeasureLatency": NotRequired[bool],
        "Inverted": NotRequired[bool],
        "Disabled": NotRequired[bool],
        "HealthThreshold": NotRequired[int],
        "ChildHealthChecks": NotRequired[list[str]],
        "EnableSNI": NotRequired[bool],
        "Regions": NotRequired[list[HealthCheckRegionType]],
        "AlarmIdentifier": NotRequired[AlarmIdentifierTypeDef],
        "InsufficientDataHealthStatus": NotRequired[InsufficientDataHealthStatusType],
        "RoutingControlArn": NotRequired[str],
        "EndpointType": NotRequired[EndpointTypeType],
        "HealthCheckSourceId": NotRequired[str],
    },
)
HealthCheckConfigTypeDef = TypedDict(
    "HealthCheckConfigTypeDef",
    {
        "Type": HealthCheckTypeType,
        "IPAddress": NotRequired[str],
        "Port": NotRequired[int],
        "ResourcePath": NotRequired[str],
        "FullyQualifiedDomainName": NotRequired[str],
        "SearchString": NotRequired[str],
        "RequestInterval": NotRequired[int],
        "FailureThreshold": NotRequired[int],
        "MeasureLatency": NotRequired[bool],
        "Inverted": NotRequired[bool],
        "Disabled": NotRequired[bool],
        "HealthThreshold": NotRequired[int],
        "ChildHealthChecks": NotRequired[Sequence[str]],
        "EnableSNI": NotRequired[bool],
        "Regions": NotRequired[Sequence[HealthCheckRegionType]],
        "AlarmIdentifier": NotRequired[AlarmIdentifierTypeDef],
        "InsufficientDataHealthStatus": NotRequired[InsufficientDataHealthStatusType],
        "RoutingControlArn": NotRequired[str],
        "EndpointType": NotRequired[EndpointTypeType],
        "HealthCheckSourceId": NotRequired[str],
    },
)


class UpdateHealthCheckRequestTypeDef(TypedDict):
    HealthCheckId: str
    HealthCheckVersion: NotRequired[int]
    IPAddress: NotRequired[str]
    Port: NotRequired[int]
    ResourcePath: NotRequired[str]
    FullyQualifiedDomainName: NotRequired[str]
    SearchString: NotRequired[str]
    FailureThreshold: NotRequired[int]
    Inverted: NotRequired[bool]
    Disabled: NotRequired[bool]
    HealthThreshold: NotRequired[int]
    ChildHealthChecks: NotRequired[Sequence[str]]
    EnableSNI: NotRequired[bool]
    Regions: NotRequired[Sequence[HealthCheckRegionType]]
    AlarmIdentifier: NotRequired[AlarmIdentifierTypeDef]
    InsufficientDataHealthStatus: NotRequired[InsufficientDataHealthStatusType]
    ResetElements: NotRequired[Sequence[ResettableElementNameType]]
    HealthCheckSourceId: NotRequired[str]


class AssociateVPCWithHostedZoneRequestTypeDef(TypedDict):
    HostedZoneId: str
    VPC: VPCTypeDef
    Comment: NotRequired[str]


class CreateVPCAssociationAuthorizationRequestTypeDef(TypedDict):
    HostedZoneId: str
    VPC: VPCTypeDef


class CreateVPCAssociationAuthorizationResponseTypeDef(TypedDict):
    HostedZoneId: str
    VPC: VPCTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVPCAssociationAuthorizationRequestTypeDef(TypedDict):
    HostedZoneId: str
    VPC: VPCTypeDef


class DisassociateVPCFromHostedZoneRequestTypeDef(TypedDict):
    HostedZoneId: str
    VPC: VPCTypeDef
    Comment: NotRequired[str]


class ListVPCAssociationAuthorizationsResponseTypeDef(TypedDict):
    HostedZoneId: str
    VPCs: list[VPCTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListHostedZoneChangeBatchesResponseTypeDef(TypedDict):
    ChangeBatchSummaries: list[ChangeBatchSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ChangeCidrCollectionRequestTypeDef(TypedDict):
    Id: str
    Changes: Sequence[CidrCollectionChangeTypeDef]
    CollectionVersion: NotRequired[int]


class UpdateHostedZoneFeaturesRequestTypeDef(TypedDict):
    HostedZoneId: str
    EnableAcceleratedRecovery: NotRequired[bool]
    EnablePublicDNSFallback: NotRequired[bool]
    ChangeGuardrails: NotRequired[Sequence[ChangeGuardrailTypeDef]]
    DryRun: NotRequired[bool]


class ChangeTagsForResourceRequestTypeDef(TypedDict):
    ResourceType: TagResourceTypeType
    ResourceId: str
    AddTags: NotRequired[Sequence[TagTypeDef]]
    RemoveTagKeys: NotRequired[Sequence[str]]


class ResourceTagSetTypeDef(TypedDict):
    ResourceType: NotRequired[TagResourceTypeType]
    ResourceId: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class ListCidrBlocksResponseTypeDef(TypedDict):
    CidrBlocks: list[CidrBlockSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


CreateCidrCollectionResponseTypeDef = TypedDict(
    "CreateCidrCollectionResponseTypeDef",
    {
        "Collection": CidrCollectionTypeDef,
        "Location": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)


class CloudWatchAlarmConfigurationTypeDef(TypedDict):
    EvaluationPeriods: int
    Threshold: float
    ComparisonOperator: ComparisonOperatorType
    Period: int
    MetricName: str
    Namespace: str
    Statistic: StatisticType
    Dimensions: NotRequired[list[DimensionTypeDef]]


class ListCidrCollectionsResponseTypeDef(TypedDict):
    CidrCollections: list[CollectionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class GeoProximityLocationTypeDef(TypedDict):
    AWSRegion: NotRequired[str]
    LocalZoneGroup: NotRequired[str]
    Coordinates: NotRequired[CoordinatesTypeDef]
    Bias: NotRequired[int]


class CreateHostedZoneRequestTypeDef(TypedDict):
    Name: str
    CallerReference: str
    VPC: NotRequired[VPCTypeDef]
    HostedZoneConfig: NotRequired[HostedZoneConfigTypeDef]
    DelegationSetId: NotRequired[str]
    EnablePublicDNSFallback: NotRequired[bool]
    ChangeGuardrails: NotRequired[Sequence[ChangeGuardrailTypeDef]]


class CreateReusableDelegationSetResponseTypeDef(TypedDict):
    DelegationSet: DelegationSetTypeDef
    Location: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetReusableDelegationSetResponseTypeDef(TypedDict):
    DelegationSet: DelegationSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListReusableDelegationSetsResponseTypeDef(TypedDict):
    DelegationSets: list[DelegationSetTypeDef]
    Marker: str
    IsTruncated: bool
    NextMarker: str
    MaxItems: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateKeySigningKeyResponseTypeDef(TypedDict):
    ChangeInfo: ChangeInfoTypeDef
    KeySigningKey: KeySigningKeyTypeDef
    Location: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateQueryLoggingConfigResponseTypeDef(TypedDict):
    QueryLoggingConfig: QueryLoggingConfigTypeDef
    Location: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetQueryLoggingConfigResponseTypeDef(TypedDict):
    QueryLoggingConfig: QueryLoggingConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListQueryLoggingConfigsResponseTypeDef(TypedDict):
    QueryLoggingConfigs: list[QueryLoggingConfigTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateResourceRecordSetProtectionsRequestTypeDef(TypedDict):
    HostedZoneId: str
    Protections: Sequence[ResourceRecordSetProtectionConfigTypeDef]


class CreateTrafficPolicyInstanceResponseTypeDef(TypedDict):
    TrafficPolicyInstance: TrafficPolicyInstanceTypeDef
    Location: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetTrafficPolicyInstanceResponseTypeDef(TypedDict):
    TrafficPolicyInstance: TrafficPolicyInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListTrafficPolicyInstancesByHostedZoneResponseTypeDef(TypedDict):
    TrafficPolicyInstances: list[TrafficPolicyInstanceTypeDef]
    TrafficPolicyInstanceNameMarker: str
    TrafficPolicyInstanceTypeMarker: RRTypeType
    IsTruncated: bool
    MaxItems: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTrafficPolicyInstancesByPolicyResponseTypeDef(TypedDict):
    TrafficPolicyInstances: list[TrafficPolicyInstanceTypeDef]
    HostedZoneIdMarker: str
    TrafficPolicyInstanceNameMarker: str
    TrafficPolicyInstanceTypeMarker: RRTypeType
    IsTruncated: bool
    MaxItems: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTrafficPolicyInstancesResponseTypeDef(TypedDict):
    TrafficPolicyInstances: list[TrafficPolicyInstanceTypeDef]
    HostedZoneIdMarker: str
    TrafficPolicyInstanceNameMarker: str
    TrafficPolicyInstanceTypeMarker: RRTypeType
    IsTruncated: bool
    MaxItems: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTrafficPolicyInstanceResponseTypeDef(TypedDict):
    TrafficPolicyInstance: TrafficPolicyInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTrafficPolicyResponseTypeDef(TypedDict):
    TrafficPolicy: TrafficPolicyTypeDef
    Location: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTrafficPolicyVersionResponseTypeDef(TypedDict):
    TrafficPolicy: TrafficPolicyTypeDef
    Location: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetTrafficPolicyResponseTypeDef(TypedDict):
    TrafficPolicy: TrafficPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListTrafficPolicyVersionsResponseTypeDef(TypedDict):
    TrafficPolicies: list[TrafficPolicyTypeDef]
    IsTruncated: bool
    TrafficPolicyVersionMarker: str
    MaxItems: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateTrafficPolicyCommentResponseTypeDef(TypedDict):
    TrafficPolicy: TrafficPolicyTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetDNSSECResponseTypeDef(TypedDict):
    Status: DNSSECStatusTypeDef
    KeySigningKeys: list[KeySigningKeyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteResourceRecordSetProtectionsRequestTypeDef(TypedDict):
    HostedZoneId: str
    Protections: Sequence[ResourceRecordSetProtectionKeyTypeDef]


class GetGeoLocationResponseTypeDef(TypedDict):
    GeoLocationDetails: GeoLocationDetailsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListGeoLocationsResponseTypeDef(TypedDict):
    GeoLocationDetailsList: list[GeoLocationDetailsTypeDef]
    IsTruncated: bool
    NextContinentCode: str
    NextCountryCode: str
    NextSubdivisionCode: str
    MaxItems: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetChangeRequestWaitTypeDef(TypedDict):
    Id: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetHealthCheckSourceRequestWaitExtraTypeDef(TypedDict):
    HealthCheckSourceId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetHealthCheckSourceRequestWaitTypeDef(TypedDict):
    HealthCheckSourceId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class GetHostedZoneLimitResponseTypeDef(TypedDict):
    Limit: HostedZoneLimitTypeDef
    Count: int
    ResponseMetadata: ResponseMetadataTypeDef


class GetReusableDelegationSetLimitResponseTypeDef(TypedDict):
    Limit: ReusableDelegationSetLimitTypeDef
    Count: int
    ResponseMetadata: ResponseMetadataTypeDef


class HealthCheckObservationTypeDef(TypedDict):
    Region: NotRequired[HealthCheckRegionType]
    IPAddress: NotRequired[str]
    StatusReport: NotRequired[StatusReportTypeDef]


class HealthCheckSourceConfigOutputTypeDef(TypedDict):
    VpcId: str
    SubnetConfigurationList: list[SubnetConfigurationOutputTypeDef]


class HealthCheckSourceConfigTypeDef(TypedDict):
    VpcId: str
    SubnetConfigurationList: Sequence[SubnetConfigurationTypeDef]


class HostedZoneFeaturesTypeDef(TypedDict):
    AcceleratedRecoveryStatus: NotRequired[AcceleratedRecoveryStatusType]
    PublicDNSFallbackStatus: NotRequired[FeatureStatusType]
    ChangeHistory: NotRequired[ChangeHistoryFeatureTypeDef]
    FailureReasons: NotRequired[HostedZoneFailureReasonsTypeDef]
    ChangeGuardrails: NotRequired[list[ChangeGuardrailTypeDef]]


class HostedZoneSummaryTypeDef(TypedDict):
    HostedZoneId: str
    Name: str
    Owner: HostedZoneOwnerTypeDef


class ListCidrBlocksRequestPaginateTypeDef(TypedDict):
    CollectionId: str
    LocationName: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCidrCollectionsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCidrLocationsRequestPaginateTypeDef(TypedDict):
    CollectionId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListHealthCheckSourcesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListHealthChecksBySourceRequestPaginateTypeDef(TypedDict):
    HealthCheckSourceId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListHealthChecksRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListHostedZoneChangeBatchesRequestPaginateTypeDef(TypedDict):
    HostedZoneId: str
    SubmittedAfter: NotRequired[str]
    SubmittedBefore: NotRequired[str]
    StartAfterChangeId: NotRequired[str]
    SortOrder: NotRequired[ChangeHistorySortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListHostedZonesRequestPaginateTypeDef(TypedDict):
    DelegationSetId: NotRequired[str]
    HostedZoneType: NotRequired[Literal["PrivateHostedZone"]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListQueryLoggingConfigsRequestPaginateTypeDef(TypedDict):
    HostedZoneId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResourceRecordSetChangesRequestPaginateTypeDef(TypedDict):
    HostedZoneId: str
    RecordName: NotRequired[str]
    RecordType: NotRequired[RRTypeType]
    SubmittedAfter: NotRequired[str]
    SubmittedBefore: NotRequired[str]
    SortOrder: NotRequired[ChangeHistorySortOrderType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResourceRecordSetProtectionsRequestPaginateTypeDef(TypedDict):
    HostedZoneId: str
    StartRecordName: NotRequired[str]
    StartRecordType: NotRequired[RRTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListResourceRecordSetsRequestPaginateTypeDef(TypedDict):
    HostedZoneId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListVPCAssociationAuthorizationsRequestPaginateTypeDef(TypedDict):
    HostedZoneId: str
    MaxResults: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListCidrLocationsResponseTypeDef(TypedDict):
    CidrLocations: list[LocationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListResourceRecordSetProtectionsResponseTypeDef(TypedDict):
    ResourceRecordSetProtections: list[ResourceRecordSetProtectionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ListTrafficPoliciesResponseTypeDef(TypedDict):
    TrafficPolicySummaries: list[TrafficPolicySummaryTypeDef]
    IsTruncated: bool
    TrafficPolicyIdMarker: str
    MaxItems: str
    ResponseMetadata: ResponseMetadataTypeDef


HealthCheckConfigUnionTypeDef = Union[HealthCheckConfigTypeDef, HealthCheckConfigOutputTypeDef]


class ListTagsForResourceResponseTypeDef(TypedDict):
    ResourceTagSet: ResourceTagSetTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourcesResponseTypeDef(TypedDict):
    ResourceTagSets: list[ResourceTagSetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class HealthCheckTypeDef(TypedDict):
    Id: str
    CallerReference: str
    HealthCheckConfig: HealthCheckConfigOutputTypeDef
    HealthCheckVersion: int
    LinkedService: NotRequired[LinkedServiceTypeDef]
    CloudWatchAlarmConfiguration: NotRequired[CloudWatchAlarmConfigurationTypeDef]


ResourceRecordSetOutputTypeDef = TypedDict(
    "ResourceRecordSetOutputTypeDef",
    {
        "Name": str,
        "Type": RRTypeType,
        "SetIdentifier": NotRequired[str],
        "Weight": NotRequired[int],
        "Region": NotRequired[ResourceRecordSetRegionType],
        "GeoLocation": NotRequired[GeoLocationTypeDef],
        "Failover": NotRequired[ResourceRecordSetFailoverType],
        "MultiValueAnswer": NotRequired[bool],
        "TTL": NotRequired[int],
        "ResourceRecords": NotRequired[list[ResourceRecordTypeDef]],
        "AliasTarget": NotRequired[AliasTargetTypeDef],
        "HealthCheckId": NotRequired[str],
        "TrafficPolicyInstanceId": NotRequired[str],
        "CidrRoutingConfig": NotRequired[CidrRoutingConfigTypeDef],
        "GeoProximityLocation": NotRequired[GeoProximityLocationTypeDef],
        "AZAffinity": NotRequired[AZAffinityTypeDef],
    },
)
ResourceRecordSetTypeDef = TypedDict(
    "ResourceRecordSetTypeDef",
    {
        "Name": str,
        "Type": RRTypeType,
        "SetIdentifier": NotRequired[str],
        "Weight": NotRequired[int],
        "Region": NotRequired[ResourceRecordSetRegionType],
        "GeoLocation": NotRequired[GeoLocationTypeDef],
        "Failover": NotRequired[ResourceRecordSetFailoverType],
        "MultiValueAnswer": NotRequired[bool],
        "TTL": NotRequired[int],
        "ResourceRecords": NotRequired[Sequence[ResourceRecordTypeDef]],
        "AliasTarget": NotRequired[AliasTargetTypeDef],
        "HealthCheckId": NotRequired[str],
        "TrafficPolicyInstanceId": NotRequired[str],
        "CidrRoutingConfig": NotRequired[CidrRoutingConfigTypeDef],
        "GeoProximityLocation": NotRequired[GeoProximityLocationTypeDef],
        "AZAffinity": NotRequired[AZAffinityTypeDef],
    },
)


class GetHealthCheckLastFailureReasonResponseTypeDef(TypedDict):
    HealthCheckObservations: list[HealthCheckObservationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class GetHealthCheckStatusResponseTypeDef(TypedDict):
    HealthCheckObservations: list[HealthCheckObservationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class HealthCheckSourceTypeDef(TypedDict):
    HealthCheckSourceId: str
    HealthCheckSourceStatus: HealthCheckSourceStatusType
    HealthCheckSourceConfig: HealthCheckSourceConfigOutputTypeDef
    StatusReasonCode: NotRequired[HealthCheckSourceStatusReasonCodeType]
    StatusReason: NotRequired[str]


HealthCheckSourceConfigUnionTypeDef = Union[
    HealthCheckSourceConfigTypeDef, HealthCheckSourceConfigOutputTypeDef
]


class HostedZoneTypeDef(TypedDict):
    Id: str
    Name: str
    CallerReference: str
    Config: NotRequired[HostedZoneConfigTypeDef]
    ResourceRecordSetCount: NotRequired[int]
    LinkedService: NotRequired[LinkedServiceTypeDef]
    Features: NotRequired[HostedZoneFeaturesTypeDef]


class ListHostedZonesByVPCResponseTypeDef(TypedDict):
    HostedZoneSummaries: list[HostedZoneSummaryTypeDef]
    MaxItems: str
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateHealthCheckRequestTypeDef(TypedDict):
    CallerReference: str
    HealthCheckConfig: HealthCheckConfigUnionTypeDef


class CreateHealthCheckResponseTypeDef(TypedDict):
    HealthCheck: HealthCheckTypeDef
    Location: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetHealthCheckResponseTypeDef(TypedDict):
    HealthCheck: HealthCheckTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListHealthChecksBySourceResponseTypeDef(TypedDict):
    HealthChecks: list[HealthCheckTypeDef]
    Marker: str
    IsTruncated: bool
    NextMarker: str
    MaxItems: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListHealthChecksResponseTypeDef(TypedDict):
    HealthChecks: list[HealthCheckTypeDef]
    Marker: str
    IsTruncated: bool
    NextMarker: str
    MaxItems: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateHealthCheckResponseTypeDef(TypedDict):
    HealthCheck: HealthCheckTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ChangeOutputTypeDef(TypedDict):
    Action: ChangeActionType
    ResourceRecordSet: ResourceRecordSetOutputTypeDef


class ListResourceRecordSetsResponseTypeDef(TypedDict):
    ResourceRecordSets: list[ResourceRecordSetOutputTypeDef]
    IsTruncated: bool
    NextRecordName: str
    NextRecordType: RRTypeType
    NextRecordIdentifier: str
    MaxItems: str
    ResponseMetadata: ResponseMetadataTypeDef


class ResourceRecordSetChangeTypeDef(TypedDict):
    ChangeId: str
    Operation: ChangeHistoryOperationType
    SubmittedAt: datetime
    Action: ChangeActionType
    ResourceRecordSet: ResourceRecordSetOutputTypeDef
    SubmittedBy: NotRequired[str]
    RequestId: NotRequired[str]


class ChangeTypeDef(TypedDict):
    Action: ChangeActionType
    ResourceRecordSet: ResourceRecordSetTypeDef


class GetHealthCheckSourceResponseTypeDef(TypedDict):
    HealthCheckSource: HealthCheckSourceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListHealthCheckSourcesResponseTypeDef(TypedDict):
    HealthCheckSources: list[HealthCheckSourceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateHealthCheckSourceRequestTypeDef(TypedDict):
    HealthCheckSourceConfig: HealthCheckSourceConfigUnionTypeDef
    CallerReference: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateHostedZoneResponseTypeDef(TypedDict):
    HostedZone: HostedZoneTypeDef
    ChangeInfo: ChangeInfoTypeDef
    DelegationSet: DelegationSetTypeDef
    VPC: VPCTypeDef
    Location: str
    ResponseMetadata: ResponseMetadataTypeDef


class GetHostedZoneResponseTypeDef(TypedDict):
    HostedZone: HostedZoneTypeDef
    DelegationSet: DelegationSetTypeDef
    VPCs: list[VPCTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListHostedZonesByNameResponseTypeDef(TypedDict):
    HostedZones: list[HostedZoneTypeDef]
    DNSName: str
    HostedZoneId: str
    IsTruncated: bool
    NextDNSName: str
    NextHostedZoneId: str
    MaxItems: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListHostedZonesResponseTypeDef(TypedDict):
    HostedZones: list[HostedZoneTypeDef]
    Marker: str
    IsTruncated: bool
    NextMarker: str
    MaxItems: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateHostedZoneCommentResponseTypeDef(TypedDict):
    HostedZone: HostedZoneTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ChangeBatchOutputTypeDef(TypedDict):
    Changes: list[ChangeOutputTypeDef]
    Comment: NotRequired[str]


class ListResourceRecordSetChangesResponseTypeDef(TypedDict):
    ResourceRecordSetChanges: list[ResourceRecordSetChangeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class ChangeBatchTypeDef(TypedDict):
    Changes: Sequence[ChangeTypeDef]
    Comment: NotRequired[str]


class GetHostedZoneChangeBatchResponseTypeDef(TypedDict):
    ChangeBatchSummary: ChangeBatchSummaryTypeDef
    ChangeBatch: ChangeBatchOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


ChangeBatchUnionTypeDef = Union[ChangeBatchTypeDef, ChangeBatchOutputTypeDef]


class ChangeResourceRecordSetsRequestTypeDef(TypedDict):
    HostedZoneId: str
    ChangeBatch: ChangeBatchUnionTypeDef
