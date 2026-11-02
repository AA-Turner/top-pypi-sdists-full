from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.s3_proxy_bucket_response_200 import S3ProxyBucketResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    storage: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["storage"] = storage

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/w/{workspace}/job_helpers/v2/s3_proxy_bucket".format(
            workspace=workspace,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[S3ProxyBucketResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = S3ProxyBucketResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[S3ProxyBucketResponse200]:
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
    storage: Union[Unset, None, str] = UNSET,
) -> Response[S3ProxyBucketResponse200]:
    """Returns the bucket S3 clients name to reach a workspace storage through the S3 proxy, or null when
    that storage is not S3

    Args:
        workspace (str):
        storage (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[S3ProxyBucketResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        storage=storage,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    storage: Union[Unset, None, str] = UNSET,
) -> Optional[S3ProxyBucketResponse200]:
    """Returns the bucket S3 clients name to reach a workspace storage through the S3 proxy, or null when
    that storage is not S3

    Args:
        workspace (str):
        storage (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        S3ProxyBucketResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        storage=storage,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    storage: Union[Unset, None, str] = UNSET,
) -> Response[S3ProxyBucketResponse200]:
    """Returns the bucket S3 clients name to reach a workspace storage through the S3 proxy, or null when
    that storage is not S3

    Args:
        workspace (str):
        storage (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[S3ProxyBucketResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        storage=storage,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    storage: Union[Unset, None, str] = UNSET,
) -> Optional[S3ProxyBucketResponse200]:
    """Returns the bucket S3 clients name to reach a workspace storage through the S3 proxy, or null when
    that storage is not S3

    Args:
        workspace (str):
        storage (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        S3ProxyBucketResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            storage=storage,
        )
    ).parsed
