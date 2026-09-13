"""PROMPT PRE-FLIGHT at the send boundary — refuse before the provider does.

Live 2026-09-12, workflow run ``cdde033d`` (definition "Newsroom Desk"): four
per-document ledger agents, a Gather, and a merge step that received the WHOLE
agent results (each carrying the document inside its ``messages`` history).
Anthropic refused it — ``prompt is too long: 1,019,616 tokens > 1,000,000
maximum`` — six steps in, naming no step, no field and no remedy, after the run
had already paid for four agents.

Locked here: the send boundary measures the prompt against the resolved model's
declared context window and RAISES first, naming the step, the numbers and the
remedy; a prompt that fits is untouched; an unmeasurable model is passed
through (never a guessed ceiling); and the catalog is where the window comes
from.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.config import context_preflight
from matrx_ai.config.context_preflight import PromptTooLargeError, estimate_prompt_tokens
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send, reset_loop_state

CONVERSATION_ID = "conv-preflight"
REQUEST_ID = "req-preflight"
ONE_MILLION = 1_000_000


def _config(tokens: int, model: str = "claude-opus-4-5") -> SimpleNamespace:
    # chars/4 is the estimator, so N tokens of prompt = 4N chars.
    return SimpleNamespace(
        model=model,
        matrx_model_name=model,
        messages=[{"role": "user", "content": "x" * (tokens * 4)}],
        system_instruction=None,
        tools=[],
        prompt_cache_key=None,
    )


@pytest.fixture(autouse=True)
def _clean():
    reset_loop_state(CONVERSATION_ID, REQUEST_ID)
    context_preflight.configure_context_preflight(enabled=True, trip_fraction=1.0)
    yield
    reset_loop_state(CONVERSATION_ID, REQUEST_ID)
    context_preflight.configure_context_preflight(enabled=True, trip_fraction=1.0)


@pytest.fixture
def _window(monkeypatch):
    def _set(window: int | None):
        monkeypatch.setattr(context_preflight, "_declared_window", lambda _ref: window)

    return _set


@pytest.mark.asyncio
async def test_over_window_prompt_is_refused_before_the_provider(_window) -> None:
    _window(ONE_MILLION)
    with pytest.raises(PromptTooLargeError) as excinfo:
        await prepare_for_send(
            _config(1_100_000),
            stage=STAGE_LOOP,
            conversation_id=CONVERSATION_ID,
            request_id=REQUEST_ID,
            iteration=1,
        )

    err = excinfo.value
    assert err.estimated_tokens > ONE_MILLION
    assert err.context_window == ONE_MILLION
    message = str(err)
    # The four things the provider's own refusal never said:
    assert "conversation conv-preflight" in message  # WHICH step/call
    assert "1,100,0" in message and "1,000,000" in message  # the numbers
    assert "claude-opus-4-5" in message  # the model
    assert "select the field" in message  # the remedy
    assert "structured_outputs" in message  # and where to point the edge


@pytest.mark.asyncio
async def test_the_refusal_names_the_workflow_step(_window, monkeypatch) -> None:
    _window(ONE_MILLION)
    ctx = SimpleNamespace(metadata={"workflow_node_id": "n_cross"}, execution_id="cdde033d")
    monkeypatch.setattr("matrx_ai.context.app_context.try_get_app_context", lambda: ctx)

    with pytest.raises(PromptTooLargeError) as excinfo:
        await prepare_for_send(
            _config(1_100_000),
            stage=STAGE_LOOP,
            conversation_id=CONVERSATION_ID,
            request_id=REQUEST_ID,
            iteration=1,
        )
    assert "n_cross" in str(excinfo.value)
    assert "cdde033d" in str(excinfo.value)


@pytest.mark.asyncio
async def test_a_prompt_that_fits_passes_and_is_not_trimmed(_window) -> None:
    _window(ONE_MILLION)
    config = _config(10_000)
    before = list(config.messages)

    prep = await prepare_for_send(
        config,
        stage=STAGE_LOOP,
        conversation_id=CONVERSATION_ID,
        request_id=REQUEST_ID,
        iteration=1,
    )

    assert prep.preflight is not None
    assert prep.preflight["context_window"] == ONE_MILLION
    assert prep.preflight["estimated_tokens"] == pytest.approx(10_000, rel=0.01)
    assert config.messages == before  # a pre-flight never shortens anything


@pytest.mark.asyncio
async def test_a_model_with_no_declared_window_is_passed_through(_window) -> None:
    _window(None)  # unmeasurable — announced by the module, never guessed
    prep = await prepare_for_send(
        _config(5_000_000),
        stage=STAGE_LOOP,
        conversation_id=CONVERSATION_ID,
        request_id=REQUEST_ID,
        iteration=1,
    )
    assert prep.preflight is None


def test_estimator_counts_system_messages_and_tools() -> None:
    config = SimpleNamespace(
        model="m",
        matrx_model_name="m",
        system_instruction="s" * 400,
        messages=[{"role": "user", "content": "u" * 400}],
        tools=[{"name": "t", "description": "d" * 400}],
    )
    # All three parts counted (~1200 chars / 4), never messages alone.
    assert estimate_prompt_tokens(config) >= 300


def test_catalog_is_where_the_window_comes_from() -> None:
    """The ONE source of the ceiling: ai.model_definition.context_window,
    served by the catalog manager — never a constant in this package."""
    from matrx_ai.catalog.manager import ai_catalog_manager

    ai_catalog_manager.load_from_rows(
        endpoints=[],
        apis=[],
        offerings=[],
        settings=[],
        providers={},
        models=[
            {
                "id": "11111111-1111-1111-1111-111111111111",
                "name": "preflight-test-model",
                "common_name": "Preflight Test Model",
                "context_window": ONE_MILLION,
            },
            {
                "id": "22222222-2222-2222-2222-222222222222",
                "name": "windowless-test-model",
                "common_name": "Windowless",
            },
        ],
        aliases=[],
        voices=[],
    )
    assert ai_catalog_manager.context_window("preflight-test-model") == ONE_MILLION
    assert ai_catalog_manager.context_window("windowless-test-model") is None
    assert ai_catalog_manager.context_window("not-a-model") is None
