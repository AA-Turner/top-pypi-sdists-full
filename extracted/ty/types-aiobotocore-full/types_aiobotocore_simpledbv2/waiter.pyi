"""
Type annotations for simpledbv2 service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_simpledbv2/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_simpledbv2.client import SimpleDBv2Client
    from types_aiobotocore_simpledbv2.waiter import (
        ExportSucceededWaiter,
    )

    session = get_session()
    async with session.create_client("simpledbv2") as client:
        client: SimpleDBv2Client

        export_succeeded_waiter: ExportSucceededWaiter = client.get_waiter("export_succeeded")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import GetExportRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ExportSucceededWaiter",)

class ExportSucceededWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simpledbv2/waiter/ExportSucceeded.html#SimpleDBv2.Waiter.ExportSucceeded)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_simpledbv2/waiters/#exportsucceededwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetExportRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simpledbv2/waiter/ExportSucceeded.html#SimpleDBv2.Waiter.ExportSucceeded.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_simpledbv2/waiters/#exportsucceededwaiter)
        """
