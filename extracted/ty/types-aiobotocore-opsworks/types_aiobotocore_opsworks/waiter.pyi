"""
Type annotations for opsworks service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_opsworks.client import OpsWorksClient
    from types_aiobotocore_opsworks.waiter import (
        AppExistsWaiter,
        DeploymentSuccessfulWaiter,
        InstanceOnlineWaiter,
        InstanceRegisteredWaiter,
        InstanceStoppedWaiter,
        InstanceTerminatedWaiter,
    )

    session = get_session()
    async with session.create_client("opsworks") as client:
        client: OpsWorksClient

        app_exists_waiter: AppExistsWaiter = client.get_waiter("app_exists")
        deployment_successful_waiter: DeploymentSuccessfulWaiter = client.get_waiter("deployment_successful")
        instance_online_waiter: InstanceOnlineWaiter = client.get_waiter("instance_online")
        instance_registered_waiter: InstanceRegisteredWaiter = client.get_waiter("instance_registered")
        instance_stopped_waiter: InstanceStoppedWaiter = client.get_waiter("instance_stopped")
        instance_terminated_waiter: InstanceTerminatedWaiter = client.get_waiter("instance_terminated")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeAppsRequestWaitTypeDef,
    DescribeDeploymentsRequestWaitTypeDef,
    DescribeInstancesRequestWaitExtraExtraExtraTypeDef,
    DescribeInstancesRequestWaitExtraExtraTypeDef,
    DescribeInstancesRequestWaitExtraTypeDef,
    DescribeInstancesRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "AppExistsWaiter",
    "DeploymentSuccessfulWaiter",
    "InstanceOnlineWaiter",
    "InstanceRegisteredWaiter",
    "InstanceStoppedWaiter",
    "InstanceTerminatedWaiter",
)

class AppExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/waiter/AppExists.html#OpsWorks.Waiter.AppExists)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#appexistswaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAppsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/waiter/AppExists.html#OpsWorks.Waiter.AppExists.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#appexistswaiter)
        """

class DeploymentSuccessfulWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/waiter/DeploymentSuccessful.html#OpsWorks.Waiter.DeploymentSuccessful)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#deploymentsuccessfulwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDeploymentsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/waiter/DeploymentSuccessful.html#OpsWorks.Waiter.DeploymentSuccessful.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#deploymentsuccessfulwaiter)
        """

class InstanceOnlineWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/waiter/InstanceOnline.html#OpsWorks.Waiter.InstanceOnline)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#instanceonlinewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInstancesRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/waiter/InstanceOnline.html#OpsWorks.Waiter.InstanceOnline.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#instanceonlinewaiter)
        """

class InstanceRegisteredWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/waiter/InstanceRegistered.html#OpsWorks.Waiter.InstanceRegistered)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#instanceregisteredwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInstancesRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/waiter/InstanceRegistered.html#OpsWorks.Waiter.InstanceRegistered.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#instanceregisteredwaiter)
        """

class InstanceStoppedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/waiter/InstanceStopped.html#OpsWorks.Waiter.InstanceStopped)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#instancestoppedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInstancesRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/waiter/InstanceStopped.html#OpsWorks.Waiter.InstanceStopped.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#instancestoppedwaiter)
        """

class InstanceTerminatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/waiter/InstanceTerminated.html#OpsWorks.Waiter.InstanceTerminated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#instanceterminatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInstancesRequestWaitExtraExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/waiter/InstanceTerminated.html#OpsWorks.Waiter.InstanceTerminated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/waiters/#instanceterminatedwaiter)
        """
