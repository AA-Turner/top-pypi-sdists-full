"""Convert one workflow step between Run Mandate, Run Typed Agent and Run Workflow.

Arman, 2026-10-27 (generic-only VISION § Mandates inside workflows): *"a simple utility that
can convert a mandate node into either a workflow run node or an agent run node. Or the other
way around."* Pure: definition JSON + the mandate's facts in, the rewritten node and the edges
it touches out. No database, no I/O — the host loads :class:`MandateFacts` and applies the
result through its one patch path (validation + optimistic concurrency).

What moves, mandate → typed agent (``ai.agent.produce``):

* WHO: the mandate's default Holder agent (latest version; ``pin_version`` pins the Holder's
  version row).
* WHAT IT ANSWERS IN: the node's ``data.output_kind``, else the mandate's ``output_kind``. It
  must be a structural kind — Run Typed Agent refuses a format (``json``/``text``).
* THE GOAL: the mandate's goal onto ``config.goal``; ``config.goal_approved`` is true when the
  goal is human-grounded (``H``/``V``), so an approved goal is never asked again.
* THE INPUTS: the mandate's consumption map (one doer variable ← one offered value) becomes the
  step's input mapping — static ``provision_values`` become the variables, an incoming edge
  mapping ``provision_values: P`` becomes ``variable: P.<offered>`` per entry, and each variable
  is exposed as a connection point (``config.exposed_variables``).
* THE OUTPUT: an outgoing edge reading ``structured_output[.k]`` reads ``$FULL_PAYLOAD``/``k``
  (the typed step's payload IS the structured answer); an unmapped outgoing edge gets
  ``structured_output: $FULL_PAYLOAD`` so downstream keeps the key it read.
* Everything else on the node (label, position, ``once``, config, cost attribution
  ``source_feature``) is carried verbatim.

Typed agent → mandate is the exact inverse (``mandate_to_agent`` then ``agent_to_mandate`` is
identity on every meaningful field — the round-trip test pins it). Mandate → workflow
(``subgraph.call``) applies when the Holder is a workflow.

* A JOIN (several offered values into one variable, or one value the binding shapes — heading,
  templates, ``max_items``…) becomes a visible Join Values step (``text.join_values``) in front of
  the typed step, carrying the binding's parts verbatim; it runs the binding's own join code, so
  the variable's text is unchanged. Converting back folds it into the mandate's state again.
* An outgoing edge reading a run fact (``final_text``, ``content``, ``messages``, ``usage``,
  ``conversation_id``, ``metadata``…) keeps its read: the typed step hands those over beside its
  answer (``config.run_envelope``).

Refuses, naming the reason, rather than producing a step that would run differently: a request
firewall (Run Typed Agent has none), a read of something no run has, a runtime-chosen mandate.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Literal

from matrx_ai.graph_nodes.shared import RUN_ENVELOPE_FIELDS

MANDATE_STEP = "ai.mandate.start"
TYPED_AGENT_STEP = "ai.agent.produce"
WORKFLOW_STEP = "subgraph.call"
WHOLE = "$FULL_PAYLOAD"
STATE_FIELD = "provision_values"
ENVELOPE_ANSWER = "structured_output"
#: A text mandate's answer is the envelope's ``final_text``; the typed text step's is ``text``.
ENVELOPE_TEXT = "final_text"
TEXT_ANSWER = "text"

#: The visible step that builds a joined agent variable (registered by the host: aidream
#: ``graph_actions/text/join_values.py``), and the output field it hands the variable in.
JOIN_STEP = "text.join_values"
JOIN_OUTPUT = "value"
#: A binding source key that SHAPES its value — a source carrying one is a join step, never a
#: pass-through (passing it as-is would silently drop the shaping).
_SHAPING_KEYS = ("heading", "template", "item_template", "max_items", "item_fields", "field_max_chars",
                 "keep_keys", "item_where", "prune_empty", "compact", "max_chars", "separator")

ConvertTarget = Literal["agent", "mandate", "workflow"]
TARGET_STEP: dict[str, str] = {"agent": TYPED_AGENT_STEP, "mandate": MANDATE_STEP, "workflow": WORKFLOW_STEP}
_HUMAN_GROUNDINGS = frozenset({"H", "V"})
#: Formats Run Typed Agent cannot bind to. ``text`` is NOT here: the step answers in the
#: registered ``text`` kind (coordinator decision 2026-10-27).
_FORMAT_KINDS = frozenset({"", "json", "markdown", "string"})
#: Run Mandate fields Run Typed Agent does not have — set to anything but the default, the
#: conversion would silently drop a safety rule.
_FIREWALL_DEFAULTS: dict[str, Any] = {
    "must_not_contain": None,
    "must_not_contain_match": "folded",
    "no_tools": False,
    "no_auto_context": False,
}


class StepConversionRefused(ValueError):
    """The step cannot be converted without changing what it does. The message says why."""


@dataclass(frozen=True)
class MandateFacts:
    """What the host read off ``mandate.definition`` for the one mandate involved."""

    mandate_key: str
    holder_type: str
    holder_id: str | None
    holder_version_id: str | None = None
    output_kind: str | None = None
    goal: str = ""
    goal_grounding: str = "A"
    consumption_map: dict[str, Any] = field(default_factory=dict)
    required_output_keys: tuple[str, ...] = ()
    default_config_overrides: dict[str, Any] = field(default_factory=dict)
    #: Live organization/person rebindings of this mandate. A typed step names ONE agent, so they
    #: no longer apply after converting — said in the notes, never silently dropped.
    binding_overrides: int = 0


@dataclass
class Conversion:
    node: dict[str, Any]
    edges: list[dict[str, Any]]
    notes: list[str]
    #: The node before (for the caller's report).
    from_type: str = ""
    #: Steps / connections the conversion adds (a Join Values step) or removes (converting back).
    added_nodes: list[dict[str, Any]] = field(default_factory=list)
    added_edges: list[dict[str, Any]] = field(default_factory=list)
    removed_nodes: list[str] = field(default_factory=list)
    removed_edges: list[str] = field(default_factory=list)


def mandate_cost_stamp(mandate_key: str) -> str:
    """The ``source_feature`` a Run Mandate step's spend files under (``mandate:<key>``)."""
    return f"mandate:{mandate_key}"


