"""
Type annotations for inspector2 service client waiters.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_inspector2.client import Inspector2Client
    from mypy_boto3_inspector2.waiter import (
        ConnectorConnectedWaiter,
        ConnectorDeletedWaiter,
        ConnectorEnabledWaiter,
    )

    session = Session()
    client: Inspector2Client = session.client("inspector2")

    connector_connected_waiter: ConnectorConnectedWaiter = client.get_waiter("connector_connected")
    connector_deleted_waiter: ConnectorDeletedWaiter = client.get_waiter("connector_deleted")
    connector_enabled_waiter: ConnectorEnabledWaiter = client.get_waiter("connector_enabled")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import (
    ListConnectorsRequestWaitExtraExtraTypeDef,
    ListConnectorsRequestWaitExtraTypeDef,
    ListConnectorsRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ConnectorConnectedWaiter", "ConnectorDeletedWaiter", "ConnectorEnabledWaiter")


class ConnectorConnectedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/waiter/ConnectorConnected.html#Inspector2.Waiter.ConnectorConnected)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/waiters/#connectorconnectedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[ListConnectorsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/waiter/ConnectorConnected.html#Inspector2.Waiter.ConnectorConnected.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/waiters/#connectorconnectedwaiter)
        """


class ConnectorDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/waiter/ConnectorDeleted.html#Inspector2.Waiter.ConnectorDeleted)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/waiters/#connectordeletedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[ListConnectorsRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/waiter/ConnectorDeleted.html#Inspector2.Waiter.ConnectorDeleted.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/waiters/#connectordeletedwaiter)
        """


class ConnectorEnabledWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/waiter/ConnectorEnabled.html#Inspector2.Waiter.ConnectorEnabled)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/waiters/#connectorenabledwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[ListConnectorsRequestWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector2/waiter/ConnectorEnabled.html#Inspector2.Waiter.ConnectorEnabled.wait)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_inspector2/waiters/#connectorenabledwaiter)
        """
