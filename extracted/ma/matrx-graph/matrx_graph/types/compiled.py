from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.once import OncePolicy
from matrx_graph.in_organization import InOrganizationPolicy
from matrx_graph.one_at_a_time import OneAtATimePolicy

from matrx_graph.types.channel import ChannelSpec
from matrx_graph.types.input_surface import InputSpec
from matrx_graph.types.primitives import EdgeKind, RetryPolicy
from matrx_graph.types.review import ReviewMark
from matrx_graph.types.variables import VariableSpec


class StepClock(BaseModel):
    """One node's OWN wall-clock limit (``NodeDef.data.step_clock``).

    ``seconds`` is the declared starting limit; ``knob`` (``{feature, key}``)
    names the ``platform.feature_knob`` row an admin turns. The row wins when it
    resolves; an unreadable row falls back to ``seconds`` — never to the
    platform ceiling and never to "no limit".
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    seconds: int = Field(ge=1)
    knob_feature: str | None = None
    knob_key: str | None = None


class CompiledNode(BaseModel):
    """Scheduler-ready view of a node.

    Config has been validated against the registered NodeSpec's config_schema
    and is materialized as a typed BaseModel instance. Incoming/outgoing edges
    are precomputed so super-step scheduling doesn't walk the edge list.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    node_id: str
    spec_type: str
    # The AUTHOR's name for this step ("Study Pack", "Draft the outline"),
    # carried from ``NodeDef.data.label``. The only name the reader has ever
    # seen — a failure that names ``n-l4fuKvk13v`` instead names nothing. None
    # for programmatic definitions that never set one; callers fall back to the
    # node_id only as a last resort.
    label: str | None = None
    config: BaseModel
    # SETTINGS FROM RUN INPUTS (2026-10-27): top-level config fields authored as
    # ``{"$input": name}`` — field → the ref. ``config`` holds the compile-time
    # stand-in (the ref's default, else the field's); the scheduler resolves each
    # ref from the run's inputs and re-validates the config per invocation.
    # Scalar fields only (sizes, counts, flags, short text) — see compile.py.
    config_input_refs: dict[str, dict[str, Any]] = Field(default_factory=dict)
    static_inputs: dict[str, Any] = Field(default_factory=dict)
    incoming_edge_ids: tuple[str, ...]
    outgoing_edge_ids: tuple[str, ...]
    reads_channels: tuple[str, ...]
    writes_channels: tuple[str, ...]
    # Phase 6.2 — per-node mock mode. When ``mock_response`` is set, the
    # scheduler short-circuits this node's executor and returns the
    # contained ``output`` instead, validated against the node's
    # ``output_schema``. Used for fast iteration / dev-without-API-keys.
    # None means "really run the executor" (default). When set, the
    # NodeOutcome gets ``source="mocked"``.
    mock_response: dict[str, Any] | None = None
    # Phase 6.1 — per-node RetryPolicy override. When set, the scheduler
    # uses THIS policy instead of the registered NodeSpec's class-level
    # default (spec.retry). Lets the user dial retries per-node from the
    # inspector without editing the action's code. None = inherit the
    # spec default.
    retry_policy: RetryPolicy | None = None
    # Per-node wall clock (``data.step_clock``). When set it wins over the
    # NodeSpec's ``timeout_ms`` and the platform ceiling for THIS node only —
    # a long step (a podcast produced end to end) declares its own limit
    # instead of the platform default being raised for every step.
    step_clock: StepClock | None = None
    # Run once per key (``data.once``, matrx_graph/once.py): the scheduler reuses a stored
    # success for the same key instead of executing, and claims the key while it executes so
    # concurrent runs wait instead of paying twice. None = an ordinary step (default).
    once: OncePolicy | None = None
    # One at a time per key (``data.one_at_a_time``, matrx_graph/one_at_a_time.py): while another
    # invocation holds this key's turn the step waits (and says so), then works. None = ordinary.
    one_at_a_time: OneAtATimePolicy | None = None
    # Run in another organization the run's person belongs to (``data.in_organization``,
    # matrx_graph/in_organization.py): the host admits the person, then the executor call runs
    # in that organization. None = the run's own organization (default).
    in_organization: InOrganizationPolicy | None = None
    # Set when the node's NodeSpec has ``dynamic_output=True`` (e.g.
    # io.user_input): the JSON Schema computed from this node's config at
    # compile time. Used to generate the run form and for downstream type
    # hints. None for the vast majority of nodes (static output_schema).
    effective_output_schema: dict[str, Any] | None = None
    # Platform kinds (content_ir.kind_definition slugs) this node's I/O
    # conforms to. Seeded from the NodeSpec; a NodeDef may override via
    # ``data.input_kind`` / ``data.output_kind`` (how a workflow author binds
    # an LLM/dynamic node's output to a named Shape). input_kind gates inputs
    # pre-execute (fatal, per-field); output_kind is stamped on the recorded
    # NodeOutcome and validated post-execute; under the live ``workflow_io``
    # enforcement a violation fails the step (``KindContractViolation``).
    input_kind: str | None = None
    output_kind: str | None = None
    # Authored as ``data.output_channel`` on the NodeDef: after this node
    # succeeds (or is mocked), its full output dump is written to the named
    # channel through the channel's reducer. This is the only aggregation
    # path that survives send-driven fan-in — edge routing groups results
    # by target node and merges them last-writer-wins, so N parallel
    # invocations routed over edges collapse to one payload. None (default)
    # means the node writes no channel beyond what its executor does.
    output_channel: str | None = None
    # Join semantics (ENGINE_SPEC §3.3/§3.4/§3.7). Authored on NodeDef.data,
    # validated by validate_definition, consumed by the scheduler's binding
    # accumulator: join_policy decides when a firing is Ready;
    # on_skipped_upstream/skip_defaults govern user_skip upstreams; arg_merge
    # opts specific target args into a declared multi-writer reducer
    # (replace | append | merge | sum) applied in deterministic edge-id
    # order — without it, two writers on one arg is an EdgeRoutingError.
    join_policy: Literal["all", "any"] = "all"
    on_skipped_upstream: Literal["propagate_empty", "block", "default_value"] = "propagate_empty"
    skip_defaults: dict[str, Any] = Field(default_factory=dict)
    arg_merge: dict[str, str] = Field(default_factory=dict)
    # Node Result System — fan-out item-failure policy. Authored as
    # ``data.on_item_failure`` on the WORKER node of a fanned chain
    # (control.map → worker → gather). 'park' (default): a failed item parks
    # the whole run ERRORED, today's behavior. 'hole': the failed item is
    # recorded as an explicit FAILED entry in the aggregated §4.4 dispatch —
    # its structured NodeError rides the items list into control.gather's
    # holes report — and the run survives (one bad URL out of 50 no longer
    # kills a 49-success fan-out).
    on_item_failure: Literal["park", "hole"] = "park"
    # Fail-soft step (``data.optional: true``): a final failure is recorded on the step and its
    # normal edges prune (a branch not taken) instead of parking the run ERRORED.
    optional: bool = False
    # The author's ``data.deliverable`` flag (True/False), None when unset — the override half of
    # THE deliverable rule (``types.deliverables.deliverable_node_ids``), which the scheduler reads
    # twice: an ERROR connection into a deliverable is one of its inputs, never a gate, and a run
    # whose deliverables ALL never ran because a step failed ends FAILED (``deliverable_never_ran``).
    deliverable: bool | None = None
    # Author review mark (``data.review``): each attempt that starts raises one review flag.
    review: ReviewMark | None = None
    # Per-node concurrency cap (ENGINE_SPEC §4.6). Authored as
    # ``data.concurrency``: at most N concurrent invocations of THIS node
    # within a super-step (a per-node semaphore nested inside the run-level
    # step_concurrency bound). None = unbounded (default).
    concurrency: int | None = None
    # ``data.concurrency`` authored as ``{"$input": name}`` (2026-10-27): the cap is read from the
    # run's inputs when the node's gate first opens; ``concurrency`` is then None.
    concurrency_input_ref: dict[str, Any] | None = None
    # Readiness on run facts (``data.ready_when``): dotted run-variable paths that must all be
    # non-empty for the node to fire in a run; unmet -> skipped for the run with a reason.
    ready_when: list[str] = Field(default_factory=list)
    # Kind trigger (KINDS_EVERYWHERE_PLAN §7.7c). Authored as
    # ``data.trigger_kind`` + friends: this node is wired to NOTHING and fires
    # when the named kind appears anywhere in the run's data, at any nesting
    # depth. Set => the node is EXCLUDED from derived entry nodes (it would
    # otherwise look like an entry node and fire at step 1 on nothing) and its
    # firings come from the subscription matcher, never from the join
    # accumulator. None (default) for every ordinary node.
    trigger_kind: str | None = None
    trigger_mode: Literal["all", "each"] = "all"
    trigger_fire_once: bool = False
    trigger_debounce_steps: int = 0
    trigger_item_key: str = "value"


