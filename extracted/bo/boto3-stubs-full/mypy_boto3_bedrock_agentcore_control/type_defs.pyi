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
    ActorTokenContentTypeType,
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
    ClientAuthenticationMethodTypeType,
    CodeInterpreterNetworkModeType,
    CodeInterpreterStatusType,
    ConfigurationBundleStatusType,
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
    GatewayRuleStatusType,
    GatewayStatusType,
    HarnessStatusType,
    HarnessToolTypeType,
    HarnessTruncationStrategyType,
    InboundTokenClaimValueTypeType,
    IncludedDataType,
    KeyTypeType,
    ListingModeType,
    MemoryStatusType,
    MemoryStrategyStatusType,
    MemoryStrategyTypeType,
    MemoryViewType,
    MetadataValueTypeType,
    NetworkModeType,
    OAuthGrantTypeType,
    OnBehalfOfTokenExchangeGrantTypeTypeType,
    OnlineEvaluationConfigStatusType,
    OnlineEvaluationExecutionStatusType,
    OverrideTypeType,
    PaymentConnectorStatusType,
    PaymentConnectorTypeType,
    PaymentCredentialProviderVendorTypeType,
    PaymentManagerStatusType,
    PaymentsAuthorizerTypeType,
    PolicyEngineStatusType,
    PolicyGenerationStatusType,
    PolicyStatusType,
    PolicyValidationModeType,
    PrincipalMatchOperatorType,
    RegistryAuthorizerTypeType,
    RegistryRecordCredentialProviderTypeType,
    RegistryRecordStatusType,
    RegistryStatusType,
    ResourceTypeType,
    RestApiMethodType,
    SchemaTypeType,
    ServerProtocolType,
    StatusType,
    TargetProtocolTypeType,
    TargetStatusType,
)

if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict

