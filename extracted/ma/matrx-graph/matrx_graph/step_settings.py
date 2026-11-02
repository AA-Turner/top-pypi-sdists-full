"""Built-in step settings: Only when · If skipped · Shape the result · Run once per item.

Three ``data`` keys any step may carry, so the plumbing a person used to build by hand around a
step lives ON the step and the canvas shows one card:

* ``data.when``       — a condition over the step's own inputs (``inputs['review']``). False: the
                        step does not run, exactly like a conditional connection not taken.
* ``data.if_skipped`` — an expression over the step's inputs whose value is the step's result
                        when ``when`` said no (``{'keywords': inputs['items']}``). Downstream
                        steps then run as if the step had produced it.
* ``data.shape``      — an expression over what the step produced (``{'keywords':
                        inputs['answer']}``); downstream connections read the shaped result.
* ``data.for_each``   — ``{}`` or ``{"as": "page", "max_dispatches": 200, …}``: the step runs once
                        per element of the list its connections deliver as ``items``; each run gets
                        the element under ``as`` (default ``item``) and every OTHER input the
                        connections deliver, and the steps after it get the gathered results
                        (``values``, ``count``, ``holes`` … — what a Gather gives). With
                        ``"pairs": true`` the list is also handed to the Gather (``items_from``):
                        ``pairs`` holds each item beside its result and each hole names its
                        item. Replaces the For each → step → Gather trio.

SUGAR OVER THE PRIMITIVES, never a second engine path. ``expand_step_settings`` rewrites the
Definition into the steps people build today — a ``data.transform`` that gathers the inputs, a
conditional connection, a transform that computes the skipped result, a transform that shapes the
output, a For each and a Gather — with ids ``<step>~when`` / ``~skipped`` / ``~shape`` / ``~each`` /
``~gather``. ``compile`` and
``validate_definition`` both expand first, so run history, Retry, Skip and Re-run from work on
the real steps, and the authored Definition (what the canvas draws) keeps one card.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from matrx_graph.types.definition import Definition, EdgeDef, NodeDef

WHEN = "when"
IF_SKIPPED = "if_skipped"
SHAPE = "shape"
FOR_EACH = "for_each"
STEP_SETTING_KEYS: tuple[str, ...] = (WHEN, IF_SKIPPED, SHAPE)
#: Helper parts a step setting writes out (``owner_of`` recognises exactly these).
_PARTS = frozenset({WHEN, IF_SKIPPED, SHAPE, "each", "gather"})
#: What ``data.for_each`` may set: the For Each's own options, plus ``as`` (the item's input name).
_FOR_EACH_KEYS = frozenset({"as", "include_index", "max_dispatches", "payload_template", "pairs"})
#: With ``data.for_each.pairs``: the input the Gather receives the fanned-out list under
#: (``control.gather`` ``items_from``), so each result and each hole carries its item.
SENT_ITEMS = "sent_items"

#: Separates a step's id from the part a helper stands for. Never typed by an author.
HELPER_SEP = "~"

#: What each helper is called on screens that show the expanded graph.
_PART_LABEL = {WHEN: "Only when", IF_SKIPPED: "If skipped", SHAPE: "Shape the result", "each": "For each",
               "gather": "Every result"}

#: Dispatchers send items straight to ``config.target_node_id``, around any gathering step.
_DISPATCHERS = frozenset({"control.map", "control.send", "control.loop", "control.work_queue"})

#: How a step's inputs JOIN: these settings move to the gate, which is now what receives them.
_JOIN_KEYS = ("join_policy", "on_skipped_upstream", "skip_defaults", "arg_merge")

#: Output handles that are the step's single plain output (anything else routes by handle).
_PLAIN_HANDLES = frozenset({"", "out", "output"})


class StepSettingError(ValueError):
    """A step setting that cannot be expanded; ``node_id`` is the authored step."""

    def __init__(self, node_id: str, message: str) -> None:
        super().__init__(message)
        self.node_id = node_id


def helper_id(node_id: str, part: str) -> str:
    return f"{node_id}{HELPER_SEP}{part}"


def owner_of(node_id: str | None) -> str | None:
    """The authored step a helper belongs to; None for an authored step."""
    if not node_id or HELPER_SEP not in node_id:
        return None
    owner, _, part = node_id.rpartition(HELPER_SEP)
    return owner if part in _PARTS else None


def when_gate_owner(node_id: str | None) -> str | None:
    """The authored step an 'Only when' gate (``<step>~when``) belongs to; None otherwise."""
    if not node_id or not node_id.endswith(f"{HELPER_SEP}{WHEN}"):
        return None
    return owner_of(node_id)


def _text(raw: Any) -> str | None:
    return raw.strip() if isinstance(raw, str) and raw.strip() else None


def step_settings(node: NodeDef) -> dict[str, str]:
    """The step's set settings, each a non-empty expression."""
    return {key: text for key in STEP_SETTING_KEYS if (text := _text(node.data.get(key))) is not None}


