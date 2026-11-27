"""HTTP and MCP clients routed through the Connectors Gateway.

Both come from the mistralai SDK's ``beta.connectors`` helpers, which send gateway requests
through the HTTP client configured on the ``Mistral`` instance. The instance is the connector
activity client, so requests carry the workflow identity selected by ``run_as``.
"""

from __future__ import annotations

import importlib
import inspect
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from functools import cache
from importlib.metadata import version
from typing import Any

import httpx
from mcp import ClientSession

from mistralai.client import Mistral
from mistralai.workflows.exceptions import WorkflowError

from .activities import _build_connector_client
from .run_as import RunAs


@cache
def sdk_supports_gateway_clients() -> bool:
    """Whether the installed mistralai sends gateway requests through the SDK's configured client.

    Earlier helpers build their own client and authenticate with the SDK API key, which the
    connector activity client leaves unset, so their requests would carry no workflow identity.
    """
    try:
        sdk_gateway = importlib.import_module("mistralai.extra.connectors_gateway")
    except ImportError:
        return False
    return "sdk_client" in inspect.signature(sdk_gateway.http_client).parameters


@asynccontextmanager
async def _connector_sdk(run_as: RunAs) -> AsyncIterator[Mistral]:
    if not sdk_supports_gateway_clients():
        raise WorkflowError(
            "ConnectorClient.mcp_client() and http_client() need a mistralai release whose "
            "connectors gateway helpers send through the SDK's configured client "
            f"(installed: {version('mistralai')}). Upgrade mistralai, or use call_tool().",
            non_retryable=True,
        )
    sdk = _build_connector_client(run_as)
    try:
        yield sdk
    finally:
        # The SDK leaves supplied clients to their owner, and the gateway helpers only borrow them.
        if sdk.sdk_configuration.async_client is not None:
            await sdk.sdk_configuration.async_client.aclose()
        if sdk.sdk_configuration.client is not None:
            sdk.sdk_configuration.client.close()


def _gateway_helpers(sdk: Mistral) -> Any:
    # Untyped: the plugin type-checks against mistralai 2.x, which has no gateway helpers.
    return sdk.beta.connectors


@asynccontextmanager
async def open_gateway_http_client(
    connector_id_or_name: str, *, credentials_name: str | None, run_as: RunAs
) -> AsyncIterator[httpx.AsyncClient]:
    async with _connector_sdk(run_as) as sdk:
        async with _gateway_helpers(sdk).http_client(
            connector_id_or_name=connector_id_or_name,
            credentials_name=credentials_name,
        ) as http_client:
            yield http_client


@asynccontextmanager
async def open_gateway_mcp_session(
    connector_id_or_name: str, *, credentials_name: str | None, run_as: RunAs
) -> AsyncIterator[ClientSession]:
    async with _connector_sdk(run_as) as sdk:
        async with _gateway_helpers(sdk).mcp_client(
            connector_id_or_name=connector_id_or_name,
            credentials_name=credentials_name,
        ) as mcp_session:
            yield mcp_session
