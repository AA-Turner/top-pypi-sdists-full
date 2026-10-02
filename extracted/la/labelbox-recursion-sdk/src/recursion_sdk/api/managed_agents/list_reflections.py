from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_reflections_status import ListReflectionsStatus
from ...models.list_reflections_triggered_by import ListReflectionsTriggeredBy
from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_forbidden import ManagedAgentsApiErrorForbidden
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_reflection_list_response import ManagedAgentsReflectionListResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    agent_id: str | Unset = UNSET,
    status: ListReflectionsStatus | Unset = UNSET,
    triggered_by: ListReflectionsTriggeredBy | Unset = UNSET,
    limit: int | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["agent_id"] = agent_id

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status

    json_triggered_by: str | Unset = UNSET
    if not isinstance(triggered_by, Unset):
        json_triggered_by = triggered_by.value

    params["triggered_by"] = json_triggered_by

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/reflections",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsReflectionListResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsReflectionListResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsReflectionListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    agent_id: str | Unset = UNSET,
    status: ListReflectionsStatus | Unset = UNSET,
    triggered_by: ListReflectionsTriggeredBy | Unset = UNSET,
    limit: int | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsReflectionListResponse]:
    """ List consolidation runs

     Returns memory consolidation runs, newest first. Each names the digests it read, the collection it
    updated, and the session that ran it -- streaming that session shows the consolidation reasoning in
    real time, because it is an ordinary agent session.

    Args:
        agent_id (str | Unset): Only runs for this agent.
        status (ListReflectionsStatus | Unset): Only runs in this state.
        triggered_by (ListReflectionsTriggeredBy | Unset): Only runs started this way.
        limit (int | Unset): Maximum runs to return. Defaults to 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsReflectionListResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
status=status,
triggered_by=triggered_by,
limit=limit,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    agent_id: str | Unset = UNSET,
    status: ListReflectionsStatus | Unset = UNSET,
    triggered_by: ListReflectionsTriggeredBy | Unset = UNSET,
    limit: int | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsReflectionListResponse | None:
    """ List consolidation runs

     Returns memory consolidation runs, newest first. Each names the digests it read, the collection it
    updated, and the session that ran it -- streaming that session shows the consolidation reasoning in
    real time, because it is an ordinary agent session.

    Args:
        agent_id (str | Unset): Only runs for this agent.
        status (ListReflectionsStatus | Unset): Only runs in this state.
        triggered_by (ListReflectionsTriggeredBy | Unset): Only runs started this way.
        limit (int | Unset): Maximum runs to return. Defaults to 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsReflectionListResponse
     """


    return sync_detailed(
        client=client,
agent_id=agent_id,
status=status,
triggered_by=triggered_by,
limit=limit,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    agent_id: str | Unset = UNSET,
    status: ListReflectionsStatus | Unset = UNSET,
    triggered_by: ListReflectionsTriggeredBy | Unset = UNSET,
    limit: int | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsReflectionListResponse]:
    """ List consolidation runs

     Returns memory consolidation runs, newest first. Each names the digests it read, the collection it
    updated, and the session that ran it -- streaming that session shows the consolidation reasoning in
    real time, because it is an ordinary agent session.

    Args:
        agent_id (str | Unset): Only runs for this agent.
        status (ListReflectionsStatus | Unset): Only runs in this state.
        triggered_by (ListReflectionsTriggeredBy | Unset): Only runs started this way.
        limit (int | Unset): Maximum runs to return. Defaults to 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsReflectionListResponse]
     """


    kwargs = _get_kwargs(
        agent_id=agent_id,
status=status,
triggered_by=triggered_by,
limit=limit,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    agent_id: str | Unset = UNSET,
    status: ListReflectionsStatus | Unset = UNSET,
    triggered_by: ListReflectionsTriggeredBy | Unset = UNSET,
    limit: int | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsReflectionListResponse | None:
    """ List consolidation runs

     Returns memory consolidation runs, newest first. Each names the digests it read, the collection it
    updated, and the session that ran it -- streaming that session shows the consolidation reasoning in
    real time, because it is an ordinary agent session.

    Args:
        agent_id (str | Unset): Only runs for this agent.
        status (ListReflectionsStatus | Unset): Only runs in this state.
        triggered_by (ListReflectionsTriggeredBy | Unset): Only runs started this way.
        limit (int | Unset): Maximum runs to return. Defaults to 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsReflectionListResponse
     """


    return (await asyncio_detailed(
        client=client,
agent_id=agent_id,
status=status,
triggered_by=triggered_by,
limit=limit,

    )).parsed
