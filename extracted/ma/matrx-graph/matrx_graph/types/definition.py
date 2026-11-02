from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from matrx_graph.types.channel import ChannelSpec
from matrx_graph.types.primitives import EdgeKind
from matrx_graph.types.review import ReviewMark, parse_review_mark
from matrx_graph.types.variables import VariableSpec


class Viewport(BaseModel):
    model_config = ConfigDict(extra="ignore")

    x: float = 0.0
    y: float = 0.0
    zoom: float = Field(default=1.0, gt=0.0)


class Position(BaseModel):
    model_config = ConfigDict(extra="ignore")

    x: float
    y: float


class NodeDef(BaseModel):
    """User-authored node in a ReactFlow-compatible definition.

    The `data.config` payload is validated against the registered NodeSpec's
    `config_schema` at compile time — not at definition time — so the raw JSON
    round-trips cleanly regardless of whether the target NodeSpec is loaded.
    """

    model_config = ConfigDict(extra="allow")

    id: str = Field(min_length=1, max_length=120)
    type: str = Field(
        min_length=1,
        max_length=120,
        description="NodeSpec.type — must match a registered node type at compile time.",
    )
    position: Position
    data: dict[str, Any] = Field(default_factory=dict)

    @property
    def spec_type(self) -> str:
        """Canonical spec type for engine executor lookup.

        The UI-first data model stores the React Flow visual category in
        `node.type` (e.g. ``"llm"``) and the real dotted spec identifier in
        ``node.data["spec_type"]`` (e.g. ``"ai.chat.manual"``).  When
        ``data.spec_type`` is present it takes precedence; otherwise ``type``
        is used directly (legacy Python API where type was already the dotted
        spec id).
        """
        from_data = self.data.get("spec_type")
        if isinstance(from_data, str) and from_data:
            return from_data
        return self.type

    @property
    def config(self) -> dict[str, Any]:
        """Convenience accessor for the author-time config payload.

        ReactFlow's convention stores arbitrary node payload under `data`. We
        nest config under `data.config` so other fields (label, ui hints) can
        live alongside without colliding.
        """
        cfg = self.data.get("config", {})
        return cfg if isinstance(cfg, dict) else {}

    @property
    def label(self) -> str | None:
        lbl = self.data.get("label")
        return lbl if isinstance(lbl, str) else None

    # --- Join semantics (ENGINE_SPEC §3.3/§3.4/§3.7) -----------------------
    # Recognized ``data`` keys, validated by validate_definition (a bad value
    # fails validation/compilation loudly — these accessors only normalize).

    @property
    def join_policy(self) -> str:
        """ "all" (default): fire when every required inbound edge resolved.
        "any": fire per delivery boundary (explicit multi-fire)."""
        raw = self.data.get("join_policy")
        return raw if isinstance(raw, str) and raw else "all"

    @property
    def on_skipped_upstream(self) -> str:
        """Policy when an upstream resolves via user_skip: "propagate_empty"
        (default, deliver as-is) | "block" | "default_value"."""
        raw = self.data.get("on_skipped_upstream")
        return raw if isinstance(raw, str) and raw else "propagate_empty"

    @property
    def skip_defaults(self) -> dict[str, Any]:
        """Per-target-arg defaults delivered when on_skipped_upstream is
        "default_value". Completeness is a validation error (§3.4)."""
        raw = self.data.get("skip_defaults")
        return raw if isinstance(raw, dict) else {}

    @property
    def arg_merge(self) -> dict[str, str]:
        """Opt-in multi-writer merge: {target_arg: reducer} with the channel
        reducer vocabulary (replace | append | merge | sum), applied in
        deterministic edge-id order (§3.7)."""
        raw = self.data.get("arg_merge")
        if not isinstance(raw, dict):
            return {}
        return {k: v for k, v in raw.items() if isinstance(k, str) and isinstance(v, str)}

    @property
    def on_item_failure(self) -> str:
        """Fan-out item-failure policy (Node Result System): "park" (default —
        a failed fanned item parks the whole run) | "hole" (the failed item
        becomes an explicit error-carrying hole in the aggregated dispatch)."""
        raw = self.data.get("on_item_failure")
        return raw if isinstance(raw, str) and raw else "park"

    @property
    def optional(self) -> bool:
        """Fail-soft step (``data.optional: true``): when it fails for good the failure is
        recorded on the step (``node_failed`` with its reason) and its normal outgoing edges
        PRUNE — exactly like a branch not taken — so the run goes on and completes. A required
        step (the default) still parks the run ERRORED. For side steps off the critical path
        (2026-10-14: one key-people leaf refusing its binding errored every Smart Add round).
        A fan-out whose EVERY item of an optional step failed errors the run (2026-10-22)."""
        return self.data.get("optional") is True

    @property
    def review(self) -> ReviewMark | None:
        """Author review mark (``data.review = {reason, category, label?}``): every attempt
        this step STARTS raises one review flag (source ``flagged_step``, label
        ``review.label`` or ``flagged_step.<node_id>``). None when unmarked or no reason."""
        return parse_review_mark(self.data.get("review"))

    @property
    def ready_when(self) -> list[str]:
        """Readiness on run facts: dotted run-variable paths (``"confirmed.name"``) that must
        each hold a non-empty value for this node to fire in a run. Unmet -> the node is skipped
        for the run (empty output, ``node_skipped`` with ``reason``), never invoked, never billed.
        The reactive pattern: each new confirmed fact starts a run that carries it, and only the
        nodes whose facts are present fire. [] (default) = always ready."""
        raw = self.data.get("ready_when")
        if not isinstance(raw, list):
            return []
        return [p for p in raw if isinstance(p, str) and p.strip()]

    @property
    def concurrency(self) -> int | None:
        """Per-node concurrency cap (ENGINE_SPEC §4.6): at most N concurrent
        invocations of this node within a super-step. None = unbounded."""
        raw = self.data.get("concurrency")
        if isinstance(raw, bool) or not isinstance(raw, int):
            return None
        return raw if raw >= 1 else None

    @property
    def concurrency_input_ref(self) -> dict[str, Any] | None:
        """``data.concurrency`` authored as ``{"$input": name}``: the cap comes from the run's
        inputs (a caller's "at most 2 at a time"), bound per run; the ``workflow.fan_out``
        ceiling still holds it. None when the cap is a literal or absent."""
        from matrx_graph.types.variables import is_input_ref

        raw = self.data.get("concurrency")
        return dict(raw) if is_input_ref(raw) else None


