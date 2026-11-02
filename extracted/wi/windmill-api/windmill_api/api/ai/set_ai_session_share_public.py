from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.set_ai_session_share_public_json_body import SetAiSessionSharePublicJsonBody
from ...models.set_ai_session_share_public_response_200 import SetAiSessionSharePublicResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    id: str,
    *,
    json_body: SetAiSessionSharePublicJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/ai/shared_sessions/set_public/{id}".format(
            workspace=workspace,
            id=id,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[SetAiSessionSharePublicResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = SetAiSessionSharePublicResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[SetAiSessionSharePublicResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SetAiSessionSharePublicJsonBody,
) -> Response[SetAiSessionSharePublicResponse200]:
    """make a shared AI session public, or reserve it to workspace members

    Args:
        workspace (str):
        id (str):
        json_body (SetAiSessionSharePublicJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SetAiSessionSharePublicResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SetAiSessionSharePublicJsonBody,
) -> Optional[SetAiSessionSharePublicResponse200]:
    """make a shared AI session public, or reserve it to workspace members

    Args:
        workspace (str):
        id (str):
        json_body (SetAiSessionSharePublicJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SetAiSessionSharePublicResponse200
    """

    return sync_detailed(
        workspace=workspace,
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SetAiSessionSharePublicJsonBody,
) -> Response[SetAiSessionSharePublicResponse200]:
    """make a shared AI session public, or reserve it to workspace members

    Args:
        workspace (str):
        id (str):
        json_body (SetAiSessionSharePublicJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SetAiSessionSharePublicResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        id=id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SetAiSessionSharePublicJsonBody,
) -> Optional[SetAiSessionSharePublicResponse200]:
    """make a shared AI session public, or reserve it to workspace members

    Args:
        workspace (str):
        id (str):
        json_body (SetAiSessionSharePublicJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SetAiSessionSharePublicResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
