"""Fold reshape-only steps into the connections around them.

A ``data.map_template`` whose template only picks, renames, defaults and numbers the fields of each
item, and a ``data.limit`` with a fixed count, exist only to move data. Since connection sources can
pick, rename, default and slice (``matrx_graph.paths``), such a step is the connection that feeds it,
re-pointed: ``S -> M -> T`` becomes ``S -> T`` with the step's work written into the source.

    {"url": "$item.url", "title": {"$optional": "$item.title", "default": ""}, "n": "$index"}
    on items "pages"                                 ->  "pages.{url, title: title ?? \\"\\", n: #}"
    data.limit {count: 3, offset: 2} on "keywords"   ->  "keywords[2:5]"

A For Each whose per-item step is one Transform formula, gathered right after, is three steps for
one list formula: ``For each -> Transform -> Gather`` becomes ONE Transform
``{'values': [<formula> for each_index, each_item in enumerate(inputs['items'])], 'count': …}``
(the formula's ``inputs['x']`` rewritten to what the payload template gave it). It keeps the Gather's
id, so every connection out of it is untouched. Not folded: a template with ``$optional`` / ``$run``
/ ``$format``, a formula that reads ``inputs`` as a whole or a key the template does not give, a
Gather reporting holes or texts, or any step with its own settings.

Any other For Each whose step is gathered plainly right after (an AI step, a scan, a sub-workflow) becomes
that ONE step with "Run once per item" set (``data.for_each``, ``matrx_graph.step_settings``): the For Each's
connections go into the step, the Gather's connections come out of it, and the engine writes the For Each
and the Gather back out when it runs. A Gather that names its items (``items_from``, fed the same list the
For Each fans out) folds too, as ``data.for_each.pairs``: ``pairs`` and every hole still carry their item.

A Transform — or a template / filter step, written as the same formula (a template through ``fill()``,
the template engine itself, a filter as a list loop) — whose only connection goes to a Transform is
written INTO that Transform: ``inputs['k']`` there becomes the expression that computed ``k``, and the
first one's connections come straight in (an input name the second already uses is renamed). Not merged
when the first returns anything but a literal dict with plain keys, reads ``inputs`` as a whole, has
its own settings, or the merged formula would be refused (loop depth). One behavior difference: a key
of the first formula nobody read is no longer evaluated, so an error only it would raise is gone.

Two narrowing steps in a row (Filter / Dedupe / Sort / Limit / Choose Items), the first read only by the
second's list, become ONE Choose Items step (``data.choose``) when its fixed stage order (rules → repeats →
order → per group → at most N) gives the same answer: a Filter becomes a "leave out when not (…)" rule (its
``inputs['x']`` → ``inputs['item']['x']``, ``inputs['$in'][y]`` → ``inputs[y]``), and may follow a Sort unless a
Dedupe came before it; a Dedupe may not follow a Sort; nothing follows a rank written by ``rank_as``; nothing follows a Limit; a Filter over plain values, a Dedupe that merges or keeps
the last, and a receiver reading ``matches`` / ``left_out`` keep the steps apart.

``fold_reshape_steps(definition)`` returns the new definition (the input is never changed) and one
:class:`Fold` per removed step. A step is folded ONLY when the rewrite cannot change what any
receiving step gets: exactly one plain data connection in, every connection out a plain data
connection whose sources read the step's list output, no setting that gives the step its own
behavior (review marks, run-once, Only when / Shape, declared kinds, result step), and a template
made only of item paths, defaults, ``$item``, ``$index`` and literals. Everything else is left as is
and reported with the reason, so an author sees why a step stayed.

Two semantic differences, by design: a template path that does not resolve FAILS a map_template,
while a picked field that reads nothing is left out of the record (the receiving step's own input
check then decides); and an ``$optional`` default applies only to a MISSING value, while the folded
``??`` also applies it to a null one. Callers that need the old behavior keep the step.
"""

from __future__ import annotations

import ast
import copy
import json
from dataclasses import dataclass, field
from typing import Any

from matrx_graph.paths import _alternatives, _function, path_syntax_problem

__all__ = ["Fold", "Kept", "fold_reshape_steps"]

#: Step data keys that give a step behavior of its own; a step carrying one is never folded.
_OWN_BEHAVIOR = (
    "review", "once", "one_at_a_time", "when", "if_skipped", "shape", "output_kind", "input_kind",
    "deliverable", "is_primary", "join_policy", "on_skipped_upstream", "skip_defaults", "arg_merge",
    "retry", "timeout_seconds", "on_error",
)
_PLAIN_KEY = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")


@dataclass
class Fold:
    step_id: str
    step_type: str
    label: str
    source: str
    into: list[str] = field(default_factory=list)


@dataclass
class Kept:
    step_id: str
    step_type: str
    reason: str


def _kind(edge: dict[str, Any]) -> str:
    return str((edge.get("data") or {}).get("kind") or "data")


def _type(node: dict[str, Any]) -> str:
    data = node.get("data") or {}
    return str(data.get("spec_type") or node.get("type") or "")


def _plain(text: str) -> bool:
    """A name or path segment the connection grammar reads only one way: ASCII word characters that a
    pick could not mistake for a fixed value (``0``, ``true``, ``null``)."""
    if not text or not set(text) <= _PLAIN_KEY:
        return False
    try:
        json.loads(text)
    except ValueError:
        return True
    return False


def _quoted(name: str) -> str | None:
    return name if _plain(name) else None


def _literal(value: Any) -> str | None:
    """A template literal as source text, or None when it holds a template ref."""
    text = json.dumps(value)
    return None if '"$' in text else text


def _field_source(value: Any) -> str | None:
    """One template field as a pick source (``"$item.url"`` -> ``"url"``), or None."""
    if isinstance(value, str):
        if value == "$item":
            return "@"
        if value == "$index":
            return "#"
        if value.startswith("$item."):
            path = value[len("$item."):]
            return path if all(_plain(seg) for seg in path.split(".")) else None
        if value.startswith("$"):
            return None
        return json.dumps(value)
    if isinstance(value, dict) and set(value) <= {"$optional", "default"} and "$optional" in value:
        inner = _field_source(value["$optional"])
        default = _literal(value.get("default"))
        if inner is None or default is None or inner in ("@", "#") or inner.startswith('"'):
            return None
        return f"{inner} ?? {default}"
    return _literal(value)


