"""
Type annotations for rtbfabric service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rtbfabric/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_rtbfabric.client import RTBFabricClient
    from mypy_boto3_rtbfabric.paginator import (
        ListAvailableModuleVersionsPaginator,
        ListAvailableModulesPaginator,
        ListCertificateAssociationsPaginator,
        ListLinkRoutingRulesPaginator,
        ListLinksPaginator,
        ListRequesterGatewaysPaginator,
        ListResponderGatewaysPaginator,
        ListUpdatesPaginator,
    )

    session = Session()
    client: RTBFabricClient = session.client("rtbfabric")

    list_available_module_versions_paginator: ListAvailableModuleVersionsPaginator = client.get_paginator("list_available_module_versions")
    list_available_modules_paginator: ListAvailableModulesPaginator = client.get_paginator("list_available_modules")
    list_certificate_associations_paginator: ListCertificateAssociationsPaginator = client.get_paginator("list_certificate_associations")
    list_link_routing_rules_paginator: ListLinkRoutingRulesPaginator = client.get_paginator("list_link_routing_rules")
    list_links_paginator: ListLinksPaginator = client.get_paginator("list_links")
    list_requester_gateways_paginator: ListRequesterGatewaysPaginator = client.get_paginator("list_requester_gateways")
    list_responder_gateways_paginator: ListResponderGatewaysPaginator = client.get_paginator("list_responder_gateways")
    list_updates_paginator: ListUpdatesPaginator = client.get_paginator("list_updates")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAvailableModulesRequestPaginateTypeDef,
    ListAvailableModulesResponseTypeDef,
    ListAvailableModuleVersionsRequestPaginateTypeDef,
    ListAvailableModuleVersionsResponseTypeDef,
    ListCertificateAssociationsRequestPaginateTypeDef,
    ListCertificateAssociationsResponseTypeDef,
    ListLinkRoutingRulesRequestPaginateTypeDef,
    ListLinkRoutingRulesResponseTypeDef,
    ListLinksRequestPaginateTypeDef,
    ListLinksResponseTypeDef,
    ListRequesterGatewaysRequestPaginateTypeDef,
    ListRequesterGatewaysResponseTypeDef,
    ListResponderGatewaysRequestPaginateTypeDef,
    ListResponderGatewaysResponseTypeDef,
    ListUpdatesRequestPaginateTypeDef,
    ListUpdatesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAvailableModuleVersionsPaginator",
    "ListAvailableModulesPaginator",
    "ListCertificateAssociationsPaginator",
    "ListLinkRoutingRulesPaginator",
    "ListLinksPaginator",
    "ListRequesterGatewaysPaginator",
    "ListResponderGatewaysPaginator",
    "ListUpdatesPaginator",
)


if TYPE_CHECKING:
    _ListAvailableModuleVersionsPaginatorBase = Paginator[
        ListAvailableModuleVersionsResponseTypeDef
    ]
else:
    _ListAvailableModuleVersionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListAvailableModuleVersionsPaginator(_ListAvailableModuleVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListAvailableModuleVersions.html#RTBFabric.Paginator.ListAvailableModuleVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rtbfabric/paginators/#listavailablemoduleversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAvailableModuleVersionsRequestPaginateTypeDef]
    ) -> PageIterator[ListAvailableModuleVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListAvailableModuleVersions.html#RTBFabric.Paginator.ListAvailableModuleVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rtbfabric/paginators/#listavailablemoduleversionspaginator)
        """


if TYPE_CHECKING:
    _ListAvailableModulesPaginatorBase = Paginator[ListAvailableModulesResponseTypeDef]
else:
    _ListAvailableModulesPaginatorBase = Paginator  # type: ignore[assignment]


