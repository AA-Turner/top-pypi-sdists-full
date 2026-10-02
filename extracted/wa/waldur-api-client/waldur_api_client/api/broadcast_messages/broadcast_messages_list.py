from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.broadcast_message import BroadcastMessage
from ...models.broadcast_message_field_enum import BroadcastMessageFieldEnum
from ...models.broadcast_message_o_enum import BroadcastMessageOEnum
from ...models.broadcast_message_state_enum import BroadcastMessageStateEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    field: Union[Unset, list[BroadcastMessageFieldEnum]] = UNSET,
    o: Union[Unset, list[BroadcastMessageOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, BroadcastMessageStateEnum] = UNSET,
    subject: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_field: Union[Unset, list[str]] = UNSET
    if not isinstance(field, Unset):
        json_field = []
        for field_item_data in field:
            field_item = field_item_data.value
            json_field.append(field_item)

    params["field"] = json_field

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    json_state: Union[Unset, str] = UNSET
    if not isinstance(state, Unset):
        json_state = state.value

    params["state"] = json_state

    params["subject"] = subject

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/broadcast-messages/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["BroadcastMessage"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = BroadcastMessage.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["BroadcastMessage"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[BroadcastMessageFieldEnum]] = UNSET,
    o: Union[Unset, list[BroadcastMessageOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, BroadcastMessageStateEnum] = UNSET,
    subject: Union[Unset, str] = UNSET,
) -> Response[list["BroadcastMessage"]]:
    """
    Args:
        field (Union[Unset, list[BroadcastMessageFieldEnum]]):
        o (Union[Unset, list[BroadcastMessageOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, BroadcastMessageStateEnum]):
        subject (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['BroadcastMessage']]
    """

    kwargs = _get_kwargs(
        field=field,
        o=o,
        page=page,
        page_size=page_size,
        state=state,
        subject=subject,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[BroadcastMessageFieldEnum]] = UNSET,
    o: Union[Unset, list[BroadcastMessageOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, BroadcastMessageStateEnum] = UNSET,
    subject: Union[Unset, str] = UNSET,
) -> list["BroadcastMessage"]:
    """
    Args:
        field (Union[Unset, list[BroadcastMessageFieldEnum]]):
        o (Union[Unset, list[BroadcastMessageOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, BroadcastMessageStateEnum]):
        subject (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['BroadcastMessage']
    """

    return sync_detailed(
        client=client,
        field=field,
        o=o,
        page=page,
        page_size=page_size,
        state=state,
        subject=subject,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[BroadcastMessageFieldEnum]] = UNSET,
    o: Union[Unset, list[BroadcastMessageOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, BroadcastMessageStateEnum] = UNSET,
    subject: Union[Unset, str] = UNSET,
) -> Response[list["BroadcastMessage"]]:
    """
    Args:
        field (Union[Unset, list[BroadcastMessageFieldEnum]]):
        o (Union[Unset, list[BroadcastMessageOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, BroadcastMessageStateEnum]):
        subject (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['BroadcastMessage']]
    """

    kwargs = _get_kwargs(
        field=field,
        o=o,
        page=page,
        page_size=page_size,
        state=state,
        subject=subject,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[BroadcastMessageFieldEnum]] = UNSET,
    o: Union[Unset, list[BroadcastMessageOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    state: Union[Unset, BroadcastMessageStateEnum] = UNSET,
    subject: Union[Unset, str] = UNSET,
) -> list["BroadcastMessage"]:
    """
    Args:
        field (Union[Unset, list[BroadcastMessageFieldEnum]]):
        o (Union[Unset, list[BroadcastMessageOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        state (Union[Unset, BroadcastMessageStateEnum]):
        subject (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['BroadcastMessage']
    """

    return (
        await asyncio_detailed(
            client=client,
            field=field,
            o=o,
            page=page,
            page_size=page_size,
            state=state,
            subject=subject,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[BroadcastMessageFieldEnum]] = UNSET,
    o: Union[Unset, list[BroadcastMessageOEnum]] = UNSET,
    state: Union[Unset, BroadcastMessageStateEnum] = UNSET,
    subject: Union[Unset, str] = UNSET,
) -> list["BroadcastMessage"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        field (Union[Unset, list[BroadcastMessageFieldEnum]]):
        o (Union[Unset, list[BroadcastMessageOEnum]]):
        state (Union[Unset, BroadcastMessageStateEnum]):
        subject (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['BroadcastMessage']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[BroadcastMessage] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        field=field,
        o=o,
        state=state,
        subject=subject,
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
    field: Union[Unset, list[BroadcastMessageFieldEnum]] = UNSET,
    o: Union[Unset, list[BroadcastMessageOEnum]] = UNSET,
    state: Union[Unset, BroadcastMessageStateEnum] = UNSET,
    subject: Union[Unset, str] = UNSET,
) -> list["BroadcastMessage"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        field (Union[Unset, list[BroadcastMessageFieldEnum]]):
        o (Union[Unset, list[BroadcastMessageOEnum]]):
        state (Union[Unset, BroadcastMessageStateEnum]):
        subject (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['BroadcastMessage']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[BroadcastMessage] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        field=field,
        o=o,
        state=state,
        subject=subject,
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
