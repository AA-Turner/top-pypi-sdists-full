"""Prompt blocks: ``{{<name>}}`` for a DECLARED block becomes ``<name>\\n{text}\\n</name>`` (R2).

Exact strings only. The resolver runs against an in-memory BlockSource (the host seam)."""

from __future__ import annotations

import asyncio

import pytest

from matrx_ai.agents.definition import Agent
from matrx_ai.config.template_substitution import substitute_authored
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.prompt_blocks import (
    BlockRow,
    ModelFacts,
    PromptBlocksMissing,
    PromptBlocksNotResolved,
    SkillBody,
    VariantRow,
    resolve_declared_blocks,
    set_block_source,
)

CREATOR = "11111111-1111-1111-1111-111111111111"
OTHER = "22222222-2222-2222-2222-222222222222"
ORG = "33333333-3333-3333-3333-333333333333"


def sub(text: str, variables: dict | None = None, blocks: dict | None = None) -> str:
    return substitute_authored(text, text, variables or {}, str, unescape=True, blocks=blocks)


# ── substitution (template_substitution.py) ──────────────────────────────────────────────


def test_declared_block_is_wrapped_in_a_tag_of_its_name() -> None:
    assert sub("Follow:\n{{<research_rules>}}\nGo.", blocks={"research_rules": "Cite sources."}) == (
        "Follow:\n<research_rules>\nCite sources.\n</research_rules>\nGo."
    )


def test_undeclared_block_tag_is_left_exactly_as_written() -> None:
    assert sub("A {{<nope>}} B", blocks={"other": "x"}) == "A {{<nope>}} B"
    assert sub("A {{<nope>}} B") == "A {{<nope>}} B"


def test_escape_turns_into_the_literal_tag() -> None:
    assert sub("{{!<rules>}} {{<rules>}}", blocks={"rules": "R"}) == "{{<rules>}} <rules>\nR\n</rules>"


def test_empty_block_text_becomes_nothing() -> None:
    assert sub("A{{<rules>}}B", blocks={"rules": ""}) == "AB"
    assert sub("A{{<rules>}}B", blocks={"rules": "  \n "}) == "AB"


def test_block_text_is_a_value_never_filled_or_unescaped() -> None:
    out = sub("{{x}} {{<rules>}}", {"x": "1"}, {"rules": "use {{x}} and {{!y}} and {{#x}}s{{/x}}"})
    assert out == "1 <rules>\nuse {{x}} and {{!y}} and {{#x}}s{{/x}}\n</rules>"


def test_block_inside_a_section_follows_the_section() -> None:
    t = "{{#aud}}\n{{<kids_rules>}}\n{{/aud}}\nEnd"
    assert sub(t, {"aud": "kids"}, {"kids_rules": "Be gentle."}) == "<kids_rules>\nBe gentle.\n</kids_rules>\nEnd"
    assert sub(t, {"aud": ""}, {"kids_rules": "Be gentle."}) == "End"


def test_hyphenated_names_and_a_variable_with_the_same_name() -> None:
    assert sub("{{<a-b>}}|{{a-b}}", {"a-b": "V"}, {"a-b": "B"}) == "<a-b>\nB\n</a-b>|V"


def _config(system: str, user: str, blocks: list[str]) -> UnifiedConfig:
    config = UnifiedConfig.from_dict(
        {"model": "claude-opus-5-5", "system_instruction": system,
         "messages": [{"role": "user", "content": user}], "prompt_blocks": blocks}
    )
    return config


def test_system_and_message_text_both_expand() -> None:
    config = _config("S {{<rules>}}", "U {{<rules>}} {{<x>}}", ["rules"])
    config.prompt_block_texts = {"rules": "R"}
    config.replace_variables({})
    assert config.system_instruction.base_instruction == "S <rules>\nR\n</rules>"
    assert config.messages[0].content[0].text == "U <rules>\nR\n</rules> {{<x>}}"


def test_replace_variables_refuses_declared_but_unresolved_blocks() -> None:
    config = _config("S {{<rules>}}", "U", ["rules"])
    with pytest.raises(PromptBlocksNotResolved):
        config.replace_variables({})


def test_declarations_and_report_persist_with_the_conversation() -> None:
    config = _config("S", "U", ["rules"])
    config.prompt_block_report = [{"name": "rules", "level": "system"}]
    config.prompt_block_tool_ids = ["t1"]
    again = UnifiedConfig.from_dict(config.to_dict())
    assert again.prompt_blocks == ["rules"]
    assert again.prompt_block_report == [{"name": "rules", "level": "system"}]
    assert again.prompt_block_tool_ids == ["t1"]
    assert again.prompt_block_texts is None


