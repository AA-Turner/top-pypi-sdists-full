from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.native_trigger_service_callback_json_body import NativeTriggerServiceCallbackJsonBody
from ...models.native_trigger_service_callback_service_name import NativeTriggerServiceCallbackServiceName
from ...types import Response


def _get_kwargs(
    workspace: str,
    service_name: NativeTriggerServiceCallbackServiceName,
    *,
    json_body: NativeTriggerServiceCallbackJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/native_triggers/integrations/{service_name}/callback".format(
            workspace=workspace,
            service_name=service_name,
        ),
        "json": json_json_body,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[str]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(str, response.json())
        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    service_name: NativeTriggerServiceCallbackServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: NativeTriggerServiceCallbackJsonBody,
) -> Response[str]:
    """native trigger service oauth callback

    Args:
        workspace (str):
        service_name (NativeTriggerServiceCallbackServiceName):
        json_body (NativeTriggerServiceCallbackJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
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


def sync(
    workspace: str,
    service_name: NativeTriggerServiceCallbackServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: NativeTriggerServiceCallbackJsonBody,
) -> Optional[str]:
    """native trigger service oauth callback

    Args:
        workspace (str):
        service_name (NativeTriggerServiceCallbackServiceName):
        json_body (NativeTriggerServiceCallbackJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        str
    """

    return sync_detailed(
        workspace=workspace,
        service_name=service_name,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    service_name: NativeTriggerServiceCallbackServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: NativeTriggerServiceCallbackJsonBody,
) -> Response[str]:
    """native trigger service oauth callback

    Args:
        workspace (str):
        service_name (NativeTriggerServiceCallbackServiceName):
        json_body (NativeTriggerServiceCallbackJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        service_name=service_name,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    service_name: NativeTriggerServiceCallbackServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: NativeTriggerServiceCallbackJsonBody,
) -> Optional[str]:
    """native trigger service oauth callback

    Args:
        workspace (str):
        service_name (NativeTriggerServiceCallbackServiceName):
        json_body (NativeTriggerServiceCallbackJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        str
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            service_name=service_name,
            client=client,
            json_body=json_body,
        )
    ).parsed
