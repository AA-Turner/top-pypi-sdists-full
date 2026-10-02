import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.agent_processor import AgentProcessor
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    backend_type: Union[Unset, str] = UNSET,
    backend_version: Union[Unset, str] = UNSET,
    last_run: Union[Unset, datetime.datetime] = UNSET,
    last_run_before: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    service_uuid: Union[Unset, UUID] = UNSET,
    stale: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["backend_type"] = backend_type

    params["backend_version"] = backend_version

    json_last_run: Union[Unset, str] = UNSET
    if not isinstance(last_run, Unset):
        json_last_run = last_run.isoformat()
    params["last_run"] = json_last_run

    json_last_run_before: Union[Unset, str] = UNSET
    if not isinstance(last_run_before, Unset):
        json_last_run_before = last_run_before.isoformat()
    params["last_run_before"] = json_last_run_before

    params["page"] = page

    params["page_size"] = page_size

    json_service_uuid: Union[Unset, str] = UNSET
    if not isinstance(service_uuid, Unset):
        json_service_uuid = str(service_uuid)
    params["service_uuid"] = json_service_uuid

    params["stale"] = stale

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/marketplace-site-agent-processors/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["AgentProcessor"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AgentProcessor.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["AgentProcessor"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    backend_type: Union[Unset, str] = UNSET,
    backend_version: Union[Unset, str] = UNSET,
    last_run: Union[Unset, datetime.datetime] = UNSET,
    last_run_before: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    service_uuid: Union[Unset, UUID] = UNSET,
    stale: Union[Unset, bool] = UNSET,
) -> Response[list["AgentProcessor"]]:
    """
    Args:
        backend_type (Union[Unset, str]):
        backend_version (Union[Unset, str]):
        last_run (Union[Unset, datetime.datetime]):
        last_run_before (Union[Unset, datetime.datetime]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        service_uuid (Union[Unset, UUID]):
        stale (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AgentProcessor']]
    """

    kwargs = _get_kwargs(
        backend_type=backend_type,
        backend_version=backend_version,
        last_run=last_run,
        last_run_before=last_run_before,
        page=page,
        page_size=page_size,
        service_uuid=service_uuid,
        stale=stale,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    backend_type: Union[Unset, str] = UNSET,
    backend_version: Union[Unset, str] = UNSET,
    last_run: Union[Unset, datetime.datetime] = UNSET,
    last_run_before: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    service_uuid: Union[Unset, UUID] = UNSET,
    stale: Union[Unset, bool] = UNSET,
) -> list["AgentProcessor"]:
    """
    Args:
        backend_type (Union[Unset, str]):
        backend_version (Union[Unset, str]):
        last_run (Union[Unset, datetime.datetime]):
        last_run_before (Union[Unset, datetime.datetime]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        service_uuid (Union[Unset, UUID]):
        stale (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AgentProcessor']
    """

    return sync_detailed(
        client=client,
        backend_type=backend_type,
        backend_version=backend_version,
        last_run=last_run,
        last_run_before=last_run_before,
        page=page,
        page_size=page_size,
        service_uuid=service_uuid,
        stale=stale,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    backend_type: Union[Unset, str] = UNSET,
    backend_version: Union[Unset, str] = UNSET,
    last_run: Union[Unset, datetime.datetime] = UNSET,
    last_run_before: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    service_uuid: Union[Unset, UUID] = UNSET,
    stale: Union[Unset, bool] = UNSET,
) -> Response[list["AgentProcessor"]]:
    """
    Args:
        backend_type (Union[Unset, str]):
        backend_version (Union[Unset, str]):
        last_run (Union[Unset, datetime.datetime]):
        last_run_before (Union[Unset, datetime.datetime]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        service_uuid (Union[Unset, UUID]):
        stale (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AgentProcessor']]
    """

    kwargs = _get_kwargs(
        backend_type=backend_type,
        backend_version=backend_version,
        last_run=last_run,
        last_run_before=last_run_before,
        page=page,
        page_size=page_size,
        service_uuid=service_uuid,
        stale=stale,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    backend_type: Union[Unset, str] = UNSET,
    backend_version: Union[Unset, str] = UNSET,
    last_run: Union[Unset, datetime.datetime] = UNSET,
    last_run_before: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    service_uuid: Union[Unset, UUID] = UNSET,
    stale: Union[Unset, bool] = UNSET,
) -> list["AgentProcessor"]:
    """
    Args:
        backend_type (Union[Unset, str]):
        backend_version (Union[Unset, str]):
        last_run (Union[Unset, datetime.datetime]):
        last_run_before (Union[Unset, datetime.datetime]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        service_uuid (Union[Unset, UUID]):
        stale (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AgentProcessor']
    """

    return (
        await asyncio_detailed(
            client=client,
            backend_type=backend_type,
            backend_version=backend_version,
            last_run=last_run,
            last_run_before=last_run_before,
            page=page,
            page_size=page_size,
            service_uuid=service_uuid,
            stale=stale,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    backend_type: Union[Unset, str] = UNSET,
    backend_version: Union[Unset, str] = UNSET,
    last_run: Union[Unset, datetime.datetime] = UNSET,
    last_run_before: Union[Unset, datetime.datetime] = UNSET,
    service_uuid: Union[Unset, UUID] = UNSET,
    stale: Union[Unset, bool] = UNSET,
) -> list["AgentProcessor"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        backend_type (Union[Unset, str]):
        backend_version (Union[Unset, str]):
        last_run (Union[Unset, datetime.datetime]):
        last_run_before (Union[Unset, datetime.datetime]):
        service_uuid (Union[Unset, UUID]):
        stale (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AgentProcessor']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[AgentProcessor] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        backend_type=backend_type,
        backend_version=backend_version,
        last_run=last_run,
        last_run_before=last_run_before,
        service_uuid=service_uuid,
        stale=stale,
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
    backend_type: Union[Unset, str] = UNSET,
    backend_version: Union[Unset, str] = UNSET,
    last_run: Union[Unset, datetime.datetime] = UNSET,
    last_run_before: Union[Unset, datetime.datetime] = UNSET,
    service_uuid: Union[Unset, UUID] = UNSET,
    stale: Union[Unset, bool] = UNSET,
) -> list["AgentProcessor"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        backend_type (Union[Unset, str]):
        backend_version (Union[Unset, str]):
        last_run (Union[Unset, datetime.datetime]):
        last_run_before (Union[Unset, datetime.datetime]):
        service_uuid (Union[Unset, UUID]):
        stale (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AgentProcessor']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[AgentProcessor] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        backend_type=backend_type,
        backend_version=backend_version,
        last_run=last_run,
        last_run_before=last_run_before,
        service_uuid=service_uuid,
        stale=stale,
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