__all__ = (
    "A2aDescriptorTypeDef",
    "ActionOutputTypeDef",
    "ActionTypeDef",
    "ActionUnionTypeDef",
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
    "CoinbaseCdpConfigurationInputTypeDef",
    "CoinbaseCdpConfigurationOutputTypeDef",
    "ComponentConfigurationOutputTypeDef",
    "ComponentConfigurationTypeDef",
    "ComponentConfigurationUnionTypeDef",
    "ConditionOutputTypeDef",
    "ConditionTypeDef",
    "ConditionUnionTypeDef",
    "ConfigurationBundleActionOutputTypeDef",
    "ConfigurationBundleActionTypeDef",
    "ConfigurationBundleActionUnionTypeDef",
    "ConfigurationBundleReferenceTypeDef",
    "ConfigurationBundleSummaryTypeDef",
    "ConfigurationBundleVersionSummaryTypeDef",
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
    "CreateConfigurationBundleRequestTypeDef",
    "CreateConfigurationBundleResponseTypeDef",
    "CreateEvaluatorRequestTypeDef",
    "CreateEvaluatorResponseTypeDef",
    "CreateGatewayRequestTypeDef",
    "CreateGatewayResponseTypeDef",
    "CreateGatewayRuleRequestTypeDef",
    "CreateGatewayRuleResponseTypeDef",
    "CreateGatewayTargetRequestTypeDef",
    "CreateGatewayTargetResponseTypeDef",
    "CreateHarnessRequestTypeDef",
    "CreateHarnessResponseTypeDef",
    "CreateMemoryInputTypeDef",
    "CreateMemoryOutputTypeDef",
    "CreateOauth2CredentialProviderRequestTypeDef",
    "CreateOauth2CredentialProviderResponseTypeDef",
    "CreateOnlineEvaluationConfigRequestTypeDef",
    "CreateOnlineEvaluationConfigResponseTypeDef",
    "CreatePaymentConnectorRequestTypeDef",
    "CreatePaymentConnectorResponseTypeDef",
    "CreatePaymentCredentialProviderRequestTypeDef",
    "CreatePaymentCredentialProviderResponseTypeDef",
    "CreatePaymentManagerRequestTypeDef",
    "CreatePaymentManagerResponseTypeDef",
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
    "CredentialsProviderConfigurationTypeDef",
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
    "DeleteConfigurationBundleRequestTypeDef",
    "DeleteConfigurationBundleResponseTypeDef",
    "DeleteEvaluatorRequestTypeDef",
    "DeleteEvaluatorResponseTypeDef",
    "DeleteGatewayRequestTypeDef",
    "DeleteGatewayResponseTypeDef",
    "DeleteGatewayRuleRequestTypeDef",
    "DeleteGatewayRuleResponseTypeDef",
    "DeleteGatewayTargetRequestTypeDef",
    "DeleteGatewayTargetResponseTypeDef",
    "DeleteHarnessRequestTypeDef",
    "DeleteHarnessResponseTypeDef",
    "DeleteMemoryInputTypeDef",
    "DeleteMemoryOutputTypeDef",
    "DeleteMemoryStrategyInputTypeDef",
    "DeleteOauth2CredentialProviderRequestTypeDef",
    "DeleteOnlineEvaluationConfigRequestTypeDef",
    "DeleteOnlineEvaluationConfigResponseTypeDef",
    "DeletePaymentConnectorRequestTypeDef",
    "DeletePaymentConnectorResponseTypeDef",
    "DeletePaymentCredentialProviderRequestTypeDef",
    "DeletePaymentManagerRequestTypeDef",
    "DeletePaymentManagerResponseTypeDef",
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
    "EfsAccessPointConfigurationTypeDef",
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
    "ExtractionConfigOutputTypeDef",
    "ExtractionConfigTypeDef",
    "ExtractionConfigUnionTypeDef",
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
    "GatewayRuleDetailTypeDef",
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
    "GetConfigurationBundleRequestTypeDef",
    "GetConfigurationBundleResponseTypeDef",
    "GetConfigurationBundleVersionRequestTypeDef",
    "GetConfigurationBundleVersionResponseTypeDef",
    "GetEvaluatorRequestTypeDef",
    "GetEvaluatorResponseTypeDef",
    "GetGatewayRequestTypeDef",
    "GetGatewayResponseTypeDef",
    "GetGatewayRuleRequestTypeDef",
    "GetGatewayRuleResponseTypeDef",
    "GetGatewayTargetRequestTypeDef",
    "GetGatewayTargetResponseTypeDef",
    "GetHarnessRequestTypeDef",
    "GetHarnessResponseTypeDef",
    "GetMemoryInputTypeDef",
    "GetMemoryInputWaitTypeDef",
    "GetMemoryOutputTypeDef",
    "GetOauth2CredentialProviderRequestTypeDef",
    "GetOauth2CredentialProviderResponseTypeDef",
    "GetOnlineEvaluationConfigRequestTypeDef",
    "GetOnlineEvaluationConfigResponseTypeDef",
    "GetPaymentConnectorRequestTypeDef",
    "GetPaymentConnectorResponseTypeDef",
    "GetPaymentCredentialProviderRequestTypeDef",
    "GetPaymentCredentialProviderResponseTypeDef",
    "GetPaymentManagerRequestTypeDef",
    "GetPaymentManagerResponseTypeDef",
    "GetPolicyEngineRequestTypeDef",
    "GetPolicyEngineRequestWaitExtraTypeDef",
    "GetPolicyEngineRequestWaitTypeDef",
    "GetPolicyEngineResponseTypeDef",
    "GetPolicyEngineSummaryRequestTypeDef",
    "GetPolicyEngineSummaryResponseTypeDef",
    "GetPolicyGenerationRequestTypeDef",
    "GetPolicyGenerationRequestWaitTypeDef",
    "GetPolicyGenerationResponseTypeDef",
    "GetPolicyGenerationSummaryRequestTypeDef",
    "GetPolicyGenerationSummaryResponseTypeDef",
    "GetPolicyRequestTypeDef",
    "GetPolicyRequestWaitExtraTypeDef",
    "GetPolicyRequestWaitTypeDef",
    "GetPolicyResponseTypeDef",
    "GetPolicySummaryRequestTypeDef",
    "GetPolicySummaryResponseTypeDef",
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
    "HarnessAgentCoreBrowserConfigTypeDef",
    "HarnessAgentCoreCodeInterpreterConfigTypeDef",
    "HarnessAgentCoreGatewayConfigOutputTypeDef",
    "HarnessAgentCoreGatewayConfigTypeDef",
    "HarnessAgentCoreGatewayConfigUnionTypeDef",
    "HarnessAgentCoreMemoryConfigurationOutputTypeDef",
    "HarnessAgentCoreMemoryConfigurationTypeDef",
    "HarnessAgentCoreMemoryConfigurationUnionTypeDef",
    "HarnessAgentCoreMemoryRetrievalConfigTypeDef",
    "HarnessAgentCoreRuntimeEnvironmentRequestTypeDef",
    "HarnessAgentCoreRuntimeEnvironmentTypeDef",
    "HarnessBedrockModelConfigTypeDef",
    "HarnessEnvironmentArtifactTypeDef",
    "HarnessEnvironmentProviderRequestTypeDef",
    "HarnessEnvironmentProviderTypeDef",
    "HarnessGatewayOutboundAuthOutputTypeDef",
    "HarnessGatewayOutboundAuthTypeDef",
    "HarnessGatewayOutboundAuthUnionTypeDef",
    "HarnessGeminiModelConfigTypeDef",
    "HarnessInlineFunctionConfigOutputTypeDef",
    "HarnessInlineFunctionConfigTypeDef",
    "HarnessInlineFunctionConfigUnionTypeDef",
    "HarnessMemoryConfigurationOutputTypeDef",
    "HarnessMemoryConfigurationTypeDef",
    "HarnessMemoryConfigurationUnionTypeDef",
    "HarnessModelConfigurationTypeDef",
    "HarnessOpenAiModelConfigTypeDef",
    "HarnessRemoteMcpConfigOutputTypeDef",
    "HarnessRemoteMcpConfigTypeDef",
    "HarnessRemoteMcpConfigUnionTypeDef",
    "HarnessSkillTypeDef",
    "HarnessSlidingWindowConfigurationTypeDef",
    "HarnessSummarizationConfigurationTypeDef",
    "HarnessSummaryTypeDef",
    "HarnessSystemContentBlockTypeDef",
    "HarnessToolConfigurationOutputTypeDef",
    "HarnessToolConfigurationTypeDef",
    "HarnessToolConfigurationUnionTypeDef",
    "HarnessToolOutputTypeDef",
    "HarnessToolTypeDef",
    "HarnessToolUnionTypeDef",
    "HarnessTruncationConfigurationTypeDef",
    "HarnessTruncationStrategyConfigurationTypeDef",
    "HarnessTypeDef",
    "HttpTargetConfigurationTypeDef",
    "IamCredentialProviderTypeDef",
    "IamPrincipalTypeDef",
    "IncludedOauth2ProviderConfigInputTypeDef",
    "IncludedOauth2ProviderConfigOutputTypeDef",
    "IndexedKeyTypeDef",
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
    "ListConfigurationBundleVersionsRequestPaginateTypeDef",
    "ListConfigurationBundleVersionsRequestTypeDef",
    "ListConfigurationBundleVersionsResponseTypeDef",
    "ListConfigurationBundlesRequestPaginateTypeDef",
    "ListConfigurationBundlesRequestTypeDef",
    "ListConfigurationBundlesResponseTypeDef",
    "ListEvaluatorsRequestPaginateTypeDef",
    "ListEvaluatorsRequestTypeDef",
    "ListEvaluatorsResponseTypeDef",
    "ListGatewayRulesRequestPaginateTypeDef",
    "ListGatewayRulesRequestTypeDef",
    "ListGatewayRulesResponseTypeDef",
    "ListGatewayTargetsRequestPaginateTypeDef",
    "ListGatewayTargetsRequestTypeDef",
    "ListGatewayTargetsResponseTypeDef",
    "ListGatewaysRequestPaginateTypeDef",
    "ListGatewaysRequestTypeDef",
    "ListGatewaysResponseTypeDef",
    "ListHarnessesRequestPaginateTypeDef",
    "ListHarnessesRequestTypeDef",
    "ListHarnessesResponseTypeDef",
    "ListMemoriesInputPaginateTypeDef",
    "ListMemoriesInputTypeDef",
    "ListMemoriesOutputTypeDef",
    "ListOauth2CredentialProvidersRequestPaginateTypeDef",
    "ListOauth2CredentialProvidersRequestTypeDef",
    "ListOauth2CredentialProvidersResponseTypeDef",
    "ListOnlineEvaluationConfigsRequestPaginateTypeDef",
    "ListOnlineEvaluationConfigsRequestTypeDef",
    "ListOnlineEvaluationConfigsResponseTypeDef",
    "ListPaymentConnectorsRequestPaginateTypeDef",
    "ListPaymentConnectorsRequestTypeDef",
    "ListPaymentConnectorsResponseTypeDef",
    "ListPaymentCredentialProvidersRequestPaginateTypeDef",
    "ListPaymentCredentialProvidersRequestTypeDef",
    "ListPaymentCredentialProvidersResponseTypeDef",
    "ListPaymentManagersRequestPaginateTypeDef",
    "ListPaymentManagersRequestTypeDef",
    "ListPaymentManagersResponseTypeDef",
    "ListPoliciesRequestPaginateTypeDef",
    "ListPoliciesRequestTypeDef",
    "ListPoliciesResponseTypeDef",
    "ListPolicyEngineSummariesRequestPaginateTypeDef",
    "ListPolicyEngineSummariesRequestTypeDef",
    "ListPolicyEngineSummariesResponseTypeDef",
    "ListPolicyEnginesRequestPaginateTypeDef",
    "ListPolicyEnginesRequestTypeDef",
    "ListPolicyEnginesResponseTypeDef",
    "ListPolicyGenerationAssetsRequestPaginateTypeDef",
    "ListPolicyGenerationAssetsRequestTypeDef",
    "ListPolicyGenerationAssetsResponseTypeDef",
    "ListPolicyGenerationSummariesRequestPaginateTypeDef",
    "ListPolicyGenerationSummariesRequestTypeDef",
    "ListPolicyGenerationSummariesResponseTypeDef",
    "ListPolicyGenerationsRequestPaginateTypeDef",
    "ListPolicyGenerationsRequestTypeDef",
    "ListPolicyGenerationsResponseTypeDef",
    "ListPolicySummariesRequestPaginateTypeDef",
    "ListPolicySummariesRequestTypeDef",
    "ListPolicySummariesResponseTypeDef",
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
    "LlmExtractionConfigOutputTypeDef",
    "LlmExtractionConfigTypeDef",
    "LlmExtractionConfigUnionTypeDef",
    "MCPGatewayConfigurationOutputTypeDef",
    "MCPGatewayConfigurationTypeDef",
    "ManagedResourceDetailsTypeDef",
    "ManagedVpcResourceOutputTypeDef",
    "ManagedVpcResourceTypeDef",
    "ManagedVpcResourceUnionTypeDef",
    "MatchPathsOutputTypeDef",
    "MatchPathsTypeDef",
    "MatchPathsUnionTypeDef",
    "MatchPrincipalEntryTypeDef",
    "MatchPrincipalsOutputTypeDef",
    "MatchPrincipalsTypeDef",
    "MatchPrincipalsUnionTypeDef",
    "McpDescriptorTypeDef",
    "McpLambdaTargetConfigurationOutputTypeDef",
    "McpLambdaTargetConfigurationTypeDef",
    "McpServerTargetConfigurationTypeDef",
    "McpTargetConfigurationOutputTypeDef",
    "McpTargetConfigurationTypeDef",
    "McpToolSchemaConfigurationTypeDef",
    "MemoryRecordSchemaOutputTypeDef",
    "MemoryRecordSchemaTypeDef",
    "MemoryRecordSchemaUnionTypeDef",
    "MemoryStrategyInputTypeDef",
    "MemoryStrategyTypeDef",
    "MemorySummaryTypeDef",
    "MemoryTypeDef",
    "MessageBasedTriggerInputTypeDef",
    "MessageBasedTriggerTypeDef",
    "MetadataConfigurationOutputTypeDef",
    "MetadataConfigurationTypeDef",
    "MetadataConfigurationUnionTypeDef",
    "MetadataSchemaEntryOutputTypeDef",
    "MetadataSchemaEntryTypeDef",
    "MetadataSchemaEntryUnionTypeDef",
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
    "NumberValidationTypeDef",
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
    "OnBehalfOfTokenExchangeConfigTypeOutputTypeDef",
    "OnBehalfOfTokenExchangeConfigTypeTypeDef",
    "OnBehalfOfTokenExchangeConfigTypeUnionTypeDef",
    "OnlineEvaluationConfigSummaryTypeDef",
    "OutputConfigTypeDef",
    "PaginatorConfigTypeDef",
    "PaymentConnectorSummaryTypeDef",
    "PaymentCredentialProviderConfigurationTypeDef",
    "PaymentCredentialProviderItemTypeDef",
    "PaymentManagerSummaryTypeDef",
    "PaymentProviderConfigurationInputTypeDef",
    "PaymentProviderConfigurationOutputTypeDef",
    "PolicyDefinitionTypeDef",
    "PolicyEngineSummaryTypeDef",
    "PolicyEngineTypeDef",
    "PolicyGenerationAssetTypeDef",
    "PolicyGenerationDetailsTypeDef",
    "PolicyGenerationSummaryTypeDef",
    "PolicyGenerationTypeDef",
    "PolicySummaryTypeDef",
    "PolicyTypeDef",
    "PrivateEndpointOutputTypeDef",
    "PrivateEndpointOverrideOutputTypeDef",
    "PrivateEndpointOverrideTypeDef",
    "PrivateEndpointOverrideUnionTypeDef",
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
    "RouteToTargetActionOutputTypeDef",
    "RouteToTargetActionTypeDef",
    "RouteToTargetActionUnionTypeDef",
    "RuleOutputTypeDef",
    "RuleTypeDef",
    "RuleUnionTypeDef",
    "RuntimeMetadataConfigurationTypeDef",
    "RuntimeTargetConfigurationTypeDef",
    "S3ConfigurationTypeDef",
    "S3FilesAccessPointConfigurationTypeDef",
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
    "SessionConfigurationTypeDef",
    "SessionStorageConfigurationTypeDef",
    "SetTokenVaultCMKRequestTypeDef",
    "SetTokenVaultCMKResponseTypeDef",
    "SkillDefinitionTypeDef",
    "SkillMdDefinitionTypeDef",
    "SlackOauth2ProviderConfigInputTypeDef",
    "SlackOauth2ProviderConfigOutputTypeDef",
    "StartPolicyGenerationRequestTypeDef",
    "StartPolicyGenerationResponseTypeDef",
    "StaticOverrideTypeDef",
    "StaticRouteTypeDef",
    "StrategyConfigurationTypeDef",
    "StreamDeliveryResourceOutputTypeDef",
    "StreamDeliveryResourceTypeDef",
    "StreamDeliveryResourcesOutputTypeDef",
    "StreamDeliveryResourcesTypeDef",
    "StreamDeliveryResourcesUnionTypeDef",
    "StreamingConfigurationTypeDef",
    "StringListValidationOutputTypeDef",
    "StringListValidationTypeDef",
    "StringListValidationUnionTypeDef",
    "StringValidationOutputTypeDef",
    "StringValidationTypeDef",
    "StringValidationUnionTypeDef",
    "StripePrivyConfigurationInputTypeDef",
    "StripePrivyConfigurationOutputTypeDef",
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
    "SystemManagedBlockTypeDef",
    "TagResourceRequestTypeDef",
    "TargetConfigurationOutputTypeDef",
    "TargetConfigurationTypeDef",
    "TargetConfigurationUnionTypeDef",
    "TargetSummaryTypeDef",
    "TargetTrafficSplitEntryOutputTypeDef",
    "TargetTrafficSplitEntryTypeDef",
    "TargetTrafficSplitEntryUnionTypeDef",
    "TimeBasedTriggerInputTypeDef",
    "TimeBasedTriggerTypeDef",
    "TokenBasedTriggerInputTypeDef",
    "TokenBasedTriggerTypeDef",
    "TokenExchangeGrantTypeConfigTypeOutputTypeDef",
    "TokenExchangeGrantTypeConfigTypeTypeDef",
    "TokenExchangeGrantTypeConfigTypeUnionTypeDef",
    "ToolDefinitionOutputTypeDef",
    "ToolDefinitionTypeDef",
    "ToolSchemaOutputTypeDef",
    "ToolSchemaTypeDef",
    "ToolsDefinitionTypeDef",
    "TrafficSplitEntryOutputTypeDef",
    "TrafficSplitEntryTypeDef",
    "TrafficSplitEntryUnionTypeDef",
    "TriggerConditionInputTypeDef",
    "TriggerConditionTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateAgentRuntimeEndpointRequestTypeDef",
    "UpdateAgentRuntimeEndpointResponseTypeDef",
    "UpdateAgentRuntimeRequestTypeDef",
    "UpdateAgentRuntimeResponseTypeDef",
    "UpdateApiKeyCredentialProviderRequestTypeDef",
    "UpdateApiKeyCredentialProviderResponseTypeDef",
    "UpdateConfigurationBundleRequestTypeDef",
    "UpdateConfigurationBundleResponseTypeDef",
    "UpdateEvaluatorRequestTypeDef",
    "UpdateEvaluatorResponseTypeDef",
    "UpdateGatewayRequestTypeDef",
    "UpdateGatewayResponseTypeDef",
    "UpdateGatewayRuleRequestTypeDef",
    "UpdateGatewayRuleResponseTypeDef",
    "UpdateGatewayTargetRequestTypeDef",
    "UpdateGatewayTargetResponseTypeDef",
    "UpdateHarnessRequestTypeDef",
    "UpdateHarnessResponseTypeDef",
    "UpdateMemoryInputTypeDef",
    "UpdateMemoryOutputTypeDef",
    "UpdateOauth2CredentialProviderRequestTypeDef",
    "UpdateOauth2CredentialProviderResponseTypeDef",
    "UpdateOnlineEvaluationConfigRequestTypeDef",
    "UpdateOnlineEvaluationConfigResponseTypeDef",
    "UpdatePaymentConnectorRequestTypeDef",
    "UpdatePaymentConnectorResponseTypeDef",
    "UpdatePaymentCredentialProviderRequestTypeDef",
    "UpdatePaymentCredentialProviderResponseTypeDef",
    "UpdatePaymentManagerRequestTypeDef",
    "UpdatePaymentManagerResponseTypeDef",
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
    "UpdatedHarnessEnvironmentArtifactTypeDef",
    "UpdatedHarnessMemoryConfigurationTypeDef",
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
    "ValidationOutputTypeDef",
    "ValidationTypeDef",
    "ValidationUnionTypeDef",
    "VersionCreatedBySourceTypeDef",
    "VersionFilterTypeDef",
    "VersionLineageMetadataTypeDef",
    "VpcConfigOutputTypeDef",
    "VpcConfigTypeDef",
    "VpcConfigUnionTypeDef",
    "WaiterConfigTypeDef",
    "WeightedOverrideOutputTypeDef",
    "WeightedOverrideTypeDef",
    "WeightedOverrideUnionTypeDef",
    "WeightedRouteOutputTypeDef",
    "WeightedRouteTypeDef",
    "WeightedRouteUnionTypeDef",
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
    requireServiceS3Endpoint: NotRequired[bool]

class VpcConfigTypeDef(TypedDict):
    securityGroups: Sequence[str]
    subnets: Sequence[str]
    requireServiceS3Endpoint: NotRequired[bool]

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

class CoinbaseCdpConfigurationInputTypeDef(TypedDict):
    apiKeyId: str
    apiKeySecret: str
    walletSecret: str

class SecretTypeDef(TypedDict):
    secretArn: str

class ComponentConfigurationOutputTypeDef(TypedDict):
    configuration: dict[str, Any]

class ComponentConfigurationTypeDef(TypedDict):
    configuration: Mapping[str, Any]

class MatchPathsOutputTypeDef(TypedDict):
    anyOf: list[str]

class StaticOverrideTypeDef(TypedDict):
    bundleArn: str
    bundleVersion: str

class ConfigurationBundleReferenceTypeDef(TypedDict):
    bundleArn: str
    bundleVersion: str

class ConfigurationBundleSummaryTypeDef(TypedDict):
    bundleArn: str
    bundleId: str
    bundleName: str
    description: NotRequired[str]

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

class CreateBrowserProfileRequestTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    clientToken: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class VersionCreatedBySourceTypeDef(TypedDict):
    name: str
    arn: NotRequired[str]

class GatewayPolicyEngineConfigurationTypeDef(TypedDict):
    arn: str
    mode: GatewayPolicyEngineModeType

class SystemManagedBlockTypeDef(TypedDict):
    managedBy: str

class ManagedResourceDetailsTypeDef(TypedDict):
    domain: NotRequired[str]
    resourceGatewayArn: NotRequired[str]
    resourceAssociationArn: NotRequired[str]

class MetadataConfigurationOutputTypeDef(TypedDict):
    allowedRequestHeaders: NotRequired[list[str]]
    allowedQueryParameters: NotRequired[list[str]]
    allowedResponseHeaders: NotRequired[list[str]]

class HarnessSkillTypeDef(TypedDict):
    path: NotRequired[str]

class HarnessSystemContentBlockTypeDef(TypedDict):
    text: NotRequired[str]

IndexedKeyTypeDef = TypedDict(
    "IndexedKeyTypeDef",
    {
        "key": str,
        "type": MetadataValueTypeType,
    },
)

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

class PaymentCredentialProviderConfigurationTypeDef(TypedDict):
    credentialProviderArn: str

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

class DeleteConfigurationBundleRequestTypeDef(TypedDict):
    bundleId: str

class DeleteEvaluatorRequestTypeDef(TypedDict):
    evaluatorId: str

class DeleteGatewayRequestTypeDef(TypedDict):
    gatewayIdentifier: str

class DeleteGatewayRuleRequestTypeDef(TypedDict):
    gatewayIdentifier: str
    ruleId: str

class DeleteGatewayTargetRequestTypeDef(TypedDict):
    gatewayIdentifier: str
    targetId: str

class DeleteHarnessRequestTypeDef(TypedDict):
    harnessId: str
    clientToken: NotRequired[str]

class DeleteMemoryInputTypeDef(TypedDict):
    memoryId: str
    clientToken: NotRequired[str]

class DeleteMemoryStrategyInputTypeDef(TypedDict):
    memoryStrategyId: str

class DeleteOauth2CredentialProviderRequestTypeDef(TypedDict):
    name: str

class DeleteOnlineEvaluationConfigRequestTypeDef(TypedDict):
    onlineEvaluationConfigId: str

class DeletePaymentConnectorRequestTypeDef(TypedDict):
    paymentManagerId: str
    paymentConnectorId: str
    clientToken: NotRequired[str]

class DeletePaymentCredentialProviderRequestTypeDef(TypedDict):
    name: str

class DeletePaymentManagerRequestTypeDef(TypedDict):
    paymentManagerId: str
    clientToken: NotRequired[str]

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

class EfsAccessPointConfigurationTypeDef(TypedDict):
    accessPointArn: str
    mountPath: str

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
    kmsKeyArn: NotRequired[str]

class S3FilesAccessPointConfigurationTypeDef(TypedDict):
    accessPointArn: str
    mountPath: str

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

class GatewaySummaryTypeDef(TypedDict):
    gatewayId: str
    name: str
    status: GatewayStatusType
    createdAt: datetime
    updatedAt: datetime
    authorizerType: AuthorizerTypeType
    description: NotRequired[str]
    protocolType: NotRequired[Literal["MCP"]]

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

class GetConfigurationBundleRequestTypeDef(TypedDict):
    bundleId: str
    branchName: NotRequired[str]

class GetConfigurationBundleVersionRequestTypeDef(TypedDict):
    bundleId: str
    versionId: str

class GetEvaluatorRequestTypeDef(TypedDict):
    evaluatorId: str
    includedData: NotRequired[IncludedDataType]

class GetGatewayRequestTypeDef(TypedDict):
    gatewayIdentifier: str

class GetGatewayRuleRequestTypeDef(TypedDict):
    gatewayIdentifier: str
    ruleId: str

class GetGatewayTargetRequestTypeDef(TypedDict):
    gatewayIdentifier: str
    targetId: str

class GetHarnessRequestTypeDef(TypedDict):
    harnessId: str

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

class GetPaymentConnectorRequestTypeDef(TypedDict):
    paymentManagerId: str
    paymentConnectorId: str

class GetPaymentCredentialProviderRequestTypeDef(TypedDict):
    name: str

class GetPaymentManagerRequestTypeDef(TypedDict):
    paymentManagerId: str

class GetPolicyEngineRequestTypeDef(TypedDict):
    policyEngineId: str

class GetPolicyEngineSummaryRequestTypeDef(TypedDict):
    policyEngineId: str

class GetPolicyGenerationRequestTypeDef(TypedDict):
    policyGenerationId: str
    policyEngineId: str

class ResourceTypeDef(TypedDict):
    arn: NotRequired[str]

class GetPolicyGenerationSummaryRequestTypeDef(TypedDict):
    policyGenerationId: str
    policyEngineId: str

class GetPolicyRequestTypeDef(TypedDict):
    policyEngineId: str
    policyId: str

class GetPolicySummaryRequestTypeDef(TypedDict):
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

class HarnessAgentCoreBrowserConfigTypeDef(TypedDict):
    browserArn: NotRequired[str]

class HarnessAgentCoreCodeInterpreterConfigTypeDef(TypedDict):
    codeInterpreterArn: NotRequired[str]

class HarnessAgentCoreMemoryRetrievalConfigTypeDef(TypedDict):
    topK: NotRequired[int]
    relevanceScore: NotRequired[float]
    strategyId: NotRequired[str]

class HarnessBedrockModelConfigTypeDef(TypedDict):
    modelId: str
    maxTokens: NotRequired[int]
    temperature: NotRequired[float]
    topP: NotRequired[float]

class HarnessGeminiModelConfigTypeDef(TypedDict):
    modelId: str
    apiKeyArn: str
    maxTokens: NotRequired[int]
    temperature: NotRequired[float]
    topP: NotRequired[float]
    topK: NotRequired[int]

class HarnessInlineFunctionConfigOutputTypeDef(TypedDict):
    description: str
    inputSchema: dict[str, Any]

class HarnessInlineFunctionConfigTypeDef(TypedDict):
    description: str
    inputSchema: Mapping[str, Any]

class HarnessOpenAiModelConfigTypeDef(TypedDict):
    modelId: str
    apiKeyArn: str
    maxTokens: NotRequired[int]
    temperature: NotRequired[float]
    topP: NotRequired[float]

class HarnessRemoteMcpConfigOutputTypeDef(TypedDict):
    url: str
    headers: NotRequired[dict[str, str]]

class HarnessRemoteMcpConfigTypeDef(TypedDict):
    url: str
    headers: NotRequired[Mapping[str, str]]

class HarnessSlidingWindowConfigurationTypeDef(TypedDict):
    messagesCount: NotRequired[int]

class HarnessSummarizationConfigurationTypeDef(TypedDict):
    summaryRatio: NotRequired[float]
    preserveRecentMessages: NotRequired[int]
    summarizationSystemPrompt: NotRequired[str]

class HarnessSummaryTypeDef(TypedDict):
    harnessId: str
    harnessName: str
    arn: str
    status: HarnessStatusType
    createdAt: datetime
    updatedAt: datetime

class RuntimeTargetConfigurationTypeDef(TypedDict):
    arn: str
    qualifier: NotRequired[str]

IamPrincipalTypeDef = TypedDict(
    "IamPrincipalTypeDef",
    {
        "arn": str,
        "operator": NotRequired[PrincipalMatchOperatorType],
    },
)

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

class VersionFilterTypeDef(TypedDict):
    branchName: NotRequired[str]
    createdByName: NotRequired[str]
    latestPerBranch: NotRequired[bool]

class ListConfigurationBundlesRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListEvaluatorsRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListGatewayRulesRequestTypeDef(TypedDict):
    gatewayIdentifier: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

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
    resourcePriority: NotRequired[int]

class ListGatewaysRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class ListHarnessesRequestTypeDef(TypedDict):
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

class ListPaymentConnectorsRequestTypeDef(TypedDict):
    paymentManagerId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

PaymentConnectorSummaryTypeDef = TypedDict(
    "PaymentConnectorSummaryTypeDef",
    {
        "paymentConnectorId": str,
        "name": str,
        "type": PaymentConnectorTypeType,
        "status": PaymentConnectorStatusType,
        "lastUpdatedAt": datetime,
    },
)

class ListPaymentCredentialProvidersRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class PaymentCredentialProviderItemTypeDef(TypedDict):
    name: str
    credentialProviderVendor: PaymentCredentialProviderVendorTypeType
    credentialProviderArn: str
    createdTime: datetime
    lastUpdatedTime: datetime

class ListPaymentManagersRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]

