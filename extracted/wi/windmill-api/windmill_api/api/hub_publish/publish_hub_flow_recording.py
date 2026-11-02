from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.publish_hub_flow_recording_json_body import PublishHubFlowRecordingJsonBody
from ...types import UNSET, Response


def _get_kwargs(
    workspace: str,
    flow_id: int,
    *,
    json_body: PublishHubFlowRecordingJsonBody,
    folder: str,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["folder"] = folder

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/hub/flows/{flow_id}/recording".format(
            workspace=workspace,
            flow_id=flow_id,
        ),
        "json": json_json_body,
        "params": params,
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
    flow_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: PublishHubFlowRecordingJsonBody,
    folder: str,
) -> Response[Any]:
    """attach a recording to a hub flow

     Requires the caller to be a workspace admin. Forwards the request to the
    configured Hub scoped to the `{workspace}:{folder}` source and returns
    the Hub's status code and raw response body.

    Args:
        workspace (str):
        flow_id (int):
        folder (str):
        json_body (PublishHubFlowRecordingJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        flow_id=flow_id,
        json_body=json_body,
        folder=folder,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    workspace: str,
    flow_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: PublishHubFlowRecordingJsonBody,
    folder: str,
) -> Response[Any]:
    """attach a recording to a hub flow

     Requires the caller to be a workspace admin. Forwards the request to the
    configured Hub scoped to the `{workspace}:{folder}` source and returns
    the Hub's status code and raw response body.

    Args:
        workspace (str):
        flow_id (int):
        folder (str):
        json_body (PublishHubFlowRecordingJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        flow_id=flow_id,
        json_body=json_body,
        folder=folder,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
