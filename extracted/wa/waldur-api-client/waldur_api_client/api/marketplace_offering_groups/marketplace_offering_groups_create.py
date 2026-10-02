from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.offering_group import OfferingGroup
from ...models.offering_group_request import OfferingGroupRequest
from ...models.offering_group_request_form import OfferingGroupRequestForm
from ...models.offering_group_request_multipart import OfferingGroupRequestMultipart
from ...types import Response


def _get_kwargs(
    *,
    body: Union[
        OfferingGroupRequest,
        OfferingGroupRequestForm,
        OfferingGroupRequestMultipart,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/marketplace-offering-groups/",
    }

    if isinstance(body, OfferingGroupRequest):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, OfferingGroupRequestForm):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, OfferingGroupRequestMultipart):
        _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> OfferingGroup:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = OfferingGroup.from_dict(response.json())

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[OfferingGroup]:
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
        OfferingGroupRequest,
        OfferingGroupRequestForm,
        OfferingGroupRequestMultipart,
    ],
) -> Response[OfferingGroup]:
    """
    Args:
        body (OfferingGroupRequest):
        body (OfferingGroupRequestForm):
        body (OfferingGroupRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OfferingGroup]
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
        OfferingGroupRequest,
        OfferingGroupRequestForm,
        OfferingGroupRequestMultipart,
    ],
) -> OfferingGroup:
    """
    Args:
        body (OfferingGroupRequest):
        body (OfferingGroupRequestForm):
        body (OfferingGroupRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OfferingGroup
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: Union[
        OfferingGroupRequest,
        OfferingGroupRequestForm,
        OfferingGroupRequestMultipart,
    ],
) -> Response[OfferingGroup]:
    """
    Args:
        body (OfferingGroupRequest):
        body (OfferingGroupRequestForm):
        body (OfferingGroupRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OfferingGroup]
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
        OfferingGroupRequest,
        OfferingGroupRequestForm,
        OfferingGroupRequestMultipart,
    ],
) -> OfferingGroup:
    """
    Args:
        body (OfferingGroupRequest):
        body (OfferingGroupRequestForm):
        body (OfferingGroupRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OfferingGroup
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
