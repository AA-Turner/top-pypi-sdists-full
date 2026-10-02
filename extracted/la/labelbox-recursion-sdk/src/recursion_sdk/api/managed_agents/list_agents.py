from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.managed_agents_agent_list_response import ManagedAgentsAgentListResponse
from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_forbidden import ManagedAgentsApiErrorForbidden
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_api_error_not_found import ManagedAgentsApiErrorNotFound
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    tag_ids: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["tag_ids"] = tag_ids


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/agents",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsAgentListResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsAgentListResponse.from_dict(response.json())



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
        response_404 = ManagedAgentsApiErrorNotFound.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsAgentListResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    tag_ids: str | Unset = UNSET,

) -> Response[ManagedAgentsAgentListResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound]:
    """ List agents

     Returns every agent in the calling organization, each resolved to its latest immutable version and
    hydrated with current tag definitions in one batch. tag_ids is a comma-separated AND filter: every
    returned agent carries every requested tag. Soft-deleted agents are omitted, and the response is not
    paginated.

    Args:
        tag_ids (str | Unset): Comma-separated tag ids, with at most 32 distinct ids. Blank
            segments are ignored. An agent must carry every requested tag (AND semantics). Unknown or
            cross-organization ids return 404.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsAgentListResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound]
     """


    kwargs = _get_kwargs(
        tag_ids=tag_ids,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    tag_ids: str | Unset = UNSET,

) -> ManagedAgentsAgentListResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | None:
    """ List agents

     Returns every agent in the calling organization, each resolved to its latest immutable version and
    hydrated with current tag definitions in one batch. tag_ids is a comma-separated AND filter: every
    returned agent carries every requested tag. Soft-deleted agents are omitted, and the response is not
    paginated.

    Args:
        tag_ids (str | Unset): Comma-separated tag ids, with at most 32 distinct ids. Blank
            segments are ignored. An agent must carry every requested tag (AND semantics). Unknown or
            cross-organization ids return 404.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsAgentListResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound
     """


    return sync_detailed(
        client=client,
tag_ids=tag_ids,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    tag_ids: str | Unset = UNSET,

) -> Response[ManagedAgentsAgentListResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound]:
    """ List agents

     Returns every agent in the calling organization, each resolved to its latest immutable version and
    hydrated with current tag definitions in one batch. tag_ids is a comma-separated AND filter: every
    returned agent carries every requested tag. Soft-deleted agents are omitted, and the response is not
    paginated.

    Args:
        tag_ids (str | Unset): Comma-separated tag ids, with at most 32 distinct ids. Blank
            segments are ignored. An agent must carry every requested tag (AND semantics). Unknown or
            cross-organization ids return 404.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsAgentListResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound]
     """


    kwargs = _get_kwargs(
        tag_ids=tag_ids,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    tag_ids: str | Unset = UNSET,

) -> ManagedAgentsAgentListResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | None:
    """ List agents

     Returns every agent in the calling organization, each resolved to its latest immutable version and
    hydrated with current tag definitions in one batch. tag_ids is a comma-separated AND filter: every
    returned agent carries every requested tag. Soft-deleted agents are omitted, and the response is not
    paginated.

    Args:
        tag_ids (str | Unset): Comma-separated tag ids, with at most 32 distinct ids. Blank
            segments are ignored. An agent must carry every requested tag (AND semantics). Unknown or
            cross-organization ids return 404.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsAgentListResponse | ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound
     """


    return (await asyncio_detailed(
        client=client,
tag_ids=tag_ids,

    )).parsed
