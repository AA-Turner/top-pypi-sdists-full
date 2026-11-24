"""Input enrichment pass: read native input facts the AI snapshot omits.

One ``locator.evaluate`` per form-control node (concurrent, capped at
``max_nodes``, bounded by ``budget_s`` in total; text inputs go first). A
password value is masked as Chrome does. Native date/time/color
inputs are re-roled to Chrome's spellings with their ``value``;
``required``/``readonly`` are set; a native select's value is its selected
option label. Nodes over budget are left as parsed, except that a
textbox/searchbox whose facts did not arrive loses its value: the snapshot
prints a password's raw value, so an unconfirmed input fails closed.
"""
from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

from ._refs import ref_locator

if TYPE_CHECKING:
    from ._parse import ParsedSnapshot

_log = logging.getLogger("testmu")

# Roles whose snapshot value may be a raw password (fail closed, enrich first).
_TEXT_INPUT_ROLES = frozenset({"textbox", "searchbox"})

_ENRICH_ROLES = frozenset({
    "textbox", "searchbox", "spinbutton", "combobox", "slider", "checkbox", "radio", "switch",
})

# input[type] -> Chrome AX role spelling (as Chrome 154 reports them:
# month/week are "datetime", not "date").
_NATIVE_TYPE_ROLES = {
    "date": "date",
    "time": "inputtime",
    "datetime-local": "datetime",
    "month": "datetime",
    "week": "datetime",
    "color": "colorwell",
}

_FACTS_JS = """el => {
    const tag = (el.tagName || '').toLowerCase();
    let value = '';
    if (tag === 'select') {
        const o = el.selectedOptions && el.selectedOptions[0];
        value = o ? (o.label || o.textContent || '').trim() : '';
    } else if (typeof el.value === 'string') {
        value = el.value;
    }
    // Chrome exposes a password field's value masked; the AI snapshot does not.
    const masked = tag === 'input' && (el.type || '').toLowerCase() === 'password';
    if (masked) value = '\u2022'.repeat(value.length);
    return {
        tag: tag,
        type: (el.getAttribute('type') || el.type || '').toLowerCase(),
        value: value,
        required: !!el.required || el.getAttribute('aria-required') === 'true',
        readOnly: !!el.readOnly || el.getAttribute('aria-readonly') === 'true',
        multiple: !!el.multiple,
        masked: masked,
    };
}"""


def _apply(node, facts: dict) -> None:
    tag = facts.get("tag") or ""
    itype = facts.get("type") or ""
    if tag == "input" and itype in _NATIVE_TYPE_ROLES:
        node.role = _NATIVE_TYPE_ROLES[itype]
        node.value = str(facts.get("value") or "")
    elif facts.get("masked"):
        node.value = str(facts.get("value") or "")
    elif tag == "select" and not facts.get("multiple"):
        if facts.get("value"):
            node.value = str(facts["value"])
    if facts.get("required"):
        node.required = True
    if facts.get("readOnly") and tag != "select":
        node.readonly = True


def _all_nodes(parsed: "ParsedSnapshot"):
    """Every node of the parsed forest (main tree and all frame captures)."""
    forest = parsed.forest
    stack = [forest.main_tree] if forest.main_tree is not None else []
    captures = list(forest.frame_captures or [])
    while captures:
        fc = captures.pop()
        if fc.tree is not None:
            stack.append(fc.tree)
        captures.extend(fc.children or [])
    while stack:
        node = stack.pop()
        yield node
        stack.extend(node.children)


async def enrich_inputs(page, parsed: "ParsedSnapshot", *, max_nodes: int = 150, budget_s: float = 1.5) -> None:
    candidates = [
        (handle, node) for handle, node in parsed.nodes_by_handle.items()
        if node.role in _ENRICH_ROLES
    ]
    # Text inputs first (stable sort), so their real values survive the cap.
    candidates.sort(key=lambda hn: hn[1].role not in _TEXT_INPUT_ROLES)
    targets = candidates[:max_nodes]
    confirmed: set[int] = set()
    try:
        if targets:
            await _enrich_targets(page, targets, confirmed, budget_s)
    finally:
        # Fail closed: a text input's value is shown only when its facts
        # arrived (a password's was masked by _apply).
        for node in _all_nodes(parsed):
            if node.role in _TEXT_INPUT_ROLES and node.value and id(node) not in confirmed:
                node.value = ""


