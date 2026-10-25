"""Deterministic help for the visual-map repair loop: mechanical fixes, patches, and diagnostic groups.

Repair-reliability lane (legible-diagrams REGISTER "After closing fixes", 2026-10-23): on Haiku 5.5 the
repair rounds made diagrams worse (S2 1→11, S4 2→28) because (a) the model rewrote the WHOLE spec each
round and changed things no diagnostic named, (b) every round restarted from the latest (worse) spec, and
(c) most errors were ``render/tooSmall`` texts whose one cause is the canvas scale at the 736px chat
column — no text edit can fix them, so the model shortened labels round after round to no effect.

This module holds the parts that need no model:

- ``mechanical_fixes`` — edits the engine's own evidence fully determines: a too-small, clipped or
  overflowing sublabel / tag moves into a "Details" card (the full text is kept, never lost); an unreadable
  legend is hidden; a pinned field the engine names as conflicting is deleted; a label the engine gives an
  exact ``labelAt`` for gets it; an authored ``fromSide``/``toSide`` the engine says to remove is removed.
- ``scale_diagnostic`` — every ``render/tooSmall`` collapsed into ONE computed instruction (the canvas width
  the text needs at the chat width).
- ``pick_group`` — one diagnostic group per round when the list is long.
- ``parse_patch`` / ``apply_patch`` / ``patch_from_whole_spec`` — the model answers with the changed items
  only; code applies them to the BEST spec; a whole-spec answer is diffed and changes to items the round's
  diagnostics never named are reverted.

Pure functions; no I/O. matrx-ai never imports the host.
"""

from __future__ import annotations

import copy
import json
import re
from typing import Any

#: Fields of a drawn item that are secondary text (never its identity or primary label).
SECONDARY_TEXT_FIELDS: tuple[str, ...] = ("sublabel", "tag")
#: Top-level spec keys whose items are drawn things (the lists a node/edge text id points into).
ITEM_LISTS: tuple[str, ...] = (
    "components", "nodes", "states", "participants", "entities", "types", "events", "spans",
    "connections", "edges", "flows", "transitions", "messages", "relationships",
    "boundaries", "groups", "lanes", "phases", "stages", "segments", "activations",
)
#: Diagram types whose ``meta`` accepts ``legend`` (engine SCHEMAS, @ai-matrx/diagrams 0.4).
LEGEND_TYPES = frozenset({"architecture", "workflow", "sequence", "dataflow", "lifecycle", "erd", "class"})
DETAILS_CARD_TITLE = "Details"
#: Hand-set routing on a relationship; the engine routes everything left out.
ROUTE_GEOMETRY: tuple[str, ...] = ("route", "via", "channelX", "channelY", "bias", "fromSide", "toSide")
#: Codes whose fix is global (no one item to blame): a whole-spec answer keeps every change for these.
GLOBAL_CODES = ("render/scale", "render/tooSmall", "content/dropped", "schema/")

_OVERFLOW = re.compile(r'(Sublabel|Tag) ".*?" needs ~\d+px at the [\d.]+px legible minimum, but node "([^"]+)" provides')
_TEXT_ID = re.compile(r"^(node|edge):(.+?)(?:#\d+)?$")
_LABEL_AT = re.compile(
    r'Label "(?P<label>.+?)".*?Suggested fix: set labelAt \[(?P<x>-?[\d.]+), (?P<y>-?[\d.]+)\]', re.S
)


