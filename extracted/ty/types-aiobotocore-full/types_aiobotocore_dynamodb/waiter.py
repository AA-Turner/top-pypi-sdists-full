"""
Type annotations for dynamodb service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_dynamodb.client import DynamoDBClient
    from types_aiobotocore_dynamodb.waiter import (
        TableExistsWaiter,
        TableNotExistsWaiter,
    )

    session = get_session()
    async with session.create_client("dynamodb") as client:
        client: DynamoDBClient

        table_exists_waiter: TableExistsWaiter = client.get_waiter("table_exists")
        table_not_exists_waiter: TableNotExistsWaiter = client.get_waiter("table_not_exists")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import DescribeTableInputWaitExtraTypeDef, DescribeTableInputWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("TableExistsWaiter", "TableNotExistsWaiter")


class TableExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/TableExists.html#DynamoDB.Waiter.TableExists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/waiters/#tableexistswaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTableInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/TableExists.html#DynamoDB.Waiter.TableExists.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/waiters/#tableexistswaiter)
        """


class TableNotExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/TableNotExists.html#DynamoDB.Waiter.TableNotExists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/waiters/#tablenotexistswaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTableInputWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/waiter/TableNotExists.html#DynamoDB.Waiter.TableNotExists.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_dynamodb/waiters/#tablenotexistswaiter)
        """
