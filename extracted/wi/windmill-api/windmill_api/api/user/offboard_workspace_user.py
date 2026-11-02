from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.offboard_workspace_user_json_body import OffboardWorkspaceUserJsonBody
from ...models.offboard_workspace_user_response_200 import OffboardWorkspaceUserResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    username: str,
    *,
    json_body: OffboardWorkspaceUserJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/users/offboard/{username}".format(
            workspace=workspace,
            username=username,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[OffboardWorkspaceUserResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = OffboardWorkspaceUserResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[OffboardWorkspaceUserResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    username: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: OffboardWorkspaceUserJsonBody,
) -> Response[OffboardWorkspaceUserResponse200]:
    """offboard a workspace user (reassign objects, optionally delete user)

    Args:
        workspace (str):
        username (str):
        json_body (OffboardWorkspaceUserJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OffboardWorkspaceUserResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        username=username,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    username: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: OffboardWorkspaceUserJsonBody,
) -> Optional[OffboardWorkspaceUserResponse200]:
    """offboard a workspace user (reassign objects, optionally delete user)

    Args:
        workspace (str):
        username (str):
        json_body (OffboardWorkspaceUserJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OffboardWorkspaceUserResponse200
    """

    return sync_detailed(
        workspace=workspace,
        username=username,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    username: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: OffboardWorkspaceUserJsonBody,
) -> Response[OffboardWorkspaceUserResponse200]:
    """offboard a workspace user (reassign objects, optionally delete user)

    Args:
        workspace (str):
        username (str):
        json_body (OffboardWorkspaceUserJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OffboardWorkspaceUserResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        username=username,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    username: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: OffboardWorkspaceUserJsonBody,
) -> Optional[OffboardWorkspaceUserResponse200]:
    """offboard a workspace user (reassign objects, optionally delete user)

    Args:
        workspace (str):
        username (str):
        json_body (OffboardWorkspaceUserJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OffboardWorkspaceUserResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            username=username,
            client=client,
            json_body=json_body,
        )
    ).parsed
