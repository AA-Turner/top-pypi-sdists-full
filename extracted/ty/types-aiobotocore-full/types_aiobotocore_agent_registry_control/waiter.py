"""
Type annotations for agent-registry-control service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_agent_registry_control.client import AgentRegistryControlClient
    from types_aiobotocore_agent_registry_control.waiter import (
        RegistryReadyWaiter,
        RegistryRecordApprovedWaiter,
    )

    session = get_session()
    async with session.create_client("agent-registry-control") as client:
        client: AgentRegistryControlClient

        registry_ready_waiter: RegistryReadyWaiter = client.get_waiter("registry_ready")
        registry_record_approved_waiter: RegistryRecordApprovedWaiter = client.get_waiter("registry_record_approved")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import GetRegistryRecordRequestWaitTypeDef, GetRegistryRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("RegistryReadyWaiter", "RegistryRecordApprovedWaiter")


class RegistryReadyWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/waiter/RegistryReady.html#AgentRegistryControl.Waiter.RegistryReady)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/waiters/#registryreadywaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRegistryRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/waiter/RegistryReady.html#AgentRegistryControl.Waiter.RegistryReady.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/waiters/#registryreadywaiter)
        """


class RegistryRecordApprovedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/waiter/RegistryRecordApproved.html#AgentRegistryControl.Waiter.RegistryRecordApproved)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/waiters/#registryrecordapprovedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRegistryRecordRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/waiter/RegistryRecordApproved.html#AgentRegistryControl.Waiter.RegistryRecordApproved.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/waiters/#registryrecordapprovedwaiter)
        """
