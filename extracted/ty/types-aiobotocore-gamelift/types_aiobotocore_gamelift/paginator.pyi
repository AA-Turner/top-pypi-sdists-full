"""
Type annotations for gamelift service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_gamelift.client import GameLiftClient
    from types_aiobotocore_gamelift.paginator import (
        DescribeFleetAttributesPaginator,
        DescribeFleetCapacityPaginator,
        DescribeFleetEventsPaginator,
        DescribeFleetUtilizationPaginator,
        DescribeGameServerInstancesPaginator,
        DescribeGameSessionDetailsPaginator,
        DescribeGameSessionQueuesPaginator,
        DescribeGameSessionsPaginator,
        DescribeInstancesPaginator,
        DescribeMatchmakingConfigurationsPaginator,
        DescribeMatchmakingRuleSetsPaginator,
        DescribePlayerSessionsPaginator,
        DescribeScalingPoliciesPaginator,
        ListAliasesPaginator,
        ListBuildsPaginator,
        ListComputePaginator,
        ListContainerFleetsPaginator,
        ListContainerGroupDefinitionVersionsPaginator,
        ListContainerGroupDefinitionsPaginator,
        ListFleetDeploymentsPaginator,
        ListFleetsPaginator,
        ListGameServerGroupsPaginator,
        ListGameServersPaginator,
        ListLocationsPaginator,
        ListScriptsPaginator,
        SearchGameSessionsPaginator,
    )

    session = get_session()
    with session.create_client("gamelift") as client:
        client: GameLiftClient

        describe_fleet_attributes_paginator: DescribeFleetAttributesPaginator = client.get_paginator("describe_fleet_attributes")
        describe_fleet_capacity_paginator: DescribeFleetCapacityPaginator = client.get_paginator("describe_fleet_capacity")
        describe_fleet_events_paginator: DescribeFleetEventsPaginator = client.get_paginator("describe_fleet_events")
        describe_fleet_utilization_paginator: DescribeFleetUtilizationPaginator = client.get_paginator("describe_fleet_utilization")
        describe_game_server_instances_paginator: DescribeGameServerInstancesPaginator = client.get_paginator("describe_game_server_instances")
        describe_game_session_details_paginator: DescribeGameSessionDetailsPaginator = client.get_paginator("describe_game_session_details")
        describe_game_session_queues_paginator: DescribeGameSessionQueuesPaginator = client.get_paginator("describe_game_session_queues")
        describe_game_sessions_paginator: DescribeGameSessionsPaginator = client.get_paginator("describe_game_sessions")
        describe_instances_paginator: DescribeInstancesPaginator = client.get_paginator("describe_instances")
        describe_matchmaking_configurations_paginator: DescribeMatchmakingConfigurationsPaginator = client.get_paginator("describe_matchmaking_configurations")
        describe_matchmaking_rule_sets_paginator: DescribeMatchmakingRuleSetsPaginator = client.get_paginator("describe_matchmaking_rule_sets")
        describe_player_sessions_paginator: DescribePlayerSessionsPaginator = client.get_paginator("describe_player_sessions")
        describe_scaling_policies_paginator: DescribeScalingPoliciesPaginator = client.get_paginator("describe_scaling_policies")
        list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
        list_builds_paginator: ListBuildsPaginator = client.get_paginator("list_builds")
        list_compute_paginator: ListComputePaginator = client.get_paginator("list_compute")
        list_container_fleets_paginator: ListContainerFleetsPaginator = client.get_paginator("list_container_fleets")
        list_container_group_definition_versions_paginator: ListContainerGroupDefinitionVersionsPaginator = client.get_paginator("list_container_group_definition_versions")
        list_container_group_definitions_paginator: ListContainerGroupDefinitionsPaginator = client.get_paginator("list_container_group_definitions")
        list_fleet_deployments_paginator: ListFleetDeploymentsPaginator = client.get_paginator("list_fleet_deployments")
        list_fleets_paginator: ListFleetsPaginator = client.get_paginator("list_fleets")
        list_game_server_groups_paginator: ListGameServerGroupsPaginator = client.get_paginator("list_game_server_groups")
        list_game_servers_paginator: ListGameServersPaginator = client.get_paginator("list_game_servers")
        list_locations_paginator: ListLocationsPaginator = client.get_paginator("list_locations")
        list_scripts_paginator: ListScriptsPaginator = client.get_paginator("list_scripts")
        search_game_sessions_paginator: SearchGameSessionsPaginator = client.get_paginator("search_game_sessions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeFleetAttributesInputPaginateTypeDef,
    DescribeFleetAttributesOutputTypeDef,
    DescribeFleetCapacityInputPaginateTypeDef,
    DescribeFleetCapacityOutputTypeDef,
    DescribeFleetEventsInputPaginateTypeDef,
    DescribeFleetEventsOutputTypeDef,
    DescribeFleetUtilizationInputPaginateTypeDef,
    DescribeFleetUtilizationOutputTypeDef,
    DescribeGameServerInstancesInputPaginateTypeDef,
    DescribeGameServerInstancesOutputTypeDef,
    DescribeGameSessionDetailsInputPaginateTypeDef,
    DescribeGameSessionDetailsOutputTypeDef,
    DescribeGameSessionQueuesInputPaginateTypeDef,
    DescribeGameSessionQueuesOutputTypeDef,
    DescribeGameSessionsInputPaginateTypeDef,
    DescribeGameSessionsOutputTypeDef,
    DescribeInstancesInputPaginateTypeDef,
    DescribeInstancesOutputTypeDef,
    DescribeMatchmakingConfigurationsInputPaginateTypeDef,
    DescribeMatchmakingConfigurationsOutputTypeDef,
    DescribeMatchmakingRuleSetsInputPaginateTypeDef,
    DescribeMatchmakingRuleSetsOutputTypeDef,
    DescribePlayerSessionsInputPaginateTypeDef,
    DescribePlayerSessionsOutputTypeDef,
    DescribeScalingPoliciesInputPaginateTypeDef,
    DescribeScalingPoliciesOutputTypeDef,
    ListAliasesInputPaginateTypeDef,
    ListAliasesOutputTypeDef,
    ListBuildsInputPaginateTypeDef,
    ListBuildsOutputTypeDef,
    ListComputeInputPaginateTypeDef,
    ListComputeOutputTypeDef,
    ListContainerFleetsInputPaginateTypeDef,
    ListContainerFleetsOutputTypeDef,
    ListContainerGroupDefinitionsInputPaginateTypeDef,
    ListContainerGroupDefinitionsOutputTypeDef,
    ListContainerGroupDefinitionVersionsInputPaginateTypeDef,
    ListContainerGroupDefinitionVersionsOutputTypeDef,
    ListFleetDeploymentsInputPaginateTypeDef,
    ListFleetDeploymentsOutputTypeDef,
    ListFleetsInputPaginateTypeDef,
    ListFleetsOutputTypeDef,
    ListGameServerGroupsInputPaginateTypeDef,
    ListGameServerGroupsOutputTypeDef,
    ListGameServersInputPaginateTypeDef,
    ListGameServersOutputTypeDef,
    ListLocationsInputPaginateTypeDef,
    ListLocationsOutputTypeDef,
    ListScriptsInputPaginateTypeDef,
    ListScriptsOutputTypeDef,
    SearchGameSessionsInputPaginateTypeDef,
    SearchGameSessionsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeFleetAttributesPaginator",
    "DescribeFleetCapacityPaginator",
    "DescribeFleetEventsPaginator",
    "DescribeFleetUtilizationPaginator",
    "DescribeGameServerInstancesPaginator",
    "DescribeGameSessionDetailsPaginator",
    "DescribeGameSessionQueuesPaginator",
    "DescribeGameSessionsPaginator",
    "DescribeInstancesPaginator",
    "DescribeMatchmakingConfigurationsPaginator",
    "DescribeMatchmakingRuleSetsPaginator",
    "DescribePlayerSessionsPaginator",
    "DescribeScalingPoliciesPaginator",
    "ListAliasesPaginator",
    "ListBuildsPaginator",
    "ListComputePaginator",
    "ListContainerFleetsPaginator",
    "ListContainerGroupDefinitionVersionsPaginator",
    "ListContainerGroupDefinitionsPaginator",
    "ListFleetDeploymentsPaginator",
    "ListFleetsPaginator",
    "ListGameServerGroupsPaginator",
    "ListGameServersPaginator",
    "ListLocationsPaginator",
    "ListScriptsPaginator",
    "SearchGameSessionsPaginator",
)

if TYPE_CHECKING:
    _DescribeFleetAttributesPaginatorBase = AioPaginator[DescribeFleetAttributesOutputTypeDef]
else:
    _DescribeFleetAttributesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeFleetAttributesPaginator(_DescribeFleetAttributesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetAttributes.html#GameLift.Paginator.DescribeFleetAttributes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleetattributespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFleetAttributesInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeFleetAttributesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetAttributes.html#GameLift.Paginator.DescribeFleetAttributes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleetattributespaginator)
        """

