"""Forcing-function tests for the tool-result content gate.

Green here only when the real mechanism works. The three fixtures are REAL
oversized tool results pulled from ``chat.tool_call`` on 2026-09-20 (project
brsgrqvjdzwihsvnfqkf) — a ``data`` catalog, a ``read_page`` accessibility dump
and a ``research_web`` report — not shapes invented to match the sectioner.

What each test would catch if the code regressed:
  * knobs — a cap read from this file's constants instead of the org's row, and
    a reader whose failure silently applies a number no admin can see.
  * sectioner — a JSON item cut in half, which is the fabrication risk at this
    seam: a judge answers fluently on half a record and the gate drops the half
    that mattered.
  * holder absent — a positional cut that does NOT say it was positional, i.e.
    the gate failing silently.
  * stubbed holder — a threshold that does not actually decide, an order that
    does not survive, and a withheld note that does not name what is missing.
"""

from __future__ import annotations

import json
import pathlib

import pytest

from matrx_ai.tools import result_gate as rg
from matrx_ai.tools.result_gate import GateContext, apply_size_gate_async
from matrx_ai.tools.result_gate_limits import (
    ResultGateLimits,
    limits_from_values,
    load_result_gate_limits,
)
from matrx_ai.tools.sections import section_result

FIXTURES = pathlib.Path(__file__).parent / "fixtures" / "oversized_tool_results"
REAL_SHAPES = ("data", "read_page", "research_web")


def _fixture(name: str) -> str:
    return (FIXTURES / f"{name}.txt").read_text(encoding="utf-8")


def _content_dict(content: str, call_id: str = "call-gate-1") -> dict:
    return {
        "tool_use_id": call_id,
        "call_id": call_id,
        "name": "data",
        "content": content,
        "is_error": False,
        "output_chars": len(content),
        "output_preview": {},
    }


def _need() -> GateContext:
    return GateContext(
        user_question="Which of these resources can store a transcript?",
        organization_id="org-1",
    )


@pytest.fixture(autouse=True)
def _clean_ext():
    """Every test owns the injected seams; none leaks into the next."""
    from matrx_ai import _ext

    saved = dict(_ext._registry)
    yield
    _ext._registry.clear()
    _ext._registry.update(saved)


def _inject(**hooks) -> None:
    from matrx_ai import _ext

    _ext.configure_ext(**hooks)


# ---------------------------------------------------------------------------
# 1. The caps are the ORG's rows, not this file's constants
# ---------------------------------------------------------------------------


def test_every_knob_key_has_a_field_and_vice_versa():
    """A key the migration seeds that no field reads is a knob governing nothing."""
    from matrx_ai.tools.result_gate_limits import RESULT_GATE_KNOB_KEYS

    fields = {f for f in ResultGateLimits.__dataclass_fields__ if f != "source"}
    assert set(RESULT_GATE_KNOB_KEYS) == fields


@pytest.mark.asyncio
async def test_limits_come_from_the_injected_reader():
    seen: dict = {}

    async def reader(*, organization_id=None, user_id=None):
        seen["org"] = organization_id
        seen["user"] = user_id
        return {"soft_cap_chars": 1234, "section_relevance_threshold": 0.9}

    _inject(result_gate_limits_reader=reader)
    limits = await load_result_gate_limits("org-7", "user-7")
    assert (seen["org"], seen["user"]) == ("org-7", "user-7")
    assert limits.soft_cap_chars == 1234
    assert limits.section_relevance_threshold == 0.9
    assert limits.source == "knobs"
    # A key the door did not answer keeps the declared default, never zero.
    assert limits.canary_chars == ResultGateLimits().canary_chars


@pytest.mark.asyncio
async def test_no_reader_means_package_defaults_and_says_so():
    limits = await load_result_gate_limits("org-7", "user-7")
    assert limits == ResultGateLimits()
    assert limits.source == "package_defaults"


@pytest.mark.asyncio
async def test_a_failing_reader_degrades_to_defaults_never_to_zero():
    async def reader(*, organization_id=None, user_id=None):
        raise RuntimeError("settings unavailable")

    _inject(result_gate_limits_reader=reader)
    limits = await load_result_gate_limits("org-7", "user-7")
    assert limits == ResultGateLimits()


def test_unreadable_knob_values_keep_the_default():
    limits = limits_from_values({"soft_cap_chars": "not a number", "canary_chars": None})
    assert limits.soft_cap_chars == ResultGateLimits().soft_cap_chars
    assert limits.canary_chars == ResultGateLimits().canary_chars


