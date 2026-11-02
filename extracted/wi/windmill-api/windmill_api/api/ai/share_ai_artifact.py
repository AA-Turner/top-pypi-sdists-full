from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.share_ai_artifact_json_body import ShareAiArtifactJsonBody
from ...models.share_ai_artifact_response_200 import ShareAiArtifactResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    *,
    json_body: ShareAiArtifactJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/ai/shared_artifacts/share".format(
            workspace=workspace,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ShareAiArtifactResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ShareAiArtifactResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ShareAiArtifactResponse200]:
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
    json_body: ShareAiArtifactJsonBody,
) -> Response[ShareAiArtifactResponse200]:
    """share an AI session artifact with the workspace

     Stores a read-only copy that any member of the workspace can open by id. Sharing the same artifact
    again updates that copy, keeps its id, and restarts its retention window.

    Args:
        workspace (str):
        json_body (ShareAiArtifactJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ShareAiArtifactResponse200]
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
    json_body: ShareAiArtifactJsonBody,
) -> Optional[ShareAiArtifactResponse200]:
    """share an AI session artifact with the workspace

     Stores a read-only copy that any member of the workspace can open by id. Sharing the same artifact
    again updates that copy, keeps its id, and restarts its retention window.

    Args:
        workspace (str):
        json_body (ShareAiArtifactJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ShareAiArtifactResponse200
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
    json_body: ShareAiArtifactJsonBody,
) -> Response[ShareAiArtifactResponse200]:
    """share an AI session artifact with the workspace

     Stores a read-only copy that any member of the workspace can open by id. Sharing the same artifact
    again updates that copy, keeps its id, and restarts its retention window.

    Args:
        workspace (str):
        json_body (ShareAiArtifactJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ShareAiArtifactResponse200]
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
    json_body: ShareAiArtifactJsonBody,
) -> Optional[ShareAiArtifactResponse200]:
    """share an AI session artifact with the workspace

     Stores a read-only copy that any member of the workspace can open by id. Sharing the same artifact
    again updates that copy, keeps its id, and restarts its retention window.

    Args:
        workspace (str):
        json_body (ShareAiArtifactJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ShareAiArtifactResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            json_body=json_body,
        )
    ).parsed
