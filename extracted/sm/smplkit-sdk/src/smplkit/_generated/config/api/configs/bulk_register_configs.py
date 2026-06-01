from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.config_bulk_request import ConfigBulkRequest
from ...models.config_bulk_response import ConfigBulkResponse


def _get_kwargs(
    *,
    body: ConfigBulkRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/configs/bulk",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/vnd.api+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ConfigBulkResponse | None:
    if response.status_code == 200:
        response_200 = ConfigBulkResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ConfigBulkResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ConfigBulkRequest,
) -> Response[ConfigBulkResponse]:
    """Bulk Register Configs

     Register configs declared by an SDK.

    For each item in the batch:
    - If no config with that key exists, create one with ``managed=false``
      (auto-discovered) using the declared items, parent, name, and
      description.
    - If a config with that key already exists, leave the config row
      untouched (per ADR-024 §2.9).
    - Either way, upsert a ``config_source`` row for ``(config, service,
      environment)`` and refresh its ``last_seen`` timestamp.

    Per ADR-022 §2.11 rule 2 this endpoint never enforces
    ``config.managed_configurations`` — discovered configs do not consume
    a managed slot.

    Args:
        body (ConfigBulkRequest): Inputs to the bulk-register-configs action. Example: {'configs':
            [{'environment': 'production', 'id': 'billing', 'items': {'plan.max_seats':
            {'description': 'Maximum seats per organization.', 'type': 'NUMBER', 'value': 5}},
            'parent': 'common', 'service': 'billing-service'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConfigBulkResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: ConfigBulkRequest,
) -> ConfigBulkResponse | None:
    """Bulk Register Configs

     Register configs declared by an SDK.

    For each item in the batch:
    - If no config with that key exists, create one with ``managed=false``
      (auto-discovered) using the declared items, parent, name, and
      description.
    - If a config with that key already exists, leave the config row
      untouched (per ADR-024 §2.9).
    - Either way, upsert a ``config_source`` row for ``(config, service,
      environment)`` and refresh its ``last_seen`` timestamp.

    Per ADR-022 §2.11 rule 2 this endpoint never enforces
    ``config.managed_configurations`` — discovered configs do not consume
    a managed slot.

    Args:
        body (ConfigBulkRequest): Inputs to the bulk-register-configs action. Example: {'configs':
            [{'environment': 'production', 'id': 'billing', 'items': {'plan.max_seats':
            {'description': 'Maximum seats per organization.', 'type': 'NUMBER', 'value': 5}},
            'parent': 'common', 'service': 'billing-service'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConfigBulkResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ConfigBulkRequest,
) -> Response[ConfigBulkResponse]:
    """Bulk Register Configs

     Register configs declared by an SDK.

    For each item in the batch:
    - If no config with that key exists, create one with ``managed=false``
      (auto-discovered) using the declared items, parent, name, and
      description.
    - If a config with that key already exists, leave the config row
      untouched (per ADR-024 §2.9).
    - Either way, upsert a ``config_source`` row for ``(config, service,
      environment)`` and refresh its ``last_seen`` timestamp.

    Per ADR-022 §2.11 rule 2 this endpoint never enforces
    ``config.managed_configurations`` — discovered configs do not consume
    a managed slot.

    Args:
        body (ConfigBulkRequest): Inputs to the bulk-register-configs action. Example: {'configs':
            [{'environment': 'production', 'id': 'billing', 'items': {'plan.max_seats':
            {'description': 'Maximum seats per organization.', 'type': 'NUMBER', 'value': 5}},
            'parent': 'common', 'service': 'billing-service'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConfigBulkResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ConfigBulkRequest,
) -> ConfigBulkResponse | None:
    """Bulk Register Configs

     Register configs declared by an SDK.

    For each item in the batch:
    - If no config with that key exists, create one with ``managed=false``
      (auto-discovered) using the declared items, parent, name, and
      description.
    - If a config with that key already exists, leave the config row
      untouched (per ADR-024 §2.9).
    - Either way, upsert a ``config_source`` row for ``(config, service,
      environment)`` and refresh its ``last_seen`` timestamp.

    Per ADR-022 §2.11 rule 2 this endpoint never enforces
    ``config.managed_configurations`` — discovered configs do not consume
    a managed slot.

    Args:
        body (ConfigBulkRequest): Inputs to the bulk-register-configs action. Example: {'configs':
            [{'environment': 'production', 'id': 'billing', 'items': {'plan.max_seats':
            {'description': 'Maximum seats per organization.', 'type': 'NUMBER', 'value': 5}},
            'parent': 'common', 'service': 'billing-service'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConfigBulkResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
