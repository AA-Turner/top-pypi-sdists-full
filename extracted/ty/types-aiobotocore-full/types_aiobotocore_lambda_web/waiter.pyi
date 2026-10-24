"""
Type annotations for lambda-web service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_lambda_web.client import LambdaWebClient
    from types_aiobotocore_lambda_web.waiter import (
        WebFunctionActiveWaiter,
        WebFunctionDeletedWaiter,
        WebFunctionEndpointActiveWaiter,
        WebFunctionEndpointDeletedWaiter,
        WebFunctionEndpointUpdatedWaiter,
        WebFunctionRevisionActiveWaiter,
    )

    session = get_session()
    async with session.create_client("lambda-web") as client:
        client: LambdaWebClient

        web_function_active_waiter: WebFunctionActiveWaiter = client.get_waiter("web_function_active")
        web_function_deleted_waiter: WebFunctionDeletedWaiter = client.get_waiter("web_function_deleted")
        web_function_endpoint_active_waiter: WebFunctionEndpointActiveWaiter = client.get_waiter("web_function_endpoint_active")
        web_function_endpoint_deleted_waiter: WebFunctionEndpointDeletedWaiter = client.get_waiter("web_function_endpoint_deleted")
        web_function_endpoint_updated_waiter: WebFunctionEndpointUpdatedWaiter = client.get_waiter("web_function_endpoint_updated")
        web_function_revision_active_waiter: WebFunctionRevisionActiveWaiter = client.get_waiter("web_function_revision_active")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    GetWebFunctionEndpointRequestWaitExtraExtraTypeDef,
    GetWebFunctionEndpointRequestWaitExtraTypeDef,
    GetWebFunctionEndpointRequestWaitTypeDef,
    GetWebFunctionRequestWaitExtraTypeDef,
    GetWebFunctionRequestWaitTypeDef,
    GetWebFunctionRevisionRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "WebFunctionActiveWaiter",
    "WebFunctionDeletedWaiter",
    "WebFunctionEndpointActiveWaiter",
    "WebFunctionEndpointDeletedWaiter",
    "WebFunctionEndpointUpdatedWaiter",
    "WebFunctionRevisionActiveWaiter",
)

class WebFunctionActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionActive.html#LambdaWeb.Waiter.WebFunctionActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/waiters/#webfunctionactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetWebFunctionRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionActive.html#LambdaWeb.Waiter.WebFunctionActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/waiters/#webfunctionactivewaiter)
        """

class WebFunctionDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionDeleted.html#LambdaWeb.Waiter.WebFunctionDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/waiters/#webfunctiondeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetWebFunctionRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionDeleted.html#LambdaWeb.Waiter.WebFunctionDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/waiters/#webfunctiondeletedwaiter)
        """

class WebFunctionEndpointActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionEndpointActive.html#LambdaWeb.Waiter.WebFunctionEndpointActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/waiters/#webfunctionendpointactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetWebFunctionEndpointRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionEndpointActive.html#LambdaWeb.Waiter.WebFunctionEndpointActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/waiters/#webfunctionendpointactivewaiter)
        """

class WebFunctionEndpointDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionEndpointDeleted.html#LambdaWeb.Waiter.WebFunctionEndpointDeleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/waiters/#webfunctionendpointdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetWebFunctionEndpointRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionEndpointDeleted.html#LambdaWeb.Waiter.WebFunctionEndpointDeleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/waiters/#webfunctionendpointdeletedwaiter)
        """

class WebFunctionEndpointUpdatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionEndpointUpdated.html#LambdaWeb.Waiter.WebFunctionEndpointUpdated)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/waiters/#webfunctionendpointupdatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetWebFunctionEndpointRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionEndpointUpdated.html#LambdaWeb.Waiter.WebFunctionEndpointUpdated.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/waiters/#webfunctionendpointupdatedwaiter)
        """

class WebFunctionRevisionActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionRevisionActive.html#LambdaWeb.Waiter.WebFunctionRevisionActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/waiters/#webfunctionrevisionactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetWebFunctionRevisionRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionRevisionActive.html#LambdaWeb.Waiter.WebFunctionRevisionActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/waiters/#webfunctionrevisionactivewaiter)
        """
