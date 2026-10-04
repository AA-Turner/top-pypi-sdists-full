"""Every catalog writer is told when a text chat model declares no function calling.

The 2026-07-07 cut from the retired ``api_class`` to capability data backfilled structured
output (ai_011) but not ``function_calling``: gemini-2.5-flash, gpt-5.1 and gpt-5.2 kept
serving with NO tools and nothing said so. ``normalize_capabilities`` — the one check the
agent DB write tool, ``scripts/set_model_capabilities.py`` and the vocabulary audit share —
now carries the notice.
"""

from __future__ import annotations

from matrx_ai.providers.capability_vocabulary import normalize_capabilities

_CHAT = {"input": ["text"], "output": ["text"], "interaction": "turn"}


def test_a_text_chat_model_without_function_calling_is_flagged() -> None:
    result = normalize_capabilities(
        {**_CHAT, "features": ["json_mode", "structured_output"]}, label="gemini-2.5-flash"
    )
    assert result.ok
    assert len(result.notices) == 1 and "function_calling" in result.notices[0]


def test_tool_models_and_media_models_are_not_flagged() -> None:
    assert not normalize_capabilities({**_CHAT, "features": ["function_calling"]}).notices
    assert not normalize_capabilities(
        {"input": ["text"], "output": ["audio"], "interaction": "turn", "features": []}
    ).notices
    assert not normalize_capabilities(
        {"input": ["audio"], "output": ["text"], "interaction": "turn", "features": []}
    ).notices


def test_the_agent_db_write_tool_announces_the_notice() -> None:
    from matrx_ai.tools.implementations import database

    rows = [{"name": "gpt-5.1", "capabilities": {**_CHAT, "features": ["json_mode"]}}]
    error, corrections = database._guard_vocabulary("ai", "model_definition", rows)
    assert error is None
    assert any(c.startswith("REVIEW:") and "function_calling" in c for c in corrections)
