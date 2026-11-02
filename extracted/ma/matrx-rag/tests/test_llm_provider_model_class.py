"""The grounding judge's chosen model CLASS reaches the injected llm_provider.

A model's class (its serving endpoint, carried as ``offering_id``) is a separate
product a person picks; a judge run on "Qwen · Lightning" must not quietly run
"Qwen · Fast". The seam stays independent: ``offering_id`` is an optional
keyword, passed only to a provider that accepts it, and announced when one
cannot take it.
"""

from __future__ import annotations

import logging
from typing import Any

import matrx_rag.grounding as grounding
import pytest
from matrx_rag._ext import provider_call_kwargs

QWEN = "572667d5-bc84-449c-800e-e89acd36b5f5"
LIGHTNING = "29874e67-5683-40c2-9adb-fb797ea9a176"


class _Provider:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def chat(self, messages, *, model, offering_id=None, **_k: Any) -> str:
        self.calls.append({"model": model, "offering_id": offering_id})
        if _k.get("purpose") == "grounding_judge":
            return '[{"claim_index": 1, "verdict": "supported", "confidence": 0.9}]'
        return '["claim one"]'


class _OldProvider:
    async def chat(self, messages, *, model, offered=None) -> str:  # pre-class seam
        return "[]"


def test_kwargs_carry_the_class_to_a_provider_that_takes_it() -> None:
    assert provider_call_kwargs(_Provider().chat, None, offering_id=LIGHTNING) == {
        "offering_id": LIGHTNING
    }


def test_a_provider_without_the_class_keeps_working_and_is_told(caplog) -> None:
    with caplog.at_level(logging.WARNING):
        assert provider_call_kwargs(_OldProvider().chat, {"a": 1}, offering_id=LIGHTNING) == {
            "offered": {"a": 1}
        }
    assert "cannot ride" in caplog.text


@pytest.mark.asyncio
async def test_verify_grounded_runs_the_judges_class(monkeypatch) -> None:
    provider = _Provider()

    async def _reported(requested: str | None, fallback: str) -> str:
        return requested or fallback

    monkeypatch.setattr(grounding, "get_llm_provider", lambda: provider)
    monkeypatch.setattr(grounding, "_reported_model", _reported)
    await grounding.verify_grounded(
        answer="Claim one.",
        retrieved=[{"chunk_id": "c1", "content_text": "Claim one."}],
        judge_model=QWEN,
        judge_offering_id=LIGHTNING,
    )
    assert len(provider.calls) == 2
    assert all(call == {"model": QWEN, "offering_id": LIGHTNING} for call in provider.calls)


@pytest.mark.asyncio
async def test_a_class_without_a_judge_model_is_dropped(monkeypatch) -> None:
    provider = _Provider()

    async def _reported(requested: str | None, fallback: str) -> str:
        return requested or fallback

    monkeypatch.setattr(grounding, "get_llm_provider", lambda: provider)
    monkeypatch.setattr(grounding, "_reported_model", _reported)
    await grounding.verify_grounded(
        answer="Claim one.",
        retrieved=[{"chunk_id": "c1", "content_text": "Claim one."}],
        judge_offering_id=LIGHTNING,
    )
    assert all(call["offering_id"] is None for call in provider.calls)
