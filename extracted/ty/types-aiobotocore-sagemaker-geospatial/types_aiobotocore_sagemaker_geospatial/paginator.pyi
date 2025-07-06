"""
Type annotations for sagemaker-geospatial service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sagemaker_geospatial.client import SageMakergeospatialcapabilitiesClient
    from types_aiobotocore_sagemaker_geospatial.paginator import (
        ListEarthObservationJobsPaginator,
        ListRasterDataCollectionsPaginator,
        ListVectorEnrichmentJobsPaginator,
    )

    session = get_session()
    with session.create_client("sagemaker-geospatial") as client:
        client: SageMakergeospatialcapabilitiesClient

        list_earth_observation_jobs_paginator: ListEarthObservationJobsPaginator = client.get_paginator("list_earth_observation_jobs")
        list_raster_data_collections_paginator: ListRasterDataCollectionsPaginator = client.get_paginator("list_raster_data_collections")
        list_vector_enrichment_jobs_paginator: ListVectorEnrichmentJobsPaginator = client.get_paginator("list_vector_enrichment_jobs")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListEarthObservationJobInputPaginateTypeDef,
    ListEarthObservationJobOutputTypeDef,
    ListRasterDataCollectionsInputPaginateTypeDef,
    ListRasterDataCollectionsOutputTypeDef,
    ListVectorEnrichmentJobInputPaginateTypeDef,
    ListVectorEnrichmentJobOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListEarthObservationJobsPaginator",
    "ListRasterDataCollectionsPaginator",
    "ListVectorEnrichmentJobsPaginator",
)

if TYPE_CHECKING:
    _ListEarthObservationJobsPaginatorBase = AioPaginator[ListEarthObservationJobOutputTypeDef]
else:
    _ListEarthObservationJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEarthObservationJobsPaginator(_ListEarthObservationJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/paginator/ListEarthObservationJobs.html#SageMakergeospatialcapabilities.Paginator.ListEarthObservationJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/paginators/#listearthobservationjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEarthObservationJobInputPaginateTypeDef]
    ) -> AioPageIterator[ListEarthObservationJobOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/paginator/ListEarthObservationJobs.html#SageMakergeospatialcapabilities.Paginator.ListEarthObservationJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/paginators/#listearthobservationjobspaginator)
        """

if TYPE_CHECKING:
    _ListRasterDataCollectionsPaginatorBase = AioPaginator[ListRasterDataCollectionsOutputTypeDef]
else:
    _ListRasterDataCollectionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRasterDataCollectionsPaginator(_ListRasterDataCollectionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/paginator/ListRasterDataCollections.html#SageMakergeospatialcapabilities.Paginator.ListRasterDataCollections)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/paginators/#listrasterdatacollectionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRasterDataCollectionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListRasterDataCollectionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/paginator/ListRasterDataCollections.html#SageMakergeospatialcapabilities.Paginator.ListRasterDataCollections.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/paginators/#listrasterdatacollectionspaginator)
        """

if TYPE_CHECKING:
    _ListVectorEnrichmentJobsPaginatorBase = AioPaginator[ListVectorEnrichmentJobOutputTypeDef]
else:
    _ListVectorEnrichmentJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListVectorEnrichmentJobsPaginator(_ListVectorEnrichmentJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/paginator/ListVectorEnrichmentJobs.html#SageMakergeospatialcapabilities.Paginator.ListVectorEnrichmentJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/paginators/#listvectorenrichmentjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVectorEnrichmentJobInputPaginateTypeDef]
    ) -> AioPageIterator[ListVectorEnrichmentJobOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/paginator/ListVectorEnrichmentJobs.html#SageMakergeospatialcapabilities.Paginator.ListVectorEnrichmentJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/paginators/#listvectorenrichmentjobspaginator)
        """