class EdgeDef(BaseModel):
    """User-authored edge in a ReactFlow-compatible definition.

    The edge's semantic `kind` (DATA / CONTROL / CONDITIONAL / ERROR / STREAM)
    lives under data.kind. `type` on ReactFlow is purely a visual style hint.
    Conditional edges carry a predicate expression under data.condition that
    the compiler validates.
    """

    model_config = ConfigDict(extra="allow")

    id: str = Field(min_length=1, max_length=120)
    source: str = Field(min_length=1, max_length=120)
    target: str = Field(min_length=1, max_length=120)
    sourceHandle: str | None = None
    targetHandle: str | None = None
    type: str | None = Field(
        default=None,
        description="ReactFlow visual style hint (e.g. 'smoothstep'). Not the semantic kind.",
    )
    data: dict[str, Any] = Field(default_factory=dict)

    @property
    def kind(self) -> EdgeKind:
        raw = self.data.get("kind", EdgeKind.DATA.value)
        if isinstance(raw, EdgeKind):
            return raw
        try:
            return EdgeKind(raw)
        except ValueError:
            return EdgeKind.DATA

    @property
    def condition(self) -> str | None:
        """Predicate expression for CONDITIONAL edges. None for other kinds."""
        cond = self.data.get("condition")
        return cond if isinstance(cond, str) else None

    @property
    def mappings(self) -> dict[str, str] | None:
        """Declarative payload mapping from source keys to target keys. None if no mapping is provided."""
        maps = self.data.get("mappings")
        return maps if isinstance(maps, dict) else None

    @property
    def review(self) -> ReviewMark | None:
        """Author review mark (``data.review``): every time this connection is TAKEN (its
        payload delivered, never when pruned) one review flag is raised against the TARGET
        step (source ``flagged_path``, label ``review.label`` or ``flagged_path.<edge_id>``)."""
        return parse_review_mark(self.data.get("review"))


