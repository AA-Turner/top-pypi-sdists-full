"""
Type annotations for elb-proxy service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb_proxy/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_elb_proxy.client import ELBProxyClient
    from mypy_boto3_elb_proxy.paginator import (
        ListCertificateAssociationsPaginator,
        ListProxiesPaginator,
        ListProxyUpdatesPaginator,
        ListProxyVersionsPaginator,
    )

    session = Session()
    client: ELBProxyClient = session.client("elb-proxy")

    list_certificate_associations_paginator: ListCertificateAssociationsPaginator = client.get_paginator("list_certificate_associations")
    list_proxies_paginator: ListProxiesPaginator = client.get_paginator("list_proxies")
    list_proxy_updates_paginator: ListProxyUpdatesPaginator = client.get_paginator("list_proxy_updates")
    list_proxy_versions_paginator: ListProxyVersionsPaginator = client.get_paginator("list_proxy_versions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListCertificateAssociationsRequestPaginateTypeDef,
    ListCertificateAssociationsResponseTypeDef,
    ListProxiesRequestPaginateTypeDef,
    ListProxiesResponseTypeDef,
    ListProxyUpdatesRequestPaginateTypeDef,
    ListProxyUpdatesResponseTypeDef,
    ListProxyVersionsRequestPaginateTypeDef,
    ListProxyVersionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListCertificateAssociationsPaginator",
    "ListProxiesPaginator",
    "ListProxyUpdatesPaginator",
    "ListProxyVersionsPaginator",
)


if TYPE_CHECKING:
    _ListCertificateAssociationsPaginatorBase = Paginator[
        ListCertificateAssociationsResponseTypeDef
    ]
else:
    _ListCertificateAssociationsPaginatorBase = Paginator  # type: ignore[assignment]


class ListCertificateAssociationsPaginator(_ListCertificateAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/paginator/ListCertificateAssociations.html#ELBProxy.Paginator.ListCertificateAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb_proxy/paginators/#listcertificateassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCertificateAssociationsRequestPaginateTypeDef]
    ) -> PageIterator[ListCertificateAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/paginator/ListCertificateAssociations.html#ELBProxy.Paginator.ListCertificateAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb_proxy/paginators/#listcertificateassociationspaginator)
        """


if TYPE_CHECKING:
    _ListProxiesPaginatorBase = Paginator[ListProxiesResponseTypeDef]
else:
    _ListProxiesPaginatorBase = Paginator  # type: ignore[assignment]


class ListProxiesPaginator(_ListProxiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/paginator/ListProxies.html#ELBProxy.Paginator.ListProxies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb_proxy/paginators/#listproxiespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProxiesRequestPaginateTypeDef]
    ) -> PageIterator[ListProxiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/paginator/ListProxies.html#ELBProxy.Paginator.ListProxies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb_proxy/paginators/#listproxiespaginator)
        """


if TYPE_CHECKING:
    _ListProxyUpdatesPaginatorBase = Paginator[ListProxyUpdatesResponseTypeDef]
else:
    _ListProxyUpdatesPaginatorBase = Paginator  # type: ignore[assignment]


class ListProxyUpdatesPaginator(_ListProxyUpdatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/paginator/ListProxyUpdates.html#ELBProxy.Paginator.ListProxyUpdates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb_proxy/paginators/#listproxyupdatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProxyUpdatesRequestPaginateTypeDef]
    ) -> PageIterator[ListProxyUpdatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/paginator/ListProxyUpdates.html#ELBProxy.Paginator.ListProxyUpdates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb_proxy/paginators/#listproxyupdatespaginator)
        """


if TYPE_CHECKING:
    _ListProxyVersionsPaginatorBase = Paginator[ListProxyVersionsResponseTypeDef]
else:
    _ListProxyVersionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListProxyVersionsPaginator(_ListProxyVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/paginator/ListProxyVersions.html#ELBProxy.Paginator.ListProxyVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb_proxy/paginators/#listproxyversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProxyVersionsRequestPaginateTypeDef]
    ) -> PageIterator[ListProxyVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/paginator/ListProxyVersions.html#ELBProxy.Paginator.ListProxyVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_elb_proxy/paginators/#listproxyversionspaginator)
        """
