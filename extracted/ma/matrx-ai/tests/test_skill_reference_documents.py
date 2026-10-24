"""Skills as reference documents: section-aware reading + skill sets.

Drives the real path: DB-shaped row → ``_row_to_body`` (provider) →
``resolve_skills_for_agent`` → ``render_preamble`` / the ``skill`` tool's ``get``.

* A long reference skill is read as an outline + one section, and ``section=``
  returns exactly that section's text (never the whole 100k-char document).
* A listed long reference skill names its sections on its preamble line, and the
  preamble is byte-identical across runs (prompt caching).
* A skill SET (``skill_type="set"``, ``config.set_members``) attached in any tier
  resolves to its members at run time — included, listed, or forbidden.
"""

from __future__ import annotations

import importlib
from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.skills.models import SkillConfig
from matrx_ai.skills.preamble import render_preamble
from matrx_ai.skills.providers import _row_to_body
from matrx_ai.skills.resolver import resolve_skills_for_agent
from matrx_ai.skills.sections import compact_outline, find_section, parse_sections
from matrx_ai.tools.models import ToolContext

# The package re-exports the ``skill`` function under the module's own name.
skill_tool = importlib.import_module("matrx_ai.tools.implementations.skill")

FILLER = "Detail sentence about the rule and how it applies in practice. " * 40  # ~2.6k


def _doc() -> str:
    return (
        "Read this guide before filing.\n\n"
        "# Tax Guide\n\n"
        "## Filing Status\n\n" + FILLER + "\n\n"
        "### Single\n\n" + FILLER + "\n\n"
        "```python\n# not a heading — inside a fence\n```\n\n"
        "### Married\n\nJoint or separate.\n\n"
        "## Deductions\n\n" + FILLER + "\n\n"
        "### Standard\n\nSTANDARD-DEDUCTION-MARKER the flat amount.\n\n"
        "## Credits\n\nCREDITS-MARKER child credit.\n\n"
        "## Deductions\n\nA second heading with the same text.\n"
    )


def _row(skill_id: str, *, body: str = "# Short\n\nbody", skill_type: str = "reference", config=None):
    return SimpleNamespace(
        id=uuid4(),
        skill_id=skill_id,
        label=skill_id.replace("-", " ").title(),
        description=f"What {skill_id} covers.",
        skill_type=skill_type,
        body=body,
        allowed_tools=[],
        trigger_patterns=[],
        disable_auto_invocation=False,
        version=1,
        config=config or {},
    )


def _set(skill_id: str, members) -> SimpleNamespace:
    return _row(
        skill_id,
        body="",
        skill_type="set",
        config={"set_members": [str(m.id) for m in members]},
    )


class _Provider:
    def __init__(self, rows):
        self._rows = {r.id: r for r in rows}
        self.loads = 0

    async def category_overview(self, *, user_id=None):
        return []

    async def get_by_id(self, skill_uuid, *, user_id=None):
        self.loads += 1
        row = self._rows.get(skill_uuid)
        return _row_to_body(row, []) if row else None


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------


def test_sections_follow_headings_ignore_fences_and_include_children():
    body = _doc()
    sections = parse_sections(body)
    ids = [s.id for s in sections]
    assert ids == [
        "intro",
        "tax-guide",
        "filing-status",
        "single",
        "married",
        "deductions",
        "standard",
        "credits",
        "deductions-1",
    ]
    numbers = {s.id: s.number for s in sections}
    assert numbers["tax-guide"] == "1"
    assert numbers["filing-status"] == "1.1"
    assert numbers["married"] == "1.1.2"
    assert numbers["deductions"] == "1.2"
    # A section spans its subsections and stops at the next same-level heading.
    filing = find_section(sections, "filing-status")
    text = body[filing.start : filing.end]
    assert "### Single" in text and "### Married" in text and "## Deductions" not in text
    # Every handle reaches the same section.
    assert find_section(sections, "1.2.1").id == "standard"
    assert find_section(sections, "deductions/standard").id == "standard"
    assert find_section(sections, "Credits").id == "credits"
    assert find_section(sections, "## Credits").id == "credits"
    assert find_section(sections, "nope") is None