class ListAvailableModulesPaginator(_ListAvailableModulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListAvailableModules.html#RTBFabric.Paginator.ListAvailableModules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rtbfabric/paginators/#listavailablemodulespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAvailableModulesRequestPaginateTypeDef]
    ) -> PageIterator[ListAvailableModulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListAvailableModules.html#RTBFabric.Paginator.ListAvailableModules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rtbfabric/paginators/#listavailablemodulespaginator)
        """


if TYPE_CHECKING:
    _ListCertificateAssociationsPaginatorBase = Paginator[
        ListCertificateAssociationsResponseTypeDef
    ]
else:
    _ListCertificateAssociationsPaginatorBase = Paginator  # type: ignore[assignment]


class ListCertificateAssociationsPaginator(_ListCertificateAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListCertificateAssociations.html#RTBFabric.Paginator.ListCertificateAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rtbfabric/paginators/#listcertificateassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCertificateAssociationsRequestPaginateTypeDef]
    ) -> PageIterator[ListCertificateAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListCertificateAssociations.html#RTBFabric.Paginator.ListCertificateAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rtbfabric/paginators/#listcertificateassociationspaginator)
        """


if TYPE_CHECKING:
    _ListLinkRoutingRulesPaginatorBase = Paginator[ListLinkRoutingRulesResponseTypeDef]
else:
    _ListLinkRoutingRulesPaginatorBase = Paginator  # type: ignore[assignment]


class ListLinkRoutingRulesPaginator(_ListLinkRoutingRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListLinkRoutingRules.html#RTBFabric.Paginator.ListLinkRoutingRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rtbfabric/paginators/#listlinkroutingrulespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLinkRoutingRulesRequestPaginateTypeDef]
    ) -> PageIterator[ListLinkRoutingRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListLinkRoutingRules.html#RTBFabric.Paginator.ListLinkRoutingRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rtbfabric/paginators/#listlinkroutingrulespaginator)
        """


if TYPE_CHECKING:
    _ListLinksPaginatorBase = Paginator[ListLinksResponseTypeDef]
else:
    _ListLinksPaginatorBase = Paginator  # type: ignore[assignment]


class ListLinksPaginator(_ListLinksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListLinks.html#RTBFabric.Paginator.ListLinks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rtbfabric/paginators/#listlinkspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLinksRequestPaginateTypeDef]
    ) -> PageIterator[ListLinksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListLinks.html#RTBFabric.Paginator.ListLinks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rtbfabric/paginators/#listlinkspaginator)
        """


if TYPE_CHECKING:
    _ListRequesterGatewaysPaginatorBase = Paginator[ListRequesterGatewaysResponseTypeDef]
else:
    _ListRequesterGatewaysPaginatorBase = Paginator  # type: ignore[assignment]


class ListRequesterGatewaysPaginator(_ListRequesterGatewaysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListRequesterGateways.html#RTBFabric.Paginator.ListRequesterGateways)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rtbfabric/paginators/#listrequestergatewayspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRequesterGatewaysRequestPaginateTypeDef]
    ) -> PageIterator[ListRequesterGatewaysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListRequesterGateways.html#RTBFabric.Paginator.ListRequesterGateways.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rtbfabric/paginators/#listrequestergatewayspaginator)
        """


if TYPE_CHECKING:
    _ListResponderGatewaysPaginatorBase = Paginator[ListResponderGatewaysResponseTypeDef]
else:
    _ListResponderGatewaysPaginatorBase = Paginator  # type: ignore[assignment]


class ListResponderGatewaysPaginator(_ListResponderGatewaysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListResponderGateways.html#RTBFabric.Paginator.ListResponderGateways)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rtbfabric/paginators/#listrespondergatewayspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResponderGatewaysRequestPaginateTypeDef]
    ) -> PageIterator[ListResponderGatewaysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListResponderGateways.html#RTBFabric.Paginator.ListResponderGateways.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rtbfabric/paginators/#listrespondergatewayspaginator)
        """


if TYPE_CHECKING:
    _ListUpdatesPaginatorBase = Paginator[ListUpdatesResponseTypeDef]
else:
    _ListUpdatesPaginatorBase = Paginator  # type: ignore[assignment]


class ListUpdatesPaginator(_ListUpdatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListUpdates.html#RTBFabric.Paginator.ListUpdates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rtbfabric/paginators/#listupdatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUpdatesRequestPaginateTypeDef]
    ) -> PageIterator[ListUpdatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rtbfabric/paginator/ListUpdates.html#RTBFabric.Paginator.ListUpdates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rtbfabric/paginators/#listupdatespaginator)
        """
