"""
Type annotations for mediastore service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mediastore.client import MediaStoreClient
    from types_aiobotocore_mediastore.paginator import (
        ListContainersPaginator,
    )

    session = get_session()
    with session.create_client("mediastore") as client:
        client: MediaStoreClient

        list_containers_paginator: ListContainersPaginator = client.get_paginator("list_containers")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListContainersInputPaginateTypeDef, ListContainersOutputTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListContainersPaginator",)

if TYPE_CHECKING:
    _ListContainersPaginatorBase = AioPaginator[ListContainersOutputTypeDef]
else:
    _ListContainersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListContainersPaginator(_ListContainersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/paginator/ListContainers.html#MediaStore.Paginator.ListContainers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore/paginators/#listcontainerspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContainersInputPaginateTypeDef]
    ) -> AioPageIterator[ListContainersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore/paginator/ListContainers.html#MediaStore.Paginator.ListContainers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore/paginators/#listcontainerspaginator)
        """
