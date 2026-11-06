"""
Type annotations for account-access-runtime service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account_access_runtime/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_account_access_runtime.client import AccountAccessRuntimeClient
    from mypy_boto3_account_access_runtime.paginator import (
        ListRolesPaginator,
    )

    session = Session()
    client: AccountAccessRuntimeClient = session.client("account-access-runtime")

    list_roles_paginator: ListRolesPaginator = client.get_paginator("list_roles")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import ListRolesRequestPaginateTypeDef, ListRolesResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListRolesPaginator",)


if TYPE_CHECKING:
    _ListRolesPaginatorBase = Paginator[ListRolesResponseTypeDef]
else:
    _ListRolesPaginatorBase = Paginator  # type: ignore[assignment]


class ListRolesPaginator(_ListRolesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access-runtime/paginator/ListRoles.html#AccountAccessRuntime.Paginator.ListRoles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account_access_runtime/paginators/#listrolespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRolesRequestPaginateTypeDef]
    ) -> PageIterator[ListRolesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/account-access-runtime/paginator/ListRoles.html#AccountAccessRuntime.Paginator.ListRoles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_account_access_runtime/paginators/#listrolespaginator)
        """