def step_type_of(node: dict[str, Any]) -> str:
    data = node.get("data") or {}
    return str(data.get("spec_type") or node.get("type") or "")


def step_inputs(data: dict[str, Any]) -> dict[str, Any]:
    """A step's static inputs, read the way the compiler reads them (matrx_graph.compile): ``data.input``
    (singular, the Studio's canonical key) when it is a dict, else ``data.inputs`` (the plural fallback
    older and programmatic definitions saved). A copy, never the stored dict."""
    raw = data.get("input")
    if not isinstance(raw, dict):
        raw = data.get("inputs")
    return dict(raw) if isinstance(raw, dict) else {}


def one_to_one_map(facts: MandateFacts) -> dict[str, str]:
    """``{doer variable: offered name}`` — refuses a join, a heading, or a non-offered entry."""
    out: dict[str, str] = {}
    for variable, raw in (facts.consumption_map or {}).items():
        entries = raw if isinstance(raw, list) else [raw]
        if len(entries) != 1 or not isinstance(entries[0], dict):
            raise StepConversionRefused(
                f"mandate {facts.mandate_key!r} joins {len(entries)} offered values into the agent's "
                f"variable {variable!r}. A step input takes one value — add a step that builds "
                f"{variable!r}, then convert."
            )
        entry = entries[0]
        if entry.get("heading") or entry.get("mapType", "offered_value") != "offered_value":
            raise StepConversionRefused(
                f"mandate {facts.mandate_key!r} shapes the agent's variable {variable!r} "
                f"(mapType {entry.get('mapType')!r}, heading {entry.get('heading')!r}); a step input "
                "passes a value as it is. Add a step that shapes it, then convert."
            )
        out[str(variable)] = str(entry.get("target") or variable)
    return out


def _is_pass_through(entries: list[Any]) -> bool:
    if len(entries) != 1 or not isinstance(entries[0], dict):
        return False
    entry = entries[0]
    if entry.get("mapType", "offered_value") != "offered_value":
        return False
    return not any(entry.get(k) not in (None, False, "", [], {}) for k in _SHAPING_KEYS)


OPTIONAL_SOURCE = "optional"


def _optional_variables(facts: MandateFacts, variable_of: dict[str, str]) -> dict[str, Any]:
    """``{variable: default or None}`` for pass-through variables whose source may be absent."""
    out: dict[str, Any] = {}
    for var in variable_of:
        raw = (facts.consumption_map or {}).get(var)
        entry = raw[0] if isinstance(raw, list) else raw
        if isinstance(entry, dict) and entry.get("when_absent") in ("skip", "use_default"):
            out[var] = entry.get("default") if entry.get("when_absent") == "use_default" else None
    return out


def split_binding(facts: MandateFacts) -> tuple[dict[str, str], dict[str, list[Any]]]:
    """``({variable: offered}, {variable: [parts]})`` — pass-through variables, and the variables a
    Join Values step must build (several sources, a shaped source, or a fixed value)."""
    direct: dict[str, str] = {}
    joins: dict[str, list[Any]] = {}
    for variable, raw in (facts.consumption_map or {}).items():
        entries = raw if isinstance(raw, list) else [raw]
        if _is_pass_through(entries):
            direct[str(variable)] = str(entries[0].get("target") or variable)
            continue
        for entry in entries:
            if not isinstance(entry, dict) or entry.get("mapType", "offered_value") not in ("offered_value", "direct_value"):
                raise StepConversionRefused(
                    f"mandate {facts.mandate_key!r} feeds the agent's {variable!r} from a "
                    f"{(entry or {}).get('mapType') if isinstance(entry, dict) else type(entry).__name__!r} source "
                    "(asks a person at run time); a workflow step cannot. Give it a run input, then convert."
                )
        joins[str(variable)] = copy.deepcopy(entries)
    return direct, joins


