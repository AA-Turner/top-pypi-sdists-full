"""
Type annotations for cloudcontrol service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudcontrol.client import CloudControlApiClient
    from types_aiobotocore_cloudcontrol.waiter import (
        ResourceRequestSuccessWaiter,
    )

    session = get_session()
    async with session.create_client("cloudcontrol") as client:
        client: CloudControlApiClient

        resource_request_success_waiter: ResourceRequestSuccessWaiter = client.get_waiter("resource_request_success")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import GetResourceRequestStatusInputWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ResourceRequestSuccessWaiter",)


class ResourceRequestSuccessWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/waiter/ResourceRequestSuccess.html#CloudControlApi.Waiter.ResourceRequestSuccess)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/waiters/#resourcerequestsuccesswaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetResourceRequestStatusInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudcontrol/waiter/ResourceRequestSuccess.html#CloudControlApi.Waiter.ResourceRequestSuccess.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudcontrol/waiters/#resourcerequestsuccesswaiter)
        """
