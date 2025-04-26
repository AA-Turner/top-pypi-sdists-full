from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.move_captures_and_configs_json_body import MoveCapturesAndConfigsJsonBody
from ...models.move_captures_and_configs_runnable_kind import MoveCapturesAndConfigsRunnableKind
from ...types import Response


def _get_kwargs(
    workspace: str,
    runnable_kind: MoveCapturesAndConfigsRunnableKind,
    path: str,
    *,
    json_body: MoveCapturesAndConfigsJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/capture/move/{runnable_kind}/{path}".format(
            workspace=workspace,
            runnable_kind=runnable_kind,
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
    runnable_kind: MoveCapturesAndConfigsRunnableKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: MoveCapturesAndConfigsJsonBody,
) -> Response[Any]:
    """move captures and configs for a script or flow

    Args:
        workspace (str):
        runnable_kind (MoveCapturesAndConfigsRunnableKind):
        path (str):
        json_body (MoveCapturesAndConfigsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        runnable_kind=runnable_kind,
        path=path,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    workspace: str,
    runnable_kind: MoveCapturesAndConfigsRunnableKind,
    path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: MoveCapturesAndConfigsJsonBody,
) -> Response[Any]:
    """move captures and configs for a script or flow

    Args:
        workspace (str):
        runnable_kind (MoveCapturesAndConfigsRunnableKind):
        path (str):
        json_body (MoveCapturesAndConfigsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        runnable_kind=runnable_kind,
        path=path,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
