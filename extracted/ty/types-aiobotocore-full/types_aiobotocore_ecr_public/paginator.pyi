"""
Type annotations for ecr-public service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ecr_public.client import ECRPublicClient
    from types_aiobotocore_ecr_public.paginator import (
        DescribeImageTagsPaginator,
        DescribeImagesPaginator,
        DescribeRegistriesPaginator,
        DescribeRepositoriesPaginator,
    )

    session = get_session()
    with session.create_client("ecr-public") as client:
        client: ECRPublicClient

        describe_image_tags_paginator: DescribeImageTagsPaginator = client.get_paginator("describe_image_tags")
        describe_images_paginator: DescribeImagesPaginator = client.get_paginator("describe_images")
        describe_registries_paginator: DescribeRegistriesPaginator = client.get_paginator("describe_registries")
        describe_repositories_paginator: DescribeRepositoriesPaginator = client.get_paginator("describe_repositories")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeImagesRequestPaginateTypeDef,
    DescribeImagesResponseTypeDef,
    DescribeImageTagsRequestPaginateTypeDef,
    DescribeImageTagsResponseTypeDef,
    DescribeRegistriesRequestPaginateTypeDef,
    DescribeRegistriesResponseTypeDef,
    DescribeRepositoriesRequestPaginateTypeDef,
    DescribeRepositoriesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeImageTagsPaginator",
    "DescribeImagesPaginator",
    "DescribeRegistriesPaginator",
    "DescribeRepositoriesPaginator",
)

if TYPE_CHECKING:
    _DescribeImageTagsPaginatorBase = AioPaginator[DescribeImageTagsResponseTypeDef]
else:
    _DescribeImageTagsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeImageTagsPaginator(_DescribeImageTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/paginator/DescribeImageTags.html#ECRPublic.Paginator.DescribeImageTags)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/paginators/#describeimagetagspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeImageTagsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeImageTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/paginator/DescribeImageTags.html#ECRPublic.Paginator.DescribeImageTags.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/paginators/#describeimagetagspaginator)
        """

if TYPE_CHECKING:
    _DescribeImagesPaginatorBase = AioPaginator[DescribeImagesResponseTypeDef]
else:
    _DescribeImagesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeImagesPaginator(_DescribeImagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/paginator/DescribeImages.html#ECRPublic.Paginator.DescribeImages)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/paginators/#describeimagespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeImagesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeImagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/paginator/DescribeImages.html#ECRPublic.Paginator.DescribeImages.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/paginators/#describeimagespaginator)
        """

if TYPE_CHECKING:
    _DescribeRegistriesPaginatorBase = AioPaginator[DescribeRegistriesResponseTypeDef]
else:
    _DescribeRegistriesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeRegistriesPaginator(_DescribeRegistriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/paginator/DescribeRegistries.html#ECRPublic.Paginator.DescribeRegistries)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/paginators/#describeregistriespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeRegistriesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeRegistriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/paginator/DescribeRegistries.html#ECRPublic.Paginator.DescribeRegistries.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/paginators/#describeregistriespaginator)
        """

if TYPE_CHECKING:
    _DescribeRepositoriesPaginatorBase = AioPaginator[DescribeRepositoriesResponseTypeDef]
else:
    _DescribeRepositoriesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeRepositoriesPaginator(_DescribeRepositoriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/paginator/DescribeRepositories.html#ECRPublic.Paginator.DescribeRepositories)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/paginators/#describerepositoriespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeRepositoriesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeRepositoriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecr-public/paginator/DescribeRepositories.html#ECRPublic.Paginator.DescribeRepositories.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/paginators/#describerepositoriespaginator)
        """
