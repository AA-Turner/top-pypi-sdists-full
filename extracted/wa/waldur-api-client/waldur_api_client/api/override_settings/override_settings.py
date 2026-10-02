from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.constance_settings_request import ConstanceSettingsRequest
from ...models.constance_settings_request_form import ConstanceSettingsRequestForm
from ...models.constance_settings_request_multipart import ConstanceSettingsRequestMultipart
from ...types import Response


def _get_kwargs(
    *,
    body: Union[
        ConstanceSettingsRequest,
        ConstanceSettingsRequestForm,
        ConstanceSettingsRequestMultipart,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/override-settings/",
    }

    if isinstance(body, ConstanceSettingsRequest):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, ConstanceSettingsRequestForm):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, ConstanceSettingsRequestMultipart):
        _kwargs["files"] = body.to_multipart()

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
    *,
    client: AuthenticatedClient,
    body: Union[
        ConstanceSettingsRequest,
        ConstanceSettingsRequestForm,
        ConstanceSettingsRequestMultipart,
    ],
) -> Response[Any]:
    """Update overridable settings

     Updates one or more settings in the database via the Constance backend. Requires admin permissions.

    Args:
        body (ConstanceSettingsRequest):
        body (ConstanceSettingsRequestForm):
        body (ConstanceSettingsRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: Union[
        ConstanceSettingsRequest,
        ConstanceSettingsRequestForm,
        ConstanceSettingsRequestMultipart,
    ],
) -> Response[Any]:
    """Update overridable settings

     Updates one or more settings in the database via the Constance backend. Requires admin permissions.

    Args:
        body (ConstanceSettingsRequest):
        body (ConstanceSettingsRequestForm):
        body (ConstanceSettingsRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
