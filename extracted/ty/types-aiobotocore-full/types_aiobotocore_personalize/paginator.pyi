"""
Type annotations for personalize service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_personalize.client import PersonalizeClient
    from types_aiobotocore_personalize.paginator import (
        ListBatchInferenceJobsPaginator,
        ListBatchSegmentJobsPaginator,
        ListCampaignsPaginator,
        ListDatasetExportJobsPaginator,
        ListDatasetGroupsPaginator,
        ListDatasetImportJobsPaginator,
        ListDatasetsPaginator,
        ListEventTrackersPaginator,
        ListFiltersPaginator,
        ListMetricAttributionMetricsPaginator,
        ListMetricAttributionsPaginator,
        ListRecipesPaginator,
        ListRecommendersPaginator,
        ListSchemasPaginator,
        ListSolutionVersionsPaginator,
        ListSolutionsPaginator,
    )

    session = get_session()
    with session.create_client("personalize") as client:
        client: PersonalizeClient

        list_batch_inference_jobs_paginator: ListBatchInferenceJobsPaginator = client.get_paginator("list_batch_inference_jobs")
        list_batch_segment_jobs_paginator: ListBatchSegmentJobsPaginator = client.get_paginator("list_batch_segment_jobs")
        list_campaigns_paginator: ListCampaignsPaginator = client.get_paginator("list_campaigns")
        list_dataset_export_jobs_paginator: ListDatasetExportJobsPaginator = client.get_paginator("list_dataset_export_jobs")
        list_dataset_groups_paginator: ListDatasetGroupsPaginator = client.get_paginator("list_dataset_groups")
        list_dataset_import_jobs_paginator: ListDatasetImportJobsPaginator = client.get_paginator("list_dataset_import_jobs")
        list_datasets_paginator: ListDatasetsPaginator = client.get_paginator("list_datasets")
        list_event_trackers_paginator: ListEventTrackersPaginator = client.get_paginator("list_event_trackers")
        list_filters_paginator: ListFiltersPaginator = client.get_paginator("list_filters")
        list_metric_attribution_metrics_paginator: ListMetricAttributionMetricsPaginator = client.get_paginator("list_metric_attribution_metrics")
        list_metric_attributions_paginator: ListMetricAttributionsPaginator = client.get_paginator("list_metric_attributions")
        list_recipes_paginator: ListRecipesPaginator = client.get_paginator("list_recipes")
        list_recommenders_paginator: ListRecommendersPaginator = client.get_paginator("list_recommenders")
        list_schemas_paginator: ListSchemasPaginator = client.get_paginator("list_schemas")
        list_solution_versions_paginator: ListSolutionVersionsPaginator = client.get_paginator("list_solution_versions")
        list_solutions_paginator: ListSolutionsPaginator = client.get_paginator("list_solutions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListBatchInferenceJobsRequestPaginateTypeDef,
    ListBatchInferenceJobsResponseTypeDef,
    ListBatchSegmentJobsRequestPaginateTypeDef,
    ListBatchSegmentJobsResponseTypeDef,
    ListCampaignsRequestPaginateTypeDef,
    ListCampaignsResponseTypeDef,
    ListDatasetExportJobsRequestPaginateTypeDef,
    ListDatasetExportJobsResponseTypeDef,
    ListDatasetGroupsRequestPaginateTypeDef,
    ListDatasetGroupsResponseTypeDef,
    ListDatasetImportJobsRequestPaginateTypeDef,
    ListDatasetImportJobsResponseTypeDef,
    ListDatasetsRequestPaginateTypeDef,
    ListDatasetsResponseTypeDef,
    ListEventTrackersRequestPaginateTypeDef,
    ListEventTrackersResponseTypeDef,
    ListFiltersRequestPaginateTypeDef,
    ListFiltersResponseTypeDef,
    ListMetricAttributionMetricsRequestPaginateTypeDef,
    ListMetricAttributionMetricsResponseTypeDef,
    ListMetricAttributionsRequestPaginateTypeDef,
    ListMetricAttributionsResponseTypeDef,
    ListRecipesRequestPaginateTypeDef,
    ListRecipesResponseTypeDef,
    ListRecommendersRequestPaginateTypeDef,
    ListRecommendersResponseTypeDef,
    ListSchemasRequestPaginateTypeDef,
    ListSchemasResponseTypeDef,
    ListSolutionsRequestPaginateTypeDef,
    ListSolutionsResponseTypeDef,
    ListSolutionVersionsRequestPaginateTypeDef,
    ListSolutionVersionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListBatchInferenceJobsPaginator",
    "ListBatchSegmentJobsPaginator",
    "ListCampaignsPaginator",
    "ListDatasetExportJobsPaginator",
    "ListDatasetGroupsPaginator",
    "ListDatasetImportJobsPaginator",
    "ListDatasetsPaginator",
    "ListEventTrackersPaginator",
    "ListFiltersPaginator",
    "ListMetricAttributionMetricsPaginator",
    "ListMetricAttributionsPaginator",
    "ListRecipesPaginator",
    "ListRecommendersPaginator",
    "ListSchemasPaginator",
    "ListSolutionVersionsPaginator",
    "ListSolutionsPaginator",
)

if TYPE_CHECKING:
    _ListBatchInferenceJobsPaginatorBase = AioPaginator[ListBatchInferenceJobsResponseTypeDef]
else:
    _ListBatchInferenceJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBatchInferenceJobsPaginator(_ListBatchInferenceJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListBatchInferenceJobs.html#Personalize.Paginator.ListBatchInferenceJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listbatchinferencejobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBatchInferenceJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBatchInferenceJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListBatchInferenceJobs.html#Personalize.Paginator.ListBatchInferenceJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listbatchinferencejobspaginator)
        """

