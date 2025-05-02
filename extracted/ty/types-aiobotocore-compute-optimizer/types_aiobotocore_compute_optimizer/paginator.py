"""
Type annotations for compute-optimizer service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_compute_optimizer.client import ComputeOptimizerClient
    from types_aiobotocore_compute_optimizer.paginator import (
        DescribeRecommendationExportJobsPaginator,
        GetEnrollmentStatusesForOrganizationPaginator,
        GetLambdaFunctionRecommendationsPaginator,
        GetRecommendationPreferencesPaginator,
        GetRecommendationSummariesPaginator,
    )

    session = get_session()
    with session.create_client("compute-optimizer") as client:
        client: ComputeOptimizerClient

        describe_recommendation_export_jobs_paginator: DescribeRecommendationExportJobsPaginator = client.get_paginator("describe_recommendation_export_jobs")
        get_enrollment_statuses_for_organization_paginator: GetEnrollmentStatusesForOrganizationPaginator = client.get_paginator("get_enrollment_statuses_for_organization")
        get_lambda_function_recommendations_paginator: GetLambdaFunctionRecommendationsPaginator = client.get_paginator("get_lambda_function_recommendations")
        get_recommendation_preferences_paginator: GetRecommendationPreferencesPaginator = client.get_paginator("get_recommendation_preferences")
        get_recommendation_summaries_paginator: GetRecommendationSummariesPaginator = client.get_paginator("get_recommendation_summaries")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeRecommendationExportJobsRequestPaginateTypeDef,
    DescribeRecommendationExportJobsResponseTypeDef,
    GetEnrollmentStatusesForOrganizationRequestPaginateTypeDef,
    GetEnrollmentStatusesForOrganizationResponseTypeDef,
    GetLambdaFunctionRecommendationsRequestPaginateTypeDef,
    GetLambdaFunctionRecommendationsResponseTypeDef,
    GetRecommendationPreferencesRequestPaginateTypeDef,
    GetRecommendationPreferencesResponseTypeDef,
    GetRecommendationSummariesRequestPaginateTypeDef,
    GetRecommendationSummariesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeRecommendationExportJobsPaginator",
    "GetEnrollmentStatusesForOrganizationPaginator",
    "GetLambdaFunctionRecommendationsPaginator",
    "GetRecommendationPreferencesPaginator",
    "GetRecommendationSummariesPaginator",
)


if TYPE_CHECKING:
    _DescribeRecommendationExportJobsPaginatorBase = AioPaginator[
        DescribeRecommendationExportJobsResponseTypeDef
    ]
else:
    _DescribeRecommendationExportJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeRecommendationExportJobsPaginator(_DescribeRecommendationExportJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/paginator/DescribeRecommendationExportJobs.html#ComputeOptimizer.Paginator.DescribeRecommendationExportJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/paginators/#describerecommendationexportjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeRecommendationExportJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeRecommendationExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/paginator/DescribeRecommendationExportJobs.html#ComputeOptimizer.Paginator.DescribeRecommendationExportJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/paginators/#describerecommendationexportjobspaginator)
        """


if TYPE_CHECKING:
    _GetEnrollmentStatusesForOrganizationPaginatorBase = AioPaginator[
        GetEnrollmentStatusesForOrganizationResponseTypeDef
    ]
else:
    _GetEnrollmentStatusesForOrganizationPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetEnrollmentStatusesForOrganizationPaginator(
    _GetEnrollmentStatusesForOrganizationPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/paginator/GetEnrollmentStatusesForOrganization.html#ComputeOptimizer.Paginator.GetEnrollmentStatusesForOrganization)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/paginators/#getenrollmentstatusesfororganizationpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetEnrollmentStatusesForOrganizationRequestPaginateTypeDef]
    ) -> AioPageIterator[GetEnrollmentStatusesForOrganizationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/paginator/GetEnrollmentStatusesForOrganization.html#ComputeOptimizer.Paginator.GetEnrollmentStatusesForOrganization.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/paginators/#getenrollmentstatusesfororganizationpaginator)
        """


if TYPE_CHECKING:
    _GetLambdaFunctionRecommendationsPaginatorBase = AioPaginator[
        GetLambdaFunctionRecommendationsResponseTypeDef
    ]
else:
    _GetLambdaFunctionRecommendationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetLambdaFunctionRecommendationsPaginator(_GetLambdaFunctionRecommendationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/paginator/GetLambdaFunctionRecommendations.html#ComputeOptimizer.Paginator.GetLambdaFunctionRecommendations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/paginators/#getlambdafunctionrecommendationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetLambdaFunctionRecommendationsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetLambdaFunctionRecommendationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/paginator/GetLambdaFunctionRecommendations.html#ComputeOptimizer.Paginator.GetLambdaFunctionRecommendations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/paginators/#getlambdafunctionrecommendationspaginator)
        """


if TYPE_CHECKING:
    _GetRecommendationPreferencesPaginatorBase = AioPaginator[
        GetRecommendationPreferencesResponseTypeDef
    ]
else:
    _GetRecommendationPreferencesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetRecommendationPreferencesPaginator(_GetRecommendationPreferencesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/paginator/GetRecommendationPreferences.html#ComputeOptimizer.Paginator.GetRecommendationPreferences)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/paginators/#getrecommendationpreferencespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetRecommendationPreferencesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetRecommendationPreferencesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/paginator/GetRecommendationPreferences.html#ComputeOptimizer.Paginator.GetRecommendationPreferences.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/paginators/#getrecommendationpreferencespaginator)
        """


if TYPE_CHECKING:
    _GetRecommendationSummariesPaginatorBase = AioPaginator[
        GetRecommendationSummariesResponseTypeDef
    ]
else:
    _GetRecommendationSummariesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetRecommendationSummariesPaginator(_GetRecommendationSummariesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/paginator/GetRecommendationSummaries.html#ComputeOptimizer.Paginator.GetRecommendationSummaries)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/paginators/#getrecommendationsummariespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetRecommendationSummariesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetRecommendationSummariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/compute-optimizer/paginator/GetRecommendationSummaries.html#ComputeOptimizer.Paginator.GetRecommendationSummaries.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_compute_optimizer/paginators/#getrecommendationsummariespaginator)
        """
