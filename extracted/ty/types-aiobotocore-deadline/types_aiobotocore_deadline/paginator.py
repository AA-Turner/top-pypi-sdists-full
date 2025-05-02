"""
Type annotations for deadline service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_deadline.client import DeadlineCloudClient
    from types_aiobotocore_deadline.paginator import (
        GetSessionsStatisticsAggregationPaginator,
        ListAvailableMeteredProductsPaginator,
        ListBudgetsPaginator,
        ListFarmMembersPaginator,
        ListFarmsPaginator,
        ListFleetMembersPaginator,
        ListFleetsPaginator,
        ListJobMembersPaginator,
        ListJobParameterDefinitionsPaginator,
        ListJobsPaginator,
        ListLicenseEndpointsPaginator,
        ListLimitsPaginator,
        ListMeteredProductsPaginator,
        ListMonitorsPaginator,
        ListQueueEnvironmentsPaginator,
        ListQueueFleetAssociationsPaginator,
        ListQueueLimitAssociationsPaginator,
        ListQueueMembersPaginator,
        ListQueuesPaginator,
        ListSessionActionsPaginator,
        ListSessionsForWorkerPaginator,
        ListSessionsPaginator,
        ListStepConsumersPaginator,
        ListStepDependenciesPaginator,
        ListStepsPaginator,
        ListStorageProfilesForQueuePaginator,
        ListStorageProfilesPaginator,
        ListTasksPaginator,
        ListWorkersPaginator,
    )

    session = get_session()
    with session.create_client("deadline") as client:
        client: DeadlineCloudClient

        get_sessions_statistics_aggregation_paginator: GetSessionsStatisticsAggregationPaginator = client.get_paginator("get_sessions_statistics_aggregation")
        list_available_metered_products_paginator: ListAvailableMeteredProductsPaginator = client.get_paginator("list_available_metered_products")
        list_budgets_paginator: ListBudgetsPaginator = client.get_paginator("list_budgets")
        list_farm_members_paginator: ListFarmMembersPaginator = client.get_paginator("list_farm_members")
        list_farms_paginator: ListFarmsPaginator = client.get_paginator("list_farms")
        list_fleet_members_paginator: ListFleetMembersPaginator = client.get_paginator("list_fleet_members")
        list_fleets_paginator: ListFleetsPaginator = client.get_paginator("list_fleets")
        list_job_members_paginator: ListJobMembersPaginator = client.get_paginator("list_job_members")
        list_job_parameter_definitions_paginator: ListJobParameterDefinitionsPaginator = client.get_paginator("list_job_parameter_definitions")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_license_endpoints_paginator: ListLicenseEndpointsPaginator = client.get_paginator("list_license_endpoints")
        list_limits_paginator: ListLimitsPaginator = client.get_paginator("list_limits")
        list_metered_products_paginator: ListMeteredProductsPaginator = client.get_paginator("list_metered_products")
        list_monitors_paginator: ListMonitorsPaginator = client.get_paginator("list_monitors")
        list_queue_environments_paginator: ListQueueEnvironmentsPaginator = client.get_paginator("list_queue_environments")
        list_queue_fleet_associations_paginator: ListQueueFleetAssociationsPaginator = client.get_paginator("list_queue_fleet_associations")
        list_queue_limit_associations_paginator: ListQueueLimitAssociationsPaginator = client.get_paginator("list_queue_limit_associations")
        list_queue_members_paginator: ListQueueMembersPaginator = client.get_paginator("list_queue_members")
        list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
        list_session_actions_paginator: ListSessionActionsPaginator = client.get_paginator("list_session_actions")
        list_sessions_for_worker_paginator: ListSessionsForWorkerPaginator = client.get_paginator("list_sessions_for_worker")
        list_sessions_paginator: ListSessionsPaginator = client.get_paginator("list_sessions")
        list_step_consumers_paginator: ListStepConsumersPaginator = client.get_paginator("list_step_consumers")
        list_step_dependencies_paginator: ListStepDependenciesPaginator = client.get_paginator("list_step_dependencies")
        list_steps_paginator: ListStepsPaginator = client.get_paginator("list_steps")
        list_storage_profiles_for_queue_paginator: ListStorageProfilesForQueuePaginator = client.get_paginator("list_storage_profiles_for_queue")
        list_storage_profiles_paginator: ListStorageProfilesPaginator = client.get_paginator("list_storage_profiles")
        list_tasks_paginator: ListTasksPaginator = client.get_paginator("list_tasks")
        list_workers_paginator: ListWorkersPaginator = client.get_paginator("list_workers")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetSessionsStatisticsAggregationRequestPaginateTypeDef,
    GetSessionsStatisticsAggregationResponseTypeDef,
    ListAvailableMeteredProductsRequestPaginateTypeDef,
    ListAvailableMeteredProductsResponseTypeDef,
    ListBudgetsRequestPaginateTypeDef,
    ListBudgetsResponseTypeDef,
    ListFarmMembersRequestPaginateTypeDef,
    ListFarmMembersResponseTypeDef,
    ListFarmsRequestPaginateTypeDef,
    ListFarmsResponseTypeDef,
    ListFleetMembersRequestPaginateTypeDef,
    ListFleetMembersResponseTypeDef,
    ListFleetsRequestPaginateTypeDef,
    ListFleetsResponseTypeDef,
    ListJobMembersRequestPaginateTypeDef,
    ListJobMembersResponseTypeDef,
    ListJobParameterDefinitionsRequestPaginateTypeDef,
    ListJobParameterDefinitionsResponseTypeDef,
    ListJobsRequestPaginateTypeDef,
    ListJobsResponseTypeDef,
    ListLicenseEndpointsRequestPaginateTypeDef,
    ListLicenseEndpointsResponseTypeDef,
    ListLimitsRequestPaginateTypeDef,
    ListLimitsResponseTypeDef,
    ListMeteredProductsRequestPaginateTypeDef,
    ListMeteredProductsResponseTypeDef,
    ListMonitorsRequestPaginateTypeDef,
    ListMonitorsResponseTypeDef,
    ListQueueEnvironmentsRequestPaginateTypeDef,
    ListQueueEnvironmentsResponseTypeDef,
    ListQueueFleetAssociationsRequestPaginateTypeDef,
    ListQueueFleetAssociationsResponseTypeDef,
    ListQueueLimitAssociationsRequestPaginateTypeDef,
    ListQueueLimitAssociationsResponseTypeDef,
    ListQueueMembersRequestPaginateTypeDef,
    ListQueueMembersResponseTypeDef,
    ListQueuesRequestPaginateTypeDef,
    ListQueuesResponseTypeDef,
    ListSessionActionsRequestPaginateTypeDef,
    ListSessionActionsResponseTypeDef,
    ListSessionsForWorkerRequestPaginateTypeDef,
    ListSessionsForWorkerResponseTypeDef,
    ListSessionsRequestPaginateTypeDef,
    ListSessionsResponseTypeDef,
    ListStepConsumersRequestPaginateTypeDef,
    ListStepConsumersResponseTypeDef,
    ListStepDependenciesRequestPaginateTypeDef,
    ListStepDependenciesResponseTypeDef,
    ListStepsRequestPaginateTypeDef,
    ListStepsResponseTypeDef,
    ListStorageProfilesForQueueRequestPaginateTypeDef,
    ListStorageProfilesForQueueResponseTypeDef,
    ListStorageProfilesRequestPaginateTypeDef,
    ListStorageProfilesResponseTypeDef,
    ListTasksRequestPaginateTypeDef,
    ListTasksResponseTypeDef,
    ListWorkersRequestPaginateTypeDef,
    ListWorkersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetSessionsStatisticsAggregationPaginator",
    "ListAvailableMeteredProductsPaginator",
    "ListBudgetsPaginator",
    "ListFarmMembersPaginator",
    "ListFarmsPaginator",
    "ListFleetMembersPaginator",
    "ListFleetsPaginator",
    "ListJobMembersPaginator",
    "ListJobParameterDefinitionsPaginator",
    "ListJobsPaginator",
    "ListLicenseEndpointsPaginator",
    "ListLimitsPaginator",
    "ListMeteredProductsPaginator",
    "ListMonitorsPaginator",
    "ListQueueEnvironmentsPaginator",
    "ListQueueFleetAssociationsPaginator",
    "ListQueueLimitAssociationsPaginator",
    "ListQueueMembersPaginator",
    "ListQueuesPaginator",
    "ListSessionActionsPaginator",
    "ListSessionsForWorkerPaginator",
    "ListSessionsPaginator",
    "ListStepConsumersPaginator",
    "ListStepDependenciesPaginator",
    "ListStepsPaginator",
    "ListStorageProfilesForQueuePaginator",
    "ListStorageProfilesPaginator",
    "ListTasksPaginator",
    "ListWorkersPaginator",
)


if TYPE_CHECKING:
    _GetSessionsStatisticsAggregationPaginatorBase = AioPaginator[
        GetSessionsStatisticsAggregationResponseTypeDef
    ]
else:
    _GetSessionsStatisticsAggregationPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetSessionsStatisticsAggregationPaginator(_GetSessionsStatisticsAggregationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/GetSessionsStatisticsAggregation.html#DeadlineCloud.Paginator.GetSessionsStatisticsAggregation)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#getsessionsstatisticsaggregationpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetSessionsStatisticsAggregationRequestPaginateTypeDef]
    ) -> AioPageIterator[GetSessionsStatisticsAggregationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/GetSessionsStatisticsAggregation.html#DeadlineCloud.Paginator.GetSessionsStatisticsAggregation.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#getsessionsstatisticsaggregationpaginator)
        """