def test_compact_outline_skips_a_single_wrapping_title_and_is_stable():
    line = compact_outline(_doc())
    # The lone "# Tax Guide" wrapper is skipped; level-2 + level-3 headings are named.
    assert line.startswith("1.1 Filing Status (")
    assert "1.1.1 Single" in line and "1.2 Deductions" in line and "Tax Guide" not in line
    assert compact_outline(_doc()) == line
    assert compact_outline("# Only one heading\n\ntext") == ""


# ---------------------------------------------------------------------------
# skill get
# ---------------------------------------------------------------------------


@pytest.fixture
def wired(monkeypatch):
    def install(rows, config=None):
        provider = _Provider(rows)

        async def _p():
            return provider

        monkeypatch.setattr(skill_tool, "_provider", _p)
        monkeypatch.setattr(skill_tool, "_user_id_from_ctx", lambda ctx: None)
        monkeypatch.setattr(skill_tool, "_agent_skill_config", lambda ctx: config)
        return provider

    return install


def _ctx() -> ToolContext:
    return ToolContext(call_id="c1", tool_name="skill")


async def _get(**args):
    result = await skill_tool.skill({"action": "get", **args}, _ctx())
    assert result.success, result.error
    return result.output


@pytest.mark.asyncio
async def test_long_document_reads_as_outline_plus_first_section(wired):
    doc = _row("tax-guide", body=_doc())
    wired([doc])
    out = await _get(skill_id=str(doc.id))
    assert out["mode"] == "outline"
    assert out["__kind"] == "skill_tool_result"  # the result still fits its declared kind
    assert [r["id"] for r in out["outline"]][:3] == ["intro", "tax-guide", "filing-status"]
    assert out["section"]["id"] == "intro"
    assert out["body"].startswith("Read this guide before filing.")
    assert out["next_section_id"] == "tax-guide"
    assert out["total_chars"] == len(_doc())


@pytest.mark.asyncio
async def test_section_argument_returns_exactly_that_section(wired):
    doc = _row("tax-guide", body=_doc())
    wired([doc])
    result = await skill_tool.skill(
        {"action": "get", "skill_id": str(doc.id), "section": "1.2.1"}, _ctx()
    )
    assert result.success
    assert result.output_kind == "skill_tool_result"
    out = result.output
    from matrx_ai.tools.kinds.workbench import SkillToolResult

    assert SkillToolResult.model_validate(out).model_dump(mode="json") == out
    assert out["mode"] == "section"
    assert out["section"]["id"] == "standard"
    assert out["body"] == "### Standard\n\nSTANDARD-DEDUCTION-MARKER the flat amount.\n\n"
    assert out["next_section_id"] == "credits"
    assert "CREDITS-MARKER" not in out["body"]


@pytest.mark.asyncio
async def test_set_skill_result_uses_the_registered_wire_contract(wired):
    member = _row("skill-member", body="A complete method.", skill_type="procedure")
    skill_set = _set("research-set", [member])
    wired([skill_set, member])

    result = await skill_tool.skill(
        {"action": "get", "skill_id": str(skill_set.id)}, _ctx()
    )

    assert result.success
    assert result.output_kind == "skill_tool_result"
    assert result.output["__kind"] == "skill_tool_result"
    from matrx_ai.tools.kinds.workbench import SkillToolResult

    assert SkillToolResult.model_validate(result.output).model_dump(mode="json") == result.output
    assert result.output["mode"] == "set"
    assert result.output["count"] == 1
    assert result.output["members"][0]["skill_id"] == "skill-member"


@pytest.mark.asyncio
async def test_missing_section_refusal_stays_on_error_channel_without_a_kind(wired):
    doc = _row("tax-guide", body=_doc())
    wired([doc])

    result = await skill_tool.skill(
        {"action": "get", "skill_id": str(doc.id), "section": "not-a-section"}, _ctx()
    )

    assert not result.success
    assert result.error is not None and result.error.error_type == "not_found"
    assert result.output is None
    assert result.output_kind is None


