import datetime
from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.email_log_o_enum import EmailLogOEnum
from ...types import UNSET, Response, Unset


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
        "method": "head",
        "url": "/api/email-logs/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> int:
    if response.status_code == HTTPStatus.OK:
        try:
            return int(response.headers["x-result-count"])
        except KeyError:
            raise errors.UnexpectedStatus(
                response.status_code,
                b"Expected 'X-Result-Count' header for HEAD request, but it was not found.",
                response.url,
            )
        except ValueError:
            count_val = response.headers.get("x-result-count")
            msg = f"Expected 'X-Result-Count' header to be an integer, but got '{count_val}'."
            raise errors.UnexpectedStatus(response.status_code, msg.encode(), response.url)
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[int]:
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
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

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
        Response[int]
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
) -> int:
    """Get number of items in the collection matching the request parameters.

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
        int
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
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

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
        Response[int]
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
) -> int:
    """Get number of items in the collection matching the request parameters.

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
        int
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
