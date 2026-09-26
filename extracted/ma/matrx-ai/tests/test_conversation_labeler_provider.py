"""The conversation labeler runs through its mandates — never a provider SDK.

2026-09-25: the labeler used to call ``AsyncGroq`` directly with an inline prompt.
It is now held by ``conversation.label_chat`` / ``conversation.label_agent_run``;
the Holder owns the model, prompt and settings. These tests pin the three things
the code still owns: WHICH mandate a conversation goes to, the data bounding that
keeps a 227K-character agent definition under the provider's admission boundary,
and the loud failure capture.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

import matrx_ai.agent_runners.conversation_labeler as labeler
import matrx_ai.mandates as mandates
from matrx_ai.code_call_mandate_keys import (
    CONVERSATION_LABEL_AGENT_RUN_MANDATE,
    CONVERSATION_LABEL_CHAT_MANDATE,
)


@pytest.fixture
def held_calls(monkeypatch):
    calls: list[dict] = []

    async def _hold(mandate_key, *, consumer, variables=None, metadata=None):
        calls.append({"mandate_key": mandate_key, "consumer": consumer, "variables": variables})
        return SimpleNamespace(mandate_key=mandate_key, model="holder-model")

    async def _run(held, **kwargs):
        return SimpleNamespace(
            final_text='{"label":"Held","description":"By the Holder","keywords":[]}'
        )

    monkeypatch.setattr(mandates, "hold_code_call", _hold)
    monkeypatch.setattr(mandates, "run_held_call", _run)
    return calls


def _imported_modules(path: str) -> set[str]:
    import ast

    tree = ast.parse(open(path).read())
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def test_labeler_imports_no_provider_sdk() -> None:
    imported = _imported_modules(labeler.__file__)
    assert not {m for m in imported if m.split(".")[0] in {"groq", "openai", "anthropic"}}
    assert not hasattr(labeler, "LABELER_MODEL")


async def test_chat_goes_to_the_chat_mandate(held_calls) -> None:
    result = await labeler.label_chat_conversation("User:\nhi", recent_titles="")

    assert result.success is True
    assert result.output.startswith('{"label":"Held"')
    assert held_calls[0]["mandate_key"] == CONVERSATION_LABEL_CHAT_MANDATE
    assert held_calls[0]["variables"] == {
        "conversation_content": "User:\nhi",
        "recent_titles": labeler.NONE_VALUE,
    }


async def test_agent_run_goes_to_the_agent_mandate(held_calls) -> None:
    await labeler.label_agent_conversation(
        conversation_content="User:\nhi",
        recent_titles="- Old title",
        agent_name="Recipe Writer",
        agent_description="",
        user_variables="",
        user_prompt="",
    )

    call = held_calls[0]
    assert call["mandate_key"] == CONVERSATION_LABEL_AGENT_RUN_MANDATE
    assert call["variables"]["agent_name"] == "Recipe Writer"
    assert call["variables"]["agent_description"] == labeler.NOT_AVAILABLE
    assert call["variables"]["user_variables"] == labeler.NONE_PROVIDED
    assert call["variables"]["recent_titles"] == "- Old title"


async def test_agent_labeler_bounds_every_untrusted_value(held_calls) -> None:
    """Regress the provider TPM failure caused by a 227K-character prompt."""
    huge = "distinct-start " + ("x" * 120_000) + " distinct-end"

    await labeler.label_agent_conversation(
        conversation_content=labeler._trim_content(huge, 5000),
        recent_titles=huge,
        agent_name=huge,
        agent_description=huge,
        user_variables=huge,
        user_prompt=huge,
    )

    variables = held_calls[0]["variables"]
    assert sum(len(v) for v in variables.values()) < 25_000
    assert all("distinct-start" in v and "distinct-end" in v for v in variables.values())
    assert sum(v.count("[... content trimmed ...]") for v in variables.values()) == 6


async def test_labeler_failure_reaches_central_capture(monkeypatch) -> None:
    captured: dict = {}

    async def _hold(mandate_key, **_kwargs):
        return SimpleNamespace(mandate_key=mandate_key, model="holder-model")

    async def _run(held, **kwargs):
        raise RuntimeError("provider model unavailable")

    async def _capture(exc, *, kind, **fields):
        captured.update({"exc": exc, "kind": kind, **fields})

    monkeypatch.setattr(mandates, "hold_code_call", _hold)
    monkeypatch.setattr(mandates, "run_held_call", _run)
    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", _capture)

    result = await labeler.label_chat_conversation("User:\nhi", recent_titles="")

    assert result.success is False
    assert result.error == "provider model unavailable"
    assert captured["kind"] == "conversation_labeler_failed"
    assert captured["payload"] == {
        "mandate_key": CONVERSATION_LABEL_CHAT_MANDATE,
        "model": "holder-model",
    }


async def test_unresolvable_mandate_is_captured_not_silent(monkeypatch) -> None:
    captured: dict = {}

    async def _hold(mandate_key, **_kwargs):
        raise mandates.MandateResolutionUnavailable(mandate_key, "conversation.labeler", "no Holder")

    async def _capture(exc, *, kind, **fields):
        captured.update({"exc": exc, "kind": kind, **fields})

    monkeypatch.setattr(mandates, "hold_code_call", _hold)
    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", _capture)

    result = await labeler.label_chat_conversation("User:\nhi", recent_titles="")

    assert result.success is False
    assert captured["kind"] == "conversation_labeler_failed"
    assert captured["payload"]["model"] is None
