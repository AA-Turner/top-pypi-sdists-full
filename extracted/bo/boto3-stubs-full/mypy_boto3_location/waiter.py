"""
Type annotations for location service client waiters.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_location.client import LocationServiceClient
    from mypy_boto3_location.waiter import (
        JobCompletedWaiter,
    )

    session = Session()
    client: LocationServiceClient = session.client("location")

    job_completed_waiter: JobCompletedWaiter = client.get_waiter("job_completed")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import GetJobRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("JobCompletedWaiter",)


class JobCompletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/waiter/JobCompleted.html#LocationService.Waiter.JobCompleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/waiters/#jobcompletedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location/waiter/JobCompleted.html#LocationService.Waiter.JobCompleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_location/waiters/#jobcompletedwaiter)
        """
