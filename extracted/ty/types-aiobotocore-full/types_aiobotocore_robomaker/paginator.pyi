"""
Type annotations for robomaker service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_robomaker.client import RoboMakerClient
    from types_aiobotocore_robomaker.paginator import (
        ListDeploymentJobsPaginator,
        ListFleetsPaginator,
        ListRobotApplicationsPaginator,
        ListRobotsPaginator,
        ListSimulationApplicationsPaginator,
        ListSimulationJobBatchesPaginator,
        ListSimulationJobsPaginator,
        ListWorldExportJobsPaginator,
        ListWorldGenerationJobsPaginator,
        ListWorldTemplatesPaginator,
        ListWorldsPaginator,
    )

    session = get_session()
    with session.create_client("robomaker") as client:
        client: RoboMakerClient

        list_deployment_jobs_paginator: ListDeploymentJobsPaginator = client.get_paginator("list_deployment_jobs")
        list_fleets_paginator: ListFleetsPaginator = client.get_paginator("list_fleets")
        list_robot_applications_paginator: ListRobotApplicationsPaginator = client.get_paginator("list_robot_applications")
        list_robots_paginator: ListRobotsPaginator = client.get_paginator("list_robots")
        list_simulation_applications_paginator: ListSimulationApplicationsPaginator = client.get_paginator("list_simulation_applications")
        list_simulation_job_batches_paginator: ListSimulationJobBatchesPaginator = client.get_paginator("list_simulation_job_batches")
        list_simulation_jobs_paginator: ListSimulationJobsPaginator = client.get_paginator("list_simulation_jobs")
        list_world_export_jobs_paginator: ListWorldExportJobsPaginator = client.get_paginator("list_world_export_jobs")
        list_world_generation_jobs_paginator: ListWorldGenerationJobsPaginator = client.get_paginator("list_world_generation_jobs")
        list_world_templates_paginator: ListWorldTemplatesPaginator = client.get_paginator("list_world_templates")
        list_worlds_paginator: ListWorldsPaginator = client.get_paginator("list_worlds")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListDeploymentJobsRequestPaginateTypeDef,
    ListDeploymentJobsResponseTypeDef,
    ListFleetsRequestPaginateTypeDef,
    ListFleetsResponseTypeDef,
    ListRobotApplicationsRequestPaginateTypeDef,
    ListRobotApplicationsResponseTypeDef,
    ListRobotsRequestPaginateTypeDef,
    ListRobotsResponseTypeDef,
    ListSimulationApplicationsRequestPaginateTypeDef,
    ListSimulationApplicationsResponseTypeDef,
    ListSimulationJobBatchesRequestPaginateTypeDef,
    ListSimulationJobBatchesResponseTypeDef,
    ListSimulationJobsRequestPaginateTypeDef,
    ListSimulationJobsResponseTypeDef,
    ListWorldExportJobsRequestPaginateTypeDef,
    ListWorldExportJobsResponseTypeDef,
    ListWorldGenerationJobsRequestPaginateTypeDef,
    ListWorldGenerationJobsResponseTypeDef,
    ListWorldsRequestPaginateTypeDef,
    ListWorldsResponseTypeDef,
    ListWorldTemplatesRequestPaginateTypeDef,
    ListWorldTemplatesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListDeploymentJobsPaginator",
    "ListFleetsPaginator",
    "ListRobotApplicationsPaginator",
    "ListRobotsPaginator",
    "ListSimulationApplicationsPaginator",
    "ListSimulationJobBatchesPaginator",
    "ListSimulationJobsPaginator",
    "ListWorldExportJobsPaginator",
    "ListWorldGenerationJobsPaginator",
    "ListWorldTemplatesPaginator",
    "ListWorldsPaginator",
)

if TYPE_CHECKING:
    _ListDeploymentJobsPaginatorBase = AioPaginator[ListDeploymentJobsResponseTypeDef]
else:
    _ListDeploymentJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDeploymentJobsPaginator(_ListDeploymentJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListDeploymentJobs.html#RoboMaker.Paginator.ListDeploymentJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listdeploymentjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeploymentJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDeploymentJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListDeploymentJobs.html#RoboMaker.Paginator.ListDeploymentJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listdeploymentjobspaginator)
        """

if TYPE_CHECKING:
    _ListFleetsPaginatorBase = AioPaginator[ListFleetsResponseTypeDef]
