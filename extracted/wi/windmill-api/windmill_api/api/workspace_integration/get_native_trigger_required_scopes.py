from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_native_trigger_required_scopes_service_name import GetNativeTriggerRequiredScopesServiceName
from ...types import Response


def _get_kwargs(
    workspace: str,
    service_name: GetNativeTriggerRequiredScopesServiceName,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/native_triggers/integrations/{service_name}/required_scopes".format(
            workspace=workspace,
            service_name=service_name,
        ),
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[List[str]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(List[str], response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[List[str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    service_name: GetNativeTriggerRequiredScopesServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[List[str]]:
    """list the scopes the service's triggers need

    Args:
        workspace (str):
        service_name (GetNativeTriggerRequiredScopesServiceName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[str]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        service_name=service_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    service_name: GetNativeTriggerRequiredScopesServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[List[str]]:
    """list the scopes the service's triggers need

    Args:
        workspace (str):
        service_name (GetNativeTriggerRequiredScopesServiceName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List[str]
    """

    return sync_detailed(
        workspace=workspace,
        service_name=service_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    service_name: GetNativeTriggerRequiredScopesServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[List[str]]:
    """list the scopes the service's triggers need

    Args:
        workspace (str):
        service_name (GetNativeTriggerRequiredScopesServiceName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[str]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        service_name=service_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    service_name: GetNativeTriggerRequiredScopesServiceName,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[List[str]]:
    """list the scopes the service's triggers need

    Args:
        workspace (str):
        service_name (GetNativeTriggerRequiredScopesServiceName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List[str]
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            service_name=service_name,
            client=client,
        )
    ).parsed
