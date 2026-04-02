from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    group_id: str,
    offering_uuid: str,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["group_id"] = group_id

    params["offering_uuid"] = offering_uuid

    params["page"] = page

    params["page_size"] = page_size

    json_resource_uuid: Union[Unset, str] = UNSET
    if not isinstance(resource_uuid, Unset):
        json_resource_uuid = str(resource_uuid)
    params["resource_uuid"] = json_resource_uuid

    json_role_uuid: Union[Unset, str] = UNSET
    if not isinstance(role_uuid, Unset):
        json_role_uuid = str(role_uuid)
    params["role_uuid"] = json_role_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/offering-keycloak-groups/remote_group_members/",
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
    group_id: str,
    offering_uuid: str,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """List members of a remote Keycloak group

     Get number of items in the collection matching the request parameters.

    Args:
        group_id (str):
        offering_uuid (str):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        resource_uuid (Union[Unset, UUID]):
        role_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        resource_uuid=resource_uuid,
        role_uuid=role_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    group_id: str,
    offering_uuid: str,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """List members of a remote Keycloak group

     Get number of items in the collection matching the request parameters.

    Args:
        group_id (str):
        offering_uuid (str):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        resource_uuid (Union[Unset, UUID]):
        role_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        group_id=group_id,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        resource_uuid=resource_uuid,
        role_uuid=role_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    group_id: str,
    offering_uuid: str,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """List members of a remote Keycloak group

     Get number of items in the collection matching the request parameters.

    Args:
        group_id (str):
        offering_uuid (str):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        resource_uuid (Union[Unset, UUID]):
        role_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        offering_uuid=offering_uuid,
        page=page,
        page_size=page_size,
        resource_uuid=resource_uuid,
        role_uuid=role_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    group_id: str,
    offering_uuid: str,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    resource_uuid: Union[Unset, UUID] = UNSET,
    role_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """List members of a remote Keycloak group

     Get number of items in the collection matching the request parameters.

    Args:
        group_id (str):
        offering_uuid (str):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        resource_uuid (Union[Unset, UUID]):
        role_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            group_id=group_id,
            offering_uuid=offering_uuid,
            page=page,
            page_size=page_size,
            resource_uuid=resource_uuid,
            role_uuid=role_uuid,
        )
    ).parsed
