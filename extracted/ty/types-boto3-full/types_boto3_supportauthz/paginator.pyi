"""
Type annotations for supportauthz service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supportauthz/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_supportauthz.client import SupportAuthZClient
    from types_boto3_supportauthz.paginator import (
        ListActionsPaginator,
        ListSupportPermitRequestsPaginator,
        ListSupportPermitsPaginator,
    )

    session = Session()
    client: SupportAuthZClient = session.client("supportauthz")

    list_actions_paginator: ListActionsPaginator = client.get_paginator("list_actions")
    list_support_permit_requests_paginator: ListSupportPermitRequestsPaginator = client.get_paginator("list_support_permit_requests")
    list_support_permits_paginator: ListSupportPermitsPaginator = client.get_paginator("list_support_permits")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListActionsInputPaginateTypeDef,
    ListActionsOutputTypeDef,
    ListSupportPermitRequestsInputPaginateTypeDef,
    ListSupportPermitRequestsOutputTypeDef,
    ListSupportPermitsInputPaginateTypeDef,
    ListSupportPermitsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListActionsPaginator",
    "ListSupportPermitRequestsPaginator",
    "ListSupportPermitsPaginator",
)

if TYPE_CHECKING:
    _ListActionsPaginatorBase = Paginator[ListActionsOutputTypeDef]
else:
    _ListActionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListActionsPaginator(_ListActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/paginator/ListActions.html#SupportAuthZ.Paginator.ListActions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supportauthz/paginators/#listactionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListActionsInputPaginateTypeDef]
    ) -> PageIterator[ListActionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/paginator/ListActions.html#SupportAuthZ.Paginator.ListActions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supportauthz/paginators/#listactionspaginator)
        """

if TYPE_CHECKING:
    _ListSupportPermitRequestsPaginatorBase = Paginator[ListSupportPermitRequestsOutputTypeDef]
else:
    _ListSupportPermitRequestsPaginatorBase = Paginator  # type: ignore[assignment]

class ListSupportPermitRequestsPaginator(_ListSupportPermitRequestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/paginator/ListSupportPermitRequests.html#SupportAuthZ.Paginator.ListSupportPermitRequests)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supportauthz/paginators/#listsupportpermitrequestspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSupportPermitRequestsInputPaginateTypeDef]
    ) -> PageIterator[ListSupportPermitRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/paginator/ListSupportPermitRequests.html#SupportAuthZ.Paginator.ListSupportPermitRequests.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supportauthz/paginators/#listsupportpermitrequestspaginator)
        """

if TYPE_CHECKING:
    _ListSupportPermitsPaginatorBase = Paginator[ListSupportPermitsOutputTypeDef]
else:
    _ListSupportPermitsPaginatorBase = Paginator  # type: ignore[assignment]

class ListSupportPermitsPaginator(_ListSupportPermitsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/paginator/ListSupportPermits.html#SupportAuthZ.Paginator.ListSupportPermits)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supportauthz/paginators/#listsupportpermitspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSupportPermitsInputPaginateTypeDef]
    ) -> PageIterator[ListSupportPermitsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/paginator/ListSupportPermits.html#SupportAuthZ.Paginator.ListSupportPermits.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_supportauthz/paginators/#listsupportpermitspaginator)
        """
