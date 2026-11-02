from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.migrate_secrets_from_http_store_json_body import MigrateSecretsFromHttpStoreJsonBody
from ...models.migrate_secrets_from_http_store_response_200 import MigrateSecretsFromHttpStoreResponse200
from ...types import Response


def _get_kwargs(
    *,
    json_body: MigrateSecretsFromHttpStoreJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/settings/migrate_secrets_from_http_store",
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[MigrateSecretsFromHttpStoreResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = MigrateSecretsFromHttpStoreResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[MigrateSecretsFromHttpStoreResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: MigrateSecretsFromHttpStoreJsonBody,
) -> Response[MigrateSecretsFromHttpStoreResponse200]:
    """copy the values of HTTP secret store references into the database

    Args:
        json_body (MigrateSecretsFromHttpStoreJsonBody): Read-only secret backend for any secret
            store with an HTTP API. A secret variable saved with an empty value references the store
            key derived from its workspace and path.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MigrateSecretsFromHttpStoreResponse200]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: MigrateSecretsFromHttpStoreJsonBody,
) -> Optional[MigrateSecretsFromHttpStoreResponse200]:
    """copy the values of HTTP secret store references into the database

    Args:
        json_body (MigrateSecretsFromHttpStoreJsonBody): Read-only secret backend for any secret
            store with an HTTP API. A secret variable saved with an empty value references the store
            key derived from its workspace and path.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MigrateSecretsFromHttpStoreResponse200
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: MigrateSecretsFromHttpStoreJsonBody,
) -> Response[MigrateSecretsFromHttpStoreResponse200]:
    """copy the values of HTTP secret store references into the database

    Args:
        json_body (MigrateSecretsFromHttpStoreJsonBody): Read-only secret backend for any secret
            store with an HTTP API. A secret variable saved with an empty value references the store
            key derived from its workspace and path.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MigrateSecretsFromHttpStoreResponse200]
    """

    kwargs = _get_kwargs(
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: MigrateSecretsFromHttpStoreJsonBody,
) -> Optional[MigrateSecretsFromHttpStoreResponse200]:
    """copy the values of HTTP secret store references into the database

    Args:
        json_body (MigrateSecretsFromHttpStoreJsonBody): Read-only secret backend for any secret
            store with an HTTP API. A secret variable saved with an empty value references the store
            key derived from its workspace and path.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MigrateSecretsFromHttpStoreResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
