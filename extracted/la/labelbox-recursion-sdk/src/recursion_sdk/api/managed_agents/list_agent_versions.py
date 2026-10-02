from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.managed_agents_agent_version_list_response import ManagedAgentsAgentVersionListResponse
from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_forbidden import ManagedAgentsApiErrorForbidden
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from typing import cast
from uuid import UUID



def _get_kwargs(
    agent_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/agents/{agent_id}/versions".format(agent_id=quote(str(agent_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsAgentVersionListResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsAgentVersionListResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = ManagedAgentsApiError.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = ManagedAgentsApiError.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = ManagedAgentsApiErrorForbidden.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = ManagedAgentsApiError.from_dict(response.json())



        return response_404

    if response.status_code == 429:
        response_429 = ManagedAgentsApiError.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        response_500 = ManagedAgentsApiError.from_dict(response.json())



        return response_500

    if response.status_code == 502:
        response_502 = ManagedAgentsApiErrorBadGateway.from_dict(response.json())



        return response_502

    if response.status_code == 503:
        response_503 = ManagedAgentsApiError.from_dict(response.json())



        return response_503

    if response.status_code == 504:
        response_504 = ManagedAgentsApiErrorGatewayTimeout.from_dict(response.json())



        return response_504

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsAgentVersionListResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    agent_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[ManagedAgentsAgentVersionListResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout]:
    """ List an agent's immutable version history

     Returns all immutable agent versions, newest to oldest, projected through the current public
    contract. Prompt, model, and supported capabilities remain visible; inert legacy tool declarations
    remain stored but are omitted from these responses. The response is not paginated.

    Args:
        agent_id (UUID): Agent id (UUID) as returned by createAgent or listAgents.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsAgentVersionListResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> ManagedAgentsAgentVersionListResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | None:
    """ List an agent's immutable version history

     Returns all immutable agent versions, newest to oldest, projected through the current public
    contract. Prompt, model, and supported capabilities remain visible; inert legacy tool declarations
    remain stored but are omitted from these responses. The response is not paginated.

    Args:
        agent_id (UUID): Agent id (UUID) as returned by createAgent or listAgents.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsAgentVersionListResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout
     """


    return sync_detailed(
        agent_id=agent_id,
client=client,

    ).parsed

async def asyncio_detailed(
    agent_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[ManagedAgentsAgentVersionListResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout]:
    """ List an agent's immutable version history

     Returns all immutable agent versions, newest to oldest, projected through the current public
    contract. Prompt, model, and supported capabilities remain visible; inert legacy tool declarations
    remain stored but are omitted from these responses. The response is not paginated.

    Args:
        agent_id (UUID): Agent id (UUID) as returned by createAgent or listAgents.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsAgentVersionListResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> ManagedAgentsAgentVersionListResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | None:
    """ List an agent's immutable version history

     Returns all immutable agent versions, newest to oldest, projected through the current public
    contract. Prompt, model, and supported capabilities remain visible; inert legacy tool declarations
    remain stored but are omitted from these responses. The response is not paginated.

    Args:
        agent_id (UUID): Agent id (UUID) as returned by createAgent or listAgents.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsAgentVersionListResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout
     """


    return (await asyncio_detailed(
        agent_id=agent_id,
client=client,

    )).parsed
