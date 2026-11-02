from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.share_ai_session_json_body import ShareAiSessionJsonBody
from ...models.share_ai_session_response_200 import ShareAiSessionResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    *,
    json_body: ShareAiSessionJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/ai/shared_sessions/share".format(
            workspace=workspace,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ShareAiSessionResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ShareAiSessionResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ShareAiSessionResponse200]:
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
    json_body: ShareAiSessionJsonBody,
) -> Response[ShareAiSessionResponse200]:
    """share an AI session transcript by link

     Stores a read-only snapshot of the session that members of the workspace can open by id, or anyone
    with the link once it is public. Sharing the same session again updates that snapshot and keeps its
    id.

    Args:
        workspace (str):
        json_body (ShareAiSessionJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ShareAiSessionResponse200]
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
    json_body: ShareAiSessionJsonBody,
) -> Optional[ShareAiSessionResponse200]:
    """share an AI session transcript by link

     Stores a read-only snapshot of the session that members of the workspace can open by id, or anyone
    with the link once it is public. Sharing the same session again updates that snapshot and keeps its
    id.

    Args:
        workspace (str):
        json_body (ShareAiSessionJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ShareAiSessionResponse200
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
    json_body: ShareAiSessionJsonBody,
) -> Response[ShareAiSessionResponse200]:
    """share an AI session transcript by link

     Stores a read-only snapshot of the session that members of the workspace can open by id, or anyone
    with the link once it is public. Sharing the same session again updates that snapshot and keeps its
    id.

    Args:
        workspace (str):
        json_body (ShareAiSessionJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ShareAiSessionResponse200]
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
    json_body: ShareAiSessionJsonBody,
) -> Optional[ShareAiSessionResponse200]:
    """share an AI session transcript by link

     Stores a read-only snapshot of the session that members of the workspace can open by id, or anyone
    with the link once it is public. Sharing the same session again updates that snapshot and keeps its
    id.

    Args:
        workspace (str):
        json_body (ShareAiSessionJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ShareAiSessionResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            json_body=json_body,
        )
    ).parsed
