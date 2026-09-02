"""matrx-ai → matrx-graph integration: AI entry points as typed actions.

Import this module from the host app (e.g. aidream) to register all four
AI entry points with matrx-graph's default registry::

    from matrx_ai.graph_nodes import register_with_graph
    register_with_graph()

Actions registered:

- ``ai.llm.chat``              — single-shot LLM call (no tools, no loop).
- ``ai.chat.manual``           — full-control chat with explicit model +
                                 messages + tools.
- ``ai.agent.start``           — run a saved agent with a user input.
- ``ai.agent.assignment_batch``— durable coordinated variable assignments.
- ``ai.agent.tool_calling``    — inline agent loop with native provider
                                 tool calling.
- ``ai.agent.react``           — inline ReAct-style agent with structured
                                 Thought / Action / Observation trace.
- ``ai.conversation.continue`` — append a user turn to an existing thread.
- ``ai.transcribe``            — catalog-dispatched speech-to-text.
- ``ai.text_to_speech``        — voice synthesis (ElevenLabs / Groq /
                                 Google / OpenAI) via UnifiedConfig.
- ``ai.generate_image``        — text → image (Imagen / FLUX / DALL-E /
                                 SD) via UnifiedConfig.
- ``ai.image.concept_generate``— pick visual concepts for a topic (large model).
- ``ai.image.prompt_write``    — write image prompts from a concept (small model).
- ``ai.image.qc_judge``        — vision-model pass/fail on a generated image.
Every action returns the canonical ``AiExecutionResult`` — stable Pydantic
shape regardless of which entry point ran. Downstream workflow nodes wire
to ``result.final_text``, ``result.conversation_id``, ``result.usage``, etc.
"""

from __future__ import annotations

from matrx_ai.graph_nodes.shared import AiExecutionResult, AiMessage, AiUsage

_registered = False


def register_with_graph() -> None:
    """Import the action modules, which triggers ``@action`` decoration.

    Idempotent — safe to call multiple times. Imports are side-effectful
    (each module's ``@action`` runs at import time and registers into
    matrx-graph's default registries).
    """
    global _registered
    if _registered:
        return

    from matrx_ai.graph_nodes import (  # noqa: F401 — imported for side effects
        agent_action,
        agent_assignment_action,
        agent_loop_actions,
        agent_produce_action,
        chat_action,
        conversation_action,
        extract_action,
        image_action,
        image_pipeline_actions,
        llm_action,
        scrape_action,
        search_action,
        transcribe_action,
        tts_action,
        util_action,
        video_action,
    )

    _registered = True


__all__ = [
    "AiExecutionResult",
    "AiMessage",
    "AiUsage",
    "register_with_graph",
]