def _norm(text: Any) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def item_identity(item: dict[str, Any]) -> str | None:
    for key in ("id", "label", "name", "title", "text"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    if item.get("from") is not None and item.get("to") is not None:
        return f"{item.get('from')}->{item.get('to')}"
    return None


def _find_item(spec: dict[str, Any], ident: str) -> tuple[str, int, dict[str, Any]] | None:
    for key in ITEM_LISTS:
        for i, item in enumerate(spec.get(key) or []):
            if isinstance(item, dict) and (item.get("id") == ident or item_identity(item) == ident):
                return key, i, item
    return None


def _find_edge(spec: dict[str, Any], ref: str) -> dict[str, Any] | None:
    """An edge text id is ``a->b`` (measure.mjs); match by from/to, else by id."""
    src, _, dst = ref.partition("->")
    for key in ITEM_LISTS:
        for item in spec.get(key) or []:
            if isinstance(item, dict) and item.get("from") == src and item.get("to") == dst:
                return item
    found = _find_item(spec, ref)
    return found[2] if found else None


def _details_card(spec: dict[str, Any]) -> dict[str, Any]:
    cards = spec.setdefault("cards", [])
    for card in cards:
        if isinstance(card, dict) and card.get("title") == DETAILS_CARD_TITLE:
            card.setdefault("items", [])
            return card
    card = {"dot": "emerald", "title": DETAILS_CARD_TITLE, "items": []}
    cards.append(card)
    return card


def _move_to_card(spec: dict[str, Any], item: dict[str, Any], field: str) -> str | None:
    text = item.get(field)
    if not isinstance(text, str) or not text.strip():
        return None
    name = item.get("label") or item.get("name") or item.get("id") or "item"
    _details_card(spec)["items"].append(f"{_norm(name)}: {_norm(text)}")
    del item[field]
    return f"moved the {field} of {item.get('id') or name} (\"{_norm(text)}\") into the {DETAILS_CARD_TITLE} card"


def _delete_pointer(spec: dict[str, Any], pointer: str, *, allow_root: bool = False) -> bool:
    parts = [p.replace("~1", "/").replace("~0", "~") for p in pointer.strip("/").split("/") if p != ""]
    if len(parts) < (1 if allow_root else 2) or (len(parts) == 1 and parts[0] in _FROZEN):
        return False
    target: Any = spec
    for p in parts[:-1]:
        if isinstance(target, list) and p.isdigit() and int(p) < len(target):
            target = target[int(p)]
        elif isinstance(target, dict) and p in target:
            target = target[p]
        else:
            return False
    last = parts[-1]
    if isinstance(target, dict) and last in target and last not in ("id", "from", "to", "label"):
        del target[last]
        return True
    return False


def _secondary_field_for(item: dict[str, Any], text: str) -> str | None:
    text = _norm(text)
    for field in SECONDARY_TEXT_FIELDS:
        if _norm(item.get(field)) == text and text:
            return field
    return None


def identity_fixes(spec: dict[str, Any], diagnostics: list[dict[str, Any]]) -> tuple[dict[str, Any], list[str]]:
    """The spec's identity set to the engine's own constant. Returns (new spec, edits made).

    ``schema/const`` at /schema_version or /diagram_type carries the one allowed value as evidence: fully
    determined, and frozen to the repairer (``_FROZEN``). 2026-10-24 live: a lifecycle written as
    diagram_type "state" / schema_version 1; three repair answers set 3 + "lifecycle", every one was
    refused, and the error could never clear. The loop adopts these edits unconditionally: no other
    change can remove the error."""
    out = copy.deepcopy(spec)
    edits: list[str] = []
    for d in diagnostics:
        if not isinstance(d, dict) or d.get("severity") != "error" or d.get("code") != "schema/const":
            continue
        path = str((d.get("subject") or {}).get("path") or "").strip("/")
        evidence = d.get("evidence") or {}
        if path in _FROZEN and "allowedValue" in evidence and out.get(path) != evidence["allowedValue"]:
            edits.append(f"{path}: {out.get(path)!r} → {evidence['allowedValue']!r} (the engine's constant)")
            out[path] = evidence["allowedValue"]
    return out, edits


def mechanical_fixes(
    type_: str, spec: dict[str, Any], diagnostics: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[str]]:
    """Apply every fix the diagnostics' own evidence fully determines. Returns (new spec, edits made).

    Never removes a drawn item or a primary label; secondary text is moved into a card, never lost."""
    out = copy.deepcopy(spec)
    edits: list[str] = []
    legend_small = False
    renamed = _rename_misnamed_list(out, diagnostics)
    if renamed:
        edits.append(renamed)
    for d in diagnostics:
        if not isinstance(d, dict) or d.get("severity") != "error":
            continue
        code = str(d.get("code") or "")
        subject = d.get("subject") or {}
        evidence = d.get("evidence") or {}
        message = str(d.get("message") or "")
        # Measured secondary text (render/tooSmall | clipped | truncated) → into the Details card.
        if code in ("render/tooSmall", "render/clipped", "render/truncated"):
            ident = str(subject.get("id") or "")
            text = _text_of(message)
            m = _TEXT_ID.match(ident)
            if m and m.group(1) == "node":
                found = _find_item(out, m.group(2))
                if found and text is not None:
                    field = _secondary_field_for(found[2], text)
                    if field:
                        edit = _move_to_card(out, found[2], field)
                        if edit:
                            edits.append(edit)
            elif code == "render/tooSmall" and ident.startswith(("text:", "boundary:")):
                legend_small = True
            continue
        # Engine readability of a secondary text field, with the field's path.
        path = str(subject.get("path") or "")
        if path.endswith(tuple(f"/{f}" for f in SECONDARY_TEXT_FIELDS)) and "readab" in code:
            field = path.rsplit("/", 1)[1]
            parts = path.strip("/").split("/")
            if len(parts) == 3 and parts[1].isdigit():
                items = out.get(parts[0]) or []
                idx = int(parts[1])
                if idx < len(items) and isinstance(items[idx], dict):
                    edit = _move_to_card(out, items[idx], field)
                    if edit:
                        edits.append(edit)
            continue
        # A workflow node too narrow for its sublabel / tag arrives as layout/constraint with the field and
        # node only in the message ("Sublabel "…" needs ~252px …, but node "x" provides 192px"); engine
        # releases from 2026-10-23 shorten such a sublabel themselves, older ones refuse the picture.
        named = _OVERFLOW.findall(message) if code == "layout/constraint" else []
        if named:
            for field, node_id in named:
                found = _find_item(out, node_id)
                if found:
                    edit = _move_to_card(out, found[2], field.lower())
                    if edit:
                        edits.append(edit)
            continue
        if code.endswith("tag-overflow") and subject.get("nodeId"):
            found = _find_item(out, str(subject["nodeId"]))
            if found:
                edit = _move_to_card(out, found[2], "tag")
                if edit:
                    edits.append(edit)
            continue
        # A property the schema does not allow, named by the engine: delete it (content loss is caught by
        # the content check, which would keep this from being adopted).
        if code == "schema/additionalProperties" and evidence.get("additionalProperty"):
            if renamed or (path in ("", "/") and isinstance(out.get(evidence["additionalProperty"]), list)
                           and out.get(evidence["additionalProperty"])):
                continue  # a list of drawn items is never deleted; the rename above or the model handles it
            pointer = (path.rstrip("/") + "/" + str(evidence["additionalProperty"])) if path else ""
            if pointer and _delete_pointer(out, pointer, allow_root=True):
                edits.append(f"deleted {pointer} (not a field this diagram type has)")
            continue
        # A route preset the engine cannot satisfy: drop the preset and its hand-set sides so it routes.
        if code.endswith("route-preset-conflict") and subject.get("edge"):
            found = _find_item(out, str(subject["edge"]))
            if found:
                removed = [k for k in ("route", "bias", "fromSide", "toSide", "via") if found[2].pop(k, None) is not None]
                if removed:
                    edits.append(f"removed {', '.join(removed)} from edge {subject['edge']} (its route preset cannot be drawn)")
            continue
        # Hand-set geometry the engine names as conflicting: delete it and let the engine route.
        pins = [p.get("path") for p in evidence.get("conflictingPins") or [] if isinstance(p, dict) and p.get("path")]
        if pins:
            for pointer in pins:
                if _delete_pointer(out, pointer):
                    edits.append(f"deleted the conflicting pin {pointer}")
            continue
        # The engine computed a free spot for an overlapping label.
        m = _LABEL_AT.search(message)
        if code == "layout/constraint" and m:
            label = m.group("label")
            matches = [it for key in ITEM_LISTS for it in out.get(key) or []
                       if isinstance(it, dict) and "from" in it and it.get("label") == label]
            if len(matches) == 1:
                rel = matches[0]
                rel["labelAt"] = [float(m.group("x")), float(m.group("y"))]
                for k in ("labelDx", "labelDy", "labelSegment"):
                    rel.pop(k, None)
                edits.append(f"set labelAt {rel['labelAt']} on the \"{label}\" label (the engine's suggested spot)")
            continue
        # The engine says: remove authored sides so it can re-plan the route.
        if "remove them so the renderer can re-plan" in message and subject.get("collection") is not None:
            items = out.get(str(subject["collection"])) or []
            idx = subject.get("index")
            if isinstance(idx, int) and idx < len(items) and isinstance(items[idx], dict):
                removed = [k for k in ("fromSide", "toSide") if items[idx].pop(k, None) is not None]
                if removed:
                    edits.append(f"removed {', '.join(removed)} from {subject.get('collection')}[{idx}] "
                                 f"({subject.get('id') or ''}) so the engine re-plans its route")
        # A route conflict on relationships that carry hand-set geometry: drop that geometry so the engine
        # routes them itself (the notice already prefers deleting geometry; the monotone check keeps this
        # only when it lowers the error count).
        if code.startswith(("composition/", "clean-flow/")):
            for ref in (subject, evidence.get("otherRelationship")):
                if not isinstance(ref, dict) or ref.get("collection") is None or not isinstance(ref.get("index"), int):
                    continue
                items = out.get(str(ref["collection"])) or []
                if ref["index"] < len(items) and isinstance(items[ref["index"]], dict):
                    item = items[ref["index"]]
                    removed = [k for k in ROUTE_GEOMETRY if item.pop(k, None) is not None]
                    if removed:
                        edits.append(f"removed {', '.join(removed)} from {ref['collection']}[{ref['index']}] "
                                     f"({ref.get('id') or ''}) so the engine routes it")
    if legend_small and type_ in LEGEND_TYPES:
        meta = out.setdefault("meta", {})
        legend = meta.get("legend") if isinstance(meta.get("legend"), dict) else {}
        if legend.get("mode") != "hidden":
            meta["legend"] = {**legend, "mode": "hidden"}
            edits.append("hid the legend (its text cannot be drawn at a legible size at the chat width)")
    # De-duplicate (the same text is reported per capture key).
    seen: set[str] = set()
    unique = [e for e in edits if not (e in seen or seen.add(e))]
    return (out if unique else spec), unique


def _rename_misnamed_list(spec: dict[str, Any], diagnostics: list[dict[str, Any]]) -> str | None:
    """A required list written under another name (2026-10-23 S5: a dataflow's ``flows`` written as ``edges``):
    the engine reports one missing required list and one unsupported list at the root — rename it."""
    missing = [str((d.get("evidence") or {}).get("missingProperty")) for d in diagnostics
               if isinstance(d, dict) and d.get("code") == "schema/required"
               and str((d.get("subject") or {}).get("path") or "/") in ("", "/")
               and (d.get("evidence") or {}).get("missingProperty") in ITEM_LISTS]
    extra = [str((d.get("evidence") or {}).get("additionalProperty")) for d in diagnostics
             if isinstance(d, dict) and d.get("code") == "schema/additionalProperties"
             and str((d.get("subject") or {}).get("path") or "/") in ("", "/")
             and isinstance(spec.get((d.get("evidence") or {}).get("additionalProperty")), list)]
    if len(missing) != 1 or len(extra) != 1 or missing[0] in spec:
        return None
    spec[missing[0]] = spec.pop(extra[0])
    return f"renamed {extra[0]} to {missing[0]} (the list this diagram type requires)"


def _text_of(message: str) -> str | None:
    m = re.match(r'Text "(.*)" \(', message, re.S)
    return m.group(1) if m else None


# ── The scale group ────────────────────────────────────────────────────────────


def scale_diagnostic(
    diagnostics: list[dict[str, Any]], canvas_width: float | None,
) -> dict[str, Any] | None:
    """Every ``render/tooSmall`` error as ONE computed instruction: the canvas width the smallest text needs.

    Text px = font x (display width / canvas width), so shortening a label does not make it bigger; only a
    narrower canvas does (2026-10-23 S2: sublabels shortened from "browser / app" to "app" stayed at 4.73px)."""
    small = [d for d in diagnostics if isinstance(d, dict) and d.get("code") == "render/tooSmall"]
    if not small:
        return None
    pxs = [float((d.get("evidence") or {}).get("px") or 0) for d in small]
    pxs = [p for p in pxs if p > 0]
    floor = next((float((d.get("evidence") or {}).get("floor_px")) for d in small
                  if (d.get("evidence") or {}).get("floor_px")), None)
    smallest = min(pxs) if pxs else None
    texts = sorted({_text_of(str(d.get("message") or "")) or "" for d in small} - {""})
    evidence: dict[str, Any] = {"texts": len(small), "smallest_px": smallest, "floor_px": floor}
    fixes: list[str]
    if canvas_width and smallest and floor:
        target = int(canvas_width * smallest / floor)
        evidence.update({"canvas_width": round(canvas_width), "max_canvas_width": target})
        message = (
            f"{len(small)} texts are drawn below the {floor:g}px floor at the chat width (smallest {smallest:g}px) "
            f"because the whole diagram is {round(canvas_width)} units wide and is scaled down to fit the chat "
            f"column. Shortening words does not help; the canvas must be at most {target} units wide."
        )
        fixes = [
            f"make the diagram at most {target} units wide: put items in more rows and fewer columns, or bring "
            "columns closer together (smaller x positions / gaps), keeping every item",
            "narrow wide nodes (shorter primary labels let the engine draw narrower boxes)",
        ]
    else:
        message = (f"{len(small)} texts are drawn below the legibility floor at the chat width; the diagram is "
                   "too wide for the chat column")
        fixes = ["make the diagram narrower: more rows, fewer columns, keeping every item"]
    return {"code": "render/scale", "severity": "error", "message": message,
            "subject": {"texts": texts[:12]}, "evidence": evidence, "supportedFixes": fixes}


def _group_key(d: dict[str, Any]) -> str:
    code = str(d.get("code") or "unknown")
    return "schema/" if code.startswith("schema/") else code


def prompt_diagnostics(
    diagnostics: list[dict[str, Any]], *, canvas_width: float | None, group_max: int,
) -> tuple[list[dict[str, Any]], str | None]:
    """The errors the model is shown this round: tooSmall collapsed into the scale instruction, and only ONE
    group when there are more than ``group_max``. Returns (errors to show, the group's name or None)."""
    errors = [d for d in diagnostics if isinstance(d, dict) and d.get("severity") == "error"]
    scale = scale_diagnostic(errors, canvas_width)
    shown = [d for d in errors if d.get("code") != "render/tooSmall"] + ([scale] if scale else [])
    if len(errors) <= group_max:
        return shown, None
    groups: dict[str, list[dict[str, Any]]] = {}
    for d in shown:
        groups.setdefault(_group_key(d), []).append(d)
    weight = {k: sum(1 for d in errors if _group_key(d) == k) for k in groups}
    weight["render/scale"] = sum(1 for d in errors if d.get("code") == "render/tooSmall")

    def rank(key: str) -> tuple[int, int]:
        first = 0 if key == "schema/" else 1 if key == "content/dropped" else 2
        return (first, -weight.get(key, len(groups[key])))

    key = sorted(groups, key=rank)[0]
    return groups[key][: max(group_max, 1)] if key != "render/scale" else groups[key], key


# ── Patches ────────────────────────────────────────────────────────────────────

PATCH_INSTRUCTIONS = (
    "Answer with ONLY a patch: the items you change, never the whole diagram. Format:\n"
    '{"changes": [\n'
    '  {"list": "<list name, e.g. nodes>", "id": "<item id>", "set": {"<field>": <new value>}, "unset": ["<field>"]},\n'
    '  {"list": "<list name>", "add": {<a new item>}},\n'
    '  {"key": "meta", "set": {"<field>": <new value>}},\n'
    '  {"key": "<top-level field, e.g. stages>", "value": <its whole new value>}\n'
    "]}\n"
    "Every item you do not name stays exactly as it is. Never remove an item. No prose."
)


def _json_objects(text: str) -> list[Any]:
    """Every top-level JSON object in ``text`` (fenced or bare), in order."""
    out: list[Any] = []
    depth = 0
    start = None
    in_str = False
    esc = False
    for i, ch in enumerate(text):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}" and depth:
            depth -= 1
            if depth == 0 and start is not None:
                try:
                    out.append(json.loads(text[start : i + 1]))
                except ValueError:
                    pass
                start = None
    return out


