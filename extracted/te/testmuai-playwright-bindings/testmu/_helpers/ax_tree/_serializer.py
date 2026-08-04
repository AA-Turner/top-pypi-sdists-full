"""AX-tree text serializer producing a greppable doc + per-step ref table.

In its text-only mode, the reasoning model never receives the raw
accessibility tree or a screenshot directly; instead it pulls page
context via a grep tool over the document this module produces. Each
emitted node gets a per-step reference (``e1``, ``e2``, ...) later used for
action grounding (ref -> backendNodeId). Refs are regenerated every step and
are only valid for the step that produced them.

Pure Python, no I/O — the caller captures the ``AxNode`` tree (see
``testmu._helpers._dom_structured``) before calling this module.

## Frame-aware merge

``serialize_ax_tree`` optionally accepts ``frame_children`` — the list of
``FrameCapture``s (see ``frame_capture.py``) belonging directly to the
tree being walked. Whenever the walk encounters an ``iframe``-role AX node
it looks that node up in a dict keyed by each ``FrameCapture``'s
``owner_backend_node_id`` (the SAME iframe AX node's own
``backend_dom_node_id``) — a stable-identity lookup, never positional.
Earlier revisions consumed ``frame_children`` positionally
(``next(iterator)`` as each ``iframe`` node was visited), assuming capture
enumerated a frame's children in the same order the AX tree renders its
``iframe`` nodes in; a live repro proved frame ATTACH order (what capture
used to enumerate by) and AX/document RENDER order can diverge with equal
counts, silently swapping which captured content lands under which
``iframe`` line. See ``frame_capture.py``'s module docstring for the fix
and the repro.

A matched frame's own serialized block is inlined directly beneath the
iframe's line, one indent level deeper, marked ``[frame f<N>]`` on the
iframe's own line. A frame that was skipped or failed renders a
bracketed note line instead of content. A frame whose OWNER could
not be resolved to a real content frame id at all
(``status == "unresolved"``) renders ``[frame ?]`` on the iframe's own line
and ``[frame ? unresolved — not captured]`` beneath it — never a guessed
frame number. Refs and the 500KB doc cap are shared globally across the
whole merge — one continuous ``e<N>`` space. Passing no
``frame_children`` (or an empty list) reproduces today's single-tree
output byte-for-byte — the default keeps existing callers and plain
(iframe-free) pages unchanged.

## Per-frame line budget removed

Earlier revisions additionally capped each individual frame's own content
at a fixed ``FRAME_LINE_BUDGET`` line count, past which a truncation note
replaced the rest of that frame's tree. Removed: this document is never
sent to the model directly (the grep/digest tools operate over capped
windows into it), so truncating the *document* protected nothing the
model reads while making caller-side state (grep diagnostics, digest
inputs) silently incomplete. The global ``AX_DOC_MAX_CHARS`` cap below is
unchanged and remains the only size guard on this module's output.

## Deterministic frame numbering

``[frame fN]`` display numbers are minted HERE, during this function's own
depth-first document-order walk — never carried in from ``FrameCapture``
(``frame_capture.py`` no longer even has a ``frame_number`` field). Frame
capture happens concurrently (``asyncio.gather``, per nesting level), so
any number assigned at discovery time would depend on real-world
completion order, not document order — the same forest could render two
different ``[frame fN]`` numberings across two runs. Since this walk
already visits ``iframe`` AX nodes in true document order (the same order
the attribution fix above made correct), a single counter incremented once
per merge candidate encountered here is deterministic by construction:
same forest -> same doc, byte-for-byte, regardless of capture-completion
order.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

# serialize_ax_tree only READS attributes, so no node class import is needed.
# FRAME_ROLE / FRAME_DEPTH_BACKSTOP live in _constants.py / _frame_capture.py
# — imported here so both walkers share a single source (no duplication/drift).
from ._constants import FRAME_ROLE
from ._frame_capture import FRAME_DEPTH_BACKSTOP

if TYPE_CHECKING:
    from .._dom_structured import AxNode  # type hints only
    from ._frame_capture import FrameCapture

logger = logging.getLogger(__name__)

# Structural/container roles that carry no information of their own: skipped
# in the rendered doc, but their children are promoted to the same depth as
# the skipped node (it consumes neither a ref nor an indent level). Mirrors
# full_flat_dom.py's _SKIP_ROLES (spec section 2).
_SKIP_ROLES = frozenset({"none", "generic", "rootwebarea", "webarea", "inlinetextbox"})

AX_DOC_MAX_CHARS = 500_000
TEXT_TRUNCATE_CHARS = 200

_TRUNCATION_MARKER = "…[document truncated]"

# Column layout: "e<N>" + _BASE_GAP spaces + (_INDENT_PER_DEPTH * depth) spaces + role.
# Matches the worked example in spec section 2 (depth 0 -> 3 spaces, depth 1 -> 5, ...).
_BASE_GAP = 3
_INDENT_PER_DEPTH = 2


def _index_by_owner(frame_children: list[FrameCapture]) -> dict[int, FrameCapture]:
    """Index a level's ``FrameCapture``s by their
    OWNER iframe AX node's ``backend_dom_node_id`` — a stable identity key
    — instead of the positional iterator ``walk`` used to consume. Entries
    with no owner id (should not happen in practice; defensive only) are
    dropped rather than colliding on a ``None`` key."""
    return {
        fc.owner_backend_node_id: fc
        for fc in frame_children
        if fc.owner_backend_node_id is not None
    }


def _truncate(text: str) -> str:
    """Truncate a name/text string at TEXT_TRUNCATE_CHARS, marking cuts with '…'."""
    if len(text) > TEXT_TRUNCATE_CHARS:
        return text[:TEXT_TRUNCATE_CHARS] + "…"
    return text


def _render_states(node: "AxNode") -> list[str]:
    """Render sparse state tags in the fixed order required by spec section 2."""
    states: list[str] = []
    if node.disabled:
        states.append("[disabled]")
    if node.checked == "mixed":
        states.append("[checked=mixed]")
    elif node.checked is True:
        states.append("[checked]")
    elif node.checked is False:
        # Two-sided on purpose: an empty box is a FACT the reader acts on, and
        # it cannot be carried by omission — absence would be indistinguishable
        # from a non-checkable element. `None` (no tri-state at all) stays
        # silent, which is what keeps this tag meaningful.
        states.append("[unchecked]")
    if node.expanded is True:
        states.append("[expanded]")
    elif node.expanded is False:
        states.append("[collapsed]")
    if node.selected:
        states.append("[selected]")
    if node.pressed == "mixed":
        states.append("[pressed=mixed]")
    elif node.pressed is True:
        states.append("[pressed]")
    elif node.pressed is False:
        states.append("[unpressed]")
    if node.focused:
        states.append("[focused]")
    if node.required:
        states.append("[required]")
    if node.readonly:
        states.append("[readonly]")
    return states


def _render_line(ref: str, depth: int, role: str, node: "AxNode") -> str:
    """Render one doc line for an already-normalized (non-skipped) role."""
    gap = " " * (_BASE_GAP + _INDENT_PER_DEPTH * depth)
    name = _truncate(node.name or "")
    extras = _render_states(node)

    if role == "heading" and node.level is not None:
        extras.append(f"level={node.level}")
    elif node.url:
        extras.append(f"url={node.url}")

    if node.value:
        extras.append(f"{{value={_truncate(node.value)}}}")

    line = f'{ref}{gap}{role} "{name}"'
    if extras:
        line += " " + " ".join(extras)
    return line


def serialize_ax_tree(
    root: "AxNode",
    frame_children: list["FrameCapture"] | None = None,
) -> tuple[str, dict[str, dict]]:
    """Serialize an accessibility tree into a greppable text doc + ref table.

    Args:
        root: The tree to walk (main frame, or a captured frame's own root
            when this function recurses into a merge — callers always pass
            the top-level/main tree here).
        frame_children: Ordered ``FrameCapture`` list for iframes directly
            owned by ``root``'s tree. ``None`` or ``[]``
            reproduces today's single-tree output exactly — no frame
            markers, and every ref_table entry's ``frame_id`` is ``""``.

    Returns:
        (doc, ref_table)
        doc: one line per node, format
            'e<N>   <2*depth spaces><role> "<name>"[ states][ url=…|level=…][ {value=…}]'
            An ``iframe`` node with a merged/noted frame gains a trailing
            ``[frame f<N>]`` marker; that frame's own content (or a
            bracketed note) is inlined directly beneath, one indent level
            deeper.
        ref_table: {'e<N>': {'backend_dom_node_id': int|None, 'role': str,
            'name': str, 'frame_id': str}}. ``frame_id`` is ``""`` for the
            main frame — absent/empty both mean "main frame",
            for backward compatibility with any reader that predates this
            field.

    Rendering rules (spec section 2, + frame-merge rules below):
        - Structural container roles ({"none", "generic", "rootwebarea",
          "webarea", "inlinetextbox"}) and role-less nodes are skipped, but
          their children are recursed into at the *same* depth.
        - State tags render sparsely, in a fixed order: disabled, checked,
          unchecked, checked=mixed, expanded, collapsed, selected, pressed,
          unpressed, pressed=mixed, focused, required, readonly. ``pressed``
          mirrors ``checked``'s tri-state: ARIA toggle buttons support
          ``aria-pressed="mixed"`` same as checkboxes do.
        - The tri-states (``checked``/``pressed``) are the exception to sparse
          rendering: they render BOTH ways, because "the box is empty" is a
          fact a reader acts on and omission cannot express it — an absent tag
          would be indistinguishable from an element with no tick state at all.
          ``None`` still renders nothing, which is what keeps the off-tag
          meaningful. (Values arrive from CDP as the strings "true"/"false"/
          "mixed" and are normalized to True/False/"mixed" by
          ``accessibility._normalize_tristate`` before reaching here.)
        - ``heading`` nodes render ``level=<n>`` when they expose a level.
        - Name/text is truncated at TEXT_TRUNCATE_CHARS with a trailing '…'.
        - Every emitted node gets a ref, assigned sequentially in document
          order starting at e1, shared globally across every merged frame
          (one continuous ref space). Refs are per-step only (see
          module docstring).
        - The doc is hard-capped at AX_DOC_MAX_CHARS (shared globally, the
          ONLY size guard on this output — this doc is state, not a
          prompt); once the cap would be exceeded the whole walk stops and
          the doc ends with a truncation marker line. Nodes past the cap
          get no ref and no ref_table entry. A frame's own content is no
          longer separately truncated (the per-frame line budget was
          removed — see module docstring).
        - A frame whose capture was skipped/failed renders
          ``[frame f<N> hidden — not captured]``,
          ``[frame f<N> not captured — depth exceeds <FRAME_DEPTH_BACKSTOP>]``
          (the pathology backstop from ``frame_capture.py``, interpolated —
          never a hardcoded literal), or ``[frame f<N> capture failed]``
          instead of content. ``<N>`` is minted here, during this walk, in
          document order (see "Deterministic frame numbering" above) — NOT
          carried in from ``FrameCapture``.
    """
    lines: list[str] = []
    ref_table: dict[str, dict] = {}
    state = {"ref": 0, "length": 0, "truncated": False, "frame_num": 0}

    def append_line(line: str) -> bool:
        """Append honoring the global char cap; False means the cap was
        just hit and the caller must stop (state['truncated'] is set)."""
        added_len = len(line) + (1 if lines else 0)  # +1 for the joining newline
        char_budget = AX_DOC_MAX_CHARS - len(_TRUNCATION_MARKER) - 1
        if state["length"] + added_len > char_budget:
            state["truncated"] = True
            return False
        lines.append(line)
        state["length"] += added_len
        return True

    def render_frame(fc: "FrameCapture", depth: int, frame_num: int) -> None:
        """Render one FrameCapture's marker/content at ``depth``.

        ``frame_num`` is the display number the caller already minted (in
        ``walk``, during this same document-order pass) for this exact
        merge candidate — never read off ``fc`` itself (see "Deterministic
        frame numbering" in the module docstring)."""
        gap = " " * (_BASE_GAP + _INDENT_PER_DEPTH * depth)
        if fc.status == "unresolved":
            append_line(f"{gap}[frame ? unresolved — not captured]")
            return
        if fc.status == "hidden":
            append_line(f"{gap}[frame f{frame_num} hidden — not captured]")
            return
        if fc.status == "depth_exceeded":
            append_line(
                f"{gap}[frame f{frame_num} not captured — "
                f"depth exceeds {FRAME_DEPTH_BACKSTOP}]"
            )
            return
        if fc.status != "captured" or fc.tree is None:
            append_line(f"{gap}[frame f{frame_num} capture failed]")
            return

        children_by_owner = _index_by_owner(fc.children)
        walk(fc.tree, depth, fc.frame_id, children_by_owner)

    def walk(
        node: "AxNode",
        depth: int,
        frame_id: str,
        frame_children_by_owner: dict[int, "FrameCapture"],
    ) -> None:
        if state["truncated"]:
            return

        role = (node.role or "").strip().lower()
        if not role or role in _SKIP_ROLES:
            for child in node.children:
                walk(child, depth, frame_id, frame_children_by_owner)
                if state["truncated"]:
                    return
            return

        state["ref"] += 1
        ref = f"e{state['ref']}"
        # Matched by the iframe node's OWN backend_dom_node_id
        # (a stable identity), never by consuming an iterator positionally.
        fc = (
            frame_children_by_owner.get(node.backend_dom_node_id)
            if role == FRAME_ROLE
            else None
        )

        # The display number is minted HERE, in
        # this document-order walk — never read off `fc` (see module
        # docstring "Deterministic frame numbering"). Incremented for every
        # merge candidate encountered, matched or unresolved, so numbering
        # stays stable/contiguous across statuses exactly as before.
        frame_num = 0
        if fc is not None:
            state["frame_num"] += 1
            frame_num = state["frame_num"]

        line = _render_line(ref, depth, role, node)
        if fc is not None:
            line += " [frame ?]" if fc.status == "unresolved" else f" [frame f{frame_num}]"

        if not append_line(line):
            return

        ref_table[ref] = {
            "backend_dom_node_id": node.backend_dom_node_id,
            "role": role,
            # Stripped at the source: downstream locator-enrichment
            # comparisons strip the name before comparing against the DOM's
            # accessible name, so storing it unstripped here caused a
            # raw-vs-stripped mismatch — fix it at the root instead of on
            # the comparison side.
            "name": (node.name or "").strip(),
            "frame_id": frame_id,
        }

        if fc is not None:
            render_frame(fc, depth + 1, frame_num)
            if state["truncated"]:
                return

        for child in node.children:
            walk(child, depth + 1, frame_id, frame_children_by_owner)
            if state["truncated"]:
                return

    walk(root, 0, "", _index_by_owner(frame_children or []))

    doc = "\n".join(lines)
    if state["truncated"]:
        doc = f"{doc}\n{_TRUNCATION_MARKER}" if doc else _TRUNCATION_MARKER

    return doc, ref_table
