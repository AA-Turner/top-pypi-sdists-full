"""
Type annotations for bedrock-agentcore-control service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_bedrock_agentcore_control.client import BedrockAgentCoreControlPlaneFrontingLayerClient

    session = Session()
    client: BedrockAgentCoreControlPlaneFrontingLayerClient = session.client("bedrock-agentcore-control")
    ```
"""

from __future__ import annotations

import sys
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListAgentRuntimeEndpointsPaginator,
    ListAgentRuntimesPaginator,
    ListAgentRuntimeVersionsPaginator,
    ListApiKeyCredentialProvidersPaginator,
    ListBrowsersPaginator,
    ListCodeInterpretersPaginator,
    ListGatewaysPaginator,
    ListGatewayTargetsPaginator,
    ListMemoriesPaginator,
    ListOauth2CredentialProvidersPaginator,
    ListWorkloadIdentitiesPaginator,
)
from .type_defs import (
    CreateAgentRuntimeEndpointRequestTypeDef,
    CreateAgentRuntimeEndpointResponseTypeDef,
    CreateAgentRuntimeRequestTypeDef,
    CreateAgentRuntimeResponseTypeDef,
    CreateApiKeyCredentialProviderRequestTypeDef,
    CreateApiKeyCredentialProviderResponseTypeDef,
    CreateBrowserRequestTypeDef,
    CreateBrowserResponseTypeDef,
    CreateCodeInterpreterRequestTypeDef,
    CreateCodeInterpreterResponseTypeDef,
    CreateGatewayRequestTypeDef,
    CreateGatewayResponseTypeDef,
    CreateGatewayTargetRequestTypeDef,
    CreateGatewayTargetResponseTypeDef,
    CreateMemoryInputTypeDef,
    CreateMemoryOutputTypeDef,
    CreateOauth2CredentialProviderRequestTypeDef,
    CreateOauth2CredentialProviderResponseTypeDef,
    CreateWorkloadIdentityRequestTypeDef,
    CreateWorkloadIdentityResponseTypeDef,
    DeleteAgentRuntimeEndpointRequestTypeDef,
    DeleteAgentRuntimeEndpointResponseTypeDef,
    DeleteAgentRuntimeRequestTypeDef,
    DeleteAgentRuntimeResponseTypeDef,
    DeleteApiKeyCredentialProviderRequestTypeDef,
    DeleteBrowserRequestTypeDef,
    DeleteBrowserResponseTypeDef,
    DeleteCodeInterpreterRequestTypeDef,
    DeleteCodeInterpreterResponseTypeDef,
    DeleteGatewayRequestTypeDef,
    DeleteGatewayResponseTypeDef,
    DeleteGatewayTargetRequestTypeDef,
    DeleteGatewayTargetResponseTypeDef,
    DeleteMemoryInputTypeDef,
    DeleteMemoryOutputTypeDef,
    DeleteOauth2CredentialProviderRequestTypeDef,
    DeleteWorkloadIdentityRequestTypeDef,
    GetAgentRuntimeEndpointRequestTypeDef,
    GetAgentRuntimeEndpointResponseTypeDef,
    GetAgentRuntimeRequestTypeDef,
    GetAgentRuntimeResponseTypeDef,
    GetApiKeyCredentialProviderRequestTypeDef,
    GetApiKeyCredentialProviderResponseTypeDef,
    GetBrowserRequestTypeDef,
    GetBrowserResponseTypeDef,
    GetCodeInterpreterRequestTypeDef,
    GetCodeInterpreterResponseTypeDef,
    GetGatewayRequestTypeDef,
    GetGatewayResponseTypeDef,
    GetGatewayTargetRequestTypeDef,
    GetGatewayTargetResponseTypeDef,
    GetMemoryInputTypeDef,
    GetMemoryOutputTypeDef,
    GetOauth2CredentialProviderRequestTypeDef,
    GetOauth2CredentialProviderResponseTypeDef,
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
    ListBrowsersRequestTypeDef,
    ListBrowsersResponseTypeDef,
    ListCodeInterpretersRequestTypeDef,
    ListCodeInterpretersResponseTypeDef,
    ListGatewaysRequestTypeDef,
    ListGatewaysResponseTypeDef,
    ListGatewayTargetsRequestTypeDef,
    ListGatewayTargetsResponseTypeDef,
    ListMemoriesInputTypeDef,
    ListMemoriesOutputTypeDef,
    ListOauth2CredentialProvidersRequestTypeDef,
    ListOauth2CredentialProvidersResponseTypeDef,
    ListWorkloadIdentitiesRequestTypeDef,
    ListWorkloadIdentitiesResponseTypeDef,
    SetTokenVaultCMKRequestTypeDef,
    SetTokenVaultCMKResponseTypeDef,
    UpdateAgentRuntimeEndpointRequestTypeDef,
    UpdateAgentRuntimeEndpointResponseTypeDef,
    UpdateAgentRuntimeRequestTypeDef,
    UpdateAgentRuntimeResponseTypeDef,
    UpdateApiKeyCredentialProviderRequestTypeDef,
    UpdateApiKeyCredentialProviderResponseTypeDef,
    UpdateGatewayRequestTypeDef,
    UpdateGatewayResponseTypeDef,
    UpdateGatewayTargetRequestTypeDef,
    UpdateGatewayTargetResponseTypeDef,
    UpdateMemoryInputTypeDef,
    UpdateMemoryOutputTypeDef,
    UpdateOauth2CredentialProviderRequestTypeDef,
    UpdateOauth2CredentialProviderResponseTypeDef,
    UpdateWorkloadIdentityRequestTypeDef,
    UpdateWorkloadIdentityResponseTypeDef,
)
from .waiter import MemoryCreatedWaiter

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("BedrockAgentCoreControlPlaneFrontingLayerClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DecryptionFailure: Type[BotocoreClientError]
    EncryptionFailure: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceLimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottledException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class BedrockAgentCoreControlPlaneFrontingLayerClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control.html#BedrockAgentCoreControlPlaneFrontingLayer.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BedrockAgentCoreControlPlaneFrontingLayerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control.html#BedrockAgentCoreControlPlaneFrontingLayer.Client)
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

    def create_agent_runtime(
        self, **kwargs: Unpack[CreateAgentRuntimeRequestTypeDef]
    ) -> CreateAgentRuntimeResponseTypeDef:
        """
        Creates an Amazon Secure Agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_agent_runtime.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_agent_runtime)
        """

    def create_agent_runtime_endpoint(
        self, **kwargs: Unpack[CreateAgentRuntimeEndpointRequestTypeDef]
    ) -> CreateAgentRuntimeEndpointResponseTypeDef:
        """
        Creates an Amazon Secure AgentEndpoint.

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

    def create_code_interpreter(
        self, **kwargs: Unpack[CreateCodeInterpreterRequestTypeDef]
    ) -> CreateCodeInterpreterResponseTypeDef:
        """
        Creates a custom code interpreter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_code_interpreter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_code_interpreter)
        """

    def create_gateway(
        self, **kwargs: Unpack[CreateGatewayRequestTypeDef]
    ) -> CreateGatewayResponseTypeDef:
        """
        Creates a gateway for Amazon Bedrock Agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_gateway.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_gateway)
        """

    def create_gateway_target(
        self, **kwargs: Unpack[CreateGatewayTargetRequestTypeDef]
    ) -> CreateGatewayTargetResponseTypeDef:
        """
        Creates a target for a gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/create_gateway_target.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#create_gateway_target)
        """

    def create_memory(
        self, **kwargs: Unpack[CreateMemoryInputTypeDef]
    ) -> CreateMemoryOutputTypeDef:
        """
        Creates a new memory.

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
        Deletes an Amazon Secure Agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_agent_runtime.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_agent_runtime)
        """

    def delete_agent_runtime_endpoint(
        self, **kwargs: Unpack[DeleteAgentRuntimeEndpointRequestTypeDef]
    ) -> DeleteAgentRuntimeEndpointResponseTypeDef:
        """
        Deletes an Amazon Secure AgentEndpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_agent_runtime_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_agent_runtime_endpoint)
        """

    def delete_api_key_credential_provider(
        self, **kwargs: Unpack[DeleteApiKeyCredentialProviderRequestTypeDef]
    ) -> Dict[str, Any]:
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

    def delete_code_interpreter(
        self, **kwargs: Unpack[DeleteCodeInterpreterRequestTypeDef]
    ) -> DeleteCodeInterpreterResponseTypeDef:
        """
        Deletes a custom code interpreter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_code_interpreter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_code_interpreter)
        """

    def delete_gateway(
        self, **kwargs: Unpack[DeleteGatewayRequestTypeDef]
    ) -> DeleteGatewayResponseTypeDef:
        """
        Deletes a Gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_gateway.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_gateway)
        """

    def delete_gateway_target(
        self, **kwargs: Unpack[DeleteGatewayTargetRequestTypeDef]
    ) -> DeleteGatewayTargetResponseTypeDef:
        """
        Deletes a Gateway Target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_gateway_target.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_gateway_target)
        """

    def delete_memory(
        self, **kwargs: Unpack[DeleteMemoryInputTypeDef]
    ) -> DeleteMemoryOutputTypeDef:
        """
        Deletes a memory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_memory.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_memory)
        """

    def delete_oauth2_credential_provider(
        self, **kwargs: Unpack[DeleteOauth2CredentialProviderRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an OAuth2 credential provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_oauth2_credential_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_oauth2_credential_provider)
        """

    def delete_workload_identity(
        self, **kwargs: Unpack[DeleteWorkloadIdentityRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a workload identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/delete_workload_identity.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#delete_workload_identity)
        """

    def get_agent_runtime(
        self, **kwargs: Unpack[GetAgentRuntimeRequestTypeDef]
    ) -> GetAgentRuntimeResponseTypeDef:
        """
        Gets an Amazon Secure Agent.

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

    def get_code_interpreter(
        self, **kwargs: Unpack[GetCodeInterpreterRequestTypeDef]
    ) -> GetCodeInterpreterResponseTypeDef:
        """
        Gets information about a custom code interpreter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_code_interpreter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_code_interpreter)
        """

    def get_gateway(self, **kwargs: Unpack[GetGatewayRequestTypeDef]) -> GetGatewayResponseTypeDef:
        """
        Retrieves information about a specific Gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_gateway.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_gateway)
        """

    def get_gateway_target(
        self, **kwargs: Unpack[GetGatewayTargetRequestTypeDef]
    ) -> GetGatewayTargetResponseTypeDef:
        """
        Retrieves information about a specific Gateway Target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_gateway_target.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_gateway_target)
        """

    def get_memory(self, **kwargs: Unpack[GetMemoryInputTypeDef]) -> GetMemoryOutputTypeDef:
        """
        Retrieve an existing memory.

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

    def list_gateway_targets(
        self, **kwargs: Unpack[ListGatewayTargetsRequestTypeDef]
    ) -> ListGatewayTargetsResponseTypeDef:
        """
        Lists all targets for a specific Gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_gateway_targets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_gateway_targets)
        """

    def list_gateways(
        self, **kwargs: Unpack[ListGatewaysRequestTypeDef]
    ) -> ListGatewaysResponseTypeDef:
        """
        Lists all Gateways in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_gateways.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_gateways)
        """

    def list_memories(
        self, **kwargs: Unpack[ListMemoriesInputTypeDef]
    ) -> ListMemoriesOutputTypeDef:
        """
        Lists the memory present.

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

    def list_workload_identities(
        self, **kwargs: Unpack[ListWorkloadIdentitiesRequestTypeDef]
    ) -> ListWorkloadIdentitiesResponseTypeDef:
        """
        Lists all workload identities in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/list_workload_identities.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#list_workload_identities)
        """

    def set_token_vault_cmk(
        self, **kwargs: Unpack[SetTokenVaultCMKRequestTypeDef]
    ) -> SetTokenVaultCMKResponseTypeDef:
        """
        Sets the customer master key (CMK) for a token vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/set_token_vault_cmk.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#set_token_vault_cmk)
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
        Updates an existing Amazon Secure AgentEndpoint.

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

    def update_gateway(
        self, **kwargs: Unpack[UpdateGatewayRequestTypeDef]
    ) -> UpdateGatewayResponseTypeDef:
        """
        Updates an existing Gateway.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_gateway.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_gateway)
        """

    def update_gateway_target(
        self, **kwargs: Unpack[UpdateGatewayTargetRequestTypeDef]
    ) -> UpdateGatewayTargetResponseTypeDef:
        """
        Updates an existing Gateway Target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/update_gateway_target.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#update_gateway_target)
        """

    def update_memory(
        self, **kwargs: Unpack[UpdateMemoryInputTypeDef]
    ) -> UpdateMemoryOutputTypeDef:
        """
        Update memory.

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
        self, operation_name: Literal["list_workload_identities"]
    ) -> ListWorkloadIdentitiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_paginator)
        """

    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["memory_created"]
    ) -> MemoryCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/client/#get_waiter)
        """
