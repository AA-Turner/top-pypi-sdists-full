"""
Type annotations for glacier service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_glacier.client import GlacierClient
    from types_aiobotocore_glacier.paginator import (
        ListJobsPaginator,
        ListMultipartUploadsPaginator,
        ListPartsPaginator,
        ListVaultsPaginator,
    )

    session = get_session()
    with session.create_client("glacier") as client:
        client: GlacierClient

        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_multipart_uploads_paginator: ListMultipartUploadsPaginator = client.get_paginator("list_multipart_uploads")
        list_parts_paginator: ListPartsPaginator = client.get_paginator("list_parts")
        list_vaults_paginator: ListVaultsPaginator = client.get_paginator("list_vaults")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListJobsInputPaginateTypeDef,
    ListJobsOutputTypeDef,
    ListMultipartUploadsInputPaginateTypeDef,
    ListMultipartUploadsOutputTypeDef,
    ListPartsInputPaginateTypeDef,
    ListPartsOutputTypeDef,
    ListVaultsInputPaginateTypeDef,
    ListVaultsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListJobsPaginator",
    "ListMultipartUploadsPaginator",
    "ListPartsPaginator",
    "ListVaultsPaginator",
)

if TYPE_CHECKING:
    _ListJobsPaginatorBase = AioPaginator[ListJobsOutputTypeDef]
else:
    _ListJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListJobsPaginator(_ListJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListJobs.html#Glacier.Paginator.ListJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators/#listjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobsInputPaginateTypeDef]
    ) -> AioPageIterator[ListJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListJobs.html#Glacier.Paginator.ListJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators/#listjobspaginator)
        """

if TYPE_CHECKING:
    _ListMultipartUploadsPaginatorBase = AioPaginator[ListMultipartUploadsOutputTypeDef]
else:
    _ListMultipartUploadsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMultipartUploadsPaginator(_ListMultipartUploadsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListMultipartUploads.html#Glacier.Paginator.ListMultipartUploads)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators/#listmultipartuploadspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMultipartUploadsInputPaginateTypeDef]
    ) -> AioPageIterator[ListMultipartUploadsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListMultipartUploads.html#Glacier.Paginator.ListMultipartUploads.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators/#listmultipartuploadspaginator)
        """

if TYPE_CHECKING:
    _ListPartsPaginatorBase = AioPaginator[ListPartsOutputTypeDef]
else:
    _ListPartsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPartsPaginator(_ListPartsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListParts.html#Glacier.Paginator.ListParts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators/#listpartspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPartsInputPaginateTypeDef]
    ) -> AioPageIterator[ListPartsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListParts.html#Glacier.Paginator.ListParts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators/#listpartspaginator)
        """

if TYPE_CHECKING:
    _ListVaultsPaginatorBase = AioPaginator[ListVaultsOutputTypeDef]
else:
    _ListVaultsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListVaultsPaginator(_ListVaultsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListVaults.html#Glacier.Paginator.ListVaults)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators/#listvaultspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVaultsInputPaginateTypeDef]
    ) -> AioPageIterator[ListVaultsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListVaults.html#Glacier.Paginator.ListVaults.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/paginators/#listvaultspaginator)
        """
