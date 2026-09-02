"""AgentPlan — the simplified scheme agents use to design mini workflows.

The shape is deliberately flat (a step list, not a node/edge graph) because
that is what an LLM can author reliably. ``plan_json_schema()`` is the
output_schema a planner agent is given; ``compile_plan`` (compiler.py)
converts a validated plan into a standard ``matrx_graph.Definition``.

Reference grammar (strict — anything else ``$``-prefixed is a validation
error, catching typos like ``$step.1``):

    $inputs.<path>              value from AgentPlan.inputs (inlined at
                                compile time — plans re-run with new inputs
                                by recompiling, which is cheap and
                                deterministic)
    $steps.<n>.output           the whole output payload of step n
    $steps.<n>.output.<path>    a path into it (an agent step's payload is
                                the AiExecutionResult dump — final_text,
                                structured_output, usage, ...; a for_each
                                step's payload is {values: [...], count: N})
    $item / $item.<path>        the current item — for_each steps only

``<path>`` is dot-separated identifiers or list indices (digits). No
wildcards and no ``[]`` — per-item work is expressed with ``for_each``,
never with array plucks.
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from typing import Any, NamedTuple
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

# CAPS — bounds, not feature flags. A plan is a "mini" workflow by contract;
# anything bigger belongs in the full workflow system.
MAX_PLAN_STEPS = 20
FOR_EACH_MAX_ITEMS = 200

_SEG = r"[A-Za-z_][A-Za-z0-9_]*|\d+"
PLAN_REF_RE = re.compile(
    rf"^\$(?:"
    rf"inputs(?:\.(?:{_SEG}))+"
    rf"|steps\.\d+\.output(?:\.(?:{_SEG}))*"
    rf"|item(?:\.(?:{_SEG}))*"
    rf")$"
)

# Embedded step-output references inside a `when` predicate expression.
WHEN_REF_RE = re.compile(rf"\$steps\.(\d+)\.output((?:\.(?:{_SEG}))*)")


class ParsedRef(NamedTuple):
    kind: str  # "inputs" | "steps" | "item"
    step: int | None
    path: tuple[str, ...]


def parse_ref(value: str) -> ParsedRef | None:
    """Parse a ``$``-reference string. Returns None when it doesn't match the
    grammar (callers decide whether that's an error — any ``$``-prefixed
    string that fails to parse is)."""
    if not PLAN_REF_RE.match(value):
        return None
    body = value[1:]
    parts = body.split(".")
    if parts[0] == "inputs":
        return ParsedRef("inputs", None, tuple(parts[1:]))
    if parts[0] == "steps":
        return ParsedRef("steps", int(parts[1]), tuple(parts[3:]))
    return ParsedRef("item", None, tuple(parts[1:]))


def is_ref(value: Any) -> bool:
    return isinstance(value, str) and value.startswith("$")


def iter_ref_strings(value: Any, path: str = "") -> Iterator[tuple[str, str]]:
    """Yield ``(json_path, ref_string)`` for every $-prefixed string anywhere
    in a value tree — top level, nested lists, nested objects."""
    if is_ref(value):
        yield path, value
    elif isinstance(value, dict):
        for k, v in value.items():
            yield from iter_ref_strings(v, f"{path}.{k}" if path else str(k))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from iter_ref_strings(v, f"{path}[{i}]" if path else f"[{i}]")


# The keys a plain agent step's output payload actually has (the
# AiExecutionResult dump — graph_nodes/shared.py). $steps.N.output.<first>
# must start with one of these; the agent's own JSON fields live under
# structured_output. A for_each step's payload has FAN_OUT_PAYLOAD_KEYS.
AGENT_PAYLOAD_KEYS = frozenset(
    {
        "conversation_id",
        "request_id",
        "iterations",
        "finish_reason",
        "final_text",
        "final_message",
        "messages",
        "usage",
        "duration_ms",
        "tool_calls_made",
        "metadata",
        "structured_output",
    }
)
FAN_OUT_PAYLOAD_KEYS = frozenset({"values", "count"})
# Payload keys that are scalars — a ref path can never continue past them.
# (The 2026-07-07 review showed depth-1-only checking let
# $steps.1.output.final_text.foo and $steps.2.output.values.final_text
# through the gate to die at runtime after paid calls.)
SCALAR_PAYLOAD_KEYS = frozenset(
    {
        "conversation_id",
        "request_id",
        "iterations",
        "finish_reason",
        "final_text",
        "duration_ms",
        "tool_calls_made",
    }
)


class PlanStep(BaseModel):
    """One agent invocation in the plan."""

    model_config = ConfigDict(extra="forbid")

    step: int = Field(ge=1, description="Unique step number, 1-based.")
    agent_id: UUID = Field(description="The saved agent to run.")
    purpose: str = Field(
        min_length=1,
        description="What this step accomplishes — becomes the node label.",
    )
    inputs: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Inputs for the agent. The reserved key 'user_input' becomes the "
            "user message; every other key must be one of the agent's "
            "declared variables. Values are JSON literals (strings, numbers, "
            "booleans, lists, objects) or $-reference strings — references "
            "work inside nested lists/objects too."
        ),
    )
    depends_on: list[int] = Field(
        default_factory=list,
        description=(
            "Steps that must complete first. Steps referenced via $steps.N "
            "in inputs/for_each/when are dependencies automatically; list "
            "here only pure-ordering dependencies."
        ),
    )

    @field_validator("inputs", "depends_on", mode="before")
    @classmethod
    def _null_means_default(cls, v: Any, info: ValidationInfo) -> Any:
        # LLMs routinely emit explicit nulls for "nothing here" — treat
        # null exactly like omission instead of failing validation.
        if v is None:
            return {} if info.field_name == "inputs" else []
        return v
    for_each: str | None = Field(
        default=None,
        description=(
            "A $-reference resolving to a list. When set, this step runs "
            "once per item IN PARALLEL, and inputs may use $item.<path>. "
            "The step's output becomes {values: [per-item results], count}."
        ),
    )
    when: str | None = Field(
        default=None,
        description=(
            "Optional condition. A boolean expression over "
            "$steps.M.output.<path> references and literals, where M is this "
            "step's single dependency (e.g. \"$steps.1.output.iterations < "
            "5\"). When false, this step and everything depending on it are "
            "skipped."
        ),
    )


class AgentPlan(BaseModel):
    """A complete agent-designed mini workflow."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(
        min_length=1,
        max_length=120,
        description="Short human-readable name for the workflow.",
    )
    reasoning: str = Field(
        min_length=1,
        description="Why the plan is shaped this way — steps, dependencies, parallelism.",
    )
    inputs: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Named runtime parameters referenced via $inputs.<name>. "
            "Resolved when the plan is compiled."
        ),
    )
    steps: list[PlanStep] = Field(min_length=1, max_length=MAX_PLAN_STEPS)

    @field_validator("inputs", mode="before")
    @classmethod
    def _null_inputs_means_default(cls, v: Any) -> Any:
        return {} if v is None else v


def plan_json_schema() -> dict[str, Any]:
    """The JSON Schema a planner agent is given as its output_schema.

    Routed through the provider-aware schema gate's portable derivation
    (matrx_ai.schema) so the raw Pydantic dump — which leaves defaulted
    fields out of ``required`` — becomes valid for OpenAI strict, Anthropic
    and Gemini alike. Never hand-massage provider rules here.
    """
    from matrx_ai.schema import lint_output_schema

    raw = AgentPlan.model_json_schema()
    portable = lint_output_schema(raw).portable_schema
    return portable if isinstance(portable, dict) else raw
