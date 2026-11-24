from __future__ import annotations

import difflib
import logging
import re
from typing import Any

from matrx_utils.suggest import format_options, suggestion_line
from pydantic import BaseModel, ValidationError

from matrx_graph.nodes._sandbox import validate_expression
from matrx_graph.diagnostics.compile_validation import (
    config_extra_is_input_hint,
    scream_node_config_rejected,
)
from matrx_graph.errors import MatrxGraphError
from matrx_graph.deprecations import deprecation_for, deprecation_message
from matrx_graph.executor.registry import NodeRegistry, canonical_spec_type, default_registry
from matrx_graph.mapping_sources import (
    WHOLE_PAYLOAD,
    dotted_target_message,
    unknown_sigil,
    unknown_sigil_message,
)
from matrx_graph.paths import first_segment as first_path_segment
from matrx_graph.paths import path_syntax_problem
from matrx_graph.shape_probe import (
    TEMPLATE_HOSTS,
    declared_field_names,
    is_described,
    item_schema_of,
    model_json_schema,
    path_problem,
    resolve_ref,
    schema_at_path,
    template_item_paths,
)
from matrx_graph.text_inputs import text_only as _text_only_input
from matrx_graph.types.definition import Definition, EdgeDef
from matrx_graph.types.handle import (
    HandleDirection,
    config_output_handles,
    normalized_config_output_fields,
)
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import EdgeKind
from matrx_graph.types.usl import RENDERS_TEMPLATE_KEY
from matrx_graph.types.variables import is_input_ref, iter_input_refs, iter_var_refs

_log = logging.getLogger(__name__)

# Registered node-type list bound in the "unknown node type" message —
# closest-first, capped, with a remainder count (there can be many types).
_UNKNOWN_TYPE_LIST_CAP = 15

# Tombstones for node types the engine DELETED — a definition still using
# one gets a loud, actionable error instead of the generic "unknown node
# type" (which would suggest a registration bug rather than a removal).
REMOVED_NODE_TYPES: dict[str, str] = {
    "control.barrier": (
        "control.barrier was removed — map fan-ins synchronize "
        "automatically; use control.gather. Cross-branch synchronization "
        "needs no node at all: a step with multiple inbound connections "
        "fires exactly once, when every connection has resolved "
        "(ENGINE_SPEC §3/§6.1)."
    ),
    "research.capture.save_many": (
        "research.capture.save_many was removed — use the Save research to a topic "
        "unit (research.save_to_topic)."
    ),
    "ai.search.rank_sources": (
        "ai.search.rank_sources was removed — use the Find pages for a keyword unit "
        "(web.find_pages), which ranks with research.source_authority."
    ),
    "ai.extract": (
        "ai.extract (Extract with AI) was removed — use Ask AI (ai.llm.chat) with an "
        "output_schema: text -> prompt, instruction -> system_instruction, "
        "schema_definition -> output_schema; downstream reads extracted_data -> "
        "structured_output and raw_response -> final_text."
    ),
    **{
        removed: (
            f"{removed} was removed (2026-10-29) — its prompt was an agent hidden in node code. "
            "Use the saved workflow 'Image production' (f02ba908-5679-4052-a895-93a2b0564b90) "
            "as a Run Workflow step, or a Run Typed Agent step on the agent you choose."
        )
        for removed in ("ai.image.concept_generate", "ai.image.prompt_write", "ai.image.qc_judge")
    },
    "ai.agent.tool_calling": (
        "ai.agent.tool_calling (Agent with Tools) was removed (2026-10-29) — use Custom AI "
        "Call (ai.chat.manual): same model, user_input, system_instruction, tools and "
        "max_iterations; or Run Agent (ai.agent.start) when a saved agent does the job."
    ),
    "ai.agent.react": (
        "ai.agent.react (Agent with Visible Reasoning) was removed (2026-10-29) — use Custom "
        "AI Call (ai.chat.manual) and set its reasoning_effort; its react_trace output is gone."
    ),
}

# Node types whose config.target_node_id names another node on the same
# canvas — validated so a typo'd target fails at save time, badged on the
# dispatcher, instead of at runtime. Extend when adding a dispatcher node.
DISPATCHER_NODE_TYPES: frozenset[str] = frozenset(
    {"control.map", "control.send", "control.loop", "control.work_queue"}
)

# Steps built to receive a fan-in's collected list whose input schema takes it
# as an extra rather than a declared `items` field (control.gather is extra=allow).
_COLLECTOR_NODE_TYPES: frozenset[str] = frozenset({"control.gather"})

# Join-semantics NodeDef.data keys (ENGINE_SPEC §3.3/§3.4/§3.7).
_JOIN_POLICIES = ("all", "any")
_SKIP_POLICIES = ("propagate_empty", "block", "default_value")
# §3.3b — what a step does when a step it reads from was skipped by its 'Only when'.
_WHEN_INPUT_SKIPPED = ("skip", "run")
# Node Result System — fan-out item-failure policy (data.on_item_failure).
_ITEM_FAILURE_POLICIES = ("park", "hole")
# The channel-reducer vocabulary sanctioned for arg_merge (§3.7) — a subset
# of executor/channels.py reducers (last_writer_wins/topic_map are
# channel-only concepts).
_ARG_MERGE_REDUCERS = ("replace", "append", "merge", "sum")

# A node is a Plan anchor in BOTH identities or in NEITHER. ``node.type`` is the
# renderer Studio draws; ``data.spec_type`` is what the engine runs. A resolve
# rewrites both ATOMICALLY (matrx_graph.patch.UpdateNodeTypeOp beside
# UpdateNodeDataOp) — this check is the forcing function that makes any future
# path which rewrites only one of them fail the save gate instead of leaving a
# Plan card drawn over an already-settled step (live defect, 2026-08-20:
# definition 33c69869 node p1 sat at type='plan' / spec_type='data.transform'
# with its plan row already phase=resolved).
_PLAN_IDENTITY_PREFIX = "plan."
_PLAN_IDENTITY_ROOT = "plan"


#: Config keys that hold a sandboxed expression (data.transform, data.assert,
#: math.evaluate, output.to_frontend). Validated with the SAME AST gate the
#: runtime uses, so a definition never saves with a formula the run refuses.
_EXPRESSION_CONFIG_KEYS: tuple[str, ...] = ("expression", "transform_expression")


def _is_plan_identity(value: str | None) -> bool:
    """True for the Plan renderer category ("plan") and any Plan spec
    ("plan.step"). Concrete specs that merely start with the letters — there
    are none today, and a dotted prefix match keeps it that way — are excluded
    by requiring the separator."""
    if not value:
        return False
    return value == _PLAN_IDENTITY_ROOT or value.startswith(_PLAN_IDENTITY_PREFIX)


# Mapping source values that address the whole payload / are not a field path,
# so they must never be checked against the source's declared output schema.
# The vocabulary itself is canonical in ``matrx_graph.mapping_sources`` — every
# layer that reads a mapping source shares it.
_WHOLE_PAYLOAD_SOURCE = WHOLE_PAYLOAD

# Host-injected ADMISSION request models — node_type → the canonical request
# model the node constructs at RUN time (e.g. ai.agent.start builds the host's
# AgentStartRequest from its inputs). The node's own input_schema is
# deliberately permissive (extra="allow" variable ports), so a static value
# the run-time request model rejects (an unregistered source_feature, a
# malformed ToolSpec) used to pass /validate and only explode after a PAID run
# started. Registering the model here lets validate_definition exercise its
# FIELD validators over the node's authored static inputs — validators only,
# no execution, no construction of a complete request.
_ADMISSION_REQUEST_MODELS: dict[str, type[BaseModel]] = {}


def register_admission_request_model(node_type: str, model: type[BaseModel]) -> None:
    """Bind a run-time request model to a node type for static-input admission.

    Called by the host (or a package's ``configure()``) at startup. During
    ``validate_definition`` every authored static input field that is also a
    declared field on ``model`` is validated through the model's field
    validators; failures surface as normal per-node validation errors instead
    of run-time crashes. Fields fed at run time (edges, run variables) are
    never checked — only static literals are.
    """
    _ADMISSION_REQUEST_MODELS[node_type] = model


def _static_input_admission_issues(node: Any, raw_static: dict[str, Any]) -> list[ValidationIssue]:
    """Validate a node's authored static inputs against its admission model.

    Rules (deliberately conservative — this must NEVER reject a definition a
    run would accept):
      * only keys that are DECLARED fields on the request model are checked
        (extras are agent-variable ports, never request fields);
      * a value carrying a ``{"$var": ...}`` reference anywhere is skipped —
        it resolves at run time;
      * ``missing``-type errors are dropped (required run-time fields like
        ``conversation_id`` are supplied by the node executor, not the author);
      * only errors rooted at a checked field are kept (no root-model errors —
        the candidate is a partial request by construction).
    """
    model = _ADMISSION_REQUEST_MODELS.get(node.spec_type)
    if model is None:
        return []
    declared_fields = set(model.model_fields)
    candidate = {
        key: value
        for key, value in raw_static.items()
        if key in declared_fields and not iter_var_refs(value) and not iter_input_refs(value)
    }
    if not candidate:
        return []
    try:
        model.model_validate(candidate)
    except ValidationError as e:
        issues: list[ValidationIssue] = []
        for err in e.errors():
            if err["type"] == "missing":
                continue
            loc = err["loc"]
            if not loc or str(loc[0]) not in candidate:
                continue
            path = ".".join(str(p) for p in loc)
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].data.input.{path}",
                    node_id=node.id,
                    message=(
                        f"Static input rejected by the run-time request contract "
                        f"({model.__name__}): {err['msg']}"
                    ),
                )
            )
        return issues
    return []


def _source_path_problem(model: type[BaseModel], source_key: str) -> str | None:
    """Why ``source_key`` can NEVER resolve against ``model``'s output — or None.

    Thin wrapper over ``matrx_graph.shape_probe.path_problem`` (THE ONE probe,
    shared with the ``$item`` template check below and with the authoring tool's
    shape digest).
    """
    return path_problem(model_json_schema(model), source_key)


def _schema_props(model: type[BaseModel]) -> tuple[set[str], bool]:
    """Return (top-level property names, schema_is_closed) for a model.

    ``schema_is_closed`` is True only when the model forbids extra keys
    (``model_config = ConfigDict(extra="forbid")`` → ``additionalProperties:
    false``). An OPEN schema (``extra="allow"`` or the default) legitimately
    carries keys beyond the declared ones, so a mapping against a key absent
    from an open schema is NOT worth a warning — only a typo against a CLOSED
    schema is a high-signal finding.
    """
    schema = model_json_schema(model)  # cached per class; {} when it won't render
    props = set(schema.get("properties", {}).keys())
    is_closed = schema.get("additionalProperties") is False
    return props, is_closed


def _accepted_input_names(model: type[BaseModel]) -> set[str] | None:
    """Every input name ``model`` accepts (field names and their aliases), or None when it takes any name.

    Only a model that FORBIDS extra keys refuses a name: the default (``ignore``) drops it and ``allow``
    keeps it, so neither can ever refuse a step for an unknown input."""
    if (getattr(model, "model_config", None) or {}).get("extra") != "forbid":
        return None
    names: set[str] = set()
    for name, field in model.model_fields.items():
        names.add(name)
        for alias in (field.alias, field.validation_alias):
            names |= _alias_input_names(alias)
    return names


def _alias_input_names(alias: object) -> set[str]:
    """The top-level input names one alias accepts: a plain name, every member of an ``AliasChoices``, and
    the first key of an ``AliasPath`` (``AliasPath("a", 0)`` reads input ``a``)."""
    from pydantic import AliasChoices, AliasPath

    if isinstance(alias, str):
        return {alias}
    if isinstance(alias, AliasChoices):
        return set().union(*(_alias_input_names(choice) for choice in alias.choices))
    if isinstance(alias, AliasPath):
        return {alias.path[0]} if alias.path and isinstance(alias.path[0], str) else set()
    return set()


def unaccepted_input_issues(
    raw: dict[str, Any] | Definition, registry: NodeRegistry | None = None
) -> list[ValidationIssue]:
    """Steps handed an input name their action or node refuses — ERRORS, each naming the step and the field.

    A step whose input model forbids extra keys refuses, at run time, every name it does not declare
    (``spec.input_schema.model_validate(merged)``: extra_forbidden). Two places hand a step names: its
    fixed inputs (``data.input``, else ``data.inputs``) and the target keys of its connections' field
    links (``data.mappings``). A name the step does not take there fails EVERY run that reaches the step
    (research triage 7f6f480b v11, 2026-11-10: ``log.record`` given ``category``, a setting, as an
    input — each run errored there and the keyword read stopped). Publish refuses it instead.

    A third place is a For each's per-item payload (``config.payload_template`` keys, a ``data.for_each``
    step's ``as``): checked against the step it runs once per item. The check reads the graph the
    engine runs (built-in step settings expanded, information nodes out), so a link into a step with
    an 'Only when' reaches its gate, which hands the step only the names it takes.

    Never refuses what a run accepts: an open model (``extra`` ``allow`` / ``ignore``), an unknown or
    non-running step type and ``__``-prefixed markers are skipped; input names a step's settings
    expose as connection points count as accepted, and so does the input a 'Run in another
    organization' setting reads (``data.in_organization.input``: consumed before the check; Knowledge
    buckets 6b86c945 v41's per-item ``organization_id``). A definition whose step settings do not expand is
    left to the compile gate (no issues here)."""
    from matrx_graph.in_organization import parse_in_organization
    from matrx_graph.information import split_information
    from matrx_graph.step_settings import StepSettingError, expand_step_settings

    registry = registry or default_registry()
    definition = raw if isinstance(raw, Definition) else Definition.model_validate(raw)
    try:
        definition = split_information(expand_step_settings(definition), registry).executable
    except StepSettingError:
        return []
    accepted: dict[str, set[str]] = {}
    issues: list[ValidationIssue] = []
    for node in definition.nodes:
        try:
            spec = registry.get(node.spec_type).spec
        except Exception:  # noqa: BLE001 — an unknown step type is the compile gate's refusal
            continue
        if not spec.executes or spec.is_source:
            continue
        names = _accepted_input_names(spec.input_schema)
        if names is None:
            continue
        config = node.data.get("config") if isinstance(node.data.get("config"), dict) else {}
        for field_name, field in spec.config_schema.model_fields.items():
            extra = field.json_schema_extra
            exposed = config.get(field_name)
            if isinstance(extra, dict) and extra.get("workflow_input_handles") is True and isinstance(exposed, list):
                names |= {n for n in exposed if isinstance(n, str)}
        try:
            policy = parse_in_organization(node.data.get("in_organization"))
        except ValueError:  # a bad setting is the compile gate's refusal
            policy = None
        if policy is not None and policy.input:
            # 'Run in another organization' reads this input and removes it before the step's inputs are
            # checked when the step does not take it (in_organization.consume_setting_input).
            names = names | {str(policy.input).split(".", 1)[0]}
        accepted[node.id] = names
        fixed = node.data.get("input") if isinstance(node.data.get("input"), dict) else node.data.get("inputs")
        where = "input" if isinstance(node.data.get("input"), dict) else "inputs"
        for key in fixed if isinstance(fixed, dict) else {}:
            if str(key).startswith("__") or key in names:
                continue
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].data.{where}.{key}",
                    node_id=node.id,
                    code="input_not_accepted",
                    message=(
                        f"Step '{node.id}' ({spec.node_type}) is given the fixed input '{key}', which it "
                        f"does not take: every run would fail there. It takes {format_options(sorted(names), 12)}."
                    ),
                )
            )
    for node in definition.nodes:
        config = node.data.get("config") if isinstance(node.data.get("config"), dict) else {}
        target, template = config.get("target_node_id"), config.get("payload_template")
        names = accepted.get(str(target or ""))
        if names is None or not isinstance(template, dict):
            continue
        for key in template:
            if str(key).startswith("__") or key in names:
                continue
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].data.config.payload_template.{key}",
                    node_id=str(target),
                    code="input_not_accepted",
                    message=(
                        f"Step '{target}' ({definition_node_type(definition, str(target))}) is given the input "
                        f"'{key}' for each item by '{node.id}', which it does not take: every run would fail "
                        f"there. It takes {format_options(sorted(names), 12)}."
                    ),
                )
            )
    for edge in definition.edges:
        names = accepted.get(edge.target)
        mappings = edge.data.get("mappings")
        if names is None or not isinstance(mappings, dict) or edge.kind is EdgeKind.STREAM:
            continue
        for key in mappings:
            if str(key).startswith("__") or key in names:
                continue
            target_type = definition_node_type(definition, edge.target)
            issues.append(
                ValidationIssue(
                    path=f"edges[{edge.id}].data.mappings.{key}",
                    node_id=edge.target,
                    edge_id=edge.id,
                    code="input_not_accepted",
                    message=(
                        f"Step '{edge.target}' ({target_type}) is given the input '{key}' by connection "
                        f"'{edge.id}' from '{edge.source}', which it does not take: every run would fail "
                        f"there. It takes {format_options(sorted(names), 12)}."
                    ),
                )
            )
    return issues


