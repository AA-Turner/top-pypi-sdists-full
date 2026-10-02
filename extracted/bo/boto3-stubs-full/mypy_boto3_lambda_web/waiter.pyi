"""
Type annotations for lambda-web service client waiters.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_web/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_lambda_web.client import LambdaWebClient
    from mypy_boto3_lambda_web.waiter import (
        WebFunctionActiveWaiter,
        WebFunctionDeletedWaiter,
        WebFunctionEndpointActiveWaiter,
        WebFunctionEndpointDeletedWaiter,
        WebFunctionEndpointUpdatedWaiter,
        WebFunctionRevisionActiveWaiter,
    )

    session = Session()
    client: LambdaWebClient = session.client("lambda-web")

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

from botocore.waiter import Waiter

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

class WebFunctionActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionActive.html#LambdaWeb.Waiter.WebFunctionActive)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_web/waiters/#webfunctionactivewaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetWebFunctionRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionActive.html#LambdaWeb.Waiter.WebFunctionActive.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_web/waiters/#webfunctionactivewaiter)
        """

class WebFunctionDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionDeleted.html#LambdaWeb.Waiter.WebFunctionDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_web/waiters/#webfunctiondeletedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetWebFunctionRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionDeleted.html#LambdaWeb.Waiter.WebFunctionDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_web/waiters/#webfunctiondeletedwaiter)
        """

class WebFunctionEndpointActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionEndpointActive.html#LambdaWeb.Waiter.WebFunctionEndpointActive)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_web/waiters/#webfunctionendpointactivewaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetWebFunctionEndpointRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionEndpointActive.html#LambdaWeb.Waiter.WebFunctionEndpointActive.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_web/waiters/#webfunctionendpointactivewaiter)
        """

class WebFunctionEndpointDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionEndpointDeleted.html#LambdaWeb.Waiter.WebFunctionEndpointDeleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_web/waiters/#webfunctionendpointdeletedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetWebFunctionEndpointRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionEndpointDeleted.html#LambdaWeb.Waiter.WebFunctionEndpointDeleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_web/waiters/#webfunctionendpointdeletedwaiter)
        """

class WebFunctionEndpointUpdatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionEndpointUpdated.html#LambdaWeb.Waiter.WebFunctionEndpointUpdated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_web/waiters/#webfunctionendpointupdatedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetWebFunctionEndpointRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionEndpointUpdated.html#LambdaWeb.Waiter.WebFunctionEndpointUpdated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_web/waiters/#webfunctionendpointupdatedwaiter)
        """

class WebFunctionRevisionActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionRevisionActive.html#LambdaWeb.Waiter.WebFunctionRevisionActive)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_web/waiters/#webfunctionrevisionactivewaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetWebFunctionRevisionRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/waiter/WebFunctionRevisionActive.html#LambdaWeb.Waiter.WebFunctionRevisionActive.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_web/waiters/#webfunctionrevisionactivewaiter)
        """
