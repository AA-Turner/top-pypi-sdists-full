"""
Type annotations for lambda-core service client waiters.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_lambda_core.client import LambdaCoreClient
    from mypy_boto3_lambda_core.waiter import (
        RuntimeAliasActiveWaiter,
        RuntimeVersionActiveWaiter,
    )

    session = Session()
    client: LambdaCoreClient = session.client("lambda-core")

    runtime_alias_active_waiter: RuntimeAliasActiveWaiter = client.get_waiter("runtime_alias_active")
    runtime_version_active_waiter: RuntimeVersionActiveWaiter = client.get_waiter("runtime_version_active")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import GetRuntimeAliasRequestWaitTypeDef, GetRuntimeVersionRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("RuntimeAliasActiveWaiter", "RuntimeVersionActiveWaiter")

class RuntimeAliasActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/waiter/RuntimeAliasActive.html#LambdaCore.Waiter.RuntimeAliasActive)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/waiters/#runtimealiasactivewaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRuntimeAliasRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/waiter/RuntimeAliasActive.html#LambdaCore.Waiter.RuntimeAliasActive.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/waiters/#runtimealiasactivewaiter)
        """

class RuntimeVersionActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/waiter/RuntimeVersionActive.html#LambdaCore.Waiter.RuntimeVersionActive)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/waiters/#runtimeversionactivewaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetRuntimeVersionRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-core/waiter/RuntimeVersionActive.html#LambdaCore.Waiter.RuntimeVersionActive.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_core/waiters/#runtimeversionactivewaiter)
        """
