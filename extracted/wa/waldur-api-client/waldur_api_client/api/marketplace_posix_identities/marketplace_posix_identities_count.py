from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.posix_identity_consumer_type_enum import PosixIdentityConsumerTypeEnum
from ...models.posix_identity_o_enum import PosixIdentityOEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    consumer_type: Union[Unset, PosixIdentityConsumerTypeEnum] = UNSET,
    gid: Union[Unset, int] = UNSET,
    gid_max: Union[Unset, int] = UNSET,
    gid_min: Union[Unset, int] = UNSET,
    is_released: Union[Unset, bool] = UNSET,
    keyword: Union[Unset, str] = UNSET,
    o: Union[Unset, list[PosixIdentityOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    pool_uuid: Union[Unset, UUID] = UNSET,
    recyclable: Union[Unset, bool] = UNSET,
    uid: Union[Unset, int] = UNSET,
    uid_max: Union[Unset, int] = UNSET,
    uid_min: Union[Unset, int] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_consumer_type: Union[Unset, str] = UNSET
    if not isinstance(consumer_type, Unset):
        json_consumer_type = consumer_type.value

    params["consumer_type"] = json_consumer_type

    params["gid"] = gid

    params["gid_max"] = gid_max

    params["gid_min"] = gid_min

    params["is_released"] = is_released

    params["keyword"] = keyword

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    json_offering_uuid: Union[Unset, str] = UNSET
    if not isinstance(offering_uuid, Unset):
        json_offering_uuid = str(offering_uuid)
    params["offering_uuid"] = json_offering_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_pool_uuid: Union[Unset, str] = UNSET
    if not isinstance(pool_uuid, Unset):
        json_pool_uuid = str(pool_uuid)
    params["pool_uuid"] = json_pool_uuid

    params["recyclable"] = recyclable

    params["uid"] = uid

    params["uid_max"] = uid_max

    params["uid_min"] = uid_min

    json_user_uuid: Union[Unset, str] = UNSET
    if not isinstance(user_uuid, Unset):
        json_user_uuid = str(user_uuid)
    params["user_uuid"] = json_user_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/marketplace-posix-identities/",
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
    consumer_type: Union[Unset, PosixIdentityConsumerTypeEnum] = UNSET,
    gid: Union[Unset, int] = UNSET,
    gid_max: Union[Unset, int] = UNSET,
    gid_min: Union[Unset, int] = UNSET,
    is_released: Union[Unset, bool] = UNSET,
    keyword: Union[Unset, str] = UNSET,
    o: Union[Unset, list[PosixIdentityOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    pool_uuid: Union[Unset, UUID] = UNSET,
    recyclable: Union[Unset, bool] = UNSET,
    uid: Union[Unset, int] = UNSET,
    uid_max: Union[Unset, int] = UNSET,
    uid_min: Union[Unset, int] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        consumer_type (Union[Unset, PosixIdentityConsumerTypeEnum]):
        gid (Union[Unset, int]):
        gid_max (Union[Unset, int]):
        gid_min (Union[Unset, int]):
        is_released (Union[Unset, bool]):
        keyword (Union[Unset, str]):
        o (Union[Unset, list[PosixIdentityOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        pool_uuid (Union[Unset, UUID]):
        recyclable (Union[Unset, bool]):
        uid (Union[Unset, int]):
        uid_max (Union[Unset, int]):
        uid_min (Union[Unset, int]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        consumer_type=consumer_type,
        gid=gid,
        gid_max=gid_max,
        gid_min=gid_min,
        is_released=is_released,
        keyword=keyword,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        pool_uuid=pool_uuid,
        recyclable=recyclable,
        uid=uid,
        uid_max=uid_max,
        uid_min=uid_min,
        user_uuid=user_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    consumer_type: Union[Unset, PosixIdentityConsumerTypeEnum] = UNSET,
    gid: Union[Unset, int] = UNSET,
    gid_max: Union[Unset, int] = UNSET,
    gid_min: Union[Unset, int] = UNSET,
    is_released: Union[Unset, bool] = UNSET,
    keyword: Union[Unset, str] = UNSET,
    o: Union[Unset, list[PosixIdentityOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    pool_uuid: Union[Unset, UUID] = UNSET,
    recyclable: Union[Unset, bool] = UNSET,
    uid: Union[Unset, int] = UNSET,
    uid_max: Union[Unset, int] = UNSET,
    uid_min: Union[Unset, int] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        consumer_type (Union[Unset, PosixIdentityConsumerTypeEnum]):
        gid (Union[Unset, int]):
        gid_max (Union[Unset, int]):
        gid_min (Union[Unset, int]):
        is_released (Union[Unset, bool]):
        keyword (Union[Unset, str]):
        o (Union[Unset, list[PosixIdentityOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        pool_uuid (Union[Unset, UUID]):
        recyclable (Union[Unset, bool]):
        uid (Union[Unset, int]):
        uid_max (Union[Unset, int]):
        uid_min (Union[Unset, int]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        consumer_type=consumer_type,
        gid=gid,
        gid_max=gid_max,
        gid_min=gid_min,
        is_released=is_released,
        keyword=keyword,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        pool_uuid=pool_uuid,
        recyclable=recyclable,
        uid=uid,
        uid_max=uid_max,
        uid_min=uid_min,
        user_uuid=user_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    consumer_type: Union[Unset, PosixIdentityConsumerTypeEnum] = UNSET,
    gid: Union[Unset, int] = UNSET,
    gid_max: Union[Unset, int] = UNSET,
    gid_min: Union[Unset, int] = UNSET,
    is_released: Union[Unset, bool] = UNSET,
    keyword: Union[Unset, str] = UNSET,
    o: Union[Unset, list[PosixIdentityOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    pool_uuid: Union[Unset, UUID] = UNSET,
    recyclable: Union[Unset, bool] = UNSET,
    uid: Union[Unset, int] = UNSET,
    uid_max: Union[Unset, int] = UNSET,
    uid_min: Union[Unset, int] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        consumer_type (Union[Unset, PosixIdentityConsumerTypeEnum]):
        gid (Union[Unset, int]):
        gid_max (Union[Unset, int]):
        gid_min (Union[Unset, int]):
        is_released (Union[Unset, bool]):
        keyword (Union[Unset, str]):
        o (Union[Unset, list[PosixIdentityOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        pool_uuid (Union[Unset, UUID]):
        recyclable (Union[Unset, bool]):
        uid (Union[Unset, int]):
        uid_max (Union[Unset, int]):
        uid_min (Union[Unset, int]):
        user_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        consumer_type=consumer_type,
        gid=gid,
        gid_max=gid_max,
        gid_min=gid_min,
        is_released=is_released,
        keyword=keyword,
        o=o,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        pool_uuid=pool_uuid,
        recyclable=recyclable,
        uid=uid,
        uid_max=uid_max,
        uid_min=uid_min,
        user_uuid=user_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    consumer_type: Union[Unset, PosixIdentityConsumerTypeEnum] = UNSET,
    gid: Union[Unset, int] = UNSET,
    gid_max: Union[Unset, int] = UNSET,
    gid_min: Union[Unset, int] = UNSET,
    is_released: Union[Unset, bool] = UNSET,
    keyword: Union[Unset, str] = UNSET,
    o: Union[Unset, list[PosixIdentityOEnum]] = UNSET,
    offering_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    pool_uuid: Union[Unset, UUID] = UNSET,
    recyclable: Union[Unset, bool] = UNSET,
    uid: Union[Unset, int] = UNSET,
    uid_max: Union[Unset, int] = UNSET,
    uid_min: Union[Unset, int] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        consumer_type (Union[Unset, PosixIdentityConsumerTypeEnum]):
        gid (Union[Unset, int]):
        gid_max (Union[Unset, int]):
        gid_min (Union[Unset, int]):
        is_released (Union[Unset, bool]):
        keyword (Union[Unset, str]):
        o (Union[Unset, list[PosixIdentityOEnum]]):
        offering_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        pool_uuid (Union[Unset, UUID]):
        recyclable (Union[Unset, bool]):
        uid (Union[Unset, int]):
        uid_max (Union[Unset, int]):
        uid_min (Union[Unset, int]):
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
            consumer_type=consumer_type,
            gid=gid,
            gid_max=gid_max,
            gid_min=gid_min,
            is_released=is_released,
            keyword=keyword,
            o=o,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
            pool_uuid=pool_uuid,
            recyclable=recyclable,
            uid=uid,
            uid_max=uid_max,
            uid_min=uid_min,
            user_uuid=user_uuid,
        )
    ).parsed
