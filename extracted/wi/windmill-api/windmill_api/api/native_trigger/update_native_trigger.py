from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_native_trigger_json_body import UpdateNativeTriggerJsonBody
from ...models.update_native_trigger_service_name import UpdateNativeTriggerServiceName
from ...types import Response


def _get_kwargs(
    workspace: str,
    service_name: UpdateNativeTriggerServiceName,
    external_id: str,
    *,
    json_body: UpdateNativeTriggerJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/native_triggers/{service_name}/update/{external_id}".format(
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
    service_name: UpdateNativeTriggerServiceName,
    external_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateNativeTriggerJsonBody,
) -> Response[Any]:
    """update native trigger

     Updates an existing native trigger.
    Requires write access to the script or flow that the trigger is associated with.

    Args:
        workspace (str):
        service_name (UpdateNativeTriggerServiceName):
        external_id (str):
        json_body (UpdateNativeTriggerJsonBody): Data for creating or updating a native trigger

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
    service_name: UpdateNativeTriggerServiceName,
    external_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateNativeTriggerJsonBody,
) -> Response[Any]:
    """update native trigger

     Updates an existing native trigger.
    Requires write access to the script or flow that the trigger is associated with.

    Args:
        workspace (str):
        service_name (UpdateNativeTriggerServiceName):
        external_id (str):
        json_body (UpdateNativeTriggerJsonBody): Data for creating or updating a native trigger

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
