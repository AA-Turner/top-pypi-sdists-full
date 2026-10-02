from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.user_role_details_field_enum import UserRoleDetailsFieldEnum
from ...models.user_role_details_o_enum import UserRoleDetailsOEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    uuid: UUID,
    *,
    field: Union[Unset, list[UserRoleDetailsFieldEnum]] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[UserRoleDetailsOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role: Union[Unset, list[str]] = UNSET,
    search_string: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
    user_url: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_field: Union[Unset, list[str]] = UNSET
    if not isinstance(field, Unset):
        json_field = []
        for field_item_data in field:
            field_item = field_item_data.value
            json_field.append(field_item)

    params["field"] = json_field

    params["full_name"] = full_name

    params["native_name"] = native_name

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    json_role: Union[Unset, list[str]] = UNSET
    if not isinstance(role, Unset):
        json_role = role

    params["role"] = json_role

    params["search_string"] = search_string

    json_user: Union[Unset, str] = UNSET
    if not isinstance(user, Unset):
        json_user = str(user)
    params["user"] = json_user

    params["user_slug"] = user_slug

    params["user_url"] = user_url

    params["username"] = username

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": f"/api/marketplace-provider-offerings/{uuid}/list_users/",
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
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[UserRoleDetailsFieldEnum]] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[UserRoleDetailsOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role: Union[Unset, list[str]] = UNSET,
    search_string: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
    user_url: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[int]:
    """List users and their roles in a scope

     Get number of items in the collection matching the request parameters.

    Args:
        uuid (UUID):
        field (Union[Unset, list[UserRoleDetailsFieldEnum]]):
        full_name (Union[Unset, str]):
        native_name (Union[Unset, str]):
        o (Union[Unset, list[UserRoleDetailsOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role (Union[Unset, list[str]]):
        search_string (Union[Unset, str]):
        user (Union[Unset, UUID]):
        user_slug (Union[Unset, str]):
        user_url (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        field=field,
        full_name=full_name,
        native_name=native_name,
        o=o,
        page=page,
        page_size=page_size,
        role=role,
        search_string=search_string,
        user=user,
        user_slug=user_slug,
        user_url=user_url,
        username=username,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[UserRoleDetailsFieldEnum]] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[UserRoleDetailsOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role: Union[Unset, list[str]] = UNSET,
    search_string: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
    user_url: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> int:
    """List users and their roles in a scope

     Get number of items in the collection matching the request parameters.

    Args:
        uuid (UUID):
        field (Union[Unset, list[UserRoleDetailsFieldEnum]]):
        full_name (Union[Unset, str]):
        native_name (Union[Unset, str]):
        o (Union[Unset, list[UserRoleDetailsOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role (Union[Unset, list[str]]):
        search_string (Union[Unset, str]):
        user (Union[Unset, UUID]):
        user_slug (Union[Unset, str]):
        user_url (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        field=field,
        full_name=full_name,
        native_name=native_name,
        o=o,
        page=page,
        page_size=page_size,
        role=role,
        search_string=search_string,
        user=user,
        user_slug=user_slug,
        user_url=user_url,
        username=username,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[UserRoleDetailsFieldEnum]] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[UserRoleDetailsOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role: Union[Unset, list[str]] = UNSET,
    search_string: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
    user_url: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> Response[int]:
    """List users and their roles in a scope

     Get number of items in the collection matching the request parameters.

    Args:
        uuid (UUID):
        field (Union[Unset, list[UserRoleDetailsFieldEnum]]):
        full_name (Union[Unset, str]):
        native_name (Union[Unset, str]):
        o (Union[Unset, list[UserRoleDetailsOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role (Union[Unset, list[str]]):
        search_string (Union[Unset, str]):
        user (Union[Unset, UUID]):
        user_slug (Union[Unset, str]):
        user_url (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        field=field,
        full_name=full_name,
        native_name=native_name,
        o=o,
        page=page,
        page_size=page_size,
        role=role,
        search_string=search_string,
        user=user,
        user_slug=user_slug,
        user_url=user_url,
        username=username,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    field: Union[Unset, list[UserRoleDetailsFieldEnum]] = UNSET,
    full_name: Union[Unset, str] = UNSET,
    native_name: Union[Unset, str] = UNSET,
    o: Union[Unset, list[UserRoleDetailsOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    role: Union[Unset, list[str]] = UNSET,
    search_string: Union[Unset, str] = UNSET,
    user: Union[Unset, UUID] = UNSET,
    user_slug: Union[Unset, str] = UNSET,
    user_url: Union[Unset, str] = UNSET,
    username: Union[Unset, str] = UNSET,
) -> int:
    """List users and their roles in a scope

     Get number of items in the collection matching the request parameters.

    Args:
        uuid (UUID):
        field (Union[Unset, list[UserRoleDetailsFieldEnum]]):
        full_name (Union[Unset, str]):
        native_name (Union[Unset, str]):
        o (Union[Unset, list[UserRoleDetailsOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        role (Union[Unset, list[str]]):
        search_string (Union[Unset, str]):
        user (Union[Unset, UUID]):
        user_slug (Union[Unset, str]):
        user_url (Union[Unset, str]):
        username (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            field=field,
            full_name=full_name,
            native_name=native_name,
            o=o,
            page=page,
            page_size=page_size,
            role=role,
            search_string=search_string,
            user=user,
            user_slug=user_slug,
            user_url=user_url,
            username=username,
        )
    ).parsed