def _template_pick(template: Any) -> str | None:
    if template == "$item":
        return ""
    if not isinstance(template, dict) or not template:
        return None
    parts: list[str] = []
    for name, value in template.items():
        if not isinstance(name, str) or not name or name.startswith("$"):
            return None
        source = _field_source(value)
        quoted = _quoted(name)
        if source is None or quoted is None:
            return None
        parts.append(quoted if source == name else f"{quoted}: {source}")
    return "{" + ", ".join(parts) + "}"


def _composable(source: str) -> bool:
    """An incoming source a pick or slice can be appended to: one path, no alternatives, no call."""
    alts = _alternatives(source)
    return len(alts) == 1 and _function(alts[0]) is None and path_syntax_problem(source) is None


def _join(base: str, suffix: str) -> str:
    if not suffix:
        return base
    if not base:
        return suffix
    return f"{base}{suffix}" if suffix.startswith("[") else f"{base}.{suffix}"


def _rewrite(step: dict[str, Any], incoming_source: str) -> tuple[str | None, str, str]:
    """(source expression for the step's list output, output list key, reason when not foldable)."""
    kind = _type(step)
    data = step.get("data") or {}
    config = data.get("config") or {}
    if data.get("input"):
        return None, "", "it has fixed inputs of its own"
    if kind == "data.map_template":
        if set(config) - {"template"}:
            return None, "", f"its {sorted(set(config) - {'template'})} setting has no connection twin"
        pick = _template_pick(config.get("template", "$item"))
        if pick is None:
            return None, "", "its template uses more than item paths, defaults and $index ($in, $run, $format …)"
        return _join(incoming_source, pick), "values", ""
    if kind == "data.limit":
        count, offset = config.get("count"), config.get("offset", 0)
        if set(config) - {"count", "offset"}:
            return None, "", f"its {sorted(set(config) - {'count', 'offset'})} setting has no connection twin"
        if not isinstance(count, int) or not isinstance(offset, int):
            return None, "", "its count comes from a run input, not a fixed number"
        return _join(incoming_source, f"[{offset or ''}:{offset + count}]"), "items", ""
    return None, "", "not a reshape step"


def _one_fold(defn: dict[str, Any], kept: dict[str, Kept]) -> Fold | None:
    nodes = {n["id"]: n for n in defn["nodes"]}
    entry = set(defn.get("entry_nodes") or [])
    for step in defn["nodes"]:
        sid, kind = step["id"], _type(step)
        if kind not in ("data.map_template", "data.limit") or sid in kept:
            continue

        def keep(reason: str) -> None:
            kept[sid] = Kept(sid, kind, reason)

        data = step.get("data") or {}
        own = [k for k in _OWN_BEHAVIOR if data.get(k)]
        if own:
            keep(f"it has its own {', '.join(own)}")
            continue
        if sid in entry:
            keep("it is where the run starts")
            continue
        ins = [e for e in defn["edges"] if e["target"] == sid]
        outs = [e for e in defn["edges"] if e["source"] == sid]
        if len(ins) != 1 or _kind(ins[0]) != "data" or ins[0].get("sourceHandle") or ins[0].get("targetHandle"):
            keep("it does not have exactly one plain connection in")
            continue
        maps_in = (ins[0].get("data") or {}).get("mappings")
        list_in = "items" if maps_in is None else (maps_in.get("items") if set(maps_in) == {"items"} else None)
        if not isinstance(list_in, str) or list_in.startswith("$") or not _composable(list_in):
            keep("its connection in carries more than a plain list path")
            continue
        if any(set(e.get("data") or {}) - {"kind", "mappings"} for e in ins + outs):
            keep("a connection in or out has its own settings (a review mark, a note …)")
            continue
        if not outs:
            keep("nothing reads it")
            continue
        source_expr, out_key, reason = _rewrite(step, list_in)
        if source_expr is None:
            keep(reason)
            continue
        new_maps: list[dict[str, str]] = []
        for out in outs:
            maps_out = (out.get("data") or {}).get("mappings")
            if _kind(out) != "data" or out.get("sourceHandle") or out.get("targetHandle") or not maps_out:
                reason = "a connection out is not a plain mapped data connection"
                break
            rewritten: dict[str, str] = {}
            for target_key, source in maps_out.items():
                if not isinstance(source, str) or not (source == out_key or source.startswith(out_key + ".")
                                                       or source.startswith(out_key + "[")):
                    reason = f"a connection out reads '{source}', not the step's list"
                    break
                rewritten[target_key] = _join(source_expr, source[len(out_key):].lstrip("."))
            else:
                new_maps.append(rewritten)
                continue
            break
        else:
            reason = ""
        if reason:
            keep(reason)
            continue
        upstream = ins[0]["source"]
        if upstream not in nodes:
            keep("its connection in comes from a step that is not in the workflow")
            continue
        edge_ids = {e["id"] for e in defn["edges"]}
        defn["edges"] = [e for e in defn["edges"] if e["target"] != sid and e["source"] != sid]
        for out, rewritten in zip(outs, new_maps):
            existing = next((e for e in defn["edges"] if e["source"] == upstream and e["target"] == out["target"]
                             and _kind(e) == "data" and (e.get("data") or {}).get("mappings") is not None
                             and not set(e.get("data") or {}) - {"kind", "mappings"}
                             and not set((e["data"]["mappings"])) & set(rewritten)
                             and not e.get("sourceHandle") and not e.get("targetHandle")), None)
            if existing is not None:
                existing["data"]["mappings"].update(rewritten)
                continue
            edge = copy.deepcopy(out)
            edge["source"] = upstream
            edge["data"]["mappings"] = rewritten
            base, n = f"{out['id']}~folded", 1
            edge["id"] = base
            while edge["id"] in edge_ids:
                n += 1
                edge["id"] = f"{base}{n}"
            edge_ids.add(edge["id"])
            defn["edges"].append(edge)
        defn["nodes"] = [n for n in defn["nodes"] if n["id"] != sid]
        return Fold(sid, kind, str(data.get("label") or sid), source_expr, [o["target"] for o in outs])
    return None


_ITEM, _INDEX = "each_item", "each_index"


def _template_value(value: Any) -> ast.expr | None:
    """One payload-template value as the expression that computes it inside the loop."""
    if isinstance(value, str) and value.startswith("$"):
        if value == "$item":
            return ast.Name(_ITEM, ast.Load())
        if value == "$index":
            return ast.Name(_INDEX, ast.Load())
        for prefix, root in (("$item.", ast.Name(_ITEM, ast.Load())), ("$in.", ast.Name("inputs", ast.Load()))):
            if value.startswith(prefix):
                node: ast.expr = root
                for part in value[len(prefix):].split("."):
                    if not part or any(ch in part for ch in "{}[]$"):
                        return None  # an item-dependent look-up ($in.x.{$index}) stays a template
                    key: Any = int(part) if part.lstrip("-").isdigit() and prefix == "$item." else part
                    node = ast.Subscript(node, ast.Constant(key), ast.Load())
                return node
        return None
    text = json.dumps(value)
    if '"$' in text:
        return None
    return ast.parse(repr(value), mode="eval").body


