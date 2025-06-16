"""
Type annotations for logs service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_logs.client import CloudWatchLogsClient
    from types_aiobotocore_logs.paginator import (
        DescribeConfigurationTemplatesPaginator,
        DescribeDeliveriesPaginator,
        DescribeDeliveryDestinationsPaginator,
        DescribeDeliverySourcesPaginator,
        DescribeDestinationsPaginator,
        DescribeExportTasksPaginator,
        DescribeLogGroupsPaginator,
        DescribeLogStreamsPaginator,
        DescribeMetricFiltersPaginator,
        DescribeQueriesPaginator,
        DescribeResourcePoliciesPaginator,
        DescribeSubscriptionFiltersPaginator,
        FilterLogEventsPaginator,
        ListAnomaliesPaginator,
        ListLogAnomalyDetectorsPaginator,
        ListLogGroupsForQueryPaginator,
    )

    session = get_session()
    with session.create_client("logs") as client:
        client: CloudWatchLogsClient

        describe_configuration_templates_paginator: DescribeConfigurationTemplatesPaginator = client.get_paginator("describe_configuration_templates")
        describe_deliveries_paginator: DescribeDeliveriesPaginator = client.get_paginator("describe_deliveries")
        describe_delivery_destinations_paginator: DescribeDeliveryDestinationsPaginator = client.get_paginator("describe_delivery_destinations")
        describe_delivery_sources_paginator: DescribeDeliverySourcesPaginator = client.get_paginator("describe_delivery_sources")
        describe_destinations_paginator: DescribeDestinationsPaginator = client.get_paginator("describe_destinations")
        describe_export_tasks_paginator: DescribeExportTasksPaginator = client.get_paginator("describe_export_tasks")
        describe_log_groups_paginator: DescribeLogGroupsPaginator = client.get_paginator("describe_log_groups")
        describe_log_streams_paginator: DescribeLogStreamsPaginator = client.get_paginator("describe_log_streams")
        describe_metric_filters_paginator: DescribeMetricFiltersPaginator = client.get_paginator("describe_metric_filters")
        describe_queries_paginator: DescribeQueriesPaginator = client.get_paginator("describe_queries")
        describe_resource_policies_paginator: DescribeResourcePoliciesPaginator = client.get_paginator("describe_resource_policies")
        describe_subscription_filters_paginator: DescribeSubscriptionFiltersPaginator = client.get_paginator("describe_subscription_filters")
        filter_log_events_paginator: FilterLogEventsPaginator = client.get_paginator("filter_log_events")
        list_anomalies_paginator: ListAnomaliesPaginator = client.get_paginator("list_anomalies")
        list_log_anomaly_detectors_paginator: ListLogAnomalyDetectorsPaginator = client.get_paginator("list_log_anomaly_detectors")
        list_log_groups_for_query_paginator: ListLogGroupsForQueryPaginator = client.get_paginator("list_log_groups_for_query")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeConfigurationTemplatesRequestPaginateTypeDef,
    DescribeConfigurationTemplatesResponseTypeDef,
    DescribeDeliveriesRequestPaginateTypeDef,
    DescribeDeliveriesResponseTypeDef,
    DescribeDeliveryDestinationsRequestPaginateTypeDef,
    DescribeDeliveryDestinationsResponseTypeDef,
    DescribeDeliverySourcesRequestPaginateTypeDef,
    DescribeDeliverySourcesResponseTypeDef,
    DescribeDestinationsRequestPaginateTypeDef,
    DescribeDestinationsResponseTypeDef,
    DescribeExportTasksRequestPaginateTypeDef,
    DescribeExportTasksResponseTypeDef,
    DescribeLogGroupsRequestPaginateTypeDef,
    DescribeLogGroupsResponseTypeDef,
    DescribeLogStreamsRequestPaginateTypeDef,
    DescribeLogStreamsResponseTypeDef,
    DescribeMetricFiltersRequestPaginateTypeDef,
    DescribeMetricFiltersResponseTypeDef,
    DescribeQueriesRequestPaginateTypeDef,
    DescribeQueriesResponseTypeDef,
    DescribeResourcePoliciesRequestPaginateTypeDef,
    DescribeResourcePoliciesResponseTypeDef,
    DescribeSubscriptionFiltersRequestPaginateTypeDef,
    DescribeSubscriptionFiltersResponseTypeDef,
    FilterLogEventsRequestPaginateTypeDef,
    FilterLogEventsResponseTypeDef,
    ListAnomaliesRequestPaginateTypeDef,
    ListAnomaliesResponseTypeDef,
    ListLogAnomalyDetectorsRequestPaginateTypeDef,
    ListLogAnomalyDetectorsResponseTypeDef,
    ListLogGroupsForQueryRequestPaginateTypeDef,
    ListLogGroupsForQueryResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeConfigurationTemplatesPaginator",
    "DescribeDeliveriesPaginator",
    "DescribeDeliveryDestinationsPaginator",
    "DescribeDeliverySourcesPaginator",
    "DescribeDestinationsPaginator",
    "DescribeExportTasksPaginator",
    "DescribeLogGroupsPaginator",
    "DescribeLogStreamsPaginator",
    "DescribeMetricFiltersPaginator",
    "DescribeQueriesPaginator",
    "DescribeResourcePoliciesPaginator",
    "DescribeSubscriptionFiltersPaginator",
    "FilterLogEventsPaginator",
    "ListAnomaliesPaginator",
    "ListLogAnomalyDetectorsPaginator",
    "ListLogGroupsForQueryPaginator",
)


if TYPE_CHECKING:
    _DescribeConfigurationTemplatesPaginatorBase = AioPaginator[
        DescribeConfigurationTemplatesResponseTypeDef
    ]
else:
    _DescribeConfigurationTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeConfigurationTemplatesPaginator(_DescribeConfigurationTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeConfigurationTemplates.html#CloudWatchLogs.Paginator.DescribeConfigurationTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeconfigurationtemplatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeConfigurationTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeConfigurationTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeConfigurationTemplates.html#CloudWatchLogs.Paginator.DescribeConfigurationTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeconfigurationtemplatespaginator)
        """


