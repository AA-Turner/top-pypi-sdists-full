from __future__ import annotations

from typing import Any, Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.types.handle import HandleSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory, RetryPolicy

InputT = TypeVar("InputT", bound=BaseModel)
OutputT = TypeVar("OutputT", bound=BaseModel)
ConfigT = TypeVar("ConfigT", bound=BaseModel)


class EmptyInput(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EmptyOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EmptyConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class NodeSpec(BaseModel, Generic[InputT, OutputT, ConfigT]):
    """Static declaration of a node type.

    A NodeSpec is registered once by the node author; many NodeDefs in a user's
    graph may reference the same NodeSpec by `type`. The spec carries all the
    information the scheduler needs to execute a node correctly (schemas,
    handles, determinism, retry policy) and everything the UI needs to render
    its palette entry and config form (schemas again, plus category/icon).

    Generic parameters:
        InputT  — Pydantic model for inbound channel payload / previous-node output
        OutputT — Pydantic model for the value this node writes to its output channels
        ConfigT — Pydantic model for author-time config (what the UI form captures)

    The schemas are stored as `type[BaseModel]` class references so they can
    participate in JSON Schema export, TypeAdapter validation, and compiler
    type-compatibility checks.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        frozen=True,
        populate_by_name=True,
    )

    node_type: str = Field(
        alias="type",
        min_length=1,
        max_length=120,
        pattern=r"^[a-z][a-z0-9_]*(\.[a-z0-9_]+)+$",
        description=(
            "Dotted identifier, e.g. 'control.branch', 'llm.chat', 'tool.call'. "
            "First segment is the category namespace; remainder is the node name. "
            "Stored as `node_type` internally to avoid shadowing the builtin `type` "
            "in annotations like `type[BaseModel]`."
        ),
    )
    category: NodeCategory
    display_name: str = Field(min_length=1, max_length=120)
    description: str = ""
    icon: str | None = None

    input_schema: type[BaseModel] = EmptyInput
    output_schema: type[BaseModel] = EmptyOutput
    config_schema: type[BaseModel] = EmptyConfig

    handles: tuple[HandleSpec, ...] = ()

    determinism: ActionTier = ActionTier.NON_DETERMINISTIC
    retry: RetryPolicy = Field(default_factory=RetryPolicy.default)

    timeout_ms: int | None = Field(
        default=None,
        ge=1,
        description=(
            "Per-attempt timeout in milliseconds. None (default) = no timeout. "
            "When set, the scheduler wraps the executor call in asyncio.wait_for; "
            "exceeding the budget raises NodeTimeoutError, which the retry policy "
            "treats like any other exception (eligible for retry if 'NodeTimeoutError' "
            "is in retry_on or retry_on is empty). The timeout applies to ONE attempt; "
            "with max_attempts=3 and timeout_ms=5000, the worst-case latency for that "
            "node is 3*5000ms = 15s plus any backoff delays."
        ),
    )

    re_execute_on_resume: bool = Field(
        default=False,
        description=(
            "If true, the scheduler SKIPS the idempotency lookup on resume and "
            "re-invokes this node fresh — even if a prior outcome was recorded. "
            "Use for nodes whose correctness depends on 'now' rather than cached "
            "state (timestamps, rate-limited external calls that must not be "
            "replayed mid-backoff, user-facing notifications that shouldn't "
            "double-send). Default false: resume-after-crash reuses recorded "
            "outputs, which is safe for pure + idempotent nodes and acceptable "
            "for most side-effectful ones."
        ),
    )

    emits_stream: bool = False
    can_interrupt: bool = False
    # WHERE THIS STEP'S OUTPUT VALUES COME FROM (lane 11 round 5) — deny-by-default.
    #   'deterministic' — computed only from its inputs and config (records.*, data/text
    #                     transforms, control.*, flow.*);
    #   'outside'       — fetched from a system the owner pointed it at (http.*): the owner's
    #                     own design, not a model's;
    #   'ai'            — anything a model, an agent, a person answering, or an unknown
    #                     executor may have shaped. THE DEFAULT: a step nobody declared counts
    #                     as AI, so a write downstream of it follows the organization's
    #                     agent-change setting instead of being the owner's standing rule.
    values_are: Literal["deterministic", "outside", "ai"] = "ai"
    # LAUNCH DECLARATION (2026-10-01). True when the executor may call
    # ``ctx.send`` to a target NOT given by ``config.target_node_id`` (the
    # dispatchers in ``validation.DISPATCHER_NODE_TYPES`` launch that static
    # target and need no flag). The resume pre-flight treats a live launcher
    # as "anything may still fire" and never refuses on reachability; a census
    # test fails any executor that calls ``ctx.send`` without declaring it.
    launches_nodes: bool = False
    # RUN-ROW OUTPUT (2026-10-05). False when this step's output is a large working document that
    # the NEXT step consumes (the news monitor's run document, ~2 MB). The output is still persisted
    # in full on the step's own ``workflow.node_outcome`` row and still flows to the next step; only
    # the ``workflow.run.output`` aggregate gets a small ``{"output_elided": true, …}`` marker naming where it
    # is. Without it a 20-step run wrote ~11 MB into one row and its final write timed out.
    output_in_run_row: bool = True
    default_join_policy: Literal["all", "any"] | None = Field(
        default=None,
        description=(
            "Join policy this node TYPE defaults to when the author has not "
            "set NodeDef.data.join_policy (ENGINE_SPEC §3.3). None = the "
            "engine default ('all'). control.loop declares 'any': its return "
            "edge delivers once per iteration and must re-fire the loop per "
            "delivery — under 'all' every loop would deadlock on its first "
            "firing (the return edge can't be satisfied yet). An authored "
            "data.join_policy always wins."
        ),
    )
    is_source: bool = Field(
        default=False,
        description="True if this node has no inputs and seeds a graph's initial state.",
    )
    is_sink: bool = Field(
        default=False,
        description="True if this node has no outputs and terminates a branch.",
    )
    dynamic_output: bool = Field(
        default=False,
        description=(
            "True if this node's effective output schema is computed from its "
            "config at compile time, not the static output_schema (e.g. "
            "io.user_input, whose fields the author defines). The compiler "
            "stores the computed JSON Schema on the CompiledNode for run-form "
            "generation and downstream type hints; the registered output_schema "
            "stays permissive (extra='allow') so static validation never rejects "
            "author-defined fields."
        ),
    )

    input_kind: str | None = Field(
        default=None,
        description=(
            "Platform kind (content_ir.kind_definition slug) this node's input "
            "payload conforms to. The kind is the CANONICAL cross-platform "
            "declaration; input_schema remains the node's implementation "
            "detail. When set, the scheduler validates merged inputs against "
            "the kind's registered JSON Schema before execute (per-field "
            "errors, parks the run on this node). None = no named kind; the "
            "pydantic input_schema (or the compiled dynamic schema) is the "
            "inline anonymous shape."
        ),
    )
    output_kind: str | None = Field(
        default=None,
        description=(
            "Platform kind this node's output conforms to. Stamped onto every "
            "recorded NodeOutcome (workflow.node_outcome.output_kind) and "
            "exposed to UIs so outputs render/route through the Shape "
            "registry. Output mismatches are a NODE-AUTHOR defect, so the "
            "scheduler logs them LOUDLY but does not fail the run (mirrors "
            "the malformed-schema posture in schema_validation). Generic "
            "pass-through nodes declare 'json'/'text'. A dynamic-output node "
            "whose shape is only known at compile time (io.user_input) leaves "
            "this None and carries its compiled inline schema instead; "
            "subgraph.call, though also composed at compile time, declares the "
            "stable 'workflow_run_result' kind."
        ),
    )

    renders_input_templates: bool = Field(
        default=False,
        description=(
            "True if this node type INTERPRETS placeholder templates inside "
            "its INPUT values — i.e. an authored '{{name}}' / '{name}' there "
            "is a slot the node fills, not literal text. Only text.template "
            "does this today; every other template in the engine is read from "
            "CONFIG (control.map's payload_template, text.render_list's "
            "item_template, control.human_input's prompt …), which this flag "
            "says nothing about. validate_definition refuses a placeholder in "
            "a literal input of a node that does NOT declare it: on "
            "2026-09-12 the Masterwork Conductor wrote '{{sealed_case_id}}' "
            "into an ai.chat.manual node's user_input, the save gate "
            "said nothing, and the agent received those 18 characters "
            "verbatim (the run died on 'invalid input syntax for type uuid')."
        ),
    )

    tags: tuple[str, ...] = ()
    version: str = "1.0.0"

    def input_json_schema(self) -> dict[str, Any]:
        return self.input_schema.model_json_schema()

    def output_json_schema(self) -> dict[str, Any]:
        return self.output_schema.model_json_schema()

    def config_json_schema(self) -> dict[str, Any]:
        return self.config_schema.model_json_schema()

    def to_palette_descriptor(self) -> dict[str, Any]:
        """Serializable palette entry for the Studio UI.

        Returns the shape consumed by GET /workflow/node-types — JSON Schemas for
        config/input/output plus UI-facing metadata (display name, category, icon).
        """
        return {
            "type": self.node_type,
            "category": self.category.value,
            "display_name": self.display_name,
            "description": self.description,
            "icon": self.icon,
            "handles": [h.model_dump() for h in self.handles],
            "input_schema": self.input_json_schema(),
            "output_schema": self.output_json_schema(),
            "config_schema": self.config_json_schema(),
            "determinism": self.determinism.value,
            "emits_stream": self.emits_stream,
            "can_interrupt": self.can_interrupt,
            "is_source": self.is_source,
            "is_sink": self.is_sink,
            "dynamic_output": self.dynamic_output,
            "renders_input_templates": self.renders_input_templates,
            "input_kind": self.input_kind,
            "output_kind": self.output_kind,
            "tags": list(self.tags),
            "version": self.version,
            # DEPRECATED STEPS (matrx_graph.deprecations): Studio marks the step card
            # "Deprecated — replace with …" and never offers it for a new step.
            "deprecation": _palette_deprecation(self.node_type),
        }


def _palette_deprecation(node_type: str) -> dict[str, str] | None:
    from matrx_graph.deprecations import palette_entry

    return palette_entry(node_type)