class _Rebind(ast.NodeTransformer):
    """``inputs['x']`` -> what the template gave ``x``; ``'x' in inputs`` -> a constant."""

    def __init__(self, payload: dict[str, ast.expr]) -> None:
        self.payload = payload
        self.ok = True

    def visit_Subscript(self, node: ast.Subscript) -> ast.AST:
        if isinstance(node.value, ast.Name) and node.value.id == "inputs":
            key = node.slice.value if isinstance(node.slice, ast.Constant) else None
            if isinstance(key, str) and key in self.payload:
                return copy.deepcopy(self.payload[key])
            self.ok = False
            return node
        return self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare) -> ast.AST:
        if (len(node.ops) == 1 and isinstance(node.ops[0], (ast.In, ast.NotIn))
                and isinstance(node.left, ast.Constant) and isinstance(node.comparators[0], ast.Name)
                and node.comparators[0].id == "inputs"):
            present = node.left.value in self.payload
            return ast.Constant(present if isinstance(node.ops[0], ast.In) else not present)
        return self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> ast.AST:
        if node.id == "inputs":
            self.ok = False  # the whole payload, or a key we cannot see — leave the step
        return node


def _for_each_formula(each: dict[str, Any], body: dict[str, Any]) -> tuple[str | None, str]:
    from matrx_graph.nodes._sandbox import validate_expression
    from matrx_graph.nodes.data.transform import expression_output_shape

    config = (each.get("data") or {}).get("config") or {}
    extra = set(config) - {"target_node_id", "payload_template", "payload_key", "include_index"}
    if extra:
        return None, f"the For Each's {sorted(extra)} setting has no list-formula twin"
    template = config.get("payload_template")
    raw: dict[str, Any] = dict(template) if isinstance(template, dict) else {config.get("payload_key", "value"): "$item"}
    if config.get("include_index"):
        raw["index"] = "$index"
    payload: dict[str, ast.expr] = {}
    for key, value in raw.items():
        expr = _template_value(value)
        if expr is None:
            return None, f"its payload template's '{key}' uses more than $item, $index, $in and literals"
        payload[key] = expr
    body_config = (body.get("data") or {}).get("config") or {}
    expression = body_config.get("expression")
    if not isinstance(expression, str) or body_config.get("define"):
        return None, "its per-item step has no single formula (or has named parts)"
    tree = ast.parse(expression, mode="eval")
    if not isinstance(tree.body, ast.Dict) and expression_output_shape(expression) is None:
        return None, "its per-item formula's result shape is not knowable"
    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    if _ITEM in names or _INDEX in names:
        return None, f"its per-item formula already uses the name {_ITEM} or {_INDEX}"
    rebind = _Rebind(payload)
    per_item = rebind.visit(tree.body)
    if not rebind.ok:
        return None, "its per-item formula reads inputs the template does not give"
    uses_index = any(isinstance(n, ast.Name) and n.id == _INDEX for n in ast.walk(per_item))
    items = "inputs['items']"
    loop = f"for {_INDEX}, {_ITEM} in enumerate({items})" if uses_index else f"for {_ITEM} in {items}"
    formula = f"{{'values': [{ast.unparse(per_item)} {loop}], 'count': len({items})}}"
    try:
        validate_expression(formula)
    except Exception as exc:  # noqa: BLE001 — any refusal means the step stays
        return None, f"as one list formula it would be refused ({exc})"
    return formula, ""


def _one_for_each_fold(defn: dict[str, Any], kept: dict[str, Kept]) -> Fold | None:
    nodes = {n["id"]: n for n in defn["nodes"]}
    for each in defn["nodes"]:
        eid = each["id"]
        if _type(each) != "control.map" or eid in kept:
            continue

        def keep(reason: str) -> None:
            kept[eid] = Kept(eid, "control.map", reason)

        body_id = ((each.get("data") or {}).get("config") or {}).get("target_node_id")
        body = nodes.get(body_id)
        if body is None or _type(body) != "data.transform":
            keep("its per-item step is real work (not one Transform formula)")
            continue
        body_out = [e for e in defn["edges"] if e["source"] == body_id]
        if any(e["target"] == body_id for e in defn["edges"]) or len(body_out) != 1:
            keep("its per-item step has other connections")
            continue
        gather = nodes.get(body_out[0]["target"])
        if (gather is None or _type(gather) != "control.gather" or _kind(body_out[0]) != "data"
                or (body_out[0].get("data") or {}).get("mappings") is not None
                or ((gather.get("data") or {}).get("config") or {})
                or [e for e in defn["edges"] if e["target"] == gather["id"] and e["source"] != body_id]):
            keep("its per-item step is not gathered plainly right after")
            continue
        gid = gather["id"]
        own = [f"{n['id']}.{k}" for n in (each, body, gather) for k in _OWN_BEHAVIOR if (n.get("data") or {}).get(k)]
        if own:
            keep(f"a step in it has its own {', '.join(own)}")
            continue
        others = json.dumps([n for n in defn["nodes"] if n["id"] not in (eid, body_id, gid)])
        if any(f'"{x}"' in others for x in (eid, body_id, gid)):
            keep("another step names one of its steps in its settings")
            continue
        outs = [e for e in defn["edges"] if e["source"] == gid]
        reads_more = [s for e in outs for s in ((e.get("data") or {}).get("mappings") or {"*": "*"}).values()
                      if not (isinstance(s, str) and (s in ("values", "count") or s.startswith(("values.", "values["))))]
        if reads_more or any(_kind(e) not in ("data", "conditional", "control") for e in outs) or any(
                e["source"] == eid for e in defn["edges"]):
            keep("something reads the For Each or the Gather beyond its values and count")
            continue
        ins = [e for e in defn["edges"] if e["target"] == eid]
        if not ins or any(_kind(e) != "data" or (e.get("data") or {}).get("mappings") is None for e in ins):
            keep("a connection into the For Each is not a plain mapped data connection")
            continue
        if any(set(e.get("data") or {}) - {"kind", "mappings"} for e in ins + body_out):
            keep("a connection in the loop has its own settings (a review mark, a note …)")
            continue
        formula, reason = _for_each_formula(each, body)
        if formula is None:
            keep(reason)
            continue
        label = str((body.get("data") or {}).get("label") or body_id)
        merged = {"id": gid, "type": "data.transform", "position": gather.get("position") or {"x": 0, "y": 0},
                  "data": {"label": label, "config": {"expression": formula}, "spec_type": "data.transform"}}
        for key in ("note", "description"):
            for source in (body, each):
                if (source.get("data") or {}).get(key):
                    merged["data"][key] = source["data"][key]
                    break
        defn["nodes"] = [n for n in defn["nodes"] if n["id"] not in (eid, body_id, gid)] + [merged]
        defn["edges"] = [e for e in defn["edges"] if e["source"] not in (eid, body_id) and e["target"] not in (eid, body_id, gid)]
        for e in ins:
            moved = copy.deepcopy(e)
            moved["target"] = gid
            defn["edges"].append(moved)
        return Fold(eid, "control.map", f"{(each.get('data') or {}).get('label') or eid} -> one list formula", formula,
                    [e["target"] for e in outs])
    return None


