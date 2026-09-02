from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.paginated_templates_response import PaginatedTemplatesResponse
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    template_type: Union[Unset, str] = "template_build",
    page: Union[Unset, int] = 1,
    limit: Union[Unset, int] = 20,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    if not isinstance(template_type, Unset):
        params["template_type"] = template_type

    if not isinstance(page, Unset):
        params["page"] = page

    if not isinstance(limit, Unset):
        params["limit"] = limit

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v2/templates",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[PaginatedTemplatesResponse, Error]]:
    if response.status_code == 200:
        response_200 = PaginatedTemplatesResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401
    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[PaginatedTemplatesResponse, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    template_type: Union[Unset, str] = "template_build",
    page: Union[Unset, int] = 1,
    limit: Union[Unset, int] = 20,
) -> Response[Union[PaginatedTemplatesResponse, Error]]:
    """List templates with pagination support

    Args:
        template_type (Union[Unset, str]): Filter templates by type. Defaults to "template_build".
            - "template_build": Include only original templates built from Dockerfile
            - "snapshot_template": Include only templates generated from snapshots/commits
        page (Union[Unset, int]): Page number (1-based). Defaults to 1.
        limit (Union[Unset, int]): Number of items per page (max 100). Defaults to 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[PaginatedTemplatesResponse, Error]]
    """

    kwargs = _get_kwargs(
        template_type=template_type,
        page=page,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    template_type: Union[Unset, str] = "template_build",
    page: Union[Unset, int] = 1,
    limit: Union[Unset, int] = 20,
) -> Optional[Union[PaginatedTemplatesResponse, Error]]:
    """List templates with pagination support

    Args:
        template_type (Union[Unset, str]): Filter templates by type. Defaults to "template_build".
            - "template_build": Include only original templates built from Dockerfile
            - "snapshot_template": Include only templates generated from snapshots/commits
        page (Union[Unset, int]): Page number (1-based). Defaults to 1.
        limit (Union[Unset, int]): Number of items per page (max 100). Defaults to 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[PaginatedTemplatesResponse, Error]
    """

    return sync_detailed(
        client=client,
        template_type=template_type,
        page=page,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    template_type: Union[Unset, str] = "template_build",
    page: Union[Unset, int] = 1,
    limit: Union[Unset, int] = 20,
) -> Response[Union[PaginatedTemplatesResponse, Error]]:
    """List templates with pagination support

    Args:
        template_type (Union[Unset, str]): Filter templates by type. Defaults to "template_build".
            - "template_build": Include only original templates built from Dockerfile
            - "snapshot_template": Include only templates generated from snapshots/commits
        page (Union[Unset, int]): Page number (1-based). Defaults to 1.
        limit (Union[Unset, int]): Number of items per page (max 100). Defaults to 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[PaginatedTemplatesResponse, Error]]
    """

    kwargs = _get_kwargs(
        template_type=template_type,
        page=page,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    template_type: Union[Unset, str] = "template_build",
    page: Union[Unset, int] = 1,
    limit: Union[Unset, int] = 20,
) -> Optional[Union[PaginatedTemplatesResponse, Error]]:
    """List templates with pagination support

    Args:
        template_type (Union[Unset, str]): Filter templates by type. Defaults to "template_build".
            - "template_build": Include only original templates built from Dockerfile
            - "snapshot_template": Include only templates generated from snapshots/commits
        page (Union[Unset, int]): Page number (1-based). Defaults to 1.
        limit (Union[Unset, int]): Number of items per page (max 100). Defaults to 20.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[PaginatedTemplatesResponse, Error]
    """

    return (
        await asyncio_detailed(
            client=client,
            template_type=template_type,
            page=page,
            limit=limit,
        )
    ).parsed
