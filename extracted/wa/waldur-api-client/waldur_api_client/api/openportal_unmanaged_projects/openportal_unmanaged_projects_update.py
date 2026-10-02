from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.project import Project
from ...models.project_request import ProjectRequest
from ...models.project_request_form import ProjectRequestForm
from ...models.project_request_multipart import ProjectRequestMultipart
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: Union[
        ProjectRequest,
        ProjectRequestForm,
        ProjectRequestMultipart,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/api/openportal-unmanaged-projects/{uuid}/",
    }

    if isinstance(body, ProjectRequest):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"
    if isinstance(body, ProjectRequestForm):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, ProjectRequestMultipart):
        _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Project:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = Project.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Project]:
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
        ProjectRequest,
        ProjectRequestForm,
        ProjectRequestMultipart,
    ],
) -> Response[Project]:
    """Update project details

     Update the details of a project. Requires project administrator or customer owner permissions.

    Args:
        uuid (UUID):
        body (ProjectRequest):
        body (ProjectRequestForm):
        body (ProjectRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Project]
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
        ProjectRequest,
        ProjectRequestForm,
        ProjectRequestMultipart,
    ],
) -> Project:
    """Update project details

     Update the details of a project. Requires project administrator or customer owner permissions.

    Args:
        uuid (UUID):
        body (ProjectRequest):
        body (ProjectRequestForm):
        body (ProjectRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Project
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
        ProjectRequest,
        ProjectRequestForm,
        ProjectRequestMultipart,
    ],
) -> Response[Project]:
    """Update project details

     Update the details of a project. Requires project administrator or customer owner permissions.

    Args:
        uuid (UUID):
        body (ProjectRequest):
        body (ProjectRequestForm):
        body (ProjectRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Project]
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
        ProjectRequest,
        ProjectRequestForm,
        ProjectRequestMultipart,
    ],
) -> Project:
    """Update project details

     Update the details of a project. Requires project administrator or customer owner permissions.

    Args:
        uuid (UUID):
        body (ProjectRequest):
        body (ProjectRequestForm):
        body (ProjectRequestMultipart):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Project
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