class PaymentManagerSummaryTypeDef(TypedDict):
    paymentManagerArn: str
    paymentManagerId: str
    name: str
    authorizerType: PaymentsAuthorizerTypeType
    roleArn: str
    status: PaymentManagerStatusType
    lastUpdatedAt: datetime
    description: NotRequired[str]
    createdAt: NotRequired[datetime]

class ListPoliciesRequestTypeDef(TypedDict):
    policyEngineId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    targetResourceScope: NotRequired[str]

class ListPolicyEngineSummariesRequestTypeDef(TypedDict):
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class PolicyEngineSummaryTypeDef(TypedDict):
    policyEngineId: str
    name: str
    createdAt: datetime
    updatedAt: datetime
    policyEngineArn: str
    status: PolicyEngineStatusType
    encryptionKeyArn: NotRequired[str]

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
    encryptionKeyArn: NotRequired[str]
    description: NotRequired[str]

class ListPolicyGenerationAssetsRequestTypeDef(TypedDict):
    policyGenerationId: str
    policyEngineId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListPolicyGenerationSummariesRequestTypeDef(TypedDict):
    policyEngineId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListPolicyGenerationsRequestTypeDef(TypedDict):
    policyEngineId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]

class ListPolicySummariesRequestTypeDef(TypedDict):
    policyEngineId: str
    nextToken: NotRequired[str]
    maxResults: NotRequired[int]
    targetResourceScope: NotRequired[str]

class PolicySummaryTypeDef(TypedDict):
    policyId: str
    name: str
    policyEngineId: str
    createdAt: datetime
    updatedAt: datetime
    policyArn: str
    status: PolicyStatusType

class ListRegistriesRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    status: NotRequired[RegistryStatusType]
    authorizerType: NotRequired[RegistryAuthorizerTypeType]

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

class SessionConfigurationTypeDef(TypedDict):
    sessionTimeoutInSeconds: NotRequired[int]

class StreamingConfigurationTypeDef(TypedDict):
    enableResponseStreaming: NotRequired[bool]

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

class MatchPathsTypeDef(TypedDict):
    anyOf: Sequence[str]

class ServerDefinitionTypeDef(TypedDict):
    schemaVersion: NotRequired[str]
    inlineContent: NotRequired[str]

class ToolsDefinitionTypeDef(TypedDict):
    protocolVersion: NotRequired[str]
    inlineContent: NotRequired[str]

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

class NumberValidationTypeDef(TypedDict):
    minValue: NotRequired[float]
    maxValue: NotRequired[float]

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

class TokenExchangeGrantTypeConfigTypeOutputTypeDef(TypedDict):
    actorTokenContent: ActorTokenContentTypeType
    actorTokenScopes: NotRequired[list[str]]

class StripePrivyConfigurationInputTypeDef(TypedDict):
    appId: str
    appSecret: str
    authorizationPrivateKey: str
    authorizationId: str

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

class StaticRouteTypeDef(TypedDict):
    targetName: str

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

class StringListValidationOutputTypeDef(TypedDict):
    allowedValues: NotRequired[list[str]]
    maxItems: NotRequired[int]

class StringListValidationTypeDef(TypedDict):
    allowedValues: NotRequired[Sequence[str]]
    maxItems: NotRequired[int]

class StringValidationOutputTypeDef(TypedDict):
    allowedValues: list[str]

class StringValidationTypeDef(TypedDict):
    allowedValues: Sequence[str]

class SubmitRegistryRecordForApprovalRequestTypeDef(TypedDict):
    registryId: str
    recordId: str

class SynchronizeGatewayTargetsRequestTypeDef(TypedDict):
    gatewayIdentifier: str
    targetIdList: Sequence[str]

class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]

class TargetTrafficSplitEntryOutputTypeDef(TypedDict):
    name: str
    weight: int
    targetName: str
    description: NotRequired[str]
    metadata: NotRequired[dict[str, str]]

class TargetTrafficSplitEntryTypeDef(TypedDict):
    name: str
    weight: int
    targetName: str
    description: NotRequired[str]
    metadata: NotRequired[Mapping[str, str]]

class TimeBasedTriggerInputTypeDef(TypedDict):
    idleSessionTimeout: NotRequired[int]

class TimeBasedTriggerTypeDef(TypedDict):
    idleSessionTimeout: NotRequired[int]

class TokenBasedTriggerInputTypeDef(TypedDict):
    tokenCount: NotRequired[int]

class TokenBasedTriggerTypeDef(TypedDict):
    tokenCount: NotRequired[int]

class TokenExchangeGrantTypeConfigTypeTypeDef(TypedDict):
    actorTokenContent: ActorTokenContentTypeType
    actorTokenScopes: NotRequired[Sequence[str]]

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

class HarnessEnvironmentArtifactTypeDef(TypedDict):
    containerConfiguration: NotRequired[ContainerConfigurationTypeDef]

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

VpcConfigUnionTypeDef = Union[VpcConfigTypeDef, VpcConfigOutputTypeDef]

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

class CoinbaseCdpConfigurationOutputTypeDef(TypedDict):
    apiKeyId: str
    apiKeySecretArn: SecretTypeDef
    walletSecretArn: SecretTypeDef

class StripePrivyConfigurationOutputTypeDef(TypedDict):
    appId: str
    appSecretArn: SecretTypeDef
    authorizationPrivateKeyArn: SecretTypeDef
    authorizationId: str

ComponentConfigurationUnionTypeDef = Union[
    ComponentConfigurationTypeDef, ComponentConfigurationOutputTypeDef
]