def definition_node_type(definition: Definition, node_id: str) -> str:
    """The step type of ``node_id`` in ``definition`` ('' when absent)."""
    return next((n.spec_type for n in definition.nodes if n.id == node_id), "")


class ValidationIssue(BaseModel):
    """A single problem with a Definition. Rendered as a badge in the UI."""

    path: str
    message: str
    node_id: str | None = None
    edge_id: str | None = None
    severity: str = "error"
    #: What kind of finding it is, when a reader orders or groups by it (``unknown_step_key``).
    code: str | None = None
    #: The settings/inputs a finding is about, by their stored names (``missing_input``: the required inputs
    #: nothing supplies), so a host words the sentence without parsing ``message``.
    fields: list[str] = []


class ValidationResult(BaseModel):
    valid: bool
    issues: list[ValidationIssue] = []


#: Warnings that are only notices — a key nothing reads. They sort after every error and every other
#: warning, so a reader that shows "the first issue" (a compile sentence, a publish's open-plan list)
#: never shows a notice ahead of what matters.
NOTICE_CODES = frozenset({"unknown_step_key"})


def ordered_issues(issues: list[ValidationIssue]) -> list[ValidationIssue]:
    """Errors first, then warnings, then notices (:data:`NOTICE_CODES`); stable within each."""
    def rank(issue: ValidationIssue) -> int:
        if issue.severity == "error":
            return 0
        return 2 if issue.code in NOTICE_CODES else 1

    return sorted(issues, key=rank)


def _reads_run(value: Any) -> bool:
    """True when ``value`` holds a ``{"$run": …}`` reference or a ``{run.…}`` text placeholder."""
    if isinstance(value, dict):
        return "$run" in value or any(_reads_run(v) for v in value.values())
    if isinstance(value, list):
        return any(_reads_run(v) for v in value)
    return isinstance(value, str) and ("{run." in value or "{run}" in value)


def _once_reads_run_issues(node_id: str, data: Any) -> list[ValidationIssue]:
    """``data.once`` + ``$run`` is a trap either way: in the inputs the run id is part of the
    reuse key, so the step never reuses; in the settings it is outside the key, so a reused
    result carries the FIRST run's id. A warning (validation offers, never blocks)."""
    if not isinstance(data, dict) or data.get("once") is None:
        return []
    found: list[ValidationIssue] = []
    inputs = data.get("input") if data.get("input") is not None else data.get("inputs")
    if _reads_run(inputs):
        found.append(
            ValidationIssue(
                path=f"nodes[{node_id}].data.input",
                node_id=node_id,
                severity="warning",
                message=(
                    "This step runs once per key, but its inputs read the run ($run): the run id "
                    "changes every run, so a saved result is never reused. Stamp the run on a "
                    "later step that is not run-once."
                ),
            )
        )
    if _reads_run(data.get("config")):
        found.append(
            ValidationIssue(
                path=f"nodes[{node_id}].data.config",
                node_id=node_id,
                severity="warning",
                message=(
                    "This step runs once per key, but its settings read the run ($run), which "
                    "the reuse key leaves out: a reused result carries the FIRST run's id. Stamp "
                    "the run on a later step that is not run-once."
                ),
            )
        )
    return found


def _per_item_steps(definition: Definition) -> dict[str, bool]:
    """Every step that runs once per item (a dispatcher's ``target_node_id``, a For each expanded to one,
    an ``each`` connection's target) → whether its items have a known total (always True since 2026-11-19: a
    paced ``until`` For each still knows its list's length, which ``{total}`` says)."""
    out: dict[str, bool] = {}
    for node in definition.nodes:
        if node.spec_type not in DISPATCHER_NODE_TYPES:
            continue
        config = (node.data or {}).get("config") if isinstance(node.data, dict) else None
        config = config if isinstance(config, dict) else {}
        target = config.get("target_node_id")
        if isinstance(target, str) and target and target != node.id:
            out[target] = out.get(target, True)
    for edge in definition.edges:
        if isinstance(edge.data, dict) and edge.data.get("fan_out") == "each":
            out.setdefault(edge.target, True)
    return out


def _says_issues(node_id: str, data: Any, per_item: dict[str, bool]) -> list[ValidationIssue]:
    """``data.says`` (matrx_graph/says.py): a malformed row, and a placeholder that can never have a value for
    its row type (F4: ``{result.x}`` on start, ``{error}`` outside the failure rows, counts and the per-item rows
    on a step with no For each). An error: the definition saves and
    keeps editing, publish refuses it with the sentence."""
    if not isinstance(data, dict) or not data.get("says"):
        return []
    from matrx_graph.says import parse_says, row_problems

    path = f"nodes[{node_id}].data.says"
    try:
        policy = parse_says(data.get("says"))
    except ValueError as e:
        return [ValidationIssue(path=path, node_id=node_id, code="says_invalid", message=f"What this step says: {e}.")]
    if policy is None:
        return []
    return [
        ValidationIssue(path=path, node_id=node_id, code="says_never_has_a_value", message=f"What this step says: {p}.")
        for p in row_problems(policy, per_item=node_id in per_item)
    ]


def _review_mark_issues(
    raw: Any, path: str, *, node_id: str | None = None, edge_id: str | None = None
) -> list[ValidationIssue]:
    """``data.review`` author mark (review flags): an object with a non-empty ``reason`` and a
    ``category`` from ``run_log.CATEGORIES``. Offers, never blocks — a warning, and the run
    reads an unusable mark as unmarked / an unknown category as ``other``."""
    if raw is None:
        return []
    from matrx_graph.run_log import CATEGORIES

    def issue(sub: str, message: str) -> ValidationIssue:
        return ValidationIssue(
            path=f"{path}{sub}", node_id=node_id, edge_id=edge_id, message=message, severity="warning"
        )

    if not isinstance(raw, dict):
        return [issue("", "Review mark must be an object with a reason and a category.")]
    found: list[ValidationIssue] = []
    reason = raw.get("reason")
    if not isinstance(reason, str) or not reason.strip():
        found.append(issue(".reason", "Review mark needs a reason — it is not raised without one."))
    category = raw.get("category")
    if category is not None and category not in CATEGORIES:
        found.append(
            issue(".category", f"Unknown review category {category!r}; it is recorded as 'other'. "
                  f"Allowed: {', '.join(CATEGORIES)}.")
        )
    label = raw.get("label")
    if label is not None and (not isinstance(label, str) or not label.strip()):
        found.append(issue(".label", "Review label must be a non-empty text key when set."))
    return found


def normalize_config_output_handles(
    definition: Definition,
    registry: NodeRegistry | None = None,
) -> Definition:
    """``definition`` with every config-declared handle list recomputed.

    THE SAVE TWIN of :func:`config_output_handles`: a handle list stored in a
    node's config (``option_keys``, ``route_keys``, ``question_names``…) is
    derived by the node's config model, so what is persisted is what the
    model computes — never a stale or missing copy some writer sent. Only the
    marker fields are rewritten; every other config key is left exactly as
    written, and a node whose type is unknown or whose config does not
    validate is left untouched (the validator reports it). Returns a copy;
    the input is not mutated.
    """
    registry = registry or default_registry()
    changed = False
    nodes = []
    for node in definition.nodes:
        config = node.data.get("config") if isinstance(node.data, dict) else None
        if not isinstance(config, dict) or not registry.has(node.spec_type):
            nodes.append(node)
            continue
        fields = normalized_config_output_fields(registry.get(node.spec_type).spec, config)
        if not fields or all(config.get(name) == value for name, value in fields.items()):
            nodes.append(node)
            continue
        changed = True
        nodes.append(
            node.model_copy(update={"data": {**node.data, "config": {**config, **fields}}})
        )
    return definition.model_copy(update={"nodes": nodes}) if changed else definition


def _misspelled_edge_key_issues(definition: Definition) -> list[ValidationIssue]:
    """REFUSE an edge key that spells an engine field the engine never reads.

    ``EdgeDef`` keeps ``extra="allow"`` because the definition is the canvas's
    ReactFlow JSON verbatim (``animated``, ``style``, ``label`` …) and the
    backend never rewrites it. But a snake_case spelling of a field the engine
    ROUTES on (``source_handle`` for ``sourceHandle``) is not a visual key: it
    is accepted, ignored, and every branch handle then delivers — a silent
    misroute. Normalizing would rewrite the author's JSON; refusing names the
    one fix. Rule: an extra key whose camelCase form is a declared field."""
    found: list[ValidationIssue] = []
    for edge in definition.edges:
        for key in sorted(edge.model_extra or {}):
            parts = key.split("_")
            camel = parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:])
            if camel != key and camel in EdgeDef.model_fields:
                found.append(
                    ValidationIssue(
                        path=f"edges[{edge.id}].{key}",
                        edge_id=edge.id,
                        message=(
                            f"Unknown edge key '{key}': the engine reads '{camel}'. "
                            f"'{key}' is ignored, so this connection would route as if "
                            f"it had no {camel}. Rename it to '{camel}'."
                        ),
                    )
                )
    return found


def _unknown_step_key_issues(definition: Definition) -> list[ValidationIssue]:
    """SAY a step key nothing reads. A step's ``data`` is free-form (the canvas's JSON, kept verbatim), so a key
    the engine does not have is accepted and ignored: ``on_failure: continue`` looked like error handling and
    did nothing. Generic: any ``data`` key outside ``STEP_DATA_KEYS`` warns by name, and a step-data key written
    on the step itself (beside ``data``) warns with where it belongs. A warning, never a refusal: a key only the
    canvas uses must not stop a save."""
    from matrx_graph.types.definition import STEP_DATA_KEYS

    found: list[ValidationIssue] = []
    for node in definition.nodes:
        for key in sorted(set(node.data) - STEP_DATA_KEYS):
            found.append(ValidationIssue(
                path=f"nodes[{node.id}].data.{key}", node_id=node.id, severity="warning", code="unknown_step_key",
                message=(f"Unknown step key '{key}': nothing reads it, so it does nothing. Remove it, or use the "
                         "setting that does this (a step's inputs and settings are under 'input' and 'config').")))
        # An empty key (the shared graph wire always carries width/height, null when unset) writes nothing to warn about.
        for key in sorted({k for k, v in (node.model_extra or {}).items() if v is not None} & STEP_DATA_KEYS):
            found.append(ValidationIssue(
                path=f"nodes[{node.id}].{key}", node_id=node.id, severity="warning", code="unknown_step_key",
                message=(f"'{key}' is written on the step itself, where nothing reads it. Move it under the "
                         f"step's 'data' (data.{key}).")))
    return found


def validate_definition(
    raw: dict[str, Any] | Definition,
    registry: NodeRegistry | None = None,
    *,
    workflow_id: str = "",
    workflow_name: str = "",
) -> ValidationResult:
    """Validate a ReactFlow-shaped definition against the engine + registry.

    Runs in two phases:
        1. Pydantic structural validation (unknown fields preserved; required
           fields checked; duplicate ids rejected).
        2. Registry-aware semantic validation — every `node.type` must be a
           registered node type, every edge's source/target must exist, and
           every handle referenced must be declared on the NodeSpec.

    Returns a ValidationResult the router can return directly — UI reads
    `issues[*].node_id` / `edge_id` to render per-element badges.
    """
    registry = registry or default_registry()
    issues: list[ValidationIssue] = []

    if isinstance(raw, Definition):
        definition = raw
    else:
        try:
            definition = Definition.model_validate(raw)
        except ValidationError as e:
            for err in e.errors():
                loc = ".".join(str(p) for p in err["loc"])
                issues.append(
                    ValidationIssue(
                        path=loc or "<root>",
                        message=err["msg"],
                        severity="error",
                    )
                )
            return ValidationResult(valid=False, issues=issues)

    issues.extend(_unsaved_chat_issues(definition))

    # Built-in step settings (Only when / If skipped / Shape the result) are validated as the
    # real steps they become; every issue on a helper step is badged on the step the author
    # wrote (matrx_graph/step_settings.py).
    from matrx_graph.step_settings import StepSettingError, expand_step_settings

    try:
        definition = expand_step_settings(definition)
    except StepSettingError as e:
        return ValidationResult(
            valid=False,
            issues=[*issues, ValidationIssue(path=f"nodes[{e.node_id}].data", node_id=e.node_id, message=str(e))],
        )
    # Information nodes (notes, frames, media, kinds, records) never run: check them on their own,
    # then validate the executable graph without them (matrx_graph/information.py).
    from matrx_graph.information import information_problems, split_information

    for problem in information_problems(definition, registry):
        issues.append(
            ValidationIssue(path=problem.path, node_id=problem.node_id, edge_id=problem.edge_id, message=problem.message)
        )
    definition = split_information(definition, registry).executable
    result = _validate_expanded(definition, registry, issues, workflow_id=workflow_id, workflow_name=workflow_name)
    return _badge_helpers_on_their_step(result)


def _unsaved_chat_issues(definition: Definition) -> list[ValidationIssue]:
    """A person can always open the full chat of anything AI that runs (Arman, 2026-11-08: "A
    user should always be able to see the full chat for anything that runs"). A step that sets
    ``store: false`` (in its inputs or its per-item template) runs the agent and keeps no chat,
    so nobody can ever see what it was asked or what it said. Only a dry run (a preview that
    never calls the model) may skip saving. Read on the steps as written, before step settings
    expand a per-item template. A warning: validation offers, never blocks."""
    found: list[ValidationIssue] = []
    for node in definition.nodes:
        data = node.data if isinstance(node.data, dict) else {}
        for_each = data.get("for_each") if isinstance(data.get("for_each"), dict) else {}
        template = for_each.get("payload_template") if isinstance(for_each.get("payload_template"), dict) else {}
        for where, values in (("inputs", data.get("inputs")), ("config", data.get("config")),
                              ("for_each.payload_template", template)):
            if not isinstance(values, dict) or values.get("store") is not False or values.get("dry_run") is True:
                continue
            found.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].data.{where}.store",
                    node_id=node.id,
                    severity="warning",
                    message=(
                        "This step keeps no chat (store is off), so nobody can open what its agent "
                        "was asked or answered. Remove store: false."
                    ),
                )
            )
    return found


