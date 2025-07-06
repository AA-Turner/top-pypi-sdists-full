"""
Type annotations for sagemaker-geospatial service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sagemaker_geospatial.client import SageMakergeospatialcapabilitiesClient

    session = get_session()
    async with session.create_client("sagemaker-geospatial") as client:
        client: SageMakergeospatialcapabilitiesClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListEarthObservationJobsPaginator,
    ListRasterDataCollectionsPaginator,
    ListVectorEnrichmentJobsPaginator,
)
from .type_defs import (
    DeleteEarthObservationJobInputTypeDef,
    DeleteVectorEnrichmentJobInputTypeDef,
    ExportEarthObservationJobInputTypeDef,
    ExportEarthObservationJobOutputTypeDef,
    ExportVectorEnrichmentJobInputTypeDef,
    ExportVectorEnrichmentJobOutputTypeDef,
    GetEarthObservationJobInputTypeDef,
    GetEarthObservationJobOutputTypeDef,
    GetRasterDataCollectionInputTypeDef,
    GetRasterDataCollectionOutputTypeDef,
    GetTileInputTypeDef,
    GetTileOutputTypeDef,
    GetVectorEnrichmentJobInputTypeDef,
    GetVectorEnrichmentJobOutputTypeDef,
    ListEarthObservationJobInputTypeDef,
    ListEarthObservationJobOutputTypeDef,
    ListRasterDataCollectionsInputTypeDef,
    ListRasterDataCollectionsOutputTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListVectorEnrichmentJobInputTypeDef,
    ListVectorEnrichmentJobOutputTypeDef,
    SearchRasterDataCollectionInputTypeDef,
    SearchRasterDataCollectionOutputTypeDef,
    StartEarthObservationJobInputTypeDef,
    StartEarthObservationJobOutputTypeDef,
    StartVectorEnrichmentJobInputTypeDef,
    StartVectorEnrichmentJobOutputTypeDef,
    StopEarthObservationJobInputTypeDef,
    StopVectorEnrichmentJobInputTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("SageMakergeospatialcapabilitiesClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class SageMakergeospatialcapabilitiesClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SageMakergeospatialcapabilitiesClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#generate_presigned_url)
        """

    async def delete_earth_observation_job(
        self, **kwargs: Unpack[DeleteEarthObservationJobInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Use this operation to delete an Earth Observation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/delete_earth_observation_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#delete_earth_observation_job)
        """

    async def delete_vector_enrichment_job(
        self, **kwargs: Unpack[DeleteVectorEnrichmentJobInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Use this operation to delete a Vector Enrichment job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/delete_vector_enrichment_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#delete_vector_enrichment_job)
        """

    async def export_earth_observation_job(
        self, **kwargs: Unpack[ExportEarthObservationJobInputTypeDef]
    ) -> ExportEarthObservationJobOutputTypeDef:
        """
        Use this operation to export results of an Earth Observation job and optionally
        source images used as input to the EOJ to an Amazon S3 location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/export_earth_observation_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#export_earth_observation_job)
        """

    async def export_vector_enrichment_job(
        self, **kwargs: Unpack[ExportVectorEnrichmentJobInputTypeDef]
    ) -> ExportVectorEnrichmentJobOutputTypeDef:
        """
        Use this operation to copy results of a Vector Enrichment job to an Amazon S3
        location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/export_vector_enrichment_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#export_vector_enrichment_job)
        """

    async def get_earth_observation_job(
        self, **kwargs: Unpack[GetEarthObservationJobInputTypeDef]
    ) -> GetEarthObservationJobOutputTypeDef:
        """
        Get the details for a previously initiated Earth Observation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/get_earth_observation_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#get_earth_observation_job)
        """

    async def get_raster_data_collection(
        self, **kwargs: Unpack[GetRasterDataCollectionInputTypeDef]
    ) -> GetRasterDataCollectionOutputTypeDef:
        """
        Use this operation to get details of a specific raster data collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/get_raster_data_collection.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#get_raster_data_collection)
        """

    async def get_tile(self, **kwargs: Unpack[GetTileInputTypeDef]) -> GetTileOutputTypeDef:
        """
        Gets a web mercator tile for the given Earth Observation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/get_tile.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#get_tile)
        """

    async def get_vector_enrichment_job(
        self, **kwargs: Unpack[GetVectorEnrichmentJobInputTypeDef]
    ) -> GetVectorEnrichmentJobOutputTypeDef:
        """
        Retrieves details of a Vector Enrichment Job for a given job Amazon Resource
        Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/get_vector_enrichment_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#get_vector_enrichment_job)
        """

    async def list_earth_observation_jobs(
        self, **kwargs: Unpack[ListEarthObservationJobInputTypeDef]
    ) -> ListEarthObservationJobOutputTypeDef:
        """
        Use this operation to get a list of the Earth Observation jobs associated with
        the calling Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/list_earth_observation_jobs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#list_earth_observation_jobs)
        """

    async def list_raster_data_collections(
        self, **kwargs: Unpack[ListRasterDataCollectionsInputTypeDef]
    ) -> ListRasterDataCollectionsOutputTypeDef:
        """
        Use this operation to get raster data collections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/list_raster_data_collections.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#list_raster_data_collections)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags attached to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#list_tags_for_resource)
        """

    async def list_vector_enrichment_jobs(
        self, **kwargs: Unpack[ListVectorEnrichmentJobInputTypeDef]
    ) -> ListVectorEnrichmentJobOutputTypeDef:
        """
        Retrieves a list of vector enrichment jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/list_vector_enrichment_jobs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#list_vector_enrichment_jobs)
        """

    async def search_raster_data_collection(
        self, **kwargs: Unpack[SearchRasterDataCollectionInputTypeDef]
    ) -> SearchRasterDataCollectionOutputTypeDef:
        """
        Allows you run image query on a specific raster data collection to get a list
        of the satellite imagery matching the selected filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/search_raster_data_collection.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#search_raster_data_collection)
        """

    async def start_earth_observation_job(
        self, **kwargs: Unpack[StartEarthObservationJobInputTypeDef]
    ) -> StartEarthObservationJobOutputTypeDef:
        """
        Use this operation to create an Earth observation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/start_earth_observation_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#start_earth_observation_job)
        """

    async def start_vector_enrichment_job(
        self, **kwargs: Unpack[StartVectorEnrichmentJobInputTypeDef]
    ) -> StartVectorEnrichmentJobOutputTypeDef:
        """
        Creates a Vector Enrichment job for the supplied job type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/start_vector_enrichment_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#start_vector_enrichment_job)
        """

    async def stop_earth_observation_job(
        self, **kwargs: Unpack[StopEarthObservationJobInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Use this operation to stop an existing earth observation job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/stop_earth_observation_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#stop_earth_observation_job)
        """

    async def stop_vector_enrichment_job(
        self, **kwargs: Unpack[StopVectorEnrichmentJobInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops the Vector Enrichment job for a given job ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/stop_vector_enrichment_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#stop_vector_enrichment_job)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        The resource you want to tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        The resource you want to untag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#untag_resource)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_earth_observation_jobs"]
    ) -> ListEarthObservationJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_raster_data_collections"]
    ) -> ListRasterDataCollectionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_vector_enrichment_jobs"]
    ) -> ListVectorEnrichmentJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-geospatial.html#SageMakergeospatialcapabilities.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_geospatial/client/)
        """