def parse_patch(answer: Any) -> list[dict[str, Any]] | None:
    """The ``changes`` list of a patch answer, or None when the answer holds no patch."""
    candidates = [answer] if isinstance(answer, dict) else _json_objects(answer) if isinstance(answer, str) else []
    for obj in reversed(candidates):
        if isinstance(obj, dict) and isinstance(obj.get("changes"), list):
            return [c for c in obj["changes"] if isinstance(c, dict)]
    return None


_FROZEN = frozenset({"schema_version", "diagram_type"})


def apply_patch(spec: dict[str, Any], changes: list[dict[str, Any]]) -> tuple[dict[str, Any], list[str], list[str]]:
    """Apply a patch to a COPY of ``spec``. Returns (new spec, applied, refused) — refusals are named."""
    out = copy.deepcopy(spec)
    applied: list[str] = []
    refused: list[str] = []
    for c in changes:
        sets = c.get("set") if isinstance(c.get("set"), dict) else {}
        raw_unset = c.get("unset")
        unsets = [raw_unset] if isinstance(raw_unset, str) else [
            u for u in (raw_unset if isinstance(raw_unset, list) else []) if isinstance(u, str)]
        if isinstance(c.get("key"), str) and ("value" in c or isinstance(c.get("set"), list)):
            key = c["key"]
            if key in _FROZEN:
                refused.append(f"{key} cannot be replaced")
                continue
            out[key] = copy.deepcopy(c["value"] if "value" in c else c["set"])
            applied.append(f"{key}: replaced")
            continue
        if isinstance(c.get("key"), str):
            key = c["key"]
            if key in _FROZEN or key in ITEM_LISTS:
                refused.append(f"key {key} cannot be patched as an object")
                continue
            target = out.setdefault(key, {})
            if not isinstance(target, dict):
                refused.append(f"{key} is not an object")
                continue
            target.update(sets)
            for u in unsets:
                target.pop(u, None)
            applied.append(f"{key}: set {sorted(sets)} unset {unsets}")
            continue
        lst = c.get("list")
        if not isinstance(lst, str) or (lst not in out and lst not in ITEM_LISTS) or lst in _FROZEN:
            refused.append(f"unknown list {lst!r}")
            continue
        items = out.setdefault(lst, [])
        if not isinstance(items, list):
            refused.append(f"{lst} is not a list")
            continue
        if isinstance(c.get("add"), dict):
            items.append(copy.deepcopy(c["add"]))
            applied.append(f"{lst}: added {item_identity(c['add'])}")
            continue
        target = None
        if c.get("id") is not None:
            target = next((it for it in items if isinstance(it, dict)
                           and (it.get("id") == c["id"] or item_identity(it) == c["id"])), None)
        elif isinstance(c.get("index"), int) and 0 <= c["index"] < len(items):
            target = items[c["index"]]
        if not isinstance(target, dict):
            refused.append(f"{lst}: no item {c.get('id', c.get('index'))!r}")
            continue
        for k in ("id", "from", "to"):
            if k in sets and sets[k] != target.get(k):
                refused.append(f"{lst}/{c.get('id')}: {k} cannot change")
                sets = {kk: vv for kk, vv in sets.items() if kk != k}
        target.update(sets)
        for u in unsets:
            if u not in ("id", "from", "to", "label"):
                target.pop(u, None)
        applied.append(f"{lst}/{c.get('id', c.get('index'))}: set {sorted(sets)} unset {unsets}")
    return out, applied, refused


