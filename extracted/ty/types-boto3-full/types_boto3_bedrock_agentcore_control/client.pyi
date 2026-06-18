"""
Type annotations for bedrock-agentcore-control service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_bedrock_agentcore_control.client import BedrockAgentCoreControlClient

    session = Session()
    client: BedrockAgentCoreControlClient = session.client("bedrock-agentcore-control")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListAgentRuntimeEndpointsPaginator,
    ListAgentRuntimesPaginator,
    ListAgentRuntimeVersionsPaginator,
    ListApiKeyCredentialProvidersPaginator,
    ListBrowserProfilesPaginator,
    ListBrowsersPaginator,
    ListCodeInterpretersPaginator,
    ListConfigurationBundlesPaginator,
    ListConfigurationBundleVersionsPaginator,
    ListDatasetExamplesPaginator,
    ListDatasetsPaginator,
    ListDatasetVersionsPaginator,
    ListEvaluatorsPaginator,
    ListGatewayRulesPaginator,
    ListGatewaysPaginator,
    ListGatewayTargetsPaginator,
    ListHarnessEndpointsPaginator,
    ListHarnessesPaginator,
    ListHarnessVersionsPaginator,
    ListMemoriesPaginator,
    ListOauth2CredentialProvidersPaginator,
    ListOnlineEvaluationConfigsPaginator,
    ListPaymentConnectorsPaginator,
    ListPaymentCredentialProvidersPaginator,
    ListPaymentManagersPaginator,
    ListPoliciesPaginator,
    ListPolicyEnginesPaginator,
    ListPolicyEngineSummariesPaginator,
    ListPolicyGenerationAssetsPaginator,
    ListPolicyGenerationsPaginator,
    ListPolicyGenerationSummariesPaginator,
    ListPolicySummariesPaginator,
    ListRegistriesPaginator,
    ListRegistryRecordsPaginator,
    ListWorkloadIdentitiesPaginator,
)
from .type_defs import (
    AddDatasetExamplesRequestTypeDef,
    AddDatasetExamplesResponseTypeDef,
    CreateAgentRuntimeEndpointRequestTypeDef,
    CreateAgentRuntimeEndpointResponseTypeDef,
    CreateAgentRuntimeRequestTypeDef,
    CreateAgentRuntimeResponseTypeDef,
    CreateApiKeyCredentialProviderRequestTypeDef,
    CreateApiKeyCredentialProviderResponseTypeDef,
    CreateBrowserProfileRequestTypeDef,
    CreateBrowserProfileResponseTypeDef,
    CreateBrowserRequestTypeDef,
    CreateBrowserResponseTypeDef,
    CreateCodeInterpreterRequestTypeDef,
    CreateCodeInterpreterResponseTypeDef,
    CreateConfigurationBundleRequestTypeDef,
    CreateConfigurationBundleResponseTypeDef,
    CreateDatasetRequestTypeDef,
    CreateDatasetResponseTypeDef,
    CreateDatasetVersionRequestTypeDef,
    CreateDatasetVersionResponseTypeDef,
    CreateEvaluatorRequestTypeDef,
    CreateEvaluatorResponseTypeDef,
    CreateGatewayRequestTypeDef,
    CreateGatewayResponseTypeDef,
    CreateGatewayRuleRequestTypeDef,
    CreateGatewayRuleResponseTypeDef,
    CreateGatewayTargetRequestTypeDef,
    CreateGatewayTargetResponseTypeDef,
    CreateHarnessEndpointRequestTypeDef,
    CreateHarnessEndpointResponseTypeDef,
    CreateHarnessRequestTypeDef,
    CreateHarnessResponseTypeDef,
    CreateMemoryInputTypeDef,
    CreateMemoryOutputTypeDef,
    CreateOauth2CredentialProviderRequestTypeDef,
    CreateOauth2CredentialProviderResponseTypeDef,
    CreateOnlineEvaluationConfigRequestTypeDef,
    CreateOnlineEvaluationConfigResponseTypeDef,
    CreatePaymentConnectorRequestTypeDef,
    CreatePaymentConnectorResponseTypeDef,
    CreatePaymentCredentialProviderRequestTypeDef,
    CreatePaymentCredentialProviderResponseTypeDef,
    CreatePaymentManagerRequestTypeDef,
    CreatePaymentManagerResponseTypeDef,
    CreatePolicyEngineRequestTypeDef,
    CreatePolicyEngineResponseTypeDef,
    CreatePolicyRequestTypeDef,
    CreatePolicyResponseTypeDef,
    CreateRegistryRecordRequestTypeDef,
    CreateRegistryRecordResponseTypeDef,
    CreateRegistryRequestTypeDef,
    CreateRegistryResponseTypeDef,
    CreateWorkloadIdentityRequestTypeDef,
    CreateWorkloadIdentityResponseTypeDef,
    DeleteAgentRuntimeEndpointRequestTypeDef,
    DeleteAgentRuntimeEndpointResponseTypeDef,
    DeleteAgentRuntimeRequestTypeDef,
    DeleteAgentRuntimeResponseTypeDef,
    DeleteApiKeyCredentialProviderRequestTypeDef,
    DeleteBrowserProfileRequestTypeDef,
    DeleteBrowserProfileResponseTypeDef,
    DeleteBrowserRequestTypeDef,
    DeleteBrowserResponseTypeDef,
    DeleteCodeInterpreterRequestTypeDef,
    DeleteCodeInterpreterResponseTypeDef,
    DeleteConfigurationBundleRequestTypeDef,
    DeleteConfigurationBundleResponseTypeDef,
    DeleteDatasetExamplesRequestTypeDef,
    DeleteDatasetExamplesResponseTypeDef,
    DeleteDatasetRequestTypeDef,
    DeleteDatasetResponseTypeDef,
    DeleteEvaluatorRequestTypeDef,
    DeleteEvaluatorResponseTypeDef,
    DeleteGatewayRequestTypeDef,
    DeleteGatewayResponseTypeDef,
    DeleteGatewayRuleRequestTypeDef,
    DeleteGatewayRuleResponseTypeDef,
    DeleteGatewayTargetRequestTypeDef,
    DeleteGatewayTargetResponseTypeDef,
    DeleteHarnessEndpointRequestTypeDef,
    DeleteHarnessEndpointResponseTypeDef,
    DeleteHarnessRequestTypeDef,
    DeleteHarnessResponseTypeDef,
    DeleteMemoryInputTypeDef,
    DeleteMemoryOutputTypeDef,
    DeleteOauth2CredentialProviderRequestTypeDef,
    DeleteOnlineEvaluationConfigRequestTypeDef,
    DeleteOnlineEvaluationConfigResponseTypeDef,
    DeletePaymentConnectorRequestTypeDef,
    DeletePaymentConnectorResponseTypeDef,
    DeletePaymentCredentialProviderRequestTypeDef,
    DeletePaymentManagerRequestTypeDef,
    DeletePaymentManagerResponseTypeDef,
    DeletePolicyEngineRequestTypeDef,
    DeletePolicyEngineResponseTypeDef,
    DeletePolicyRequestTypeDef,
    DeletePolicyResponseTypeDef,
    DeleteRegistryRecordRequestTypeDef,
    DeleteRegistryRequestTypeDef,
    DeleteRegistryResponseTypeDef,
    DeleteResourcePolicyRequestTypeDef,
    DeleteWorkloadIdentityRequestTypeDef,
    GetAgentRuntimeEndpointRequestTypeDef,
    GetAgentRuntimeEndpointResponseTypeDef,
    GetAgentRuntimeRequestTypeDef,
    GetAgentRuntimeResponseTypeDef,
    GetApiKeyCredentialProviderRequestTypeDef,
    GetApiKeyCredentialProviderResponseTypeDef,
    GetBrowserProfileRequestTypeDef,
    GetBrowserProfileResponseTypeDef,
    GetBrowserRequestTypeDef,
    GetBrowserResponseTypeDef,
    GetCodeInterpreterRequestTypeDef,
    GetCodeInterpreterResponseTypeDef,
    GetConfigurationBundleRequestTypeDef,
    GetConfigurationBundleResponseTypeDef,
    GetConfigurationBundleVersionRequestTypeDef,
    GetConfigurationBundleVersionResponseTypeDef,
    GetDatasetRequestTypeDef,
    GetDatasetResponseTypeDef,
    GetEvaluatorRequestTypeDef,
    GetEvaluatorResponseTypeDef,
    GetGatewayRequestTypeDef,
    GetGatewayResponseTypeDef,
    GetGatewayRuleRequestTypeDef,
    GetGatewayRuleResponseTypeDef,
    GetGatewayTargetRequestTypeDef,
    GetGatewayTargetResponseTypeDef,
    GetHarnessEndpointRequestTypeDef,
    GetHarnessEndpointResponseTypeDef,
    GetHarnessRequestTypeDef,
    GetHarnessResponseTypeDef,
    GetMemoryInputTypeDef,
    GetMemoryOutputTypeDef,
    GetOauth2CredentialProviderRequestTypeDef,
    GetOauth2CredentialProviderResponseTypeDef,
    GetOnlineEvaluationConfigRequestTypeDef,
    GetOnlineEvaluationConfigResponseTypeDef,
    GetPaymentConnectorRequestTypeDef,
    GetPaymentConnectorResponseTypeDef,
    GetPaymentCredentialProviderRequestTypeDef,
    GetPaymentCredentialProviderResponseTypeDef,
    GetPaymentManagerRequestTypeDef,
    GetPaymentManagerResponseTypeDef,
    GetPolicyEngineRequestTypeDef,
    GetPolicyEngineResponseTypeDef,
    GetPolicyEngineSummaryRequestTypeDef,
    GetPolicyEngineSummaryResponseTypeDef,
    GetPolicyGenerationRequestTypeDef,
    GetPolicyGenerationResponseTypeDef,
    GetPolicyGenerationSummaryRequestTypeDef,
    GetPolicyGenerationSummaryResponseTypeDef,
    GetPolicyRequestTypeDef,
    GetPolicyResponseTypeDef,
    GetPolicySummaryRequestTypeDef,
    GetPolicySummaryResponseTypeDef,
    GetRegistryRecordRequestTypeDef,
    GetRegistryRecordResponseTypeDef,
    GetRegistryRequestTypeDef,
    GetRegistryResponseTypeDef,
    GetResourcePolicyRequestTypeDef,
    GetResourcePolicyResponseTypeDef,
    GetTokenVaultRequestTypeDef,
    GetTokenVaultResponseTypeDef,
    GetWorkloadIdentityRequestTypeDef,
    GetWorkloadIdentityResponseTypeDef,
    ListAgentRuntimeEndpointsRequestTypeDef,
    ListAgentRuntimeEndpointsResponseTypeDef,
    ListAgentRuntimesRequestTypeDef,
    ListAgentRuntimesResponseTypeDef,
    ListAgentRuntimeVersionsRequestTypeDef,
    ListAgentRuntimeVersionsResponseTypeDef,
    ListApiKeyCredentialProvidersRequestTypeDef,
    ListApiKeyCredentialProvidersResponseTypeDef,
    ListBrowserProfilesRequestTypeDef,
    ListBrowserProfilesResponseTypeDef,
    ListBrowsersRequestTypeDef,
    ListBrowsersResponseTypeDef,
    ListCodeInterpretersRequestTypeDef,
    ListCodeInterpretersResponseTypeDef,
    ListConfigurationBundlesRequestTypeDef,
    ListConfigurationBundlesResponseTypeDef,
    ListConfigurationBundleVersionsRequestTypeDef,
    ListConfigurationBundleVersionsResponseTypeDef,
    ListDatasetExamplesRequestTypeDef,
    ListDatasetExamplesResponseTypeDef,
    ListDatasetsRequestTypeDef,
    ListDatasetsResponseTypeDef,
    ListDatasetVersionsRequestTypeDef,
    ListDatasetVersionsResponseTypeDef,
    ListEvaluatorsRequestTypeDef,
    ListEvaluatorsResponseTypeDef,
    ListGatewayRulesRequestTypeDef,
    ListGatewayRulesResponseTypeDef,
    ListGatewaysRequestTypeDef,
    ListGatewaysResponseTypeDef,
    ListGatewayTargetsRequestTypeDef,
    ListGatewayTargetsResponseTypeDef,
    ListHarnessEndpointsRequestTypeDef,
    ListHarnessEndpointsResponseTypeDef,
    ListHarnessesRequestTypeDef,
    ListHarnessesResponseTypeDef,
    ListHarnessVersionsRequestTypeDef,
    ListHarnessVersionsResponseTypeDef,
    ListMemoriesInputTypeDef,
    ListMemoriesOutputTypeDef,
    ListOauth2CredentialProvidersRequestTypeDef,
    ListOauth2CredentialProvidersResponseTypeDef,
    ListOnlineEvaluationConfigsRequestTypeDef,
    ListOnlineEvaluationConfigsResponseTypeDef,
    ListPaymentConnectorsRequestTypeDef,
    ListPaymentConnectorsResponseTypeDef,
    ListPaymentCredentialProvidersRequestTypeDef,
    ListPaymentCredentialProvidersResponseTypeDef,
    ListPaymentManagersRequestTypeDef,
    ListPaymentManagersResponseTypeDef,
    ListPoliciesRequestTypeDef,
    ListPoliciesResponseTypeDef,
    ListPolicyEnginesRequestTypeDef,
    ListPolicyEnginesResponseTypeDef,
    ListPolicyEngineSummariesRequestTypeDef,
    ListPolicyEngineSummariesResponseTypeDef,
    ListPolicyGenerationAssetsRequestTypeDef,
    ListPolicyGenerationAssetsResponseTypeDef,
    ListPolicyGenerationsRequestTypeDef,
    ListPolicyGenerationsResponseTypeDef,
    ListPolicyGenerationSummariesRequestTypeDef,
    ListPolicyGenerationSummariesResponseTypeDef,
    ListPolicySummariesRequestTypeDef,
    ListPolicySummariesResponseTypeDef,
    ListRegistriesRequestTypeDef,
    ListRegistriesResponseTypeDef,
    ListRegistryRecordsRequestTypeDef,
    ListRegistryRecordsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListWorkloadIdentitiesRequestTypeDef,
    ListWorkloadIdentitiesResponseTypeDef,
    PutResourcePolicyRequestTypeDef,
    PutResourcePolicyResponseTypeDef,
    SetTokenVaultCMKRequestTypeDef,
    SetTokenVaultCMKResponseTypeDef,
    StartPolicyGenerationRequestTypeDef,
    StartPolicyGenerationResponseTypeDef,
    SubmitRegistryRecordForApprovalRequestTypeDef,
    SubmitRegistryRecordForApprovalResponseTypeDef,
    SynchronizeGatewayTargetsRequestTypeDef,
    SynchronizeGatewayTargetsResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateAgentRuntimeEndpointRequestTypeDef,
    UpdateAgentRuntimeEndpointResponseTypeDef,
    UpdateAgentRuntimeRequestTypeDef,
    UpdateAgentRuntimeResponseTypeDef,
    UpdateApiKeyCredentialProviderRequestTypeDef,
    UpdateApiKeyCredentialProviderResponseTypeDef,
    UpdateConfigurationBundleRequestTypeDef,
    UpdateConfigurationBundleResponseTypeDef,
    UpdateDatasetExamplesRequestTypeDef,
    UpdateDatasetExamplesResponseTypeDef,
    UpdateDatasetRequestTypeDef,
    UpdateDatasetResponseTypeDef,
    UpdateEvaluatorRequestTypeDef,
    UpdateEvaluatorResponseTypeDef,
    UpdateGatewayRequestTypeDef,
    UpdateGatewayResponseTypeDef,
    UpdateGatewayRuleRequestTypeDef,
    UpdateGatewayRuleResponseTypeDef,
    UpdateGatewayTargetRequestTypeDef,
    UpdateGatewayTargetResponseTypeDef,
    UpdateHarnessEndpointRequestTypeDef,
    UpdateHarnessEndpointResponseTypeDef,
    UpdateHarnessRequestTypeDef,
    UpdateHarnessResponseTypeDef,
    UpdateMemoryInputTypeDef,
    UpdateMemoryOutputTypeDef,
    UpdateOauth2CredentialProviderRequestTypeDef,
    UpdateOauth2CredentialProviderResponseTypeDef,
    UpdateOnlineEvaluationConfigRequestTypeDef,
    UpdateOnlineEvaluationConfigResponseTypeDef,
    UpdatePaymentConnectorRequestTypeDef,
    UpdatePaymentConnectorResponseTypeDef,
    UpdatePaymentCredentialProviderRequestTypeDef,
    UpdatePaymentCredentialProviderResponseTypeDef,
    UpdatePaymentManagerRequestTypeDef,
    UpdatePaymentManagerResponseTypeDef,
    UpdatePolicyEngineRequestTypeDef,
    UpdatePolicyEngineResponseTypeDef,
    UpdatePolicyRequestTypeDef,
    UpdatePolicyResponseTypeDef,
    UpdateRegistryRecordRequestTypeDef,
    UpdateRegistryRecordResponseTypeDef,
    UpdateRegistryRecordStatusRequestTypeDef,
    UpdateRegistryRecordStatusResponseTypeDef,
    UpdateRegistryRequestTypeDef,
    UpdateRegistryResponseTypeDef,
    UpdateWorkloadIdentityRequestTypeDef,
    UpdateWorkloadIdentityResponseTypeDef,
)
from .waiter import (
    MemoryCreatedWaiter,
    PolicyActiveWaiter,
    PolicyDeletedWaiter,
    PolicyEngineActiveWaiter,
    PolicyEngineDeletedWaiter,
    PolicyGenerationCompletedWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("BedrockAgentCoreControlClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConcurrentModificationException: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    DecryptionFailure: type[BotocoreClientError]
    EncryptionFailure: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceLimitExceededException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottledException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    UnauthorizedException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class BedrockAgentCoreControlClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control.html#BedrockAgentCoreControl.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BedrockAgentCoreControlClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control.html#BedrockAgentCoreControl.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#generate_presigned_url)
        """

    def add_dataset_examples(
        self, **kwargs: Unpack[AddDatasetExamplesRequestTypeDef]
    ) -> AddDatasetExamplesResponseTypeDef:
        """
        Adds examples to the dataset's DRAFT.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/add_dataset_examples.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#add_dataset_examples)
        """

    def create_agent_runtime(
        self, **kwargs: Unpack[CreateAgentRuntimeRequestTypeDef]
    ) -> CreateAgentRuntimeResponseTypeDef:
        """
        Creates an Amazon Bedrock AgentCore Runtime.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_agent_runtime.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_agent_runtime)
        """

    def create_agent_runtime_endpoint(
        self, **kwargs: Unpack[CreateAgentRuntimeEndpointRequestTypeDef]
    ) -> CreateAgentRuntimeEndpointResponseTypeDef:
        """
        Creates an AgentCore Runtime endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_agent_runtime_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_agent_runtime_endpoint)
        """

    def create_api_key_credential_provider(
        self, **kwargs: Unpack[CreateApiKeyCredentialProviderRequestTypeDef]
    ) -> CreateApiKeyCredentialProviderResponseTypeDef:
        """
        Creates a new API key credential provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_api_key_credential_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_api_key_credential_provider)
        """

    def create_browser(
        self, **kwargs: Unpack[CreateBrowserRequestTypeDef]
    ) -> CreateBrowserResponseTypeDef:
        """
        Creates a custom browser.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_browser.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_browser)
        """

    def create_browser_profile(
        self, **kwargs: Unpack[CreateBrowserProfileRequestTypeDef]
    ) -> CreateBrowserProfileResponseTypeDef:
        """
        Creates a browser profile in Amazon Bedrock AgentCore.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_browser_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_browser_profile)
        """

    def create_code_interpreter(
        self, **kwargs: Unpack[CreateCodeInterpreterRequestTypeDef]
    ) -> CreateCodeInterpreterResponseTypeDef:
        """
        Creates a custom code interpreter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_code_interpreter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_code_interpreter)
        """

    def create_configuration_bundle(
        self, **kwargs: Unpack[CreateConfigurationBundleRequestTypeDef]
    ) -> CreateConfigurationBundleResponseTypeDef:
        """
        Creates a new configuration bundle resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_configuration_bundle.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_configuration_bundle)
        """

    def create_dataset(
        self, **kwargs: Unpack[CreateDatasetRequestTypeDef]
    ) -> CreateDatasetResponseTypeDef:
        """
        Creates a new dataset resource asynchronously.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_dataset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_dataset)
        """

    def create_dataset_version(
        self, **kwargs: Unpack[CreateDatasetVersionRequestTypeDef]
    ) -> CreateDatasetVersionResponseTypeDef:
        """
        Publishes the current DRAFT as a new numbered version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_dataset_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_dataset_version)
        """

    def create_evaluator(
        self, **kwargs: Unpack[CreateEvaluatorRequestTypeDef]
    ) -> CreateEvaluatorResponseTypeDef:
        """
        Creates a custom evaluator for agent quality assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_evaluator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_evaluator)
        """

    def create_gateway(
        self, **kwargs: Unpack[CreateGatewayRequestTypeDef]
    ) -> CreateGatewayResponseTypeDef:
        """
        Creates a gateway for Amazon Bedrock Agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_gateway.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_gateway)
        """

    def create_gateway_rule(
        self, **kwargs: Unpack[CreateGatewayRuleRequestTypeDef]
    ) -> CreateGatewayRuleResponseTypeDef:
        """
        Creates a rule for a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_gateway_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_gateway_rule)
        """

    def create_gateway_target(
        self, **kwargs: Unpack[CreateGatewayTargetRequestTypeDef]
    ) -> CreateGatewayTargetResponseTypeDef:
        """
        Creates a target for a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_gateway_target.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_gateway_target)
        """

    def create_harness(
        self, **kwargs: Unpack[CreateHarnessRequestTypeDef]
    ) -> CreateHarnessResponseTypeDef:
        """
        Operation to create a harness.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_harness.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_harness)
        """

    def create_harness_endpoint(
        self, **kwargs: Unpack[CreateHarnessEndpointRequestTypeDef]
    ) -> CreateHarnessEndpointResponseTypeDef:
        """
        Operation to create a harness endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_harness_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_harness_endpoint)
        """

    def create_memory(
        self, **kwargs: Unpack[CreateMemoryInputTypeDef]
    ) -> CreateMemoryOutputTypeDef:
        """
        Creates a new Amazon Bedrock AgentCore Memory resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_memory.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_memory)
        """

    def create_oauth2_credential_provider(
        self, **kwargs: Unpack[CreateOauth2CredentialProviderRequestTypeDef]
    ) -> CreateOauth2CredentialProviderResponseTypeDef:
        """
        Creates a new OAuth2 credential provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_oauth2_credential_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_oauth2_credential_provider)
        """

    def create_online_evaluation_config(
        self, **kwargs: Unpack[CreateOnlineEvaluationConfigRequestTypeDef]
    ) -> CreateOnlineEvaluationConfigResponseTypeDef:
        """
        Creates an online evaluation configuration for continuous monitoring of agent
        performance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_online_evaluation_config.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_online_evaluation_config)
        """

    def create_payment_connector(
        self, **kwargs: Unpack[CreatePaymentConnectorRequestTypeDef]
    ) -> CreatePaymentConnectorResponseTypeDef:
        """
        Creates a new payment connector for a payment manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_payment_connector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_payment_connector)
        """

    def create_payment_credential_provider(
        self, **kwargs: Unpack[CreatePaymentCredentialProviderRequestTypeDef]
    ) -> CreatePaymentCredentialProviderResponseTypeDef:
        """
        Creates a new payment credential provider for storing authentication
        credentials used by payment connectors to communicate with external payment
        providers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_payment_credential_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_payment_credential_provider)
        """

    def create_payment_manager(
        self, **kwargs: Unpack[CreatePaymentManagerRequestTypeDef]
    ) -> CreatePaymentManagerResponseTypeDef:
        """
        Creates a new payment manager in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_payment_manager.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_payment_manager)
        """

    def create_policy(
        self, **kwargs: Unpack[CreatePolicyRequestTypeDef]
    ) -> CreatePolicyResponseTypeDef:
        """
        Creates a policy within the AgentCore Policy system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_policy)
        """

    def create_policy_engine(
        self, **kwargs: Unpack[CreatePolicyEngineRequestTypeDef]
    ) -> CreatePolicyEngineResponseTypeDef:
        """
        Creates a new policy engine within the AgentCore Policy system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_policy_engine.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_policy_engine)
        """

    def create_registry(
        self, **kwargs: Unpack[CreateRegistryRequestTypeDef]
    ) -> CreateRegistryResponseTypeDef:
        """
        Creates a new registry in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_registry.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_registry)
        """

    def create_registry_record(
        self, **kwargs: Unpack[CreateRegistryRecordRequestTypeDef]
    ) -> CreateRegistryRecordResponseTypeDef:
        """
        Creates a new registry record within the specified registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_registry_record.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_registry_record)
        """

    def create_workload_identity(
        self, **kwargs: Unpack[CreateWorkloadIdentityRequestTypeDef]
    ) -> CreateWorkloadIdentityResponseTypeDef:
        """
        Creates a new workload identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_workload_identity.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_workload_identity)
        """

    def delete_agent_runtime(
        self, **kwargs: Unpack[DeleteAgentRuntimeRequestTypeDef]
    ) -> DeleteAgentRuntimeResponseTypeDef:
        """
        Deletes an Amazon Bedrock AgentCore Runtime.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_agent_runtime.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_agent_runtime)
        """

    def delete_agent_runtime_endpoint(
        self, **kwargs: Unpack[DeleteAgentRuntimeEndpointRequestTypeDef]
    ) -> DeleteAgentRuntimeEndpointResponseTypeDef:
        """
        Deletes an AAgentCore Runtime endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_agent_runtime_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_agent_runtime_endpoint)
        """

    def delete_api_key_credential_provider(
        self, **kwargs: Unpack[DeleteApiKeyCredentialProviderRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes an API key credential provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_api_key_credential_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_api_key_credential_provider)
        """

    def delete_browser(
        self, **kwargs: Unpack[DeleteBrowserRequestTypeDef]
    ) -> DeleteBrowserResponseTypeDef:
        """
        Deletes a custom browser.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_browser.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_browser)
        """

    def delete_browser_profile(
        self, **kwargs: Unpack[DeleteBrowserProfileRequestTypeDef]
    ) -> DeleteBrowserProfileResponseTypeDef:
        """
        Deletes a browser profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_browser_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_browser_profile)
        """

    def delete_code_interpreter(
        self, **kwargs: Unpack[DeleteCodeInterpreterRequestTypeDef]
    ) -> DeleteCodeInterpreterResponseTypeDef:
        """
        Deletes a custom code interpreter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_code_interpreter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_code_interpreter)
        """

    def delete_configuration_bundle(
        self, **kwargs: Unpack[DeleteConfigurationBundleRequestTypeDef]
    ) -> DeleteConfigurationBundleResponseTypeDef:
        """
        Deletes a configuration bundle and all of its versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_configuration_bundle.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_configuration_bundle)
        """

    def delete_dataset(
        self, **kwargs: Unpack[DeleteDatasetRequestTypeDef]
    ) -> DeleteDatasetResponseTypeDef:
        """
        Deletes a dataset version or an entire dataset asynchronously.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_dataset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_dataset)
        """

    def delete_dataset_examples(
        self, **kwargs: Unpack[DeleteDatasetExamplesRequestTypeDef]
    ) -> DeleteDatasetExamplesResponseTypeDef:
        """
        Deletes specific examples by ID from DRAFT.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_dataset_examples.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_dataset_examples)
        """

    def delete_evaluator(
        self, **kwargs: Unpack[DeleteEvaluatorRequestTypeDef]
    ) -> DeleteEvaluatorResponseTypeDef:
        """
        Deletes a custom evaluator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_evaluator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_evaluator)
        """

    def delete_gateway(
        self, **kwargs: Unpack[DeleteGatewayRequestTypeDef]
    ) -> DeleteGatewayResponseTypeDef:
        """
        Deletes a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_gateway.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_gateway)
        """

    def delete_gateway_rule(
        self, **kwargs: Unpack[DeleteGatewayRuleRequestTypeDef]
    ) -> DeleteGatewayRuleResponseTypeDef:
        """
        Deletes a gateway rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_gateway_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_gateway_rule)
        """

    def delete_gateway_target(
        self, **kwargs: Unpack[DeleteGatewayTargetRequestTypeDef]
    ) -> DeleteGatewayTargetResponseTypeDef:
        """
        Deletes a gateway target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_gateway_target.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_gateway_target)
        """

    def delete_harness(
        self, **kwargs: Unpack[DeleteHarnessRequestTypeDef]
    ) -> DeleteHarnessResponseTypeDef:
        """
        Operation to delete a Harness.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_harness.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_harness)
        """

    def delete_harness_endpoint(
        self, **kwargs: Unpack[DeleteHarnessEndpointRequestTypeDef]
    ) -> DeleteHarnessEndpointResponseTypeDef:
        """
        Operation to delete a harness endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_harness_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_harness_endpoint)
        """

    def delete_memory(
        self, **kwargs: Unpack[DeleteMemoryInputTypeDef]
    ) -> DeleteMemoryOutputTypeDef:
        """
        Deletes an Amazon Bedrock AgentCore Memory resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_memory.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_memory)
        """

    def delete_oauth2_credential_provider(
        self, **kwargs: Unpack[DeleteOauth2CredentialProviderRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes an OAuth2 credential provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_oauth2_credential_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_oauth2_credential_provider)
        """

    def delete_online_evaluation_config(
        self, **kwargs: Unpack[DeleteOnlineEvaluationConfigRequestTypeDef]
    ) -> DeleteOnlineEvaluationConfigResponseTypeDef:
        """
        Deletes an online evaluation configuration and stops any ongoing evaluation
        processes associated with it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_online_evaluation_config.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_online_evaluation_config)
        """

    def delete_payment_connector(
        self, **kwargs: Unpack[DeletePaymentConnectorRequestTypeDef]
    ) -> DeletePaymentConnectorResponseTypeDef:
        """
        Deletes a payment connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_payment_connector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_payment_connector)
        """

    def delete_payment_credential_provider(
        self, **kwargs: Unpack[DeletePaymentCredentialProviderRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes a payment credential provider and its associated stored credentials.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_payment_credential_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_payment_credential_provider)
        """

    def delete_payment_manager(
        self, **kwargs: Unpack[DeletePaymentManagerRequestTypeDef]
    ) -> DeletePaymentManagerResponseTypeDef:
        """
        Deletes a payment manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_payment_manager.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_payment_manager)
        """

    def delete_policy(
        self, **kwargs: Unpack[DeletePolicyRequestTypeDef]
    ) -> DeletePolicyResponseTypeDef:
        """
        Deletes an existing policy from the AgentCore Policy system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_policy)
        """

    def delete_policy_engine(
        self, **kwargs: Unpack[DeletePolicyEngineRequestTypeDef]
    ) -> DeletePolicyEngineResponseTypeDef:
        """
        Deletes an existing policy engine from the AgentCore Policy system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_policy_engine.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_policy_engine)
        """

    def delete_registry(
        self, **kwargs: Unpack[DeleteRegistryRequestTypeDef]
    ) -> DeleteRegistryResponseTypeDef:
        """
        Deletes a registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_registry.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_registry)
        """

    def delete_registry_record(
        self, **kwargs: Unpack[DeleteRegistryRecordRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes a registry record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_registry_record.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_registry_record)
        """

    def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes the resource-based policy for a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_resource_policy)
        """

    def delete_workload_identity(
        self, **kwargs: Unpack[DeleteWorkloadIdentityRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes a workload identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_workload_identity.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_workload_identity)
        """

    def get_agent_runtime(
        self, **kwargs: Unpack[GetAgentRuntimeRequestTypeDef]
    ) -> GetAgentRuntimeResponseTypeDef:
        """
        Gets an Amazon Bedrock AgentCore Runtime.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_agent_runtime.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_agent_runtime)
        """

    def get_agent_runtime_endpoint(
        self, **kwargs: Unpack[GetAgentRuntimeEndpointRequestTypeDef]
    ) -> GetAgentRuntimeEndpointResponseTypeDef:
        """
        Gets information about an Amazon Secure AgentEndpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_agent_runtime_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_agent_runtime_endpoint)
        """

    def get_api_key_credential_provider(
        self, **kwargs: Unpack[GetApiKeyCredentialProviderRequestTypeDef]
    ) -> GetApiKeyCredentialProviderResponseTypeDef:
        """
        Retrieves information about an API key credential provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_api_key_credential_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_api_key_credential_provider)
        """

    def get_browser(self, **kwargs: Unpack[GetBrowserRequestTypeDef]) -> GetBrowserResponseTypeDef:
        """
        Gets information about a custom browser.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_browser.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_browser)
        """

    def get_browser_profile(
        self, **kwargs: Unpack[GetBrowserProfileRequestTypeDef]
    ) -> GetBrowserProfileResponseTypeDef:
        """
        Gets information about a browser profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_browser_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_browser_profile)
        """

    def get_code_interpreter(
        self, **kwargs: Unpack[GetCodeInterpreterRequestTypeDef]
    ) -> GetCodeInterpreterResponseTypeDef:
        """
        Gets information about a custom code interpreter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_code_interpreter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_code_interpreter)
        """

    def get_configuration_bundle(
        self, **kwargs: Unpack[GetConfigurationBundleRequestTypeDef]
    ) -> GetConfigurationBundleResponseTypeDef:
        """
        Gets the latest version of a configuration bundle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_configuration_bundle.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_configuration_bundle)
        """

    def get_configuration_bundle_version(
        self, **kwargs: Unpack[GetConfigurationBundleVersionRequestTypeDef]
    ) -> GetConfigurationBundleVersionResponseTypeDef:
        """
        Gets a specific version of a configuration bundle by its version identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_configuration_bundle_version.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_configuration_bundle_version)
        """

    def get_dataset(self, **kwargs: Unpack[GetDatasetRequestTypeDef]) -> GetDatasetResponseTypeDef:
        """
        Retrieves dataset metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_dataset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_dataset)
        """

    def get_evaluator(
        self, **kwargs: Unpack[GetEvaluatorRequestTypeDef]
    ) -> GetEvaluatorResponseTypeDef:
        """
        Retrieves detailed information about an evaluator, including its configuration,
        status, and metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_evaluator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_evaluator)
        """

    def get_gateway(self, **kwargs: Unpack[GetGatewayRequestTypeDef]) -> GetGatewayResponseTypeDef:
        """
        Retrieves information about a specific Gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_gateway.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_gateway)
        """

    def get_gateway_rule(
        self, **kwargs: Unpack[GetGatewayRuleRequestTypeDef]
    ) -> GetGatewayRuleResponseTypeDef:
        """
        Retrieves detailed information about a specific gateway rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_gateway_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_gateway_rule)
        """

    def get_gateway_target(
        self, **kwargs: Unpack[GetGatewayTargetRequestTypeDef]
    ) -> GetGatewayTargetResponseTypeDef:
        """
        Retrieves information about a specific gateway target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_gateway_target.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_gateway_target)
        """

    def get_harness(self, **kwargs: Unpack[GetHarnessRequestTypeDef]) -> GetHarnessResponseTypeDef:
        """
        Operation to get a single harness.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_harness.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_harness)
        """

    def get_harness_endpoint(
        self, **kwargs: Unpack[GetHarnessEndpointRequestTypeDef]
    ) -> GetHarnessEndpointResponseTypeDef:
        """
        Operation to get a single harness endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_harness_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_harness_endpoint)
        """

    def get_memory(self, **kwargs: Unpack[GetMemoryInputTypeDef]) -> GetMemoryOutputTypeDef:
        """
        Retrieve an existing Amazon Bedrock AgentCore Memory resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_memory.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_memory)
        """

    def get_oauth2_credential_provider(
        self, **kwargs: Unpack[GetOauth2CredentialProviderRequestTypeDef]
    ) -> GetOauth2CredentialProviderResponseTypeDef:
        """
        Retrieves information about an OAuth2 credential provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_oauth2_credential_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_oauth2_credential_provider)
        """

    def get_online_evaluation_config(
        self, **kwargs: Unpack[GetOnlineEvaluationConfigRequestTypeDef]
    ) -> GetOnlineEvaluationConfigResponseTypeDef:
        """
        Retrieves detailed information about an online evaluation configuration,
        including its rules, data sources, evaluators, and execution status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_online_evaluation_config.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_online_evaluation_config)
        """

    def get_payment_connector(
        self, **kwargs: Unpack[GetPaymentConnectorRequestTypeDef]
    ) -> GetPaymentConnectorResponseTypeDef:
        """
        Retrieves information about a specific payment connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_payment_connector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_payment_connector)
        """

    def get_payment_credential_provider(
        self, **kwargs: Unpack[GetPaymentCredentialProviderRequestTypeDef]
    ) -> GetPaymentCredentialProviderResponseTypeDef:
        """
        Retrieves information about a specific payment credential provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_payment_credential_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_payment_credential_provider)
        """

    def get_payment_manager(
        self, **kwargs: Unpack[GetPaymentManagerRequestTypeDef]
    ) -> GetPaymentManagerResponseTypeDef:
        """
        Retrieves information about a specific payment manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_payment_manager.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_payment_manager)
        """

    def get_policy(self, **kwargs: Unpack[GetPolicyRequestTypeDef]) -> GetPolicyResponseTypeDef:
        """
        Retrieves detailed information about a specific policy within the AgentCore
        Policy system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_policy)
        """

    def get_policy_engine(
        self, **kwargs: Unpack[GetPolicyEngineRequestTypeDef]
    ) -> GetPolicyEngineResponseTypeDef:
        """
        Retrieves detailed information about a specific policy engine within the
        AgentCore Policy system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_policy_engine.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_policy_engine)
        """

    def get_policy_engine_summary(
        self, **kwargs: Unpack[GetPolicyEngineSummaryRequestTypeDef]
    ) -> GetPolicyEngineSummaryResponseTypeDef:
        """
        Retrieves a metadata-only summary of a specific policy engine without
        decrypting customer content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_policy_engine_summary.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_policy_engine_summary)
        """

    def get_policy_generation(
        self, **kwargs: Unpack[GetPolicyGenerationRequestTypeDef]
    ) -> GetPolicyGenerationResponseTypeDef:
        """
        Retrieves information about a policy generation request within the AgentCore
        Policy system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_policy_generation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_policy_generation)
        """

    def get_policy_generation_summary(
        self, **kwargs: Unpack[GetPolicyGenerationSummaryRequestTypeDef]
    ) -> GetPolicyGenerationSummaryResponseTypeDef:
        """
        Retrieves a metadata-only summary of a specific policy generation request
        without decrypting customer content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_policy_generation_summary.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_policy_generation_summary)
        """

    def get_policy_summary(
        self, **kwargs: Unpack[GetPolicySummaryRequestTypeDef]
    ) -> GetPolicySummaryResponseTypeDef:
        """
        Retrieves a metadata-only summary of a specific policy without decrypting
        customer content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_policy_summary.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_policy_summary)
        """

    def get_registry(
        self, **kwargs: Unpack[GetRegistryRequestTypeDef]
    ) -> GetRegistryResponseTypeDef:
        """
        Retrieves information about a specific registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_registry.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_registry)
        """

    def get_registry_record(
        self, **kwargs: Unpack[GetRegistryRecordRequestTypeDef]
    ) -> GetRegistryRecordResponseTypeDef:
        """
        Retrieves information about a specific registry record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_registry_record.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_registry_record)
        """

    def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyRequestTypeDef]
    ) -> GetResourcePolicyResponseTypeDef:
        """
        Retrieves the resource-based policy for a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_resource_policy)
        """

    def get_token_vault(
        self, **kwargs: Unpack[GetTokenVaultRequestTypeDef]
    ) -> GetTokenVaultResponseTypeDef:
        """
        Retrieves information about a token vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_token_vault.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_token_vault)
        """

    def get_workload_identity(
        self, **kwargs: Unpack[GetWorkloadIdentityRequestTypeDef]
    ) -> GetWorkloadIdentityResponseTypeDef:
        """
        Retrieves information about a workload identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_workload_identity.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_workload_identity)
        """

    def list_agent_runtime_endpoints(
        self, **kwargs: Unpack[ListAgentRuntimeEndpointsRequestTypeDef]
    ) -> ListAgentRuntimeEndpointsResponseTypeDef:
        """
        Lists all endpoints for a specific Amazon Secure Agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_agent_runtime_endpoints.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_agent_runtime_endpoints)
        """

    def list_agent_runtime_versions(
        self, **kwargs: Unpack[ListAgentRuntimeVersionsRequestTypeDef]
    ) -> ListAgentRuntimeVersionsResponseTypeDef:
        """
        Lists all versions of a specific Amazon Secure Agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_agent_runtime_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_agent_runtime_versions)
        """

    def list_agent_runtimes(
        self, **kwargs: Unpack[ListAgentRuntimesRequestTypeDef]
    ) -> ListAgentRuntimesResponseTypeDef:
        """
        Lists all Amazon Secure Agents in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_agent_runtimes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_agent_runtimes)
        """

    def list_api_key_credential_providers(
        self, **kwargs: Unpack[ListApiKeyCredentialProvidersRequestTypeDef]
    ) -> ListApiKeyCredentialProvidersResponseTypeDef:
        """
        Lists all API key credential providers in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_api_key_credential_providers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_api_key_credential_providers)
        """

    def list_browser_profiles(
        self, **kwargs: Unpack[ListBrowserProfilesRequestTypeDef]
    ) -> ListBrowserProfilesResponseTypeDef:
        """
        Lists all browser profiles in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_browser_profiles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_browser_profiles)
        """

    def list_browsers(
        self, **kwargs: Unpack[ListBrowsersRequestTypeDef]
    ) -> ListBrowsersResponseTypeDef:
        """
        Lists all custom browsers in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_browsers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_browsers)
        """

    def list_code_interpreters(
        self, **kwargs: Unpack[ListCodeInterpretersRequestTypeDef]
    ) -> ListCodeInterpretersResponseTypeDef:
        """
        Lists all custom code interpreters in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_code_interpreters.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_code_interpreters)
        """

    def list_configuration_bundle_versions(
        self, **kwargs: Unpack[ListConfigurationBundleVersionsRequestTypeDef]
    ) -> ListConfigurationBundleVersionsResponseTypeDef:
        """
        Lists all versions of a configuration bundle, with optional filtering by branch
        name or creation source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_configuration_bundle_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_configuration_bundle_versions)
        """

    def list_configuration_bundles(
        self, **kwargs: Unpack[ListConfigurationBundlesRequestTypeDef]
    ) -> ListConfigurationBundlesResponseTypeDef:
        """
        Lists all configuration bundles in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_configuration_bundles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_configuration_bundles)
        """

    def list_dataset_examples(
        self, **kwargs: Unpack[ListDatasetExamplesRequestTypeDef]
    ) -> ListDatasetExamplesResponseTypeDef:
        """
        Returns paginated examples from the dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_dataset_examples.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_dataset_examples)
        """

    def list_dataset_versions(
        self, **kwargs: Unpack[ListDatasetVersionsRequestTypeDef]
    ) -> ListDatasetVersionsResponseTypeDef:
        """
        Lists all published versions of a dataset, sorted by version number descending
        (newest first).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_dataset_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_dataset_versions)
        """

    def list_datasets(
        self, **kwargs: Unpack[ListDatasetsRequestTypeDef]
    ) -> ListDatasetsResponseTypeDef:
        """
        Lists all datasets in the caller's account, paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_datasets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_datasets)
        """

    def list_evaluators(
        self, **kwargs: Unpack[ListEvaluatorsRequestTypeDef]
    ) -> ListEvaluatorsResponseTypeDef:
        """
        Lists all available evaluators, including both builtin evaluators provided by
        the service and custom evaluators created by the user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_evaluators.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_evaluators)
        """

    def list_gateway_rules(
        self, **kwargs: Unpack[ListGatewayRulesRequestTypeDef]
    ) -> ListGatewayRulesResponseTypeDef:
        """
        Lists all rules for a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_gateway_rules.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_gateway_rules)
        """

    def list_gateway_targets(
        self, **kwargs: Unpack[ListGatewayTargetsRequestTypeDef]
    ) -> ListGatewayTargetsResponseTypeDef:
        """
        Lists all targets for a specific gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_gateway_targets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_gateway_targets)
        """

    def list_gateways(
        self, **kwargs: Unpack[ListGatewaysRequestTypeDef]
    ) -> ListGatewaysResponseTypeDef:
        """
        Lists all gateways in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_gateways.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_gateways)
        """

    def list_harness_endpoints(
        self, **kwargs: Unpack[ListHarnessEndpointsRequestTypeDef]
    ) -> ListHarnessEndpointsResponseTypeDef:
        """
        Operation to list the endpoints of a harness.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_harness_endpoints.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_harness_endpoints)
        """

    def list_harness_versions(
        self, **kwargs: Unpack[ListHarnessVersionsRequestTypeDef]
    ) -> ListHarnessVersionsResponseTypeDef:
        """
        Operation to list the versions of a Harness.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_harness_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_harness_versions)
        """

    def list_harnesses(
        self, **kwargs: Unpack[ListHarnessesRequestTypeDef]
    ) -> ListHarnessesResponseTypeDef:
        """
        Operation to list harnesses.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_harnesses.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_harnesses)
        """

    def list_memories(
        self, **kwargs: Unpack[ListMemoriesInputTypeDef]
    ) -> ListMemoriesOutputTypeDef:
        """
        Lists the available Amazon Bedrock AgentCore Memory resources in the current
        Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_memories.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_memories)
        """

    def list_oauth2_credential_providers(
        self, **kwargs: Unpack[ListOauth2CredentialProvidersRequestTypeDef]
    ) -> ListOauth2CredentialProvidersResponseTypeDef:
        """
        Lists all OAuth2 credential providers in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_oauth2_credential_providers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_oauth2_credential_providers)
        """

    def list_online_evaluation_configs(
        self, **kwargs: Unpack[ListOnlineEvaluationConfigsRequestTypeDef]
    ) -> ListOnlineEvaluationConfigsResponseTypeDef:
        """
        Lists all online evaluation configurations in the account, providing summary
        information about each configuration's status and settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_online_evaluation_configs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_online_evaluation_configs)
        """

    def list_payment_connectors(
        self, **kwargs: Unpack[ListPaymentConnectorsRequestTypeDef]
    ) -> ListPaymentConnectorsResponseTypeDef:
        """
        Lists all payment connectors for a specified payment manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_payment_connectors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_payment_connectors)
        """

    def list_payment_credential_providers(
        self, **kwargs: Unpack[ListPaymentCredentialProvidersRequestTypeDef]
    ) -> ListPaymentCredentialProvidersResponseTypeDef:
        """
        Lists all payment credential providers in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_payment_credential_providers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_payment_credential_providers)
        """

    def list_payment_managers(
        self, **kwargs: Unpack[ListPaymentManagersRequestTypeDef]
    ) -> ListPaymentManagersResponseTypeDef:
        """
        Lists all payment managers in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_payment_managers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_payment_managers)
        """

    def list_policies(
        self, **kwargs: Unpack[ListPoliciesRequestTypeDef]
    ) -> ListPoliciesResponseTypeDef:
        """
        Retrieves a list of policies within the AgentCore Policy engine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_policies)
        """

    def list_policy_engine_summaries(
        self, **kwargs: Unpack[ListPolicyEngineSummariesRequestTypeDef]
    ) -> ListPolicyEngineSummariesResponseTypeDef:
        """
        Retrieves a paginated list of metadata-only policy engine summaries without
        decrypting customer content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_policy_engine_summaries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_policy_engine_summaries)
        """

    def list_policy_engines(
        self, **kwargs: Unpack[ListPolicyEnginesRequestTypeDef]
    ) -> ListPolicyEnginesResponseTypeDef:
        """
        Retrieves a list of policy engines within the AgentCore Policy system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_policy_engines.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_policy_engines)
        """

    def list_policy_generation_assets(
        self, **kwargs: Unpack[ListPolicyGenerationAssetsRequestTypeDef]
    ) -> ListPolicyGenerationAssetsResponseTypeDef:
        """
        Retrieves a list of generated policy assets from a policy generation request
        within the AgentCore Policy system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_policy_generation_assets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_policy_generation_assets)
        """

    def list_policy_generation_summaries(
        self, **kwargs: Unpack[ListPolicyGenerationSummariesRequestTypeDef]
    ) -> ListPolicyGenerationSummariesResponseTypeDef:
        """
        Retrieves a paginated list of metadata-only policy generation summaries within
        a policy engine without decrypting customer content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_policy_generation_summaries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_policy_generation_summaries)
        """

    def list_policy_generations(
        self, **kwargs: Unpack[ListPolicyGenerationsRequestTypeDef]
    ) -> ListPolicyGenerationsResponseTypeDef:
        """
        Retrieves a list of policy generation requests within the AgentCore Policy
        system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_policy_generations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_policy_generations)
        """

    def list_policy_summaries(
        self, **kwargs: Unpack[ListPolicySummariesRequestTypeDef]
    ) -> ListPolicySummariesResponseTypeDef:
        """
        Retrieves a paginated list of metadata-only policy summaries within a policy
        engine without decrypting customer content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_policy_summaries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_policy_summaries)
        """

    def list_registries(
        self, **kwargs: Unpack[ListRegistriesRequestTypeDef]
    ) -> ListRegistriesResponseTypeDef:
        """
        Lists all registries in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_registries.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_registries)
        """

    def list_registry_records(
        self, **kwargs: Unpack[ListRegistryRecordsRequestTypeDef]
    ) -> ListRegistryRecordsResponseTypeDef:
        """
        Lists registry records within a registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_registry_records.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_registry_records)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags associated with the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_tags_for_resource)
        """

    def list_workload_identities(
        self, **kwargs: Unpack[ListWorkloadIdentitiesRequestTypeDef]
    ) -> ListWorkloadIdentitiesResponseTypeDef:
        """
        Lists all workload identities in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_workload_identities.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_workload_identities)
        """

    def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyRequestTypeDef]
    ) -> PutResourcePolicyResponseTypeDef:
        """
        Creates or updates a resource-based policy for a resource with the specified
        resourceArn.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/put_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#put_resource_policy)
        """

    def set_token_vault_cmk(
        self, **kwargs: Unpack[SetTokenVaultCMKRequestTypeDef]
    ) -> SetTokenVaultCMKResponseTypeDef:
        """
        Sets the customer master key (CMK) for a token vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/set_token_vault_cmk.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#set_token_vault_cmk)
        """

    def start_policy_generation(
        self, **kwargs: Unpack[StartPolicyGenerationRequestTypeDef]
    ) -> StartPolicyGenerationResponseTypeDef:
        """
        Initiates the AI-powered generation of Cedar policies from natural language
        descriptions within the AgentCore Policy system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/start_policy_generation.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#start_policy_generation)
        """

    def submit_registry_record_for_approval(
        self, **kwargs: Unpack[SubmitRegistryRecordForApprovalRequestTypeDef]
    ) -> SubmitRegistryRecordForApprovalResponseTypeDef:
        """
        Submits a registry record for approval.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/submit_registry_record_for_approval.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#submit_registry_record_for_approval)
        """

    def synchronize_gateway_targets(
        self, **kwargs: Unpack[SynchronizeGatewayTargetsRequestTypeDef]
    ) -> SynchronizeGatewayTargetsResponseTypeDef:
        """
        Synchronizes the gateway targets by fetching the latest tool definitions from
        the target endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/synchronize_gateway_targets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#synchronize_gateway_targets)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Associates the specified tags to a resource with the specified resourceArn.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Removes the specified tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#untag_resource)
        """

    def update_agent_runtime(
        self, **kwargs: Unpack[UpdateAgentRuntimeRequestTypeDef]
    ) -> UpdateAgentRuntimeResponseTypeDef:
        """
        Updates an existing Amazon Secure Agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_agent_runtime.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_agent_runtime)
        """

    def update_agent_runtime_endpoint(
        self, **kwargs: Unpack[UpdateAgentRuntimeEndpointRequestTypeDef]
    ) -> UpdateAgentRuntimeEndpointResponseTypeDef:
        """
        Updates an existing Amazon Bedrock AgentCore Runtime endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_agent_runtime_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_agent_runtime_endpoint)
        """

    def update_api_key_credential_provider(
        self, **kwargs: Unpack[UpdateApiKeyCredentialProviderRequestTypeDef]
    ) -> UpdateApiKeyCredentialProviderResponseTypeDef:
        """
        Updates an existing API key credential provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_api_key_credential_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_api_key_credential_provider)
        """

    def update_configuration_bundle(
        self, **kwargs: Unpack[UpdateConfigurationBundleRequestTypeDef]
    ) -> UpdateConfigurationBundleResponseTypeDef:
        """
        Updates a configuration bundle by creating a new version with the specified
        changes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_configuration_bundle.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_configuration_bundle)
        """

    def update_dataset(
        self, **kwargs: Unpack[UpdateDatasetRequestTypeDef]
    ) -> UpdateDatasetResponseTypeDef:
        """
        Updates a dataset's metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_dataset.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_dataset)
        """

    def update_dataset_examples(
        self, **kwargs: Unpack[UpdateDatasetExamplesRequestTypeDef]
    ) -> UpdateDatasetExamplesResponseTypeDef:
        """
        Updates multiple existing examples in-place on DRAFT.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_dataset_examples.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_dataset_examples)
        """

    def update_evaluator(
        self, **kwargs: Unpack[UpdateEvaluatorRequestTypeDef]
    ) -> UpdateEvaluatorResponseTypeDef:
        """
        Updates a custom evaluator's configuration, description, or evaluation level.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_evaluator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_evaluator)
        """

    def update_gateway(
        self, **kwargs: Unpack[UpdateGatewayRequestTypeDef]
    ) -> UpdateGatewayResponseTypeDef:
        """
        Updates an existing gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_gateway.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_gateway)
        """

    def update_gateway_rule(
        self, **kwargs: Unpack[UpdateGatewayRuleRequestTypeDef]
    ) -> UpdateGatewayRuleResponseTypeDef:
        """
        Updates a gateway rule's priority, conditions, actions, or description.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_gateway_rule.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_gateway_rule)
        """

    def update_gateway_target(
        self, **kwargs: Unpack[UpdateGatewayTargetRequestTypeDef]
    ) -> UpdateGatewayTargetResponseTypeDef:
        """
        Updates an existing gateway target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_gateway_target.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_gateway_target)
        """

    def update_harness(
        self, **kwargs: Unpack[UpdateHarnessRequestTypeDef]
    ) -> UpdateHarnessResponseTypeDef:
        """
        Operation to update a harness.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_harness.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_harness)
        """

    def update_harness_endpoint(
        self, **kwargs: Unpack[UpdateHarnessEndpointRequestTypeDef]
    ) -> UpdateHarnessEndpointResponseTypeDef:
        """
        Operation to update a harness endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_harness_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_harness_endpoint)
        """

    def update_memory(
        self, **kwargs: Unpack[UpdateMemoryInputTypeDef]
    ) -> UpdateMemoryOutputTypeDef:
        """
        Update an Amazon Bedrock AgentCore Memory resource memory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_memory.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_memory)
        """

    def update_oauth2_credential_provider(
        self, **kwargs: Unpack[UpdateOauth2CredentialProviderRequestTypeDef]
    ) -> UpdateOauth2CredentialProviderResponseTypeDef:
        """
        Updates an existing OAuth2 credential provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_oauth2_credential_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_oauth2_credential_provider)
        """

    def update_online_evaluation_config(
        self, **kwargs: Unpack[UpdateOnlineEvaluationConfigRequestTypeDef]
    ) -> UpdateOnlineEvaluationConfigResponseTypeDef:
        """
        Updates an online evaluation configuration's settings, including rules, data
        sources, evaluators, and execution status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_online_evaluation_config.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_online_evaluation_config)
        """

    def update_payment_connector(
        self, **kwargs: Unpack[UpdatePaymentConnectorRequestTypeDef]
    ) -> UpdatePaymentConnectorResponseTypeDef:
        """
        Updates an existing payment connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_payment_connector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_payment_connector)
        """

    def update_payment_credential_provider(
        self, **kwargs: Unpack[UpdatePaymentCredentialProviderRequestTypeDef]
    ) -> UpdatePaymentCredentialProviderResponseTypeDef:
        """
        Updates an existing payment credential provider with new authentication
        credentials.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_payment_credential_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_payment_credential_provider)
        """

    def update_payment_manager(
        self, **kwargs: Unpack[UpdatePaymentManagerRequestTypeDef]
    ) -> UpdatePaymentManagerResponseTypeDef:
        """
        Updates an existing payment manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_payment_manager.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_payment_manager)
        """

    def update_policy(
        self, **kwargs: Unpack[UpdatePolicyRequestTypeDef]
    ) -> UpdatePolicyResponseTypeDef:
        """
        Updates an existing policy within the AgentCore Policy system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_policy)
        """

    def update_policy_engine(
        self, **kwargs: Unpack[UpdatePolicyEngineRequestTypeDef]
    ) -> UpdatePolicyEngineResponseTypeDef:
        """
        Updates an existing policy engine within the AgentCore Policy system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_policy_engine.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_policy_engine)
        """

    def update_registry(
        self, **kwargs: Unpack[UpdateRegistryRequestTypeDef]
    ) -> UpdateRegistryResponseTypeDef:
        """
        Updates an existing registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_registry.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_registry)
        """

    def update_registry_record(
        self, **kwargs: Unpack[UpdateRegistryRecordRequestTypeDef]
    ) -> UpdateRegistryRecordResponseTypeDef:
        """
        Updates an existing registry record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_registry_record.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_registry_record)
        """

    def update_registry_record_status(
        self, **kwargs: Unpack[UpdateRegistryRecordStatusRequestTypeDef]
    ) -> UpdateRegistryRecordStatusResponseTypeDef:
        """
        Updates the status of a registry record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_registry_record_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_registry_record_status)
        """

    def update_workload_identity(
        self, **kwargs: Unpack[UpdateWorkloadIdentityRequestTypeDef]
    ) -> UpdateWorkloadIdentityResponseTypeDef:
        """
        Updates an existing workload identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_workload_identity.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_workload_identity)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_agent_runtime_endpoints"]
    ) -> ListAgentRuntimeEndpointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_agent_runtime_versions"]
    ) -> ListAgentRuntimeVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_agent_runtimes"]
    ) -> ListAgentRuntimesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_api_key_credential_providers"]
    ) -> ListApiKeyCredentialProvidersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_browser_profiles"]
    ) -> ListBrowserProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_browsers"]
    ) -> ListBrowsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_code_interpreters"]
    ) -> ListCodeInterpretersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_configuration_bundle_versions"]
    ) -> ListConfigurationBundleVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_configuration_bundles"]
    ) -> ListConfigurationBundlesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_dataset_examples"]
    ) -> ListDatasetExamplesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_dataset_versions"]
    ) -> ListDatasetVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_datasets"]
    ) -> ListDatasetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_evaluators"]
    ) -> ListEvaluatorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_gateway_rules"]
    ) -> ListGatewayRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_gateway_targets"]
    ) -> ListGatewayTargetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_gateways"]
    ) -> ListGatewaysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_harness_endpoints"]
    ) -> ListHarnessEndpointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_harness_versions"]
    ) -> ListHarnessVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_harnesses"]
    ) -> ListHarnessesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_memories"]
    ) -> ListMemoriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_oauth2_credential_providers"]
    ) -> ListOauth2CredentialProvidersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_online_evaluation_configs"]
    ) -> ListOnlineEvaluationConfigsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_payment_connectors"]
    ) -> ListPaymentConnectorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_payment_credential_providers"]
    ) -> ListPaymentCredentialProvidersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_payment_managers"]
    ) -> ListPaymentManagersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_policies"]
    ) -> ListPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_policy_engine_summaries"]
    ) -> ListPolicyEngineSummariesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_policy_engines"]
    ) -> ListPolicyEnginesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_policy_generation_assets"]
    ) -> ListPolicyGenerationAssetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_policy_generation_summaries"]
    ) -> ListPolicyGenerationSummariesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_policy_generations"]
    ) -> ListPolicyGenerationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_policy_summaries"]
    ) -> ListPolicySummariesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_registries"]
    ) -> ListRegistriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_registry_records"]
    ) -> ListRegistryRecordsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_workload_identities"]
    ) -> ListWorkloadIdentitiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["memory_created"]
    ) -> MemoryCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["policy_active"]
    ) -> PolicyActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["policy_deleted"]
    ) -> PolicyDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["policy_engine_active"]
    ) -> PolicyEngineActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["policy_engine_deleted"]
    ) -> PolicyEngineDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["policy_generation_completed"]
    ) -> PolicyGenerationCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_waiter)
        """
