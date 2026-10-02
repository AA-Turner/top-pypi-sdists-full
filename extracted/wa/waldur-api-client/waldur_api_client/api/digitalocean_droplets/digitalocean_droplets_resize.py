from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.digital_ocean_droplet_resize_request import DigitalOceanDropletResizeRequest
from ...models.status import Status
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: DigitalOceanDropletResizeRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/digitalocean-droplets/{uuid}/resize/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Status:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 202:
        response_202 = Status.from_dict(response.json())

        return response_202
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Status]:
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
    body: DigitalOceanDropletResizeRequest,
) -> Response[Status]:
    """To resize droplet, submit a POST request to the instance URL, specifying URI of a target size.

    Pass {'disk': true} along with target size in order to perform permanent resizing,
    which allows you to resize your disk space as well as CPU and RAM.
    After increasing the disk size, you will not be able to decrease it.

    Pass {'disk': false} along with target size in order to perform flexible resizing,
    which only upgrades your CPU and RAM. This option is reversible.

    Note that instance must be OFFLINE.

    Args:
        uuid (UUID):
        body (DigitalOceanDropletResizeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Status]
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
    body: DigitalOceanDropletResizeRequest,
) -> Status:
    """To resize droplet, submit a POST request to the instance URL, specifying URI of a target size.

    Pass {'disk': true} along with target size in order to perform permanent resizing,
    which allows you to resize your disk space as well as CPU and RAM.
    After increasing the disk size, you will not be able to decrease it.

    Pass {'disk': false} along with target size in order to perform flexible resizing,
    which only upgrades your CPU and RAM. This option is reversible.

    Note that instance must be OFFLINE.

    Args:
        uuid (UUID):
        body (DigitalOceanDropletResizeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Status
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
    body: DigitalOceanDropletResizeRequest,
) -> Response[Status]:
    """To resize droplet, submit a POST request to the instance URL, specifying URI of a target size.

    Pass {'disk': true} along with target size in order to perform permanent resizing,
    which allows you to resize your disk space as well as CPU and RAM.
    After increasing the disk size, you will not be able to decrease it.

    Pass {'disk': false} along with target size in order to perform flexible resizing,
    which only upgrades your CPU and RAM. This option is reversible.

    Note that instance must be OFFLINE.

    Args:
        uuid (UUID):
        body (DigitalOceanDropletResizeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Status]
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
    body: DigitalOceanDropletResizeRequest,
) -> Status:
    """To resize droplet, submit a POST request to the instance URL, specifying URI of a target size.

    Pass {'disk': true} along with target size in order to perform permanent resizing,
    which allows you to resize your disk space as well as CPU and RAM.
    After increasing the disk size, you will not be able to decrease it.

    Pass {'disk': false} along with target size in order to perform flexible resizing,
    which only upgrades your CPU and RAM. This option is reversible.

    Note that instance must be OFFLINE.

    Args:
        uuid (UUID):
        body (DigitalOceanDropletResizeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Status
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