def _one_per_item_fold(defn: dict[str, Any], kept: dict[str, Kept]) -> Fold | None:
    nodes = {n["id"]: n for n in defn["nodes"]}
    entry = set(defn.get("entry_nodes") or [])
    for each in defn["nodes"]:
        eid = each["id"]
        if _type(each) != "control.map" or f"{eid}#per_item" in kept:
            continue

        def keep(reason: str) -> None:
            kept[f"{eid}#per_item"] = Kept(eid, "control.map", reason)

        config = (each.get("data") or {}).get("config") or {}
        body_id = config.get("target_node_id")
        body = nodes.get(body_id)
        if body is None or body_id in entry:
            keep("its per-item step is missing or starts the run")
            continue
        body_data = body.get("data") or {}
        if any(body_data.get(k) for k in ("when", "if_skipped", "shape", "for_each")):
            keep("its per-item step already has its own step settings")
            continue
        body_out = [e for e in defn["edges"] if e["source"] == body_id]
        if any(e["target"] == body_id for e in defn["edges"]) or len(body_out) != 1:
            keep("its per-item step has other connections")
            continue
        gather = nodes.get(body_out[0]["target"])
        gather_config = ((gather or {}).get("data") or {}).get("config") or {}
        items_from = gather_config.get("items_from") if set(gather_config) == {"items_from"} else None
        beside = [e for e in defn["edges"] if gather is not None and e["target"] == gather["id"] and e["source"] != body_id]
        if (gather is None or _type(gather) != "control.gather" or _kind(body_out[0]) != "data"
                or (body_out[0].get("data") or {}).get("mappings") is not None
                or (gather_config and items_from is None)
                or (beside and items_from is None)):
            keep("its per-item step is not gathered plainly right after")
            continue
        gid = gather["id"]
        own = [f"{n['id']}.{k}" for n in (each, gather) for k in _OWN_BEHAVIOR if (n.get("data") or {}).get(k)]
        if own:
            keep(f"its For Each or Gather has its own {', '.join(own)}")
            continue
        others = json.dumps([n for n in defn["nodes"] if n["id"] not in (eid, body_id, gid)])
        if any(f'"{x}"' in others for x in (eid, gid)):
            keep("another step names its For Each or Gather in its settings")
            continue
        ins = [e for e in defn["edges"] if e["target"] == eid]
        if (not ins or any(_kind(e) != "data" or (e.get("data") or {}).get("mappings") is None for e in ins)
                or "items" not in {k for e in ins for k in e["data"]["mappings"]}):
            keep("a connection into the For Each is not a plain mapped data connection with the list as items")
            continue
        if any(e["source"] == eid for e in defn["edges"]):
            keep("something reads the For Each itself")
            continue
        if any(_kind(e) not in ("data", "conditional", "control") for e in defn["edges"] if e["source"] == gid):
            keep("a failure connection leaves the Gather (it would fire per item on the step)")
            continue
        if any(((n.get("data") or {}).get("config") or {}).get("target_node_id") == body_id
               for n in defn["nodes"] if n["id"] != eid):
            keep("another step also dispatches to its per-item step")
            continue
        if any(body_data.get(k) for k in ("join_policy", "on_skipped_upstream", "skip_defaults", "arg_merge")):
            keep("its per-item step has its own join settings")
            continue
        if any(set(e.get("data") or {}) - {"kind", "mappings"} for e in ins + body_out):
            keep("a connection into the For Each or the step has its own settings (a review mark, a note …)")
            continue
        if items_from is not None and not _same_list_beside(ins, beside, items_from):
            keep("its Gather names its items from a list that is not the one the For Each fans out")
            continue
        extra = set(config) - {"target_node_id", "payload_template", "payload_key", "include_index", "max_dispatches"}
        if extra:
            keep(f"the For Each's {sorted(extra)} setting has no step-setting twin")
            continue
        template = config.get("payload_template")
        if template is None:
            template = {config.get("payload_key", "value"): "$item"}
        setting: dict[str, Any] = {"payload_template": template}
        for key in ("include_index", "max_dispatches"):
            if key in config:
                setting[key] = config[key]
        if items_from is not None:
            setting["pairs"] = True
        body = copy.deepcopy(body)
        body.setdefault("data", {})["for_each"] = setting
        defn["nodes"] = [body if n["id"] == body_id else n for n in defn["nodes"] if n["id"] not in (eid, gid)]
        outs = [e for e in defn["edges"] if e["source"] == gid]
        defn["edges"] = [e for e in defn["edges"] if eid not in (e["source"], e["target"]) and gid not in (e["source"], e["target"])]
        for e in ins:
            moved = copy.deepcopy(e)
            moved["target"] = body_id
            defn["edges"].append(moved)
        for e in outs:
            moved = copy.deepcopy(e)
            moved["source"] = body_id
            defn["edges"].append(moved)
        return Fold(eid, "control.map", f"{(each.get('data') or {}).get('label') or eid} -> 'Run once per item' on "
                    f"{body_data.get('label') or body_id}", "data.for_each", [e["target"] for e in outs])
    return None


