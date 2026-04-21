"""
Type annotations for bedrock-agentcore-control service type definitions.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/type_defs/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from mypy_boto3_bedrock_agentcore_control.type_defs import AgentCardDefinitionTypeDef

    data: AgentCardDefinitionTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Union

from .literals import (
    AgentManagedRuntimeTypeType,
    AgentRuntimeEndpointStatusType,
    AgentRuntimeStatusType,
    ApiKeyCredentialLocationType,
    AuthorizerTypeType,
    BrowserEnterprisePolicyTypeType,
    BrowserNetworkModeType,
    BrowserProfileStatusType,
    BrowserStatusType,
    ClaimMatchOperatorTypeType,
    CodeInterpreterNetworkModeType,
    CodeInterpreterStatusType,
    ContentLevelType,
    CredentialProviderTypeType,
    CredentialProviderVendorTypeType,
    DescriptorTypeType,
    EndpointIpAddressTypeType,
    EvaluatorLevelType,
    EvaluatorStatusType,
    EvaluatorTypeType,
    FilterOperatorType,
    FindingTypeType,
    GatewayInterceptionPointType,
    GatewayPolicyEngineModeType,
    GatewayStatusType,
    InboundTokenClaimValueTypeType,
    KeyTypeType,
    ListingModeType,
    MemoryStatusType,
    MemoryStrategyStatusType,
    MemoryStrategyTypeType,
    MemoryViewType,
    NetworkModeType,
    OAuthGrantTypeType,
    OnlineEvaluationConfigStatusType,
    OnlineEvaluationExecutionStatusType,
    OverrideTypeType,
    PolicyEngineStatusType,
    PolicyGenerationStatusType,
    PolicyStatusType,
    PolicyValidationModeType,
    RegistryAuthorizerTypeType,
    RegistryRecordCredentialProviderTypeType,
    RegistryRecordStatusType,
    RegistryStatusType,
    ResourceTypeType,
    RestApiMethodType,
    SchemaTypeType,
    ServerProtocolType,
    TargetStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "A2aDescriptorTypeDef",
    "AgentCardDefinitionTypeDef",
    "AgentRuntimeArtifactOutputTypeDef",
    "AgentRuntimeArtifactTypeDef",
    "AgentRuntimeArtifactUnionTypeDef",
    "AgentRuntimeEndpointTypeDef",
    "AgentRuntimeTypeDef",
    "AgentSkillsDescriptorTypeDef",
    "ApiGatewayTargetConfigurationOutputTypeDef",
    "ApiGatewayTargetConfigurationTypeDef",
    "ApiGatewayToolConfigurationOutputTypeDef",
    "ApiGatewayToolConfigurationTypeDef",
    "ApiGatewayToolFilterOutputTypeDef",
    "ApiGatewayToolFilterTypeDef",
    "ApiGatewayToolOverrideTypeDef",
    "ApiKeyCredentialProviderItemTypeDef",
    "ApiKeyCredentialProviderTypeDef",
    "ApiSchemaConfigurationTypeDef",
    "ApprovalConfigurationTypeDef",
    "AtlassianOauth2ProviderConfigInputTypeDef",
    "AtlassianOauth2ProviderConfigOutputTypeDef",
    "AuthorizationDataTypeDef",
    "AuthorizerConfigurationOutputTypeDef",
    "AuthorizerConfigurationTypeDef",
    "AuthorizerConfigurationUnionTypeDef",
    "AuthorizingClaimMatchValueTypeOutputTypeDef",
    "AuthorizingClaimMatchValueTypeTypeDef",
    "AuthorizingClaimMatchValueTypeUnionTypeDef",
    "BedrockEvaluatorModelConfigOutputTypeDef",
    "BedrockEvaluatorModelConfigTypeDef",
    "BrowserEnterprisePolicyTypeDef",
    "BrowserNetworkConfigurationOutputTypeDef",
    "BrowserNetworkConfigurationTypeDef",
    "BrowserNetworkConfigurationUnionTypeDef",
    "BrowserProfileSummaryTypeDef",
    "BrowserSigningConfigInputTypeDef",
    "BrowserSigningConfigOutputTypeDef",
    "BrowserSummaryTypeDef",
    "CategoricalScaleDefinitionTypeDef",
    "CedarPolicyTypeDef",
    "CertificateLocationTypeDef",
    "CertificateTypeDef",
    "ClaimMatchValueTypeOutputTypeDef",
    "ClaimMatchValueTypeTypeDef",
    "ClaimMatchValueTypeUnionTypeDef",
    "CloudWatchLogsInputConfigOutputTypeDef",
    "CloudWatchLogsInputConfigTypeDef",
    "CloudWatchOutputConfigTypeDef",
    "CodeBasedEvaluatorConfigTypeDef",
    "CodeConfigurationOutputTypeDef",
    "CodeConfigurationTypeDef",
    "CodeInterpreterNetworkConfigurationOutputTypeDef",
    "CodeInterpreterNetworkConfigurationTypeDef",
    "CodeInterpreterNetworkConfigurationUnionTypeDef",
    "CodeInterpreterSummaryTypeDef",
    "CodeTypeDef",
    "ConsolidationConfigurationTypeDef",
    "ContainerConfigurationTypeDef",
    "ContentConfigurationTypeDef",
    "ContentTypeDef",
    "CreateAgentRuntimeEndpointRequestTypeDef",
    "CreateAgentRuntimeEndpointResponseTypeDef",
    "CreateAgentRuntimeRequestTypeDef",
    "CreateAgentRuntimeResponseTypeDef",
    "CreateApiKeyCredentialProviderRequestTypeDef",
    "CreateApiKeyCredentialProviderResponseTypeDef",
    "CreateBrowserProfileRequestTypeDef",
    "CreateBrowserProfileResponseTypeDef",
    "CreateBrowserRequestTypeDef",
    "CreateBrowserResponseTypeDef",
    "CreateCodeInterpreterRequestTypeDef",
    "CreateCodeInterpreterResponseTypeDef",
    "CreateEvaluatorRequestTypeDef",
    "CreateEvaluatorResponseTypeDef",
    "CreateGatewayRequestTypeDef",
    "CreateGatewayResponseTypeDef",
    "CreateGatewayTargetRequestTypeDef",
    "CreateGatewayTargetResponseTypeDef",
    "CreateMemoryInputTypeDef",
    "CreateMemoryOutputTypeDef",
    "CreateOauth2CredentialProviderRequestTypeDef",
    "CreateOauth2CredentialProviderResponseTypeDef",
    "CreateOnlineEvaluationConfigRequestTypeDef",
    "CreateOnlineEvaluationConfigResponseTypeDef",
    "CreatePolicyEngineRequestTypeDef",
    "CreatePolicyEngineResponseTypeDef",
    "CreatePolicyRequestTypeDef",
    "CreatePolicyResponseTypeDef",
    "CreateRegistryRecordRequestTypeDef",
    "CreateRegistryRecordResponseTypeDef",
    "CreateRegistryRequestTypeDef",
    "CreateRegistryResponseTypeDef",
    "CreateWorkloadIdentityRequestTypeDef",
    "CreateWorkloadIdentityResponseTypeDef",
    "CredentialProviderConfigurationOutputTypeDef",
    "CredentialProviderConfigurationTypeDef",
    "CredentialProviderConfigurationUnionTypeDef",
    "CredentialProviderOutputTypeDef",
    "CredentialProviderTypeDef",
    "CredentialProviderUnionTypeDef",
    "CustomClaimValidationTypeOutputTypeDef",
    "CustomClaimValidationTypeTypeDef",
    "CustomClaimValidationTypeUnionTypeDef",
    "CustomConfigurationInputTypeDef",
    "CustomConsolidationConfigurationInputTypeDef",
    "CustomConsolidationConfigurationTypeDef",
    "CustomDescriptorTypeDef",
    "CustomExtractionConfigurationInputTypeDef",
    "CustomExtractionConfigurationTypeDef",
    "CustomJWTAuthorizerConfigurationOutputTypeDef",
    "CustomJWTAuthorizerConfigurationTypeDef",
    "CustomJWTAuthorizerConfigurationUnionTypeDef",
    "CustomMemoryStrategyInputTypeDef",
    "CustomOauth2ProviderConfigInputTypeDef",
    "CustomOauth2ProviderConfigOutputTypeDef",
    "CustomReflectionConfigurationInputTypeDef",
    "CustomReflectionConfigurationTypeDef",
    "DataSourceConfigOutputTypeDef",
    "DataSourceConfigTypeDef",
    "DataSourceConfigUnionTypeDef",
    "DeleteAgentRuntimeEndpointRequestTypeDef",
    "DeleteAgentRuntimeEndpointResponseTypeDef",
    "DeleteAgentRuntimeRequestTypeDef",
    "DeleteAgentRuntimeResponseTypeDef",
    "DeleteApiKeyCredentialProviderRequestTypeDef",
    "DeleteBrowserProfileRequestTypeDef",
    "DeleteBrowserProfileResponseTypeDef",
    "DeleteBrowserRequestTypeDef",
    "DeleteBrowserResponseTypeDef",
    "DeleteCodeInterpreterRequestTypeDef",
    "DeleteCodeInterpreterResponseTypeDef",
    "DeleteEvaluatorRequestTypeDef",
    "DeleteEvaluatorResponseTypeDef",
    "DeleteGatewayRequestTypeDef",
    "DeleteGatewayResponseTypeDef",
    "DeleteGatewayTargetRequestTypeDef",
    "DeleteGatewayTargetResponseTypeDef",
    "DeleteMemoryInputTypeDef",
    "DeleteMemoryOutputTypeDef",
    "DeleteMemoryStrategyInputTypeDef",
    "DeleteOauth2CredentialProviderRequestTypeDef",
    "DeleteOnlineEvaluationConfigRequestTypeDef",
    "DeleteOnlineEvaluationConfigResponseTypeDef",
    "DeletePolicyEngineRequestTypeDef",
    "DeletePolicyEngineResponseTypeDef",
    "DeletePolicyRequestTypeDef",
    "DeletePolicyResponseTypeDef",
    "DeleteRegistryRecordRequestTypeDef",
    "DeleteRegistryRequestTypeDef",
    "DeleteRegistryResponseTypeDef",
    "DeleteResourcePolicyRequestTypeDef",
    "DeleteWorkloadIdentityRequestTypeDef",
    "DescriptorsTypeDef",
    "EpisodicConsolidationOverrideTypeDef",
    "EpisodicExtractionOverrideTypeDef",
    "EpisodicMemoryStrategyInputTypeDef",
    "EpisodicOverrideConfigurationInputTypeDef",
    "EpisodicOverrideConsolidationConfigurationInputTypeDef",
    "EpisodicOverrideExtractionConfigurationInputTypeDef",
    "EpisodicOverrideReflectionConfigurationInputTypeDef",
    "EpisodicReflectionConfigurationInputTypeDef",
    "EpisodicReflectionConfigurationTypeDef",
    "EpisodicReflectionOverrideTypeDef",
    "EvaluatorConfigOutputTypeDef",
    "EvaluatorConfigTypeDef",
    "EvaluatorConfigUnionTypeDef",
    "EvaluatorModelConfigOutputTypeDef",
    "EvaluatorModelConfigTypeDef",
    "EvaluatorReferenceTypeDef",
    "EvaluatorSummaryTypeDef",
    "ExtractionConfigurationTypeDef",
    "FilesystemConfigurationTypeDef",
    "FilterTypeDef",
    "FilterValueTypeDef",
    "FindingTypeDef",
    "FromUrlSynchronizationConfigurationOutputTypeDef",
    "FromUrlSynchronizationConfigurationTypeDef",
    "FromUrlSynchronizationConfigurationUnionTypeDef",
    "GatewayInterceptorConfigurationOutputTypeDef",
    "GatewayInterceptorConfigurationTypeDef",
    "GatewayInterceptorConfigurationUnionTypeDef",
    "GatewayPolicyEngineConfigurationTypeDef",
    "GatewayProtocolConfigurationOutputTypeDef",
    "GatewayProtocolConfigurationTypeDef",
    "GatewayProtocolConfigurationUnionTypeDef",
    "GatewaySummaryTypeDef",
    "GatewayTargetTypeDef",
    "GetAgentRuntimeEndpointRequestTypeDef",
    "GetAgentRuntimeEndpointResponseTypeDef",
    "GetAgentRuntimeRequestTypeDef",
    "GetAgentRuntimeResponseTypeDef",
    "GetApiKeyCredentialProviderRequestTypeDef",
    "GetApiKeyCredentialProviderResponseTypeDef",
    "GetBrowserProfileRequestTypeDef",
    "GetBrowserProfileResponseTypeDef",
    "GetBrowserRequestTypeDef",
    "GetBrowserResponseTypeDef",
    "GetCodeInterpreterRequestTypeDef",
    "GetCodeInterpreterResponseTypeDef",
    "GetEvaluatorRequestTypeDef",
    "GetEvaluatorResponseTypeDef",
    "GetGatewayRequestTypeDef",
    "GetGatewayResponseTypeDef",
    "GetGatewayTargetRequestTypeDef",
    "GetGatewayTargetResponseTypeDef",
    "GetMemoryInputTypeDef",
    "GetMemoryInputWaitTypeDef",
    "GetMemoryOutputTypeDef",
    "GetOauth2CredentialProviderRequestTypeDef",
    "GetOauth2CredentialProviderResponseTypeDef",
    "GetOnlineEvaluationConfigRequestTypeDef",
    "GetOnlineEvaluationConfigResponseTypeDef",
    "GetPolicyEngineRequestTypeDef",
    "GetPolicyEngineRequestWaitExtraTypeDef",
    "GetPolicyEngineRequestWaitTypeDef",
    "GetPolicyEngineResponseTypeDef",
    "GetPolicyGenerationRequestTypeDef",
    "GetPolicyGenerationRequestWaitTypeDef",
    "GetPolicyGenerationResponseTypeDef",
    "GetPolicyRequestTypeDef",
    "GetPolicyRequestWaitExtraTypeDef",
    "GetPolicyRequestWaitTypeDef",
    "GetPolicyResponseTypeDef",
    "GetRegistryRecordRequestTypeDef",
    "GetRegistryRecordResponseTypeDef",
    "GetRegistryRequestTypeDef",
    "GetRegistryResponseTypeDef",
    "GetResourcePolicyRequestTypeDef",
    "GetResourcePolicyResponseTypeDef",
    "GetTokenVaultRequestTypeDef",
    "GetTokenVaultResponseTypeDef",
    "GetWorkloadIdentityRequestTypeDef",
    "GetWorkloadIdentityResponseTypeDef",
    "GithubOauth2ProviderConfigInputTypeDef",
    "GithubOauth2ProviderConfigOutputTypeDef",
    "GoogleOauth2ProviderConfigInputTypeDef",
    "GoogleOauth2ProviderConfigOutputTypeDef",
    "IamCredentialProviderTypeDef",
    "IncludedOauth2ProviderConfigInputTypeDef",
    "IncludedOauth2ProviderConfigOutputTypeDef",
    "InferenceConfigurationOutputTypeDef",
    "InferenceConfigurationTypeDef",
    "InterceptorConfigurationTypeDef",
    "InterceptorInputConfigurationTypeDef",
    "InvocationConfigurationInputTypeDef",
    "InvocationConfigurationTypeDef",
    "KinesisResourceOutputTypeDef",
    "KinesisResourceTypeDef",
    "KmsConfigurationTypeDef",
    "LambdaEvaluatorConfigTypeDef",
    "LambdaInterceptorConfigurationTypeDef",
    "LifecycleConfigurationTypeDef",
    "LinkedinOauth2ProviderConfigInputTypeDef",
    "LinkedinOauth2ProviderConfigOutputTypeDef",
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
    "ListBrowserProfilesRequestPaginateTypeDef",
    "ListBrowserProfilesRequestTypeDef",
    "ListBrowserProfilesResponseTypeDef",
    "ListBrowsersRequestPaginateTypeDef",
    "ListBrowsersRequestTypeDef",
    "ListBrowsersResponseTypeDef",
    "ListCodeInterpretersRequestPaginateTypeDef",
    "ListCodeInterpretersRequestTypeDef",
    "ListCodeInterpretersResponseTypeDef",
    "ListEvaluatorsRequestPaginateTypeDef",
    "ListEvaluatorsRequestTypeDef",
    "ListEvaluatorsResponseTypeDef",
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
    "ListOnlineEvaluationConfigsRequestPaginateTypeDef",
    "ListOnlineEvaluationConfigsRequestTypeDef",
    "ListOnlineEvaluationConfigsResponseTypeDef",
    "ListPoliciesRequestPaginateTypeDef",
    "ListPoliciesRequestTypeDef",
    "ListPoliciesResponseTypeDef",
    "ListPolicyEnginesRequestPaginateTypeDef",
    "ListPolicyEnginesRequestTypeDef",
    "ListPolicyEnginesResponseTypeDef",
    "ListPolicyGenerationAssetsRequestPaginateTypeDef",
    "ListPolicyGenerationAssetsRequestTypeDef",
    "ListPolicyGenerationAssetsResponseTypeDef",
    "ListPolicyGenerationsRequestPaginateTypeDef",
    "ListPolicyGenerationsRequestTypeDef",
    "ListPolicyGenerationsResponseTypeDef",
    "ListRegistriesRequestPaginateTypeDef",
    "ListRegistriesRequestTypeDef",
    "ListRegistriesResponseTypeDef",
    "ListRegistryRecordsRequestPaginateTypeDef",
    "ListRegistryRecordsRequestTypeDef",
    "ListRegistryRecordsResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListWorkloadIdentitiesRequestPaginateTypeDef",
    "ListWorkloadIdentitiesRequestTypeDef",
    "ListWorkloadIdentitiesResponseTypeDef",
    "LlmAsAJudgeEvaluatorConfigOutputTypeDef",
    "LlmAsAJudgeEvaluatorConfigTypeDef",
    "MCPGatewayConfigurationOutputTypeDef",
    "MCPGatewayConfigurationTypeDef",
    "ManagedLatticeResourceOutputTypeDef",
    "ManagedLatticeResourceTypeDef",
    "ManagedResourceDetailsTypeDef",
    "McpDescriptorTypeDef",
    "McpLambdaTargetConfigurationOutputTypeDef",
    "McpLambdaTargetConfigurationTypeDef",
    "McpServerTargetConfigurationTypeDef",
    "McpTargetConfigurationOutputTypeDef",
    "McpTargetConfigurationTypeDef",
    "McpToolSchemaConfigurationTypeDef",
    "MemoryStrategyInputTypeDef",
    "MemoryStrategyTypeDef",
    "MemorySummaryTypeDef",
    "MemoryTypeDef",
    "MessageBasedTriggerInputTypeDef",
    "MessageBasedTriggerTypeDef",
    "MetadataConfigurationOutputTypeDef",
    "MetadataConfigurationTypeDef",
    "MetadataConfigurationUnionTypeDef",
    "MicrosoftOauth2ProviderConfigInputTypeDef",
    "MicrosoftOauth2ProviderConfigOutputTypeDef",
    "ModifyConsolidationConfigurationTypeDef",
    "ModifyExtractionConfigurationTypeDef",
    "ModifyInvocationConfigurationInputTypeDef",
    "ModifyMemoryStrategiesTypeDef",
    "ModifyMemoryStrategyInputTypeDef",
    "ModifyReflectionConfigurationTypeDef",
    "ModifySelfManagedConfigurationTypeDef",
    "ModifyStrategyConfigurationTypeDef",
    "NetworkConfigurationOutputTypeDef",
    "NetworkConfigurationTypeDef",
    "NetworkConfigurationUnionTypeDef",
    "NumericalScaleDefinitionTypeDef",
    "OAuth2AuthorizationDataTypeDef",
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
    "OnlineEvaluationConfigSummaryTypeDef",
    "OutputConfigTypeDef",
    "PaginatorConfigTypeDef",
    "PolicyDefinitionTypeDef",
    "PolicyEngineTypeDef",
    "PolicyGenerationAssetTypeDef",
    "PolicyGenerationDetailsTypeDef",
    "PolicyGenerationTypeDef",
    "PolicyTypeDef",
    "PrivateEndpointOutputTypeDef",
    "PrivateEndpointTypeDef",
    "PrivateEndpointUnionTypeDef",
    "ProtocolConfigurationTypeDef",
    "PutResourcePolicyRequestTypeDef",
    "PutResourcePolicyResponseTypeDef",
    "RatingScaleOutputTypeDef",
    "RatingScaleTypeDef",
    "RecordingConfigTypeDef",
    "ReflectionConfigurationTypeDef",
    "RegistryRecordCredentialProviderConfigurationOutputTypeDef",
    "RegistryRecordCredentialProviderConfigurationTypeDef",
    "RegistryRecordCredentialProviderConfigurationUnionTypeDef",
    "RegistryRecordCredentialProviderUnionOutputTypeDef",
    "RegistryRecordCredentialProviderUnionTypeDef",
    "RegistryRecordCredentialProviderUnionUnionTypeDef",
    "RegistryRecordIamCredentialProviderTypeDef",
    "RegistryRecordOAuthCredentialProviderOutputTypeDef",
    "RegistryRecordOAuthCredentialProviderTypeDef",
    "RegistryRecordOAuthCredentialProviderUnionTypeDef",
    "RegistryRecordSummaryTypeDef",
    "RegistrySummaryTypeDef",
    "RequestHeaderConfigurationOutputTypeDef",
    "RequestHeaderConfigurationTypeDef",
    "RequestHeaderConfigurationUnionTypeDef",
    "ResourceLocationTypeDef",
    "ResourceTypeDef",
    "ResponseMetadataTypeDef",
    "RuleOutputTypeDef",
    "RuleTypeDef",
    "RuleUnionTypeDef",
    "RuntimeMetadataConfigurationTypeDef",
    "S3ConfigurationTypeDef",
    "S3LocationTypeDef",
    "SalesforceOauth2ProviderConfigInputTypeDef",
    "SalesforceOauth2ProviderConfigOutputTypeDef",
    "SamplingConfigTypeDef",
    "SchemaDefinitionOutputTypeDef",
    "SchemaDefinitionTypeDef",
    "SecretTypeDef",
    "SecretsManagerLocationTypeDef",
    "SelfManagedConfigurationInputTypeDef",
    "SelfManagedConfigurationTypeDef",
    "SelfManagedLatticeResourceTypeDef",
    "SemanticConsolidationOverrideTypeDef",
    "SemanticExtractionOverrideTypeDef",
    "SemanticMemoryStrategyInputTypeDef",
    "SemanticOverrideConfigurationInputTypeDef",
    "SemanticOverrideConsolidationConfigurationInputTypeDef",
    "SemanticOverrideExtractionConfigurationInputTypeDef",
    "ServerDefinitionTypeDef",
    "SessionConfigTypeDef",
    "SessionStorageConfigurationTypeDef",
    "SetTokenVaultCMKRequestTypeDef",
    "SetTokenVaultCMKResponseTypeDef",
    "SkillDefinitionTypeDef",
    "SkillMdDefinitionTypeDef",
    "SlackOauth2ProviderConfigInputTypeDef",
    "SlackOauth2ProviderConfigOutputTypeDef",
    "StartPolicyGenerationRequestTypeDef",
    "StartPolicyGenerationResponseTypeDef",
    "StrategyConfigurationTypeDef",
    "StreamDeliveryResourceOutputTypeDef",
    "StreamDeliveryResourceTypeDef",
    "StreamDeliveryResourcesOutputTypeDef",
    "StreamDeliveryResourcesTypeDef",
    "StreamDeliveryResourcesUnionTypeDef",
    "SubmitRegistryRecordForApprovalRequestTypeDef",
    "SubmitRegistryRecordForApprovalResponseTypeDef",
    "SummaryConsolidationOverrideTypeDef",
    "SummaryMemoryStrategyInputTypeDef",
    "SummaryOverrideConfigurationInputTypeDef",
    "SummaryOverrideConsolidationConfigurationInputTypeDef",
    "SynchronizationConfigurationOutputTypeDef",
    "SynchronizationConfigurationTypeDef",
    "SynchronizationConfigurationUnionTypeDef",
    "SynchronizeGatewayTargetsRequestTypeDef",
    "SynchronizeGatewayTargetsResponseTypeDef",
    "TagResourceRequestTypeDef",
    "TargetConfigurationOutputTypeDef",
    "TargetConfigurationTypeDef",
    "TargetConfigurationUnionTypeDef",
    "TargetSummaryTypeDef",
    "TimeBasedTriggerInputTypeDef",
    "TimeBasedTriggerTypeDef",
    "TokenBasedTriggerInputTypeDef",
    "TokenBasedTriggerTypeDef",
    "ToolDefinitionOutputTypeDef",
    "ToolDefinitionTypeDef",
    "ToolSchemaOutputTypeDef",
    "ToolSchemaTypeDef",
    "ToolsDefinitionTypeDef",
    "TriggerConditionInputTypeDef",
    "TriggerConditionTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateAgentRuntimeEndpointRequestTypeDef",
    "UpdateAgentRuntimeEndpointResponseTypeDef",
    "UpdateAgentRuntimeRequestTypeDef",
    "UpdateAgentRuntimeResponseTypeDef",
    "UpdateApiKeyCredentialProviderRequestTypeDef",
    "UpdateApiKeyCredentialProviderResponseTypeDef",
    "UpdateEvaluatorRequestTypeDef",
    "UpdateEvaluatorResponseTypeDef",
    "UpdateGatewayRequestTypeDef",
    "UpdateGatewayResponseTypeDef",
    "UpdateGatewayTargetRequestTypeDef",
    "UpdateGatewayTargetResponseTypeDef",
    "UpdateMemoryInputTypeDef",
    "UpdateMemoryOutputTypeDef",
    "UpdateOauth2CredentialProviderRequestTypeDef",
    "UpdateOauth2CredentialProviderResponseTypeDef",
    "UpdateOnlineEvaluationConfigRequestTypeDef",
    "UpdateOnlineEvaluationConfigResponseTypeDef",
    "UpdatePolicyEngineRequestTypeDef",
    "UpdatePolicyEngineResponseTypeDef",
    "UpdatePolicyRequestTypeDef",
    "UpdatePolicyResponseTypeDef",
    "UpdateRegistryRecordRequestTypeDef",
    "UpdateRegistryRecordResponseTypeDef",
    "UpdateRegistryRecordStatusRequestTypeDef",
    "UpdateRegistryRecordStatusResponseTypeDef",
    "UpdateRegistryRequestTypeDef",
    "UpdateRegistryResponseTypeDef",
    "UpdateWorkloadIdentityRequestTypeDef",
    "UpdateWorkloadIdentityResponseTypeDef",
    "UpdatedA2aDescriptorTypeDef",
    "UpdatedAgentSkillsDescriptorFieldsTypeDef",
    "UpdatedAgentSkillsDescriptorTypeDef",
    "UpdatedApprovalConfigurationTypeDef",
    "UpdatedAuthorizerConfigurationTypeDef",
    "UpdatedCustomDescriptorTypeDef",
    "UpdatedDescriptionTypeDef",
    "UpdatedDescriptorsTypeDef",
    "UpdatedDescriptorsUnionTypeDef",
    "UpdatedMcpDescriptorFieldsTypeDef",
    "UpdatedMcpDescriptorTypeDef",
    "UpdatedServerDefinitionTypeDef",
    "UpdatedSkillDefinitionTypeDef",
    "UpdatedSkillMdDefinitionTypeDef",
    "UpdatedSynchronizationConfigurationTypeDef",
    "UpdatedSynchronizationTypeTypeDef",
    "UpdatedToolsDefinitionTypeDef",
    "UserPreferenceConsolidationOverrideTypeDef",
    "UserPreferenceExtractionOverrideTypeDef",
    "UserPreferenceMemoryStrategyInputTypeDef",
    "UserPreferenceOverrideConfigurationInputTypeDef",
    "UserPreferenceOverrideConsolidationConfigurationInputTypeDef",
    "UserPreferenceOverrideExtractionConfigurationInputTypeDef",
    "VpcConfigOutputTypeDef",
    "VpcConfigTypeDef",
    "WaiterConfigTypeDef",
    "WorkloadIdentityDetailsTypeDef",
    "WorkloadIdentityTypeTypeDef",
)

class AgentCardDefinitionTypeDef(TypedDict):
    schemaVersion: NotRequired[str]
    inlineContent: NotRequired[str]

class ContainerConfigurationTypeDef(TypedDict):
    containerUri: str

AgentRuntimeEndpointTypeDef = TypedDict(
    "AgentRuntimeEndpointTypeDef",
    {
        "name": str,
        "agentRuntimeEndpointArn": str,
        "agentRuntimeArn": str,
        "status": AgentRuntimeEndpointStatusType,
        "id": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "liveVersion": NotRequired[str],
        "targetVersion": NotRequired[str],
        "description": NotRequired[str],
    },
)

class AgentRuntimeTypeDef(TypedDict):
    agentRuntimeArn: str
    agentRuntimeId: str
    agentRuntimeVersion: str
    agentRuntimeName: str
    description: str
    lastUpdatedAt: datetime
    status: AgentRuntimeStatusType

class SkillDefinitionTypeDef(TypedDict):
    schemaVersion: NotRequired[str]
    inlineContent: NotRequired[str]

class SkillMdDefinitionTypeDef(TypedDict):
    inlineContent: NotRequired[str]

class ApiGatewayToolFilterOutputTypeDef(TypedDict):
    filterPath: str
    methods: list[RestApiMethodType]

class ApiGatewayToolOverrideTypeDef(TypedDict):
    name: str
    path: str
    method: RestApiMethodType
    description: NotRequired[str]

class ApiGatewayToolFilterTypeDef(TypedDict):
    filterPath: str
    methods: Sequence[RestApiMethodType]

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

class ApprovalConfigurationTypeDef(TypedDict):
    autoApproval: NotRequired[bool]

class AtlassianOauth2ProviderConfigInputTypeDef(TypedDict):
    clientId: str
    clientSecret: str

class OAuth2AuthorizationDataTypeDef(TypedDict):
    authorizationUrl: str
    userId: NotRequired[str]

class ClaimMatchValueTypeOutputTypeDef(TypedDict):
    matchValueString: NotRequired[str]
    matchValueStringList: NotRequired[list[str]]

class InferenceConfigurationOutputTypeDef(TypedDict):
    maxTokens: NotRequired[int]
    temperature: NotRequired[float]
    topP: NotRequired[float]
    stopSequences: NotRequired[list[str]]

class InferenceConfigurationTypeDef(TypedDict):
    maxTokens: NotRequired[int]
    temperature: NotRequired[float]
    topP: NotRequired[float]
    stopSequences: NotRequired[Sequence[str]]

class VpcConfigOutputTypeDef(TypedDict):
    securityGroups: list[str]
    subnets: list[str]

class VpcConfigTypeDef(TypedDict):
    securityGroups: Sequence[str]
    subnets: Sequence[str]

class BrowserProfileSummaryTypeDef(TypedDict):
    profileId: str
    profileArn: str
    name: str
    status: BrowserProfileStatusType
    createdAt: datetime
    lastUpdatedAt: datetime
    description: NotRequired[str]
    lastSavedAt: NotRequired[datetime]
    lastSavedBrowserSessionId: NotRequired[str]
    lastSavedBrowserId: NotRequired[str]

class BrowserSigningConfigInputTypeDef(TypedDict):
    enabled: bool

class BrowserSigningConfigOutputTypeDef(TypedDict):
    enabled: bool

class BrowserSummaryTypeDef(TypedDict):
    browserId: str
    browserArn: str
    status: BrowserStatusType
    createdAt: datetime
    name: NotRequired[str]
    description: NotRequired[str]
    lastUpdatedAt: NotRequired[datetime]

class CategoricalScaleDefinitionTypeDef(TypedDict):
    definition: str
    label: str

class CedarPolicyTypeDef(TypedDict):
    statement: str

class SecretsManagerLocationTypeDef(TypedDict):
    secretArn: str

class ClaimMatchValueTypeTypeDef(TypedDict):
    matchValueString: NotRequired[str]
    matchValueStringList: NotRequired[Sequence[str]]

class CloudWatchLogsInputConfigOutputTypeDef(TypedDict):
    logGroupNames: list[str]
    serviceNames: list[str]

class CloudWatchLogsInputConfigTypeDef(TypedDict):
    logGroupNames: Sequence[str]
    serviceNames: Sequence[str]

class CloudWatchOutputConfigTypeDef(TypedDict):
    logGroupName: str

class LambdaEvaluatorConfigTypeDef(TypedDict):
    lambdaArn: str
    lambdaTimeoutInSeconds: NotRequired[int]

class CodeInterpreterSummaryTypeDef(TypedDict):
    codeInterpreterId: str
    codeInterpreterArn: str
    status: CodeInterpreterStatusType
    createdAt: datetime
    name: NotRequired[str]
    description: NotRequired[str]
    lastUpdatedAt: NotRequired[datetime]

class S3LocationTypeDef(TypedDict):
    bucket: str
    prefix: str
    versionId: NotRequired[str]

ContentConfigurationTypeDef = TypedDict(
    "ContentConfigurationTypeDef",
    {
        "type": Literal["MEMORY_RECORDS"],
        "level": NotRequired[ContentLevelType],
    },
)

class ContentTypeDef(TypedDict):
    rawText: NotRequired[str]

class CreateAgentRuntimeEndpointRequestTypeDef(TypedDict):
    agentRuntimeId: str
    name: str
    agentRuntimeVersion: NotRequired[str]
    description: NotRequired[str]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class LifecycleConfigurationTypeDef(TypedDict):
    idleRuntimeSessionTimeout: NotRequired[int]
    maxLifetime: NotRequired[int]

class ProtocolConfigurationTypeDef(TypedDict):
    serverProtocol: ServerProtocolType

class WorkloadIdentityDetailsTypeDef(TypedDict):
    workloadIdentityArn: str

class CreateApiKeyCredentialProviderRequestTypeDef(TypedDict):
    name: str
    apiKey: str
    tags: NotRequired[Mapping[str, str]]

class SecretTypeDef(TypedDict):
    secretArn: str

class CreateBrowserProfileRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class GatewayPolicyEngineConfigurationTypeDef(TypedDict):
    arn: str
    mode: GatewayPolicyEngineModeType

class ManagedResourceDetailsTypeDef(TypedDict):
    domain: NotRequired[str]
    resourceGatewayArn: NotRequired[str]
    resourceAssociationArn: NotRequired[str]

class MetadataConfigurationOutputTypeDef(TypedDict):
    allowedRequestHeaders: NotRequired[list[str]]
    allowedQueryParameters: NotRequired[list[str]]
    allowedResponseHeaders: NotRequired[list[str]]

class EvaluatorReferenceTypeDef(TypedDict):
    evaluatorId: NotRequired[str]

class CreatePolicyEngineRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    clientToken: NotRequired[str]
    encryptionKeyArn: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class CreateWorkloadIdentityRequestTypeDef(TypedDict):
    name: str
    allowedResourceOauth2ReturnUrls: NotRequired[Sequence[str]]
    tags: NotRequired[Mapping[str, str]]

class IamCredentialProviderTypeDef(TypedDict):
    service: str
    region: NotRequired[str]

class OAuthCredentialProviderOutputTypeDef(TypedDict):
    providerArn: str
    scopes: list[str]
    customParameters: NotRequired[dict[str, str]]
    grantType: NotRequired[OAuthGrantTypeType]
    defaultReturnUrl: NotRequired[str]

class EpisodicOverrideConsolidationConfigurationInputTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str

class SemanticOverrideConsolidationConfigurationInputTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str

class SummaryOverrideConsolidationConfigurationInputTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str

class UserPreferenceOverrideConsolidationConfigurationInputTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str

class EpisodicConsolidationOverrideTypeDef(TypedDict):
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

class CustomDescriptorTypeDef(TypedDict):
    inlineContent: NotRequired[str]

class EpisodicOverrideExtractionConfigurationInputTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str

class SemanticOverrideExtractionConfigurationInputTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str

class UserPreferenceOverrideExtractionConfigurationInputTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str

class EpisodicExtractionOverrideTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str

class SemanticExtractionOverrideTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str

class UserPreferenceExtractionOverrideTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str

class EpisodicOverrideReflectionConfigurationInputTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str
    namespaces: NotRequired[Sequence[str]]
    namespaceTemplates: NotRequired[Sequence[str]]

class EpisodicReflectionOverrideTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str
    namespaces: NotRequired[list[str]]
    namespaceTemplates: NotRequired[list[str]]

class DeleteAgentRuntimeEndpointRequestTypeDef(TypedDict):
    agentRuntimeId: str
    endpointName: str
    clientToken: NotRequired[str]

class DeleteAgentRuntimeRequestTypeDef(TypedDict):
    agentRuntimeId: str
    clientToken: NotRequired[str]

class DeleteApiKeyCredentialProviderRequestTypeDef(TypedDict):
    name: str

class DeleteBrowserProfileRequestTypeDef(TypedDict):
    profileId: str
    clientToken: NotRequired[str]

class DeleteBrowserRequestTypeDef(TypedDict):
    browserId: str
    clientToken: NotRequired[str]

class DeleteCodeInterpreterRequestTypeDef(TypedDict):
    codeInterpreterId: str
    clientToken: NotRequired[str]

class DeleteEvaluatorRequestTypeDef(TypedDict):
    evaluatorId: str

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

class DeleteOnlineEvaluationConfigRequestTypeDef(TypedDict):
    onlineEvaluationConfigId: str

class DeletePolicyEngineRequestTypeDef(TypedDict):
    policyEngineId: str

class DeletePolicyRequestTypeDef(TypedDict):
    policyEngineId: str
    policyId: str

class DeleteRegistryRecordRequestTypeDef(TypedDict):
    registryId: str
    recordId: str

class DeleteRegistryRequestTypeDef(TypedDict):
    registryId: str

class DeleteResourcePolicyRequestTypeDef(TypedDict):
    resourceArn: str

class DeleteWorkloadIdentityRequestTypeDef(TypedDict):
    name: str

class EpisodicReflectionConfigurationInputTypeDef(TypedDict):
    namespaces: NotRequired[Sequence[str]]
    namespaceTemplates: NotRequired[Sequence[str]]

class EpisodicReflectionConfigurationTypeDef(TypedDict):
    namespaces: NotRequired[list[str]]
    namespaceTemplates: NotRequired[list[str]]

class EvaluatorSummaryTypeDef(TypedDict):
    evaluatorArn: str
    evaluatorId: str
    evaluatorName: str
    evaluatorType: EvaluatorTypeType
    status: EvaluatorStatusType
    createdAt: datetime
    updatedAt: datetime
    description: NotRequired[str]
    level: NotRequired[EvaluatorLevelType]
    lockedForModification: NotRequired[bool]

class SessionStorageConfigurationTypeDef(TypedDict):
    mountPath: str

class FilterValueTypeDef(TypedDict):
    stringValue: NotRequired[str]
    doubleValue: NotRequired[float]
    booleanValue: NotRequired[bool]

FindingTypeDef = TypedDict(
    "FindingTypeDef",
    {
        "type": NotRequired[FindingTypeType],
        "description": NotRequired[str],
    },
)

class InterceptorInputConfigurationTypeDef(TypedDict):
    passRequestHeaders: bool

class MCPGatewayConfigurationOutputTypeDef(TypedDict):
    supportedVersions: NotRequired[list[str]]
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
    authorizerType: AuthorizerTypeType
    protocolType: Literal["MCP"]
    description: NotRequired[str]

class GetAgentRuntimeEndpointRequestTypeDef(TypedDict):
    agentRuntimeId: str
    endpointName: str

class GetAgentRuntimeRequestTypeDef(TypedDict):
    agentRuntimeId: str
    agentRuntimeVersion: NotRequired[str]

class RequestHeaderConfigurationOutputTypeDef(TypedDict):
    requestHeaderAllowlist: NotRequired[list[str]]

class RuntimeMetadataConfigurationTypeDef(TypedDict):
    requireMMDSV2: bool

class GetApiKeyCredentialProviderRequestTypeDef(TypedDict):
    name: str

class GetBrowserProfileRequestTypeDef(TypedDict):
    profileId: str

class GetBrowserRequestTypeDef(TypedDict):
    browserId: str

class GetCodeInterpreterRequestTypeDef(TypedDict):
    codeInterpreterId: str

class GetEvaluatorRequestTypeDef(TypedDict):
    evaluatorId: str

class GetGatewayRequestTypeDef(TypedDict):
    gatewayIdentifier: str

class GetGatewayTargetRequestTypeDef(TypedDict):
    gatewayIdentifier: str
    targetId: str

class GetMemoryInputTypeDef(TypedDict):
    memoryId: str
    view: NotRequired[MemoryViewType]

class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]

class GetOauth2CredentialProviderRequestTypeDef(TypedDict):
    name: str

class GetOnlineEvaluationConfigRequestTypeDef(TypedDict):
    onlineEvaluationConfigId: str

class GetPolicyEngineRequestTypeDef(TypedDict):
    policyEngineId: str

class GetPolicyGenerationRequestTypeDef(TypedDict):
    policyGenerationId: str
    policyEngineId: str

class ResourceTypeDef(TypedDict):
    arn: NotRequired[str]

class GetPolicyRequestTypeDef(TypedDict):
    policyEngineId: str
    policyId: str

class GetRegistryRecordRequestTypeDef(TypedDict):
    registryId: str
    recordId: str

class GetRegistryRequestTypeDef(TypedDict):
    registryId: str

class GetResourcePolicyRequestTypeDef(TypedDict):
    resourceArn: str

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

class IncludedOauth2ProviderConfigInputTypeDef(TypedDict):
    clientId: str
    clientSecret: str
    issuer: NotRequired[str]
    authorizationEndpoint: NotRequired[str]
    tokenEndpoint: NotRequired[str]

class LambdaInterceptorConfigurationTypeDef(TypedDict):
    arn: str

class InvocationConfigurationInputTypeDef(TypedDict):
    topicArn: str
    payloadDeliveryBucketName: str

class InvocationConfigurationTypeDef(TypedDict):
    topicArn: str
    payloadDeliveryBucketName: str

class LinkedinOauth2ProviderConfigInputTypeDef(TypedDict):
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

class ListBrowserProfilesRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    name: NotRequired[str]

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

class ListEvaluatorsRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

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

class ListOnlineEvaluationConfigsRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class OnlineEvaluationConfigSummaryTypeDef(TypedDict):
    onlineEvaluationConfigArn: str
    onlineEvaluationConfigId: str
    onlineEvaluationConfigName: str
    status: OnlineEvaluationConfigStatusType
    executionStatus: OnlineEvaluationExecutionStatusType
    createdAt: datetime
    updatedAt: datetime
    description: NotRequired[str]
    failureReason: NotRequired[str]

class ListPoliciesRequestTypeDef(TypedDict):
    policyEngineId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    targetResourceScope: NotRequired[str]

class ListPolicyEnginesRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class PolicyEngineTypeDef(TypedDict):
    policyEngineId: str
    name: str
    createdAt: datetime
    updatedAt: datetime
    policyEngineArn: str
    status: PolicyEngineStatusType
    statusReasons: list[str]
    description: NotRequired[str]
    encryptionKeyArn: NotRequired[str]

class ListPolicyGenerationAssetsRequestTypeDef(TypedDict):
    policyGenerationId: str
    policyEngineId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListPolicyGenerationsRequestTypeDef(TypedDict):
    policyEngineId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListRegistriesRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[RegistryStatusType]

class RegistrySummaryTypeDef(TypedDict):
    name: str
    registryId: str
    registryArn: str
    status: RegistryStatusType
    createdAt: datetime
    updatedAt: datetime
    description: NotRequired[str]
    authorizerType: NotRequired[RegistryAuthorizerTypeType]
    statusReason: NotRequired[str]

class ListRegistryRecordsRequestTypeDef(TypedDict):
    registryId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    name: NotRequired[str]
    status: NotRequired[RegistryRecordStatusType]
    descriptorType: NotRequired[DescriptorTypeType]

class RegistryRecordSummaryTypeDef(TypedDict):
    registryArn: str
    recordArn: str
    recordId: str
    name: str
    descriptorType: DescriptorTypeType
    recordVersion: str
    status: RegistryRecordStatusType
    createdAt: datetime
    updatedAt: datetime
    description: NotRequired[str]

class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str

class ListWorkloadIdentitiesRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class WorkloadIdentityTypeTypeDef(TypedDict):
    name: str
    workloadIdentityArn: str

class ManagedLatticeResourceOutputTypeDef(TypedDict):
    vpcIdentifier: str
    subnetIds: list[str]
    endpointIpAddressType: EndpointIpAddressTypeType
    securityGroupIds: NotRequired[list[str]]
    tags: NotRequired[dict[str, str]]
    routingDomain: NotRequired[str]

class ManagedLatticeResourceTypeDef(TypedDict):
    vpcIdentifier: str
    subnetIds: Sequence[str]
    endpointIpAddressType: EndpointIpAddressTypeType
    securityGroupIds: NotRequired[Sequence[str]]
    tags: NotRequired[Mapping[str, str]]
    routingDomain: NotRequired[str]

class ServerDefinitionTypeDef(TypedDict):
    schemaVersion: NotRequired[str]
    inlineContent: NotRequired[str]

class ToolsDefinitionTypeDef(TypedDict):
    protocolVersion: NotRequired[str]
    inlineContent: NotRequired[str]

class SemanticMemoryStrategyInputTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    namespaces: NotRequired[Sequence[str]]
    namespaceTemplates: NotRequired[Sequence[str]]

class SummaryMemoryStrategyInputTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    namespaces: NotRequired[Sequence[str]]
    namespaceTemplates: NotRequired[Sequence[str]]

class UserPreferenceMemoryStrategyInputTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    namespaces: NotRequired[Sequence[str]]
    namespaceTemplates: NotRequired[Sequence[str]]

class MessageBasedTriggerInputTypeDef(TypedDict):
    messageCount: NotRequired[int]

class MessageBasedTriggerTypeDef(TypedDict):
    messageCount: NotRequired[int]

class MetadataConfigurationTypeDef(TypedDict):
    allowedRequestHeaders: NotRequired[Sequence[str]]
    allowedQueryParameters: NotRequired[Sequence[str]]
    allowedResponseHeaders: NotRequired[Sequence[str]]

class MicrosoftOauth2ProviderConfigInputTypeDef(TypedDict):
    clientId: str
    clientSecret: str
    tenantId: NotRequired[str]

class ModifyInvocationConfigurationInputTypeDef(TypedDict):
    topicArn: NotRequired[str]
    payloadDeliveryBucketName: NotRequired[str]

class NumericalScaleDefinitionTypeDef(TypedDict):
    definition: str
    value: float
    label: str

class OAuthCredentialProviderTypeDef(TypedDict):
    providerArn: str
    scopes: Sequence[str]
    customParameters: NotRequired[Mapping[str, str]]
    grantType: NotRequired[OAuthGrantTypeType]
    defaultReturnUrl: NotRequired[str]

class Oauth2AuthorizationServerMetadataOutputTypeDef(TypedDict):
    issuer: str
    authorizationEndpoint: str
    tokenEndpoint: str
    responseTypes: NotRequired[list[str]]
    tokenEndpointAuthMethods: NotRequired[list[str]]

class Oauth2AuthorizationServerMetadataTypeDef(TypedDict):
    issuer: str
    authorizationEndpoint: str
    tokenEndpoint: str
    responseTypes: NotRequired[Sequence[str]]
    tokenEndpointAuthMethods: NotRequired[Sequence[str]]

class SalesforceOauth2ProviderConfigInputTypeDef(TypedDict):
    clientId: str
    clientSecret: str

class SlackOauth2ProviderConfigInputTypeDef(TypedDict):
    clientId: str
    clientSecret: str

class PolicyGenerationDetailsTypeDef(TypedDict):
    policyGenerationId: str
    policyGenerationAssetId: str

class SelfManagedLatticeResourceTypeDef(TypedDict):
    resourceConfigurationIdentifier: NotRequired[str]

class PutResourcePolicyRequestTypeDef(TypedDict):
    resourceArn: str
    policy: str

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

class RequestHeaderConfigurationTypeDef(TypedDict):
    requestHeaderAllowlist: NotRequired[Sequence[str]]

class SamplingConfigTypeDef(TypedDict):
    samplingPercentage: float

class SessionConfigTypeDef(TypedDict):
    sessionTimeoutMinutes: int

SchemaDefinitionOutputTypeDef = TypedDict(
    "SchemaDefinitionOutputTypeDef",
    {
        "type": SchemaTypeType,
        "properties": NotRequired[dict[str, dict[str, Any]]],
        "required": NotRequired[list[str]],
        "items": NotRequired[dict[str, Any]],
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

class SubmitRegistryRecordForApprovalRequestTypeDef(TypedDict):
    registryId: str
    recordId: str

class SynchronizeGatewayTargetsRequestTypeDef(TypedDict):
    gatewayIdentifier: str
    targetIdList: Sequence[str]

class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class TimeBasedTriggerInputTypeDef(TypedDict):
    idleSessionTimeout: NotRequired[int]

class TimeBasedTriggerTypeDef(TypedDict):
    idleSessionTimeout: NotRequired[int]

class TokenBasedTriggerInputTypeDef(TypedDict):
    tokenCount: NotRequired[int]

class TokenBasedTriggerTypeDef(TypedDict):
    tokenCount: NotRequired[int]

class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]

class UpdateAgentRuntimeEndpointRequestTypeDef(TypedDict):
    agentRuntimeId: str
    endpointName: str
    agentRuntimeVersion: NotRequired[str]
    description: NotRequired[str]
    clientToken: NotRequired[str]

class UpdateApiKeyCredentialProviderRequestTypeDef(TypedDict):
    name: str
    apiKey: str

class UpdatedDescriptionTypeDef(TypedDict):
    optionalValue: NotRequired[str]

class UpdatedSynchronizationTypeTypeDef(TypedDict):
    optionalValue: NotRequired[Literal["URL"]]

class UpdateRegistryRecordStatusRequestTypeDef(TypedDict):
    registryId: str
    recordId: str
    status: RegistryRecordStatusType
    statusReason: str

class UpdateWorkloadIdentityRequestTypeDef(TypedDict):
    name: str
    allowedResourceOauth2ReturnUrls: NotRequired[Sequence[str]]

class A2aDescriptorTypeDef(TypedDict):
    agentCard: NotRequired[AgentCardDefinitionTypeDef]

class UpdatedSkillDefinitionTypeDef(TypedDict):
    optionalValue: NotRequired[SkillDefinitionTypeDef]

class AgentSkillsDescriptorTypeDef(TypedDict):
    skillMd: NotRequired[SkillMdDefinitionTypeDef]
    skillDefinition: NotRequired[SkillDefinitionTypeDef]

class UpdatedSkillMdDefinitionTypeDef(TypedDict):
    optionalValue: NotRequired[SkillMdDefinitionTypeDef]

class ApiGatewayToolConfigurationOutputTypeDef(TypedDict):
    toolFilters: list[ApiGatewayToolFilterOutputTypeDef]
    toolOverrides: NotRequired[list[ApiGatewayToolOverrideTypeDef]]

class ApiGatewayToolConfigurationTypeDef(TypedDict):
    toolFilters: Sequence[ApiGatewayToolFilterTypeDef]
    toolOverrides: NotRequired[Sequence[ApiGatewayToolOverrideTypeDef]]

class ApiSchemaConfigurationTypeDef(TypedDict):
    s3: NotRequired[S3ConfigurationTypeDef]
    inlinePayload: NotRequired[str]

class McpToolSchemaConfigurationTypeDef(TypedDict):
    s3: NotRequired[S3ConfigurationTypeDef]
    inlinePayload: NotRequired[str]

class UpdatedApprovalConfigurationTypeDef(TypedDict):
    optionalValue: NotRequired[ApprovalConfigurationTypeDef]

class AuthorizationDataTypeDef(TypedDict):
    oauth2: NotRequired[OAuth2AuthorizationDataTypeDef]

class AuthorizingClaimMatchValueTypeOutputTypeDef(TypedDict):
    claimMatchValue: ClaimMatchValueTypeOutputTypeDef
    claimMatchOperator: ClaimMatchOperatorTypeType

class BedrockEvaluatorModelConfigOutputTypeDef(TypedDict):
    modelId: str
    inferenceConfig: NotRequired[InferenceConfigurationOutputTypeDef]
    additionalModelRequestFields: NotRequired[dict[str, Any]]

class BedrockEvaluatorModelConfigTypeDef(TypedDict):
    modelId: str
    inferenceConfig: NotRequired[InferenceConfigurationTypeDef]
    additionalModelRequestFields: NotRequired[Mapping[str, Any]]

class BrowserNetworkConfigurationOutputTypeDef(TypedDict):
    networkMode: BrowserNetworkModeType
    vpcConfig: NotRequired[VpcConfigOutputTypeDef]

class CodeInterpreterNetworkConfigurationOutputTypeDef(TypedDict):
    networkMode: CodeInterpreterNetworkModeType
    vpcConfig: NotRequired[VpcConfigOutputTypeDef]

class NetworkConfigurationOutputTypeDef(TypedDict):
    networkMode: NetworkModeType
    networkModeConfig: NotRequired[VpcConfigOutputTypeDef]

class BrowserNetworkConfigurationTypeDef(TypedDict):
    networkMode: BrowserNetworkModeType
    vpcConfig: NotRequired[VpcConfigTypeDef]

class CodeInterpreterNetworkConfigurationTypeDef(TypedDict):
    networkMode: CodeInterpreterNetworkModeType
    vpcConfig: NotRequired[VpcConfigTypeDef]

class NetworkConfigurationTypeDef(TypedDict):
    networkMode: NetworkModeType
    networkModeConfig: NotRequired[VpcConfigTypeDef]

class CertificateLocationTypeDef(TypedDict):
    secretsManager: NotRequired[SecretsManagerLocationTypeDef]

ClaimMatchValueTypeUnionTypeDef = Union[
    ClaimMatchValueTypeTypeDef, ClaimMatchValueTypeOutputTypeDef
]

class DataSourceConfigOutputTypeDef(TypedDict):
    cloudWatchLogs: NotRequired[CloudWatchLogsInputConfigOutputTypeDef]

class DataSourceConfigTypeDef(TypedDict):
    cloudWatchLogs: NotRequired[CloudWatchLogsInputConfigTypeDef]

class OutputConfigTypeDef(TypedDict):
    cloudWatchConfig: CloudWatchOutputConfigTypeDef

class CodeBasedEvaluatorConfigTypeDef(TypedDict):
    lambdaConfig: NotRequired[LambdaEvaluatorConfigTypeDef]

class CodeTypeDef(TypedDict):
    s3: NotRequired[S3LocationTypeDef]

class RecordingConfigTypeDef(TypedDict):
    enabled: NotRequired[bool]
    s3Location: NotRequired[S3LocationTypeDef]

class ResourceLocationTypeDef(TypedDict):
    s3: NotRequired[S3LocationTypeDef]

class KinesisResourceOutputTypeDef(TypedDict):
    dataStreamArn: str
    contentConfigurations: list[ContentConfigurationTypeDef]

class KinesisResourceTypeDef(TypedDict):
    dataStreamArn: str
    contentConfigurations: Sequence[ContentConfigurationTypeDef]

class CreateAgentRuntimeEndpointResponseTypeDef(TypedDict):
    targetVersion: str
    agentRuntimeEndpointArn: str
    agentRuntimeArn: str
    agentRuntimeId: str
    endpointName: str
    status: AgentRuntimeEndpointStatusType
    createdAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateBrowserProfileResponseTypeDef(TypedDict):
    profileId: str
    profileArn: str
    createdAt: datetime
    status: BrowserProfileStatusType
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

class CreateEvaluatorResponseTypeDef(TypedDict):
    evaluatorArn: str
    evaluatorId: str
    createdAt: datetime
    status: EvaluatorStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class CreatePolicyEngineResponseTypeDef(TypedDict):
    policyEngineId: str
    name: str
    description: str
    createdAt: datetime
    updatedAt: datetime
    policyEngineArn: str
    status: PolicyEngineStatusType
    statusReasons: list[str]
    encryptionKeyArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRegistryRecordResponseTypeDef(TypedDict):
    recordArn: str
    status: RegistryRecordStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateRegistryResponseTypeDef(TypedDict):
    registryArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class CreateWorkloadIdentityResponseTypeDef(TypedDict):
    name: str
    workloadIdentityArn: str
    allowedResourceOauth2ReturnUrls: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAgentRuntimeEndpointResponseTypeDef(TypedDict):
    status: AgentRuntimeEndpointStatusType
    agentRuntimeId: str
    endpointName: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteAgentRuntimeResponseTypeDef(TypedDict):
    status: AgentRuntimeStatusType
    agentRuntimeId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteBrowserProfileResponseTypeDef(TypedDict):
    profileId: str
    profileArn: str
    status: BrowserProfileStatusType
    lastUpdatedAt: datetime
    lastSavedAt: datetime
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

class DeleteEvaluatorResponseTypeDef(TypedDict):
    evaluatorArn: str
    evaluatorId: str
    status: EvaluatorStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteGatewayResponseTypeDef(TypedDict):
    gatewayId: str
    status: GatewayStatusType
    statusReasons: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteGatewayTargetResponseTypeDef(TypedDict):
    gatewayArn: str
    targetId: str
    status: TargetStatusType
    statusReasons: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteMemoryOutputTypeDef(TypedDict):
    memoryId: str
    status: MemoryStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteOnlineEvaluationConfigResponseTypeDef(TypedDict):
    onlineEvaluationConfigArn: str
    onlineEvaluationConfigId: str
    status: OnlineEvaluationConfigStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class DeletePolicyEngineResponseTypeDef(TypedDict):
    policyEngineId: str
    name: str
    description: str
    createdAt: datetime
    updatedAt: datetime
    policyEngineArn: str
    status: PolicyEngineStatusType
    statusReasons: list[str]
    encryptionKeyArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteRegistryResponseTypeDef(TypedDict):
    status: RegistryStatusType
    ResponseMetadata: ResponseMetadataTypeDef

GetAgentRuntimeEndpointResponseTypeDef = TypedDict(
    "GetAgentRuntimeEndpointResponseTypeDef",
    {
        "liveVersion": str,
        "targetVersion": str,
        "agentRuntimeEndpointArn": str,
        "agentRuntimeArn": str,
        "description": str,
        "status": AgentRuntimeEndpointStatusType,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "failureReason": str,
        "name": str,
        "id": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class GetBrowserProfileResponseTypeDef(TypedDict):
    profileId: str
    profileArn: str
    name: str
    description: str
    status: BrowserProfileStatusType
    createdAt: datetime
    lastUpdatedAt: datetime
    lastSavedAt: datetime
    lastSavedBrowserSessionId: str
    lastSavedBrowserId: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetPolicyEngineResponseTypeDef(TypedDict):
    policyEngineId: str
    name: str
    description: str
    createdAt: datetime
    updatedAt: datetime
    policyEngineArn: str
    status: PolicyEngineStatusType
    statusReasons: list[str]
    encryptionKeyArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetResourcePolicyResponseTypeDef(TypedDict):
    policy: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetWorkloadIdentityResponseTypeDef(TypedDict):
    name: str
    workloadIdentityArn: str
    allowedResourceOauth2ReturnUrls: list[str]
    createdTime: datetime
    lastUpdatedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ListAgentRuntimeEndpointsResponseTypeDef(TypedDict):
    runtimeEndpoints: list[AgentRuntimeEndpointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAgentRuntimeVersionsResponseTypeDef(TypedDict):
    agentRuntimes: list[AgentRuntimeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListAgentRuntimesResponseTypeDef(TypedDict):
    agentRuntimes: list[AgentRuntimeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListApiKeyCredentialProvidersResponseTypeDef(TypedDict):
    credentialProviders: list[ApiKeyCredentialProviderItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListBrowserProfilesResponseTypeDef(TypedDict):
    profileSummaries: list[BrowserProfileSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListBrowsersResponseTypeDef(TypedDict):
    browserSummaries: list[BrowserSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListCodeInterpretersResponseTypeDef(TypedDict):
    codeInterpreterSummaries: list[CodeInterpreterSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class PutResourcePolicyResponseTypeDef(TypedDict):
    policy: str
    ResponseMetadata: ResponseMetadataTypeDef

class SubmitRegistryRecordForApprovalResponseTypeDef(TypedDict):
    registryArn: str
    recordArn: str
    recordId: str
    status: RegistryRecordStatusType
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAgentRuntimeEndpointResponseTypeDef(TypedDict):
    liveVersion: str
    targetVersion: str
    agentRuntimeEndpointArn: str
    agentRuntimeArn: str
    status: AgentRuntimeEndpointStatusType
    createdAt: datetime
    lastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateEvaluatorResponseTypeDef(TypedDict):
    evaluatorArn: str
    evaluatorId: str
    updatedAt: datetime
    status: EvaluatorStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateOnlineEvaluationConfigResponseTypeDef(TypedDict):
    onlineEvaluationConfigArn: str
    onlineEvaluationConfigId: str
    updatedAt: datetime
    status: OnlineEvaluationConfigStatusType
    executionStatus: OnlineEvaluationExecutionStatusType
    failureReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePolicyEngineResponseTypeDef(TypedDict):
    policyEngineId: str
    name: str
    description: str
    createdAt: datetime
    updatedAt: datetime
    policyEngineArn: str
    status: PolicyEngineStatusType
    statusReasons: list[str]
    encryptionKeyArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRegistryRecordStatusResponseTypeDef(TypedDict):
    registryArn: str
    recordArn: str
    recordId: str
    status: RegistryRecordStatusType
    statusReason: str
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateWorkloadIdentityResponseTypeDef(TypedDict):
    name: str
    workloadIdentityArn: str
    allowedResourceOauth2ReturnUrls: list[str]
    createdTime: datetime
    lastUpdatedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CreateAgentRuntimeResponseTypeDef(TypedDict):
    agentRuntimeArn: str
    workloadIdentityDetails: WorkloadIdentityDetailsTypeDef
    agentRuntimeId: str
    agentRuntimeVersion: str
    createdAt: datetime
    status: AgentRuntimeStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateAgentRuntimeResponseTypeDef(TypedDict):
    agentRuntimeArn: str
    agentRuntimeId: str
    workloadIdentityDetails: WorkloadIdentityDetailsTypeDef
    agentRuntimeVersion: str
    createdAt: datetime
    lastUpdatedAt: datetime
    status: AgentRuntimeStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class CreateApiKeyCredentialProviderResponseTypeDef(TypedDict):
    apiKeySecretArn: SecretTypeDef
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
    iamCredentialProvider: NotRequired[IamCredentialProviderTypeDef]

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
    episodicConsolidationOverride: NotRequired[
        EpisodicOverrideConsolidationConfigurationInputTypeDef
    ]

class CustomConsolidationConfigurationTypeDef(TypedDict):
    semanticConsolidationOverride: NotRequired[SemanticConsolidationOverrideTypeDef]
    summaryConsolidationOverride: NotRequired[SummaryConsolidationOverrideTypeDef]
    userPreferenceConsolidationOverride: NotRequired[UserPreferenceConsolidationOverrideTypeDef]
    episodicConsolidationOverride: NotRequired[EpisodicConsolidationOverrideTypeDef]

class UpdatedCustomDescriptorTypeDef(TypedDict):
    optionalValue: NotRequired[CustomDescriptorTypeDef]

class SemanticOverrideConfigurationInputTypeDef(TypedDict):
    extraction: NotRequired[SemanticOverrideExtractionConfigurationInputTypeDef]
    consolidation: NotRequired[SemanticOverrideConsolidationConfigurationInputTypeDef]

class CustomExtractionConfigurationInputTypeDef(TypedDict):
    semanticExtractionOverride: NotRequired[SemanticOverrideExtractionConfigurationInputTypeDef]
    userPreferenceExtractionOverride: NotRequired[
        UserPreferenceOverrideExtractionConfigurationInputTypeDef
    ]
    episodicExtractionOverride: NotRequired[EpisodicOverrideExtractionConfigurationInputTypeDef]

class UserPreferenceOverrideConfigurationInputTypeDef(TypedDict):
    extraction: NotRequired[UserPreferenceOverrideExtractionConfigurationInputTypeDef]
    consolidation: NotRequired[UserPreferenceOverrideConsolidationConfigurationInputTypeDef]

class CustomExtractionConfigurationTypeDef(TypedDict):
    semanticExtractionOverride: NotRequired[SemanticExtractionOverrideTypeDef]
    userPreferenceExtractionOverride: NotRequired[UserPreferenceExtractionOverrideTypeDef]
    episodicExtractionOverride: NotRequired[EpisodicExtractionOverrideTypeDef]

class CustomReflectionConfigurationInputTypeDef(TypedDict):
    episodicReflectionOverride: NotRequired[EpisodicOverrideReflectionConfigurationInputTypeDef]

class EpisodicOverrideConfigurationInputTypeDef(TypedDict):
    extraction: NotRequired[EpisodicOverrideExtractionConfigurationInputTypeDef]
    consolidation: NotRequired[EpisodicOverrideConsolidationConfigurationInputTypeDef]
    reflection: NotRequired[EpisodicOverrideReflectionConfigurationInputTypeDef]

class CustomReflectionConfigurationTypeDef(TypedDict):
    episodicReflectionOverride: NotRequired[EpisodicReflectionOverrideTypeDef]

class EpisodicMemoryStrategyInputTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    namespaces: NotRequired[Sequence[str]]
    namespaceTemplates: NotRequired[Sequence[str]]
    reflectionConfiguration: NotRequired[EpisodicReflectionConfigurationInputTypeDef]

class ListEvaluatorsResponseTypeDef(TypedDict):
    evaluators: list[EvaluatorSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class FilesystemConfigurationTypeDef(TypedDict):
    sessionStorage: NotRequired[SessionStorageConfigurationTypeDef]

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "key": str,
        "operator": FilterOperatorType,
        "value": FilterValueTypeDef,
    },
)

class GatewayProtocolConfigurationOutputTypeDef(TypedDict):
    mcp: NotRequired[MCPGatewayConfigurationOutputTypeDef]

class GatewayProtocolConfigurationTypeDef(TypedDict):
    mcp: NotRequired[MCPGatewayConfigurationTypeDef]

class ListGatewaysResponseTypeDef(TypedDict):
    items: list[GatewaySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GetMemoryInputWaitTypeDef(TypedDict):
    memoryId: str
    view: NotRequired[MemoryViewType]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetPolicyEngineRequestWaitExtraTypeDef(TypedDict):
    policyEngineId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetPolicyEngineRequestWaitTypeDef(TypedDict):
    policyEngineId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetPolicyGenerationRequestWaitTypeDef(TypedDict):
    policyGenerationId: str
    policyEngineId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetPolicyRequestWaitExtraTypeDef(TypedDict):
    policyEngineId: str
    policyId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetPolicyRequestWaitTypeDef(TypedDict):
    policyEngineId: str
    policyId: str
    WaiterConfig: NotRequired[WaiterConfigTypeDef]

class GetPolicyGenerationResponseTypeDef(TypedDict):
    policyEngineId: str
    policyGenerationId: str
    name: str
    policyGenerationArn: str
    resource: ResourceTypeDef
    createdAt: datetime
    updatedAt: datetime
    status: PolicyGenerationStatusType
    statusReasons: list[str]
    findings: str
    ResponseMetadata: ResponseMetadataTypeDef

class PolicyGenerationTypeDef(TypedDict):
    policyEngineId: str
    policyGenerationId: str
    name: str
    policyGenerationArn: str
    resource: ResourceTypeDef
    createdAt: datetime
    updatedAt: datetime
    status: PolicyGenerationStatusType
    statusReasons: list[str]
    findings: NotRequired[str]

class StartPolicyGenerationRequestTypeDef(TypedDict):
    policyEngineId: str
    resource: ResourceTypeDef
    content: ContentTypeDef
    name: str
    clientToken: NotRequired[str]

class StartPolicyGenerationResponseTypeDef(TypedDict):
    policyEngineId: str
    policyGenerationId: str
    name: str
    policyGenerationArn: str
    resource: ResourceTypeDef
    createdAt: datetime
    updatedAt: datetime
    status: PolicyGenerationStatusType
    statusReasons: list[str]
    findings: str
    ResponseMetadata: ResponseMetadataTypeDef

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

InterceptorConfigurationTypeDef = TypedDict(
    "InterceptorConfigurationTypeDef",
    {
        "lambda": NotRequired[LambdaInterceptorConfigurationTypeDef],
    },
)

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

class ListBrowserProfilesRequestPaginateTypeDef(TypedDict):
    name: NotRequired[str]
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

class ListEvaluatorsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListGatewayTargetsRequestPaginateTypeDef(TypedDict):
    gatewayIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListGatewaysRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListMemoriesInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOauth2CredentialProvidersRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOnlineEvaluationConfigsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPoliciesRequestPaginateTypeDef(TypedDict):
    policyEngineId: str
    targetResourceScope: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPolicyEnginesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPolicyGenerationAssetsRequestPaginateTypeDef(TypedDict):
    policyGenerationId: str
    policyEngineId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPolicyGenerationsRequestPaginateTypeDef(TypedDict):
    policyEngineId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRegistriesRequestPaginateTypeDef(TypedDict):
    status: NotRequired[RegistryStatusType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRegistryRecordsRequestPaginateTypeDef(TypedDict):
    registryId: str
    name: NotRequired[str]
    status: NotRequired[RegistryRecordStatusType]
    descriptorType: NotRequired[DescriptorTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListWorkloadIdentitiesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListGatewayTargetsResponseTypeDef(TypedDict):
    items: list[TargetSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListMemoriesOutputTypeDef(TypedDict):
    memories: list[MemorySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListOauth2CredentialProvidersResponseTypeDef(TypedDict):
    credentialProviders: list[Oauth2CredentialProviderItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListOnlineEvaluationConfigsResponseTypeDef(TypedDict):
    onlineEvaluationConfigs: list[OnlineEvaluationConfigSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListPolicyEnginesResponseTypeDef(TypedDict):
    policyEngines: list[PolicyEngineTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListRegistriesResponseTypeDef(TypedDict):
    registries: list[RegistrySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListRegistryRecordsResponseTypeDef(TypedDict):
    registryRecords: list[RegistryRecordSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListWorkloadIdentitiesResponseTypeDef(TypedDict):
    workloadIdentities: list[WorkloadIdentityTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class UpdatedServerDefinitionTypeDef(TypedDict):
    optionalValue: NotRequired[ServerDefinitionTypeDef]

class McpDescriptorTypeDef(TypedDict):
    server: NotRequired[ServerDefinitionTypeDef]
    tools: NotRequired[ToolsDefinitionTypeDef]

class UpdatedToolsDefinitionTypeDef(TypedDict):
    optionalValue: NotRequired[ToolsDefinitionTypeDef]

MetadataConfigurationUnionTypeDef = Union[
    MetadataConfigurationTypeDef, MetadataConfigurationOutputTypeDef
]

class RatingScaleOutputTypeDef(TypedDict):
    numerical: NotRequired[list[NumericalScaleDefinitionTypeDef]]
    categorical: NotRequired[list[CategoricalScaleDefinitionTypeDef]]

class RatingScaleTypeDef(TypedDict):
    numerical: NotRequired[Sequence[NumericalScaleDefinitionTypeDef]]
    categorical: NotRequired[Sequence[CategoricalScaleDefinitionTypeDef]]

OAuthCredentialProviderUnionTypeDef = Union[
    OAuthCredentialProviderTypeDef, OAuthCredentialProviderOutputTypeDef
]

class Oauth2DiscoveryOutputTypeDef(TypedDict):
    discoveryUrl: NotRequired[str]
    authorizationServerMetadata: NotRequired[Oauth2AuthorizationServerMetadataOutputTypeDef]

Oauth2AuthorizationServerMetadataUnionTypeDef = Union[
    Oauth2AuthorizationServerMetadataTypeDef, Oauth2AuthorizationServerMetadataOutputTypeDef
]

class PolicyDefinitionTypeDef(TypedDict):
    cedar: NotRequired[CedarPolicyTypeDef]
    policyGeneration: NotRequired[PolicyGenerationDetailsTypeDef]

class PrivateEndpointOutputTypeDef(TypedDict):
    selfManagedLatticeResource: NotRequired[SelfManagedLatticeResourceTypeDef]
    managedLatticeResource: NotRequired[ManagedLatticeResourceOutputTypeDef]

class PrivateEndpointTypeDef(TypedDict):
    selfManagedLatticeResource: NotRequired[SelfManagedLatticeResourceTypeDef]
    managedLatticeResource: NotRequired[ManagedLatticeResourceTypeDef]

class RegistryRecordCredentialProviderUnionOutputTypeDef(TypedDict):
    oauthCredentialProvider: NotRequired[RegistryRecordOAuthCredentialProviderOutputTypeDef]
    iamCredentialProvider: NotRequired[RegistryRecordIamCredentialProviderTypeDef]

RegistryRecordOAuthCredentialProviderUnionTypeDef = Union[
    RegistryRecordOAuthCredentialProviderTypeDef, RegistryRecordOAuthCredentialProviderOutputTypeDef
]
RequestHeaderConfigurationUnionTypeDef = Union[
    RequestHeaderConfigurationTypeDef, RequestHeaderConfigurationOutputTypeDef
]

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

class TriggerConditionInputTypeDef(TypedDict):
    messageBasedTrigger: NotRequired[MessageBasedTriggerInputTypeDef]
    tokenBasedTrigger: NotRequired[TokenBasedTriggerInputTypeDef]
    timeBasedTrigger: NotRequired[TimeBasedTriggerInputTypeDef]

class TriggerConditionTypeDef(TypedDict):
    messageBasedTrigger: NotRequired[MessageBasedTriggerTypeDef]
    tokenBasedTrigger: NotRequired[TokenBasedTriggerTypeDef]
    timeBasedTrigger: NotRequired[TimeBasedTriggerTypeDef]

class UpdatePolicyEngineRequestTypeDef(TypedDict):
    policyEngineId: str
    description: NotRequired[UpdatedDescriptionTypeDef]

class UpdatedA2aDescriptorTypeDef(TypedDict):
    optionalValue: NotRequired[A2aDescriptorTypeDef]

class UpdatedAgentSkillsDescriptorFieldsTypeDef(TypedDict):
    skillMd: NotRequired[UpdatedSkillMdDefinitionTypeDef]
    skillDefinition: NotRequired[UpdatedSkillDefinitionTypeDef]

class ApiGatewayTargetConfigurationOutputTypeDef(TypedDict):
    restApiId: str
    stage: str
    apiGatewayToolConfiguration: ApiGatewayToolConfigurationOutputTypeDef

class ApiGatewayTargetConfigurationTypeDef(TypedDict):
    restApiId: str
    stage: str
    apiGatewayToolConfiguration: ApiGatewayToolConfigurationTypeDef

class McpServerTargetConfigurationTypeDef(TypedDict):
    endpoint: str
    mcpToolSchema: NotRequired[McpToolSchemaConfigurationTypeDef]
    listingMode: NotRequired[ListingModeType]

class CustomClaimValidationTypeOutputTypeDef(TypedDict):
    inboundTokenClaimName: str
    inboundTokenClaimValueType: InboundTokenClaimValueTypeType
    authorizingClaimMatchValue: AuthorizingClaimMatchValueTypeOutputTypeDef

class EvaluatorModelConfigOutputTypeDef(TypedDict):
    bedrockEvaluatorModelConfig: NotRequired[BedrockEvaluatorModelConfigOutputTypeDef]

class EvaluatorModelConfigTypeDef(TypedDict):
    bedrockEvaluatorModelConfig: NotRequired[BedrockEvaluatorModelConfigTypeDef]

BrowserNetworkConfigurationUnionTypeDef = Union[
    BrowserNetworkConfigurationTypeDef, BrowserNetworkConfigurationOutputTypeDef
]
CodeInterpreterNetworkConfigurationUnionTypeDef = Union[
    CodeInterpreterNetworkConfigurationTypeDef, CodeInterpreterNetworkConfigurationOutputTypeDef
]
NetworkConfigurationUnionTypeDef = Union[
    NetworkConfigurationTypeDef, NetworkConfigurationOutputTypeDef
]

class CertificateTypeDef(TypedDict):
    location: CertificateLocationTypeDef

class AuthorizingClaimMatchValueTypeTypeDef(TypedDict):
    claimMatchValue: ClaimMatchValueTypeUnionTypeDef
    claimMatchOperator: ClaimMatchOperatorTypeType

DataSourceConfigUnionTypeDef = Union[DataSourceConfigTypeDef, DataSourceConfigOutputTypeDef]

class CreateOnlineEvaluationConfigResponseTypeDef(TypedDict):
    onlineEvaluationConfigArn: str
    onlineEvaluationConfigId: str
    createdAt: datetime
    outputConfig: OutputConfigTypeDef
    status: OnlineEvaluationConfigStatusType
    executionStatus: OnlineEvaluationExecutionStatusType
    failureReason: str
    ResponseMetadata: ResponseMetadataTypeDef

class CodeConfigurationOutputTypeDef(TypedDict):
    code: CodeTypeDef
    runtime: AgentManagedRuntimeTypeType
    entryPoint: list[str]

class CodeConfigurationTypeDef(TypedDict):
    code: CodeTypeDef
    runtime: AgentManagedRuntimeTypeType
    entryPoint: Sequence[str]

BrowserEnterprisePolicyTypeDef = TypedDict(
    "BrowserEnterprisePolicyTypeDef",
    {
        "location": ResourceLocationTypeDef,
        "type": NotRequired[BrowserEnterprisePolicyTypeType],
    },
)

class StreamDeliveryResourceOutputTypeDef(TypedDict):
    kinesis: NotRequired[KinesisResourceOutputTypeDef]

class StreamDeliveryResourceTypeDef(TypedDict):
    kinesis: NotRequired[KinesisResourceTypeDef]

class CredentialProviderConfigurationOutputTypeDef(TypedDict):
    credentialProviderType: CredentialProviderTypeType
    credentialProvider: NotRequired[CredentialProviderOutputTypeDef]

class ModifyConsolidationConfigurationTypeDef(TypedDict):
    customConsolidationConfiguration: NotRequired[CustomConsolidationConfigurationInputTypeDef]

class ConsolidationConfigurationTypeDef(TypedDict):
    customConsolidationConfiguration: NotRequired[CustomConsolidationConfigurationTypeDef]

class ModifyExtractionConfigurationTypeDef(TypedDict):
    customExtractionConfiguration: NotRequired[CustomExtractionConfigurationInputTypeDef]

class ExtractionConfigurationTypeDef(TypedDict):
    customExtractionConfiguration: NotRequired[CustomExtractionConfigurationTypeDef]

class ModifyReflectionConfigurationTypeDef(TypedDict):
    episodicReflectionConfiguration: NotRequired[EpisodicReflectionConfigurationInputTypeDef]
    customReflectionConfiguration: NotRequired[CustomReflectionConfigurationInputTypeDef]

class ReflectionConfigurationTypeDef(TypedDict):
    customReflectionConfiguration: NotRequired[CustomReflectionConfigurationTypeDef]
    episodicReflectionConfiguration: NotRequired[EpisodicReflectionConfigurationTypeDef]

class RuleOutputTypeDef(TypedDict):
    samplingConfig: SamplingConfigTypeDef
    filters: NotRequired[list[FilterTypeDef]]
    sessionConfig: NotRequired[SessionConfigTypeDef]

class RuleTypeDef(TypedDict):
    samplingConfig: SamplingConfigTypeDef
    filters: NotRequired[Sequence[FilterTypeDef]]
    sessionConfig: NotRequired[SessionConfigTypeDef]

GatewayProtocolConfigurationUnionTypeDef = Union[
    GatewayProtocolConfigurationTypeDef, GatewayProtocolConfigurationOutputTypeDef
]

class ListPolicyGenerationsResponseTypeDef(TypedDict):
    policyGenerations: list[PolicyGenerationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class GatewayInterceptorConfigurationOutputTypeDef(TypedDict):
    interceptor: InterceptorConfigurationTypeDef
    interceptionPoints: list[GatewayInterceptionPointType]
    inputConfiguration: NotRequired[InterceptorInputConfigurationTypeDef]

class GatewayInterceptorConfigurationTypeDef(TypedDict):
    interceptor: InterceptorConfigurationTypeDef
    interceptionPoints: Sequence[GatewayInterceptionPointType]
    inputConfiguration: NotRequired[InterceptorInputConfigurationTypeDef]

class DescriptorsTypeDef(TypedDict):
    mcp: NotRequired[McpDescriptorTypeDef]
    a2a: NotRequired[A2aDescriptorTypeDef]
    custom: NotRequired[CustomDescriptorTypeDef]
    agentSkills: NotRequired[AgentSkillsDescriptorTypeDef]

class UpdatedMcpDescriptorFieldsTypeDef(TypedDict):
    server: NotRequired[UpdatedServerDefinitionTypeDef]
    tools: NotRequired[UpdatedToolsDefinitionTypeDef]

class CredentialProviderTypeDef(TypedDict):
    oauthCredentialProvider: NotRequired[OAuthCredentialProviderUnionTypeDef]
    apiKeyCredentialProvider: NotRequired[ApiKeyCredentialProviderTypeDef]
    iamCredentialProvider: NotRequired[IamCredentialProviderTypeDef]

class AtlassianOauth2ProviderConfigOutputTypeDef(TypedDict):
    oauthDiscovery: Oauth2DiscoveryOutputTypeDef
    clientId: NotRequired[str]

class CustomOauth2ProviderConfigOutputTypeDef(TypedDict):
    oauthDiscovery: Oauth2DiscoveryOutputTypeDef
    clientId: NotRequired[str]

class GithubOauth2ProviderConfigOutputTypeDef(TypedDict):
    oauthDiscovery: Oauth2DiscoveryOutputTypeDef
    clientId: NotRequired[str]

class GoogleOauth2ProviderConfigOutputTypeDef(TypedDict):
    oauthDiscovery: Oauth2DiscoveryOutputTypeDef
    clientId: NotRequired[str]

class IncludedOauth2ProviderConfigOutputTypeDef(TypedDict):
    oauthDiscovery: Oauth2DiscoveryOutputTypeDef
    clientId: NotRequired[str]

class LinkedinOauth2ProviderConfigOutputTypeDef(TypedDict):
    oauthDiscovery: Oauth2DiscoveryOutputTypeDef
    clientId: NotRequired[str]

class MicrosoftOauth2ProviderConfigOutputTypeDef(TypedDict):
    oauthDiscovery: Oauth2DiscoveryOutputTypeDef
    clientId: NotRequired[str]

class SalesforceOauth2ProviderConfigOutputTypeDef(TypedDict):
    oauthDiscovery: Oauth2DiscoveryOutputTypeDef
    clientId: NotRequired[str]

class SlackOauth2ProviderConfigOutputTypeDef(TypedDict):
    oauthDiscovery: Oauth2DiscoveryOutputTypeDef
    clientId: NotRequired[str]

class Oauth2DiscoveryTypeDef(TypedDict):
    discoveryUrl: NotRequired[str]
    authorizationServerMetadata: NotRequired[Oauth2AuthorizationServerMetadataUnionTypeDef]

class CreatePolicyRequestTypeDef(TypedDict):
    name: str
    definition: PolicyDefinitionTypeDef
    policyEngineId: str
    description: NotRequired[str]
    validationMode: NotRequired[PolicyValidationModeType]
    clientToken: NotRequired[str]

class CreatePolicyResponseTypeDef(TypedDict):
    policyId: str
    name: str
    policyEngineId: str
    definition: PolicyDefinitionTypeDef
    description: str
    createdAt: datetime
    updatedAt: datetime
    policyArn: str
    status: PolicyStatusType
    statusReasons: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class DeletePolicyResponseTypeDef(TypedDict):
    policyId: str
    name: str
    policyEngineId: str
    definition: PolicyDefinitionTypeDef
    description: str
    createdAt: datetime
    updatedAt: datetime
    policyArn: str
    status: PolicyStatusType
    statusReasons: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetPolicyResponseTypeDef(TypedDict):
    policyId: str
    name: str
    policyEngineId: str
    definition: PolicyDefinitionTypeDef
    description: str
    createdAt: datetime
    updatedAt: datetime
    policyArn: str
    status: PolicyStatusType
    statusReasons: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class PolicyGenerationAssetTypeDef(TypedDict):
    policyGenerationAssetId: str
    rawTextFragment: str
    findings: list[FindingTypeDef]
    definition: NotRequired[PolicyDefinitionTypeDef]

class PolicyTypeDef(TypedDict):
    policyId: str
    name: str
    policyEngineId: str
    definition: PolicyDefinitionTypeDef
    createdAt: datetime
    updatedAt: datetime
    policyArn: str
    status: PolicyStatusType
    statusReasons: list[str]
    description: NotRequired[str]

class UpdatePolicyRequestTypeDef(TypedDict):
    policyEngineId: str
    policyId: str
    description: NotRequired[UpdatedDescriptionTypeDef]
    definition: NotRequired[PolicyDefinitionTypeDef]
    validationMode: NotRequired[PolicyValidationModeType]

class UpdatePolicyResponseTypeDef(TypedDict):
    policyId: str
    name: str
    policyEngineId: str
    definition: PolicyDefinitionTypeDef
    description: str
    createdAt: datetime
    updatedAt: datetime
    policyArn: str
    status: PolicyStatusType
    statusReasons: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

PrivateEndpointUnionTypeDef = Union[PrivateEndpointTypeDef, PrivateEndpointOutputTypeDef]

class RegistryRecordCredentialProviderConfigurationOutputTypeDef(TypedDict):
    credentialProviderType: RegistryRecordCredentialProviderTypeType
    credentialProvider: RegistryRecordCredentialProviderUnionOutputTypeDef

class RegistryRecordCredentialProviderUnionTypeDef(TypedDict):
    oauthCredentialProvider: NotRequired[RegistryRecordOAuthCredentialProviderUnionTypeDef]
    iamCredentialProvider: NotRequired[RegistryRecordIamCredentialProviderTypeDef]

class ToolSchemaOutputTypeDef(TypedDict):
    s3: NotRequired[S3ConfigurationTypeDef]
    inlinePayload: NotRequired[list[ToolDefinitionOutputTypeDef]]

class ToolSchemaTypeDef(TypedDict):
    s3: NotRequired[S3ConfigurationTypeDef]
    inlinePayload: NotRequired[Sequence[ToolDefinitionTypeDef]]

class ModifySelfManagedConfigurationTypeDef(TypedDict):
    triggerConditions: NotRequired[Sequence[TriggerConditionInputTypeDef]]
    invocationConfiguration: NotRequired[ModifyInvocationConfigurationInputTypeDef]
    historicalContextWindowSize: NotRequired[int]

class SelfManagedConfigurationInputTypeDef(TypedDict):
    invocationConfiguration: InvocationConfigurationInputTypeDef
    triggerConditions: NotRequired[Sequence[TriggerConditionInputTypeDef]]
    historicalContextWindowSize: NotRequired[int]

class SelfManagedConfigurationTypeDef(TypedDict):
    triggerConditions: list[TriggerConditionTypeDef]
    invocationConfiguration: InvocationConfigurationTypeDef
    historicalContextWindowSize: int

class UpdatedAgentSkillsDescriptorTypeDef(TypedDict):
    optionalValue: NotRequired[UpdatedAgentSkillsDescriptorFieldsTypeDef]

class CustomJWTAuthorizerConfigurationOutputTypeDef(TypedDict):
    discoveryUrl: str
    allowedAudience: NotRequired[list[str]]
    allowedClients: NotRequired[list[str]]
    allowedScopes: NotRequired[list[str]]
    customClaims: NotRequired[list[CustomClaimValidationTypeOutputTypeDef]]

class LlmAsAJudgeEvaluatorConfigOutputTypeDef(TypedDict):
    instructions: str
    ratingScale: RatingScaleOutputTypeDef
    modelConfig: EvaluatorModelConfigOutputTypeDef

class LlmAsAJudgeEvaluatorConfigTypeDef(TypedDict):
    instructions: str
    ratingScale: RatingScaleTypeDef
    modelConfig: EvaluatorModelConfigTypeDef

class CreateCodeInterpreterRequestTypeDef(TypedDict):
    name: str
    networkConfiguration: CodeInterpreterNetworkConfigurationUnionTypeDef
    description: NotRequired[str]
    executionRoleArn: NotRequired[str]
    certificates: NotRequired[Sequence[CertificateTypeDef]]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class GetCodeInterpreterResponseTypeDef(TypedDict):
    codeInterpreterId: str
    codeInterpreterArn: str
    name: str
    description: str
    executionRoleArn: str
    networkConfiguration: CodeInterpreterNetworkConfigurationOutputTypeDef
    status: CodeInterpreterStatusType
    certificates: list[CertificateTypeDef]
    failureReason: str
    createdAt: datetime
    lastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

AuthorizingClaimMatchValueTypeUnionTypeDef = Union[
    AuthorizingClaimMatchValueTypeTypeDef, AuthorizingClaimMatchValueTypeOutputTypeDef
]

class AgentRuntimeArtifactOutputTypeDef(TypedDict):
    containerConfiguration: NotRequired[ContainerConfigurationTypeDef]
    codeConfiguration: NotRequired[CodeConfigurationOutputTypeDef]

class AgentRuntimeArtifactTypeDef(TypedDict):
    containerConfiguration: NotRequired[ContainerConfigurationTypeDef]
    codeConfiguration: NotRequired[CodeConfigurationTypeDef]

class CreateBrowserRequestTypeDef(TypedDict):
    name: str
    networkConfiguration: BrowserNetworkConfigurationUnionTypeDef
    description: NotRequired[str]
    executionRoleArn: NotRequired[str]
    recording: NotRequired[RecordingConfigTypeDef]
    browserSigning: NotRequired[BrowserSigningConfigInputTypeDef]
    enterprisePolicies: NotRequired[Sequence[BrowserEnterprisePolicyTypeDef]]
    certificates: NotRequired[Sequence[CertificateTypeDef]]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class GetBrowserResponseTypeDef(TypedDict):
    browserId: str
    browserArn: str
    name: str
    description: str
    executionRoleArn: str
    networkConfiguration: BrowserNetworkConfigurationOutputTypeDef
    recording: RecordingConfigTypeDef
    browserSigning: BrowserSigningConfigOutputTypeDef
    enterprisePolicies: list[BrowserEnterprisePolicyTypeDef]
    certificates: list[CertificateTypeDef]
    status: BrowserStatusType
    failureReason: str
    createdAt: datetime
    lastUpdatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class StreamDeliveryResourcesOutputTypeDef(TypedDict):
    resources: list[StreamDeliveryResourceOutputTypeDef]

class StreamDeliveryResourcesTypeDef(TypedDict):
    resources: Sequence[StreamDeliveryResourceTypeDef]

class GetOnlineEvaluationConfigResponseTypeDef(TypedDict):
    onlineEvaluationConfigArn: str
    onlineEvaluationConfigId: str
    onlineEvaluationConfigName: str
    description: str
    rule: RuleOutputTypeDef
    dataSourceConfig: DataSourceConfigOutputTypeDef
    evaluators: list[EvaluatorReferenceTypeDef]
    outputConfig: OutputConfigTypeDef
    evaluationExecutionRoleArn: str
    status: OnlineEvaluationConfigStatusType
    executionStatus: OnlineEvaluationExecutionStatusType
    createdAt: datetime
    updatedAt: datetime
    failureReason: str
    ResponseMetadata: ResponseMetadataTypeDef

RuleUnionTypeDef = Union[RuleTypeDef, RuleOutputTypeDef]
GatewayInterceptorConfigurationUnionTypeDef = Union[
    GatewayInterceptorConfigurationTypeDef, GatewayInterceptorConfigurationOutputTypeDef
]

class UpdatedMcpDescriptorTypeDef(TypedDict):
    optionalValue: NotRequired[UpdatedMcpDescriptorFieldsTypeDef]

CredentialProviderUnionTypeDef = Union[CredentialProviderTypeDef, CredentialProviderOutputTypeDef]

class Oauth2ProviderConfigOutputTypeDef(TypedDict):
    customOauth2ProviderConfig: NotRequired[CustomOauth2ProviderConfigOutputTypeDef]
    googleOauth2ProviderConfig: NotRequired[GoogleOauth2ProviderConfigOutputTypeDef]
    githubOauth2ProviderConfig: NotRequired[GithubOauth2ProviderConfigOutputTypeDef]
    slackOauth2ProviderConfig: NotRequired[SlackOauth2ProviderConfigOutputTypeDef]
    salesforceOauth2ProviderConfig: NotRequired[SalesforceOauth2ProviderConfigOutputTypeDef]
    microsoftOauth2ProviderConfig: NotRequired[MicrosoftOauth2ProviderConfigOutputTypeDef]
    atlassianOauth2ProviderConfig: NotRequired[AtlassianOauth2ProviderConfigOutputTypeDef]
    linkedinOauth2ProviderConfig: NotRequired[LinkedinOauth2ProviderConfigOutputTypeDef]
    includedOauth2ProviderConfig: NotRequired[IncludedOauth2ProviderConfigOutputTypeDef]

Oauth2DiscoveryUnionTypeDef = Union[Oauth2DiscoveryTypeDef, Oauth2DiscoveryOutputTypeDef]

class ListPolicyGenerationAssetsResponseTypeDef(TypedDict):
    policyGenerationAssets: list[PolicyGenerationAssetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListPoliciesResponseTypeDef(TypedDict):
    policies: list[PolicyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class FromUrlSynchronizationConfigurationOutputTypeDef(TypedDict):
    url: str
    credentialProviderConfigurations: NotRequired[
        list[RegistryRecordCredentialProviderConfigurationOutputTypeDef]
    ]

RegistryRecordCredentialProviderUnionUnionTypeDef = Union[
    RegistryRecordCredentialProviderUnionTypeDef, RegistryRecordCredentialProviderUnionOutputTypeDef
]

class McpLambdaTargetConfigurationOutputTypeDef(TypedDict):
    lambdaArn: str
    toolSchema: ToolSchemaOutputTypeDef

class McpLambdaTargetConfigurationTypeDef(TypedDict):
    lambdaArn: str
    toolSchema: ToolSchemaTypeDef

class ModifyStrategyConfigurationTypeDef(TypedDict):
    extraction: NotRequired[ModifyExtractionConfigurationTypeDef]
    consolidation: NotRequired[ModifyConsolidationConfigurationTypeDef]
    reflection: NotRequired[ModifyReflectionConfigurationTypeDef]
    selfManagedConfiguration: NotRequired[ModifySelfManagedConfigurationTypeDef]

class CustomConfigurationInputTypeDef(TypedDict):
    semanticOverride: NotRequired[SemanticOverrideConfigurationInputTypeDef]
    summaryOverride: NotRequired[SummaryOverrideConfigurationInputTypeDef]
    userPreferenceOverride: NotRequired[UserPreferenceOverrideConfigurationInputTypeDef]
    episodicOverride: NotRequired[EpisodicOverrideConfigurationInputTypeDef]
    selfManagedConfiguration: NotRequired[SelfManagedConfigurationInputTypeDef]

StrategyConfigurationTypeDef = TypedDict(
    "StrategyConfigurationTypeDef",
    {
        "type": NotRequired[OverrideTypeType],
        "extraction": NotRequired[ExtractionConfigurationTypeDef],
        "consolidation": NotRequired[ConsolidationConfigurationTypeDef],
        "reflection": NotRequired[ReflectionConfigurationTypeDef],
        "selfManagedConfiguration": NotRequired[SelfManagedConfigurationTypeDef],
    },
)

class AuthorizerConfigurationOutputTypeDef(TypedDict):
    customJWTAuthorizer: NotRequired[CustomJWTAuthorizerConfigurationOutputTypeDef]

class EvaluatorConfigOutputTypeDef(TypedDict):
    llmAsAJudge: NotRequired[LlmAsAJudgeEvaluatorConfigOutputTypeDef]
    codeBased: NotRequired[CodeBasedEvaluatorConfigTypeDef]

class EvaluatorConfigTypeDef(TypedDict):
    llmAsAJudge: NotRequired[LlmAsAJudgeEvaluatorConfigTypeDef]
    codeBased: NotRequired[CodeBasedEvaluatorConfigTypeDef]

class CustomClaimValidationTypeTypeDef(TypedDict):
    inboundTokenClaimName: str
    inboundTokenClaimValueType: InboundTokenClaimValueTypeType
    authorizingClaimMatchValue: AuthorizingClaimMatchValueTypeUnionTypeDef

AgentRuntimeArtifactUnionTypeDef = Union[
    AgentRuntimeArtifactTypeDef, AgentRuntimeArtifactOutputTypeDef
]
StreamDeliveryResourcesUnionTypeDef = Union[
    StreamDeliveryResourcesTypeDef, StreamDeliveryResourcesOutputTypeDef
]

class CreateOnlineEvaluationConfigRequestTypeDef(TypedDict):
    onlineEvaluationConfigName: str
    rule: RuleUnionTypeDef
    dataSourceConfig: DataSourceConfigUnionTypeDef
    evaluators: Sequence[EvaluatorReferenceTypeDef]
    evaluationExecutionRoleArn: str
    enableOnCreate: bool
    clientToken: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class UpdateOnlineEvaluationConfigRequestTypeDef(TypedDict):
    onlineEvaluationConfigId: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    rule: NotRequired[RuleUnionTypeDef]
    dataSourceConfig: NotRequired[DataSourceConfigUnionTypeDef]
    evaluators: NotRequired[Sequence[EvaluatorReferenceTypeDef]]
    evaluationExecutionRoleArn: NotRequired[str]
    executionStatus: NotRequired[OnlineEvaluationExecutionStatusType]

class UpdatedDescriptorsUnionTypeDef(TypedDict):
    mcp: NotRequired[UpdatedMcpDescriptorTypeDef]
    a2a: NotRequired[UpdatedA2aDescriptorTypeDef]
    custom: NotRequired[UpdatedCustomDescriptorTypeDef]
    agentSkills: NotRequired[UpdatedAgentSkillsDescriptorTypeDef]

class CredentialProviderConfigurationTypeDef(TypedDict):
    credentialProviderType: CredentialProviderTypeType
    credentialProvider: NotRequired[CredentialProviderUnionTypeDef]

class CreateOauth2CredentialProviderResponseTypeDef(TypedDict):
    clientSecretArn: SecretTypeDef
    name: str
    credentialProviderArn: str
    callbackUrl: str
    oauth2ProviderConfigOutput: Oauth2ProviderConfigOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetOauth2CredentialProviderResponseTypeDef(TypedDict):
    clientSecretArn: SecretTypeDef
    name: str
    credentialProviderArn: str
    credentialProviderVendor: CredentialProviderVendorTypeType
    callbackUrl: str
    oauth2ProviderConfigOutput: Oauth2ProviderConfigOutputTypeDef
    createdTime: datetime
    lastUpdatedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateOauth2CredentialProviderResponseTypeDef(TypedDict):
    clientSecretArn: SecretTypeDef
    name: str
    credentialProviderVendor: CredentialProviderVendorTypeType
    credentialProviderArn: str
    callbackUrl: str
    oauth2ProviderConfigOutput: Oauth2ProviderConfigOutputTypeDef
    createdTime: datetime
    lastUpdatedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CustomOauth2ProviderConfigInputTypeDef(TypedDict):
    oauthDiscovery: Oauth2DiscoveryUnionTypeDef
    clientId: str
    clientSecret: str

class SynchronizationConfigurationOutputTypeDef(TypedDict):
    fromUrl: NotRequired[FromUrlSynchronizationConfigurationOutputTypeDef]

class RegistryRecordCredentialProviderConfigurationTypeDef(TypedDict):
    credentialProviderType: RegistryRecordCredentialProviderTypeType
    credentialProvider: RegistryRecordCredentialProviderUnionUnionTypeDef

McpTargetConfigurationOutputTypeDef = TypedDict(
    "McpTargetConfigurationOutputTypeDef",
    {
        "openApiSchema": NotRequired[ApiSchemaConfigurationTypeDef],
        "smithyModel": NotRequired[ApiSchemaConfigurationTypeDef],
        "lambda": NotRequired[McpLambdaTargetConfigurationOutputTypeDef],
        "mcpServer": NotRequired[McpServerTargetConfigurationTypeDef],
        "apiGateway": NotRequired[ApiGatewayTargetConfigurationOutputTypeDef],
    },
)
McpTargetConfigurationTypeDef = TypedDict(
    "McpTargetConfigurationTypeDef",
    {
        "openApiSchema": NotRequired[ApiSchemaConfigurationTypeDef],
        "smithyModel": NotRequired[ApiSchemaConfigurationTypeDef],
        "lambda": NotRequired[McpLambdaTargetConfigurationTypeDef],
        "mcpServer": NotRequired[McpServerTargetConfigurationTypeDef],
        "apiGateway": NotRequired[ApiGatewayTargetConfigurationTypeDef],
    },
)

class ModifyMemoryStrategyInputTypeDef(TypedDict):
    memoryStrategyId: str
    description: NotRequired[str]
    namespaces: NotRequired[Sequence[str]]
    namespaceTemplates: NotRequired[Sequence[str]]
    configuration: NotRequired[ModifyStrategyConfigurationTypeDef]

class CustomMemoryStrategyInputTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    namespaces: NotRequired[Sequence[str]]
    namespaceTemplates: NotRequired[Sequence[str]]
    configuration: NotRequired[CustomConfigurationInputTypeDef]

MemoryStrategyTypeDef = TypedDict(
    "MemoryStrategyTypeDef",
    {
        "strategyId": str,
        "name": str,
        "type": MemoryStrategyTypeType,
        "namespaces": list[str],
        "namespaceTemplates": list[str],
        "description": NotRequired[str],
        "configuration": NotRequired[StrategyConfigurationTypeDef],
        "createdAt": NotRequired[datetime],
        "updatedAt": NotRequired[datetime],
        "status": NotRequired[MemoryStrategyStatusType],
    },
)

class CreateGatewayResponseTypeDef(TypedDict):
    gatewayArn: str
    gatewayId: str
    gatewayUrl: str
    createdAt: datetime
    updatedAt: datetime
    status: GatewayStatusType
    statusReasons: list[str]
    name: str
    description: str
    roleArn: str
    protocolType: Literal["MCP"]
    protocolConfiguration: GatewayProtocolConfigurationOutputTypeDef
    authorizerType: AuthorizerTypeType
    authorizerConfiguration: AuthorizerConfigurationOutputTypeDef
    kmsKeyArn: str
    interceptorConfigurations: list[GatewayInterceptorConfigurationOutputTypeDef]
    policyEngineConfiguration: GatewayPolicyEngineConfigurationTypeDef
    workloadIdentityDetails: WorkloadIdentityDetailsTypeDef
    exceptionLevel: Literal["DEBUG"]
    ResponseMetadata: ResponseMetadataTypeDef

class GetAgentRuntimeResponseTypeDef(TypedDict):
    agentRuntimeArn: str
    agentRuntimeName: str
    agentRuntimeId: str
    agentRuntimeVersion: str
    createdAt: datetime
    lastUpdatedAt: datetime
    roleArn: str
    networkConfiguration: NetworkConfigurationOutputTypeDef
    status: AgentRuntimeStatusType
    lifecycleConfiguration: LifecycleConfigurationTypeDef
    failureReason: str
    description: str
    workloadIdentityDetails: WorkloadIdentityDetailsTypeDef
    agentRuntimeArtifact: AgentRuntimeArtifactOutputTypeDef
    protocolConfiguration: ProtocolConfigurationTypeDef
    environmentVariables: dict[str, str]
    authorizerConfiguration: AuthorizerConfigurationOutputTypeDef
    requestHeaderConfiguration: RequestHeaderConfigurationOutputTypeDef
    metadataConfiguration: RuntimeMetadataConfigurationTypeDef
    filesystemConfigurations: list[FilesystemConfigurationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class GetGatewayResponseTypeDef(TypedDict):
    gatewayArn: str
    gatewayId: str
    gatewayUrl: str
    createdAt: datetime
    updatedAt: datetime
    status: GatewayStatusType
    statusReasons: list[str]
    name: str
    description: str
    roleArn: str
    protocolType: Literal["MCP"]
    protocolConfiguration: GatewayProtocolConfigurationOutputTypeDef
    authorizerType: AuthorizerTypeType
    authorizerConfiguration: AuthorizerConfigurationOutputTypeDef
    kmsKeyArn: str
    interceptorConfigurations: list[GatewayInterceptorConfigurationOutputTypeDef]
    policyEngineConfiguration: GatewayPolicyEngineConfigurationTypeDef
    workloadIdentityDetails: WorkloadIdentityDetailsTypeDef
    exceptionLevel: Literal["DEBUG"]
    ResponseMetadata: ResponseMetadataTypeDef

class GetRegistryResponseTypeDef(TypedDict):
    name: str
    description: str
    registryId: str
    registryArn: str
    authorizerType: RegistryAuthorizerTypeType
    authorizerConfiguration: AuthorizerConfigurationOutputTypeDef
    approvalConfiguration: ApprovalConfigurationTypeDef
    status: RegistryStatusType
    statusReason: str
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateGatewayResponseTypeDef(TypedDict):
    gatewayArn: str
    gatewayId: str
    gatewayUrl: str
    createdAt: datetime
    updatedAt: datetime
    status: GatewayStatusType
    statusReasons: list[str]
    name: str
    description: str
    roleArn: str
    protocolType: Literal["MCP"]
    protocolConfiguration: GatewayProtocolConfigurationOutputTypeDef
    authorizerType: AuthorizerTypeType
    authorizerConfiguration: AuthorizerConfigurationOutputTypeDef
    kmsKeyArn: str
    interceptorConfigurations: list[GatewayInterceptorConfigurationOutputTypeDef]
    policyEngineConfiguration: GatewayPolicyEngineConfigurationTypeDef
    workloadIdentityDetails: WorkloadIdentityDetailsTypeDef
    exceptionLevel: Literal["DEBUG"]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRegistryResponseTypeDef(TypedDict):
    name: str
    description: str
    registryId: str
    registryArn: str
    authorizerType: RegistryAuthorizerTypeType
    authorizerConfiguration: AuthorizerConfigurationOutputTypeDef
    approvalConfiguration: ApprovalConfigurationTypeDef
    status: RegistryStatusType
    statusReason: str
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetEvaluatorResponseTypeDef(TypedDict):
    evaluatorArn: str
    evaluatorId: str
    evaluatorName: str
    description: str
    evaluatorConfig: EvaluatorConfigOutputTypeDef
    level: EvaluatorLevelType
    status: EvaluatorStatusType
    createdAt: datetime
    updatedAt: datetime
    lockedForModification: bool
    ResponseMetadata: ResponseMetadataTypeDef

EvaluatorConfigUnionTypeDef = Union[EvaluatorConfigTypeDef, EvaluatorConfigOutputTypeDef]
CustomClaimValidationTypeUnionTypeDef = Union[
    CustomClaimValidationTypeTypeDef, CustomClaimValidationTypeOutputTypeDef
]

class UpdatedDescriptorsTypeDef(TypedDict):
    optionalValue: NotRequired[UpdatedDescriptorsUnionTypeDef]

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
    atlassianOauth2ProviderConfig: NotRequired[AtlassianOauth2ProviderConfigInputTypeDef]
    linkedinOauth2ProviderConfig: NotRequired[LinkedinOauth2ProviderConfigInputTypeDef]
    includedOauth2ProviderConfig: NotRequired[IncludedOauth2ProviderConfigInputTypeDef]

class GetRegistryRecordResponseTypeDef(TypedDict):
    registryArn: str
    recordArn: str
    recordId: str
    name: str
    description: str
    descriptorType: DescriptorTypeType
    descriptors: DescriptorsTypeDef
    recordVersion: str
    status: RegistryRecordStatusType
    createdAt: datetime
    updatedAt: datetime
    statusReason: str
    synchronizationType: Literal["URL"]
    synchronizationConfiguration: SynchronizationConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateRegistryRecordResponseTypeDef(TypedDict):
    registryArn: str
    recordArn: str
    recordId: str
    name: str
    description: str
    descriptorType: DescriptorTypeType
    descriptors: DescriptorsTypeDef
    recordVersion: str
    status: RegistryRecordStatusType
    createdAt: datetime
    updatedAt: datetime
    statusReason: str
    synchronizationType: Literal["URL"]
    synchronizationConfiguration: SynchronizationConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

RegistryRecordCredentialProviderConfigurationUnionTypeDef = Union[
    RegistryRecordCredentialProviderConfigurationTypeDef,
    RegistryRecordCredentialProviderConfigurationOutputTypeDef,
]

class TargetConfigurationOutputTypeDef(TypedDict):
    mcp: NotRequired[McpTargetConfigurationOutputTypeDef]

class TargetConfigurationTypeDef(TypedDict):
    mcp: NotRequired[McpTargetConfigurationTypeDef]

class MemoryStrategyInputTypeDef(TypedDict):
    semanticMemoryStrategy: NotRequired[SemanticMemoryStrategyInputTypeDef]
    summaryMemoryStrategy: NotRequired[SummaryMemoryStrategyInputTypeDef]
    userPreferenceMemoryStrategy: NotRequired[UserPreferenceMemoryStrategyInputTypeDef]
    customMemoryStrategy: NotRequired[CustomMemoryStrategyInputTypeDef]
    episodicMemoryStrategy: NotRequired[EpisodicMemoryStrategyInputTypeDef]

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
        "strategies": NotRequired[list[MemoryStrategyTypeDef]],
        "streamDeliveryResources": NotRequired[StreamDeliveryResourcesOutputTypeDef],
    },
)

class CreateEvaluatorRequestTypeDef(TypedDict):
    evaluatorName: str
    evaluatorConfig: EvaluatorConfigUnionTypeDef
    level: EvaluatorLevelType
    clientToken: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class UpdateEvaluatorRequestTypeDef(TypedDict):
    evaluatorId: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    evaluatorConfig: NotRequired[EvaluatorConfigUnionTypeDef]
    level: NotRequired[EvaluatorLevelType]

class CustomJWTAuthorizerConfigurationTypeDef(TypedDict):
    discoveryUrl: str
    allowedAudience: NotRequired[Sequence[str]]
    allowedClients: NotRequired[Sequence[str]]
    allowedScopes: NotRequired[Sequence[str]]
    customClaims: NotRequired[Sequence[CustomClaimValidationTypeUnionTypeDef]]

class CreateOauth2CredentialProviderRequestTypeDef(TypedDict):
    name: str
    credentialProviderVendor: CredentialProviderVendorTypeType
    oauth2ProviderConfigInput: Oauth2ProviderConfigInputTypeDef
    tags: NotRequired[Mapping[str, str]]

class UpdateOauth2CredentialProviderRequestTypeDef(TypedDict):
    name: str
    credentialProviderVendor: CredentialProviderVendorTypeType
    oauth2ProviderConfigInput: Oauth2ProviderConfigInputTypeDef

class FromUrlSynchronizationConfigurationTypeDef(TypedDict):
    url: str
    credentialProviderConfigurations: NotRequired[
        Sequence[RegistryRecordCredentialProviderConfigurationUnionTypeDef]
    ]

class CreateGatewayTargetResponseTypeDef(TypedDict):
    gatewayArn: str
    targetId: str
    createdAt: datetime
    updatedAt: datetime
    status: TargetStatusType
    statusReasons: list[str]
    name: str
    description: str
    targetConfiguration: TargetConfigurationOutputTypeDef
    credentialProviderConfigurations: list[CredentialProviderConfigurationOutputTypeDef]
    lastSynchronizedAt: datetime
    metadataConfiguration: MetadataConfigurationOutputTypeDef
    privateEndpoint: PrivateEndpointOutputTypeDef
    privateEndpointManagedResources: list[ManagedResourceDetailsTypeDef]
    authorizationData: AuthorizationDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GatewayTargetTypeDef(TypedDict):
    gatewayArn: str
    targetId: str
    createdAt: datetime
    updatedAt: datetime
    status: TargetStatusType
    name: str
    targetConfiguration: TargetConfigurationOutputTypeDef
    credentialProviderConfigurations: list[CredentialProviderConfigurationOutputTypeDef]
    statusReasons: NotRequired[list[str]]
    description: NotRequired[str]
    lastSynchronizedAt: NotRequired[datetime]
    metadataConfiguration: NotRequired[MetadataConfigurationOutputTypeDef]
    privateEndpoint: NotRequired[PrivateEndpointOutputTypeDef]
    privateEndpointManagedResources: NotRequired[list[ManagedResourceDetailsTypeDef]]
    authorizationData: NotRequired[AuthorizationDataTypeDef]

class GetGatewayTargetResponseTypeDef(TypedDict):
    gatewayArn: str
    targetId: str
    createdAt: datetime
    updatedAt: datetime
    status: TargetStatusType
    statusReasons: list[str]
    name: str
    description: str
    targetConfiguration: TargetConfigurationOutputTypeDef
    credentialProviderConfigurations: list[CredentialProviderConfigurationOutputTypeDef]
    lastSynchronizedAt: datetime
    metadataConfiguration: MetadataConfigurationOutputTypeDef
    privateEndpoint: PrivateEndpointOutputTypeDef
    privateEndpointManagedResources: list[ManagedResourceDetailsTypeDef]
    authorizationData: AuthorizationDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateGatewayTargetResponseTypeDef(TypedDict):
    gatewayArn: str
    targetId: str
    createdAt: datetime
    updatedAt: datetime
    status: TargetStatusType
    statusReasons: list[str]
    name: str
    description: str
    targetConfiguration: TargetConfigurationOutputTypeDef
    credentialProviderConfigurations: list[CredentialProviderConfigurationOutputTypeDef]
    lastSynchronizedAt: datetime
    metadataConfiguration: MetadataConfigurationOutputTypeDef
    privateEndpoint: PrivateEndpointOutputTypeDef
    privateEndpointManagedResources: list[ManagedResourceDetailsTypeDef]
    authorizationData: AuthorizationDataTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

TargetConfigurationUnionTypeDef = Union[
    TargetConfigurationTypeDef, TargetConfigurationOutputTypeDef
]

class CreateMemoryInputTypeDef(TypedDict):
    name: str
    eventExpiryDuration: int
    clientToken: NotRequired[str]
    description: NotRequired[str]
    encryptionKeyArn: NotRequired[str]
    memoryExecutionRoleArn: NotRequired[str]
    memoryStrategies: NotRequired[Sequence[MemoryStrategyInputTypeDef]]
    streamDeliveryResources: NotRequired[StreamDeliveryResourcesUnionTypeDef]
    tags: NotRequired[Mapping[str, str]]

class ModifyMemoryStrategiesTypeDef(TypedDict):
    addMemoryStrategies: NotRequired[Sequence[MemoryStrategyInputTypeDef]]
    modifyMemoryStrategies: NotRequired[Sequence[ModifyMemoryStrategyInputTypeDef]]
    deleteMemoryStrategies: NotRequired[Sequence[DeleteMemoryStrategyInputTypeDef]]

class CreateMemoryOutputTypeDef(TypedDict):
    memory: MemoryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetMemoryOutputTypeDef(TypedDict):
    memory: MemoryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateMemoryOutputTypeDef(TypedDict):
    memory: MemoryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

CustomJWTAuthorizerConfigurationUnionTypeDef = Union[
    CustomJWTAuthorizerConfigurationTypeDef, CustomJWTAuthorizerConfigurationOutputTypeDef
]
FromUrlSynchronizationConfigurationUnionTypeDef = Union[
    FromUrlSynchronizationConfigurationTypeDef, FromUrlSynchronizationConfigurationOutputTypeDef
]

class SynchronizeGatewayTargetsResponseTypeDef(TypedDict):
    targets: list[GatewayTargetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class CreateGatewayTargetRequestTypeDef(TypedDict):
    gatewayIdentifier: str
    name: str
    targetConfiguration: TargetConfigurationUnionTypeDef
    description: NotRequired[str]
    clientToken: NotRequired[str]
    credentialProviderConfigurations: NotRequired[
        Sequence[CredentialProviderConfigurationUnionTypeDef]
    ]
    metadataConfiguration: NotRequired[MetadataConfigurationUnionTypeDef]
    privateEndpoint: NotRequired[PrivateEndpointUnionTypeDef]

class UpdateGatewayTargetRequestTypeDef(TypedDict):
    gatewayIdentifier: str
    targetId: str
    name: str
    targetConfiguration: TargetConfigurationUnionTypeDef
    description: NotRequired[str]
    credentialProviderConfigurations: NotRequired[
        Sequence[CredentialProviderConfigurationUnionTypeDef]
    ]
    metadataConfiguration: NotRequired[MetadataConfigurationUnionTypeDef]
    privateEndpoint: NotRequired[PrivateEndpointUnionTypeDef]

class UpdateMemoryInputTypeDef(TypedDict):
    memoryId: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    eventExpiryDuration: NotRequired[int]
    memoryExecutionRoleArn: NotRequired[str]
    memoryStrategies: NotRequired[ModifyMemoryStrategiesTypeDef]
    streamDeliveryResources: NotRequired[StreamDeliveryResourcesUnionTypeDef]

class AuthorizerConfigurationTypeDef(TypedDict):
    customJWTAuthorizer: NotRequired[CustomJWTAuthorizerConfigurationUnionTypeDef]

class SynchronizationConfigurationTypeDef(TypedDict):
    fromUrl: NotRequired[FromUrlSynchronizationConfigurationUnionTypeDef]

AuthorizerConfigurationUnionTypeDef = Union[
    AuthorizerConfigurationTypeDef, AuthorizerConfigurationOutputTypeDef
]
SynchronizationConfigurationUnionTypeDef = Union[
    SynchronizationConfigurationTypeDef, SynchronizationConfigurationOutputTypeDef
]

class CreateAgentRuntimeRequestTypeDef(TypedDict):
    agentRuntimeName: str
    agentRuntimeArtifact: AgentRuntimeArtifactUnionTypeDef
    roleArn: str
    networkConfiguration: NetworkConfigurationUnionTypeDef
    clientToken: NotRequired[str]
    description: NotRequired[str]
    authorizerConfiguration: NotRequired[AuthorizerConfigurationUnionTypeDef]
    requestHeaderConfiguration: NotRequired[RequestHeaderConfigurationUnionTypeDef]
    protocolConfiguration: NotRequired[ProtocolConfigurationTypeDef]
    lifecycleConfiguration: NotRequired[LifecycleConfigurationTypeDef]
    environmentVariables: NotRequired[Mapping[str, str]]
    filesystemConfigurations: NotRequired[Sequence[FilesystemConfigurationTypeDef]]
    tags: NotRequired[Mapping[str, str]]

class CreateGatewayRequestTypeDef(TypedDict):
    name: str
    roleArn: str
    protocolType: Literal["MCP"]
    authorizerType: AuthorizerTypeType
    description: NotRequired[str]
    clientToken: NotRequired[str]
    protocolConfiguration: NotRequired[GatewayProtocolConfigurationUnionTypeDef]
    authorizerConfiguration: NotRequired[AuthorizerConfigurationUnionTypeDef]
    kmsKeyArn: NotRequired[str]
    interceptorConfigurations: NotRequired[Sequence[GatewayInterceptorConfigurationUnionTypeDef]]
    policyEngineConfiguration: NotRequired[GatewayPolicyEngineConfigurationTypeDef]
    exceptionLevel: NotRequired[Literal["DEBUG"]]
    tags: NotRequired[Mapping[str, str]]

class CreateRegistryRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    authorizerType: NotRequired[RegistryAuthorizerTypeType]
    authorizerConfiguration: NotRequired[AuthorizerConfigurationUnionTypeDef]
    clientToken: NotRequired[str]
    approvalConfiguration: NotRequired[ApprovalConfigurationTypeDef]

class UpdateAgentRuntimeRequestTypeDef(TypedDict):
    agentRuntimeId: str
    agentRuntimeArtifact: AgentRuntimeArtifactUnionTypeDef
    roleArn: str
    networkConfiguration: NetworkConfigurationUnionTypeDef
    description: NotRequired[str]
    authorizerConfiguration: NotRequired[AuthorizerConfigurationUnionTypeDef]
    requestHeaderConfiguration: NotRequired[RequestHeaderConfigurationUnionTypeDef]
    protocolConfiguration: NotRequired[ProtocolConfigurationTypeDef]
    lifecycleConfiguration: NotRequired[LifecycleConfigurationTypeDef]
    metadataConfiguration: NotRequired[RuntimeMetadataConfigurationTypeDef]
    environmentVariables: NotRequired[Mapping[str, str]]
    filesystemConfigurations: NotRequired[Sequence[FilesystemConfigurationTypeDef]]
    clientToken: NotRequired[str]

class UpdateGatewayRequestTypeDef(TypedDict):
    gatewayIdentifier: str
    name: str
    roleArn: str
    protocolType: Literal["MCP"]
    authorizerType: AuthorizerTypeType
    description: NotRequired[str]
    protocolConfiguration: NotRequired[GatewayProtocolConfigurationUnionTypeDef]
    authorizerConfiguration: NotRequired[AuthorizerConfigurationUnionTypeDef]
    kmsKeyArn: NotRequired[str]
    interceptorConfigurations: NotRequired[Sequence[GatewayInterceptorConfigurationUnionTypeDef]]
    policyEngineConfiguration: NotRequired[GatewayPolicyEngineConfigurationTypeDef]
    exceptionLevel: NotRequired[Literal["DEBUG"]]

class UpdatedAuthorizerConfigurationTypeDef(TypedDict):
    optionalValue: NotRequired[AuthorizerConfigurationUnionTypeDef]

class CreateRegistryRecordRequestTypeDef(TypedDict):
    registryId: str
    name: str
    descriptorType: DescriptorTypeType
    description: NotRequired[str]
    descriptors: NotRequired[DescriptorsTypeDef]
    recordVersion: NotRequired[str]
    synchronizationType: NotRequired[Literal["URL"]]
    synchronizationConfiguration: NotRequired[SynchronizationConfigurationUnionTypeDef]
    clientToken: NotRequired[str]

class UpdatedSynchronizationConfigurationTypeDef(TypedDict):
    optionalValue: NotRequired[SynchronizationConfigurationUnionTypeDef]

class UpdateRegistryRequestTypeDef(TypedDict):
    registryId: str
    name: NotRequired[str]
    description: NotRequired[UpdatedDescriptionTypeDef]
    authorizerConfiguration: NotRequired[UpdatedAuthorizerConfigurationTypeDef]
    approvalConfiguration: NotRequired[UpdatedApprovalConfigurationTypeDef]

class UpdateRegistryRecordRequestTypeDef(TypedDict):
    registryId: str
    recordId: str
    name: NotRequired[str]
    description: NotRequired[UpdatedDescriptionTypeDef]
    descriptorType: NotRequired[DescriptorTypeType]
    descriptors: NotRequired[UpdatedDescriptorsTypeDef]
    recordVersion: NotRequired[str]
    synchronizationType: NotRequired[UpdatedSynchronizationTypeTypeDef]
    synchronizationConfiguration: NotRequired[UpdatedSynchronizationConfigurationTypeDef]
    triggerSynchronization: NotRequired[bool]