else:
    _ListFleetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFleetsPaginator(_ListFleetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListFleets.html#RoboMaker.Paginator.ListFleets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listfleetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFleetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFleetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListFleets.html#RoboMaker.Paginator.ListFleets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listfleetspaginator)
        """

if TYPE_CHECKING:
    _ListRobotApplicationsPaginatorBase = AioPaginator[ListRobotApplicationsResponseTypeDef]
else:
    _ListRobotApplicationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRobotApplicationsPaginator(_ListRobotApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListRobotApplications.html#RoboMaker.Paginator.ListRobotApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listrobotapplicationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRobotApplicationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRobotApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListRobotApplications.html#RoboMaker.Paginator.ListRobotApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listrobotapplicationspaginator)
        """

if TYPE_CHECKING:
    _ListRobotsPaginatorBase = AioPaginator[ListRobotsResponseTypeDef]
else:
    _ListRobotsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRobotsPaginator(_ListRobotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListRobots.html#RoboMaker.Paginator.ListRobots)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listrobotspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRobotsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRobotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListRobots.html#RoboMaker.Paginator.ListRobots.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listrobotspaginator)
        """

if TYPE_CHECKING:
    _ListSimulationApplicationsPaginatorBase = AioPaginator[
        ListSimulationApplicationsResponseTypeDef
    ]
else:
    _ListSimulationApplicationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSimulationApplicationsPaginator(_ListSimulationApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListSimulationApplications.html#RoboMaker.Paginator.ListSimulationApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listsimulationapplicationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSimulationApplicationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSimulationApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListSimulationApplications.html#RoboMaker.Paginator.ListSimulationApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listsimulationapplicationspaginator)
        """

if TYPE_CHECKING:
    _ListSimulationJobBatchesPaginatorBase = AioPaginator[ListSimulationJobBatchesResponseTypeDef]
else:
    _ListSimulationJobBatchesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSimulationJobBatchesPaginator(_ListSimulationJobBatchesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListSimulationJobBatches.html#RoboMaker.Paginator.ListSimulationJobBatches)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listsimulationjobbatchespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSimulationJobBatchesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSimulationJobBatchesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListSimulationJobBatches.html#RoboMaker.Paginator.ListSimulationJobBatches.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listsimulationjobbatchespaginator)
        """

if TYPE_CHECKING:
    _ListSimulationJobsPaginatorBase = AioPaginator[ListSimulationJobsResponseTypeDef]
else:
    _ListSimulationJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSimulationJobsPaginator(_ListSimulationJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListSimulationJobs.html#RoboMaker.Paginator.ListSimulationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listsimulationjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSimulationJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSimulationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListSimulationJobs.html#RoboMaker.Paginator.ListSimulationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listsimulationjobspaginator)
        """

if TYPE_CHECKING:
    _ListWorldExportJobsPaginatorBase = AioPaginator[ListWorldExportJobsResponseTypeDef]
else:
    _ListWorldExportJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListWorldExportJobsPaginator(_ListWorldExportJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorldExportJobs.html#RoboMaker.Paginator.ListWorldExportJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listworldexportjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorldExportJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorldExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorldExportJobs.html#RoboMaker.Paginator.ListWorldExportJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listworldexportjobspaginator)
        """

if TYPE_CHECKING:
    _ListWorldGenerationJobsPaginatorBase = AioPaginator[ListWorldGenerationJobsResponseTypeDef]
else:
    _ListWorldGenerationJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListWorldGenerationJobsPaginator(_ListWorldGenerationJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorldGenerationJobs.html#RoboMaker.Paginator.ListWorldGenerationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listworldgenerationjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorldGenerationJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorldGenerationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorldGenerationJobs.html#RoboMaker.Paginator.ListWorldGenerationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listworldgenerationjobspaginator)
        """

if TYPE_CHECKING:
    _ListWorldTemplatesPaginatorBase = AioPaginator[ListWorldTemplatesResponseTypeDef]
else:
    _ListWorldTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListWorldTemplatesPaginator(_ListWorldTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorldTemplates.html#RoboMaker.Paginator.ListWorldTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listworldtemplatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorldTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorldTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorldTemplates.html#RoboMaker.Paginator.ListWorldTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listworldtemplatespaginator)
        """

if TYPE_CHECKING:
    _ListWorldsPaginatorBase = AioPaginator[ListWorldsResponseTypeDef]
else:
    _ListWorldsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListWorldsPaginator(_ListWorldsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorlds.html#RoboMaker.Paginator.ListWorlds)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listworldspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorldsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorldsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/robomaker/paginator/ListWorlds.html#RoboMaker.Paginator.ListWorlds.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_robomaker/paginators/#listworldspaginator)
        """
