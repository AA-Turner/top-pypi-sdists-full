import datetime
from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.email_log import EmailLog
from ...models.email_log_o_enum import EmailLogOEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    body: Union[Unset, str] = UNSET,
    emails: Union[Unset, str] = UNSET,
    o: Union[Unset, list[EmailLogOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    sent_at: Union[Unset, datetime.date] = UNSET,
    subject: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["body"] = body

    params["emails"] = emails

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    json_sent_at: Union[Unset, str] = UNSET
    if not isinstance(sent_at, Unset):
        json_sent_at = sent_at.isoformat()
    params["sent_at"] = json_sent_at

    params["subject"] = subject

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/email-logs/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["EmailLog"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = EmailLog.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["EmailLog"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: Union[Unset, str] = UNSET,
    emails: Union[Unset, str] = UNSET,
    o: Union[Unset, list[EmailLogOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    sent_at: Union[Unset, datetime.date] = UNSET,
    subject: Union[Unset, str] = UNSET,
) -> Response[list["EmailLog"]]:
    """
    Args:
        body (Union[Unset, str]):
        emails (Union[Unset, str]):
        o (Union[Unset, list[EmailLogOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        sent_at (Union[Unset, datetime.date]):
        subject (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['EmailLog']]
    """

    kwargs = _get_kwargs(
        body=body,
        emails=emails,
        o=o,
        page=page,
        page_size=page_size,
        sent_at=sent_at,
        subject=subject,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: Union[Unset, str] = UNSET,
    emails: Union[Unset, str] = UNSET,
    o: Union[Unset, list[EmailLogOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    sent_at: Union[Unset, datetime.date] = UNSET,
    subject: Union[Unset, str] = UNSET,
) -> list["EmailLog"]:
    """
    Args:
        body (Union[Unset, str]):
        emails (Union[Unset, str]):
        o (Union[Unset, list[EmailLogOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        sent_at (Union[Unset, datetime.date]):
        subject (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['EmailLog']
    """

    return sync_detailed(
        client=client,
        body=body,
        emails=emails,
        o=o,
        page=page,
        page_size=page_size,
        sent_at=sent_at,
        subject=subject,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: Union[Unset, str] = UNSET,
    emails: Union[Unset, str] = UNSET,
    o: Union[Unset, list[EmailLogOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    sent_at: Union[Unset, datetime.date] = UNSET,
    subject: Union[Unset, str] = UNSET,
) -> Response[list["EmailLog"]]:
    """
    Args:
        body (Union[Unset, str]):
        emails (Union[Unset, str]):
        o (Union[Unset, list[EmailLogOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        sent_at (Union[Unset, datetime.date]):
        subject (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['EmailLog']]
    """

    kwargs = _get_kwargs(
        body=body,
        emails=emails,
        o=o,
        page=page,
        page_size=page_size,
        sent_at=sent_at,
        subject=subject,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: Union[Unset, str] = UNSET,
    emails: Union[Unset, str] = UNSET,
    o: Union[Unset, list[EmailLogOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    sent_at: Union[Unset, datetime.date] = UNSET,
    subject: Union[Unset, str] = UNSET,
) -> list["EmailLog"]:
    """
    Args:
        body (Union[Unset, str]):
        emails (Union[Unset, str]):
        o (Union[Unset, list[EmailLogOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        sent_at (Union[Unset, datetime.date]):
        subject (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['EmailLog']
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            emails=emails,
            o=o,
            page=page,
            page_size=page_size,
            sent_at=sent_at,
            subject=subject,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    body: Union[Unset, str] = UNSET,
    emails: Union[Unset, str] = UNSET,
    o: Union[Unset, list[EmailLogOEnum]] = UNSET,
    sent_at: Union[Unset, datetime.date] = UNSET,
    subject: Union[Unset, str] = UNSET,
) -> list["EmailLog"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        body (Union[Unset, str]):
        emails (Union[Unset, str]):
        o (Union[Unset, list[EmailLogOEnum]]):
        sent_at (Union[Unset, datetime.date]):
        subject (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['EmailLog']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[EmailLog] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        body=body,
        emails=emails,
        o=o,
        sent_at=sent_at,
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
    body: Union[Unset, str] = UNSET,
    emails: Union[Unset, str] = UNSET,
    o: Union[Unset, list[EmailLogOEnum]] = UNSET,
    sent_at: Union[Unset, datetime.date] = UNSET,
    subject: Union[Unset, str] = UNSET,
) -> list["EmailLog"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        body (Union[Unset, str]):
        emails (Union[Unset, str]):
        o (Union[Unset, list[EmailLogOEnum]]):
        sent_at (Union[Unset, datetime.date]):
        subject (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['EmailLog']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[EmailLog] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        body=body,
        emails=emails,
        o=o,
        sent_at=sent_at,
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
