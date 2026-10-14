from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.resource_api_key_status import ResourceApiKeyStatus
from ...models.resource_api_key_usage_request import ResourceApiKeyUsageRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: ResourceApiKeyUsageRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-resource-api-keys/{uuid}/report_usage/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ResourceApiKeyStatus:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ResourceApiKeyStatus.from_dict(response.json())

        return response_200
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
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: ResourceApiKeyUsageRequest,
) -> Response[ResourceApiKeyStatus]:
    """Report API key usage

     Used by the site agent to report a key's usage so far in a month, per component type. Merged into
    the key's usage for that month; a later month replaces it, and an earlier one is refused. A key
    whose usage reaches its limit is paused, and a key paused for its limit is resumed once under it
    again. Accepted for a deleted key too.

    Args:
        uuid (UUID):
        body (ResourceApiKeyUsageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResourceApiKeyStatus]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: ResourceApiKeyUsageRequest,
) -> ResourceApiKeyStatus:
    """Report API key usage

     Used by the site agent to report a key's usage so far in a month, per component type. Merged into
    the key's usage for that month; a later month replaces it, and an earlier one is refused. A key
    whose usage reaches its limit is paused, and a key paused for its limit is resumed once under it
    again. Accepted for a deleted key too.

    Args:
        uuid (UUID):
        body (ResourceApiKeyUsageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResourceApiKeyStatus
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: ResourceApiKeyUsageRequest,
) -> Response[ResourceApiKeyStatus]:
    """Report API key usage

     Used by the site agent to report a key's usage so far in a month, per component type. Merged into
    the key's usage for that month; a later month replaces it, and an earlier one is refused. A key
    whose usage reaches its limit is paused, and a key paused for its limit is resumed once under it
    again. Accepted for a deleted key too.

    Args:
        uuid (UUID):
        body (ResourceApiKeyUsageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResourceApiKeyStatus]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: ResourceApiKeyUsageRequest,
) -> ResourceApiKeyStatus:
    """Report API key usage

     Used by the site agent to report a key's usage so far in a month, per component type. Merged into
    the key's usage for that month; a later month replaces it, and an earlier one is refused. A key
    whose usage reaches its limit is paused, and a key paused for its limit is resumed once under it
    again. Accepted for a deleted key too.

    Args:
        uuid (UUID):
        body (ResourceApiKeyUsageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResourceApiKeyStatus
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