# ── resolver (ladder, variants, tool binding, skills) ────────────────────────────────────


class FakeSource:
    def __init__(self, rows, skills=None, facts=None, personal_rung=True):
        self.rows = rows
        self.skills = skills or {}
        self.facts = facts
        self.personal_rung = personal_rung
        self.asked_personal: list[str | None] = []

    async def candidates(self, names, *, organization_id, personal_user_id):
        self.asked_personal.append(personal_user_id)
        return [r for r in self.rows if r.name in names and (r.level != "personal" or personal_user_id)]

    async def skill(self, skill_id):
        return self.skills.get(skill_id)

    async def model_facts(self, model):
        return self.facts

    async def personal_rung_enabled(self, organization_id):
        return self.personal_rung


def row(name, level, content, **kw):
    return BlockRow(id=f"{level}-{name}", name=name, level=level, content=content, **kw)


def resolve(config, source, runner=CREATOR):
    return asyncio.run(resolve_declared_blocks(config, runner_id=runner, organization_id=ORG, source=source))


def _declared(*names, creator=CREATOR, tools=None, effort=None):
    config = _config("{{<" + ">}} {{<".join(names) + ">}}", "U", list(names))
    config.prompt_block_creator = creator
    if tools is not None:
        config.tools = tools
    if effort is not None:
        config.reasoning_effort = effort
    return config


LADDER = [row("rules", "system", "SYS"), row("rules", "organization", "ORG"), row("rules", "personal", "ME")]


def test_personal_wins_only_when_the_runner_is_the_creator() -> None:
    config = _declared("rules")
    resolve(config, FakeSource(LADDER))
    assert config.prompt_block_texts == {"rules": "ME"}
    other = _declared("rules")
    resolve(other, FakeSource(LADDER), runner=OTHER)
    assert other.prompt_block_texts == {"rules": "ORG"}


def test_the_personal_rung_knob_off_skips_personal() -> None:
    config = _declared("rules")
    source = FakeSource(LADDER, personal_rung=False)
    resolve(config, source)
    assert config.prompt_block_texts == {"rules": "ORG"}
    assert source.asked_personal == [None]


def test_an_org_overrides_a_system_agents_block() -> None:
    config = _declared("rules", creator="system-agent-creator")
    resolve(config, FakeSource(LADDER))
    assert config.prompt_block_texts == {"rules": "ORG"}
    config.replace_variables({})
    assert config.system_instruction.base_instruction == "<rules>\nORG\n</rules>"
    assert config.prompt_block_report[0]["level"] == "organization"


def test_system_is_the_last_rung() -> None:
    config = _declared("rules")
    resolve(config, FakeSource([row("rules", "system", "SYS")]))
    assert config.prompt_block_texts == {"rules": "SYS"}


def test_a_missing_declared_block_refuses_the_run_naming_it() -> None:
    config = _declared("rules", "gone")
    with pytest.raises(PromptBlocksMissing) as err:
        resolve(config, FakeSource(LADDER))
    assert err.value.names == ["gone"]
    assert err.value.error_info.error_type == "prompt_block_missing"
    assert err.value.error_info.status_code == 422
    assert config.prompt_block_texts is None


FACTS = ModelFacts(name="claude-opus-5-5", provider="Anthropic", latest=True,
                   names=frozenset({"claude-opus-5-5", "latest-claude-opus"}))


def _variants(*vs):
    return [row("rules", "system", "DEFAULT", variants=tuple(vs))]


def V(i, cond, sort=0):
    return VariantRow(id=f"v{i}", label=f"v{i}", condition=cond, content=f"V{i}", sort_order=sort)


@pytest.mark.parametrize(
    ("cond", "effort", "expected"),
    [
        ({"provider": ["Anthropic"]}, None, "V1"),
        ({"provider": ["OpenAI"]}, None, "DEFAULT"),
        ({"model": ["latest-claude-opus"]}, None, "V1"),
        ({"model": ["gpt-5"]}, None, "DEFAULT"),
        ({"latest": True}, None, "V1"),
        ({"latest": False}, None, "DEFAULT"),
        ({"reasoning": ["high", "max"]}, "high", "V1"),
        ({"reasoning": ["high"]}, "low", "DEFAULT"),
        ({"reasoning": ["unset"]}, None, "V1"),
        ({"provider": ["Anthropic"], "reasoning": ["max"]}, "high", "DEFAULT"),
        ({}, None, "DEFAULT"),
    ],
)
def test_variant_conditions(cond, effort, expected) -> None:
    config = _declared("rules", effort=effort)
    resolve(config, FakeSource(_variants(V(1, cond)), facts=FACTS))
    assert config.prompt_block_texts == {"rules": expected}


