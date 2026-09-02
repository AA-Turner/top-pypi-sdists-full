from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_native_trigger_service_json_body import CreateNativeTriggerServiceJsonBody
from ...models.create_native_trigger_service_service_name import CreateNativeTriggerServiceServiceName
from ...types import Response


def _get_kwargs(
    workspace: str,
    service_name: CreateNativeTriggerServiceServiceName,
    *,
    json_body: CreateNativeTriggerServiceJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/native_triggers/integrations/{service_name}/create".format(
            workspace=workspace,
            service_name=service_name,
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
    service_name: CreateNativeTriggerServiceServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CreateNativeTriggerServiceJsonBody,
) -> Response[Any]:
    """create native trigger service

    Args:
        workspace (str):
        service_name (CreateNativeTriggerServiceServiceName):
        json_body (CreateNativeTriggerServiceJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        service_name=service_name,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    workspace: str,
    service_name: CreateNativeTriggerServiceServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CreateNativeTriggerServiceJsonBody,
) -> Response[Any]:
    """create native trigger service

    Args:
        workspace (str):
        service_name (CreateNativeTriggerServiceServiceName):
        json_body (CreateNativeTriggerServiceJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        service_name=service_name,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
