from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_concurrency_key_status_response_200 import GetConcurrencyKeyStatusResponse200
from ...types import Response


def _get_kwargs(
    id: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/concurrency_groups/{id}/key_status".format(
            id=id,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Optional[GetConcurrencyKeyStatusResponse200]]:
    if response.status_code == HTTPStatus.OK:
        _response_200 = response.json()
        response_200: Optional[GetConcurrencyKeyStatusResponse200]
        if _response_200 is None:
            response_200 = None
        else:
            response_200 = GetConcurrencyKeyStatusResponse200.from_dict(_response_200)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Optional[GetConcurrencyKeyStatusResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Optional[GetConcurrencyKeyStatusResponse200]]:
    """Get a job's concurrency key and whether its limit held it back

     Requires read access to the job, the same as reading the run itself. Returns null when the job has
    no concurrency key.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Optional[GetConcurrencyKeyStatusResponse200]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Optional[GetConcurrencyKeyStatusResponse200]]:
    """Get a job's concurrency key and whether its limit held it back

     Requires read access to the job, the same as reading the run itself. Returns null when the job has
    no concurrency key.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Optional[GetConcurrencyKeyStatusResponse200]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Optional[GetConcurrencyKeyStatusResponse200]]:
    """Get a job's concurrency key and whether its limit held it back

     Requires read access to the job, the same as reading the run itself. Returns null when the job has
    no concurrency key.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Optional[GetConcurrencyKeyStatusResponse200]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Optional[GetConcurrencyKeyStatusResponse200]]:
    """Get a job's concurrency key and whether its limit held it back

     Requires read access to the job, the same as reading the run itself. Returns null when the job has
    no concurrency key.

    Args:
        id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Optional[GetConcurrencyKeyStatusResponse200]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
