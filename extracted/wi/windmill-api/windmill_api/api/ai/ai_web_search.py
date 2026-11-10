from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.ai_web_search_json_body import AiWebSearchJsonBody
from ...models.ai_web_search_response_200 import AiWebSearchResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    *,
    json_body: AiWebSearchJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/ai/web_search".format(
            workspace=workspace,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[AiWebSearchResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AiWebSearchResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AiWebSearchResponse200]:
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
    json_body: AiWebSearchJsonBody,
) -> Response[AiWebSearchResponse200]:
    """search the web through the workspace's web search API

     Runs a query against the search API (Exa, Tavily, Linkup or DeepSeek) set in the workspace's AI
    settings, with the key of its resource. The AI chat uses it when the model's provider has no built-
    in web search.

    Args:
        workspace (str):
        json_body (AiWebSearchJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AiWebSearchResponse200]
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
    json_body: AiWebSearchJsonBody,
) -> Optional[AiWebSearchResponse200]:
    """search the web through the workspace's web search API

     Runs a query against the search API (Exa, Tavily, Linkup or DeepSeek) set in the workspace's AI
    settings, with the key of its resource. The AI chat uses it when the model's provider has no built-
    in web search.

    Args:
        workspace (str):
        json_body (AiWebSearchJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AiWebSearchResponse200
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
    json_body: AiWebSearchJsonBody,
) -> Response[AiWebSearchResponse200]:
    """search the web through the workspace's web search API

     Runs a query against the search API (Exa, Tavily, Linkup or DeepSeek) set in the workspace's AI
    settings, with the key of its resource. The AI chat uses it when the model's provider has no built-
    in web search.

    Args:
        workspace (str):
        json_body (AiWebSearchJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AiWebSearchResponse200]
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
    json_body: AiWebSearchJsonBody,
) -> Optional[AiWebSearchResponse200]:
    """search the web through the workspace's web search API

     Runs a query against the search API (Exa, Tavily, Linkup or DeepSeek) set in the workspace's AI
    settings, with the key of its resource. The AI chat uses it when the model's provider has no built-
    in web search.

    Args:
        workspace (str):
        json_body (AiWebSearchJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AiWebSearchResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            json_body=json_body,
        )
    ).parsed
