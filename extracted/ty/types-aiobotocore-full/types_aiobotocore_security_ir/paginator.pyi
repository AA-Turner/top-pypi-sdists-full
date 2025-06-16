"""
Type annotations for security-ir service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_security_ir.client import SecurityIncidentResponseClient
    from types_aiobotocore_security_ir.paginator import (
        ListCaseEditsPaginator,
        ListCasesPaginator,
        ListCommentsPaginator,
        ListMembershipsPaginator,
    )

    session = get_session()
    with session.create_client("security-ir") as client:
        client: SecurityIncidentResponseClient

        list_case_edits_paginator: ListCaseEditsPaginator = client.get_paginator("list_case_edits")
        list_cases_paginator: ListCasesPaginator = client.get_paginator("list_cases")
        list_comments_paginator: ListCommentsPaginator = client.get_paginator("list_comments")
        list_memberships_paginator: ListMembershipsPaginator = client.get_paginator("list_memberships")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListCaseEditsRequestPaginateTypeDef,
    ListCaseEditsResponseTypeDef,
    ListCasesRequestPaginateTypeDef,
    ListCasesResponseTypeDef,
    ListCommentsRequestPaginateTypeDef,
    ListCommentsResponseTypeDef,
    ListMembershipsRequestPaginateTypeDef,
    ListMembershipsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListCaseEditsPaginator",
    "ListCasesPaginator",
    "ListCommentsPaginator",
    "ListMembershipsPaginator",
)

if TYPE_CHECKING:
    _ListCaseEditsPaginatorBase = AioPaginator[ListCaseEditsResponseTypeDef]
else:
    _ListCaseEditsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCaseEditsPaginator(_ListCaseEditsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/paginator/ListCaseEdits.html#SecurityIncidentResponse.Paginator.ListCaseEdits)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/paginators/#listcaseeditspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCaseEditsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCaseEditsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/paginator/ListCaseEdits.html#SecurityIncidentResponse.Paginator.ListCaseEdits.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/paginators/#listcaseeditspaginator)
        """

if TYPE_CHECKING:
    _ListCasesPaginatorBase = AioPaginator[ListCasesResponseTypeDef]
else:
    _ListCasesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCasesPaginator(_ListCasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/paginator/ListCases.html#SecurityIncidentResponse.Paginator.ListCases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/paginators/#listcasespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCasesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/paginator/ListCases.html#SecurityIncidentResponse.Paginator.ListCases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/paginators/#listcasespaginator)
        """

if TYPE_CHECKING:
    _ListCommentsPaginatorBase = AioPaginator[ListCommentsResponseTypeDef]
else:
    _ListCommentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCommentsPaginator(_ListCommentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/paginator/ListComments.html#SecurityIncidentResponse.Paginator.ListComments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/paginators/#listcommentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCommentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCommentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/paginator/ListComments.html#SecurityIncidentResponse.Paginator.ListComments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/paginators/#listcommentspaginator)
        """

if TYPE_CHECKING:
    _ListMembershipsPaginatorBase = AioPaginator[ListMembershipsResponseTypeDef]
else:
    _ListMembershipsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMembershipsPaginator(_ListMembershipsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/paginator/ListMemberships.html#SecurityIncidentResponse.Paginator.ListMemberships)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/paginators/#listmembershipspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMembershipsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMembershipsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/paginator/ListMemberships.html#SecurityIncidentResponse.Paginator.ListMemberships.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/paginators/#listmembershipspaginator)
        """
