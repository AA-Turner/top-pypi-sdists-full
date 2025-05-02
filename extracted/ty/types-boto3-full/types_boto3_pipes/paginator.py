"""
Type annotations for pipes service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pipes/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_pipes.client import EventBridgePipesClient
    from types_boto3_pipes.paginator import (
        ListPipesPaginator,
    )

    session = Session()
    client: EventBridgePipesClient = session.client("pipes")

    list_pipes_paginator: ListPipesPaginator = client.get_paginator("list_pipes")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import ListPipesRequestPaginateTypeDef, ListPipesResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListPipesPaginator",)


if TYPE_CHECKING:
    _ListPipesPaginatorBase = Paginator[ListPipesResponseTypeDef]
else:
    _ListPipesPaginatorBase = Paginator  # type: ignore[assignment]


class ListPipesPaginator(_ListPipesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/paginator/ListPipes.html#EventBridgePipes.Paginator.ListPipes)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pipes/paginators/#listpipespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPipesRequestPaginateTypeDef]
    ) -> PageIterator[ListPipesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes/paginator/ListPipes.html#EventBridgePipes.Paginator.ListPipes.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pipes/paginators/#listpipespaginator)
        """
