from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.discounts_update_request import DiscountsUpdateRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: DiscountsUpdateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-plans/{uuid}/update_discounts/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Any:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
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
    body: DiscountsUpdateRequest,
) -> Response[Any]:
    """Update plan component discounts


            Update volume discount configuration for plan components.

            This endpoint allows updating discount thresholds and rates for multiple
            plan components in a single request. Discounts are applied automatically
            when limit quantities meet or exceed the threshold.

            The discount configuration affects future billing:
            - Creates separate invoice items showing the discount.
            - Can be enabled or disabled per component.


    Args:
        uuid (UUID):
        body (DiscountsUpdateRequest):

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
    body: DiscountsUpdateRequest,
) -> Response[Any]:
    """Update plan component discounts


            Update volume discount configuration for plan components.

            This endpoint allows updating discount thresholds and rates for multiple
            plan components in a single request. Discounts are applied automatically
            when limit quantities meet or exceed the threshold.

            The discount configuration affects future billing:
            - Creates separate invoice items showing the discount.
            - Can be enabled or disabled per component.


    Args:
        uuid (UUID):
        body (DiscountsUpdateRequest):

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