@pytest.mark.asyncio
async def test_a_huge_section_is_paged(wired):
    doc = _row("tax-guide", body=_doc())
    wired([doc])
    first = await _get(skill_id=str(doc.id), section="filing-status", chars=1000)
    assert first["has_more"] is True and len(first["body"]) == 1000
    second = await _get(
        skill_id=str(doc.id), section="filing-status", chars=1000, offset=first["next_offset"]
    )
    assert second["offset"] == 1000 and second["body"] != first["body"]


@pytest.mark.asyncio
async def test_unknown_section_says_which_exist(wired):
    doc = _row("tax-guide", body=_doc())
    wired([doc])
    result = await skill_tool.skill(
        {"action": "get", "skill_id": str(doc.id), "section": "estate tax"}, _ctx()
    )
    assert not result.success
    assert result.error.error_type == "not_found"
    assert "1.2.1 standard" in result.error.suggested_action


@pytest.mark.asyncio
async def test_short_skill_and_explicit_full_still_return_the_whole_body(wired):
    short = _row("short-one")
    doc = _row("tax-guide", body=_doc())
    wired([short, doc])
    assert (await _get(skill_id=str(short.id)))["mode"] == "full"
    full = await _get(skill_id=str(doc.id), mode="full")
    assert full["mode"] == "full" and full["body"] == _doc()


@pytest.mark.asyncio
async def test_get_on_a_set_lists_its_readable_unforbidden_members(wired):
    a, b, hidden = _row("doc-a"), _row("doc-b"), _row("doc-hidden")
    s = _set("tax-library", [a, b, hidden])
    wired([a, b, hidden, s], config=SkillConfig(forbidden=[hidden.id]))
    out = await _get(skill_id=str(s.id))
    assert out["mode"] == "set"
    assert [m["skill_id"] for m in out["members"]] == ["doc-a", "doc-b"]


# ---------------------------------------------------------------------------
# Resolver: sets + listed outlines
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_a_set_resolves_to_its_members_in_every_tier():
    a, b, c, d = _row("doc-a"), _row("doc-b"), _row("doc-c"), _row("doc-d")
    inner = _set("inner", [c])
    outer = _set("outer", [a, inner, b])
    # A loop must not hang or duplicate: outer contains inner, and inner points back at outer.
    inner.config["set_members"].append(str(outer.id))
    forbidden_set = _set("nope", [d])
    provider = _Provider([a, b, c, d, inner, outer, forbidden_set])
    agent = SimpleNamespace(
        skill_config=SkillConfig(
            included=[outer.id], listed=[a.id, d.id], forbidden=[forbidden_set.id]
        )
    )
    resolved = await resolve_skills_for_agent(agent, provider)

    assert [s.skill_id for s in resolved.preamble.included_skills] == ["doc-a", "doc-c", "doc-b"]
    # a is included via the set, so it is not listed again; d is forbidden via its set.
    assert resolved.preamble.listed_skills == []
    assert resolved.config.included == [a.id, c.id, b.id]
    assert resolved.config.is_forbidden(d.id)
    text = render_preamble(resolved.preamble)
    assert "outer" not in text and "inner" not in text  # set rows never reach the prompt


@pytest.mark.asyncio
async def test_adding_a_member_to_the_set_reaches_the_agent_without_touching_it():
    a, b = _row("doc-a"), _row("doc-b")
    s = _set("library", [a])
    provider = _Provider([a, b, s])
    agent = SimpleNamespace(skill_config=SkillConfig(listed=[s.id]))
    before = await resolve_skills_for_agent(agent, provider)
    assert [h.skill_id for h in before.preamble.listed_skills] == ["doc-a"]
    s.config["set_members"].append(str(b.id))
    after = await resolve_skills_for_agent(agent, provider)
    assert [h.skill_id for h in after.preamble.listed_skills] == ["doc-a", "doc-b"]


