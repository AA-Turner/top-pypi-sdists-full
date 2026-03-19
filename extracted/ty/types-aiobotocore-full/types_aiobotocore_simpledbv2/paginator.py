"""
Type annotations for simpledbv2 service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_simpledbv2/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_simpledbv2.client import SimpleDBv2Client
    from types_aiobotocore_simpledbv2.paginator import (
        ListExportsPaginator,
    )

    session = get_session()
    with session.create_client("simpledbv2") as client:
        client: SimpleDBv2Client

        list_exports_paginator: ListExportsPaginator = client.get_paginator("list_exports")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListExportsRequestPaginateTypeDef, ListExportsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListExportsPaginator",)


if TYPE_CHECKING:
    _ListExportsPaginatorBase = AioPaginator[ListExportsResponseTypeDef]
else:
    _ListExportsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListExportsPaginator(_ListExportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simpledbv2/paginator/ListExports.html#SimpleDBv2.Paginator.ListExports)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_simpledbv2/paginators/#listexportspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExportsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListExportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/simpledbv2/paginator/ListExports.html#SimpleDBv2.Paginator.ListExports.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_simpledbv2/paginators/#listexportspaginator)
        """