def _same_list_beside(ins: list[dict[str, Any]], beside: list[dict[str, Any]], name: str) -> bool:
    """True when the ONE plain connection beside the per-item results brings the Gather, under
    ``name``, the very list a connection into the For Each brings as ``items`` (same step, same
    handle, same path) — what ``data.for_each.pairs`` wires when the engine writes it back out."""
    if len(beside) != 1:
        return False
    (edge,) = beside
    data = edge.get("data") or {}
    if _kind(edge) != "data" or set(data) - {"kind", "mappings"} or set(data.get("mappings") or {}) != {name}:
        return False
    path = data["mappings"][name]
    return any(
        e["source"] == edge["source"] and e.get("sourceHandle") == edge.get("sourceHandle")
        and e["data"]["mappings"].get("items") == path
        for e in ins
    )


def _dict_parts(expression: str) -> dict[str, ast.expr] | None:
    try:
        tree = ast.parse(expression, mode="eval").body
    except SyntaxError:
        return None
    if not isinstance(tree, ast.Dict) or any(not (isinstance(k, ast.Constant) and isinstance(k.value, str)) for k in tree.keys):
        return None
    return {k.value: v for k, v in zip(tree.keys, tree.values)}  # type: ignore[union-attr]


def _input_names(expr: ast.AST) -> set[str] | None:
    """Names read as ``inputs['x']``; None when ``inputs`` is read any other way."""
    names: set[str] = set()
    subscripted: set[int] = set()
    for node in ast.walk(expr):
        if (isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and node.value.id == "inputs"
                and isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str)):
            names.add(node.slice.value)
            subscripted.add(id(node.value))
        if (isinstance(node, ast.Compare) and isinstance(node.left, ast.Constant) and len(node.comparators) == 1
                and isinstance(node.comparators[0], ast.Name) and node.comparators[0].id == "inputs"):
            subscripted.add(id(node.comparators[0]))
    for node in ast.walk(expr):
        if isinstance(node, ast.Name) and node.id == "inputs" and id(node) not in subscripted:
            return None
    return names


class _Rename(ast.NodeTransformer):
    def __init__(self, renames: dict[str, str]) -> None:
        self.renames = renames

    def visit_Subscript(self, node: ast.Subscript) -> ast.AST:
        if (isinstance(node.value, ast.Name) and node.value.id == "inputs" and isinstance(node.slice, ast.Constant)
                and node.slice.value in self.renames):
            return ast.Subscript(node.value, ast.Constant(self.renames[node.slice.value]), ast.Load())
        return self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare) -> ast.AST:
        if (isinstance(node.left, ast.Constant) and node.left.value in self.renames and len(node.comparators) == 1
                and isinstance(node.comparators[0], ast.Name) and node.comparators[0].id == "inputs"):
            node.left = ast.Constant(self.renames[node.left.value])
        return self.generic_visit(node)


class _ItemPredicate(ast.NodeTransformer):
    """A data.filter predicate over one item -> the same test inside a list loop: ``inputs['f']`` is
    the item's field, ``inputs['$in']['k']`` the step's other input ``k``."""

    def __init__(self) -> None:
        self.ok = True

    def visit_Subscript(self, node: ast.Subscript) -> ast.AST:
        inner = node.value
        if (isinstance(inner, ast.Subscript) and isinstance(inner.value, ast.Name) and inner.value.id == "inputs"
                and isinstance(inner.slice, ast.Constant) and inner.slice.value == "$in"
                and isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str)):
            return ast.Subscript(ast.Name("inputs", ast.Load()), ast.Constant(node.slice.value), ast.Load())
        if isinstance(inner, ast.Name) and inner.id == "inputs" and isinstance(node.slice, ast.Constant):
            if node.slice.value in ("$in", "value"):
                self.ok = False  # the whole $in, or a scalar item bound as 'value'
                return node
            return ast.Subscript(ast.Name(_ITEM, ast.Load()), node.slice, ast.Load())
        return self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare) -> ast.AST:
        if (len(node.comparators) == 1 and isinstance(node.comparators[0], ast.Name)
                and node.comparators[0].id == "inputs"):
            node.comparators = [ast.Name(_ITEM, ast.Load())]
            node.left = self.visit(node.left)
            return node
        return self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> ast.AST:
        if node.id == "inputs":
            self.ok = False
        return node


def _as_formula(step: dict[str, Any], mapped_in: set[str]) -> str | None:
    """The step as ONE formula over the inputs its connections bring, or None. Transform: its own.
    map_template: ``fill()`` — the template engine itself — per item. Filter: a list loop."""
    data = step.get("data") or {}
    config = data.get("config") or {}
    kind = _type(step)
    if kind == "data.transform":
        return config.get("expression") if set(config) <= {"expression"} else None
    if "items" not in mapped_in:
        return None
    if kind == "data.map_template":
        if set(config) - {"template", "require_path"} or "$run" in json.dumps(config.get("template")):
            return None
        req = config.get("require_path")
        if req is not None and (not isinstance(req, str) or not all(p and (p.isdigit() or _plain(p)) for p in req.split("."))):
            return None
        kept = f"[{_ITEM} for {_ITEM} in inputs['items'] if bool(get({_ITEM}, {req!r}))]" if req else "inputs['items']"
        capped = f"({kept} if inputs['limit'] is None else {kept}[:inputs['limit']])" if "limit" in mapped_in else kept
        extra = "{" + ", ".join(f"{k!r}: inputs[{k!r}]" for k in sorted(mapped_in - {"items", "limit"})) + "}"
        template = repr(config.get("template", "$item"))
        return (f"{{'values': [fill({template}, {_ITEM}, {_INDEX}, {extra}) for {_INDEX}, {_ITEM} in enumerate({capped})], "
                f"'count': len({capped}), 'dropped': len(inputs['items']) - len({capped})}}")
    if kind == "data.filter":
        if set(config) - {"predicate"} or not isinstance(config.get("predicate"), str):
            return None
        try:
            tree = ast.parse(config["predicate"], mode="eval")
        except SyntaxError:
            return None
        if any(isinstance(n, ast.Name) and n.id in (_ITEM, _INDEX) for n in ast.walk(tree)):
            return None
        rewrite = _ItemPredicate()
        test = ast.unparse(rewrite.visit(tree).body)
        if not rewrite.ok:
            return None
        kept_list = f"[{_ITEM} for {_ITEM} in inputs['items'] if {test}]"
        return f"{{'items': {kept_list}, 'kept': len({kept_list}), 'dropped': len(inputs['items']) - len({kept_list})}}"
    return None


_MERGEABLE = ("data.transform", "data.map_template", "data.filter")


