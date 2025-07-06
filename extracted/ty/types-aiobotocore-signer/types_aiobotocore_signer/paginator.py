"""
Type annotations for signer service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signer/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_signer.client import SignerClient
    from types_aiobotocore_signer.paginator import (
        ListSigningJobsPaginator,
        ListSigningPlatformsPaginator,
        ListSigningProfilesPaginator,
    )

    session = get_session()
    with session.create_client("signer") as client:
        client: SignerClient

        list_signing_jobs_paginator: ListSigningJobsPaginator = client.get_paginator("list_signing_jobs")
        list_signing_platforms_paginator: ListSigningPlatformsPaginator = client.get_paginator("list_signing_platforms")
        list_signing_profiles_paginator: ListSigningProfilesPaginator = client.get_paginator("list_signing_profiles")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListSigningJobsRequestPaginateTypeDef,
    ListSigningJobsResponseTypeDef,
    ListSigningPlatformsRequestPaginateTypeDef,
    ListSigningPlatformsResponseTypeDef,
    ListSigningProfilesRequestPaginateTypeDef,
    ListSigningProfilesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListSigningJobsPaginator",
    "ListSigningPlatformsPaginator",
    "ListSigningProfilesPaginator",
)


if TYPE_CHECKING:
    _ListSigningJobsPaginatorBase = AioPaginator[ListSigningJobsResponseTypeDef]
else:
    _ListSigningJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSigningJobsPaginator(_ListSigningJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/paginator/ListSigningJobs.html#Signer.Paginator.ListSigningJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signer/paginators/#listsigningjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSigningJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSigningJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/paginator/ListSigningJobs.html#Signer.Paginator.ListSigningJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signer/paginators/#listsigningjobspaginator)
        """


if TYPE_CHECKING:
    _ListSigningPlatformsPaginatorBase = AioPaginator[ListSigningPlatformsResponseTypeDef]
else:
    _ListSigningPlatformsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSigningPlatformsPaginator(_ListSigningPlatformsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/paginator/ListSigningPlatforms.html#Signer.Paginator.ListSigningPlatforms)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signer/paginators/#listsigningplatformspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSigningPlatformsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSigningPlatformsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/paginator/ListSigningPlatforms.html#Signer.Paginator.ListSigningPlatforms.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signer/paginators/#listsigningplatformspaginator)
        """


if TYPE_CHECKING:
    _ListSigningProfilesPaginatorBase = AioPaginator[ListSigningProfilesResponseTypeDef]
else:
    _ListSigningProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSigningProfilesPaginator(_ListSigningProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/paginator/ListSigningProfiles.html#Signer.Paginator.ListSigningProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signer/paginators/#listsigningprofilespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSigningProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSigningProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signer/paginator/ListSigningProfiles.html#Signer.Paginator.ListSigningProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_signer/paginators/#listsigningprofilespaginator)
        """
