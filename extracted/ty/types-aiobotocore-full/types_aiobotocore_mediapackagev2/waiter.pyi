"""
Type annotations for mediapackagev2 service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackagev2/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mediapackagev2.client import Mediapackagev2Client
    from types_aiobotocore_mediapackagev2.waiter import (
        HarvestJobFinishedWaiter,
    )

    session = get_session()
    async with session.create_client("mediapackagev2") as client:
        client: Mediapackagev2Client

        harvest_job_finished_waiter: HarvestJobFinishedWaiter = client.get_waiter("harvest_job_finished")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import GetHarvestJobRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("HarvestJobFinishedWaiter",)

class HarvestJobFinishedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2/waiter/HarvestJobFinished.html#Mediapackagev2.Waiter.HarvestJobFinished)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackagev2/waiters/#harvestjobfinishedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetHarvestJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediapackagev2/waiter/HarvestJobFinished.html#Mediapackagev2.Waiter.HarvestJobFinished.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediapackagev2/waiters/#harvestjobfinishedwaiter)
        """
