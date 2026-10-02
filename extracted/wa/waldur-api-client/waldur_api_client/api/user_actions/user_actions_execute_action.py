from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.execute_action_error_response import ExecuteActionErrorResponse
from ...models.execute_action_request import ExecuteActionRequest
from ...models.execute_action_response import ExecuteActionResponse
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: ExecuteActionRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/user-actions/{uuid}/execute_action/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[ExecuteActionErrorResponse, ExecuteActionResponse]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ExecuteActionResponse.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = ExecuteActionErrorResponse.from_dict(response.json())

        return response_404
    if response.status_code == 500:
        response_500 = ExecuteActionErrorResponse.from_dict(response.json())

        return response_500
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ExecuteActionErrorResponse, ExecuteActionResponse]]:
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
    body: ExecuteActionRequest,
) -> Response[Union[ExecuteActionErrorResponse, ExecuteActionResponse]]:
    """Execute a corrective action

    Args:
        uuid (UUID):
        body (ExecuteActionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ExecuteActionErrorResponse, ExecuteActionResponse]]
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
    body: ExecuteActionRequest,
) -> Union[ExecuteActionErrorResponse, ExecuteActionResponse]:
    """Execute a corrective action

    Args:
        uuid (UUID):
        body (ExecuteActionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ExecuteActionErrorResponse, ExecuteActionResponse]
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
    body: ExecuteActionRequest,
) -> Response[Union[ExecuteActionErrorResponse, ExecuteActionResponse]]:
    """Execute a corrective action

    Args:
        uuid (UUID):
        body (ExecuteActionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ExecuteActionErrorResponse, ExecuteActionResponse]]
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
    body: ExecuteActionRequest,
) -> Union[ExecuteActionErrorResponse, ExecuteActionResponse]:
    """Execute a corrective action

    Args:
        uuid (UUID):
        body (ExecuteActionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ExecuteActionErrorResponse, ExecuteActionResponse]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