@pytest.mark.asyncio
async def test_the_org_soft_cap_actually_governs_the_cut():
    """The point of a knob: turning it changes what the agent sees."""

    async def reader(*, organization_id=None, user_id=None):
        return {"soft_cap_chars": 5_000}

    _inject(result_gate_limits_reader=reader)
    body = _fixture("research_web")[:20_000]
    out, truncated = await apply_size_gate_async(
        _content_dict(body),
        output_self_capped=False,
        tool_name="research_web",
        tool_kind="native",
        conversation_id="conv-1",
        user_id="user-1",
        gate_context=_need(),
    )
    # 20,000 chars is under the 50,000 CONSTANT and over the 5,000 ROW.
    assert truncated is True
    assert len(out["content"]) < 20_000


# ---------------------------------------------------------------------------
# 2. The sectioner, on the three real shapes
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", REAL_SHAPES)
def test_sections_are_exact_substrings_in_order(name):
    text = _fixture(name)
    result = section_result(text)
    assert len(result.sections) >= 2
    last_end = -1
    for section in result.sections:
        assert section.text == text[section.start : section.end]
        assert section.chars == section.end - section.start
        assert section.start > last_end
        last_end = section.start
        assert section.section_source in (
            "json_item",
            "heading",
            "paragraph_block",
            "fixed_window",
        )


def test_real_shapes_are_recognised_for_what_they_are():
    assert section_result(_fixture("data")).result_format == "json"
    assert section_result(_fixture("read_page")).result_format == "json"
    assert section_result(_fixture("research_web")).result_format == "markdown"


@pytest.mark.parametrize("name", ["data", "read_page"])
def test_a_json_item_is_never_split_in_half(name):
    """THE invariant. A section that holds array items must parse as items.

    Wrapping a section in brackets and parsing it is the mechanical check: half
    of one record glued to half of the next cannot survive it.
    """
    text = _fixture(name)
    result = section_result(text)
    item_sections = [s for s in result.sections if s.heading and "[" in s.heading]
    assert item_sections, f"{name} produced no array-item sections"
    for section in item_sections:
        json.loads("[" + section.text + "]")


@pytest.mark.parametrize("name", ["data", "read_page"])
def test_json_never_falls_back_to_a_fixed_window(name):
    """A fixed window through JSON is the mis-cut this sectioner exists to stop."""
    result = section_result(_fixture(name))
    assert {s.section_source for s in result.sections} == {"json_item"}


def test_the_section_cap_groups_and_never_splits():
    text = _fixture("read_page")
    capped = section_result(text, max_sections=10)
    assert len(capped.sections) <= 10
    for section in capped.sections:
        assert section.text == text[section.start : section.end]
    # Grouping is announced, not silent.
    assert any("more)" in (s.heading or "") for s in capped.sections)


def test_prose_with_no_structure_falls_back_to_fixed_windows_and_says_so():
    result = section_result("z" * 12_000, target_section_chars=4_000)
    assert [s.section_source for s in result.sections] == ["fixed_window"] * 3


# ---------------------------------------------------------------------------
# 3. No Holder bound → today's positional cut, and it SAYS it was positional
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_holder_absent_keeps_the_positional_cut_and_names_the_mandate():
    body = _fixture("research_web")
    out, truncated = await apply_size_gate_async(
        _content_dict(body),
        output_self_capped=False,
        tool_name="research_web",
        tool_kind="native",
        conversation_id="conv-1",
        user_id="user-1",
        gate_context=_need(),
    )
    assert truncated is True
    content = out["content"]
    assert content.startswith(body[:1_000])  # positional: the HEAD was kept
    assert "by POSITION" in content
    assert rg.SECTION_RELEVANCE_MANDATE_KEY in content
    assert "fetch_tool_result" in content


@pytest.mark.asyncio
async def test_nothing_states_the_need_so_relevance_is_not_even_asked():
    called: list = []

    async def decider(provisions):
        called.append(provisions)
        return [{"section_index": 0, "relevant": 1.0}]

    _inject(section_relevance_decider=decider)
    out, truncated = await apply_size_gate_async(
        _content_dict(_fixture("data")),
        output_self_capped=False,
        tool_name="data",
        tool_kind="native",
        conversation_id="conv-1",
        user_id="user-1",
        gate_context=GateContext(),  # no question, no turn, no goal
    )
    assert called == []
    assert truncated is True
    assert "by POSITION" in out["content"]


