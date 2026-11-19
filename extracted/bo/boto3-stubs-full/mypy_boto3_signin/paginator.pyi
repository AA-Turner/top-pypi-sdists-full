"""
Type annotations for signin service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signin/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_signin.client import SignInServiceClient
    from mypy_boto3_signin.paginator import (
        ListResourcePermissionStatementsPaginator,
        ListSessionsPaginator,
    )

    session = Session()
    client: SignInServiceClient = session.client("signin")

    list_resource_permission_statements_paginator: ListResourcePermissionStatementsPaginator = client.get_paginator("list_resource_permission_statements")
    list_sessions_paginator: ListSessionsPaginator = client.get_paginator("list_sessions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListResourcePermissionStatementsInputPaginateTypeDef,
    ListResourcePermissionStatementsOutputTypeDef,
    ListSessionsInputPaginateTypeDef,
    ListSessionsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListResourcePermissionStatementsPaginator", "ListSessionsPaginator")

if TYPE_CHECKING:
    _ListResourcePermissionStatementsPaginatorBase = Paginator[
        ListResourcePermissionStatementsOutputTypeDef
    ]
else:
    _ListResourcePermissionStatementsPaginatorBase = Paginator  # type: ignore[assignment]

class ListResourcePermissionStatementsPaginator(_ListResourcePermissionStatementsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signin/paginator/ListResourcePermissionStatements.html#SignInService.Paginator.ListResourcePermissionStatements)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signin/paginators/#listresourcepermissionstatementspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourcePermissionStatementsInputPaginateTypeDef]
    ) -> PageIterator[ListResourcePermissionStatementsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signin/paginator/ListResourcePermissionStatements.html#SignInService.Paginator.ListResourcePermissionStatements.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signin/paginators/#listresourcepermissionstatementspaginator)
        """

if TYPE_CHECKING:
    _ListSessionsPaginatorBase = Paginator[ListSessionsOutputTypeDef]
else:
    _ListSessionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListSessionsPaginator(_ListSessionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signin/paginator/ListSessions.html#SignInService.Paginator.ListSessions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signin/paginators/#listsessionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSessionsInputPaginateTypeDef]
    ) -> PageIterator[ListSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/signin/paginator/ListSessions.html#SignInService.Paginator.ListSessions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_signin/paginators/#listsessionspaginator)
        """
