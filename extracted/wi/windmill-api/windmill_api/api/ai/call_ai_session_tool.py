from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.call_ai_session_tool_json_body import CallAiSessionToolJsonBody
from ...models.call_ai_session_tool_response_200 import CallAiSessionToolResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    name: str,
    *,
    json_body: CallAiSessionToolJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/ai_session_tools/{name}".format(
            workspace=workspace,
            name=name,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[CallAiSessionToolResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CallAiSessionToolResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CallAiSessionToolResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CallAiSessionToolJsonBody,
) -> Response[CallAiSessionToolResponse200]:
    """run one of the AI session's tools as the calling user

     The in-app chat's entry to the session toolset the MCP server also serves. Refused for job tokens
    and scoped tokens.

    Args:
        workspace (str):
        name (str):
        json_body (CallAiSessionToolJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallAiSessionToolResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        name=name,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CallAiSessionToolJsonBody,
) -> Optional[CallAiSessionToolResponse200]:
    """run one of the AI session's tools as the calling user

     The in-app chat's entry to the session toolset the MCP server also serves. Refused for job tokens
    and scoped tokens.

    Args:
        workspace (str):
        name (str):
        json_body (CallAiSessionToolJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallAiSessionToolResponse200
    """

    return sync_detailed(
        workspace=workspace,
        name=name,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CallAiSessionToolJsonBody,
) -> Response[CallAiSessionToolResponse200]:
    """run one of the AI session's tools as the calling user

     The in-app chat's entry to the session toolset the MCP server also serves. Refused for job tokens
    and scoped tokens.

    Args:
        workspace (str):
        name (str):
        json_body (CallAiSessionToolJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallAiSessionToolResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        name=name,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CallAiSessionToolJsonBody,
) -> Optional[CallAiSessionToolResponse200]:
    """run one of the AI session's tools as the calling user

     The in-app chat's entry to the session toolset the MCP server also serves. Refused for job tokens
    and scoped tokens.

    Args:
        workspace (str):
        name (str):
        json_body (CallAiSessionToolJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallAiSessionToolResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            name=name,
            client=client,
            json_body=json_body,
        )
    ).parsed
