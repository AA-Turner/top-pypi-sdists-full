"""
Type annotations for gamelift service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_gamelift.client import GameLiftClient

    session = Session()
    client: GameLiftClient = session.client("gamelift")
    ```
"""

from __future__ import annotations

import sys
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
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
    ListContainerGroupDefinitionsPaginator,
    ListContainerGroupDefinitionVersionsPaginator,
    ListFleetDeploymentsPaginator,
    ListFleetsPaginator,
    ListGameServerGroupsPaginator,
    ListGameServersPaginator,
    ListLocationsPaginator,
    ListScriptsPaginator,
    SearchGameSessionsPaginator,
)
from .type_defs import (
    AcceptMatchInputTypeDef,
    ClaimGameServerInputTypeDef,
    ClaimGameServerOutputTypeDef,
    CreateAliasInputTypeDef,
    CreateAliasOutputTypeDef,
    CreateBuildInputTypeDef,
    CreateBuildOutputTypeDef,
    CreateContainerFleetInputTypeDef,
    CreateContainerFleetOutputTypeDef,
    CreateContainerGroupDefinitionInputTypeDef,
    CreateContainerGroupDefinitionOutputTypeDef,
    CreateFleetInputTypeDef,
    CreateFleetLocationsInputTypeDef,
    CreateFleetLocationsOutputTypeDef,
    CreateFleetOutputTypeDef,
    CreateGameServerGroupInputTypeDef,
    CreateGameServerGroupOutputTypeDef,
    CreateGameSessionInputTypeDef,
    CreateGameSessionOutputTypeDef,
    CreateGameSessionQueueInputTypeDef,
    CreateGameSessionQueueOutputTypeDef,
    CreateLocationInputTypeDef,
    CreateLocationOutputTypeDef,
    CreateMatchmakingConfigurationInputTypeDef,
    CreateMatchmakingConfigurationOutputTypeDef,
    CreateMatchmakingRuleSetInputTypeDef,
    CreateMatchmakingRuleSetOutputTypeDef,
    CreatePlayerSessionInputTypeDef,
    CreatePlayerSessionOutputTypeDef,
    CreatePlayerSessionsInputTypeDef,
    CreatePlayerSessionsOutputTypeDef,
    CreateScriptInputTypeDef,
    CreateScriptOutputTypeDef,
    CreateVpcPeeringAuthorizationInputTypeDef,
    CreateVpcPeeringAuthorizationOutputTypeDef,
    CreateVpcPeeringConnectionInputTypeDef,
    DeleteAliasInputTypeDef,
    DeleteBuildInputTypeDef,
    DeleteContainerFleetInputTypeDef,
    DeleteContainerGroupDefinitionInputTypeDef,
    DeleteFleetInputTypeDef,
    DeleteFleetLocationsInputTypeDef,
    DeleteFleetLocationsOutputTypeDef,
    DeleteGameServerGroupInputTypeDef,
    DeleteGameServerGroupOutputTypeDef,
    DeleteGameSessionQueueInputTypeDef,
    DeleteLocationInputTypeDef,
    DeleteMatchmakingConfigurationInputTypeDef,
    DeleteMatchmakingRuleSetInputTypeDef,
    DeleteScalingPolicyInputTypeDef,
    DeleteScriptInputTypeDef,
    DeleteVpcPeeringAuthorizationInputTypeDef,
    DeleteVpcPeeringConnectionInputTypeDef,
    DeregisterComputeInputTypeDef,
    DeregisterGameServerInputTypeDef,
    DescribeAliasInputTypeDef,
    DescribeAliasOutputTypeDef,
    DescribeBuildInputTypeDef,
    DescribeBuildOutputTypeDef,
    DescribeComputeInputTypeDef,
    DescribeComputeOutputTypeDef,
    DescribeContainerFleetInputTypeDef,
    DescribeContainerFleetOutputTypeDef,
    DescribeContainerGroupDefinitionInputTypeDef,
    DescribeContainerGroupDefinitionOutputTypeDef,
    DescribeEC2InstanceLimitsInputTypeDef,
    DescribeEC2InstanceLimitsOutputTypeDef,
    DescribeFleetAttributesInputTypeDef,
    DescribeFleetAttributesOutputTypeDef,
    DescribeFleetCapacityInputTypeDef,
    DescribeFleetCapacityOutputTypeDef,
    DescribeFleetDeploymentInputTypeDef,
    DescribeFleetDeploymentOutputTypeDef,
    DescribeFleetEventsInputTypeDef,
    DescribeFleetEventsOutputTypeDef,
    DescribeFleetLocationAttributesInputTypeDef,
    DescribeFleetLocationAttributesOutputTypeDef,
    DescribeFleetLocationCapacityInputTypeDef,
    DescribeFleetLocationCapacityOutputTypeDef,
    DescribeFleetLocationUtilizationInputTypeDef,
    DescribeFleetLocationUtilizationOutputTypeDef,
    DescribeFleetPortSettingsInputTypeDef,
    DescribeFleetPortSettingsOutputTypeDef,
    DescribeFleetUtilizationInputTypeDef,
    DescribeFleetUtilizationOutputTypeDef,
    DescribeGameServerGroupInputTypeDef,
    DescribeGameServerGroupOutputTypeDef,
    DescribeGameServerInputTypeDef,
    DescribeGameServerInstancesInputTypeDef,
    DescribeGameServerInstancesOutputTypeDef,
    DescribeGameServerOutputTypeDef,
    DescribeGameSessionDetailsInputTypeDef,
    DescribeGameSessionDetailsOutputTypeDef,
    DescribeGameSessionPlacementInputTypeDef,
    DescribeGameSessionPlacementOutputTypeDef,
    DescribeGameSessionQueuesInputTypeDef,
    DescribeGameSessionQueuesOutputTypeDef,
    DescribeGameSessionsInputTypeDef,
    DescribeGameSessionsOutputTypeDef,
    DescribeInstancesInputTypeDef,
    DescribeInstancesOutputTypeDef,
    DescribeMatchmakingConfigurationsInputTypeDef,
    DescribeMatchmakingConfigurationsOutputTypeDef,
    DescribeMatchmakingInputTypeDef,
    DescribeMatchmakingOutputTypeDef,
    DescribeMatchmakingRuleSetsInputTypeDef,
    DescribeMatchmakingRuleSetsOutputTypeDef,
    DescribePlayerSessionsInputTypeDef,
    DescribePlayerSessionsOutputTypeDef,
    DescribeRuntimeConfigurationInputTypeDef,
    DescribeRuntimeConfigurationOutputTypeDef,
    DescribeScalingPoliciesInputTypeDef,
    DescribeScalingPoliciesOutputTypeDef,
    DescribeScriptInputTypeDef,
    DescribeScriptOutputTypeDef,
    DescribeVpcPeeringAuthorizationsOutputTypeDef,
    DescribeVpcPeeringConnectionsInputTypeDef,
    DescribeVpcPeeringConnectionsOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    GetComputeAccessInputTypeDef,
    GetComputeAccessOutputTypeDef,
    GetComputeAuthTokenInputTypeDef,
    GetComputeAuthTokenOutputTypeDef,
    GetGameSessionLogUrlInputTypeDef,
    GetGameSessionLogUrlOutputTypeDef,
    GetInstanceAccessInputTypeDef,
    GetInstanceAccessOutputTypeDef,
    ListAliasesInputTypeDef,
    ListAliasesOutputTypeDef,
    ListBuildsInputTypeDef,
    ListBuildsOutputTypeDef,
    ListComputeInputTypeDef,
    ListComputeOutputTypeDef,
    ListContainerFleetsInputTypeDef,
    ListContainerFleetsOutputTypeDef,
    ListContainerGroupDefinitionsInputTypeDef,
    ListContainerGroupDefinitionsOutputTypeDef,
    ListContainerGroupDefinitionVersionsInputTypeDef,
    ListContainerGroupDefinitionVersionsOutputTypeDef,
    ListFleetDeploymentsInputTypeDef,
    ListFleetDeploymentsOutputTypeDef,
    ListFleetsInputTypeDef,
    ListFleetsOutputTypeDef,
    ListGameServerGroupsInputTypeDef,
    ListGameServerGroupsOutputTypeDef,
    ListGameServersInputTypeDef,
    ListGameServersOutputTypeDef,
    ListLocationsInputTypeDef,
    ListLocationsOutputTypeDef,
    ListScriptsInputTypeDef,
    ListScriptsOutputTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutScalingPolicyInputTypeDef,
    PutScalingPolicyOutputTypeDef,
    RegisterComputeInputTypeDef,
    RegisterComputeOutputTypeDef,
    RegisterGameServerInputTypeDef,
    RegisterGameServerOutputTypeDef,
    RequestUploadCredentialsInputTypeDef,
    RequestUploadCredentialsOutputTypeDef,
    ResolveAliasInputTypeDef,
    ResolveAliasOutputTypeDef,
    ResumeGameServerGroupInputTypeDef,
    ResumeGameServerGroupOutputTypeDef,
    SearchGameSessionsInputTypeDef,
    SearchGameSessionsOutputTypeDef,
    StartFleetActionsInputTypeDef,
    StartFleetActionsOutputTypeDef,
    StartGameSessionPlacementInputTypeDef,
    StartGameSessionPlacementOutputTypeDef,
    StartMatchBackfillInputTypeDef,
    StartMatchBackfillOutputTypeDef,
    StartMatchmakingInputTypeDef,
    StartMatchmakingOutputTypeDef,
    StopFleetActionsInputTypeDef,
    StopFleetActionsOutputTypeDef,
    StopGameSessionPlacementInputTypeDef,
    StopGameSessionPlacementOutputTypeDef,
    StopMatchmakingInputTypeDef,
    SuspendGameServerGroupInputTypeDef,
    SuspendGameServerGroupOutputTypeDef,
    TagResourceRequestTypeDef,
    TerminateGameSessionInputTypeDef,
    TerminateGameSessionOutputTypeDef,
    UntagResourceRequestTypeDef,
    UpdateAliasInputTypeDef,
    UpdateAliasOutputTypeDef,
    UpdateBuildInputTypeDef,
    UpdateBuildOutputTypeDef,
    UpdateContainerFleetInputTypeDef,
    UpdateContainerFleetOutputTypeDef,
    UpdateContainerGroupDefinitionInputTypeDef,
    UpdateContainerGroupDefinitionOutputTypeDef,
    UpdateFleetAttributesInputTypeDef,
    UpdateFleetAttributesOutputTypeDef,
    UpdateFleetCapacityInputTypeDef,
    UpdateFleetCapacityOutputTypeDef,
    UpdateFleetPortSettingsInputTypeDef,
    UpdateFleetPortSettingsOutputTypeDef,
    UpdateGameServerGroupInputTypeDef,
    UpdateGameServerGroupOutputTypeDef,
    UpdateGameServerInputTypeDef,
    UpdateGameServerOutputTypeDef,
    UpdateGameSessionInputTypeDef,
    UpdateGameSessionOutputTypeDef,
    UpdateGameSessionQueueInputTypeDef,
    UpdateGameSessionQueueOutputTypeDef,
    UpdateMatchmakingConfigurationInputTypeDef,
    UpdateMatchmakingConfigurationOutputTypeDef,
    UpdateRuntimeConfigurationInputTypeDef,
    UpdateRuntimeConfigurationOutputTypeDef,
    UpdateScriptInputTypeDef,
    UpdateScriptOutputTypeDef,
    ValidateMatchmakingRuleSetInputTypeDef,
    ValidateMatchmakingRuleSetOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("GameLiftClient",)

class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    FleetCapacityExceededException: Type[BotocoreClientError]
    GameSessionFullException: Type[BotocoreClientError]
    IdempotentParameterMismatchException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidFleetStatusException: Type[BotocoreClientError]
    InvalidGameSessionStatusException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    NotReadyException: Type[BotocoreClientError]
    OutOfCapacityException: Type[BotocoreClientError]
    TaggingFailedException: Type[BotocoreClientError]
    TerminalRoutingStrategyException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]
    UnsupportedRegionException: Type[BotocoreClientError]

class GameLiftClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GameLiftClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#generate_presigned_url)
        """

    def accept_match(self, **kwargs: Unpack[AcceptMatchInputTypeDef]) -> Dict[str, Any]:
        """
        Registers a player's acceptance or rejection of a proposed FlexMatch match.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/accept_match.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#accept_match)
        """

    def claim_game_server(
        self, **kwargs: Unpack[ClaimGameServerInputTypeDef]
    ) -> ClaimGameServerOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/claim_game_server.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#claim_game_server)
        """

    def create_alias(self, **kwargs: Unpack[CreateAliasInputTypeDef]) -> CreateAliasOutputTypeDef:
        """
        Creates an alias for a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_alias.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_alias)
        """

    def create_build(self, **kwargs: Unpack[CreateBuildInputTypeDef]) -> CreateBuildOutputTypeDef:
        """
        Creates a new Amazon GameLift build resource for your game server binary files.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_build.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_build)
        """

    def create_container_fleet(
        self, **kwargs: Unpack[CreateContainerFleetInputTypeDef]
    ) -> CreateContainerFleetOutputTypeDef:
        """
        Creates a managed fleet of Amazon Elastic Compute Cloud (Amazon EC2) instances
        to host your containerized game servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_container_fleet.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_container_fleet)
        """

    def create_container_group_definition(
        self, **kwargs: Unpack[CreateContainerGroupDefinitionInputTypeDef]
    ) -> CreateContainerGroupDefinitionOutputTypeDef:
        """
        Creates a <code>ContainerGroupDefinition</code> that describes a set of
        containers for hosting your game server with Amazon GameLift managed containers
        hosting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_container_group_definition.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_container_group_definition)
        """

    def create_fleet(self, **kwargs: Unpack[CreateFleetInputTypeDef]) -> CreateFleetOutputTypeDef:
        """
        Creates a fleet of compute resources to host your game servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_fleet.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_fleet)
        """

    def create_fleet_locations(
        self, **kwargs: Unpack[CreateFleetLocationsInputTypeDef]
    ) -> CreateFleetLocationsOutputTypeDef:
        """
        Adds remote locations to an EC2 and begins populating the new locations with
        instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_fleet_locations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_fleet_locations)
        """

    def create_game_server_group(
        self, **kwargs: Unpack[CreateGameServerGroupInputTypeDef]
    ) -> CreateGameServerGroupOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_game_server_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_game_server_group)
        """

    def create_game_session(
        self, **kwargs: Unpack[CreateGameSessionInputTypeDef]
    ) -> CreateGameSessionOutputTypeDef:
        """
        Creates a multiplayer game session for players in a specific fleet location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_game_session.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_game_session)
        """

    def create_game_session_queue(
        self, **kwargs: Unpack[CreateGameSessionQueueInputTypeDef]
    ) -> CreateGameSessionQueueOutputTypeDef:
        """
        Creates a placement queue that processes requests for new game sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_game_session_queue.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_game_session_queue)
        """

    def create_location(
        self, **kwargs: Unpack[CreateLocationInputTypeDef]
    ) -> CreateLocationOutputTypeDef:
        """
        Creates a custom location for use in an Anywhere fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_location.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_location)
        """

    def create_matchmaking_configuration(
        self, **kwargs: Unpack[CreateMatchmakingConfigurationInputTypeDef]
    ) -> CreateMatchmakingConfigurationOutputTypeDef:
        """
        Defines a new matchmaking configuration for use with FlexMatch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_matchmaking_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_matchmaking_configuration)
        """

    def create_matchmaking_rule_set(
        self, **kwargs: Unpack[CreateMatchmakingRuleSetInputTypeDef]
    ) -> CreateMatchmakingRuleSetOutputTypeDef:
        """
        Creates a new rule set for FlexMatch matchmaking.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_matchmaking_rule_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_matchmaking_rule_set)
        """

    def create_player_session(
        self, **kwargs: Unpack[CreatePlayerSessionInputTypeDef]
    ) -> CreatePlayerSessionOutputTypeDef:
        """
        Reserves an open player slot in a game session for a player.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_player_session.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_player_session)
        """

    def create_player_sessions(
        self, **kwargs: Unpack[CreatePlayerSessionsInputTypeDef]
    ) -> CreatePlayerSessionsOutputTypeDef:
        """
        Reserves open slots in a game session for a group of players.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_player_sessions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_player_sessions)
        """

    def create_script(
        self, **kwargs: Unpack[CreateScriptInputTypeDef]
    ) -> CreateScriptOutputTypeDef:
        """
        Creates a new script record for your Amazon GameLift Realtime script.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_script.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_script)
        """

    def create_vpc_peering_authorization(
        self, **kwargs: Unpack[CreateVpcPeeringAuthorizationInputTypeDef]
    ) -> CreateVpcPeeringAuthorizationOutputTypeDef:
        """
        Requests authorization to create or delete a peer connection between the VPC
        for your Amazon GameLift fleet and a virtual private cloud (VPC) in your Amazon
        Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_vpc_peering_authorization.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_vpc_peering_authorization)
        """

    def create_vpc_peering_connection(
        self, **kwargs: Unpack[CreateVpcPeeringConnectionInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Establishes a VPC peering connection between a virtual private cloud (VPC) in
        an Amazon Web Services account with the VPC for your Amazon GameLift fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_vpc_peering_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#create_vpc_peering_connection)
        """

    def delete_alias(
        self, **kwargs: Unpack[DeleteAliasInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_alias.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_alias)
        """

    def delete_build(
        self, **kwargs: Unpack[DeleteBuildInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_build.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_build)
        """

    def delete_container_fleet(
        self, **kwargs: Unpack[DeleteContainerFleetInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes all resources and information related to a container fleet and shuts
        down currently running fleet instances, including those in remote locations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_container_fleet.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_container_fleet)
        """

    def delete_container_group_definition(
        self, **kwargs: Unpack[DeleteContainerGroupDefinitionInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a container group definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_container_group_definition.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_container_group_definition)
        """

    def delete_fleet(
        self, **kwargs: Unpack[DeleteFleetInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes all resources and information related to a fleet and shuts down any
        currently running fleet instances, including those in remote locations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_fleet.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_fleet)
        """

    def delete_fleet_locations(
        self, **kwargs: Unpack[DeleteFleetLocationsInputTypeDef]
    ) -> DeleteFleetLocationsOutputTypeDef:
        """
        Removes locations from a multi-location fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_fleet_locations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_fleet_locations)
        """

    def delete_game_server_group(
        self, **kwargs: Unpack[DeleteGameServerGroupInputTypeDef]
    ) -> DeleteGameServerGroupOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_game_server_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_game_server_group)
        """

    def delete_game_session_queue(
        self, **kwargs: Unpack[DeleteGameSessionQueueInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a game session queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_game_session_queue.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_game_session_queue)
        """

    def delete_location(self, **kwargs: Unpack[DeleteLocationInputTypeDef]) -> Dict[str, Any]:
        """
        Deletes a custom location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_location.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_location)
        """

    def delete_matchmaking_configuration(
        self, **kwargs: Unpack[DeleteMatchmakingConfigurationInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Permanently removes a FlexMatch matchmaking configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_matchmaking_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_matchmaking_configuration)
        """

    def delete_matchmaking_rule_set(
        self, **kwargs: Unpack[DeleteMatchmakingRuleSetInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an existing matchmaking rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_matchmaking_rule_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_matchmaking_rule_set)
        """

    def delete_scaling_policy(
        self, **kwargs: Unpack[DeleteScalingPolicyInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a fleet scaling policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_scaling_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_scaling_policy)
        """

    def delete_script(
        self, **kwargs: Unpack[DeleteScriptInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Realtime script.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_script.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_script)
        """

    def delete_vpc_peering_authorization(
        self, **kwargs: Unpack[DeleteVpcPeeringAuthorizationInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels a pending VPC peering authorization for the specified VPC.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_vpc_peering_authorization.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_vpc_peering_authorization)
        """

    def delete_vpc_peering_connection(
        self, **kwargs: Unpack[DeleteVpcPeeringConnectionInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a VPC peering connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_vpc_peering_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#delete_vpc_peering_connection)
        """

    def deregister_compute(self, **kwargs: Unpack[DeregisterComputeInputTypeDef]) -> Dict[str, Any]:
        """
        Removes a compute resource from an Anywhere fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/deregister_compute.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#deregister_compute)
        """

    def deregister_game_server(
        self, **kwargs: Unpack[DeregisterGameServerInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/deregister_game_server.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#deregister_game_server)
        """

    def describe_alias(
        self, **kwargs: Unpack[DescribeAliasInputTypeDef]
    ) -> DescribeAliasOutputTypeDef:
        """
        Retrieves properties for an alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_alias.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_alias)
        """

    def describe_build(
        self, **kwargs: Unpack[DescribeBuildInputTypeDef]
    ) -> DescribeBuildOutputTypeDef:
        """
        Retrieves properties for a custom game build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_build.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_build)
        """

    def describe_compute(
        self, **kwargs: Unpack[DescribeComputeInputTypeDef]
    ) -> DescribeComputeOutputTypeDef:
        """
        Retrieves properties for a specific compute resource in an Amazon GameLift
        fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_compute.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_compute)
        """

    def describe_container_fleet(
        self, **kwargs: Unpack[DescribeContainerFleetInputTypeDef]
    ) -> DescribeContainerFleetOutputTypeDef:
        """
        Retrieves the properties for a container fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_container_fleet.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_container_fleet)
        """

    def describe_container_group_definition(
        self, **kwargs: Unpack[DescribeContainerGroupDefinitionInputTypeDef]
    ) -> DescribeContainerGroupDefinitionOutputTypeDef:
        """
        Retrieves the properties of a container group definition, including all
        container definitions in the group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_container_group_definition.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_container_group_definition)
        """

    def describe_ec2_instance_limits(
        self, **kwargs: Unpack[DescribeEC2InstanceLimitsInputTypeDef]
    ) -> DescribeEC2InstanceLimitsOutputTypeDef:
        """
        Retrieves the instance limits and current utilization for an Amazon Web
        Services Region or location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_ec2_instance_limits.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_ec2_instance_limits)
        """

    def describe_fleet_attributes(
        self, **kwargs: Unpack[DescribeFleetAttributesInputTypeDef]
    ) -> DescribeFleetAttributesOutputTypeDef:
        """
        Retrieves core fleet-wide properties for fleets in an Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_fleet_attributes)
        """

    def describe_fleet_capacity(
        self, **kwargs: Unpack[DescribeFleetCapacityInputTypeDef]
    ) -> DescribeFleetCapacityOutputTypeDef:
        """
        Retrieves the resource capacity settings for one or more fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_capacity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_fleet_capacity)
        """

    def describe_fleet_deployment(
        self, **kwargs: Unpack[DescribeFleetDeploymentInputTypeDef]
    ) -> DescribeFleetDeploymentOutputTypeDef:
        """
        Retrieves information about a managed container fleet deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_deployment.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_fleet_deployment)
        """

    def describe_fleet_events(
        self, **kwargs: Unpack[DescribeFleetEventsInputTypeDef]
    ) -> DescribeFleetEventsOutputTypeDef:
        """
        Retrieves entries from a fleet's event log.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_events.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_fleet_events)
        """

    def describe_fleet_location_attributes(
        self, **kwargs: Unpack[DescribeFleetLocationAttributesInputTypeDef]
    ) -> DescribeFleetLocationAttributesOutputTypeDef:
        """
        Retrieves information on a fleet's remote locations, including life-cycle
        status and any suspended fleet activity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_location_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_fleet_location_attributes)
        """

    def describe_fleet_location_capacity(
        self, **kwargs: Unpack[DescribeFleetLocationCapacityInputTypeDef]
    ) -> DescribeFleetLocationCapacityOutputTypeDef:
        """
        Retrieves the resource capacity settings for a fleet location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_location_capacity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_fleet_location_capacity)
        """

    def describe_fleet_location_utilization(
        self, **kwargs: Unpack[DescribeFleetLocationUtilizationInputTypeDef]
    ) -> DescribeFleetLocationUtilizationOutputTypeDef:
        """
        Retrieves current usage data for a fleet location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_location_utilization.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_fleet_location_utilization)
        """

    def describe_fleet_port_settings(
        self, **kwargs: Unpack[DescribeFleetPortSettingsInputTypeDef]
    ) -> DescribeFleetPortSettingsOutputTypeDef:
        """
        Retrieves a fleet's inbound connection permissions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_port_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_fleet_port_settings)
        """

    def describe_fleet_utilization(
        self, **kwargs: Unpack[DescribeFleetUtilizationInputTypeDef]
    ) -> DescribeFleetUtilizationOutputTypeDef:
        """
        Retrieves utilization statistics for one or more fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_utilization.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_fleet_utilization)
        """

    def describe_game_server(
        self, **kwargs: Unpack[DescribeGameServerInputTypeDef]
    ) -> DescribeGameServerOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_game_server.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_game_server)
        """

    def describe_game_server_group(
        self, **kwargs: Unpack[DescribeGameServerGroupInputTypeDef]
    ) -> DescribeGameServerGroupOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_game_server_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_game_server_group)
        """

    def describe_game_server_instances(
        self, **kwargs: Unpack[DescribeGameServerInstancesInputTypeDef]
    ) -> DescribeGameServerInstancesOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_game_server_instances.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_game_server_instances)
        """

    def describe_game_session_details(
        self, **kwargs: Unpack[DescribeGameSessionDetailsInputTypeDef]
    ) -> DescribeGameSessionDetailsOutputTypeDef:
        """
        Retrieves additional game session properties, including the game session
        protection policy in force, a set of one or more game sessions in a specific
        fleet location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_game_session_details.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_game_session_details)
        """

    def describe_game_session_placement(
        self, **kwargs: Unpack[DescribeGameSessionPlacementInputTypeDef]
    ) -> DescribeGameSessionPlacementOutputTypeDef:
        """
        Retrieves information, including current status, about a game session placement
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_game_session_placement.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_game_session_placement)
        """

    def describe_game_session_queues(
        self, **kwargs: Unpack[DescribeGameSessionQueuesInputTypeDef]
    ) -> DescribeGameSessionQueuesOutputTypeDef:
        """
        Retrieves the properties for one or more game session queues.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_game_session_queues.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_game_session_queues)
        """

    def describe_game_sessions(
        self, **kwargs: Unpack[DescribeGameSessionsInputTypeDef]
    ) -> DescribeGameSessionsOutputTypeDef:
        """
        Retrieves a set of one or more game sessions in a specific fleet location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_game_sessions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_game_sessions)
        """

    def describe_instances(
        self, **kwargs: Unpack[DescribeInstancesInputTypeDef]
    ) -> DescribeInstancesOutputTypeDef:
        """
        Retrieves information about the EC2 instances in an Amazon GameLift managed
        fleet, including instance ID, connection data, and status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_instances.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_instances)
        """

    def describe_matchmaking(
        self, **kwargs: Unpack[DescribeMatchmakingInputTypeDef]
    ) -> DescribeMatchmakingOutputTypeDef:
        """
        Retrieves one or more matchmaking tickets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_matchmaking.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_matchmaking)
        """

    def describe_matchmaking_configurations(
        self, **kwargs: Unpack[DescribeMatchmakingConfigurationsInputTypeDef]
    ) -> DescribeMatchmakingConfigurationsOutputTypeDef:
        """
        Retrieves the details of FlexMatch matchmaking configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_matchmaking_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_matchmaking_configurations)
        """

    def describe_matchmaking_rule_sets(
        self, **kwargs: Unpack[DescribeMatchmakingRuleSetsInputTypeDef]
    ) -> DescribeMatchmakingRuleSetsOutputTypeDef:
        """
        Retrieves the details for FlexMatch matchmaking rule sets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_matchmaking_rule_sets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_matchmaking_rule_sets)
        """

    def describe_player_sessions(
        self, **kwargs: Unpack[DescribePlayerSessionsInputTypeDef]
    ) -> DescribePlayerSessionsOutputTypeDef:
        """
        Retrieves properties for one or more player sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_player_sessions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_player_sessions)
        """

    def describe_runtime_configuration(
        self, **kwargs: Unpack[DescribeRuntimeConfigurationInputTypeDef]
    ) -> DescribeRuntimeConfigurationOutputTypeDef:
        """
        Retrieves a fleet's runtime configuration settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_runtime_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_runtime_configuration)
        """

    def describe_scaling_policies(
        self, **kwargs: Unpack[DescribeScalingPoliciesInputTypeDef]
    ) -> DescribeScalingPoliciesOutputTypeDef:
        """
        Retrieves all scaling policies applied to a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_scaling_policies.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_scaling_policies)
        """

    def describe_script(
        self, **kwargs: Unpack[DescribeScriptInputTypeDef]
    ) -> DescribeScriptOutputTypeDef:
        """
        Retrieves properties for a Realtime script.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_script.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_script)
        """

    def describe_vpc_peering_authorizations(self) -> DescribeVpcPeeringAuthorizationsOutputTypeDef:
        """
        Retrieves valid VPC peering authorizations that are pending for the Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_vpc_peering_authorizations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_vpc_peering_authorizations)
        """

    def describe_vpc_peering_connections(
        self, **kwargs: Unpack[DescribeVpcPeeringConnectionsInputTypeDef]
    ) -> DescribeVpcPeeringConnectionsOutputTypeDef:
        """
        Retrieves information on VPC peering connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_vpc_peering_connections.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#describe_vpc_peering_connections)
        """

    def get_compute_access(
        self, **kwargs: Unpack[GetComputeAccessInputTypeDef]
    ) -> GetComputeAccessOutputTypeDef:
        """
        Requests authorization to remotely connect to a hosting resource in a Amazon
        GameLift managed fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_compute_access.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_compute_access)
        """

    def get_compute_auth_token(
        self, **kwargs: Unpack[GetComputeAuthTokenInputTypeDef]
    ) -> GetComputeAuthTokenOutputTypeDef:
        """
        Requests an authentication token from Amazon GameLift for a compute resource in
        an Amazon GameLift fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_compute_auth_token.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_compute_auth_token)
        """

    def get_game_session_log_url(
        self, **kwargs: Unpack[GetGameSessionLogUrlInputTypeDef]
    ) -> GetGameSessionLogUrlOutputTypeDef:
        """
        Retrieves the location of stored game session logs for a specified game session
        on Amazon GameLift managed fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_game_session_log_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_game_session_log_url)
        """

    def get_instance_access(
        self, **kwargs: Unpack[GetInstanceAccessInputTypeDef]
    ) -> GetInstanceAccessOutputTypeDef:
        """
        Requests authorization to remotely connect to an instance in an Amazon GameLift
        managed fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_instance_access.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_instance_access)
        """

    def list_aliases(self, **kwargs: Unpack[ListAliasesInputTypeDef]) -> ListAliasesOutputTypeDef:
        """
        Retrieves all aliases for this Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_aliases.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#list_aliases)
        """

    def list_builds(self, **kwargs: Unpack[ListBuildsInputTypeDef]) -> ListBuildsOutputTypeDef:
        """
        Retrieves build resources for all builds associated with the Amazon Web
        Services account in use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_builds.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#list_builds)
        """

    def list_compute(self, **kwargs: Unpack[ListComputeInputTypeDef]) -> ListComputeOutputTypeDef:
        """
        Retrieves information on the compute resources in an Amazon GameLift fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_compute.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#list_compute)
        """

    def list_container_fleets(
        self, **kwargs: Unpack[ListContainerFleetsInputTypeDef]
    ) -> ListContainerFleetsOutputTypeDef:
        """
        Retrieves a collection of container fleet resources in an Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_container_fleets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#list_container_fleets)
        """

    def list_container_group_definition_versions(
        self, **kwargs: Unpack[ListContainerGroupDefinitionVersionsInputTypeDef]
    ) -> ListContainerGroupDefinitionVersionsOutputTypeDef:
        """
        Retrieves all versions of a container group definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_container_group_definition_versions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#list_container_group_definition_versions)
        """

    def list_container_group_definitions(
        self, **kwargs: Unpack[ListContainerGroupDefinitionsInputTypeDef]
    ) -> ListContainerGroupDefinitionsOutputTypeDef:
        """
        Retrieves container group definitions for the Amazon Web Services account and
        Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_container_group_definitions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#list_container_group_definitions)
        """

    def list_fleet_deployments(
        self, **kwargs: Unpack[ListFleetDeploymentsInputTypeDef]
    ) -> ListFleetDeploymentsOutputTypeDef:
        """
        Retrieves a collection of container fleet deployments in an Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_fleet_deployments.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#list_fleet_deployments)
        """

    def list_fleets(self, **kwargs: Unpack[ListFleetsInputTypeDef]) -> ListFleetsOutputTypeDef:
        """
        Retrieves a collection of fleet resources in an Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_fleets.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#list_fleets)
        """

    def list_game_server_groups(
        self, **kwargs: Unpack[ListGameServerGroupsInputTypeDef]
    ) -> ListGameServerGroupsOutputTypeDef:
        """
        Lists a game server groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_game_server_groups.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#list_game_server_groups)
        """

    def list_game_servers(
        self, **kwargs: Unpack[ListGameServersInputTypeDef]
    ) -> ListGameServersOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_game_servers.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#list_game_servers)
        """

    def list_locations(
        self, **kwargs: Unpack[ListLocationsInputTypeDef]
    ) -> ListLocationsOutputTypeDef:
        """
        Lists all custom and Amazon Web Services locations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_locations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#list_locations)
        """

    def list_scripts(self, **kwargs: Unpack[ListScriptsInputTypeDef]) -> ListScriptsOutputTypeDef:
        """
        Retrieves script records for all Realtime scripts that are associated with the
        Amazon Web Services account in use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_scripts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#list_scripts)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves all tags assigned to a Amazon GameLift resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#list_tags_for_resource)
        """

    def put_scaling_policy(
        self, **kwargs: Unpack[PutScalingPolicyInputTypeDef]
    ) -> PutScalingPolicyOutputTypeDef:
        """
        Creates or updates a scaling policy for a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/put_scaling_policy.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#put_scaling_policy)
        """

    def register_compute(
        self, **kwargs: Unpack[RegisterComputeInputTypeDef]
    ) -> RegisterComputeOutputTypeDef:
        """
        Registers a compute resource in an Amazon GameLift Anywhere fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/register_compute.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#register_compute)
        """

    def register_game_server(
        self, **kwargs: Unpack[RegisterGameServerInputTypeDef]
    ) -> RegisterGameServerOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/register_game_server.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#register_game_server)
        """

    def request_upload_credentials(
        self, **kwargs: Unpack[RequestUploadCredentialsInputTypeDef]
    ) -> RequestUploadCredentialsOutputTypeDef:
        """
        Retrieves a fresh set of credentials for use when uploading a new set of game
        build files to Amazon GameLift's Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/request_upload_credentials.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#request_upload_credentials)
        """

    def resolve_alias(
        self, **kwargs: Unpack[ResolveAliasInputTypeDef]
    ) -> ResolveAliasOutputTypeDef:
        """
        Attempts to retrieve a fleet ID that is associated with an alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/resolve_alias.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#resolve_alias)
        """

    def resume_game_server_group(
        self, **kwargs: Unpack[ResumeGameServerGroupInputTypeDef]
    ) -> ResumeGameServerGroupOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/resume_game_server_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#resume_game_server_group)
        """

    def search_game_sessions(
        self, **kwargs: Unpack[SearchGameSessionsInputTypeDef]
    ) -> SearchGameSessionsOutputTypeDef:
        """
        Retrieves all active game sessions that match a set of search criteria and
        sorts them into a specified order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/search_game_sessions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#search_game_sessions)
        """

    def start_fleet_actions(
        self, **kwargs: Unpack[StartFleetActionsInputTypeDef]
    ) -> StartFleetActionsOutputTypeDef:
        """
        Resumes certain types of activity on fleet instances that were suspended with
        <a
        href="https://docs.aws.amazon.com/gamelift/latest/apireference/API_StopFleetActions.html">StopFleetActions</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/start_fleet_actions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#start_fleet_actions)
        """

    def start_game_session_placement(
        self, **kwargs: Unpack[StartGameSessionPlacementInputTypeDef]
    ) -> StartGameSessionPlacementOutputTypeDef:
        """
        Makes a request to start a new game session using a game session queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/start_game_session_placement.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#start_game_session_placement)
        """

    def start_match_backfill(
        self, **kwargs: Unpack[StartMatchBackfillInputTypeDef]
    ) -> StartMatchBackfillOutputTypeDef:
        """
        Finds new players to fill open slots in currently running game sessions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/start_match_backfill.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#start_match_backfill)
        """

    def start_matchmaking(
        self, **kwargs: Unpack[StartMatchmakingInputTypeDef]
    ) -> StartMatchmakingOutputTypeDef:
        """
        Uses FlexMatch to create a game match for a group of players based on custom
        matchmaking rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/start_matchmaking.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#start_matchmaking)
        """

    def stop_fleet_actions(
        self, **kwargs: Unpack[StopFleetActionsInputTypeDef]
    ) -> StopFleetActionsOutputTypeDef:
        """
        Suspends certain types of activity in a fleet location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/stop_fleet_actions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#stop_fleet_actions)
        """

    def stop_game_session_placement(
        self, **kwargs: Unpack[StopGameSessionPlacementInputTypeDef]
    ) -> StopGameSessionPlacementOutputTypeDef:
        """
        Cancels a game session placement that's in <code>PENDING</code> status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/stop_game_session_placement.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#stop_game_session_placement)
        """

    def stop_matchmaking(self, **kwargs: Unpack[StopMatchmakingInputTypeDef]) -> Dict[str, Any]:
        """
        Cancels a matchmaking ticket or match backfill ticket that is currently being
        processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/stop_matchmaking.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#stop_matchmaking)
        """

    def suspend_game_server_group(
        self, **kwargs: Unpack[SuspendGameServerGroupInputTypeDef]
    ) -> SuspendGameServerGroupOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/suspend_game_server_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#suspend_game_server_group)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Assigns a tag to an Amazon GameLift resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#tag_resource)
        """

    def terminate_game_session(
        self, **kwargs: Unpack[TerminateGameSessionInputTypeDef]
    ) -> TerminateGameSessionOutputTypeDef:
        """
        Ends a game session that's currently in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/terminate_game_session.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#terminate_game_session)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes a tag assigned to a Amazon GameLift resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#untag_resource)
        """

    def update_alias(self, **kwargs: Unpack[UpdateAliasInputTypeDef]) -> UpdateAliasOutputTypeDef:
        """
        Updates properties for an alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_alias.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_alias)
        """

    def update_build(self, **kwargs: Unpack[UpdateBuildInputTypeDef]) -> UpdateBuildOutputTypeDef:
        """
        Updates metadata in a build resource, including the build name and version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_build.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_build)
        """

    def update_container_fleet(
        self, **kwargs: Unpack[UpdateContainerFleetInputTypeDef]
    ) -> UpdateContainerFleetOutputTypeDef:
        """
        Updates the properties of a managed container fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_container_fleet.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_container_fleet)
        """

    def update_container_group_definition(
        self, **kwargs: Unpack[UpdateContainerGroupDefinitionInputTypeDef]
    ) -> UpdateContainerGroupDefinitionOutputTypeDef:
        """
        Updates properties in an existing container group definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_container_group_definition.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_container_group_definition)
        """

    def update_fleet_attributes(
        self, **kwargs: Unpack[UpdateFleetAttributesInputTypeDef]
    ) -> UpdateFleetAttributesOutputTypeDef:
        """
        Updates a fleet's mutable attributes, such as game session protection and
        resource creation limits.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_fleet_attributes.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_fleet_attributes)
        """

    def update_fleet_capacity(
        self, **kwargs: Unpack[UpdateFleetCapacityInputTypeDef]
    ) -> UpdateFleetCapacityOutputTypeDef:
        """
        Updates capacity settings for a managed EC2 fleet or managed container fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_fleet_capacity.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_fleet_capacity)
        """

    def update_fleet_port_settings(
        self, **kwargs: Unpack[UpdateFleetPortSettingsInputTypeDef]
    ) -> UpdateFleetPortSettingsOutputTypeDef:
        """
        Updates permissions that allow inbound traffic to connect to game sessions in
        the fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_fleet_port_settings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_fleet_port_settings)
        """

    def update_game_server(
        self, **kwargs: Unpack[UpdateGameServerInputTypeDef]
    ) -> UpdateGameServerOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_game_server.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_game_server)
        """

    def update_game_server_group(
        self, **kwargs: Unpack[UpdateGameServerGroupInputTypeDef]
    ) -> UpdateGameServerGroupOutputTypeDef:
        """
        <b>This operation is used with the Amazon GameLift FleetIQ solution and game
        server groups.</b>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_game_server_group.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_game_server_group)
        """

    def update_game_session(
        self, **kwargs: Unpack[UpdateGameSessionInputTypeDef]
    ) -> UpdateGameSessionOutputTypeDef:
        """
        Updates the mutable properties of a game session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_game_session.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_game_session)
        """

    def update_game_session_queue(
        self, **kwargs: Unpack[UpdateGameSessionQueueInputTypeDef]
    ) -> UpdateGameSessionQueueOutputTypeDef:
        """
        Updates the configuration of a game session queue, which determines how the
        queue processes new game session requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_game_session_queue.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_game_session_queue)
        """

    def update_matchmaking_configuration(
        self, **kwargs: Unpack[UpdateMatchmakingConfigurationInputTypeDef]
    ) -> UpdateMatchmakingConfigurationOutputTypeDef:
        """
        Updates settings for a FlexMatch matchmaking configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_matchmaking_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_matchmaking_configuration)
        """

    def update_runtime_configuration(
        self, **kwargs: Unpack[UpdateRuntimeConfigurationInputTypeDef]
    ) -> UpdateRuntimeConfigurationOutputTypeDef:
        """
        Updates the runtime configuration for the specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_runtime_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_runtime_configuration)
        """

    def update_script(
        self, **kwargs: Unpack[UpdateScriptInputTypeDef]
    ) -> UpdateScriptOutputTypeDef:
        """
        Updates Realtime script metadata and content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_script.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#update_script)
        """

    def validate_matchmaking_rule_set(
        self, **kwargs: Unpack[ValidateMatchmakingRuleSetInputTypeDef]
    ) -> ValidateMatchmakingRuleSetOutputTypeDef:
        """
        Validates the syntax of a matchmaking rule or rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/validate_matchmaking_rule_set.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#validate_matchmaking_rule_set)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_fleet_attributes"]
    ) -> DescribeFleetAttributesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_fleet_capacity"]
    ) -> DescribeFleetCapacityPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_fleet_events"]
    ) -> DescribeFleetEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_fleet_utilization"]
    ) -> DescribeFleetUtilizationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_game_server_instances"]
    ) -> DescribeGameServerInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_game_session_details"]
    ) -> DescribeGameSessionDetailsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_game_session_queues"]
    ) -> DescribeGameSessionQueuesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_game_sessions"]
    ) -> DescribeGameSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_instances"]
    ) -> DescribeInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_matchmaking_configurations"]
    ) -> DescribeMatchmakingConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_matchmaking_rule_sets"]
    ) -> DescribeMatchmakingRuleSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_player_sessions"]
    ) -> DescribePlayerSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_scaling_policies"]
    ) -> DescribeScalingPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_aliases"]
    ) -> ListAliasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_builds"]
    ) -> ListBuildsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_compute"]
    ) -> ListComputePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_container_fleets"]
    ) -> ListContainerFleetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_container_group_definition_versions"]
    ) -> ListContainerGroupDefinitionVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_container_group_definitions"]
    ) -> ListContainerGroupDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_fleet_deployments"]
    ) -> ListFleetDeploymentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_fleets"]
    ) -> ListFleetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_game_server_groups"]
    ) -> ListGameServerGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_game_servers"]
    ) -> ListGameServersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_locations"]
    ) -> ListLocationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_scripts"]
    ) -> ListScriptsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_game_sessions"]
    ) -> SearchGameSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_gamelift/client/#get_paginator)
        """
