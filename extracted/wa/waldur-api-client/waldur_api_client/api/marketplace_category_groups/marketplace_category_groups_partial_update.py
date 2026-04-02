from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.category_group import CategoryGroup
from ...models.patched_category_group_request import PatchedCategoryGroupRequest
from ...models.patched_category_group_request_form import PatchedCategoryGroupRequestForm
from ...models.patched_category_group_request_multipart import PatchedCategoryGroupRequestMultipart
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: Union[
        PatchedCategoryGroupRequest,
        PatchedCategoryGroupRequestForm,
        PatchedCategoryGroupRequestMultipart,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/api/marketplace-category-groups/{uuid}/",
    }

    if isinstance(body, PatchedCategoryGroupRequest):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, PatchedCategoryGroupRequestForm):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, PatchedCategoryGroupRequestMultipart):
        _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> CategoryGroup:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = CategoryGroup.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[CategoryGroup]:
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
    body: Union[
        PatchedCategoryGroupRequest,
        PatchedCategoryGroupRequestForm,
        PatchedCategoryGroupRequestMultipart,
    ],
) -> Response[CategoryGroup]:
    """Partially update a category group

     Partially updates an existing category group. Requires staff permissions.

    Args:
        uuid (UUID):
        body (PatchedCategoryGroupRequest):
        body (PatchedCategoryGroupRequestForm):
        body (PatchedCategoryGroupRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CategoryGroup]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: Union[
        PatchedCategoryGroupRequest,
        PatchedCategoryGroupRequestForm,
        PatchedCategoryGroupRequestMultipart,
    ],
) -> CategoryGroup:
    """Partially update a category group

     Partially updates an existing category group. Requires staff permissions.

    Args:
        uuid (UUID):
        body (PatchedCategoryGroupRequest):
        body (PatchedCategoryGroupRequestForm):
        body (PatchedCategoryGroupRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CategoryGroup
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: Union[
        PatchedCategoryGroupRequest,
        PatchedCategoryGroupRequestForm,
        PatchedCategoryGroupRequestMultipart,
    ],
) -> Response[CategoryGroup]:
    """Partially update a category group

     Partially updates an existing category group. Requires staff permissions.

    Args:
        uuid (UUID):
        body (PatchedCategoryGroupRequest):
        body (PatchedCategoryGroupRequestForm):
        body (PatchedCategoryGroupRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CategoryGroup]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: Union[
        PatchedCategoryGroupRequest,
        PatchedCategoryGroupRequestForm,
        PatchedCategoryGroupRequestMultipart,
    ],
) -> CategoryGroup:
    """Partially update a category group

     Partially updates an existing category group. Requires staff permissions.

    Args:
        uuid (UUID):
        body (PatchedCategoryGroupRequest):
        body (PatchedCategoryGroupRequestForm):
        body (PatchedCategoryGroupRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CategoryGroup
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
