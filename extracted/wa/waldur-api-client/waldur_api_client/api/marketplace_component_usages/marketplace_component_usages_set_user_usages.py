from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.component_user_usage_bulk_create_request import ComponentUserUsageBulkCreateRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: ComponentUserUsageBulkCreateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-component-usages/{uuid}/set_user_usages/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Any:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        return None
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
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
    body: ComponentUserUsageBulkCreateRequest,
) -> Response[Any]:
    """Bulk set user-specific component usages


            Allows a service provider to report usage for multiple users associated with a resource's
    component
            in a single request. This avoids the need for one API call per user.

            - All usages are processed atomically: if any item fails validation, none are persisted.
            - If a user-specific usage record already exists for the given component usage, it will be
    updated.
            - Otherwise, a new record is created.


    Args:
        uuid (UUID):
        body (ComponentUserUsageBulkCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: ComponentUserUsageBulkCreateRequest,
) -> Response[Any]:
    """Bulk set user-specific component usages


            Allows a service provider to report usage for multiple users associated with a resource's
    component
            in a single request. This avoids the need for one API call per user.

            - All usages are processed atomically: if any item fails validation, none are persisted.
            - If a user-specific usage record already exists for the given component usage, it will be
    updated.
            - Otherwise, a new record is created.


    Args:
        uuid (UUID):
        body (ComponentUserUsageBulkCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
