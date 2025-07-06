"""
Type annotations for managedblockchain service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_managedblockchain.client import ManagedBlockchainClient
    from types_aiobotocore_managedblockchain.paginator import (
        ListAccessorsPaginator,
    )

    session = get_session()
    with session.create_client("managedblockchain") as client:
        client: ManagedBlockchainClient

        list_accessors_paginator: ListAccessorsPaginator = client.get_paginator("list_accessors")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListAccessorsInputPaginateTypeDef, ListAccessorsOutputTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListAccessorsPaginator",)

if TYPE_CHECKING:
    _ListAccessorsPaginatorBase = AioPaginator[ListAccessorsOutputTypeDef]
else:
    _ListAccessorsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAccessorsPaginator(_ListAccessorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/paginator/ListAccessors.html#ManagedBlockchain.Paginator.ListAccessors)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/paginators/#listaccessorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccessorsInputPaginateTypeDef]
    ) -> AioPageIterator[ListAccessorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/managedblockchain/paginator/ListAccessors.html#ManagedBlockchain.Paginator.ListAccessors.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_managedblockchain/paginators/#listaccessorspaginator)
        """
