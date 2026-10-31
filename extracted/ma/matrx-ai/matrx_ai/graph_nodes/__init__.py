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
- ``ai.mandate.start``         — run a named JOB; the database picks the doer.
- ``ai.agent.assignment_batch``— durable coordinated variable assignments.
- ``ai.conversation.continue`` — append a user turn to an existing thread.
- ``ai.conversation.revise`` — check an answer; revise it in the same thread on a miss.
- ``ai.transcribe``            — catalog-dispatched speech-to-text.
- ``ai.text_to_speech``        — voice synthesis (ElevenLabs / Groq /
                                 Google / OpenAI) via UnifiedConfig.
- ``ai.generate_image``        — text → image (Imagen / FLUX / DALL-E /
                                 SD) via UnifiedConfig.
- ``ai.image.edit``            — AI edit of existing images (+ optional mask).
- ``ai.vision.read``           — describe / read the text in / ask about images.
- ``ai.generate_music``        — text → music (Eleven Music / Lyria).
- ``ai.generate_sound_effect`` — text → a short sound effect (ElevenLabs).
- ``ai.voice_to_voice``        — speech → the same speech in another voice (ElevenLabs).
- ``ai.moderate``              — text → a safety verdict with category scores (OpenAI).
- ``ai.judge.resolve``         — the author's judge agent picks the best of N gathered arms, or merges them.
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
        agent_produce_action,
        chat_action,
        conversation_action,
        image_action,
        image_edit_action,
        llm_action,
        mandate_action,
        moderation_action,
        music_action,
        resolve_action,
        revise_action,
        scrape_action,
        sound_effect_action,
        transcribe_action,
        tts_action,
        util_action,
        video_action,
        vision_action,
        voice_to_voice_action,
    )

    _registered = True


__all__ = [
    "AiExecutionResult",
    "AiMessage",
    "AiUsage",
    "register_with_graph",
]
