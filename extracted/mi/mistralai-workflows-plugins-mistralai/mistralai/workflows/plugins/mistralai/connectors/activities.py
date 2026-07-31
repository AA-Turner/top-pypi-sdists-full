"""Activities for connector operations using the Mistral SDK.

These activities are scheduled by the ``ConnectorAuthInterceptor`` (for auth
preflight) and by ``ToolCallClient`` (for tool calls).  They run outside the
Temporal workflow sandbox as regular activity tasks.
"""

from __future__ import annotations

import asyncio
import datetime
import time
from typing import Any

import structlog
import temporalio.activity

from mistralai.client import Mistral
from mistralai.client.models import CredentialsResponse, PublicAuthenticationMethod
from mistralai.workflows.client import get_mistral_client
from mistralai.workflows.core.activity import activity
from mistralai.workflows.plugins.mistralai.connectors.exceptions import ConnectorToolCallError
from mistralai.workflows.plugins.mistralai.connectors.mcp_apps import (
    complete_mcp_app_call_events,
    fail_mcp_app_call_events,
    start_mcp_app_call_events,
)
from mistralai.workflows.plugins.mistralai.connectors.models import (
    ResolvedConnector,
)
from mistralai.workflows.plugins.mistralai.connectors.run_as import ConnectorRunAs, use_executor_credentials_for

logger = structlog.get_logger(__name__)


def _build_connector_client(run_as: ConnectorRunAs = ConnectorRunAs.AUTO) -> Mistral:
    return get_mistral_client(use_executor_credentials=use_executor_credentials_for(run_as))


@activity(
    name="__internal__connector_resolve",
    start_to_close_timeout=datetime.timedelta(seconds=30),
    _allow_reserved_name=True,
)
async def connector_resolve(
    connector_id_or_name: str,
    run_as: ConnectorRunAs = ConnectorRunAs.AUTO,
) -> ResolvedConnector:
    """Resolve a connector by name or ID via the Mistral SDK."""
    client = _build_connector_client(run_as)
    conn = await client.beta.connectors.get_async(
        connector_id_or_name=connector_id_or_name,
    )

    logger.info(
        "Resolved connector",
        connector_id=conn.id,
        connector_name=conn.name,
    )

    return ResolvedConnector(
        id=conn.id,
        name=conn.name,
        description=conn.description,
    )


@activity(
    name="__internal__connector_get_auth_url",
    start_to_close_timeout=datetime.timedelta(seconds=30),
    _allow_reserved_name=True,
)
async def connector_get_auth_url(
    connector_id_or_name: str, credentials_name: str | None = None, run_as: ConnectorRunAs = ConnectorRunAs.AUTO
) -> str:
    """Get the OAuth authorization URL for a connector."""
    client = _build_connector_client(run_as)
    result = await client.beta.connectors.get_auth_url_async(
        connector_id_or_name=connector_id_or_name, credentials_name=credentials_name
    )

    logger.info(
        "Got connector auth URL",
        connector_id_or_name=connector_id_or_name,
    )

    return str(result.auth_url)


@activity(
    name="__internal__connector_tool_call",
    start_to_close_timeout=datetime.timedelta(seconds=120),
    _allow_reserved_name=True,
)
async def connector_tool_call(
    connector_id_or_name: str,
    tool_name: str,
    arguments: dict[str, Any] | None = None,
    credentials_name: str | None = None,
    mcp_ui_resource_uri: str | None = None,
    run_as: ConnectorRunAs = ConnectorRunAs.AUTO,
) -> Any:
    """Call a tool on a connector via the Mistral SDK."""
    client = _build_connector_client(run_as)

    logger.info(
        "Connector tool call",
        connector_id_or_name=connector_id_or_name,
        tool_name=tool_name,
        has_arguments=arguments is not None,
        credentials_name=credentials_name,
    )

    call_kwargs: dict[str, Any] = {
        "connector_id_or_name": connector_id_or_name,
        "tool_name": tool_name,
        "arguments": arguments,
    }
    if credentials_name is not None:
        call_kwargs["credentials_name"] = credentials_name

    mcp_app_events = start_mcp_app_call_events(
        uri=mcp_ui_resource_uri,
        connector_id=connector_id_or_name,
        tool_name=tool_name,
        arguments=arguments,
    )

    try:
        result = await client.beta.connectors.call_tool_async(**call_kwargs)
    except Exception as e:
        fail_mcp_app_call_events(mcp_app_events, message=str(e))
        raise

    metadata = result.metadata
    if metadata and metadata.mcp_meta and metadata.mcp_meta.is_error:
        logger.error(
            "Connector tool call returned MCP error",
            connector_id_or_name=connector_id_or_name,
            tool_name=tool_name,
            # We dump the whole response because the context of the error is in the 'content' field
            response=result.model_dump(),
        )
        fail_mcp_app_call_events(
            mcp_app_events,
            message=f"[{connector_id_or_name}] connector tool call failed",
        )
        raise ConnectorToolCallError(connector_id_or_name=connector_id_or_name, response=result)

    # Returned to the workflow with the legacy dump options to avoid changing the
    # shape consumed by existing (non-MCP) connector_tool_call callers.
    dumped = result.model_dump()

    complete_mcp_app_call_events(mcp_app_events, result)

    return dumped


