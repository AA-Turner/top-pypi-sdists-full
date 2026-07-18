"""
Type annotations for supportauthz service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_supportauthz.client import SupportAuthZClient
    from types_aiobotocore_supportauthz.paginator import (
        ListActionsPaginator,
        ListSupportPermitRequestsPaginator,
        ListSupportPermitsPaginator,
    )

    session = get_session()
    with session.create_client("supportauthz") as client:
        client: SupportAuthZClient

        list_actions_paginator: ListActionsPaginator = client.get_paginator("list_actions")
        list_support_permit_requests_paginator: ListSupportPermitRequestsPaginator = client.get_paginator("list_support_permit_requests")
        list_support_permits_paginator: ListSupportPermitsPaginator = client.get_paginator("list_support_permits")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

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
    _ListActionsPaginatorBase = AioPaginator[ListActionsOutputTypeDef]
else:
    _ListActionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListActionsPaginator(_ListActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/paginator/ListActions.html#SupportAuthZ.Paginator.ListActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/paginators/#listactionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListActionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListActionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/paginator/ListActions.html#SupportAuthZ.Paginator.ListActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/paginators/#listactionspaginator)
        """

if TYPE_CHECKING:
    _ListSupportPermitRequestsPaginatorBase = AioPaginator[ListSupportPermitRequestsOutputTypeDef]
else:
    _ListSupportPermitRequestsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSupportPermitRequestsPaginator(_ListSupportPermitRequestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/paginator/ListSupportPermitRequests.html#SupportAuthZ.Paginator.ListSupportPermitRequests)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/paginators/#listsupportpermitrequestspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSupportPermitRequestsInputPaginateTypeDef]
    ) -> AioPageIterator[ListSupportPermitRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/paginator/ListSupportPermitRequests.html#SupportAuthZ.Paginator.ListSupportPermitRequests.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/paginators/#listsupportpermitrequestspaginator)
        """

if TYPE_CHECKING:
    _ListSupportPermitsPaginatorBase = AioPaginator[ListSupportPermitsOutputTypeDef]
else:
    _ListSupportPermitsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSupportPermitsPaginator(_ListSupportPermitsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/paginator/ListSupportPermits.html#SupportAuthZ.Paginator.ListSupportPermits)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/paginators/#listsupportpermitspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSupportPermitsInputPaginateTypeDef]
    ) -> AioPageIterator[ListSupportPermitsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/paginator/ListSupportPermits.html#SupportAuthZ.Paginator.ListSupportPermits.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supportauthz/paginators/#listsupportpermitspaginator)
        """
