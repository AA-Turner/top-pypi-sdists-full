from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.managed_agents_api_error_auth_unavailable import ManagedAgentsApiErrorAuthUnavailable
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_forbidden import ManagedAgentsApiErrorForbidden
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_api_error_integrations_unconfigured import ManagedAgentsApiErrorIntegrationsUnconfigured
from ...models.managed_agents_api_error_internal_error import ManagedAgentsApiErrorInternalError
from ...models.managed_agents_api_error_invalid_request import ManagedAgentsApiErrorInvalidRequest
from ...models.managed_agents_api_error_invariant_violation import ManagedAgentsApiErrorInvariantViolation
from ...models.managed_agents_api_error_managed_agents_unavailable import ManagedAgentsApiErrorManagedAgentsUnavailable
from ...models.managed_agents_api_error_not_found import ManagedAgentsApiErrorNotFound
from ...models.managed_agents_api_error_rate_limit_exceeded import ManagedAgentsApiErrorRateLimitExceeded
from ...models.managed_agents_api_error_rate_limited import ManagedAgentsApiErrorRateLimited
from ...models.managed_agents_api_error_service_unavailable import ManagedAgentsApiErrorServiceUnavailable
from ...models.managed_agents_api_error_slack_channels_rejected import ManagedAgentsApiErrorSlackChannelsRejected
from ...models.managed_agents_api_error_slack_channels_unavailable import ManagedAgentsApiErrorSlackChannelsUnavailable
from ...models.managed_agents_api_error_slack_channels_unconfigured import ManagedAgentsApiErrorSlackChannelsUnconfigured
from ...models.managed_agents_api_error_slack_connection_malformed import ManagedAgentsApiErrorSlackConnectionMalformed
from ...models.managed_agents_api_error_slack_installation_mismatch import ManagedAgentsApiErrorSlackInstallationMismatch
from ...models.managed_agents_api_error_slack_missing_scope import ManagedAgentsApiErrorSlackMissingScope
from ...models.managed_agents_api_error_slack_rate_limited import ManagedAgentsApiErrorSlackRateLimited
from ...models.managed_agents_api_error_slack_reapproval_required import ManagedAgentsApiErrorSlackReapprovalRequired
from ...models.managed_agents_api_error_unauthorized import ManagedAgentsApiErrorUnauthorized
from ...models.managed_agents_slack_channels import ManagedAgentsSlackChannels
from typing import cast
from uuid import UUID



