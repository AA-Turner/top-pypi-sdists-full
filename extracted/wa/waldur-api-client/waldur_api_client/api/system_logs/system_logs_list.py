from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.system_log import SystemLog
from ...models.system_log_level_enum import SystemLogLevelEnum
from ...models.system_log_o_enum import SystemLogOEnum
from ...models.system_log_source_enum import SystemLogSourceEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


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
        "method": "get",
        "url": "/api/system-logs/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["SystemLog"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SystemLog.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["SystemLog"]]:
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
) -> Response[list["SystemLog"]]:
    """
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
        Response[list['SystemLog']]
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
) -> list["SystemLog"]:
    """
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
        list['SystemLog']
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
) -> Response[list["SystemLog"]]:
    """
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
        Response[list['SystemLog']]
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
) -> list["SystemLog"]:
    """
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
        list['SystemLog']
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


def sync_all(
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
    source: Union[Unset, SystemLogSourceEnum] = UNSET,
) -> list["SystemLog"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created_from (Union[Unset, float]):
        created_to (Union[Unset, float]):
        instance (Union[Unset, str]):
        level (Union[Unset, SystemLogLevelEnum]):
        level_gte (Union[Unset, int]):
        logger_name (Union[Unset, str]):
        message (Union[Unset, str]):
        o (Union[Unset, list[SystemLogOEnum]]):
        source (Union[Unset, SystemLogSourceEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['SystemLog']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[SystemLog] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created_from=created_from,
        created_to=created_to,
        instance=instance,
        level=level,
        level_gte=level_gte,
        logger_name=logger_name,
        message=message,
        o=o,
        source=source,
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
    created_from: Union[Unset, float] = UNSET,
    created_to: Union[Unset, float] = UNSET,
    instance: Union[Unset, str] = UNSET,
    level: Union[Unset, SystemLogLevelEnum] = UNSET,
    level_gte: Union[Unset, int] = UNSET,
    logger_name: Union[Unset, str] = UNSET,
    message: Union[Unset, str] = UNSET,
    o: Union[Unset, list[SystemLogOEnum]] = UNSET,
    source: Union[Unset, SystemLogSourceEnum] = UNSET,
) -> list["SystemLog"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        created_from (Union[Unset, float]):
        created_to (Union[Unset, float]):
        instance (Union[Unset, str]):
        level (Union[Unset, SystemLogLevelEnum]):
        level_gte (Union[Unset, int]):
        logger_name (Union[Unset, str]):
        message (Union[Unset, str]):
        o (Union[Unset, list[SystemLogOEnum]]):
        source (Union[Unset, SystemLogSourceEnum]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['SystemLog']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[SystemLog] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        created_from=created_from,
        created_to=created_to,
        instance=instance,
        level=level,
        level_gte=level_gte,
        logger_name=logger_name,
        message=message,
        o=o,
        source=source,
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