def _join_reads(parts: list[Any]) -> list[str]:
    return [str(p["target"]) for p in parts if isinstance(p, dict) and p.get("mapType", "offered_value") == "offered_value" and p.get("target")]


def _join_node_id(definition: dict[str, Any], node_id: str, variable: str) -> str:
    taken = {n.get("id") for n in definition.get("nodes") or []}
    base = f"{node_id}__build_{variable}"
    out, n = base, 2
    while out in taken:
        out, n = f"{base}_{n}", n + 1
    return out


def _join_steps(
    definition: dict[str, Any], node: dict[str, Any], state: Any, incoming: list[dict], joins: dict[str, list[Any]]
) -> tuple[list[dict], list[dict]]:
    """One Join Values step per joined variable, fed exactly what fed the mandate's state."""
    nodes: list[dict] = []
    edges: list[dict] = []
    pos = node.get("position") or {}
    for index, (variable, parts) in enumerate(joins.items()):
        join_id = _join_node_id(definition, node["id"], variable)
        reads = _join_reads(parts)
        static = {k: v for k, v in (state or {}).items() if k in reads} if isinstance(state, dict) else {}
        join_input: dict[str, Any] = {"parts": parts}
        if static:
            join_input["values"] = static
        join = {"id": join_id, "type": JOIN_STEP,
                "data": {"label": f"Build {variable}", "spec_type": JOIN_STEP, "input": join_input, "config": {}}}
        if isinstance(pos.get("x"), int | float) and isinstance(pos.get("y"), int | float):
            join["position"] = {"x": pos["x"] - 280, "y": pos["y"] + 120 * index}
        nodes.append(join)
        for edge in incoming:
            maps = _mappings(edge)
            if not maps or STATE_FIELD not in maps:
                continue
            edges.append({"id": f"{edge.get('id')}__{join_id}", "source": edge.get("source"), "target": join_id,
                          **({"sourceHandle": edge["sourceHandle"]} if edge.get("sourceHandle") else {}),
                          "data": {"kind": "data", "mappings": {"values": maps[STATE_FIELD]}}})
        edges.append({"id": f"{join_id}__{node['id']}", "source": join_id, "target": node["id"],
                      "data": {"kind": "data", "mappings": {variable: JOIN_OUTPUT}}})
    return nodes, edges


def _node(definition: dict[str, Any], node_id: str) -> dict[str, Any]:
    for node in definition.get("nodes") or []:
        if node.get("id") == node_id:
            return node
    raise StepConversionRefused(f"the workflow has no step {node_id!r}")


def _edges_touching(definition: dict[str, Any], node_id: str) -> tuple[list[dict], list[dict]]:
    incoming = [e for e in definition.get("edges") or [] if e.get("target") == node_id]
    outgoing = [e for e in definition.get("edges") or [] if e.get("source") == node_id]
    return incoming, outgoing


def _mappings(edge: dict[str, Any]) -> dict[str, Any] | None:
    data = edge.get("data") or {}
    maps = data.get("mappings")
    return maps if isinstance(maps, dict) else None


def _set_mappings(edge: dict[str, Any], maps: dict[str, Any] | None) -> None:
    data = edge.setdefault("data", {})
    if maps is None:
        data.pop("mappings", None)
    else:
        data["mappings"] = maps


def _structural(kind: str | None) -> bool:
    return bool(kind) and str(kind).strip().lower() not in _FORMAT_KINDS


# ── mandate → typed agent / workflow ─────────────────────────────────────────


def _rekey_once(data: dict[str, Any], prefix_of: dict[str, str]) -> None:
    """Rewrite a run-once key's input paths when the step's inputs are renamed.

    A Run Mandate step keys on ``provision_values.<offered>``; the typed step has no
    ``provision_values`` — its input is the agent's variable. A key left pointing at a path that
    no longer exists reads nothing, so every run shares one key and reuses the first answer.
    """
    once = data.get("once")
    if not isinstance(once, dict) or not isinstance(once.get("key"), list):
        return
    rebuilt = []
    for path in once["key"]:
        text = str(path)
        for old, new in prefix_of.items():
            if text == old or text.startswith(old + "."):
                text = new + text[len(old):]
                break
        rebuilt.append(text)
    data["once"] = {**once, "key": rebuilt}


