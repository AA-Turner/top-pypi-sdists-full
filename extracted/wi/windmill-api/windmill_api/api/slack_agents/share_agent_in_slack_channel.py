from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.share_agent_in_slack_channel_json_body import ShareAgentInSlackChannelJsonBody
from ...types import Response


def _get_kwargs(
    workspace: str,
    path: str,
    *,
    json_body: ShareAgentInSlackChannelJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/slack_agents/agent_channels/{path}".format(
            workspace=workspace,
            path=path,
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
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ShareAgentInSlackChannelJsonBody,
) -> Response[Any]:
    """share an agent in a Slack channel, or change how it answers there

     the workspace members in the channel whose Slack email matches and who can read the agent can then
    ask it, or anyone there when its settings say so (slack_anyone, with run_on_behalf_of). Needs edit
    access to the agent; making it the channel's default takes an admin.

    Args:
        workspace (str):
        path (str):
        json_body (ShareAgentInSlackChannelJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ShareAgentInSlackChannelJsonBody,
) -> Response[Any]:
    """share an agent in a Slack channel, or change how it answers there

     the workspace members in the channel whose Slack email matches and who can read the agent can then
    ask it, or anyone there when its settings say so (slack_anyone, with run_on_behalf_of). Needs edit
    access to the agent; making it the channel's default takes an admin.

    Args:
        workspace (str):
        path (str):
        json_body (ShareAgentInSlackChannelJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
