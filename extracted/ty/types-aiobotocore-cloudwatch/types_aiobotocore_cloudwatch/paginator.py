"""
Type annotations for cloudwatch service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudwatch.client import CloudWatchClient
    from types_aiobotocore_cloudwatch.paginator import (
        DescribeAlarmHistoryPaginator,
        DescribeAlarmsPaginator,
        DescribeAnomalyDetectorsPaginator,
        GetMetricDataPaginator,
        ListDashboardsPaginator,
        ListMetricsPaginator,
    )

    session = get_session()
    with session.create_client("cloudwatch") as client:
        client: CloudWatchClient

        describe_alarm_history_paginator: DescribeAlarmHistoryPaginator = client.get_paginator("describe_alarm_history")
        describe_alarms_paginator: DescribeAlarmsPaginator = client.get_paginator("describe_alarms")
        describe_anomaly_detectors_paginator: DescribeAnomalyDetectorsPaginator = client.get_paginator("describe_anomaly_detectors")
        get_metric_data_paginator: GetMetricDataPaginator = client.get_paginator("get_metric_data")
        list_dashboards_paginator: ListDashboardsPaginator = client.get_paginator("list_dashboards")
        list_metrics_paginator: ListMetricsPaginator = client.get_paginator("list_metrics")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeAlarmHistoryInputPaginateTypeDef,
    DescribeAlarmHistoryOutputTypeDef,
    DescribeAlarmsInputPaginateTypeDef,
    DescribeAlarmsOutputTypeDef,
    DescribeAnomalyDetectorsInputPaginateTypeDef,
    DescribeAnomalyDetectorsOutputTypeDef,
    GetMetricDataInputPaginateTypeDef,
    GetMetricDataOutputTypeDef,
    ListDashboardsInputPaginateTypeDef,
    ListDashboardsOutputTypeDef,
    ListMetricsInputPaginateTypeDef,
    ListMetricsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeAlarmHistoryPaginator",
    "DescribeAlarmsPaginator",
    "DescribeAnomalyDetectorsPaginator",
    "GetMetricDataPaginator",
    "ListDashboardsPaginator",
    "ListMetricsPaginator",
)


if TYPE_CHECKING:
    _DescribeAlarmHistoryPaginatorBase = AioPaginator[DescribeAlarmHistoryOutputTypeDef]
else:
    _DescribeAlarmHistoryPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeAlarmHistoryPaginator(_DescribeAlarmHistoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/DescribeAlarmHistory.html#CloudWatch.Paginator.DescribeAlarmHistory)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#describealarmhistorypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAlarmHistoryInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeAlarmHistoryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/DescribeAlarmHistory.html#CloudWatch.Paginator.DescribeAlarmHistory.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#describealarmhistorypaginator)
        """


if TYPE_CHECKING:
    _DescribeAlarmsPaginatorBase = AioPaginator[DescribeAlarmsOutputTypeDef]
else:
    _DescribeAlarmsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeAlarmsPaginator(_DescribeAlarmsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/DescribeAlarms.html#CloudWatch.Paginator.DescribeAlarms)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#describealarmspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAlarmsInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeAlarmsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/DescribeAlarms.html#CloudWatch.Paginator.DescribeAlarms.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#describealarmspaginator)
        """


if TYPE_CHECKING:
    _DescribeAnomalyDetectorsPaginatorBase = AioPaginator[DescribeAnomalyDetectorsOutputTypeDef]
else:
    _DescribeAnomalyDetectorsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeAnomalyDetectorsPaginator(_DescribeAnomalyDetectorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/DescribeAnomalyDetectors.html#CloudWatch.Paginator.DescribeAnomalyDetectors)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#describeanomalydetectorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAnomalyDetectorsInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeAnomalyDetectorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/DescribeAnomalyDetectors.html#CloudWatch.Paginator.DescribeAnomalyDetectors.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#describeanomalydetectorspaginator)
        """


if TYPE_CHECKING:
    _GetMetricDataPaginatorBase = AioPaginator[GetMetricDataOutputTypeDef]
else:
    _GetMetricDataPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetMetricDataPaginator(_GetMetricDataPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/GetMetricData.html#CloudWatch.Paginator.GetMetricData)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#getmetricdatapaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetMetricDataInputPaginateTypeDef]
    ) -> AioPageIterator[GetMetricDataOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/GetMetricData.html#CloudWatch.Paginator.GetMetricData.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#getmetricdatapaginator)
        """


if TYPE_CHECKING:
    _ListDashboardsPaginatorBase = AioPaginator[ListDashboardsOutputTypeDef]
else:
    _ListDashboardsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDashboardsPaginator(_ListDashboardsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/ListDashboards.html#CloudWatch.Paginator.ListDashboards)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#listdashboardspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDashboardsInputPaginateTypeDef]
    ) -> AioPageIterator[ListDashboardsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/ListDashboards.html#CloudWatch.Paginator.ListDashboards.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#listdashboardspaginator)
        """


if TYPE_CHECKING:
    _ListMetricsPaginatorBase = AioPaginator[ListMetricsOutputTypeDef]
else:
    _ListMetricsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListMetricsPaginator(_ListMetricsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/ListMetrics.html#CloudWatch.Paginator.ListMetrics)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#listmetricspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMetricsInputPaginateTypeDef]
    ) -> AioPageIterator[ListMetricsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/paginator/ListMetrics.html#CloudWatch.Paginator.ListMetrics.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudwatch/paginators/#listmetricspaginator)
        """
