"""
Type annotations for marketplace-catalog service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_catalog/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_marketplace_catalog.client import MarketplaceCatalogClient
    from types_aiobotocore_marketplace_catalog.paginator import (
        DescribeAssessmentPaginator,
        ListAssessmentsPaginator,
        ListChangeSetsPaginator,
        ListEntitiesPaginator,
    )

    session = get_session()
    with session.create_client("marketplace-catalog") as client:
        client: MarketplaceCatalogClient

        describe_assessment_paginator: DescribeAssessmentPaginator = client.get_paginator("describe_assessment")
        list_assessments_paginator: ListAssessmentsPaginator = client.get_paginator("list_assessments")
        list_change_sets_paginator: ListChangeSetsPaginator = client.get_paginator("list_change_sets")
        list_entities_paginator: ListEntitiesPaginator = client.get_paginator("list_entities")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeAssessmentRequestPaginateTypeDef,
    DescribeAssessmentResponseTypeDef,
    ListAssessmentsRequestPaginateTypeDef,
    ListAssessmentsResponseTypeDef,
    ListChangeSetsRequestPaginateTypeDef,
    ListChangeSetsResponseTypeDef,
    ListEntitiesRequestPaginateTypeDef,
    ListEntitiesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeAssessmentPaginator",
    "ListAssessmentsPaginator",
    "ListChangeSetsPaginator",
    "ListEntitiesPaginator",
)

if TYPE_CHECKING:
    _DescribeAssessmentPaginatorBase = AioPaginator[DescribeAssessmentResponseTypeDef]
else:
    _DescribeAssessmentPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeAssessmentPaginator(_DescribeAssessmentPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-catalog/paginator/DescribeAssessment.html#MarketplaceCatalog.Paginator.DescribeAssessment)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_catalog/paginators/#describeassessmentpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAssessmentRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeAssessmentResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-catalog/paginator/DescribeAssessment.html#MarketplaceCatalog.Paginator.DescribeAssessment.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_catalog/paginators/#describeassessmentpaginator)
        """

if TYPE_CHECKING:
    _ListAssessmentsPaginatorBase = AioPaginator[ListAssessmentsResponseTypeDef]
else:
    _ListAssessmentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAssessmentsPaginator(_ListAssessmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-catalog/paginator/ListAssessments.html#MarketplaceCatalog.Paginator.ListAssessments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_catalog/paginators/#listassessmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssessmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssessmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-catalog/paginator/ListAssessments.html#MarketplaceCatalog.Paginator.ListAssessments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_catalog/paginators/#listassessmentspaginator)
        """

if TYPE_CHECKING:
    _ListChangeSetsPaginatorBase = AioPaginator[ListChangeSetsResponseTypeDef]
else:
    _ListChangeSetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListChangeSetsPaginator(_ListChangeSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-catalog/paginator/ListChangeSets.html#MarketplaceCatalog.Paginator.ListChangeSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_catalog/paginators/#listchangesetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListChangeSetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListChangeSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-catalog/paginator/ListChangeSets.html#MarketplaceCatalog.Paginator.ListChangeSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_catalog/paginators/#listchangesetspaginator)
        """

if TYPE_CHECKING:
    _ListEntitiesPaginatorBase = AioPaginator[ListEntitiesResponseTypeDef]
else:
    _ListEntitiesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEntitiesPaginator(_ListEntitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-catalog/paginator/ListEntities.html#MarketplaceCatalog.Paginator.ListEntities)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_catalog/paginators/#listentitiespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEntitiesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEntitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/marketplace-catalog/paginator/ListEntities.html#MarketplaceCatalog.Paginator.ListEntities.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_catalog/paginators/#listentitiespaginator)
        """
