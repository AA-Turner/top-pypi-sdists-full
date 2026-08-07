"""
Type annotations for agent-registry-control service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_agent_registry_control/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_agent_registry_control.type_defs import ApprovalConfigurationOutputTypeDef

    data: ApprovalConfigurationOutputTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Union

from .literals import (
    ClaimMatchOperatorTypeType,
    EndpointIpAddressTypeType,
    InboundTokenClaimValueTypeType,
    RecordTypeType,
    RegistryAuthorizerTypeType,
    RegistryFilterNameType,
    RegistryRecordCredentialProviderTypeType,
    RegistryRecordFilterNameType,
    RegistryRecordStatusType,
    RegistryStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "A2aAgentCardDescriptorOutputTypeDef",
    "A2aAgentCardDescriptorTypeDef",
    "AgentSkillsAdditionalDataOutputTypeDef",
    "AgentSkillsAdditionalDataTypeDef",
    "AgentSkillsDefinitionDescriptorOutputTypeDef",
    "AgentSkillsDefinitionDescriptorTypeDef",
    "AgentSkillsMdDescriptorOutputTypeDef",
    "AgentSkillsMdDescriptorTypeDef",
    "ApprovalConfigurationOutputTypeDef",
    "ApprovalConfigurationTypeDef",
    "ApprovalConfigurationUnionTypeDef",
    "AuthorizerConfigurationOutputTypeDef",
    "AuthorizerConfigurationTypeDef",
    "AuthorizerConfigurationUnionTypeDef",
    "AuthorizingClaimMatchValueTypeOutputTypeDef",
    "AuthorizingClaimMatchValueTypeTypeDef",
    "AuthorizingClaimMatchValueTypeUnionTypeDef",
    "ClaimMatchValueTypeOutputTypeDef",
    "ClaimMatchValueTypeTypeDef",
    "ClaimMatchValueTypeUnionTypeDef",
    "CreateRegistryRecordRequestTypeDef",
    "CreateRegistryRecordResponseTypeDef",
    "CreateRegistryRequestTypeDef",
    "CreateRegistryResponseTypeDef",
    "CustomClaimValidationTypeOutputTypeDef",
    "CustomClaimValidationTypeTypeDef",
    "CustomClaimValidationTypeUnionTypeDef",
    "CustomDescriptorTypeDef",
    "CustomJWTAuthorizerConfigurationOutputTypeDef",
    "CustomJWTAuthorizerConfigurationTypeDef",
    "CustomJWTAuthorizerConfigurationUnionTypeDef",
    "DeleteRegistryRecordRequestTypeDef",
    "DeleteRegistryRequestTypeDef",
    "DeleteRegistryResponseTypeDef",
    "DescriptorSourceFromUrlOutputTypeDef",
    "DescriptorSourceFromUrlTypeDef",
    "DescriptorSourceFromUrlUnionTypeDef",
    "DescriptorSourceOutputTypeDef",
    "DescriptorSourceTypeDef",
    "DescriptorSourceUnionTypeDef",
    "DescriptorsOutputTypeDef",
    "DescriptorsTypeDef",
    "DescriptorsUnionTypeDef",
    "DiscoveryConfigurationOutputTypeDef",
    "DiscoveryConfigurationTypeDef",
    "DiscoveryConfigurationUnionTypeDef",
    "GetRegistryRecordRequestTypeDef",
    "GetRegistryRecordRequestWaitTypeDef",
    "GetRegistryRecordResponseTypeDef",
    "GetRegistryRequestTypeDef",
    "GetRegistryRequestWaitTypeDef",
    "GetRegistryResponseTypeDef",
    "ListRegistriesRequestPaginateTypeDef",
    "ListRegistriesRequestTypeDef",
    "ListRegistriesResponseTypeDef",
    "ListRegistryRecordsRequestPaginateTypeDef",
    "ListRegistryRecordsRequestTypeDef",
    "ListRegistryRecordsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ManagedVpcResourceOutputTypeDef",
    "ManagedVpcResourceTypeDef",
    "ManagedVpcResourceUnionTypeDef",
    "McpServerAdditionalDataTypeDef",
    "McpServerDescriptorOutputTypeDef",
    "McpServerDescriptorTypeDef",
    "McpToolsDescriptorTypeDef",
    "PaginatorConfigTypeDef",
    "PrivateEndpointOutputTypeDef",
    "PrivateEndpointOverrideOutputTypeDef",
    "PrivateEndpointOverrideTypeDef",
    "PrivateEndpointOverrideUnionTypeDef",
    "PrivateEndpointTypeDef",
    "PrivateEndpointUnionTypeDef",
    "RegistryFilterTypeDef",
    "RegistryRecordCredentialProviderConfigurationOutputTypeDef",
    "RegistryRecordCredentialProviderConfigurationTypeDef",
    "RegistryRecordCredentialProviderConfigurationUnionTypeDef",
    "RegistryRecordCredentialProviderUnionOutputTypeDef",
    "RegistryRecordCredentialProviderUnionTypeDef",
    "RegistryRecordCredentialProviderUnionUnionTypeDef",
    "RegistryRecordFilterTypeDef",
    "RegistryRecordIamCredentialProviderTypeDef",
    "RegistryRecordOAuthCredentialProviderOutputTypeDef",
    "RegistryRecordOAuthCredentialProviderTypeDef",
    "RegistryRecordOAuthCredentialProviderUnionTypeDef",
    "RegistryRecordSummaryTypeDef",
    "RegistrySummaryTypeDef",
    "ResponseMetadataTypeDef",
    "SelfManagedLatticeResourceTypeDef",
    "SubmitRegistryRecordForApprovalRequestTypeDef",
    "SubmitRegistryRecordForApprovalResponseTypeDef",
    "TagResourceRequestTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateRegistryRecordRequestTypeDef",
    "UpdateRegistryRecordResponseTypeDef",
    "UpdateRegistryRecordStatusRequestTypeDef",
    "UpdateRegistryRecordStatusResponseTypeDef",
    "UpdateRegistryRequestTypeDef",
    "UpdateRegistryResponseTypeDef",
    "UpdatedA2aAgentCardDescriptorFieldsTypeDef",
    "UpdatedA2aAgentCardDescriptorTypeDef",
    "UpdatedAgentSkillsAdditionalDataFieldsTypeDef",
    "UpdatedAgentSkillsAdditionalDataTypeDef",
    "UpdatedAgentSkillsDefinitionDescriptorFieldsTypeDef",
    "UpdatedAgentSkillsDefinitionDescriptorTypeDef",
    "UpdatedAgentSkillsMdDescriptorFieldsTypeDef",
    "UpdatedAgentSkillsMdDescriptorTypeDef",
    "UpdatedApprovalConfigurationTypeDef",
    "UpdatedAuthorizerConfigurationTypeDef",
    "UpdatedCustomDescriptorFieldsTypeDef",
    "UpdatedCustomDescriptorTypeDef",
    "UpdatedDataSchemaVersionTypeDef",
    "UpdatedDescriptionTypeDef",
    "UpdatedDescriptorDataTypeDef",
    "UpdatedDescriptorSourceTypeDef",
    "UpdatedDescriptorsFieldsTypeDef",
    "UpdatedDescriptorsTypeDef",
    "UpdatedDiscoveryConfigurationTypeDef",
    "UpdatedDisplayNameTypeDef",
    "UpdatedMcpServerAdditionalDataFieldsTypeDef",
    "UpdatedMcpServerAdditionalDataTypeDef",
    "UpdatedMcpServerDescriptorFieldsTypeDef",
    "UpdatedMcpServerDescriptorTypeDef",
    "UpdatedMcpToolsDescriptorFieldsTypeDef",
    "UpdatedMcpToolsDescriptorTypeDef",
    "WaiterConfigTypeDef",
)

class ApprovalConfigurationOutputTypeDef(TypedDict):
    autoApprovalRules: NotRequired[list[Literal["APPROVE_ALL"]]]

class ApprovalConfigurationTypeDef(TypedDict):
    autoApprovalRules: NotRequired[Sequence[Literal["APPROVE_ALL"]]]

class ClaimMatchValueTypeOutputTypeDef(TypedDict):
    matchValueString: NotRequired[str]
    matchValueStringList: NotRequired[list[str]]

class ClaimMatchValueTypeTypeDef(TypedDict):
    matchValueString: NotRequired[str]
    matchValueStringList: NotRequired[Sequence[str]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class CustomDescriptorTypeDef(TypedDict):
    data: NotRequired[str]

class DeleteRegistryRecordRequestTypeDef(TypedDict):
    registryId: str
    recordId: str

class DeleteRegistryRequestTypeDef(TypedDict):
    registryId: str

class GetRegistryRecordRequestTypeDef(TypedDict):
    registryId: str
    recordId: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class GetRegistryRequestTypeDef(TypedDict):
    registryId: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class RegistryFilterTypeDef(TypedDict):
    name: RegistryFilterNameType
    values: Sequence[str]

class RegistryRecordFilterTypeDef(TypedDict):
    name: RegistryRecordFilterNameType
    values: Sequence[str]

class RegistryRecordSummaryTypeDef(TypedDict):
    registryArn: str
    recordArn: str
    recordId: str
    name: str
    recordType: RecordTypeType
    recordVersion: str
    status: RegistryRecordStatusType
    createdAt: datetime
    updatedAt: datetime
    displayName: NotRequired[str]
    description: NotRequired[str]

class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str

class ManagedVpcResourceOutputTypeDef(TypedDict):
    vpcIdentifier: str
    subnetIds: list[str]
    endpointIpAddressType: EndpointIpAddressTypeType
    securityGroupIds: NotRequired[list[str]]
    tags: NotRequired[dict[str, str]]
    routingDomain: NotRequired[str]

class ManagedVpcResourceTypeDef(TypedDict):
    vpcIdentifier: str
    subnetIds: Sequence[str]
    endpointIpAddressType: EndpointIpAddressTypeType
    securityGroupIds: NotRequired[Sequence[str]]
    tags: NotRequired[Mapping[str, str]]
    routingDomain: NotRequired[str]

class McpToolsDescriptorTypeDef(TypedDict):
    data: NotRequired[str]
    dataSchemaVersion: NotRequired[str]

class SelfManagedLatticeResourceTypeDef(TypedDict):
    resourceConfigurationIdentifier: NotRequired[str]

class RegistryRecordIamCredentialProviderTypeDef(TypedDict):
    roleArn: NotRequired[str]
    service: NotRequired[str]
    region: NotRequired[str]

class RegistryRecordOAuthCredentialProviderOutputTypeDef(TypedDict):
    providerArn: str
    grantType: NotRequired[Literal["CLIENT_CREDENTIALS"]]
    scopes: NotRequired[list[str]]
    customParameters: NotRequired[dict[str, str]]

class RegistryRecordOAuthCredentialProviderTypeDef(TypedDict):
    providerArn: str
    grantType: NotRequired[Literal["CLIENT_CREDENTIALS"]]
    scopes: NotRequired[Sequence[str]]
    customParameters: NotRequired[Mapping[str, str]]

class SubmitRegistryRecordForApprovalRequestTypeDef(TypedDict):
    registryId: str
    recordId: str

class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdatedDescriptionTypeDef(TypedDict):
    optionalValue: NotRequired[str]

class UpdatedDisplayNameTypeDef(TypedDict):
    optionalValue: NotRequired[str]

class UpdateRegistryRecordStatusRequestTypeDef(TypedDict):
    registryId: str
    recordId: str
    status: RegistryRecordStatusType
    statusReason: str

class UpdatedDataSchemaVersionTypeDef(TypedDict):
    optionalValue: NotRequired[str]

class UpdatedDescriptorDataTypeDef(TypedDict):
    optionalValue: NotRequired[str]

ApprovalConfigurationUnionTypeDef = Union[
    ApprovalConfigurationTypeDef, ApprovalConfigurationOutputTypeDef
]

class AuthorizingClaimMatchValueTypeOutputTypeDef(TypedDict):
    claimMatchValue: ClaimMatchValueTypeOutputTypeDef
    claimMatchOperator: ClaimMatchOperatorTypeType

ClaimMatchValueTypeUnionTypeDef = Union[
    ClaimMatchValueTypeTypeDef, ClaimMatchValueTypeOutputTypeDef
]

class CreateRegistryRecordResponseTypeDef(TypedDict):
    recordArn: str
    status: RegistryRecordStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRegistryResponseTypeDef(TypedDict):
    registryArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteRegistryResponseTypeDef(TypedDict):
    status: RegistryStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class SubmitRegistryRecordForApprovalResponseTypeDef(TypedDict):
    registryArn: str
    recordArn: str
    recordId: str
    status: RegistryRecordStatusType
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRegistryRecordStatusResponseTypeDef(TypedDict):
    registryArn: str
    recordArn: str
    recordId: str
    status: RegistryRecordStatusType
    statusReason: str
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetRegistryRecordRequestWaitTypeDef(TypedDict):
    registryId: str
    recordId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetRegistryRequestWaitTypeDef(TypedDict):
    registryId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class ListRegistriesRequestPaginateTypeDef(TypedDict):
    filters: NotRequired[Sequence[RegistryFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRegistriesRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    filters: NotRequired[Sequence[RegistryFilterTypeDef]]

class ListRegistryRecordsRequestPaginateTypeDef(TypedDict):
    registryId: str
    filters: NotRequired[Sequence[RegistryRecordFilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRegistryRecordsRequestTypeDef(TypedDict):
    registryId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    filters: NotRequired[Sequence[RegistryRecordFilterTypeDef]]

class ListRegistryRecordsResponseTypeDef(TypedDict):
    registryRecords: list[RegistryRecordSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

ManagedVpcResourceUnionTypeDef = Union[ManagedVpcResourceTypeDef, ManagedVpcResourceOutputTypeDef]

class McpServerAdditionalDataTypeDef(TypedDict):
    tools: NotRequired[McpToolsDescriptorTypeDef]

class PrivateEndpointOutputTypeDef(TypedDict):
    selfManagedLatticeResource: NotRequired[SelfManagedLatticeResourceTypeDef]
    managedVpcResource: NotRequired[ManagedVpcResourceOutputTypeDef]

class RegistryRecordCredentialProviderUnionOutputTypeDef(TypedDict):
    oauthCredentialProvider: NotRequired[RegistryRecordOAuthCredentialProviderOutputTypeDef]
    iamCredentialProvider: NotRequired[RegistryRecordIamCredentialProviderTypeDef]

RegistryRecordOAuthCredentialProviderUnionTypeDef = Union[
    RegistryRecordOAuthCredentialProviderTypeDef, RegistryRecordOAuthCredentialProviderOutputTypeDef
]

class UpdatedCustomDescriptorFieldsTypeDef(TypedDict):
    data: NotRequired[UpdatedDescriptorDataTypeDef]

class UpdatedMcpToolsDescriptorFieldsTypeDef(TypedDict):
    data: NotRequired[UpdatedDescriptorDataTypeDef]
    dataSchemaVersion: NotRequired[UpdatedDataSchemaVersionTypeDef]

class UpdatedApprovalConfigurationTypeDef(TypedDict):
    optionalValue: NotRequired[ApprovalConfigurationUnionTypeDef]

class CustomClaimValidationTypeOutputTypeDef(TypedDict):
    inboundTokenClaimName: str
    inboundTokenClaimValueType: InboundTokenClaimValueTypeType
    authorizingClaimMatchValue: AuthorizingClaimMatchValueTypeOutputTypeDef

class AuthorizingClaimMatchValueTypeTypeDef(TypedDict):
    claimMatchValue: ClaimMatchValueTypeUnionTypeDef
    claimMatchOperator: ClaimMatchOperatorTypeType

class PrivateEndpointTypeDef(TypedDict):
    selfManagedLatticeResource: NotRequired[SelfManagedLatticeResourceTypeDef]
    managedVpcResource: NotRequired[ManagedVpcResourceUnionTypeDef]

class PrivateEndpointOverrideOutputTypeDef(TypedDict):
    domain: str
    privateEndpoint: PrivateEndpointOutputTypeDef

class RegistryRecordCredentialProviderConfigurationOutputTypeDef(TypedDict):
    credentialProviderType: RegistryRecordCredentialProviderTypeType
    credentialProvider: RegistryRecordCredentialProviderUnionOutputTypeDef

class RegistryRecordCredentialProviderUnionTypeDef(TypedDict):
    oauthCredentialProvider: NotRequired[RegistryRecordOAuthCredentialProviderUnionTypeDef]
    iamCredentialProvider: NotRequired[RegistryRecordIamCredentialProviderTypeDef]

class UpdatedCustomDescriptorTypeDef(TypedDict):
    optionalValue: NotRequired[UpdatedCustomDescriptorFieldsTypeDef]

class UpdatedMcpToolsDescriptorTypeDef(TypedDict):
    optionalValue: NotRequired[UpdatedMcpToolsDescriptorFieldsTypeDef]

AuthorizingClaimMatchValueTypeUnionTypeDef = Union[
    AuthorizingClaimMatchValueTypeTypeDef, AuthorizingClaimMatchValueTypeOutputTypeDef
]
PrivateEndpointUnionTypeDef = Union[PrivateEndpointTypeDef, PrivateEndpointOutputTypeDef]

class CustomJWTAuthorizerConfigurationOutputTypeDef(TypedDict):
    discoveryUrl: str
    allowedAudience: NotRequired[list[str]]
    allowedClients: NotRequired[list[str]]
    allowedScopes: NotRequired[list[str]]
    customClaims: NotRequired[list[CustomClaimValidationTypeOutputTypeDef]]
    privateEndpoint: NotRequired[PrivateEndpointOutputTypeDef]
    privateEndpointOverrides: NotRequired[list[PrivateEndpointOverrideOutputTypeDef]]

class DescriptorSourceFromUrlOutputTypeDef(TypedDict):
    url: str
    credentialProviderConfigurations: NotRequired[
        list[RegistryRecordCredentialProviderConfigurationOutputTypeDef]
    ]

RegistryRecordCredentialProviderUnionUnionTypeDef = Union[
    RegistryRecordCredentialProviderUnionTypeDef, RegistryRecordCredentialProviderUnionOutputTypeDef
]

class UpdatedMcpServerAdditionalDataFieldsTypeDef(TypedDict):
    tools: NotRequired[UpdatedMcpToolsDescriptorTypeDef]

class CustomClaimValidationTypeTypeDef(TypedDict):
    inboundTokenClaimName: str
    inboundTokenClaimValueType: InboundTokenClaimValueTypeType
    authorizingClaimMatchValue: AuthorizingClaimMatchValueTypeUnionTypeDef

class PrivateEndpointOverrideTypeDef(TypedDict):
    domain: str
    privateEndpoint: PrivateEndpointUnionTypeDef

class AuthorizerConfigurationOutputTypeDef(TypedDict):
    customJWTAuthorizer: NotRequired[CustomJWTAuthorizerConfigurationOutputTypeDef]

class DescriptorSourceOutputTypeDef(TypedDict):
    fromUrl: NotRequired[DescriptorSourceFromUrlOutputTypeDef]

class RegistryRecordCredentialProviderConfigurationTypeDef(TypedDict):
    credentialProviderType: RegistryRecordCredentialProviderTypeType
    credentialProvider: RegistryRecordCredentialProviderUnionUnionTypeDef

class UpdatedMcpServerAdditionalDataTypeDef(TypedDict):
    optionalValue: NotRequired[UpdatedMcpServerAdditionalDataFieldsTypeDef]

CustomClaimValidationTypeUnionTypeDef = Union[
    CustomClaimValidationTypeTypeDef, CustomClaimValidationTypeOutputTypeDef
]
PrivateEndpointOverrideUnionTypeDef = Union[
    PrivateEndpointOverrideTypeDef, PrivateEndpointOverrideOutputTypeDef
]

class DiscoveryConfigurationOutputTypeDef(TypedDict):
    authorizerConfiguration: NotRequired[AuthorizerConfigurationOutputTypeDef]
    authorizerType: NotRequired[RegistryAuthorizerTypeType]

class A2aAgentCardDescriptorOutputTypeDef(TypedDict):
    data: NotRequired[str]
    dataSchemaVersion: NotRequired[str]
    source: NotRequired[DescriptorSourceOutputTypeDef]

class AgentSkillsMdDescriptorOutputTypeDef(TypedDict):
    data: NotRequired[str]
    dataSchemaVersion: NotRequired[str]
    source: NotRequired[DescriptorSourceOutputTypeDef]

class McpServerDescriptorOutputTypeDef(TypedDict):
    data: NotRequired[str]
    dataSchemaVersion: NotRequired[str]
    additionalData: NotRequired[McpServerAdditionalDataTypeDef]
    source: NotRequired[DescriptorSourceOutputTypeDef]

RegistryRecordCredentialProviderConfigurationUnionTypeDef = Union[
    RegistryRecordCredentialProviderConfigurationTypeDef,
    RegistryRecordCredentialProviderConfigurationOutputTypeDef,
]

class CustomJWTAuthorizerConfigurationTypeDef(TypedDict):
    discoveryUrl: str
    allowedAudience: NotRequired[Sequence[str]]
    allowedClients: NotRequired[Sequence[str]]
    allowedScopes: NotRequired[Sequence[str]]
    customClaims: NotRequired[Sequence[CustomClaimValidationTypeUnionTypeDef]]
    privateEndpoint: NotRequired[PrivateEndpointUnionTypeDef]
    privateEndpointOverrides: NotRequired[Sequence[PrivateEndpointOverrideUnionTypeDef]]

class GetRegistryResponseTypeDef(TypedDict):
    name: str
    description: str
    registryId: str
    registryArn: str
    discoveryConfiguration: DiscoveryConfigurationOutputTypeDef
    approvalConfiguration: ApprovalConfigurationOutputTypeDef
    status: RegistryStatusType
    statusReason: str
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class RegistrySummaryTypeDef(TypedDict):
    name: str
    registryId: str
    registryArn: str
    status: RegistryStatusType
    createdAt: datetime
    updatedAt: datetime
    description: NotRequired[str]
    discoveryConfiguration: NotRequired[DiscoveryConfigurationOutputTypeDef]
    statusReason: NotRequired[str]

class UpdateRegistryResponseTypeDef(TypedDict):
    name: str
    description: str
    registryId: str
    registryArn: str
    discoveryConfiguration: DiscoveryConfigurationOutputTypeDef
    approvalConfiguration: ApprovalConfigurationOutputTypeDef
    status: RegistryStatusType
    statusReason: str
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class AgentSkillsAdditionalDataOutputTypeDef(TypedDict):
    skillMd: NotRequired[AgentSkillsMdDescriptorOutputTypeDef]

class DescriptorSourceFromUrlTypeDef(TypedDict):
    url: str
    credentialProviderConfigurations: NotRequired[
        Sequence[RegistryRecordCredentialProviderConfigurationUnionTypeDef]
    ]

CustomJWTAuthorizerConfigurationUnionTypeDef = Union[
    CustomJWTAuthorizerConfigurationTypeDef, CustomJWTAuthorizerConfigurationOutputTypeDef
]

class ListRegistriesResponseTypeDef(TypedDict):
    registries: list[RegistrySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class AgentSkillsDefinitionDescriptorOutputTypeDef(TypedDict):
    data: NotRequired[str]
    dataSchemaVersion: NotRequired[str]
    additionalData: NotRequired[AgentSkillsAdditionalDataOutputTypeDef]

DescriptorSourceFromUrlUnionTypeDef = Union[
    DescriptorSourceFromUrlTypeDef, DescriptorSourceFromUrlOutputTypeDef
]

class AuthorizerConfigurationTypeDef(TypedDict):
    customJWTAuthorizer: NotRequired[CustomJWTAuthorizerConfigurationUnionTypeDef]

class DescriptorsOutputTypeDef(TypedDict):
    mcpServer: NotRequired[McpServerDescriptorOutputTypeDef]
    a2aAgentCard: NotRequired[A2aAgentCardDescriptorOutputTypeDef]
    agentSkillsDefinition: NotRequired[AgentSkillsDefinitionDescriptorOutputTypeDef]
    custom: NotRequired[CustomDescriptorTypeDef]

class DescriptorSourceTypeDef(TypedDict):
    fromUrl: NotRequired[DescriptorSourceFromUrlUnionTypeDef]

AuthorizerConfigurationUnionTypeDef = Union[
    AuthorizerConfigurationTypeDef, AuthorizerConfigurationOutputTypeDef
]

class DiscoveryConfigurationTypeDef(TypedDict):
    authorizerConfiguration: NotRequired[AuthorizerConfigurationTypeDef]
    authorizerType: NotRequired[RegistryAuthorizerTypeType]

class GetRegistryRecordResponseTypeDef(TypedDict):
    registryArn: str
    recordArn: str
    recordId: str
    name: str
    displayName: str
    description: str
    recordType: RecordTypeType
    descriptors: DescriptorsOutputTypeDef
    recordVersion: str
    status: RegistryRecordStatusType
    createdAt: datetime
    updatedAt: datetime
    statusReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRegistryRecordResponseTypeDef(TypedDict):
    registryArn: str
    recordArn: str
    recordId: str
    name: str
    displayName: str
    description: str
    recordType: RecordTypeType
    descriptors: DescriptorsOutputTypeDef
    recordVersion: str
    status: RegistryRecordStatusType
    createdAt: datetime
    updatedAt: datetime
    statusReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class A2aAgentCardDescriptorTypeDef(TypedDict):
    data: NotRequired[str]
    dataSchemaVersion: NotRequired[str]
    source: NotRequired[DescriptorSourceTypeDef]

class AgentSkillsMdDescriptorTypeDef(TypedDict):
    data: NotRequired[str]
    dataSchemaVersion: NotRequired[str]
    source: NotRequired[DescriptorSourceTypeDef]

DescriptorSourceUnionTypeDef = Union[DescriptorSourceTypeDef, DescriptorSourceOutputTypeDef]

class McpServerDescriptorTypeDef(TypedDict):
    data: NotRequired[str]
    dataSchemaVersion: NotRequired[str]
    additionalData: NotRequired[McpServerAdditionalDataTypeDef]
    source: NotRequired[DescriptorSourceTypeDef]

class UpdatedAuthorizerConfigurationTypeDef(TypedDict):
    optionalValue: NotRequired[AuthorizerConfigurationUnionTypeDef]

DiscoveryConfigurationUnionTypeDef = Union[
    DiscoveryConfigurationTypeDef, DiscoveryConfigurationOutputTypeDef
]

class AgentSkillsAdditionalDataTypeDef(TypedDict):
    skillMd: NotRequired[AgentSkillsMdDescriptorTypeDef]

class UpdatedDescriptorSourceTypeDef(TypedDict):
    optionalValue: NotRequired[DescriptorSourceUnionTypeDef]

class UpdatedDiscoveryConfigurationTypeDef(TypedDict):
    authorizerConfiguration: NotRequired[UpdatedAuthorizerConfigurationTypeDef]

class CreateRegistryRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    discoveryConfiguration: NotRequired[DiscoveryConfigurationUnionTypeDef]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]
    approvalConfiguration: NotRequired[ApprovalConfigurationUnionTypeDef]

class AgentSkillsDefinitionDescriptorTypeDef(TypedDict):
    data: NotRequired[str]
    dataSchemaVersion: NotRequired[str]
    additionalData: NotRequired[AgentSkillsAdditionalDataTypeDef]

class UpdatedA2aAgentCardDescriptorFieldsTypeDef(TypedDict):
    data: NotRequired[UpdatedDescriptorDataTypeDef]
    dataSchemaVersion: NotRequired[UpdatedDataSchemaVersionTypeDef]
    source: NotRequired[UpdatedDescriptorSourceTypeDef]

class UpdatedAgentSkillsMdDescriptorFieldsTypeDef(TypedDict):
    data: NotRequired[UpdatedDescriptorDataTypeDef]
    dataSchemaVersion: NotRequired[UpdatedDataSchemaVersionTypeDef]
    source: NotRequired[UpdatedDescriptorSourceTypeDef]

class UpdatedMcpServerDescriptorFieldsTypeDef(TypedDict):
    data: NotRequired[UpdatedDescriptorDataTypeDef]
    dataSchemaVersion: NotRequired[UpdatedDataSchemaVersionTypeDef]
    source: NotRequired[UpdatedDescriptorSourceTypeDef]
    additionalData: NotRequired[UpdatedMcpServerAdditionalDataTypeDef]

class UpdateRegistryRequestTypeDef(TypedDict):
    registryId: str
    name: NotRequired[str]
    description: NotRequired[UpdatedDescriptionTypeDef]
    discoveryConfiguration: NotRequired[UpdatedDiscoveryConfigurationTypeDef]
    approvalConfiguration: NotRequired[UpdatedApprovalConfigurationTypeDef]

class DescriptorsTypeDef(TypedDict):
    mcpServer: NotRequired[McpServerDescriptorTypeDef]
    a2aAgentCard: NotRequired[A2aAgentCardDescriptorTypeDef]
    agentSkillsDefinition: NotRequired[AgentSkillsDefinitionDescriptorTypeDef]
    custom: NotRequired[CustomDescriptorTypeDef]

class UpdatedA2aAgentCardDescriptorTypeDef(TypedDict):
    optionalValue: NotRequired[UpdatedA2aAgentCardDescriptorFieldsTypeDef]

class UpdatedAgentSkillsMdDescriptorTypeDef(TypedDict):
    optionalValue: NotRequired[UpdatedAgentSkillsMdDescriptorFieldsTypeDef]

class UpdatedMcpServerDescriptorTypeDef(TypedDict):
    optionalValue: NotRequired[UpdatedMcpServerDescriptorFieldsTypeDef]

DescriptorsUnionTypeDef = Union[DescriptorsTypeDef, DescriptorsOutputTypeDef]

class UpdatedAgentSkillsAdditionalDataFieldsTypeDef(TypedDict):
    skillMd: NotRequired[UpdatedAgentSkillsMdDescriptorTypeDef]

class CreateRegistryRecordRequestTypeDef(TypedDict):
    registryId: str
    name: str
    recordType: RecordTypeType
    descriptors: DescriptorsUnionTypeDef
    displayName: NotRequired[str]
    description: NotRequired[str]
    recordVersion: NotRequired[str]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class UpdatedAgentSkillsAdditionalDataTypeDef(TypedDict):
    optionalValue: NotRequired[UpdatedAgentSkillsAdditionalDataFieldsTypeDef]

class UpdatedAgentSkillsDefinitionDescriptorFieldsTypeDef(TypedDict):
    data: NotRequired[UpdatedDescriptorDataTypeDef]
    dataSchemaVersion: NotRequired[UpdatedDataSchemaVersionTypeDef]
    additionalData: NotRequired[UpdatedAgentSkillsAdditionalDataTypeDef]

class UpdatedAgentSkillsDefinitionDescriptorTypeDef(TypedDict):
    optionalValue: NotRequired[UpdatedAgentSkillsDefinitionDescriptorFieldsTypeDef]

class UpdatedDescriptorsFieldsTypeDef(TypedDict):
    mcpServer: NotRequired[UpdatedMcpServerDescriptorTypeDef]
    a2aAgentCard: NotRequired[UpdatedA2aAgentCardDescriptorTypeDef]
    agentSkillsDefinition: NotRequired[UpdatedAgentSkillsDefinitionDescriptorTypeDef]
    custom: NotRequired[UpdatedCustomDescriptorTypeDef]

class UpdatedDescriptorsTypeDef(TypedDict):
    optionalValue: NotRequired[UpdatedDescriptorsFieldsTypeDef]

class UpdateRegistryRecordRequestTypeDef(TypedDict):
    registryId: str
    recordId: str
    name: NotRequired[str]
    displayName: NotRequired[UpdatedDisplayNameTypeDef]
    description: NotRequired[UpdatedDescriptionTypeDef]
    recordType: NotRequired[RecordTypeType]
    descriptors: NotRequired[UpdatedDescriptorsTypeDef]
    recordVersion: NotRequired[str]
    triggerSynchronization: NotRequired[bool]
