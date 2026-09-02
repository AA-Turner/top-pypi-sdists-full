import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_asset_partitions_in_range_response_200 import ListAssetPartitionsInRangeResponse200
from ...types import UNSET, Response


def _get_kwargs(
    workspace: str,
    *,
    path: str,
    from_: datetime.date,
    to: datetime.date,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["path"] = path

    json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to = to.isoformat()
    params["to"] = json_to

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/assets/partitions_in_range".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListAssetPartitionsInRangeResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListAssetPartitionsInRangeResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListAssetPartitionsInRangeResponse200]:
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
    path: str,
    from_: datetime.date,
    to: datetime.date,
) -> Response[ListAssetPartitionsInRangeResponse200]:
    """List expected partitions of a ducklake asset in a date range with their materialization status
    (enterprise)

    Args:
        workspace (str):
        path (str):
        from_ (datetime.date):
        to (datetime.date):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListAssetPartitionsInRangeResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        from_=from_,
        to=to,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    path: str,
    from_: datetime.date,
    to: datetime.date,
) -> Optional[ListAssetPartitionsInRangeResponse200]:
    """List expected partitions of a ducklake asset in a date range with their materialization status
    (enterprise)

    Args:
        workspace (str):
        path (str):
        from_ (datetime.date):
        to (datetime.date):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListAssetPartitionsInRangeResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        path=path,
        from_=from_,
        to=to,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    path: str,
    from_: datetime.date,
    to: datetime.date,
) -> Response[ListAssetPartitionsInRangeResponse200]:
    """List expected partitions of a ducklake asset in a date range with their materialization status
    (enterprise)

    Args:
        workspace (str):
        path (str):
        from_ (datetime.date):
        to (datetime.date):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListAssetPartitionsInRangeResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        from_=from_,
        to=to,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    path: str,
    from_: datetime.date,
    to: datetime.date,
) -> Optional[ListAssetPartitionsInRangeResponse200]:
    """List expected partitions of a ducklake asset in a date range with their materialization status
    (enterprise)

    Args:
        workspace (str):
        path (str):
        from_ (datetime.date):
        to (datetime.date):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListAssetPartitionsInRangeResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            path=path,
            from_=from_,
            to=to,
        )
    ).parsed