def named_items(diagnostics: list[dict[str, Any]]) -> set[str]:
    """Every item identity the diagnostics name (ids, from->to pairs, collection[index])."""
    names: set[str] = set()

    def add_rel(obj: Any) -> None:
        if not isinstance(obj, dict):
            return
        for k in ("id", "node", "nodeId", "edge", "obstacleId", "otherEdge"):
            if isinstance(obj.get(k), str):
                names.add(obj[k])
        if obj.get("from") is not None and obj.get("to") is not None:
            names.add(f"{obj['from']}->{obj['to']}")
        if obj.get("collection") is not None and isinstance(obj.get("index"), int):
            names.add(f"{obj['collection']}[{obj['index']}]")
        for i in obj.get("ids") or []:
            names.add(str(i))

    for d in diagnostics:
        if not isinstance(d, dict):
            continue
        subject = d.get("subject") or {}
        add_rel(subject)
        evidence = d.get("evidence") or {}
        add_rel(evidence.get("otherRelationship"))
        add_rel({k: evidence.get(k) for k in ("obstacleId", "otherEdge")})
        m = _TEXT_ID.match(str(subject.get("id") or ""))
        if m:
            names.add(m.group(2))
    return names


def _is_named(item: dict[str, Any], lst: str, index: int, names: set[str]) -> bool:
    keys = {str(item.get("id")) if item.get("id") is not None else "", item_identity(item) or "",
            f"{item.get('from')}->{item.get('to')}", f"{lst}[{index}]"}
    return bool(keys & names)