def _badge_helpers_on_their_step(result: ValidationResult) -> ValidationResult:
    from matrx_graph.step_settings import owner_of

    issues = [
        issue.model_copy(update={"node_id": owner}) if (owner := owner_of(issue.node_id)) else issue
        for issue in result.issues
    ]
    return result.model_copy(update={"issues": ordered_issues(issues)})


def _validate_expanded(
    definition: Definition,
    registry: NodeRegistry,
    issues: list[ValidationIssue],
    *,
    workflow_id: str,
    workflow_name: str,
) -> ValidationResult:
    issues.extend(_misspelled_edge_key_issues(definition))

    node_ids: set[str] = set()
    node_definitions = {node.id: node for node in definition.nodes}
    per_item_steps = _per_item_steps(definition)
    # node_id → resolved NodeSpec, populated only for nodes whose type is
    # registered. Edge-level checks (handles, mappings) read it; an unknown
    # or removed type is skipped there (already reported as a node error).
    node_specs: dict[str, NodeSpec] = {}
    for node in definition.nodes:
        node_ids.add(node.id)
        raw_spec_type = node.data.get("spec_type")
        if isinstance(raw_spec_type, str) and raw_spec_type:
            spec_is_plan = _is_plan_identity(raw_spec_type)
            if spec_is_plan != _is_plan_identity(node.type):
                issues.append(
                    ValidationIssue(
                        path=f"nodes[{node.id}].type",
                        node_id=node.id,
                        message=(
                            f"Node renderer type '{node.type}' and executable "
                            f"spec_type '{raw_spec_type}' disagree about whether "
                            "this is a Plan anchor. A Plan node is a Plan in both "
                            "or in neither: resolving one must rewrite the other "
                            "in the same patch (update_node_type beside "
                            "update_node_data), or Studio draws a Plan card over "
                            "a step that already settled."
                        ),
                    )
                )
        # DEPRECATED STEPS scream on EVERY validation — so every write door (create,
        # save, publish, validate, the agent tools, the Conductor) warns the same way.
        # A warning, never a refusal (validation offers, never blocks).
        deprecation = deprecation_for(node.spec_type)
        if deprecation is not None:
            message = deprecation_message(
                deprecation,
                display_name=(
                    registry.get(node.spec_type).spec.display_name
                    if registry.has(node.spec_type)
                    else node.spec_type
                ),
                node_id=node.id,
                workflow_name=workflow_name,
                workflow_id=workflow_id,
            )
            _log.info("[workflow validate] %s", message)
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].type",
                    node_id=node.id,
                    message=message,
                    severity="warning",
                )
            )
        removed_key = canonical_spec_type(node.spec_type)
        if removed_key in REMOVED_NODE_TYPES:
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].type",
                    node_id=node.id,
                    message=REMOVED_NODE_TYPES[removed_key],
                )
            )
            continue
        if not registry.has(node.spec_type):
            known = registry.all_types()
            hint = suggestion_line(node.spec_type, known, noun="node type")
            closest_first = sorted(
                known,
                key=lambda t: difflib.SequenceMatcher(None, node.spec_type, t).ratio(),
                reverse=True,
            )
            message = f"Unknown node type '{node.spec_type}'. Not registered with the engine."
            if hint:
                message += f" {hint}"
            if closest_first:
                message += (
                    f" Registered types (closest first): "
                    f"{format_options(closest_first, _UNKNOWN_TYPE_LIST_CAP)}."
                )
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].type",
                    node_id=node.id,
                    message=message,
                )
            )
            continue

        spec = registry.get(node.spec_type).spec
        node_specs[node.id] = spec
        # The expression sandbox is ONE checker (2026-09-11): a formula the
        # runtime will refuse ("Disallowed expression element 'ListComp'")
        # must be refused here first — a save that passes and a run that dies
        # at step 8 cost an Expert a whole run. Same AST gate as safe_eval.
        for expr_key in _EXPRESSION_CONFIG_KEYS:
            expr = node.config.get(expr_key) if isinstance(node.config, dict) else None
            if isinstance(expr, str) and expr.strip():
                try:
                    validate_expression(expr)
                except Exception as exc:  # noqa: BLE001 — the sandbox's reason is the message
                    issues.append(
                        ValidationIssue(
                            path=f"nodes[{node.id}].data.config.{expr_key}",
                            node_id=node.id,
                            message=(
                                f"Expression rejected by the runtime sandbox — it would fail "
                                f"at execution: {exc}"
                            ),
                        )
                    )
        define = node.config.get("define") if isinstance(node.config, dict) else None
        if isinstance(define, dict):
            for part, formula in define.items():
                if not isinstance(formula, str) or not formula.strip():
                    continue
                try:
                    validate_expression(formula)
                except Exception as exc:  # noqa: BLE001 — the sandbox's reason is the message
                    issues.append(ValidationIssue(
                        path=f"nodes[{node.id}].data.config.define.{part}", node_id=node.id,
                        message=f"Part '{part}' rejected by the runtime sandbox — it would fail at execution: {exc}",
                    ))
        # A setting may come from a run input ({"$input": name}): validate its stand-in and
        # refuse it on a field that cannot take one (the name is checked with the surface below).
        stand_in_config, _setting_refs, setting_problems = split_setting_refs(
            spec.config_schema, node.config, declared_input_defaults(definition)
        )
        for problem in setting_problems:
            issues.append(ValidationIssue(path=f"nodes[{node.id}].data.config", node_id=node.id, message=problem))
        try:
            spec.config_schema.model_validate(stand_in_config)
        except ValidationError as e:
            scream_node_config_rejected(
                node_id=node.id,
                spec_type=node.spec_type,
                config_schema=spec.config_schema,
                raw_config=node.config,
                node_data=node.data,
                validation_error=e,
                input_schema=spec.input_schema,
            )
            for err in e.errors():
                loc = ".".join(str(p) for p in err["loc"])
                message = err["msg"]
                # THE INPUT-NOT-CONFIG HINT (W68). "Extra inputs are not
                # permitted" is true and useless: an author who put an INPUT
                # under data.config deletes it and ships a node that cannot
                # start. Name where the key belongs, here — the one place the
                # author tool and the /validate route both read.
                if err["type"] == "extra_forbidden":
                    hint = config_extra_is_input_hint(
                        key=str(err["loc"][-1]) if err["loc"] else "",
                        spec_type=node.spec_type,
                        input_schema=spec.input_schema,
                        config_schema=spec.config_schema,
                    )
                    if hint:
                        message = f"{message}. {hint}"
                issues.append(
                    ValidationIssue(
                        path=f"nodes[{node.id}].data.config.{loc}",
                        node_id=node.id,
                        message=message,
                    )
                )
        except MatrxGraphError as e:
            # A config validator that raised the engine's own error instead of ValueError escapes
            # pydantic; validation reports it on the step rather than crashing the caller (the
            # /workflows/validate route answered 500 for a sandbox refusal, 2026-11-02).
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].data.config",
                    node_id=node.id,
                    message=str(e),
                )
            )

    # --- THE INPUT SURFACE (INPUT-SURFACE.md, 2026-08-27) ------------------
    # The compiled surface is the name-unique union of every io.user_input
    # node's field keys + the declared variables (folded in). Collisions are
    # ERRORS here (the compiler refuses them too — this is the authoring-time
    # badge), and {'$input': name} references must name a surface entry.
    surface_names: dict[str, str] = {}  # input name -> declaring owner (for messages)
    from matrx_graph.nodes.io.user_input import INPUT_SOURCE_TYPES, TRIGGER_STEP_TYPE, input_source_label

    issues.extend(_trigger_step_issues(definition, TRIGGER_STEP_TYPE))
    for node in definition.nodes:
        if node.spec_type not in INPUT_SOURCE_TYPES:
            continue
        raw_fields = node.config.get("fields")
        if not isinstance(raw_fields, list):
            continue
        for fld in raw_fields:
            if not isinstance(fld, dict):
                continue
            key = fld.get("key") or fld.get("name")
            if not isinstance(key, str) or not key:
                continue
            owner = input_source_label(node.spec_type, node.id)
            if key in surface_names:
                issues.append(
                    ValidationIssue(
                        path=f"nodes[{node.id}].data.config.fields",
                        node_id=node.id,
                        message=(
                            f"Workflow input name collision: '{key}' is declared "
                            f"by both {surface_names[key]} and {owner}. The input "
                            f"surface is one flat namespace — rename one of them."
                        ),
                    )
                )
                continue
            surface_names[key] = owner
    for v in definition.variables:
        if v.name in surface_names:
            issues.append(
                ValidationIssue(
                    path=f"variables[{v.name}]",
                    message=(
                        f"Workflow input name collision: variable '{v.name}' "
                        f"shadows the input declared by {surface_names[v.name]}. "
                        f"Variables fold into the one input surface — rename "
                        f"one of them."
                    ),
                )
            )
        else:
            surface_names[v.name] = "the workflow's declared variables"
    # Workflow settings (workflow_settings.py): each always has a value that fits its plain type.
    from matrx_graph.workflow_settings import definition_setting_problems

    for name, problem in definition_setting_problems(list(definition.variables)):
        issues.append(ValidationIssue(path=f"variables[{name}]", message=problem))
    # Settings read from run inputs ({"$input": name} in data.config) must name a surface entry.
    for node in definition.nodes:
        if not isinstance(node.config, dict):
            continue
        node_spec = node_specs.get(node.id)
        flat = [(k, v) for k, v in node.config.items()] + [
            (f"{k}.{sub}", sv)
            for k, v in node.config.items()
            if node_spec is not None
            and isinstance(v, dict)
            and not is_input_ref(v)
            and _nested_settings_model(node_spec.config_schema.model_fields.get(k)) is not None
            for sub, sv in v.items()
        ]
        for key, value in flat:
            if is_input_ref(value) and value["$input"] not in surface_names:
                issues.append(
                    ValidationIssue(
                        path=f"nodes[{node.id}].data.config.{key}",
                        node_id=node.id,
                        message=(
                            f"Setting '{key}' reads workflow input '{value['$input']}', which is "
                            "not on this workflow's input surface."
                        ),
                    )
                )

    # Run-variable references — every {'$var': name} in a node's authored
    # static inputs must name a DECLARED variable (definition.variables).
    # An undeclared reference fails HERE, loudly, instead of silently
    # resolving to an empty value at run time.
    declared_variables = {v.name for v in definition.variables}
    for node in definition.nodes:
        raw_static = node.data.get("input")
        if not isinstance(raw_static, dict):
            raw_static = node.data.get("inputs")
        if not isinstance(raw_static, dict):
            continue
        # Admission check: static literals must survive the node's RUN-TIME
        # request model's field validators (e.g. an unregistered
        # source_feature on ai.agent.start) — validators only, no execution.
        issues.extend(_static_input_admission_issues(node, raw_static))
        # {'$input': name} references (the one namespace) resolve against the
        # compiled surface — an undeclared name is an authoring error.
        for ref_path, input_name in iter_input_refs(raw_static):
            if input_name in surface_names:
                continue
            message = (
                f"Input references workflow input '{input_name}', which is not "
                f"on this workflow's input surface."
            )
            hint = suggestion_line(input_name, set(surface_names), noun="input")
            if hint:
                message += f" {hint}"
            elif surface_names:
                message += f" Declared: {format_options(sorted(surface_names), 10)}."
            else:
                message += " This workflow declares no inputs."
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].data.input.{ref_path}",
                    node_id=node.id,
                    message=message,
                )
            )
        for ref_path, var_name in iter_var_refs(raw_static):
            # Deprecation posture (INPUT-SURFACE.md): $var survives for stored
            # definitions until the marker migration runs, but every authored
            # marker is badged so authors move to $input. The save seam
            # (aidream) refuses NEW $var markers outright.
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].data.input.{ref_path}",
                    node_id=node.id,
                    severity="warning",
                    message=(
                        f"Deprecated marker: {{'$var': '{var_name}'}} — the $var "
                        f"namespace is replaced by {{'$input': '{var_name}'}}. "
                        f"Existing definitions keep working until the marker "
                        f"migration; new $var markers are refused at save."
                    ),
                )
            )
            if var_name in declared_variables:
                continue
            message = (
                f"Input references run variable '{var_name}' which is not "
                f"declared in the workflow's variables."
            )
            hint = suggestion_line(var_name, declared_variables, noun="variable")
            if hint:
                message += f" {hint}"
            elif declared_variables:
                message += f" Declared: {format_options(sorted(declared_variables), 10)}."
            else:
                message += " This workflow declares no variables."
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].data.input.{ref_path}",
                    node_id=node.id,
                    message=message,
                )
            )

    # Dispatch-target references — a dispatcher node's config.target_node_id
    # must name a node on THIS canvas. A typo'd target used to compile clean
    # and only surface at runtime (formerly a bare KeyError mid-run); fail
    # here, badged on the dispatcher, with a closest-match hint.
    for node in definition.nodes:
        if node.spec_type not in DISPATCHER_NODE_TYPES:
            continue
        config = node.config if isinstance(node.config, dict) else {}
        target = config.get("target_node_id")
        if not isinstance(target, str) or not target:
            continue  # missing/empty already fails the config schema above
        if target == node.id:
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].data.config.target_node_id",
                    node_id=node.id,
                    message=(
                        f"'{node.id}' targets itself — a dispatcher cannot "
                        "be its own target (infinite self-dispatch)."
                    ),
                )
            )
            continue
        if target not in node_ids:
            message = f"Dispatch target '{target}' is not a step on this workflow."
            hint = suggestion_line(target, node_ids, noun="node id")
            if hint:
                message += f" {hint}"
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].data.config.target_node_id",
                    node_id=node.id,
                    message=message,
                )
            )

    # A For Each's target runs ONLY when dispatched. A plain connection INTO it
    # makes the engine fire it once on its own the moment that value arrives —
    # with no item — and the gather after it then fails ("no engine-aggregated
    # 'items'"). Live 2026-10-28, Write questions blind v21: two spend-cap
    # settings wired straight into the per-pass writer. A value every item needs
    # goes to the For Each and rides in its payload template as `$in.<name>`.
    # (A loop / work-queue body's static input is a supported join; not refused.)
    dispatched_by = {
        node.config.get("target_node_id"): node.id
        for node in definition.nodes
        if node.spec_type == "control.map" and isinstance(node.config, dict)
    }
    for edge in definition.edges:
        dispatcher = dispatched_by.get(edge.target)
        if dispatcher is None or edge.source == dispatcher or edge.kind not in (EdgeKind.DATA, EdgeKind.CONDITIONAL):
            continue
        issues.append(
            ValidationIssue(
                path=f"edges[{edge.id}]",
                edge_id=edge.id,
                node_id=edge.target,
                message=(
                    f"'{edge.target}' runs once per item of '{dispatcher}', so a connection from "
                    f"'{edge.source}' straight into it would run it once more on its own, with no item. "
                    f"Connect '{edge.source}' to '{dispatcher}' instead and add the value to its "
                    f"payload template as \"$in.<name>\" — every item then receives it."
                ),
            )
        )

    # A For Each's target runs once per item, and EVERY edge out of it is a
    # fan-in: the engine waits for all items and hands the next step ONE
    # payload, {"items": [...]} (ENGINE_SPEC §4.4 as the scheduler implements
    # it — the edge's mappings apply inside each item, never at top level). A
    # next step that declares no `items` input therefore never receives the
    # fields the edge maps; the run dies there instead of here. Live
    # 2026-09-25, run 99de02f7-f197-4764-b8f9-0dfa649e3e9a: a per-page
    # data.transform mapped `topic` into a Run Agent step, validate said
    # "valid", the step failed with "variable 'topic' ... received no value".
    fanned_by: dict[str, str] = {}
    for node in definition.nodes:
        if node.spec_type != "control.map":
            continue
        config = node.config if isinstance(node.config, dict) else {}
        target = config.get("target_node_id")
        if isinstance(target, str) and target in node_ids and target != node.id:
            fanned_by.setdefault(target, node.id)
    spec_type_by_id = {node.id: node.spec_type for node in definition.nodes}
    for edge in definition.edges:
        dispatcher = fanned_by.get(edge.source)
        if dispatcher is None or edge.kind not in (EdgeKind.DATA, EdgeKind.CONDITIONAL):
            continue
        target_spec = node_specs.get(edge.target)
        if (
            target_spec is None
            or spec_type_by_id.get(edge.target) in _COLLECTOR_NODE_TYPES
            or "items" in target_spec.input_schema.model_fields
        ):
            continue
        mapped = sorted((edge.data or {}).get("mappings") or {})
        issues.append(
            ValidationIssue(
                path=f"edges[{edge.id}]",
                edge_id=edge.id,
                node_id=edge.target,
                message=(
                    f"'{edge.source}' runs once per item of the For Each '{dispatcher}', "
                    f"so this connection is where the items are collected: '{edge.target}' "
                    "runs once, after every item, and receives a single list under "
                    "`items` — "
                    + (
                        f"the fields this connection maps ({format_options(mapped, 6)}) never "
                        "arrive on their own. "
                        if mapped
                        else "no per-item field arrives on its own. "
                    )
                    + f"'{edge.target}' has no `items` input. Make '{edge.target}' the For "
                    f"Each's target itself, or collect the items first (control.gather) and "
                    "read the list from there."
                ),
            )
        )

    # Join-semantics keys (ENGINE_SPEC §3). Enum-shaped values fail loudly
    # here (badged per node) so the scheduler can trust CompiledNode fields;
    # the §3.4 skip_defaults completeness rule needs the inbound-edge map.
    incoming_data_edges: dict[str, list[Any]] = {}
    for edge in definition.edges:
        if edge.kind in (EdgeKind.DATA, EdgeKind.CONDITIONAL):
            incoming_data_edges.setdefault(edge.target, []).append(edge)

    for node in definition.nodes:
        raw_join_policy = node.data.get("join_policy")
        if raw_join_policy is not None and raw_join_policy not in _JOIN_POLICIES:
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].data.join_policy",
                    node_id=node.id,
                    message=(
                        f"Invalid join_policy {raw_join_policy!r}. "
                        f"Allowed: {', '.join(_JOIN_POLICIES)}."
                    ),
                )
            )

        raw_skip_policy = node.data.get("on_skipped_upstream")
        if raw_skip_policy is not None and raw_skip_policy not in _SKIP_POLICIES:
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].data.on_skipped_upstream",
                    node_id=node.id,
                    message=(
                        f"Invalid on_skipped_upstream {raw_skip_policy!r}. "
                        f"Allowed: {', '.join(_SKIP_POLICIES)}."
                    ),
                )
            )

        raw_when_skipped = node.data.get("when_input_skipped")
        if raw_when_skipped is not None and raw_when_skipped not in _WHEN_INPUT_SKIPPED:
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].data.when_input_skipped",
                    node_id=node.id,
                    message=(
                        f"Invalid when_input_skipped {raw_when_skipped!r}. "
                        f"Allowed: {', '.join(_WHEN_INPUT_SKIPPED)}."
                    ),
                )
            )

        raw_item_failure = node.data.get("on_item_failure")
        if raw_item_failure is not None and raw_item_failure not in _ITEM_FAILURE_POLICIES:
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].data.on_item_failure",
                    node_id=node.id,
                    message=(
                        f"Invalid on_item_failure {raw_item_failure!r}. "
                        f"Allowed: {', '.join(_ITEM_FAILURE_POLICIES)} "
                        "(Node Result System fan-out failure policy)."
                    ),
                )
            )

        raw_optional = node.data.get("optional")
        if raw_optional is not None and not isinstance(raw_optional, bool):
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].data.optional",
                    node_id=node.id,
                    message=f"Invalid optional {raw_optional!r}. Allowed: true or false.",
                )
            )

        issues.extend(
            _review_mark_issues(node.data.get("review"), f"nodes[{node.id}].data.review", node_id=node.id)
        )
        issues.extend(_once_reads_run_issues(node.id, node.data))
        issues.extend(_says_issues(node.id, node.data, per_item_steps))

        raw_concurrency = node.data.get("concurrency")
        if is_input_ref(raw_concurrency):
            # The cap comes from a run input (a caller's "at most 2 at a time"): the name must be
            # on the surface and a written default must itself be a valid cap. The run's value is
            # checked when the node's gate opens (scheduler ``_node_gate``).
            ref_name = raw_concurrency["$input"]
            ref_default = raw_concurrency.get("default")
            if ref_name not in surface_names:
                issues.append(
                    ValidationIssue(
                        path=f"nodes[{node.id}].data.concurrency",
                        node_id=node.id,
                        message=(
                            f"How many at once reads workflow input '{ref_name}', which is not "
                            "on this workflow's input surface."
                        ),
                    )
                )
            if ref_default is not None and concurrency_cap(ref_default) is None:
                issues.append(
                    ValidationIssue(
                        path=f"nodes[{node.id}].data.concurrency.default",
                        node_id=node.id,
                        message=f"How many at once must be a whole number of 1 or more, not {ref_default!r}.",
                    )
                )
        elif raw_concurrency is not None and (
            isinstance(raw_concurrency, bool)
            or not isinstance(raw_concurrency, int)
            or raw_concurrency < 1
        ):
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].data.concurrency",
                    node_id=node.id,
                    message=(
                        f"Invalid concurrency {raw_concurrency!r}. Must be an "
                        "integer >= 1 (per-node concurrent-invocation cap, "
                        "ENGINE_SPEC §4.6)."
                    ),
                )
            )

        raw_ready = node.data.get("ready_when")
        if raw_ready is not None and (
            not isinstance(raw_ready, list)
            or not all(isinstance(p, str) and p.strip() for p in raw_ready)
        ):
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].data.ready_when",
                    node_id=node.id,
                    message=(
                        f"Invalid ready_when {raw_ready!r}. Must be a list of dotted "
                        "run-variable paths (e.g. ['confirmed.name'])."
                    ),
                )
            )

        raw_arg_merge = node.data.get("arg_merge")
        if raw_arg_merge is not None:
            if not isinstance(raw_arg_merge, dict):
                issues.append(
                    ValidationIssue(
                        path=f"nodes[{node.id}].data.arg_merge",
                        node_id=node.id,
                        message=(
                            "arg_merge must be a {target_arg: reducer} object, "
                            f"got {type(raw_arg_merge).__name__}."
                        ),
                    )
                )
            else:
                for arg_key, reducer in raw_arg_merge.items():
                    if reducer not in _ARG_MERGE_REDUCERS:
                        issues.append(
                            ValidationIssue(
                                path=f"nodes[{node.id}].data.arg_merge.{arg_key}",
                                node_id=node.id,
                                message=(
                                    f"Invalid arg_merge reducer {reducer!r} for "
                                    f"arg {arg_key!r}. Allowed: "
                                    f"{', '.join(_ARG_MERGE_REDUCERS)}."
                                ),
                            )
                        )

        # §3.4 — default_value requires a skip_defaults entry for every arg
        # an inbound edge explicitly maps. A BROADCAST (no-mappings) inbound
        # data edge is rejected outright (F8): a skipped broadcast upstream
        # would have to deliver the WHOLE skip_defaults dict, which collides
        # with every sibling edge on every key — structurally guaranteed
        # multi-writer failure at run time. The author must add explicit
        # field links (edge mappings) so each default is per-arg addressable.
        if raw_skip_policy == "default_value":
            for in_edge in incoming_data_edges.get(node.id, []):
                if in_edge.mappings is None:
                    issues.append(
                        ValidationIssue(
                            path=f"nodes[{node.id}].data.on_skipped_upstream",
                            node_id=node.id,
                            edge_id=in_edge.id,
                            message=(
                                f"on_skipped_upstream='default_value' cannot "
                                f"be combined with broadcast edge "
                                f"'{in_edge.id}' (no field mappings): a "
                                f"skipped upstream would deliver the entire "
                                f"skip_defaults dict and collide with every "
                                f"other inbound edge (ENGINE_SPEC §3.4). Add "
                                f"explicit field links (mappings) on the "
                                f"edge so each default substitutes one "
                                f"named arg."
                            ),
                        )
                    )
            raw_skip_defaults = node.data.get("skip_defaults")
            if not isinstance(raw_skip_defaults, dict):
                issues.append(
                    ValidationIssue(
                        path=f"nodes[{node.id}].data.skip_defaults",
                        node_id=node.id,
                        message=(
                            "on_skipped_upstream='default_value' requires a "
                            "skip_defaults {target_arg: value} object."
                        ),
                    )
                )
            else:
                for in_edge in incoming_data_edges.get(node.id, []):
                    for target_key in in_edge.mappings or {}:
                        if target_key not in raw_skip_defaults:
                            issues.append(
                                ValidationIssue(
                                    path=f"nodes[{node.id}].data.skip_defaults",
                                    node_id=node.id,
                                    edge_id=in_edge.id,
                                    message=(
                                        f"skip_defaults is missing key "
                                        f"'{target_key}' — edge '{in_edge.id}' "
                                        f"maps it into this node, and "
                                        f"on_skipped_upstream='default_value' "
                                        f"must be able to substitute every "
                                        f"mapped arg (ENGINE_SPEC §3.4)."
                                    ),
                                )
                            )

    for edge in definition.edges:
        issues.extend(
            _review_mark_issues(edge.data.get("review"), f"edges[{edge.id}].data.review", edge_id=edge.id)
        )
        source_known = edge.source in node_ids
        target_known = edge.target in node_ids
        if not source_known:
            issues.append(
                ValidationIssue(
                    path=f"edges[{edge.id}].source",
                    edge_id=edge.id,
                    message=f"Edge source '{edge.source}' does not match any node id.",
                )
            )
        if not target_known:
            issues.append(
                ValidationIssue(
                    path=f"edges[{edge.id}].target",
                    edge_id=edge.id,
                    message=f"Edge target '{edge.target}' does not match any node id.",
                )
            )

        source_spec = node_specs.get(edge.source)
        target_spec = node_specs.get(edge.target)

        # --- Handle validation (the promised-but-dead §S4 check) --------------
        # A sourceHandle/targetHandle names one of the node's DECLARED handles.
        # A typo (studio wires sourceHandle="true" on a branch — "tru" reaches
        # NOTHING and routes silently, scheduler.py:1694) is caught here, named.
        if edge.sourceHandle is not None and source_spec is not None:
            out_handles = {
                h.id for h in source_spec.handles if h.direction == HandleDirection.OUTPUT
            }
            out_handles.update(
                config_output_handles(source_spec, node_definitions.get(edge.source))
            )
            if edge.sourceHandle not in out_handles:
                message = (
                    f"Edge references sourceHandle '{edge.sourceHandle}' which is "
                    f"not a declared output handle on node '{edge.source}' "
                    f"(type '{source_spec.node_type}')."
                )
                hint = suggestion_line(edge.sourceHandle, out_handles, noun="handle")
                if hint:
                    message += f" {hint}"
                elif out_handles:
                    message += f" Output handles: {format_options(sorted(out_handles), 10)}."
                else:
                    message += " This node declares no output handles."
                issues.append(
                    ValidationIssue(
                        path=f"edges[{edge.id}].sourceHandle",
                        edge_id=edge.id,
                        node_id=edge.source,
                        message=message,
                    )
                )
        if edge.targetHandle is not None and target_spec is not None:
            in_handles = {h.id for h in target_spec.handles if h.direction == HandleDirection.INPUT}
            # Node authors may declare config fields that expose additional
            # input connection points. Only validated, explicitly marked fields
            # qualify; arbitrary config keys cannot relax handle validation.
            target_node = node_definitions.get(edge.target)
            config = target_node.data.get("config", {}) if target_node is not None else {}
            try:
                parsed_config = target_spec.config_schema.model_validate(config)
            except Exception:
                parsed_config = None  # the config gate reports the actual issue
            if parsed_config is not None:
                for field_name, field in target_spec.config_schema.model_fields.items():
                    metadata = field.json_schema_extra
                    if (
                        not isinstance(metadata, dict)
                        or metadata.get("workflow_input_handles") is not True
                    ):
                        continue
                    exposed = getattr(parsed_config, field_name, None)
                    if isinstance(exposed, list):
                        in_handles.update(
                            name
                            for name in exposed
                            if isinstance(name, str)
                            and name.strip() == name
                            and name
                            and name not in target_spec.input_schema.model_fields
                        )
            if edge.targetHandle not in in_handles:
                message = (
                    f"Edge references targetHandle '{edge.targetHandle}' which is "
                    f"not a declared input handle on node '{edge.target}' "
                    f"(type '{target_spec.node_type}')."
                )
                hint = suggestion_line(edge.targetHandle, in_handles, noun="handle")
                if hint:
                    message += f" {hint}"
                elif in_handles:
                    message += f" Input handles: {format_options(sorted(in_handles), 10)}."
                else:
                    message += " This node declares no input handles."
                issues.append(
                    ValidationIssue(
                        path=f"edges[{edge.id}].targetHandle",
                        edge_id=edge.id,
                        node_id=edge.target,
                        message=message,
                    )
                )

        # --- Condition-without-conditional-kind (adversarial wave 2) ---------
        # An edge carrying data.condition but whose kind is not CONDITIONAL is
        # a silent no-op: the scheduler only evaluates edge.condition on
        # CONDITIONAL edges, and definition.py defaults an unspecified kind to
        # DATA. The predicate the author wrote does NOTHING, with no runtime
        # signal. Fail loudly and tell them to set the connection to conditional.
        if edge.condition and edge.kind != EdgeKind.CONDITIONAL:
            issues.append(
                ValidationIssue(
                    path=f"edges[{edge.id}].data.condition",
                    edge_id=edge.id,
                    message=(
                        f"Edge sets a condition predicate ({edge.condition!r}) but "
                        f"its type is '{edge.kind.value}', not 'conditional' — the "
                        f"predicate is SILENTLY IGNORED at run time. Set the "
                        f"connection type to 'conditional' (data.kind='conditional') "
                        f"so the predicate actually gates the edge."
                    ),
                )
            )

        # --- A CONTROL EDGE CARRIES NO PAYLOAD (W71, 2026-09-12) -------------
        # The scheduler binds ``fragment = {}`` for every CONTROL delivery: the
        # edge transfers control and nothing else. Mappings authored on one are
        # therefore INERT — and silently so. Live, run 533fda6f: the Conductor
        # wrote all four desk connections as kind 'control' WITH mappings
        # ({"variables": "$FULL_PAYLOAD"}, {"user_input": "text"} …), the save
        # passed, the template rendered a blank id and the agent step died on
        # missing_input for user_input.
        # ``sourceHandle`` is deliberately NOT a finding here: the scheduler
        # still honors it on a CONTROL edge as the PRUNE gate (a branch not
        # taken prunes the control edge too), so sequencing off one branch is
        # lawful. Only the mappings are provably inert.
        if edge.kind is EdgeKind.CONTROL and isinstance(edge.data.get("mappings"), dict):
            control_mappings = edge.data["mappings"]
            if control_mappings:
                issues.append(
                    ValidationIssue(
                        path=f"edges[{edge.id}].data.mappings",
                        edge_id=edge.id,
                        node_id=edge.target,
                        message=(
                            f"Connection '{edge.id}' is type 'control' but declares "
                            f"mappings ({format_options(sorted(control_mappings), 6)}). "
                            f"A control connection transfers CONTROL only — the engine "
                            f"delivers an EMPTY payload over it, so those mappings are "
                            f"silently ignored and the target starts with nothing (it "
                            f"then fails on missing_input). Set this connection's type "
                            f"to 'data' (data.kind='data') to deliver the same "
                            f"mappings, or drop them if you really only meant to "
                            f"sequence the steps."
                        ),
                    )
                )

        # --- Mapping validation (§S4) ----------------------------------------
        # An explicit but EMPTY mappings object means "route nothing" at run
        # time (a target that received {} still ran, COMPLETED — the silent
        # route-nothing the FE guards against but the server accepted from any
        # other client). Reject it: the author either wants a broadcast (drop
        # the mappings key entirely) or must map at least one field.
        raw_mappings = edge.data.get("mappings")
        if isinstance(raw_mappings, dict) and not raw_mappings:
            issues.append(
                ValidationIssue(
                    path=f"edges[{edge.id}].data.mappings",
                    edge_id=edge.id,
                    message=(
                        "Edge declares an empty mappings object — at run time this "
                        "routes NOTHING to the target (silent non-delivery). Remove "
                        "the 'mappings' key entirely to broadcast the whole payload, "
                        "or map at least one field."
                    ),
                )
            )
        elif (
            raw_mappings is None
            and edge.kind is EdgeKind.DATA
            and source_spec is not None
            and target_spec is not None
            and not source_spec.dynamic_output
        ):
            # A WHOLE-output connection into a CLOSED step hands it every field of the source's
            # output: a field the step does not declare is refused at run time (extra_forbidden).
            # Only when both schemas are closed is the field list certain (2026-11-09, L7e:
            # search workflow 79c58b1f fed closed steps fields only another step read).
            src_props, src_closed = _schema_props(source_spec.output_schema)
            tgt_props, tgt_closed = _schema_props(target_spec.input_schema)
            extra = sorted(src_props - tgt_props - {"__kind"}) if src_closed and tgt_closed else []
            if extra:
                issues.append(
                    ValidationIssue(
                        path=f"edges[{edge.id}]",
                        edge_id=edge.id,
                        severity="warning",
                        message=(
                            f"Connection '{edge.id}' hands '{edge.target}' the whole output of "
                            f"'{edge.source}', including {format_options(extra, 6)}, which "
                            f"'{edge.target}' does not take — it will refuse them when it runs. "
                            "Map only the fields it takes (field links), or make it a control connection."
                        ),
                    )
                )
        elif isinstance(raw_mappings, dict) and raw_mappings:
            # source dot-path top-level segment must plausibly exist on the
            # source's output (skipped for dynamic-output nodes, $FULL_PAYLOAD,
            # and OPEN output schemas — those legitimately carry extra keys, so
            # a warning there is noise). Target key must plausibly exist on a
            # CLOSED target input schema. Both are WARNINGS — a persisted sample
            # or an open schema may still provide the field at run time.
            if edge.kind is EdgeKind.ERROR:
                # Node Result System: an ERROR edge delivers the structured
                # NodeError dump, not the source's output — its mapping
                # source keys address {code, message, details}.
                src_props, src_closed = ({"code", "message", "details"}, True)
            else:
                src_props, src_closed = (
                    _schema_props(source_spec.output_schema)
                    if source_spec is not None
                    else (set(), False)
                )
            tgt_props, tgt_closed = (
                _schema_props(target_spec.input_schema)
                if target_spec is not None
                else (set(), False)
            )
            src_dynamic = bool(source_spec is not None and source_spec.dynamic_output)
            for target_key, source_key in raw_mappings.items():
                # A dotted TARGET key can never run (live 2026-11-17, 'provision_values.policies'): said plainly at
                # save and publish as a WARNING (Law 6: validation offers, never blocks a person); the run then
                # fails loudly with the same sentence. An AGENT's save is refused by the host on this code.
                if isinstance(target_key, str) and "." in target_key:
                    issues.append(
                        ValidationIssue(
                            path=f"edges[{edge.id}].data.mappings.{target_key}",
                            edge_id=edge.id,
                            node_id=edge.target,
                            code="dotted_target_key",
                            severity="warning",
                            message=dotted_target_message(
                                target_key,
                                str(source_key),
                                edge_id=str(edge.id),
                                node_id=edge.target,
                                takes=sorted(tgt_props) if tgt_props else None,
                            ),
                        )
                    )
                    continue
                # An unsupported '$' token is an ERROR, and the ONE mapping
                # finding that needs no schema at all: no node emits a
                # '$'-prefixed output key, so the run dies on it whatever the
                # upstream declares. Every schema-shaped check below goes
                # quiet on a dynamic or open upstream — which is exactly where
                # '$payload' slipped through into a paid run (129a4ec1).
                bad_sigil = unknown_sigil(source_key)
                if bad_sigil is not None:
                    issues.append(
                        ValidationIssue(
                            path=f"edges[{edge.id}].data.mappings.{target_key}",
                            edge_id=edge.id,
                            node_id=edge.source,
                            message=unknown_sigil_message(
                                str(target_key), bad_sigil, edge_id=str(edge.id)
                            ),
                        )
                    )
                    continue
                # PATH SYNTAX. The resolver never refuses a path — `items[]` reads
                # a key named "" and the step silently receives nothing (live
                # 2026-10-27: `items[].page_id` saved "valid"). A path the grammar
                # cannot read is an ERROR whatever the upstream declares.
                if isinstance(source_key, str) and source_key != _WHOLE_PAYLOAD_SOURCE:
                    syntax = path_syntax_problem(source_key)
                    if syntax is not None:
                        issues.append(
                            ValidationIssue(
                                path=f"edges[{edge.id}].data.mappings.{target_key}",
                                edge_id=edge.id,
                                node_id=edge.target,
                                message=(
                                    f"Mapping '{target_key}' <- '{source_key}' on edge "
                                    f"'{edge.id}' ({edge.source} -> {edge.target}) is not a "
                                    f"readable path: {syntax}."
                                ),
                            )
                        )
                        continue
                # SOURCE-PATH CHECK. A mapping source is a PATH into the
                # upstream output — `structured_output.entries`, `items[0].x`
                # — so the check walks the path against the declared output
                # schema, not just its first segment. A path the schema
                # provably rules out is an ERROR (the run would die at the
                # edge, six steps in); anything the schema cannot settle
                # (dynamic outputs, open schemas, undescribed levels) passes
                # through exactly as before.
                if (
                    source_spec is not None
                    and edge.kind is not EdgeKind.ERROR
                    and not src_dynamic
                    and isinstance(source_key, str)
                    and source_key != _WHOLE_PAYLOAD_SOURCE
                ):
                    problem = _source_path_problem(source_spec.output_schema, source_key)
                    if problem is not None:
                        issues.append(
                            ValidationIssue(
                                path=f"edges[{edge.id}].data.mappings.{target_key}",
                                edge_id=edge.id,
                                node_id=edge.source,
                                message=(
                                    f"Mapping source path '{source_key}' can never "
                                    f"resolve against the output of node "
                                    f"'{edge.source}' (type "
                                    f"'{source_spec.node_type}'): {problem}. Point it "
                                    f"at a field the step actually emits."
                                ),
                            )
                        )
                    elif (
                        src_closed
                        and first_path_segment(source_key)
                        and first_path_segment(source_key) not in src_props
                    ):
                        issues.append(
                            ValidationIssue(
                                path=f"edges[{edge.id}].data.mappings.{target_key}",
                                edge_id=edge.id,
                                node_id=edge.source,
                                severity="warning",
                                message=(
                                    f"Mapping source '{source_key}' addresses key "
                                    f"'{first_path_segment(source_key)}' which is not "
                                    f"declared on the output of node '{edge.source}' "
                                    f"(type '{source_spec.node_type}'). It may be "
                                    f"provided by sample/run data, but check for a typo."
                                ),
                            )
                        )
                if (
                    target_spec is not None
                    and tgt_closed
                    and isinstance(target_key, str)
                    and target_key not in tgt_props
                ):
                    issues.append(
                        ValidationIssue(
                            path=f"edges[{edge.id}].data.mappings.{target_key}",
                            edge_id=edge.id,
                            node_id=edge.target,
                            severity="warning",
                            message=(
                                f"Mapping target key '{target_key}' is not a declared "
                                f"input on node '{edge.target}' (type "
                                f"'{target_spec.node_type}'). It will be ignored (or "
                                f"rejected) at run time — check for a typo."
                            ),
                        )
                    )

    issues.extend(_config_path_syntax_issues(definition))
    issues.extend(_required_input_issues(definition, node_specs, set(surface_names)))
    issues.extend(_unrendered_placeholder_issues(definition, node_specs))
    issues.extend(_kind_routing_issues(definition))
    issues.extend(_template_path_issues(definition, node_specs))
    issues.extend(_half_fed_step_issues(definition, node_specs))
    issues.extend(_failure_joined_step_issues(definition, node_specs))
    issues.extend(_skip_joined_step_issues(definition, node_specs))
    issues.extend(_visible_io_issues(definition, registry))
    issues.extend(_whole_list_payload_issues(definition))
    issues.extend(_text_input_fed_object_issues(definition, node_specs))
    issues.extend(_unknown_step_key_issues(definition))
    issues.extend(_accidental_loop_issues(definition))

    return ValidationResult(valid=not any(i.severity == "error" for i in issues), issues=issues)


