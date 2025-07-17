"""
Type annotations for bedrock-agentcore-control service client waiters.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_bedrock_agentcore_control.client import BedrockAgentCoreControlPlaneFrontingLayerClient
    from types_boto3_bedrock_agentcore_control.waiter import (
        MemoryCreatedWaiter,
    )

    session = Session()
    client: BedrockAgentCoreControlPlaneFrontingLayerClient = session.client("bedrock-agentcore-control")

    memory_created_waiter: MemoryCreatedWaiter = client.get_waiter("memory_created")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import GetMemoryInputWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("MemoryCreatedWaiter",)

class MemoryCreatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/waiter/MemoryCreated.html#BedrockAgentCoreControlPlaneFrontingLayer.Waiter.MemoryCreated)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/waiters/#memorycreatedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetMemoryInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/waiter/MemoryCreated.html#BedrockAgentCoreControlPlaneFrontingLayer.Waiter.MemoryCreated.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/waiters/#memorycreatedwaiter)
        """
