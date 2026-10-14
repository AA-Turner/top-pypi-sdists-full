from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    probe: Union[Unset, str] = UNSET,
    return_url: Union[Unset, str] = UNSET,
    ui_locales: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["probe"] = probe

    params["return_url"] = return_url

    params["ui_locales"] = ui_locales

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api-auth/default/init/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Any:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 302:
        return None
    if response.status_code == 204:
        return None
    if response.status_code == 404:
        return None
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    probe: Union[Unset, str] = UNSET,
    return_url: Union[Unset, str] = UNSET,
    ui_locales: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """Redirect user to the authorization endpoint of the default identity provider

    Args:
        probe (Union[Unset, str]):
        return_url (Union[Unset, str]):
        ui_locales (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        probe=probe,
        return_url=return_url,
        ui_locales=ui_locales,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    probe: Union[Unset, str] = UNSET,
    return_url: Union[Unset, str] = UNSET,
    ui_locales: Union[Unset, str] = UNSET,
) -> Response[Any]:
    """Redirect user to the authorization endpoint of the default identity provider

    Args:
        probe (Union[Unset, str]):
        return_url (Union[Unset, str]):
        ui_locales (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        probe=probe,
        return_url=return_url,
        ui_locales=ui_locales,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
