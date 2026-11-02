from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.connect_remote_deploy_json_body import ConnectRemoteDeployJsonBody
from ...models.connect_remote_deploy_response_200 import ConnectRemoteDeployResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    *,
    json_body: ConnectRemoteDeployJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/remote_deploy/connect".format(
            workspace=workspace,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ConnectRemoteDeployResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ConnectRemoteDeployResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ConnectRemoteDeployResponse200]:
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
    json_body: ConnectRemoteDeployJsonBody,
) -> Response[ConnectRemoteDeployResponse200]:
    """store the caller's own token for the remote deploy target

     The token is checked against the target's whoami before it is stored. `target` names the
    target the token was obtained for, and the request is refused if the workspace now points
    elsewhere, so a token is never sent to an instance it was not meant for.

    Args:
        workspace (str):
        json_body (ConnectRemoteDeployJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConnectRemoteDeployResponse200]
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
    json_body: ConnectRemoteDeployJsonBody,
) -> Optional[ConnectRemoteDeployResponse200]:
    """store the caller's own token for the remote deploy target

     The token is checked against the target's whoami before it is stored. `target` names the
    target the token was obtained for, and the request is refused if the workspace now points
    elsewhere, so a token is never sent to an instance it was not meant for.

    Args:
        workspace (str):
        json_body (ConnectRemoteDeployJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConnectRemoteDeployResponse200
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
    json_body: ConnectRemoteDeployJsonBody,
) -> Response[ConnectRemoteDeployResponse200]:
    """store the caller's own token for the remote deploy target

     The token is checked against the target's whoami before it is stored. `target` names the
    target the token was obtained for, and the request is refused if the workspace now points
    elsewhere, so a token is never sent to an instance it was not meant for.

    Args:
        workspace (str):
        json_body (ConnectRemoteDeployJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConnectRemoteDeployResponse200]
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
    json_body: ConnectRemoteDeployJsonBody,
) -> Optional[ConnectRemoteDeployResponse200]:
    """store the caller's own token for the remote deploy target

     The token is checked against the target's whoami before it is stored. `target` names the
    target the token was obtained for, and the request is refused if the workspace now points
    elsewhere, so a token is never sent to an instance it was not meant for.

    Args:
        workspace (str):
        json_body (ConnectRemoteDeployJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConnectRemoteDeployResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            json_body=json_body,
        )
    ).parsed
