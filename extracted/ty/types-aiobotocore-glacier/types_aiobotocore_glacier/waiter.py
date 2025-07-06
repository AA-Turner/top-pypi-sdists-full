"""
Type annotations for glacier service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_glacier.client import GlacierClient
    from types_aiobotocore_glacier.waiter import (
        VaultExistsWaiter,
        VaultNotExistsWaiter,
    )

    session = get_session()
    async with session.create_client("glacier") as client:
        client: GlacierClient

        vault_exists_waiter: VaultExistsWaiter = client.get_waiter("vault_exists")
        vault_not_exists_waiter: VaultNotExistsWaiter = client.get_waiter("vault_not_exists")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import DescribeVaultInputWaitExtraTypeDef, DescribeVaultInputWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("VaultExistsWaiter", "VaultNotExistsWaiter")


class VaultExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/waiter/VaultExists.html#Glacier.Waiter.VaultExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/waiters/#vaultexistswaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeVaultInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/waiter/VaultExists.html#Glacier.Waiter.VaultExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/waiters/#vaultexistswaiter)
        """


class VaultNotExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/waiter/VaultNotExists.html#Glacier.Waiter.VaultNotExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/waiters/#vaultnotexistswaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeVaultInputWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/waiter/VaultNotExists.html#Glacier.Waiter.VaultNotExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/waiters/#vaultnotexistswaiter)
        """
