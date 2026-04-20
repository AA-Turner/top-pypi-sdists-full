"""Unit tests for the auto-propose memory extractor (#1454)."""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import AsyncMock

import pytest

from anteroom.config import MemoryAutoProposeConfig
from anteroom.services.memory_extractor import (
    ExtractedCandidate,
    extract_candidates,
)
from anteroom.services.memory_recall import RecalledMemory


def _config(**overrides: Any) -> MemoryAutoProposeConfig:
    base: dict[str, Any] = {
        "enabled": True,
        "max_candidates_per_turn": 2,
        "categories": ["preference", "project_fact", "decision", "workflow_hint"],
        "min_confidence": 0.7,
        "notify_inline": True,
        "cooldown_turns": 5,
    }
    base.update(overrides)
    return MemoryAutoProposeConfig(**base)


def _ai(json_text: str | None) -> Any:
    """Mock AIService whose ``complete`` returns the given JSON string."""
    svc = AsyncMock()
    svc.complete = AsyncMock(return_value=json_text)
    return svc


def _memory(content: str, *, category: str = "preference") -> RecalledMemory:
    return RecalledMemory(
        fqn=f"@user/memory/{category[:4]}-abc",
        namespace="@user/memory",
        name="test",
        content=content,
        distance=0.1,
        scope="user",
        category=category,
    )


@pytest.mark.asyncio
async def test_disabled_returns_disabled_reason() -> None:
    cfg = _config(enabled=False)
    items, reason = await extract_candidates(
        assistant_text="The user prefers dark mode and Python tabs.",
        ai_service=_ai('{"candidates":[]}'),
        recalled_memories=[],
        config=cfg,
    )
    assert items == []
    assert reason == "disabled"


@pytest.mark.asyncio
async def test_empty_input_skipped() -> None:
    items, reason = await extract_candidates(
        assistant_text="OK.",
        ai_service=_ai('{"candidates":[]}'),
        recalled_memories=[],
        config=_config(),
    )
    assert items == []
    assert reason == "empty_input"


@pytest.mark.asyncio
async def test_ai_returns_none_failed() -> None:
    items, reason = await extract_candidates(
        assistant_text="x" * 200,
        ai_service=_ai(None),
        recalled_memories=[],
        config=_config(),
    )
    assert items == []
    assert reason == "failed"


@pytest.mark.asyncio
async def test_ai_raises_failed() -> None:
    svc = AsyncMock()
    svc.complete = AsyncMock(side_effect=RuntimeError("boom"))
    items, reason = await extract_candidates(
        assistant_text="x" * 200,
        ai_service=svc,
        recalled_memories=[],
        config=_config(),
    )
    assert items == []
    assert reason == "failed"


@pytest.mark.asyncio
async def test_invalid_json_failed() -> None:
    items, reason = await extract_candidates(
        assistant_text="x" * 200,
        ai_service=_ai("not json {[}"),
        recalled_memories=[],
        config=_config(),
    )
    assert items == []
    assert reason == "failed"


@pytest.mark.asyncio
async def test_valid_extraction_ok() -> None:
    payload = json.dumps(
        {
            "candidates": [
                {
                    "category": "preference",
                    "content": "User prefers dark mode in IDE.",
                    "confidence": 0.9,
                }
            ]
        }
    )
    items, reason = await extract_candidates(
        assistant_text="x" * 200,
        ai_service=_ai(payload),
        recalled_memories=[],
        config=_config(),
    )
    assert reason == "ok"
    assert len(items) == 1
    assert items[0].content == "User prefers dark mode in IDE."
    assert items[0].category == "preference"
    assert items[0].confidence == 0.9
    assert items[0].scope == "user"  # default


@pytest.mark.asyncio
async def test_low_confidence_filtered() -> None:
    payload = json.dumps(
        {
            "candidates": [
                {"category": "preference", "content": "Low conf statement.", "confidence": 0.5},
            ]
        }
    )
    items, reason = await extract_candidates(
        assistant_text="x" * 200,
        ai_service=_ai(payload),
        recalled_memories=[],
        config=_config(min_confidence=0.7),
    )
    assert items == []
    assert reason == "no_results"


@pytest.mark.asyncio
async def test_category_filter() -> None:
    payload = json.dumps(
        {
            "candidates": [
                {"category": "preference", "content": "Allowed pref.", "confidence": 0.95},
                {"category": "tool_pref", "content": "Disallowed cat.", "confidence": 0.95},
            ]
        }
    )
    items, reason = await extract_candidates(
        assistant_text="x" * 200,
        ai_service=_ai(payload),
        recalled_memories=[],
        config=_config(categories=["preference"]),
    )
    assert reason == "ok"
    assert len(items) == 1
    assert items[0].category == "preference"


@pytest.mark.asyncio
async def test_max_candidates_per_turn_caps() -> None:
    payload = json.dumps(
        {
            "candidates": [
                {"category": "preference", "content": f"Pref {i}.", "confidence": 0.9 - i * 0.01} for i in range(5)
            ]
        }
    )
    items, _reason = await extract_candidates(
        assistant_text="x" * 200,
        ai_service=_ai(payload),
        recalled_memories=[],
        config=_config(max_candidates_per_turn=2),
    )
    assert len(items) == 2


