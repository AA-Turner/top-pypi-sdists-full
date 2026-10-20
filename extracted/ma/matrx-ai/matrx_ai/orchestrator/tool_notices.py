"""The ONE ``tool_processing`` notice — sent by the shared tool loop for every provider.

PB-03 defect 11 (2026-10-16): each provider adapter sent its own ``info``
``tool_processing`` event, and the OpenAI and Google adapters never did, so the
same agent call announced itself on Claude and was silent on GPT and Gemini.
``orchestrator.executor.handle_tool_calls`` calls this once per provider
response, before any tool is dispatched; no adapter emits the event itself
(guard: ``tests/test_tool_processing_is_provider_independent.py``).
"""

from __future__ import annotations

from typing import Any


async def emit_tool_processing(response: Any, emitter: Any) -> None:
    """Announce every tool call in ``response`` (one ``info`` event per call). Never raises."""
    if emitter is None:
        return
    try:
        from matrx_connect.context.events import InfoPayload

        from matrx_ai.config.tools_config import ToolCallContent

        messages = getattr(response, "messages", None) or []
        if not isinstance(messages, list):
            messages = [messages]
        for message in messages:
            for content in getattr(message, "content", None) or []:
                if not isinstance(content, ToolCallContent):
                    continue
                await emitter.send_info(
                    InfoPayload(
                        code="tool_processing",
                        system_message=f"Executing {content.name}",
                        user_message=f"Using tool {content.name}",
                        metadata={"tool_call": content.name, "call_id": content.id},
                    )
                )
    except Exception as exc:  # noqa: BLE001 — a notice must never break the tool loop
        from matrx_utils import vcprint

        vcprint(f"[tool_notices] could not send tool_processing: {exc!r}", color="yellow")
