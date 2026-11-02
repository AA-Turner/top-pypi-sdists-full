from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_add_admins_and_developers_to_forks_json_body import EditAddAdminsAndDevelopersToForksJsonBody
from ...types import Response


def _get_kwargs(
    workspace: str,
    *,
    json_body: EditAddAdminsAndDevelopersToForksJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/workspaces/edit_add_admins_and_developers_to_forks".format(
            workspace=workspace,
        ),
        "json": json_json_body,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
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
    json_body: EditAddAdminsAndDevelopersToForksJsonBody,
) -> Response[Any]:
    """choose whether new forks of this workspace start with its admins and developers

     When on, every fork created from this workspace gets the workspace's admins and developers as
    members, with the role they hold here; operators, disabled users and service accounts are left out.
    The setting is copied into each fork, so forks of a fork follow it too. Off by default. Workspace-
    admin gated.

    Args:
        workspace (str):
        json_body (EditAddAdminsAndDevelopersToForksJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: EditAddAdminsAndDevelopersToForksJsonBody,
) -> Response[Any]:
    """choose whether new forks of this workspace start with its admins and developers

     When on, every fork created from this workspace gets the workspace's admins and developers as
    members, with the role they hold here; operators, disabled users and service accounts are left out.
    The setting is copied into each fork, so forks of a fork follow it too. Off by default. Workspace-
    admin gated.

    Args:
        workspace (str):
        json_body (EditAddAdminsAndDevelopersToForksJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
