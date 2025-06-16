"""
Type annotations for elastictranscoder service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_elastictranscoder.client import ElasticTranscoderClient
    from types_aiobotocore_elastictranscoder.waiter import (
        JobCompleteWaiter,
    )

    session = get_session()
    async with session.create_client("elastictranscoder") as client:
        client: ElasticTranscoderClient

        job_complete_waiter: JobCompleteWaiter = client.get_waiter("job_complete")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import ReadJobRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("JobCompleteWaiter",)

class JobCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/waiter/JobComplete.html#ElasticTranscoder.Waiter.JobComplete)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/waiters/#jobcompletewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[ReadJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastictranscoder/waiter/JobComplete.html#ElasticTranscoder.Waiter.JobComplete.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elastictranscoder/waiters/#jobcompletewaiter)
        """
