from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_native_trigger_response_200 import GetNativeTriggerResponse200
from ...models.get_native_trigger_service_name import GetNativeTriggerServiceName
from ...types import Response


def _get_kwargs(
    workspace: str,
    service_name: GetNativeTriggerServiceName,
    external_id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/native_triggers/{service_name}/get/{external_id}".format(
            workspace=workspace,
            service_name=service_name,
            external_id=external_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetNativeTriggerResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetNativeTriggerResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetNativeTriggerResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    service_name: GetNativeTriggerServiceName,
    external_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[GetNativeTriggerResponse200]:
    """get native trigger

     Retrieves a native trigger by its external ID.
    Requires write access to the script or flow that the trigger is associated with.

    Args:
        workspace (str):
        service_name (GetNativeTriggerServiceName):
        external_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetNativeTriggerResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        service_name=service_name,
        external_id=external_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    service_name: GetNativeTriggerServiceName,
    external_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[GetNativeTriggerResponse200]:
    """get native trigger

     Retrieves a native trigger by its external ID.
    Requires write access to the script or flow that the trigger is associated with.

    Args:
        workspace (str):
        service_name (GetNativeTriggerServiceName):
        external_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetNativeTriggerResponse200
    """

    return sync_detailed(
        workspace=workspace,
        service_name=service_name,
        external_id=external_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    service_name: GetNativeTriggerServiceName,
    external_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[GetNativeTriggerResponse200]:
    """get native trigger

     Retrieves a native trigger by its external ID.
    Requires write access to the script or flow that the trigger is associated with.

    Args:
        workspace (str):
        service_name (GetNativeTriggerServiceName):
        external_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetNativeTriggerResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        service_name=service_name,
        external_id=external_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    service_name: GetNativeTriggerServiceName,
    external_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[GetNativeTriggerResponse200]:
    """get native trigger

     Retrieves a native trigger by its external ID.
    Requires write access to the script or flow that the trigger is associated with.

    Args:
        workspace (str):
        service_name (GetNativeTriggerServiceName):
        external_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetNativeTriggerResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            service_name=service_name,
            external_id=external_id,
            client=client,
        )
    ).parsed
