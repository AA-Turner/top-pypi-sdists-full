"""
Type annotations for ssm-incidents service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ssm_incidents.client import SSMIncidentsClient
    from types_aiobotocore_ssm_incidents.waiter import (
        WaitForReplicationSetActiveWaiter,
        WaitForReplicationSetDeletedWaiter,
    )

    session = get_session()
    async with session.create_client("ssm-incidents") as client:
        client: SSMIncidentsClient

        wait_for_replication_set_active_waiter: WaitForReplicationSetActiveWaiter = client.get_waiter("wait_for_replication_set_active")
        wait_for_replication_set_deleted_waiter: WaitForReplicationSetDeletedWaiter = client.get_waiter("wait_for_replication_set_deleted")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import GetReplicationSetInputWaitExtraTypeDef, GetReplicationSetInputWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("WaitForReplicationSetActiveWaiter", "WaitForReplicationSetDeletedWaiter")


class WaitForReplicationSetActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/waiter/WaitForReplicationSetActive.html#SSMIncidents.Waiter.WaitForReplicationSetActive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/waiters/#waitforreplicationsetactivewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetReplicationSetInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/waiter/WaitForReplicationSetActive.html#SSMIncidents.Waiter.WaitForReplicationSetActive.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/waiters/#waitforreplicationsetactivewaiter)
        """


class WaitForReplicationSetDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/waiter/WaitForReplicationSetDeleted.html#SSMIncidents.Waiter.WaitForReplicationSetDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/waiters/#waitforreplicationsetdeletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetReplicationSetInputWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/waiter/WaitForReplicationSetDeleted.html#SSMIncidents.Waiter.WaitForReplicationSetDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/waiters/#waitforreplicationsetdeletedwaiter)
        """