if TYPE_CHECKING:
    _ListBatchSegmentJobsPaginatorBase = AioPaginator[ListBatchSegmentJobsResponseTypeDef]
else:
    _ListBatchSegmentJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBatchSegmentJobsPaginator(_ListBatchSegmentJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListBatchSegmentJobs.html#Personalize.Paginator.ListBatchSegmentJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listbatchsegmentjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBatchSegmentJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBatchSegmentJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListBatchSegmentJobs.html#Personalize.Paginator.ListBatchSegmentJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listbatchsegmentjobspaginator)
        """

if TYPE_CHECKING:
    _ListCampaignsPaginatorBase = AioPaginator[ListCampaignsResponseTypeDef]
else:
    _ListCampaignsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCampaignsPaginator(_ListCampaignsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListCampaigns.html#Personalize.Paginator.ListCampaigns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listcampaignspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCampaignsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCampaignsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListCampaigns.html#Personalize.Paginator.ListCampaigns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listcampaignspaginator)
        """

if TYPE_CHECKING:
    _ListDatasetExportJobsPaginatorBase = AioPaginator[ListDatasetExportJobsResponseTypeDef]
else:
    _ListDatasetExportJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDatasetExportJobsPaginator(_ListDatasetExportJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListDatasetExportJobs.html#Personalize.Paginator.ListDatasetExportJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listdatasetexportjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDatasetExportJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDatasetExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListDatasetExportJobs.html#Personalize.Paginator.ListDatasetExportJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listdatasetexportjobspaginator)
        """

if TYPE_CHECKING:
    _ListDatasetGroupsPaginatorBase = AioPaginator[ListDatasetGroupsResponseTypeDef]
else:
    _ListDatasetGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDatasetGroupsPaginator(_ListDatasetGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListDatasetGroups.html#Personalize.Paginator.ListDatasetGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listdatasetgroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDatasetGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDatasetGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListDatasetGroups.html#Personalize.Paginator.ListDatasetGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listdatasetgroupspaginator)
        """

if TYPE_CHECKING:
    _ListDatasetImportJobsPaginatorBase = AioPaginator[ListDatasetImportJobsResponseTypeDef]
else:
    _ListDatasetImportJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDatasetImportJobsPaginator(_ListDatasetImportJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListDatasetImportJobs.html#Personalize.Paginator.ListDatasetImportJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listdatasetimportjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDatasetImportJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDatasetImportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListDatasetImportJobs.html#Personalize.Paginator.ListDatasetImportJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listdatasetimportjobspaginator)
        """

if TYPE_CHECKING:
    _ListDatasetsPaginatorBase = AioPaginator[ListDatasetsResponseTypeDef]
else:
    _ListDatasetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDatasetsPaginator(_ListDatasetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListDatasets.html#Personalize.Paginator.ListDatasets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listdatasetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDatasetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListDatasets.html#Personalize.Paginator.ListDatasets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listdatasetspaginator)
        """

if TYPE_CHECKING:
    _ListEventTrackersPaginatorBase = AioPaginator[ListEventTrackersResponseTypeDef]
else:
    _ListEventTrackersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEventTrackersPaginator(_ListEventTrackersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListEventTrackers.html#Personalize.Paginator.ListEventTrackers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listeventtrackerspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventTrackersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEventTrackersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListEventTrackers.html#Personalize.Paginator.ListEventTrackers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listeventtrackerspaginator)
        """

if TYPE_CHECKING:
    _ListFiltersPaginatorBase = AioPaginator[ListFiltersResponseTypeDef]
else:
    _ListFiltersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFiltersPaginator(_ListFiltersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListFilters.html#Personalize.Paginator.ListFilters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listfilterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFiltersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFiltersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListFilters.html#Personalize.Paginator.ListFilters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listfilterspaginator)
        """

if TYPE_CHECKING:
    _ListMetricAttributionMetricsPaginatorBase = AioPaginator[
        ListMetricAttributionMetricsResponseTypeDef
    ]
else:
    _ListMetricAttributionMetricsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMetricAttributionMetricsPaginator(_ListMetricAttributionMetricsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListMetricAttributionMetrics.html#Personalize.Paginator.ListMetricAttributionMetrics)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listmetricattributionmetricspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMetricAttributionMetricsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMetricAttributionMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListMetricAttributionMetrics.html#Personalize.Paginator.ListMetricAttributionMetrics.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listmetricattributionmetricspaginator)
        """

if TYPE_CHECKING:
    _ListMetricAttributionsPaginatorBase = AioPaginator[ListMetricAttributionsResponseTypeDef]
else:
    _ListMetricAttributionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMetricAttributionsPaginator(_ListMetricAttributionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListMetricAttributions.html#Personalize.Paginator.ListMetricAttributions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listmetricattributionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMetricAttributionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMetricAttributionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListMetricAttributions.html#Personalize.Paginator.ListMetricAttributions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listmetricattributionspaginator)
        """

if TYPE_CHECKING:
    _ListRecipesPaginatorBase = AioPaginator[ListRecipesResponseTypeDef]
else:
    _ListRecipesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRecipesPaginator(_ListRecipesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListRecipes.html#Personalize.Paginator.ListRecipes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listrecipespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecipesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRecipesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListRecipes.html#Personalize.Paginator.ListRecipes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listrecipespaginator)
        """

if TYPE_CHECKING:
    _ListRecommendersPaginatorBase = AioPaginator[ListRecommendersResponseTypeDef]
else:
    _ListRecommendersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRecommendersPaginator(_ListRecommendersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListRecommenders.html#Personalize.Paginator.ListRecommenders)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listrecommenderspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecommendersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRecommendersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListRecommenders.html#Personalize.Paginator.ListRecommenders.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listrecommenderspaginator)
        """

if TYPE_CHECKING:
    _ListSchemasPaginatorBase = AioPaginator[ListSchemasResponseTypeDef]
else:
    _ListSchemasPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSchemasPaginator(_ListSchemasPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListSchemas.html#Personalize.Paginator.ListSchemas)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listschemaspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSchemasRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSchemasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListSchemas.html#Personalize.Paginator.ListSchemas.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listschemaspaginator)
        """

if TYPE_CHECKING:
    _ListSolutionVersionsPaginatorBase = AioPaginator[ListSolutionVersionsResponseTypeDef]
else:
    _ListSolutionVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSolutionVersionsPaginator(_ListSolutionVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListSolutionVersions.html#Personalize.Paginator.ListSolutionVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listsolutionversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSolutionVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSolutionVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListSolutionVersions.html#Personalize.Paginator.ListSolutionVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listsolutionversionspaginator)
        """

if TYPE_CHECKING:
    _ListSolutionsPaginatorBase = AioPaginator[ListSolutionsResponseTypeDef]
else:
    _ListSolutionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSolutionsPaginator(_ListSolutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListSolutions.html#Personalize.Paginator.ListSolutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listsolutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSolutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSolutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize/paginator/ListSolutions.html#Personalize.Paginator.ListSolutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize/paginators/#listsolutionspaginator)
        """
