"""
Type annotations for lambda-microvms service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_lambda_microvms.client import LambdaMicroVMsClient
    from types_aiobotocore_lambda_microvms.paginator import (
        ListManagedMicrovmImageVersionsPaginator,
        ListManagedMicrovmImagesPaginator,
        ListMicrovmImageBuildsPaginator,
        ListMicrovmImageVersionsPaginator,
        ListMicrovmImagesPaginator,
        ListMicrovmsPaginator,
    )

    session = get_session()
    with session.create_client("lambda-microvms") as client:
        client: LambdaMicroVMsClient

        list_managed_microvm_image_versions_paginator: ListManagedMicrovmImageVersionsPaginator = client.get_paginator("list_managed_microvm_image_versions")
        list_managed_microvm_images_paginator: ListManagedMicrovmImagesPaginator = client.get_paginator("list_managed_microvm_images")
        list_microvm_image_builds_paginator: ListMicrovmImageBuildsPaginator = client.get_paginator("list_microvm_image_builds")
        list_microvm_image_versions_paginator: ListMicrovmImageVersionsPaginator = client.get_paginator("list_microvm_image_versions")
        list_microvm_images_paginator: ListMicrovmImagesPaginator = client.get_paginator("list_microvm_images")
        list_microvms_paginator: ListMicrovmsPaginator = client.get_paginator("list_microvms")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListManagedMicrovmImagesInputPaginateTypeDef,
    ListManagedMicrovmImagesOutputTypeDef,
    ListManagedMicrovmImageVersionsInputPaginateTypeDef,
    ListManagedMicrovmImageVersionsOutputTypeDef,
    ListMicrovmImageBuildsInputPaginateTypeDef,
    ListMicrovmImageBuildsOutputTypeDef,
    ListMicrovmImagesRequestPaginateTypeDef,
    ListMicrovmImagesResponseTypeDef,
    ListMicrovmImageVersionsInputPaginateTypeDef,
    ListMicrovmImageVersionsOutputTypeDef,
    ListMicrovmsRequestPaginateTypeDef,
    ListMicrovmsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListManagedMicrovmImageVersionsPaginator",
    "ListManagedMicrovmImagesPaginator",
    "ListMicrovmImageBuildsPaginator",
    "ListMicrovmImageVersionsPaginator",
    "ListMicrovmImagesPaginator",
    "ListMicrovmsPaginator",
)

if TYPE_CHECKING:
    _ListManagedMicrovmImageVersionsPaginatorBase = AioPaginator[
        ListManagedMicrovmImageVersionsOutputTypeDef
    ]
else:
    _ListManagedMicrovmImageVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListManagedMicrovmImageVersionsPaginator(_ListManagedMicrovmImageVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListManagedMicrovmImageVersions.html#LambdaMicroVMs.Paginator.ListManagedMicrovmImageVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/paginators/#listmanagedmicrovmimageversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedMicrovmImageVersionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListManagedMicrovmImageVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListManagedMicrovmImageVersions.html#LambdaMicroVMs.Paginator.ListManagedMicrovmImageVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/paginators/#listmanagedmicrovmimageversionspaginator)
        """

if TYPE_CHECKING:
    _ListManagedMicrovmImagesPaginatorBase = AioPaginator[ListManagedMicrovmImagesOutputTypeDef]
else:
    _ListManagedMicrovmImagesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListManagedMicrovmImagesPaginator(_ListManagedMicrovmImagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListManagedMicrovmImages.html#LambdaMicroVMs.Paginator.ListManagedMicrovmImages)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/paginators/#listmanagedmicrovmimagespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedMicrovmImagesInputPaginateTypeDef]
    ) -> AioPageIterator[ListManagedMicrovmImagesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListManagedMicrovmImages.html#LambdaMicroVMs.Paginator.ListManagedMicrovmImages.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/paginators/#listmanagedmicrovmimagespaginator)
        """

if TYPE_CHECKING:
    _ListMicrovmImageBuildsPaginatorBase = AioPaginator[ListMicrovmImageBuildsOutputTypeDef]
else:
    _ListMicrovmImageBuildsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMicrovmImageBuildsPaginator(_ListMicrovmImageBuildsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListMicrovmImageBuilds.html#LambdaMicroVMs.Paginator.ListMicrovmImageBuilds)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/paginators/#listmicrovmimagebuildspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMicrovmImageBuildsInputPaginateTypeDef]
    ) -> AioPageIterator[ListMicrovmImageBuildsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListMicrovmImageBuilds.html#LambdaMicroVMs.Paginator.ListMicrovmImageBuilds.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/paginators/#listmicrovmimagebuildspaginator)
        """

if TYPE_CHECKING:
    _ListMicrovmImageVersionsPaginatorBase = AioPaginator[ListMicrovmImageVersionsOutputTypeDef]
else:
    _ListMicrovmImageVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMicrovmImageVersionsPaginator(_ListMicrovmImageVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListMicrovmImageVersions.html#LambdaMicroVMs.Paginator.ListMicrovmImageVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/paginators/#listmicrovmimageversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMicrovmImageVersionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListMicrovmImageVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListMicrovmImageVersions.html#LambdaMicroVMs.Paginator.ListMicrovmImageVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/paginators/#listmicrovmimageversionspaginator)
        """

if TYPE_CHECKING:
    _ListMicrovmImagesPaginatorBase = AioPaginator[ListMicrovmImagesResponseTypeDef]
else:
    _ListMicrovmImagesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMicrovmImagesPaginator(_ListMicrovmImagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListMicrovmImages.html#LambdaMicroVMs.Paginator.ListMicrovmImages)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/paginators/#listmicrovmimagespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMicrovmImagesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMicrovmImagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListMicrovmImages.html#LambdaMicroVMs.Paginator.ListMicrovmImages.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/paginators/#listmicrovmimagespaginator)
        """

if TYPE_CHECKING:
    _ListMicrovmsPaginatorBase = AioPaginator[ListMicrovmsResponseTypeDef]
else:
    _ListMicrovmsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMicrovmsPaginator(_ListMicrovmsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListMicrovms.html#LambdaMicroVMs.Paginator.ListMicrovms)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/paginators/#listmicrovmspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMicrovmsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMicrovmsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListMicrovms.html#LambdaMicroVMs.Paginator.ListMicrovms.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/paginators/#listmicrovmspaginator)
        """
