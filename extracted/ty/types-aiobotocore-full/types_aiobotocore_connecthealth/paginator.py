"""
Type annotations for connecthealth service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_connecthealth.client import ConnectHealthClient
    from types_aiobotocore_connecthealth.paginator import (
        ListDomainsPaginator,
        ListSubscriptionsPaginator,
    )

    session = get_session()
    with session.create_client("connecthealth") as client:
        client: ConnectHealthClient

        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        list_subscriptions_paginator: ListSubscriptionsPaginator = client.get_paginator("list_subscriptions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListDomainsInputPaginateTypeDef,
    ListDomainsOutputTypeDef,
    ListSubscriptionsInputPaginateTypeDef,
    ListSubscriptionsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListDomainsPaginator", "ListSubscriptionsPaginator")


if TYPE_CHECKING:
    _ListDomainsPaginatorBase = AioPaginator[ListDomainsOutputTypeDef]
else:
    _ListDomainsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDomainsPaginator(_ListDomainsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/paginator/ListDomains.html#ConnectHealth.Paginator.ListDomains)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/paginators/#listdomainspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDomainsInputPaginateTypeDef]
    ) -> AioPageIterator[ListDomainsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/paginator/ListDomains.html#ConnectHealth.Paginator.ListDomains.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/paginators/#listdomainspaginator)
        """


if TYPE_CHECKING:
    _ListSubscriptionsPaginatorBase = AioPaginator[ListSubscriptionsOutputTypeDef]
else:
    _ListSubscriptionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSubscriptionsPaginator(_ListSubscriptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/paginator/ListSubscriptions.html#ConnectHealth.Paginator.ListSubscriptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/paginators/#listsubscriptionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSubscriptionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListSubscriptionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/paginator/ListSubscriptions.html#ConnectHealth.Paginator.ListSubscriptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/paginators/#listsubscriptionspaginator)
        """
