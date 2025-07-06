"""
Type annotations for sdb service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sdb.client import SimpleDBClient
    from types_aiobotocore_sdb.paginator import (
        ListDomainsPaginator,
        SelectPaginator,
    )

    session = get_session()
    with session.create_client("sdb") as client:
        client: SimpleDBClient

        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        select_paginator: SelectPaginator = client.get_paginator("select")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListDomainsRequestPaginateTypeDef,
    ListDomainsResultTypeDef,
    SelectRequestPaginateTypeDef,
    SelectResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListDomainsPaginator", "SelectPaginator")

if TYPE_CHECKING:
    _ListDomainsPaginatorBase = AioPaginator[ListDomainsResultTypeDef]
else:
    _ListDomainsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDomainsPaginator(_ListDomainsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/paginator/ListDomains.html#SimpleDB.Paginator.ListDomains)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/paginators/#listdomainspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDomainsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDomainsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/paginator/ListDomains.html#SimpleDB.Paginator.ListDomains.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/paginators/#listdomainspaginator)
        """

if TYPE_CHECKING:
    _SelectPaginatorBase = AioPaginator[SelectResultTypeDef]
else:
    _SelectPaginatorBase = AioPaginator  # type: ignore[assignment]

class SelectPaginator(_SelectPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/paginator/Select.html#SimpleDB.Paginator.Select)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/paginators/#selectpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SelectRequestPaginateTypeDef]
    ) -> AioPageIterator[SelectResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb/paginator/Select.html#SimpleDB.Paginator.Select.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sdb/paginators/#selectpaginator)
        """
