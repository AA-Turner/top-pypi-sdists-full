"""
Type annotations for rum service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_rum.client import CloudWatchRUMClient

    session = get_session()
    async with session.create_client("rum") as client:
        client: CloudWatchRUMClient
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

from .paginator import (
    BatchGetRumMetricDefinitionsPaginator,
    GetAppMonitorDataPaginator,
    ListAppMonitorsPaginator,
    ListRumMetricsDestinationsPaginator,
)
from .type_defs import (
    BatchCreateRumMetricDefinitionsRequestTypeDef,
    BatchCreateRumMetricDefinitionsResponseTypeDef,
    BatchDeleteRumMetricDefinitionsRequestTypeDef,
    BatchDeleteRumMetricDefinitionsResponseTypeDef,
    BatchGetRumMetricDefinitionsRequestTypeDef,
    BatchGetRumMetricDefinitionsResponseTypeDef,
    CreateAppMonitorRequestTypeDef,
    CreateAppMonitorResponseTypeDef,
    DeleteAppMonitorRequestTypeDef,
    DeleteResourcePolicyRequestTypeDef,
    DeleteResourcePolicyResponseTypeDef,
    DeleteRumMetricsDestinationRequestTypeDef,
    GetAppMonitorDataRequestTypeDef,
    GetAppMonitorDataResponseTypeDef,
    GetAppMonitorRequestTypeDef,
    GetAppMonitorResponseTypeDef,
    GetResourcePolicyRequestTypeDef,
    GetResourcePolicyResponseTypeDef,
    ListAppMonitorsRequestTypeDef,
    ListAppMonitorsResponseTypeDef,
    ListRumMetricsDestinationsRequestTypeDef,
    ListRumMetricsDestinationsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutResourcePolicyRequestTypeDef,
    PutResourcePolicyResponseTypeDef,
    PutRumEventsRequestTypeDef,
    PutRumMetricsDestinationRequestTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateAppMonitorRequestTypeDef,
    UpdateRumMetricDefinitionRequestTypeDef,
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

__all__ = ("CloudWatchRUMClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidPolicyRevisionIdException: Type[BotocoreClientError]
    MalformedPolicyDocumentException: Type[BotocoreClientError]
    PolicyNotFoundException: Type[BotocoreClientError]
    PolicySizeLimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class CloudWatchRUMClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudWatchRUMClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#generate_presigned_url)
        """

    async def batch_create_rum_metric_definitions(
        self, **kwargs: Unpack[BatchCreateRumMetricDefinitionsRequestTypeDef]
    ) -> BatchCreateRumMetricDefinitionsResponseTypeDef:
        """
        Specifies the extended metrics and custom metrics that you want a CloudWatch
        RUM app monitor to send to a destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/batch_create_rum_metric_definitions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#batch_create_rum_metric_definitions)
        """

    async def batch_delete_rum_metric_definitions(
        self, **kwargs: Unpack[BatchDeleteRumMetricDefinitionsRequestTypeDef]
    ) -> BatchDeleteRumMetricDefinitionsResponseTypeDef:
        """
        Removes the specified metrics from being sent to an extended metrics
        destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/batch_delete_rum_metric_definitions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#batch_delete_rum_metric_definitions)
        """

    async def batch_get_rum_metric_definitions(
        self, **kwargs: Unpack[BatchGetRumMetricDefinitionsRequestTypeDef]
    ) -> BatchGetRumMetricDefinitionsResponseTypeDef:
        """
        Retrieves the list of metrics and dimensions that a RUM app monitor is sending
        to a single destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/batch_get_rum_metric_definitions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#batch_get_rum_metric_definitions)
        """

    async def create_app_monitor(
        self, **kwargs: Unpack[CreateAppMonitorRequestTypeDef]
    ) -> CreateAppMonitorResponseTypeDef:
        """
        Creates a Amazon CloudWatch RUM app monitor, which collects telemetry data from
        your application and sends that data to RUM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/create_app_monitor.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#create_app_monitor)
        """

    async def delete_app_monitor(
        self, **kwargs: Unpack[DeleteAppMonitorRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an existing app monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/delete_app_monitor.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#delete_app_monitor)
        """

    async def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyRequestTypeDef]
    ) -> DeleteResourcePolicyResponseTypeDef:
        """
        Removes the association of a resource-based policy from an app monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/delete_resource_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#delete_resource_policy)
        """

    async def delete_rum_metrics_destination(
        self, **kwargs: Unpack[DeleteRumMetricsDestinationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a destination for CloudWatch RUM extended metrics, so that the
        specified app monitor stops sending extended metrics to that destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/delete_rum_metrics_destination.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#delete_rum_metrics_destination)
        """

    async def get_app_monitor(
        self, **kwargs: Unpack[GetAppMonitorRequestTypeDef]
    ) -> GetAppMonitorResponseTypeDef:
        """
        Retrieves the complete configuration information for one app monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/get_app_monitor.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#get_app_monitor)
        """

    async def get_app_monitor_data(
        self, **kwargs: Unpack[GetAppMonitorDataRequestTypeDef]
    ) -> GetAppMonitorDataResponseTypeDef:
        """
        Retrieves the raw performance events that RUM has collected from your web
        application, so that you can do your own processing or analysis of this data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/get_app_monitor_data.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#get_app_monitor_data)
        """

    async def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyRequestTypeDef]
    ) -> GetResourcePolicyResponseTypeDef:
        """
        Use this operation to retrieve information about a resource-based policy that
        is attached to an app monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/get_resource_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#get_resource_policy)
        """

    async def list_app_monitors(
        self, **kwargs: Unpack[ListAppMonitorsRequestTypeDef]
    ) -> ListAppMonitorsResponseTypeDef:
        """
        Returns a list of the Amazon CloudWatch RUM app monitors in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/list_app_monitors.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#list_app_monitors)
        """

    async def list_rum_metrics_destinations(
        self, **kwargs: Unpack[ListRumMetricsDestinationsRequestTypeDef]
    ) -> ListRumMetricsDestinationsResponseTypeDef:
        """
        Returns a list of destinations that you have created to receive RUM extended
        metrics, for the specified app monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/list_rum_metrics_destinations.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#list_rum_metrics_destinations)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Displays the tags associated with a CloudWatch RUM resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#list_tags_for_resource)
        """

    async def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyRequestTypeDef]
    ) -> PutResourcePolicyResponseTypeDef:
        """
        Use this operation to assign a resource-based policy to a CloudWatch RUM app
        monitor to control access to it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/put_resource_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#put_resource_policy)
        """

    async def put_rum_events(self, **kwargs: Unpack[PutRumEventsRequestTypeDef]) -> Dict[str, Any]:
        """
        Sends telemetry events about your application performance and user behavior to
        CloudWatch RUM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/put_rum_events.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#put_rum_events)
        """

    async def put_rum_metrics_destination(
        self, **kwargs: Unpack[PutRumMetricsDestinationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates or updates a destination to receive extended metrics from CloudWatch
        RUM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/put_rum_metrics_destination.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#put_rum_metrics_destination)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified CloudWatch RUM
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#untag_resource)
        """

    async def update_app_monitor(
        self, **kwargs: Unpack[UpdateAppMonitorRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the configuration of an existing app monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/update_app_monitor.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#update_app_monitor)
        """

    async def update_rum_metric_definition(
        self, **kwargs: Unpack[UpdateRumMetricDefinitionRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Modifies one existing metric definition for CloudWatch RUM extended metrics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/update_rum_metric_definition.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#update_rum_metric_definition)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["batch_get_rum_metric_definitions"]
    ) -> BatchGetRumMetricDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_app_monitor_data"]
    ) -> GetAppMonitorDataPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_app_monitors"]
    ) -> ListAppMonitorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_rum_metrics_destinations"]
    ) -> ListRumMetricsDestinationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rum.html#CloudWatchRUM.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rum/client/)
        """
