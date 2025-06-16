"""
Type annotations for databrew service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_databrew.client import GlueDataBrewClient
    from types_aiobotocore_databrew.paginator import (
        ListDatasetsPaginator,
        ListJobRunsPaginator,
        ListJobsPaginator,
        ListProjectsPaginator,
        ListRecipeVersionsPaginator,
        ListRecipesPaginator,
        ListRulesetsPaginator,
        ListSchedulesPaginator,
    )

    session = get_session()
    with session.create_client("databrew") as client:
        client: GlueDataBrewClient

        list_datasets_paginator: ListDatasetsPaginator = client.get_paginator("list_datasets")
        list_job_runs_paginator: ListJobRunsPaginator = client.get_paginator("list_job_runs")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
        list_recipe_versions_paginator: ListRecipeVersionsPaginator = client.get_paginator("list_recipe_versions")
        list_recipes_paginator: ListRecipesPaginator = client.get_paginator("list_recipes")
        list_rulesets_paginator: ListRulesetsPaginator = client.get_paginator("list_rulesets")
        list_schedules_paginator: ListSchedulesPaginator = client.get_paginator("list_schedules")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListDatasetsRequestPaginateTypeDef,
    ListDatasetsResponseTypeDef,
    ListJobRunsRequestPaginateTypeDef,
    ListJobRunsResponseTypeDef,
    ListJobsRequestPaginateTypeDef,
    ListJobsResponseTypeDef,
    ListProjectsRequestPaginateTypeDef,
    ListProjectsResponseTypeDef,
    ListRecipesRequestPaginateTypeDef,
    ListRecipesResponseTypeDef,
    ListRecipeVersionsRequestPaginateTypeDef,
    ListRecipeVersionsResponseTypeDef,
    ListRulesetsRequestPaginateTypeDef,
    ListRulesetsResponseTypeDef,
    ListSchedulesRequestPaginateTypeDef,
    ListSchedulesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListDatasetsPaginator",
    "ListJobRunsPaginator",
    "ListJobsPaginator",
    "ListProjectsPaginator",
    "ListRecipeVersionsPaginator",
    "ListRecipesPaginator",
    "ListRulesetsPaginator",
    "ListSchedulesPaginator",
)

if TYPE_CHECKING:
    _ListDatasetsPaginatorBase = AioPaginator[ListDatasetsResponseTypeDef]
else:
    _ListDatasetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDatasetsPaginator(_ListDatasetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListDatasets.html#GlueDataBrew.Paginator.ListDatasets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listdatasetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDatasetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListDatasets.html#GlueDataBrew.Paginator.ListDatasets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listdatasetspaginator)
        """

if TYPE_CHECKING:
    _ListJobRunsPaginatorBase = AioPaginator[ListJobRunsResponseTypeDef]
else:
    _ListJobRunsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListJobRunsPaginator(_ListJobRunsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListJobRuns.html#GlueDataBrew.Paginator.ListJobRuns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listjobrunspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobRunsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListJobRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListJobRuns.html#GlueDataBrew.Paginator.ListJobRuns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listjobrunspaginator)
        """

if TYPE_CHECKING:
    _ListJobsPaginatorBase = AioPaginator[ListJobsResponseTypeDef]
else:
    _ListJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListJobsPaginator(_ListJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListJobs.html#GlueDataBrew.Paginator.ListJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListJobs.html#GlueDataBrew.Paginator.ListJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listjobspaginator)
        """

if TYPE_CHECKING:
    _ListProjectsPaginatorBase = AioPaginator[ListProjectsResponseTypeDef]
else:
    _ListProjectsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProjectsPaginator(_ListProjectsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListProjects.html#GlueDataBrew.Paginator.ListProjects)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listprojectspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProjectsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProjectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListProjects.html#GlueDataBrew.Paginator.ListProjects.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listprojectspaginator)
        """

if TYPE_CHECKING:
    _ListRecipeVersionsPaginatorBase = AioPaginator[ListRecipeVersionsResponseTypeDef]
else:
    _ListRecipeVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRecipeVersionsPaginator(_ListRecipeVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListRecipeVersions.html#GlueDataBrew.Paginator.ListRecipeVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listrecipeversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecipeVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRecipeVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListRecipeVersions.html#GlueDataBrew.Paginator.ListRecipeVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listrecipeversionspaginator)
        """

if TYPE_CHECKING:
    _ListRecipesPaginatorBase = AioPaginator[ListRecipesResponseTypeDef]
else:
    _ListRecipesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRecipesPaginator(_ListRecipesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListRecipes.html#GlueDataBrew.Paginator.ListRecipes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listrecipespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecipesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRecipesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListRecipes.html#GlueDataBrew.Paginator.ListRecipes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listrecipespaginator)
        """

if TYPE_CHECKING:
    _ListRulesetsPaginatorBase = AioPaginator[ListRulesetsResponseTypeDef]
else:
    _ListRulesetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRulesetsPaginator(_ListRulesetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListRulesets.html#GlueDataBrew.Paginator.ListRulesets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listrulesetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRulesetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRulesetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListRulesets.html#GlueDataBrew.Paginator.ListRulesets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listrulesetspaginator)
        """

if TYPE_CHECKING:
    _ListSchedulesPaginatorBase = AioPaginator[ListSchedulesResponseTypeDef]
else:
    _ListSchedulesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSchedulesPaginator(_ListSchedulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListSchedules.html#GlueDataBrew.Paginator.ListSchedules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listschedulespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSchedulesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSchedulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew/paginator/ListSchedules.html#GlueDataBrew.Paginator.ListSchedules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/paginators/#listschedulespaginator)
        """
