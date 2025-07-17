"""
Main interface for bedrock-agentcore-control service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_bedrock_agentcore_control import (
        BedrockAgentCoreControlPlaneFrontingLayerClient,
        Client,
        ListAgentRuntimeEndpointsPaginator,
        ListAgentRuntimeVersionsPaginator,
        ListAgentRuntimesPaginator,
        ListApiKeyCredentialProvidersPaginator,
        ListBrowsersPaginator,
        ListCodeInterpretersPaginator,
        ListGatewayTargetsPaginator,
        ListGatewaysPaginator,
        ListMemoriesPaginator,
        ListOauth2CredentialProvidersPaginator,
        ListWorkloadIdentitiesPaginator,
        MemoryCreatedWaiter,
    )

    session = Session()
    client: BedrockAgentCoreControlPlaneFrontingLayerClient = session.client("bedrock-agentcore-control")

    memory_created_waiter: MemoryCreatedWaiter = client.get_waiter("memory_created")

    list_agent_runtime_endpoints_paginator: ListAgentRuntimeEndpointsPaginator = client.get_paginator("list_agent_runtime_endpoints")
    list_agent_runtime_versions_paginator: ListAgentRuntimeVersionsPaginator = client.get_paginator("list_agent_runtime_versions")
    list_agent_runtimes_paginator: ListAgentRuntimesPaginator = client.get_paginator("list_agent_runtimes")
    list_api_key_credential_providers_paginator: ListApiKeyCredentialProvidersPaginator = client.get_paginator("list_api_key_credential_providers")
    list_browsers_paginator: ListBrowsersPaginator = client.get_paginator("list_browsers")
    list_code_interpreters_paginator: ListCodeInterpretersPaginator = client.get_paginator("list_code_interpreters")
    list_gateway_targets_paginator: ListGatewayTargetsPaginator = client.get_paginator("list_gateway_targets")
    list_gateways_paginator: ListGatewaysPaginator = client.get_paginator("list_gateways")
    list_memories_paginator: ListMemoriesPaginator = client.get_paginator("list_memories")
    list_oauth2_credential_providers_paginator: ListOauth2CredentialProvidersPaginator = client.get_paginator("list_oauth2_credential_providers")
    list_workload_identities_paginator: ListWorkloadIdentitiesPaginator = client.get_paginator("list_workload_identities")
    ```
"""

from .client import BedrockAgentCoreControlPlaneFrontingLayerClient
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
from .waiter import MemoryCreatedWaiter

Client = BedrockAgentCoreControlPlaneFrontingLayerClient

__all__ = (
    "BedrockAgentCoreControlPlaneFrontingLayerClient",
    "Client",
    "ListAgentRuntimeEndpointsPaginator",
    "ListAgentRuntimeVersionsPaginator",
    "ListAgentRuntimesPaginator",
    "ListApiKeyCredentialProvidersPaginator",
    "ListBrowsersPaginator",
    "ListCodeInterpretersPaginator",
    "ListGatewayTargetsPaginator",
    "ListGatewaysPaginator",
    "ListMemoriesPaginator",
    "ListOauth2CredentialProvidersPaginator",
    "ListWorkloadIdentitiesPaginator",
    "MemoryCreatedWaiter",
)
