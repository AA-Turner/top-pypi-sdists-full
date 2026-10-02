from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.get_sandbox_provider_status_provider import GetSandboxProviderStatusProvider
from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_sandbox_provider_status import ManagedAgentsSandboxProviderStatus
from typing import cast



def _get_kwargs(
    provider: GetSandboxProviderStatusProvider,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/sandbox-providers/{provider}/status".format(provider=quote(str(provider), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSandboxProviderStatus | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsSandboxProviderStatus.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = ManagedAgentsApiError.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = ManagedAgentsApiError.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = ManagedAgentsApiError.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSandboxProviderStatus]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    provider: GetSandboxProviderStatusProvider,
    *,
    client: AuthenticatedClient | Client,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSandboxProviderStatus]:
    """ Check sandbox provider connectivity

     Performs a live connectivity check against a deployment-owned sandbox provider and returns
    connected, misconfigured, unauthorized, or unavailable with an operator-facing message. Connectivity
    status exists only for the runs provider; any other provider id is a 400. No billable compute is
    provisioned, and no endpoint or credential material is returned. Reachable with an API key through
    this API, which authorizes the caller and then calls the upstream service with its own credential.
    The upstream operation is not callable with a customer key directly.

    Args:
        provider (GetSandboxProviderStatusProvider): Sandbox provider id, as reported by
            listSandboxProviders. Connectivity status exists only for runs; the others return 400.
            self_hosted is retired but accepted for historical queries.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSandboxProviderStatus]
     """


    kwargs = _get_kwargs(
        provider=provider,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    provider: GetSandboxProviderStatusProvider,
    *,
    client: AuthenticatedClient | Client,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSandboxProviderStatus | None:
    """ Check sandbox provider connectivity

     Performs a live connectivity check against a deployment-owned sandbox provider and returns
    connected, misconfigured, unauthorized, or unavailable with an operator-facing message. Connectivity
    status exists only for the runs provider; any other provider id is a 400. No billable compute is
    provisioned, and no endpoint or credential material is returned. Reachable with an API key through
    this API, which authorizes the caller and then calls the upstream service with its own credential.
    The upstream operation is not callable with a customer key directly.

    Args:
        provider (GetSandboxProviderStatusProvider): Sandbox provider id, as reported by
            listSandboxProviders. Connectivity status exists only for runs; the others return 400.
            self_hosted is retired but accepted for historical queries.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSandboxProviderStatus
     """


    return sync_detailed(
        provider=provider,
client=client,

    ).parsed

async def asyncio_detailed(
    provider: GetSandboxProviderStatusProvider,
    *,
    client: AuthenticatedClient | Client,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSandboxProviderStatus]:
    """ Check sandbox provider connectivity

     Performs a live connectivity check against a deployment-owned sandbox provider and returns
    connected, misconfigured, unauthorized, or unavailable with an operator-facing message. Connectivity
    status exists only for the runs provider; any other provider id is a 400. No billable compute is
    provisioned, and no endpoint or credential material is returned. Reachable with an API key through
    this API, which authorizes the caller and then calls the upstream service with its own credential.
    The upstream operation is not callable with a customer key directly.

    Args:
        provider (GetSandboxProviderStatusProvider): Sandbox provider id, as reported by
            listSandboxProviders. Connectivity status exists only for runs; the others return 400.
            self_hosted is retired but accepted for historical queries.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSandboxProviderStatus]
     """


    kwargs = _get_kwargs(
        provider=provider,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    provider: GetSandboxProviderStatusProvider,
    *,
    client: AuthenticatedClient | Client,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSandboxProviderStatus | None:
    """ Check sandbox provider connectivity

     Performs a live connectivity check against a deployment-owned sandbox provider and returns
    connected, misconfigured, unauthorized, or unavailable with an operator-facing message. Connectivity
    status exists only for the runs provider; any other provider id is a 400. No billable compute is
    provisioned, and no endpoint or credential material is returned. Reachable with an API key through
    this API, which authorizes the caller and then calls the upstream service with its own credential.
    The upstream operation is not callable with a customer key directly.

    Args:
        provider (GetSandboxProviderStatusProvider): Sandbox provider id, as reported by
            listSandboxProviders. Connectivity status exists only for runs; the others return 400.
            self_hosted is retired but accepted for historical queries.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSandboxProviderStatus
     """


    return (await asyncio_detailed(
        provider=provider,
client=client,

    )).parsed
