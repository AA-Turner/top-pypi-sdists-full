from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.patched_project_info_request import PatchedProjectInfoRequest
from ...models.project_info import ProjectInfo
from ...types import Response


def _get_kwargs(
    project: int,
    *,
    body: PatchedProjectInfoRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/api/openportal-projectinfo/{project}/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ProjectInfo:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ProjectInfo.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProjectInfo]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project: int,
    *,
    client: AuthenticatedClient,
    body: PatchedProjectInfoRequest,
) -> Response[ProjectInfo]:
    """
    Args:
        project (int):
        body (PatchedProjectInfoRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProjectInfo]
    """

    kwargs = _get_kwargs(
        project=project,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    project: int,
    *,
    client: AuthenticatedClient,
    body: PatchedProjectInfoRequest,
) -> ProjectInfo:
    """
    Args:
        project (int):
        body (PatchedProjectInfoRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProjectInfo
    """

    return sync_detailed(
        project=project,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    project: int,
    *,
    client: AuthenticatedClient,
    body: PatchedProjectInfoRequest,
) -> Response[ProjectInfo]:
    """
    Args:
        project (int):
        body (PatchedProjectInfoRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProjectInfo]
    """

    kwargs = _get_kwargs(
        project=project,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    project: int,
    *,
    client: AuthenticatedClient,
    body: PatchedProjectInfoRequest,
) -> ProjectInfo:
    """
    Args:
        project (int):
        body (PatchedProjectInfoRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProjectInfo
    """

    return (
        await asyncio_detailed(
            project=project,
            client=client,
            body=body,
        )
    ).parsed
