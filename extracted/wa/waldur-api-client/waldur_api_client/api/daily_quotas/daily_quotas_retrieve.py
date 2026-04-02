import datetime
from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.daily_quotas_retrieve_response_200 import DailyQuotasRetrieveResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    end: Union[Unset, datetime.date] = UNSET,
    quota_names: Union[Unset, list[str]] = UNSET,
    scope: Union[Unset, UUID] = UNSET,
    start: Union[Unset, datetime.date] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_end: Union[Unset, str] = UNSET
    if not isinstance(end, Unset):
        json_end = end.isoformat()
    params["end"] = json_end

    json_quota_names: Union[Unset, list[str]] = UNSET
    if not isinstance(quota_names, Unset):
        json_quota_names = quota_names

    params["quota_names"] = json_quota_names

    json_scope: Union[Unset, str] = UNSET
    if not isinstance(scope, Unset):
        json_scope = str(scope)
    params["scope"] = json_scope

    json_start: Union[Unset, str] = UNSET
    if not isinstance(start, Unset):
        json_start = start.isoformat()
    params["start"] = json_start

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/daily-quotas/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> DailyQuotasRetrieveResponse200:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = DailyQuotasRetrieveResponse200.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[DailyQuotasRetrieveResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    end: Union[Unset, datetime.date] = UNSET,
    quota_names: Union[Unset, list[str]] = UNSET,
    scope: Union[Unset, UUID] = UNSET,
    start: Union[Unset, datetime.date] = UNSET,
) -> Response[DailyQuotasRetrieveResponse200]:
    """
    Args:
        end (Union[Unset, datetime.date]):
        quota_names (Union[Unset, list[str]]):
        scope (Union[Unset, UUID]):
        start (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DailyQuotasRetrieveResponse200]
    """

    kwargs = _get_kwargs(
        end=end,
        quota_names=quota_names,
        scope=scope,
        start=start,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    end: Union[Unset, datetime.date] = UNSET,
    quota_names: Union[Unset, list[str]] = UNSET,
    scope: Union[Unset, UUID] = UNSET,
    start: Union[Unset, datetime.date] = UNSET,
) -> DailyQuotasRetrieveResponse200:
    """
    Args:
        end (Union[Unset, datetime.date]):
        quota_names (Union[Unset, list[str]]):
        scope (Union[Unset, UUID]):
        start (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DailyQuotasRetrieveResponse200
    """

    return sync_detailed(
        client=client,
        end=end,
        quota_names=quota_names,
        scope=scope,
        start=start,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    end: Union[Unset, datetime.date] = UNSET,
    quota_names: Union[Unset, list[str]] = UNSET,
    scope: Union[Unset, UUID] = UNSET,
    start: Union[Unset, datetime.date] = UNSET,
) -> Response[DailyQuotasRetrieveResponse200]:
    """
    Args:
        end (Union[Unset, datetime.date]):
        quota_names (Union[Unset, list[str]]):
        scope (Union[Unset, UUID]):
        start (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DailyQuotasRetrieveResponse200]
    """

    kwargs = _get_kwargs(
        end=end,
        quota_names=quota_names,
        scope=scope,
        start=start,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    end: Union[Unset, datetime.date] = UNSET,
    quota_names: Union[Unset, list[str]] = UNSET,
    scope: Union[Unset, UUID] = UNSET,
    start: Union[Unset, datetime.date] = UNSET,
) -> DailyQuotasRetrieveResponse200:
    """
    Args:
        end (Union[Unset, datetime.date]):
        quota_names (Union[Unset, list[str]]):
        scope (Union[Unset, UUID]):
        start (Union[Unset, datetime.date]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DailyQuotasRetrieveResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            end=end,
            quota_names=quota_names,
            scope=scope,
            start=start,
        )
    ).parsed
