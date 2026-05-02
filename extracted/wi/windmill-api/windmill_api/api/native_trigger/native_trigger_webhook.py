from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.native_trigger_webhook_json_body import NativeTriggerWebhookJsonBody
from ...models.native_trigger_webhook_service_name import NativeTriggerWebhookServiceName
from ...types import Response


def _get_kwargs(
    service_name: NativeTriggerWebhookServiceName,
    workspace_id: str,
    internal_id: int,
    *,
    json_body: NativeTriggerWebhookJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/native_triggers/{service_name}/w/{workspace_id}/webhook/{internal_id}".format(
            service_name=service_name,
            workspace_id=workspace_id,
            internal_id=internal_id,
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
    service_name: NativeTriggerWebhookServiceName,
    workspace_id: str,
    internal_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: NativeTriggerWebhookJsonBody,
) -> Response[Any]:
    """receive webhook from external native trigger service

    Args:
        service_name (NativeTriggerWebhookServiceName):
        workspace_id (str):
        internal_id (int):
        json_body (NativeTriggerWebhookJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        service_name=service_name,
        workspace_id=workspace_id,
        internal_id=internal_id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    service_name: NativeTriggerWebhookServiceName,
    workspace_id: str,
    internal_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: NativeTriggerWebhookJsonBody,
) -> Response[Any]:
    """receive webhook from external native trigger service

    Args:
        service_name (NativeTriggerWebhookServiceName):
        workspace_id (str):
        internal_id (int):
        json_body (NativeTriggerWebhookJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        service_name=service_name,
        workspace_id=workspace_id,
        internal_id=internal_id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
