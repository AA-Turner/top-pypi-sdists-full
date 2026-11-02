"""A judge answer cut off by the output cap is "couldn't check", never "unsupported"."""

from __future__ import annotations

import json
from typing import Any

import matrx_rag.grounding as grounding
import pytest

PASSAGES = [{"chunk_id": "c1", "content_text": "passage"}]


def _items(indices: list[int]) -> list[dict[str, Any]]:
    return [
        {"claim_index": i, "verdict": "supported", "confidence": 0.9,
         "supporting_chunk_ids": ["c1"], "reasoning": "ok"}
        for i in indices
    ]


class _Provider:
    """Judge whose FIRST (whole-list) call is cut off after `first_ok` items."""

    def __init__(self, first_ok: int, *, retry_works: bool) -> None:
        self.first_ok = first_ok
        self.retry_works = retry_works
        self.sizes: list[int] = []

    async def chat(self, messages, **kwargs: Any) -> str:
        user = messages[-1]["content"]
        n = sum(1 for line in user.splitlines() if line[:1].isdigit() and ". " in line[:5])
        self.sizes.append(n)
        if len(self.sizes) == 1:
            full = json.dumps(_items(list(range(1, self.first_ok + 1))))
            return full[: -15]  # cut mid-object: invalid JSON
        if not self.retry_works:
            return '[{"claim_index": 1, "verd'
        return json.dumps(_items(list(range(1, n + 1))))


def _claims(n: int) -> list[str]:
    return [f"claim number {i}" for i in range(n)]


async def test_cut_off_answer_is_retried_in_batches(monkeypatch):
    p = _Provider(first_ok=3, retry_works=True)
    monkeypatch.setattr(grounding, "get_llm_provider", lambda: p)
    out = await grounding.judge_claims(_claims(20), PASSAGES)
    assert [v.verdict for v in out].count("unsupported") == 0
    assert all(v.verdict == "supported" for v in out)
    assert len(p.sizes) > 1  # a retry really happened
    # The first pass finished 2 verdicts before the cut, so no retry carries more.
    assert max(p.sizes[1:]) <= 2


def test_retry_batch_size_is_what_the_first_pass_fit():
    assert grounding._retry_batch_size(20, 18) == 2
    assert grounding._retry_batch_size(10, 10) == 5
    assert grounding._retry_batch_size(1, 1) == 1


async def test_still_cut_off_is_unchecked_never_unsupported(monkeypatch):
    p = _Provider(first_ok=3, retry_works=False)
    monkeypatch.setattr(grounding, "get_llm_provider", lambda: p)
    out = await grounding.judge_claims(_claims(10), PASSAGES)
    assert [v.verdict for v in out[:2]] == ["supported", "supported"]
    unjudged = out[2:]
    assert unjudged and all(v.verdict == "unchecked" for v in unjudged)
    assert not any(v.verdict == "unsupported" for v in out)


async def test_report_counts_unchecked_and_scores_only_checked(monkeypatch):
    p = _Provider(first_ok=3, retry_works=False)
    monkeypatch.setattr(grounding, "get_llm_provider", lambda: p)

    async def _claims_stub(*a, **k):
        return _claims(10)

    monkeypatch.setattr(grounding, "extract_claims", _claims_stub)
    report = await grounding.verify_grounded(answer="x", retrieved=PASSAGES)
    assert report.unchecked_claims > 0
    assert report.error is None
    assert report.overall_faithfulness == pytest.approx(0.9)


async def test_nothing_judged_reports_an_error_not_a_zero_score(monkeypatch):
    class _Garbage:
        async def chat(self, messages, **kwargs):
            return "I cannot"

    monkeypatch.setattr(grounding, "get_llm_provider", lambda: _Garbage())

    async def _claims_stub(*a, **k):
        return _claims(3)

    monkeypatch.setattr(grounding, "extract_claims", _claims_stub)
    report = await grounding.verify_grounded(answer="x", retrieved=PASSAGES)
    assert report.error
    assert all(v.verdict == "unchecked" for v in report.claims)
