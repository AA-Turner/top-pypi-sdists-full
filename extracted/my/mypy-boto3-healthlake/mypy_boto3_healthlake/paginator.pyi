"""
Type annotations for healthlake service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_healthlake/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_healthlake.client import HealthLakeClient
    from mypy_boto3_healthlake.paginator import (
        ListDataTransformationJobsPaginator,
        ListDataTransformationProfileVersionsPaginator,
        ListDataTransformationProfilesPaginator,
    )

    session = Session()
    client: HealthLakeClient = session.client("healthlake")

    list_data_transformation_jobs_paginator: ListDataTransformationJobsPaginator = client.get_paginator("list_data_transformation_jobs")
    list_data_transformation_profile_versions_paginator: ListDataTransformationProfileVersionsPaginator = client.get_paginator("list_data_transformation_profile_versions")
    list_data_transformation_profiles_paginator: ListDataTransformationProfilesPaginator = client.get_paginator("list_data_transformation_profiles")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

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
    _ListDataTransformationJobsPaginatorBase = Paginator[ListDataTransformationJobsResponseTypeDef]
else:
    _ListDataTransformationJobsPaginatorBase = Paginator  # type: ignore[assignment]

class ListDataTransformationJobsPaginator(_ListDataTransformationJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/paginator/ListDataTransformationJobs.html#HealthLake.Paginator.ListDataTransformationJobs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_healthlake/paginators/#listdatatransformationjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataTransformationJobsRequestPaginateTypeDef]
    ) -> PageIterator[ListDataTransformationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/paginator/ListDataTransformationJobs.html#HealthLake.Paginator.ListDataTransformationJobs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_healthlake/paginators/#listdatatransformationjobspaginator)
        """

if TYPE_CHECKING:
    _ListDataTransformationProfileVersionsPaginatorBase = Paginator[
        ListDataTransformationProfileVersionsResponseTypeDef
    ]
else:
    _ListDataTransformationProfileVersionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListDataTransformationProfileVersionsPaginator(
    _ListDataTransformationProfileVersionsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/paginator/ListDataTransformationProfileVersions.html#HealthLake.Paginator.ListDataTransformationProfileVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_healthlake/paginators/#listdatatransformationprofileversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataTransformationProfileVersionsRequestPaginateTypeDef]
    ) -> PageIterator[ListDataTransformationProfileVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/paginator/ListDataTransformationProfileVersions.html#HealthLake.Paginator.ListDataTransformationProfileVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_healthlake/paginators/#listdatatransformationprofileversionspaginator)
        """

if TYPE_CHECKING:
    _ListDataTransformationProfilesPaginatorBase = Paginator[
        ListDataTransformationProfilesResponseTypeDef
    ]
else:
    _ListDataTransformationProfilesPaginatorBase = Paginator  # type: ignore[assignment]

class ListDataTransformationProfilesPaginator(_ListDataTransformationProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/paginator/ListDataTransformationProfiles.html#HealthLake.Paginator.ListDataTransformationProfiles)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_healthlake/paginators/#listdatatransformationprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataTransformationProfilesRequestPaginateTypeDef]
    ) -> PageIterator[ListDataTransformationProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/healthlake/paginator/ListDataTransformationProfiles.html#HealthLake.Paginator.ListDataTransformationProfiles.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_healthlake/paginators/#listdatatransformationprofilespaginator)
        """
