"""
Type annotations for evs service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evs/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_evs.client import EVSClient
    from types_aiobotocore_evs.paginator import (
        ListEnvironmentConnectorsPaginator,
        ListEnvironmentHostsPaginator,
        ListEnvironmentVlansPaginator,
        ListEnvironmentsPaginator,
        ListVmEntitlementsPaginator,
    )

    session = get_session()
    with session.create_client("evs") as client:
        client: EVSClient

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

from aiobotocore.paginate import AioPageIterator, AioPaginator

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
    _ListEnvironmentConnectorsPaginatorBase = AioPaginator[ListEnvironmentConnectorsResponseTypeDef]
else:
    _ListEnvironmentConnectorsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEnvironmentConnectorsPaginator(_ListEnvironmentConnectorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evs/paginator/ListEnvironmentConnectors.html#EVS.Paginator.ListEnvironmentConnectors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evs/paginators/#listenvironmentconnectorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentConnectorsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEnvironmentConnectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evs/paginator/ListEnvironmentConnectors.html#EVS.Paginator.ListEnvironmentConnectors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evs/paginators/#listenvironmentconnectorspaginator)
        """

if TYPE_CHECKING:
    _ListEnvironmentHostsPaginatorBase = AioPaginator[ListEnvironmentHostsResponseTypeDef]
else:
    _ListEnvironmentHostsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEnvironmentHostsPaginator(_ListEnvironmentHostsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evs/paginator/ListEnvironmentHosts.html#EVS.Paginator.ListEnvironmentHosts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evs/paginators/#listenvironmenthostspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentHostsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEnvironmentHostsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evs/paginator/ListEnvironmentHosts.html#EVS.Paginator.ListEnvironmentHosts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evs/paginators/#listenvironmenthostspaginator)
        """

if TYPE_CHECKING:
    _ListEnvironmentVlansPaginatorBase = AioPaginator[ListEnvironmentVlansResponseTypeDef]
else:
    _ListEnvironmentVlansPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEnvironmentVlansPaginator(_ListEnvironmentVlansPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evs/paginator/ListEnvironmentVlans.html#EVS.Paginator.ListEnvironmentVlans)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evs/paginators/#listenvironmentvlanspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentVlansRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEnvironmentVlansResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evs/paginator/ListEnvironmentVlans.html#EVS.Paginator.ListEnvironmentVlans.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evs/paginators/#listenvironmentvlanspaginator)
        """

if TYPE_CHECKING:
    _ListEnvironmentsPaginatorBase = AioPaginator[ListEnvironmentsResponseTypeDef]
else:
    _ListEnvironmentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEnvironmentsPaginator(_ListEnvironmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evs/paginator/ListEnvironments.html#EVS.Paginator.ListEnvironments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evs/paginators/#listenvironmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evs/paginator/ListEnvironments.html#EVS.Paginator.ListEnvironments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evs/paginators/#listenvironmentspaginator)
        """

if TYPE_CHECKING:
    _ListVmEntitlementsPaginatorBase = AioPaginator[ListVmEntitlementsResponseTypeDef]
else:
    _ListVmEntitlementsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListVmEntitlementsPaginator(_ListVmEntitlementsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evs/paginator/ListVmEntitlements.html#EVS.Paginator.ListVmEntitlements)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evs/paginators/#listvmentitlementspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVmEntitlementsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListVmEntitlementsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/evs/paginator/ListVmEntitlements.html#EVS.Paginator.ListVmEntitlements.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_evs/paginators/#listvmentitlementspaginator)
        """
