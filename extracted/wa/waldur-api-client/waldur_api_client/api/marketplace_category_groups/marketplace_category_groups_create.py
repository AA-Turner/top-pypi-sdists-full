from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.category_group import CategoryGroup
from ...models.category_group_request import CategoryGroupRequest
from ...models.category_group_request_form import CategoryGroupRequestForm
from ...models.category_group_request_multipart import CategoryGroupRequestMultipart
from ...types import Response


def _get_kwargs(
    *,
    body: Union[
        CategoryGroupRequest,
        CategoryGroupRequestForm,
        CategoryGroupRequestMultipart,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/marketplace-category-groups/",
    }

    if isinstance(body, CategoryGroupRequest):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, CategoryGroupRequestForm):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, CategoryGroupRequestMultipart):
        _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> CategoryGroup:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = CategoryGroup.from_dict(response.json())

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[CategoryGroup]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: Union[
        CategoryGroupRequest,
        CategoryGroupRequestForm,
        CategoryGroupRequestMultipart,
    ],
) -> Response[CategoryGroup]:
    """Create a category group

     Creates a new category group. Requires staff permissions.

    Args:
        body (CategoryGroupRequest):
        body (CategoryGroupRequestForm):
        body (CategoryGroupRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CategoryGroup]
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
    body: Union[
        CategoryGroupRequest,
        CategoryGroupRequestForm,
        CategoryGroupRequestMultipart,
    ],
) -> CategoryGroup:
    """Create a category group

     Creates a new category group. Requires staff permissions.

    Args:
        body (CategoryGroupRequest):
        body (CategoryGroupRequestForm):
        body (CategoryGroupRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CategoryGroup
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: Union[
        CategoryGroupRequest,
        CategoryGroupRequestForm,
        CategoryGroupRequestMultipart,
    ],
) -> Response[CategoryGroup]:
    """Create a category group

     Creates a new category group. Requires staff permissions.

    Args:
        body (CategoryGroupRequest):
        body (CategoryGroupRequestForm):
        body (CategoryGroupRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CategoryGroup]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: Union[
        CategoryGroupRequest,
        CategoryGroupRequestForm,
        CategoryGroupRequestMultipart,
    ],
) -> CategoryGroup:
    """Create a category group

     Creates a new category group. Requires staff permissions.

    Args:
        body (CategoryGroupRequest):
        body (CategoryGroupRequestForm):
        body (CategoryGroupRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CategoryGroup
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