def test_first_matching_variant_wins_by_author_order() -> None:
    config = _declared("rules")
    resolve(config, FakeSource(_variants(V(2, {"latest": True}, 2), V(1, {"provider": "Anthropic"}, 1)), facts=FACTS))
    assert config.prompt_block_texts == {"rules": "V1"}
    assert config.prompt_block_report[0]["variant_id"] == "v1"


def test_a_tool_bound_block_is_absent_when_the_tool_is_not_in_the_run() -> None:
    rows = [row("web_rules", "system", "Search well.", bound_tool="web_search")]
    without = _declared("web_rules", tools=["read_file"])
    resolve(without, FakeSource(rows))
    assert without.prompt_block_texts == {"web_rules": ""}
    without.replace_variables({})
    assert without.system_instruction.base_instruction == ""
    with_tool = _declared("web_rules", tools=["web_search"])
    resolve(with_tool, FakeSource(rows))
    assert with_tool.prompt_block_texts == {"web_rules": "Search well."}


def test_a_tool_bound_block_that_is_off_says_so(caplog) -> None:
    """Never a silent "": the report (the Model view's Prompt blocks list) and the log name why."""
    import logging

    rows = [row("web_rules", "system", "Search well.", bound_tool="web_search")]
    without = _declared("web_rules", tools=["read_file"])
    with caplog.at_level(logging.INFO, logger="matrx_ai.prompt_blocks.resolve"):
        resolve(without, FakeSource(rows))
    report = without.prompt_block_report[0]
    assert report["off"] == "tool not in run" and report["bound_tool"] == "web_search"
    assert report["chars"] == 0
    assert any("web_rules" in r.getMessage() and "web_search" in r.getMessage() for r in caplog.records)
    with_tool = _declared("web_rules", tools=["web_search"])
    resolve(with_tool, FakeSource(rows))
    assert with_tool.prompt_block_report[0]["off"] is None


def test_a_skill_linked_block_renders_the_skill_body_and_brings_its_tools() -> None:
    rows = [row("deep-research", "system", "", source_kind="skill", source_ref="deep-research")]
    skills = {"deep-research": SkillBody("deep-research", "Research deeply.", ("tool-a", "tool-b"))}
    config = _declared("deep-research", tools=[])
    resolve(config, FakeSource(rows, skills))
    assert config.prompt_block_texts == {"deep-research": "Research deeply."}
    assert config.prompt_block_tool_ids == ["tool-a", "tool-b"]
    assert config.prompt_block_report[0]["skill_id"] == "deep-research"


def test_a_skill_that_disables_auto_invocation_brings_no_tools() -> None:
    rows = [row("s", "system", "", source_kind="skill", source_ref="s")]
    config = _declared("s", tools=[])
    resolve(config, FakeSource(rows, {"s": SkillBody("s", "B", ("t",), disable_auto_invocation=True)}))
    assert config.prompt_block_tool_ids == []


def test_a_skill_linked_block_whose_skill_is_gone_refuses() -> None:
    rows = [row("s", "system", "", source_kind="skill", source_ref="s")]
    with pytest.raises(PromptBlocksMissing):
        resolve(_declared("s"), FakeSource(rows))


def test_resolution_is_once_frozen_with_the_conversation() -> None:
    config = _declared("rules")
    resolve(config, FakeSource(LADDER))
    resolve(config, FakeSource([row("rules", "system", "CHANGED")]))
    assert config.prompt_block_texts == {"rules": "ME"}


# ── the matrx-ai Agent door (definition.py) ──────────────────────────────────────────────


def test_the_agent_door_resolves_and_fills_blocks_without_any_variables() -> None:
    config = _declared("rules")
    agent = Agent(config=config, variable_defaults={})
    set_block_source(FakeSource(LADDER))
    try:
        asyncio.run(agent.prepare_variables())
        agent.apply_variables()
    finally:
        set_block_source(None)
    # No app context -> no runner -> the personal rung never applies.
    assert agent.config.system_instruction.base_instruction == "<rules>\nORG\n</rules>"
