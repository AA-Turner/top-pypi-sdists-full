from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.backend_resource_request_set_erred_request import BackendResourceRequestSetErredRequest
from ...models.backend_resource_requests_set_erred_response_200 import BackendResourceRequestsSetErredResponse200
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: BackendResourceRequestSetErredRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/backend-resource-requests/{uuid}/set_erred/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> BackendResourceRequestsSetErredResponse200:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = BackendResourceRequestsSetErredResponse200.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[BackendResourceRequestsSetErredResponse200]:
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
    body: BackendResourceRequestSetErredRequest,
) -> Response[BackendResourceRequestsSetErredResponse200]:
    """Mark a request as erred

     Transitions the request state to 'Erred'. This is used by a site agent to report a failure during
    the resource fetching process. An error message and traceback should be provided.

    Args:
        uuid (UUID):
        body (BackendResourceRequestSetErredRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BackendResourceRequestsSetErredResponse200]
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
    body: BackendResourceRequestSetErredRequest,
) -> BackendResourceRequestsSetErredResponse200:
    """Mark a request as erred

     Transitions the request state to 'Erred'. This is used by a site agent to report a failure during
    the resource fetching process. An error message and traceback should be provided.

    Args:
        uuid (UUID):
        body (BackendResourceRequestSetErredRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BackendResourceRequestsSetErredResponse200
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
    body: BackendResourceRequestSetErredRequest,
) -> Response[BackendResourceRequestsSetErredResponse200]:
    """Mark a request as erred

     Transitions the request state to 'Erred'. This is used by a site agent to report a failure during
    the resource fetching process. An error message and traceback should be provided.

    Args:
        uuid (UUID):
        body (BackendResourceRequestSetErredRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BackendResourceRequestsSetErredResponse200]
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
    body: BackendResourceRequestSetErredRequest,
) -> BackendResourceRequestsSetErredResponse200:
    """Mark a request as erred

     Transitions the request state to 'Erred'. This is used by a site agent to report a failure during
    the resource fetching process. An error message and traceback should be provided.

    Args:
        uuid (UUID):
        body (BackendResourceRequestSetErredRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BackendResourceRequestsSetErredResponse200
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
