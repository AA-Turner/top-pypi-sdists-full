from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.reviewer_profile_o_enum import ReviewerProfileOEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    expertise_category_uuid: Union[Unset, UUID] = UNSET,
    expertise_keyword: Union[Unset, str] = UNSET,
    has_orcid: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[ReviewerProfileOEnum]] = UNSET,
    orcid_id: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user_email: Union[Unset, str] = UNSET,
    user_name: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_expertise_category_uuid: Union[Unset, str] = UNSET
    if not isinstance(expertise_category_uuid, Unset):
        json_expertise_category_uuid = str(expertise_category_uuid)
    params["expertise_category_uuid"] = json_expertise_category_uuid

    params["expertise_keyword"] = expertise_keyword

    params["has_orcid"] = has_orcid

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["orcid_id"] = orcid_id

    params["page"] = page

    params["page_size"] = page_size

    params["user_email"] = user_email

    params["user_name"] = user_name

    json_user_uuid: Union[Unset, str] = UNSET
    if not isinstance(user_uuid, Unset):
        json_user_uuid = str(user_uuid)
    params["user_uuid"] = json_user_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/reviewer-profiles/",
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
    expertise_category_uuid: Union[Unset, UUID] = UNSET,
    expertise_keyword: Union[Unset, str] = UNSET,
    has_orcid: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[ReviewerProfileOEnum]] = UNSET,
    orcid_id: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user_email: Union[Unset, str] = UNSET,
    user_name: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        expertise_category_uuid (Union[Unset, UUID]):
        expertise_keyword (Union[Unset, str]):
        has_orcid (Union[Unset, bool]):
        o (Union[Unset, list[ReviewerProfileOEnum]]):
        orcid_id (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        user_email (Union[Unset, str]):
        user_name (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        expertise_category_uuid=expertise_category_uuid,
        expertise_keyword=expertise_keyword,
        has_orcid=has_orcid,
        o=o,
        orcid_id=orcid_id,
        page=page,
        page_size=page_size,
        user_email=user_email,
        user_name=user_name,
        user_uuid=user_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    expertise_category_uuid: Union[Unset, UUID] = UNSET,
    expertise_keyword: Union[Unset, str] = UNSET,
    has_orcid: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[ReviewerProfileOEnum]] = UNSET,
    orcid_id: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user_email: Union[Unset, str] = UNSET,
    user_name: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        expertise_category_uuid (Union[Unset, UUID]):
        expertise_keyword (Union[Unset, str]):
        has_orcid (Union[Unset, bool]):
        o (Union[Unset, list[ReviewerProfileOEnum]]):
        orcid_id (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        user_email (Union[Unset, str]):
        user_name (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        expertise_category_uuid=expertise_category_uuid,
        expertise_keyword=expertise_keyword,
        has_orcid=has_orcid,
        o=o,
        orcid_id=orcid_id,
        page=page,
        page_size=page_size,
        user_email=user_email,
        user_name=user_name,
        user_uuid=user_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    expertise_category_uuid: Union[Unset, UUID] = UNSET,
    expertise_keyword: Union[Unset, str] = UNSET,
    has_orcid: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[ReviewerProfileOEnum]] = UNSET,
    orcid_id: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user_email: Union[Unset, str] = UNSET,
    user_name: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        expertise_category_uuid (Union[Unset, UUID]):
        expertise_keyword (Union[Unset, str]):
        has_orcid (Union[Unset, bool]):
        o (Union[Unset, list[ReviewerProfileOEnum]]):
        orcid_id (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        user_email (Union[Unset, str]):
        user_name (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        expertise_category_uuid=expertise_category_uuid,
        expertise_keyword=expertise_keyword,
        has_orcid=has_orcid,
        o=o,
        orcid_id=orcid_id,
        page=page,
        page_size=page_size,
        user_email=user_email,
        user_name=user_name,
        user_uuid=user_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    expertise_category_uuid: Union[Unset, UUID] = UNSET,
    expertise_keyword: Union[Unset, str] = UNSET,
    has_orcid: Union[Unset, bool] = UNSET,
    o: Union[Unset, list[ReviewerProfileOEnum]] = UNSET,
    orcid_id: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    user_email: Union[Unset, str] = UNSET,
    user_name: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        expertise_category_uuid (Union[Unset, UUID]):
        expertise_keyword (Union[Unset, str]):
        has_orcid (Union[Unset, bool]):
        o (Union[Unset, list[ReviewerProfileOEnum]]):
        orcid_id (Union[Unset, str]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        user_email (Union[Unset, str]):
        user_name (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            expertise_category_uuid=expertise_category_uuid,
            expertise_keyword=expertise_keyword,
            has_orcid=has_orcid,
            o=o,
            orcid_id=orcid_id,
            page=page,
            page_size=page_size,
            user_email=user_email,
            user_name=user_name,
            user_uuid=user_uuid,
        )
    ).parsed
