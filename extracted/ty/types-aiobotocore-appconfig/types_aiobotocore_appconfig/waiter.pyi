"""
Type annotations for appconfig service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_appconfig.client import AppConfigClient
    from types_aiobotocore_appconfig.waiter import (
        DeploymentCompleteWaiter,
        EnvironmentReadyForDeploymentWaiter,
    )

    session = get_session()
    async with session.create_client("appconfig") as client:
        client: AppConfigClient

        deployment_complete_waiter: DeploymentCompleteWaiter = client.get_waiter("deployment_complete")
        environment_ready_for_deployment_waiter: EnvironmentReadyForDeploymentWaiter = client.get_waiter("environment_ready_for_deployment")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import GetDeploymentRequestWaitTypeDef, GetEnvironmentRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("DeploymentCompleteWaiter", "EnvironmentReadyForDeploymentWaiter")

class DeploymentCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/waiter/DeploymentComplete.html#AppConfig.Waiter.DeploymentComplete)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/waiters/#deploymentcompletewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetDeploymentRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/waiter/DeploymentComplete.html#AppConfig.Waiter.DeploymentComplete.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/waiters/#deploymentcompletewaiter)
        """

class EnvironmentReadyForDeploymentWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/waiter/EnvironmentReadyForDeployment.html#AppConfig.Waiter.EnvironmentReadyForDeployment)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/waiters/#environmentreadyfordeploymentwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetEnvironmentRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appconfig/waiter/EnvironmentReadyForDeployment.html#AppConfig.Waiter.EnvironmentReadyForDeployment.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appconfig/waiters/#environmentreadyfordeploymentwaiter)
        """
