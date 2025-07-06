"""
Main interface for sagemaker-geospatial service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sagemaker_geospatial import (
        Client,
        ListEarthObservationJobsPaginator,
        ListRasterDataCollectionsPaginator,
        ListVectorEnrichmentJobsPaginator,
        SageMakergeospatialcapabilitiesClient,
    )

    session = get_session()
    async with session.create_client("sagemaker-geospatial") as client:
        client: SageMakergeospatialcapabilitiesClient
        ...


    list_earth_observation_jobs_paginator: ListEarthObservationJobsPaginator = client.get_paginator("list_earth_observation_jobs")
    list_raster_data_collections_paginator: ListRasterDataCollectionsPaginator = client.get_paginator("list_raster_data_collections")
    list_vector_enrichment_jobs_paginator: ListVectorEnrichmentJobsPaginator = client.get_paginator("list_vector_enrichment_jobs")
    ```
"""

from .client import SageMakergeospatialcapabilitiesClient
from .paginator import (
    ListEarthObservationJobsPaginator,
    ListRasterDataCollectionsPaginator,
    ListVectorEnrichmentJobsPaginator,
)

Client = SageMakergeospatialcapabilitiesClient


__all__ = (
    "Client",
    "ListEarthObservationJobsPaginator",
    "ListRasterDataCollectionsPaginator",
    "ListVectorEnrichmentJobsPaginator",
    "SageMakergeospatialcapabilitiesClient",
)
