"""
Type annotations for networkmonitor service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_networkmonitor.client import CloudWatchNetworkMonitorClient
    from types_aiobotocore_networkmonitor.paginator import (
        ListMonitorsPaginator,
    )

    session = get_session()
    with session.create_client("networkmonitor") as client:
        client: CloudWatchNetworkMonitorClient

        list_monitors_paginator: ListMonitorsPaginator = client.get_paginator("list_monitors")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListMonitorsInputPaginateTypeDef, ListMonitorsOutputTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListMonitorsPaginator",)

if TYPE_CHECKING:
    _ListMonitorsPaginatorBase = AioPaginator[ListMonitorsOutputTypeDef]
else:
    _ListMonitorsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMonitorsPaginator(_ListMonitorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor/paginator/ListMonitors.html#CloudWatchNetworkMonitor.Paginator.ListMonitors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/paginators/#listmonitorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMonitorsInputPaginateTypeDef]
    ) -> AioPageIterator[ListMonitorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor/paginator/ListMonitors.html#CloudWatchNetworkMonitor.Paginator.ListMonitors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/paginators/#listmonitorspaginator)
        """
