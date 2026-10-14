from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.account_options_change_request import AccountOptionsChangeRequest
from ...models.account_options_preview import AccountOptionsPreview
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: AccountOptionsChangeRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-service-providers/{uuid}/account_options_preview/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> AccountOptionsPreview:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = AccountOptionsPreview.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AccountOptionsPreview]:
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
    body: AccountOptionsChangeRequest,
) -> Response[AccountOptionsPreview]:
    """Preview a change of the provider's account options

     Shows what a change of the provider's account options would do, without saving it: each offering's
    account settings before and after, the offering accounts that would be renamed, the provider
    accounts that keep their names, and what a new person would get. The options are merged into the
    current ones key by key, as the provider update does; a blank value removes a setting.

    Args:
        uuid (UUID):
        body (AccountOptionsChangeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountOptionsPreview]
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
    body: AccountOptionsChangeRequest,
) -> AccountOptionsPreview:
    """Preview a change of the provider's account options

     Shows what a change of the provider's account options would do, without saving it: each offering's
    account settings before and after, the offering accounts that would be renamed, the provider
    accounts that keep their names, and what a new person would get. The options are merged into the
    current ones key by key, as the provider update does; a blank value removes a setting.

    Args:
        uuid (UUID):
        body (AccountOptionsChangeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountOptionsPreview
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
    body: AccountOptionsChangeRequest,
) -> Response[AccountOptionsPreview]:
    """Preview a change of the provider's account options

     Shows what a change of the provider's account options would do, without saving it: each offering's
    account settings before and after, the offering accounts that would be renamed, the provider
    accounts that keep their names, and what a new person would get. The options are merged into the
    current ones key by key, as the provider update does; a blank value removes a setting.

    Args:
        uuid (UUID):
        body (AccountOptionsChangeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountOptionsPreview]
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
    body: AccountOptionsChangeRequest,
) -> AccountOptionsPreview:
    """Preview a change of the provider's account options

     Shows what a change of the provider's account options would do, without saving it: each offering's
    account settings before and after, the offering accounts that would be renamed, the provider
    accounts that keep their names, and what a new person would get. The options are merged into the
    current ones key by key, as the provider update does; a blank value removes a setting.

    Args:
        uuid (UUID):
        body (AccountOptionsChangeRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountOptionsPreview
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