def for_each_setting(node: NodeDef) -> dict[str, Any] | None:
    """The step's ``data.for_each`` (an object; ``{}`` turns it on with every default), or None."""
    raw = node.data.get(FOR_EACH)
    return dict(raw) if isinstance(raw, dict) else None


def uses_step_settings(definition: Definition) -> bool:
    return any(step_settings(node) or for_each_setting(node) is not None for node in definition.nodes)


def _transform(node_id: str, owner: NodeDef, part: str, expression: str) -> NodeDef:
    name = owner.label or owner.id
    return NodeDef(
        id=node_id,
        type="data",
        position=owner.position,
        data={
            "spec_type": "data.transform",
            "label": f"{_PART_LABEL[part]}: {name}",
            "config": {"expression": expression},
            "step_setting_of": owner.id,
        },
    )


def _edge(edge_id: str, source: str, target: str, data: dict[str, Any]) -> EdgeDef:
    return EdgeDef(id=edge_id, source=source, target=target, data=data)


def expand_step_settings(definition: Definition) -> Definition:
    """The Definition with every step setting written out as real steps and connections.

    Returns ``definition`` itself when no step uses a setting. Raises ``StepSettingError`` for a
    setting that cannot be honored (the message names why, in the author's words)."""
    if not uses_step_settings(definition):
        return definition

    nodes: list[NodeDef] = []
    edges: list[EdgeDef] = [edge.model_copy(deep=True) for edge in definition.edges]
    entry_nodes = list(definition.entry_nodes)
    dispatched = {
        str(node.config.get("target_node_id"))
        for node in definition.nodes
        if node.spec_type in _DISPATCHERS and node.config.get("target_node_id")
    }

    for node in definition.nodes:
        settings = step_settings(node)
        each = for_each_setting(node)
        if each is not None:
            if settings:
                raise StepSettingError(
                    node.id,
                    f"'{node.label or node.id}' runs once per item; put 'Only when' or 'Shape the result' on the "
                    "step after it (they would apply to every item, not to the step).",
                )
            nodes.extend(_expand_for_each(node, each, edges, dispatched, entry_nodes))
            continue
        if not settings:
            nodes.append(node)
            continue
        name = node.label or node.id
        when, if_skipped, shape = settings.get(WHEN), settings.get(IF_SKIPPED), settings.get(SHAPE)
        if if_skipped and not when:
            raise StepSettingError(
                node.id, f"'{name}' says what to use if it is skipped, but has no 'Only when' — it is never skipped."
            )
        if when and node.id in dispatched:
            raise StepSettingError(
                node.id,
                f"'{name}' receives items from a For each, which hands them straight to the step; "
                "put 'Only when' on a step inside the loop instead.",
            )
        if shape and node.id in dispatched:
            raise StepSettingError(
                node.id,
                f"'{name}' receives items from a For each; shape each item's result in the next step instead.",
            )
        outgoing = [e for e in edges if e.source == node.id and e.kind.value not in ("error", "stream")]
        if (shape or if_skipped) and not outgoing:
            raise StepSettingError(
                node.id,
                f"'{name}' ends the workflow, so its result is the workflow's result; to shape or replace "
                "it, add a Transform after it.",
            )
        if (shape or if_skipped) and any((e.sourceHandle or "") not in _PLAIN_HANDLES for e in outgoing):
            raise StepSettingError(
                node.id,
                f"'{name}' sends its result out of a named output, so its result cannot be "
                "shaped or replaced; shape it in the next step instead.",
            )

        owner = node.model_copy(deep=True)
        for key in STEP_SETTING_KEYS:
            owner.data.pop(key, None)
        nodes.append(owner)

        if when:
            gate = helper_id(node.id, WHEN)
            gate_node = _transform(gate, node, WHEN, "inputs")
            # The condition sees what the step sees: the step's own authored inputs
            # (``{"$input": name}`` run inputs, literals) are read the same way compile reads
            # them — ``data.input`` first, else ``data.inputs`` — and handed to the gate too.
            # Before 2026-10-28 they stayed on the step only, so ``inputs['name']`` in 'Only
            # when' raised (or said no) for a run input the step itself received.
            authored = owner.data.get("input") if isinstance(owner.data.get("input"), dict) else owner.data.get("inputs")
            if isinstance(authored, dict) and authored:
                gate_node.data["inputs"] = deepcopy(authored)
            for key in _JOIN_KEYS:
                if key in owner.data:
                    gate_node.data[key] = owner.data.pop(key)
            nodes.append(gate_node)
            for edge in edges:
                if edge.target == node.id and edge.kind.value not in ("error", "stream"):
                    edge.target, edge.targetHandle = gate, None
            edges.append(_edge(f"{gate}>run", gate, node.id, {"kind": "conditional", "condition": when}))
            if node.id in entry_nodes:
                entry_nodes[entry_nodes.index(node.id)] = gate

        result_source = node.id
        if shape:
            result_source = helper_id(node.id, SHAPE)
            nodes.append(_transform(result_source, node, SHAPE, shape))
            for edge in outgoing:
                edge.source, edge.sourceHandle = result_source, None
            edges.append(_edge(f"{result_source}<run", node.id, result_source, {"kind": "data"}))

        if if_skipped:
            skipped = helper_id(node.id, IF_SKIPPED)
            nodes.append(_transform(skipped, node, IF_SKIPPED, if_skipped))
            edges.append(
                _edge(
                    f"{skipped}<gate",
                    helper_id(node.id, WHEN),
                    skipped,
                    {"kind": "conditional", "condition": f"not ({when})"},
                )
            )
            for edge in outgoing:
                copy = edge.model_copy(deep=True)
                copy.id, copy.source, copy.sourceHandle = f"{edge.id}{HELPER_SEP}skipped", skipped, None
                edges.append(copy)

    return definition.model_copy(update={"nodes": nodes, "edges": edges, "entry_nodes": entry_nodes})


