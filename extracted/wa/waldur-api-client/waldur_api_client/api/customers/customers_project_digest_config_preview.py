from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.project_digest_preview_request import ProjectDigestPreviewRequest
from ...models.project_digest_preview_response import ProjectDigestPreviewResponse
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: ProjectDigestPreviewRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/customers/{uuid}/project-digest-config/preview/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> ProjectDigestPreviewResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ProjectDigestPreviewResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ProjectDigestPreviewResponse]:
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
    body: ProjectDigestPreviewRequest,
) -> Response[ProjectDigestPreviewResponse]:
    """Preview digest for a project

     Returns rendered HTML preview of the digest for a specific project.

    Args:
        uuid (UUID):
        body (ProjectDigestPreviewRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProjectDigestPreviewResponse]
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
    body: ProjectDigestPreviewRequest,
) -> ProjectDigestPreviewResponse:
    """Preview digest for a project

     Returns rendered HTML preview of the digest for a specific project.

    Args:
        uuid (UUID):
        body (ProjectDigestPreviewRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProjectDigestPreviewResponse
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
    body: ProjectDigestPreviewRequest,
) -> Response[ProjectDigestPreviewResponse]:
    """Preview digest for a project

     Returns rendered HTML preview of the digest for a specific project.

    Args:
        uuid (UUID):
        body (ProjectDigestPreviewRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProjectDigestPreviewResponse]
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
    body: ProjectDigestPreviewRequest,
) -> ProjectDigestPreviewResponse:
    """Preview digest for a project

     Returns rendered HTML preview of the digest for a specific project.

    Args:
        uuid (UUID):
        body (ProjectDigestPreviewRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProjectDigestPreviewResponse
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
