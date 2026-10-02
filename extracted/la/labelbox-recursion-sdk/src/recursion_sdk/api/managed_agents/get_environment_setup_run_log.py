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
from ...models.managed_agents_environment_setup_run_log_response import ManagedAgentsEnvironmentSetupRunLogResponse
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    environment_id: UUID,
    setup_run_id: UUID,
    *,
    after: int | Unset = UNSET,
    limit: int | Unset = UNSET,
    wait_seconds: int | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["after"] = after

    params["limit"] = limit

    params["wait_seconds"] = wait_seconds


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/environments/{environment_id}/setup-runs/{setup_run_id}/log".format(environment_id=quote(str(environment_id), safe=""),setup_run_id=quote(str(setup_run_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRunLogResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsEnvironmentSetupRunLogResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRunLogResponse]:
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
    after: int | Unset = UNSET,
    limit: int | Unset = UNSET,
    wait_seconds: int | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRunLogResponse]:
    """ Read or tail a setup run's log

     Returns the run's output after a cursor: stdout and stderr as the script produced them, marker lines
    naming each script line before it runs, and system lines for control-plane phases (provision,
    gpu_check, profile, cleanup). Secrets are redacted before storage. To tail a live run, loop with
    after=next_after and wait_seconds=0, sleeping two seconds client-side, until status is terminal and
    a page comes back empty.

    Args:
        environment_id (UUID): Environment id (UUID).
        setup_run_id (UUID): Setup run id.
        after (int | Unset): Return lines with seq greater than this. Pass the previous response's
            next_after to continue a tail; 0 (the default) starts from the beginning.
        limit (int | Unset): Maximum lines to return. Defaults to 500.
        wait_seconds (int | Unset): When no new lines exist and the run is still going, block up
            to this many seconds for more before responding. The server caps the wait at 5 seconds;
            larger values are accepted and clamped. Through the public API, prefer wait_seconds=0,
            sleep two seconds client-side, and loop with after=next_after until status is terminal.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRunLogResponse]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
setup_run_id=setup_run_id,
after=after,
limit=limit,
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
    after: int | Unset = UNSET,
    limit: int | Unset = UNSET,
    wait_seconds: int | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRunLogResponse | None:
    """ Read or tail a setup run's log

     Returns the run's output after a cursor: stdout and stderr as the script produced them, marker lines
    naming each script line before it runs, and system lines for control-plane phases (provision,
    gpu_check, profile, cleanup). Secrets are redacted before storage. To tail a live run, loop with
    after=next_after and wait_seconds=0, sleeping two seconds client-side, until status is terminal and
    a page comes back empty.

    Args:
        environment_id (UUID): Environment id (UUID).
        setup_run_id (UUID): Setup run id.
        after (int | Unset): Return lines with seq greater than this. Pass the previous response's
            next_after to continue a tail; 0 (the default) starts from the beginning.
        limit (int | Unset): Maximum lines to return. Defaults to 500.
        wait_seconds (int | Unset): When no new lines exist and the run is still going, block up
            to this many seconds for more before responding. The server caps the wait at 5 seconds;
            larger values are accepted and clamped. Through the public API, prefer wait_seconds=0,
            sleep two seconds client-side, and loop with after=next_after until status is terminal.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRunLogResponse
     """


    return sync_detailed(
        environment_id=environment_id,
setup_run_id=setup_run_id,
client=client,
after=after,
limit=limit,
wait_seconds=wait_seconds,

    ).parsed

async def asyncio_detailed(
    environment_id: UUID,
    setup_run_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    after: int | Unset = UNSET,
    limit: int | Unset = UNSET,
    wait_seconds: int | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRunLogResponse]:
    """ Read or tail a setup run's log

     Returns the run's output after a cursor: stdout and stderr as the script produced them, marker lines
    naming each script line before it runs, and system lines for control-plane phases (provision,
    gpu_check, profile, cleanup). Secrets are redacted before storage. To tail a live run, loop with
    after=next_after and wait_seconds=0, sleeping two seconds client-side, until status is terminal and
    a page comes back empty.

    Args:
        environment_id (UUID): Environment id (UUID).
        setup_run_id (UUID): Setup run id.
        after (int | Unset): Return lines with seq greater than this. Pass the previous response's
            next_after to continue a tail; 0 (the default) starts from the beginning.
        limit (int | Unset): Maximum lines to return. Defaults to 500.
        wait_seconds (int | Unset): When no new lines exist and the run is still going, block up
            to this many seconds for more before responding. The server caps the wait at 5 seconds;
            larger values are accepted and clamped. Through the public API, prefer wait_seconds=0,
            sleep two seconds client-side, and loop with after=next_after until status is terminal.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRunLogResponse]
     """


    kwargs = _get_kwargs(
        environment_id=environment_id,
setup_run_id=setup_run_id,
after=after,
limit=limit,
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
    after: int | Unset = UNSET,
    limit: int | Unset = UNSET,
    wait_seconds: int | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRunLogResponse | None:
    """ Read or tail a setup run's log

     Returns the run's output after a cursor: stdout and stderr as the script produced them, marker lines
    naming each script line before it runs, and system lines for control-plane phases (provision,
    gpu_check, profile, cleanup). Secrets are redacted before storage. To tail a live run, loop with
    after=next_after and wait_seconds=0, sleeping two seconds client-side, until status is terminal and
    a page comes back empty.

    Args:
        environment_id (UUID): Environment id (UUID).
        setup_run_id (UUID): Setup run id.
        after (int | Unset): Return lines with seq greater than this. Pass the previous response's
            next_after to continue a tail; 0 (the default) starts from the beginning.
        limit (int | Unset): Maximum lines to return. Defaults to 500.
        wait_seconds (int | Unset): When no new lines exist and the run is still going, block up
            to this many seconds for more before responding. The server caps the wait at 5 seconds;
            larger values are accepted and clamped. Through the public API, prefer wait_seconds=0,
            sleep two seconds client-side, and loop with after=next_after until status is terminal.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsEnvironmentSetupRunLogResponse
     """


    return (await asyncio_detailed(
        environment_id=environment_id,
setup_run_id=setup_run_id,
client=client,
after=after,
limit=limit,
wait_seconds=wait_seconds,

    )).parsed