async def _enrich_targets(page, targets, confirmed: set[int], budget_s: float) -> None:
    timeout_ms = max(100, int(budget_s * 1000))

    async def one(handle, node) -> None:
        facts = await ref_locator(page, handle).evaluate(_FACTS_JS, timeout=timeout_ms)
        if isinstance(facts, dict):
            _apply(node, facts)
            confirmed.add(id(node))

    tasks = [asyncio.ensure_future(one(h, n)) for h, n in targets]
    done, pending = await asyncio.wait(tasks, timeout=budget_s)
    for t in pending:
        t.cancel()
    for t in done:
        if not t.cancelled() and t.exception() is not None:
            _log.debug("aria_perception.enrich_inputs: %s", t.exception())
    if pending:
        _log.debug("aria_perception.enrich_inputs: %d node(s) over budget", len(pending))


# ---------------------------------------------------------------------------
# Editable regions (contenteditable): the AI snapshot prints a rich-text
# editor as a plain ``generic``, which the serializer drops, leaving only
# its text. Chrome's capture turns the editable root into a textbox; this
# pass does the same.
# ---------------------------------------------------------------------------

_HAS_EDITABLE_JS = (
    "() => document.designMode === 'on' || "
    "!!document.querySelector('[contenteditable]:not([contenteditable=\"false\"])')"
)

# Roles a contenteditable root (or, when the snapshot collapsed a one-child
# root, its child) is printed as.
_EDITABLE_CANDIDATE_ROLES = ("generic", "paragraph")

# -> {root: <id of the editable root>, depth: <levels below it>, text} for
# an element inside a contenteditable, else null. Root ids live in a page
# WeakMap: nothing is written to the DOM.
_EDITABLE_ROOT_JS = """el => {
    if (!el.isContentEditable) return null;
    let root = el, depth = 0;
    while (root.parentElement && root.parentElement.isContentEditable) {
        root = root.parentElement; depth++;
    }
    const ids = window.__testmuEditableRoots || (window.__testmuEditableRoots = new WeakMap());
    if (!ids.has(root)) ids.set(root, Math.random().toString(36).slice(2));
    return {
        root: ids.get(root),
        depth: depth,
        text: (root.innerText || '').replace(/\\s+/g, ' ').trim().slice(0, 2000),
    };
}"""


async def _any_frame_editable(page, timeout_s: float) -> bool:
    async def one(frame) -> bool:
        try:
            return bool(await asyncio.wait_for(frame.evaluate(_HAS_EDITABLE_JS), timeout_s))
        except Exception:  # noqa: BLE001 — a detached or slow frame is not editable
            return False
    try:
        frames = list(page.frames)
    except Exception:  # noqa: BLE001
        return False
    return any(await asyncio.gather(*(one(f) for f in frames)))


def _promote_editable(node, text: str) -> None:
    node.role = "textbox"
    node.value = text
    # Its text now lives in the value; formatted children (bold, links) stay.
    node.children = [c for c in node.children
                     if c.role != "statictext" or c.children]


async def enrich_editables(page, parsed: "ParsedSnapshot", *, max_nodes: int = 150,
                           budget_s: float = 1.0) -> None:
    """Re-role each contenteditable root to ``textbox`` with its text as the
    value; when the snapshot collapsed a one-child root, its closest printed
    node stands for it. A page without editable content costs one probe per
    frame."""
    candidates = [
        (handle, node) for handle, node in parsed.nodes_by_handle.items()
        if node.role in _EDITABLE_CANDIDATE_ROLES
    ]
    if not candidates or not await _any_frame_editable(page, budget_s / 2):
        return
    candidates.sort(key=lambda hn: hn[1].role != "generic")  # roots are usually generic
    timeout_ms = max(100, int(budget_s * 1000))
    # root id -> (depth, node, text) of the closest printed node
    closest: dict[str, tuple[int, object, str]] = {}

    async def one(handle, node) -> None:
        facts = await ref_locator(page, handle).evaluate(_EDITABLE_ROOT_JS, timeout=timeout_ms)
        if not isinstance(facts, dict) or not facts.get("root"):
            return
        depth = int(facts.get("depth") or 0)
        best = closest.get(facts["root"])
        if best is None or depth < best[0]:
            closest[facts["root"]] = (depth, node, str(facts.get("text") or ""))

    tasks = [asyncio.ensure_future(one(h, n)) for h, n in candidates[:max_nodes]]
    done, pending = await asyncio.wait(tasks, timeout=budget_s)
    for t in pending:
        t.cancel()
    for t in done:
        if not t.cancelled() and t.exception() is not None:
            _log.debug("aria_perception.enrich_editables: %s", t.exception())
    if pending:
        _log.debug("aria_perception.enrich_editables: %d node(s) over budget", len(pending))
    for _depth, node, text in closest.values():
        _promote_editable(node, text)
