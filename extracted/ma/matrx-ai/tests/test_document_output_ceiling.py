"""THE DOCUMENT-CEILING FLOOR, proven — an output whose length the INPUT decides
never runs under a number an author guessed.

What is being proven:

1. ``matrx_ai.config.output_ceiling.enforce_document_ceiling`` RAISES an
   explicit ceiling to the model's real maximum for the three document shapes
   (a schema carrying an array, a schema carrying a maxLength-free string, free
   prose with nowhere to continue) and LEAVES ALONE everything else (a fully
   bounded schema, free prose in a conversation, an absent ceiling, an unknown
   model maximum).
2. ``matrx_ai.graph_nodes.mandates.hold_step`` — the one door every authored AI
   workflow step goes through — applies that floor on the real merge path and
   stamps ``continuable: False`` on the step's request metadata.

The numbers are the live incident's own (workflow run
2cf711eb-1a15-49ed-baf7-ddb166dba129, 2026-09-12): a prose step authored at
``max_tokens: 1200`` (a parent saw four of her seven questions, under an offer
to "ask me to continue" that nobody inside a workflow run can perform) and a
structured step authored at ``max_tokens: 2500`` (its JSON never closed and the
whole paid run errored).

Why it is a forcing test: the step-level case runs the REAL ``hold_step``, the
REAL merge, the REAL ``step_metadata`` and the REAL ``enforce_document_ceiling``.
Only two seams are doubled — the host's mandate resolver (the same replacement
the host performs at startup, following ``test_workflow_step_holder.py``) and
the catalog lookup that would need a database. Neutralising the floor — calling
``hold_step`` with ``enforce_document_ceiling`` replaced by a no-op, which is
exactly the pre-fix code — turns the step-level assertions red.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai import mandates as mandates_mod
from matrx_ai.agents.named import AgentSource
from matrx_ai.config.finish_reason import CONTINUABLE_METADATA_KEY
from matrx_ai.config.output_ceiling import enforce_document_ceiling
from matrx_ai.graph_nodes import mandates as step_mandates
from matrx_ai.graph_nodes.mandates import hold_step
from matrx_ai.mandates import MandateResolution

# Two real catalog maxima (ai.model_definition.max_tokens), so no single
# hard-coded return value can satisfy the raising cases.
SONNET_MAX = 64_000
OPUS_MAX = 128_000

#: The incident's own authored ceilings.
PROSE_CEILING = 1_200
STRUCTURED_CEILING = 2_500

ARRAY_SCHEMA = {
    "type": "object",
    "properties": {
        "rules": {
            "type": "array",
            "items": {"type": "object", "properties": {"rule_id": {"type": "string"}}},
        }
    },
}

FREE_TEXT_SCHEMA = {
    "type": "object",
    "properties": {"rationale": {"type": "string"}},
}

BOUNDED_SCHEMA = {
    "type": "object",
    "properties": {
        "verdict": {"type": "string", "enum": ["escalate", "observe"]},
        "kind": {"const": "diagnosis"},
        "confidence": {"type": "number"},
        "note": {"type": "string", "maxLength": 200},
    },
}


# --------------------------------------------------------------------------
# (a) (b) (c) — the three document shapes are raised to the model's maximum
# --------------------------------------------------------------------------
@pytest.mark.parametrize("model_max", [SONNET_MAX, OPUS_MAX])
@pytest.mark.parametrize(
    "declared, schema, continuable, expected_reason",
    [
        (STRUCTURED_CEILING, ARRAY_SCHEMA, False, "array"),
        (PROSE_CEILING, ARRAY_SCHEMA, True, "array"),
        (STRUCTURED_CEILING, FREE_TEXT_SCHEMA, False, "free-text"),
        (PROSE_CEILING, FREE_TEXT_SCHEMA, True, "free-text"),
        (PROSE_CEILING, None, False, "prose"),
        (STRUCTURED_CEILING, None, False, "prose"),
    ],
)
def test_a_document_ceiling_is_raised_to_the_model_maximum(
    declared: int, schema: Any, continuable: bool, expected_reason: str, model_max: int
) -> None:
    settings = {"max_output_tokens": declared, "temperature": 0.4}

    repairs = enforce_document_ceiling(
        settings,
        model_max=model_max,
        output_schema=schema,
        continuable=continuable,
        label="the incident step",
    )

    assert settings["max_output_tokens"] == model_max
    assert settings["temperature"] == 0.4, "only the ceiling is touched"
    assert len(repairs) == 1
    assert expected_reason in repairs[0]
    assert f"{declared} -> {model_max}" in repairs[0]
    assert "the incident step" in repairs[0]


def test_it_mutates_an_object_in_place_too() -> None:
    """A live UnifiedConfig is an object, not a dict; the caller keeps holding it."""

    class _Config:
        max_output_tokens = PROSE_CEILING

    config = _Config()
    repairs = enforce_document_ceiling(
        config, model_max=SONNET_MAX, output_schema=ARRAY_SCHEMA, continuable=False
    )

    assert config.max_output_tokens == SONNET_MAX
    assert len(repairs) == 1


# --------------------------------------------------------------------------
# (d) (e) (f) (g) — what it must NEVER touch
# --------------------------------------------------------------------------
@pytest.mark.parametrize(
    "case, settings, kwargs",
    [
        (
            "a fully bounded schema keeps its cost knob",
            {"max_output_tokens": PROSE_CEILING},
            {"model_max": SONNET_MAX, "output_schema": BOUNDED_SCHEMA, "continuable": False},
        ),
        (
            "free prose in a conversation keeps its cost knob",
            {"max_output_tokens": PROSE_CEILING},
            {"model_max": SONNET_MAX, "output_schema": None, "continuable": True},
        ),
        (
            "an absent ceiling is never invented",
            {"temperature": 0.4},
            {"model_max": SONNET_MAX, "output_schema": ARRAY_SCHEMA, "continuable": False},
        ),
        (
            "an unknown model maximum stays quiet",
            {"max_output_tokens": STRUCTURED_CEILING},
            {"model_max": None, "output_schema": ARRAY_SCHEMA, "continuable": False},
        ),
        (
            "a ceiling already at the maximum is not a defect",
            {"max_output_tokens": SONNET_MAX},
            {"model_max": SONNET_MAX, "output_schema": ARRAY_SCHEMA, "continuable": False},
        ),
    ],
)
def test_a_legitimate_ceiling_is_left_exactly_alone(
    case: str, settings: dict[str, Any], kwargs: dict[str, Any]
) -> None:
    before = dict(settings)

    repairs = enforce_document_ceiling(settings, **kwargs)

    assert repairs == [], case
    assert settings == before, case


# --------------------------------------------------------------------------
# THE STEP-LEVEL FORCING TEST — the live incident's own step shape
# --------------------------------------------------------------------------
class _HolderConfig:
    """The slice of a UnifiedConfig the Holder merge reads."""

    model = "holder-model"
    system_instruction = "HOLDER RULES"
    temperature = 0.7


class _Holder:
    name = "Workflow Step Intelligence"
    config = _HolderConfig()


class _Source(AgentSource):
    agent_id: str = "holder-agent-id"
    is_version: bool = False

    async def load(self) -> Any:
        return _Holder()


def _install_resolver(monkeypatch) -> None:
    """Replace ONLY the host's mandate resolver — the same replacement aidream
    performs at startup (the convention in ``test_workflow_step_holder.py``)."""

    async def _resolver(mandate_key: str) -> MandateResolution:
        return MandateResolution(source=_Source())

    monkeypatch.setattr(mandates_mod, "_MANDATE_RESOLVER", _resolver)


def _install_catalog(monkeypatch, maximum: int | None) -> None:
    """Replace ONLY the catalog lookup, which would need a database."""

    async def _max(model_id_or_name: Any) -> int | None:
        return maximum

    monkeypatch.setattr(step_mandates, "model_output_maximum", _max)


#: The live incident's prose step, as the node hands it to ``hold_step``.
INCIDENT_STEP: dict[str, Any] = {
    "model": "the-conductor-model",
    "messages": [
        {"role": "user", "content": "My four-year-old refuses to put her shoes on."}
    ],
    "system_instruction": "Ask the parent what you need to know.",
    "max_tokens": PROSE_CEILING,
}


@pytest.mark.asyncio
@pytest.mark.parametrize("model_max", [SONNET_MAX, OPUS_MAX])
async def test_an_authored_prose_step_runs_at_the_model_maximum(
    monkeypatch, model_max: int
) -> None:
    """The 1,200-token prose step: no ceiling an author types can be right, and
    a cut inside a workflow run is final."""
    _install_resolver(monkeypatch)
    _install_catalog(monkeypatch, model_max)

    held = await hold_step(
        dict(INCIDENT_STEP), spec_type="ai.llm", consumer="ai.llm.chat"
    )

    assert held.config["max_tokens"] == model_max
    assert held.config["messages"] == INCIDENT_STEP["messages"], "the step is otherwise intact"
    assert held.config["system_instruction"] == INCIDENT_STEP["system_instruction"]


@pytest.mark.asyncio
async def test_an_authored_step_is_never_continuable(monkeypatch) -> None:
    """There is no conversation inside a workflow run, so the truncation notice
    must never offer "ask me to continue"."""
    _install_resolver(monkeypatch)
    _install_catalog(monkeypatch, SONNET_MAX)

    held = await hold_step(
        dict(INCIDENT_STEP), spec_type="ai.llm", consumer="ai.llm.chat"
    )

    assert held.metadata[CONTINUABLE_METADATA_KEY] is False


@pytest.mark.asyncio
async def test_a_structured_step_with_an_array_is_raised_too(monkeypatch) -> None:
    """The 2,500-token ``read_case`` half of the same run: arrays of rule ids and
    free-text rationales, whose JSON never closed."""
    _install_resolver(monkeypatch)
    _install_catalog(monkeypatch, OPUS_MAX)

    step = {
        **INCIDENT_STEP,
        "max_tokens": STRUCTURED_CEILING,
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": "read_case", "schema": ARRAY_SCHEMA},
        },
    }

    held = await hold_step(dict(step), spec_type="ai.llm", consumer="ai.llm.chat")

    assert held.config["max_tokens"] == OPUS_MAX


@pytest.mark.asyncio
async def test_a_bounded_structured_step_keeps_its_authored_ceiling(monkeypatch) -> None:
    """The floor is not a blanket raise: a schema that bounds its own size keeps
    the author's number."""
    _install_resolver(monkeypatch)
    _install_catalog(monkeypatch, SONNET_MAX)

    step = {
        **INCIDENT_STEP,
        "max_tokens": PROSE_CEILING,
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": "triage", "schema": BOUNDED_SCHEMA},
        },
    }

    held = await hold_step(dict(step), spec_type="ai.llm", consumer="ai.llm.chat")

    assert held.config["max_tokens"] == PROSE_CEILING


@pytest.mark.asyncio
async def test_an_unknown_model_maximum_leaves_the_step_alone(monkeypatch) -> None:
    """The catalog could not say, so the floor stays quiet rather than inventing
    a maximum — the release-health sweep still catches the row."""
    _install_resolver(monkeypatch)
    _install_catalog(monkeypatch, None)

    held = await hold_step(
        dict(INCIDENT_STEP), spec_type="ai.llm", consumer="ai.llm.chat"
    )

    assert held.config["max_tokens"] == PROSE_CEILING
