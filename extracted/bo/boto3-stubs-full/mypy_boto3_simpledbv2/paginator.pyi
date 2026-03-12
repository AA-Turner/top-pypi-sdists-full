"""
Type annotations for simpledbv2 service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simpledbv2/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_simpledbv2.client import SimpleDBv2Client
    from mypy_boto3_simpledbv2.paginator import (
        ListExportsPaginator,
    )

    session = Session()
    client: SimpleDBv2Client = session.client("simpledbv2")

    list_exports_paginator: ListExportsPaginator = client.get_paginator("list_exports")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import ListExportsRequestPaginateTypeDef, ListExportsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListExportsPaginator",)

if TYPE_CHECKING:
    _ListExportsPaginatorBase = Paginator[ListExportsResponseTypeDef]
else:
    _ListExportsPaginatorBase = Paginator  # type: ignore[assignment]

class ListExportsPaginator(_ListExportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simpledbv2/paginator/ListExports.html#SimpleDBv2.Paginator.ListExports)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simpledbv2/paginators/#listexportspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExportsRequestPaginateTypeDef]
    ) -> PageIterator[ListExportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simpledbv2/paginator/ListExports.html#SimpleDBv2.Paginator.ListExports.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simpledbv2/paginators/#listexportspaginator)
        """
