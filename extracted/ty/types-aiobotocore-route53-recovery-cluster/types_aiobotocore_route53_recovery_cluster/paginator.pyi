"""
Type annotations for route53-recovery-cluster service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_route53_recovery_cluster.client import Route53RecoveryClusterClient
    from types_aiobotocore_route53_recovery_cluster.paginator import (
        ListRoutingControlsPaginator,
    )

    session = get_session()
    with session.create_client("route53-recovery-cluster") as client:
        client: Route53RecoveryClusterClient

        list_routing_controls_paginator: ListRoutingControlsPaginator = client.get_paginator("list_routing_controls")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import ListRoutingControlsRequestPaginateTypeDef, ListRoutingControlsResponseTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListRoutingControlsPaginator",)

if TYPE_CHECKING:
    _ListRoutingControlsPaginatorBase = AioPaginator[ListRoutingControlsResponseTypeDef]
else:
    _ListRoutingControlsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRoutingControlsPaginator(_ListRoutingControlsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster/paginator/ListRoutingControls.html#Route53RecoveryCluster.Paginator.ListRoutingControls)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/paginators/#listroutingcontrolspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRoutingControlsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRoutingControlsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-cluster/paginator/ListRoutingControls.html#Route53RecoveryCluster.Paginator.ListRoutingControls.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_cluster/paginators/#listroutingcontrolspaginator)
        """
