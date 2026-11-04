"""Get Exit Upstream"""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing import Any

import httpx

from plato.chronos.errors import raise_for_status
from plato.chronos.models import LoginVaultExitUpstream


def _build_request_args(
    name: str,
    login_key: str | None = None,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> dict[str, Any]:
    """Build request arguments."""
    url = f"/api/login-vault/exits/{name}/upstream"

    params: dict[str, Any] = {}
    if login_key is not None:
        params["login_key"] = login_key

    headers: dict[str, str] = {}
    if x_chronos_session_id is not None:
        headers["X-Chronos-Session-Id"] = x_chronos_session_id
    if x_api_key is not None:
        headers["X-API-Key"] = x_api_key

    return {
        "method": "GET",
        "url": url,
        "params": params,
        "headers": headers,
    }


def sync(
    client: httpx.Client,
    name: str,
    login_key: str | None = None,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultExitUpstream:
    """The exit's upstream URL, credentials included, built from the provider item by the worlds' own rule (what a VM's proxy takes). 409 when the exit is banned for `login_key` (a ban for every app also refuses a call without one); the ban is read fresh every call. 404 for a name that is no exit; 502 when the provider item lacks a field the URL needs. Every vault-org key."""

    request_args = _build_request_args(
        name=name,
        login_key=login_key,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = client.request(**request_args)
    raise_for_status(response)
    return LoginVaultExitUpstream.model_validate(response.json())


async def asyncio(
    client: httpx.AsyncClient,
    name: str,
    login_key: str | None = None,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> LoginVaultExitUpstream:
    """The exit's upstream URL, credentials included, built from the provider item by the worlds' own rule (what a VM's proxy takes). 409 when the exit is banned for `login_key` (a ban for every app also refuses a call without one); the ban is read fresh every call. 404 for a name that is no exit; 502 when the provider item lacks a field the URL needs. Every vault-org key."""

    request_args = _build_request_args(
        name=name,
        login_key=login_key,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    response = await client.request(**request_args)
    raise_for_status(response)
    return LoginVaultExitUpstream.model_validate(response.json())


def sync_stream(
    client: httpx.Client,
    name: str,
    login_key: str | None = None,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> Iterator[dict[str, Any]]:
    """Get Exit Upstream (streaming)"""
    import json

    request_args = _build_request_args(
        name=name,
        login_key=login_key,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    with client.stream(**request_args) as response:
        raise_for_status(response)
        for line in response.iter_lines():
            if line.strip():
                yield json.loads(line)


async def asyncio_stream(
    client: httpx.AsyncClient,
    name: str,
    login_key: str | None = None,
    x_chronos_session_id: str | None = None,
    x_api_key: str | None = None,
) -> AsyncIterator[dict[str, Any]]:
    """Get Exit Upstream (streaming)"""
    import json

    request_args = _build_request_args(
        name=name,
        login_key=login_key,
        x_chronos_session_id=x_chronos_session_id,
        x_api_key=x_api_key,
    )

    async with client.stream(**request_args) as response:
        raise_for_status(response)
        async for line in response.aiter_lines():
            if line.strip():
                yield json.loads(line)