def _one_transform_merge(defn: dict[str, Any], kept: dict[str, Kept]) -> Fold | None:
    from matrx_graph.nodes._sandbox import validate_expression

    nodes = {n["id"]: n for n in defn["nodes"]}
    entry = set(defn.get("entry_nodes") or [])
    dispatched = {((n.get("data") or {}).get("config") or {}).get("target_node_id") for n in defn["nodes"]}
    for first in defn["nodes"]:
        fid = first["id"]
        if _type(first) not in _MERGEABLE or f"{fid}#merge" in kept or fid in entry or fid in dispatched:
            continue

        def keep(reason: str) -> None:
            kept[f"{fid}#merge"] = Kept(fid, "data.transform", reason)

        outs = [e for e in defn["edges"] if e["source"] == fid]
        if (len(outs) != 1 or _kind(outs[0]) != "data" or outs[0].get("sourceHandle") or outs[0].get("targetHandle")
                or set(outs[0].get("data") or {}) - {"kind", "mappings"}):
            continue  # read by more than one step, or a connection with its own settings: not merged
        second = nodes.get(outs[0]["target"])
        if second is None or _type(second) != "data.transform" or second["id"] in dispatched:
            continue
        sid = second["id"]
        if ((second.get("data") or {}).get("config") or {}).get("define"):
            continue  # a step with named parts reads inputs by those names too; never rewritten
        steps_data = [first.get("data") or {}, second.get("data") or {}]
        own = [k for d in steps_data for k in (*_OWN_BEHAVIOR, "for_each") if d.get(k)]
        if own:
            keep(f"it or the step it feeds has its own {', '.join(own)}")
            continue
        mapped_in = {k for e in defn["edges"] if e["target"] == fid for k in ((e.get("data") or {}).get("mappings") or {})}
        formula = _as_formula(first, mapped_in)
        parts = _dict_parts(formula or "")
        if parts is None:
            keep("it is not one formula returning a literal record (a template or filter with options, …)")
            continue
        maps = (outs[0].get("data") or {}).get("mappings")
        if maps is None:
            maps = {k: k for k in parts}
        if any(not isinstance(src, str) or src not in parts for src in maps.values()):
            keep("its connection reads more than its record's top-level keys")
            continue
        second_expr = ((second.get("data") or {}).get("config") or {}).get("expression", "")
        try:
            second_tree = ast.parse(second_expr, mode="eval")
        except SyntaxError:
            continue
        second_reads = _input_names(second_tree.body)
        first_reads: set[str] = set()
        for v in parts.values():
            names = _input_names(v)
            if names is None:
                first_reads = None  # type: ignore[assignment]
                break
            first_reads |= names
        if second_reads is None or first_reads is None:
            keep("a formula reads inputs as a whole")
            continue
        first_ins = [e for e in defn["edges"] if e["target"] == fid]
        if not first_ins or any(d.get("input") or d.get("inputs") for d in steps_data):
            keep("it starts the run or has fixed inputs of its own")
            continue
        if any(_kind(e) != "data" or (e.get("data") or {}).get("mappings") is None
               or set(e.get("data") or {}) - {"kind", "mappings"} for e in first_ins):
            keep("a connection into it is not a plain mapped data connection")
            continue
        second_other = {k for e in defn["edges"] if e["target"] == sid and e["id"] != outs[0]["id"]
                        for k in ((e.get("data") or {}).get("mappings") or {})}
        renames = {x: f"{x}_{fid}" for x in first_reads if x in second_other or x in maps}
        rename = _Rename(renames)
        replaced: dict[str, ast.expr] = {tk: rename.visit(copy.deepcopy(parts[src])) for tk, src in maps.items()}
        rebound = _Rebind(replaced)
        rebound_ok_names = set(replaced)

        class _Inline(ast.NodeTransformer):
            def visit_Subscript(self, node: ast.Subscript) -> ast.AST:
                if (isinstance(node.value, ast.Name) and node.value.id == "inputs" and isinstance(node.slice, ast.Constant)
                        and node.slice.value in rebound_ok_names):
                    return copy.deepcopy(replaced[node.slice.value])
                return self.generic_visit(node)

            def visit_Compare(self, node: ast.Compare) -> ast.AST:
                if (len(node.ops) == 1 and isinstance(node.ops[0], (ast.In, ast.NotIn)) and isinstance(node.left, ast.Constant)
                        and node.left.value in rebound_ok_names and isinstance(node.comparators[0], ast.Name)
                        and node.comparators[0].id == "inputs"):
                    return ast.Constant(isinstance(node.ops[0], ast.In))
                return self.generic_visit(node)

        _ = rebound
        merged_expr = ast.unparse(_Inline().visit(second_tree).body)
        try:
            validate_expression(merged_expr)
        except Exception as exc:  # noqa: BLE001 — a refusal means the steps stay
            keep(f"as one formula it would be refused ({exc})")
            continue
        merged = copy.deepcopy(second)
        merged["data"]["config"] = {**(merged["data"].get("config") or {}), "expression": merged_expr}
        defn["nodes"] = [merged if n["id"] == sid else n for n in defn["nodes"] if n["id"] != fid]
        defn["edges"] = [e for e in defn["edges"] if e["id"] != outs[0]["id"] and e["target"] != fid]
        edge_ids = {e["id"] for e in defn["edges"]}
        for e in first_ins:
            moved = copy.deepcopy(e)
            moved["target"] = sid
            moved["data"]["mappings"] = {renames.get(k, k): v for k, v in e["data"]["mappings"].items()}
            existing = next((x for x in defn["edges"] if x["source"] == moved["source"] and x["target"] == sid
                             and _kind(x) == "data" and (x.get("data") or {}).get("mappings") is not None
                             and not set(x.get("data") or {}) - {"kind", "mappings"}
                             and not set(x["data"]["mappings"]) & set(moved["data"]["mappings"])), None)
            if existing is not None:
                existing["data"]["mappings"].update(moved["data"]["mappings"])
                continue
            while moved["id"] in edge_ids:
                moved["id"] = moved["id"] + "~m"
            edge_ids.add(moved["id"])
            defn["edges"].append(moved)
        return Fold(fid, "data.transform", f"{(first.get('data') or {}).get('label') or fid} -> written into "
                    f"{(second.get('data') or {}).get('label') or sid}", merged_expr, [sid])
    return None


# --- narrowing chains -> Choose Items -------------------------------------------------------------------
#: The stage each narrowing step becomes in ``data.choose`` (rules < repeats < order < limit).
_CHOOSE_STAGE = {"data.filter": 0, "data.dedupe": 1, "data.sort": 2, "data.limit": 4}
_LEFT = "left out"


