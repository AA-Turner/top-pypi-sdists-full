from __future__ import annotations

import copy
import weakref
from typing import Any, Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.types.handle import HandleSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory, RetryPolicy

InputT = TypeVar("InputT", bound=BaseModel)
OutputT = TypeVar("OutputT", bound=BaseModel)
ConfigT = TypeVar("ConfigT", bound=BaseModel)

# A schema model's JSON Schema, built ONCE per class. Pydantic regenerates ``model_json_schema()`` on every call, and
# the palette, /ai/context/preview and validate_definition ask it for every node spec in a request — that rebuild ran
# on the event loop and was the named frame of repeated 1-3 s ``event_loop_stall`` rows (2026-11-02/03). Weak keys:
# a schema class composed at compile time leaves the cache with its class. Callers get their own copy to mutate.
_JSON_SCHEMAS: weakref.WeakKeyDictionary[type[BaseModel], dict[str, Any]] = weakref.WeakKeyDictionary()


def model_json_schema_once(model: type[BaseModel]) -> dict[str, Any]:
    built = _JSON_SCHEMAS.get(model)
    if built is None:
        built = _JSON_SCHEMAS[model] = model.model_json_schema()
    return copy.deepcopy(built)


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

    timeout_knob: str | None = Field(
        default=None,
        description=(
            "A key in the 'workflow.step_clock' knob feature whose row is this kind of step's "
            "per-attempt limit in seconds, so an admin can turn it; timeout_ms is that row's "
            "mirror when it cannot be read. A node's own data.step_clock still wins."
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
    # INFORMATION NODES (one-graph CONTRACTS §2.1). False = never compiled, never run, never an
    # entry node or a result: ``matrx_graph.information.split_information`` takes every node of
    # such a type out of the graph before validation and compile.
    executes: bool = True
    # Which faces the type has (``detailed`` / ``map`` / ``essentials`` / ``figure``); empty =
    # the generic face. Read by canvas hosts; the engine never does.
    looks: tuple[str, ...] = ()
    # Where the type may be placed: graph kinds (workflow, orchestra, org_chart, topical_map,
    # map, board) or ``*``. Empty = its home graph only (workflow).
    allowed_graphs: tuple[str, ...] = ()
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
    # EMITS ONLY (L-SPEED round 6a): the step's only side effect is a stream emission that is never
    # load-bearing (Show on Screen). Running it again on a resume only shows the same thing again, so
    # it may join a chain of re-runnable steps (scheduler ``_step_defers_outcomes``) whatever its
    # ``determinism`` tier says. Never set it on a step that writes, sends or spends.
    emits_only: bool = False
    # SPENDS (2026-11-09 review: category is not a sign of spending — search.decide is DATA and runs an
    # agent). True: running it can cost money; False: it never does (a pure transform, a database read);
    # None: inferred — only a PURE data/control/io/info step spends nothing, every other step MAY spend.
    # The ONE answer for the spend reader (``spend_gate.may_spend``) and chain eligibility (only a step
    # that spends nothing rides a chain).
    spends: bool | None = None
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
        return model_json_schema_once(self.input_schema)

    def output_json_schema(self) -> dict[str, Any]:
        return model_json_schema_once(self.output_schema)

    def config_json_schema(self) -> dict[str, Any]:
        return model_json_schema_once(self.config_schema)

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
            "executes": self.executes,
            "looks": list(self.looks),
            "allowed_graphs": list(self.allowed_graphs),
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
            # THE LIBRARY GROUP AND TIER (matrx_graph.palette_groups): every surface reads
            # these two fields; none re-derives them.
            **_palette_placement(self.node_type, self.category.value, self.determinism.value),
        }


def _palette_placement(node_type: str, category: str, determinism: str) -> dict[str, str | None]:
    from matrx_graph.palette_groups import palette_group, step_family, step_tier

    group = palette_group(node_type, category, determinism)
    return {
        "group": group,
        "tier": step_tier(node_type, group),
        "family": step_family(node_type, group, category),
    }


def _palette_deprecation(node_type: str) -> dict[str, str] | None:
    from matrx_graph.deprecations import palette_entry

    return palette_entry(node_type)
