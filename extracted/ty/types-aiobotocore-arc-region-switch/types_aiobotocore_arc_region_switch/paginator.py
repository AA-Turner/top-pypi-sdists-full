"""
Type annotations for arc-region-switch service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_arc_region_switch.client import ARCRegionswitchClient
    from types_aiobotocore_arc_region_switch.paginator import (
        GetPlanEvaluationStatusPaginator,
        GetPlanExecutionPaginator,
        ListPlanExecutionEventsPaginator,
        ListPlanExecutionsPaginator,
        ListPlansInRegionPaginator,
        ListPlansPaginator,
        ListRoute53HealthChecksInRegionPaginator,
        ListRoute53HealthChecksPaginator,
    )

    session = get_session()
    with session.create_client("arc-region-switch") as client:
        client: ARCRegionswitchClient

        get_plan_evaluation_status_paginator: GetPlanEvaluationStatusPaginator = client.get_paginator("get_plan_evaluation_status")
        get_plan_execution_paginator: GetPlanExecutionPaginator = client.get_paginator("get_plan_execution")
        list_plan_execution_events_paginator: ListPlanExecutionEventsPaginator = client.get_paginator("list_plan_execution_events")
        list_plan_executions_paginator: ListPlanExecutionsPaginator = client.get_paginator("list_plan_executions")
        list_plans_in_region_paginator: ListPlansInRegionPaginator = client.get_paginator("list_plans_in_region")
        list_plans_paginator: ListPlansPaginator = client.get_paginator("list_plans")
        list_route53_health_checks_in_region_paginator: ListRoute53HealthChecksInRegionPaginator = client.get_paginator("list_route53_health_checks_in_region")
        list_route53_health_checks_paginator: ListRoute53HealthChecksPaginator = client.get_paginator("list_route53_health_checks")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetPlanEvaluationStatusRequestPaginateTypeDef,
    GetPlanEvaluationStatusResponseTypeDef,
    GetPlanExecutionRequestPaginateTypeDef,
    GetPlanExecutionResponsePaginatorTypeDef,
    ListPlanExecutionEventsRequestPaginateTypeDef,
    ListPlanExecutionEventsResponseTypeDef,
    ListPlanExecutionsRequestPaginateTypeDef,
    ListPlanExecutionsResponseTypeDef,
    ListPlansInRegionRequestPaginateTypeDef,
    ListPlansInRegionResponseTypeDef,
    ListPlansRequestPaginateTypeDef,
    ListPlansResponseTypeDef,
    ListRoute53HealthChecksInRegionRequestPaginateTypeDef,
    ListRoute53HealthChecksInRegionResponseTypeDef,
    ListRoute53HealthChecksRequestPaginateTypeDef,
    ListRoute53HealthChecksResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetPlanEvaluationStatusPaginator",
    "GetPlanExecutionPaginator",
    "ListPlanExecutionEventsPaginator",
    "ListPlanExecutionsPaginator",
    "ListPlansInRegionPaginator",
    "ListPlansPaginator",
    "ListRoute53HealthChecksInRegionPaginator",
    "ListRoute53HealthChecksPaginator",
)


if TYPE_CHECKING:
    _GetPlanEvaluationStatusPaginatorBase = AioPaginator[GetPlanEvaluationStatusResponseTypeDef]
else:
    _GetPlanEvaluationStatusPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetPlanEvaluationStatusPaginator(_GetPlanEvaluationStatusPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-region-switch/paginator/GetPlanEvaluationStatus.html#ARCRegionswitch.Paginator.GetPlanEvaluationStatus)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/paginators/#getplanevaluationstatuspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetPlanEvaluationStatusRequestPaginateTypeDef]
    ) -> AioPageIterator[GetPlanEvaluationStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-region-switch/paginator/GetPlanEvaluationStatus.html#ARCRegionswitch.Paginator.GetPlanEvaluationStatus.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/paginators/#getplanevaluationstatuspaginator)
        """


if TYPE_CHECKING:
    _GetPlanExecutionPaginatorBase = AioPaginator[GetPlanExecutionResponsePaginatorTypeDef]