if TYPE_CHECKING:
    _ListAvailableMeteredProductsPaginatorBase = AioPaginator[
        ListAvailableMeteredProductsResponseTypeDef
    ]
else:
    _ListAvailableMeteredProductsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAvailableMeteredProductsPaginator(_ListAvailableMeteredProductsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListAvailableMeteredProducts.html#DeadlineCloud.Paginator.ListAvailableMeteredProducts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listavailablemeteredproductspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAvailableMeteredProductsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAvailableMeteredProductsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListAvailableMeteredProducts.html#DeadlineCloud.Paginator.ListAvailableMeteredProducts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listavailablemeteredproductspaginator)
        """


if TYPE_CHECKING:
    _ListBudgetsPaginatorBase = AioPaginator[ListBudgetsResponseTypeDef]
else:
    _ListBudgetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBudgetsPaginator(_ListBudgetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListBudgets.html#DeadlineCloud.Paginator.ListBudgets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listbudgetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBudgetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBudgetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListBudgets.html#DeadlineCloud.Paginator.ListBudgets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listbudgetspaginator)
        """


if TYPE_CHECKING:
    _ListFarmMembersPaginatorBase = AioPaginator[ListFarmMembersResponseTypeDef]
else:
    _ListFarmMembersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFarmMembersPaginator(_ListFarmMembersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFarmMembers.html#DeadlineCloud.Paginator.ListFarmMembers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfarmmemberspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFarmMembersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFarmMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFarmMembers.html#DeadlineCloud.Paginator.ListFarmMembers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfarmmemberspaginator)
        """


if TYPE_CHECKING:
    _ListFarmsPaginatorBase = AioPaginator[ListFarmsResponseTypeDef]
else:
    _ListFarmsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFarmsPaginator(_ListFarmsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFarms.html#DeadlineCloud.Paginator.ListFarms)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfarmspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFarmsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFarmsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFarms.html#DeadlineCloud.Paginator.ListFarms.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfarmspaginator)
        """


if TYPE_CHECKING:
    _ListFleetMembersPaginatorBase = AioPaginator[ListFleetMembersResponseTypeDef]
else:
    _ListFleetMembersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFleetMembersPaginator(_ListFleetMembersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFleetMembers.html#DeadlineCloud.Paginator.ListFleetMembers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfleetmemberspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFleetMembersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFleetMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFleetMembers.html#DeadlineCloud.Paginator.ListFleetMembers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfleetmemberspaginator)
        """


if TYPE_CHECKING:
    _ListFleetsPaginatorBase = AioPaginator[ListFleetsResponseTypeDef]
else:
    _ListFleetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFleetsPaginator(_ListFleetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFleets.html#DeadlineCloud.Paginator.ListFleets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfleetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFleetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFleetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListFleets.html#DeadlineCloud.Paginator.ListFleets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listfleetspaginator)
        """


if TYPE_CHECKING:
    _ListJobMembersPaginatorBase = AioPaginator[ListJobMembersResponseTypeDef]
else:
    _ListJobMembersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListJobMembersPaginator(_ListJobMembersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListJobMembers.html#DeadlineCloud.Paginator.ListJobMembers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listjobmemberspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobMembersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListJobMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListJobMembers.html#DeadlineCloud.Paginator.ListJobMembers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listjobmemberspaginator)
        """


if TYPE_CHECKING:
    _ListJobParameterDefinitionsPaginatorBase = AioPaginator[
        ListJobParameterDefinitionsResponseTypeDef
    ]
else:
    _ListJobParameterDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListJobParameterDefinitionsPaginator(_ListJobParameterDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListJobParameterDefinitions.html#DeadlineCloud.Paginator.ListJobParameterDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listjobparameterdefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobParameterDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListJobParameterDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListJobParameterDefinitions.html#DeadlineCloud.Paginator.ListJobParameterDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listjobparameterdefinitionspaginator)
        """


if TYPE_CHECKING:
    _ListJobsPaginatorBase = AioPaginator[ListJobsResponseTypeDef]
else:
    _ListJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListJobsPaginator(_ListJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListJobs.html#DeadlineCloud.Paginator.ListJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListJobs.html#DeadlineCloud.Paginator.ListJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listjobspaginator)
        """


if TYPE_CHECKING:
    _ListLicenseEndpointsPaginatorBase = AioPaginator[ListLicenseEndpointsResponseTypeDef]
else:
    _ListLicenseEndpointsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListLicenseEndpointsPaginator(_ListLicenseEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListLicenseEndpoints.html#DeadlineCloud.Paginator.ListLicenseEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listlicenseendpointspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLicenseEndpointsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLicenseEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListLicenseEndpoints.html#DeadlineCloud.Paginator.ListLicenseEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listlicenseendpointspaginator)
        """


if TYPE_CHECKING:
    _ListLimitsPaginatorBase = AioPaginator[ListLimitsResponseTypeDef]
else:
    _ListLimitsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListLimitsPaginator(_ListLimitsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListLimits.html#DeadlineCloud.Paginator.ListLimits)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listlimitspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLimitsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLimitsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListLimits.html#DeadlineCloud.Paginator.ListLimits.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listlimitspaginator)
        """


if TYPE_CHECKING:
    _ListMeteredProductsPaginatorBase = AioPaginator[ListMeteredProductsResponseTypeDef]
else:
    _ListMeteredProductsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListMeteredProductsPaginator(_ListMeteredProductsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListMeteredProducts.html#DeadlineCloud.Paginator.ListMeteredProducts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listmeteredproductspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMeteredProductsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMeteredProductsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListMeteredProducts.html#DeadlineCloud.Paginator.ListMeteredProducts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listmeteredproductspaginator)
        """


if TYPE_CHECKING:
    _ListMonitorsPaginatorBase = AioPaginator[ListMonitorsResponseTypeDef]
else:
    _ListMonitorsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListMonitorsPaginator(_ListMonitorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListMonitors.html#DeadlineCloud.Paginator.ListMonitors)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listmonitorspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMonitorsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMonitorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListMonitors.html#DeadlineCloud.Paginator.ListMonitors.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listmonitorspaginator)
        """


if TYPE_CHECKING:
    _ListQueueEnvironmentsPaginatorBase = AioPaginator[ListQueueEnvironmentsResponseTypeDef]
else:
    _ListQueueEnvironmentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListQueueEnvironmentsPaginator(_ListQueueEnvironmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueueEnvironments.html#DeadlineCloud.Paginator.ListQueueEnvironments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueueenvironmentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListQueueEnvironmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListQueueEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueueEnvironments.html#DeadlineCloud.Paginator.ListQueueEnvironments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueueenvironmentspaginator)
        """


if TYPE_CHECKING:
    _ListQueueFleetAssociationsPaginatorBase = AioPaginator[
        ListQueueFleetAssociationsResponseTypeDef
    ]
else:
    _ListQueueFleetAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListQueueFleetAssociationsPaginator(_ListQueueFleetAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueueFleetAssociations.html#DeadlineCloud.Paginator.ListQueueFleetAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueuefleetassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListQueueFleetAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListQueueFleetAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueueFleetAssociations.html#DeadlineCloud.Paginator.ListQueueFleetAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueuefleetassociationspaginator)
        """


if TYPE_CHECKING:
    _ListQueueLimitAssociationsPaginatorBase = AioPaginator[
        ListQueueLimitAssociationsResponseTypeDef
    ]
else:
    _ListQueueLimitAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListQueueLimitAssociationsPaginator(_ListQueueLimitAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueueLimitAssociations.html#DeadlineCloud.Paginator.ListQueueLimitAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueuelimitassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListQueueLimitAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListQueueLimitAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueueLimitAssociations.html#DeadlineCloud.Paginator.ListQueueLimitAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueuelimitassociationspaginator)
        """


if TYPE_CHECKING:
    _ListQueueMembersPaginatorBase = AioPaginator[ListQueueMembersResponseTypeDef]
else:
    _ListQueueMembersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListQueueMembersPaginator(_ListQueueMembersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueueMembers.html#DeadlineCloud.Paginator.ListQueueMembers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueuememberspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListQueueMembersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListQueueMembersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueueMembers.html#DeadlineCloud.Paginator.ListQueueMembers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueuememberspaginator)
        """


if TYPE_CHECKING:
    _ListQueuesPaginatorBase = AioPaginator[ListQueuesResponseTypeDef]
else:
    _ListQueuesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListQueuesPaginator(_ListQueuesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueues.html#DeadlineCloud.Paginator.ListQueues)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueuespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListQueuesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListQueues.html#DeadlineCloud.Paginator.ListQueues.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listqueuespaginator)
        """


if TYPE_CHECKING:
    _ListSessionActionsPaginatorBase = AioPaginator[ListSessionActionsResponseTypeDef]
else:
    _ListSessionActionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSessionActionsPaginator(_ListSessionActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSessionActions.html#DeadlineCloud.Paginator.ListSessionActions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listsessionactionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSessionActionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSessionActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSessionActions.html#DeadlineCloud.Paginator.ListSessionActions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listsessionactionspaginator)
        """


if TYPE_CHECKING:
    _ListSessionsForWorkerPaginatorBase = AioPaginator[ListSessionsForWorkerResponseTypeDef]
else:
    _ListSessionsForWorkerPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSessionsForWorkerPaginator(_ListSessionsForWorkerPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSessionsForWorker.html#DeadlineCloud.Paginator.ListSessionsForWorker)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listsessionsforworkerpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSessionsForWorkerRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSessionsForWorkerResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSessionsForWorker.html#DeadlineCloud.Paginator.ListSessionsForWorker.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listsessionsforworkerpaginator)
        """


if TYPE_CHECKING:
    _ListSessionsPaginatorBase = AioPaginator[ListSessionsResponseTypeDef]
else:
    _ListSessionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSessionsPaginator(_ListSessionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSessions.html#DeadlineCloud.Paginator.ListSessions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listsessionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSessionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSessions.html#DeadlineCloud.Paginator.ListSessions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listsessionspaginator)
        """


if TYPE_CHECKING:
    _ListStepConsumersPaginatorBase = AioPaginator[ListStepConsumersResponseTypeDef]
else:
    _ListStepConsumersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListStepConsumersPaginator(_ListStepConsumersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStepConsumers.html#DeadlineCloud.Paginator.ListStepConsumers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststepconsumerspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStepConsumersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListStepConsumersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStepConsumers.html#DeadlineCloud.Paginator.ListStepConsumers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststepconsumerspaginator)
        """


if TYPE_CHECKING:
    _ListStepDependenciesPaginatorBase = AioPaginator[ListStepDependenciesResponseTypeDef]
else:
    _ListStepDependenciesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListStepDependenciesPaginator(_ListStepDependenciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStepDependencies.html#DeadlineCloud.Paginator.ListStepDependencies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststepdependenciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStepDependenciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListStepDependenciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStepDependencies.html#DeadlineCloud.Paginator.ListStepDependencies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststepdependenciespaginator)
        """


if TYPE_CHECKING:
    _ListStepsPaginatorBase = AioPaginator[ListStepsResponseTypeDef]
else:
    _ListStepsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListStepsPaginator(_ListStepsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSteps.html#DeadlineCloud.Paginator.ListSteps)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststepspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStepsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListSteps.html#DeadlineCloud.Paginator.ListSteps.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststepspaginator)
        """


if TYPE_CHECKING:
    _ListStorageProfilesForQueuePaginatorBase = AioPaginator[
        ListStorageProfilesForQueueResponseTypeDef
    ]
else:
    _ListStorageProfilesForQueuePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListStorageProfilesForQueuePaginator(_ListStorageProfilesForQueuePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStorageProfilesForQueue.html#DeadlineCloud.Paginator.ListStorageProfilesForQueue)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststorageprofilesforqueuepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStorageProfilesForQueueRequestPaginateTypeDef]
    ) -> AioPageIterator[ListStorageProfilesForQueueResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStorageProfilesForQueue.html#DeadlineCloud.Paginator.ListStorageProfilesForQueue.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststorageprofilesforqueuepaginator)
        """


if TYPE_CHECKING:
    _ListStorageProfilesPaginatorBase = AioPaginator[ListStorageProfilesResponseTypeDef]
else:
    _ListStorageProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListStorageProfilesPaginator(_ListStorageProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStorageProfiles.html#DeadlineCloud.Paginator.ListStorageProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststorageprofilespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStorageProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListStorageProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListStorageProfiles.html#DeadlineCloud.Paginator.ListStorageProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#liststorageprofilespaginator)
        """


if TYPE_CHECKING:
    _ListTasksPaginatorBase = AioPaginator[ListTasksResponseTypeDef]
else:
    _ListTasksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTasksPaginator(_ListTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListTasks.html#DeadlineCloud.Paginator.ListTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listtaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTasksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListTasks.html#DeadlineCloud.Paginator.ListTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listtaskspaginator)
        """


if TYPE_CHECKING:
    _ListWorkersPaginatorBase = AioPaginator[ListWorkersResponseTypeDef]
else:
    _ListWorkersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWorkersPaginator(_ListWorkersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListWorkers.html#DeadlineCloud.Paginator.ListWorkers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listworkerspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/paginator/ListWorkers.html#DeadlineCloud.Paginator.ListWorkers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/paginators/#listworkerspaginator)
        """
