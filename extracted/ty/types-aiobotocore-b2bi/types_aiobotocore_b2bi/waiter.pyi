"""
Type annotations for b2bi service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_b2bi.client import B2BIClient
    from types_aiobotocore_b2bi.waiter import (
        TransformerJobSucceededWaiter,
    )

    session = get_session()
    async with session.create_client("b2bi") as client:
        client: B2BIClient

        transformer_job_succeeded_waiter: TransformerJobSucceededWaiter = client.get_waiter("transformer_job_succeeded")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import GetTransformerJobRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("TransformerJobSucceededWaiter",)

class TransformerJobSucceededWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/waiter/TransformerJobSucceeded.html#B2BI.Waiter.TransformerJobSucceeded)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/waiters/#transformerjobsucceededwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetTransformerJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/waiter/TransformerJobSucceeded.html#B2BI.Waiter.TransformerJobSucceeded.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/waiters/#transformerjobsucceededwaiter)
        """
