"""ABC monkey-patch factory for the client query entry point."""

from __future__ import annotations

import functools
import logging
from typing import Any

from aigie.tracing.monkey_patch_lifecycle import PatchTarget

from aigie.integrations.claude_agent_sdk.session_context import get_or_create_session_context
from aigie.integrations.claude_agent_sdk._patches._shared import (
    _enable_hook_events,
    _extract_agent_name,
    _shorten_model_name,
    _wrap_user_hooks,
)

logger = logging.getLogger(__name__)


def client_query_patch_target() -> PatchTarget:  # noqa: C901, PLR0915
    """Declarative patch target for ``ClaudeSDKClient.query``.

    Note: ClaudeSDKClient.query() returns None and sends a message.
    Messages are received via receive_messages() or receive_response().
    We just trace the call itself here.
    """

    def get_target() -> tuple[Any, str]:
        from claude_agent_sdk import ClaudeSDKClient

        return ClaudeSDKClient, "query"

    def make_wrapper(original_query: Any) -> Any:  # noqa: C901, PLR0915
        @functools.wraps(original_query)
        async def traced_client_query(self, prompt, session_id: str = "default"):  # noqa: C901, PLR0915, PLR0912
            """Traced version of ClaudeSDKClient.query()."""
            from aigie.client import get_aigie
            from aigie.integrations.claude_agent_sdk.config import ClaudeAgentSDKConfig
            from aigie.integrations.claude_agent_sdk.native_callback import ClaudeAgentSDKEvents

            aigie = get_aigie()
            config = ClaudeAgentSDKConfig.from_env()

            if aigie and aigie._initialized and config.enabled:
                # Get model and system_prompt from client options
                client_options = getattr(self, "options", None)
                _enable_hook_events(client_options)
                model: str = (
                    getattr(client_options, "model", None)
                    or getattr(self, "model", None)
                    or "claude-sonnet-4-20250514"
                )
                system_prompt = getattr(client_options, "system_prompt", "") or ""

                # Extract agent name from system prompt if available
                trace_name = (
                    _extract_agent_name(system_prompt, model, aigie)
                    if (system_prompt or getattr(aigie, "_agent_name", None))
                    else f"{_shorten_model_name(model)} Client Session"
                )

                # Get or create session context - reuse existing trace
                session_ctx = get_or_create_session_context(trace_name=trace_name)

                # Get or create handler with session context
                handler = getattr(self, "_aigie_handler", None)
                if handler is None:
                    handler = ClaudeAgentSDKEvents(
                        trace_name=trace_name,
                        capture_tool_results=config.capture_tool_results,
                        capture_messages=config.capture_messages,
                        session_context=session_ctx,
                    )
                    handler._aigie = aigie
                    self._aigie_handler = handler
                    _wrap_user_hooks(client_options, handler)
                prompt_str = prompt if isinstance(prompt, str) else "<async_input>"

                # Generate turn ID
                import uuid

                turn_id = str(uuid.uuid4())

                # Start a turn for this query - turn number comes from session context
                await handler.handle_turn_start(turn_id, prompt_str)

                # Store the turn_id for later completion
                if not hasattr(self, "_pending_turn_ids"):
                    self._pending_turn_ids = []
                self._pending_turn_ids.append(turn_id)

                try:
                    # Call original - returns None (sends message)
                    return await original_query(self, prompt, session_id)
                except Exception as e:
                    # Remove from pending and complete with error
                    if turn_id in self._pending_turn_ids:
                        self._pending_turn_ids.remove(turn_id)
                    await handler.handle_turn_end(turn_id, error=str(e))
                    raise
            else:
                return await original_query(self, prompt, session_id)

        return traced_client_query

    return PatchTarget(
        name="ClaudeSDKClient.query",
        get_target=get_target,
        make_wrapper=make_wrapper,
    )
