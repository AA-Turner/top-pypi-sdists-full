from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_guest_entry_by_custom_path_response_200 import GetGuestEntryByCustomPathResponse200
from ...types import Response


def _get_kwargs(
    custom_path: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/apps_u/guest_entry_by_custom_path/{custom_path}".format(
            custom_path=custom_path,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetGuestEntryByCustomPathResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetGuestEntryByCustomPathResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetGuestEntryByCustomPathResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    custom_path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[GetGuestEntryByCustomPathResponse200]:
    """whether the app behind a custom path admits guests

     The custom-path counterpart of `getGuestEntry`. Unauthenticated; 404 unless the app's execution mode
    is `guest` AND its workspace has `guest_access_enabled` AND the instance has not set
    `guest_access_disabled`. Returns the workspace too, since a custom URL may not carry it.

    Args:
        custom_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetGuestEntryByCustomPathResponse200]
    """

    kwargs = _get_kwargs(
        custom_path=custom_path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    custom_path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[GetGuestEntryByCustomPathResponse200]:
    """whether the app behind a custom path admits guests

     The custom-path counterpart of `getGuestEntry`. Unauthenticated; 404 unless the app's execution mode
    is `guest` AND its workspace has `guest_access_enabled` AND the instance has not set
    `guest_access_disabled`. Returns the workspace too, since a custom URL may not carry it.

    Args:
        custom_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetGuestEntryByCustomPathResponse200
    """

    return sync_detailed(
        custom_path=custom_path,
        client=client,
    ).parsed


async def asyncio_detailed(
    custom_path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[GetGuestEntryByCustomPathResponse200]:
    """whether the app behind a custom path admits guests

     The custom-path counterpart of `getGuestEntry`. Unauthenticated; 404 unless the app's execution mode
    is `guest` AND its workspace has `guest_access_enabled` AND the instance has not set
    `guest_access_disabled`. Returns the workspace too, since a custom URL may not carry it.

    Args:
        custom_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetGuestEntryByCustomPathResponse200]
    """

    kwargs = _get_kwargs(
        custom_path=custom_path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    custom_path: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[GetGuestEntryByCustomPathResponse200]:
    """whether the app behind a custom path admits guests

     The custom-path counterpart of `getGuestEntry`. Unauthenticated; 404 unless the app's execution mode
    is `guest` AND its workspace has `guest_access_enabled` AND the instance has not set
    `guest_access_disabled`. Returns the workspace too, since a custom URL may not carry it.

    Args:
        custom_path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetGuestEntryByCustomPathResponse200
    """

    return (
        await asyncio_detailed(
            custom_path=custom_path,
            client=client,
        )
    ).parsed
