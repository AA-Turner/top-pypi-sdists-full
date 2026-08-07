"""
Type annotations for agent-registry-control service client waiters.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_agent_registry_control/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_agent_registry_control.client import AgentRegistryControlClient
    from types_boto3_agent_registry_control.waiter import (
        RegistryReadyWaiter,
        RegistryRecordApprovedWaiter,
    )

    session = Session()
    client: AgentRegistryControlClient = session.client("agent-registry-control")

    registry_ready_waiter: RegistryReadyWaiter = client.get_waiter("registry_ready")
    registry_record_approved_waiter: RegistryRecordApprovedWaiter = client.get_waiter("registry_record_approved")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import GetRegistryRecordRequestWaitTypeDef, GetRegistryRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("RegistryReadyWaiter", "RegistryRecordApprovedWaiter")


class RegistryReadyWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/waiter/RegistryReady.html#AgentRegistryControl.Waiter.RegistryReady)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_agent_registry_control/waiters/#registryreadywaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRegistryRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/waiter/RegistryReady.html#AgentRegistryControl.Waiter.RegistryReady.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_agent_registry_control/waiters/#registryreadywaiter)
        """


class RegistryRecordApprovedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/waiter/RegistryRecordApproved.html#AgentRegistryControl.Waiter.RegistryRecordApproved)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_agent_registry_control/waiters/#registryrecordapprovedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRegistryRecordRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/waiter/RegistryRecordApproved.html#AgentRegistryControl.Waiter.RegistryRecordApproved.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_agent_registry_control/waiters/#registryrecordapprovedwaiter)
        """
