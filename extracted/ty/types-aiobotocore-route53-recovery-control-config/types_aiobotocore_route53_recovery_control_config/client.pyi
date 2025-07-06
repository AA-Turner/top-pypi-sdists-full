"""
Type annotations for route53-recovery-control-config service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_route53_recovery_control_config.client import Route53RecoveryControlConfigClient

    session = get_session()
    async with session.create_client("route53-recovery-control-config") as client:
        client: Route53RecoveryControlConfigClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListAssociatedRoute53HealthChecksPaginator,
    ListClustersPaginator,
    ListControlPanelsPaginator,
    ListRoutingControlsPaginator,
    ListSafetyRulesPaginator,
)
from .type_defs import (
    CreateClusterRequestTypeDef,
    CreateClusterResponseTypeDef,
    CreateControlPanelRequestTypeDef,
    CreateControlPanelResponseTypeDef,
    CreateRoutingControlRequestTypeDef,
    CreateRoutingControlResponseTypeDef,
    CreateSafetyRuleRequestTypeDef,
    CreateSafetyRuleResponseTypeDef,
    DeleteClusterRequestTypeDef,
    DeleteControlPanelRequestTypeDef,
    DeleteRoutingControlRequestTypeDef,
    DeleteSafetyRuleRequestTypeDef,
    DescribeClusterRequestTypeDef,
    DescribeClusterResponseTypeDef,
    DescribeControlPanelRequestTypeDef,
    DescribeControlPanelResponseTypeDef,
    DescribeRoutingControlRequestTypeDef,
    DescribeRoutingControlResponseTypeDef,
    DescribeSafetyRuleRequestTypeDef,
    DescribeSafetyRuleResponseTypeDef,
    GetResourcePolicyRequestTypeDef,
    GetResourcePolicyResponseTypeDef,
    ListAssociatedRoute53HealthChecksRequestTypeDef,
    ListAssociatedRoute53HealthChecksResponseTypeDef,
    ListClustersRequestTypeDef,
    ListClustersResponseTypeDef,
    ListControlPanelsRequestTypeDef,
    ListControlPanelsResponseTypeDef,
    ListRoutingControlsRequestTypeDef,
    ListRoutingControlsResponseTypeDef,
    ListSafetyRulesRequestTypeDef,
    ListSafetyRulesResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateClusterRequestTypeDef,
    UpdateClusterResponseTypeDef,
    UpdateControlPanelRequestTypeDef,
    UpdateControlPanelResponseTypeDef,
    UpdateRoutingControlRequestTypeDef,
    UpdateRoutingControlResponseTypeDef,
    UpdateSafetyRuleRequestTypeDef,
    UpdateSafetyRuleResponseTypeDef,
)
from .waiter import (
    ClusterCreatedWaiter,
    ClusterDeletedWaiter,
    ControlPanelCreatedWaiter,
    ControlPanelDeletedWaiter,
    RoutingControlCreatedWaiter,
    RoutingControlDeletedWaiter,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("Route53RecoveryControlConfigClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class Route53RecoveryControlConfigClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Route53RecoveryControlConfigClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#generate_presigned_url)
        """

    async def create_cluster(
        self, **kwargs: Unpack[CreateClusterRequestTypeDef]
    ) -> CreateClusterResponseTypeDef:
        """
        Create a new cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/create_cluster.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#create_cluster)
        """

    async def create_control_panel(
        self, **kwargs: Unpack[CreateControlPanelRequestTypeDef]
    ) -> CreateControlPanelResponseTypeDef:
        """
        Creates a new control panel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/create_control_panel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#create_control_panel)
        """

    async def create_routing_control(
        self, **kwargs: Unpack[CreateRoutingControlRequestTypeDef]
    ) -> CreateRoutingControlResponseTypeDef:
        """
        Creates a new routing control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/create_routing_control.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#create_routing_control)
        """

    async def create_safety_rule(
        self, **kwargs: Unpack[CreateSafetyRuleRequestTypeDef]
    ) -> CreateSafetyRuleResponseTypeDef:
        """
        Creates a safety rule in a control panel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/create_safety_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#create_safety_rule)
        """

    async def delete_cluster(self, **kwargs: Unpack[DeleteClusterRequestTypeDef]) -> Dict[str, Any]:
        """
        Delete a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/delete_cluster.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#delete_cluster)
        """

    async def delete_control_panel(
        self, **kwargs: Unpack[DeleteControlPanelRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a control panel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/delete_control_panel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#delete_control_panel)
        """

    async def delete_routing_control(
        self, **kwargs: Unpack[DeleteRoutingControlRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a routing control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/delete_routing_control.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#delete_routing_control)
        """

    async def delete_safety_rule(
        self, **kwargs: Unpack[DeleteSafetyRuleRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a safety rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/delete_safety_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#delete_safety_rule)
        """

    async def describe_cluster(
        self, **kwargs: Unpack[DescribeClusterRequestTypeDef]
    ) -> DescribeClusterResponseTypeDef:
        """
        Display the details about a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/describe_cluster.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#describe_cluster)
        """

    async def describe_control_panel(
        self, **kwargs: Unpack[DescribeControlPanelRequestTypeDef]
    ) -> DescribeControlPanelResponseTypeDef:
        """
        Displays details about a control panel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/describe_control_panel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#describe_control_panel)
        """

    async def describe_routing_control(
        self, **kwargs: Unpack[DescribeRoutingControlRequestTypeDef]
    ) -> DescribeRoutingControlResponseTypeDef:
        """
        Displays details about a routing control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/describe_routing_control.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#describe_routing_control)
        """

    async def describe_safety_rule(
        self, **kwargs: Unpack[DescribeSafetyRuleRequestTypeDef]
    ) -> DescribeSafetyRuleResponseTypeDef:
        """
        Returns information about a safety rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/describe_safety_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#describe_safety_rule)
        """

    async def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyRequestTypeDef]
    ) -> GetResourcePolicyResponseTypeDef:
        """
        Get information about the resource policy for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/get_resource_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#get_resource_policy)
        """

    async def list_associated_route53_health_checks(
        self, **kwargs: Unpack[ListAssociatedRoute53HealthChecksRequestTypeDef]
    ) -> ListAssociatedRoute53HealthChecksResponseTypeDef:
        """
        Returns an array of all Amazon Route 53 health checks associated with a
        specific routing control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/list_associated_route53_health_checks.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#list_associated_route53_health_checks)
        """

    async def list_clusters(
        self, **kwargs: Unpack[ListClustersRequestTypeDef]
    ) -> ListClustersResponseTypeDef:
        """
        Returns an array of all the clusters in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/list_clusters.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#list_clusters)
        """

    async def list_control_panels(
        self, **kwargs: Unpack[ListControlPanelsRequestTypeDef]
    ) -> ListControlPanelsResponseTypeDef:
        """
        Returns an array of control panels in an account or in a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/list_control_panels.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#list_control_panels)
        """

    async def list_routing_controls(
        self, **kwargs: Unpack[ListRoutingControlsRequestTypeDef]
    ) -> ListRoutingControlsResponseTypeDef:
        """
        Returns an array of routing controls for a control panel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/list_routing_controls.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#list_routing_controls)
        """

    async def list_safety_rules(
        self, **kwargs: Unpack[ListSafetyRulesRequestTypeDef]
    ) -> ListSafetyRulesResponseTypeDef:
        """
        List the safety rules (the assertion rules and gating rules) that you've
        defined for the routing controls in a control panel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/list_safety_rules.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#list_safety_rules)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#list_tags_for_resource)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds a tag to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes a tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#untag_resource)
        """

    async def update_cluster(
        self, **kwargs: Unpack[UpdateClusterRequestTypeDef]
    ) -> UpdateClusterResponseTypeDef:
        """
        Updates an existing cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/update_cluster.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#update_cluster)
        """

    async def update_control_panel(
        self, **kwargs: Unpack[UpdateControlPanelRequestTypeDef]
    ) -> UpdateControlPanelResponseTypeDef:
        """
        Updates a control panel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/update_control_panel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#update_control_panel)
        """

    async def update_routing_control(
        self, **kwargs: Unpack[UpdateRoutingControlRequestTypeDef]
    ) -> UpdateRoutingControlResponseTypeDef:
        """
        Updates a routing control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/update_routing_control.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#update_routing_control)
        """

    async def update_safety_rule(
        self, **kwargs: Unpack[UpdateSafetyRuleRequestTypeDef]
    ) -> UpdateSafetyRuleResponseTypeDef:
        """
        Update a safety rule (an assertion rule or gating rule).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/update_safety_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#update_safety_rule)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_associated_route53_health_checks"]
    ) -> ListAssociatedRoute53HealthChecksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_clusters"]
    ) -> ListClustersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_control_panels"]
    ) -> ListControlPanelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_routing_controls"]
    ) -> ListRoutingControlsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_safety_rules"]
    ) -> ListSafetyRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["cluster_created"]
    ) -> ClusterCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["cluster_deleted"]
    ) -> ClusterDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["control_panel_created"]
    ) -> ControlPanelCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["control_panel_deleted"]
    ) -> ControlPanelDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["routing_control_created"]
    ) -> RoutingControlCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["routing_control_deleted"]
    ) -> RoutingControlDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/#get_waiter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53-recovery-control-config.html#Route53RecoveryControlConfig.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53_recovery_control_config/client/)
        """