@pytest.mark.asyncio
async def test_listed_long_reference_names_its_sections_and_stays_byte_stable():
    doc = _row("tax-guide", body=_doc())
    short = _row("short-one")
    provider = _Provider([doc, short])
    agent = SimpleNamespace(skill_config=SkillConfig(listed=[doc.id, short.id]))
    first = render_preamble((await resolve_skills_for_agent(agent, provider)).preamble)
    second = render_preamble((await resolve_skills_for_agent(agent, provider)).preamble)
    assert first == second
    assert f"- tax-guide — What tax-guide covers.\n  sections ({len(_doc()):,} chars; " in first
    assert "1.2.1 Standard" in first
    # A short skill's line is unchanged (no outline).
    assert "- short-one — What short-one covers.\n" in first


# ---------------------------------------------------------------------------
# L8 review rulings: bounded included, reference-only outline, skipped members, knobs
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_non_reference_long_skill_is_read_whole_by_default(wired):
    proc = _row("file-the-return", body=_doc(), skill_type="workflow")
    wired([proc])
    out = await _get(skill_id=str(proc.id))
    assert out["mode"] == "full"
    assert out["body"] == _doc()


@pytest.mark.asyncio
async def test_set_get_counts_members_it_could_not_show(wired):
    a = _row("a-doc")
    gone = _row("deleted-doc")
    s = _set("the-set", [a, gone])
    wired([s, a])  # `gone` is not loadable (deleted / unreadable)
    out = await _get(skill_id=str(s.id))
    assert [m["skill_id"] for m in out["members"]] == ["a-doc"]
    assert out["skipped"] == 1


@pytest.mark.asyncio
async def test_included_overflow_past_the_budget_is_listed_with_one_line_on_turn_one(monkeypatch):
    import matrx_ai.skills.resolver as resolver

    monkeypatch.setattr(resolver, "skill_bodies_budget", lambda: 6000)
    big = _row("big-ref", body=_doc())  # ~15k chars: over the budget
    small = _row("small-ref", body="# Small\n\nsmall body text")
    s = _set("both", [small, big])
    provider = _Provider([s, small, big])
    agent = SimpleNamespace(skill_config=SkillConfig(included=[s.id]))
    resolved = await resolve_skills_for_agent(agent, provider)
    text = render_preamble(resolved.preamble)
    assert [b.skill_id for b in resolved.preamble.included_skills] == ["small-ref"]
    assert "big-ref" in [h.skill_id for h in resolved.preamble.listed_skills]
    big_hint = next(h for h in resolved.preamble.listed_skills if h.skill_id == "big-ref")
    assert big_hint.outline  # the demoted document still names its sections
    assert "<active_skills>" in text and "small body text" in text
    assert "STANDARD-DEDUCTION-MARKER" not in text  # the body is NOT in the prompt
    assert text.count("listed instead of included") == 1
    assert "1 attached skill(s)" in text


@pytest.mark.asyncio
async def test_included_under_the_budget_is_untouched(monkeypatch):
    import matrx_ai.skills.resolver as resolver

    monkeypatch.setattr(resolver, "skill_bodies_budget", lambda: 100_000)
    doc = _row("tax-guide", body=_doc())
    agent = SimpleNamespace(skill_config=SkillConfig(included=[doc.id]))
    resolved = await resolve_skills_for_agent(agent, _Provider([doc]))
    assert [b.skill_id for b in resolved.preamble.included_skills] == ["tax-guide"]
    assert "listed instead of included" not in render_preamble(resolved.preamble)


def test_outline_limits_come_from_the_knob_reader():
    from matrx_ai.skills import knobs

    knobs.configure_skill_knobs(lambda key: {"skill_preamble_outline_entries": 2}.get(key, 4000))
    try:
        line = compact_outline(_doc())
        assert line.count(" · ") <= 2 and "more)" in line
    finally:
        knobs.configure_skill_knobs(None)