def _get_kwargs(
    connection_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/integrations/connections/{connection_id}/channel-catalog".format(connection_id=quote(str(connection_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorIntegrationsUnconfigured | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorSlackChannelsUnavailable | ManagedAgentsApiErrorSlackChannelsUnconfigured | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSlackRateLimited | ManagedAgentsApiErrorSlackChannelsRejected | ManagedAgentsApiErrorSlackConnectionMalformed | ManagedAgentsApiErrorSlackInstallationMismatch | ManagedAgentsApiErrorSlackMissingScope | ManagedAgentsApiErrorSlackReapprovalRequired | ManagedAgentsApiErrorUnauthorized | ManagedAgentsSlackChannels | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsSlackChannels.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = ManagedAgentsApiErrorInvalidRequest.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = ManagedAgentsApiErrorUnauthorized.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = ManagedAgentsApiErrorForbidden.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = ManagedAgentsApiErrorNotFound.from_dict(response.json())



        return response_404

    if response.status_code == 422:
        def _parse_response_422(data: object) -> ManagedAgentsApiErrorSlackChannelsRejected | ManagedAgentsApiErrorSlackConnectionMalformed | ManagedAgentsApiErrorSlackInstallationMismatch | ManagedAgentsApiErrorSlackMissingScope | ManagedAgentsApiErrorSlackReapprovalRequired:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_422_type_0 = ManagedAgentsApiErrorSlackChannelsRejected.from_dict(data)



                return response_422_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_422_type_1 = ManagedAgentsApiErrorSlackConnectionMalformed.from_dict(data)



                return response_422_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_422_type_2 = ManagedAgentsApiErrorSlackInstallationMismatch.from_dict(data)



                return response_422_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_422_type_3 = ManagedAgentsApiErrorSlackMissingScope.from_dict(data)



                return response_422_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_422_type_4 = ManagedAgentsApiErrorSlackReapprovalRequired.from_dict(data)



            return response_422_type_4

        response_422 = _parse_response_422(response.json())

        return response_422

    if response.status_code == 429:
        def _parse_response_429(data: object) -> ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSlackRateLimited:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_429_type_0 = ManagedAgentsApiErrorRateLimitExceeded.from_dict(data)



                return response_429_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_429_type_1 = ManagedAgentsApiErrorRateLimited.from_dict(data)



                return response_429_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_429_type_2 = ManagedAgentsApiErrorSlackRateLimited.from_dict(data)



            return response_429_type_2

        response_429 = _parse_response_429(response.json())

        return response_429

    if response.status_code == 500:
        def _parse_response_500(data: object) -> ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_500_type_0 = ManagedAgentsApiErrorInternalError.from_dict(data)



                return response_500_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_500_type_1 = ManagedAgentsApiErrorInvariantViolation.from_dict(data)



            return response_500_type_1

        response_500 = _parse_response_500(response.json())

        return response_500

    if response.status_code == 502:
        response_502 = ManagedAgentsApiErrorBadGateway.from_dict(response.json())



        return response_502

    if response.status_code == 503:
        def _parse_response_503(data: object) -> ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorIntegrationsUnconfigured | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorSlackChannelsUnavailable | ManagedAgentsApiErrorSlackChannelsUnconfigured:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_503_type_0 = ManagedAgentsApiErrorAuthUnavailable.from_dict(data)



                return response_503_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_503_type_1 = ManagedAgentsApiErrorIntegrationsUnconfigured.from_dict(data)



                return response_503_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_503_type_2 = ManagedAgentsApiErrorManagedAgentsUnavailable.from_dict(data)



                return response_503_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_503_type_3 = ManagedAgentsApiErrorServiceUnavailable.from_dict(data)



                return response_503_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_503_type_4 = ManagedAgentsApiErrorSlackChannelsUnavailable.from_dict(data)



                return response_503_type_4
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_503_type_5 = ManagedAgentsApiErrorSlackChannelsUnconfigured.from_dict(data)



            return response_503_type_5

        response_503 = _parse_response_503(response.json())

        return response_503

    if response.status_code == 504:
        response_504 = ManagedAgentsApiErrorGatewayTimeout.from_dict(response.json())



        return response_504

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorIntegrationsUnconfigured | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorSlackChannelsUnavailable | ManagedAgentsApiErrorSlackChannelsUnconfigured | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSlackRateLimited | ManagedAgentsApiErrorSlackChannelsRejected | ManagedAgentsApiErrorSlackConnectionMalformed | ManagedAgentsApiErrorSlackInstallationMismatch | ManagedAgentsApiErrorSlackMissingScope | ManagedAgentsApiErrorSlackReapprovalRequired | ManagedAgentsApiErrorUnauthorized | ManagedAgentsSlackChannels]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    connection_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorIntegrationsUnconfigured | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorSlackChannelsUnavailable | ManagedAgentsApiErrorSlackChannelsUnconfigured | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSlackRateLimited | ManagedAgentsApiErrorSlackChannelsRejected | ManagedAgentsApiErrorSlackConnectionMalformed | ManagedAgentsApiErrorSlackInstallationMismatch | ManagedAgentsApiErrorSlackMissingScope | ManagedAgentsApiErrorSlackReapprovalRequired | ManagedAgentsApiErrorUnauthorized | ManagedAgentsSlackChannels]:
    """ Get the connected Slack bot's bounded channel-selection catalog

     Returns a channel-selection snapshot of at most 1,000 memberships from the connected Slack
    workspace, using that installation's credential, so an automation trigger can be configured by
    picking a channel instead of pasting its id. Only a Slack connection has channels; the list is
    scoped to the connection's own workspace. A channel the bot is not a member of is never listed:
    invite the bot in Slack first. Throttled reads return 429 slack_rate_limited. A list that stopped at
    the size budget says truncated=true, so absence from the list never proves the bot is not a member.
    If the Slack app lacks channels:read or groups:read the response is 422 slack_missing_scope naming
    the scopes to add.

    Args:
        connection_id (UUID): Slack integration connection identifier.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorIntegrationsUnconfigured | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorSlackChannelsUnavailable | ManagedAgentsApiErrorSlackChannelsUnconfigured | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSlackRateLimited | ManagedAgentsApiErrorSlackChannelsRejected | ManagedAgentsApiErrorSlackConnectionMalformed | ManagedAgentsApiErrorSlackInstallationMismatch | ManagedAgentsApiErrorSlackMissingScope | ManagedAgentsApiErrorSlackReapprovalRequired | ManagedAgentsApiErrorUnauthorized | ManagedAgentsSlackChannels]
     """


    kwargs = _get_kwargs(
        connection_id=connection_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    connection_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorIntegrationsUnconfigured | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorSlackChannelsUnavailable | ManagedAgentsApiErrorSlackChannelsUnconfigured | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSlackRateLimited | ManagedAgentsApiErrorSlackChannelsRejected | ManagedAgentsApiErrorSlackConnectionMalformed | ManagedAgentsApiErrorSlackInstallationMismatch | ManagedAgentsApiErrorSlackMissingScope | ManagedAgentsApiErrorSlackReapprovalRequired | ManagedAgentsApiErrorUnauthorized | ManagedAgentsSlackChannels | None:
    """ Get the connected Slack bot's bounded channel-selection catalog

     Returns a channel-selection snapshot of at most 1,000 memberships from the connected Slack
    workspace, using that installation's credential, so an automation trigger can be configured by
    picking a channel instead of pasting its id. Only a Slack connection has channels; the list is
    scoped to the connection's own workspace. A channel the bot is not a member of is never listed:
    invite the bot in Slack first. Throttled reads return 429 slack_rate_limited. A list that stopped at
    the size budget says truncated=true, so absence from the list never proves the bot is not a member.
    If the Slack app lacks channels:read or groups:read the response is 422 slack_missing_scope naming
    the scopes to add.

    Args:
        connection_id (UUID): Slack integration connection identifier.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorIntegrationsUnconfigured | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorSlackChannelsUnavailable | ManagedAgentsApiErrorSlackChannelsUnconfigured | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSlackRateLimited | ManagedAgentsApiErrorSlackChannelsRejected | ManagedAgentsApiErrorSlackConnectionMalformed | ManagedAgentsApiErrorSlackInstallationMismatch | ManagedAgentsApiErrorSlackMissingScope | ManagedAgentsApiErrorSlackReapprovalRequired | ManagedAgentsApiErrorUnauthorized | ManagedAgentsSlackChannels
     """


    return sync_detailed(
        connection_id=connection_id,
client=client,

    ).parsed

async def asyncio_detailed(
    connection_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorIntegrationsUnconfigured | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorSlackChannelsUnavailable | ManagedAgentsApiErrorSlackChannelsUnconfigured | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSlackRateLimited | ManagedAgentsApiErrorSlackChannelsRejected | ManagedAgentsApiErrorSlackConnectionMalformed | ManagedAgentsApiErrorSlackInstallationMismatch | ManagedAgentsApiErrorSlackMissingScope | ManagedAgentsApiErrorSlackReapprovalRequired | ManagedAgentsApiErrorUnauthorized | ManagedAgentsSlackChannels]:
    """ Get the connected Slack bot's bounded channel-selection catalog

     Returns a channel-selection snapshot of at most 1,000 memberships from the connected Slack
    workspace, using that installation's credential, so an automation trigger can be configured by
    picking a channel instead of pasting its id. Only a Slack connection has channels; the list is
    scoped to the connection's own workspace. A channel the bot is not a member of is never listed:
    invite the bot in Slack first. Throttled reads return 429 slack_rate_limited. A list that stopped at
    the size budget says truncated=true, so absence from the list never proves the bot is not a member.
    If the Slack app lacks channels:read or groups:read the response is 422 slack_missing_scope naming
    the scopes to add.

    Args:
        connection_id (UUID): Slack integration connection identifier.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorIntegrationsUnconfigured | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorSlackChannelsUnavailable | ManagedAgentsApiErrorSlackChannelsUnconfigured | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSlackRateLimited | ManagedAgentsApiErrorSlackChannelsRejected | ManagedAgentsApiErrorSlackConnectionMalformed | ManagedAgentsApiErrorSlackInstallationMismatch | ManagedAgentsApiErrorSlackMissingScope | ManagedAgentsApiErrorSlackReapprovalRequired | ManagedAgentsApiErrorUnauthorized | ManagedAgentsSlackChannels]
     """


    kwargs = _get_kwargs(
        connection_id=connection_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    connection_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorIntegrationsUnconfigured | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorSlackChannelsUnavailable | ManagedAgentsApiErrorSlackChannelsUnconfigured | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSlackRateLimited | ManagedAgentsApiErrorSlackChannelsRejected | ManagedAgentsApiErrorSlackConnectionMalformed | ManagedAgentsApiErrorSlackInstallationMismatch | ManagedAgentsApiErrorSlackMissingScope | ManagedAgentsApiErrorSlackReapprovalRequired | ManagedAgentsApiErrorUnauthorized | ManagedAgentsSlackChannels | None:
    """ Get the connected Slack bot's bounded channel-selection catalog

     Returns a channel-selection snapshot of at most 1,000 memberships from the connected Slack
    workspace, using that installation's credential, so an automation trigger can be configured by
    picking a channel instead of pasting its id. Only a Slack connection has channels; the list is
    scoped to the connection's own workspace. A channel the bot is not a member of is never listed:
    invite the bot in Slack first. Throttled reads return 429 slack_rate_limited. A list that stopped at
    the size budget says truncated=true, so absence from the list never proves the bot is not a member.
    If the Slack app lacks channels:read or groups:read the response is 422 slack_missing_scope naming
    the scopes to add.

    Args:
        connection_id (UUID): Slack integration connection identifier.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiErrorAuthUnavailable | ManagedAgentsApiErrorIntegrationsUnconfigured | ManagedAgentsApiErrorManagedAgentsUnavailable | ManagedAgentsApiErrorServiceUnavailable | ManagedAgentsApiErrorSlackChannelsUnavailable | ManagedAgentsApiErrorSlackChannelsUnconfigured | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorInternalError | ManagedAgentsApiErrorInvariantViolation | ManagedAgentsApiErrorInvalidRequest | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorRateLimited | ManagedAgentsApiErrorRateLimitExceeded | ManagedAgentsApiErrorSlackRateLimited | ManagedAgentsApiErrorSlackChannelsRejected | ManagedAgentsApiErrorSlackConnectionMalformed | ManagedAgentsApiErrorSlackInstallationMismatch | ManagedAgentsApiErrorSlackMissingScope | ManagedAgentsApiErrorSlackReapprovalRequired | ManagedAgentsApiErrorUnauthorized | ManagedAgentsSlackChannels
     """


    return (await asyncio_detailed(
        connection_id=connection_id,
client=client,

    )).parsed
