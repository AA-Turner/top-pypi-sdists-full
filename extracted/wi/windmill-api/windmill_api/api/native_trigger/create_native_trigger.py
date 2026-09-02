from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_native_trigger_json_body import CreateNativeTriggerJsonBody
from ...models.create_native_trigger_response_201 import CreateNativeTriggerResponse201
from ...models.create_native_trigger_service_name import CreateNativeTriggerServiceName
from ...types import Response


def _get_kwargs(
    workspace: str,
    service_name: CreateNativeTriggerServiceName,
    *,
    json_body: CreateNativeTriggerJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/native_triggers/{service_name}/create".format(
            workspace=workspace,
            service_name=service_name,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[CreateNativeTriggerResponse201]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = CreateNativeTriggerResponse201.from_dict(response.json())

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CreateNativeTriggerResponse201]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    service_name: CreateNativeTriggerServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CreateNativeTriggerJsonBody,
) -> Response[CreateNativeTriggerResponse201]:
    """create native trigger

     Creates a new native trigger for the specified service.
    Requires write access to the script or flow that the trigger will be associated with.

    Args:
        workspace (str):
        service_name (CreateNativeTriggerServiceName):
        json_body (CreateNativeTriggerJsonBody): Data for creating or updating a native trigger

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateNativeTriggerResponse201]
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
    service_name: CreateNativeTriggerServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CreateNativeTriggerJsonBody,
) -> Optional[CreateNativeTriggerResponse201]:
    """create native trigger

     Creates a new native trigger for the specified service.
    Requires write access to the script or flow that the trigger will be associated with.

    Args:
        workspace (str):
        service_name (CreateNativeTriggerServiceName):
        json_body (CreateNativeTriggerJsonBody): Data for creating or updating a native trigger

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateNativeTriggerResponse201
    """

    return sync_detailed(
        workspace=workspace,
        service_name=service_name,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    service_name: CreateNativeTriggerServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CreateNativeTriggerJsonBody,
) -> Response[CreateNativeTriggerResponse201]:
    """create native trigger

     Creates a new native trigger for the specified service.
    Requires write access to the script or flow that the trigger will be associated with.

    Args:
        workspace (str):
        service_name (CreateNativeTriggerServiceName):
        json_body (CreateNativeTriggerJsonBody): Data for creating or updating a native trigger

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateNativeTriggerResponse201]
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
    service_name: CreateNativeTriggerServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CreateNativeTriggerJsonBody,
) -> Optional[CreateNativeTriggerResponse201]:
    """create native trigger

     Creates a new native trigger for the specified service.
    Requires write access to the script or flow that the trigger will be associated with.

    Args:
        workspace (str):
        service_name (CreateNativeTriggerServiceName):
        json_body (CreateNativeTriggerJsonBody): Data for creating or updating a native trigger

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateNativeTriggerResponse201
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            service_name=service_name,
            client=client,
            json_body=json_body,
        )
    ).parsed
