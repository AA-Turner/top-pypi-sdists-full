"""
Type annotations for route53-recovery-control-config service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_route53_recovery_control_config.client import Route53RecoveryControlConfigClient
    from types_aiobotocore_route53_recovery_control_config.paginator import (
        ListAssociatedRoute53HealthChecksPaginator,
        ListClustersPaginator,
        ListControlPanelsPaginator,
        ListRoutingControlsPaginator,
        ListSafetyRulesPaginator,
    )

    session = get_session()
    with session.create_client("route53-recovery-control-config") as client:
        client: Route53RecoveryControlConfigClient

        list_associated_route53_health_checks_paginator: ListAssociatedRoute53HealthChecksPaginator = client.get_paginator("list_associated_route53_health_checks")
        list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
        list_control_panels_paginator: ListControlPanelsPaginator = client.get_paginator("list_control_panels")
        list_routing_controls_paginator: ListRoutingControlsPaginator = client.get_paginator("list_routing_controls")
        list_safety_rules_paginator: ListSafetyRulesPaginator = client.get_paginator("list_safety_rules")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAssociatedRoute53HealthChecksRequestPaginateTypeDef,
    ListAssociatedRoute53HealthChecksResponseTypeDef,
    ListClustersRequestPaginateTypeDef,
    ListClustersResponseTypeDef,
    ListControlPanelsRequestPaginateTypeDef,
    ListControlPanelsResponseTypeDef,
    ListRoutingControlsRequestPaginateTypeDef,
    ListRoutingControlsResponseTypeDef,
    ListSafetyRulesRequestPaginateTypeDef,
    ListSafetyRulesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAssociatedRoute53HealthChecksPaginator",
    "ListClustersPaginator",
    "ListControlPanelsPaginator",
    "ListRoutingControlsPaginator",
    "ListSafetyRulesPaginator",
)

if TYPE_CHECKING:
    _ListAssociatedRoute53HealthChecksPaginatorBase = AioPaginator[
        ListAssociatedRoute53HealthChecksResponseTypeDef
    ]
else:
    _ListAssociatedRoute53HealthChecksPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAssociatedRoute53HealthChecksPaginator(_ListAssociatedRoute53HealthChecksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/paginator/ListAssociatedRoute53HealthChecks.html#Route53RecoveryControlConfig.Paginator.ListAssociatedRoute53HealthChecks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/paginators/#listassociatedroute53healthcheckspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssociatedRoute53HealthChecksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssociatedRoute53HealthChecksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/paginator/ListAssociatedRoute53HealthChecks.html#Route53RecoveryControlConfig.Paginator.ListAssociatedRoute53HealthChecks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/paginators/#listassociatedroute53healthcheckspaginator)
        """

if TYPE_CHECKING:
    _ListClustersPaginatorBase = AioPaginator[ListClustersResponseTypeDef]
else:
    _ListClustersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListClustersPaginator(_ListClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/paginator/ListClusters.html#Route53RecoveryControlConfig.Paginator.ListClusters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/paginators/#listclusterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListClustersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/paginator/ListClusters.html#Route53RecoveryControlConfig.Paginator.ListClusters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/paginators/#listclusterspaginator)
        """

if TYPE_CHECKING:
    _ListControlPanelsPaginatorBase = AioPaginator[ListControlPanelsResponseTypeDef]
else:
    _ListControlPanelsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListControlPanelsPaginator(_ListControlPanelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/paginator/ListControlPanels.html#Route53RecoveryControlConfig.Paginator.ListControlPanels)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/paginators/#listcontrolpanelspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListControlPanelsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListControlPanelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/paginator/ListControlPanels.html#Route53RecoveryControlConfig.Paginator.ListControlPanels.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/paginators/#listcontrolpanelspaginator)
        """

if TYPE_CHECKING:
    _ListRoutingControlsPaginatorBase = AioPaginator[ListRoutingControlsResponseTypeDef]
else:
    _ListRoutingControlsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRoutingControlsPaginator(_ListRoutingControlsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/paginator/ListRoutingControls.html#Route53RecoveryControlConfig.Paginator.ListRoutingControls)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/paginators/#listroutingcontrolspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRoutingControlsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRoutingControlsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/paginator/ListRoutingControls.html#Route53RecoveryControlConfig.Paginator.ListRoutingControls.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/paginators/#listroutingcontrolspaginator)
        """

if TYPE_CHECKING:
    _ListSafetyRulesPaginatorBase = AioPaginator[ListSafetyRulesResponseTypeDef]
else:
    _ListSafetyRulesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSafetyRulesPaginator(_ListSafetyRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/paginator/ListSafetyRules.html#Route53RecoveryControlConfig.Paginator.ListSafetyRules)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/paginators/#listsafetyrulespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSafetyRulesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSafetyRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/paginator/ListSafetyRules.html#Route53RecoveryControlConfig.Paginator.ListSafetyRules.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/paginators/#listsafetyrulespaginator)
        """
