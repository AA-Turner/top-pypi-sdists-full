from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.screenshot import Screenshot
from ...models.screenshot_request import ScreenshotRequest
from ...models.screenshot_request_form import ScreenshotRequestForm
from ...models.screenshot_request_multipart import ScreenshotRequestMultipart
from ...types import Response


def _get_kwargs(
    *,
    body: Union[
        ScreenshotRequest,
        ScreenshotRequestForm,
        ScreenshotRequestMultipart,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/marketplace-screenshots/",
    }

    if isinstance(body, ScreenshotRequest):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, ScreenshotRequestForm):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, ScreenshotRequestMultipart):
        _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Screenshot:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 201:
        response_201 = Screenshot.from_dict(response.json())

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Screenshot]:
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
        ScreenshotRequest,
        ScreenshotRequestForm,
        ScreenshotRequestMultipart,
    ],
) -> Response[Screenshot]:
    """
    Args:
        body (ScreenshotRequest):
        body (ScreenshotRequestForm):
        body (ScreenshotRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Screenshot]
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
        ScreenshotRequest,
        ScreenshotRequestForm,
        ScreenshotRequestMultipart,
    ],
) -> Screenshot:
    """
    Args:
        body (ScreenshotRequest):
        body (ScreenshotRequestForm):
        body (ScreenshotRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Screenshot
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: Union[
        ScreenshotRequest,
        ScreenshotRequestForm,
        ScreenshotRequestMultipart,
    ],
) -> Response[Screenshot]:
    """
    Args:
        body (ScreenshotRequest):
        body (ScreenshotRequestForm):
        body (ScreenshotRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Screenshot]
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
        ScreenshotRequest,
        ScreenshotRequestForm,
        ScreenshotRequestMultipart,
    ],
) -> Screenshot:
    """
    Args:
        body (ScreenshotRequest):
        body (ScreenshotRequestForm):
        body (ScreenshotRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Screenshot
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