class CompiledEdge(BaseModel):
    model_config = ConfigDict(frozen=True)

    edge_id: str
    source_node_id: str
    target_node_id: str
    source_handle: str | None
    target_handle: str | None
    kind: EdgeKind
    condition: str | None = None
    mappings: dict[str, str] | None = None
    # ENGINE_SPEC §3.2 back-edge exclusion (F13 compat). True when compile's
    # DFS from the entry nodes classified this edge as a cycle back-edge: it
    # is EXCLUDED from its target's required join set and its deliveries open
    # a NEW firing directly (join_policy='any' semantics for the delivery,
    # merged with the node's static inputs) — the Pregel-heritage behavior
    # legacy feedback-edge definitions rely on. Forward edges keep full §3
    # join semantics.
    is_back_edge: bool = False
    # Kind-filtered edges + fan-out modes (KINDS_EVERYWHERE_PLAN §7.3/§7.4).
    # ``kind_filter``: carry only instances of this kind, drawn from wherever
    # they appear in the source payload; an edge whose kind never appears
    # simply PRUNES (a conditional downstream path with zero custom code).
    # ``fan_out``: 'all' (DEFAULT — the whole list to one invocation) or
    # 'each' (one target invocation per instance, over the engine's existing
    # Send machinery). Fan-out is always a deliberate, visible authoring
    # choice, never implicit parallelism (Arman, 2026-08-20). An 'each' edge is
    # EXCLUDED from its target's required join set, exactly like a back-edge:
    # its deliveries open new firings directly instead of resolving a join.
    kind_filter: str | None = None
    fan_out: Literal["all", "each"] = "all"
    item_key: str = "value"
    # Author review mark (``data.review``): each delivery over this edge raises one flag.
    review: ReviewMark | None = None