if TYPE_CHECKING:
    _DescribeDeliveriesPaginatorBase = AioPaginator[DescribeDeliveriesResponseTypeDef]
else:
    _DescribeDeliveriesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDeliveriesPaginator(_DescribeDeliveriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDeliveries.html#CloudWatchLogs.Paginator.DescribeDeliveries)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describedeliveriespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDeliveriesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeDeliveriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDeliveries.html#CloudWatchLogs.Paginator.DescribeDeliveries.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describedeliveriespaginator)
        """


if TYPE_CHECKING:
    _DescribeDeliveryDestinationsPaginatorBase = AioPaginator[
        DescribeDeliveryDestinationsResponseTypeDef
    ]
else:
    _DescribeDeliveryDestinationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDeliveryDestinationsPaginator(_DescribeDeliveryDestinationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDeliveryDestinations.html#CloudWatchLogs.Paginator.DescribeDeliveryDestinations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describedeliverydestinationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDeliveryDestinationsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeDeliveryDestinationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDeliveryDestinations.html#CloudWatchLogs.Paginator.DescribeDeliveryDestinations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describedeliverydestinationspaginator)
        """


if TYPE_CHECKING:
    _DescribeDeliverySourcesPaginatorBase = AioPaginator[DescribeDeliverySourcesResponseTypeDef]
else:
    _DescribeDeliverySourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDeliverySourcesPaginator(_DescribeDeliverySourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDeliverySources.html#CloudWatchLogs.Paginator.DescribeDeliverySources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describedeliverysourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDeliverySourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeDeliverySourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDeliverySources.html#CloudWatchLogs.Paginator.DescribeDeliverySources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describedeliverysourcespaginator)
        """


if TYPE_CHECKING:
    _DescribeDestinationsPaginatorBase = AioPaginator[DescribeDestinationsResponseTypeDef]
else:
    _DescribeDestinationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeDestinationsPaginator(_DescribeDestinationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDestinations.html#CloudWatchLogs.Paginator.DescribeDestinations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describedestinationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDestinationsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeDestinationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeDestinations.html#CloudWatchLogs.Paginator.DescribeDestinations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describedestinationspaginator)
        """


if TYPE_CHECKING:
    _DescribeExportTasksPaginatorBase = AioPaginator[DescribeExportTasksResponseTypeDef]
else:
    _DescribeExportTasksPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeExportTasksPaginator(_DescribeExportTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeExportTasks.html#CloudWatchLogs.Paginator.DescribeExportTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeexporttaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeExportTasksRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeExportTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeExportTasks.html#CloudWatchLogs.Paginator.DescribeExportTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeexporttaskspaginator)
        """


if TYPE_CHECKING:
    _DescribeLogGroupsPaginatorBase = AioPaginator[DescribeLogGroupsResponseTypeDef]
else:
    _DescribeLogGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeLogGroupsPaginator(_DescribeLogGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeLogGroups.html#CloudWatchLogs.Paginator.DescribeLogGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeloggroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeLogGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeLogGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeLogGroups.html#CloudWatchLogs.Paginator.DescribeLogGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeloggroupspaginator)
        """


if TYPE_CHECKING:
    _DescribeLogStreamsPaginatorBase = AioPaginator[DescribeLogStreamsResponseTypeDef]
else:
    _DescribeLogStreamsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeLogStreamsPaginator(_DescribeLogStreamsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeLogStreams.html#CloudWatchLogs.Paginator.DescribeLogStreams)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describelogstreamspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeLogStreamsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeLogStreamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeLogStreams.html#CloudWatchLogs.Paginator.DescribeLogStreams.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describelogstreamspaginator)
        """


if TYPE_CHECKING:
    _DescribeMetricFiltersPaginatorBase = AioPaginator[DescribeMetricFiltersResponseTypeDef]
else:
    _DescribeMetricFiltersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeMetricFiltersPaginator(_DescribeMetricFiltersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeMetricFilters.html#CloudWatchLogs.Paginator.DescribeMetricFilters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describemetricfilterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMetricFiltersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeMetricFiltersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeMetricFilters.html#CloudWatchLogs.Paginator.DescribeMetricFilters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describemetricfilterspaginator)
        """


if TYPE_CHECKING:
    _DescribeQueriesPaginatorBase = AioPaginator[DescribeQueriesResponseTypeDef]
else:
    _DescribeQueriesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeQueriesPaginator(_DescribeQueriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeQueries.html#CloudWatchLogs.Paginator.DescribeQueries)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describequeriespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeQueriesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeQueriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeQueries.html#CloudWatchLogs.Paginator.DescribeQueries.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describequeriespaginator)
        """


if TYPE_CHECKING:
    _DescribeResourcePoliciesPaginatorBase = AioPaginator[DescribeResourcePoliciesResponseTypeDef]
else:
    _DescribeResourcePoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeResourcePoliciesPaginator(_DescribeResourcePoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeResourcePolicies.html#CloudWatchLogs.Paginator.DescribeResourcePolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeresourcepoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeResourcePoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeResourcePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeResourcePolicies.html#CloudWatchLogs.Paginator.DescribeResourcePolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describeresourcepoliciespaginator)
        """


if TYPE_CHECKING:
    _DescribeSubscriptionFiltersPaginatorBase = AioPaginator[
        DescribeSubscriptionFiltersResponseTypeDef
    ]
else:
    _DescribeSubscriptionFiltersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeSubscriptionFiltersPaginator(_DescribeSubscriptionFiltersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeSubscriptionFilters.html#CloudWatchLogs.Paginator.DescribeSubscriptionFilters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describesubscriptionfilterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSubscriptionFiltersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeSubscriptionFiltersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/DescribeSubscriptionFilters.html#CloudWatchLogs.Paginator.DescribeSubscriptionFilters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#describesubscriptionfilterspaginator)
        """


if TYPE_CHECKING:
    _FilterLogEventsPaginatorBase = AioPaginator[FilterLogEventsResponseTypeDef]
else:
    _FilterLogEventsPaginatorBase = AioPaginator  # type: ignore[assignment]


class FilterLogEventsPaginator(_FilterLogEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/FilterLogEvents.html#CloudWatchLogs.Paginator.FilterLogEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#filterlogeventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[FilterLogEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[FilterLogEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/FilterLogEvents.html#CloudWatchLogs.Paginator.FilterLogEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#filterlogeventspaginator)
        """


if TYPE_CHECKING:
    _ListAnomaliesPaginatorBase = AioPaginator[ListAnomaliesResponseTypeDef]
else:
    _ListAnomaliesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAnomaliesPaginator(_ListAnomaliesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/ListAnomalies.html#CloudWatchLogs.Paginator.ListAnomalies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#listanomaliespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAnomaliesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAnomaliesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/ListAnomalies.html#CloudWatchLogs.Paginator.ListAnomalies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#listanomaliespaginator)
        """


if TYPE_CHECKING:
    _ListLogAnomalyDetectorsPaginatorBase = AioPaginator[ListLogAnomalyDetectorsResponseTypeDef]
else:
    _ListLogAnomalyDetectorsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListLogAnomalyDetectorsPaginator(_ListLogAnomalyDetectorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/ListLogAnomalyDetectors.html#CloudWatchLogs.Paginator.ListLogAnomalyDetectors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#listloganomalydetectorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLogAnomalyDetectorsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLogAnomalyDetectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/ListLogAnomalyDetectors.html#CloudWatchLogs.Paginator.ListLogAnomalyDetectors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#listloganomalydetectorspaginator)
        """


if TYPE_CHECKING:
    _ListLogGroupsForQueryPaginatorBase = AioPaginator[ListLogGroupsForQueryResponseTypeDef]
else:
    _ListLogGroupsForQueryPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListLogGroupsForQueryPaginator(_ListLogGroupsForQueryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/ListLogGroupsForQuery.html#CloudWatchLogs.Paginator.ListLogGroupsForQuery)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#listloggroupsforquerypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLogGroupsForQueryRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLogGroupsForQueryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs/paginator/ListLogGroupsForQuery.html#CloudWatchLogs.Paginator.ListLogGroupsForQuery.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/paginators/#listloggroupsforquerypaginator)
        """
