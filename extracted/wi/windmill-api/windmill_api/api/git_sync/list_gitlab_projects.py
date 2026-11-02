from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_gitlab_projects_json_body import ListGitlabProjectsJsonBody
from ...models.list_gitlab_projects_response_200_item import ListGitlabProjectsResponse200Item
from ...types import Response


def _get_kwargs(
    workspace: str,
    *,
    json_body: ListGitlabProjectsJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/git_sync/gitlab/projects".format(
            workspace=workspace,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["ListGitlabProjectsResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListGitlabProjectsResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["ListGitlabProjectsResponse200Item"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ListGitlabProjectsJsonBody,
) -> Response[List["ListGitlabProjectsResponse200Item"]]:
    """List the GitLab projects a token can sync

     Lists the projects the supplied GitLab token can push to, so a git repository resource can be filled
    in without hand-writing a project path. The token is used for this call only and is never stored.
    Requires workspace admin.

    Args:
        workspace (str):
        json_body (ListGitlabProjectsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListGitlabProjectsResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ListGitlabProjectsJsonBody,
) -> Optional[List["ListGitlabProjectsResponse200Item"]]:
    """List the GitLab projects a token can sync

     Lists the projects the supplied GitLab token can push to, so a git repository resource can be filled
    in without hand-writing a project path. The token is used for this call only and is never stored.
    Requires workspace admin.

    Args:
        workspace (str):
        json_body (ListGitlabProjectsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListGitlabProjectsResponse200Item']
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ListGitlabProjectsJsonBody,
) -> Response[List["ListGitlabProjectsResponse200Item"]]:
    """List the GitLab projects a token can sync

     Lists the projects the supplied GitLab token can push to, so a git repository resource can be filled
    in without hand-writing a project path. The token is used for this call only and is never stored.
    Requires workspace admin.

    Args:
        workspace (str):
        json_body (ListGitlabProjectsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['ListGitlabProjectsResponse200Item']]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ListGitlabProjectsJsonBody,
) -> Optional[List["ListGitlabProjectsResponse200Item"]]:
    """List the GitLab projects a token can sync

     Lists the projects the supplied GitLab token can push to, so a git repository resource can be filled
    in without hand-writing a project path. The token is used for this call only and is never stored.
    Requires workspace admin.

    Args:
        workspace (str):
        json_body (ListGitlabProjectsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['ListGitlabProjectsResponse200Item']
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            json_body=json_body,
        )
    ).parsed
