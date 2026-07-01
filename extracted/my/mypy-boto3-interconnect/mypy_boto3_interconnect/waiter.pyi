"""
Type annotations for interconnect service client waiters.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_interconnect/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_interconnect.client import InterconnectClient
    from mypy_boto3_interconnect.waiter import (
        ConnectionAvailableWaiter,
        ConnectionDeletedWaiter,
    )

    session = Session()
    client: InterconnectClient = session.client("interconnect")

    connection_available_waiter: ConnectionAvailableWaiter = client.get_waiter("connection_available")
    connection_deleted_waiter: ConnectionDeletedWaiter = client.get_waiter("connection_deleted")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import GetConnectionRequestWaitExtraTypeDef, GetConnectionRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ConnectionAvailableWaiter", "ConnectionDeletedWaiter")

class ConnectionAvailableWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/interconnect/waiter/ConnectionAvailable.html#Interconnect.Waiter.ConnectionAvailable)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_interconnect/waiters/#connectionavailablewaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetConnectionRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/interconnect/waiter/ConnectionAvailable.html#Interconnect.Waiter.ConnectionAvailable.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_interconnect/waiters/#connectionavailablewaiter)
        """

class ConnectionDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/interconnect/waiter/ConnectionDeleted.html#Interconnect.Waiter.ConnectionDeleted)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_interconnect/waiters/#connectiondeletedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetConnectionRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/interconnect/waiter/ConnectionDeleted.html#Interconnect.Waiter.ConnectionDeleted.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_interconnect/waiters/#connectiondeletedwaiter)
        """
