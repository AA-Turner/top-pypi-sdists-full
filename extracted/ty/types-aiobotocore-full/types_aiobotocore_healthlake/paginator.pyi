"""
Type annotations for healthlake service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_healthlake.client import HealthLakeClient
    from types_aiobotocore_healthlake.paginator import (
        ListDataTransformationJobsPaginator,
        ListDataTransformationProfileVersionsPaginator,
        ListDataTransformationProfilesPaginator,
    )

    session = get_session()
    with session.create_client("healthlake") as client:
        client: HealthLakeClient

        list_data_transformation_jobs_paginator: ListDataTransformationJobsPaginator = client.get_paginator("list_data_transformation_jobs")
        list_data_transformation_profile_versions_paginator: ListDataTransformationProfileVersionsPaginator = client.get_paginator("list_data_transformation_profile_versions")
        list_data_transformation_profiles_paginator: ListDataTransformationProfilesPaginator = client.get_paginator("list_data_transformation_profiles")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListDataTransformationJobsRequestPaginateTypeDef,
    ListDataTransformationJobsResponseTypeDef,
    ListDataTransformationProfilesRequestPaginateTypeDef,
    ListDataTransformationProfilesResponseTypeDef,
    ListDataTransformationProfileVersionsRequestPaginateTypeDef,
    ListDataTransformationProfileVersionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListDataTransformationJobsPaginator",
    "ListDataTransformationProfileVersionsPaginator",
    "ListDataTransformationProfilesPaginator",
)

if TYPE_CHECKING:
    _ListDataTransformationJobsPaginatorBase = AioPaginator[
        ListDataTransformationJobsResponseTypeDef
    ]
else:
    _ListDataTransformationJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataTransformationJobsPaginator(_ListDataTransformationJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/paginator/ListDataTransformationJobs.html#HealthLake.Paginator.ListDataTransformationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/paginators/#listdatatransformationjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataTransformationJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataTransformationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/paginator/ListDataTransformationJobs.html#HealthLake.Paginator.ListDataTransformationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/paginators/#listdatatransformationjobspaginator)
        """

if TYPE_CHECKING:
    _ListDataTransformationProfileVersionsPaginatorBase = AioPaginator[
        ListDataTransformationProfileVersionsResponseTypeDef
    ]
else:
    _ListDataTransformationProfileVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataTransformationProfileVersionsPaginator(
    _ListDataTransformationProfileVersionsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/paginator/ListDataTransformationProfileVersions.html#HealthLake.Paginator.ListDataTransformationProfileVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/paginators/#listdatatransformationprofileversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataTransformationProfileVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataTransformationProfileVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/paginator/ListDataTransformationProfileVersions.html#HealthLake.Paginator.ListDataTransformationProfileVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/paginators/#listdatatransformationprofileversionspaginator)
        """

if TYPE_CHECKING:
    _ListDataTransformationProfilesPaginatorBase = AioPaginator[
        ListDataTransformationProfilesResponseTypeDef
    ]
else:
    _ListDataTransformationProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDataTransformationProfilesPaginator(_ListDataTransformationProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/paginator/ListDataTransformationProfiles.html#HealthLake.Paginator.ListDataTransformationProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/paginators/#listdatatransformationprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataTransformationProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataTransformationProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/paginator/ListDataTransformationProfiles.html#HealthLake.Paginator.ListDataTransformationProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_healthlake/paginators/#listdatatransformationprofilespaginator)
        """
