from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.matrix_appservice_setup_request import MatrixAppserviceSetupRequest
from ...models.matrix_appservice_setup_response import MatrixAppserviceSetupResponse
from ...types import Response


def _get_kwargs(
    *,
    body: MatrixAppserviceSetupRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/matrix-appservice/setup/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> MatrixAppserviceSetupResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = MatrixAppserviceSetupResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[MatrixAppserviceSetupResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: MatrixAppserviceSetupRequest,
) -> Response[MatrixAppserviceSetupResponse]:
    """Setup Matrix appservice registration

     Generates fresh appservice tokens (rotating any existing ones), enables the appservice, and returns
    registration YAML.

    Args:
        body (MatrixAppserviceSetupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MatrixAppserviceSetupResponse]
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
    body: MatrixAppserviceSetupRequest,
) -> MatrixAppserviceSetupResponse:
    """Setup Matrix appservice registration

     Generates fresh appservice tokens (rotating any existing ones), enables the appservice, and returns
    registration YAML.

    Args:
        body (MatrixAppserviceSetupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MatrixAppserviceSetupResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: MatrixAppserviceSetupRequest,
) -> Response[MatrixAppserviceSetupResponse]:
    """Setup Matrix appservice registration

     Generates fresh appservice tokens (rotating any existing ones), enables the appservice, and returns
    registration YAML.

    Args:
        body (MatrixAppserviceSetupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MatrixAppserviceSetupResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: MatrixAppserviceSetupRequest,
) -> MatrixAppserviceSetupResponse:
    """Setup Matrix appservice registration

     Generates fresh appservice tokens (rotating any existing ones), enables the appservice, and returns
    registration YAML.

    Args:
        body (MatrixAppserviceSetupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MatrixAppserviceSetupResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
