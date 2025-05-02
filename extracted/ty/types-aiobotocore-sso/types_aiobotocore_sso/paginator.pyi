"""
Type annotations for sso service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sso.client import SSOClient
    from types_aiobotocore_sso.paginator import (
        ListAccountRolesPaginator,
        ListAccountsPaginator,
    )

    session = get_session()
    with session.create_client("sso") as client:
        client: SSOClient

        list_account_roles_paginator: ListAccountRolesPaginator = client.get_paginator("list_account_roles")
        list_accounts_paginator: ListAccountsPaginator = client.get_paginator("list_accounts")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAccountRolesRequestPaginateTypeDef,
    ListAccountRolesResponseTypeDef,
    ListAccountsRequestPaginateTypeDef,
    ListAccountsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListAccountRolesPaginator", "ListAccountsPaginator")

if TYPE_CHECKING:
    _ListAccountRolesPaginatorBase = AioPaginator[ListAccountRolesResponseTypeDef]
else:
    _ListAccountRolesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAccountRolesPaginator(_ListAccountRolesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso/paginator/ListAccountRoles.html#SSO.Paginator.ListAccountRoles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso/paginators/#listaccountrolespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccountRolesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAccountRolesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso/paginator/ListAccountRoles.html#SSO.Paginator.ListAccountRoles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso/paginators/#listaccountrolespaginator)
        """

if TYPE_CHECKING:
    _ListAccountsPaginatorBase = AioPaginator[ListAccountsResponseTypeDef]
else:
    _ListAccountsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAccountsPaginator(_ListAccountsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso/paginator/ListAccounts.html#SSO.Paginator.ListAccounts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso/paginators/#listaccountspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccountsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso/paginator/ListAccounts.html#SSO.Paginator.ListAccounts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso/paginators/#listaccountspaginator)
        """
