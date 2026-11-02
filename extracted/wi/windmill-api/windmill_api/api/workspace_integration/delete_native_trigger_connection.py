from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_native_trigger_connection_service_name import DeleteNativeTriggerConnectionServiceName
from ...types import UNSET, Response


def _get_kwargs(
    workspace: str,
    service_name: DeleteNativeTriggerConnectionServiceName,
    *,
    path: str,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["path"] = path

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "delete",
        "url": "/w/{workspace}/native_triggers/integrations/{service_name}/connections/delete".format(
            workspace=workspace,
            service_name=service_name,
        ),
        "params": params,
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
    service_name: DeleteNativeTriggerConnectionServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
    path: str,
) -> Response[str]:
    """disconnect a native trigger connection and delete the triggers using it

    Args:
        workspace (str):
        service_name (DeleteNativeTriggerConnectionServiceName):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        service_name=service_name,
        path=path,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    service_name: DeleteNativeTriggerConnectionServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
    path: str,
) -> Optional[str]:
    """disconnect a native trigger connection and delete the triggers using it

    Args:
        workspace (str):
        service_name (DeleteNativeTriggerConnectionServiceName):
        path (str):

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
        path=path,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    service_name: DeleteNativeTriggerConnectionServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
    path: str,
) -> Response[str]:
    """disconnect a native trigger connection and delete the triggers using it

    Args:
        workspace (str):
        service_name (DeleteNativeTriggerConnectionServiceName):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        service_name=service_name,
        path=path,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    service_name: DeleteNativeTriggerConnectionServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
    path: str,
) -> Optional[str]:
    """disconnect a native trigger connection and delete the triggers using it

    Args:
        workspace (str):
        service_name (DeleteNativeTriggerConnectionServiceName):
        path (str):

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
            path=path,
        )
    ).parsed
