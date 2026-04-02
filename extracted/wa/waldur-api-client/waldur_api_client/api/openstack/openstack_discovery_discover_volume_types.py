from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.discover_volume_types_request_request import DiscoverVolumeTypesRequestRequest
from ...models.volume_type_response import VolumeTypeResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: DiscoverVolumeTypesRequestRequest,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["page"] = page

    params["page_size"] = page_size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/openstack/discovery/discover_volume_types/",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["VolumeTypeResponse"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = VolumeTypeResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["VolumeTypeResponse"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: DiscoverVolumeTypesRequestRequest,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> Response[list["VolumeTypeResponse"]]:
    """Discover available volume types.

    Args:
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        body (DiscoverVolumeTypesRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VolumeTypeResponse']]
    """

    kwargs = _get_kwargs(
        body=body,
        page=page,
        page_size=page_size,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: DiscoverVolumeTypesRequestRequest,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> list["VolumeTypeResponse"]:
    """Discover available volume types.

    Args:
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        body (DiscoverVolumeTypesRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VolumeTypeResponse']
    """

    return sync_detailed(
        client=client,
        body=body,
        page=page,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: DiscoverVolumeTypesRequestRequest,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> Response[list["VolumeTypeResponse"]]:
    """Discover available volume types.

    Args:
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        body (DiscoverVolumeTypesRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VolumeTypeResponse']]
    """

    kwargs = _get_kwargs(
        body=body,
        page=page,
        page_size=page_size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: DiscoverVolumeTypesRequestRequest,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> list["VolumeTypeResponse"]:
    """Discover available volume types.

    Args:
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        body (DiscoverVolumeTypesRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VolumeTypeResponse']
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            page=page,
            page_size=page_size,
        )
    ).parsed