# ---------------------------------------------------------------------------
# 4. A stubbed Holder: the threshold decides, order survives, the note is honest
# ---------------------------------------------------------------------------


def _threshold_decider(scores: dict[int, float], *, boilerplate: set[int] = frozenset()):
    async def decider(provisions):
        return [
            {
                "section_index": p["section_index"],
                "relevant": scores.get(p["section_index"], 0.0),
                "is_boilerplate": p["section_index"] in boilerplate,
                "density": 3,
            }
            for p in provisions
        ]

    return decider


@pytest.mark.asyncio
async def test_a_stubbed_holder_keeps_by_threshold_and_preserves_order():
    text = _fixture("data")
    sections = section_result(text).sections
    keep = {0, 3, 7}
    scores = {s.index: (0.95 if s.index in keep else 0.1) for s in sections}
    _inject(section_relevance_decider=_threshold_decider(scores))

    out, truncated = await apply_size_gate_async(
        _content_dict(text),
        output_self_capped=False,
        tool_name="data",
        tool_kind="native",
        conversation_id="conv-1",
        user_id="user-1",
        gate_context=_need(),
    )
    assert truncated is True
    content = out["content"]
    body = content.split("\n\n[⚠️ TOOL RESULT FILTERED")[0]
    expected = "".join(s.text for s in sections if s.index in keep)
    assert body == expected  # exact text, original order, nothing rewritten
    assert len(body) < len(text)
    assert out["output_chars"] == len(content)
    assert out["output_preview"]["content_gated"] is True
    assert out["output_preview"]["true_output_chars"] == len(text)


@pytest.mark.asyncio
async def test_the_threshold_is_the_org_row_not_a_constant():
    text = _fixture("data")
    sections = section_result(text).sections
    scores = {s.index: (0.5 if s.index == 0 else 0.0) for s in sections}

    async def reader(*, organization_id=None, user_id=None):
        return {"section_relevance_threshold": 0.4}

    _inject(
        section_relevance_decider=_threshold_decider(scores),
        result_gate_limits_reader=reader,
    )
    out, _ = await apply_size_gate_async(
        _content_dict(text),
        output_self_capped=False,
        tool_name="data",
        tool_kind="native",
        conversation_id="conv-1",
        user_id="user-1",
        gate_context=_need(),
    )
    # 0.5 clears a 0.4 bar and would have failed the 0.6 default.
    assert out["content"].startswith(sections[0].text)
    assert "TOOL RESULT FILTERED" in out["content"]


@pytest.mark.asyncio
async def test_the_withheld_note_names_count_sources_and_the_way_back():
    text = _fixture("read_page")
    sections = section_result(text).sections
    scores = {s.index: (1.0 if s.index < 3 else 0.0) for s in sections}
    _inject(section_relevance_decider=_threshold_decider(scores))

    out, _ = await apply_size_gate_async(
        _content_dict(text, call_id="call-note-1"),
        output_self_capped=False,
        tool_name="read_page",
        tool_kind="external",
        conversation_id="conv-1",
        user_id="user-1",
        gate_context=_need(),
    )
    note = out["content"].split("[⚠️ TOOL RESULT FILTERED")[1]
    withheld = len(sections) - 3
    assert f"{withheld:,} of the result's sections" in note
    assert "by json_item" in note  # the source is NAMED, not implied
    assert 'call_id="call-note-1"' in note
    assert "fetch_tool_result" in note
    assert "NOTHING WAS DELETED" in note
    assert f"#{sections[3].index}" in note  # the first withheld one, by index


@pytest.mark.asyncio
async def test_boilerplate_is_withheld_even_when_scored_relevant():
    text = _fixture("read_page")
    sections = section_result(text).sections
    scores = {s.index: 1.0 for s in sections}
    _inject(
        section_relevance_decider=_threshold_decider(scores, boilerplate={1, 2})
    )
    out, _ = await apply_size_gate_async(
        _content_dict(text),
        output_self_capped=False,
        tool_name="read_page",
        tool_kind="external",
        conversation_id="conv-1",
        user_id="user-1",
        gate_context=_need(),
    )
    assert sections[1].text not in out["content"]
    assert sections[0].text in out["content"]