class _FilterToRule(ast.NodeTransformer):
    """A Filter predicate (item = ``inputs``, other inputs = ``inputs['$in'][x]``) as a Rules predicate (item =
    ``inputs['item']``, other inputs = ``inputs[x]``). ``ok`` is False when the predicate reads ``value`` (a
    plain-value list is wrapped as ``{'value': x}`` by Filter and not by Rules) or ``$in`` as a whole."""

    def __init__(self) -> None:
        self.ok = True
        self.others: set[str] = set()

    def visit_Subscript(self, node: ast.Subscript) -> ast.AST:
        if isinstance(node.value, ast.Name) and node.value.id == "inputs" and isinstance(node.slice, ast.Constant):
            if node.slice.value == "$in":
                self.ok = False  # $in read as a whole (an $in[x] is handled one level up)
                return node
            if node.slice.value == "value" or not isinstance(node.slice.value, str):
                self.ok = False  # a plain value or list item: Filter wraps it as {'value': x}, Rules does not
            return ast.Subscript(_item(), node.slice, ast.Load())
        inner = node.value
        if (isinstance(inner, ast.Subscript) and isinstance(inner.value, ast.Name) and inner.value.id == "inputs"
                and isinstance(inner.slice, ast.Constant) and inner.slice.value == "$in"):
            if not isinstance(node.slice, ast.Constant) or not isinstance(node.slice.value, str):
                self.ok = False
                return node
            self.others.add(node.slice.value)
            return ast.Subscript(ast.Name("inputs", ast.Load()), node.slice, ast.Load())
        return self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare) -> ast.AST:
        if (len(node.ops) == 1 and isinstance(node.ops[0], (ast.In, ast.NotIn))
                and isinstance(node.comparators[0], ast.Name) and node.comparators[0].id == "inputs"):
            # `'x' in inputs`: over a plain-value list Filter refuses it and Rules would test a substring.
            self.ok = False
            return node
        return self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> ast.AST:
        if node.id == "inputs":
            # `inputs` as a whole: Filter's holds `$in` and wraps a plain value; Rules' item does neither.
            self.ok = False
        return node


def _item() -> ast.expr:
    return ast.Subscript(ast.Name("inputs", ast.Load()), ast.Constant("item"), ast.Load())


def _as_choose(step: dict[str, Any]) -> tuple[dict[str, Any], int, set[str]] | str:
    """(Choose Items config, last stage, other inputs read) for one narrowing step, or why it cannot be one."""
    kind = _type(step)
    config = copy.deepcopy((step.get("data") or {}).get("config") or {})
    # A setting written out at its default value is no setting.
    for key, default in (("left_out", False), ("left_out_reason", ""), ("left_out_label_path", ""), ("offset", 0),
                         ("from_end", False), ("round_robin", None), ("keep", "first"), ("normalize", "none"),
                         ("missing", "last"), ("order_by", []), ("id_key", None), ("parent_key", None)):
        if key in config and config[key] == default:
            del config[key]
    if kind == "data.choose":
        last = 4 if config.get("limit") is not None else 3 if config.get("per_group") else 2 if config.get("order_by") \
            else 1 if config.get("unique_by") else 0
        return config, last, set()
    if kind == "data.filter":
        if set(config) - {"predicate", "left_out", "left_out_reason", "left_out_label_path"}:  # id_key/parent_key
            return "a Filter with tree settings"
        if not isinstance(config.get("predicate"), str):
            return "its predicate comes from a run input"
        try:
            tree = ast.parse(config["predicate"], mode="eval")
        except SyntaxError:
            return "its predicate does not parse"
        rewrite = _FilterToRule()
        when = ast.unparse(rewrite.visit(tree).body)
        if not rewrite.ok:
            return "its predicate reads a plain value, a list position or `inputs` as a whole"
        reason = config.get("left_out_reason") or f"did not pass: {config['predicate']}"
        rule = {"when": f"not ({when})", "then": {"label": _LEFT, "reason": reason}}
        return {"rules": [rule], "left_out_labels": [_LEFT]}, 0, rewrite.others
    if kind == "data.dedupe":
        if set(config) - {"key", "keep", "normalize"} or config.get("keep", "first") != "first" or not config.get("key"):
            return "a Dedupe that keeps the last, merges, matches near-duplicates or has no key"
        return {"unique_by": {"key": config["key"], "normalize": config.get("normalize", "none")}}, 1, set()
    if kind == "data.sort":
        if set(config) - {"key", "order", "missing", "order_by"}:
            return "a Sort with other settings"
        keys = config.get("order_by") or [{"key": config.get("key", ""), "order": config.get("order", "asc")}]
        others = {k["position_in"] for k in keys if k.get("position_in")}
        if any(k.get("expression") for k in keys):
            return "a Sort by expression (its other inputs are read as $in)"
        return {"order_by": keys, "missing": config.get("missing", "last")}, 2, others
    if kind == "data.limit":
        if set(config) - {"count", "round_robin"}:
            return "a Limit with an offset, from the end, or left out"
        out = {"limit": config["count"]}
        if config.get("round_robin"):
            out["round_robin"] = config["round_robin"]
        return out, 4, set()
    return "not a narrowing step"


