"""A stored ``source_set`` never sends media the TURN's model cannot take (one-input review A7).

A reloaded turn re-splices the media its set resolved to. Before every provider call
``resolve_structured_inputs`` asks the ONE capability check
(``provider_io_capabilities.model_media_inputs`` — model row × provider route) what this turn's
model takes; a stored kind it cannot take is re-resolved for this model as text, with a notice.
And the turn's model always decides: a set's own ``target_model_id`` never outranks it.

Only the edges are faked: the model row and catalog route (DB) and the host resolver seam.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

FILE = "5a0b1c2d-3e4f-4a5b-8c6d-7e8f9a0b1c2d"
OLD_MODEL = "11111111-1111-4111-8111-111111111111"
TURN_MODEL = "22222222-2222-4222-8222-222222222222"


def _row(inputs: list[str]) -> Any:
    return SimpleNamespace(
        name="m",
        capabilities={"input": inputs, "output": ["text"], "features": [], "interaction": "turn", "multilingual": True},
    )


@pytest.fixture
def edges(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    from matrx_connect.context import app_context

    from matrx_ai import _ext
    from matrx_ai.catalog import manager as catalog
    from matrx_ai.db.ai_models import ai_model_manager as models
    from matrx_ai.providers.provider_io_capabilities import endpoint_native_inputs

    if endpoint_native_inputs("anthropic_chat") is None:
        pytest.skip("anthropic_chat is not a chat route in this catalog build")

    state: dict[str, Any] = {"inputs": ["text"], "asked": [], "fail": False}

    async def load_model(_ref: str) -> Any:
        return _row(state["inputs"])

    async def loaded() -> None:
        return None

    async def resolver(source_set: dict[str, Any], *, user_id: str | None) -> dict[str, Any]:
        state["asked"].append(source_set.get("target_model_id"))
        if state["fail"]:
            raise RuntimeError("the file store is down")
        takes_image = "image" in state["inputs"]
        return {
            "text": "## Source 1: chart.png\nA bar chart of revenue by month.",
            "media": [{"type": "media", "kind": "image", "file_id": FILE, "mime_type": "image/png"}]
            if takes_image
            else [],
            "dropped": [],
        }

    monkeypatch.setattr(models.ai_model_manager_instance, "load_model", load_model)
    monkeypatch.setattr(catalog.ai_catalog_manager, "ensure_loaded", loaded)
    monkeypatch.setattr(catalog.ai_catalog_manager, "wire_format_for", lambda *_a, **_k: "anthropic_chat")
    monkeypatch.setattr(app_context, "try_get_app_context", lambda: SimpleNamespace(user_id="u", metadata={}))
    monkeypatch.setitem(_ext._registry, _ext._SOURCE_SET_RESOLVER_KEY, resolver)
    return state


def _stored_history() -> Any:
    """A reloaded conversation: turn 1 resolved its set to an image for a vision model."""
    from matrx_ai.config.message_config import MessageList, UnifiedMessage

    stored_part = {
        "type": "source_set",
        "source_set": {
            "envelope": "source_set",
            "version": 1,
            "target_model_id": OLD_MODEL,
            "sources": [
                {"envelope": "resource_ref", "resource_type": "file", "resource_id": FILE,
                 "representation": "media", "label": "chart.png"},
            ],
        },
        "metadata": {
            "resolved_text": "## Source 1: chart.png\nDelivered as image media alongside this text.",
            "resolved_media": [{"type": "media", "kind": "image", "file_id": FILE, "mime_type": "image/png"}],
        },
    }
    return MessageList(
        [
            UnifiedMessage.from_dict({"role": "user", "content": [{"type": "text", "text": "What is it?"}, stored_part]}),
            UnifiedMessage.from_dict({"role": "assistant", "content": [{"type": "text", "text": "A chart."}]}),
            UnifiedMessage.from_dict({"role": "user", "content": [{"type": "text", "text": "And the peak?"}]}),
        ]
    )


def _first_turn_blocks(messages: Any) -> list[dict[str, Any]]:
    return list(messages)[0].to_anthropic_blocks()


@pytest.mark.asyncio
async def test_a_text_only_turn_model_never_receives_the_stored_image(edges) -> None:
    from matrx_ai.config.media_config import ImageContent
    from matrx_ai.config.structured_input_resolver import resolve_structured_inputs

    messages = _stored_history()
    first = list(messages)[0]
    assert [c for c in first.content if isinstance(c, ImageContent)], "the reload re-spliced the image"

    edges["inputs"] = ["text"]
    await resolve_structured_inputs(messages, model_id=TURN_MODEL)

    assert not [c for c in first.content if isinstance(c, ImageContent)]
    blocks = _first_turn_blocks(messages)
    assert not [b for b in blocks if b.get("type") == "image"]
    texts = "\n".join(b.get("text", "") for b in blocks if b.get("type") == "text")
    assert "A bar chart of revenue by month." in texts, "the item fell back to its text"
    assert "cannot take image directly" in texts, "the model is told why"
    # Re-resolved for THIS turn's model, never the set's stored target.
    assert edges["asked"] == [TURN_MODEL]


@pytest.mark.asyncio
async def test_a_turn_model_that_takes_images_replays_them_untouched(edges) -> None:
    from matrx_ai.config.media_config import ImageContent
    from matrx_ai.config.structured_input_resolver import resolve_structured_inputs

    edges["inputs"] = ["text", "image"]
    messages = _stored_history()
    await resolve_structured_inputs(messages, model_id=TURN_MODEL)

    first = list(messages)[0]
    assert len([c for c in first.content if isinstance(c, ImageContent)]) == 1
    assert edges["asked"] == [], "a stored set the model can take is never re-read"


@pytest.mark.asyncio
async def test_a_failed_re_read_withholds_the_media_and_says_so(edges) -> None:
    from matrx_ai.config.media_config import ImageContent
    from matrx_ai.config.structured_input_resolver import resolve_structured_inputs

    edges["inputs"], edges["fail"] = ["text"], True
    messages = _stored_history()
    await resolve_structured_inputs(messages, model_id=TURN_MODEL)

    first = list(messages)[0]
    assert not [c for c in first.content if isinstance(c, ImageContent)]
    texts = "\n".join(b.get("text", "") for b in _first_turn_blocks(messages) if b.get("type") == "text")
    assert "cannot take image directly" in texts


@pytest.mark.asyncio
async def test_the_turns_model_outranks_the_sets_own_target(edges) -> None:
    from matrx_ai.config.message_config import MessageList, UnifiedMessage
    from matrx_ai.config.structured_input_resolver import resolve_structured_inputs

    part = {
        "type": "source_set",
        "source_set": {
            "envelope": "source_set",
            "version": 1,
            "target_model_id": OLD_MODEL,
            "sources": [{"envelope": "resource_ref", "resource_type": "file", "resource_id": FILE,
                         "representation": "media"}],
        },
    }
    messages = MessageList([UnifiedMessage.from_dict({"role": "user", "content": [part]})])
    await resolve_structured_inputs(messages, model_id=TURN_MODEL)
    assert edges["asked"] == [TURN_MODEL]
