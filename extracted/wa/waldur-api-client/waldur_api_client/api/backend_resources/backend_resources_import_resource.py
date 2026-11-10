from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.backend_resource_import_request import BackendResourceImportRequest
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: BackendResourceImportRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/backend-resources/{uuid}/import_resource/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Any:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
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
    body: BackendResourceImportRequest,
) -> Response[Any]:
    """Import a backend resource (staff only)


            Converts a backend resource into a full marketplace resource. This action is restricted to
    staff users.
            Upon successful import, the original backend resource record is deleted. A fake order in the
    'done'
            state is created to represent the import event.


    Args:
        uuid (UUID):
        body (BackendResourceImportRequest):

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
    body: BackendResourceImportRequest,
) -> Response[Any]:
    """Import a backend resource (staff only)


            Converts a backend resource into a full marketplace resource. This action is restricted to
    staff users.
            Upon successful import, the original backend resource record is deleted. A fake order in the
    'done'
            state is created to represent the import event.


    Args:
        uuid (UUID):
        body (BackendResourceImportRequest):

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
