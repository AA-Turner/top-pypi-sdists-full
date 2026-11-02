"""The step contract, the three pipe bindings, and pipe selection.

Pure data + pure functions — no engine, no IO, no AI. ``step.py`` executes
what this module decides. Split so pipe selection (the part that decides
whether a whole pipeline can run human-only or AI-only) is testable without
a scheduler, a database, or a provider key.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

from matrx_graph.decisions import EscalationPolicy
from matrx_graph.types.usl import field_extras

Pipe = Literal["code", "human", "ai"]

PIPES: tuple[Pipe, ...] = ("code", "human", "ai")

# The reserved run-variable key that selects a pipe for a whole run. Value is
# either a bare pipe name ("run this entire workflow as a human") or a map
# {node_id: pipe} with an optional "*" default. Lives in
# AppContext.initial_variables, which the scheduler already carries and forks
# per invocation — so a run-scope override needs no engine change and no new
# wire field.
RUN_PIPE_VARIABLE = "__pipe"


class StepContract(BaseModel):
    """What this step IS — declared once, satisfied identically by every pipe.

    The contract is the entire reason the three pipes are interchangeable:
    ``output_schema`` is validated against whatever the selected pipe
    produces (the human's answer is validated by the engine at resume via
    the interrupt payload's ``schema_hint``; code and AI outputs are
    validated in the executor), so a downstream step cannot tell which pipe
    ran.
    """

    model_config = ConfigDict(extra="forbid")

    name: str = Field(
        min_length=1,
        max_length=200,
        description="What this step accomplishes, in plain language.",
        json_schema_extra=field_extras(order=0, placeholder="Pick the 5 keywords to target"),
    )
    question: str = Field(
        default="",
        description=(
            "What a person is asked, and what an agent is told, to do this "
            "step. '{dot.path}' placeholders interpolate this step's inputs, "
            "so upstream data appears inside the question. Defaults to `name`."
        ),
        json_schema_extra=field_extras(order=1, widget="textarea", multiline_rows=4),
    )
    output_schema: dict[str, JsonValue] = Field(
        description=(
            "JSON Schema for this step's result. THE contract — every pipe "
            "must produce a value that satisfies it, which is what makes the "
            "pipes swappable. Must describe an object."
        ),
        json_schema_extra=field_extras(order=2, widget="json"),
    )
    output_kind: str | None = Field(
        default=None,
        description=(
            "Optional platform kind (content_ir.kind_definition slug) this "
            "step's result conforms to — same vocabulary as every other "
            "node's output_kind, never a second one."
        ),
        json_schema_extra=field_extras(order=3, widget="kind_picker"),
    )

    @model_validator(mode="after")
    def _schema_is_an_object(self) -> StepContract:
        declared = self.output_schema.get("type")
        if declared not in (None, "object"):
            raise ValueError(
                "contract.output_schema must describe an object (got "
                f"type={declared!r}) — a step's result is a named set of "
                "fields so downstream connections can map individual values."
            )
        return self

    def prompt_text(self) -> str:
        return self.question.strip() or self.name


class CodePipe(BaseModel):
    """Run this step deterministically by delegating to a registered node.

    The delegate is any node type the engine already knows (``tool.call``,
    ``http.get``, a product action) — the code pipe adds no new execution
    machinery, it borrows the registry.
    """

    model_config = ConfigDict(extra="forbid")

    node_type: str = Field(
        default="",
        description=(
            "Registered node type to run for the CODE pipe (e.g. 'tool.call', "
            "'http.get'). Blank = this step has no code pipe."
        ),
        json_schema_extra=field_extras(order=0, widget="node_type_picker"),
    )
    config: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="Author-time config handed to the delegate node.",
        json_schema_extra=field_extras(order=1, widget="json"),
    )
    output_path: str = Field(
        default="",
        description=(
            "Optional dot path into the delegate's output to take as this "
            "step's result (e.g. 'result.data'). Blank = the whole output."
        ),
        json_schema_extra=field_extras(order=2, placeholder="result.data"),
    )
    inputs: dict[str, str] = Field(
        default_factory=dict,
        description=(
            "Optional {delegate field: dot path into this step's inputs} map "
            "(e.g. {'text': 'page_title'}). Blank = hand the delegate this "
            "step's whole input namespace. A step usually carries MORE than "
            "one action needs — the human and AI pipes read all of it — and a "
            "delegate that forbids unknown fields would reject the extras, so "
            "this map is what lets a strict action carry a real step."
        ),
        json_schema_extra=field_extras(order=3, widget="json"),
    )

    @property
    def available(self) -> bool:
        return bool(self.node_type.strip())


class HumanPipe(BaseModel):
    """Ask a person. Always available unless the author switches it off.

    Deliberately needs no configuration: the contract already says what is
    being asked and what a valid answer looks like. That is what makes
    "run the whole pipeline with only the human pipe" true by construction
    rather than by per-step authoring effort.
    """

    model_config = ConfigDict(extra="forbid")

    enabled: bool = Field(
        default=True,
        description="Can a person do this step?",
        json_schema_extra=field_extras(order=0, widget="toggle"),
    )
    instructions: str = Field(
        default="",
        description=(
            "Extra guidance shown alongside the contract's question. "
            "'{dot.path}' placeholders interpolate this step's inputs."
        ),
        json_schema_extra=field_extras(order=1, widget="textarea", multiline_rows=3),
    )
    default_answer: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="Pre-filled answer shown in the form (an editable draft).",
        json_schema_extra=field_extras(order=2, widget="json"),
    )

    @property
    def available(self) -> bool:
        return self.enabled


class AiPipe(BaseModel):
    """Run this step with a purpose-built agent.

    THE THREE PIPES law is explicit that generic is not good enough on the
    AI pipe, so there is no implicit "just use some model" fallback: the
    author binds an Mandate (preferred — swappable per org/user without a
    code change) or a specific agent. Unbound means the AI pipe is
    UNAVAILABLE, loudly, which is exactly the gap signal the growth-loop map
    wants to see.
    """

    model_config = ConfigDict(extra="forbid")

    mandate_key: str = Field(
        default="",
        description=(
            "Mandate that decides which agent runs this step "
            "(e.g. 'seo.keyword_classifier'). Preferred over agent_id — a "
            "slot is swappable per organization and per user without "
            "touching the workflow."
        ),
        json_schema_extra=field_extras(order=0, widget="mandate_agent_picker"),
    )
    agent_id: str = Field(
        default="",
        description="Specific saved agent, when this step is not on a slot.",
        json_schema_extra=field_extras(order=1, widget="agent_picker"),
    )
    instructions: str = Field(
        default="",
        description=(
            "Extra instructions handed to the agent on top of the contract's "
            "question. '{dot.path}' placeholders interpolate this step's inputs."
        ),
        json_schema_extra=field_extras(order=2, widget="textarea", multiline_rows=3),
    )

    @property
    def available(self) -> bool:
        return bool(self.mandate_key.strip() or self.agent_id.strip())


class PipeBindings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: CodePipe = Field(default_factory=CodePipe)
    human: HumanPipe = Field(default_factory=HumanPipe)
    ai: AiPipe = Field(default_factory=AiPipe)

    def get(self, pipe: Pipe) -> CodePipe | HumanPipe | AiPipe:
        return {"code": self.code, "human": self.human, "ai": self.ai}[pipe]

    def available(self) -> tuple[Pipe, ...]:
        return tuple(p for p in PIPES if self.get(p).available)


class PipePolicy(BaseModel):
    """Which pipe runs, and what happens when it can't.

    ``escalation`` is Arman's decision-point primitive — "the user gets
    prompted, and within a certain time if the user answers we go with the
    user; if not, we ask AI what to do". It is the platform's ONE escalation
    type (:mod:`matrx_graph.decisions`), consumed here unchanged rather than
    re-declared: the step freezes the absolute deadline onto its durable
    interrupt payload and the sweeper that acts on it decides for every
    asking node in the engine, not just this one.
    """

    model_config = ConfigDict(extra="forbid")

    pipe: Pipe = Field(
        default="ai",
        description="Which pipe runs this step by default.",
        json_schema_extra=field_extras(order=0, widget="pipe_selector"),
    )
    fallback: list[Pipe] = Field(
        default_factory=list,
        description=(
            "Ordered pipes to try when the chosen one is not available on "
            "this step. Empty = fail loudly instead of substituting."
        ),
        json_schema_extra=field_extras(order=1),
    )
    escalation: EscalationPolicy | None = Field(
        default=None,
        description=(
            "Optional deadline for the human pipe. Left empty, the step waits "
            "for the person indefinitely. Set, the run continues without them "
            "once the deadline passes — an agent decides, or the default "
            "answer is applied — and the output records who decided."
        ),
        json_schema_extra=field_extras(order=2, widget="json", help="Timed hand-off to AI"),
    )


class PipeStepConfig(BaseModel):
    """Author-time configuration for one contract-declared, pipe-swappable step."""

    model_config = ConfigDict(extra="forbid")

    contract: StepContract = Field(
        description="What this step is and what a valid result looks like.",
        json_schema_extra=field_extras(order=0, group="Contract"),
    )
    pipes: PipeBindings = Field(
        default_factory=PipeBindings,
        description="How this step can be done: by code, by a person, by an agent.",
        json_schema_extra=field_extras(order=1, group="Pipes"),
    )
    policy: PipePolicy = Field(
        default_factory=PipePolicy,
        description="Which pipe runs by default, and what happens if it can't.",
        json_schema_extra=field_extras(order=2, group="Policy"),
    )

    def effective_output_json_schema(self) -> dict[str, Any]:
        """The step's real output shape — read at compile time.

        ``NodeSpec.dynamic_output`` is True for ``pipe.step`` because the
        contract, not the registered model, is the output shape. The compiler
        stores this on the CompiledNode so downstream connections, the run
        form, and the studio's result rendering all see the real fields.
        """
        return dict(self.contract.output_schema)


class PipeSelection(BaseModel):
    """The decision: which pipe runs, why, and what was rejected."""

    model_config = ConfigDict(extra="forbid")

    pipe: Pipe | None
    reason: Literal["run_override", "authored", "fallback", "unavailable"]
    requested: Pipe | None = None
    available: list[Pipe] = Field(default_factory=list)

    @property
    def substituted(self) -> bool:
        return self.reason == "fallback"


def run_pipe_override(run_variables: dict[str, Any] | None, node_id: str) -> Pipe | None:
    """Read the run-scope pipe override for ``node_id``.

    Accepts a bare pipe name (applies to every step in the run — this is the
    "run this whole pipeline as a human" switch) or a map keyed by node id
    with an optional ``"*"`` default. Anything else is ignored: a malformed
    cosmetic override must never kill a live run.
    """
    if not run_variables:
        return None
    raw = run_variables.get(RUN_PIPE_VARIABLE)
    if isinstance(raw, str):
        candidate: Any = raw
    elif isinstance(raw, dict):
        candidate = raw.get(node_id, raw.get("*"))
    else:
        return None
    if isinstance(candidate, str) and candidate in PIPES:
        return candidate  # type: ignore[return-value]
    return None


def select_pipe(
    config: PipeStepConfig,
    *,
    node_id: str,
    run_variables: dict[str, Any] | None = None,
) -> PipeSelection:
    """Decide which pipe runs this step.

    Precedence: run override → authored default → authored fallback order.
    A pipe that is not bound on this step is never silently swapped for
    another unless the author declared a fallback — substitution without
    consent is how a "fully human" run quietly becomes an AI run.
    """
    available = list(config.pipes.available())
    requested = run_pipe_override(run_variables, node_id)
    reason: Literal["run_override", "authored"] = "authored"
    if requested is not None:
        reason = "run_override"
    else:
        requested = config.policy.pipe

    if config.pipes.get(requested).available:
        return PipeSelection(
            pipe=requested, reason=reason, requested=requested, available=available
        )

    for candidate in config.policy.fallback:
        if candidate != requested and config.pipes.get(candidate).available:
            return PipeSelection(
                pipe=candidate,
                reason="fallback",
                requested=requested,
                available=available,
            )

    return PipeSelection(pipe=None, reason="unavailable", requested=requested, available=available)


def dig(payload: Any, path: str) -> Any:
    """Walk a dot path into a value. Missing segment → None."""
    if not path:
        return payload
    current = payload
    for segment in path.split("."):
        if isinstance(current, dict) and segment in current:
            current = current[segment]
        else:
            return None
    return current
