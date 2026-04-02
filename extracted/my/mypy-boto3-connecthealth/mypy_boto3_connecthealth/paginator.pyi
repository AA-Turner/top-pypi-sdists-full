"""
Type annotations for connecthealth service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connecthealth/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_connecthealth.client import ConnectHealthClient
    from mypy_boto3_connecthealth.paginator import (
        ListDomainsPaginator,
        ListSubscriptionsPaginator,
    )

    session = Session()
    client: ConnectHealthClient = session.client("connecthealth")

    list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
    list_subscriptions_paginator: ListSubscriptionsPaginator = client.get_paginator("list_subscriptions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

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
    _ListDomainsPaginatorBase = Paginator[ListDomainsOutputTypeDef]
else:
    _ListDomainsPaginatorBase = Paginator  # type: ignore[assignment]

class ListDomainsPaginator(_ListDomainsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/paginator/ListDomains.html#ConnectHealth.Paginator.ListDomains)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connecthealth/paginators/#listdomainspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDomainsInputPaginateTypeDef]
    ) -> PageIterator[ListDomainsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/paginator/ListDomains.html#ConnectHealth.Paginator.ListDomains.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connecthealth/paginators/#listdomainspaginator)
        """

if TYPE_CHECKING:
    _ListSubscriptionsPaginatorBase = Paginator[ListSubscriptionsOutputTypeDef]
else:
    _ListSubscriptionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListSubscriptionsPaginator(_ListSubscriptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/paginator/ListSubscriptions.html#ConnectHealth.Paginator.ListSubscriptions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connecthealth/paginators/#listsubscriptionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSubscriptionsInputPaginateTypeDef]
    ) -> PageIterator[ListSubscriptionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/paginator/ListSubscriptions.html#ConnectHealth.Paginator.ListSubscriptions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connecthealth/paginators/#listsubscriptionspaginator)
        """
