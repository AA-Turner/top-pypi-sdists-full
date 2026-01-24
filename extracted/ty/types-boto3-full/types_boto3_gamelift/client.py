"""
Type annotations for gamelift service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_gamelift.client import GameLiftClient

    session = Session()
    client: GameLiftClient = session.client("gamelift")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
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

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("GameLiftClient",)


class Exceptions(BaseClientExceptions):
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    FleetCapacityExceededException: type[BotocoreClientError]
    GameSessionFullException: type[BotocoreClientError]
    IdempotentParameterMismatchException: type[BotocoreClientError]
    InternalServiceException: type[BotocoreClientError]
    InvalidFleetStatusException: type[BotocoreClientError]
    InvalidGameSessionStatusException: type[BotocoreClientError]
    InvalidRequestException: type[BotocoreClientError]
    LimitExceededException: type[BotocoreClientError]
    NotFoundException: type[BotocoreClientError]
    NotReadyException: type[BotocoreClientError]
    OutOfCapacityException: type[BotocoreClientError]
    TaggingFailedException: type[BotocoreClientError]
    TerminalRoutingStrategyException: type[BotocoreClientError]
    UnauthorizedException: type[BotocoreClientError]
    UnsupportedRegionException: type[BotocoreClientError]


class GameLiftClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GameLiftClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift.html#GameLift.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#can_paginate)
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
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#generate_presigned_url)
        """

    def accept_match(self, **kwargs: Unpack[AcceptMatchInputTypeDef]) -> dict[str, Any]:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/accept_match.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#accept_match)
        """

    def claim_game_server(
        self, **kwargs: Unpack[ClaimGameServerInputTypeDef]
    ) -> ClaimGameServerOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2 (FleetIQ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/claim_game_server.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#claim_game_server)
        """

    def create_alias(self, **kwargs: Unpack[CreateAliasInputTypeDef]) -> CreateAliasOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#create_alias)
        """

    def create_build(self, **kwargs: Unpack[CreateBuildInputTypeDef]) -> CreateBuildOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_build.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#create_build)
        """

    def create_container_fleet(
        self, **kwargs: Unpack[CreateContainerFleetInputTypeDef]
    ) -> CreateContainerFleetOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_container_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#create_container_fleet)
        """

    def create_container_group_definition(
        self, **kwargs: Unpack[CreateContainerGroupDefinitionInputTypeDef]
    ) -> CreateContainerGroupDefinitionOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_container_group_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#create_container_group_definition)
        """

    def create_fleet(self, **kwargs: Unpack[CreateFleetInputTypeDef]) -> CreateFleetOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#create_fleet)
        """

    def create_fleet_locations(
        self, **kwargs: Unpack[CreateFleetLocationsInputTypeDef]
    ) -> CreateFleetLocationsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_fleet_locations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#create_fleet_locations)
        """

    def create_game_server_group(
        self, **kwargs: Unpack[CreateGameServerGroupInputTypeDef]
    ) -> CreateGameServerGroupOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2 (FleetIQ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_game_server_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#create_game_server_group)
        """

    def create_game_session(
        self, **kwargs: Unpack[CreateGameSessionInputTypeDef]
    ) -> CreateGameSessionOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_game_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#create_game_session)
        """

    def create_game_session_queue(
        self, **kwargs: Unpack[CreateGameSessionQueueInputTypeDef]
    ) -> CreateGameSessionQueueOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_game_session_queue.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#create_game_session_queue)
        """

    def create_location(
        self, **kwargs: Unpack[CreateLocationInputTypeDef]
    ) -> CreateLocationOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> Anywhere.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_location.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#create_location)
        """

    def create_matchmaking_configuration(
        self, **kwargs: Unpack[CreateMatchmakingConfigurationInputTypeDef]
    ) -> CreateMatchmakingConfigurationOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_matchmaking_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#create_matchmaking_configuration)
        """

    def create_matchmaking_rule_set(
        self, **kwargs: Unpack[CreateMatchmakingRuleSetInputTypeDef]
    ) -> CreateMatchmakingRuleSetOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_matchmaking_rule_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#create_matchmaking_rule_set)
        """

    def create_player_session(
        self, **kwargs: Unpack[CreatePlayerSessionInputTypeDef]
    ) -> CreatePlayerSessionOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_player_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#create_player_session)
        """

    def create_player_sessions(
        self, **kwargs: Unpack[CreatePlayerSessionsInputTypeDef]
    ) -> CreatePlayerSessionsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_player_sessions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#create_player_sessions)
        """

    def create_script(
        self, **kwargs: Unpack[CreateScriptInputTypeDef]
    ) -> CreateScriptOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_script.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#create_script)
        """

    def create_vpc_peering_authorization(
        self, **kwargs: Unpack[CreateVpcPeeringAuthorizationInputTypeDef]
    ) -> CreateVpcPeeringAuthorizationOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_vpc_peering_authorization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#create_vpc_peering_authorization)
        """

    def create_vpc_peering_connection(
        self, **kwargs: Unpack[CreateVpcPeeringConnectionInputTypeDef]
    ) -> dict[str, Any]:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/create_vpc_peering_connection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#create_vpc_peering_connection)
        """

    def delete_alias(
        self, **kwargs: Unpack[DeleteAliasInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#delete_alias)
        """

    def delete_build(
        self, **kwargs: Unpack[DeleteBuildInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_build.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#delete_build)
        """

    def delete_container_fleet(
        self, **kwargs: Unpack[DeleteContainerFleetInputTypeDef]
    ) -> dict[str, Any]:
        """
        <b>This API works with the following fleet types:</b> Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_container_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#delete_container_fleet)
        """

    def delete_container_group_definition(
        self, **kwargs: Unpack[DeleteContainerGroupDefinitionInputTypeDef]
    ) -> dict[str, Any]:
        """
        <b>This API works with the following fleet types:</b> Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_container_group_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#delete_container_group_definition)
        """

    def delete_fleet(
        self, **kwargs: Unpack[DeleteFleetInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#delete_fleet)
        """

    def delete_fleet_locations(
        self, **kwargs: Unpack[DeleteFleetLocationsInputTypeDef]
    ) -> DeleteFleetLocationsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_fleet_locations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#delete_fleet_locations)
        """

    def delete_game_server_group(
        self, **kwargs: Unpack[DeleteGameServerGroupInputTypeDef]
    ) -> DeleteGameServerGroupOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2 (FleetIQ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_game_server_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#delete_game_server_group)
        """

    def delete_game_session_queue(
        self, **kwargs: Unpack[DeleteGameSessionQueueInputTypeDef]
    ) -> dict[str, Any]:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_game_session_queue.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#delete_game_session_queue)
        """

    def delete_location(self, **kwargs: Unpack[DeleteLocationInputTypeDef]) -> dict[str, Any]:
        """
        <b>This API works with the following fleet types:</b> Anywhere.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_location.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#delete_location)
        """

    def delete_matchmaking_configuration(
        self, **kwargs: Unpack[DeleteMatchmakingConfigurationInputTypeDef]
    ) -> dict[str, Any]:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_matchmaking_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#delete_matchmaking_configuration)
        """

    def delete_matchmaking_rule_set(
        self, **kwargs: Unpack[DeleteMatchmakingRuleSetInputTypeDef]
    ) -> dict[str, Any]:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_matchmaking_rule_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#delete_matchmaking_rule_set)
        """

    def delete_scaling_policy(
        self, **kwargs: Unpack[DeleteScalingPolicyInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_scaling_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#delete_scaling_policy)
        """

    def delete_script(
        self, **kwargs: Unpack[DeleteScriptInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_script.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#delete_script)
        """

    def delete_vpc_peering_authorization(
        self, **kwargs: Unpack[DeleteVpcPeeringAuthorizationInputTypeDef]
    ) -> dict[str, Any]:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_vpc_peering_authorization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#delete_vpc_peering_authorization)
        """

    def delete_vpc_peering_connection(
        self, **kwargs: Unpack[DeleteVpcPeeringConnectionInputTypeDef]
    ) -> dict[str, Any]:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/delete_vpc_peering_connection.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#delete_vpc_peering_connection)
        """

    def deregister_compute(self, **kwargs: Unpack[DeregisterComputeInputTypeDef]) -> dict[str, Any]:
        """
        <b>This API works with the following fleet types:</b> Anywhere.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/deregister_compute.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#deregister_compute)
        """

    def deregister_game_server(
        self, **kwargs: Unpack[DeregisterGameServerInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2 (FleetIQ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/deregister_game_server.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#deregister_game_server)
        """

    def describe_alias(
        self, **kwargs: Unpack[DescribeAliasInputTypeDef]
    ) -> DescribeAliasOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_alias)
        """

    def describe_build(
        self, **kwargs: Unpack[DescribeBuildInputTypeDef]
    ) -> DescribeBuildOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_build.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_build)
        """

    def describe_compute(
        self, **kwargs: Unpack[DescribeComputeInputTypeDef]
    ) -> DescribeComputeOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_compute.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_compute)
        """

    def describe_container_fleet(
        self, **kwargs: Unpack[DescribeContainerFleetInputTypeDef]
    ) -> DescribeContainerFleetOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_container_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_container_fleet)
        """

    def describe_container_group_definition(
        self, **kwargs: Unpack[DescribeContainerGroupDefinitionInputTypeDef]
    ) -> DescribeContainerGroupDefinitionOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_container_group_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_container_group_definition)
        """

    def describe_ec2_instance_limits(
        self, **kwargs: Unpack[DescribeEC2InstanceLimitsInputTypeDef]
    ) -> DescribeEC2InstanceLimitsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_ec2_instance_limits.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_ec2_instance_limits)
        """

    def describe_fleet_attributes(
        self, **kwargs: Unpack[DescribeFleetAttributesInputTypeDef]
    ) -> DescribeFleetAttributesOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_fleet_attributes)
        """

    def describe_fleet_capacity(
        self, **kwargs: Unpack[DescribeFleetCapacityInputTypeDef]
    ) -> DescribeFleetCapacityOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_capacity.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_fleet_capacity)
        """

    def describe_fleet_deployment(
        self, **kwargs: Unpack[DescribeFleetDeploymentInputTypeDef]
    ) -> DescribeFleetDeploymentOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_deployment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_fleet_deployment)
        """

    def describe_fleet_events(
        self, **kwargs: Unpack[DescribeFleetEventsInputTypeDef]
    ) -> DescribeFleetEventsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_events.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_fleet_events)
        """

    def describe_fleet_location_attributes(
        self, **kwargs: Unpack[DescribeFleetLocationAttributesInputTypeDef]
    ) -> DescribeFleetLocationAttributesOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_location_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_fleet_location_attributes)
        """

    def describe_fleet_location_capacity(
        self, **kwargs: Unpack[DescribeFleetLocationCapacityInputTypeDef]
    ) -> DescribeFleetLocationCapacityOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_location_capacity.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_fleet_location_capacity)
        """

    def describe_fleet_location_utilization(
        self, **kwargs: Unpack[DescribeFleetLocationUtilizationInputTypeDef]
    ) -> DescribeFleetLocationUtilizationOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_location_utilization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_fleet_location_utilization)
        """

    def describe_fleet_port_settings(
        self, **kwargs: Unpack[DescribeFleetPortSettingsInputTypeDef]
    ) -> DescribeFleetPortSettingsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_port_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_fleet_port_settings)
        """

    def describe_fleet_utilization(
        self, **kwargs: Unpack[DescribeFleetUtilizationInputTypeDef]
    ) -> DescribeFleetUtilizationOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_fleet_utilization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_fleet_utilization)
        """

    def describe_game_server(
        self, **kwargs: Unpack[DescribeGameServerInputTypeDef]
    ) -> DescribeGameServerOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2 (FleetIQ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_game_server.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_game_server)
        """

    def describe_game_server_group(
        self, **kwargs: Unpack[DescribeGameServerGroupInputTypeDef]
    ) -> DescribeGameServerGroupOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2 (FleetIQ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_game_server_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_game_server_group)
        """

    def describe_game_server_instances(
        self, **kwargs: Unpack[DescribeGameServerInstancesInputTypeDef]
    ) -> DescribeGameServerInstancesOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2 (FleetIQ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_game_server_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_game_server_instances)
        """

    def describe_game_session_details(
        self, **kwargs: Unpack[DescribeGameSessionDetailsInputTypeDef]
    ) -> DescribeGameSessionDetailsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_game_session_details.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_game_session_details)
        """

    def describe_game_session_placement(
        self, **kwargs: Unpack[DescribeGameSessionPlacementInputTypeDef]
    ) -> DescribeGameSessionPlacementOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_game_session_placement.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_game_session_placement)
        """

    def describe_game_session_queues(
        self, **kwargs: Unpack[DescribeGameSessionQueuesInputTypeDef]
    ) -> DescribeGameSessionQueuesOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_game_session_queues.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_game_session_queues)
        """

    def describe_game_sessions(
        self, **kwargs: Unpack[DescribeGameSessionsInputTypeDef]
    ) -> DescribeGameSessionsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_game_sessions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_game_sessions)
        """

    def describe_instances(
        self, **kwargs: Unpack[DescribeInstancesInputTypeDef]
    ) -> DescribeInstancesOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_instances)
        """

    def describe_matchmaking(
        self, **kwargs: Unpack[DescribeMatchmakingInputTypeDef]
    ) -> DescribeMatchmakingOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_matchmaking.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_matchmaking)
        """

    def describe_matchmaking_configurations(
        self, **kwargs: Unpack[DescribeMatchmakingConfigurationsInputTypeDef]
    ) -> DescribeMatchmakingConfigurationsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_matchmaking_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_matchmaking_configurations)
        """

    def describe_matchmaking_rule_sets(
        self, **kwargs: Unpack[DescribeMatchmakingRuleSetsInputTypeDef]
    ) -> DescribeMatchmakingRuleSetsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_matchmaking_rule_sets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_matchmaking_rule_sets)
        """

    def describe_player_sessions(
        self, **kwargs: Unpack[DescribePlayerSessionsInputTypeDef]
    ) -> DescribePlayerSessionsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_player_sessions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_player_sessions)
        """

    def describe_runtime_configuration(
        self, **kwargs: Unpack[DescribeRuntimeConfigurationInputTypeDef]
    ) -> DescribeRuntimeConfigurationOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_runtime_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_runtime_configuration)
        """

    def describe_scaling_policies(
        self, **kwargs: Unpack[DescribeScalingPoliciesInputTypeDef]
    ) -> DescribeScalingPoliciesOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_scaling_policies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_scaling_policies)
        """

    def describe_script(
        self, **kwargs: Unpack[DescribeScriptInputTypeDef]
    ) -> DescribeScriptOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_script.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_script)
        """

    def describe_vpc_peering_authorizations(self) -> DescribeVpcPeeringAuthorizationsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_vpc_peering_authorizations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_vpc_peering_authorizations)
        """

    def describe_vpc_peering_connections(
        self, **kwargs: Unpack[DescribeVpcPeeringConnectionsInputTypeDef]
    ) -> DescribeVpcPeeringConnectionsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/describe_vpc_peering_connections.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#describe_vpc_peering_connections)
        """

    def get_compute_access(
        self, **kwargs: Unpack[GetComputeAccessInputTypeDef]
    ) -> GetComputeAccessOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_compute_access.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_compute_access)
        """

    def get_compute_auth_token(
        self, **kwargs: Unpack[GetComputeAuthTokenInputTypeDef]
    ) -> GetComputeAuthTokenOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_compute_auth_token.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_compute_auth_token)
        """

    def get_game_session_log_url(
        self, **kwargs: Unpack[GetGameSessionLogUrlInputTypeDef]
    ) -> GetGameSessionLogUrlOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_game_session_log_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_game_session_log_url)
        """

    def get_instance_access(
        self, **kwargs: Unpack[GetInstanceAccessInputTypeDef]
    ) -> GetInstanceAccessOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_instance_access.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_instance_access)
        """

    def list_aliases(self, **kwargs: Unpack[ListAliasesInputTypeDef]) -> ListAliasesOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_aliases.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#list_aliases)
        """

    def list_builds(self, **kwargs: Unpack[ListBuildsInputTypeDef]) -> ListBuildsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_builds.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#list_builds)
        """

    def list_compute(self, **kwargs: Unpack[ListComputeInputTypeDef]) -> ListComputeOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_compute.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#list_compute)
        """

    def list_container_fleets(
        self, **kwargs: Unpack[ListContainerFleetsInputTypeDef]
    ) -> ListContainerFleetsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_container_fleets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#list_container_fleets)
        """

    def list_container_group_definition_versions(
        self, **kwargs: Unpack[ListContainerGroupDefinitionVersionsInputTypeDef]
    ) -> ListContainerGroupDefinitionVersionsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_container_group_definition_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#list_container_group_definition_versions)
        """

    def list_container_group_definitions(
        self, **kwargs: Unpack[ListContainerGroupDefinitionsInputTypeDef]
    ) -> ListContainerGroupDefinitionsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_container_group_definitions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#list_container_group_definitions)
        """

    def list_fleet_deployments(
        self, **kwargs: Unpack[ListFleetDeploymentsInputTypeDef]
    ) -> ListFleetDeploymentsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_fleet_deployments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#list_fleet_deployments)
        """

    def list_fleets(self, **kwargs: Unpack[ListFleetsInputTypeDef]) -> ListFleetsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_fleets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#list_fleets)
        """

    def list_game_server_groups(
        self, **kwargs: Unpack[ListGameServerGroupsInputTypeDef]
    ) -> ListGameServerGroupsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2 (FleetIQ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_game_server_groups.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#list_game_server_groups)
        """

    def list_game_servers(
        self, **kwargs: Unpack[ListGameServersInputTypeDef]
    ) -> ListGameServersOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2 (FleetIQ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_game_servers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#list_game_servers)
        """

    def list_locations(
        self, **kwargs: Unpack[ListLocationsInputTypeDef]
    ) -> ListLocationsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> Anywhere.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_locations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#list_locations)
        """

    def list_scripts(self, **kwargs: Unpack[ListScriptsInputTypeDef]) -> ListScriptsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_scripts.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#list_scripts)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#list_tags_for_resource)
        """

    def put_scaling_policy(
        self, **kwargs: Unpack[PutScalingPolicyInputTypeDef]
    ) -> PutScalingPolicyOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/put_scaling_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#put_scaling_policy)
        """

    def register_compute(
        self, **kwargs: Unpack[RegisterComputeInputTypeDef]
    ) -> RegisterComputeOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/register_compute.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#register_compute)
        """

    def register_game_server(
        self, **kwargs: Unpack[RegisterGameServerInputTypeDef]
    ) -> RegisterGameServerOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2 (FleetIQ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/register_game_server.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#register_game_server)
        """

    def request_upload_credentials(
        self, **kwargs: Unpack[RequestUploadCredentialsInputTypeDef]
    ) -> RequestUploadCredentialsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/request_upload_credentials.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#request_upload_credentials)
        """

    def resolve_alias(
        self, **kwargs: Unpack[ResolveAliasInputTypeDef]
    ) -> ResolveAliasOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/resolve_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#resolve_alias)
        """

    def resume_game_server_group(
        self, **kwargs: Unpack[ResumeGameServerGroupInputTypeDef]
    ) -> ResumeGameServerGroupOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2 (FleetIQ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/resume_game_server_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#resume_game_server_group)
        """

    def search_game_sessions(
        self, **kwargs: Unpack[SearchGameSessionsInputTypeDef]
    ) -> SearchGameSessionsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/search_game_sessions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#search_game_sessions)
        """

    def start_fleet_actions(
        self, **kwargs: Unpack[StartFleetActionsInputTypeDef]
    ) -> StartFleetActionsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/start_fleet_actions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#start_fleet_actions)
        """

    def start_game_session_placement(
        self, **kwargs: Unpack[StartGameSessionPlacementInputTypeDef]
    ) -> StartGameSessionPlacementOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/start_game_session_placement.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#start_game_session_placement)
        """

    def start_match_backfill(
        self, **kwargs: Unpack[StartMatchBackfillInputTypeDef]
    ) -> StartMatchBackfillOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/start_match_backfill.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#start_match_backfill)
        """

    def start_matchmaking(
        self, **kwargs: Unpack[StartMatchmakingInputTypeDef]
    ) -> StartMatchmakingOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/start_matchmaking.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#start_matchmaking)
        """

    def stop_fleet_actions(
        self, **kwargs: Unpack[StopFleetActionsInputTypeDef]
    ) -> StopFleetActionsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/stop_fleet_actions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#stop_fleet_actions)
        """

    def stop_game_session_placement(
        self, **kwargs: Unpack[StopGameSessionPlacementInputTypeDef]
    ) -> StopGameSessionPlacementOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/stop_game_session_placement.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#stop_game_session_placement)
        """

    def stop_matchmaking(self, **kwargs: Unpack[StopMatchmakingInputTypeDef]) -> dict[str, Any]:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/stop_matchmaking.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#stop_matchmaking)
        """

    def suspend_game_server_group(
        self, **kwargs: Unpack[SuspendGameServerGroupInputTypeDef]
    ) -> SuspendGameServerGroupOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2 (FleetIQ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/suspend_game_server_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#suspend_game_server_group)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#tag_resource)
        """

    def terminate_game_session(
        self, **kwargs: Unpack[TerminateGameSessionInputTypeDef]
    ) -> TerminateGameSessionOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/terminate_game_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#terminate_game_session)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#untag_resource)
        """

    def update_alias(self, **kwargs: Unpack[UpdateAliasInputTypeDef]) -> UpdateAliasOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_alias.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#update_alias)
        """

    def update_build(self, **kwargs: Unpack[UpdateBuildInputTypeDef]) -> UpdateBuildOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_build.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#update_build)
        """

    def update_container_fleet(
        self, **kwargs: Unpack[UpdateContainerFleetInputTypeDef]
    ) -> UpdateContainerFleetOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_container_fleet.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#update_container_fleet)
        """

    def update_container_group_definition(
        self, **kwargs: Unpack[UpdateContainerGroupDefinitionInputTypeDef]
    ) -> UpdateContainerGroupDefinitionOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_container_group_definition.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#update_container_group_definition)
        """

    def update_fleet_attributes(
        self, **kwargs: Unpack[UpdateFleetAttributesInputTypeDef]
    ) -> UpdateFleetAttributesOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_fleet_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#update_fleet_attributes)
        """

    def update_fleet_capacity(
        self, **kwargs: Unpack[UpdateFleetCapacityInputTypeDef]
    ) -> UpdateFleetCapacityOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_fleet_capacity.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#update_fleet_capacity)
        """

    def update_fleet_port_settings(
        self, **kwargs: Unpack[UpdateFleetPortSettingsInputTypeDef]
    ) -> UpdateFleetPortSettingsOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_fleet_port_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#update_fleet_port_settings)
        """

    def update_game_server(
        self, **kwargs: Unpack[UpdateGameServerInputTypeDef]
    ) -> UpdateGameServerOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2 (FleetIQ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_game_server.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#update_game_server)
        """

    def update_game_server_group(
        self, **kwargs: Unpack[UpdateGameServerGroupInputTypeDef]
    ) -> UpdateGameServerGroupOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2 (FleetIQ).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_game_server_group.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#update_game_server_group)
        """

    def update_game_session(
        self, **kwargs: Unpack[UpdateGameSessionInputTypeDef]
    ) -> UpdateGameSessionOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_game_session.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#update_game_session)
        """

    def update_game_session_queue(
        self, **kwargs: Unpack[UpdateGameSessionQueueInputTypeDef]
    ) -> UpdateGameSessionQueueOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_game_session_queue.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#update_game_session_queue)
        """

    def update_matchmaking_configuration(
        self, **kwargs: Unpack[UpdateMatchmakingConfigurationInputTypeDef]
    ) -> UpdateMatchmakingConfigurationOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_matchmaking_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#update_matchmaking_configuration)
        """

    def update_runtime_configuration(
        self, **kwargs: Unpack[UpdateRuntimeConfigurationInputTypeDef]
    ) -> UpdateRuntimeConfigurationOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_runtime_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#update_runtime_configuration)
        """

    def update_script(
        self, **kwargs: Unpack[UpdateScriptInputTypeDef]
    ) -> UpdateScriptOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/update_script.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#update_script)
        """

    def validate_matchmaking_rule_set(
        self, **kwargs: Unpack[ValidateMatchmakingRuleSetInputTypeDef]
    ) -> ValidateMatchmakingRuleSetOutputTypeDef:
        """
        <b>This API works with the following fleet types:</b> EC2, Anywhere, Container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/validate_matchmaking_rule_set.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#validate_matchmaking_rule_set)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_fleet_attributes"]
    ) -> DescribeFleetAttributesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_fleet_capacity"]
    ) -> DescribeFleetCapacityPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_fleet_events"]
    ) -> DescribeFleetEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_fleet_utilization"]
    ) -> DescribeFleetUtilizationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_game_server_instances"]
    ) -> DescribeGameServerInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_game_session_details"]
    ) -> DescribeGameSessionDetailsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_game_session_queues"]
    ) -> DescribeGameSessionQueuesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_game_sessions"]
    ) -> DescribeGameSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_instances"]
    ) -> DescribeInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_matchmaking_configurations"]
    ) -> DescribeMatchmakingConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_matchmaking_rule_sets"]
    ) -> DescribeMatchmakingRuleSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_player_sessions"]
    ) -> DescribePlayerSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_scaling_policies"]
    ) -> DescribeScalingPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_aliases"]
    ) -> ListAliasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_builds"]
    ) -> ListBuildsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_compute"]
    ) -> ListComputePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_container_fleets"]
    ) -> ListContainerFleetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_container_group_definition_versions"]
    ) -> ListContainerGroupDefinitionVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_container_group_definitions"]
    ) -> ListContainerGroupDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_fleet_deployments"]
    ) -> ListFleetDeploymentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_fleets"]
    ) -> ListFleetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_game_server_groups"]
    ) -> ListGameServerGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_game_servers"]
    ) -> ListGameServersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_locations"]
    ) -> ListLocationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_scripts"]
    ) -> ListScriptsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_game_sessions"]
    ) -> SearchGameSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/gamelift/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_gamelift/client/#get_paginator)
        """