@pytest.mark.asyncio
async def test_sorted_by_confidence_desc() -> None:
    payload = json.dumps(
        {
            "candidates": [
                {"category": "preference", "content": "Lower.", "confidence": 0.75},
                {"category": "preference", "content": "Higher.", "confidence": 0.95},
            ]
        }
    )
    items, _reason = await extract_candidates(
        assistant_text="x" * 200,
        ai_service=_ai(payload),
        recalled_memories=[],
        config=_config(max_candidates_per_turn=2),
    )
    assert items[0].content == "Higher."
    assert items[1].content == "Lower."


@pytest.mark.asyncio
async def test_recalled_memory_dedupe() -> None:
    payload = json.dumps(
        {
            "candidates": [
                # Near-paraphrase of the recalled memory below.
                {
                    "category": "preference",
                    "content": "User prefers dark mode in their IDE.",
                    "confidence": 0.95,
                }
            ]
        }
    )
    recalled = [_memory("user prefers dark mode in IDE")]
    items, reason = await extract_candidates(
        assistant_text="x" * 200,
        ai_service=_ai(payload),
        recalled_memories=recalled,
        config=_config(),
    )
    assert items == []
    assert reason == "no_results"


@pytest.mark.asyncio
async def test_explicit_scope_honored() -> None:
    payload = json.dumps(
        {
            "candidates": [
                {
                    "category": "project_fact",
                    "content": "Service mesh uses linkerd.",
                    "confidence": 0.95,
                    "scope": "project",
                }
            ]
        }
    )
    items, _reason = await extract_candidates(
        assistant_text="x" * 200,
        ai_service=_ai(payload),
        recalled_memories=[],
        config=_config(),
    )
    assert items[0].scope == "project"


@pytest.mark.asyncio
async def test_invalid_scope_falls_back_to_user() -> None:
    payload = json.dumps(
        {
            "candidates": [
                {
                    "category": "preference",
                    "content": "Pref.",
                    "confidence": 0.95,
                    "scope": "global",  # not a valid scope
                }
            ]
        }
    )
    items, _reason = await extract_candidates(
        assistant_text="x" * 200,
        ai_service=_ai(payload),
        recalled_memories=[],
        config=_config(),
    )
    assert items[0].scope == "user"


@pytest.mark.asyncio
async def test_strips_markdown_fences() -> None:
    payload = (
        "```json\n"
        + json.dumps({"candidates": [{"category": "preference", "content": "Pref.", "confidence": 0.9}]})
        + "\n```"
    )
    items, reason = await extract_candidates(
        assistant_text="x" * 200,
        ai_service=_ai(payload),
        recalled_memories=[],
        config=_config(),
    )
    assert reason == "ok"
    assert len(items) == 1


@pytest.mark.asyncio
async def test_strips_leading_prose() -> None:
    payload = "Sure! Here you go:\n" + json.dumps(
        {"candidates": [{"category": "preference", "content": "Pref.", "confidence": 0.9}]}
    )
    items, reason = await extract_candidates(
        assistant_text="x" * 200,
        ai_service=_ai(payload),
        recalled_memories=[],
        config=_config(),
    )
    assert reason == "ok"
    assert len(items) == 1


@pytest.mark.asyncio
async def test_non_dict_candidates_skipped() -> None:
    payload = json.dumps(
        {
            "candidates": [
                "not a dict",
                42,
                {"category": "preference", "content": "OK.", "confidence": 0.9},
            ]
        }
    )
    items, _reason = await extract_candidates(
        assistant_text="x" * 200,
        ai_service=_ai(payload),
        recalled_memories=[],
        config=_config(),
    )
    assert len(items) == 1


@pytest.mark.asyncio
async def test_missing_content_or_category_skipped() -> None:
    payload = json.dumps(
        {
            "candidates": [
                {"category": "preference", "content": "", "confidence": 0.9},
                {"category": "", "content": "Has content.", "confidence": 0.9},
            ]
        }
    )
    items, reason = await extract_candidates(
        assistant_text="x" * 200,
        ai_service=_ai(payload),
        recalled_memories=[],
        config=_config(),
    )
    assert items == []
    assert reason == "no_results"


@pytest.mark.asyncio
async def test_long_input_truncated_no_crash() -> None:
    payload = json.dumps({"candidates": [{"category": "preference", "content": "Pref.", "confidence": 0.9}]})
    items, reason = await extract_candidates(
        assistant_text="x" * 100_000,
        ai_service=_ai(payload),
        recalled_memories=[],
        config=_config(),
    )
    assert reason == "ok"
    assert len(items) == 1


@pytest.mark.asyncio
async def test_unparseable_confidence_skipped() -> None:
    payload = json.dumps(
        {
            "candidates": [
                {"category": "preference", "content": "X.", "confidence": "high"},
                {"category": "preference", "content": "Y.", "confidence": 0.9},
            ]
        }
    )
    items, _reason = await extract_candidates(
        assistant_text="x" * 200,
        ai_service=_ai(payload),
        recalled_memories=[],
        config=_config(),
    )
    assert len(items) == 1
    assert items[0].content == "Y."


def test_extracted_candidate_is_frozen() -> None:
    c = ExtractedCandidate(content="x", category="preference", confidence=0.9, scope="user")
    with pytest.raises(Exception):
        c.content = "y"  # type: ignore[misc]