def _refuse_firewall(inputs: dict[str, Any], target: str) -> None:
    set_fields = [k for k, default in _FIREWALL_DEFAULTS.items() if inputs.get(k, default) not in (default, [], None)]
    if set_fields:
        raise StepConversionRefused(
            f"this Run Mandate step sets {set_fields} (a request firewall). The {target} step has no "
            "request firewall, so converting would drop a safety rule. Remove it first, or keep the step."
        )


def _state_to_variables(
    inputs: dict[str, Any], incoming: list[dict], variable_of: dict[str, str], joined: set[str] | None = None
) -> tuple[dict[str, Any], list[dict], list[str]]:
    """Static state → step variables; edges feeding ``provision_values`` → per-variable mappings."""
    notes: list[str] = []
    offered_to_var = {offered: var for var, offered in variable_of.items()}
    state = inputs.pop(STATE_FIELD, None)
    if isinstance(state, dict):
        for offered, value in state.items():
            var = offered_to_var.get(str(offered))
            if var is None:
                if str(offered) in (joined or set()):
                    continue  # a Join Values step reads it
                notes.append(f"dropped offered value {offered!r}: the mandate's binding delivers it to no variable")
                continue
            inputs[var] = value
    changed: list[dict] = []
    for edge in incoming:
        maps = _mappings(edge)
        if not maps or STATE_FIELD not in maps:
            continue
        source = maps[STATE_FIELD]
        rebuilt: dict[str, Any] = {}
        for target, src in maps.items():
            if target != STATE_FIELD:
                rebuilt[target] = src
                continue
            for var, offered in variable_of.items():
                rebuilt[var] = offered if source == WHOLE else f"{source}.{offered}"
        edge = copy.deepcopy(edge)
        _set_mappings(edge, rebuilt)
        changed.append(edge)
    return inputs, changed, notes


def _envelope_head(src: str) -> str | None:
    head = src.split(".", 1)[0]
    return head if head in RUN_ENVELOPE_FIELDS else None


def _rewrite_outgoing(
    outgoing: list[dict], answer_field: str, *, typed: bool, text_kind: bool = False,
    kept_envelope: list[str] | None = None,
) -> list[dict]:
    """``structured_output[.k]`` → the new step's answer path. A typed step keeps every other run-fact
    read as it is (collected into ``kept_envelope``: the step hands those over beside its answer);
    anything else refuses."""
    changed: list[dict] = []
    for edge in outgoing:
        if (edge.get("data") or {}).get("kind") == "control":
            continue  # a control connection carries no payload; a mapping on it is refused
        maps = _mappings(edge)
        edge = copy.deepcopy(edge)
        if maps is None:
            if typed:
                _set_mappings(edge, {ENVELOPE_ANSWER: WHOLE})
                changed.append(edge)
            continue
        rebuilt: dict[str, Any] = {}
        for target, src in maps.items():
            src_s = str(src)
            if src_s == ENVELOPE_ANSWER:
                rebuilt[target] = WHOLE if typed else answer_field
            elif typed and text_kind and src_s == ENVELOPE_TEXT:
                rebuilt[target] = TEXT_ANSWER  # a text step's answer is {"__kind": "text", "text": ...}
            elif src_s.startswith(ENVELOPE_ANSWER + "."):
                rest = src_s[len(ENVELOPE_ANSWER) + 1:]
                rebuilt[target] = rest if typed else f"{answer_field}.{rest}"
            elif typed and kept_envelope is not None and _envelope_head(src_s):
                rebuilt[target] = src_s
                if _envelope_head(src_s) not in kept_envelope:
                    kept_envelope.append(_envelope_head(src_s))
            else:
                raise StepConversionRefused(
                    f"the connection {edge.get('id')!r} reads {src_s!r} from this step's run envelope; "
                    + ("no run has that field" if typed else "the converted step hands over only the answer")
                    + f". Point that connection at {ENVELOPE_ANSWER!r} (or a key inside it) first."
                )
        _set_mappings(edge, rebuilt)
        changed.append(edge)
    return changed


