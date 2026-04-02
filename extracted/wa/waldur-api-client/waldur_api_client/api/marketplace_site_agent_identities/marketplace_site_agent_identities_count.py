import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    last_restarted: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    orphaned: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    version: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_last_restarted: Union[Unset, str] = UNSET
    if not isinstance(last_restarted, Unset):
        json_last_restarted = last_restarted.isoformat()
    params["last_restarted"] = json_last_restarted

    params["name"] = name

    json_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    params["orphaned"] = orphaned

    params["page"] = page

    params["page_size"] = page_size

    params["version"] = version

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/marketplace-site-agent-identities/",
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
    last_restarted: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    orphaned: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    version: Union[Unset, str] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        last_restarted (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        orphaned (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        version (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        last_restarted=last_restarted,
        name=name,
        offering_uuid=offering_uuid,
        orphaned=orphaned,
        page=page,
        page_size=page_size,
        version=version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    last_restarted: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    orphaned: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    version: Union[Unset, str] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        last_restarted (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        orphaned (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        version (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        last_restarted=last_restarted,
        name=name,
        offering_uuid=offering_uuid,
        orphaned=orphaned,
        page=page,
        page_size=page_size,
        version=version,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    last_restarted: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    orphaned: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    version: Union[Unset, str] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        last_restarted (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        orphaned (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        version (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        last_restarted=last_restarted,
        name=name,
        offering_uuid=offering_uuid,
        orphaned=orphaned,
        page=page,
        page_size=page_size,
        version=version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    last_restarted: Union[Unset, datetime.datetime] = UNSET,
    name: Union[Unset, str] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    orphaned: Union[Unset, bool] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    version: Union[Unset, str] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        last_restarted (Union[Unset, datetime.datetime]):
        name (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        orphaned (Union[Unset, bool]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        version (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            last_restarted=last_restarted,
            name=name,
            offering_uuid=offering_uuid,
            orphaned=orphaned,
            page=page,
            page_size=page_size,
            version=version,
        )
    ).parsed
