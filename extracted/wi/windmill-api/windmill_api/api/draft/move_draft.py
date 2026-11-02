from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.move_draft_json_body import MoveDraftJsonBody
from ...models.move_draft_kind import MoveDraftKind
from ...types import Response


def _get_kwargs(
    workspace: str,
    kind: MoveDraftKind,
    path: str,
    *,
    json_body: MoveDraftJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/drafts/move/{kind}/{path}".format(
            workspace=workspace,
            kind=kind,
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
    kind: MoveDraftKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: MoveDraftJsonBody,
) -> Response[Any]:
    """move the current user's draft-only item to another path

     Relocates the authed user's own draft row, along with both path keys inside its value (the typed
    path and the mirror the editors keep beside it). Only for draft-only items — a deployed item must be
    moved through its own deploy endpoint, which carries every draft with it. Restricted to script,
    flow, app and raw_app; any other kind is rejected with 400, because only these keep their deploy
    target where this endpoint rewrites it.

    Args:
        workspace (str):
        kind (MoveDraftKind):
        path (str):
        json_body (MoveDraftJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        kind=kind,
        path=path,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    workspace: str,
    kind: MoveDraftKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: MoveDraftJsonBody,
) -> Response[Any]:
    """move the current user's draft-only item to another path

     Relocates the authed user's own draft row, along with both path keys inside its value (the typed
    path and the mirror the editors keep beside it). Only for draft-only items — a deployed item must be
    moved through its own deploy endpoint, which carries every draft with it. Restricted to script,
    flow, app and raw_app; any other kind is rejected with 400, because only these keep their deploy
    target where this endpoint rewrites it.

    Args:
        workspace (str):
        kind (MoveDraftKind):
        path (str):
        json_body (MoveDraftJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        kind=kind,
        path=path,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