#: Steps built to be returned to: a loop through one of them is one the author declared.
LOOP_NODE_TYPES: frozenset[str] = frozenset({"control.loop", "control.work_queue"})


def _accidental_loop_issues(definition: Definition) -> list[ValidationIssue]:
    """A loop no loop step declares, named at save and publish (2026-11-16).

    Compile orients every reachable cycle by the SAME classifier the scheduler runs on
    (``compile._detect_back_edges``) and treats the closing connection as a feedback edge: its
    target re-fires once per delivery. An edit that wires a later step back into an earlier one
    did exactly that to the research Read step (after the pick -> keywords -> judge -> pick), and
    every run crashed while save and publish said nothing. A warning: validation offers, never blocks."""
    from types import SimpleNamespace

    from matrx_graph.compile import _ROUTABLE_KINDS, _detect_back_edges
    from matrx_graph.content_ir.triggers import TriggerDeclarationError, parse_node_trigger
    from matrx_graph.errors import CompilationError

    nodes = {n.id: n for n in definition.nodes}
    edges = {
        e.id: SimpleNamespace(edge_id=e.id, kind=e.kind, source_node_id=e.source, target_node_id=e.target)
        for e in definition.edges
        if e.source in nodes and e.target in nodes
    }
    outgoing: dict[str, list[str]] = {}
    has_inbound: set[str] = set()
    for e in edges.values():
        outgoing.setdefault(e.source_node_id, []).append(e.edge_id)
        has_inbound.add(e.target_node_id)
    if definition.entry_nodes:
        entry = tuple(n for n in definition.entry_nodes if n in nodes)
    else:  # the entry set compile derives: no inbound connection, not trigger-fired, not a dispatch target
        dispatch_targets = {
            target
            for n in definition.nodes
            if n.spec_type in DISPATCHER_NODE_TYPES
            and isinstance(target := ((n.data or {}).get("config") or {}).get("target_node_id"), str)
            and target != n.id
        }

        def _triggered(data: Any) -> bool:
            try:
                return parse_node_trigger(data) is not None
            except TriggerDeclarationError:
                return False

        entry = tuple(
            nid for nid, n in nodes.items()
            if nid not in has_inbound and nid not in dispatch_targets and not _triggered(n.data)
        )
    try:
        back = _detect_back_edges(entry, edges, outgoing, list(nodes))  # type: ignore[arg-type]
    except CompilationError:
        return []  # a loop no entry reaches: compile refuses it by name already

    def _label(nid: str) -> str:
        label = (nodes[nid].data or {}).get("label")
        return str(label).strip() if isinstance(label, str) and label.strip() else nid

    found: list[ValidationIssue] = []
    for eid in [e.id for e in definition.edges if e.id in back]:
        closing = edges[eid]
        start, end = closing.target_node_id, closing.source_node_id
        # The loop's steps: the shortest forward path from where the loop restarts to the step that closes it.
        parent: dict[str, str | None] = {start: None}
        frontier = [start]
        while frontier and end not in parent:
            nxt: list[str] = []
            for nid in frontier:
                for oid in outgoing.get(nid, ()):
                    e = edges[oid]
                    if oid == eid or e.kind not in _ROUTABLE_KINDS or e.target_node_id in parent:
                        continue
                    parent[e.target_node_id] = nid
                    nxt.append(e.target_node_id)
            frontier = nxt
        path: list[str] = []
        cur: str | None = end if end in parent else start
        while cur is not None:
            path.append(cur)
            cur = parent[cur]
        path.reverse()
        if any(nodes[nid].spec_type in LOOP_NODE_TYPES for nid in path):
            continue
        from matrx_graph.step_settings import owner_of

        # A built-in setting's helper (Only when, If skipped, Shape) is read as the step the author wrote.
        shown = [owner_of(nid) or nid for nid in [*path, start]]
        steps = " -> ".join(_label(nid) for i, nid in enumerate(shown) if nid in nodes and (i == 0 or nid != shown[i - 1]))
        found.append(
            ValidationIssue(
                path=f"edges[{eid}]",
                edge_id=eid,
                node_id=start,
                severity="warning",
                code="accidental_loop",
                message=(
                    f"These steps form a loop: {steps}. The connection from {_label(end)} to {_label(start)} "
                    f"closes it, so {_label(start)} runs again every time {_label(end)} delivers. Remove that "
                    "connection, or use a Loop step if the repeat is meant."
                ),
            )
        )
    return found


