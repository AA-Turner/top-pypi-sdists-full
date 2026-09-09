from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.set_native_trigger_enabled_json_body import SetNativeTriggerEnabledJsonBody
from ...models.set_native_trigger_enabled_service_name import SetNativeTriggerEnabledServiceName
from ...types import Response


def _get_kwargs(
    workspace: str,
    service_name: SetNativeTriggerEnabledServiceName,
    external_id: str,
    *,
    json_body: SetNativeTriggerEnabledJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/native_triggers/{service_name}/setenabled/{external_id}".format(
            workspace=workspace,
            service_name=service_name,
            external_id=external_id,
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
    service_name: SetNativeTriggerEnabledServiceName,
    external_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SetNativeTriggerEnabledJsonBody,
) -> Response[Any]:
    """set enabled state of native trigger

     Enables or disables a native trigger. A disabled trigger stays registered on the
    external service but starts no job when it fires.
    Requires write access to the script or flow that the trigger is associated with.

    Args:
        workspace (str):
        service_name (SetNativeTriggerEnabledServiceName):
        external_id (str):
        json_body (SetNativeTriggerEnabledJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        service_name=service_name,
        external_id=external_id,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    workspace: str,
    service_name: SetNativeTriggerEnabledServiceName,
    external_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: SetNativeTriggerEnabledJsonBody,
) -> Response[Any]:
    """set enabled state of native trigger

     Enables or disables a native trigger. A disabled trigger stays registered on the
    external service but starts no job when it fires.
    Requires write access to the script or flow that the trigger is associated with.

    Args:
        workspace (str):
        service_name (SetNativeTriggerEnabledServiceName):
        external_id (str):
        json_body (SetNativeTriggerEnabledJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        service_name=service_name,
        external_id=external_id,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
