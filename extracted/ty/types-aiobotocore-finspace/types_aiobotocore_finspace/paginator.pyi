"""
Type annotations for finspace service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_finspace.client import FinspaceClient
    from types_aiobotocore_finspace.paginator import (
        ListKxEnvironmentsPaginator,
    )

    session = get_session()
    with session.create_client("finspace") as client:
        client: FinspaceClient

        list_kx_environments_paginator: ListKxEnvironmentsPaginator = client.get_paginator("list_kx_environments")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListKxEnvironmentsRequestPaginateTypeDef, ListKxEnvironmentsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListKxEnvironmentsPaginator",)

if TYPE_CHECKING:
    _ListKxEnvironmentsPaginatorBase = AioPaginator[ListKxEnvironmentsResponseTypeDef]
else:
    _ListKxEnvironmentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListKxEnvironmentsPaginator(_ListKxEnvironmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/paginator/ListKxEnvironments.html#Finspace.Paginator.ListKxEnvironments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/paginators/#listkxenvironmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListKxEnvironmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListKxEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace/paginator/ListKxEnvironments.html#Finspace.Paginator.ListKxEnvironments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace/paginators/#listkxenvironmentspaginator)
        """
