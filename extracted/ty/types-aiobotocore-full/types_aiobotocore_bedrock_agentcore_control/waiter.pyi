"""
Type annotations for bedrock-agentcore-control service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore_control/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_bedrock_agentcore_control.client import BedrockAgentCoreControlPlaneFrontingLayerClient
    from types_aiobotocore_bedrock_agentcore_control.waiter import (
        MemoryCreatedWaiter,
    )

    session = get_session()
    async with session.create_client("bedrock-agentcore-control") as client:
        client: BedrockAgentCoreControlPlaneFrontingLayerClient

        memory_created_waiter: MemoryCreatedWaiter = client.get_waiter("memory_created")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import GetMemoryInputWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("MemoryCreatedWaiter",)

class MemoryCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/waiter/MemoryCreated.html#BedrockAgentCoreControlPlaneFrontingLayer.Waiter.MemoryCreated)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore_control/waiters/#memorycreatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetMemoryInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/waiter/MemoryCreated.html#BedrockAgentCoreControlPlaneFrontingLayer.Waiter.MemoryCreated.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore_control/waiters/#memorycreatedwaiter)
        """
