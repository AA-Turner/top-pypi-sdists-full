"""
Type annotations for lambda-microvms service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_microvms/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_lambda_microvms.client import LambdaMicroVMsClient
    from mypy_boto3_lambda_microvms.paginator import (
        ListManagedMicrovmImageVersionsPaginator,
        ListManagedMicrovmImagesPaginator,
        ListMicrovmImageBuildsPaginator,
        ListMicrovmImageVersionsPaginator,
        ListMicrovmImagesPaginator,
        ListMicrovmsPaginator,
    )

    session = Session()
    client: LambdaMicroVMsClient = session.client("lambda-microvms")

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

from botocore.paginate import PageIterator, Paginator

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
    _ListManagedMicrovmImageVersionsPaginatorBase = Paginator[
        ListManagedMicrovmImageVersionsOutputTypeDef
    ]
else:
    _ListManagedMicrovmImageVersionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListManagedMicrovmImageVersionsPaginator(_ListManagedMicrovmImageVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListManagedMicrovmImageVersions.html#LambdaMicroVMs.Paginator.ListManagedMicrovmImageVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_microvms/paginators/#listmanagedmicrovmimageversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedMicrovmImageVersionsInputPaginateTypeDef]
    ) -> PageIterator[ListManagedMicrovmImageVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListManagedMicrovmImageVersions.html#LambdaMicroVMs.Paginator.ListManagedMicrovmImageVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_microvms/paginators/#listmanagedmicrovmimageversionspaginator)
        """


if TYPE_CHECKING:
    _ListManagedMicrovmImagesPaginatorBase = Paginator[ListManagedMicrovmImagesOutputTypeDef]
else:
    _ListManagedMicrovmImagesPaginatorBase = Paginator  # type: ignore[assignment]


class ListManagedMicrovmImagesPaginator(_ListManagedMicrovmImagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListManagedMicrovmImages.html#LambdaMicroVMs.Paginator.ListManagedMicrovmImages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_microvms/paginators/#listmanagedmicrovmimagespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedMicrovmImagesInputPaginateTypeDef]
    ) -> PageIterator[ListManagedMicrovmImagesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListManagedMicrovmImages.html#LambdaMicroVMs.Paginator.ListManagedMicrovmImages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_microvms/paginators/#listmanagedmicrovmimagespaginator)
        """


if TYPE_CHECKING:
    _ListMicrovmImageBuildsPaginatorBase = Paginator[ListMicrovmImageBuildsOutputTypeDef]
else:
    _ListMicrovmImageBuildsPaginatorBase = Paginator  # type: ignore[assignment]


class ListMicrovmImageBuildsPaginator(_ListMicrovmImageBuildsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListMicrovmImageBuilds.html#LambdaMicroVMs.Paginator.ListMicrovmImageBuilds)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_microvms/paginators/#listmicrovmimagebuildspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMicrovmImageBuildsInputPaginateTypeDef]
    ) -> PageIterator[ListMicrovmImageBuildsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListMicrovmImageBuilds.html#LambdaMicroVMs.Paginator.ListMicrovmImageBuilds.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_microvms/paginators/#listmicrovmimagebuildspaginator)
        """


if TYPE_CHECKING:
    _ListMicrovmImageVersionsPaginatorBase = Paginator[ListMicrovmImageVersionsOutputTypeDef]
else:
    _ListMicrovmImageVersionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListMicrovmImageVersionsPaginator(_ListMicrovmImageVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListMicrovmImageVersions.html#LambdaMicroVMs.Paginator.ListMicrovmImageVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_microvms/paginators/#listmicrovmimageversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMicrovmImageVersionsInputPaginateTypeDef]
    ) -> PageIterator[ListMicrovmImageVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListMicrovmImageVersions.html#LambdaMicroVMs.Paginator.ListMicrovmImageVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_microvms/paginators/#listmicrovmimageversionspaginator)
        """


if TYPE_CHECKING:
    _ListMicrovmImagesPaginatorBase = Paginator[ListMicrovmImagesResponseTypeDef]
else:
    _ListMicrovmImagesPaginatorBase = Paginator  # type: ignore[assignment]


class ListMicrovmImagesPaginator(_ListMicrovmImagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListMicrovmImages.html#LambdaMicroVMs.Paginator.ListMicrovmImages)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_microvms/paginators/#listmicrovmimagespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMicrovmImagesRequestPaginateTypeDef]
    ) -> PageIterator[ListMicrovmImagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListMicrovmImages.html#LambdaMicroVMs.Paginator.ListMicrovmImages.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_microvms/paginators/#listmicrovmimagespaginator)
        """


if TYPE_CHECKING:
    _ListMicrovmsPaginatorBase = Paginator[ListMicrovmsResponseTypeDef]
else:
    _ListMicrovmsPaginatorBase = Paginator  # type: ignore[assignment]


class ListMicrovmsPaginator(_ListMicrovmsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListMicrovms.html#LambdaMicroVMs.Paginator.ListMicrovms)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_microvms/paginators/#listmicrovmspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMicrovmsRequestPaginateTypeDef]
    ) -> PageIterator[ListMicrovmsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/paginator/ListMicrovms.html#LambdaMicroVMs.Paginator.ListMicrovms.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_microvms/paginators/#listmicrovmspaginator)
        """
