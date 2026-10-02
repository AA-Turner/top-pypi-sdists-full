from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_forbidden import ManagedAgentsApiErrorForbidden
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_environment_setup_run_list_response import ManagedAgentsEnvironmentSetupRunListResponse
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    environment_id: UUID,
    *,
    limit: int | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/environments/{environment_id}/setup-runs".format(environment_id=quote(str(environment_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRunListResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsEnvironmentSetupRunListResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRunListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRunListResponse]:
    """ List setup runs

     Returns the environment's recent setup runs, newest first, manual and session-triggered alike. The
    newest manual run is the one the environment's setup_verification describes; a session run records
    what happened when a session provisioned, so a session that failed in setup can be read here by its
    session_id.

    Args:
        environment_id (UUID): Environment id (UUID).
        limit (int | Unset): Maximum runs to return, newest first. Defaults to 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRunListResponse]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
limit=limit,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRunListResponse | None:
    """ List setup runs

     Returns the environment's recent setup runs, newest first, manual and session-triggered alike. The
    newest manual run is the one the environment's setup_verification describes; a session run records
    what happened when a session provisioned, so a session that failed in setup can be read here by its
    session_id.

    Args:
        environment_id (UUID): Environment id (UUID).
        limit (int | Unset): Maximum runs to return, newest first. Defaults to 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRunListResponse
     """


    return sync_detailed(
        environment_id=environment_id,
client=client,
limit=limit,

    ).parsed

async def asyncio_detailed(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRunListResponse]:
    """ List setup runs

     Returns the environment's recent setup runs, newest first, manual and session-triggered alike. The
    newest manual run is the one the environment's setup_verification describes; a session run records
    what happened when a session provisioned, so a session that failed in setup can be read here by its
    session_id.

    Args:
        environment_id (UUID): Environment id (UUID).
        limit (int | Unset): Maximum runs to return, newest first. Defaults to 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRunListResponse]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
limit=limit,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    environment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRunListResponse | None:
    """ List setup runs

     Returns the environment's recent setup runs, newest first, manual and session-triggered alike. The
    newest manual run is the one the environment's setup_verification describes; a session run records
    what happened when a session provisioned, so a session that failed in setup can be read here by its
    session_id.

    Args:
        environment_id (UUID): Environment id (UUID).
        limit (int | Unset): Maximum runs to return, newest first. Defaults to 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRunListResponse
     """


    return (await asyncio_detailed(
        environment_id=environment_id,
client=client,
limit=limit,

    )).parsed
