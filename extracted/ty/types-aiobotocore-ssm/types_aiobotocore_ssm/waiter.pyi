"""
Type annotations for ssm service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ssm.client import SSMClient
    from types_aiobotocore_ssm.waiter import (
        CommandExecutedWaiter,
    )

    session = get_session()
    async with session.create_client("ssm") as client:
        client: SSMClient

        command_executed_waiter: CommandExecutedWaiter = client.get_waiter("command_executed")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import GetCommandInvocationRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("CommandExecutedWaiter",)

class CommandExecutedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/waiter/CommandExecuted.html#SSM.Waiter.CommandExecuted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/waiters/#commandexecutedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetCommandInvocationRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/waiter/CommandExecuted.html#SSM.Waiter.CommandExecuted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/waiters/#commandexecutedwaiter)
        """