def _one_choose_fold(defn: dict[str, Any], kept: dict[str, Kept]) -> Fold | None:
    """Two narrowing steps in a row (Filter / Dedupe / Sort / Limit / Choose Items), the first read only by
    the second, become ONE Choose Items step when Choose's fixed stage order gives the same answer: a Filter
    may follow a Sort (filtering keeps order); a Dedupe may not follow a Sort (the first copy would change);
    nothing follows a Limit; one Sort and one Limit per step."""
    nodes = {n["id"]: n for n in defn["nodes"]}
    entry = set(defn.get("entry_nodes") or [])
    dispatched = {((n.get("data") or {}).get("config") or {}).get("target_node_id") for n in defn["nodes"]}
    for first in defn["nodes"]:
        fid = first["id"]
        if _type(first) not in (*_CHOOSE_STAGE, "data.choose") or f"{fid}#choose" in kept or fid in entry or fid in dispatched:
            continue

        def keep(reason: str) -> None:
            kept[f"{fid}#choose"] = Kept(fid, _type(first), reason)

        outs = [e for e in defn["edges"] if e["source"] == fid]
        if len(outs) != 1 or _kind(outs[0]) != "data" or set(outs[0].get("data") or {}) - {"kind", "mappings"} \
                or outs[0].get("sourceHandle") or outs[0].get("targetHandle"):
            continue
        second = nodes.get(outs[0]["target"])
        if (second is None or _type(second) not in (*_CHOOSE_STAGE, "data.choose") or second["id"] in dispatched
                or second["id"] in entry):
            continue
        sid = second["id"]
        if (outs[0].get("data") or {}).get("mappings") != {"items": "items"}:
            keep("the next step reads more than its list")
            continue
        own = [k for d in (first.get("data") or {}, second.get("data") or {}) for k in (*_OWN_BEHAVIOR, "for_each", "inputs") if d.get(k)]
        if own:
            keep(f"it or the next step has its own {', '.join(own)}")
            continue
        a, b = _as_choose(first), _as_choose(second)
        if isinstance(a, str) or isinstance(b, str):
            keep(f"{a if isinstance(a, str) else b}")
            continue
        (ca, la, oa), (cb, _lb, ob) = a, b
        stage_b = min((v for k, v in (("rules", 0), ("unique_by", 1), ("order_by", 2), ("per_group", 3), ("limit", 4))
                       if k in cb), default=0)
        if ca.get("rank_as"):
            keep("the first step writes a rank, which the next step would no longer see")
            continue
        # A Filter may run before an earlier Sort (filtering keeps order), never before an earlier Dedupe.
        filter_after_sort = set(cb) <= {"rules", "left_out_labels"} and la == 2 and "unique_by" not in ca
        if not (stage_b > la or filter_after_sort) or (set(ca) & set(cb) - {"rules", "left_out_labels"}):
            keep("Choose Items' stage order would change the answer (e.g. a Dedupe after a Sort, anything after a Limit)")
            continue
        if cb.get("rules") and (any(k in ca for k in ("decision_keys", "default", "mode")) or any(
                (r.get("then") or {}).get("label") not in ca.get("left_out_labels", []) for r in ca.get("rules", []))):
            # The second step's rows are appended to a first-match table: that equals running them after the
            # first step only when every earlier row leaves its item out.
            keep("both steps decide with rules")
            continue
        # The second step's other inputs come into the merged step; a name both use is not merged.
        a_ins = [e for e in defn["edges"] if e["target"] == fid]
        b_others = [e for e in defn["edges"] if e["target"] == sid and e["id"] != outs[0]["id"]]
        names_a = {k for e in a_ins for k in ((e.get("data") or {}).get("mappings") or {})}
        names_b = {k for e in b_others for k in ((e.get("data") or {}).get("mappings") or {})}
        if any(_kind(e) != "data" or (e.get("data") or {}).get("mappings") is None for e in a_ins + b_others):
            keep("a connection into it is not a plain mapped data connection")
            continue
        if "against" in (names_a if _type(first) == "data.dedupe" else set()) | (names_b if _type(second) == "data.dedupe" else set()):
            keep("a Dedupe against saved entries")
            continue
        if (names_a & names_b) or {"item", "index"} & (names_a | names_b):
            keep("the two steps read different values under the same name")
            continue
        if not (oa <= names_a and ob <= names_b):
            keep("a predicate or sort reads an input no connection gives")
            continue
        merged_cfg = copy.deepcopy(ca)
        if cb.get("rules"):
            merged_cfg["rules"] = [*merged_cfg.get("rules", []), *cb["rules"]]
            merged_cfg["left_out_labels"] = sorted({*merged_cfg.get("left_out_labels", []), *cb["left_out_labels"]})
        for k, v in cb.items():
            if k not in ("rules", "left_out_labels"):
                merged_cfg[k] = v
        try:
            from matrx_graph.nodes.data.choose import ChooseConfig
            from matrx_graph.validation import split_setting_refs

            standing_in, _refs, problems = split_setting_refs(ChooseConfig, merged_cfg)  # {"$input": …} settings
            if problems:
                raise ValueError("; ".join(problems))
            ChooseConfig.model_validate(standing_in)
        except Exception as exc:  # noqa: BLE001 — a refusal means the steps stay
            keep(f"as one Choose Items step it would be refused ({exc})")
            continue
        # The outgoing connections: Choose Items answers items / kept / dropped like Filter, Dedupe and Limit.
        b_outs = [e for e in defn["edges"] if e["source"] == sid]
        first_drops = set(ca) - {"order_by", "missing"}
        readable = {"items", "count"} if _type(second) == "data.sort" else {"items", "kept", *(() if first_drops else ("dropped",))}
        if any((e.get("data") or {}).get("mappings") is None
               or not set(e["data"]["mappings"].values()) <= readable for e in b_outs):
            keep("a step after it reads matches, left_out or a count that would mean something else merged")
            continue
        merged = copy.deepcopy(second)
        merged["data"]["spec_type"] = "data.choose"
        if merged.get("type") in _CHOOSE_STAGE:
            merged["type"] = "data.choose"
        merged["data"]["config"] = merged_cfg
        notes = [n for n in ((first.get("data") or {}).get("note"), (second.get("data") or {}).get("note")) if n]
        if notes:
            merged["data"]["note"] = "\n".join(notes)
        for e in b_outs:  # Sort answered `count`; Choose Items answers `kept`
            m = (e.get("data") or {}).get("mappings")
            if m and _type(second) == "data.sort":
                e["data"]["mappings"] = {k: ("kept" if v == "count" else v) for k, v in m.items()}
        defn["nodes"] = [merged if n["id"] == sid else n for n in defn["nodes"] if n["id"] != fid]
        defn["edges"] = [e for e in defn["edges"] if e is not outs[0]]
        for e in a_ins:
            e["target"] = sid
        return Fold(fid, _type(first), f"{(first.get('data') or {}).get('label') or fid} + "
                    f"{(second.get('data') or {}).get('label') or sid} -> one Choose Items step", sid, [sid])
    return None


def fold_reshape_steps(definition: dict[str, Any]) -> tuple[dict[str, Any], list[Fold], list[Kept]]:
    """Fold every reshape-only step into its connections (repeatedly, so chains fold too)."""
    defn = copy.deepcopy(definition)
    folds: list[Fold] = []
    kept: dict[str, Kept] = {}
    while (fold := _one_fold(defn, kept) or _one_for_each_fold(defn, kept) or _one_per_item_fold(defn, kept)
           or _one_transform_merge(defn, kept) or _one_choose_fold(defn, kept)) is not None:
        folds.append(fold)
    # A For Each folded into "Run once per item" is not a reason it stayed.
    folded = {f.step_id for f in folds}
    return defn, folds, [k for key, k in kept.items() if k.step_id not in folded]
