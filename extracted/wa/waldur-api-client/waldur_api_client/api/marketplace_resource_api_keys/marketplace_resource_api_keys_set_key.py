from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.resource_api_key_set_key_request import ResourceApiKeySetKeyRequest
from ...models.resource_api_key_status import ResourceApiKeyStatus
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: ResourceApiKeySetKeyRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-resource-api-keys/{uuid}/set_key/",
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
    body: ResourceApiKeySetKeyRequest,
) -> Response[ResourceApiKeyStatus]:
    """Report a rotated API key value

     Used by the site agent after it applied a rotated key. Replaces the stored value and marks the key
    OK.

    Args:
        uuid (UUID):
        body (ResourceApiKeySetKeyRequest):

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
    body: ResourceApiKeySetKeyRequest,
) -> ResourceApiKeyStatus:
    """Report a rotated API key value

     Used by the site agent after it applied a rotated key. Replaces the stored value and marks the key
    OK.

    Args:
        uuid (UUID):
        body (ResourceApiKeySetKeyRequest):

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
    body: ResourceApiKeySetKeyRequest,
) -> Response[ResourceApiKeyStatus]:
    """Report a rotated API key value

     Used by the site agent after it applied a rotated key. Replaces the stored value and marks the key
    OK.

    Args:
        uuid (UUID):
        body (ResourceApiKeySetKeyRequest):

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
    body: ResourceApiKeySetKeyRequest,
) -> ResourceApiKeyStatus:
    """Report a rotated API key value

     Used by the site agent after it applied a rotated key. Replaces the stored value and marks the key
    OK.

    Args:
        uuid (UUID):
        body (ResourceApiKeySetKeyRequest):

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
