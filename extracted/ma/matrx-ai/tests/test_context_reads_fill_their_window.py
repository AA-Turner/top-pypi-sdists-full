"""A context read delivers the window it advertises — never a resolver's smaller one.

PB-04 (2026-10-01, conversation 39dc45a9…): a 33,890-char attached text came back
from a ``context`` batch as 24,000 chars with ``has_more`` while the same result
said it could carry 34,767 — aidream's processed-document resolver caps one slice
at 24,000 and the tool took that slice as the whole window. The agent never read
on, and the insured name in the last paragraph was reported missing (W-36).

These tests use a resolver that caps each slice at 24,000, like the real one.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from matrx_ai.tools.implementations import ctx as ctx_mod

from test_context_self_cap import _call, _inline

BUDGET = ctx_mod._MAX_RESULT_CHARS
RESOLVER_CAP = 24_000
TAIL_FACT = "Larchmont Tower Owners Association of Oakland"


def _rules_text(total: int) -> str:
    body = "Section 1. Movers must sign in at the front desk. " * (total // 50)
    tail = f" The additional insured is {TAIL_FACT}."
    return (body[: total - len(tail)] + tail)[:total]


def _capped_lazy(key: str, body: str, calls: list[dict[str, Any]]):
    obj = SimpleNamespace(
        key=key,
        type=SimpleNamespace(value="json"),
        label="larchmont-tower-move-in-rules.txt",
        summary_agent_id=None,
        descriptor=None,
        source=SimpleNamespace(kind="file", id="ec92460c"),
        is_lazy_source=lambda: True,
        content_as_str=lambda: "",
    )

    async def materialize(source: Any, *, mode: str, offset: int, chars: int | None, user_id: str):
        calls.append({"mode": mode, "offset": offset, "chars": chars})
        window = min(chars or RESOLVER_CAP, RESOLVER_CAP)
        end = min(len(body), offset + window)
        return SimpleNamespace(
            representation="raw",
            text=body[offset:end],
            offset=offset,
            total_chars=len(body),
            has_more=end < len(body),
            next_offset=end if end < len(body) else None,
            page_range=None,
        )

    return obj, materialize


async def test_a_text_under_the_budget_is_delivered_whole_through_a_capped_resolver() -> None:
    body = _rules_text(33_890)
    calls: list[dict[str, Any]] = []
    obj, mat = _capped_lazy("resource_file_ec92460c", body, calls)
    r = await _call([obj], {"action": "get", "key": obj.key, "mode": "full"}, materialize_context_source=mat)
    out = r.output
    assert out.content == body, f"got {out.chars_returned:,} of {len(body):,} chars"
    assert TAIL_FACT in out.content
    assert out.has_more is False and out.fell_back_from is None and out.note is None


async def test_in_a_batch_the_text_fits_what_is_left_and_arrives_whole() -> None:
    # The PB-04 shape: an earlier batch entry used ~5K, leaving 34,767-ish.
    body = _rules_text(33_890)
    calls: list[dict[str, Any]] = []
    obj, mat = _capped_lazy("resource_file_ec92460c", body, calls)
    pdf = _inline("resource_file_b9eb9293", "Move 4472 customs packet. " * 190)
    r = await _call(
        [pdf, obj],
        {"action": "batch", "requests": [{"key": pdf.key, "mode": "full"}, {"key": obj.key, "mode": "full"}]},
        materialize_context_source=mat,
    )
    entry = r.output.results[1].output
    assert entry["content"] == body and entry["has_more"] is False
    assert r.output.note is None


async def test_a_text_over_the_budget_fills_the_budget_and_the_next_read_is_unmissable() -> None:
    body = _rules_text(100_000)
    calls: list[dict[str, Any]] = []
    obj, mat = _capped_lazy("resource_file_big", body, calls)
    r = await _call([obj], {"action": "get", "key": obj.key, "mode": "full"}, materialize_context_source=mat)
    out = r.output
    # The capacity the note states and the page delivered agree.
    assert out.chars_returned == BUDGET and out.next_offset == BUDGET and out.has_more is True
    assert "PARTIAL READ" in out.note and f"offset={BUDGET}" in out.note
    assert f"chars={BUDGET}" in out.note  # a concrete size, not "<up to N>"
    assert "Nothing was dropped" not in out.note


async def test_an_explicit_page_gets_the_chars_it_asked_for() -> None:
    body = _rules_text(80_000)
    calls: list[dict[str, Any]] = []
    obj, mat = _capped_lazy("resource_file_big", body, calls)
    r = await _call(
        [obj],
        {"action": "get", "key": obj.key, "mode": "page", "offset": 1_000, "chars": 30_000},
        materialize_context_source=mat,
    )
    assert r.output.content == body[1_000:31_000]
    assert r.output.next_offset == 31_000


async def test_a_batch_names_every_partial_read_at_the_top() -> None:
    body = _rules_text(60_000)
    calls: list[dict[str, Any]] = []
    obj, mat = _capped_lazy("resource_file_long", body, calls)
    r = await _call([obj], {"action": "batch", "requests": [{"key": obj.key, "mode": "full"}]}, materialize_context_source=mat)
    assert r.output.results[0].output["has_more"] is True
    assert r.output.note and "PARTIAL READS" in r.output.note
    assert "resource_file_long" in r.output.note and f"offset={BUDGET}" in r.output.note


async def test_the_fill_never_stitches_two_versions_of_a_body() -> None:
    # Review 2026-10-01: clean text finishing between slices of a raw read.
    raw, clean = _rules_text(60_000), _rules_text(50_000).upper()
    obj, _ = _capped_lazy("resource_file_flip", raw, [])
    seen: list[int] = []

    async def materialize(source, *, mode, offset, chars, user_id):
        seen.append(offset)
        body, rep = (raw, "raw") if offset == 0 else (clean, "clean")
        end = min(len(body), offset + min(chars or RESOLVER_CAP, RESOLVER_CAP))
        return SimpleNamespace(representation=rep, text=body[offset:end], offset=offset,
                               total_chars=len(body), has_more=end < len(body),
                               next_offset=end if end < len(body) else None, page_range=None)

    r = await _call([obj], {"action": "get", "key": obj.key, "mode": "full"}, materialize_context_source=materialize)
    assert r.output.content == raw[:RESOLVER_CAP] and r.output.next_offset == RESOLVER_CAP
    assert "PARTIAL READ" in r.output.note


async def test_a_failed_follow_up_slice_keeps_what_was_read() -> None:
    body = _rules_text(33_890)
    obj, _ = _capped_lazy("resource_file_flaky", body, [])

    async def materialize(source, *, mode, offset, chars, user_id):
        if offset:
            raise RuntimeError("connection reset")
        return SimpleNamespace(representation="raw", text=body[:RESOLVER_CAP], offset=0,
                               total_chars=len(body), has_more=True, next_offset=RESOLVER_CAP,
                               page_range=None)

    r = await _call([obj], {"action": "get", "key": obj.key, "mode": "full"}, materialize_context_source=materialize)
    assert r.success and r.output.content == body[:RESOLVER_CAP]
    assert f"offset={RESOLVER_CAP}" in r.output.note


async def test_a_page_the_agent_chose_is_not_flagged_as_a_partial_read() -> None:
    body = _rules_text(60_000)
    obj, mat = _capped_lazy("resource_file_paged", body, [])
    r = await _call([obj], {"action": "batch", "requests": [{"key": obj.key, "mode": "page", "chars": 4_000}]},
                    materialize_context_source=mat)
    assert r.output.results[0].output["has_more"] is True
    assert r.output.note is None
