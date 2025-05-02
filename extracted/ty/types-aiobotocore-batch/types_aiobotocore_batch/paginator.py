"""
Type annotations for batch service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_batch.client import BatchClient
    from types_aiobotocore_batch.paginator import (
        DescribeComputeEnvironmentsPaginator,
        DescribeJobDefinitionsPaginator,
        DescribeJobQueuesPaginator,
        ListConsumableResourcesPaginator,
        ListJobsByConsumableResourcePaginator,
        ListJobsPaginator,
        ListSchedulingPoliciesPaginator,
    )

    session = get_session()
    with session.create_client("batch") as client:
        client: BatchClient

        describe_compute_environments_paginator: DescribeComputeEnvironmentsPaginator = client.get_paginator("describe_compute_environments")
        describe_job_definitions_paginator: DescribeJobDefinitionsPaginator = client.get_paginator("describe_job_definitions")
        describe_job_queues_paginator: DescribeJobQueuesPaginator = client.get_paginator("describe_job_queues")
        list_consumable_resources_paginator: ListConsumableResourcesPaginator = client.get_paginator("list_consumable_resources")
        list_jobs_by_consumable_resource_paginator: ListJobsByConsumableResourcePaginator = client.get_paginator("list_jobs_by_consumable_resource")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_scheduling_policies_paginator: ListSchedulingPoliciesPaginator = client.get_paginator("list_scheduling_policies")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeComputeEnvironmentsRequestPaginateTypeDef,
    DescribeComputeEnvironmentsResponseTypeDef,
    DescribeJobDefinitionsRequestPaginateTypeDef,
    DescribeJobDefinitionsResponseTypeDef,
    DescribeJobQueuesRequestPaginateTypeDef,
    DescribeJobQueuesResponseTypeDef,
    ListConsumableResourcesRequestPaginateTypeDef,
    ListConsumableResourcesResponseTypeDef,
    ListJobsByConsumableResourceRequestPaginateTypeDef,
    ListJobsByConsumableResourceResponseTypeDef,
    ListJobsRequestPaginateTypeDef,
    ListJobsResponseTypeDef,
    ListSchedulingPoliciesRequestPaginateTypeDef,
    ListSchedulingPoliciesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeComputeEnvironmentsPaginator",
    "DescribeJobDefinitionsPaginator",
    "DescribeJobQueuesPaginator",
    "ListConsumableResourcesPaginator",
    "ListJobsByConsumableResourcePaginator",
    "ListJobsPaginator",
    "ListSchedulingPoliciesPaginator",
)


if TYPE_CHECKING:
    _DescribeComputeEnvironmentsPaginatorBase = AioPaginator[
        DescribeComputeEnvironmentsResponseTypeDef
    ]
else:
    _DescribeComputeEnvironmentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeComputeEnvironmentsPaginator(_DescribeComputeEnvironmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/DescribeComputeEnvironments.html#Batch.Paginator.DescribeComputeEnvironments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/paginators/#describecomputeenvironmentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeComputeEnvironmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeComputeEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/DescribeComputeEnvironments.html#Batch.Paginator.DescribeComputeEnvironments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/paginators/#describecomputeenvironmentspaginator)
        """


if TYPE_CHECKING:
    _DescribeJobDefinitionsPaginatorBase = AioPaginator[DescribeJobDefinitionsResponseTypeDef]
else:
    _DescribeJobDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeJobDefinitionsPaginator(_DescribeJobDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/DescribeJobDefinitions.html#Batch.Paginator.DescribeJobDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/paginators/#describejobdefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeJobDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/DescribeJobDefinitions.html#Batch.Paginator.DescribeJobDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/paginators/#describejobdefinitionspaginator)
        """


if TYPE_CHECKING:
    _DescribeJobQueuesPaginatorBase = AioPaginator[DescribeJobQueuesResponseTypeDef]
else:
    _DescribeJobQueuesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeJobQueuesPaginator(_DescribeJobQueuesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/DescribeJobQueues.html#Batch.Paginator.DescribeJobQueues)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/paginators/#describejobqueuespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeJobQueuesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeJobQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/DescribeJobQueues.html#Batch.Paginator.DescribeJobQueues.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/paginators/#describejobqueuespaginator)
        """


if TYPE_CHECKING:
    _ListConsumableResourcesPaginatorBase = AioPaginator[ListConsumableResourcesResponseTypeDef]
else:
    _ListConsumableResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListConsumableResourcesPaginator(_ListConsumableResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/ListConsumableResources.html#Batch.Paginator.ListConsumableResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/paginators/#listconsumableresourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConsumableResourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConsumableResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/ListConsumableResources.html#Batch.Paginator.ListConsumableResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/paginators/#listconsumableresourcespaginator)
        """


if TYPE_CHECKING:
    _ListJobsByConsumableResourcePaginatorBase = AioPaginator[
        ListJobsByConsumableResourceResponseTypeDef
    ]
else:
    _ListJobsByConsumableResourcePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListJobsByConsumableResourcePaginator(_ListJobsByConsumableResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/ListJobsByConsumableResource.html#Batch.Paginator.ListJobsByConsumableResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/paginators/#listjobsbyconsumableresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobsByConsumableResourceRequestPaginateTypeDef]
    ) -> AioPageIterator[ListJobsByConsumableResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/ListJobsByConsumableResource.html#Batch.Paginator.ListJobsByConsumableResource.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/paginators/#listjobsbyconsumableresourcepaginator)
        """


if TYPE_CHECKING:
    _ListJobsPaginatorBase = AioPaginator[ListJobsResponseTypeDef]
else:
    _ListJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListJobsPaginator(_ListJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/ListJobs.html#Batch.Paginator.ListJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/paginators/#listjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/ListJobs.html#Batch.Paginator.ListJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/paginators/#listjobspaginator)
        """


if TYPE_CHECKING:
    _ListSchedulingPoliciesPaginatorBase = AioPaginator[ListSchedulingPoliciesResponseTypeDef]
else:
    _ListSchedulingPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSchedulingPoliciesPaginator(_ListSchedulingPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/ListSchedulingPolicies.html#Batch.Paginator.ListSchedulingPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/paginators/#listschedulingpoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSchedulingPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSchedulingPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/batch/paginator/ListSchedulingPolicies.html#Batch.Paginator.ListSchedulingPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_batch/paginators/#listschedulingpoliciespaginator)
        """
