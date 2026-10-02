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
        "method": "head",
        "url": "/api/marketplace-site-agent-processors/",
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
    backend_type: Union[Unset, str] = UNSET,
    backend_version: Union[Unset, str] = UNSET,
    last_run: Union[Unset, datetime.datetime] = UNSET,
    last_run_before: Union[Unset, datetime.datetime] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    service_uuid: Union[Unset, UUID] = UNSET,
    stale: Union[Unset, bool] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

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
        Response[int]
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
) -> int:
    """Get number of items in the collection matching the request parameters.

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
        int
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
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

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
        Response[int]
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
) -> int:
    """Get number of items in the collection matching the request parameters.

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
        int
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
