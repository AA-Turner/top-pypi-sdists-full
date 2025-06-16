"""
Type annotations for internetmonitor service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_internetmonitor.client import CloudWatchInternetMonitorClient
    from types_aiobotocore_internetmonitor.paginator import (
        ListHealthEventsPaginator,
        ListInternetEventsPaginator,
        ListMonitorsPaginator,
    )

    session = get_session()
    with session.create_client("internetmonitor") as client:
        client: CloudWatchInternetMonitorClient

        list_health_events_paginator: ListHealthEventsPaginator = client.get_paginator("list_health_events")
        list_internet_events_paginator: ListInternetEventsPaginator = client.get_paginator("list_internet_events")
        list_monitors_paginator: ListMonitorsPaginator = client.get_paginator("list_monitors")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListHealthEventsInputPaginateTypeDef,
    ListHealthEventsOutputTypeDef,
    ListInternetEventsInputPaginateTypeDef,
    ListInternetEventsOutputTypeDef,
    ListMonitorsInputPaginateTypeDef,
    ListMonitorsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListHealthEventsPaginator", "ListInternetEventsPaginator", "ListMonitorsPaginator")

if TYPE_CHECKING:
    _ListHealthEventsPaginatorBase = AioPaginator[ListHealthEventsOutputTypeDef]
else:
    _ListHealthEventsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListHealthEventsPaginator(_ListHealthEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/paginator/ListHealthEvents.html#CloudWatchInternetMonitor.Paginator.ListHealthEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/paginators/#listhealtheventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHealthEventsInputPaginateTypeDef]
    ) -> AioPageIterator[ListHealthEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/paginator/ListHealthEvents.html#CloudWatchInternetMonitor.Paginator.ListHealthEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/paginators/#listhealtheventspaginator)
        """

if TYPE_CHECKING:
    _ListInternetEventsPaginatorBase = AioPaginator[ListInternetEventsOutputTypeDef]
else:
    _ListInternetEventsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListInternetEventsPaginator(_ListInternetEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/paginator/ListInternetEvents.html#CloudWatchInternetMonitor.Paginator.ListInternetEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/paginators/#listinterneteventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInternetEventsInputPaginateTypeDef]
    ) -> AioPageIterator[ListInternetEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/paginator/ListInternetEvents.html#CloudWatchInternetMonitor.Paginator.ListInternetEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/paginators/#listinterneteventspaginator)
        """

if TYPE_CHECKING:
    _ListMonitorsPaginatorBase = AioPaginator[ListMonitorsOutputTypeDef]
else:
    _ListMonitorsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMonitorsPaginator(_ListMonitorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/paginator/ListMonitors.html#CloudWatchInternetMonitor.Paginator.ListMonitors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/paginators/#listmonitorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMonitorsInputPaginateTypeDef]
    ) -> AioPageIterator[ListMonitorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/paginator/ListMonitors.html#CloudWatchInternetMonitor.Paginator.ListMonitors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/paginators/#listmonitorspaginator)
        """