if TYPE_CHECKING:
    _DescribeFleetCapacityPaginatorBase = AioPaginator[DescribeFleetCapacityOutputTypeDef]
else:
    _DescribeFleetCapacityPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeFleetCapacityPaginator(_DescribeFleetCapacityPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetCapacity.html#GameLift.Paginator.DescribeFleetCapacity)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleetcapacitypaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFleetCapacityInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeFleetCapacityOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetCapacity.html#GameLift.Paginator.DescribeFleetCapacity.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleetcapacitypaginator)
        """

if TYPE_CHECKING:
    _DescribeFleetEventsPaginatorBase = AioPaginator[DescribeFleetEventsOutputTypeDef]
else:
    _DescribeFleetEventsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeFleetEventsPaginator(_DescribeFleetEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetEvents.html#GameLift.Paginator.DescribeFleetEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleeteventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFleetEventsInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeFleetEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetEvents.html#GameLift.Paginator.DescribeFleetEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleeteventspaginator)
        """

if TYPE_CHECKING:
    _DescribeFleetUtilizationPaginatorBase = AioPaginator[DescribeFleetUtilizationOutputTypeDef]
else:
    _DescribeFleetUtilizationPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeFleetUtilizationPaginator(_DescribeFleetUtilizationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetUtilization.html#GameLift.Paginator.DescribeFleetUtilization)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleetutilizationpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFleetUtilizationInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeFleetUtilizationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetUtilization.html#GameLift.Paginator.DescribeFleetUtilization.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describefleetutilizationpaginator)
        """

if TYPE_CHECKING:
    _DescribeGameServerInstancesPaginatorBase = AioPaginator[
        DescribeGameServerInstancesOutputTypeDef
    ]
else:
    _DescribeGameServerInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeGameServerInstancesPaginator(_DescribeGameServerInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameServerInstances.html#GameLift.Paginator.DescribeGameServerInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegameserverinstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeGameServerInstancesInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeGameServerInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameServerInstances.html#GameLift.Paginator.DescribeGameServerInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegameserverinstancespaginator)
        """

if TYPE_CHECKING:
    _DescribeGameSessionDetailsPaginatorBase = AioPaginator[DescribeGameSessionDetailsOutputTypeDef]
else:
    _DescribeGameSessionDetailsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeGameSessionDetailsPaginator(_DescribeGameSessionDetailsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessionDetails.html#GameLift.Paginator.DescribeGameSessionDetails)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegamesessiondetailspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeGameSessionDetailsInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeGameSessionDetailsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessionDetails.html#GameLift.Paginator.DescribeGameSessionDetails.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegamesessiondetailspaginator)
        """

if TYPE_CHECKING:
    _DescribeGameSessionQueuesPaginatorBase = AioPaginator[DescribeGameSessionQueuesOutputTypeDef]
else:
    _DescribeGameSessionQueuesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeGameSessionQueuesPaginator(_DescribeGameSessionQueuesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessionQueues.html#GameLift.Paginator.DescribeGameSessionQueues)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegamesessionqueuespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeGameSessionQueuesInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeGameSessionQueuesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessionQueues.html#GameLift.Paginator.DescribeGameSessionQueues.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegamesessionqueuespaginator)
        """

if TYPE_CHECKING:
    _DescribeGameSessionsPaginatorBase = AioPaginator[DescribeGameSessionsOutputTypeDef]
else:
    _DescribeGameSessionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeGameSessionsPaginator(_DescribeGameSessionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessions.html#GameLift.Paginator.DescribeGameSessions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegamesessionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeGameSessionsInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeGameSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessions.html#GameLift.Paginator.DescribeGameSessions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describegamesessionspaginator)
        """

if TYPE_CHECKING:
    _DescribeInstancesPaginatorBase = AioPaginator[DescribeInstancesOutputTypeDef]
else:
    _DescribeInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeInstancesPaginator(_DescribeInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeInstances.html#GameLift.Paginator.DescribeInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describeinstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInstancesInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeInstances.html#GameLift.Paginator.DescribeInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describeinstancespaginator)
        """

if TYPE_CHECKING:
    _DescribeMatchmakingConfigurationsPaginatorBase = AioPaginator[
        DescribeMatchmakingConfigurationsOutputTypeDef
    ]
else:
    _DescribeMatchmakingConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeMatchmakingConfigurationsPaginator(_DescribeMatchmakingConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeMatchmakingConfigurations.html#GameLift.Paginator.DescribeMatchmakingConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describematchmakingconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMatchmakingConfigurationsInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeMatchmakingConfigurationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeMatchmakingConfigurations.html#GameLift.Paginator.DescribeMatchmakingConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describematchmakingconfigurationspaginator)
        """

if TYPE_CHECKING:
    _DescribeMatchmakingRuleSetsPaginatorBase = AioPaginator[
        DescribeMatchmakingRuleSetsOutputTypeDef
    ]
else:
    _DescribeMatchmakingRuleSetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeMatchmakingRuleSetsPaginator(_DescribeMatchmakingRuleSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeMatchmakingRuleSets.html#GameLift.Paginator.DescribeMatchmakingRuleSets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describematchmakingrulesetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMatchmakingRuleSetsInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeMatchmakingRuleSetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeMatchmakingRuleSets.html#GameLift.Paginator.DescribeMatchmakingRuleSets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describematchmakingrulesetspaginator)
        """

if TYPE_CHECKING:
    _DescribePlayerSessionsPaginatorBase = AioPaginator[DescribePlayerSessionsOutputTypeDef]
else:
    _DescribePlayerSessionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribePlayerSessionsPaginator(_DescribePlayerSessionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribePlayerSessions.html#GameLift.Paginator.DescribePlayerSessions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describeplayersessionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribePlayerSessionsInputPaginateTypeDef]
    ) -> AioPageIterator[DescribePlayerSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribePlayerSessions.html#GameLift.Paginator.DescribePlayerSessions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describeplayersessionspaginator)
        """

if TYPE_CHECKING:
    _DescribeScalingPoliciesPaginatorBase = AioPaginator[DescribeScalingPoliciesOutputTypeDef]
else:
    _DescribeScalingPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeScalingPoliciesPaginator(_DescribeScalingPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeScalingPolicies.html#GameLift.Paginator.DescribeScalingPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describescalingpoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeScalingPoliciesInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeScalingPoliciesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeScalingPolicies.html#GameLift.Paginator.DescribeScalingPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#describescalingpoliciespaginator)
        """

if TYPE_CHECKING:
    _ListAliasesPaginatorBase = AioPaginator[ListAliasesOutputTypeDef]
else:
    _ListAliasesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAliasesPaginator(_ListAliasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListAliases.html#GameLift.Paginator.ListAliases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listaliasespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAliasesInputPaginateTypeDef]
    ) -> AioPageIterator[ListAliasesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListAliases.html#GameLift.Paginator.ListAliases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listaliasespaginator)
        """

if TYPE_CHECKING:
    _ListBuildsPaginatorBase = AioPaginator[ListBuildsOutputTypeDef]
else:
    _ListBuildsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBuildsPaginator(_ListBuildsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListBuilds.html#GameLift.Paginator.ListBuilds)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listbuildspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBuildsInputPaginateTypeDef]
    ) -> AioPageIterator[ListBuildsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListBuilds.html#GameLift.Paginator.ListBuilds.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listbuildspaginator)
        """

if TYPE_CHECKING:
    _ListComputePaginatorBase = AioPaginator[ListComputeOutputTypeDef]
else:
    _ListComputePaginatorBase = AioPaginator  # type: ignore[assignment]

class ListComputePaginator(_ListComputePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListCompute.html#GameLift.Paginator.ListCompute)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listcomputepaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListComputeInputPaginateTypeDef]
    ) -> AioPageIterator[ListComputeOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListCompute.html#GameLift.Paginator.ListCompute.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listcomputepaginator)
        """

if TYPE_CHECKING:
    _ListContainerFleetsPaginatorBase = AioPaginator[ListContainerFleetsOutputTypeDef]
else:
    _ListContainerFleetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListContainerFleetsPaginator(_ListContainerFleetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListContainerFleets.html#GameLift.Paginator.ListContainerFleets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listcontainerfleetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContainerFleetsInputPaginateTypeDef]
    ) -> AioPageIterator[ListContainerFleetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListContainerFleets.html#GameLift.Paginator.ListContainerFleets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listcontainerfleetspaginator)
        """

if TYPE_CHECKING:
    _ListContainerGroupDefinitionVersionsPaginatorBase = AioPaginator[
        ListContainerGroupDefinitionVersionsOutputTypeDef
    ]
else:
    _ListContainerGroupDefinitionVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListContainerGroupDefinitionVersionsPaginator(
    _ListContainerGroupDefinitionVersionsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListContainerGroupDefinitionVersions.html#GameLift.Paginator.ListContainerGroupDefinitionVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listcontainergroupdefinitionversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContainerGroupDefinitionVersionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListContainerGroupDefinitionVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListContainerGroupDefinitionVersions.html#GameLift.Paginator.ListContainerGroupDefinitionVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listcontainergroupdefinitionversionspaginator)
        """

if TYPE_CHECKING:
    _ListContainerGroupDefinitionsPaginatorBase = AioPaginator[
        ListContainerGroupDefinitionsOutputTypeDef
    ]
else:
    _ListContainerGroupDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListContainerGroupDefinitionsPaginator(_ListContainerGroupDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListContainerGroupDefinitions.html#GameLift.Paginator.ListContainerGroupDefinitions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listcontainergroupdefinitionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContainerGroupDefinitionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListContainerGroupDefinitionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListContainerGroupDefinitions.html#GameLift.Paginator.ListContainerGroupDefinitions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listcontainergroupdefinitionspaginator)
        """

if TYPE_CHECKING:
    _ListFleetDeploymentsPaginatorBase = AioPaginator[ListFleetDeploymentsOutputTypeDef]
else:
    _ListFleetDeploymentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFleetDeploymentsPaginator(_ListFleetDeploymentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListFleetDeployments.html#GameLift.Paginator.ListFleetDeployments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listfleetdeploymentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFleetDeploymentsInputPaginateTypeDef]
    ) -> AioPageIterator[ListFleetDeploymentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListFleetDeployments.html#GameLift.Paginator.ListFleetDeployments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listfleetdeploymentspaginator)
        """

if TYPE_CHECKING:
    _ListFleetsPaginatorBase = AioPaginator[ListFleetsOutputTypeDef]
else:
    _ListFleetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFleetsPaginator(_ListFleetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListFleets.html#GameLift.Paginator.ListFleets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listfleetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFleetsInputPaginateTypeDef]
    ) -> AioPageIterator[ListFleetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListFleets.html#GameLift.Paginator.ListFleets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listfleetspaginator)
        """

if TYPE_CHECKING:
    _ListGameServerGroupsPaginatorBase = AioPaginator[ListGameServerGroupsOutputTypeDef]
else:
    _ListGameServerGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListGameServerGroupsPaginator(_ListGameServerGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListGameServerGroups.html#GameLift.Paginator.ListGameServerGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listgameservergroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGameServerGroupsInputPaginateTypeDef]
    ) -> AioPageIterator[ListGameServerGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListGameServerGroups.html#GameLift.Paginator.ListGameServerGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listgameservergroupspaginator)
        """

if TYPE_CHECKING:
    _ListGameServersPaginatorBase = AioPaginator[ListGameServersOutputTypeDef]
else:
    _ListGameServersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListGameServersPaginator(_ListGameServersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListGameServers.html#GameLift.Paginator.ListGameServers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listgameserverspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGameServersInputPaginateTypeDef]
    ) -> AioPageIterator[ListGameServersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListGameServers.html#GameLift.Paginator.ListGameServers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listgameserverspaginator)
        """

if TYPE_CHECKING:
    _ListLocationsPaginatorBase = AioPaginator[ListLocationsOutputTypeDef]
else:
    _ListLocationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLocationsPaginator(_ListLocationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListLocations.html#GameLift.Paginator.ListLocations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listlocationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLocationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListLocationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListLocations.html#GameLift.Paginator.ListLocations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listlocationspaginator)
        """

if TYPE_CHECKING:
    _ListScriptsPaginatorBase = AioPaginator[ListScriptsOutputTypeDef]
else:
    _ListScriptsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListScriptsPaginator(_ListScriptsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListScripts.html#GameLift.Paginator.ListScripts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listscriptspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListScriptsInputPaginateTypeDef]
    ) -> AioPageIterator[ListScriptsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListScripts.html#GameLift.Paginator.ListScripts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#listscriptspaginator)
        """

if TYPE_CHECKING:
    _SearchGameSessionsPaginatorBase = AioPaginator[SearchGameSessionsOutputTypeDef]
else:
    _SearchGameSessionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchGameSessionsPaginator(_SearchGameSessionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/SearchGameSessions.html#GameLift.Paginator.SearchGameSessions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#searchgamesessionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchGameSessionsInputPaginateTypeDef]
    ) -> AioPageIterator[SearchGameSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/SearchGameSessions.html#GameLift.Paginator.SearchGameSessions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamelift/paginators/#searchgamesessionspaginator)
        """
