from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.live_kit_participant import LiveKitParticipant
from ...types import UNSET, Response
from ...utils import parse_link_header


def _get_kwargs(
    *,
    room: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["room"] = room

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/admin/matrix/livekit/participants/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["LiveKitParticipant"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = LiveKitParticipant.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["LiveKitParticipant"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    room: str,
) -> Response[list["LiveKitParticipant"]]:
    """List participants in a LiveKit room

     Participants and their tracks for a single LiveKit room. Staff only. An unknown or empty room
    returns 200 with an empty list. Returns 503 when LiveKit credentials are not configured and 502 when
    LiveKit is unreachable or rejects the configured credentials.

    Args:
        room (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['LiveKitParticipant']]
    """

    kwargs = _get_kwargs(
        room=room,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    room: str,
) -> list["LiveKitParticipant"]:
    """List participants in a LiveKit room

     Participants and their tracks for a single LiveKit room. Staff only. An unknown or empty room
    returns 200 with an empty list. Returns 503 when LiveKit credentials are not configured and 502 when
    LiveKit is unreachable or rejects the configured credentials.

    Args:
        room (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['LiveKitParticipant']
    """

    return sync_detailed(
        client=client,
        room=room,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    room: str,
) -> Response[list["LiveKitParticipant"]]:
    """List participants in a LiveKit room

     Participants and their tracks for a single LiveKit room. Staff only. An unknown or empty room
    returns 200 with an empty list. Returns 503 when LiveKit credentials are not configured and 502 when
    LiveKit is unreachable or rejects the configured credentials.

    Args:
        room (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['LiveKitParticipant']]
    """

    kwargs = _get_kwargs(
        room=room,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    room: str,
) -> list["LiveKitParticipant"]:
    """List participants in a LiveKit room

     Participants and their tracks for a single LiveKit room. Staff only. An unknown or empty room
    returns 200 with an empty list. Returns 503 when LiveKit credentials are not configured and 502 when
    LiveKit is unreachable or rejects the configured credentials.

    Args:
        room (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['LiveKitParticipant']
    """

    return (
        await asyncio_detailed(
            client=client,
            room=room,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    room: str,
) -> list["LiveKitParticipant"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        room (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['LiveKitParticipant']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[LiveKitParticipant] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        room=room,
    )

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = client.get_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = client.get_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results


async def asyncio_all(
    *,
    client: AuthenticatedClient,
    room: str,
) -> list["LiveKitParticipant"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        room (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['LiveKitParticipant']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[LiveKitParticipant] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        room=room,
    )

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = await client.get_async_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = await client.get_async_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results