class TrafficSplitEntryOutputTypeDef(TypedDict):
    name: str
    weight: int
    configurationBundle: ConfigurationBundleReferenceTypeDef
    description: NotRequired[str]
    metadata: NotRequired[dict[str, str]]

class TrafficSplitEntryTypeDef(TypedDict):
    name: str
    weight: int
    configurationBundle: ConfigurationBundleReferenceTypeDef
    description: NotRequired[str]
    metadata: NotRequired[Mapping[str, str]]

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

class CreateApiKeyCredentialProviderResponseTypeDef(TypedDict):
    apiKeySecretArn: SecretTypeDef
    name: str
    credentialProviderArn: str
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

class CreateConfigurationBundleResponseTypeDef(TypedDict):
    bundleArn: str
    bundleId: str
    versionId: str
    createdAt: datetime
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
    createdAt: datetime
    updatedAt: datetime
    policyEngineArn: str
    status: PolicyEngineStatusType
    encryptionKeyArn: str
    description: str
    statusReasons: list[str]
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

class DeleteConfigurationBundleResponseTypeDef(TypedDict):
    bundleId: str
    status: ConfigurationBundleStatusType
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

class DeleteGatewayRuleResponseTypeDef(TypedDict):
    ruleId: str
    status: GatewayRuleStatusType
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

class DeletePaymentConnectorResponseTypeDef(TypedDict):
    status: PaymentConnectorStatusType
    paymentConnectorId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeletePaymentManagerResponseTypeDef(TypedDict):
    status: PaymentManagerStatusType
    paymentManagerId: str
    ResponseMetadata: ResponseMetadataTypeDef

class DeletePolicyEngineResponseTypeDef(TypedDict):
    policyEngineId: str
    name: str
    createdAt: datetime
    updatedAt: datetime
    policyEngineArn: str
    status: PolicyEngineStatusType
    encryptionKeyArn: str
    description: str
    statusReasons: list[str]
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

class GetApiKeyCredentialProviderResponseTypeDef(TypedDict):
    apiKeySecretArn: SecretTypeDef
    name: str
    credentialProviderArn: str
    createdTime: datetime
    lastUpdatedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

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
    createdAt: datetime
    updatedAt: datetime
    policyEngineArn: str
    status: PolicyEngineStatusType
    encryptionKeyArn: str
    description: str
    statusReasons: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetPolicyEngineSummaryResponseTypeDef(TypedDict):
    policyEngineId: str
    name: str
    createdAt: datetime
    updatedAt: datetime
    policyEngineArn: str
    status: PolicyEngineStatusType
    encryptionKeyArn: str
    ResponseMetadata: ResponseMetadataTypeDef

class GetPolicySummaryResponseTypeDef(TypedDict):
    policyId: str
    name: str
    policyEngineId: str
    createdAt: datetime
    updatedAt: datetime
    policyArn: str
    status: PolicyStatusType
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

class ListConfigurationBundlesResponseTypeDef(TypedDict):
    bundles: list[ConfigurationBundleSummaryTypeDef]
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

class UpdateApiKeyCredentialProviderResponseTypeDef(TypedDict):
    apiKeySecretArn: SecretTypeDef
    name: str
    credentialProviderArn: str
    createdTime: datetime
    lastUpdatedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateConfigurationBundleResponseTypeDef(TypedDict):
    bundleArn: str
    bundleId: str
    versionId: str
    updatedAt: datetime
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
    createdAt: datetime
    updatedAt: datetime
    policyEngineArn: str
    status: PolicyEngineStatusType
    encryptionKeyArn: str
    description: str
    statusReasons: list[str]
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

class UpdatePaymentManagerResponseTypeDef(TypedDict):
    paymentManagerArn: str
    paymentManagerId: str
    name: str
    authorizerType: PaymentsAuthorizerTypeType
    roleArn: str
    workloadIdentityDetails: WorkloadIdentityDetailsTypeDef
    lastUpdatedAt: datetime
    status: PaymentManagerStatusType
    ResponseMetadata: ResponseMetadataTypeDef

class VersionLineageMetadataTypeDef(TypedDict):
    parentVersionIds: NotRequired[list[str]]
    branchName: NotRequired[str]
    createdBy: NotRequired[VersionCreatedBySourceTypeDef]
    commitMessage: NotRequired[str]

class CredentialProviderOutputTypeDef(TypedDict):
    oauthCredentialProvider: NotRequired[OAuthCredentialProviderOutputTypeDef]
    apiKeyCredentialProvider: NotRequired[ApiKeyCredentialProviderTypeDef]
    iamCredentialProvider: NotRequired[IamCredentialProviderTypeDef]

class HarnessGatewayOutboundAuthOutputTypeDef(TypedDict):
    awsIam: NotRequired[dict[str, Any]]
    none: NotRequired[dict[str, Any]]
    oauth: NotRequired[OAuthCredentialProviderOutputTypeDef]

class CredentialsProviderConfigurationTypeDef(TypedDict):
    coinbaseCDP: NotRequired[PaymentCredentialProviderConfigurationTypeDef]
    stripePrivy: NotRequired[PaymentCredentialProviderConfigurationTypeDef]

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

class ListEvaluatorsResponseTypeDef(TypedDict):
    evaluators: list[EvaluatorSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class FilesystemConfigurationTypeDef(TypedDict):
    sessionStorage: NotRequired[SessionStorageConfigurationTypeDef]
    s3FilesAccessPoint: NotRequired[S3FilesAccessPointConfigurationTypeDef]
    efsAccessPoint: NotRequired[EfsAccessPointConfigurationTypeDef]

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "key": str,
        "operator": FilterOperatorType,
        "value": FilterValueTypeDef,
    },
)

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
    findings: str
    statusReasons: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetPolicyGenerationSummaryResponseTypeDef(TypedDict):
    policyEngineId: str
    policyGenerationId: str
    name: str
    policyGenerationArn: str
    resource: ResourceTypeDef
    createdAt: datetime
    updatedAt: datetime
    status: PolicyGenerationStatusType
    findings: str
    ResponseMetadata: ResponseMetadataTypeDef

class PolicyGenerationSummaryTypeDef(TypedDict):
    policyEngineId: str
    policyGenerationId: str
    name: str
    policyGenerationArn: str
    resource: ResourceTypeDef
    createdAt: datetime
    updatedAt: datetime
    status: PolicyGenerationStatusType
    findings: NotRequired[str]

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
    findings: str
    statusReasons: list[str]
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

class HarnessAgentCoreMemoryConfigurationOutputTypeDef(TypedDict):
    arn: str
    actorId: NotRequired[str]
    messagesCount: NotRequired[int]
    retrievalConfig: NotRequired[dict[str, HarnessAgentCoreMemoryRetrievalConfigTypeDef]]

class HarnessAgentCoreMemoryConfigurationTypeDef(TypedDict):
    arn: str
    actorId: NotRequired[str]
    messagesCount: NotRequired[int]
    retrievalConfig: NotRequired[Mapping[str, HarnessAgentCoreMemoryRetrievalConfigTypeDef]]

HarnessInlineFunctionConfigUnionTypeDef = Union[
    HarnessInlineFunctionConfigTypeDef, HarnessInlineFunctionConfigOutputTypeDef
]

class HarnessModelConfigurationTypeDef(TypedDict):
    bedrockModelConfig: NotRequired[HarnessBedrockModelConfigTypeDef]
    openAiModelConfig: NotRequired[HarnessOpenAiModelConfigTypeDef]
    geminiModelConfig: NotRequired[HarnessGeminiModelConfigTypeDef]

HarnessRemoteMcpConfigUnionTypeDef = Union[
    HarnessRemoteMcpConfigTypeDef, HarnessRemoteMcpConfigOutputTypeDef
]

class HarnessTruncationStrategyConfigurationTypeDef(TypedDict):
    slidingWindow: NotRequired[HarnessSlidingWindowConfigurationTypeDef]
    summarization: NotRequired[HarnessSummarizationConfigurationTypeDef]

