from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_ai_usage_group_by import ListAiUsageGroupBy
from ...models.list_ai_usage_response_200 import ListAiUsageResponse200
from ...models.list_ai_usage_scope import ListAiUsageScope
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    days: Union[Unset, None, int] = UNSET,
    group_by: Union[Unset, None, ListAiUsageGroupBy] = UNSET,
    scope: Union[Unset, None, ListAiUsageScope] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["days"] = days

    json_group_by: Union[Unset, None, str] = UNSET
    if not isinstance(group_by, Unset):
        json_group_by = group_by.value if group_by else None

    params["group_by"] = json_group_by

    json_scope: Union[Unset, None, str] = UNSET
    if not isinstance(scope, Unset):
        json_scope = scope.value if scope else None

    params["scope"] = json_scope

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/ai/usage".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListAiUsageResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListAiUsageResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListAiUsageResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    days: Union[Unset, None, int] = UNSET,
    group_by: Union[Unset, None, ListAiUsageGroupBy] = UNSET,
    scope: Union[Unset, None, ListAiUsageScope] = UNSET,
) -> Response[ListAiUsageResponse200]:
    """list aggregated AI token usage

    Args:
        workspace (str):
        days (Union[Unset, None, int]):
        group_by (Union[Unset, None, ListAiUsageGroupBy]):
        scope (Union[Unset, None, ListAiUsageScope]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListAiUsageResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        days=days,
        group_by=group_by,
        scope=scope,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    days: Union[Unset, None, int] = UNSET,
    group_by: Union[Unset, None, ListAiUsageGroupBy] = UNSET,
    scope: Union[Unset, None, ListAiUsageScope] = UNSET,
) -> Optional[ListAiUsageResponse200]:
    """list aggregated AI token usage

    Args:
        workspace (str):
        days (Union[Unset, None, int]):
        group_by (Union[Unset, None, ListAiUsageGroupBy]):
        scope (Union[Unset, None, ListAiUsageScope]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListAiUsageResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        days=days,
        group_by=group_by,
        scope=scope,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    days: Union[Unset, None, int] = UNSET,
    group_by: Union[Unset, None, ListAiUsageGroupBy] = UNSET,
    scope: Union[Unset, None, ListAiUsageScope] = UNSET,
) -> Response[ListAiUsageResponse200]:
    """list aggregated AI token usage

    Args:
        workspace (str):
        days (Union[Unset, None, int]):
        group_by (Union[Unset, None, ListAiUsageGroupBy]):
        scope (Union[Unset, None, ListAiUsageScope]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListAiUsageResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        days=days,
        group_by=group_by,
        scope=scope,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    days: Union[Unset, None, int] = UNSET,
    group_by: Union[Unset, None, ListAiUsageGroupBy] = UNSET,
    scope: Union[Unset, None, ListAiUsageScope] = UNSET,
) -> Optional[ListAiUsageResponse200]:
    """list aggregated AI token usage

    Args:
        workspace (str):
        days (Union[Unset, None, int]):
        group_by (Union[Unset, None, ListAiUsageGroupBy]):
        scope (Union[Unset, None, ListAiUsageScope]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListAiUsageResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            days=days,
            group_by=group_by,
            scope=scope,
        )
    ).parsed
