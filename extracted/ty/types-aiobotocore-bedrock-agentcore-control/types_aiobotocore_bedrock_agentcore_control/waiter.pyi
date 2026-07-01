"""
Type annotations for bedrock-agentcore-control service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore_control/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_bedrock_agentcore_control.client import BedrockAgentCoreControlClient
    from types_aiobotocore_bedrock_agentcore_control.waiter import (
        MemoryCreatedWaiter,
        PolicyActiveWaiter,
        PolicyDeletedWaiter,
        PolicyEngineActiveWaiter,
        PolicyEngineDeletedWaiter,
        PolicyGenerationCompletedWaiter,
    )

    session = get_session()
    async with session.create_client("bedrock-agentcore-control") as client:
        client: BedrockAgentCoreControlClient

        memory_created_waiter: MemoryCreatedWaiter = client.get_waiter("memory_created")
        policy_active_waiter: PolicyActiveWaiter = client.get_waiter("policy_active")
        policy_deleted_waiter: PolicyDeletedWaiter = client.get_waiter("policy_deleted")
        policy_engine_active_waiter: PolicyEngineActiveWaiter = client.get_waiter("policy_engine_active")
        policy_engine_deleted_waiter: PolicyEngineDeletedWaiter = client.get_waiter("policy_engine_deleted")
        policy_generation_completed_waiter: PolicyGenerationCompletedWaiter = client.get_waiter("policy_generation_completed")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    GetMemoryInputWaitTypeDef,
    GetPolicyEngineRequestWaitExtraTypeDef,
    GetPolicyEngineRequestWaitTypeDef,
    GetPolicyGenerationRequestWaitTypeDef,
    GetPolicyRequestWaitExtraTypeDef,
    GetPolicyRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "MemoryCreatedWaiter",
    "PolicyActiveWaiter",
    "PolicyDeletedWaiter",
    "PolicyEngineActiveWaiter",
    "PolicyEngineDeletedWaiter",
    "PolicyGenerationCompletedWaiter",
)

class MemoryCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/waiter/MemoryCreated.html#BedrockAgentCoreControl.Waiter.MemoryCreated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore_control/waiters/#memorycreatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetMemoryInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/waiter/MemoryCreated.html#BedrockAgentCoreControl.Waiter.MemoryCreated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore_control/waiters/#memorycreatedwaiter)
        """

class PolicyActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/waiter/PolicyActive.html#BedrockAgentCoreControl.Waiter.PolicyActive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore_control/waiters/#policyactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetPolicyRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/waiter/PolicyActive.html#BedrockAgentCoreControl.Waiter.PolicyActive.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore_control/waiters/#policyactivewaiter)
        """

class PolicyDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/waiter/PolicyDeleted.html#BedrockAgentCoreControl.Waiter.PolicyDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore_control/waiters/#policydeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetPolicyRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/waiter/PolicyDeleted.html#BedrockAgentCoreControl.Waiter.PolicyDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore_control/waiters/#policydeletedwaiter)
        """

class PolicyEngineActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/waiter/PolicyEngineActive.html#BedrockAgentCoreControl.Waiter.PolicyEngineActive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore_control/waiters/#policyengineactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetPolicyEngineRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/waiter/PolicyEngineActive.html#BedrockAgentCoreControl.Waiter.PolicyEngineActive.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore_control/waiters/#policyengineactivewaiter)
        """

class PolicyEngineDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/waiter/PolicyEngineDeleted.html#BedrockAgentCoreControl.Waiter.PolicyEngineDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore_control/waiters/#policyenginedeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetPolicyEngineRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/waiter/PolicyEngineDeleted.html#BedrockAgentCoreControl.Waiter.PolicyEngineDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore_control/waiters/#policyenginedeletedwaiter)
        """

class PolicyGenerationCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/waiter/PolicyGenerationCompleted.html#BedrockAgentCoreControl.Waiter.PolicyGenerationCompleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore_control/waiters/#policygenerationcompletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetPolicyGenerationRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/waiter/PolicyGenerationCompleted.html#BedrockAgentCoreControl.Waiter.PolicyGenerationCompleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore_control/waiters/#policygenerationcompletedwaiter)
        """
