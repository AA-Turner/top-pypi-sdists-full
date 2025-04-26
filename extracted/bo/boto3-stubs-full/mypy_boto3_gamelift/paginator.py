"""
Type annotations for gamelift service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_gamelift.client import GameLiftClient
    from mypy_boto3_gamelift.paginator import (
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

    session = Session()
    client: GameLiftClient = session.client("gamelift")

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

from botocore.paginate import PageIterator, Paginator

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
    _DescribeFleetAttributesPaginatorBase = Paginator[DescribeFleetAttributesOutputTypeDef]
else:
    _DescribeFleetAttributesPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeFleetAttributesPaginator(_DescribeFleetAttributesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetAttributes.html#GameLift.Paginator.DescribeFleetAttributes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleetattributespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFleetAttributesInputPaginateTypeDef]
    ) -> PageIterator[DescribeFleetAttributesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetAttributes.html#GameLift.Paginator.DescribeFleetAttributes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleetattributespaginator)
        """


if TYPE_CHECKING:
    _DescribeFleetCapacityPaginatorBase = Paginator[DescribeFleetCapacityOutputTypeDef]
else:
    _DescribeFleetCapacityPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeFleetCapacityPaginator(_DescribeFleetCapacityPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetCapacity.html#GameLift.Paginator.DescribeFleetCapacity)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleetcapacitypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFleetCapacityInputPaginateTypeDef]
    ) -> PageIterator[DescribeFleetCapacityOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetCapacity.html#GameLift.Paginator.DescribeFleetCapacity.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleetcapacitypaginator)
        """


if TYPE_CHECKING:
    _DescribeFleetEventsPaginatorBase = Paginator[DescribeFleetEventsOutputTypeDef]
else:
    _DescribeFleetEventsPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeFleetEventsPaginator(_DescribeFleetEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetEvents.html#GameLift.Paginator.DescribeFleetEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleeteventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFleetEventsInputPaginateTypeDef]
    ) -> PageIterator[DescribeFleetEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetEvents.html#GameLift.Paginator.DescribeFleetEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleeteventspaginator)
        """


if TYPE_CHECKING:
    _DescribeFleetUtilizationPaginatorBase = Paginator[DescribeFleetUtilizationOutputTypeDef]
else:
    _DescribeFleetUtilizationPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeFleetUtilizationPaginator(_DescribeFleetUtilizationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetUtilization.html#GameLift.Paginator.DescribeFleetUtilization)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleetutilizationpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFleetUtilizationInputPaginateTypeDef]
    ) -> PageIterator[DescribeFleetUtilizationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeFleetUtilization.html#GameLift.Paginator.DescribeFleetUtilization.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describefleetutilizationpaginator)
        """


if TYPE_CHECKING:
    _DescribeGameServerInstancesPaginatorBase = Paginator[DescribeGameServerInstancesOutputTypeDef]
else:
    _DescribeGameServerInstancesPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeGameServerInstancesPaginator(_DescribeGameServerInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameServerInstances.html#GameLift.Paginator.DescribeGameServerInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegameserverinstancespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeGameServerInstancesInputPaginateTypeDef]
    ) -> PageIterator[DescribeGameServerInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameServerInstances.html#GameLift.Paginator.DescribeGameServerInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegameserverinstancespaginator)
        """


if TYPE_CHECKING:
    _DescribeGameSessionDetailsPaginatorBase = Paginator[DescribeGameSessionDetailsOutputTypeDef]
else:
    _DescribeGameSessionDetailsPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeGameSessionDetailsPaginator(_DescribeGameSessionDetailsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessionDetails.html#GameLift.Paginator.DescribeGameSessionDetails)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegamesessiondetailspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeGameSessionDetailsInputPaginateTypeDef]
    ) -> PageIterator[DescribeGameSessionDetailsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessionDetails.html#GameLift.Paginator.DescribeGameSessionDetails.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegamesessiondetailspaginator)
        """


if TYPE_CHECKING:
    _DescribeGameSessionQueuesPaginatorBase = Paginator[DescribeGameSessionQueuesOutputTypeDef]
else:
    _DescribeGameSessionQueuesPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeGameSessionQueuesPaginator(_DescribeGameSessionQueuesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessionQueues.html#GameLift.Paginator.DescribeGameSessionQueues)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegamesessionqueuespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeGameSessionQueuesInputPaginateTypeDef]
    ) -> PageIterator[DescribeGameSessionQueuesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessionQueues.html#GameLift.Paginator.DescribeGameSessionQueues.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegamesessionqueuespaginator)
        """


if TYPE_CHECKING:
    _DescribeGameSessionsPaginatorBase = Paginator[DescribeGameSessionsOutputTypeDef]
else:
    _DescribeGameSessionsPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeGameSessionsPaginator(_DescribeGameSessionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessions.html#GameLift.Paginator.DescribeGameSessions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegamesessionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeGameSessionsInputPaginateTypeDef]
    ) -> PageIterator[DescribeGameSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeGameSessions.html#GameLift.Paginator.DescribeGameSessions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describegamesessionspaginator)
        """


if TYPE_CHECKING:
    _DescribeInstancesPaginatorBase = Paginator[DescribeInstancesOutputTypeDef]
else:
    _DescribeInstancesPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeInstancesPaginator(_DescribeInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeInstances.html#GameLift.Paginator.DescribeInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describeinstancespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInstancesInputPaginateTypeDef]
    ) -> PageIterator[DescribeInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeInstances.html#GameLift.Paginator.DescribeInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describeinstancespaginator)
        """


if TYPE_CHECKING:
    _DescribeMatchmakingConfigurationsPaginatorBase = Paginator[
        DescribeMatchmakingConfigurationsOutputTypeDef
    ]
else:
    _DescribeMatchmakingConfigurationsPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeMatchmakingConfigurationsPaginator(_DescribeMatchmakingConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeMatchmakingConfigurations.html#GameLift.Paginator.DescribeMatchmakingConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describematchmakingconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMatchmakingConfigurationsInputPaginateTypeDef]
    ) -> PageIterator[DescribeMatchmakingConfigurationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeMatchmakingConfigurations.html#GameLift.Paginator.DescribeMatchmakingConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describematchmakingconfigurationspaginator)
        """


if TYPE_CHECKING:
    _DescribeMatchmakingRuleSetsPaginatorBase = Paginator[DescribeMatchmakingRuleSetsOutputTypeDef]
else:
    _DescribeMatchmakingRuleSetsPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeMatchmakingRuleSetsPaginator(_DescribeMatchmakingRuleSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeMatchmakingRuleSets.html#GameLift.Paginator.DescribeMatchmakingRuleSets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describematchmakingrulesetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMatchmakingRuleSetsInputPaginateTypeDef]
    ) -> PageIterator[DescribeMatchmakingRuleSetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeMatchmakingRuleSets.html#GameLift.Paginator.DescribeMatchmakingRuleSets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describematchmakingrulesetspaginator)
        """


if TYPE_CHECKING:
    _DescribePlayerSessionsPaginatorBase = Paginator[DescribePlayerSessionsOutputTypeDef]
else:
    _DescribePlayerSessionsPaginatorBase = Paginator  # type: ignore[assignment]


class DescribePlayerSessionsPaginator(_DescribePlayerSessionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribePlayerSessions.html#GameLift.Paginator.DescribePlayerSessions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describeplayersessionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribePlayerSessionsInputPaginateTypeDef]
    ) -> PageIterator[DescribePlayerSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribePlayerSessions.html#GameLift.Paginator.DescribePlayerSessions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describeplayersessionspaginator)
        """


if TYPE_CHECKING:
    _DescribeScalingPoliciesPaginatorBase = Paginator[DescribeScalingPoliciesOutputTypeDef]
else:
    _DescribeScalingPoliciesPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeScalingPoliciesPaginator(_DescribeScalingPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeScalingPolicies.html#GameLift.Paginator.DescribeScalingPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describescalingpoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeScalingPoliciesInputPaginateTypeDef]
    ) -> PageIterator[DescribeScalingPoliciesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/DescribeScalingPolicies.html#GameLift.Paginator.DescribeScalingPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#describescalingpoliciespaginator)
        """


if TYPE_CHECKING:
    _ListAliasesPaginatorBase = Paginator[ListAliasesOutputTypeDef]
else:
    _ListAliasesPaginatorBase = Paginator  # type: ignore[assignment]


class ListAliasesPaginator(_ListAliasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListAliases.html#GameLift.Paginator.ListAliases)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listaliasespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAliasesInputPaginateTypeDef]
    ) -> PageIterator[ListAliasesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListAliases.html#GameLift.Paginator.ListAliases.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listaliasespaginator)
        """


if TYPE_CHECKING:
    _ListBuildsPaginatorBase = Paginator[ListBuildsOutputTypeDef]
else:
    _ListBuildsPaginatorBase = Paginator  # type: ignore[assignment]


class ListBuildsPaginator(_ListBuildsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListBuilds.html#GameLift.Paginator.ListBuilds)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listbuildspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBuildsInputPaginateTypeDef]
    ) -> PageIterator[ListBuildsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListBuilds.html#GameLift.Paginator.ListBuilds.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listbuildspaginator)
        """


if TYPE_CHECKING:
    _ListComputePaginatorBase = Paginator[ListComputeOutputTypeDef]
else:
    _ListComputePaginatorBase = Paginator  # type: ignore[assignment]


class ListComputePaginator(_ListComputePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListCompute.html#GameLift.Paginator.ListCompute)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listcomputepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListComputeInputPaginateTypeDef]
    ) -> PageIterator[ListComputeOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListCompute.html#GameLift.Paginator.ListCompute.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listcomputepaginator)
        """


if TYPE_CHECKING:
    _ListContainerFleetsPaginatorBase = Paginator[ListContainerFleetsOutputTypeDef]
else:
    _ListContainerFleetsPaginatorBase = Paginator  # type: ignore[assignment]


class ListContainerFleetsPaginator(_ListContainerFleetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListContainerFleets.html#GameLift.Paginator.ListContainerFleets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listcontainerfleetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContainerFleetsInputPaginateTypeDef]
    ) -> PageIterator[ListContainerFleetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListContainerFleets.html#GameLift.Paginator.ListContainerFleets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listcontainerfleetspaginator)
        """


if TYPE_CHECKING:
    _ListContainerGroupDefinitionVersionsPaginatorBase = Paginator[
        ListContainerGroupDefinitionVersionsOutputTypeDef
    ]
else:
    _ListContainerGroupDefinitionVersionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListContainerGroupDefinitionVersionsPaginator(
    _ListContainerGroupDefinitionVersionsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListContainerGroupDefinitionVersions.html#GameLift.Paginator.ListContainerGroupDefinitionVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listcontainergroupdefinitionversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContainerGroupDefinitionVersionsInputPaginateTypeDef]
    ) -> PageIterator[ListContainerGroupDefinitionVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListContainerGroupDefinitionVersions.html#GameLift.Paginator.ListContainerGroupDefinitionVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listcontainergroupdefinitionversionspaginator)
        """


if TYPE_CHECKING:
    _ListContainerGroupDefinitionsPaginatorBase = Paginator[
        ListContainerGroupDefinitionsOutputTypeDef
    ]
else:
    _ListContainerGroupDefinitionsPaginatorBase = Paginator  # type: ignore[assignment]


class ListContainerGroupDefinitionsPaginator(_ListContainerGroupDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListContainerGroupDefinitions.html#GameLift.Paginator.ListContainerGroupDefinitions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listcontainergroupdefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContainerGroupDefinitionsInputPaginateTypeDef]
    ) -> PageIterator[ListContainerGroupDefinitionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListContainerGroupDefinitions.html#GameLift.Paginator.ListContainerGroupDefinitions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listcontainergroupdefinitionspaginator)
        """


if TYPE_CHECKING:
    _ListFleetDeploymentsPaginatorBase = Paginator[ListFleetDeploymentsOutputTypeDef]
else:
    _ListFleetDeploymentsPaginatorBase = Paginator  # type: ignore[assignment]


class ListFleetDeploymentsPaginator(_ListFleetDeploymentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListFleetDeployments.html#GameLift.Paginator.ListFleetDeployments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listfleetdeploymentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFleetDeploymentsInputPaginateTypeDef]
    ) -> PageIterator[ListFleetDeploymentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListFleetDeployments.html#GameLift.Paginator.ListFleetDeployments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listfleetdeploymentspaginator)
        """


if TYPE_CHECKING:
    _ListFleetsPaginatorBase = Paginator[ListFleetsOutputTypeDef]
else:
    _ListFleetsPaginatorBase = Paginator  # type: ignore[assignment]


class ListFleetsPaginator(_ListFleetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListFleets.html#GameLift.Paginator.ListFleets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listfleetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFleetsInputPaginateTypeDef]
    ) -> PageIterator[ListFleetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListFleets.html#GameLift.Paginator.ListFleets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listfleetspaginator)
        """


if TYPE_CHECKING:
    _ListGameServerGroupsPaginatorBase = Paginator[ListGameServerGroupsOutputTypeDef]
else:
    _ListGameServerGroupsPaginatorBase = Paginator  # type: ignore[assignment]


class ListGameServerGroupsPaginator(_ListGameServerGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListGameServerGroups.html#GameLift.Paginator.ListGameServerGroups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listgameservergroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGameServerGroupsInputPaginateTypeDef]
    ) -> PageIterator[ListGameServerGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListGameServerGroups.html#GameLift.Paginator.ListGameServerGroups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listgameservergroupspaginator)
        """


if TYPE_CHECKING:
    _ListGameServersPaginatorBase = Paginator[ListGameServersOutputTypeDef]
else:
    _ListGameServersPaginatorBase = Paginator  # type: ignore[assignment]


class ListGameServersPaginator(_ListGameServersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListGameServers.html#GameLift.Paginator.ListGameServers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listgameserverspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGameServersInputPaginateTypeDef]
    ) -> PageIterator[ListGameServersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListGameServers.html#GameLift.Paginator.ListGameServers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listgameserverspaginator)
        """


if TYPE_CHECKING:
    _ListLocationsPaginatorBase = Paginator[ListLocationsOutputTypeDef]
else:
    _ListLocationsPaginatorBase = Paginator  # type: ignore[assignment]


class ListLocationsPaginator(_ListLocationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListLocations.html#GameLift.Paginator.ListLocations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listlocationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLocationsInputPaginateTypeDef]
    ) -> PageIterator[ListLocationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListLocations.html#GameLift.Paginator.ListLocations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listlocationspaginator)
        """


if TYPE_CHECKING:
    _ListScriptsPaginatorBase = Paginator[ListScriptsOutputTypeDef]
else:
    _ListScriptsPaginatorBase = Paginator  # type: ignore[assignment]


class ListScriptsPaginator(_ListScriptsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListScripts.html#GameLift.Paginator.ListScripts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listscriptspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListScriptsInputPaginateTypeDef]
    ) -> PageIterator[ListScriptsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/ListScripts.html#GameLift.Paginator.ListScripts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#listscriptspaginator)
        """


if TYPE_CHECKING:
    _SearchGameSessionsPaginatorBase = Paginator[SearchGameSessionsOutputTypeDef]
else:
    _SearchGameSessionsPaginatorBase = Paginator  # type: ignore[assignment]


class SearchGameSessionsPaginator(_SearchGameSessionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/SearchGameSessions.html#GameLift.Paginator.SearchGameSessions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#searchgamesessionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchGameSessionsInputPaginateTypeDef]
    ) -> PageIterator[SearchGameSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/paginator/SearchGameSessions.html#GameLift.Paginator.SearchGameSessions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/paginators/#searchgamesessionspaginator)
        """