def _visible_io_issues(definition: Definition, registry: NodeRegistry) -> list[ValidationIssue]:
    """Rule 18 (Arman, 2026-10-28): what comes in and what goes out is visible on the canvas — no
    input step, no output step, a run value no input step shows, a write whose result never reaches
    an output step (``matrx_graph.visible_io``). A WARNING on every save / publish / validate door:
    validation offers, never blocks. Release guard: aidream ``scripts/check_workflow_visible_io.py``."""
    from matrx_graph.visible_io import visible_io_findings

    return [
        ValidationIssue(
            path=f"nodes[{f.node_id}]" if f.node_id else "visible_io",
            node_id=f.node_id,
            message=f.message,
            severity="warning",
        )
        for f in visible_io_findings(definition, registry)
    ]


def _whole_list_payload_issues(definition: Definition) -> list[ValidationIssue]:
    """FX8 (run 424e086e, 2026-11-02): a per-item template that copies a per-item list WHOLE into
    every item (``src: "$in.batches"`` beside ``$in.batches.[batch_id={$item…}]``) — N items x the
    list, held, sent and saved once per item; it killed the worker four times. An ERROR when the list
    is provably per item (read per item elsewhere in the template, or the list being iterated) — a
    patch that introduces one is refused, and the message names the selector that fixes it; a
    WARNING when the list is one another For each iterates (``matrx_graph.fan_out_payload``). Live
    scanner: aidream ``scripts/check_fan_out_payloads.py``."""
    from matrx_graph.fan_out_payload import whole_list_payload_findings
    from matrx_graph.step_settings import FOR_EACH

    issues: list[ValidationIssue] = []
    for f in whole_list_payload_findings(definition, expanded=True):
        holder = (
            f"nodes[{f.step_id}].data.{FOR_EACH}.payload_template"
            if f.step_id != f.node_id
            else f"nodes[{f.node_id}].data.config.{'template' if f.node_type == 'data.map_template' else 'payload_template'}"
        )
        issues.append(ValidationIssue(
            path=f"{holder}.{f.where}" if f.where else holder,
            node_id=f.node_id,
            message=f.message,
            severity="error" if f.refused else "warning",
        ))
    return issues