def mandate_to_agent(
    definition: dict[str, Any], node_id: str, facts: MandateFacts, *, pin_version: bool = False
) -> Conversion:
    node = copy.deepcopy(_node(definition, node_id))
    if step_type_of(node) != MANDATE_STEP:
        raise StepConversionRefused(f"step {node_id!r} is a {step_type_of(node)!r}, not a Run Mandate step")
    data = node.setdefault("data", {})
    inputs = step_inputs(data)
    if inputs.get("mandate_key") != facts.mandate_key:
        raise StepConversionRefused(
            f"step {node_id!r} names its mandate at run time ({inputs.get('mandate_key')!r}); only a step "
            "that names one fixed mandate can become the agent that holds it."
        )
    if facts.holder_type != "agent" or not facts.holder_id:
        raise StepConversionRefused(
            f"mandate {facts.mandate_key!r} is held by a {facts.holder_type or 'missing'} holder, not an "
            "agent. Convert it to 'workflow' when a workflow holds it."
        )
    kind = data.get("output_kind") or facts.output_kind
    if not _structural(kind):
        raise StepConversionRefused(
            f"mandate {facts.mandate_key!r} answers in {kind!r}, a format, not a structure. Run Typed Agent "
            "binds the agent to a registered kind — declare one on the mandate (or the step) first."
        )
    _refuse_firewall(inputs, "Run Typed Agent")
    variable_of, joins = split_binding(facts)
    incoming, outgoing = _edges_touching(definition, node_id)

    inputs.pop("mandate_key", None)
    for key in _FIREWALL_DEFAULTS:
        inputs.pop(key, None)
    join_nodes, join_edges = _join_steps(definition, node, inputs.get(STATE_FIELD), incoming, joins)
    joined = {r for parts in joins.values() for r in _join_reads(parts)}
    inputs, in_edges, notes = _state_to_variables(inputs, incoming, variable_of, joined)
    # A connection that fed only state the Join Values steps now read carries nothing to this step:
    # it goes (the join step's own connection orders the two). Never left unmapped — an unmapped
    # connection hands its whole payload over as variables.
    dropped_edges = [str(e.get("id")) for e in in_edges if _mappings(e) == {}]
    in_edges = [e for e in in_edges if _mappings(e) != {}]
    for variable in joins:
        notes.append(f"the agent's {variable!r} is built by a Join Values step (the mandate's join, now visible)")
    rekey = {f"{STATE_FIELD}.{offered}": var for var, offered in variable_of.items()}
    for variable, parts in joins.items():
        rekey.update({f"{STATE_FIELD}.{r}": variable for r in _join_reads(parts) if f"{STATE_FIELD}.{r}" not in rekey})
    _rekey_once(data, rekey)
    if pin_version:
        if not facts.holder_version_id:
            raise StepConversionRefused(f"mandate {facts.mandate_key!r} pins no Holder version to pin to")
        inputs["agent_id"], inputs["is_version"] = facts.holder_version_id, True
    else:
        inputs["agent_id"] = facts.holder_id
    if not inputs.get("source_feature"):
        # The stamp Run Mandate itself attributes cost to (a registered pattern); a bare key is
        # refused by the run-time request contract ("unregistered source_feature").
        inputs["source_feature"] = mandate_cost_stamp(facts.mandate_key)
        notes.append(f"cost attributed to source_feature {inputs['source_feature']!r}")

    config = dict(data.get("config") or {})
    exposed = list(config.get("exposed_variables") or [])
    config["exposed_variables"] = exposed + [v for v in [*variable_of, *joins] if v not in exposed]
    # A binding source that may be absent (when_absent skip / use_default) must not turn into a
    # "connected" variable, which refuses a missing value: it is optional on the step, and a
    # use_default default becomes the step's own value.
    optional = _optional_variables(facts, variable_of)
    if optional:
        sources = dict(config.get("variable_sources") or {})
        for var, default in optional.items():
            sources.setdefault(var, OPTIONAL_SOURCE)
            if default is not None and var not in inputs:
                inputs[var] = default
        config["variable_sources"] = sources
    if facts.required_output_keys:
        config["required_output_keys"] = list(facts.required_output_keys)
    if facts.default_config_overrides:
        inputs["config_overrides"] = {**facts.default_config_overrides, **dict(inputs.get("config_overrides") or {})}
        notes.append(f"the mandate's default settings {sorted(facts.default_config_overrides)} now ride on the step")
    if facts.binding_overrides:
        notes.append(
            f"WARNING: mandate {facts.mandate_key!r} has {facts.binding_overrides} organization/person "
            "rebinding(s); this step now always runs the default Holder, so those no longer apply here"
        )
    notes.append("saved-example capture (mandate exemplars) does not apply to a typed step; its grades are on the judge ledger")
    if facts.goal:
        config["goal"] = facts.goal
        config["goal_approved"] = facts.goal_grounding in _HUMAN_GROUNDINGS
        config["goal_grounding"] = facts.goal_grounding if facts.goal_grounding in ("H", "V", "A") else "A"
    else:
        notes.append(f"mandate {facts.mandate_key!r} has no goal; the step will not be graded until one is written")
    data.pop("inputs", None)  # normalised: the converted step carries data.input only
    data.update(input=inputs, config=config, spec_type=TYPED_AGENT_STEP, output_kind=kind)
    node["type"] = TYPED_AGENT_STEP
    kept: list[str] = []
    edges = in_edges + _rewrite_outgoing(
        outgoing, "", typed=True, text_kind=str(kind).strip().lower() == TEXT_ANSWER, kept_envelope=kept
    )
    if kept:
        config["run_envelope"] = list(dict.fromkeys([*(config.get("run_envelope") or []), *kept]))
        notes.append(f"downstream reads the run's {kept}; the step hands them over beside its answer")
    return Conversion(node=node, edges=edges, notes=notes, from_type=MANDATE_STEP,
                      added_nodes=join_nodes, added_edges=join_edges, removed_edges=dropped_edges)



