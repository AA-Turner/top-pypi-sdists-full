from http import HTTPStatus
from typing import Any, Union, cast
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.open_stack_console_log_request import OpenStackConsoleLogRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: OpenStackConsoleLogRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/openstack-instances/{uuid}/console_log/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> str:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = cast(str, response.json())
        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[str]:
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
    body: OpenStackConsoleLogRequest,
) -> Response[str]:
    """Get console log

     Get console log for the instance. Same as the GET form, but takes `length` in the request body, so
    action-oriented clients such as the Ansible collection can call it like any other instance action.

    Args:
        uuid (UUID):
        body (OpenStackConsoleLogRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
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
    body: OpenStackConsoleLogRequest,
) -> str:
    """Get console log

     Get console log for the instance. Same as the GET form, but takes `length` in the request body, so
    action-oriented clients such as the Ansible collection can call it like any other instance action.

    Args:
        uuid (UUID):
        body (OpenStackConsoleLogRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        str
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
    body: OpenStackConsoleLogRequest,
) -> Response[str]:
    """Get console log

     Get console log for the instance. Same as the GET form, but takes `length` in the request body, so
    action-oriented clients such as the Ansible collection can call it like any other instance action.

    Args:
        uuid (UUID):
        body (OpenStackConsoleLogRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
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
    body: OpenStackConsoleLogRequest,
) -> str:
    """Get console log

     Get console log for the instance. Same as the GET form, but takes `length` in the request body, so
    action-oriented clients such as the Ansible collection can call it like any other instance action.

    Args:
        uuid (UUID):
        body (OpenStackConsoleLogRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        str
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
