from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.resource_api_key_report_created_request import ResourceApiKeyReportCreatedRequest
from ...models.resource_api_key_status import ResourceApiKeyStatus
from ...types import Response


def _get_kwargs(
    *,
    body: ResourceApiKeyReportCreatedRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/marketplace-resource-api-keys/report_created/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ResourceApiKeyStatus:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = ResourceApiKeyStatus.from_dict(response.json())

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ResourceApiKeyStatus]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ResourceApiKeyReportCreatedRequest,
) -> Response[ResourceApiKeyStatus]:
    """Report a freshly-applied API key

     Used by the site agent after it generated and applied a key to the backend. Stores the value
    encrypted and marks the key OK.

    Args:
        body (ResourceApiKeyReportCreatedRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResourceApiKeyStatus]
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
    client: AuthenticatedClient,
    body: ResourceApiKeyReportCreatedRequest,
) -> ResourceApiKeyStatus:
    """Report a freshly-applied API key

     Used by the site agent after it generated and applied a key to the backend. Stores the value
    encrypted and marks the key OK.

    Args:
        body (ResourceApiKeyReportCreatedRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResourceApiKeyStatus
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ResourceApiKeyReportCreatedRequest,
) -> Response[ResourceApiKeyStatus]:
    """Report a freshly-applied API key

     Used by the site agent after it generated and applied a key to the backend. Stores the value
    encrypted and marks the key OK.

    Args:
        body (ResourceApiKeyReportCreatedRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResourceApiKeyStatus]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ResourceApiKeyReportCreatedRequest,
) -> ResourceApiKeyStatus:
    """Report a freshly-applied API key

     Used by the site agent after it generated and applied a key to the backend. Stores the value
    encrypted and marks the key OK.

    Args:
        body (ResourceApiKeyReportCreatedRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResourceApiKeyStatus
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
