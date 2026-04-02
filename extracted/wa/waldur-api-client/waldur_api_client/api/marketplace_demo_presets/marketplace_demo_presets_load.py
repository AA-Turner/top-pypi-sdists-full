from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.demo_preset_load_request_request import DemoPresetLoadRequestRequest
from ...models.demo_preset_load_response import DemoPresetLoadResponse
from ...types import Response


def _get_kwargs(
    name: str,
    *,
    body: DemoPresetLoadRequestRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-demo-presets/load/{name}/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Any, DemoPresetLoadResponse]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = DemoPresetLoadResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, DemoPresetLoadResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: str,
    *,
    client: AuthenticatedClient,
    body: DemoPresetLoadRequestRequest,
) -> Response[Union[Any, DemoPresetLoadResponse]]:
    """Load demo preset

     Load a demo preset into the database. This operation will optionally clean up existing data before
    loading. Staff access only.

    Args:
        name (str):
        body (DemoPresetLoadRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DemoPresetLoadResponse]]
    """

    kwargs = _get_kwargs(
        name=name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient,
    body: DemoPresetLoadRequestRequest,
) -> Union[Any, DemoPresetLoadResponse]:
    """Load demo preset

     Load a demo preset into the database. This operation will optionally clean up existing data before
    loading. Staff access only.

    Args:
        name (str):
        body (DemoPresetLoadRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DemoPresetLoadResponse]
    """

    return sync_detailed(
        name=name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient,
    body: DemoPresetLoadRequestRequest,
) -> Response[Union[Any, DemoPresetLoadResponse]]:
    """Load demo preset

     Load a demo preset into the database. This operation will optionally clean up existing data before
    loading. Staff access only.

    Args:
        name (str):
        body (DemoPresetLoadRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DemoPresetLoadResponse]]
    """

    kwargs = _get_kwargs(
        name=name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient,
    body: DemoPresetLoadRequestRequest,
) -> Union[Any, DemoPresetLoadResponse]:
    """Load demo preset

     Load a demo preset into the database. This operation will optionally clean up existing data before
    loading. Staff access only.

    Args:
        name (str):
        body (DemoPresetLoadRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DemoPresetLoadResponse]
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            body=body,
        )
    ).parsed
