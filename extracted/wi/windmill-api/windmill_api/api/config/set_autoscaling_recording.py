from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.set_autoscaling_recording_json_body import SetAutoscalingRecordingJsonBody
from ...types import Response


def _get_kwargs(
    worker_group: str,
    *,
    json_body: SetAutoscalingRecordingJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/configs/autoscaling_recording/{worker_group}".format(
            worker_group=worker_group,
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
    worker_group: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SetAutoscalingRecordingJsonBody,
) -> Response[Any]:
    """Start recording the autoscaling decisions of a worker group for 24 hours, or stop

    Args:
        worker_group (str):
        json_body (SetAutoscalingRecordingJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        worker_group=worker_group,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    worker_group: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SetAutoscalingRecordingJsonBody,
) -> Response[Any]:
    """Start recording the autoscaling decisions of a worker group for 24 hours, or stop

    Args:
        worker_group (str):
        json_body (SetAutoscalingRecordingJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        worker_group=worker_group,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
