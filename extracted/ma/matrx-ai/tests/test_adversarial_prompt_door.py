"""Adversarial review of THE PROMPT DOOR (KINDS_EVERYWHERE_PLAN.md §4.2).

Claim under attack: ``AgentVariable._runtime_value`` strips ``__kind`` markers
before structured values enter prompts — data intact, wire vocabulary withheld.

Tests marked ``xfail(strict=True)`` are REPRODUCED HOLES: they assert the
behavior the contract PROMISES, and today's code breaks that promise. When a
fix lands they flip to XPASS (strict makes that a loud failure) and the marker
should be removed. Unmarked tests document attacks that HELD.

Run: cd /Users/armanisadeghi/code/aidream && uv run pytest \
    packages/matrx-ai/tests/test_adversarial_prompt_door.py -q
"""

from __future__ import annotations

import json

import pytest
from pydantic import BaseModel, ConfigDict, Field

from matrx_ai.agents.definition import Agent
from matrx_ai.agents.variables import AgentVariable
from matrx_ai.config.unified_config import UnifiedConfig

WIRE_KEY = "__kind"


def _prompt_texts(agent: Agent) -> list[str]:
    """Every string this agent would send as prompt text after substitution."""
    out: list[str] = []
    si = agent.config.system_instruction
    if si is not None:
        out.append(getattr(si, "base_instruction", str(si)))
    for message in agent.config.messages:
        for content in getattr(message, "content", []) or []:
            text = getattr(content, "text", None)
            if isinstance(text, str):
                out.append(text)
    return out


def _agent_with_template() -> Agent:
    config = UnifiedConfig(
        model="gpt-4.1-mini",
        messages=[],
        system_instruction="Data: {{payload}}",
    )
    config.append_user_message("User data: {{payload}}")
    return Agent(
        config=config,
        variable_defaults={"payload": AgentVariable(name="payload")},
    )


# ---------------------------------------------------------------------------
# Attacks that HELD
# ---------------------------------------------------------------------------


def test_held_dict_default_is_stripped_at_every_depth() -> None:
    """Default-value dicts: markers removed root and nested; data intact."""
    var = AgentVariable(
        name="a",
        default_value={
            WIRE_KEY: "website",
            "url": "x",
            "nested": {WIRE_KEY: "inner", "k": 1},
        },
    )
    rendered = var.get_value()
    assert WIRE_KEY not in rendered
    assert json.loads(rendered) == {"url": "x", "nested": {"k": 1}}


def test_held_list_value_strips_each_element() -> None:
    var = AgentVariable(
        name="a",
        value=[{WIRE_KEY: "website", "url": "x"}, {WIRE_KEY: "y"}, [{WIRE_KEY: "z"}]],
    )
    rendered = var.get_value()
    assert WIRE_KEY not in rendered
    assert json.loads(rendered) == [{"url": "x"}, {}, [{}]]


def test_held_structured_values_render_as_canonical_json_not_repr() -> None:
    var = AgentVariable(name="a", value={"key": "va'l", "n": 1})
    assert json.loads(var.get_value()) == {"key": "va'l", "n": 1}


# ---------------------------------------------------------------------------
# FINDING A1 (CRITICAL): explicit runtime values bypass the strip door
# entirely. Agent.apply_variables uses self.variable_values[name] RAW (no
# get_value / _runtime_value), and UnifiedConfig.replace_variables +
# TextContent.replace_variables do str(value). A dict variable set at run
# time (named.py:793 agent.set_variables(**variables) — the production
# NamedAgent path; mandates/service.py:1480; workflow-fed variables via
# build_agent_request) lands in the prompt as a PYTHON REPR carrying
# '__kind'. Two contract breaks at once: the wire key leaks AND the value is
# unparseable repr instead of canonical JSON.
# ---------------------------------------------------------------------------


# FIXED (round-1 triage, 2026-08-21): prompt_safe_value is the one door;
# this test now guards it.
def test_tuple_of_kind_instances_does_not_leak() -> None:
    var = AgentVariable(name="a", value=({WIRE_KEY: "website", "url": "x"},))
    assert WIRE_KEY not in var.get_value()


# ---------------------------------------------------------------------------
# FINDING A4 (MEDIUM): the auto-assign escape hatch is a marker smuggling
# lane. has_auto_assign_tag checks ONLY value.get("type") == "auto_assign" —
# any dict claiming that type is returned UNCHANGED, nested __kind and all.
# If auto-assignment resolution then does not replace it (unbound variable,
# resolver best-effort failure), the raw dict flows to replace_variables'
# str() with every marker intact.
# ---------------------------------------------------------------------------


class _KindShapedModel(BaseModel):
    # A model whose dump carries the wire discriminator (KindModel-style
    # alias) plus data — the exact shape a workflow hands an agent variable.
    # (The original review left this fixture undefined; the NameError hid
    # behind the xfail.)
    model_config = ConfigDict(populate_by_name=True)

    kind_: str = Field(default="website", alias=WIRE_KEY, serialization_alias=WIRE_KEY)
    url: str = "https://example.com"

    def model_dump(self, **kwargs):
        kwargs.setdefault("by_alias", True)
        return super().model_dump(**kwargs)


# FIXED (round-1 triage, 2026-08-21): prompt_safe_value is the one door;
# this test now guards it.
def test_pydantic_model_value_renders_as_stripped_json() -> None:
    var = AgentVariable(name="a", value=_KindShapedModel())
    rendered = var.get_value()
    parsed = json.loads(rendered)  # repr raises here
    assert WIRE_KEY not in parsed
