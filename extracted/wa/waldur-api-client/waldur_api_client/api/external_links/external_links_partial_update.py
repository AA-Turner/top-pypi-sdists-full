from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.external_link import ExternalLink
from ...models.patched_external_link_request import PatchedExternalLinkRequest
from ...models.patched_external_link_request_form import PatchedExternalLinkRequestForm
from ...models.patched_external_link_request_multipart import PatchedExternalLinkRequestMultipart
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: Union[
        PatchedExternalLinkRequest,
        PatchedExternalLinkRequestForm,
        PatchedExternalLinkRequestMultipart,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/api/external-links/{uuid}/",
    }

    if isinstance(body, PatchedExternalLinkRequest):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, PatchedExternalLinkRequestForm):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, PatchedExternalLinkRequestMultipart):
        _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ExternalLink:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ExternalLink.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ExternalLink]:
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
    body: Union[
        PatchedExternalLinkRequest,
        PatchedExternalLinkRequestForm,
        PatchedExternalLinkRequestMultipart,
    ],
) -> Response[ExternalLink]:
    """Partially update an external link

     Partially update an existing external link. This action is restricted to staff users.

    Args:
        uuid (UUID):
        body (PatchedExternalLinkRequest):
        body (PatchedExternalLinkRequestForm):
        body (PatchedExternalLinkRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExternalLink]
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
    body: Union[
        PatchedExternalLinkRequest,
        PatchedExternalLinkRequestForm,
        PatchedExternalLinkRequestMultipart,
    ],
) -> ExternalLink:
    """Partially update an external link

     Partially update an existing external link. This action is restricted to staff users.

    Args:
        uuid (UUID):
        body (PatchedExternalLinkRequest):
        body (PatchedExternalLinkRequestForm):
        body (PatchedExternalLinkRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExternalLink
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
    body: Union[
        PatchedExternalLinkRequest,
        PatchedExternalLinkRequestForm,
        PatchedExternalLinkRequestMultipart,
    ],
) -> Response[ExternalLink]:
    """Partially update an external link

     Partially update an existing external link. This action is restricted to staff users.

    Args:
        uuid (UUID):
        body (PatchedExternalLinkRequest):
        body (PatchedExternalLinkRequestForm):
        body (PatchedExternalLinkRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExternalLink]
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
    body: Union[
        PatchedExternalLinkRequest,
        PatchedExternalLinkRequestForm,
        PatchedExternalLinkRequestMultipart,
    ],
) -> ExternalLink:
    """Partially update an external link

     Partially update an existing external link. This action is restricted to staff users.

    Args:
        uuid (UUID):
        body (PatchedExternalLinkRequest):
        body (PatchedExternalLinkRequestForm):
        body (PatchedExternalLinkRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExternalLink
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
