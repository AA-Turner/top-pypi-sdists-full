"""
Type annotations for textract service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_textract.client import TextractClient
    from types_aiobotocore_textract.paginator import (
        ListAdapterVersionsPaginator,
        ListAdaptersPaginator,
    )

    session = get_session()
    with session.create_client("textract") as client:
        client: TextractClient

        list_adapter_versions_paginator: ListAdapterVersionsPaginator = client.get_paginator("list_adapter_versions")
        list_adapters_paginator: ListAdaptersPaginator = client.get_paginator("list_adapters")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAdaptersRequestPaginateTypeDef,
    ListAdaptersResponseTypeDef,
    ListAdapterVersionsRequestPaginateTypeDef,
    ListAdapterVersionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListAdapterVersionsPaginator", "ListAdaptersPaginator")

if TYPE_CHECKING:
    _ListAdapterVersionsPaginatorBase = AioPaginator[ListAdapterVersionsResponseTypeDef]
else:
    _ListAdapterVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAdapterVersionsPaginator(_ListAdapterVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/paginator/ListAdapterVersions.html#Textract.Paginator.ListAdapterVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/paginators/#listadapterversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAdapterVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAdapterVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/paginator/ListAdapterVersions.html#Textract.Paginator.ListAdapterVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/paginators/#listadapterversionspaginator)
        """

if TYPE_CHECKING:
    _ListAdaptersPaginatorBase = AioPaginator[ListAdaptersResponseTypeDef]
else:
    _ListAdaptersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAdaptersPaginator(_ListAdaptersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/paginator/ListAdapters.html#Textract.Paginator.ListAdapters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/paginators/#listadapterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAdaptersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAdaptersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/paginator/ListAdapters.html#Textract.Paginator.ListAdapters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/paginators/#listadapterspaginator)
        """
