"""
Type annotations for pipes service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pipes/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_pipes.client import EventBridgePipesClient
    from types_aiobotocore_pipes.paginator import (
        ListPipesPaginator,
    )

    session = get_session()
    with session.create_client("pipes") as client:
        client: EventBridgePipesClient

        list_pipes_paginator: ListPipesPaginator = client.get_paginator("list_pipes")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListPipesRequestPaginateTypeDef, ListPipesResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListPipesPaginator",)


if TYPE_CHECKING:
    _ListPipesPaginatorBase = AioPaginator[ListPipesResponseTypeDef]
else:
    _ListPipesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPipesPaginator(_ListPipesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/paginator/ListPipes.html#EventBridgePipes.Paginator.ListPipes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pipes/paginators/#listpipespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPipesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPipesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/paginator/ListPipes.html#EventBridgePipes.Paginator.ListPipes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pipes/paginators/#listpipespaginator)
        """