@pytest.mark.asyncio
async def test_a_section_nobody_judged_is_kept_never_withheld_on_silence():
    text = _fixture("data")
    sections = section_result(text).sections

    async def decider(provisions):
        # Answers for section 0 only. Every other section goes unjudged.
        return [{"section_index": 0, "relevant": 0.0}]

    _inject(section_relevance_decider=decider)
    out, _ = await apply_size_gate_async(
        _content_dict(text),
        output_self_capped=False,
        tool_name="data",
        tool_kind="native",
        conversation_id="conv-1",
        user_id="user-1",
        gate_context=_need(),
    )
    assert sections[0].text not in out["content"]
    for section in sections[1:]:
        assert section.text in out["content"]


@pytest.mark.asyncio
async def test_an_unreadable_probability_keeps_the_section():
    text = _fixture("data")
    sections = section_result(text).sections

    async def decider(provisions):
        return [
            {"section_index": p["section_index"], "relevant": "probably not"}
            for p in provisions
        ]

    _inject(section_relevance_decider=decider)
    out, truncated = await apply_size_gate_async(
        _content_dict(text),
        output_self_capped=False,
        tool_name="data",
        tool_kind="native",
        conversation_id="conv-1",
        user_id="user-1",
        gate_context=_need(),
    )
    # Nothing was withheld, so the gate falls back rather than claim a saving.
    assert truncated is True
    assert "by POSITION" in out["content"]
    assert sections[0].text[:200] in out["content"]


@pytest.mark.asyncio
async def test_a_verdict_that_would_empty_the_result_falls_back():
    text = _fixture("data")
    sections = section_result(text).sections
    _inject(section_relevance_decider=_threshold_decider({s.index: 0.0 for s in sections}))
    out, truncated = await apply_size_gate_async(
        _content_dict(text),
        output_self_capped=False,
        tool_name="data",
        tool_kind="native",
        conversation_id="conv-1",
        user_id="user-1",
        gate_context=_need(),
    )
    assert truncated is True
    assert out["content"].startswith(text[:1_000])
    assert "by POSITION" in out["content"]


@pytest.mark.asyncio
async def test_a_broken_decider_never_costs_the_tool_its_result():
    text = _fixture("data")

    async def decider(provisions):
        raise RuntimeError("holder exploded")

    _inject(section_relevance_decider=decider)
    out, truncated = await apply_size_gate_async(
        _content_dict(text),
        output_self_capped=False,
        tool_name="data",
        tool_kind="native",
        conversation_id="conv-1",
        user_id="user-1",
        gate_context=_need(),
    )
    assert truncated is True
    assert out["content"].startswith(text[:1_000])


# ---------------------------------------------------------------------------
# 5. Every withheld decision is recorded on the row
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_the_verdict_is_recorded_for_both_kinds_of_cut():
    text = _fixture("data")
    sections = section_result(text).sections
    recorded: list[tuple] = []

    _inject(gate_verdict_recorder=lambda c, conv, v: recorded.append((c, conv, v)))

    # (a) nothing bound → a positional verdict naming why.
    await apply_size_gate_async(
        _content_dict(text, call_id="call-pos"),
        output_self_capped=False,
        tool_name="data",
        tool_kind="native",
        conversation_id="conv-1",
        user_id="user-1",
        gate_context=_need(),
    )
    call_id, conversation_id, verdict = recorded[-1]
    assert (call_id, conversation_id) == ("call-pos", "conv-1")
    assert verdict["decided_by"] == "position"
    assert verdict["reason"] == "no_holder_bound"
    assert verdict["mandate_key"] == rg.SECTION_RELEVANCE_MANDATE_KEY

    # (b) a Holder answered → every withheld section is named on the row.
    scores = {s.index: (1.0 if s.index < 2 else 0.0) for s in sections}
    _inject(section_relevance_decider=_threshold_decider(scores))
    await apply_size_gate_async(
        _content_dict(text, call_id="call-rel"),
        output_self_capped=False,
        tool_name="data",
        tool_kind="native",
        conversation_id="conv-1",
        user_id="user-1",
        gate_context=_need(),
    )
    _, _, verdict = recorded[-1]
    assert verdict["decided_by"] == "relevance"
    assert verdict["kept"] == 2
    assert verdict["withheld"] == len(sections) - 2
    assert len(verdict["withheld_sections"]) == len(sections) - 2
    assert {s["section_source"] for s in verdict["withheld_sections"]} == {"json_item"}
    assert verdict["shown_chars"] < verdict["total_chars"]