@activity(
    name="__internal__connector_list_tools",
    start_to_close_timeout=datetime.timedelta(seconds=30),
    _allow_reserved_name=True,
)
async def connector_list_tools(
    connector_id_or_name: str,
    credentials_name: str | None = None,
    run_as: ConnectorRunAs = ConnectorRunAs.AUTO,
) -> bool:
    """Check if a connector's credentials are still valid by listing its tools.

    Returns ``True`` if the call succeeds, ``False`` if it fails (e.g. expired
    OAuth2 token requiring re-authorization).
    """
    client = _build_connector_client(run_as)
    try:
        await client.beta.connectors.list_tools_async(
            connector_id_or_name=connector_id_or_name, credentials_name=credentials_name
        )

        logger.info(
            "Connector list_tools succeeded",
            connector_id_or_name=connector_id_or_name,
            credentials_name=credentials_name,
        )
        return True
    except Exception:
        logger.warning(
            "Connector list_tools failed — credentials may need re-authorization",
            connector_id_or_name=connector_id_or_name,
            credentials_name=credentials_name,
        )
        return False


@activity(
    name="__internal__connector_get_auth_methods",
    start_to_close_timeout=datetime.timedelta(seconds=30),
    _allow_reserved_name=True,
)
async def connector_get_auth_methods(
    connector_id_or_name: str,
    run_as: ConnectorRunAs = ConnectorRunAs.AUTO,
) -> list[PublicAuthenticationMethod]:
    """Get the supported authentication methods for a connector.

    Returns a list of PublicAuthenticationMethod with ``method_type`` and
    optional ``headers``.
    """
    client = _build_connector_client(run_as)
    methods = await client.beta.connectors.get_authentication_methods_async(
        connector_id_or_name=connector_id_or_name,
    )
    logger.info(
        "Got connector auth methods",
        connector_id_or_name=connector_id_or_name,
        methods=[m.method_type for m in methods],
    )
    return methods


@activity(
    name="__internal__connector_list_user_credentials",
    start_to_close_timeout=datetime.timedelta(seconds=30),
    _allow_reserved_name=True,
)
async def connector_list_user_credentials(
    connector_id_or_name: str,
    run_as: ConnectorRunAs = ConnectorRunAs.AUTO,
) -> CredentialsResponse:
    """List the current user's credentials for a connector.

    Returns a CredentialsInfo with ``credentials`` (list of stored
    credentials) and ``connector_preset_credentials_for_auth`` (auth types
    the connector has preset/platform credentials for).
    """
    client = _build_connector_client(run_as)
    info = await client.beta.connectors.list_user_credentials_async(
        connector_id_or_name=connector_id_or_name,
    )
    logger.info(
        "Listed user credentials",
        connector_id_or_name=connector_id_or_name,
        credential_count=len(info.credentials),
        preset_auth_types=info.connector_preset_credentials_for_auth,
    )
    return info


_POLL_INTERVAL_SECONDS = 1.5
_POLL_TIMEOUT_SECONDS = 600


@activity(
    name="__internal__connector_wait_for_credentials",
    start_to_close_timeout=datetime.timedelta(seconds=_POLL_TIMEOUT_SECONDS + 60),
    heartbeat_timeout=datetime.timedelta(seconds=30),
    _allow_reserved_name=True,
)
async def connector_wait_for_credentials(
    connector_id: str, credentials_name: str | None = None, run_as: ConnectorRunAs = ConnectorRunAs.AUTO
) -> bool:
    """Poll the credentials API until *usable* user credentials appear.

    Runs as a single long-lived activity with heartbeats.  Returns ``True``
    when credentials are detected and verified via ``list_tools``,
    ``False`` on timeout.

    Simply checking for credential existence is not enough: when
    ``connector_list_tools`` has already determined that the current
    credential is expired, an old (unusable) credential will still be
    returned by the credentials API.  We therefore verify each candidate
    with a ``list_tools`` call before reporting success.
    """
    client = _build_connector_client(run_as)
    deadline = time.monotonic() + _POLL_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        try:
            info = await client.beta.connectors.list_user_credentials_async(
                connector_id_or_name=connector_id,
            )

            if info.credentials:
                try:
                    await client.beta.connectors.list_tools_async(
                        connector_id_or_name=connector_id, credentials_name=credentials_name
                    )
                    logger.info(
                        "Credentials detected and verified during polling",
                        connector_id=connector_id,
                        credentials_name=credentials_name,
                        credential_count=len(info.credentials),
                    )
                    return True
                except Exception:
                    logger.debug(
                        "Credentials exist but are not yet usable",
                        connector_id=connector_id,
                        credential_count=len(info.credentials),
                    )
        except Exception:
            logger.warning(
                "Transient error while polling for credentials, will retry",
                connector_id=connector_id,
            )

        temporalio.activity.heartbeat()
        if temporalio.activity.is_cancelled():
            logger.info("Credential polling cancelled", connector_id=connector_id)
            return False
        await asyncio.sleep(_POLL_INTERVAL_SECONDS)

    logger.warning(
        "Credential polling timed out",
        connector_id=connector_id,
    )
    return False