# --- A TEXT INPUT FED A WHOLE OBJECT (FIX-L6, 2026-11-03) ------------------
# Live, release 36eaeafb684: Company Setup built "Send pickup reminders" with a For each whose
# payload_template was ``{"prompt": "$item"}`` over ``table.row.list``'s ``rows`` — every item a
# whole Row object (id, values, version …) landing on ``ai.llm.chat``'s TEXT ``prompt``. The save
# said nothing; every run stopped at "Write the reminder" with ``string_type``. The
# run now sends such a value as JSON text and notes it on the step (``matrx_graph.text_inputs``);
# the save-time offer below is what lets the author pick fields instead. A WARNING (validation
# offers, never blocks) wherever the declared shapes PROVE an object or list reaches an input that takes only text: a per-item template value (``$item`` / ``$item.<path>``)
# and an edge mapping (``target <- source path``). Undescribed shapes stay silent.


def _object_shape(schema: dict[str, Any] | None, root: dict[str, Any]) -> str | None:
    """``"record"`` / ``"list"`` when a declared value is provably an object or a list, else None."""
    if not isinstance(schema, dict):
        return None
    schema = resolve_ref(schema, root)
    branches = schema.get("anyOf") or schema.get("oneOf")
    if isinstance(branches, list):
        real = [b for b in branches if isinstance(b, dict) and resolve_ref(b, root).get("type") != "null"]
        shapes = {_object_shape(b, root) for b in real}
        return shapes.pop() if real and len(shapes) == 1 and None not in shapes else None
    kind = schema.get("type")
    if kind == "object" or (kind is None and isinstance(schema.get("properties"), dict)):
        return "record"
    if kind == "array":
        return "list"
    return None


def _text_fix_hint(ref: str, shape: str) -> str:
    """How to hand a text input the object: all of it as JSON, or chosen fields."""
    inner = ref[1:]
    picks = f", or write text that picks its fields with {{{inner}.<field>}} placeholders" if shape == "record" else ""
    return f"To choose, use {{\"$format\": \"{{{inner}}}\"}} (the whole {shape} as JSON){picks}."


def _text_input_fed_object_issues(
    definition: Definition,
    node_specs: dict[str, NodeSpec],
) -> list[ValidationIssue]:
    """WARN where a text-only input is provably fed a whole object or list (see the block above)."""
    issues: list[ValidationIssue] = []
    edges_by_target: dict[str, list[Any]] = {}
    for edge in definition.edges:
        edges_by_target.setdefault(edge.target, []).append(edge)

    def text_props(node_id: str) -> tuple[dict[str, Any], dict[str, Any]] | None:
        spec = node_specs.get(node_id)
        if spec is None:
            return None
        root = model_json_schema(spec.input_schema)
        props = root.get("properties")
        return root, props if isinstance(props, dict) else {}

    # 1. Per-item templates: control.map hands each item's payload to its target step.
    for node in definition.nodes:
        if node.spec_type != "control.map" or not isinstance(node.config, dict):
            continue
        template = node.config.get("payload_template")
        target_id = node.config.get("target_node_id")
        target = text_props(target_id) if isinstance(target_id, str) else None
        if not isinstance(template, dict) or target is None:
            continue
        t_root, t_props = target
        refs = {
            k: v
            for k, v in template.items()
            if isinstance(v, str)
            and (v == "$item" or v.startswith("$item."))
            and _text_only_input(t_props.get(k), t_root)
        }
        if not refs:
            continue
        step = node.id[: -len("~each")] if node.id.endswith("~each") else node.id
        for edge in edges_by_target.get(node.id, []):
            source_spec = node_specs.get(edge.source)
            if edge.kind is EdgeKind.ERROR or source_spec is None or source_spec.dynamic_output:
                continue
            mappings = edge.data.get("mappings")
            source_path = mappings.get("items") if isinstance(mappings, dict) else "items"
            if not isinstance(source_path, str) or source_path == _WHOLE_PAYLOAD_SOURCE:
                continue
            s_root = model_json_schema(source_spec.output_schema)
            list_schema = schema_at_path(s_root, source_path)
            element = item_schema_of(list_schema, s_root) if list_schema is not None else None
            if element is None:
                continue
            for key, ref in refs.items():
                value_schema = (
                    element
                    if ref == "$item"
                    else schema_at_path(s_root, ref[len("$item."):], start=element)
                )
                shape = _object_shape(value_schema, s_root)
                if shape is None:
                    continue
                fields = (
                    declared_field_names(resolve_ref(value_schema, s_root)) if shape == "record" else []
                )
                issues.append(
                    ValidationIssue(
                        path=f"nodes[{node.id}].data.config.payload_template.{key}",
                        node_id=step,
                        edge_id=edge.id,
                        severity="warning",
                        message=(
                            f"'{target_id}' takes text for '{key}', but '{ref}' is a whole {shape} "
                            f"(one element of '{source_path}' on '{edge.source}'"
                            + (f", fields {fields}" if fields else "")
                            + "), so the run will send all of it as JSON text. "
                            + _text_fix_hint(ref, shape)
                        ),
                    )
                )

    # 2. Edge mappings: `target_key <- source path` onto a text-only input.
    for edge in definition.edges:
        mappings = edge.data.get("mappings")
        source_spec = node_specs.get(edge.source)
        target = text_props(edge.target)
        if (
            edge.kind is EdgeKind.ERROR
            or not isinstance(mappings, dict)
            or source_spec is None
            or source_spec.dynamic_output
            or target is None
        ):
            continue
        t_root, t_props = target
        s_root = model_json_schema(source_spec.output_schema)
        for target_key, source_key in mappings.items():
            if (
                not isinstance(target_key, str)
                or not isinstance(source_key, str)
                or source_key == _WHOLE_PAYLOAD_SOURCE
                or not _text_only_input(t_props.get(target_key), t_root)
            ):
                continue
            shape = _object_shape(schema_at_path(s_root, source_key), s_root)
            if shape is None:
                continue
            issues.append(
                ValidationIssue(
                    path=f"edges[{edge.id}].data.mappings.{target_key}",
                    edge_id=edge.id,
                    node_id=edge.target,
                    severity="warning",
                    message=(
                        f"'{edge.target}' takes text for '{target_key}', but '{source_key}' on "
                        f"'{edge.source}' is a whole {shape}, so the run will send all of it as JSON "
                        f"text. Map one of its text fields instead for a tighter input."
                    ),
                )
            )
    return issues


# --- THE UNRENDERED-PLACEHOLDER GATE (W68, 2026-09-12) --------------------
# ``{{name}}`` (and the engine's own single-brace ``{name}``) is filled in by
# exactly one thing: a node type that declares ``renders_input_templates`` —
# today only ``text.template`` — or ONE input a step declares with
# ``field_extras(renders_template=True)`` (notify.* bodies and send-once keys,
# 2026-10-27). Everywhere else an authored placeholder is
# LITERAL TEXT that reaches the tool, the model or the database as-is. The
# Masterwork Conductor wrote ``{{sealed_case_id}}`` into an
# ``ai.chat.manual`` node's ``user_input``; the save gate said nothing
# and the run died on "invalid input syntax for type uuid".
_DOUBLE_PLACEHOLDER = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_.]*)\s*\}\}")
# Single braces only when the token is clearly a NAME — never a regex
# quantifier ("\\d{3}"), never a brace pair that is part of a "{{…}}".
_SINGLE_PLACEHOLDER = re.compile(r"(?<!\{)\{([A-Za-z_][A-Za-z0-9_.]*)\}(?!\})")


# Config fields read by THE ONE path resolver (``matrx_graph.paths``), keyed by
# node type. Other ``*_path`` config fields use the content-IR accessor, whose
# grammar differs (``items[]`` is lawful there), so they are not checked here.
_RESOLVER_CONFIG_PATHS: dict[str, tuple[str, ...]] = {
    "output.to_frontend": ("payload_key",),
    "text.json_path": ("path",),
}


def _config_path_syntax_issues(definition: Definition) -> list[ValidationIssue]:
    """A config path the one resolver cannot read is an ERROR naming the step and field."""
    issues: list[ValidationIssue] = []
    for node in definition.nodes:
        fields = _RESOLVER_CONFIG_PATHS.get(node.type or "")
        config = node.data.get("config") if isinstance(node.data, dict) else None
        if not fields or not isinstance(config, dict):
            continue
        for field in fields:
            value = config.get(field)
            if not isinstance(value, str) or not value:
                continue
            syntax = path_syntax_problem(value)
            if syntax is not None:
                issues.append(
                    ValidationIssue(
                        path=f"nodes[{node.id}].data.config.{field}",
                        node_id=node.id,
                        message=f"Step '{node.id}' field '{field}' = '{value}' is not a readable path: {syntax}.",
                    )
                )
    return issues


def _placeholders_in(value: Any, path: str = "") -> list[tuple[str, str]]:
    """(input path, placeholder text) for every unrenderable slot in a literal."""
    found: list[tuple[str, str]] = []
    if isinstance(value, str):
        for match in _DOUBLE_PLACEHOLDER.finditer(value):
            found.append((path, match.group(0)))
        for match in _SINGLE_PLACEHOLDER.finditer(value):
            found.append((path, match.group(0)))
    elif isinstance(value, dict):
        # A marker dict ({'$input': name} / {'$var': name}) is the RESOLVED
        # way to reference a run value — never a placeholder.
        if any(k in value for k in ("$input", "$var")):
            return found
        for key, sub in value.items():
            found.extend(_placeholders_in(sub, f"{path}.{key}" if path else str(key)))
    elif isinstance(value, list):
        for index, sub in enumerate(value):
            found.extend(_placeholders_in(sub, f"{path}[{index}]"))
    return found


def _template_rendered_inputs(spec: NodeSpec) -> frozenset[str]:
    """Inputs the step itself fills placeholders in — declared per field with
    ``field_extras(renders_template=True)`` (notify.* message bodies and send-once keys)."""
    props = spec.input_json_schema().get("properties") or {}
    return frozenset(
        name for name, prop in props.items() if isinstance(prop, dict) and prop.get(RENDERS_TEMPLATE_KEY)
    )


def _unrendered_placeholder_issues(
    definition: Definition,
    node_specs: dict[str, NodeSpec],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for node in definition.nodes:
        spec = node_specs.get(node.id)
        if spec is None or spec.renders_input_templates:
            continue
        raw_static = node.data.get("input")
        if not isinstance(raw_static, dict):
            raw_static = node.data.get("inputs")
        if not isinstance(raw_static, dict):
            continue
        rendered = _template_rendered_inputs(spec)
        for input_path, placeholder in _placeholders_in(raw_static):
            if re.split(r"[.\[]", input_path, maxsplit=1)[0] in rendered:
                continue
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].data.inputs.{input_path}",
                    node_id=node.id,
                    code="unrendered_placeholder",
                    message=(
                        f"Input '{input_path}' on step '{node.id}' (type "
                        f"'{node.spec_type}') contains the placeholder "
                        f"{placeholder}, but {node.spec_type} does not render "
                        f"templates — the step receives those characters "
                        f"VERBATIM, and the run fails on the literal text. "
                        f"Route the value in instead: reference a workflow "
                        f"input directly with {{'$input': "
                        f"'{placeholder.strip('{}').strip()}'}} when it IS the "
                        f"whole value, or build the text with a 'Fill a "
                        f"Template' step (text.template — the one node type "
                        f"that fills {{{{placeholders}}}}) fed by a 'Collect "
                        f"Inputs' step, and map its output into this input "
                        f"with an edge."
                    ),
                )
            )
    return issues


# Node types whose inputs are assembled by the ENGINE at run time, not by the
# author — a static required-input check over them would be pure noise, so each
# is excluded BY NAME with its reason (never a silent pass):
#   * io.user_input — its values are the run form's answers, delivered by the
#     scheduler from the compiled input surface (``_surface_node_seed``).
_DYNAMIC_INPUT_NODE_TYPES: dict[str, str] = {
    "io.user_input": (
        "its values are the run form's answers, seeded by the scheduler from "
        "the compiled input surface"
    ),
    "io.trigger": (
        "its values are a fire's (or the run form's) answers, seeded by the "
        "scheduler from the compiled input surface"
    ),
}

# Edge kinds that actually deliver a payload into the target's inputs. A
# CONTROL edge is deliberately ABSENT: the scheduler binds ``fragment = {}``
# for it (``Scheduler._bind_delivery`` / ``_route_outputs``) — it transfers
# control and nothing else. A STREAM edge neither joins nor routes.
_DELIVERING_KINDS = (EdgeKind.DATA, EdgeKind.CONDITIONAL, EdgeKind.ERROR)

# Edge kinds that OPEN a firing on the target (so the target is not an entry
# node the run seeds) even when they deliver no payload — CONTROL included.
_FIRING_KINDS = (EdgeKind.DATA, EdgeKind.CONDITIONAL, EdgeKind.CONTROL, EdgeKind.ERROR)

# What a BROADCAST (no-mappings) ERROR edge delivers — the structured NodeError
# dump, the same three keys the mapping check addresses above.
_ERROR_PAYLOAD_KEYS = frozenset({"code", "message", "details"})


def _required_input_names(model: type[BaseModel]) -> list[str]:
    """Every field of an input schema the author MUST supply, by the name the
    author writes (alias when the model declares one)."""
    names: list[str] = []
    for field_name, field in model.model_fields.items():
        if not field.is_required():
            continue
        alias = field.alias if isinstance(field.alias, str) and field.alias else None
        names.append(alias or field_name)
    return names