def mandate_to_workflow(definition: dict[str, Any], node_id: str, facts: MandateFacts) -> Conversion:
    node = copy.deepcopy(_node(definition, node_id))
    if step_type_of(node) != MANDATE_STEP:
        raise StepConversionRefused(f"step {node_id!r} is a {step_type_of(node)!r}, not a Run Mandate step")
    if facts.holder_type != "workflow" or not facts.holder_id:
        raise StepConversionRefused(
            f"mandate {facts.mandate_key!r} is held by a {facts.holder_type or 'missing'} holder, not a "
            "workflow. Convert it to 'agent'."
        )
    data = node.setdefault("data", {})
    inputs = step_inputs(data)
    _refuse_firewall(inputs, "Run Workflow")
    variable_of = one_to_one_map(facts)
    incoming, outgoing = _edges_touching(definition, node_id)
    kept = {k: v for k, v in inputs.items() if k not in ("mandate_key", *_FIREWALL_DEFAULTS)}
    kept, in_edges, notes = _state_to_variables(kept, incoming, variable_of)
    # Run Workflow seeds the child from linked fields + `inputs`; run settings of an
    # agent step (source_app, store…) are not its inputs.
    child_inputs = {k: v for k, v in kept.items() if k in variable_of}
    dropped = sorted(set(kept) - set(child_inputs))
    if dropped:
        notes.append(f"agent run settings {dropped} do not apply to a workflow step and were dropped")
    data.pop("inputs", None)
    data.update(input={"inputs": child_inputs} if child_inputs else {}, config={"definition_id": facts.holder_id},
                spec_type=WORKFLOW_STEP)
    node["type"] = WORKFLOW_STEP
    edges = in_edges + _rewrite_outgoing(outgoing, "output", typed=False)
    return Conversion(node=node, edges=edges, notes=notes, from_type=MANDATE_STEP)


# ── typed agent / workflow → mandate ─────────────────────────────────────────


def _variables_to_state(
    inputs: dict[str, Any], incoming: list[dict], variable_of: dict[str, str], mandate_key: str
) -> tuple[dict[str, Any], list[dict]]:
    state: dict[str, Any] = {}
    for var, offered in variable_of.items():
        if var in inputs:
            state[offered] = inputs.pop(var)
    if state:
        inputs[STATE_FIELD] = state
    changed: list[dict] = []
    for edge in incoming:
        maps = _mappings(edge)
        if not maps or not (set(maps) & set(variable_of)):
            continue
        prefixes: set[str] = set()
        rebuilt: dict[str, Any] = {}
        for target, src in maps.items():
            if target not in variable_of:
                rebuilt[target] = src
                continue
            offered, src_s = variable_of[target], str(src)
            if src_s == offered:
                prefixes.add(WHOLE)
            elif src_s.endswith("." + offered):
                prefixes.add(src_s[: -len(offered) - 1])
            else:
                raise StepConversionRefused(
                    f"the connection {edge.get('id')!r} feeds the agent's {target!r} from {src_s!r}, but "
                    f"mandate {mandate_key!r} takes it as offered value {offered!r} inside the state it is "
                    "handed. Build that state in a step before this one, then convert."
                )
        if len(prefixes) != 1:
            raise StepConversionRefused(
                f"the connection {edge.get('id')!r} feeds the agent's variables from several places "
                f"({sorted(prefixes)}); a Run Mandate step takes its state as one value."
            )
        rebuilt[STATE_FIELD] = prefixes.pop()
        edge = copy.deepcopy(edge)
        _set_mappings(edge, rebuilt)
        changed.append(edge)
    return inputs, changed


