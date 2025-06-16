"""
Type annotations for codedeploy service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_codedeploy.client import CodeDeployClient
    from types_aiobotocore_codedeploy.waiter import (
        DeploymentSuccessfulWaiter,
    )

    session = get_session()
    async with session.create_client("codedeploy") as client:
        client: CodeDeployClient

        deployment_successful_waiter: DeploymentSuccessfulWaiter = client.get_waiter("deployment_successful")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import GetDeploymentInputWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("DeploymentSuccessfulWaiter",)


class DeploymentSuccessfulWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/waiter/DeploymentSuccessful.html#CodeDeploy.Waiter.DeploymentSuccessful)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/waiters/#deploymentsuccessfulwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetDeploymentInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codedeploy/waiter/DeploymentSuccessful.html#CodeDeploy.Waiter.DeploymentSuccessful.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codedeploy/waiters/#deploymentsuccessfulwaiter)
        """
