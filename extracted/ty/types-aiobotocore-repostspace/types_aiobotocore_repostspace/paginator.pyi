"""
Type annotations for repostspace service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_repostspace.client import RePostPrivateClient
    from types_aiobotocore_repostspace.paginator import (
        ListSpacesPaginator,
    )

    session = get_session()
    with session.create_client("repostspace") as client:
        client: RePostPrivateClient

        list_spaces_paginator: ListSpacesPaginator = client.get_paginator("list_spaces")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListSpacesInputPaginateTypeDef, ListSpacesOutputTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListSpacesPaginator",)

if TYPE_CHECKING:
    _ListSpacesPaginatorBase = AioPaginator[ListSpacesOutputTypeDef]
else:
    _ListSpacesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSpacesPaginator(_ListSpacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/paginator/ListSpaces.html#RePostPrivate.Paginator.ListSpaces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/paginators/#listspacespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSpacesInputPaginateTypeDef]
    ) -> AioPageIterator[ListSpacesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/paginator/ListSpaces.html#RePostPrivate.Paginator.ListSpaces.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_repostspace/paginators/#listspacespaginator)
        """