def _restore_outgoing(
    outgoing: list[dict], answer_field: str, *, typed: bool, text_kind: bool = False, envelope: list[str] | None = None
) -> list[dict]:
    changed: list[dict] = []
    for edge in outgoing:
        if (edge.get("data") or {}).get("kind") == "control":
            continue
        maps = _mappings(edge)
        if maps is None:
            continue
        edge = copy.deepcopy(edge)
        if typed and maps == {ENVELOPE_ANSWER: WHOLE}:
            _set_mappings(edge, None)
            changed.append(edge)
            continue
        rebuilt: dict[str, Any] = {}
        for target, src in maps.items():
            src_s = str(src)
            if typed and text_kind and src_s == TEXT_ANSWER:
                rebuilt[target] = ENVELOPE_TEXT
            elif typed and envelope and src_s.split(".", 1)[0] in envelope:
                rebuilt[target] = src_s  # a run fact the typed step handed over: Run Mandate hands it too
            elif typed:
                rebuilt[target] = ENVELOPE_ANSWER if src_s == WHOLE else f"{ENVELOPE_ANSWER}.{src_s}"
            elif src_s == answer_field:
                rebuilt[target] = ENVELOPE_ANSWER
            elif src_s.startswith(answer_field + "."):
                rebuilt[target] = f"{ENVELOPE_ANSWER}.{src_s[len(answer_field) + 1:]}"
            else:
                raise StepConversionRefused(
                    f"the connection {edge.get('id')!r} reads {src_s!r} from the workflow step; a Run "
                    f"Mandate step hands over its answer as {ENVELOPE_ANSWER!r}. Point it at {answer_field!r}."
                )
        _set_mappings(edge, rebuilt)
        changed.append(edge)
    return changed


def agent_to_mandate(definition: dict[str, Any], node_id: str, facts: MandateFacts) -> Conversion:
    node = copy.deepcopy(_node(definition, node_id))
    from_type = step_type_of(node)
    if from_type not in (TYPED_AGENT_STEP, WORKFLOW_STEP):
        raise StepConversionRefused(
            f"step {node_id!r} is a {from_type!r}; only a Run Typed Agent or Run Workflow step "
            "converts to a Run Mandate step"
        )
    data = node.setdefault("data", {})
    text_kind = str(data.get("output_kind") or facts.output_kind or "").strip().lower() == TEXT_ANSWER
    variable_of, joins = split_binding(facts)
    incoming, outgoing = _edges_touching(definition, node_id)
    notes: list[str] = []
    join_state, join_feeds, join_ids, join_edge_ids = _fold_join_steps(definition, incoming, joins)
    incoming = [e for e in incoming if e.get("id") not in join_edge_ids]
    envelope: list[str] = []
    if from_type == WORKFLOW_STEP:
        raw = step_inputs(data)
        inputs = {**{k: v for k, v in raw.items() if k != "inputs"}, **dict(raw.get("inputs") or {})}
        config: dict[str, Any] = {}
    else:
        inputs = step_inputs(data)
        inputs.pop("agent_id", None)
        inputs.pop("is_version", None)
        config = dict(data.get("config") or {})
        goal = config.pop("goal", None)
        config.pop("goal_approved", None)
        config.pop("goal_grounding", None)
        config.pop("required_output_keys", None)
        envelope = list(config.pop("run_envelope", None) or [])
        overrides = dict(inputs.get("config_overrides") or {})
        for key, value in (facts.default_config_overrides or {}).items():
            if overrides.get(key) == value:
                overrides.pop(key)
        if overrides:
            inputs["config_overrides"] = overrides
        else:
            inputs.pop("config_overrides", None)
        if goal and goal.strip() != (facts.goal or "").strip():
            notes.append(f"the step's own goal differs from mandate {facts.mandate_key!r}'s; the mandate's goal now grades it")
        optional = _optional_variables(facts, variable_of)
        sources = {k: v for k, v in dict(config.pop("variable_sources", None) or {}).items()
                   if not (k in optional and v == OPTIONAL_SOURCE)}
        if sources:
            config["variable_sources"] = sources
        for var, default in optional.items():
            if default is not None and inputs.get(var) == default:
                inputs.pop(var)
        exposed = [v for v in config.get("exposed_variables") or [] if v not in variable_of and v not in joins]
        if exposed:
            config["exposed_variables"] = exposed
        else:
            config.pop("exposed_variables", None)
        if inputs.get("source_feature") in (facts.mandate_key, mandate_cost_stamp(facts.mandate_key)):
            inputs.pop("source_feature")
    unbound = sorted(k for k in inputs if k not in variable_of and k in (facts.consumption_map or {}))
    if unbound:
        raise StepConversionRefused(f"variables {unbound} are not in mandate {facts.mandate_key!r}'s binding")
    inputs, in_edges = _variables_to_state(inputs, incoming, variable_of, facts.mandate_key)
    if join_state:
        inputs[STATE_FIELD] = {**dict(inputs.get(STATE_FIELD) or {}), **join_state}
    added_edges: list[dict] = []
    for original_id, (source, handle, state_from) in join_feeds.items():
        existing = next((e for e in in_edges + incoming if e.get("source") == source), None)
        if existing is not None:
            if (_mappings(existing) or {}).get(STATE_FIELD, state_from) != state_from:
                raise StepConversionRefused(
                    f"the Join Values steps and the connection {existing.get('id')!r} read the state from "
                    "different places; a Run Mandate step takes its state as one value."
                )
            if STATE_FIELD not in (_mappings(existing) or {}):
                existing = copy.deepcopy(existing)
                _set_mappings(existing, {**(_mappings(existing) or {}), STATE_FIELD: state_from})
                in_edges = [e for e in in_edges if e.get("id") != existing.get("id")] + [existing]
            continue
        added_edges.append({"id": original_id, "source": source, "target": node_id,
                            **({"sourceHandle": handle} if handle else {}),
                            "data": {"kind": "data", "mappings": {STATE_FIELD: state_from}}})
    inputs["mandate_key"] = facts.mandate_key
    data.pop("inputs", None)
    data["input"] = inputs
    data["config"] = config
    data["spec_type"] = MANDATE_STEP
    if from_type == TYPED_AGENT_STEP and data.get("output_kind") == facts.output_kind:
        data.pop("output_kind", None)
    node["type"] = MANDATE_STEP
    edges = in_edges + _restore_outgoing(
        outgoing, "output", typed=from_type == TYPED_AGENT_STEP, text_kind=text_kind, envelope=envelope
    )
    return Conversion(node=node, edges=edges, notes=notes, from_type=from_type,
                      added_edges=added_edges, removed_nodes=join_ids)


