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
from ...models.managed_agents_environment_setup_run import ManagedAgentsEnvironmentSetupRun
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    environment_id: UUID,
    setup_run_id: UUID,
    *,
    wait_seconds: int | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["wait_seconds"] = wait_seconds


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/environments/{environment_id}/setup-runs/{setup_run_id}".format(environment_id=quote(str(environment_id), safe=""),setup_run_id=quote(str(setup_run_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRun | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsEnvironmentSetupRun.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRun]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    environment_id: UUID,
    setup_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    wait_seconds: int | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRun]:
    """ Get a setup run, optionally waiting for it to finish

     Returns one setup run. With wait_seconds the call blocks until the run reaches a terminal status or
    the wait elapses, so a poll loop needs no client-side timer. next_action names the call to make on
    the result: poll again, read the log, or start a session.

    Args:
        environment_id (UUID): Environment id (UUID).
        setup_run_id (UUID): Setup run id as returned by createEnvironmentSetupRun or the
            environment's setup_verification.active_setup_run_id.
        wait_seconds (int | Unset): Block up to this many seconds for the run to reach succeeded,
            failed, or cancelled before responding. The server caps the wait at 5 seconds; larger
            values are accepted and clamped. 0 (the default) returns immediately and is recommended
            through the public API: sleep two seconds client-side and repeat to avoid intermediary
            gateway timeouts.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRun]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
setup_run_id=setup_run_id,
wait_seconds=wait_seconds,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    environment_id: UUID,
    setup_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    wait_seconds: int | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRun | None:
    """ Get a setup run, optionally waiting for it to finish

     Returns one setup run. With wait_seconds the call blocks until the run reaches a terminal status or
    the wait elapses, so a poll loop needs no client-side timer. next_action names the call to make on
    the result: poll again, read the log, or start a session.

    Args:
        environment_id (UUID): Environment id (UUID).
        setup_run_id (UUID): Setup run id as returned by createEnvironmentSetupRun or the
            environment's setup_verification.active_setup_run_id.
        wait_seconds (int | Unset): Block up to this many seconds for the run to reach succeeded,
            failed, or cancelled before responding. The server caps the wait at 5 seconds; larger
            values are accepted and clamped. 0 (the default) returns immediately and is recommended
            through the public API: sleep two seconds client-side and repeat to avoid intermediary
            gateway timeouts.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRun
     """


    return sync_detailed(
        environment_id=environment_id,
setup_run_id=setup_run_id,
client=client,
wait_seconds=wait_seconds,

    ).parsed

async def asyncio_detailed(
    environment_id: UUID,
    setup_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    wait_seconds: int | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRun]:
    """ Get a setup run, optionally waiting for it to finish

     Returns one setup run. With wait_seconds the call blocks until the run reaches a terminal status or
    the wait elapses, so a poll loop needs no client-side timer. next_action names the call to make on
    the result: poll again, read the log, or start a session.

    Args:
        environment_id (UUID): Environment id (UUID).
        setup_run_id (UUID): Setup run id as returned by createEnvironmentSetupRun or the
            environment's setup_verification.active_setup_run_id.
        wait_seconds (int | Unset): Block up to this many seconds for the run to reach succeeded,
            failed, or cancelled before responding. The server caps the wait at 5 seconds; larger
            values are accepted and clamped. 0 (the default) returns immediately and is recommended
            through the public API: sleep two seconds client-side and repeat to avoid intermediary
            gateway timeouts.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRun]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
setup_run_id=setup_run_id,
wait_seconds=wait_seconds,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    environment_id: UUID,
    setup_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    wait_seconds: int | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRun | None:
    """ Get a setup run, optionally waiting for it to finish

     Returns one setup run. With wait_seconds the call blocks until the run reaches a terminal status or
    the wait elapses, so a poll loop needs no client-side timer. next_action names the call to make on
    the result: poll again, read the log, or start a session.

    Args:
        environment_id (UUID): Environment id (UUID).
        setup_run_id (UUID): Setup run id as returned by createEnvironmentSetupRun or the
            environment's setup_verification.active_setup_run_id.
        wait_seconds (int | Unset): Block up to this many seconds for the run to reach succeeded,
            failed, or cancelled before responding. The server caps the wait at 5 seconds; larger
            values are accepted and clamped. 0 (the default) returns immediately and is recommended
            through the public API: sleep two seconds client-side and repeat to avoid intermediary
            gateway timeouts.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRun
     """


    return (await asyncio_detailed(
        environment_id=environment_id,
setup_run_id=setup_run_id,
client=client,
wait_seconds=wait_seconds,

    )).parsed
