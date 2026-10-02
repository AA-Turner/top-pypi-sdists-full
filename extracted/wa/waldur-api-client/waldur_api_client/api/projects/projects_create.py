from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.project import Project
from ...models.project_request import ProjectRequest
from ...models.project_request_form import ProjectRequestForm
from ...models.project_request_multipart import ProjectRequestMultipart
from ...types import Response


def _get_kwargs(
    *,
    body: Union[
        ProjectRequest,
        ProjectRequestForm,
        ProjectRequestMultipart,
    ],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/projects/",
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
    if response.status_code == 201:
        response_201 = Project.from_dict(response.json())

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Project]:
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
        ProjectRequest,
        ProjectRequestForm,
        ProjectRequestMultipart,
    ],
) -> Response[Project]:
    """Create a new project

     A new project can be created by users with staff privilege (is_staff=True) or customer owners.
    Project resource quota is optional.

    Args:
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
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: Union[
        ProjectRequest,
        ProjectRequestForm,
        ProjectRequestMultipart,
    ],
) -> Project:
    """Create a new project

     A new project can be created by users with staff privilege (is_staff=True) or customer owners.
    Project resource quota is optional.

    Args:
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
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: Union[
        ProjectRequest,
        ProjectRequestForm,
        ProjectRequestMultipart,
    ],
) -> Response[Project]:
    """Create a new project

     A new project can be created by users with staff privilege (is_staff=True) or customer owners.
    Project resource quota is optional.

    Args:
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
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: Union[
        ProjectRequest,
        ProjectRequestForm,
        ProjectRequestMultipart,
    ],
) -> Project:
    """Create a new project

     A new project can be created by users with staff privilege (is_staff=True) or customer owners.
    Project resource quota is optional.

    Args:
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
            client=client,
            body=body,
        )
    ).parsed
