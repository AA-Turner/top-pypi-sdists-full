from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.system_log_level_enum import SystemLogLevelEnum
from ...models.system_log_o_enum import SystemLogOEnum
from ...models.system_log_source_enum import SystemLogSourceEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    created_from: Union[Unset, float] = UNSET,
    created_to: Union[Unset, float] = UNSET,
    instance: Union[Unset, str] = UNSET,
    level: Union[Unset, SystemLogLevelEnum] = UNSET,
    level_gte: Union[Unset, int] = UNSET,
    logger_name: Union[Unset, str] = UNSET,
    message: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SystemLogOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    source: Union[Unset, SystemLogSourceEnum] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["created_from"] = created_from

    params["created_to"] = created_to

    params["instance"] = instance

    json_level: Union[Unset, str] = UNSET
    if not isinstance(level, Unset):
        json_level = level.value

    params["level"] = json_level

    params["level_gte"] = level_gte

    params["logger_name"] = logger_name

    params["message"] = message

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    json_source: Union[Unset, str] = UNSET
    if not isinstance(source, Unset):
        json_source = source.value

    params["source"] = json_source

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/system-logs/instances/",
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
    created_from: Union[Unset, float] = UNSET,
    created_to: Union[Unset, float] = UNSET,
    instance: Union[Unset, str] = UNSET,
    level: Union[Unset, SystemLogLevelEnum] = UNSET,
    level_gte: Union[Unset, int] = UNSET,
    logger_name: Union[Unset, str] = UNSET,
    message: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SystemLogOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    source: Union[Unset, SystemLogSourceEnum] = UNSET,
) -> Response[int]:
    """List system log instances

     Get number of items in the collection matching the request parameters.

    Args:
        created_from (Union[Unset, float]):
        created_to (Union[Unset, float]):
        instance (Union[Unset, str]):
        level (Union[Unset, SystemLogLevelEnum]):
        level_gte (Union[Unset, int]):
        logger_name (Union[Unset, str]):
        message (Union[Unset, str]):
        o (Union[Unset, list[SystemLogOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        source (Union[Unset, SystemLogSourceEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        created_from=created_from,
        created_to=created_to,
        instance=instance,
        level=level,
        level_gte=level_gte,
        logger_name=logger_name,
        message=message,
        o=o,
        page=page,
        page_size=page_size,
        source=source,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    created_from: Union[Unset, float] = UNSET,
    created_to: Union[Unset, float] = UNSET,
    instance: Union[Unset, str] = UNSET,
    level: Union[Unset, SystemLogLevelEnum] = UNSET,
    level_gte: Union[Unset, int] = UNSET,
    logger_name: Union[Unset, str] = UNSET,
    message: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SystemLogOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    source: Union[Unset, SystemLogSourceEnum] = UNSET,
) -> int:
    """List system log instances

     Get number of items in the collection matching the request parameters.

    Args:
        created_from (Union[Unset, float]):
        created_to (Union[Unset, float]):
        instance (Union[Unset, str]):
        level (Union[Unset, SystemLogLevelEnum]):
        level_gte (Union[Unset, int]):
        logger_name (Union[Unset, str]):
        message (Union[Unset, str]):
        o (Union[Unset, list[SystemLogOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        source (Union[Unset, SystemLogSourceEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        created_from=created_from,
        created_to=created_to,
        instance=instance,
        level=level,
        level_gte=level_gte,
        logger_name=logger_name,
        message=message,
        o=o,
        page=page,
        page_size=page_size,
        source=source,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    created_from: Union[Unset, float] = UNSET,
    created_to: Union[Unset, float] = UNSET,
    instance: Union[Unset, str] = UNSET,
    level: Union[Unset, SystemLogLevelEnum] = UNSET,
    level_gte: Union[Unset, int] = UNSET,
    logger_name: Union[Unset, str] = UNSET,
    message: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SystemLogOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    source: Union[Unset, SystemLogSourceEnum] = UNSET,
) -> Response[int]:
    """List system log instances

     Get number of items in the collection matching the request parameters.

    Args:
        created_from (Union[Unset, float]):
        created_to (Union[Unset, float]):
        instance (Union[Unset, str]):
        level (Union[Unset, SystemLogLevelEnum]):
        level_gte (Union[Unset, int]):
        logger_name (Union[Unset, str]):
        message (Union[Unset, str]):
        o (Union[Unset, list[SystemLogOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        source (Union[Unset, SystemLogSourceEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        created_from=created_from,
        created_to=created_to,
        instance=instance,
        level=level,
        level_gte=level_gte,
        logger_name=logger_name,
        message=message,
        o=o,
        page=page,
        page_size=page_size,
        source=source,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    created_from: Union[Unset, float] = UNSET,
    created_to: Union[Unset, float] = UNSET,
    instance: Union[Unset, str] = UNSET,
    level: Union[Unset, SystemLogLevelEnum] = UNSET,
    level_gte: Union[Unset, int] = UNSET,
    logger_name: Union[Unset, str] = UNSET,
    message: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SystemLogOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    source: Union[Unset, SystemLogSourceEnum] = UNSET,
) -> int:
    """List system log instances

     Get number of items in the collection matching the request parameters.

    Args:
        created_from (Union[Unset, float]):
        created_to (Union[Unset, float]):
        instance (Union[Unset, str]):
        level (Union[Unset, SystemLogLevelEnum]):
        level_gte (Union[Unset, int]):
        logger_name (Union[Unset, str]):
        message (Union[Unset, str]):
        o (Union[Unset, list[SystemLogOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        source (Union[Unset, SystemLogSourceEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            created_from=created_from,
            created_to=created_to,
            instance=instance,
            level=level,
            level_gte=level_gte,
            logger_name=logger_name,
            message=message,
            o=o,
            page=page,
            page_size=page_size,
            source=source,
        )
    ).parsed