def _required_input_issues(
    definition: Definition,
    node_specs: dict[str, NodeSpec],
    surface_names: set[str],
) -> list[ValidationIssue]:
    """A DEFINITION THAT SAVES IS A DEFINITION THAT CAN START (W68, 2026-09-12).

    Every required field of a node's registered ``input_schema`` must have a
    source at save time, because the run-time gate
    (``spec.input_schema.model_validate(merged_inputs)`` in the scheduler,
    ``Cause.MISSING_INPUT``) is fed by exactly two authored channels:

      * ``data.inputs`` / ``data.input`` — the node's static literals, with
        ``{'$input': …}`` / ``{'$var': …}`` markers resolved (the compiler reads
        them into ``CompiledNode.static_inputs``; ``resolve_invocation_inputs``
        merges them under the invocation payload);
      * an inbound delivering edge — its ``mappings`` target keys, or, with no
        mappings, the upstream's whole payload.

    plus, for an entry node, the run's compiled INPUT SURFACE.

    Live, 2026-09-12: the Masterwork Conductor moved an
    ``ai.chat.manual`` node's five inputs under ``data.config``, got only
    "Extra inputs are not permitted" back, deleted them one by one, and SAVED a
    node with no inputs at all (workflow 805c1a98). The run died at step 1 on
    ``model``. Same law as the expression sandbox above: a save that passes and
    a run that dies at step 1 costs an Expert a whole run.

    The check is deliberately conservative — it must never reject a definition a
    run would accept. It goes silent (per node) on anything whose inputs the
    engine assembles at run time: a broadcast inbound edge (payload keys unknown
    until the upstream emits), a dispatcher's ``target_node_id`` (``ctx.send``
    payloads), a kind-triggered node (the subscription matcher builds its
    inputs), an enabled ``mock_response`` (the scheduler short-circuits before
    the input gate), and the node types named in
    ``_DYNAMIC_INPUT_NODE_TYPES``.
    """
    issues: list[ValidationIssue] = []

    # Targets the engine feeds by ctx.send at run time — never statically wired.
    dispatch_targets: set[str] = set()
    for node in definition.nodes:
        if node.spec_type not in DISPATCHER_NODE_TYPES:
            continue
        target = node.config.get("target_node_id") if isinstance(node.config, dict) else None
        if isinstance(target, str) and target:
            dispatch_targets.add(target)

    inbound: dict[str, list[Any]] = {}
    fired_by_edge: set[str] = set()
    for edge in definition.edges:
        if edge.kind in _FIRING_KINDS:
            fired_by_edge.add(edge.target)
        if edge.kind in _DELIVERING_KINDS:
            inbound.setdefault(edge.target, []).append(edge)

    for node in definition.nodes:
        spec = node_specs.get(node.id)
        if spec is None:
            continue  # unknown/removed type — already reported
        required = _required_input_names(spec.input_schema)
        if not required:
            continue
        if node.spec_type in _DYNAMIC_INPUT_NODE_TYPES:
            continue
        if node.id in dispatch_targets:
            continue
        if node.data.get("trigger_kind") is not None:
            continue
        raw_mock = node.data.get("mock_response")
        if isinstance(raw_mock, dict) and raw_mock.get("enabled") is True:
            continue

        supplied: set[str] = set()
        raw_static = node.data.get("input")
        if not isinstance(raw_static, dict):
            raw_static = node.data.get("inputs")
        if isinstance(raw_static, dict):
            supplied.update(k for k in raw_static if isinstance(k, str))

        edges_in = inbound.get(node.id, [])
        unprovable = False
        for edge in edges_in:
            mappings = edge.mappings
            if mappings is None:
                if edge.kind is EdgeKind.ERROR:
                    supplied.update(_ERROR_PAYLOAD_KEYS)
                    continue
                # Broadcast: the whole upstream payload lands, and its keys are
                # only known once the upstream runs. Nothing is provable here.
                unprovable = True
                break
            supplied.update(k for k in mappings if isinstance(k, str))
        if unprovable:
            continue

        # An ENTRY node (no edge fires it) is seeded at run start: from the
        # compiled input surface (a declared name IS a source) and, for a
        # host- or trigger-started run, from the caller's broadcast ``inputs``
        # / ``node_inputs`` — names no definition can declare (a data-change
        # trigger builds them from the changed row: see aidream's
        # ``fire_from_event_watcher`` → ``build_event_inputs``). So an entry
        # node's gap is a WARNING that names what the caller must pass; only a
        # gap the definition PROVES — a node fired by edges that demonstrably
        # do not carry the field — is an error.
        is_entry = node.id not in fired_by_edge
        if is_entry:
            supplied.update(surface_names)

        missing = [name for name in required if name not in supplied]
        if not missing:
            continue
        if is_entry:
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].data.inputs",
                    node_id=node.id,
                    severity="warning",
                    code="missing_input",
                    fields=list(missing),
                    message=(
                        f"Step '{node.id}' (type '{node.spec_type}') starts the run "
                        f"and nothing in this workflow supplies its required "
                        f"input{'s' if len(missing) > 1 else ''} "
                        f"{format_options(missing, 10)} — the run fails at step 1 "
                        f"with missing_input unless whoever starts it passes "
                        f"{'those names' if len(missing) > 1 else 'that name'} as run "
                        f"input (which a person filling the run form cannot do: the "
                        f"form is built from the workflow's declared inputs). Put "
                        f"{'each value' if len(missing) > 1 else 'the value'} under "
                        f"data.inputs, add a 'Collect Inputs' step declaring "
                        f"{'them' if len(missing) > 1 else 'it'}, or wire an edge "
                        f"that supplies {'them' if len(missing) > 1 else 'it'}. "
                        f"data.config is NOT where inputs go."
                    ),
                )
            )
            continue
        issues.append(
            ValidationIssue(
                path=f"nodes[{node.id}].data.inputs",
                node_id=node.id,
                code="missing_input",
                fields=list(missing),
                message=(
                    f"Step '{node.id}' (type '{node.spec_type}') has no source for "
                    f"required input{'s' if len(missing) > 1 else ''} "
                    f"{format_options(missing, 10)}: nothing in data.inputs, and no "
                    f"incoming connection carries "
                    f"{'them' if len(missing) > 1 else 'it'} (a control connection "
                    f"transfers control only — it delivers no payload at all). This "
                    f"definition would save and then fail at this step with "
                    f"missing_input. Put "
                    f"{'each value' if len(missing) > 1 else 'the value'} under "
                    f"data.inputs (a literal, or a {{'$input': 'name'}} reference to a "
                    f"workflow input), or map "
                    f"{'them' if len(missing) > 1 else 'it'} on a data connection into "
                    f"'{node.id}'. data.config is NOT where inputs go."
                ),
            )
        )
    return issues


def _template_path_issues(
    definition: Definition,
    node_specs: dict[str, NodeSpec],
) -> list[ValidationIssue]:
    """``$item.<path>`` templates checked against the ELEMENT schema upstream.

    An edge mapping's source path has been checked against the upstream output
    schema since 2026-09-11 — but the ``$item`` template INSIDE a list-shaping
    node was never checked against anything, so the paths were authored blind
    and died mid-run. Live, 2026-09-12: the Newsroom Desk's "Keep only the
    ledger entries" step templated ``$item.entries`` over elements of
    ``gather_result.values`` (the RAW per-item agent results, whose fields are
    ``structured_output`` / ``final_text`` / ``messages`` …) — a path that could
    never resolve, after four paid ledger agents had already run.

    Same discipline as the mapping check: an ERROR only where the element schema
    is DESCRIBED and CLOSED and provably lacks the segment; total silence where
    the element is a ``JsonValue`` or any other undescribed shape (which is the
    gather case — that one is caught at run time instead, by a message that
    names the keys item 0 actually has).
    """
    issues: list[ValidationIssue] = []
    edges_by_target: dict[str, list[Any]] = {}
    for edge in definition.edges:
        edges_by_target.setdefault(edge.target, []).append(edge)

    for node in definition.nodes:
        host = TEMPLATE_HOSTS.get(node.spec_type)
        if host is None:
            continue
        config_key, list_input = host
        template = node.config.get(config_key) if isinstance(node.config, dict) else None
        paths = template_item_paths(template)
        if not paths:
            continue
        for edge in edges_by_target.get(node.id, []):
            if edge.kind is EdgeKind.ERROR:
                continue
            source_spec = node_specs.get(edge.source)
            if source_spec is None or source_spec.dynamic_output:
                continue
            mappings = edge.data.get("mappings")
            if isinstance(mappings, dict):
                if list_input not in mappings:
                    continue
                source_path = mappings[list_input]
                if not isinstance(source_path, str) or source_path == _WHOLE_PAYLOAD_SOURCE:
                    continue
            else:
                # Broadcast edge: the payload's own `<list_input>` key lands on
                # the input of the same name.
                source_path = list_input
            root = model_json_schema(source_spec.output_schema)
            list_schema = schema_at_path(root, source_path)
            if list_schema is None:
                continue
            element = item_schema_of(list_schema, root)
            if not is_described(element):
                continue  # JsonValue / undescribed element — nothing provable
            for path in paths:
                problem = path_problem(
                    root,
                    path,
                    start=element,
                    origin=f"one element of '{source_path}'",
                )
                if problem is None:
                    continue
                issues.append(
                    ValidationIssue(
                        path=f"nodes[{node.id}].data.config.{config_key}",
                        node_id=node.id,
                        edge_id=edge.id,
                        message=(
                            f"Template path '$item.{path}' can never resolve against "
                            f"the elements this step receives: '{list_input}' comes "
                            f"from '{source_path}' on node '{edge.source}' (type "
                            f"'{source_spec.node_type}'), and {problem}. One element "
                            f"offers {declared_field_names(element)} — point the "
                            f"template at one of those, or map '{list_input}' from a "
                            f"different upstream field."
                        ),
                    )
                )
    return issues


# --- THE MIXED-INBOUND RULE (ENGINE_SPEC §3.3, 2026-10-27) ----------------
# A pruned edge counts as resolved (join ``all``), so a step fed by a
# CONDITIONAL edge AND a plain edge runs when the condition is false too —
# with only the plain half. That is the designed join (merge steps with an
# optional arm rely on it; workflows STATE rule 2). The trap is a step that
# READS the conditional half unguarded (``inputs['saved']``): it waits
# correctly, then fails with KeyError on every false condition (aidream
# kit.save_output run 81a05e96). Flagged at save, never blocked.
_INPUT_SUBSCRIPT = re.compile(r"""inputs\[\s*['"]([A-Za-z_][A-Za-z0-9_]*)['"]\s*\]""")


def _strings_in(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for v in value.values() for s in _strings_in(v)]
    if isinstance(value, list):
        return [s for v in value for s in _strings_in(v)]
    return []


def _broadcast_keys(source: Any, spec: NodeSpec | None) -> set[str] | None:
    """The keys a plain broadcast edge from ``source`` certainly delivers, or
    None when they cannot be known (then it may deliver anything: no warning)."""
    if source is None:
        return None
    if source.type == "data.transform":
        from matrx_graph.nodes.data.transform import expression_output_shape

        expression = ((source.data or {}).get("config") or {}).get("expression")
        shape = expression_output_shape(expression) if isinstance(expression, str) else None
        return set(shape[0]) if shape is not None else None
    if spec is None or spec.dynamic_output:
        return None
    props, closed = _schema_props(spec.output_schema)
    return props if closed else None


def _required_inputs(spec: NodeSpec | None) -> set[str]:
    if spec is None:
        return set()
    schema = model_json_schema(spec.input_schema)
    required = schema.get("required")
    return set(required) if isinstance(required, list) else set()


def _half_fed_step_issues(
    definition: Definition, node_specs: dict[str, NodeSpec] | None = None
) -> list[ValidationIssue]:
    node_specs = node_specs or {}
    issues: list[ValidationIssue] = []
    inbound: dict[str, list[EdgeDef]] = {}
    for edge in definition.edges:
        if edge.kind in (EdgeKind.DATA, EdgeKind.CONDITIONAL, EdgeKind.CONTROL):
            inbound.setdefault(edge.target, []).append(edge)
    nodes = {n.id: n for n in definition.nodes}
    labels = {n.id: str((n.data or {}).get("label") or n.id) for n in definition.nodes}
    for node in definition.nodes:
        edges = inbound.get(node.id, [])
        conditional = [e for e in edges if e.kind is EdgeKind.CONDITIONAL]
        plain = [e for e in edges if e.kind is not EdgeKind.CONDITIONAL]
        if not conditional or not plain:
            continue
        plain_keys: set[str] = set()
        plain_unknown = False
        for e in plain:
            if e.kind is EdgeKind.CONTROL:
                continue
            if e.mappings:
                plain_keys |= set(e.mappings)
                continue
            keys = _broadcast_keys(nodes.get(e.source), node_specs.get(e.source))
            if keys is None:
                plain_unknown = True
            else:
                plain_keys |= keys
        if plain_unknown:
            continue  # a plain broadcast of unknown keys may carry anything
        static = (node.data or {}).get("input")
        if isinstance(static, dict):
            plain_keys |= set(static)
        texts = _strings_in((node.data or {}).get("config") or {})
        read_unguarded = {
            key
            for t in texts
            for key in _INPUT_SUBSCRIPT.findall(t)
            if not re.search(rf"""['"]{key}['"]\s+in\s+inputs""", t)
        }
        required = _required_inputs(node_specs.get(node.id))
        for edge in conditional:
            if edge.mappings:
                delivered = set(edge.mappings)
            else:
                # A broadcast conditional edge: whatever the step reads that no
                # plain edge supplies can only come from it.
                keys = _broadcast_keys(nodes.get(edge.source), node_specs.get(edge.source))
                delivered = keys if keys is not None else read_unguarded | required
            for key in sorted(delivered - plain_keys):
                if key in read_unguarded:
                    why = f"so inputs['{key}'] fails. Feed this step only from " \
                        f"'{labels.get(edge.source, edge.source)}', or check '{key}' in inputs first."
                elif key in required:
                    why = f"and '{key}' is a required input, so the step fails. Feed this step only " \
                        f"from '{labels.get(edge.source, edge.source)}', or make every connection into it conditional."
                else:
                    continue
                issues.append(
                    ValidationIssue(
                        path=f"nodes[{node.id}].data.config",
                        node_id=node.id,
                        edge_id=edge.id,
                        severity="warning",
                        message=(
                            f"'{labels[node.id]}' also runs when the condition on connection '{edge.id}' is "
                            f"false, with '{key}' missing, {why}"
                        ),
                    )
                )
    return issues


# --- A STEP JOINED TO A CHECKED PATH (2026-10-27) --------------------------
# When a step FAILS and its ERROR connection catches it, everything on its
# normal path stops — including a step that ALSO has inputs from another branch
# (it used to run on those alone: "Release a panel version" run f308bcea ran its
# save after the Safety Check failed). Say so at save, so a definition that
# counted on the old behavior learns it now stops, and how to keep it running.
def _failure_joined_step_issues(
    definition: Definition, node_specs: dict[str, NodeSpec] | None = None
) -> list[ValidationIssue]:
    """The scheduler's rule, run statically for each step that can fail into an ERROR
    connection: which steps does its failure stop, and which of those still had another
    input arriving (the ones that used to run on it alone)."""
    node_specs = node_specs or {}
    joinable = (EdgeKind.DATA, EdgeKind.CONDITIONAL, EdgeKind.CONTROL)
    out_edges: dict[str, list[EdgeDef]] = {}
    in_sources: dict[str, set[str]] = {}
    for edge in definition.edges:
        out_edges.setdefault(edge.source, []).append(edge)
        if edge.kind in joinable:
            in_sources.setdefault(edge.target, set()).add(edge.source)
    nodes = {n.id: n for n in definition.nodes}
    # A For Each / loop reaches its target by dispatch, not a connection.
    for node in definition.nodes:
        target = ((node.data or {}).get("config") or {}).get("target_node_id")
        if node.spec_type in DISPATCHER_NODE_TYPES and isinstance(target, str) and target in nodes:
            in_sources.setdefault(target, set()).add(node.id)
    labels = {n.id: str((n.data or {}).get("label") or n.id) for n in definition.nodes}

    def policy(node_id: str) -> str:
        spec = node_specs.get(node_id)
        return nodes[node_id].data.get("join_policy") or getattr(spec, "default_join_policy", None) or "all"

    issues: list[ValidationIssue] = []
    warned: set[str] = set()
    for failing in definition.nodes:
        error_targets = {e.target for e in out_edges.get(failing.id, []) if e.kind is EdgeKind.ERROR}
        if not error_targets or failing.optional:
            continue
        recovery: set[str] = set()
        frontier = list(error_targets)
        while frontier:
            current = frontier.pop()
            if current in recovery or current == failing.id:
                continue
            recovery.add(current)
            frontier.extend(e.target for e in out_edges.get(current, []))
        # Fixpoint: a step is stopped when an input comes from the failed step or a stopped
        # step, the failure's own error path does not lead into it, and it is not 'any'.
        stopped: set[str] = set()
        changed = True
        while changed:
            changed = False
            for node_id, sources in in_sources.items():
                if node_id in stopped or node_id == failing.id or node_id in error_targets:
                    continue
                if not sources & (stopped | {failing.id}):
                    continue
                if sources & (recovery - stopped) or (
                    policy(node_id) == "any" and sources - stopped - {failing.id}
                ):
                    continue
                stopped.add(node_id)
                changed = True
        for node_id in sorted(stopped):
            others = sorted(in_sources.get(node_id, set()) - stopped - {failing.id})
            if not others or node_id in warned:
                continue
            warned.add(node_id)
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node_id}]",
                    node_id=node_id,
                    severity="warning",
                    message=(
                        f"'{labels[node_id]}' does not run when '{labels[failing.id]}' fails, even "
                        f"though '{labels[others[0]]}' still arrives. To run it without "
                        f"'{labels[failing.id]}', mark '{labels[failing.id]}' optional."
                    ),
                )
            )
    return issues


