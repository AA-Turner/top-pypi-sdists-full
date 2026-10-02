from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.check_unique_backend_id_request import CheckUniqueBackendIDRequest
from ...models.check_unique_backend_id_response import CheckUniqueBackendIDResponse
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: CheckUniqueBackendIDRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-provider-offerings/{uuid}/check_unique_backend_id/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> CheckUniqueBackendIDResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = CheckUniqueBackendIDResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CheckUniqueBackendIDResponse]:
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
    body: CheckUniqueBackendIDRequest,
) -> Response[CheckUniqueBackendIDResponse]:
    """Check if backend_id is unique

     Checks if the provided backend_id has been used in resources of this offering or all offerings of
    the same customer. Returns true if unique, false if already used.

    Args:
        uuid (UUID):
        body (CheckUniqueBackendIDRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CheckUniqueBackendIDResponse]
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
    body: CheckUniqueBackendIDRequest,
) -> CheckUniqueBackendIDResponse:
    """Check if backend_id is unique

     Checks if the provided backend_id has been used in resources of this offering or all offerings of
    the same customer. Returns true if unique, false if already used.

    Args:
        uuid (UUID):
        body (CheckUniqueBackendIDRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CheckUniqueBackendIDResponse
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
    body: CheckUniqueBackendIDRequest,
) -> Response[CheckUniqueBackendIDResponse]:
    """Check if backend_id is unique

     Checks if the provided backend_id has been used in resources of this offering or all offerings of
    the same customer. Returns true if unique, false if already used.

    Args:
        uuid (UUID):
        body (CheckUniqueBackendIDRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CheckUniqueBackendIDResponse]
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
    body: CheckUniqueBackendIDRequest,
) -> CheckUniqueBackendIDResponse:
    """Check if backend_id is unique

     Checks if the provided backend_id has been used in resources of this offering or all offerings of
    the same customer. Returns true if unique, false if already used.

    Args:
        uuid (UUID):
        body (CheckUniqueBackendIDRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CheckUniqueBackendIDResponse
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
