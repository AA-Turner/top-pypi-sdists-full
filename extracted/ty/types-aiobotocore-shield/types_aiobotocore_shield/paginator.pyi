"""
Type annotations for shield service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_shield/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_shield.client import ShieldClient
    from types_aiobotocore_shield.paginator import (
        ListAttacksPaginator,
        ListProtectionsPaginator,
    )

    session = get_session()
    with session.create_client("shield") as client:
        client: ShieldClient

        list_attacks_paginator: ListAttacksPaginator = client.get_paginator("list_attacks")
        list_protections_paginator: ListProtectionsPaginator = client.get_paginator("list_protections")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAttacksRequestPaginateTypeDef,
    ListAttacksResponseTypeDef,
    ListProtectionsRequestPaginateTypeDef,
    ListProtectionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListAttacksPaginator", "ListProtectionsPaginator")

if TYPE_CHECKING:
    _ListAttacksPaginatorBase = AioPaginator[ListAttacksResponseTypeDef]
else:
    _ListAttacksPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAttacksPaginator(_ListAttacksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/shield/paginator/ListAttacks.html#Shield.Paginator.ListAttacks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_shield/paginators/#listattackspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAttacksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAttacksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/shield/paginator/ListAttacks.html#Shield.Paginator.ListAttacks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_shield/paginators/#listattackspaginator)
        """

if TYPE_CHECKING:
    _ListProtectionsPaginatorBase = AioPaginator[ListProtectionsResponseTypeDef]
else:
    _ListProtectionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProtectionsPaginator(_ListProtectionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/shield/paginator/ListProtections.html#Shield.Paginator.ListProtections)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_shield/paginators/#listprotectionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProtectionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProtectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/shield/paginator/ListProtections.html#Shield.Paginator.ListProtections.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_shield/paginators/#listprotectionspaginator)
        """
