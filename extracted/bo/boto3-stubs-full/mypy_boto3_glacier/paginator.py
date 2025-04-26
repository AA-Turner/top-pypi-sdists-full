"""
Type annotations for glacier service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_glacier.client import GlacierClient
    from mypy_boto3_glacier.paginator import (
        ListJobsPaginator,
        ListMultipartUploadsPaginator,
        ListPartsPaginator,
        ListVaultsPaginator,
    )

    session = Session()
    client: GlacierClient = session.client("glacier")

    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_multipart_uploads_paginator: ListMultipartUploadsPaginator = client.get_paginator("list_multipart_uploads")
    list_parts_paginator: ListPartsPaginator = client.get_paginator("list_parts")
    list_vaults_paginator: ListVaultsPaginator = client.get_paginator("list_vaults")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

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
    _ListJobsPaginatorBase = Paginator[ListJobsOutputTypeDef]
else:
    _ListJobsPaginatorBase = Paginator  # type: ignore[assignment]


class ListJobsPaginator(_ListJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListJobs.html#Glacier.Paginator.ListJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/paginators/#listjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobsInputPaginateTypeDef]
    ) -> PageIterator[ListJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListJobs.html#Glacier.Paginator.ListJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/paginators/#listjobspaginator)
        """


if TYPE_CHECKING:
    _ListMultipartUploadsPaginatorBase = Paginator[ListMultipartUploadsOutputTypeDef]
else:
    _ListMultipartUploadsPaginatorBase = Paginator  # type: ignore[assignment]


class ListMultipartUploadsPaginator(_ListMultipartUploadsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListMultipartUploads.html#Glacier.Paginator.ListMultipartUploads)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/paginators/#listmultipartuploadspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMultipartUploadsInputPaginateTypeDef]
    ) -> PageIterator[ListMultipartUploadsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListMultipartUploads.html#Glacier.Paginator.ListMultipartUploads.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/paginators/#listmultipartuploadspaginator)
        """


if TYPE_CHECKING:
    _ListPartsPaginatorBase = Paginator[ListPartsOutputTypeDef]
else:
    _ListPartsPaginatorBase = Paginator  # type: ignore[assignment]


class ListPartsPaginator(_ListPartsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListParts.html#Glacier.Paginator.ListParts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/paginators/#listpartspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPartsInputPaginateTypeDef]
    ) -> PageIterator[ListPartsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListParts.html#Glacier.Paginator.ListParts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/paginators/#listpartspaginator)
        """


if TYPE_CHECKING:
    _ListVaultsPaginatorBase = Paginator[ListVaultsOutputTypeDef]
else:
    _ListVaultsPaginatorBase = Paginator  # type: ignore[assignment]


class ListVaultsPaginator(_ListVaultsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListVaults.html#Glacier.Paginator.ListVaults)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/paginators/#listvaultspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVaultsInputPaginateTypeDef]
    ) -> PageIterator[ListVaultsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier/paginator/ListVaults.html#Glacier.Paginator.ListVaults.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_glacier/paginators/#listvaultspaginator)
        """