def _expand_for_each(
    node: NodeDef, each: dict[str, Any], edges: list[EdgeDef], dispatched: set[str], entry_nodes: list[str]
) -> list[NodeDef]:
    """``X`` with ``data.for_each`` -> ``X~each`` (For each, receives X's connections) -> ``X`` once per
    item -> ``X~gather`` (sends X's connections on). Mutates ``edges`` in place."""
    name = node.label or node.id
    unknown = sorted(set(each) - _FOR_EACH_KEYS)
    if unknown:
        raise StepSettingError(node.id, f"'{name}': 'Run once per item' has no setting {unknown}.")
    if node.id in dispatched:
        raise StepSettingError(node.id, f"'{name}' already receives items from a For each; turn one of them off.")
    if node.id in entry_nodes:
        raise StepSettingError(node.id, f"'{name}' runs once per item of a list a connection brings; it cannot start the run.")
    incoming = [e for e in edges if e.target == node.id]
    if not incoming:
        raise StepSettingError(node.id, f"'{name}' runs once per item, but nothing connects a list into it as 'items'.")
    if any(e.kind.value in ("error", "stream") for e in incoming):
        raise StepSettingError(node.id, f"'{name}' runs once per item; a failure or stream connection cannot feed every item.")
    mapped = {key for e in incoming for key in (e.mappings or {})}
    if "items" not in mapped:
        raise StepSettingError(
            node.id, f"'{name}' runs once per item of 'items', but no connection into it maps a list to 'items'."
        )
    if any(e.mappings is None for e in incoming):
        raise StepSettingError(
            node.id, f"'{name}' runs once per item: name what each connection into it brings (map its fields), "
            "so every item can receive the shared ones."
        )

    pairs = each.get("pairs", False)
    if not isinstance(pairs, bool):
        raise StepSettingError(node.id, f"'{name}': 'Run once per item' pairs is on or off (true / false).")
    list_edges = [e for e in incoming if "items" in (e.mappings or {})]
    if pairs and len(list_edges) != 1:
        raise StepSettingError(
            node.id, f"'{name}': each result can name its item only when ONE connection brings the list as 'items'."
        )

    template = each.get("payload_template")
    if template is None:
        item_as = str(each.get("as") or "item")
        if item_as in mapped - {"items"}:
            raise StepSettingError(
                node.id, f"'{name}': each item arrives as '{item_as}', but a connection also brings an input named "
                f"'{item_as}'; name the item something else."
            )
        template = {item_as: "$item", **{key: f"$in.{key}" for key in sorted(mapped - {"items"})}}
    config: dict[str, Any] = {"target_node_id": node.id, "payload_template": template}
    for key in ("include_index", "max_dispatches"):
        if key in each:
            config[key] = each[key]

    owner = node.model_copy(deep=True)
    owner.data.pop(FOR_EACH, None)
    each_id, gather_id = helper_id(node.id, "each"), helper_id(node.id, "gather")
    each_node = NodeDef(
        id=each_id, type="control", position=node.position,
        data={"spec_type": "control.map", "label": f"For each: {name}", "config": config, "step_setting_of": node.id},
    )
    for key in _JOIN_KEYS:
        if key in owner.data:
            each_node.data[key] = owner.data.pop(key)
    gather_node = NodeDef(
        id=gather_id, type="control", position=node.position,
        data={"spec_type": "control.gather", "label": f"Every result: {name}",
              "config": {"items_from": SENT_ITEMS} if pairs else {}, "step_setting_of": node.id},
    )
    if pairs:
        # The same list the For each fans out, into the Gather beside the results (``items_from``):
        # ``pairs`` holds each item beside its result and every hole names its item.
        (source,) = list_edges
        sent = source.model_copy(deep=True)
        sent.data["mappings"] = {SENT_ITEMS: source.mappings["items"]}  # type: ignore[index]
        sent.data.pop("review", None)  # the authored connection's review mark stays on it alone
        edges.append(sent.model_copy(update={"id": f"{gather_id}<items", "target": gather_id, "targetHandle": None}))
    for edge in incoming:
        edge.target, edge.targetHandle = each_id, None
    for edge in [e for e in edges if e.source == node.id and e.kind.value not in ("error", "stream")]:
        edge.source, edge.sourceHandle = gather_id, None
    edges.append(_edge(f"{gather_id}<run", node.id, gather_id, {"kind": "data"}))
    return [owner, each_node, gather_node]
