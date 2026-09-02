"""Client-host configuration validation — all errors at once.

Reproduces the 0.1.26 ``ClientModeConfigError`` UX: when a host configures any
client seam, every problem with the combination is collected and reported in
ONE exception, so the host fixes its startup wiring in one pass instead of
peeling errors one at a time.

Deliberately helpful, not restrictive: every seam is individually optional
(a host may want ONLY the key resolver, or ONLY a model catalog). Only
combinations that are guaranteed to blow up mid-run are rejected.
"""

from __future__ import annotations

from typing import Any

from matrx_ai.catalog.host_catalog import missing_catalog_methods
from matrx_ai.client_host.store import missing_store_methods

#: The configure() kwargs that mark a client-host install.
CLIENT_SEAM_KEYS: tuple[str, ...] = (
    "conversation_store",
    "model_catalog",
    "tool_source",
    "api_key_resolver",
    "get_jwt",
    "server_url",
    "source_app",
    "execution_agent_source",
)


class ClientHostConfigError(Exception):
    """Raised at configure() time when the client-host seams are inconsistent."""


def validate_client_host_config(
    *,
    conversation_store: Any = None,
    model_catalog: Any = None,
    tool_source: Any = None,
    api_key_resolver: Any = None,
    get_jwt: Any = None,
    server_url: Any = None,
    source_app: Any = None,
    execution_agent_source: Any = None,
) -> None:
    """Validate the client-host seam combination; raise with EVERY problem.

    Called from ``matrx_ai.configure()`` whenever at least one client seam is
    passed. A plain server host (none of these kwargs) never reaches this.
    """
    errors: list[str] = []

    if tool_source is not None:
        # Lazy import — matrx_ai.tools is a heavy package; only pay for it
        # when a host actually configures the seam.
        from matrx_ai.tools.tool_source import missing_tool_source_methods

        missing = missing_tool_source_methods(tool_source)
        if missing:
            errors.append(
                "tool_source does not implement the ToolSource protocol — "
                "missing/non-callable: " + ", ".join(missing)
            )

    if execution_agent_source is not None:
        from matrx_ai.client_host.agent_source import (
            missing_execution_agent_source_methods,
        )

        missing = missing_execution_agent_source_methods(execution_agent_source)
        if missing:
            errors.append(
                "execution_agent_source does not implement the "
                "ExecutionAgentSource protocol — missing/non-callable: "
                + ", ".join(missing)
            )

    if conversation_store is not None:
        missing = missing_store_methods(conversation_store)
        if missing:
            errors.append(
                "conversation_store does not implement the ConversationStore "
                "protocol — missing/non-callable: " + ", ".join(missing)
            )
        if model_catalog is None:
            errors.append(
                "conversation_store is configured without model_catalog. The "
                "execution path resolves every model through the catalog seam; "
                "without one, the first request falls through to the ORM path "
                "and dies with DBNotConfiguredError mid-run. Provide "
                "model_catalog=... (async list_models() / get_model())."
            )

    if model_catalog is not None:
        missing = missing_catalog_methods(model_catalog)
        if missing:
            errors.append(
                "model_catalog does not implement the ModelCatalog protocol — "
                "missing/non-callable: " + ", ".join(missing)
            )

    if api_key_resolver is not None and not callable(api_key_resolver):
        errors.append(
            "api_key_resolver must be a Callable[[str], str | None]; got "
            f"{type(api_key_resolver).__name__!r}."
        )

    if get_jwt is not None:
        import inspect

        if not callable(get_jwt):
            errors.append(
                "get_jwt must be a zero-argument callable returning str | None "
                f"(the current user's JWT); got {type(get_jwt).__name__!r}."
            )
        elif inspect.iscoroutinefunction(get_jwt):
            errors.append(
                "get_jwt must be a SYNC zero-argument callable returning "
                "str | None — an async def returns a coroutine at call time, "
                "which would be serialized into the Authorization header. "
                "Wrap your token cache in a sync getter."
            )
        if not server_url:
            errors.append(
                "get_jwt is configured without server_url. Server-backed "
                "features (tool registry fetch, authenticated reads) need the "
                "AIDream base URL — pass server_url=... (e.g. the value of "
                "AIDREAM_SERVER_URL_LIVE)."
            )

    if server_url is not None and (not isinstance(server_url, str) or not server_url.strip()):
        errors.append(
            f"server_url must be a non-empty string base URL; got {server_url!r}."
        )

    if source_app is not None and (not isinstance(source_app, str) or not source_app.strip()):
        errors.append(
            f"source_app must be a non-empty string (e.g. 'matrx_local'); got {source_app!r}."
        )

    if errors:
        raise ClientHostConfigError(
            "matrx-ai client-host configuration is invalid.\n"
            "The following are missing or inconsistent:\n"
            + "\n".join(f"  - {e}" for e in errors)
        )


__all__ = ["CLIENT_SEAM_KEYS", "ClientHostConfigError", "validate_client_host_config"]
