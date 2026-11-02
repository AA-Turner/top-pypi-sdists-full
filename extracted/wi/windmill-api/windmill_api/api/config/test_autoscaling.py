from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.test_autoscaling_json_body import TestAutoscalingJsonBody
from ...models.test_autoscaling_response_200 import TestAutoscalingResponse200
from ...types import Response


def _get_kwargs(
    worker_group: str,
    *,
    json_body: TestAutoscalingJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/configs/test_autoscaling/{worker_group}".format(
            worker_group=worker_group,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[TestAutoscalingResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TestAutoscalingResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[TestAutoscalingResponse200]:
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
    json_body: TestAutoscalingJsonBody,
) -> Response[TestAutoscalingResponse200]:
    """Run an autoscaling integration once for a worker group, without recording an autoscaling event

    Args:
        worker_group (str):
        json_body (TestAutoscalingJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TestAutoscalingResponse200]
    """

    kwargs = _get_kwargs(
        worker_group=worker_group,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    worker_group: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: TestAutoscalingJsonBody,
) -> Optional[TestAutoscalingResponse200]:
    """Run an autoscaling integration once for a worker group, without recording an autoscaling event

    Args:
        worker_group (str):
        json_body (TestAutoscalingJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TestAutoscalingResponse200
    """

    return sync_detailed(
        worker_group=worker_group,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    worker_group: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: TestAutoscalingJsonBody,
) -> Response[TestAutoscalingResponse200]:
    """Run an autoscaling integration once for a worker group, without recording an autoscaling event

    Args:
        worker_group (str):
        json_body (TestAutoscalingJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TestAutoscalingResponse200]
    """

    kwargs = _get_kwargs(
        worker_group=worker_group,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    worker_group: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: TestAutoscalingJsonBody,
) -> Optional[TestAutoscalingResponse200]:
    """Run an autoscaling integration once for a worker group, without recording an autoscaling event

    Args:
        worker_group (str):
        json_body (TestAutoscalingJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TestAutoscalingResponse200
    """

    return (
        await asyncio_detailed(
            worker_group=worker_group,
            client=client,
            json_body=json_body,
        )
    ).parsed
