from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.call_mcp_tool_json_body import CallMcpToolJsonBody
from ...models.call_mcp_tool_response_200 import CallMcpToolResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    path: str,
    *,
    json_body: CallMcpToolJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/resources/mcp_call_tool/{path}".format(
            workspace=workspace,
            path=path,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[CallMcpToolResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CallMcpToolResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CallMcpToolResponse200]:
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
    json_body: CallMcpToolJsonBody,
) -> Response[CallMcpToolResponse200]:
    """call a tool on the MCP server described by the resource

    Args:
        workspace (str):
        path (str):
        json_body (CallMcpToolJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallMcpToolResponse200]
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


def sync(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CallMcpToolJsonBody,
) -> Optional[CallMcpToolResponse200]:
    """call a tool on the MCP server described by the resource

    Args:
        workspace (str):
        path (str):
        json_body (CallMcpToolJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallMcpToolResponse200
    """

    return sync_detailed(
        workspace=workspace,
        path=path,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CallMcpToolJsonBody,
) -> Response[CallMcpToolResponse200]:
    """call a tool on the MCP server described by the resource

    Args:
        workspace (str):
        path (str):
        json_body (CallMcpToolJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallMcpToolResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CallMcpToolJsonBody,
) -> Optional[CallMcpToolResponse200]:
    """call a tool on the MCP server described by the resource

    Args:
        workspace (str):
        path (str):
        json_body (CallMcpToolJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallMcpToolResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            path=path,
            client=client,
            json_body=json_body,
        )
    ).parsed
