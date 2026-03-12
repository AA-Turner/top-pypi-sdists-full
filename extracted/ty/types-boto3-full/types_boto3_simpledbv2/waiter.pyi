"""
Type annotations for simpledbv2 service client waiters.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_simpledbv2/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_simpledbv2.client import SimpleDBv2Client
    from types_boto3_simpledbv2.waiter import (
        ExportSucceededWaiter,
    )

    session = Session()
    client: SimpleDBv2Client = session.client("simpledbv2")

    export_succeeded_waiter: ExportSucceededWaiter = client.get_waiter("export_succeeded")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import GetExportRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ExportSucceededWaiter",)

class ExportSucceededWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simpledbv2/waiter/ExportSucceeded.html#SimpleDBv2.Waiter.ExportSucceeded)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_simpledbv2/waiters/#exportsucceededwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetExportRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simpledbv2/waiter/ExportSucceeded.html#SimpleDBv2.Waiter.ExportSucceeded.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_simpledbv2/waiters/#exportsucceededwaiter)
        """
