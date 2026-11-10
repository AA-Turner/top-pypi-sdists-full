from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.global_user_role_create_request import GlobalUserRoleCreateRequest
from ...models.user_role_details import UserRoleDetails
from ...types import Response


def _get_kwargs(
    *,
    body: GlobalUserRoleCreateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/global-user-roles/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> UserRoleDetails:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = UserRoleDetails.from_dict(response.json())

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[UserRoleDetails]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: GlobalUserRoleCreateRequest,
) -> Response[UserRoleDetails]:
    """Grant a site-wide role

     Staff assigns a global role to a user. The role's content type must be global. An optional
    expiration time can be set.

    Args:
        body (GlobalUserRoleCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserRoleDetails]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: GlobalUserRoleCreateRequest,
) -> UserRoleDetails:
    """Grant a site-wide role

     Staff assigns a global role to a user. The role's content type must be global. An optional
    expiration time can be set.

    Args:
        body (GlobalUserRoleCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserRoleDetails
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: GlobalUserRoleCreateRequest,
) -> Response[UserRoleDetails]:
    """Grant a site-wide role

     Staff assigns a global role to a user. The role's content type must be global. An optional
    expiration time can be set.

    Args:
        body (GlobalUserRoleCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserRoleDetails]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: GlobalUserRoleCreateRequest,
) -> UserRoleDetails:
    """Grant a site-wide role

     Staff assigns a global role to a user. The role's content type must be global. An optional
    expiration time can be set.

    Args:
        body (GlobalUserRoleCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserRoleDetails
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
