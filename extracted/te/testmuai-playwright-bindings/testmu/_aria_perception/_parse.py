"""Parse Playwright's AI snapshot text into the Chrome-path data structures.

The output is the same ``AxNode`` tree + ``FrameForest`` the CDP capture
produces, so ``serialize_ax_tree`` / ``build_structured_dom`` run unchanged.
Roles and states are normalised to Chrome's spellings:

- role: lowercased ARIA role; ``- text: X`` -> ``statictext``; ``img`` -> ``image``.
- states: ``[checked]``, ``[checked=mixed]``, ``[disabled]``, ``[expanded]``,
  ``[selected]``, ``[pressed]``, ``[pressed=mixed]``, ``[level=N]``,
  ``[active]`` (-> focused), ``[cursor=pointer]`` (kept; the capture marks
  the node clickable as the CDP capture does).
- tri-state roles with no ``[checked]`` get ``checked=False``; a combobox
  with no ``[expanded]`` gets ``expanded=False`` (Chrome's ``[collapsed]``).
- ``- /url: X`` -> ``url``; a single text child of a value role -> ``value``;
  a native select's value is its ``[selected]`` option; a childless
  name-from-content node (heading, link, button, ...) regains the static-text
  child Chrome exposes for its name.
- ref-less nodes borrow a handle: the first ref'd descendant for element
  nodes (e.g. a covered link whose image carries the ref), else the nearest
  ref'd ancestor (text lines).
- a ref-less option of a native select (a ref'd combobox/listbox) gets its
  own option handle: the select's ref + its position among the options
  (``_refs.option_handle``), so the model can act on it.
- ``- iframe [ref=eK]:`` with children becomes a ``FrameCapture`` owned by
  the iframe's handle; its content leaves the main tree.

The snapshot is line-oriented YAML-ish; it is parsed by indentation with a
regex (no YAML library: quoted names contain colons). All imports of other
testmu modules are lazy to keep this package cycle-free.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from ._refs import aria_ref_to_handle, frame_id_for_ref, option_handle

if TYPE_CHECKING:
    from ._types import ModeTypes

_LINE_RE = re.compile(
    r'^(\s*)- (?:(text): (.*)|/(\w+): (.*)|([a-z][a-z-]*)(?: "((?:[^"\\]|\\.)*)")?'
    r'((?: \[[^\]]+\])*)(?::\s*(.*))?)$'
)
_ATTR_RE = re.compile(r"\[([^\]=]+)(?:=([^\]]*))?\]")

_ROLE_MAP = {"img": "image", "text": "statictext"}
_TRISTATE_ROLES = frozenset({"checkbox", "radio", "switch", "menuitemcheckbox", "menuitemradio"})
_VALUE_ROLES = frozenset({"textbox", "searchbox", "combobox", "spinbutton", "slider"})
_TEXT_ROLE = "statictext"
# Roles Chrome names from their content and then also exposes that content as
# a static-text child; Playwright folds the text into the name, so a
# childless node of these roles gets the text line back.
_NAME_FROM_CONTENT_ROLES = frozenset({
    "heading", "link", "button", "cell", "gridcell", "columnheader", "rowheader", "tab",
    "menuitem", "menuitemcheckbox", "menuitemradio", "treeitem", "tooltip",
})
_FRAME_ROLE = "iframe"


@dataclass
class ParsedSnapshot:
    forest: Any                      # the mode's FrameForest
    nodes_by_handle: dict[int, "AxNode"] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Scalar decoding
# ---------------------------------------------------------------------------

_VALUE_ESCAPES = {"\\": "\\", '"': '"', "b": "\b", "f": "\f", "n": "\n", "r": "\r", "t": "\t", "/": "/"}


def _decode_value(raw: str) -> str:
    """Decode a YAML scalar as Playwright writes it (``yamlEscapeValueIfNeeded``:
    plain, or double-quoted with JSON-ish escapes plus ``\\xNN``)."""
    s = raw.strip()
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        body, out, i = s[1:-1], [], 0
        while i < len(body):
            c = body[i]
            if c == "\\" and i + 1 < len(body):
                n = body[i + 1]
                if n == "x" and re.match(r"[0-9a-fA-F]{2}", body[i + 2:i + 4]):
                    out.append(chr(int(body[i + 2:i + 4], 16)))
                    i += 4
                    continue
                if n == "u" and re.match(r"[0-9a-fA-F]{4}", body[i + 2:i + 6]):
                    out.append(chr(int(body[i + 2:i + 6], 16)))
                    i += 6
                    continue
                out.append(_VALUE_ESCAPES.get(n, n))
                i += 2
                continue
            out.append(c)
            i += 1
        return "".join(out)
    if len(s) >= 2 and s[0] == "'" and s[-1] == "'":
        return s[1:-1].replace("''", "'")
    return s


def _decode_name(raw: str) -> str:
    try:
        return json.loads('"' + raw + '"')
    except ValueError:
        return raw


def _unquote_key(content: str) -> str:
    """Undo ``yamlEscapeKeyIfNeeded``: a key needing quotes is written as
    ``'...'`` with ``''`` for a literal quote, optionally followed by
    ``: value`` or ``:``."""
    if not content.startswith("'"):
        return content
    i = 1
    while i < len(content):
        if content[i] == "'":
            if i + 1 < len(content) and content[i + 1] == "'":
                i += 2
                continue
            return content[1:i].replace("''", "'") + content[i + 1:]
        i += 1
    return content


# ---------------------------------------------------------------------------
# Tree building
# ---------------------------------------------------------------------------

def _new_node(types: "ModeTypes", role: str, name: str = "") -> "AxNode":
    node = types.AxNode(role=role, name=name)
    node.aria_ref = None
    node.frame_id = ""
    node.cursor_pointer = False
    node._inline_text = None  # single inline text child, resolved in _normalise
    return node


def _apply_attrs(node: "AxNode", attrs: str) -> None:
    for key, val in _ATTR_RE.findall(attrs or ""):
        key = key.strip()
        if key == "ref":
            node.aria_ref = val.strip()
        elif key == "checked":
            node.checked = "mixed" if val == "mixed" else True
        elif key == "pressed":
            node.pressed = "mixed" if val == "mixed" else True
        elif key == "disabled":
            node.disabled = True
        elif key == "expanded":
            node.expanded = True
        elif key == "selected":
            node.selected = True
        elif key == "active":
            node.focused = True
        elif key == "level":
            try:
                node.level = int(val)
            except ValueError:
                pass
        elif key == "cursor":
            node.cursor_pointer = val == "pointer"


def _build_tree(text: str, types: "ModeTypes") -> "AxNode":
    root = _new_node(types, "rootwebarea")
    stack: list[tuple[int, "AxNode"]] = [(-1, root)]
    for raw_line in text.splitlines():
        if not raw_line.strip():
            continue
        stripped = raw_line.lstrip(" ")
        indent = len(raw_line) - len(stripped)
        if not stripped.startswith("- "):
            continue
        line = " " * indent + "- " + _unquote_key(stripped[2:])
        m = _LINE_RE.match(line)
        if not m:
            continue
        while stack and stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1] if stack else root
        (_, text_kw, text_val, prop_key, prop_val, role, name, attrs, inline) = m.groups()
        if text_kw:
            node = _new_node(types, _TEXT_ROLE, _decode_value(text_val))
            parent.children.append(node)
            continue
        if prop_key:
            if prop_key == "url":
                parent.url = _decode_value(prop_val)
            continue
        node = _new_node(types, _ROLE_MAP.get(role, role), _decode_name(name) if name else "")
        _apply_attrs(node, attrs)
        if inline is not None and inline.strip() != "":
            node._inline_text = _decode_value(inline)
        parent.children.append(node)
        stack.append((indent, node))
    return root


def _normalise(node: "AxNode", types: "ModeTypes") -> None:
    """The value/state rules above, bottom-up."""
    for child in node.children:
        _normalise(child, types)
    role = node.role
    inline = node._inline_text
    if role in _VALUE_ROLES:
        if inline is not None:
            node.value = inline
        elif (
            len(node.children) == 1
            and node.children[0].role == _TEXT_ROLE
            and not node.children[0].children
        ):
            node.value = node.children[0].name
            node.children = []
    elif inline is not None:
        node.children.insert(0, _new_node(types, _TEXT_ROLE, inline))
    elif role in _NAME_FROM_CONTENT_ROLES and node.name and not node.children:
        node.children.append(_new_node(types, _TEXT_ROLE, node.name))
    if role == "combobox":
        if not node.value:
            for child in node.children:
                if child.role == "option" and child.selected:
                    node.value = child.name
                    break
        if node.expanded is None:
            node.expanded = False
    if role in _TRISTATE_ROLES and node.checked is None:
        node.checked = False
    # A named generic would vanish (the serializer skips generic): keep its
    # name greppable as a text line owned by the same element.
    if role == "generic" and node.name and not any(
        c.role == _TEXT_ROLE and c.name == node.name for c in node.children
    ):
        node.children.insert(0, _new_node(types, _TEXT_ROLE, node.name))
    node._inline_text = None


def _first_descendant_ref(node: "AxNode") -> str | None:
    for child in node.children:
        if child.aria_ref:
            return child.aria_ref
        found = _first_descendant_ref(child)
        if found:
            return found
    return None


def _assign_handles(node: "AxNode", inherited: str | None, nodes_by_handle: dict[int, "AxNode"]) -> None:
    ref = node.aria_ref
    if ref:
        try:
            handle = aria_ref_to_handle(ref)
        except ValueError:
            handle = None
        if handle is not None:
            nodes_by_handle[handle] = node
        borrowed = ref
    elif node.role in (_TEXT_ROLE, "option", "rootwebarea"):
        borrowed = inherited
    else:
        borrowed = _first_descendant_ref(node) or inherited
    if borrowed:
        try:
            node.backend_dom_node_id = aria_ref_to_handle(borrowed)
        except ValueError:
            node.backend_dom_node_id = None
        node.frame_id = frame_id_for_ref(borrowed)
    for child in node.children:
        _assign_handles(child, borrowed, nodes_by_handle)


_SELECT_ROLES = frozenset({"combobox", "listbox"})


def _assign_option_handles(node: "AxNode", nodes_by_handle: dict[int, "AxNode"]) -> None:
    """Option handles for the ref-less options of each ref'd combobox/listbox
    (a native select: its options have no ref). Options are numbered in tree
    order, which is ``role=option`` order (hidden options are left out;
    optgroups flatten to a text line). Nodes under another ref'd element are not the select's options."""
    if node.aria_ref and node.role in _SELECT_ROLES:
        options: list["AxNode"] = []

        def collect(n: "AxNode") -> None:
            for child in n.children:
                if child.aria_ref:
                    continue
                if child.role == "option":
                    options.append(child)
                collect(child)

        collect(node)
        for index, opt in enumerate(options):
            try:
                handle = option_handle(node.aria_ref, index)
            except ValueError:
                handle = None
            if handle is None:
                continue
            opt.backend_dom_node_id = handle
            nodes_by_handle[handle] = opt
    for child in node.children:
        _assign_option_handles(child, nodes_by_handle)


def _frame_id_of_content(node: "AxNode") -> str:
    """The ``f<seq>`` prefix of the first ref inside a frame's own content
    (not inside a nested frame)."""
    for child in node.children:
        if child.aria_ref:
            fid = frame_id_for_ref(child.aria_ref)
            if fid:
                return fid
        if child.role != _FRAME_ROLE:
            fid = _frame_id_of_content(child)
            if fid:
                return fid
    return ""


def _extract_frames(tree: "AxNode", types: "ModeTypes") -> list:
    """Detach every ``iframe`` node's inlined content into a FrameCapture
    (recursively), leaving the iframe line childless as on Chrome."""
    captures: list = []

    def walk(node: "AxNode") -> None:
        for child in node.children:
            if child.role == _FRAME_ROLE and child.children:
                frame_root = _new_node(types, "rootwebarea")
                frame_root.children = child.children
                child.children = []
                frame_root.frame_id = _frame_id_of_content(frame_root)
                frame_root.backend_dom_node_id = child.backend_dom_node_id
                captures.append(types.FrameCapture(
                    frame_id=frame_root.frame_id,
                    status="captured",
                    tree=frame_root,
                    children=_extract_frames(frame_root, types),
                    owner_backend_node_id=child.backend_dom_node_id,
                ))
            else:
                walk(child)

    walk(tree)
    return captures


def parse_ai_snapshot(text: str, types: "ModeTypes") -> ParsedSnapshot:
    """Parse ``snapshot_for_ai`` text into a ``FrameForest`` of ``AxNode``s.

    ``AxNode.backend_dom_node_id`` is the portable handle; every node also
    carries ``aria_ref`` (its own ref or None), ``frame_id`` and
    ``cursor_pointer``. The root is a synthetic ``rootwebarea`` (skipped by
    the serializer). ``nodes_by_handle`` maps each ref'd node's handle to it.
    """
    root = _build_tree(text or "", types)
    _normalise(root, types)
    nodes_by_handle: dict[int, Any] = {}
    _assign_handles(root, None, nodes_by_handle)
    _assign_option_handles(root, nodes_by_handle)
    if not root.children:
        return ParsedSnapshot(forest=types.FrameForest(main_tree=None), nodes_by_handle={})
    captures = _extract_frames(root, types)
    return ParsedSnapshot(
        forest=types.FrameForest(main_tree=root, frame_captures=captures),
        nodes_by_handle=nodes_by_handle,
    )


def reattach_frames(tree: "AxNode", captures: list) -> "AxNode":
    """Put each captured frame's content back under its iframe node (for
    builders that want one tree: flat/structured DOM). Mutates ``tree``."""
    by_owner = {fc.owner_backend_node_id: fc for fc in captures if fc.owner_backend_node_id is not None}

    def walk(node: "AxNode", level: dict) -> None:
        for child in node.children:
            if child.role == _FRAME_ROLE and child.backend_dom_node_id in level:
                fc = level.pop(child.backend_dom_node_id)
                if fc.tree is not None:
                    child.children = list(fc.tree.children)
                    nested = {c.owner_backend_node_id: c for c in fc.children if c.owner_backend_node_id is not None}
                    walk(child, nested)
                continue
            walk(child, level)

    walk(tree, by_owner)
    return tree
