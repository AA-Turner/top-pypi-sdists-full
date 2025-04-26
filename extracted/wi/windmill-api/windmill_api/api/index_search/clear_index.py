from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.clear_index_idx_name import ClearIndexIdxName
from ...types import Response


def _get_kwargs(
    idx_name: ClearIndexIdxName,
) -> Dict[str, Any]:
    pass

    return {
        "method": "delete",
        "url": "/srch/index/delete/{idx_name}".format(
            idx_name=idx_name,
        ),
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
    idx_name: ClearIndexIdxName,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Any]:
    """Restart container and delete the index to recreate it.

    Args:
        idx_name (ClearIndexIdxName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        idx_name=idx_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    idx_name: ClearIndexIdxName,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Any]:
    """Restart container and delete the index to recreate it.

    Args:
        idx_name (ClearIndexIdxName):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        idx_name=idx_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