class Definition(BaseModel):
    """The canonical workflow definition — ReactFlow-compatible, user-authored.

    This shape matches what the XYFlow canvas posts directly. The backend
    validates it with Pydantic but NEVER rewrites the user's JSON. Compilation
    produces a separate CompiledGraph; the Definition remains the source of
    truth for the UI.
    """

    model_config = ConfigDict(extra="allow")

    version: Literal["1"] = "1"
    nodes: list[NodeDef] = Field(default_factory=list)
    edges: list[EdgeDef] = Field(default_factory=list)
    viewport: Viewport = Field(default_factory=Viewport)
    channels: list[ChannelSpec] = Field(
        default_factory=list,
        description=(
            "Explicitly declared channels. A node that writes to a channel not "
            "declared here gets an implicit 'replace' channel at compile time "
            "unless strict_channels=True."
        ),
    )
    strict_channels: bool = False
    entry_nodes: list[str] = Field(
        default_factory=list,
        description=(
            "Optional. If set, the scheduler starts from these node ids. If empty, "
            "the compiler derives entry nodes (nodes with no incoming edges)."
        ),
    )
    variables: list[VariableSpec] = Field(
        default_factory=list,
        description=(
            "Declared run variables. Node static inputs reference them with "
            "{'$var': name}; run-time initial_variables supply the values. "
            "A reference to an UNDECLARED variable fails compile/validate "
            "loudly (see matrx_graph.types.variables)."
        ),
    )
    public_media: bool = Field(
        default=False,
        description=(
            "True when this workflow's output is PUBLISHED — read by an "
            "anonymous viewer on an episode page, a blog article, a share "
            "page. Every media artifact the run generates is then persisted "
            "PUBLIC, so it gets a permanent CDN url instead of a signed one "
            "that expires. Leave False for private work: a personal image "
            "must not become world-readable because a workflow touched it."
        ),
    )
    metadata: dict[str, Any] = Field(default_factory=dict)

    # THE VERSION IS TEXT, AND "1" IS ALSO 1 (W68, 2026-09-12). A definition
    # posted with ``"version": 1`` (JSON number) answered only ``Input should
    # be '1'`` — the Emergency Conductor sent the same definition seven times,
    # read the answer as a platform bug, and stopped. The integer means exactly
    # the same thing, so accept it; anything else gets a message that says what
    # the value must be instead of echoing the Literal.
    @field_validator("version", mode="before")
    @classmethod
    def _coerce_version(cls, value: Any) -> Any:
        if isinstance(value, bool):
            raise ValueError('version must be the text "1"')
        if isinstance(value, int) and value == 1:
            return "1"
        if isinstance(value, float) and value == 1.0:
            return "1"
        if value is None or value == "1":
            return "1"
        raise ValueError('version must be the text "1"')

    @model_validator(mode="after")
    def _check_ids_unique(self) -> Definition:
        node_ids = [n.id for n in self.nodes]
        if len(node_ids) != len(set(node_ids)):
            duplicates = {nid for nid in node_ids if node_ids.count(nid) > 1}
            raise ValueError(f"Duplicate node ids: {sorted(duplicates)}")

        edge_ids = [e.id for e in self.edges]
        if len(edge_ids) != len(set(edge_ids)):
            duplicates = {eid for eid in edge_ids if edge_ids.count(eid) > 1}
            raise ValueError(f"Duplicate edge ids: {sorted(duplicates)}")

        channel_names = [c.name for c in self.channels]
        if len(channel_names) != len(set(channel_names)):
            duplicates = {cn for cn in channel_names if channel_names.count(cn) > 1}
            raise ValueError(f"Duplicate channel names: {sorted(duplicates)}")

        variable_names = [v.name for v in self.variables]
        if len(variable_names) != len(set(variable_names)):
            duplicates = {vn for vn in variable_names if variable_names.count(vn) > 1}
            raise ValueError(f"Duplicate variable names: {sorted(duplicates)}")

        return self