# --- A STEP JOINED TO A SKIPPED STEP (2026-11-07, ENGINE_SPEC §3.3b) ----------
# A step its 'Only when' said no to is SKIPPED, and what reads from it does not run on its
# other inputs (it used to run with that input missing: research search, L7a). Say so at
# save, so a definition that counted on the old behavior learns it now stops, and how to
# keep it running.
def skip_joined_steps(
    definition: Definition, node_specs: dict[str, NodeSpec] | None = None
) -> list[tuple[str, str, str]]:
    """The scheduler's §3.3b rule, run statically on an EXPANDED definition, for each step
    with an 'Only when': (stopped step, skipped step, another input that still arrives) for
    every step its skip stops although another input still arrives — the steps that ran on
    the other inputs alone before 2026-11-07."""
    from matrx_graph.step_settings import when_gate_owner

    node_specs = node_specs or {}
    nodes = {n.id: n for n in definition.nodes}
    payload_kinds = (EdgeKind.DATA, EdgeKind.CONDITIONAL)
    in_edges: dict[str, list[EdgeDef]] = {}
    for edge in definition.edges:
        if edge.kind in payload_kinds or edge.kind is EdgeKind.CONTROL:
            in_edges.setdefault(edge.target, []).append(edge)
    skippable = sorted(
        {e.target for e in definition.edges if e.kind is EdgeKind.CONDITIONAL and when_gate_owner(e.source) == e.target}
    )

    def policy(node_id: str) -> str:
        spec = node_specs.get(node_id)
        return nodes[node_id].data.get("join_policy") or getattr(spec, "default_join_policy", None) or "all"

    def fields(edge: EdgeDef) -> set[str]:
        return set(edge.mappings) if edge.mappings is not None else {"*"}

    found: list[tuple[str, str, str]] = []
    for skipped in skippable:
        stopped: set[str] = set()
        changed = True
        while changed:
            changed = False
            for node_id, edges in in_edges.items():
                node = nodes.get(node_id)
                if node is None or node_id in stopped or node_id == skipped:
                    continue
                dead = stopped | {skipped}
                marked = [e for e in edges if e.source in dead and e.kind in payload_kinds]
                if not marked:
                    continue
                live = [e for e in edges if e.source not in dead]
                if not live:
                    stopped.add(node_id)  # every input gone: pruned before 2026-11-07 too
                    changed = True
                    continue
                if (
                    policy(node_id) == "any"
                    or node.data.get("when_input_skipped") == "run"
                    or node.spec_type in _COLLECTOR_NODE_TYPES
                ):
                    continue
                arrived: set[str] = set()
                for e in live:
                    if e.kind is not EdgeKind.CONTROL:
                        arrived |= fields(e)
                if all(fields(e) <= arrived for e in marked):
                    continue  # a rejoin: another connection brings the same input
                stopped.add(node_id)
                changed = True
        for node_id in sorted(stopped):
            live = sorted({e.source for e in in_edges.get(node_id, []) if e.source not in stopped | {skipped}})
            if live:
                found.append((node_id, skipped, live[0]))
    return found


def _skip_joined_step_issues(
    definition: Definition, node_specs: dict[str, NodeSpec] | None = None
) -> list[ValidationIssue]:
    from matrx_graph.step_settings import owner_of

    labels = {n.id: str((n.data or {}).get("label") or n.id) for n in definition.nodes}
    issues: list[ValidationIssue] = []
    warned: set[str] = set()
    for node_id, skipped, other in skip_joined_steps(definition, node_specs):
        shown = owner_of(node_id) or node_id
        if shown in warned:
            continue
        warned.add(shown)
        issues.append(
            ValidationIssue(
                path=f"nodes[{shown}]",
                node_id=shown,
                severity="warning",
                message=(
                    f"'{labels.get(shown, shown)}' does not run when '{labels.get(skipped, skipped)}' is "
                    f"skipped, even though '{labels.get(owner_of(other) or other, other)}' still arrives. "
                    f"To run it anyway, set its 'when_input_skipped' to 'run'."
                ),
            )
        )
    return issues


def _kind_routing_issues(definition: Definition) -> list[ValidationIssue]:
    """Kind-filtered edges, fan-out modes, and kind-triggered nodes (§7.3/§7.4/§7.7c).

    Three findings, each a real authoring mistake rather than a style note:

    * a malformed declaration (a typo in ``fan_out`` would fan a paid step the
      wrong number of times, so it is an ERROR, never a best guess);
    * a trigger node with an inbound edge — a contradiction: two mechanisms
      would each try to open its firing and the author could not tell which
      one did;
    * an ``each`` edge with no kind filter whose source cannot offer a list.
      That one is a WARNING, not an error: the source's shape is only fully
      known at run time, and refusing to save a definition over a shape guess
      would block legitimate authoring.
    """
    from matrx_graph.content_ir.edge_routing import (
        EdgeRoutingDeclarationError,
        parse_edge_routing,
    )
    from matrx_graph.content_ir.triggers import TriggerDeclarationError, parse_node_trigger

    issues: list[ValidationIssue] = []
    trigger_nodes: set[str] = set()

    for node in definition.nodes:
        try:
            trigger = parse_node_trigger(node.data)
        except TriggerDeclarationError as exc:
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node.id}].data.trigger_kind",
                    node_id=node.id,
                    message=str(exc),
                )
            )
            continue
        if trigger is not None:
            trigger_nodes.add(node.id)

    inbound: dict[str, list[str]] = {}
    for edge in definition.edges:
        inbound.setdefault(edge.target, []).append(edge.id)
        try:
            routing = parse_edge_routing(edge.data)
        except EdgeRoutingDeclarationError as exc:
            issues.append(
                ValidationIssue(
                    path=f"edges[{edge.id}].data",
                    edge_id=edge.id,
                    message=str(exc),
                )
            )
            continue
        if routing.fans_out and routing.kind_filter is None and edge.sourceHandle is None:
            issues.append(
                ValidationIssue(
                    path=f"edges[{edge.id}].data.fan_out",
                    edge_id=edge.id,
                    node_id=edge.source,
                    severity="warning",
                    message=(
                        f"Edge '{edge.id}' fans out per item but names no kind "
                        "filter and no source handle, so at run time it must "
                        f"find exactly one list in whatever '{edge.source}' "
                        "produces. If that step's output has several lists (or "
                        "none), the edge will report that it cannot fan out. "
                        "Naming a kind filter removes the guess."
                    ),
                )
            )

    for node_id in sorted(trigger_nodes):
        edge_ids = inbound.get(node_id, [])
        if edge_ids:
            issues.append(
                ValidationIssue(
                    path=f"nodes[{node_id}].data.trigger_kind",
                    node_id=node_id,
                    message=(
                        f"Step '{node_id}' declares a kind trigger AND has "
                        f"{len(edge_ids)} incoming edge(s) ({', '.join(sorted(edge_ids))}). "
                        "A triggered step is fired by the kind appearing "
                        "anywhere in the run — it is deliberately wired to "
                        "nothing. Either remove the incoming edges (keep the "
                        "trigger) or remove trigger_kind (keep the wiring)."
                    ),
                )
            )

    return issues

_BINDABLE_SETTING_TYPES: tuple[type, ...] = (int, float, bool, str)

#: ``json_schema_extra`` key a step puts on a list/object setting that a run input MAY supply —
#: a table the caller edits (``data.rules`` ``rules``), never one that shapes the graph. The run's
#: value is validated through the step's own settings model on every invocation, exactly as an
#: authored table is (a bad predicate fails the step by row). Arman 2026-10-27, units 8 and 9 rulings.
RUN_INPUT_SETTING_KEY = "x-run-input"


def _opted_in_setting(field: Any) -> bool:
    extra = getattr(field, "json_schema_extra", None)
    return isinstance(extra, dict) and extra.get(RUN_INPUT_SETTING_KEY) is True


def _bindable_setting(annotation: Any) -> bool:
    """A config field a run input may set: a scalar (int / float / bool / str), optionally
    ``Optional`` — sizes, counts, flags and short text. Never a node type, a nested
    object or a list: those shape the graph, and a run must not reshape it."""
    import types as _types
    from typing import Literal, Union, get_args, get_origin

    if annotation in _BINDABLE_SETTING_TYPES:
        return True
    origin = get_origin(annotation)
    if origin is Literal:
        return all(isinstance(a, _BINDABLE_SETTING_TYPES) for a in get_args(annotation))
    if origin in (Union, _types.UnionType):
        args = [a for a in get_args(annotation) if a is not type(None)]
        return bool(args) and all(_bindable_setting(a) for a in args)
    return False


def declared_input_defaults(definition: Any) -> dict[str, Any]:
    """Each declared input's default (variables + io.user_input fields) — a setting's stand-in."""
    out: dict[str, Any] = {}
    for v in getattr(definition, "variables", None) or []:
        if getattr(v, "defaultValue", None) is not None:
            out[v.name] = v.defaultValue
    for node in getattr(definition, "nodes", None) or []:
        if node.spec_type not in ("io.user_input", "io.trigger") or not isinstance(node.config, dict):
            continue
        for fld in node.config.get("fields") or []:
            if not isinstance(fld, dict):
                continue
            name = fld.get("key") or fld.get("name")  # old shape / the declaration
            value = fld.get("default") if "default" in fld else fld.get("defaultValue")
            if isinstance(name, str) and value is not None:
                out.setdefault(name, value)
    return out


def split_setting_refs(
    config_schema: type[BaseModel], raw_config: dict[str, Any], input_defaults: dict[str, Any] | None = None
) -> tuple[dict[str, Any], dict[str, dict[str, Any]], list[str]]:
    """Take ``{"$input": name}`` settings out of ``raw_config``: returns the config with each
    replaced by its compile-time stand-in (the ref's ``default``, else the input's declared
    default, else the field's own default), ``field → ref``, and a sentence per ref on a field that cannot take one."""
    from matrx_graph.types.variables import is_input_ref

    refs: dict[str, dict[str, Any]] = {}
    problems: list[str] = []
    out = dict(raw_config or {})
    for key, value in list(out.items()):
        if not is_input_ref(value):
            nested = _nested_settings_model(config_schema.model_fields.get(key))
            if nested is not None and isinstance(value, dict):
                out[key] = _split_nested_number_refs(key, nested, value, input_defaults, refs, problems)
            continue
        field = config_schema.model_fields.get(key)
        if field is None or not (_bindable_setting(field.annotation) or _opted_in_setting(field)):
            problems.append(
                f"setting '{key}' cannot come from a run input — only number, yes/no and "
                "short text settings can (sizes, counts, flags), and tables a step marks as editable "
                "per run (data.rules `rules`)"
            )
            continue
        refs[key] = dict(value)
        if "default" in value:
            out[key] = value["default"]
        elif value["$input"] in (input_defaults or {}):
            out[key] = (input_defaults or {})[value["$input"]]
        else:
            out.pop(key)  # the field's own default stands in (a required one fails validation)
    return out, refs, problems


def _nested_settings_model(field: Any) -> type[BaseModel] | None:
    """The settings object a config field holds (``escalation: EscalationPolicy | None``)."""
    import types as _types
    from typing import Union, get_args, get_origin

    if field is None:
        return None
    annotation = field.annotation
    if get_origin(annotation) in (Union, _types.UnionType):
        args = [a for a in get_args(annotation) if a is not type(None)]
        annotation = args[0] if len(args) == 1 else None
    return annotation if isinstance(annotation, type) and issubclass(annotation, BaseModel) else None


def _split_nested_number_refs(
    key: str,
    model: type[BaseModel],
    value: dict[str, Any],
    input_defaults: dict[str, Any] | None,
    refs: dict[str, dict[str, Any]],
    problems: list[str],
) -> dict[str, Any]:
    """One level down: a NUMBER inside a settings object may come from a run input too
    (``escalation.after_seconds`` — an organization-chosen wait). Recorded as the dotted
    path ``"<key>.<field>"``; the object's own checks (minimums) still apply to the value."""
    import types as _types
    from typing import Union, get_args, get_origin

    from matrx_graph.types.variables import is_input_ref

    inner = dict(value)
    for sub, sub_value in list(inner.items()):
        if not is_input_ref(sub_value):
            continue
        field = model.model_fields.get(sub)
        annotation = field.annotation if field is not None else None
        if get_origin(annotation) in (Union, _types.UnionType):
            # An optional number (``int | None``) is still a number.
            kinds = [a for a in get_args(annotation) if a is not type(None)]
            annotation = kinds[0] if len(kinds) == 1 else None
        if annotation not in (int, float):
            problems.append(
                f"setting '{key}.{sub}' cannot come from a run input — inside '{key}' only a "
                "number can"
            )
            continue
        refs[f"{key}.{sub}"] = dict(sub_value)
        if "default" in sub_value:
            inner[sub] = sub_value["default"]
        elif sub_value["$input"] in (input_defaults or {}):
            inner[sub] = (input_defaults or {})[sub_value["$input"]]
        else:
            inner.pop(sub)
    return inner


def concurrency_cap(value: Any) -> int | None:
    """A run-supplied "how many at once" as a cap: a whole number >= 1 (``2``, ``2.0``, ``"2"``),
    else None. Never a yes/no."""
    if isinstance(value, bool):
        return None
    if isinstance(value, str):
        value = value.strip()
        if not (value.isascii() and value.isdigit()):
            return None
        value = int(value)
    if isinstance(value, float):
        if not value.is_integer():
            return None
        value = int(value)
    if not isinstance(value, int):
        return None
    return value if value >= 1 else None


def _trigger_step_issues(definition: Any, trigger_type: str) -> list[ValidationIssue]:
    """AT MOST ONE TRIGGER STEP, ALWAYS A SOURCE: a workflow is started from outside through one
    Trigger step (``io.trigger``), and nothing wires into it. Definitions without one are untouched."""
    steps = [n for n in definition.nodes if n.spec_type == trigger_type]
    if not steps:
        return []
    issues: list[ValidationIssue] = []
    for extra in steps[1:]:
        issues.append(
            ValidationIssue(
                path=f"nodes[{extra.id}]",
                node_id=extra.id,
                message=(
                    f"A workflow has one Trigger step; '{steps[0].id}' already is it. Remove "
                    f"'{extra.id}' or move its fields onto '{steps[0].id}'."
                ),
            )
        )
    ids = {n.id for n in steps}
    for edge in definition.edges:
        if edge.target in ids:
            issues.append(
                ValidationIssue(
                    path=f"edges[{edge.id}]",
                    node_id=edge.target,
                    message=(
                        f"The Trigger step '{edge.target}' starts the workflow; nothing connects into it. "
                        f"Remove the connection from '{edge.source}'."
                    ),
                )
            )
    return issues
