"""Actionable-node annotation: what the DOM can click that the AX tree hides.

The serializer skips ``generic``/``none``/role-less AX nodes, so a clickable
``<div>`` with no ARIA role never gets a ref — neither the authoring model
(grep over the doc) nor the locator heal (the doc inlined) can target it, even
though the DOM carries the element and the ids/classes that would locate it.

One ``DOMSnapshot.captureSnapshot`` per CDP session (only the ``cursor``,
``visibility`` and ``pointer-events`` computed styles plus paint order,
every other include off) answers, for every
rendered DOM node: does it have a real JS click listener (``isClickable``)
and what is its computed cursor. A node is **actionable** when it is rendered
(it has a layout node — ``display:none`` has none — and is
``visibility: visible``, so a collapsed menu's links stay out), contains no
interactive AX descendant (the button/link inside is already the target; a
wrapper around it is noise, and a listener on an app root is event
delegation), and either

- its cursor is ``pointer`` while its nearest rendered ancestor's is not
  (the topmost pointer element: ``cursor`` is inherited, so only the top of a
  pointer run is the clickable thing), or
- it carries a click listener.

A promoted node with no label, no hint and no children has nothing the model
could match or anchor on (an empty framework root), so it is left out. Inside
a leaf control (a link, button, option …) a node is annotated only when it
carries its own label or hint — a distinct ``×`` in a tab or chip stays, the
decorative checkbox icon inside a filter link does not (the link is the
target).

An element the AX tree carries no node for at all (Chrome drops the backend
id of a ``role="presentation"`` element) cannot be promoted; its TEXT still has
an AX line, so that ``statictext`` line is tagged ``[clickable]`` instead —
grounding a text ref already climbs to its parent element.

A node the AX tree ignores because it is BLOCKED — behind a modal
(``activeModalDialog``), ``inert``, or ``aria-hidden`` — is never annotated,
nor is anything under it: the page is telling the user it can't be reached
right now (a sign-in modal over the page), and a click there would land on
the overlay.

A radio or checkbox drawn over by its own native ``<label>`` (a custom
control: the real input is invisible and the label, or its ``::before``, is
painted on top) cannot take a pointer click, since the label intercepts it.
The same snapshot, with paint order, finds what is on top at the control's
centre; when that is the control's own label, and the label holds no other
control or link, the label is recorded as ``via_label`` and the control's
ref grounds on it (clicking a label activates its control). Disabled
controls, other overlays and a control that is itself on top are left alone.

This module only ANNOTATES the captured ``AxNode`` trees in place
(``clickable``, ``dom_hint``, ``display_name``, ``via_label``); the
serializer decides what to render. It never raises and never changes a tree
when the snapshot fails, so the doc falls back to exactly today's output.
"""

from __future__ import annotations

import asyncio
import logging
import re
import time
from dataclasses import dataclass, field
from typing import Any

from ._constants import INTERACTIVE_ROLES

logger = logging.getLogger(__name__)

# AX roles the serializer would otherwise skip; a node with one of these that
# is actionable is rendered as its own ``clickable`` line.
PROMOTABLE_ROLES = frozenset({"", "generic", "none"})

# Roles that never become actionable lines, whatever the DOM says.
_NEVER_ACTIONABLE_ROLES = frozenset({"rootwebarea", "webarea", "inlinetextbox", "statictext"})
_NEVER_ACTIONABLE_TAGS = frozenset({"HTML", "BODY", "HEAD"})

# CDP ``ignoredReasons`` that mean "the user cannot reach this right now".
_BLOCKED_REASONS = frozenset({
    "activeModalDialog", "inertElement", "inertSubtree",
    "ariaHiddenElement", "ariaHiddenSubtree",
})

# Interactive roles that are the target themselves; a clickable thing inside
# one is usually part of it. ``listbox``/``combobox`` are containers whose
# custom options are often plain divs, so they are not leaves.
_LEAF_CONTROL_ROLES = INTERACTIVE_ROLES - {"listbox", "combobox"}

_SNAPSHOT_STYLES = ["cursor", "visibility", "pointer-events"]
_SNAPSHOT_TIMEOUT_S = 3.0
_DISPLAY_NAME_MAX = 100
_MAX_HINT_CLASSES = 2
_HINT_VALUE_MAX = 60