class CompiledGraph(BaseModel):
    """Immutable, executable form of a workflow.

    Produced by compile(definition, registry). Cached by (definition_version_id)
    hash so the topological analysis and reducer resolution happen once per
    version.

    The nodes and edges collections are keyed for O(1) lookup during execution.
    """

    model_config = ConfigDict(frozen=True)

    definition_hash: str = Field(
        description="Stable hash of the source Definition JSON; cache key."
    )
    nodes: dict[str, CompiledNode]
    edges: dict[str, CompiledEdge]
    channels: dict[str, ChannelSpec]
    entry_node_ids: tuple[str, ...]
    topological_layers: tuple[tuple[str, ...], ...] = Field(
        description=(
            "Layered view for static analysis only (useful for viz, dead-node "
            "detection). Runtime scheduling uses Pregel super-steps, which are "
            "data-dependent and may differ from these layers."
        ),
    )
    strict_channels: bool = False
    public_media: bool = Field(
        default=False,
        description=(
            "Carried from Definition.public_media. When True the scheduler runs "
            "the whole graph inside `public_media_scope()`, so every media "
            "artifact any node generates is born PUBLIC (durable CDN url) "
            "rather than personal (an expiring signed url that dies inside the "
            "node_outcome row that recorded it)."
        ),
    )
    start_when_ready: bool = Field(
        default=False,
        description=(
            "From Definition.metadata['start_when_ready'] is True: the scheduler starts a "
            "step as soon as its last input lands (executor/FEATURE.md § START "
            "WHEN READY), not only one hop past the barrier."
        ),
    )
    source_metadata: dict[str, Any] = Field(default_factory=dict)
    variables: dict[str, VariableSpec] = Field(
        default_factory=dict,
        description=(
            "Declared run variables keyed by name (Definition.variables). "
            "Every {'$var': name} reference in any node's static_inputs was "
            "checked against this at compile time; the scheduler resolves "
            "references against it (declared defaults) + the run's "
            "initial_variables at input-resolution time. LEGACY — folds into "
            "input_surface; dies with the $var → $input definition migration."
        ),
    )
    input_surface: dict[str, InputSpec] = Field(
        default_factory=dict,
        description=(
            "THE compiled workflow input surface (INPUT-SURFACE.md): the "
            "name-unique union of every io.user_input node's fields plus the "
            "declared variables (folded in), keyed by input name. What the "
            "run form, programmatic callers, mandate delivery, and the "
            "workflow-as-tool schema all address — identically. A name "
            "collision was refused at compile time."
        ),
    )
