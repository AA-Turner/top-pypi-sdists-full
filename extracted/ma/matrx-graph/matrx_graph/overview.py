"""The plain-words OVERVIEW of a workflow — a deterministic collapse of a ``Definition``.

Why: the real graph a workflow runs on carries plumbing (transforms, joins, fan-out, error
branches) that a non-technical person should never have to read. This module turns a
``Definition`` into an Archify workflow-v2 spec a person can follow in one look, with NO AI:

* one LANE per node-type family (inputs, AI steps, tools, saved, results; one lane when a
  definition has only one family);
* COLUMNS from topological depth (v2 columns are ranks 0..5, so deeper graphs are compressed);
* pass-through nodes (transforms, joins, fan-out, branches) drop and their neighbours reconnect;
* PARALLEL SIBLINGS that take the same inputs and feed the same targets fold into ONE node
  labelled with a count ("8 AI steps") whose real node ids are kept in the returned ``node_map``;
* ERROR edges fold into one "If a step fails" card item per handling step, never drawn;
* labels come from the node titles, in plain words.
* a LONG flow (``STAGE_MIN_STEPS`` steps, deeper than six columns) is told as STAGES instead: cut at
  its pinch points (where the fewest connections cross), one box per stage named by its AI step (never
  its gate), wrapped into rows of six ("Part 1", "Part 2") read left to right, loop tagged once.

The spec has no place for the real node ids (Archify's node schema is closed), so
``collapse_definition_detailed`` also returns ``node_map`` — ``{overview node id: [real node ids]}``
— which the host stores in the overview row's metadata and uses to open the real nodes.

``definition_structure_hash`` is the staleness key: sha256 over the nodes (id, type) and the edges
(source, target, kind) only — never positions, labels, config or any other cosmetic field — so
dragging a node does not invalidate an overview and adding a connection does. Because the collapse
also reads labels, lanes and the title, ``definition_collapse_hash`` covers those inputs; a host
re-collapses when EITHER hash differs.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from matrx_graph.types.definition import Definition, NodeDef
from matrx_graph.types.primitives import EdgeKind

#: Bumped when the collapse rules change, so a stored overview from older rules is re-collapsed.
COLLAPSE_VERSION = 3

#: How many primary nodes the overview aims for.
TARGET_PRIMARY_NODES = 12
#: Archify v2 columns are logical ranks 0..5.
MAX_COL = 5
#: A flow deeper than one row of columns, with at least this many steps, is told as STAGES: cut at
#: its pinch points (where the fewest connections cross), one box per stage, wrapped into rows
#: ("Part 1", "Part 2") instead of squeezing the whole length into six columns.
STAGE_MIN_STEPS = 30

# --------------------------------------------------------------------------- families

LANE_ORDER = ("inputs", "ai", "tools", "saved", "results")
LANE_LABELS = {
    "inputs": "What you give it",
    "ai": "AI steps",
    "tools": "Tools and lookups",
    "saved": "What gets saved",
    "results": "What you get back",
}
#: Archify component type per lane (only its color; the legend relabels it).
LANE_NODE_TYPE = {
    "inputs": "external",
    "ai": "backend",
    "tools": "cloud",
    "saved": "database",
    "results": "frontend",
}
LANE_NOUN = {
    "inputs": "questions",
    "ai": "AI steps",
    "tools": "tool steps",
    "saved": "saves",
    "results": "results",
}
LANE_SUBLABEL = {
    "inputs": "you provide",
    "ai": "AI writes it",
    "tools": "looks things up",
    "saved": "kept for later",
    "results": "shown to you",
}

#: Spec types that only reshape data between real steps. They drop out of the picture.
_PASS_THROUGH_EXACT = frozenset(
    {
        "data.transform",
        "data.map_template",
        "data.parse_json",
        "data.stringify_json",
        "data.assert",
        "ai.util.parse_llm_json",
        "log.record",
        "settings.read",
        "pipe.step",
    }
)
_PASS_THROUGH_PREFIXES = ("text.", "flow.", "control.gather", "control.map", "control.join", "control.merge", "control.loop", "control.branch")
_PERSIST_WORDS = re.compile(r"(persist|save|upsert|commit|land|store|write|insert|apply)", re.I)
_INPUT_SPECS = ("io.user_input", "control.human_input", "human.")
_OUTPUT_PREFIXES = ("output.", "io.output")


def _is_pass_through(node: NodeDef) -> bool:
    spec = node.spec_type
    return spec in _PASS_THROUGH_EXACT or spec.startswith(_PASS_THROUGH_PREFIXES)


def node_family(node: NodeDef, categories: dict[str, str] | None = None) -> str:
    """The lane a node belongs to, from the node-type registry's category (``categories`` maps
    spec type -> category, from the registry) with the node's own stamped ``data.category`` and
    its spec-type name as the fallbacks. One of ``LANE_ORDER``."""
    spec = node.spec_type
    category = (categories or {}).get(spec) or node.data.get("category") or ""
    if spec.startswith(_INPUT_SPECS):
        return "inputs"
    if spec.startswith(_OUTPUT_PREFIXES) or spec.rsplit(".", 1)[-1] in ("deliver", "to_frontend"):
        return "results"
    if spec.startswith(("ai.agent", "ai.mandate", "ai.llm", "ai.conversation")) or category in ("agent", "llm"):
        return "ai"
    if _PERSIST_WORDS.search(spec.rsplit(".", 1)[-1]) or spec.startswith("data.record."):
        return "saved"
    return "tools"


# --------------------------------------------------------------------------- the hash


def definition_structure_hash(definition: Definition) -> str:
    """sha256 over the definition's STRUCTURE: nodes as (id, type) and edges as (source, target,
    kind). Positions, labels, config, viewport and every other cosmetic field are ignored, so
    moving a node never changes it and adding a connection or changing a step's type always does.
    ``type`` is the effective spec type (``data.spec_type`` when present)."""
    nodes = sorted((n.id, n.spec_type) for n in definition.nodes)
    edges = sorted((e.source, e.target, e.kind.value) for e in definition.edges)
    payload = json.dumps({"nodes": nodes, "edges": edges}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def definition_collapse_hash(
    definition: Definition, *, title: str = "Workflow overview", categories: dict[str, str] | None = None
) -> str:
    """sha256 over everything ``collapse_definition_detailed`` READS, so a stored overview is re-collapsed
    whenever its picture could differ. Derived from the collapse code: per node, in definition order (the
    order breaks ties), the id, the spec type, the plain-words label (``_label_of``: label, else id, else
    spec tail) and the lane (``node_family``: registry category, ``data.category``, spec name); per edge
    (sorted) source, target and kind; and the workflow title. Positions, config and every field the
    collapse never reads are ignored, so dragging a node leaves it unchanged while renaming a step changes
    it. Complements ``definition_structure_hash`` (which means STRUCTURE only); bump ``COLLAPSE_VERSION``
    when the collapse starts reading something new."""
    nodes = [[n.id, n.spec_type, _label_of(n), node_family(n, categories)] for n in definition.nodes]
    edges = sorted((e.source, e.target, e.kind.value) for e in definition.edges)
    payload = json.dumps({"title": title, "nodes": nodes, "edges": edges}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- labels

_STOPWORDS = frozenset({"the", "and", "for", "from", "with", "your", "step", "steps", "agent", "source", "run", "make", "new"})


def _plain(text: str) -> str:
    text = re.sub(r"[_\-]+", " ", text).strip()
    text = re.sub(r"\s+", " ", text)
    return text[:1].upper() + text[1:] if text else text


def _label_of(node: NodeDef) -> str:
    raw = node.label
    if raw and raw.strip():
        label = _plain(raw)
    else:
        label = _plain(node.id) if not re.fullmatch(r"[0-9a-f-]{8,}", node.id) else _plain(node.spec_type.rsplit(".", 1)[-1])
    if len(label) > 26:
        cut = label[:26].rsplit(" ", 1)[0]
        label = (cut or label[:26]).rstrip(" ,:;-") + "…"
    return label


def _short(label: str, limit: int = 18) -> str:
    base = re.sub(r"\s*\([^)]*\)", "", label).strip()
    return base if len(base) <= limit else base[: limit - 1].rstrip() + "…"


def _safe_id(raw: str, taken: set[str]) -> str:
    base = re.sub(r"[^a-zA-Z0-9_-]", "_", raw)
    if not base or not base[0].isalpha():
        base = "n_" + base
    candidate, i = base, 2
    while candidate in taken:
        candidate = f"{base}_{i}"
        i += 1
    taken.add(candidate)
    return candidate


# --------------------------------------------------------------------------- the collapse


@dataclass
class _Item:
    """One thing drawn in the overview: a real node, or a fold of several."""

    key: str
    lane: str
    label: str
    members: list[str]
    sublabel: str = ""
    tag: str = ""
    names: list[str] = field(default_factory=list)


@dataclass
class CollapseResult:
    """The spec plus what the spec has no room for."""

    spec: dict[str, Any]
    #: overview node id -> the real node ids it stands for (a fold keeps all of them).
    node_map: dict[str, list[str]]
    #: real node ids that dropped out of the picture (pass-through and failure-only steps).
    hidden: list[str]
    structure_hash: str
    collapse_version: int = COLLAPSE_VERSION
    #: ``definition_collapse_hash`` of the inputs this picture was built from.
    collapse_hash: str = ""


def collapse_definition(
    definition: Definition,
    *,
    title: str = "Workflow overview",
    categories: dict[str, str] | None = None,
) -> dict[str, Any]:
    """The Archify workflow-v2 spec for ``definition`` (deterministic, no AI). See the module doc;
    ``collapse_definition_detailed`` also returns the overview-to-real node map."""
    return collapse_definition_detailed(definition, title=title, categories=categories).spec


def collapse_definition_detailed(
    definition: Definition,
    *,
    title: str = "Workflow overview",
    categories: dict[str, str] | None = None,
) -> CollapseResult:
    nodes = {n.id: n for n in definition.nodes}
    order = {n.id: i for i, n in enumerate(definition.nodes)}
    structure_hash = definition_structure_hash(definition)

    # 1. Error edges leave the picture; remember who handles failure.
    error_targets: dict[str, list[str]] = defaultdict(list)
    flow: dict[str, set[str]] = {nid: set() for nid in nodes}
    for e in definition.edges:
        if e.source not in nodes or e.target not in nodes or e.source == e.target:
            continue
        if e.kind == EdgeKind.ERROR:
            error_targets[e.target].append(e.source)
        else:
            flow[e.source].add(e.target)

    # 2. Steps reachable only through failure edges are failure handling: card, not boxes.
    has_in = {t for targets in flow.values() for t in targets}
    roots = [nid for nid in nodes if nid not in has_in and nid not in error_targets]
    if not roots:
        roots = [nid for nid in nodes if nid not in error_targets] or list(nodes)
    reachable: set[str] = set()
    stack = list(roots)
    while stack:
        cur = stack.pop()
        if cur in reachable:
            continue
        reachable.add(cur)
        stack.extend(flow[cur] - reachable)
    failure_only = {nid for nid in nodes if nid not in reachable}

    # 3. Pass-through nodes drop; their neighbours reconnect. Never drop everything.
    drop = {nid for nid, n in nodes.items() if _is_pass_through(n)} | failure_only
    if len(drop) >= len(nodes):
        drop = set(failure_only) if len(failure_only) < len(nodes) else set()
    succ = {nid: set(flow[nid]) - failure_only for nid in nodes if nid not in failure_only}
    for nid in sorted(drop - failure_only, key=lambda x: order[x]):
        preds = {p for p, ts in succ.items() if nid in ts}
        outs = succ.pop(nid, set())
        for p in preds:
            succ[p].discard(nid)
            succ[p] |= {o for o in outs if o != p}
    kept = [nid for nid in nodes if nid not in drop]
    kept_set = set(kept)
    succ = {nid: {t for t in ts if t in kept_set and t != nid} for nid, ts in succ.items() if nid in kept_set}

    # 4. Break loops (a step that feeds an earlier one is a repeat, tagged, not drawn).
    repeats: set[str] = set()
    state: dict[str, int] = {}

    def _dfs(start: str) -> None:
        work = [(start, iter(sorted(succ[start], key=lambda x: order[x])))]
        state[start] = 1
        while work:
            node, it = work[-1]
            for nxt in it:
                if state.get(nxt) == 1:
                    succ[node].discard(nxt)
                    repeats.add(nxt)
                elif nxt not in state:
                    state[nxt] = 1
                    work.append((nxt, iter(sorted(succ[nxt], key=lambda x: order[x]))))
                    break
            else:
                state[node] = 2
                work.pop()

    for nid in sorted(kept, key=lambda x: order[x]):
        if nid not in state:
            _dfs(nid)

    _reduce_transitive(succ)

    # 5. Items: one per kept node, then fold parallel siblings.
    items: dict[str, _Item] = {}
    for nid in kept:
        n = nodes[nid]
        lane = node_family(n, categories)
        items[nid] = _Item(
            key=nid, lane=lane, label=_label_of(n), members=[nid], sublabel=LANE_SUBLABEL[lane],
            tag="repeats" if nid in repeats else "",
        )
    edges = {k: set(v) for k, v in succ.items()}
    stages = _fold_stages(items, edges, order) if len(items) >= STAGE_MIN_STEPS else None
    if stages is not None:
        return _stage_result(
            stages, items, edges, title=title, error_targets=error_targets, drop=drop, nodes=nodes,
            order=order, structure_hash=structure_hash,
            collapse_hash=definition_collapse_hash(definition, title=title, categories=categories),
        )
    _fold_siblings(items, edges, min_size=3)
    for step in (
        lambda: _fold_siblings(items, edges, min_size=2),
        lambda: _fold_chains(items, edges),
        lambda: _fold_siblings(items, edges, min_size=2, by="preds"),
        lambda: _fold_siblings(items, edges, min_size=2, by="succs"),
        lambda: _fold_chains(items, edges),
        lambda: _fold_siblings(items, edges, min_size=2),
    ):
        if len(items) <= TARGET_PRIMARY_NODES:
            break
        step()
        _reduce_transitive(edges)

    _reduce_transitive(edges)

    # 6. Lanes, columns, offsets.
    used = _lane_order(items, edges)
    if len(used) == 1:  # one family: one lane, named for the work, not the family
        lane_labels = {used[0]: "Steps"}
    else:
        lane_labels = {lane: LANE_LABELS[lane] for lane in used}
    depth = _depths(items, edges)
    top = max(depth.values(), default=0)
    col = {k: (d if top <= MAX_COL else round(d * MAX_COL / top)) for k, d in depth.items()}

    taken: set[str] = set()
    ids = {k: _safe_id(k if len(items[k].members) == 1 else f"group_{k}", taken) for k in sorted(items, key=lambda x: order.get(x, 0))}
    spec_nodes: list[dict[str, Any]] = []
    stacks: dict[tuple[str, int], list[str]] = defaultdict(list)
    for k in sorted(items, key=lambda x: (col[x], order.get(x, 0))):
        stacks[(items[k].lane, col[k])].append(k)
    stacks = _order_stacks(stacks, items, edges, used)
    offsets: dict[str, int] = {}
    for keys in stacks.values():
        for idx, k in enumerate(keys):
            offsets[k] = int(round((idx - (len(keys) - 1) / 2) * 96)) if len(keys) > 1 else 0
    for k in sorted(items, key=lambda x: (used.index(items[x].lane), col[x], order.get(x, 0))):
        it = items[k]
        node: dict[str, Any] = {
            "id": ids[k], "lane": it.lane, "col": col[k], "type": LANE_NODE_TYPE[it.lane], "label": it.label,
            "sublabel": it.sublabel,
        }
        if it.tag:
            node["tag"] = it.tag
        if offsets[k]:
            node["yOffset"] = offsets[k]
        arrivals = sum(1 for ts in edges.values() if k in ts)
        busy = max(arrivals, len(edges.get(k, ())))
        if busy >= 2:  # taller, so the arrows of several arrivals or departures land apart
            node["height"] = 52 + 16 * min(busy - 1, 4)
        spec_nodes.append(node)
    spec_edges = [
        {"id": f"e{i}", "from": ids[a], "to": ids[b]}
        for i, (a, b) in enumerate(
            sorted(((a, b) for a, ts in edges.items() for b in ts), key=lambda p: (col[p[0]], col[p[1]], order.get(p[0], 0), order.get(p[1], 0))),
            start=1,
        )
    ]

    # 7. Cards: failure handling and what was hidden — said, never silent.
    hidden = sorted(drop, key=lambda x: order[x])
    cards = _cards(error_targets, hidden, nodes, order)
    legend = {LANE_NODE_TYPE[lane]: {"label": LANE_LABELS[lane]} for lane in used}
    spec = _spec(title, legend, [{"id": lane, "label": lane_labels[lane]} for lane in used], spec_nodes, spec_edges, cards)
    node_map = {ids[k]: list(items[k].members) for k in items}
    return CollapseResult(
        spec=spec, node_map=node_map, hidden=hidden, structure_hash=structure_hash,
        collapse_hash=definition_collapse_hash(definition, title=title, categories=categories),
    )


def _cards(
    error_targets: dict[str, list[str]], hidden: list[str], nodes: dict[str, NodeDef], order: dict[str, int]
) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    if error_targets:
        # Two steps can share a label ("The judge did not answer"); say each one once.
        fail_items = list(dict.fromkeys(f"Handled by: {_label_of(nodes[t])}" for t in sorted(error_targets, key=lambda x: order[x])))
        cards.append({"dot": "rose", "title": "If a step fails", "items": fail_items})
    if hidden:
        cards.append(
            {"dot": "slate", "title": "Behind the scenes", "items": [f"{len(hidden)} behind-the-scenes steps are hidden in this overview"]}
        )
    return cards


def _spec(
    title: str,
    legend: dict[str, Any],
    lanes: list[dict[str, str]],
    spec_nodes: list[dict[str, Any]],
    spec_edges: list[dict[str, str]],
    cards: list[dict[str, Any]],
) -> dict[str, Any]:
    spec: dict[str, Any] = {
        "schema_version": 2,
        "diagram_type": "workflow",
        "meta": {
            "title": title,
            "output": "workflow-overview.html",
            "animation": "trace",
            "visual_preset": "signal-flow",
            "quality_profile": "showcase",
            "legend": {"mode": "all", "entries": legend},
        },
        "lanes": lanes,
        "nodes": spec_nodes,
        "edges": spec_edges,
    }
    if cards:
        spec["cards"] = cards
    return spec


# --------------------------------------------------------------------------- stages

_GATE_WORDS = re.compile(r"\bgate\b", re.I)
_HEADLINE_LANES = ("ai", "inputs", "results", "saved", "tools")


def _fold_stages(items: dict[str, _Item], edges: dict[str, set[str]], order: dict[str, int]) -> list[str] | None:
    """Cut a long flow into stages at its pinch points and fold each into one item; the stage keys in
    flow order, or None when the flow is short enough to draw step by step."""
    # Longest-path rank, iteratively (Kahn) — a recursive walk overflows on a few hundred chained steps.
    preds = _preds(edges)
    waiting = {k: len([p for p in preds.get(k, ()) if p in items]) for k in items}
    rank = {k: 0 for k in items}
    ready = sorted((k for k, n in waiting.items() if n == 0), key=lambda x: order.get(x, 0))
    while ready:
        k = ready.pop()
        for t in edges.get(k, ()):
            if t not in waiting:
                continue
            rank[t] = max(rank[t], rank[k] + 1)
            waiting[t] -= 1
            if waiting[t] == 0:
                ready.append(t)
    layers = max(rank.values(), default=0) + 1
    if layers <= MAX_COL + 1:
        return None
    crossing = [0] * (layers - 1)
    for a, ts in edges.items():
        for b in ts:
            for c in range(rank[a], rank[b]):
                crossing[c] += 1
    want = min(TARGET_PRIMARY_NODES, layers)
    span = layers / want
    reach = max(1, int(span * 0.35))
    cuts: list[int] = []
    for j in range(1, want):
        target = round(j * span) - 1
        window = [c for c in range(target - reach, target + reach + 1) if 0 <= c < layers - 1 and (not cuts or c > cuts[-1])]
        if window:
            cuts.append(min(window, key=lambda c: (crossing[c], abs(c - target))))
    bounds = [-1, *cuts, layers - 1]
    groups = [
        sorted((k for k in items if bounds[i] < rank[k] <= bounds[i + 1]), key=lambda x: order.get(x, 0))
        for i in range(len(bounds) - 1)
    ]
    stages: list[str] = []
    for i, keys in enumerate(groups):
        if not keys:
            continue
        headline = _headline(items, keys)
        if len(keys) == 1:
            stages.append(keys[0])
            continue
        key = f"stage_{i + 1}"
        count = sum(len(items[k].members) for k in keys)
        lane = items[headline].lane
        label = items[headline].label
        _merge(items, edges, keys, key, label)
        items[key].lane = lane
        items[key].sublabel = f"{count} steps"
        stages.append(key)
    return stages


def _headline(items: dict[str, _Item], keys: list[str]) -> str:
    """The step that names a stage: its first AI step, else its first question for you, and so on —
    never plumbing named like a gate ("Gate contract", "Jv in tools")."""
    named = [k for k in keys if not _GATE_WORDS.search(items[k].label)] or keys
    for lane in _HEADLINE_LANES:
        for k in named:
            if items[k].lane == lane:
                return k
    return named[0]


def _stage_result(
    stages: list[str],
    items: dict[str, _Item],
    edges: dict[str, set[str]],
    *,
    title: str,
    error_targets: dict[str, list[str]],
    drop: set[str],
    nodes: dict[str, NodeDef],
    order: dict[str, int],
    structure_hash: str,
    collapse_hash: str,
) -> CollapseResult:
    """Stages read like text: left to right in a row of six, then on to the next row ("Part 2")."""
    per_row = MAX_COL + 1
    rows = (len(stages) + per_row - 1) // per_row
    taken: set[str] = set()
    ids = {k: _safe_id(k, taken) for k in stages}
    lanes = [{"id": f"part_{r + 1}", "label": f"Part {r + 1}" if rows > 1 else "Steps"} for r in range(rows)]
    # A loop back re-runs everything after the step it returns to, so the merge tags nearly every stage;
    # the tag belongs on the stage the loop returns to, once.
    looped = next((k for k in stages if items[k].tag), None)
    spec_nodes: list[dict[str, Any]] = []
    for i, k in enumerate(stages):
        it = items[k]
        it.tag = it.tag if k == looped else ""
        node: dict[str, Any] = {
            "id": ids[k], "lane": f"part_{i // per_row + 1}", "col": i % per_row, "type": LANE_NODE_TYPE[it.lane],
            "label": it.label, "sublabel": it.sublabel,
        }
        if it.tag:
            node["tag"] = it.tag
        spec_nodes.append(node)
    position = {k: i for i, k in enumerate(stages)}
    pairs = sorted(
        {(a, b) for a, ts in edges.items() for b in ts if a in position and b in position and position[b] > position[a]},
        key=lambda p: (position[p[0]], position[p[1]]),
    )
    # Next stage only: a stage that also feeds one further on is shown by the chain itself — unless a
    # skip is the only way into a stage, which is then drawn so no stage floats unconnected.
    chain = [(a, b) for a, b in pairs if position[b] == position[a] + 1]
    entered = {b for _a, b in chain}
    skips = [next(p for p in pairs if p[1] == b) for b in dict.fromkeys(b for _a, b in pairs) if b not in entered]
    pairs = sorted(chain + skips, key=lambda p: (position[p[0]], position[p[1]]))
    spec_edges = [{"id": f"e{i}", "from": ids[a], "to": ids[b]} for i, (a, b) in enumerate(pairs, start=1)]
    hidden = sorted(drop, key=lambda x: order[x])
    used = [lane for lane in LANE_ORDER if any(items[k].lane == lane for k in stages)]
    legend = {LANE_NODE_TYPE[lane]: {"label": LANE_LABELS[lane]} for lane in used}
    spec = _spec(title, legend, lanes, spec_nodes, spec_edges, _cards(error_targets, hidden, nodes, order))
    return CollapseResult(
        spec=spec, node_map={ids[k]: list(items[k].members) for k in stages}, hidden=hidden,
        structure_hash=structure_hash, collapse_hash=collapse_hash,
    )


# --------------------------------------------------------------------------- folding


def _preds(edges: dict[str, set[str]]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {k: set() for k in edges}
    for a, ts in edges.items():
        for t in ts:
            out.setdefault(t, set()).add(a)
    return out


def _merge(items: dict[str, _Item], edges: dict[str, set[str]], keys: list[str], new_key: str, label: str) -> None:
    members: list[str] = []
    names: list[str] = []
    for k in keys:
        members.extend(items[k].members)
        names.extend(items[k].names or [items[k].label])
    lane = items[keys[0]].lane
    tag = "repeats" if any(items[k].tag for k in keys) else ""
    group = set(keys)
    outs = set().union(*(edges.get(k, set()) for k in keys)) - group
    ins = {a for a, ts in edges.items() if a not in group and ts & group}
    for k in keys:
        items.pop(k)
        edges.pop(k, None)
    for a in ins:
        edges[a] -= group
        edges[a].add(new_key)
    items[new_key] = _Item(
        key=new_key, lane=lane, label=label, members=members, tag=tag, names=names,
        sublabel=_names_sublabel(names),
    )
    edges[new_key] = outs - {new_key}


def _names_sublabel(names: list[str]) -> str:
    """The first member names that fit on one line of a node ("Flashcards, Quiz…")."""
    out = ""
    for i, name in enumerate(names):
        piece = _short(name, 12)
        candidate = f"{out}, {piece}" if out else piece
        if len(candidate) > 24:
            return out.rstrip("…") + "…" if out else piece
        out = candidate
    return out


def _group_label(count: int, lane: str, labels: list[str]) -> str:
    words = [set(w.lower() for w in re.findall(r"[A-Za-z]{4,}", re.sub(r"\([^)]*\)", "", lbl))) - _STOPWORDS for lbl in labels]
    common = set.intersection(*words) if words else set()
    noun = sorted(common)[0] if common else ""
    return f"{count} {noun} steps" if noun else f"{count} {LANE_NOUN[lane]}"


def _fold_siblings(items: dict[str, _Item], edges: dict[str, set[str]], *, min_size: int, by: str = "both") -> None:
    changed = True
    while changed:
        changed = False
        preds = _preds(edges)
        buckets: dict[tuple[str, frozenset[str], frozenset[str]], list[str]] = defaultdict(list)
        for k, it in items.items():
            p = frozenset(preds.get(k, set())) if by in ("both", "preds") else frozenset()
            q = frozenset(edges.get(k, set())) if by in ("both", "succs") else frozenset()
            buckets[(it.lane, p, q)].append(k)
        for (lane, _p, _s), keys in sorted(buckets.items(), key=lambda kv: min(kv[1])):
            if len(keys) >= min_size and not _would_cycle(edges, keys):
                labels = [n for k in keys for n in (items[k].names or [items[k].label])]
                total = sum(len(items[k].members) for k in keys)
                _merge(items, edges, keys, f"fold_{keys[0]}", _group_label(total, lane, labels))
                changed = True
                break


def _fold_chains(items: dict[str, _Item], edges: dict[str, set[str]]) -> None:
    """Merge straight runs (one way in, one way out, same lane) so a long line becomes one step."""
    changed = True
    while changed and len(items) > TARGET_PRIMARY_NODES:
        changed = False
        preds = _preds(edges)
        for k in list(items):
            outs = edges.get(k, set())
            if len(outs) != 1:
                continue
            (nxt,) = tuple(outs)
            if nxt not in items or len(preds.get(nxt, set())) != 1 or items[nxt].lane != items[k].lane:
                continue
            labels = [n for x in (k, nxt) for n in (items[x].names or [items[x].label])]
            total = len(items[k].members) + len(items[nxt].members)
            _merge(items, edges, [k, nxt], f"fold_{k}", _group_label(total, items[k].lane, labels))
            changed = True
            break


def _depths(items: dict[str, _Item], edges: dict[str, set[str]]) -> dict[str, int]:
    preds = _preds(edges)
    depth: dict[str, int] = {}

    def of(k: str, seen: frozenset[str] = frozenset()) -> int:
        if k in depth:
            return depth[k]
        ps = [p for p in preds.get(k, set()) if p in items and p not in seen]
        depth[k] = 0 if not ps else 1 + max(of(p, seen | {k}) for p in ps)
        return depth[k]

    for k in sorted(items):
        of(k)
    # Pull a starting step, or a single-file step feeding its own lane, as late as its successor allows, so an arrow does not skip over columns
    # when the step it feeds sits further right than its own depth needs.
    for k in sorted(items, key=lambda x: -depth[x]):
        outs = [depth[t] for t in edges.get(k, set()) if t in depth]
        (only,) = (next(iter(edges.get(k, ()))),) if len(edges.get(k, ())) == 1 else (None,)
        same_lane = only is not None and items[only].lane == items[k].lane
        if outs and (not preds.get(k) or (len(preds.get(k, ())) == 1 and same_lane)):
            depth[k] = max(depth[k], min(outs) - 1)
    return depth


def _reduce_transitive(edges: dict[str, set[str]]) -> None:
    """Drop a->c when another path a->..->c exists: bridging pass-through steps otherwise adds a
    shortcut for every skipped step, and the picture becomes a hairball of parallel arrows."""
    reach: dict[str, set[str]] = {}

    def reachable(k: str) -> set[str]:
        if k not in reach:
            reach[k] = set()
            out: set[str] = set()
            for t in edges.get(k, set()):
                out.add(t)
                out |= reachable(t)
            reach[k] = out
        return reach[k]

    for a in list(edges):
        for c in list(edges[a]):
            if any(c in reachable(b) for b in edges[a] if b != c):
                edges[a].discard(c)


def _would_cycle(edges: dict[str, set[str]], keys: list[str]) -> bool:
    """True when merging ``keys`` would make a cycle (one of them reaches another)."""
    group = set(keys)
    for k in keys:
        seen: set[str] = set()
        stack = [t for t in edges.get(k, set()) if t not in group]
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            if cur in group:
                return True
            stack.extend(edges.get(cur, set()))
    return False


def _order_stacks(
    stacks: dict[tuple[str, int], list[str]],
    items: dict[str, _Item],
    edges: dict[str, set[str]],
    lanes: list[str],
) -> dict[tuple[str, int], list[str]]:
    """Order nodes that share a lane and column by the average height of their neighbours
    (barycentre sweeps), so the arrows between them cross as little as the layout allows."""
    preds = _preds(edges)
    pos: dict[str, float] = {}
    for (lane, _c), keys in stacks.items():
        for i, k in enumerate(keys):
            pos[k] = lanes.index(lane) * 1000.0 + i * 10
    for sweep in range(6):
        forward = sweep % 2 == 0
        for (lane, _c), keys in sorted(stacks.items(), key=lambda kv: kv[0][1] if forward else -kv[0][1]):
            if len(keys) < 2:
                continue
            neigh = preds if forward else edges

            def bary(k: str) -> float:
                ns = [pos[n] for n in neigh.get(k, set()) if n in pos]
                return sum(ns) / len(ns) if ns else pos[k]

            keys.sort(key=lambda k: (bary(k), k))
            for i, k in enumerate(keys):
                pos[k] = lanes.index(lane) * 1000.0 + i * 10
    return stacks


def _lane_order(items: dict[str, _Item], edges: dict[str, set[str]]) -> list[str]:
    """The lanes top to bottom. Inputs stay on top and results at the bottom; the middle lanes
    take the order that makes the arrows span the fewest lanes (ties keep the canonical order),
    so an arrow rarely has to cross a lane it has no business in."""
    present = [lane for lane in LANE_ORDER if any(i.lane == lane for i in items.values())]
    head = [lane for lane in present if lane == "inputs"]
    tail = [lane for lane in present if lane == "results"]
    middle = [lane for lane in present if lane not in ("inputs", "results")]
    best: tuple[int, list[str]] | None = None
    for perm in itertools.permutations(middle):
        order = head + list(perm) + tail
        index = {lane: i for i, lane in enumerate(order)}
        cost = sum(abs(index[items[a].lane] - index[items[b].lane]) for a, ts in edges.items() for b in ts)
        rank = [LANE_ORDER.index(lane) for lane in perm]
        if best is None or (cost, rank) < (best[0], [LANE_ORDER.index(lane) for lane in best[1][len(head):len(head) + len(perm)]]):
            best = (cost, order)
    return best[1] if best else present
