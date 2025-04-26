"""
Type annotations for glacier service client waiters.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_glacier.client import GlacierClient
    from mypy_boto3_glacier.waiter import (
        VaultExistsWaiter,
        VaultNotExistsWaiter,
    )

    session = Session()
    client: GlacierClient = session.client("glacier")

    vault_exists_waiter: VaultExistsWaiter = client.get_waiter("vault_exists")
    vault_not_exists_waiter: VaultNotExistsWaiter = client.get_waiter("vault_not_exists")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import DescribeVaultInputWaitExtraTypeDef, DescribeVaultInputWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("VaultExistsWaiter", "VaultNotExistsWaiter")

class VaultExistsWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/waiter/VaultExists.html#Glacier.Waiter.VaultExists)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/waiters/#vaultexistswaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeVaultInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/waiter/VaultExists.html#Glacier.Waiter.VaultExists.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/waiters/#vaultexistswaiter)
        """

class VaultNotExistsWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/waiter/VaultNotExists.html#Glacier.Waiter.VaultNotExists)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/waiters/#vaultnotexistswaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeVaultInputWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/waiter/VaultNotExists.html#Glacier.Waiter.VaultNotExists.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/waiters/#vaultnotexistswaiter)
        """
