from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.exists_workers_with_tags_response_200 import ExistsWorkersWithTagsResponse200
from ...types import UNSET, Response


def _get_kwargs(
    *,
    tags: str,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["tags"] = tags

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/workers/exists_workers_with_tags",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ExistsWorkersWithTagsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ExistsWorkersWithTagsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ExistsWorkersWithTagsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    tags: str,
) -> Response[ExistsWorkersWithTagsResponse200]:
    """exists workers with tags

    Args:
        tags (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExistsWorkersWithTagsResponse200]
    """

    kwargs = _get_kwargs(
        tags=tags,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    tags: str,
) -> Optional[ExistsWorkersWithTagsResponse200]:
    """exists workers with tags

    Args:
        tags (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExistsWorkersWithTagsResponse200
    """

    return sync_detailed(
        client=client,
        tags=tags,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    tags: str,
) -> Response[ExistsWorkersWithTagsResponse200]:
    """exists workers with tags

    Args:
        tags (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExistsWorkersWithTagsResponse200]
    """

    kwargs = _get_kwargs(
        tags=tags,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    tags: str,
) -> Optional[ExistsWorkersWithTagsResponse200]:
    """exists workers with tags

    Args:
        tags (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExistsWorkersWithTagsResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            tags=tags,
        )
    ).parsed
