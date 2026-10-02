from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    is_complete: Union[Unset, bool] = UNSET,
    month: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_identifier: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource: Union[Unset, str] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["is_complete"] = is_complete

    params["month"] = month

    params["page"] = page

    params["page_size"] = page_size

    params["project_identifier"] = project_identifier

    json_project_uuid: Union[Unset, str] = UNSET
    if not isinstance(project_uuid, Unset):
        json_project_uuid = str(project_uuid)
    params["project_uuid"] = json_project_uuid

    params["resource"] = resource

    params["year"] = year

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/openportal-project-usage-reports/",
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
    is_complete: Union[Unset, bool] = UNSET,
    month: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_identifier: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource: Union[Unset, str] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        is_complete (Union[Unset, bool]):
        month (Union[Unset, int]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_identifier (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        resource (Union[Unset, str]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        is_complete=is_complete,
        month=month,
        page=page,
        page_size=page_size,
        project_identifier=project_identifier,
        project_uuid=project_uuid,
        resource=resource,
        year=year,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    is_complete: Union[Unset, bool] = UNSET,
    month: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_identifier: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource: Union[Unset, str] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        is_complete (Union[Unset, bool]):
        month (Union[Unset, int]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_identifier (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        resource (Union[Unset, str]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        is_complete=is_complete,
        month=month,
        page=page,
        page_size=page_size,
        project_identifier=project_identifier,
        project_uuid=project_uuid,
        resource=resource,
        year=year,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    is_complete: Union[Unset, bool] = UNSET,
    month: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_identifier: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource: Union[Unset, str] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        is_complete (Union[Unset, bool]):
        month (Union[Unset, int]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_identifier (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        resource (Union[Unset, str]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        is_complete=is_complete,
        month=month,
        page=page,
        page_size=page_size,
        project_identifier=project_identifier,
        project_uuid=project_uuid,
        resource=resource,
        year=year,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    is_complete: Union[Unset, bool] = UNSET,
    month: Union[Unset, int] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    project_identifier: Union[Unset, str] = UNSET,
    project_uuid: Union[Unset, UUID] = UNSET,
    resource: Union[Unset, str] = UNSET,
    year: Union[Unset, int] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        is_complete (Union[Unset, bool]):
        month (Union[Unset, int]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        project_identifier (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        resource (Union[Unset, str]):
        year (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            is_complete=is_complete,
            month=month,
            page=page,
            page_size=page_size,
            project_identifier=project_identifier,
            project_uuid=project_uuid,
            resource=resource,
            year=year,
        )
    ).parsed
