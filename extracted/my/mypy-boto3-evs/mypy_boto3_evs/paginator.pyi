"""
Type annotations for evs service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evs/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_evs.client import EVSClient
    from mypy_boto3_evs.paginator import (
        ListEnvironmentConnectorsPaginator,
        ListEnvironmentHostsPaginator,
        ListEnvironmentVlansPaginator,
        ListEnvironmentsPaginator,
        ListVmEntitlementsPaginator,
    )

    session = Session()
    client: EVSClient = session.client("evs")

    list_environment_connectors_paginator: ListEnvironmentConnectorsPaginator = client.get_paginator("list_environment_connectors")
    list_environment_hosts_paginator: ListEnvironmentHostsPaginator = client.get_paginator("list_environment_hosts")
    list_environment_vlans_paginator: ListEnvironmentVlansPaginator = client.get_paginator("list_environment_vlans")
    list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    list_vm_entitlements_paginator: ListVmEntitlementsPaginator = client.get_paginator("list_vm_entitlements")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListEnvironmentConnectorsRequestPaginateTypeDef,
    ListEnvironmentConnectorsResponseTypeDef,
    ListEnvironmentHostsRequestPaginateTypeDef,
    ListEnvironmentHostsResponseTypeDef,
    ListEnvironmentsRequestPaginateTypeDef,
    ListEnvironmentsResponseTypeDef,
    ListEnvironmentVlansRequestPaginateTypeDef,
    ListEnvironmentVlansResponseTypeDef,
    ListVmEntitlementsRequestPaginateTypeDef,
    ListVmEntitlementsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListEnvironmentConnectorsPaginator",
    "ListEnvironmentHostsPaginator",
    "ListEnvironmentVlansPaginator",
    "ListEnvironmentsPaginator",
    "ListVmEntitlementsPaginator",
)

if TYPE_CHECKING:
    _ListEnvironmentConnectorsPaginatorBase = Paginator[ListEnvironmentConnectorsResponseTypeDef]
else:
    _ListEnvironmentConnectorsPaginatorBase = Paginator  # type: ignore[assignment]

class ListEnvironmentConnectorsPaginator(_ListEnvironmentConnectorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evs/paginator/ListEnvironmentConnectors.html#EVS.Paginator.ListEnvironmentConnectors)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evs/paginators/#listenvironmentconnectorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentConnectorsRequestPaginateTypeDef]
    ) -> PageIterator[ListEnvironmentConnectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evs/paginator/ListEnvironmentConnectors.html#EVS.Paginator.ListEnvironmentConnectors.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evs/paginators/#listenvironmentconnectorspaginator)
        """

if TYPE_CHECKING:
    _ListEnvironmentHostsPaginatorBase = Paginator[ListEnvironmentHostsResponseTypeDef]
else:
    _ListEnvironmentHostsPaginatorBase = Paginator  # type: ignore[assignment]

class ListEnvironmentHostsPaginator(_ListEnvironmentHostsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evs/paginator/ListEnvironmentHosts.html#EVS.Paginator.ListEnvironmentHosts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evs/paginators/#listenvironmenthostspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentHostsRequestPaginateTypeDef]
    ) -> PageIterator[ListEnvironmentHostsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evs/paginator/ListEnvironmentHosts.html#EVS.Paginator.ListEnvironmentHosts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evs/paginators/#listenvironmenthostspaginator)
        """

if TYPE_CHECKING:
    _ListEnvironmentVlansPaginatorBase = Paginator[ListEnvironmentVlansResponseTypeDef]
else:
    _ListEnvironmentVlansPaginatorBase = Paginator  # type: ignore[assignment]

class ListEnvironmentVlansPaginator(_ListEnvironmentVlansPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evs/paginator/ListEnvironmentVlans.html#EVS.Paginator.ListEnvironmentVlans)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evs/paginators/#listenvironmentvlanspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentVlansRequestPaginateTypeDef]
    ) -> PageIterator[ListEnvironmentVlansResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evs/paginator/ListEnvironmentVlans.html#EVS.Paginator.ListEnvironmentVlans.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evs/paginators/#listenvironmentvlanspaginator)
        """

if TYPE_CHECKING:
    _ListEnvironmentsPaginatorBase = Paginator[ListEnvironmentsResponseTypeDef]
else:
    _ListEnvironmentsPaginatorBase = Paginator  # type: ignore[assignment]

class ListEnvironmentsPaginator(_ListEnvironmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evs/paginator/ListEnvironments.html#EVS.Paginator.ListEnvironments)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evs/paginators/#listenvironmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentsRequestPaginateTypeDef]
    ) -> PageIterator[ListEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evs/paginator/ListEnvironments.html#EVS.Paginator.ListEnvironments.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evs/paginators/#listenvironmentspaginator)
        """

if TYPE_CHECKING:
    _ListVmEntitlementsPaginatorBase = Paginator[ListVmEntitlementsResponseTypeDef]
else:
    _ListVmEntitlementsPaginatorBase = Paginator  # type: ignore[assignment]

class ListVmEntitlementsPaginator(_ListVmEntitlementsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evs/paginator/ListVmEntitlements.html#EVS.Paginator.ListVmEntitlements)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evs/paginators/#listvmentitlementspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVmEntitlementsRequestPaginateTypeDef]
    ) -> PageIterator[ListVmEntitlementsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evs/paginator/ListVmEntitlements.html#EVS.Paginator.ListVmEntitlements.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_evs/paginators/#listvmentitlementspaginator)
        """