def patch_from_whole_spec(
    best: dict[str, Any], answer: dict[str, Any], diagnostics: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[str]]:
    """A whole-spec answer as a patch against the BEST spec, keeping only changes the diagnostics justify.

    Removed items are not removed (content stays); changes to items no diagnostic named are reverted unless
    the group is global (scale, schema, content) or names nothing. Returns (changes, reverted notes)."""
    names = named_items(diagnostics)
    global_fix = not names or any(str(d.get("code") or "").startswith(GLOBAL_CODES) for d in diagnostics)
    changes: list[dict[str, Any]] = []
    reverted: list[str] = []
    for key in sorted(set(best) | set(answer)):
        if key in _FROZEN:
            continue
        old, new = best.get(key), answer.get(key)
        if old == new:
            continue
        if isinstance(new, list) and (isinstance(old, list) or old is None):
            old_items = {item_identity(it): (i, it) for i, it in enumerate(old or []) if isinstance(it, dict)}
            same_length = len(new) == len(old or [])
            for n, it in enumerate(new):
                if not isinstance(it, dict):
                    continue
                ident = item_identity(it)
                if ident not in old_items:
                    if same_length and isinstance((old or [])[n], dict) and (old or [])[n].get("id") is None:
                        # An id-less item whose label changed is the same item in the same place.
                        before = old[n]
                        if not global_fix and not _is_named(before, key, n, names):
                            reverted.append(f"{key}[{n}]")
                            continue
                        changes.append({"list": key, "index": n,
                                        "set": {k: v for k, v in it.items() if before.get(k) != v},
                                        "unset": [k for k in before if k not in it]})
                    else:
                        changes.append({"list": key, "add": it})
                    continue
                i, before = old_items[ident]
                if before == it:
                    continue
                if not global_fix and not _is_named(before, key, i, names):
                    reverted.append(f"{key}/{ident}")
                    continue
                sets = {k: v for k, v in it.items() if before.get(k) != v}
                unsets = [k for k in before if k not in it]
                ref = {"id": ident} if before.get("id") is not None else {"index": i}
                changes.append({"list": key, **ref, "set": sets, "unset": unsets})
            continue
        if isinstance(new, dict) and (isinstance(old, dict) or old is None):
            old = old or {}
            sets = {k: v for k, v in new.items() if old.get(k) != v}
            unsets = [k for k in old if k not in new]
            if sets or unsets:
                changes.append({"key": key, "set": sets, "unset": unsets})
            continue
        reverted.append(key)
    return changes, reverted
