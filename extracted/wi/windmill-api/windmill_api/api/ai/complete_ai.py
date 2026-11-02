from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.complete_ai_json_body import CompleteAiJsonBody
from ...models.complete_ai_response_200 import CompleteAiResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    *,
    json_body: CompleteAiJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/ai/complete".format(
            workspace=workspace,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[CompleteAiResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CompleteAiResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CompleteAiResponse200]:
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
    json_body: CompleteAiJsonBody,
) -> Response[CompleteAiResponse200]:
    """one text completion with the workspace's AI config

     Sends a system and a user message to the configured provider and returns the text of the answer,
    with no tools and no streaming. For callers that do not speak a provider's own API through the
    proxy, such as the CLI and jobs.

    Args:
        workspace (str):
        json_body (CompleteAiJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CompleteAiResponse200]
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
    json_body: CompleteAiJsonBody,
) -> Optional[CompleteAiResponse200]:
    """one text completion with the workspace's AI config

     Sends a system and a user message to the configured provider and returns the text of the answer,
    with no tools and no streaming. For callers that do not speak a provider's own API through the
    proxy, such as the CLI and jobs.

    Args:
        workspace (str):
        json_body (CompleteAiJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CompleteAiResponse200
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
    json_body: CompleteAiJsonBody,
) -> Response[CompleteAiResponse200]:
    """one text completion with the workspace's AI config

     Sends a system and a user message to the configured provider and returns the text of the answer,
    with no tools and no streaming. For callers that do not speak a provider's own API through the
    proxy, such as the CLI and jobs.

    Args:
        workspace (str):
        json_body (CompleteAiJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CompleteAiResponse200]
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
    json_body: CompleteAiJsonBody,
) -> Optional[CompleteAiResponse200]:
    """one text completion with the workspace's AI config

     Sends a system and a user message to the configured provider and returns the text of the answer,
    with no tools and no streaming. For callers that do not speak a provider's own API through the
    proxy, such as the CLI and jobs.

    Args:
        workspace (str):
        json_body (CompleteAiJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CompleteAiResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            json_body=json_body,
        )
    ).parsed