_CHECKABLE_ROLES = frozenset({"radio", "checkbox"})
# Bounds the covered-control check on a pathological page.
_MAX_COVER_CHECKS = 300
# A label holding one of these besides its own control is not clicked for it:
# the click could land on the link or the other control instead.
_LABEL_INTERACTIVE_TAGS = frozenset({"A", "BUTTON", "SELECT", "TEXTAREA", "INPUT"})
# Hit-test grid: a box is filed under every cell it overlaps, so a point
# lookup scans one cell; a box over more than _HIT_MAX_CELLS cells (a page
# wrapper) is kept in one list scanned for every lookup instead.
_HIT_CELL_PX = 256
_HIT_MAX_CELLS = 64

# Attribute order is the hint's reading order: identity first, then labels.
_HINT_ID_ATTRS = ("data-testid", "data-test", "data-test-id", "data-qa", "data-cy")
_HINT_LABEL_ATTRS = ("aria-label", "title", "alt", "placeholder", "name")

# Generated class names say nothing about the element and change per build.
_CLASS_SHAPE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{1,40}$")
_CSS_IN_JS_PREFIX = re.compile(r"^(css|sc|jss|emotion|makeStyles|styled)[-_]", re.IGNORECASE)
_DIGIT_RUN = re.compile(r"\d{3,}")


def _looks_generated(token: str) -> bool:
    """CSS-in-JS prefixes, long digit runs, or a hash-like last segment
    (``Button_root__x7Kp2``, ``card-a8f3c``: 5+ chars mixing letters and digits)."""
    if _CSS_IN_JS_PREFIX.search(token) or _DIGIT_RUN.search(token):
        return True
    last = re.split(r"[-_]", token)[-1]
    return (
        len(last) >= 5 and last != token
        and any(ch.isdigit() for ch in last) and any(ch.isalpha() for ch in last)
    )

_TEXT_TAG = "#TEXT"