class ListHarnessesResponseTypeDef(TypedDict):
    harnesses: list[HarnessSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class HttpTargetConfigurationTypeDef(TypedDict):
    agentcoreRuntime: NotRequired[RuntimeTargetConfigurationTypeDef]

class MatchPrincipalEntryTypeDef(TypedDict):
    iamPrincipal: NotRequired[IamPrincipalTypeDef]

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

class ListConfigurationBundlesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListEvaluatorsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListGatewayRulesRequestPaginateTypeDef(TypedDict):
    gatewayIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListGatewayTargetsRequestPaginateTypeDef(TypedDict):
    gatewayIdentifier: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListGatewaysRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListHarnessesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListMemoriesInputPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOauth2CredentialProvidersRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListOnlineEvaluationConfigsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPaymentConnectorsRequestPaginateTypeDef(TypedDict):
    paymentManagerId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPaymentCredentialProvidersRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPaymentManagersRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPoliciesRequestPaginateTypeDef(TypedDict):
    policyEngineId: str
    targetResourceScope: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPolicyEngineSummariesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPolicyEnginesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPolicyGenerationAssetsRequestPaginateTypeDef(TypedDict):
    policyGenerationId: str
    policyEngineId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPolicyGenerationSummariesRequestPaginateTypeDef(TypedDict):
    policyEngineId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPolicyGenerationsRequestPaginateTypeDef(TypedDict):
    policyEngineId: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListPolicySummariesRequestPaginateTypeDef(TypedDict):
    policyEngineId: str
    targetResourceScope: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRegistriesRequestPaginateTypeDef(TypedDict):
    status: NotRequired[RegistryStatusType]
    authorizerType: NotRequired[RegistryAuthorizerTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListRegistryRecordsRequestPaginateTypeDef(TypedDict):
    registryId: str
    name: NotRequired[str]
    status: NotRequired[RegistryRecordStatusType]
    descriptorType: NotRequired[DescriptorTypeType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListWorkloadIdentitiesRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

ListConfigurationBundleVersionsRequestPaginateTypeDef = TypedDict(
    "ListConfigurationBundleVersionsRequestPaginateTypeDef",
    {
        "bundleId": str,
        "filter": NotRequired[VersionFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListConfigurationBundleVersionsRequestTypeDef = TypedDict(
    "ListConfigurationBundleVersionsRequestTypeDef",
    {
        "bundleId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "filter": NotRequired[VersionFilterTypeDef],
    },
)

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

class ListPaymentConnectorsResponseTypeDef(TypedDict):
    paymentConnectors: list[PaymentConnectorSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListPaymentCredentialProvidersResponseTypeDef(TypedDict):
    credentialProviders: list[PaymentCredentialProviderItemTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListPaymentManagersResponseTypeDef(TypedDict):
    paymentManagers: list[PaymentManagerSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListPolicyEngineSummariesResponseTypeDef(TypedDict):
    policyEngines: list[PolicyEngineSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListPolicyEnginesResponseTypeDef(TypedDict):
    policyEngines: list[PolicyEngineTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListPolicySummariesResponseTypeDef(TypedDict):
    policies: list[PolicySummaryTypeDef]
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

class MCPGatewayConfigurationOutputTypeDef(TypedDict):
    supportedVersions: NotRequired[list[str]]
    instructions: NotRequired[str]
    searchType: NotRequired[Literal["SEMANTIC"]]
    sessionConfiguration: NotRequired[SessionConfigurationTypeDef]
    streamingConfiguration: NotRequired[StreamingConfigurationTypeDef]

class MCPGatewayConfigurationTypeDef(TypedDict):
    supportedVersions: NotRequired[Sequence[str]]
    instructions: NotRequired[str]
    searchType: NotRequired[Literal["SEMANTIC"]]
    sessionConfiguration: NotRequired[SessionConfigurationTypeDef]
    streamingConfiguration: NotRequired[StreamingConfigurationTypeDef]

ManagedVpcResourceUnionTypeDef = Union[ManagedVpcResourceTypeDef, ManagedVpcResourceOutputTypeDef]
MatchPathsUnionTypeDef = Union[MatchPathsTypeDef, MatchPathsOutputTypeDef]

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

class OnBehalfOfTokenExchangeConfigTypeOutputTypeDef(TypedDict):
    grantType: OnBehalfOfTokenExchangeGrantTypeTypeType
    tokenExchangeGrantTypeConfig: NotRequired[TokenExchangeGrantTypeConfigTypeOutputTypeDef]

class PaymentProviderConfigurationInputTypeDef(TypedDict):
    coinbaseCdpConfiguration: NotRequired[CoinbaseCdpConfigurationInputTypeDef]
    stripePrivyConfiguration: NotRequired[StripePrivyConfigurationInputTypeDef]

class PolicyDefinitionTypeDef(TypedDict):
    cedar: NotRequired[CedarPolicyTypeDef]
    policyGeneration: NotRequired[PolicyGenerationDetailsTypeDef]

class PrivateEndpointOutputTypeDef(TypedDict):
    selfManagedLatticeResource: NotRequired[SelfManagedLatticeResourceTypeDef]
    managedVpcResource: NotRequired[ManagedVpcResourceOutputTypeDef]

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

StringListValidationUnionTypeDef = Union[
    StringListValidationTypeDef, StringListValidationOutputTypeDef
]

class ValidationOutputTypeDef(TypedDict):
    stringValidation: NotRequired[StringValidationOutputTypeDef]
    stringListValidation: NotRequired[StringListValidationOutputTypeDef]
    numberValidation: NotRequired[NumberValidationTypeDef]

StringValidationUnionTypeDef = Union[StringValidationTypeDef, StringValidationOutputTypeDef]

class WeightedRouteOutputTypeDef(TypedDict):
    trafficSplit: list[TargetTrafficSplitEntryOutputTypeDef]

TargetTrafficSplitEntryUnionTypeDef = Union[
    TargetTrafficSplitEntryTypeDef, TargetTrafficSplitEntryOutputTypeDef
]

class TriggerConditionInputTypeDef(TypedDict):
    messageBasedTrigger: NotRequired[MessageBasedTriggerInputTypeDef]
    tokenBasedTrigger: NotRequired[TokenBasedTriggerInputTypeDef]
    timeBasedTrigger: NotRequired[TimeBasedTriggerInputTypeDef]

class TriggerConditionTypeDef(TypedDict):
    messageBasedTrigger: NotRequired[MessageBasedTriggerTypeDef]
    tokenBasedTrigger: NotRequired[TokenBasedTriggerTypeDef]
    timeBasedTrigger: NotRequired[TimeBasedTriggerTypeDef]

TokenExchangeGrantTypeConfigTypeUnionTypeDef = Union[
    TokenExchangeGrantTypeConfigTypeTypeDef, TokenExchangeGrantTypeConfigTypeOutputTypeDef
]

class UpdatePolicyEngineRequestTypeDef(TypedDict):
    policyEngineId: str
    description: NotRequired[UpdatedDescriptionTypeDef]

class UpdatedA2aDescriptorTypeDef(TypedDict):
    optionalValue: NotRequired[A2aDescriptorTypeDef]

class UpdatedHarnessEnvironmentArtifactTypeDef(TypedDict):
    optionalValue: NotRequired[HarnessEnvironmentArtifactTypeDef]

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
    resourcePriority: NotRequired[int]

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

class NetworkConfigurationTypeDef(TypedDict):
    networkMode: NetworkModeType
    networkModeConfig: NotRequired[VpcConfigUnionTypeDef]

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

class PaymentProviderConfigurationOutputTypeDef(TypedDict):
    coinbaseCdpConfiguration: NotRequired[CoinbaseCdpConfigurationOutputTypeDef]
    stripePrivyConfiguration: NotRequired[StripePrivyConfigurationOutputTypeDef]

class CreateConfigurationBundleRequestTypeDef(TypedDict):
    bundleName: str
    components: Mapping[str, ComponentConfigurationUnionTypeDef]
    clientToken: NotRequired[str]
    description: NotRequired[str]
    branchName: NotRequired[str]
    commitMessage: NotRequired[str]
    createdBy: NotRequired[VersionCreatedBySourceTypeDef]
    tags: NotRequired[Mapping[str, str]]

class UpdateConfigurationBundleRequestTypeDef(TypedDict):
    bundleId: str
    clientToken: NotRequired[str]
    bundleName: NotRequired[str]
    description: NotRequired[str]
    components: NotRequired[Mapping[str, ComponentConfigurationUnionTypeDef]]
    parentVersionIds: NotRequired[Sequence[str]]
    branchName: NotRequired[str]
    commitMessage: NotRequired[str]
    createdBy: NotRequired[VersionCreatedBySourceTypeDef]

class WeightedOverrideOutputTypeDef(TypedDict):
    trafficSplit: list[TrafficSplitEntryOutputTypeDef]

TrafficSplitEntryUnionTypeDef = Union[TrafficSplitEntryTypeDef, TrafficSplitEntryOutputTypeDef]

class StreamDeliveryResourceOutputTypeDef(TypedDict):
    kinesis: NotRequired[KinesisResourceOutputTypeDef]

class StreamDeliveryResourceTypeDef(TypedDict):
    kinesis: NotRequired[KinesisResourceTypeDef]

class ConfigurationBundleVersionSummaryTypeDef(TypedDict):
    bundleArn: str
    bundleId: str
    versionId: str
    versionCreatedAt: datetime
    lineageMetadata: NotRequired[VersionLineageMetadataTypeDef]

class GetConfigurationBundleResponseTypeDef(TypedDict):
    bundleArn: str
    bundleId: str
    bundleName: str
    description: str
    versionId: str
    components: dict[str, ComponentConfigurationOutputTypeDef]
    lineageMetadata: VersionLineageMetadataTypeDef
    createdAt: datetime
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class GetConfigurationBundleVersionResponseTypeDef(TypedDict):
    bundleArn: str
    bundleId: str
    bundleName: str
    description: str
    versionId: str
    components: dict[str, ComponentConfigurationOutputTypeDef]
    lineageMetadata: VersionLineageMetadataTypeDef
    createdAt: datetime
    versionCreatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class CredentialProviderConfigurationOutputTypeDef(TypedDict):
    credentialProviderType: CredentialProviderTypeType
    credentialProvider: NotRequired[CredentialProviderOutputTypeDef]

class HarnessAgentCoreGatewayConfigOutputTypeDef(TypedDict):
    gatewayArn: str
    outboundAuth: NotRequired[HarnessGatewayOutboundAuthOutputTypeDef]

CreatePaymentConnectorRequestTypeDef = TypedDict(
    "CreatePaymentConnectorRequestTypeDef",
    {
        "paymentManagerId": str,
        "name": str,
        "type": PaymentConnectorTypeType,
        "credentialProviderConfigurations": Sequence[CredentialsProviderConfigurationTypeDef],
        "description": NotRequired[str],
        "clientToken": NotRequired[str],
    },
)
CreatePaymentConnectorResponseTypeDef = TypedDict(
    "CreatePaymentConnectorResponseTypeDef",
    {
        "paymentConnectorId": str,
        "paymentManagerId": str,
        "name": str,
        "type": PaymentConnectorTypeType,
        "credentialProviderConfigurations": list[CredentialsProviderConfigurationTypeDef],
        "createdAt": datetime,
        "status": PaymentConnectorStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetPaymentConnectorResponseTypeDef = TypedDict(
    "GetPaymentConnectorResponseTypeDef",
    {
        "paymentConnectorId": str,
        "name": str,
        "description": str,
        "type": PaymentConnectorTypeType,
        "credentialProviderConfigurations": list[CredentialsProviderConfigurationTypeDef],
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "status": PaymentConnectorStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdatePaymentConnectorRequestTypeDef = TypedDict(
    "UpdatePaymentConnectorRequestTypeDef",
    {
        "paymentManagerId": str,
        "paymentConnectorId": str,
        "description": NotRequired[str],
        "type": NotRequired[PaymentConnectorTypeType],
        "credentialProviderConfigurations": NotRequired[
            Sequence[CredentialsProviderConfigurationTypeDef]
        ],
        "clientToken": NotRequired[str],
    },
)
UpdatePaymentConnectorResponseTypeDef = TypedDict(
    "UpdatePaymentConnectorResponseTypeDef",
    {
        "paymentConnectorId": str,
        "paymentManagerId": str,
        "name": str,
        "type": PaymentConnectorTypeType,
        "credentialProviderConfigurations": list[CredentialsProviderConfigurationTypeDef],
        "lastUpdatedAt": datetime,
        "status": PaymentConnectorStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

class ModifyConsolidationConfigurationTypeDef(TypedDict):
    customConsolidationConfiguration: NotRequired[CustomConsolidationConfigurationInputTypeDef]

class ConsolidationConfigurationTypeDef(TypedDict):
    customConsolidationConfiguration: NotRequired[CustomConsolidationConfigurationTypeDef]

class ModifyExtractionConfigurationTypeDef(TypedDict):
    customExtractionConfiguration: NotRequired[CustomExtractionConfigurationInputTypeDef]

class ExtractionConfigurationTypeDef(TypedDict):
    customExtractionConfiguration: NotRequired[CustomExtractionConfigurationTypeDef]

class HarnessAgentCoreRuntimeEnvironmentTypeDef(TypedDict):
    agentRuntimeArn: str
    agentRuntimeName: str
    agentRuntimeId: str
    lifecycleConfiguration: LifecycleConfigurationTypeDef
    networkConfiguration: NetworkConfigurationOutputTypeDef
    filesystemConfigurations: NotRequired[list[FilesystemConfigurationTypeDef]]

class RuleOutputTypeDef(TypedDict):
    samplingConfig: SamplingConfigTypeDef
    filters: NotRequired[list[FilterTypeDef]]
    sessionConfig: NotRequired[SessionConfigTypeDef]

class RuleTypeDef(TypedDict):
    samplingConfig: SamplingConfigTypeDef
    filters: NotRequired[Sequence[FilterTypeDef]]
    sessionConfig: NotRequired[SessionConfigTypeDef]

class ListPolicyGenerationSummariesResponseTypeDef(TypedDict):
    policyGenerations: list[PolicyGenerationSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListPolicyGenerationsResponseTypeDef(TypedDict):
    policyGenerations: list[PolicyGenerationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class HarnessMemoryConfigurationOutputTypeDef(TypedDict):
    agentCoreMemoryConfiguration: NotRequired[HarnessAgentCoreMemoryConfigurationOutputTypeDef]

HarnessAgentCoreMemoryConfigurationUnionTypeDef = Union[
    HarnessAgentCoreMemoryConfigurationTypeDef, HarnessAgentCoreMemoryConfigurationOutputTypeDef
]

class HarnessTruncationConfigurationTypeDef(TypedDict):
    strategy: HarnessTruncationStrategyType
    config: NotRequired[HarnessTruncationStrategyConfigurationTypeDef]

class MatchPrincipalsOutputTypeDef(TypedDict):
    anyOf: list[MatchPrincipalEntryTypeDef]

class MatchPrincipalsTypeDef(TypedDict):
    anyOf: Sequence[MatchPrincipalEntryTypeDef]

class GatewayInterceptorConfigurationOutputTypeDef(TypedDict):
    interceptor: InterceptorConfigurationTypeDef
    interceptionPoints: list[GatewayInterceptionPointType]
    inputConfiguration: NotRequired[InterceptorInputConfigurationTypeDef]

class GatewayInterceptorConfigurationTypeDef(TypedDict):
    interceptor: InterceptorConfigurationTypeDef
    interceptionPoints: Sequence[GatewayInterceptionPointType]
    inputConfiguration: NotRequired[InterceptorInputConfigurationTypeDef]

class GatewayProtocolConfigurationOutputTypeDef(TypedDict):
    mcp: NotRequired[MCPGatewayConfigurationOutputTypeDef]

class GatewayProtocolConfigurationTypeDef(TypedDict):
    mcp: NotRequired[MCPGatewayConfigurationTypeDef]

class PrivateEndpointTypeDef(TypedDict):
    selfManagedLatticeResource: NotRequired[SelfManagedLatticeResourceTypeDef]
    managedVpcResource: NotRequired[ManagedVpcResourceUnionTypeDef]

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

class HarnessGatewayOutboundAuthTypeDef(TypedDict):
    awsIam: NotRequired[Mapping[str, Any]]
    none: NotRequired[Mapping[str, Any]]
    oauth: NotRequired[OAuthCredentialProviderUnionTypeDef]

class AtlassianOauth2ProviderConfigOutputTypeDef(TypedDict):
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

class CreatePaymentCredentialProviderRequestTypeDef(TypedDict):
    name: str
    credentialProviderVendor: PaymentCredentialProviderVendorTypeType
    providerConfigurationInput: PaymentProviderConfigurationInputTypeDef
    tags: NotRequired[Mapping[str, str]]

class UpdatePaymentCredentialProviderRequestTypeDef(TypedDict):
    name: str
    credentialProviderVendor: PaymentCredentialProviderVendorTypeType
    providerConfigurationInput: PaymentProviderConfigurationInputTypeDef

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
    createdAt: datetime
    updatedAt: datetime
    policyArn: str
    status: PolicyStatusType
    definition: PolicyDefinitionTypeDef
    description: str
    statusReasons: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class DeletePolicyResponseTypeDef(TypedDict):
    policyId: str
    name: str
    policyEngineId: str
    createdAt: datetime
    updatedAt: datetime
    policyArn: str
    status: PolicyStatusType
    definition: PolicyDefinitionTypeDef
    description: str
    statusReasons: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class GetPolicyResponseTypeDef(TypedDict):
    policyId: str
    name: str
    policyEngineId: str
    createdAt: datetime
    updatedAt: datetime
    policyArn: str
    status: PolicyStatusType
    definition: PolicyDefinitionTypeDef
    description: str
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
    createdAt: datetime
    updatedAt: datetime
    policyArn: str
    status: PolicyStatusType
    definition: PolicyDefinitionTypeDef
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
    createdAt: datetime
    updatedAt: datetime
    policyArn: str
    status: PolicyStatusType
    definition: PolicyDefinitionTypeDef
    description: str
    statusReasons: list[str]
    ResponseMetadata: ResponseMetadataTypeDef

class PrivateEndpointOverrideOutputTypeDef(TypedDict):
    domain: str
    privateEndpoint: PrivateEndpointOutputTypeDef

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

class LlmExtractionConfigOutputTypeDef(TypedDict):
    definition: str
    llmExtractionInstruction: NotRequired[str]
    validation: NotRequired[ValidationOutputTypeDef]

class ValidationTypeDef(TypedDict):
    stringValidation: NotRequired[StringValidationUnionTypeDef]
    stringListValidation: NotRequired[StringListValidationUnionTypeDef]
    numberValidation: NotRequired[NumberValidationTypeDef]

class RouteToTargetActionOutputTypeDef(TypedDict):
    staticRoute: NotRequired[StaticRouteTypeDef]
    weightedRoute: NotRequired[WeightedRouteOutputTypeDef]

class WeightedRouteTypeDef(TypedDict):
    trafficSplit: Sequence[TargetTrafficSplitEntryUnionTypeDef]

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

class OnBehalfOfTokenExchangeConfigTypeTypeDef(TypedDict):
    grantType: OnBehalfOfTokenExchangeGrantTypeTypeType
    tokenExchangeGrantTypeConfig: NotRequired[TokenExchangeGrantTypeConfigTypeUnionTypeDef]

class UpdatedAgentSkillsDescriptorTypeDef(TypedDict):
    optionalValue: NotRequired[UpdatedAgentSkillsDescriptorFieldsTypeDef]

class LlmAsAJudgeEvaluatorConfigOutputTypeDef(TypedDict):
    instructions: str
    ratingScale: RatingScaleOutputTypeDef
    modelConfig: EvaluatorModelConfigOutputTypeDef

class LlmAsAJudgeEvaluatorConfigTypeDef(TypedDict):
    instructions: str
    ratingScale: RatingScaleTypeDef
    modelConfig: EvaluatorModelConfigTypeDef

NetworkConfigurationUnionTypeDef = Union[
    NetworkConfigurationTypeDef, NetworkConfigurationOutputTypeDef
]

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

class CreatePaymentCredentialProviderResponseTypeDef(TypedDict):
    name: str
    credentialProviderVendor: PaymentCredentialProviderVendorTypeType
    credentialProviderArn: str
    providerConfigurationOutput: PaymentProviderConfigurationOutputTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetPaymentCredentialProviderResponseTypeDef(TypedDict):
    name: str
    credentialProviderArn: str
    credentialProviderVendor: PaymentCredentialProviderVendorTypeType
    providerConfigurationOutput: PaymentProviderConfigurationOutputTypeDef
    createdTime: datetime
    lastUpdatedTime: datetime
    tags: dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef

class UpdatePaymentCredentialProviderResponseTypeDef(TypedDict):
    name: str
    credentialProviderVendor: PaymentCredentialProviderVendorTypeType
    credentialProviderArn: str
    providerConfigurationOutput: PaymentProviderConfigurationOutputTypeDef
    createdTime: datetime
    lastUpdatedTime: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ConfigurationBundleActionOutputTypeDef(TypedDict):
    staticOverride: NotRequired[StaticOverrideTypeDef]
    weightedOverride: NotRequired[WeightedOverrideOutputTypeDef]

class WeightedOverrideTypeDef(TypedDict):
    trafficSplit: Sequence[TrafficSplitEntryUnionTypeDef]

class StreamDeliveryResourcesOutputTypeDef(TypedDict):
    resources: list[StreamDeliveryResourceOutputTypeDef]

class StreamDeliveryResourcesTypeDef(TypedDict):
    resources: Sequence[StreamDeliveryResourceTypeDef]

class ListConfigurationBundleVersionsResponseTypeDef(TypedDict):
    versions: list[ConfigurationBundleVersionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class HarnessToolConfigurationOutputTypeDef(TypedDict):
    remoteMcp: NotRequired[HarnessRemoteMcpConfigOutputTypeDef]
    agentCoreBrowser: NotRequired[HarnessAgentCoreBrowserConfigTypeDef]
    agentCoreGateway: NotRequired[HarnessAgentCoreGatewayConfigOutputTypeDef]
    inlineFunction: NotRequired[HarnessInlineFunctionConfigOutputTypeDef]
    agentCoreCodeInterpreter: NotRequired[HarnessAgentCoreCodeInterpreterConfigTypeDef]

class HarnessEnvironmentProviderTypeDef(TypedDict):
    agentCoreRuntimeEnvironment: NotRequired[HarnessAgentCoreRuntimeEnvironmentTypeDef]

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

class HarnessMemoryConfigurationTypeDef(TypedDict):
    agentCoreMemoryConfiguration: NotRequired[HarnessAgentCoreMemoryConfigurationUnionTypeDef]

class ConditionOutputTypeDef(TypedDict):
    matchPrincipals: NotRequired[MatchPrincipalsOutputTypeDef]
    matchPaths: NotRequired[MatchPathsOutputTypeDef]

MatchPrincipalsUnionTypeDef = Union[MatchPrincipalsTypeDef, MatchPrincipalsOutputTypeDef]
GatewayInterceptorConfigurationUnionTypeDef = Union[
    GatewayInterceptorConfigurationTypeDef, GatewayInterceptorConfigurationOutputTypeDef
]
GatewayProtocolConfigurationUnionTypeDef = Union[
    GatewayProtocolConfigurationTypeDef, GatewayProtocolConfigurationOutputTypeDef
]
PrivateEndpointUnionTypeDef = Union[PrivateEndpointTypeDef, PrivateEndpointOutputTypeDef]

class UpdatedMcpDescriptorTypeDef(TypedDict):
    optionalValue: NotRequired[UpdatedMcpDescriptorFieldsTypeDef]

CredentialProviderUnionTypeDef = Union[CredentialProviderTypeDef, CredentialProviderOutputTypeDef]
HarnessGatewayOutboundAuthUnionTypeDef = Union[
    HarnessGatewayOutboundAuthTypeDef, HarnessGatewayOutboundAuthOutputTypeDef
]
Oauth2DiscoveryUnionTypeDef = Union[Oauth2DiscoveryTypeDef, Oauth2DiscoveryOutputTypeDef]

class ListPolicyGenerationAssetsResponseTypeDef(TypedDict):
    policyGenerationAssets: list[PolicyGenerationAssetTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class ListPoliciesResponseTypeDef(TypedDict):
    policies: list[PolicyTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

class CustomJWTAuthorizerConfigurationOutputTypeDef(TypedDict):
    discoveryUrl: str
    allowedAudience: NotRequired[list[str]]
    allowedClients: NotRequired[list[str]]
    allowedScopes: NotRequired[list[str]]
    customClaims: NotRequired[list[CustomClaimValidationTypeOutputTypeDef]]
    privateEndpoint: NotRequired[PrivateEndpointOutputTypeDef]
    privateEndpointOverrides: NotRequired[list[PrivateEndpointOverrideOutputTypeDef]]

class CustomOauth2ProviderConfigOutputTypeDef(TypedDict):
    oauthDiscovery: Oauth2DiscoveryOutputTypeDef
    clientId: NotRequired[str]
    privateEndpoint: NotRequired[PrivateEndpointOutputTypeDef]
    privateEndpointOverrides: NotRequired[list[PrivateEndpointOverrideOutputTypeDef]]
    onBehalfOfTokenExchangeConfig: NotRequired[OnBehalfOfTokenExchangeConfigTypeOutputTypeDef]
    clientAuthenticationMethod: NotRequired[ClientAuthenticationMethodTypeType]

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

class ExtractionConfigOutputTypeDef(TypedDict):
    llmExtractionConfig: NotRequired[LlmExtractionConfigOutputTypeDef]

ValidationUnionTypeDef = Union[ValidationTypeDef, ValidationOutputTypeDef]
WeightedRouteUnionTypeDef = Union[WeightedRouteTypeDef, WeightedRouteOutputTypeDef]
OnBehalfOfTokenExchangeConfigTypeUnionTypeDef = Union[
    OnBehalfOfTokenExchangeConfigTypeTypeDef, OnBehalfOfTokenExchangeConfigTypeOutputTypeDef
]

class EvaluatorConfigOutputTypeDef(TypedDict):
    llmAsAJudge: NotRequired[LlmAsAJudgeEvaluatorConfigOutputTypeDef]
    codeBased: NotRequired[CodeBasedEvaluatorConfigTypeDef]

class EvaluatorConfigTypeDef(TypedDict):
    llmAsAJudge: NotRequired[LlmAsAJudgeEvaluatorConfigTypeDef]
    codeBased: NotRequired[CodeBasedEvaluatorConfigTypeDef]

class HarnessAgentCoreRuntimeEnvironmentRequestTypeDef(TypedDict):
    lifecycleConfiguration: NotRequired[LifecycleConfigurationTypeDef]
    networkConfiguration: NotRequired[NetworkConfigurationUnionTypeDef]
    filesystemConfigurations: NotRequired[Sequence[FilesystemConfigurationTypeDef]]

class CustomClaimValidationTypeTypeDef(TypedDict):
    inboundTokenClaimName: str
    inboundTokenClaimValueType: InboundTokenClaimValueTypeType
    authorizingClaimMatchValue: AuthorizingClaimMatchValueTypeUnionTypeDef

AgentRuntimeArtifactUnionTypeDef = Union[
    AgentRuntimeArtifactTypeDef, AgentRuntimeArtifactOutputTypeDef
]

class ActionOutputTypeDef(TypedDict):
    configurationBundle: NotRequired[ConfigurationBundleActionOutputTypeDef]
    routeToTarget: NotRequired[RouteToTargetActionOutputTypeDef]

WeightedOverrideUnionTypeDef = Union[WeightedOverrideTypeDef, WeightedOverrideOutputTypeDef]
StreamDeliveryResourcesUnionTypeDef = Union[
    StreamDeliveryResourcesTypeDef, StreamDeliveryResourcesOutputTypeDef
]
HarnessToolOutputTypeDef = TypedDict(
    "HarnessToolOutputTypeDef",
    {
        "type": HarnessToolTypeType,
        "name": NotRequired[str],
        "config": NotRequired[HarnessToolConfigurationOutputTypeDef],
    },
)

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

HarnessMemoryConfigurationUnionTypeDef = Union[
    HarnessMemoryConfigurationTypeDef, HarnessMemoryConfigurationOutputTypeDef
]

class ConditionTypeDef(TypedDict):
    matchPrincipals: NotRequired[MatchPrincipalsUnionTypeDef]
    matchPaths: NotRequired[MatchPathsUnionTypeDef]

class PrivateEndpointOverrideTypeDef(TypedDict):
    domain: str
    privateEndpoint: PrivateEndpointUnionTypeDef

class UpdatedDescriptorsUnionTypeDef(TypedDict):
    mcp: NotRequired[UpdatedMcpDescriptorTypeDef]
    a2a: NotRequired[UpdatedA2aDescriptorTypeDef]
    custom: NotRequired[UpdatedCustomDescriptorTypeDef]
    agentSkills: NotRequired[UpdatedAgentSkillsDescriptorTypeDef]

class CredentialProviderConfigurationTypeDef(TypedDict):
    credentialProviderType: CredentialProviderTypeType
    credentialProvider: NotRequired[CredentialProviderUnionTypeDef]

class HarnessAgentCoreGatewayConfigTypeDef(TypedDict):
    gatewayArn: str
    outboundAuth: NotRequired[HarnessGatewayOutboundAuthUnionTypeDef]

class AuthorizerConfigurationOutputTypeDef(TypedDict):
    customJWTAuthorizer: NotRequired[CustomJWTAuthorizerConfigurationOutputTypeDef]

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
MetadataSchemaEntryOutputTypeDef = TypedDict(
    "MetadataSchemaEntryOutputTypeDef",
    {
        "key": str,
        "type": NotRequired[MetadataValueTypeType],
        "extractionConfig": NotRequired[ExtractionConfigOutputTypeDef],
    },
)

class LlmExtractionConfigTypeDef(TypedDict):
    definition: str
    llmExtractionInstruction: NotRequired[str]
    validation: NotRequired[ValidationUnionTypeDef]

class RouteToTargetActionTypeDef(TypedDict):
    staticRoute: NotRequired[StaticRouteTypeDef]
    weightedRoute: NotRequired[WeightedRouteUnionTypeDef]

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
    kmsKeyArn: str
    ResponseMetadata: ResponseMetadataTypeDef

EvaluatorConfigUnionTypeDef = Union[EvaluatorConfigTypeDef, EvaluatorConfigOutputTypeDef]

class HarnessEnvironmentProviderRequestTypeDef(TypedDict):
    agentCoreRuntimeEnvironment: NotRequired[HarnessAgentCoreRuntimeEnvironmentRequestTypeDef]

CustomClaimValidationTypeUnionTypeDef = Union[
    CustomClaimValidationTypeTypeDef, CustomClaimValidationTypeOutputTypeDef
]

class CreateGatewayRuleResponseTypeDef(TypedDict):
    ruleId: str
    gatewayArn: str
    priority: int
    conditions: list[ConditionOutputTypeDef]
    actions: list[ActionOutputTypeDef]
    description: str
    createdAt: datetime
    status: GatewayRuleStatusType
    system: SystemManagedBlockTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GatewayRuleDetailTypeDef(TypedDict):
    ruleId: str
    gatewayArn: str
    priority: int
    actions: list[ActionOutputTypeDef]
    createdAt: datetime
    status: GatewayRuleStatusType
    conditions: NotRequired[list[ConditionOutputTypeDef]]
    description: NotRequired[str]
    system: NotRequired[SystemManagedBlockTypeDef]
    updatedAt: NotRequired[datetime]

class GetGatewayRuleResponseTypeDef(TypedDict):
    ruleId: str
    gatewayArn: str
    priority: int
    conditions: list[ConditionOutputTypeDef]
    actions: list[ActionOutputTypeDef]
    description: str
    createdAt: datetime
    status: GatewayRuleStatusType
    system: SystemManagedBlockTypeDef
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateGatewayRuleResponseTypeDef(TypedDict):
    ruleId: str
    gatewayArn: str
    priority: int
    conditions: list[ConditionOutputTypeDef]
    actions: list[ActionOutputTypeDef]
    description: str
    createdAt: datetime
    status: GatewayRuleStatusType
    system: SystemManagedBlockTypeDef
    updatedAt: datetime
    ResponseMetadata: ResponseMetadataTypeDef

class ConfigurationBundleActionTypeDef(TypedDict):
    staticOverride: NotRequired[StaticOverrideTypeDef]
    weightedOverride: NotRequired[WeightedOverrideUnionTypeDef]

class UpdatedHarnessMemoryConfigurationTypeDef(TypedDict):
    optionalValue: NotRequired[HarnessMemoryConfigurationUnionTypeDef]

ConditionUnionTypeDef = Union[ConditionTypeDef, ConditionOutputTypeDef]
PrivateEndpointOverrideUnionTypeDef = Union[
    PrivateEndpointOverrideTypeDef, PrivateEndpointOverrideOutputTypeDef
]

class UpdatedDescriptorsTypeDef(TypedDict):
    optionalValue: NotRequired[UpdatedDescriptorsUnionTypeDef]

CredentialProviderConfigurationUnionTypeDef = Union[
    CredentialProviderConfigurationTypeDef, CredentialProviderConfigurationOutputTypeDef
]
HarnessAgentCoreGatewayConfigUnionTypeDef = Union[
    HarnessAgentCoreGatewayConfigTypeDef, HarnessAgentCoreGatewayConfigOutputTypeDef
]

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

class CreatePaymentManagerResponseTypeDef(TypedDict):
    paymentManagerArn: str
    paymentManagerId: str
    name: str
    authorizerType: PaymentsAuthorizerTypeType
    authorizerConfiguration: AuthorizerConfigurationOutputTypeDef
    roleArn: str
    workloadIdentityDetails: WorkloadIdentityDetailsTypeDef
    createdAt: datetime
    status: PaymentManagerStatusType
    tags: dict[str, str]
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

class GetPaymentManagerResponseTypeDef(TypedDict):
    paymentManagerArn: str
    paymentManagerId: str
    name: str
    description: str
    authorizerType: PaymentsAuthorizerTypeType
    authorizerConfiguration: AuthorizerConfigurationOutputTypeDef
    roleArn: str
    workloadIdentityDetails: WorkloadIdentityDetailsTypeDef
    createdAt: datetime
    lastUpdatedAt: datetime
    status: PaymentManagerStatusType
    tags: dict[str, str]
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

class HarnessTypeDef(TypedDict):
    harnessId: str
    harnessName: str
    arn: str
    status: HarnessStatusType
    executionRoleArn: str
    createdAt: datetime
    updatedAt: datetime
    model: HarnessModelConfigurationTypeDef
    systemPrompt: list[HarnessSystemContentBlockTypeDef]
    tools: list[HarnessToolOutputTypeDef]
    skills: list[HarnessSkillTypeDef]
    allowedTools: list[str]
    truncation: HarnessTruncationConfigurationTypeDef
    environment: HarnessEnvironmentProviderTypeDef
    environmentArtifact: NotRequired[HarnessEnvironmentArtifactTypeDef]
    environmentVariables: NotRequired[dict[str, str]]
    authorizerConfiguration: NotRequired[AuthorizerConfigurationOutputTypeDef]
    memory: NotRequired[HarnessMemoryConfigurationOutputTypeDef]
    maxIterations: NotRequired[int]
    maxTokens: NotRequired[int]
    timeoutSeconds: NotRequired[int]
    failureReason: NotRequired[str]

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

class CreateOauth2CredentialProviderResponseTypeDef(TypedDict):
    clientSecretArn: SecretTypeDef
    name: str
    credentialProviderArn: str
    callbackUrl: str
    oauth2ProviderConfigOutput: Oauth2ProviderConfigOutputTypeDef
    status: StatusType
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
    status: StatusType
    failureReason: str
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
    status: StatusType
    ResponseMetadata: ResponseMetadataTypeDef

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
    http: NotRequired[HttpTargetConfigurationTypeDef]

class TargetConfigurationTypeDef(TypedDict):
    mcp: NotRequired[McpTargetConfigurationTypeDef]
    http: NotRequired[HttpTargetConfigurationTypeDef]

class MemoryRecordSchemaOutputTypeDef(TypedDict):
    metadataSchema: NotRequired[list[MetadataSchemaEntryOutputTypeDef]]

LlmExtractionConfigUnionTypeDef = Union[
    LlmExtractionConfigTypeDef, LlmExtractionConfigOutputTypeDef
]
RouteToTargetActionUnionTypeDef = Union[
    RouteToTargetActionTypeDef, RouteToTargetActionOutputTypeDef
]

class CreateEvaluatorRequestTypeDef(TypedDict):
    evaluatorName: str
    evaluatorConfig: EvaluatorConfigUnionTypeDef
    level: EvaluatorLevelType
    clientToken: NotRequired[str]
    description: NotRequired[str]
    kmsKeyArn: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]

class UpdateEvaluatorRequestTypeDef(TypedDict):
    evaluatorId: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    evaluatorConfig: NotRequired[EvaluatorConfigUnionTypeDef]
    level: NotRequired[EvaluatorLevelType]
    kmsKeyArn: NotRequired[str]

class ListGatewayRulesResponseTypeDef(TypedDict):
    gatewayRules: list[GatewayRuleDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]

ConfigurationBundleActionUnionTypeDef = Union[
    ConfigurationBundleActionTypeDef, ConfigurationBundleActionOutputTypeDef
]

class CustomJWTAuthorizerConfigurationTypeDef(TypedDict):
    discoveryUrl: str
    allowedAudience: NotRequired[Sequence[str]]
    allowedClients: NotRequired[Sequence[str]]
    allowedScopes: NotRequired[Sequence[str]]
    customClaims: NotRequired[Sequence[CustomClaimValidationTypeUnionTypeDef]]
    privateEndpoint: NotRequired[PrivateEndpointUnionTypeDef]
    privateEndpointOverrides: NotRequired[Sequence[PrivateEndpointOverrideUnionTypeDef]]

class CustomOauth2ProviderConfigInputTypeDef(TypedDict):
    oauthDiscovery: Oauth2DiscoveryUnionTypeDef
    clientId: NotRequired[str]
    clientSecret: NotRequired[str]
    privateEndpoint: NotRequired[PrivateEndpointUnionTypeDef]
    privateEndpointOverrides: NotRequired[Sequence[PrivateEndpointOverrideUnionTypeDef]]
    onBehalfOfTokenExchangeConfig: NotRequired[OnBehalfOfTokenExchangeConfigTypeUnionTypeDef]
    clientAuthenticationMethod: NotRequired[ClientAuthenticationMethodTypeType]

class HarnessToolConfigurationTypeDef(TypedDict):
    remoteMcp: NotRequired[HarnessRemoteMcpConfigUnionTypeDef]
    agentCoreBrowser: NotRequired[HarnessAgentCoreBrowserConfigTypeDef]
    agentCoreGateway: NotRequired[HarnessAgentCoreGatewayConfigUnionTypeDef]
    inlineFunction: NotRequired[HarnessInlineFunctionConfigUnionTypeDef]
    agentCoreCodeInterpreter: NotRequired[HarnessAgentCoreCodeInterpreterConfigTypeDef]

class CreateHarnessResponseTypeDef(TypedDict):
    harness: HarnessTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class DeleteHarnessResponseTypeDef(TypedDict):
    harness: HarnessTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetHarnessResponseTypeDef(TypedDict):
    harness: HarnessTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateHarnessResponseTypeDef(TypedDict):
    harness: HarnessTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

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
    protocolType: TargetProtocolTypeType
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
    protocolType: NotRequired[TargetProtocolTypeType]

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
    protocolType: TargetProtocolTypeType
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
    protocolType: TargetProtocolTypeType
    ResponseMetadata: ResponseMetadataTypeDef

TargetConfigurationUnionTypeDef = Union[
    TargetConfigurationTypeDef, TargetConfigurationOutputTypeDef
]

class EpisodicReflectionConfigurationTypeDef(TypedDict):
    namespaces: NotRequired[list[str]]
    namespaceTemplates: NotRequired[list[str]]
    memoryRecordSchema: NotRequired[MemoryRecordSchemaOutputTypeDef]

class EpisodicReflectionOverrideTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str
    namespaces: NotRequired[list[str]]
    namespaceTemplates: NotRequired[list[str]]
    memoryRecordSchema: NotRequired[MemoryRecordSchemaOutputTypeDef]

class ExtractionConfigTypeDef(TypedDict):
    llmExtractionConfig: NotRequired[LlmExtractionConfigUnionTypeDef]

class ActionTypeDef(TypedDict):
    configurationBundle: NotRequired[ConfigurationBundleActionUnionTypeDef]
    routeToTarget: NotRequired[RouteToTargetActionUnionTypeDef]

CustomJWTAuthorizerConfigurationUnionTypeDef = Union[
    CustomJWTAuthorizerConfigurationTypeDef, CustomJWTAuthorizerConfigurationOutputTypeDef
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

HarnessToolConfigurationUnionTypeDef = Union[
    HarnessToolConfigurationTypeDef, HarnessToolConfigurationOutputTypeDef
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

class CustomReflectionConfigurationTypeDef(TypedDict):
    episodicReflectionOverride: NotRequired[EpisodicReflectionOverrideTypeDef]

ExtractionConfigUnionTypeDef = Union[ExtractionConfigTypeDef, ExtractionConfigOutputTypeDef]
ActionUnionTypeDef = Union[ActionTypeDef, ActionOutputTypeDef]

class AuthorizerConfigurationTypeDef(TypedDict):
    customJWTAuthorizer: NotRequired[CustomJWTAuthorizerConfigurationUnionTypeDef]

class CreateOauth2CredentialProviderRequestTypeDef(TypedDict):
    name: str
    credentialProviderVendor: CredentialProviderVendorTypeType
    oauth2ProviderConfigInput: Oauth2ProviderConfigInputTypeDef
    tags: NotRequired[Mapping[str, str]]

class UpdateOauth2CredentialProviderRequestTypeDef(TypedDict):
    name: str
    credentialProviderVendor: CredentialProviderVendorTypeType
    oauth2ProviderConfigInput: Oauth2ProviderConfigInputTypeDef

HarnessToolTypeDef = TypedDict(
    "HarnessToolTypeDef",
    {
        "type": HarnessToolTypeType,
        "name": NotRequired[str],
        "config": NotRequired[HarnessToolConfigurationUnionTypeDef],
    },
)

class SynchronizationConfigurationTypeDef(TypedDict):
    fromUrl: NotRequired[FromUrlSynchronizationConfigurationUnionTypeDef]

class ReflectionConfigurationTypeDef(TypedDict):
    customReflectionConfiguration: NotRequired[CustomReflectionConfigurationTypeDef]
    episodicReflectionConfiguration: NotRequired[EpisodicReflectionConfigurationTypeDef]

MetadataSchemaEntryTypeDef = TypedDict(
    "MetadataSchemaEntryTypeDef",
    {
        "key": str,
        "type": NotRequired[MetadataValueTypeType],
        "extractionConfig": NotRequired[ExtractionConfigUnionTypeDef],
    },
)

class CreateGatewayRuleRequestTypeDef(TypedDict):
    gatewayIdentifier: str
    priority: int
    actions: Sequence[ActionUnionTypeDef]
    clientToken: NotRequired[str]
    conditions: NotRequired[Sequence[ConditionUnionTypeDef]]
    description: NotRequired[str]

class UpdateGatewayRuleRequestTypeDef(TypedDict):
    gatewayIdentifier: str
    ruleId: str
    priority: NotRequired[int]
    conditions: NotRequired[Sequence[ConditionUnionTypeDef]]
    actions: NotRequired[Sequence[ActionUnionTypeDef]]
    description: NotRequired[str]

AuthorizerConfigurationUnionTypeDef = Union[
    AuthorizerConfigurationTypeDef, AuthorizerConfigurationOutputTypeDef
]
HarnessToolUnionTypeDef = Union[HarnessToolTypeDef, HarnessToolOutputTypeDef]
SynchronizationConfigurationUnionTypeDef = Union[
    SynchronizationConfigurationTypeDef, SynchronizationConfigurationOutputTypeDef
]
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
MetadataSchemaEntryUnionTypeDef = Union[
    MetadataSchemaEntryTypeDef, MetadataSchemaEntryOutputTypeDef
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
    authorizerType: AuthorizerTypeType
    description: NotRequired[str]
    clientToken: NotRequired[str]
    protocolType: NotRequired[Literal["MCP"]]
    protocolConfiguration: NotRequired[GatewayProtocolConfigurationUnionTypeDef]
    authorizerConfiguration: NotRequired[AuthorizerConfigurationUnionTypeDef]
    kmsKeyArn: NotRequired[str]
    interceptorConfigurations: NotRequired[Sequence[GatewayInterceptorConfigurationUnionTypeDef]]
    policyEngineConfiguration: NotRequired[GatewayPolicyEngineConfigurationTypeDef]
    exceptionLevel: NotRequired[Literal["DEBUG"]]
    tags: NotRequired[Mapping[str, str]]

class CreatePaymentManagerRequestTypeDef(TypedDict):
    name: str
    authorizerType: PaymentsAuthorizerTypeType
    roleArn: str
    description: NotRequired[str]
    authorizerConfiguration: NotRequired[AuthorizerConfigurationUnionTypeDef]
    clientToken: NotRequired[str]
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
    authorizerType: AuthorizerTypeType
    description: NotRequired[str]
    protocolType: NotRequired[Literal["MCP"]]
    protocolConfiguration: NotRequired[GatewayProtocolConfigurationUnionTypeDef]
    authorizerConfiguration: NotRequired[AuthorizerConfigurationUnionTypeDef]
    kmsKeyArn: NotRequired[str]
    interceptorConfigurations: NotRequired[Sequence[GatewayInterceptorConfigurationUnionTypeDef]]
    policyEngineConfiguration: NotRequired[GatewayPolicyEngineConfigurationTypeDef]
    exceptionLevel: NotRequired[Literal["DEBUG"]]

class UpdatePaymentManagerRequestTypeDef(TypedDict):
    paymentManagerId: str
    description: NotRequired[str]
    authorizerType: NotRequired[PaymentsAuthorizerTypeType]
    authorizerConfiguration: NotRequired[AuthorizerConfigurationUnionTypeDef]
    roleArn: NotRequired[str]
    clientToken: NotRequired[str]

class UpdatedAuthorizerConfigurationTypeDef(TypedDict):
    optionalValue: NotRequired[AuthorizerConfigurationUnionTypeDef]

class CreateHarnessRequestTypeDef(TypedDict):
    harnessName: str
    executionRoleArn: str
    clientToken: NotRequired[str]
    environment: NotRequired[HarnessEnvironmentProviderRequestTypeDef]
    environmentArtifact: NotRequired[HarnessEnvironmentArtifactTypeDef]
    environmentVariables: NotRequired[Mapping[str, str]]
    authorizerConfiguration: NotRequired[AuthorizerConfigurationUnionTypeDef]
    model: NotRequired[HarnessModelConfigurationTypeDef]
    systemPrompt: NotRequired[Sequence[HarnessSystemContentBlockTypeDef]]
    tools: NotRequired[Sequence[HarnessToolUnionTypeDef]]
    skills: NotRequired[Sequence[HarnessSkillTypeDef]]
    allowedTools: NotRequired[Sequence[str]]
    memory: NotRequired[HarnessMemoryConfigurationUnionTypeDef]
    truncation: NotRequired[HarnessTruncationConfigurationTypeDef]
    maxIterations: NotRequired[int]
    maxTokens: NotRequired[int]
    timeoutSeconds: NotRequired[int]
    tags: NotRequired[Mapping[str, str]]

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
        "memoryRecordSchema": NotRequired[MemoryRecordSchemaOutputTypeDef],
    },
)

class MemoryRecordSchemaTypeDef(TypedDict):
    metadataSchema: NotRequired[Sequence[MetadataSchemaEntryUnionTypeDef]]

class UpdateHarnessRequestTypeDef(TypedDict):
    harnessId: str
    clientToken: NotRequired[str]
    executionRoleArn: NotRequired[str]
    environment: NotRequired[HarnessEnvironmentProviderRequestTypeDef]
    environmentArtifact: NotRequired[UpdatedHarnessEnvironmentArtifactTypeDef]
    environmentVariables: NotRequired[Mapping[str, str]]
    authorizerConfiguration: NotRequired[UpdatedAuthorizerConfigurationTypeDef]
    model: NotRequired[HarnessModelConfigurationTypeDef]
    systemPrompt: NotRequired[Sequence[HarnessSystemContentBlockTypeDef]]
    tools: NotRequired[Sequence[HarnessToolUnionTypeDef]]
    skills: NotRequired[Sequence[HarnessSkillTypeDef]]
    allowedTools: NotRequired[Sequence[str]]
    memory: NotRequired[UpdatedHarnessMemoryConfigurationTypeDef]
    truncation: NotRequired[HarnessTruncationConfigurationTypeDef]
    maxIterations: NotRequired[int]
    maxTokens: NotRequired[int]
    timeoutSeconds: NotRequired[int]

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
        "indexedKeys": NotRequired[list[IndexedKeyTypeDef]],
        "streamDeliveryResources": NotRequired[StreamDeliveryResourcesOutputTypeDef],
    },
)
MemoryRecordSchemaUnionTypeDef = Union[MemoryRecordSchemaTypeDef, MemoryRecordSchemaOutputTypeDef]

class CreateMemoryOutputTypeDef(TypedDict):
    memory: MemoryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class GetMemoryOutputTypeDef(TypedDict):
    memory: MemoryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class UpdateMemoryOutputTypeDef(TypedDict):
    memory: MemoryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef

class EpisodicOverrideReflectionConfigurationInputTypeDef(TypedDict):
    appendToPrompt: str
    modelId: str
    namespaces: NotRequired[Sequence[str]]
    namespaceTemplates: NotRequired[Sequence[str]]
    memoryRecordSchema: NotRequired[MemoryRecordSchemaUnionTypeDef]

class EpisodicReflectionConfigurationInputTypeDef(TypedDict):
    namespaces: NotRequired[Sequence[str]]
    namespaceTemplates: NotRequired[Sequence[str]]
    memoryRecordSchema: NotRequired[MemoryRecordSchemaUnionTypeDef]

class SemanticMemoryStrategyInputTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    namespaces: NotRequired[Sequence[str]]
    namespaceTemplates: NotRequired[Sequence[str]]
    memoryRecordSchema: NotRequired[MemoryRecordSchemaUnionTypeDef]

class SummaryMemoryStrategyInputTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    namespaces: NotRequired[Sequence[str]]
    namespaceTemplates: NotRequired[Sequence[str]]
    memoryRecordSchema: NotRequired[MemoryRecordSchemaUnionTypeDef]

class UserPreferenceMemoryStrategyInputTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    namespaces: NotRequired[Sequence[str]]
    namespaceTemplates: NotRequired[Sequence[str]]
    memoryRecordSchema: NotRequired[MemoryRecordSchemaUnionTypeDef]

class CustomReflectionConfigurationInputTypeDef(TypedDict):
    episodicReflectionOverride: NotRequired[EpisodicOverrideReflectionConfigurationInputTypeDef]

class EpisodicOverrideConfigurationInputTypeDef(TypedDict):
    extraction: NotRequired[EpisodicOverrideExtractionConfigurationInputTypeDef]
    consolidation: NotRequired[EpisodicOverrideConsolidationConfigurationInputTypeDef]
    reflection: NotRequired[EpisodicOverrideReflectionConfigurationInputTypeDef]

class EpisodicMemoryStrategyInputTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    namespaces: NotRequired[Sequence[str]]
    namespaceTemplates: NotRequired[Sequence[str]]
    reflectionConfiguration: NotRequired[EpisodicReflectionConfigurationInputTypeDef]
    memoryRecordSchema: NotRequired[MemoryRecordSchemaUnionTypeDef]

class ModifyReflectionConfigurationTypeDef(TypedDict):
    episodicReflectionConfiguration: NotRequired[EpisodicReflectionConfigurationInputTypeDef]
    customReflectionConfiguration: NotRequired[CustomReflectionConfigurationInputTypeDef]

class CustomConfigurationInputTypeDef(TypedDict):
    semanticOverride: NotRequired[SemanticOverrideConfigurationInputTypeDef]
    summaryOverride: NotRequired[SummaryOverrideConfigurationInputTypeDef]
    userPreferenceOverride: NotRequired[UserPreferenceOverrideConfigurationInputTypeDef]
    episodicOverride: NotRequired[EpisodicOverrideConfigurationInputTypeDef]
    selfManagedConfiguration: NotRequired[SelfManagedConfigurationInputTypeDef]

class ModifyStrategyConfigurationTypeDef(TypedDict):
    extraction: NotRequired[ModifyExtractionConfigurationTypeDef]
    consolidation: NotRequired[ModifyConsolidationConfigurationTypeDef]
    reflection: NotRequired[ModifyReflectionConfigurationTypeDef]
    selfManagedConfiguration: NotRequired[ModifySelfManagedConfigurationTypeDef]

class CustomMemoryStrategyInputTypeDef(TypedDict):
    name: str
    description: NotRequired[str]
    namespaces: NotRequired[Sequence[str]]
    namespaceTemplates: NotRequired[Sequence[str]]
    configuration: NotRequired[CustomConfigurationInputTypeDef]
    memoryRecordSchema: NotRequired[MemoryRecordSchemaUnionTypeDef]

class ModifyMemoryStrategyInputTypeDef(TypedDict):
    memoryStrategyId: str
    description: NotRequired[str]
    namespaces: NotRequired[Sequence[str]]
    namespaceTemplates: NotRequired[Sequence[str]]
    configuration: NotRequired[ModifyStrategyConfigurationTypeDef]
    memoryRecordSchema: NotRequired[MemoryRecordSchemaUnionTypeDef]

class MemoryStrategyInputTypeDef(TypedDict):
    semanticMemoryStrategy: NotRequired[SemanticMemoryStrategyInputTypeDef]
    summaryMemoryStrategy: NotRequired[SummaryMemoryStrategyInputTypeDef]
    userPreferenceMemoryStrategy: NotRequired[UserPreferenceMemoryStrategyInputTypeDef]
    customMemoryStrategy: NotRequired[CustomMemoryStrategyInputTypeDef]
    episodicMemoryStrategy: NotRequired[EpisodicMemoryStrategyInputTypeDef]

class CreateMemoryInputTypeDef(TypedDict):
    name: str
    eventExpiryDuration: int
    clientToken: NotRequired[str]
    description: NotRequired[str]
    encryptionKeyArn: NotRequired[str]
    memoryExecutionRoleArn: NotRequired[str]
    memoryStrategies: NotRequired[Sequence[MemoryStrategyInputTypeDef]]
    indexedKeys: NotRequired[Sequence[IndexedKeyTypeDef]]
    streamDeliveryResources: NotRequired[StreamDeliveryResourcesUnionTypeDef]
    tags: NotRequired[Mapping[str, str]]

class ModifyMemoryStrategiesTypeDef(TypedDict):
    addMemoryStrategies: NotRequired[Sequence[MemoryStrategyInputTypeDef]]
    modifyMemoryStrategies: NotRequired[Sequence[ModifyMemoryStrategyInputTypeDef]]
    deleteMemoryStrategies: NotRequired[Sequence[DeleteMemoryStrategyInputTypeDef]]

class UpdateMemoryInputTypeDef(TypedDict):
    memoryId: str
    clientToken: NotRequired[str]
    description: NotRequired[str]
    eventExpiryDuration: NotRequired[int]
    memoryExecutionRoleArn: NotRequired[str]
    memoryStrategies: NotRequired[ModifyMemoryStrategiesTypeDef]
    addIndexedKeys: NotRequired[Sequence[IndexedKeyTypeDef]]
    streamDeliveryResources: NotRequired[StreamDeliveryResourcesUnionTypeDef]
