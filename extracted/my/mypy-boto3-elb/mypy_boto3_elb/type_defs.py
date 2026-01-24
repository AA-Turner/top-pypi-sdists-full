"""
Type annotations for elb service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_elb.type_defs import AccessLogTypeDef

    data: AccessLogTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from datetime import datetime
from typing import Union

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "AccessLogTypeDef",
    "AddAvailabilityZonesInputTypeDef",
    "AddAvailabilityZonesOutputTypeDef",
    "AddTagsInputTypeDef",
    "AdditionalAttributeTypeDef",
    "AppCookieStickinessPolicyTypeDef",
    "ApplySecurityGroupsToLoadBalancerInputTypeDef",
    "ApplySecurityGroupsToLoadBalancerOutputTypeDef",
    "AttachLoadBalancerToSubnetsInputTypeDef",
    "AttachLoadBalancerToSubnetsOutputTypeDef",
    "BackendServerDescriptionTypeDef",
    "ConfigureHealthCheckInputTypeDef",
    "ConfigureHealthCheckOutputTypeDef",
    "ConnectionDrainingTypeDef",
    "ConnectionSettingsTypeDef",
    "CreateAccessPointInputTypeDef",
    "CreateAccessPointOutputTypeDef",
    "CreateAppCookieStickinessPolicyInputTypeDef",
    "CreateLBCookieStickinessPolicyInputTypeDef",
    "CreateLoadBalancerListenerInputTypeDef",
    "CreateLoadBalancerPolicyInputTypeDef",
    "CrossZoneLoadBalancingTypeDef",
    "DeleteAccessPointInputTypeDef",
    "DeleteLoadBalancerListenerInputTypeDef",
    "DeleteLoadBalancerPolicyInputTypeDef",
    "DeregisterEndPointsInputTypeDef",
    "DeregisterEndPointsOutputTypeDef",
    "DescribeAccessPointsInputPaginateTypeDef",
    "DescribeAccessPointsInputTypeDef",
    "DescribeAccessPointsOutputTypeDef",
    "DescribeAccountLimitsInputPaginateTypeDef",
    "DescribeAccountLimitsInputTypeDef",
    "DescribeAccountLimitsOutputTypeDef",
    "DescribeEndPointStateInputTypeDef",
    "DescribeEndPointStateInputWaitExtraExtraTypeDef",
    "DescribeEndPointStateInputWaitExtraTypeDef",
    "DescribeEndPointStateInputWaitTypeDef",
    "DescribeEndPointStateOutputTypeDef",
    "DescribeLoadBalancerAttributesInputTypeDef",
    "DescribeLoadBalancerAttributesOutputTypeDef",
    "DescribeLoadBalancerPoliciesInputTypeDef",
    "DescribeLoadBalancerPoliciesOutputTypeDef",
    "DescribeLoadBalancerPolicyTypesInputTypeDef",
    "DescribeLoadBalancerPolicyTypesOutputTypeDef",
    "DescribeTagsInputTypeDef",
    "DescribeTagsOutputTypeDef",
    "DetachLoadBalancerFromSubnetsInputTypeDef",
    "DetachLoadBalancerFromSubnetsOutputTypeDef",
    "HealthCheckTypeDef",
    "InstanceStateTypeDef",
    "InstanceTypeDef",
    "LBCookieStickinessPolicyTypeDef",
    "LimitTypeDef",
    "ListenerDescriptionTypeDef",
    "ListenerTypeDef",
    "LoadBalancerAttributesOutputTypeDef",
    "LoadBalancerAttributesTypeDef",
    "LoadBalancerAttributesUnionTypeDef",
    "LoadBalancerDescriptionTypeDef",
    "ModifyLoadBalancerAttributesInputTypeDef",
    "ModifyLoadBalancerAttributesOutputTypeDef",
    "PaginatorConfigTypeDef",
    "PoliciesTypeDef",
    "PolicyAttributeDescriptionTypeDef",
    "PolicyAttributeTypeDef",
    "PolicyAttributeTypeDescriptionTypeDef",
    "PolicyDescriptionTypeDef",
    "PolicyTypeDescriptionTypeDef",
    "RegisterEndPointsInputTypeDef",
    "RegisterEndPointsOutputTypeDef",
    "RemoveAvailabilityZonesInputTypeDef",
    "RemoveAvailabilityZonesOutputTypeDef",
    "RemoveTagsInputTypeDef",
    "ResponseMetadataTypeDef",
    "SetLoadBalancerListenerSSLCertificateInputTypeDef",
    "SetLoadBalancerPoliciesForBackendServerInputTypeDef",
    "SetLoadBalancerPoliciesOfListenerInputTypeDef",
    "SourceSecurityGroupTypeDef",
    "TagDescriptionTypeDef",
    "TagKeyOnlyTypeDef",
    "TagTypeDef",
    "WaiterConfigTypeDef",
)


class AccessLogTypeDef(TypedDict):
    Enabled: bool
    S3BucketName: NotRequired[str]
    EmitInterval: NotRequired[int]
    S3BucketPrefix: NotRequired[str]


class AddAvailabilityZonesInputTypeDef(TypedDict):
    LoadBalancerName: str
    AvailabilityZones: Sequence[str]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class TagTypeDef(TypedDict):
    Key: str
    Value: NotRequired[str]


class AdditionalAttributeTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]


class AppCookieStickinessPolicyTypeDef(TypedDict):
    PolicyName: NotRequired[str]
    CookieName: NotRequired[str]


class ApplySecurityGroupsToLoadBalancerInputTypeDef(TypedDict):
    LoadBalancerName: str
    SecurityGroups: Sequence[str]


class AttachLoadBalancerToSubnetsInputTypeDef(TypedDict):
    LoadBalancerName: str
    Subnets: Sequence[str]


class BackendServerDescriptionTypeDef(TypedDict):
    InstancePort: NotRequired[int]
    PolicyNames: NotRequired[list[str]]


class HealthCheckTypeDef(TypedDict):
    Target: str
    Interval: int
    Timeout: int
    UnhealthyThreshold: int
    HealthyThreshold: int


class ConnectionDrainingTypeDef(TypedDict):
    Enabled: bool
    Timeout: NotRequired[int]


class ConnectionSettingsTypeDef(TypedDict):
    IdleTimeout: int


ListenerTypeDef = TypedDict(
    "ListenerTypeDef",
    {
        "Protocol": str,
        "LoadBalancerPort": int,
        "InstancePort": int,
        "InstanceProtocol": NotRequired[str],
        "SSLCertificateId": NotRequired[str],
    },
)


class CreateAppCookieStickinessPolicyInputTypeDef(TypedDict):
    LoadBalancerName: str
    PolicyName: str
    CookieName: str


class CreateLBCookieStickinessPolicyInputTypeDef(TypedDict):
    LoadBalancerName: str
    PolicyName: str
    CookieExpirationPeriod: NotRequired[int]


class PolicyAttributeTypeDef(TypedDict):
    AttributeName: NotRequired[str]
    AttributeValue: NotRequired[str]


class CrossZoneLoadBalancingTypeDef(TypedDict):
    Enabled: bool


class DeleteAccessPointInputTypeDef(TypedDict):
    LoadBalancerName: str


class DeleteLoadBalancerListenerInputTypeDef(TypedDict):
    LoadBalancerName: str
    LoadBalancerPorts: Sequence[int]


class DeleteLoadBalancerPolicyInputTypeDef(TypedDict):
    LoadBalancerName: str
    PolicyName: str


class InstanceTypeDef(TypedDict):
    InstanceId: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class DescribeAccessPointsInputTypeDef(TypedDict):
    LoadBalancerNames: NotRequired[Sequence[str]]
    Marker: NotRequired[str]
    PageSize: NotRequired[int]


class DescribeAccountLimitsInputTypeDef(TypedDict):
    Marker: NotRequired[str]
    PageSize: NotRequired[int]


class LimitTypeDef(TypedDict):
    Name: NotRequired[str]
    Max: NotRequired[str]


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class InstanceStateTypeDef(TypedDict):
    InstanceId: NotRequired[str]
    State: NotRequired[str]
    ReasonCode: NotRequired[str]
    Description: NotRequired[str]


class DescribeLoadBalancerAttributesInputTypeDef(TypedDict):
    LoadBalancerName: str


class DescribeLoadBalancerPoliciesInputTypeDef(TypedDict):
    LoadBalancerName: NotRequired[str]
    PolicyNames: NotRequired[Sequence[str]]


class DescribeLoadBalancerPolicyTypesInputTypeDef(TypedDict):
    PolicyTypeNames: NotRequired[Sequence[str]]


class DescribeTagsInputTypeDef(TypedDict):
    LoadBalancerNames: Sequence[str]


class DetachLoadBalancerFromSubnetsInputTypeDef(TypedDict):
    LoadBalancerName: str
    Subnets: Sequence[str]


class LBCookieStickinessPolicyTypeDef(TypedDict):
    PolicyName: NotRequired[str]
    CookieExpirationPeriod: NotRequired[int]


class SourceSecurityGroupTypeDef(TypedDict):
    OwnerAlias: NotRequired[str]
    GroupName: NotRequired[str]


class PolicyAttributeDescriptionTypeDef(TypedDict):
    AttributeName: NotRequired[str]
    AttributeValue: NotRequired[str]


class PolicyAttributeTypeDescriptionTypeDef(TypedDict):
    AttributeName: NotRequired[str]
    AttributeType: NotRequired[str]
    Description: NotRequired[str]
    DefaultValue: NotRequired[str]
    Cardinality: NotRequired[str]


class RemoveAvailabilityZonesInputTypeDef(TypedDict):
    LoadBalancerName: str
    AvailabilityZones: Sequence[str]


class TagKeyOnlyTypeDef(TypedDict):
    Key: NotRequired[str]


class SetLoadBalancerListenerSSLCertificateInputTypeDef(TypedDict):
    LoadBalancerName: str
    LoadBalancerPort: int
    SSLCertificateId: str


class SetLoadBalancerPoliciesForBackendServerInputTypeDef(TypedDict):
    LoadBalancerName: str
    InstancePort: int
    PolicyNames: Sequence[str]


class SetLoadBalancerPoliciesOfListenerInputTypeDef(TypedDict):
    LoadBalancerName: str
    LoadBalancerPort: int
    PolicyNames: Sequence[str]


class AddAvailabilityZonesOutputTypeDef(TypedDict):
    AvailabilityZones: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class ApplySecurityGroupsToLoadBalancerOutputTypeDef(TypedDict):
    SecurityGroups: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class AttachLoadBalancerToSubnetsOutputTypeDef(TypedDict):
    Subnets: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAccessPointOutputTypeDef(TypedDict):
    DNSName: str
    ResponseMetadata: ResponseMetadataTypeDef


class DetachLoadBalancerFromSubnetsOutputTypeDef(TypedDict):
    Subnets: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class RemoveAvailabilityZonesOutputTypeDef(TypedDict):
    AvailabilityZones: list[str]
    ResponseMetadata: ResponseMetadataTypeDef


class AddTagsInputTypeDef(TypedDict):
    LoadBalancerNames: Sequence[str]
    Tags: Sequence[TagTypeDef]


class TagDescriptionTypeDef(TypedDict):
    LoadBalancerName: NotRequired[str]
    Tags: NotRequired[list[TagTypeDef]]


class ConfigureHealthCheckInputTypeDef(TypedDict):
    LoadBalancerName: str
    HealthCheck: HealthCheckTypeDef


class ConfigureHealthCheckOutputTypeDef(TypedDict):
    HealthCheck: HealthCheckTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAccessPointInputTypeDef(TypedDict):
    LoadBalancerName: str
    Listeners: Sequence[ListenerTypeDef]
    AvailabilityZones: NotRequired[Sequence[str]]
    Subnets: NotRequired[Sequence[str]]
    SecurityGroups: NotRequired[Sequence[str]]
    Scheme: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateLoadBalancerListenerInputTypeDef(TypedDict):
    LoadBalancerName: str
    Listeners: Sequence[ListenerTypeDef]


class ListenerDescriptionTypeDef(TypedDict):
    Listener: NotRequired[ListenerTypeDef]
    PolicyNames: NotRequired[list[str]]


class CreateLoadBalancerPolicyInputTypeDef(TypedDict):
    LoadBalancerName: str
    PolicyName: str
    PolicyTypeName: str
    PolicyAttributes: NotRequired[Sequence[PolicyAttributeTypeDef]]


class LoadBalancerAttributesOutputTypeDef(TypedDict):
    CrossZoneLoadBalancing: NotRequired[CrossZoneLoadBalancingTypeDef]
    AccessLog: NotRequired[AccessLogTypeDef]
    ConnectionDraining: NotRequired[ConnectionDrainingTypeDef]
    ConnectionSettings: NotRequired[ConnectionSettingsTypeDef]
    AdditionalAttributes: NotRequired[list[AdditionalAttributeTypeDef]]


class LoadBalancerAttributesTypeDef(TypedDict):
    CrossZoneLoadBalancing: NotRequired[CrossZoneLoadBalancingTypeDef]
    AccessLog: NotRequired[AccessLogTypeDef]
    ConnectionDraining: NotRequired[ConnectionDrainingTypeDef]
    ConnectionSettings: NotRequired[ConnectionSettingsTypeDef]
    AdditionalAttributes: NotRequired[Sequence[AdditionalAttributeTypeDef]]


class DeregisterEndPointsInputTypeDef(TypedDict):
    LoadBalancerName: str
    Instances: Sequence[InstanceTypeDef]


class DeregisterEndPointsOutputTypeDef(TypedDict):
    Instances: list[InstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEndPointStateInputTypeDef(TypedDict):
    LoadBalancerName: str
    Instances: NotRequired[Sequence[InstanceTypeDef]]


class RegisterEndPointsInputTypeDef(TypedDict):
    LoadBalancerName: str
    Instances: Sequence[InstanceTypeDef]


class RegisterEndPointsOutputTypeDef(TypedDict):
    Instances: list[InstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAccessPointsInputPaginateTypeDef(TypedDict):
    LoadBalancerNames: NotRequired[Sequence[str]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeAccountLimitsInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeAccountLimitsOutputTypeDef(TypedDict):
    Limits: list[LimitTypeDef]
    NextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEndPointStateInputWaitExtraExtraTypeDef(TypedDict):
    LoadBalancerName: str
    Instances: NotRequired[Sequence[InstanceTypeDef]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeEndPointStateInputWaitExtraTypeDef(TypedDict):
    LoadBalancerName: str
    Instances: NotRequired[Sequence[InstanceTypeDef]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeEndPointStateInputWaitTypeDef(TypedDict):
    LoadBalancerName: str
    Instances: NotRequired[Sequence[InstanceTypeDef]]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeEndPointStateOutputTypeDef(TypedDict):
    InstanceStates: list[InstanceStateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class PoliciesTypeDef(TypedDict):
    AppCookieStickinessPolicies: NotRequired[list[AppCookieStickinessPolicyTypeDef]]
    LBCookieStickinessPolicies: NotRequired[list[LBCookieStickinessPolicyTypeDef]]
    OtherPolicies: NotRequired[list[str]]


class PolicyDescriptionTypeDef(TypedDict):
    PolicyName: NotRequired[str]
    PolicyTypeName: NotRequired[str]
    PolicyAttributeDescriptions: NotRequired[list[PolicyAttributeDescriptionTypeDef]]


class PolicyTypeDescriptionTypeDef(TypedDict):
    PolicyTypeName: NotRequired[str]
    Description: NotRequired[str]
    PolicyAttributeTypeDescriptions: NotRequired[list[PolicyAttributeTypeDescriptionTypeDef]]


class RemoveTagsInputTypeDef(TypedDict):
    LoadBalancerNames: Sequence[str]
    Tags: Sequence[TagKeyOnlyTypeDef]


class DescribeTagsOutputTypeDef(TypedDict):
    TagDescriptions: list[TagDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeLoadBalancerAttributesOutputTypeDef(TypedDict):
    LoadBalancerAttributes: LoadBalancerAttributesOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyLoadBalancerAttributesOutputTypeDef(TypedDict):
    LoadBalancerName: str
    LoadBalancerAttributes: LoadBalancerAttributesOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


LoadBalancerAttributesUnionTypeDef = Union[
    LoadBalancerAttributesTypeDef, LoadBalancerAttributesOutputTypeDef
]


class LoadBalancerDescriptionTypeDef(TypedDict):
    LoadBalancerName: NotRequired[str]
    DNSName: NotRequired[str]
    CanonicalHostedZoneName: NotRequired[str]
    CanonicalHostedZoneNameID: NotRequired[str]
    ListenerDescriptions: NotRequired[list[ListenerDescriptionTypeDef]]
    Policies: NotRequired[PoliciesTypeDef]
    BackendServerDescriptions: NotRequired[list[BackendServerDescriptionTypeDef]]
    AvailabilityZones: NotRequired[list[str]]
    Subnets: NotRequired[list[str]]
    VPCId: NotRequired[str]
    Instances: NotRequired[list[InstanceTypeDef]]
    HealthCheck: NotRequired[HealthCheckTypeDef]
    SourceSecurityGroup: NotRequired[SourceSecurityGroupTypeDef]
    SecurityGroups: NotRequired[list[str]]
    CreatedTime: NotRequired[datetime]
    Scheme: NotRequired[str]


class DescribeLoadBalancerPoliciesOutputTypeDef(TypedDict):
    PolicyDescriptions: list[PolicyDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeLoadBalancerPolicyTypesOutputTypeDef(TypedDict):
    PolicyTypeDescriptions: list[PolicyTypeDescriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyLoadBalancerAttributesInputTypeDef(TypedDict):
    LoadBalancerName: str
    LoadBalancerAttributes: LoadBalancerAttributesUnionTypeDef


class DescribeAccessPointsOutputTypeDef(TypedDict):
    LoadBalancerDescriptions: list[LoadBalancerDescriptionTypeDef]
    NextMarker: str
    ResponseMetadata: ResponseMetadataTypeDef
