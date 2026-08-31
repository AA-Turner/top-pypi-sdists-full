"""ABC monkey-patch factories for the client connect entry point + __aexit__."""

from __future__ import annotations

import functools
import logging
from typing import Any

from aigie.integrations.claude_agent_sdk._patches._shared import (
    _enable_hook_events,
    _skip_instrumentation,
    _trace_name_from_options,
    _wrap_user_hooks,
)
from aigie.integrations.claude_agent_sdk.session_context import (
    get_or_create_session_context,
    get_session_context,
    set_session_context,
)
from aigie.tracing.monkey_patch_lifecycle import PatchTarget

logger = logging.getLogger(__name__)


def client_connect_patch_target() -> PatchTarget:  # noqa: C901, PLR0915
    """Declarative patch target for ``ClaudeSDKClient.connect``."""

    def get_target() -> tuple[Any, str]:
        from claude_agent_sdk import ClaudeSDKClient

        if not hasattr(ClaudeSDKClient, "connect"):
            raise ImportError("ClaudeSDKClient.connect not available in this SDK version")
        return ClaudeSDKClient, "connect"

    def make_wrapper(original_connect: Any) -> Any:  # noqa: C901, PLR0915
        @functools.wraps(original_connect)
        async def traced_connect(self, *args, **kwargs):  # noqa: C901, PLR0915, PLR0912
            """Traced version of ClaudeSDKClient.connect()."""
            if _skip_instrumentation(self):
                return await original_connect(self, *args, **kwargs)
            from aigie.client import get_aigie
            from aigie.integrations.claude_agent_sdk.config import ClaudeAgentSDKConfig
            from aigie.integrations.claude_agent_sdk.native_callback import ClaudeAgentSDKEvents

            aigie = get_aigie()
            config = ClaudeAgentSDKConfig.from_env()

            if aigie and aigie._initialized and config.enabled:
                # Get model and system_prompt from client options
                client_options = getattr(self, "options", None)
                _enable_hook_events(client_options)
                model = getattr(client_options, "model", None) or getattr(
                    self, "model", "claude-sonnet-4-20250514"
                )
                system_prompt = getattr(client_options, "system_prompt", "") or ""

                # Check if we're already in an explicit session scope (e.g., claude_session context manager)
                existing_ctx = get_session_context()
                resume_id = getattr(client_options, "resume", None)
                owns_context = existing_ctx is None or (
                    resume_id is not None and existing_ctx.trace_id != resume_id
                )

                trace_name = _trace_name_from_options(
                    system_prompt, model, aigie, "Session", capture_content=config.capture_messages
                )

                if owns_context:
                    # Create new session context for this connection
                    session_ctx = get_or_create_session_context(
                        trace_name=trace_name, trace_id=resume_id
                    )
                else:
                    # Reuse existing session context - this connection is part of a larger session
                    session_ctx = existing_ctx

                # Track whether this connection owns the context
                self._owns_session_context = owns_context
                self._outer_session_context = existing_ctx

                handler = ClaudeAgentSDKEvents(
                    trace_name=trace_name,
                    capture_tool_results=config.capture_tool_results,
                    capture_messages=config.capture_messages,
                    session_context=session_ctx,
                )
                handler._aigie = aigie
                self._aigie_handler = handler
                handler._aigie_client = self
                _wrap_user_hooks(client_options, handler)

                from aigie.integrations.claude_agent_sdk._events._tool_catalog import (
                    resolve_tool_defs,
                )

                # Use MCP/allowed_tools fallback when options.tools is empty.
                resolved_tools = await resolve_tool_defs(
                    client_options, getattr(client_options, "tools", []) or []
                )
                options = {
                    "model": model,
                    "system_prompt": system_prompt,
                    "tools": resolved_tools,
                }

                await handler.handle_session_start(self, options)

                try:
                    return await original_connect(self, *args, **kwargs)
                except Exception as e:
                    await handler.handle_session_end(
                        handler.total_turns, handler.total_cost, str(e)
                    )
                    raise
            else:
                return await original_connect(self, *args, **kwargs)

        return traced_connect

    return PatchTarget(
        name="ClaudeSDKClient.connect",
        get_target=get_target,
        make_wrapper=make_wrapper,
    )


def client_aexit_patch_target() -> PatchTarget:  # noqa: C901, PLR0915
    """Declarative patch target for ``ClaudeSDKClient.__aexit__`` so sessions
    end cleanly on context-manager exit."""

    def get_target() -> tuple[Any, str]:
        from claude_agent_sdk import ClaudeSDKClient

        if not hasattr(ClaudeSDKClient, "__aexit__"):
            raise ImportError("ClaudeSDKClient.__aexit__ not available in this SDK version")
        return ClaudeSDKClient, "__aexit__"

    def make_wrapper(original_aexit: Any) -> Any:  # noqa: C901, PLR0915
        @functools.wraps(original_aexit)
        async def traced_aexit(self, exc_type, exc_val, exc_tb):  # noqa: C901, PLR0915, PLR0912
            """Traced version of ClaudeSDKClient.__aexit__()."""
            handler = getattr(self, "_aigie_handler", None)
            if handler and not getattr(self, "_aigie_session_ended", False):
                error = str(exc_val) if exc_val else None
                await handler.handle_session_end(handler.total_turns, handler.total_cost, error)
                self._aigie_session_ended = True
            # Only restore session context if this connection created it
            # This preserves context for operations that share a session scope
            if getattr(self, "_owns_session_context", True):
                set_session_context(getattr(self, "_outer_session_context", None))
            return await original_aexit(self, exc_type, exc_val, exc_tb)

        return traced_aexit

    return PatchTarget(
        name="ClaudeSDKClient.__aexit__",
        get_target=get_target,
        make_wrapper=make_wrapper,
    )
