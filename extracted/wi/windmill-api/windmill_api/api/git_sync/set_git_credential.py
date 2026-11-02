from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.set_git_credential_json_body import SetGitCredentialJsonBody
from ...types import Response


def _get_kwargs(
    workspace: str,
    *,
    json_body: SetGitCredentialJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/git_sync/credential".format(
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
    json_body: SetGitCredentialJsonBody,
) -> Response[Any]:
    """Store the credential for a git repository

     Stores the access token a git repository authenticates with, so it does not have to be written into
    the repository URL or a workspace variable. The token is write-only: it is served only to a git-sync
    job that presents its own job token, and a fork of this workspace reads this copy instead of holding
    one of its own. Requires workspace admin.

    Args:
        workspace (str):
        json_body (SetGitCredentialJsonBody):

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
    json_body: SetGitCredentialJsonBody,
) -> Response[Any]:
    """Store the credential for a git repository

     Stores the access token a git repository authenticates with, so it does not have to be written into
    the repository URL or a workspace variable. The token is write-only: it is served only to a git-sync
    job that presents its own job token, and a fork of this workspace reads this copy instead of holding
    one of its own. Requires workspace admin.

    Args:
        workspace (str):
        json_body (SetGitCredentialJsonBody):

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
