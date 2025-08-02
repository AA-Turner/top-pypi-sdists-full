from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_concurrency_group_response_200 import DeleteConcurrencyGroupResponse200
from ...types import Response


def _get_kwargs(
    concurrency_id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "delete",
        "url": "/concurrency_groups/prune/{concurrency_id}".format(
            concurrency_id=concurrency_id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[DeleteConcurrencyGroupResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DeleteConcurrencyGroupResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[DeleteConcurrencyGroupResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    concurrency_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[DeleteConcurrencyGroupResponse200]:
    """Delete concurrency group

    Args:
        concurrency_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteConcurrencyGroupResponse200]
    """

    kwargs = _get_kwargs(
        concurrency_id=concurrency_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    concurrency_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[DeleteConcurrencyGroupResponse200]:
    """Delete concurrency group

    Args:
        concurrency_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteConcurrencyGroupResponse200
    """

    return sync_detailed(
        concurrency_id=concurrency_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    concurrency_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[DeleteConcurrencyGroupResponse200]:
    """Delete concurrency group

    Args:
        concurrency_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteConcurrencyGroupResponse200]
    """

    kwargs = _get_kwargs(
        concurrency_id=concurrency_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    concurrency_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[DeleteConcurrencyGroupResponse200]:
    """Delete concurrency group

    Args:
        concurrency_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteConcurrencyGroupResponse200
    """

    return (
        await asyncio_detailed(
            concurrency_id=concurrency_id,
            client=client,
        )
    ).parsed
