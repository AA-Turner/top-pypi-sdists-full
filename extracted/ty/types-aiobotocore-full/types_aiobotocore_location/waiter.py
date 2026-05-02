"""
Type annotations for location service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_location.client import LocationServiceClient
    from types_aiobotocore_location.waiter import (
        JobCompletedWaiter,
    )

    session = get_session()
    async with session.create_client("location") as client:
        client: LocationServiceClient

        job_completed_waiter: JobCompletedWaiter = client.get_waiter("job_completed")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import GetJobRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("JobCompletedWaiter",)


class JobCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/waiter/JobCompleted.html#LocationService.Waiter.JobCompleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/waiters/#jobcompletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/waiter/JobCompleted.html#LocationService.Waiter.JobCompleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/waiters/#jobcompletedwaiter)
        """