def _fold_join_steps(
    definition: dict[str, Any], incoming: list[dict], joins: dict[str, list[Any]]
) -> tuple[dict[str, Any], dict[str, tuple[Any, Any, Any]], list[str], set[str]]:
    """The Join Values steps feeding this step's joined variables, folded back into the mandate's
    state: ``(static state, {connection id: (source, handle, state path)}, join step ids, join
    connection ids)``. A joined variable fed any other way refuses."""
    by_id = {n.get("id"): n for n in definition.get("nodes") or []}
    state: dict[str, Any] = {}
    feeds: dict[str, tuple[Any, Any, Any]] = {}
    join_ids: list[str] = []
    edge_ids: set[str] = set()
    for variable in joins:
        edge = next((e for e in incoming if (_mappings(e) or {}).get(variable) == JOIN_OUTPUT
                     and step_type_of(by_id.get(e.get("source")) or {}) == JOIN_STEP), None)
        if edge is None:
            raise StepConversionRefused(
                f"the agent's {variable!r} is a join in the mandate's binding, but no Join Values step "
                "builds it here; a Run Mandate step builds it from its state. Feed it from a Join Values step."
            )
        join = by_id[edge["source"]]
        join_ids.append(str(join["id"]))
        edge_ids.add(str(edge.get("id")))
        state.update(dict(step_inputs(join.get("data") or {}).get("values") or {}))
        for feed in definition.get("edges") or []:
            if feed.get("target") != join["id"]:
                continue
            maps = _mappings(feed) or {}
            if "values" in maps:
                original = str(feed.get("id"))
                suffix = f"__{join['id']}"
                original = original[: -len(suffix)] if original.endswith(suffix) else original
                feeds.setdefault(original, (feed.get("source"), feed.get("sourceHandle"), maps["values"]))
    return state, feeds, join_ids, edge_ids


def convert_step(
    definition: dict[str, Any],
    node_id: str,
    to: ConvertTarget,
    facts: MandateFacts,
    *,
    pin_version: bool = False,
) -> Conversion:
    """THE one entry: convert step ``node_id`` of ``definition`` to ``to`` using ``facts``."""
    if to == "agent":
        return mandate_to_agent(definition, node_id, facts, pin_version=pin_version)
    if to == "workflow":
        return mandate_to_workflow(definition, node_id, facts)
    if to == "mandate":
        return agent_to_mandate(definition, node_id, facts)
    raise StepConversionRefused(f"unknown target {to!r}; choose agent, mandate or workflow")


def as_patch_ops(conversion: Conversion) -> list[dict[str, Any]]:
    """The conversion as ``matrx_graph.patch`` ops: one ``replace_node`` + one ``replace_edge`` each."""
    ops: list[dict[str, Any]] = [{"op": "add_node", "node": node} for node in conversion.added_nodes]
    ops.append({"op": "replace_node", "node": conversion.node})
    ops += [{"op": "replace_edge", "edge": edge} for edge in conversion.edges]
    ops += [{"op": "remove_edge", "edge_id": edge_id} for edge_id in conversion.removed_edges]
    ops += [{"op": "add_edge", "edge": edge} for edge in conversion.added_edges]
    ops += [{"op": "remove_node", "node_id": node_id} for node_id in conversion.removed_nodes]
    return ops


__all__ = [
    "JOIN_STEP",
    "split_binding",
    "MANDATE_STEP",
    "TARGET_STEP",
    "TYPED_AGENT_STEP",
    "WORKFLOW_STEP",
    "Conversion",
    "MandateFacts",
    "StepConversionRefused",
    "step_inputs",
    "agent_to_mandate",
    "as_patch_ops",
    "convert_step",
    "mandate_to_agent",
    "mandate_to_workflow",
    "one_to_one_map",
    "step_type_of",
]
