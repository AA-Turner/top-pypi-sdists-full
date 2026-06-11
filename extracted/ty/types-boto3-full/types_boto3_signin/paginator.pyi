"""
Type annotations for signin service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signin/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_signin.client import SignInServiceClient
    from types_boto3_signin.paginator import (
        ListResourcePermissionStatementsPaginator,
    )

    session = Session()
    client: SignInServiceClient = session.client("signin")

    list_resource_permission_statements_paginator: ListResourcePermissionStatementsPaginator = client.get_paginator("list_resource_permission_statements")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListResourcePermissionStatementsInputPaginateTypeDef,
    ListResourcePermissionStatementsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListResourcePermissionStatementsPaginator",)

if TYPE_CHECKING:
    _ListResourcePermissionStatementsPaginatorBase = Paginator[
        ListResourcePermissionStatementsOutputTypeDef
    ]
else:
    _ListResourcePermissionStatementsPaginatorBase = Paginator  # type: ignore[assignment]

class ListResourcePermissionStatementsPaginator(_ListResourcePermissionStatementsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signin/paginator/ListResourcePermissionStatements.html#SignInService.Paginator.ListResourcePermissionStatements)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signin/paginators/#listresourcepermissionstatementspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourcePermissionStatementsInputPaginateTypeDef]
    ) -> PageIterator[ListResourcePermissionStatementsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signin/paginator/ListResourcePermissionStatements.html#SignInService.Paginator.ListResourcePermissionStatements.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_signin/paginators/#listresourcepermissionstatementspaginator)
        """
