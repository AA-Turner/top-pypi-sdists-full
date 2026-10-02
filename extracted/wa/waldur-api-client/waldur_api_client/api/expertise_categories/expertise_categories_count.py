from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.expertise_category_o_enum import ExpertiseCategoryOEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    code: Union[Unset, str] = UNSET,
    level: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ExpertiseCategoryOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["code"] = code

    params["level"] = level

    params["name"] = name

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    json_parent_uuid: Union[Unset, str] = UNSET
    if not isinstance(parent_uuid, Unset):
        json_parent_uuid = str(parent_uuid)
    params["parent_uuid"] = json_parent_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/expertise-categories/",
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
    code: Union[Unset, str] = UNSET,
    level: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ExpertiseCategoryOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        code (Union[Unset, str]):
        level (Union[Unset, int]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ExpertiseCategoryOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        code=code,
        level=level,
        name=name,
        o=o,
        page=page,
        page_size=page_size,
        parent_uuid=parent_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    code: Union[Unset, str] = UNSET,
    level: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ExpertiseCategoryOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        code (Union[Unset, str]):
        level (Union[Unset, int]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ExpertiseCategoryOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        code=code,
        level=level,
        name=name,
        o=o,
        page=page,
        page_size=page_size,
        parent_uuid=parent_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    code: Union[Unset, str] = UNSET,
    level: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ExpertiseCategoryOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        code (Union[Unset, str]):
        level (Union[Unset, int]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ExpertiseCategoryOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        code=code,
        level=level,
        name=name,
        o=o,
        page=page,
        page_size=page_size,
        parent_uuid=parent_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    code: Union[Unset, str] = UNSET,
    level: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[ExpertiseCategoryOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    parent_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        code (Union[Unset, str]):
        level (Union[Unset, int]):
        name (Union[Unset, str]):
        o (Union[Unset, list[ExpertiseCategoryOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        parent_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            code=code,
            level=level,
            name=name,
            o=o,
            page=page,
            page_size=page_size,
            parent_uuid=parent_uuid,
        )
    ).parsed
