"""
Type annotations for lambda service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_lambda.client import LambdaClient
    from types_aiobotocore_lambda.waiter import (
        FunctionActiveV2Waiter,
        FunctionActiveWaiter,
        FunctionExistsWaiter,
        FunctionUpdatedV2Waiter,
        FunctionUpdatedWaiter,
        PublishedVersionActiveWaiter,
    )

    session = get_session()
    async with session.create_client("lambda") as client:
        client: LambdaClient

        function_active_v2_waiter: FunctionActiveV2Waiter = client.get_waiter("function_active_v2")
        function_active_waiter: FunctionActiveWaiter = client.get_waiter("function_active")
        function_exists_waiter: FunctionExistsWaiter = client.get_waiter("function_exists")
        function_updated_v2_waiter: FunctionUpdatedV2Waiter = client.get_waiter("function_updated_v2")
        function_updated_waiter: FunctionUpdatedWaiter = client.get_waiter("function_updated")
        published_version_active_waiter: PublishedVersionActiveWaiter = client.get_waiter("published_version_active")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    GetFunctionConfigurationRequestWaitExtraExtraTypeDef,
    GetFunctionConfigurationRequestWaitExtraTypeDef,
    GetFunctionConfigurationRequestWaitTypeDef,
    GetFunctionRequestWaitExtraExtraTypeDef,
    GetFunctionRequestWaitExtraTypeDef,
    GetFunctionRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "FunctionActiveV2Waiter",
    "FunctionActiveWaiter",
    "FunctionExistsWaiter",
    "FunctionUpdatedV2Waiter",
    "FunctionUpdatedWaiter",
    "PublishedVersionActiveWaiter",
)


class FunctionActiveV2Waiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/waiter/FunctionActiveV2.html#Lambda.Waiter.FunctionActiveV2)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#functionactivev2waiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetFunctionRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/waiter/FunctionActiveV2.html#Lambda.Waiter.FunctionActiveV2.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#functionactivev2waiter)
        """


class FunctionActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/waiter/FunctionActive.html#Lambda.Waiter.FunctionActive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#functionactivewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetFunctionConfigurationRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/waiter/FunctionActive.html#Lambda.Waiter.FunctionActive.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#functionactivewaiter)
        """


class FunctionExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/waiter/FunctionExists.html#Lambda.Waiter.FunctionExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#functionexistswaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetFunctionRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/waiter/FunctionExists.html#Lambda.Waiter.FunctionExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#functionexistswaiter)
        """


class FunctionUpdatedV2Waiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/waiter/FunctionUpdatedV2.html#Lambda.Waiter.FunctionUpdatedV2)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#functionupdatedv2waiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetFunctionRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/waiter/FunctionUpdatedV2.html#Lambda.Waiter.FunctionUpdatedV2.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#functionupdatedv2waiter)
        """


class FunctionUpdatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/waiter/FunctionUpdated.html#Lambda.Waiter.FunctionUpdated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#functionupdatedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetFunctionConfigurationRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/waiter/FunctionUpdated.html#Lambda.Waiter.FunctionUpdated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#functionupdatedwaiter)
        """


class PublishedVersionActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/waiter/PublishedVersionActive.html#Lambda.Waiter.PublishedVersionActive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#publishedversionactivewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetFunctionConfigurationRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda/waiter/PublishedVersionActive.html#Lambda.Waiter.PublishedVersionActive.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#publishedversionactivewaiter)
        """