else:
    _GetPlanExecutionPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetPlanExecutionPaginator(_GetPlanExecutionPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-region-switch/paginator/GetPlanExecution.html#ARCRegionswitch.Paginator.GetPlanExecution)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/paginators/#getplanexecutionpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetPlanExecutionRequestPaginateTypeDef]
    ) -> AioPageIterator[GetPlanExecutionResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-region-switch/paginator/GetPlanExecution.html#ARCRegionswitch.Paginator.GetPlanExecution.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/paginators/#getplanexecutionpaginator)
        """


if TYPE_CHECKING:
    _ListPlanExecutionEventsPaginatorBase = AioPaginator[ListPlanExecutionEventsResponseTypeDef]
else:
    _ListPlanExecutionEventsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPlanExecutionEventsPaginator(_ListPlanExecutionEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-region-switch/paginator/ListPlanExecutionEvents.html#ARCRegionswitch.Paginator.ListPlanExecutionEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/paginators/#listplanexecutioneventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPlanExecutionEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPlanExecutionEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-region-switch/paginator/ListPlanExecutionEvents.html#ARCRegionswitch.Paginator.ListPlanExecutionEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/paginators/#listplanexecutioneventspaginator)
        """


if TYPE_CHECKING:
    _ListPlanExecutionsPaginatorBase = AioPaginator[ListPlanExecutionsResponseTypeDef]
else:
    _ListPlanExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPlanExecutionsPaginator(_ListPlanExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-region-switch/paginator/ListPlanExecutions.html#ARCRegionswitch.Paginator.ListPlanExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/paginators/#listplanexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPlanExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPlanExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-region-switch/paginator/ListPlanExecutions.html#ARCRegionswitch.Paginator.ListPlanExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/paginators/#listplanexecutionspaginator)
        """


if TYPE_CHECKING:
    _ListPlansInRegionPaginatorBase = AioPaginator[ListPlansInRegionResponseTypeDef]
else:
    _ListPlansInRegionPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPlansInRegionPaginator(_ListPlansInRegionPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-region-switch/paginator/ListPlansInRegion.html#ARCRegionswitch.Paginator.ListPlansInRegion)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/paginators/#listplansinregionpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPlansInRegionRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPlansInRegionResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-region-switch/paginator/ListPlansInRegion.html#ARCRegionswitch.Paginator.ListPlansInRegion.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/paginators/#listplansinregionpaginator)
        """


if TYPE_CHECKING:
    _ListPlansPaginatorBase = AioPaginator[ListPlansResponseTypeDef]
else:
    _ListPlansPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPlansPaginator(_ListPlansPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-region-switch/paginator/ListPlans.html#ARCRegionswitch.Paginator.ListPlans)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/paginators/#listplanspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPlansRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPlansResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-region-switch/paginator/ListPlans.html#ARCRegionswitch.Paginator.ListPlans.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/paginators/#listplanspaginator)
        """


if TYPE_CHECKING:
    _ListRoute53HealthChecksInRegionPaginatorBase = AioPaginator[
        ListRoute53HealthChecksInRegionResponseTypeDef
    ]
else:
    _ListRoute53HealthChecksInRegionPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRoute53HealthChecksInRegionPaginator(_ListRoute53HealthChecksInRegionPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-region-switch/paginator/ListRoute53HealthChecksInRegion.html#ARCRegionswitch.Paginator.ListRoute53HealthChecksInRegion)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/paginators/#listroute53healthchecksinregionpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRoute53HealthChecksInRegionRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRoute53HealthChecksInRegionResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-region-switch/paginator/ListRoute53HealthChecksInRegion.html#ARCRegionswitch.Paginator.ListRoute53HealthChecksInRegion.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/paginators/#listroute53healthchecksinregionpaginator)
        """


if TYPE_CHECKING:
    _ListRoute53HealthChecksPaginatorBase = AioPaginator[ListRoute53HealthChecksResponseTypeDef]
else:
    _ListRoute53HealthChecksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRoute53HealthChecksPaginator(_ListRoute53HealthChecksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-region-switch/paginator/ListRoute53HealthChecks.html#ARCRegionswitch.Paginator.ListRoute53HealthChecks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/paginators/#listroute53healthcheckspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRoute53HealthChecksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRoute53HealthChecksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-region-switch/paginator/ListRoute53HealthChecks.html#ARCRegionswitch.Paginator.ListRoute53HealthChecks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/paginators/#listroute53healthcheckspaginator)
        """
