"""
Type annotations for bedrock-agentcore-control service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from types_boto3_bedrock_agentcore_control.type_defs import ContainerConfigurationTypeDef

    data: ContainerConfigurationTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Any, Union

from .literals import (
    AgentEndpointStatusType,
    AgentStatusType,
    ApiKeyCredentialLocationType,
    BrowserStatusType,
    CodeInterpreterNetworkModeType,
    CodeInterpreterStatusType,
    CredentialProviderTypeType,
    CredentialProviderVendorTypeType,
    GatewayStatusType,
    KeyTypeType,
    MemoryStatusType,
    MemoryStrategyStatusType,
    MemoryStrategyTypeType,
    OverrideTypeType,
    ResourceTypeType,
    SchemaTypeType,
    ServerProtocolType,
    TargetStatusType,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import list as List
    from collections.abc import Mapping, Sequence
else:
    from typing import Dict, List, Mapping, Sequence
if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "AgentArtifactTypeDef",
    "AgentEndpointTypeDef",
    "AgentTypeDef",
    "ApiKeyCredentialProviderItemTypeDef",
    "ApiKeyCredentialProviderTypeDef",
    "ApiSchemaConfigurationTypeDef",
    "AuthorizerConfigurationOutputTypeDef",
    "AuthorizerConfigurationTypeDef",
    "AuthorizerConfigurationUnionTypeDef",
    "BrowserNetworkConfigurationTypeDef",
    "BrowserSummaryTypeDef",
    "CodeInterpreterNetworkConfigurationTypeDef",
    "CodeInterpreterSummaryTypeDef",
    "ConsolidationConfigurationTypeDef",
    "ContainerConfigurationTypeDef",
    "CreateAgentRuntimeEndpointRequestTypeDef",
    "CreateAgentRuntimeEndpointResponseTypeDef",
    "CreateAgentRuntimeRequestTypeDef",
    "CreateAgentRuntimeResponseTypeDef",
    "CreateApiKeyCredentialProviderRequestTypeDef",
    "CreateApiKeyCredentialProviderResponseTypeDef",
    "CreateBrowserRequestTypeDef",
    "CreateBrowserResponseTypeDef",
    "CreateCodeInterpreterRequestTypeDef",
    "CreateCodeInterpreterResponseTypeDef",
    "CreateGatewayRequestTypeDef",
    "CreateGatewayResponseTypeDef",
    "CreateGatewayTargetRequestTypeDef",
    "CreateGatewayTargetResponseTypeDef",
    "CreateMemoryInputTypeDef",
    "CreateMemoryOutputTypeDef",
    "CreateOauth2CredentialProviderRequestTypeDef",
    "CreateOauth2CredentialProviderResponseTypeDef",
    "CreateWorkloadIdentityRequestTypeDef",
    "CreateWorkloadIdentityResponseTypeDef",
    "CredentialProviderConfigurationOutputTypeDef",
    "CredentialProviderConfigurationTypeDef",
    "CredentialProviderConfigurationUnionTypeDef",
    "CredentialProviderOutputTypeDef",
    "CredentialProviderTypeDef",
    "CredentialProviderUnionTypeDef",
    "CustomConfigurationInputTypeDef",
    "CustomConsolidationConfigurationInputTypeDef",
    "CustomConsolidationConfigurationTypeDef",
    "CustomExtractionConfigurationInputTypeDef",
    "CustomExtractionConfigurationTypeDef",
    "CustomJWTAuthorizerConfigurationOutputTypeDef",
    "CustomJWTAuthorizerConfigurationTypeDef",
    "CustomMemoryStrategyInputTypeDef",
    "CustomOauth2ProviderConfigInputTypeDef",
    "CustomOauth2ProviderConfigOutputTypeDef",
    "DeleteAgentRuntimeEndpointRequestTypeDef",
    "DeleteAgentRuntimeEndpointResponseTypeDef",
    "DeleteAgentRuntimeRequestTypeDef",
    "DeleteAgentRuntimeResponseTypeDef",
    "DeleteApiKeyCredentialProviderRequestTypeDef",
    "DeleteBrowserRequestTypeDef",
    "DeleteBrowserResponseTypeDef",
    "DeleteCodeInterpreterRequestTypeDef",
    "DeleteCodeInterpreterResponseTypeDef",
    "DeleteGatewayRequestTypeDef",
    "DeleteGatewayResponseTypeDef",
    "DeleteGatewayTargetRequestTypeDef",
    "DeleteGatewayTargetResponseTypeDef",
    "DeleteMemoryInputTypeDef",
    "DeleteMemoryOutputTypeDef",
    "DeleteMemoryStrategyInputTypeDef",
    "DeleteOauth2CredentialProviderRequestTypeDef",
    "DeleteWorkloadIdentityRequestTypeDef",
    "ExtractionConfigurationTypeDef",
    "GatewayProtocolConfigurationOutputTypeDef",
    "GatewayProtocolConfigurationTypeDef",
    "GatewayProtocolConfigurationUnionTypeDef",
    "GatewaySummaryTypeDef",
    "GetAgentRuntimeEndpointRequestTypeDef",
    "GetAgentRuntimeEndpointResponseTypeDef",
    "GetAgentRuntimeRequestTypeDef",
    "GetAgentRuntimeResponseTypeDef",
    "GetApiKeyCredentialProviderRequestTypeDef",
    "GetApiKeyCredentialProviderResponseTypeDef",
    "GetBrowserRequestTypeDef",
    "GetBrowserResponseTypeDef",
    "GetCodeInterpreterRequestTypeDef",
    "GetCodeInterpreterResponseTypeDef",
    "GetGatewayRequestTypeDef",
    "GetGatewayResponseTypeDef",
    "GetGatewayTargetRequestTypeDef",
    "GetGatewayTargetResponseTypeDef",
    "GetMemoryInputTypeDef",
    "GetMemoryInputWaitTypeDef",
    "GetMemoryOutputTypeDef",
    "GetOauth2CredentialProviderRequestTypeDef",
    "GetOauth2CredentialProviderResponseTypeDef",
    "GetTokenVaultRequestTypeDef",
    "GetTokenVaultResponseTypeDef",
    "GetWorkloadIdentityRequestTypeDef",
    "GetWorkloadIdentityResponseTypeDef",
    "GithubOauth2ProviderConfigInputTypeDef",
    "GithubOauth2ProviderConfigOutputTypeDef",
    "GoogleOauth2ProviderConfigInputTypeDef",
    "GoogleOauth2ProviderConfigOutputTypeDef",
    "KmsConfigurationTypeDef",
    "ListAgentRuntimeEndpointsRequestPaginateTypeDef",
    "ListAgentRuntimeEndpointsRequestTypeDef",
    "ListAgentRuntimeEndpointsResponseTypeDef",
    "ListAgentRuntimeVersionsRequestPaginateTypeDef",
    "ListAgentRuntimeVersionsRequestTypeDef",
    "ListAgentRuntimeVersionsResponseTypeDef",
    "ListAgentRuntimesRequestPaginateTypeDef",
    "ListAgentRuntimesRequestTypeDef",
    "ListAgentRuntimesResponseTypeDef",
    "ListApiKeyCredentialProvidersRequestPaginateTypeDef",
    "ListApiKeyCredentialProvidersRequestTypeDef",
    "ListApiKeyCredentialProvidersResponseTypeDef",
    "ListBrowsersRequestPaginateTypeDef",
    "ListBrowsersRequestTypeDef",
    "ListBrowsersResponseTypeDef",
    "ListCodeInterpretersRequestPaginateTypeDef",
    "ListCodeInterpretersRequestTypeDef",
    "ListCodeInterpretersResponseTypeDef",
    "ListGatewayTargetsRequestPaginateTypeDef",
    "ListGatewayTargetsRequestTypeDef",
    "ListGatewayTargetsResponseTypeDef",
    "ListGatewaysRequestPaginateTypeDef",
    "ListGatewaysRequestTypeDef",
    "ListGatewaysResponseTypeDef",
    "ListMemoriesInputPaginateTypeDef",
    "ListMemoriesInputTypeDef",
    "ListMemoriesOutputTypeDef",
    "ListOauth2CredentialProvidersRequestPaginateTypeDef",
    "ListOauth2CredentialProvidersRequestTypeDef",
    "ListOauth2CredentialProvidersResponseTypeDef",
    "ListWorkloadIdentitiesRequestPaginateTypeDef",
    "ListWorkloadIdentitiesRequestTypeDef",
    "ListWorkloadIdentitiesResponseTypeDef",
    "MCPGatewayConfigurationOutputTypeDef",
    "MCPGatewayConfigurationTypeDef",
    "McpLambdaTargetConfigurationOutputTypeDef",
    "McpLambdaTargetConfigurationTypeDef",
    "McpTargetConfigurationOutputTypeDef",
    "McpTargetConfigurationTypeDef",
    "MemoryStrategyInputTypeDef",
    "MemoryStrategyTypeDef",
    "MemorySummaryTypeDef",
    "MemoryTypeDef",
    "MicrosoftOauth2ProviderConfigInputTypeDef",
    "MicrosoftOauth2ProviderConfigOutputTypeDef",
    "ModifyConsolidationConfigurationTypeDef",
    "ModifyExtractionConfigurationTypeDef",
    "ModifyMemoryStrategiesTypeDef",
    "ModifyMemoryStrategyInputTypeDef",
    "ModifyStrategyConfigurationTypeDef",
    "NetworkConfigurationTypeDef",
    "OAuthCredentialProviderOutputTypeDef",
    "OAuthCredentialProviderTypeDef",
    "OAuthCredentialProviderUnionTypeDef",
    "Oauth2AuthorizationServerMetadataOutputTypeDef",
    "Oauth2AuthorizationServerMetadataTypeDef",
    "Oauth2AuthorizationServerMetadataUnionTypeDef",
    "Oauth2CredentialProviderItemTypeDef",
    "Oauth2DiscoveryOutputTypeDef",
    "Oauth2DiscoveryTypeDef",
    "Oauth2DiscoveryUnionTypeDef",
    "Oauth2ProviderConfigInputTypeDef",
    "Oauth2ProviderConfigOutputTypeDef",
    "PaginatorConfigTypeDef",
    "ProtocolConfigurationTypeDef",
    "RecordingConfigTypeDef",
    "ResponseMetadataTypeDef",
    "S3ConfigurationTypeDef",
    "S3LocationTypeDef",
    "SalesforceOauth2ProviderConfigInputTypeDef",
    "SalesforceOauth2ProviderConfigOutputTypeDef",
    "SchemaDefinitionOutputTypeDef",
    "SchemaDefinitionTypeDef",
    "SecretTypeDef",
    "SemanticConsolidationOverrideTypeDef",
    "SemanticExtractionOverrideTypeDef",
    "SemanticMemoryStrategyInputTypeDef",
    "SemanticOverrideConfigurationInputTypeDef",
    "SemanticOverrideConsolidationConfigurationInputTypeDef",
    "SemanticOverrideExtractionConfigurationInputTypeDef",
    "SetTokenVaultCMKRequestTypeDef",
    "SetTokenVaultCMKResponseTypeDef",
    "SlackOauth2ProviderConfigInputTypeDef",
    "SlackOauth2ProviderConfigOutputTypeDef",
    "StrategyConfigurationTypeDef",
    "SummaryConsolidationOverrideTypeDef",
    "SummaryMemoryStrategyInputTypeDef",
    "SummaryOverrideConfigurationInputTypeDef",
    "SummaryOverrideConsolidationConfigurationInputTypeDef",
    "TargetConfigurationOutputTypeDef",
    "TargetConfigurationTypeDef",
    "TargetConfigurationUnionTypeDef",
    "TargetSummaryTypeDef",
    "ToolDefinitionOutputTypeDef",
    "ToolDefinitionTypeDef",
    "ToolSchemaOutputTypeDef",
    "ToolSchemaTypeDef",
    "UpdateAgentRuntimeEndpointRequestTypeDef",
    "UpdateAgentRuntimeEndpointResponseTypeDef",
    "UpdateAgentRuntimeRequestTypeDef",
    "UpdateAgentRuntimeResponseTypeDef",
    "UpdateApiKeyCredentialProviderRequestTypeDef",
    "UpdateApiKeyCredentialProviderResponseTypeDef",
    "UpdateGatewayRequestTypeDef",
    "UpdateGatewayResponseTypeDef",
    "UpdateGatewayTargetRequestTypeDef",
    "UpdateGatewayTargetResponseTypeDef",
    "UpdateMemoryInputTypeDef",
    "UpdateMemoryOutputTypeDef",
    "UpdateOauth2CredentialProviderRequestTypeDef",
    "UpdateOauth2CredentialProviderResponseTypeDef",
    "UpdateWorkloadIdentityRequestTypeDef",
    "UpdateWorkloadIdentityResponseTypeDef",
    "UserPreferenceConsolidationOverrideTypeDef",
    "UserPreferenceExtractionOverrideTypeDef",
    "UserPreferenceMemoryStrategyInputTypeDef",
    "UserPreferenceOverrideConfigurationInputTypeDef",
    "UserPreferenceOverrideConsolidationConfigurationInputTypeDef",
    "UserPreferenceOverrideExtractionConfigurationInputTypeDef",
    "WaiterConfigTypeDef",
    "WorkloadIdentityDetailsTypeDef",
    "WorkloadIdentityTypeTypeDef",
)

class ContainerConfigurationTypeDef(TypedDict):
    containerUri: str

AgentEndpointTypeDef = TypedDict(
    "AgentEndpointTypeDef",
    {
        "name": str,
        "agentRuntimeEndpointArn": str,
        "agentRuntimeArn": str,
        "status": AgentEndpointStatusType,
        "id": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "liveVersion": NotRequired[str],
        "targetVersion": NotRequired[str],
        "description": NotRequired[str],
    },
)

class AgentTypeDef(TypedDict):
    agentRuntimeArn: str
    agentRuntimeId: str
    agentRuntimeVersion: str
    agentRuntimeName: str
    description: str
    lastUpdatedAt: datetime
    status: AgentStatusType

class ApiKeyCredentialProviderItemTypeDef(TypedDict):
    name: str
    credentialProviderArn: str
    createdTime: datetime
    lastUpdatedTime: datetime

class ApiKeyCredentialProviderTypeDef(TypedDict):
    providerArn: str
    credentialParameterName: NotRequired[str]
    credentialPrefix: NotRequired[str]
    credentialLocation: NotRequired[ApiKeyCredentialLocationType]

class S3ConfigurationTypeDef(TypedDict):
    uri: NotRequired[str]
    bucketOwnerAccountId: NotRequired[str]

class CustomJWTAuthorizerConfigurationOutputTypeDef(TypedDict):
    discoveryUrl: str
    allowedAudience: NotRequired[List[str]]
    allowedClients: NotRequired[List[str]]

class CustomJWTAuthorizerConfigurationTypeDef(TypedDict):
    discoveryUrl: str
    allowedAudience: NotRequired[Sequence[str]]
    allowedClients: NotRequired[Sequence[str]]

class BrowserNetworkConfigurationTypeDef(TypedDict):
    networkMode: Literal["PUBLIC"]

class BrowserSummaryTypeDef(TypedDict):
    browserId: str
    browserArn: str
    status: BrowserStatusType
    createdAt: datetime
    name: NotRequired[str]
    description: NotRequired[str]
    lastUpdatedAt: NotRequired[datetime]

class CodeInterpreterNetworkConfigurationTypeDef(TypedDict):
    networkMode: CodeInterpreterNetworkModeType

class CodeInterpreterSummaryTypeDef(TypedDict):
    codeInterpreterId: str
    codeInterpreterArn: str
    status: CodeInterpreterStatusType
    createdAt: datetime
    name: NotRequired[str]
    description: NotRequired[str]
    lastUpdatedAt: NotRequired[datetime]

class CreateAgentRuntimeEndpointRequestTypeDef(TypedDict):
    agentRuntimeId: str
    name: str
    agentRuntimeVersion: NotRequired[str]
    description: NotRequired[str]
    clientToken: NotRequired[str]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class NetworkConfigurationTypeDef(TypedDict):
    networkMode: Literal["PUBLIC"]

class ProtocolConfigurationTypeDef(TypedDict):
    serverProtocol: ServerProtocolType

class WorkloadIdentityDetailsTypeDef(TypedDict):
    workloadIdentityArn: str

class CreateApiKeyCredentialProviderRequestTypeDef(TypedDict):
    name: str
    apiKey: str

class SecretTypeDef(TypedDict):
    secretArn: str

class CreateWorkloadIdentityRequestTypeDef(TypedDict):
    name: str
    allowedResourceOauth2ReturnUrls: NotRequired[Sequence[str]]

class OAuthCredentialProviderOutputTypeDef(TypedDict):
    providerArn: str
    scopes: List[str]
    customParameters: NotRequired[Dict[str, str]]

class SemanticOverrideConsolidationConfigurationInputTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str

class SummaryOverrideConsolidationConfigurationInputTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str

class UserPreferenceOverrideConsolidationConfigurationInputTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str

class SemanticConsolidationOverrideTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str

class SummaryConsolidationOverrideTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str

class UserPreferenceConsolidationOverrideTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str

class SemanticOverrideExtractionConfigurationInputTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str

class UserPreferenceOverrideExtractionConfigurationInputTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str

class SemanticExtractionOverrideTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str

class UserPreferenceExtractionOverrideTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str

class DeleteAgentRuntimeEndpointRequestTypeDef(TypedDict):
    agentRuntimeId: str
    endpointName: str
    clientToken: NotRequired[str]

class DeleteAgentRuntimeRequestTypeDef(TypedDict):
    agentRuntimeId: str

class DeleteApiKeyCredentialProviderRequestTypeDef(TypedDict):
    name: str

class DeleteBrowserRequestTypeDef(TypedDict):
    browserId: str
    clientToken: NotRequired[str]

class DeleteCodeInterpreterRequestTypeDef(TypedDict):
    codeInterpreterId: str
    clientToken: NotRequired[str]

class DeleteGatewayRequestTypeDef(TypedDict):
    gatewayIdentifier: str

class DeleteGatewayTargetRequestTypeDef(TypedDict):
    gatewayIdentifier: str
    targetId: str

class DeleteMemoryInputTypeDef(TypedDict):
    memoryId: str
    clientToken: NotRequired[str]

class DeleteMemoryStrategyInputTypeDef(TypedDict):
    memoryStrategyId: str

class DeleteOauth2CredentialProviderRequestTypeDef(TypedDict):
    name: str

class DeleteWorkloadIdentityRequestTypeDef(TypedDict):
    name: str

class MCPGatewayConfigurationOutputTypeDef(TypedDict):
    supportedVersions: NotRequired[List[str]]
    instructions: NotRequired[str]
    searchType: NotRequired[Literal["SEMANTIC"]]

class MCPGatewayConfigurationTypeDef(TypedDict):
    supportedVersions: NotRequired[Sequence[str]]
    instructions: NotRequired[str]
    searchType: NotRequired[Literal["SEMANTIC"]]

class GatewaySummaryTypeDef(TypedDict):
    gatewayId: str
    name: str
    status: GatewayStatusType
    createdAt: datetime
    updatedAt: datetime
    authorizerType: Literal["CUSTOM_JWT"]
    protocolType: Literal["MCP"]
    description: NotRequired[str]

class GetAgentRuntimeEndpointRequestTypeDef(TypedDict):
    agentRuntimeId: str
    endpointName: str

class GetAgentRuntimeRequestTypeDef(TypedDict):
    agentRuntimeId: str
    agentRuntimeVersion: NotRequired[str]

class GetApiKeyCredentialProviderRequestTypeDef(TypedDict):
    name: str

class GetBrowserRequestTypeDef(TypedDict):
    browserId: str

class GetCodeInterpreterRequestTypeDef(TypedDict):
    codeInterpreterId: str

class GetGatewayRequestTypeDef(TypedDict):
    gatewayIdentifier: str

class GetGatewayTargetRequestTypeDef(TypedDict):
    gatewayIdentifier: str
    targetId: str

class GetMemoryInputTypeDef(TypedDict):
    memoryId: str

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class GetOauth2CredentialProviderRequestTypeDef(TypedDict):
    name: str

class GetTokenVaultRequestTypeDef(TypedDict):
    tokenVaultId: NotRequired[str]

class KmsConfigurationTypeDef(TypedDict):
    keyType: KeyTypeType
    kmsKeyArn: NotRequired[str]

class GetWorkloadIdentityRequestTypeDef(TypedDict):
    name: str

class GithubOauth2ProviderConfigInputTypeDef(TypedDict):
    clientId: str
    clientSecret: str

class GoogleOauth2ProviderConfigInputTypeDef(TypedDict):
    clientId: str
    clientSecret: str

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class ListAgentRuntimeEndpointsRequestTypeDef(TypedDict):
    agentRuntimeId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListAgentRuntimeVersionsRequestTypeDef(TypedDict):
    agentRuntimeId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListAgentRuntimesRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListApiKeyCredentialProvidersRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

ListBrowsersRequestTypeDef = TypedDict(
    "ListBrowsersRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "type": NotRequired[ResourceTypeType],
    },
)
ListCodeInterpretersRequestTypeDef = TypedDict(
    "ListCodeInterpretersRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "type": NotRequired[ResourceTypeType],
    },
)

class ListGatewayTargetsRequestTypeDef(TypedDict):
    gatewayIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class TargetSummaryTypeDef(TypedDict):
    targetId: str
    name: str
    status: TargetStatusType
    createdAt: datetime
    updatedAt: datetime
    description: NotRequired[str]

class ListGatewaysRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListMemoriesInputTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

MemorySummaryTypeDef = TypedDict(
    "MemorySummaryTypeDef",
    {
        "createdAt": datetime,
        "updatedAt": datetime,
        "arn": NotRequired[str],
        "id": NotRequired[str],
        "status": NotRequired[MemoryStatusType],
    },
)

class ListOauth2CredentialProvidersRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class Oauth2CredentialProviderItemTypeDef(TypedDict):
    name: str
    credentialProviderVendor: CredentialProviderVendorTypeType
    credentialProviderArn: str
    createdTime: datetime
    lastUpdatedTime: datetime

class ListWorkloadIdentitiesRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class WorkloadIdentityTypeTypeDef(TypedDict):
    name: str
    workloadIdentityArn: str

class SemanticMemoryStrategyInputTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    namespaces: NotRequired[Sequence[str]]

class SummaryMemoryStrategyInputTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    namespaces: NotRequired[Sequence[str]]

class UserPreferenceMemoryStrategyInputTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    namespaces: NotRequired[Sequence[str]]

class MicrosoftOauth2ProviderConfigInputTypeDef(TypedDict):
    clientId: str
    clientSecret: str

class OAuthCredentialProviderTypeDef(TypedDict):
    providerArn: str
    scopes: Sequence[str]
    customParameters: NotRequired[Mapping[str, str]]

class Oauth2AuthorizationServerMetadataOutputTypeDef(TypedDict):
    issuer: str
    authorizationEndpoint: str
    tokenEndpoint: str
    responseTypes: NotRequired[List[str]]

class Oauth2AuthorizationServerMetadataTypeDef(TypedDict):
    issuer: str
    authorizationEndpoint: str
    tokenEndpoint: str
    responseTypes: NotRequired[Sequence[str]]

class SalesforceOauth2ProviderConfigInputTypeDef(TypedDict):
    clientId: str
    clientSecret: str

class SlackOauth2ProviderConfigInputTypeDef(TypedDict):
    clientId: str
    clientSecret: str

class S3LocationTypeDef(TypedDict):
    bucket: str
    prefix: str

SchemaDefinitionOutputTypeDef = TypedDict(
    "SchemaDefinitionOutputTypeDef",
    {
        "type": SchemaTypeType,
        "properties": NotRequired[Dict[str, Dict[str, Any]]],
        "required": NotRequired[List[str]],
        "items": NotRequired[Dict[str, Any]],
        "description": NotRequired[str],
    },
)
SchemaDefinitionTypeDef = TypedDict(
    "SchemaDefinitionTypeDef",
    {
        "type": SchemaTypeType,
        "properties": NotRequired[Mapping[str, Mapping[str, Any]]],
        "required": NotRequired[Sequence[str]],
        "items": NotRequired[Mapping[str, Any]],
        "description": NotRequired[str],
    },
)

class UpdateAgentRuntimeEndpointRequestTypeDef(TypedDict):
    agentRuntimeId: str
    endpointName: str
    agentRuntimeVersion: NotRequired[str]
    description: NotRequired[str]
    clientToken: NotRequired[str]

class UpdateApiKeyCredentialProviderRequestTypeDef(TypedDict):
    name: str
    apiKey: str

class UpdateWorkloadIdentityRequestTypeDef(TypedDict):
    name: str
    allowedResourceOauth2ReturnUrls: NotRequired[Sequence[str]]

class AgentArtifactTypeDef(TypedDict):
    containerConfiguration: NotRequired[ContainerConfigurationTypeDef]

class ApiSchemaConfigurationTypeDef(TypedDict):
    s3: NotRequired[S3ConfigurationTypeDef]
    inlinePayload: NotRequired[str]

class AuthorizerConfigurationOutputTypeDef(TypedDict):
    customJWTAuthorizer: NotRequired[CustomJWTAuthorizerConfigurationOutputTypeDef]

class AuthorizerConfigurationTypeDef(TypedDict):
    customJWTAuthorizer: NotRequired[CustomJWTAuthorizerConfigurationTypeDef]

class CreateCodeInterpreterRequestTypeDef(TypedDict):
    name: str
    networkConfiguration: CodeInterpreterNetworkConfigurationTypeDef
    description: NotRequired[str]
    executionRoleArn: NotRequired[str]
    clientToken: NotRequired[str]

class CreateAgentRuntimeEndpointResponseTypeDef(TypedDict):
    targetVersion: str
    agentRuntimeEndpointArn: str
    agentRuntimeArn: str
    status: AgentEndpointStatusType
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateBrowserResponseTypeDef(TypedDict):
    browserId: str
    browserArn: str
    createdAt: datetime
    status: BrowserStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateCodeInterpreterResponseTypeDef(TypedDict):
    codeInterpreterId: str
    codeInterpreterArn: str
    createdAt: datetime
    status: CodeInterpreterStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateWorkloadIdentityResponseTypeDef(TypedDict):
    name: str
    workloadIdentityArn: str
    allowedResourceOauth2ReturnUrls: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAgentRuntimeEndpointResponseTypeDef(TypedDict):
    status: AgentEndpointStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAgentRuntimeResponseTypeDef(TypedDict):
    status: AgentStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteBrowserResponseTypeDef(TypedDict):
    browserId: str
    status: BrowserStatusType
    lastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteCodeInterpreterResponseTypeDef(TypedDict):
    codeInterpreterId: str
    status: CodeInterpreterStatusType
    lastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteGatewayResponseTypeDef(TypedDict):
    gatewayId: str
    status: GatewayStatusType
    statusReasons: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteGatewayTargetResponseTypeDef(TypedDict):
    gatewayArn: str
    targetId: str
    status: TargetStatusType
    statusReasons: List[str]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteMemoryOutputTypeDef(TypedDict):
    memoryId: str
    status: MemoryStatusType
    ResponseMetadata: ResponseMetadataTypeDef

GetAgentRuntimeEndpointResponseTypeDef = TypedDict(
    "GetAgentRuntimeEndpointResponseTypeDef",
    {
        "liveVersion": str,
        "targetVersion": str,
        "agentRuntimeEndpointArn": str,
        "agentRuntimeArn": str,
        "description": str,
        "status": AgentEndpointStatusType,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "failureReason": str,
        "name": str,
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class GetCodeInterpreterResponseTypeDef(TypedDict):
    codeInterpreterId: str
    codeInterpreterArn: str
    name: str
    description: str
    executionRoleArn: str
    networkConfiguration: CodeInterpreterNetworkConfigurationTypeDef
    status: CodeInterpreterStatusType
    createdAt: datetime
    lastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetWorkloadIdentityResponseTypeDef(TypedDict):
    name: str
    workloadIdentityArn: str
    allowedResourceOauth2ReturnUrls: List[str]
    createdTime: datetime
    lastUpdatedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ListAgentRuntimeEndpointsResponseTypeDef(TypedDict):
    runtimeEndpoints: List[AgentEndpointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAgentRuntimeVersionsResponseTypeDef(TypedDict):
    agentRuntimes: List[AgentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAgentRuntimesResponseTypeDef(TypedDict):
    agentRuntimes: List[AgentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListApiKeyCredentialProvidersResponseTypeDef(TypedDict):
    credentialProviders: List[ApiKeyCredentialProviderItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListBrowsersResponseTypeDef(TypedDict):
    browserSummaries: List[BrowserSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListCodeInterpretersResponseTypeDef(TypedDict):
    codeInterpreterSummaries: List[CodeInterpreterSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdateAgentRuntimeEndpointResponseTypeDef(TypedDict):
    liveVersion: str
    targetVersion: str
    agentRuntimeEndpointArn: str
    agentRuntimeArn: str
    status: AgentEndpointStatusType
    createdAt: datetime
    lastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateWorkloadIdentityResponseTypeDef(TypedDict):
    name: str
    workloadIdentityArn: str
    allowedResourceOauth2ReturnUrls: List[str]
    createdTime: datetime
    lastUpdatedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAgentRuntimeResponseTypeDef(TypedDict):
    agentRuntimeArn: str
    workloadIdentityDetails: WorkloadIdentityDetailsTypeDef
    agentRuntimeId: str
    agentRuntimeVersion: str
    createdAt: datetime
    status: AgentStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAgentRuntimeResponseTypeDef(TypedDict):
    agentRuntimeArn: str
    agentRuntimeId: str
    workloadIdentityDetails: WorkloadIdentityDetailsTypeDef
    agentRuntimeVersion: str
    createdAt: datetime
    lastUpdatedAt: datetime
    status: AgentStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateApiKeyCredentialProviderResponseTypeDef(TypedDict):
    apiKeySecretArn: SecretTypeDef
    name: str
    credentialProviderArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateOauth2CredentialProviderResponseTypeDef(TypedDict):
    clientSecretArn: SecretTypeDef
    name: str
    credentialProviderArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetApiKeyCredentialProviderResponseTypeDef(TypedDict):
    apiKeySecretArn: SecretTypeDef
    name: str
    credentialProviderArn: str
    createdTime: datetime
    lastUpdatedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateApiKeyCredentialProviderResponseTypeDef(TypedDict):
    apiKeySecretArn: SecretTypeDef
    name: str
    credentialProviderArn: str
    createdTime: datetime
    lastUpdatedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CredentialProviderOutputTypeDef(TypedDict):
    oauthCredentialProvider: NotRequired[OAuthCredentialProviderOutputTypeDef]
    apiKeyCredentialProvider: NotRequired[ApiKeyCredentialProviderTypeDef]

class SummaryOverrideConfigurationInputTypeDef(TypedDict):
    consolidation: NotRequired[SummaryOverrideConsolidationConfigurationInputTypeDef]

class CustomConsolidationConfigurationInputTypeDef(TypedDict):
    semanticConsolidationOverride: NotRequired[
        SemanticOverrideConsolidationConfigurationInputTypeDef
    ]
    summaryConsolidationOverride: NotRequired[SummaryOverrideConsolidationConfigurationInputTypeDef]
    userPreferenceConsolidationOverride: NotRequired[
        UserPreferenceOverrideConsolidationConfigurationInputTypeDef
    ]

class CustomConsolidationConfigurationTypeDef(TypedDict):
    semanticConsolidationOverride: NotRequired[SemanticConsolidationOverrideTypeDef]
    summaryConsolidationOverride: NotRequired[SummaryConsolidationOverrideTypeDef]
    userPreferenceConsolidationOverride: NotRequired[UserPreferenceConsolidationOverrideTypeDef]

class SemanticOverrideConfigurationInputTypeDef(TypedDict):
    extraction: NotRequired[SemanticOverrideExtractionConfigurationInputTypeDef]
    consolidation: NotRequired[SemanticOverrideConsolidationConfigurationInputTypeDef]

class CustomExtractionConfigurationInputTypeDef(TypedDict):
    semanticExtractionOverride: NotRequired[SemanticOverrideExtractionConfigurationInputTypeDef]
    userPreferenceExtractionOverride: NotRequired[
        UserPreferenceOverrideExtractionConfigurationInputTypeDef
    ]

class UserPreferenceOverrideConfigurationInputTypeDef(TypedDict):
    extraction: NotRequired[UserPreferenceOverrideExtractionConfigurationInputTypeDef]
    consolidation: NotRequired[UserPreferenceOverrideConsolidationConfigurationInputTypeDef]

class CustomExtractionConfigurationTypeDef(TypedDict):
    semanticExtractionOverride: NotRequired[SemanticExtractionOverrideTypeDef]
    userPreferenceExtractionOverride: NotRequired[UserPreferenceExtractionOverrideTypeDef]

class GatewayProtocolConfigurationOutputTypeDef(TypedDict):
    mcp: NotRequired[MCPGatewayConfigurationOutputTypeDef]

class GatewayProtocolConfigurationTypeDef(TypedDict):
    mcp: NotRequired[MCPGatewayConfigurationTypeDef]

class ListGatewaysResponseTypeDef(TypedDict):
    items: List[GatewaySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetMemoryInputWaitTypeDef(TypedDict):
    memoryId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetTokenVaultResponseTypeDef(TypedDict):
    tokenVaultId: str
    kmsConfiguration: KmsConfigurationTypeDef
    lastModifiedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class SetTokenVaultCMKRequestTypeDef(TypedDict):
    kmsConfiguration: KmsConfigurationTypeDef
    tokenVaultId: NotRequired[str]

class SetTokenVaultCMKResponseTypeDef(TypedDict):
    tokenVaultId: str
    kmsConfiguration: KmsConfigurationTypeDef
    lastModifiedDate: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ListAgentRuntimeEndpointsRequestPaginateTypeDef(TypedDict):
    agentRuntimeId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAgentRuntimeVersionsRequestPaginateTypeDef(TypedDict):
    agentRuntimeId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListAgentRuntimesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListApiKeyCredentialProvidersRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListBrowsersRequestPaginateTypeDef = TypedDict(
    "ListBrowsersRequestPaginateTypeDef",
    {
        "type": NotRequired[ResourceTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListCodeInterpretersRequestPaginateTypeDef = TypedDict(
    "ListCodeInterpretersRequestPaginateTypeDef",
    {
        "type": NotRequired[ResourceTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

class ListGatewayTargetsRequestPaginateTypeDef(TypedDict):
    gatewayIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListGatewaysRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListMemoriesInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOauth2CredentialProvidersRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListWorkloadIdentitiesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListGatewayTargetsResponseTypeDef(TypedDict):
    items: List[TargetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListMemoriesOutputTypeDef(TypedDict):
    memories: List[MemorySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListOauth2CredentialProvidersResponseTypeDef(TypedDict):
    credentialProviders: List[Oauth2CredentialProviderItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListWorkloadIdentitiesResponseTypeDef(TypedDict):
    workloadIdentities: List[WorkloadIdentityTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

OAuthCredentialProviderUnionTypeDef = Union[
    OAuthCredentialProviderTypeDef, OAuthCredentialProviderOutputTypeDef
]

class Oauth2DiscoveryOutputTypeDef(TypedDict):
    discoveryUrl: NotRequired[str]
    authorizationServerMetadata: NotRequired[Oauth2AuthorizationServerMetadataOutputTypeDef]

Oauth2AuthorizationServerMetadataUnionTypeDef = Union[
    Oauth2AuthorizationServerMetadataTypeDef, Oauth2AuthorizationServerMetadataOutputTypeDef
]

class RecordingConfigTypeDef(TypedDict):
    enabled: NotRequired[bool]
    s3Location: NotRequired[S3LocationTypeDef]

class ToolDefinitionOutputTypeDef(TypedDict):
    name: str
    description: str
    inputSchema: SchemaDefinitionOutputTypeDef
    outputSchema: NotRequired[SchemaDefinitionOutputTypeDef]

class ToolDefinitionTypeDef(TypedDict):
    name: str
    description: str
    inputSchema: SchemaDefinitionTypeDef
    outputSchema: NotRequired[SchemaDefinitionTypeDef]

class GetAgentRuntimeResponseTypeDef(TypedDict):
    agentRuntimeArn: str
    workloadIdentityDetails: WorkloadIdentityDetailsTypeDef
    agentRuntimeName: str
    description: str
    agentRuntimeId: str
    agentRuntimeVersion: str
    createdAt: datetime
    lastUpdatedAt: datetime
    roleArn: str
    agentRuntimeArtifact: AgentArtifactTypeDef
    networkConfiguration: NetworkConfigurationTypeDef
    protocolConfiguration: ProtocolConfigurationTypeDef
    environmentVariables: Dict[str, str]
    authorizerConfiguration: AuthorizerConfigurationOutputTypeDef
    status: AgentStatusType
    ResponseMetadata: ResponseMetadataTypeDef

AuthorizerConfigurationUnionTypeDef = Union[
    AuthorizerConfigurationTypeDef, AuthorizerConfigurationOutputTypeDef
]

class CredentialProviderConfigurationOutputTypeDef(TypedDict):
    credentialProviderType: CredentialProviderTypeType
    credentialProvider: NotRequired[CredentialProviderOutputTypeDef]

class ModifyConsolidationConfigurationTypeDef(TypedDict):
    customConsolidationConfiguration: NotRequired[CustomConsolidationConfigurationInputTypeDef]

class ConsolidationConfigurationTypeDef(TypedDict):
    customConsolidationConfiguration: NotRequired[CustomConsolidationConfigurationTypeDef]

class ModifyExtractionConfigurationTypeDef(TypedDict):
    customExtractionConfiguration: NotRequired[CustomExtractionConfigurationInputTypeDef]

class CustomConfigurationInputTypeDef(TypedDict):
    semanticOverride: NotRequired[SemanticOverrideConfigurationInputTypeDef]
    summaryOverride: NotRequired[SummaryOverrideConfigurationInputTypeDef]
    userPreferenceOverride: NotRequired[UserPreferenceOverrideConfigurationInputTypeDef]

class ExtractionConfigurationTypeDef(TypedDict):
    customExtractionConfiguration: NotRequired[CustomExtractionConfigurationTypeDef]

class CreateGatewayResponseTypeDef(TypedDict):
    gatewayArn: str
    gatewayId: str
    gatewayUrl: str
    createdAt: datetime
    updatedAt: datetime
    status: GatewayStatusType
    statusReasons: List[str]
    name: str
    description: str
    roleArn: str
    protocolType: Literal["MCP"]
    protocolConfiguration: GatewayProtocolConfigurationOutputTypeDef
    authorizerType: Literal["CUSTOM_JWT"]
    authorizerConfiguration: AuthorizerConfigurationOutputTypeDef
    kmsKeyArn: str
    workloadIdentityDetails: WorkloadIdentityDetailsTypeDef
    exceptionLevel: Literal["DEBUG"]
    ResponseMetadata: ResponseMetadataTypeDef

class GetGatewayResponseTypeDef(TypedDict):
    gatewayArn: str
    gatewayId: str
    gatewayUrl: str
    createdAt: datetime
    updatedAt: datetime
    status: GatewayStatusType
    statusReasons: List[str]
    name: str
    description: str
    roleArn: str
    protocolType: Literal["MCP"]
    protocolConfiguration: GatewayProtocolConfigurationOutputTypeDef
    authorizerType: Literal["CUSTOM_JWT"]
    authorizerConfiguration: AuthorizerConfigurationOutputTypeDef
    kmsKeyArn: str
    workloadIdentityDetails: WorkloadIdentityDetailsTypeDef
    exceptionLevel: Literal["DEBUG"]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateGatewayResponseTypeDef(TypedDict):
    gatewayArn: str
    gatewayId: str
    gatewayUrl: str
    createdAt: datetime
    updatedAt: datetime
    status: GatewayStatusType
    statusReasons: List[str]
    name: str
    description: str
    roleArn: str
    protocolType: Literal["MCP"]
    protocolConfiguration: GatewayProtocolConfigurationOutputTypeDef
    authorizerType: Literal["CUSTOM_JWT"]
    authorizerConfiguration: AuthorizerConfigurationOutputTypeDef
    kmsKeyArn: str
    workloadIdentityDetails: WorkloadIdentityDetailsTypeDef
    exceptionLevel: Literal["DEBUG"]
    ResponseMetadata: ResponseMetadataTypeDef

GatewayProtocolConfigurationUnionTypeDef = Union[
    GatewayProtocolConfigurationTypeDef, GatewayProtocolConfigurationOutputTypeDef
]

class CredentialProviderTypeDef(TypedDict):
    oauthCredentialProvider: NotRequired[OAuthCredentialProviderUnionTypeDef]
    apiKeyCredentialProvider: NotRequired[ApiKeyCredentialProviderTypeDef]

class CustomOauth2ProviderConfigOutputTypeDef(TypedDict):
    oauthDiscovery: Oauth2DiscoveryOutputTypeDef

class GithubOauth2ProviderConfigOutputTypeDef(TypedDict):
    oauthDiscovery: Oauth2DiscoveryOutputTypeDef

class GoogleOauth2ProviderConfigOutputTypeDef(TypedDict):
    oauthDiscovery: Oauth2DiscoveryOutputTypeDef

class MicrosoftOauth2ProviderConfigOutputTypeDef(TypedDict):
    oauthDiscovery: Oauth2DiscoveryOutputTypeDef

class SalesforceOauth2ProviderConfigOutputTypeDef(TypedDict):
    oauthDiscovery: Oauth2DiscoveryOutputTypeDef

class SlackOauth2ProviderConfigOutputTypeDef(TypedDict):
    oauthDiscovery: Oauth2DiscoveryOutputTypeDef

class Oauth2DiscoveryTypeDef(TypedDict):
    discoveryUrl: NotRequired[str]
    authorizationServerMetadata: NotRequired[Oauth2AuthorizationServerMetadataUnionTypeDef]

class CreateBrowserRequestTypeDef(TypedDict):
    name: str
    networkConfiguration: BrowserNetworkConfigurationTypeDef
    description: NotRequired[str]
    executionRoleArn: NotRequired[str]
    recording: NotRequired[RecordingConfigTypeDef]
    clientToken: NotRequired[str]

class GetBrowserResponseTypeDef(TypedDict):
    browserId: str
    browserArn: str
    name: str
    description: str
    executionRoleArn: str
    networkConfiguration: BrowserNetworkConfigurationTypeDef
    recording: RecordingConfigTypeDef
    status: BrowserStatusType
    createdAt: datetime
    lastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ToolSchemaOutputTypeDef(TypedDict):
    s3: NotRequired[S3ConfigurationTypeDef]
    inlinePayload: NotRequired[List[ToolDefinitionOutputTypeDef]]

class ToolSchemaTypeDef(TypedDict):
    s3: NotRequired[S3ConfigurationTypeDef]
    inlinePayload: NotRequired[Sequence[ToolDefinitionTypeDef]]

class CreateAgentRuntimeRequestTypeDef(TypedDict):
    agentRuntimeName: str
    agentRuntimeArtifact: AgentArtifactTypeDef
    roleArn: str
    networkConfiguration: NetworkConfigurationTypeDef
    description: NotRequired[str]
    protocolConfiguration: NotRequired[ProtocolConfigurationTypeDef]
    clientToken: NotRequired[str]
    environmentVariables: NotRequired[Mapping[str, str]]
    authorizerConfiguration: NotRequired[AuthorizerConfigurationUnionTypeDef]

class UpdateAgentRuntimeRequestTypeDef(TypedDict):
    agentRuntimeId: str
    agentRuntimeArtifact: AgentArtifactTypeDef
    roleArn: str
    networkConfiguration: NetworkConfigurationTypeDef
    description: NotRequired[str]
    protocolConfiguration: NotRequired[ProtocolConfigurationTypeDef]
    clientToken: NotRequired[str]
    environmentVariables: NotRequired[Mapping[str, str]]
    authorizerConfiguration: NotRequired[AuthorizerConfigurationUnionTypeDef]

class ModifyStrategyConfigurationTypeDef(TypedDict):
    extraction: NotRequired[ModifyExtractionConfigurationTypeDef]
    consolidation: NotRequired[ModifyConsolidationConfigurationTypeDef]

class CustomMemoryStrategyInputTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    namespaces: NotRequired[Sequence[str]]
    configuration: NotRequired[CustomConfigurationInputTypeDef]

StrategyConfigurationTypeDef = TypedDict(
    "StrategyConfigurationTypeDef",
    {
        "type": NotRequired[OverrideTypeType],
        "extraction": NotRequired[ExtractionConfigurationTypeDef],
        "consolidation": NotRequired[ConsolidationConfigurationTypeDef],
    },
)

class CreateGatewayRequestTypeDef(TypedDict):
    name: str
    roleArn: str
    protocolType: Literal["MCP"]
    authorizerType: Literal["CUSTOM_JWT"]
    authorizerConfiguration: AuthorizerConfigurationUnionTypeDef
    description: NotRequired[str]
    clientToken: NotRequired[str]
    protocolConfiguration: NotRequired[GatewayProtocolConfigurationUnionTypeDef]
    kmsKeyArn: NotRequired[str]
    exceptionLevel: NotRequired[Literal["DEBUG"]]

class UpdateGatewayRequestTypeDef(TypedDict):
    gatewayIdentifier: str
    name: str
    roleArn: str
    protocolType: Literal["MCP"]
    authorizerType: Literal["CUSTOM_JWT"]
    authorizerConfiguration: AuthorizerConfigurationUnionTypeDef
    description: NotRequired[str]
    protocolConfiguration: NotRequired[GatewayProtocolConfigurationUnionTypeDef]
    kmsKeyArn: NotRequired[str]
    exceptionLevel: NotRequired[Literal["DEBUG"]]

CredentialProviderUnionTypeDef = Union[CredentialProviderTypeDef, CredentialProviderOutputTypeDef]

class Oauth2ProviderConfigOutputTypeDef(TypedDict):
    customOauth2ProviderConfig: NotRequired[CustomOauth2ProviderConfigOutputTypeDef]
    googleOauth2ProviderConfig: NotRequired[GoogleOauth2ProviderConfigOutputTypeDef]
    githubOauth2ProviderConfig: NotRequired[GithubOauth2ProviderConfigOutputTypeDef]
    slackOauth2ProviderConfig: NotRequired[SlackOauth2ProviderConfigOutputTypeDef]
    salesforceOauth2ProviderConfig: NotRequired[SalesforceOauth2ProviderConfigOutputTypeDef]
    microsoftOauth2ProviderConfig: NotRequired[MicrosoftOauth2ProviderConfigOutputTypeDef]

Oauth2DiscoveryUnionTypeDef = Union[Oauth2DiscoveryTypeDef, Oauth2DiscoveryOutputTypeDef]

class McpLambdaTargetConfigurationOutputTypeDef(TypedDict):
    lambdaArn: str
    toolSchema: ToolSchemaOutputTypeDef

class McpLambdaTargetConfigurationTypeDef(TypedDict):
    lambdaArn: str
    toolSchema: ToolSchemaTypeDef

class ModifyMemoryStrategyInputTypeDef(TypedDict):
    memoryStrategyId: str
    description: NotRequired[str]
    namespaces: NotRequired[Sequence[str]]
    configuration: NotRequired[ModifyStrategyConfigurationTypeDef]

class MemoryStrategyInputTypeDef(TypedDict):
    semanticMemoryStrategy: NotRequired[SemanticMemoryStrategyInputTypeDef]
    summaryMemoryStrategy: NotRequired[SummaryMemoryStrategyInputTypeDef]
    userPreferenceMemoryStrategy: NotRequired[UserPreferenceMemoryStrategyInputTypeDef]
    customMemoryStrategy: NotRequired[CustomMemoryStrategyInputTypeDef]

MemoryStrategyTypeDef = TypedDict(
    "MemoryStrategyTypeDef",
    {
        "strategyId": str,
        "name": str,
        "type": MemoryStrategyTypeType,
        "namespaces": List[str],
        "description": NotRequired[str],
        "configuration": NotRequired[StrategyConfigurationTypeDef],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "status": NotRequired[MemoryStrategyStatusType],
    },
)

class CredentialProviderConfigurationTypeDef(TypedDict):
    credentialProviderType: CredentialProviderTypeType
    credentialProvider: NotRequired[CredentialProviderUnionTypeDef]

class GetOauth2CredentialProviderResponseTypeDef(TypedDict):
    clientSecretArn: SecretTypeDef
    name: str
    credentialProviderArn: str
    credentialProviderVendor: CredentialProviderVendorTypeType
    oauth2ProviderConfigOutput: Oauth2ProviderConfigOutputTypeDef
    createdTime: datetime
    lastUpdatedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateOauth2CredentialProviderResponseTypeDef(TypedDict):
    clientSecretArn: SecretTypeDef
    name: str
    credentialProviderVendor: CredentialProviderVendorTypeType
    credentialProviderArn: str
    oauth2ProviderConfigOutput: Oauth2ProviderConfigOutputTypeDef
    createdTime: datetime
    lastUpdatedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CustomOauth2ProviderConfigInputTypeDef(TypedDict):
    oauthDiscovery: Oauth2DiscoveryUnionTypeDef
    clientId: str
    clientSecret: str

McpTargetConfigurationOutputTypeDef = TypedDict(
    "McpTargetConfigurationOutputTypeDef",
    {
        "openApiSchema": NotRequired[ApiSchemaConfigurationTypeDef],
        "smithyModel": NotRequired[ApiSchemaConfigurationTypeDef],
        "lambda": NotRequired[McpLambdaTargetConfigurationOutputTypeDef],
    },
)
McpTargetConfigurationTypeDef = TypedDict(
    "McpTargetConfigurationTypeDef",
    {
        "openApiSchema": NotRequired[ApiSchemaConfigurationTypeDef],
        "smithyModel": NotRequired[ApiSchemaConfigurationTypeDef],
        "lambda": NotRequired[McpLambdaTargetConfigurationTypeDef],
    },
)

class CreateMemoryInputTypeDef(TypedDict):
    name: str
    eventExpiryDuration: int
    clientToken: NotRequired[str]
    description: NotRequired[str]
    encryptionKeyArn: NotRequired[str]
    memoryExecutionRoleArn: NotRequired[str]
    memoryStrategies: NotRequired[Sequence[MemoryStrategyInputTypeDef]]

class ModifyMemoryStrategiesTypeDef(TypedDict):
    addMemoryStrategies: NotRequired[Sequence[MemoryStrategyInputTypeDef]]
    modifyMemoryStrategies: NotRequired[Sequence[ModifyMemoryStrategyInputTypeDef]]
    deleteMemoryStrategies: NotRequired[Sequence[DeleteMemoryStrategyInputTypeDef]]

MemoryTypeDef = TypedDict(
    "MemoryTypeDef",
    {
        "arn": str,
        "id": str,
        "name": str,
        "eventExpiryDuration": int,
        "status": MemoryStatusType,
        "createdAt": datetime,
        "updatedAt": datetime,
        "description": NotRequired[str],
        "encryptionKeyArn": NotRequired[str],
        "memoryExecutionRoleArn": NotRequired[str],
        "failureReason": NotRequired[str],
        "strategies": NotRequired[List[MemoryStrategyTypeDef]],
    },
)
CredentialProviderConfigurationUnionTypeDef = Union[
    CredentialProviderConfigurationTypeDef, CredentialProviderConfigurationOutputTypeDef
]

class Oauth2ProviderConfigInputTypeDef(TypedDict):
    customOauth2ProviderConfig: NotRequired[CustomOauth2ProviderConfigInputTypeDef]
    googleOauth2ProviderConfig: NotRequired[GoogleOauth2ProviderConfigInputTypeDef]
    githubOauth2ProviderConfig: NotRequired[GithubOauth2ProviderConfigInputTypeDef]
    slackOauth2ProviderConfig: NotRequired[SlackOauth2ProviderConfigInputTypeDef]
    salesforceOauth2ProviderConfig: NotRequired[SalesforceOauth2ProviderConfigInputTypeDef]
    microsoftOauth2ProviderConfig: NotRequired[MicrosoftOauth2ProviderConfigInputTypeDef]

class TargetConfigurationOutputTypeDef(TypedDict):
    mcp: NotRequired[McpTargetConfigurationOutputTypeDef]

class TargetConfigurationTypeDef(TypedDict):
    mcp: NotRequired[McpTargetConfigurationTypeDef]

class UpdateMemoryInputTypeDef(TypedDict):
    memoryId: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    eventExpiryDuration: NotRequired[int]
    memoryExecutionRoleArn: NotRequired[str]
    memoryStrategies: NotRequired[ModifyMemoryStrategiesTypeDef]

class CreateMemoryOutputTypeDef(TypedDict):
    memory: MemoryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetMemoryOutputTypeDef(TypedDict):
    memory: MemoryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateMemoryOutputTypeDef(TypedDict):
    memory: MemoryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class CreateOauth2CredentialProviderRequestTypeDef(TypedDict):
    name: str
    credentialProviderVendor: CredentialProviderVendorTypeType
    oauth2ProviderConfigInput: Oauth2ProviderConfigInputTypeDef

class UpdateOauth2CredentialProviderRequestTypeDef(TypedDict):
    name: str
    credentialProviderVendor: CredentialProviderVendorTypeType
    oauth2ProviderConfigInput: Oauth2ProviderConfigInputTypeDef

class CreateGatewayTargetResponseTypeDef(TypedDict):
    gatewayArn: str
    targetId: str
    createdAt: datetime
    updatedAt: datetime
    status: TargetStatusType
    statusReasons: List[str]
    name: str
    description: str
    targetConfiguration: TargetConfigurationOutputTypeDef
    credentialProviderConfigurations: List[CredentialProviderConfigurationOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetGatewayTargetResponseTypeDef(TypedDict):
    gatewayArn: str
    targetId: str
    createdAt: datetime
    updatedAt: datetime
    status: TargetStatusType
    statusReasons: List[str]
    name: str
    description: str
    targetConfiguration: TargetConfigurationOutputTypeDef
    credentialProviderConfigurations: List[CredentialProviderConfigurationOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateGatewayTargetResponseTypeDef(TypedDict):
    gatewayArn: str
    targetId: str
    createdAt: datetime
    updatedAt: datetime
    status: TargetStatusType
    statusReasons: List[str]
    name: str
    description: str
    targetConfiguration: TargetConfigurationOutputTypeDef
    credentialProviderConfigurations: List[CredentialProviderConfigurationOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

TargetConfigurationUnionTypeDef = Union[
    TargetConfigurationTypeDef, TargetConfigurationOutputTypeDef
]

class CreateGatewayTargetRequestTypeDef(TypedDict):
    gatewayIdentifier: str
    name: str
    targetConfiguration: TargetConfigurationUnionTypeDef
    credentialProviderConfigurations: Sequence[CredentialProviderConfigurationUnionTypeDef]
    description: NotRequired[str]
    clientToken: NotRequired[str]

class UpdateGatewayTargetRequestTypeDef(TypedDict):
    gatewayIdentifier: str
    targetId: str
    name: str
    targetConfiguration: TargetConfigurationUnionTypeDef
    credentialProviderConfigurations: Sequence[CredentialProviderConfigurationUnionTypeDef]
    description: NotRequired[str]
