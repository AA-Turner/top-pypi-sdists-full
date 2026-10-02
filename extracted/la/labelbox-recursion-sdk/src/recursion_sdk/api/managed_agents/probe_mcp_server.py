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
from ...models.managed_agents_api_error_not_found import ManagedAgentsApiErrorNotFound
from ...models.managed_agents_api_error_unsupported_media_type import ManagedAgentsApiErrorUnsupportedMediaType
from ...models.managed_agents_mcp_probe_response import ManagedAgentsMCPProbeResponse
from ...models.managed_agents_probe_mcp_server_request import ManagedAgentsProbeMCPServerRequest
from typing import cast



def _get_kwargs(
    *,
    body: ManagedAgentsProbeMCPServerRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/managed-agents/v1/mcp/probe",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMCPProbeResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsMCPProbeResponse.from_dict(response.json())



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

    if response.status_code == 409:
        response_409 = ManagedAgentsApiError.from_dict(response.json())



        return response_409

    if response.status_code == 413:
        response_413 = ManagedAgentsApiError.from_dict(response.json())



        return response_413

    if response.status_code == 415:
        response_415 = ManagedAgentsApiErrorUnsupportedMediaType.from_dict(response.json())



        return response_415

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMCPProbeResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsProbeMCPServerRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMCPProbeResponse]:
    """ Test an MCP server connection and list its tools

     Opens a live connection to an MCP server using exactly the credential resolution a session would
    use, and returns the tools it advertises. A server that cannot be reached or authenticated is still
    HTTP 200 with ok=false, so inspect that field rather than relying on the status code. Pass vault_ids
    to probe authenticated; omit them to probe anonymously.

    Args:
        body (ManagedAgentsProbeMCPServerRequest): Request body for a live connection test against
            an MCP server, running the same credential resolution a session would. An unreachable
            server is reported in the response body, not as an HTTP error. Example: {'server_url':
            'https://example.com', 'vault_ids': ['example']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMCPProbeResponse]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsProbeMCPServerRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMCPProbeResponse | None:
    """ Test an MCP server connection and list its tools

     Opens a live connection to an MCP server using exactly the credential resolution a session would
    use, and returns the tools it advertises. A server that cannot be reached or authenticated is still
    HTTP 200 with ok=false, so inspect that field rather than relying on the status code. Pass vault_ids
    to probe authenticated; omit them to probe anonymously.

    Args:
        body (ManagedAgentsProbeMCPServerRequest): Request body for a live connection test against
            an MCP server, running the same credential resolution a session would. An unreachable
            server is reported in the response body, not as an HTTP error. Example: {'server_url':
            'https://example.com', 'vault_ids': ['example']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMCPProbeResponse
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsProbeMCPServerRequest,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMCPProbeResponse]:
    """ Test an MCP server connection and list its tools

     Opens a live connection to an MCP server using exactly the credential resolution a session would
    use, and returns the tools it advertises. A server that cannot be reached or authenticated is still
    HTTP 200 with ok=false, so inspect that field rather than relying on the status code. Pass vault_ids
    to probe authenticated; omit them to probe anonymously.

    Args:
        body (ManagedAgentsProbeMCPServerRequest): Request body for a live connection test against
            an MCP server, running the same credential resolution a session would. An unreachable
            server is reported in the response body, not as an HTTP error. Example: {'server_url':
            'https://example.com', 'vault_ids': ['example']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMCPProbeResponse]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: ManagedAgentsProbeMCPServerRequest,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMCPProbeResponse | None:
    """ Test an MCP server connection and list its tools

     Opens a live connection to an MCP server using exactly the credential resolution a session would
    use, and returns the tools it advertises. A server that cannot be reached or authenticated is still
    HTTP 200 with ok=false, so inspect that field rather than relying on the status code. Pass vault_ids
    to probe authenticated; omit them to probe anonymously.

    Args:
        body (ManagedAgentsProbeMCPServerRequest): Request body for a live connection test against
            an MCP server, running the same credential resolution a session would. An unreachable
            server is reported in the response body, not as an HTTP error. Example: {'server_url':
            'https://example.com', 'vault_ids': ['example']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsApiErrorNotFound | ManagedAgentsApiErrorUnsupportedMediaType | ManagedAgentsMCPProbeResponse
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