class _DocLayout:
    """One snapshot document's layout boxes and paint order, to answer what
    is on top at a point. Bounds are only comparable within one document, so
    each document gets its own. Built lazily: most pages never ask."""

    def __init__(self, parents: list[int], names: list[int], strings: list[str], layout: dict[str, Any],
                 backend_ids: list[int], types: list[int], values: list[int]):
        self._parents = parents
        self._types = types
        self._values = values
        self._label_texts: dict[int, str] | None = None
        self.backend_ids = backend_ids
        self._names = names
        self._strings = strings
        self._layout = layout
        self._boxes: dict[int, list[float]] | None = None
        self._cells: dict[tuple[int, int], list[tuple[float, float, float, float, int, int]]] = {}
        self._wide: list[tuple[float, float, float, float, int, int]] = []
        self._label_controls: dict[int, list[int]] | None = None

    def _build(self) -> None:
        self._boxes = {}
        layout = self._layout
        for node_index, bounds, paint, styles in zip(
            layout.get("nodeIndex") or [], layout.get("bounds") or [],
            layout.get("paintOrders") or [], layout.get("styles") or [],
        ):
            if len(bounds) < 4:
                continue
            self._boxes.setdefault(node_index, bounds)
            x, y, w, h = bounds[:4]
            visibility = _string(self._strings, styles[1]) if len(styles) > 1 else ""
            pointer_events = _string(self._strings, styles[2]) if len(styles) > 2 else ""
            if w > 0 and h > 0 and visibility in ("", "visible") and pointer_events != "none":
                hit = (x, y, x + w, y + h, paint, node_index)
                cols = range(int(x // _HIT_CELL_PX), int((x + w) // _HIT_CELL_PX) + 1)
                rows = range(int(y // _HIT_CELL_PX), int((y + h) // _HIT_CELL_PX) + 1)
                if len(cols) * len(rows) > _HIT_MAX_CELLS:
                    self._wide.append(hit)
                    continue
                for col in cols:
                    for row in rows:
                        self._cells.setdefault((col, row), []).append(hit)

    def centre(self, i: int) -> tuple[float, float] | None:
        if self._boxes is None:
            self._build()
        box = self._boxes.get(i)
        if not box or box[2] <= 0 or box[3] <= 0:
            return None
        return box[0] + box[2] / 2, box[1] + box[3] / 2

    def top_at(self, x: float, y: float) -> int | None:
        """The node painted last at ``(x, y)``. Nodes sharing a paint layer
        tie on paint order; the later one in document order (a descendant
        or later sibling) paints over the earlier."""
        if self._boxes is None:
            self._build()
        best: tuple[int, int] | None = None
        cell = self._cells.get((int(x // _HIT_CELL_PX), int(y // _HIT_CELL_PX)), [])
        for x0, y0, x1, y1, paint, node_index in (*cell, *self._wide):
            if x0 <= x < x1 and y0 <= y < y1 and (best is None or (paint, node_index) > best):
                best = (paint, node_index)
        return best[1] if best else None

    def is_inside(self, i: int, ancestor: int) -> bool:
        while i is not None and i >= 0:
            if i == ancestor:
                return True
            i = self._parents[i] if i < len(self._parents) else -1
        return False

    def enclosing_label(self, i: int) -> int | None:
        """``i`` or its nearest ancestor that is a LABEL element."""
        while i is not None and 0 <= i < len(self._names):
            if _string(self._strings, self._names[i]).upper() == "LABEL":
                return i
            i = self._parents[i] if i < len(self._parents) else -1
        return None

    def label_text(self, label: int) -> str:
        """The text under the LABEL element ``label``, whitespace-collapsed
        and casefolded."""
        if self._label_texts is None:
            parts: dict[int, list[str]] = {}
            for i, node_type in enumerate(self._types):
                if node_type != 3:
                    continue
                p = self._parents[i] if i < len(self._parents) else -1
                while p is not None and p >= 0:
                    if _string(self._strings, self._names[p]).upper() == "LABEL":
                        parts.setdefault(p, []).append(_string(self._strings, self._values[i] if i < len(self._values) else None))
                    p = self._parents[p] if p < len(self._parents) else -1
            self._label_texts = {k: " ".join(" ".join(v).split()).casefold() for k, v in parts.items()}
        return self._label_texts.get(label, "")

    def controls_in(self, label: int) -> list[int]:
        """Links/buttons/form controls under the LABEL element ``label``."""
        if self._label_controls is None:
            self._label_controls = {}
            for i, name in enumerate(self._names):
                if _string(self._strings, name).upper() not in _LABEL_INTERACTIVE_TAGS:
                    continue
                p = self._parents[i] if i < len(self._parents) else -1
                while p is not None and p >= 0:
                    if _string(self._strings, self._names[p]).upper() == "LABEL":
                        self._label_controls.setdefault(p, []).append(i)
                    p = self._parents[p] if p < len(self._parents) else -1
        return self._label_controls.get(label, [])


@dataclass
class _DomFacts:
    tag: str
    attrs: dict[str, str]
    actionable_pointer: bool
    has_listener: bool
    # Text nodes (``tag == "#TEXT"``) only: the parent element's backend id.
    parent_backend_id: int | None = None
    # Elements only: the document's layout (None without paint order) and
    # the element's index in it.
    doc: _DocLayout | None = None
    node_index: int = -1


@dataclass
class ActionableStats:
    """Per-capture numbers, surfaced for timing and the benchmark."""

    snapshot_ms: float = 0.0
    sessions: int = 0
    dom_nodes: int = 0
    promoted: int = 0
    tagged: int = 0
    hinted: int = 0
    via_label: int = 0
    errors: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "snapshot_ms": round(self.snapshot_ms, 1),
            "sessions": self.sessions,
            "dom_nodes": self.dom_nodes,
            "promoted": self.promoted,
            "tagged": self.tagged,
            "hinted": self.hinted,
            "via_label": self.via_label,
            "errors": list(self.errors),
        }


def _string(strings: list[str], idx: int | None) -> str:
    if idx is None or idx < 0 or idx >= len(strings):
        return ""
    return strings[idx]


def index_snapshot(result: dict[str, Any]) -> dict[int, _DomFacts]:
    """``DOMSnapshot.captureSnapshot`` result -> facts per element backendNodeId.

    Element nodes are indexed with their facts; text nodes only with their
    parent element's backend id (see ``_TEXT_TAG``). Every document in the
    result (the session's own frame plus its same-process iframes) is
    indexed into one map: backend node ids are unique per CDP target.
    """
    strings: list[str] = result.get("strings") or []
    facts: dict[int, _DomFacts] = {}

    for doc in result.get("documents") or []:
        nodes = doc.get("nodes") or {}
        parents: list[int] = nodes.get("parentIndex") or []
        types: list[int] = nodes.get("nodeType") or []
        names: list[int] = nodes.get("nodeName") or []
        backend_ids: list[int] = nodes.get("backendNodeId") or []
        attributes: list[list[int]] = nodes.get("attributes") or []
        clickable_idx = set((nodes.get("isClickable") or {}).get("index") or [])

        layout = doc.get("layout") or {}
        # Paint order comes only when the snapshot asked for it (and the
        # browser supports it); without it nothing is checked for covering.
        doc_layout = (
            _DocLayout(parents, names, strings, layout, backend_ids, types, nodes.get("nodeValue") or [])
            if len(layout.get("paintOrders") or []) == len(layout.get("nodeIndex") or []) > 0
            else None
        )
        cursor_by_node: dict[int, str] = {}
        visible_nodes: set[int] = set()
        for node_index, styles in zip(layout.get("nodeIndex") or [], layout.get("styles") or []):
            cursor_by_node[node_index] = _string(strings, styles[0]) if styles else ""
            visibility = _string(strings, styles[1]) if len(styles) > 1 else ""
            if visibility in ("", "visible"):
                visible_nodes.add(node_index)

        def ancestor_cursor(i: int) -> str:
            """Cursor of the nearest RENDERED ancestor (``display:contents``
            wrappers have no layout node and are looked through)."""
            p = parents[i] if i < len(parents) else -1
            while p is not None and p >= 0:
                if p in cursor_by_node:
                    return cursor_by_node[p]
                p = parents[p] if p < len(parents) else -1
            return ""

        for i, node_type in enumerate(types):
            if i >= len(backend_ids):
                continue
            if node_type == 3:
                parent = parents[i] if i < len(parents) else -1
                if parent is not None and 0 <= parent < len(backend_ids):
                    facts[backend_ids[i]] = _DomFacts(
                        tag=_TEXT_TAG, attrs={}, actionable_pointer=False,
                        has_listener=False, parent_backend_id=backend_ids[parent],
                    )
                continue
            if node_type != 1:
                continue
            rendered = i in visible_nodes
            cursor = cursor_by_node.get(i, "")
            raw = attributes[i] if i < len(attributes) else []
            attrs = {
                _string(strings, raw[k]): _string(strings, raw[k + 1])
                for k in range(0, len(raw) - 1, 2)
            }
            facts[backend_ids[i]] = _DomFacts(
                tag=_string(strings, names[i] if i < len(names) else None).upper(),
                attrs=attrs,
                actionable_pointer=rendered and cursor == "pointer" and ancestor_cursor(i) != "pointer",
                has_listener=rendered and i in clickable_idx,
                doc=doc_layout,
                node_index=i,
            )
    return facts


def _stable_classes(class_attr: str) -> list[str]:
    kept: list[str] = []
    for cls in class_attr.split():
        if _CLASS_SHAPE.match(cls) and not _looks_generated(cls):
            kept.append(cls)
        if len(kept) >= _MAX_HINT_CLASSES:
            break
    return kept


def _clip(value: str) -> str:
    value = " ".join(value.split())
    return value if len(value) <= _HINT_VALUE_MAX else value[:_HINT_VALUE_MAX] + "…"


def build_dom_hint(attrs: dict[str, str]) -> str:
    """``{dom=#id .cls testid=x title="Close"}`` body (without braces), or ``""``.

    Identity attributes a locator would use, then the label-ish ones a grep
    would match. Generated class names and ids are left out.
    """
    parts: list[str] = []
    el_id = attrs.get("id", "")
    if el_id and _CLASS_SHAPE.match(el_id) and not _looks_generated(el_id):
        parts.append(f"#{el_id}")
    parts.extend(f".{c}" for c in _stable_classes(attrs.get("class", "")))
    for key in _HINT_ID_ATTRS:
        if attrs.get(key):
            parts.append(f"testid={_clip(attrs[key])}")
            break
    for key in _HINT_LABEL_ATTRS:
        if attrs.get(key):
            parts.append(f'{key}="{_clip(attrs[key])}"')
    return " ".join(parts)


def _subtree_text(node: Any) -> str:
    """Visible text under ``node`` as the AX tree reports it (StaticText names,
    else named leaves such as an ``image`` with alt text)."""
    out: list[str] = []

    def walk(n: Any) -> None:
        role = (n.role or "").strip().lower()
        if role == "statictext":
            if n.name:
                out.append(n.name)
            return
        if role != "inlinetextbox" and not n.children and n.name:
            out.append(n.name)
        for child in n.children:
            walk(child)

    for child in node.children:
        walk(child)
    return " ".join(" ".join(out).split())


def _label(node: Any, fact: _DomFacts) -> str:
    """What an annotated line is called: its AX name, else its subtree text,
    else a DOM label attribute — whitespace-collapsed and capped."""
    label = (node.name or "").strip() or _subtree_text(node)
    if not label:
        label = next((fact.attrs[k] for k in ("aria-label", "title", "alt") if fact.attrs.get(k)), "")
    label = " ".join(label.split())
    return label if len(label) <= _DISPLAY_NAME_MAX else label[:_DISPLAY_NAME_MAX] + "…"


def _has_interactive_descendant(node: Any) -> bool:
    for child in node.children:
        role = (child.role or "").strip().lower()
        if role in INTERACTIVE_ROLES or _has_interactive_descendant(child):
            return True
    return False


def _covering_label(node: Any, fact: _DomFacts, facts: dict[int, _DomFacts], ax_by_id: dict[int, Any]) -> Any:
    """The AX node of ``node``'s own ``<label>`` when that label (or
    something inside it, e.g. its ``::before``) is what sits on top at the
    control's centre, else None.

    The label is the control's own when its ``for`` names the control's id,
    or it has no ``for`` and wraps the control: the DOM association, which
    holds whatever the AX tree reports (Chrome's ``labelledby`` for a
    ``<label for>`` with an id carries an ``idref``, like aria-labelledby).
    None also when the label holds a link or another control (the click
    could land there), when its text is not the control's accessible name
    (an ``aria-label`` naming the control over a repeated "Yes"/"No" label,
    which only a positional locator could tell apart), or the label has no
    AX node to take its identity from.
    """
    doc = fact.doc
    if doc is None:
        return None
    centre = doc.centre(fact.node_index)
    if centre is None:
        return None
    top = doc.top_at(*centre)
    if top is None or doc.is_inside(top, fact.node_index):
        return None
    label = doc.enclosing_label(top)
    label_fact = facts.get(doc.backend_ids[label]) if label is not None and label < len(doc.backend_ids) else None
    if label_fact is None:
        return None
    if "for" in label_fact.attrs:
        if not fact.attrs.get("id") or label_fact.attrs["for"] != fact.attrs["id"]:
            return None
    elif not doc.is_inside(fact.node_index, label):
        return None
    if any(i != fact.node_index for i in doc.controls_in(label)):
        return None
    if doc.label_text(label) != " ".join((node.name or "").split()).casefold():
        return None
    return ax_by_id.get(doc.backend_ids[label])


def annotate_tree(tree: Any, facts: dict[int, _DomFacts], stats: ActionableStats) -> None:
    """Set ``clickable`` / ``dom_hint`` / ``display_name`` on ``tree``'s nodes.

    - A promotable (generic/none/role-less) actionable node: ``clickable`` +
      ``display_name`` (its subtree text, else a DOM label) + ``dom_hint``.
    - Any other non-interactive-role actionable node (``listitem``, ``image``,
      ``cell`` …): ``clickable`` + ``dom_hint`` — rendered as a ``[clickable]``
      tag on its existing line.
    - An interactive-role node with no accessible name (``button ""``):
      ``dom_hint`` only, so it can be told apart and grepped.
    - An enabled radio/checkbox covered by its own native label:
      ``via_label`` = that label's AX node.
    """

    ax_backend_ids: set[int] = set()
    ax_by_id: dict[int, Any] = {}
    checkables: list[tuple[Any, _DomFacts]] = []

    def collect(node: Any) -> None:
        if node.backend_dom_node_id:
            ax_backend_ids.add(node.backend_dom_node_id)
            ax_by_id[node.backend_dom_node_id] = node
        for child in node.children:
            collect(child)

    collect(tree)

    def tag_text_of_unattached_parent(node: Any) -> None:
        """A text line whose parent element is clickable but has no AX node."""
        fact = facts.get(node.backend_dom_node_id) if node.backend_dom_node_id else None
        if fact is None or fact.tag != _TEXT_TAG or fact.parent_backend_id in ax_backend_ids:
            return
        parent = facts.get(fact.parent_backend_id)
        if parent is None or parent.tag in _NEVER_ACTIONABLE_TAGS:
            return
        if parent.actionable_pointer or parent.has_listener:
            node.clickable = True
            node.dom_hint = build_dom_hint(parent.attrs)
            stats.tagged += 1

    def walk(node: Any, blocked: bool, in_leaf: bool) -> None:
        blocked = blocked or bool(_BLOCKED_REASONS.intersection(getattr(node, "ignored_reasons", ()) or ()))
        if blocked:
            for child in node.children:
                walk(child, True, in_leaf)
            return

        role = (node.role or "").strip().lower()
        fact = facts.get(node.backend_dom_node_id) if node.backend_dom_node_id else None

        if role == "statictext" and not in_leaf:
            tag_text_of_unattached_parent(node)
        elif fact is not None and fact.tag != _TEXT_TAG and role not in _NEVER_ACTIONABLE_ROLES and fact.tag not in _NEVER_ACTIONABLE_TAGS:
            if role in INTERACTIVE_ROLES:
                if role in _CHECKABLE_ROLES and not node.disabled:
                    checkables.append((node, fact))
                if not (node.name or "").strip():
                    node.dom_hint = build_dom_hint(fact.attrs)
                    if node.dom_hint:
                        stats.hinted += 1
            elif (fact.actionable_pointer or fact.has_listener) and not _has_interactive_descendant(node):
                hint = build_dom_hint(fact.attrs)
                if in_leaf and not (hint or _label(node, fact)):
                    pass  # part of the enclosing control, nothing of its own
                elif role in PROMOTABLE_ROLES:
                    label = _label(node, fact)
                    if label or hint or node.children:
                        node.clickable = True
                        node.dom_hint = hint
                        node.display_name = label
                        stats.promoted += 1
                else:
                    node.clickable = True
                    node.dom_hint = hint
                    if not (node.name or "").strip():
                        node.display_name = _label(node, fact)
                    stats.tagged += 1

        child_in_leaf = in_leaf or role in _LEAF_CONTROL_ROLES
        for child in node.children:
            walk(child, False, child_in_leaf)

    walk(tree, False, False)

    for node, fact in checkables[:_MAX_COVER_CHECKS]:
        label = _covering_label(node, fact, facts, ax_by_id)
        if label is not None:
            node.via_label = label
            stats.via_label += 1


async def _snapshot(session: Any) -> dict[str, Any]:
    return await asyncio.wait_for(
        session.send(
            "DOMSnapshot.captureSnapshot",
            {
                "computedStyles": _SNAPSHOT_STYLES,
                "includeDOMRects": False,
                "includePaintOrder": True,
                "includeBlendedBackgroundColors": False,
                "includeTextColorOpacities": False,
            },
        ),
        timeout=_SNAPSHOT_TIMEOUT_S,
    )


async def snapshot_facts(session: Any) -> tuple[dict[int, _DomFacts], float]:
    """Snapshot one session and index it: ``(facts, elapsed_ms)``. Raises on
    CDP failure or timeout — callers decide what a failure means."""
    start = time.monotonic()
    facts = index_snapshot(await _snapshot(session))
    return facts, (time.monotonic() - start) * 1000


async def annotate_sessions(
    groups: list[tuple[Any, list[Any]]],
    prefetched: dict[int, "asyncio.Future[tuple[dict[int, _DomFacts], float]]"] | None = None,
) -> ActionableStats:
    """One snapshot per session, then annotate every tree captured on it.

    ``groups`` = ``[(session, [tree, …]), …]``: a session's snapshot covers
    its own frame and every same-process iframe, so trees sharing a session
    share one snapshot. ``prefetched`` maps ``id(session)`` to a snapshot
    already in flight (the main session's, started alongside the AX capture);
    the rest run concurrently. A failed or timed-out session leaves its trees
    untouched. ``stats.snapshot_ms`` is the slowest session's own snapshot
    time (they overlap).
    """
    stats = ActionableStats(sessions=len(groups))
    prefetched = prefetched or {}

    async def one(session: Any) -> dict[int, _DomFacts] | None:
        try:
            pending = prefetched.get(id(session))
            facts, elapsed_ms = await (pending if pending is not None else snapshot_facts(session))
            stats.snapshot_ms = max(stats.snapshot_ms, elapsed_ms)
            return facts
        except Exception as exc:  # noqa: BLE001 — annotation is best-effort
            stats.errors.append(type(exc).__name__)
            logger.debug("actionable snapshot failed: %s", exc)
            return None

    results = await asyncio.gather(*(one(session) for session, _trees in groups))

    for (_session, trees), facts in zip(groups, results):
        if not facts:
            continue
        stats.dom_nodes += len(facts)
        for tree in trees:
            if tree is not None:
                try:
                    annotate_tree(tree, facts, stats)
                except Exception as exc:  # noqa: BLE001
                    stats.errors.append(type(exc).__name__)
    return stats
