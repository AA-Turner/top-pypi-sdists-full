"""
Type annotations for internetmonitor service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_internetmonitor.client import CloudWatchInternetMonitorClient

    session = get_session()
    async with session.create_client("internetmonitor") as client:
        client: CloudWatchInternetMonitorClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListHealthEventsPaginator, ListInternetEventsPaginator, ListMonitorsPaginator
from .type_defs import (
    CreateMonitorInputTypeDef,
    CreateMonitorOutputTypeDef,
    DeleteMonitorInputTypeDef,
    GetHealthEventInputTypeDef,
    GetHealthEventOutputTypeDef,
    GetInternetEventInputTypeDef,
    GetInternetEventOutputTypeDef,
    GetMonitorInputTypeDef,
    GetMonitorOutputTypeDef,
    GetQueryResultsInputTypeDef,
    GetQueryResultsOutputTypeDef,
    GetQueryStatusInputTypeDef,
    GetQueryStatusOutputTypeDef,
    ListHealthEventsInputTypeDef,
    ListHealthEventsOutputTypeDef,
    ListInternetEventsInputTypeDef,
    ListInternetEventsOutputTypeDef,
    ListMonitorsInputTypeDef,
    ListMonitorsOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    StartQueryInputTypeDef,
    StartQueryOutputTypeDef,
    StopQueryInputTypeDef,
    TagResourceInputTypeDef,
    UntagResourceInputTypeDef,
    UpdateMonitorInputTypeDef,
    UpdateMonitorOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("CloudWatchInternetMonitorClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class CloudWatchInternetMonitorClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor.html#CloudWatchInternetMonitor.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudWatchInternetMonitorClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor.html#CloudWatchInternetMonitor.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#generate_presigned_url)
        """

    async def create_monitor(
        self, **kwargs: Unpack[CreateMonitorInputTypeDef]
    ) -> CreateMonitorOutputTypeDef:
        """
        Creates a monitor in Amazon CloudWatch Internet Monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/client/create_monitor.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#create_monitor)
        """

    async def delete_monitor(self, **kwargs: Unpack[DeleteMonitorInputTypeDef]) -> Dict[str, Any]:
        """
        Deletes a monitor in Amazon CloudWatch Internet Monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/client/delete_monitor.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#delete_monitor)
        """

    async def get_health_event(
        self, **kwargs: Unpack[GetHealthEventInputTypeDef]
    ) -> GetHealthEventOutputTypeDef:
        """
        Gets information that Amazon CloudWatch Internet Monitor has created and stored
        about a health event for a specified monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/client/get_health_event.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#get_health_event)
        """

    async def get_internet_event(
        self, **kwargs: Unpack[GetInternetEventInputTypeDef]
    ) -> GetInternetEventOutputTypeDef:
        """
        Gets information that Amazon CloudWatch Internet Monitor has generated about an
        internet event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/client/get_internet_event.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#get_internet_event)
        """

    async def get_monitor(
        self, **kwargs: Unpack[GetMonitorInputTypeDef]
    ) -> GetMonitorOutputTypeDef:
        """
        Gets information about a monitor in Amazon CloudWatch Internet Monitor based on
        a monitor name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/client/get_monitor.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#get_monitor)
        """

    async def get_query_results(
        self, **kwargs: Unpack[GetQueryResultsInputTypeDef]
    ) -> GetQueryResultsOutputTypeDef:
        """
        Return the data for a query with the Amazon CloudWatch Internet Monitor query
        interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/client/get_query_results.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#get_query_results)
        """

    async def get_query_status(
        self, **kwargs: Unpack[GetQueryStatusInputTypeDef]
    ) -> GetQueryStatusOutputTypeDef:
        """
        Returns the current status of a query for the Amazon CloudWatch Internet
        Monitor query interface, for a specified query ID and monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/client/get_query_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#get_query_status)
        """

    async def list_health_events(
        self, **kwargs: Unpack[ListHealthEventsInputTypeDef]
    ) -> ListHealthEventsOutputTypeDef:
        """
        Lists all health events for a monitor in Amazon CloudWatch Internet Monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/client/list_health_events.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#list_health_events)
        """

    async def list_internet_events(
        self, **kwargs: Unpack[ListInternetEventsInputTypeDef]
    ) -> ListInternetEventsOutputTypeDef:
        """
        Lists internet events that cause performance or availability issues for client
        locations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/client/list_internet_events.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#list_internet_events)
        """

    async def list_monitors(
        self, **kwargs: Unpack[ListMonitorsInputTypeDef]
    ) -> ListMonitorsOutputTypeDef:
        """
        Lists all of your monitors for Amazon CloudWatch Internet Monitor and their
        statuses, along with the Amazon Resource Name (ARN) and name of each monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/client/list_monitors.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#list_monitors)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#list_tags_for_resource)
        """

    async def start_query(
        self, **kwargs: Unpack[StartQueryInputTypeDef]
    ) -> StartQueryOutputTypeDef:
        """
        Start a query to return data for a specific query type for the Amazon
        CloudWatch Internet Monitor query interface.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/client/start_query.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#start_query)
        """

    async def stop_query(self, **kwargs: Unpack[StopQueryInputTypeDef]) -> Dict[str, Any]:
        """
        Stop a query that is progress for a specific monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/client/stop_query.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#stop_query)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceInputTypeDef]) -> Dict[str, Any]:
        """
        Adds a tag to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceInputTypeDef]) -> Dict[str, Any]:
        """
        Removes a tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#untag_resource)
        """

    async def update_monitor(
        self, **kwargs: Unpack[UpdateMonitorInputTypeDef]
    ) -> UpdateMonitorOutputTypeDef:
        """
        Updates a monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/client/update_monitor.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#update_monitor)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_health_events"]
    ) -> ListHealthEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_internet_events"]
    ) -> ListInternetEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_monitors"]
    ) -> ListMonitorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor.html#CloudWatchInternetMonitor.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/internetmonitor.html#CloudWatchInternetMonitor.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/client/)
        """
