"""Parse uiautomator2 page-source XML into a flat, indexed, LLM-ready element list."""

import re
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import dataclass

BOUNDS_RE = re.compile(r"\[(-?\d+),(-?\d+)\]\[(-?\d+),(-?\d+)\]")

#: Characters XML forbids outright. A page source carries whatever an app put in a
#: label, and an app can put a raw control character there; the document is then
#: not parseable and the whole capture fails on somebody else's stray byte.
ILLEGAL_XML = re.compile(
    "[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x84\x86-\x9f\ufdd0-\ufddf\ufffe\uffff]")

#: The driver's own word for "the user can see this". uiautomator2 spells it
#: `displayed`; other producers spell it `visible-to-user`. Both are honoured, and
#: only an explicit false is acted on — an absent attribute says nothing.
VISIBILITY_ATTRS = ("displayed", "visible-to-user")

ROLE_MAP = [
    ("EditText", "input"),
    ("AutoCompleteTextView", "input"),
    ("Switch", "switch"),
    ("CheckBox", "checkbox"),
    ("RadioButton", "radio"),
    ("SeekBar", "slider"),
    ("NumberPicker", "picker"),
    ("Spinner", "dropdown"),
    ("ImageButton", "button"),
    ("Button", "button"),
    ("ToggleButton", "button"),
    ("ImageView", "image"),
    ("TextView", "text"),
    ("WebView", "webview"),
]

#: Widgets driven by touch that need not advertise it. A custom control handling
#: raw touch events — a seekbar, a rating strip, a signature pad, a map — leaves
#: `clickable="false"` in the dump, so the flags alone never see it and the model
#: is not told the control is there.
TOUCH_SURFACE_CLASSES = (
    "SeekBar", "RatingBar", "SurfaceView", "TextureView", "GLSurfaceView",
    "MapView", "VideoView",
)

#: How much of the screen an unlabelled clickable has to cover before it is a
#: backdrop rather than a target: the transparent sheet a dialog puts behind
#: itself to catch taps that dismiss it.
BACKDROP_AREA_FRACTION = 0.9

#: Name folding (P4). A clickable row's label is assembled from its
#: non-interactive descendants; without limits an outer container swallows a
#: whole screen ("Suggestions · How suggestions work · Learn more · …") and the
#: reasoning model can no longer tell rows apart.
MAX_NAME_FRAGMENTS = 3
MAX_NAME_LEN = 80
FRAGMENT_SEPARATOR = " · "


@dataclass(frozen=True)
class _ElementField:
    value_type: type | tuple[type, ...]
    meaning: str


# The neutral row contract every platform parser must produce. Consumers may
# reason from these fields without knowing which accessibility vocabulary
# supplied them.
ELEMENT_CONTRACT = {
    "index": _ElementField(int, "one-based document-order index"),
    "role": _ElementField(str, "platform-neutral semantic role"),
    "name": _ElementField(str, "searchable semantic label"),
    "visual_name": _ElementField(str, "legacy visual-mode label"),
    "bounds": _ElementField(tuple, "device-pixel x1, y1, x2, y2 bounds"),
    "center": _ElementField(tuple, "device-pixel center"),
    "states": _ElementField(list, "platform-neutral state names"),
    "affordances": _ElementField(list, "extra supported interactions"),
    "scrollable": _ElementField(bool, "whether the element can scroll"),
    "scroll_axis": _ElementField((str, type(None)), "horizontal, vertical, or unknown"),
    "interactive": _ElementField(bool, "whether visual mode may target the row"),
    "editable": _ElementField(bool, "whether the row accepts typed text"),
    "raw_child_count": _ElementField(
        int, "number of direct children in the producer-native tree"),
    "depth": _ElementField(int, "depth among emitted rows"),
    "cls": _ElementField(str, "producer-native class retained for diagnostics"),
    "package": _ElementField(str, "application or window owner"),
    "resource_id": _ElementField(str, "developer-assigned native identifier"),
    "content_desc": _ElementField(str, "raw accessibility description"),
    "text": _ElementField(str, "raw non-secret text"),
    "hint": _ElementField(str, "raw placeholder or hint"),
    "showing_hint": _ElementField(bool, "whether text currently represents the hint"),
    "position": _ElementField(str, "coarse screen position"),
    "anchors": _ElementField(dict, "screen-unique relational labels"),
    # A row is emitted for a node the parser ADMITS; the driver queries every node
    # the document has. Counting a selector's uniqueness over the returned rows
    # therefore answers a different question than the one execution asks, and
    # answers it optimistically. This field carries the driver's answer: for each
    # ROW FIELD a selector compiles from, how many elements the query built from
    # that field would return across the whole document. Keys are row-field names
    # (plus compound keys such as `resource_id+text` for a strategy that pins two),
    # so a consumer already counting a field over its rows can ask the same
    # question of the document without knowing the producer's query dialect.
    #
    # Empty is a valid answer and means "this producer publishes no counts" — the
    # consumer keeps its own. Take the LARGER of the two: a strategy either source
    # calls ambiguous is ambiguous, and a count can only ever be missing evidence,
    # never fabricate it.
    "query_matches": _ElementField(dict, "elements each field's query would match"),
    # Additive producer metadata. These fields preserve information already in
    # UiAutomator2's XML without changing the long-standing role/name/state and
    # selector fields above. Transient source coordinates are for reasoning and
    # diagnostics only; they are never durable locator identity.
    "source_index": _ElementField((int, type(None)), "producer-native sibling index"),
    "source_path": _ElementField(tuple, "producer-native ordinal path from the root"),
    "parent_index": _ElementField(
        (int, type(None)), "nearest emitted parent row index"),
    "displayed": _ElementField((bool, type(None)), "producer visibility flag"),
    "clickable": _ElementField((bool, type(None)), "producer click capability flag"),
    "checkable": _ElementField((bool, type(None)), "producer toggle capability flag"),
    "checked": _ElementField((bool, type(None)), "producer checked value"),
    "enabled": _ElementField((bool, type(None)), "producer enabled value"),
    "focusable": _ElementField((bool, type(None)), "producer focus capability flag"),
    "focused": _ElementField((bool, type(None)), "producer input-focus value"),
    "long_clickable": _ElementField(
        (bool, type(None)), "producer long-click capability flag"),
    "context_clickable": _ElementField(
        (bool, type(None)), "producer context-click capability flag"),
    "selected": _ElementField((bool, type(None)), "producer selected value"),
    "dismissable": _ElementField((bool, type(None)), "whether the node can dismiss"),
    "accessibility_focused": _ElementField(
        (bool, type(None)), "producer accessibility-focus value"),
    "a11y_important": _ElementField(
        (bool, type(None)), "whether the producer marks the node accessibility-important"),
    "screen_reader_focusable": _ElementField(
        (bool, type(None)), "whether a screen reader treats the node as one unit"),
    "input_type": _ElementField((int, type(None)), "raw Android input-type bitmask"),
    "input_kind": _ElementField((str, type(None)), "normalized input purpose"),
    "multiline": _ElementField((bool, type(None)), "whether the input accepts newlines"),
    "max_text_length": _ElementField(
        (int, type(None)), "producer maximum editable text length"),
    "selection_start": _ElementField(
        (int, type(None)), "current editable selection start"),
    "selection_end": _ElementField((int, type(None)), "current editable selection end"),
    "content_invalid": _ElementField(
        (bool, type(None)), "producer validation-invalid flag"),
    "error_text": _ElementField(str, "producer validation error text"),
    "pane_title": _ElementField(str, "accessibility pane title"),
    "tooltip_text": _ElementField(str, "accessibility tooltip text"),
    "heading": _ElementField((bool, type(None)), "accessibility heading flag"),
    "text_entry_key": _ElementField(
        (bool, type(None)), "whether the node is a software text-entry key"),
    "text_has_clickable_span": _ElementField(
        (bool, type(None)), "whether text contains an inline clickable span"),
    "live_region": _ElementField((int, type(None)), "Android live-region mode"),
    "window_id": _ElementField((int, type(None)), "accessibility window identifier"),
    "drawing_order": _ElementField(
        (int, type(None)), "producer sibling drawing order"),
    "accessibility_actions": _ElementField(
        list, "raw accessibility action names published by UiAutomator2"),
    "capabilities": _ElementField(list, "normalized supported interactions"),
    "semantic_traits": _ElementField(list, "additional semantics without replacing role"),
    "role_description": _ElementField(str, "allowlisted accessibility role description"),
    "html_role": _ElementField(str, "allowlisted projected web role"),
}


#: Row field → the XML attribute the compiled clause compares against.
#: `resourceId`, ACCESSIBILITY_ID and `.text()` are three independent clauses, so
#: each is counted on its own. A producer whose text strategy compiles to an OR
#: across several attributes has to count NODES instead, or a node answering on
#: two of them reads as two elements.
_QUERY_FIELDS = {"resource_id": "resource-id",
                 "content_desc": "content-desc",
                 "text": "text"}


def _optional_bool(attrs, key):
    """A producer boolean while preserving absence as unknown."""
    if key not in attrs:
        return None
    raw = str(attrs.get(key)).lower()
    if raw == "true":
        return True
    if raw == "false":
        return False
    return None


def _optional_int(attrs, key):
    """A producer integer, or None for an absent/malformed value."""
    raw = attrs.get(key)
    if raw in (None, ""):
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def _optional_nonnegative_int(attrs, key):
    value = _optional_int(attrs, key)
    return value if value is not None and value >= 0 else None


# Android InputType masks. The raw bitmask is retained separately; this is only
# the compact, platform-neutral purpose useful to a reasoning model.
_INPUT_CLASS_MASK = 0x0000000F
_INPUT_VARIATION_MASK = 0x00000FF0
_INPUT_CLASS_TEXT = 0x00000001
_INPUT_CLASS_NUMBER = 0x00000002
_INPUT_CLASS_PHONE = 0x00000003
_INPUT_CLASS_DATETIME = 0x00000004


def _input_kind(input_type):
    if input_type is None:
        return None
    input_class = input_type & _INPUT_CLASS_MASK
    variation = input_type & _INPUT_VARIATION_MASK
    if input_class == _INPUT_CLASS_TEXT:
        return {
            0x00000010: "url",
            0x00000020: "email",
            0x00000080: "password",
            0x00000090: "password",
            0x000000B0: "search",
            0x000000D0: "email",
            0x000000E0: "password",
        }.get(variation, "text")
    if input_class == _INPUT_CLASS_NUMBER:
        if variation == 0x00000010:
            return "password"
        return "decimal" if input_type & 0x00002000 else "number"
    if input_class == _INPUT_CLASS_PHONE:
        return "phone"
    if input_class == _INPUT_CLASS_DATETIME:
        return {0x00000010: "date", 0x00000020: "time"}.get(
            variation, "datetime")
    return None


_ACTION_CAPABILITIES = {
    "ACTION_CLICK": "activate",
    "ACTION_LONG_CLICK": "long-press",
    "ACTION_FOCUS": "focus",
    "ACTION_CLEAR_FOCUS": "clear-focus",
    "ACTION_ACCESSIBILITY_FOCUS": "accessibility-focus",
    "ACTION_CLEAR_ACCESSIBILITY_FOCUS": "clear-accessibility-focus",
    "ACTION_SELECT": "select",
    "ACTION_CLEAR_SELECTION": "clear-selection",
    "ACTION_SET_TEXT": "set-text",
    "ACTION_SET_SELECTION": "set-selection",
    "ACTION_SET_PROGRESS": "set-progress",
    "ACTION_SCROLL_FORWARD": "scroll-forward",
    "ACTION_SCROLL_BACKWARD": "scroll-backward",
    "ACTION_SCROLL_UP": "scroll-up",
    "ACTION_SCROLL_DOWN": "scroll-down",
    "ACTION_SCROLL_LEFT": "scroll-left",
    "ACTION_SCROLL_RIGHT": "scroll-right",
    "ACTION_SCROLL_TO_POSITION": "scroll-to-position",
    "ACTION_SCROLL_IN_DIRECTION": "scroll-in-direction",
    "ACTION_PAGE_UP": "page-up",
    "ACTION_PAGE_DOWN": "page-down",
    "ACTION_PAGE_LEFT": "page-left",
    "ACTION_PAGE_RIGHT": "page-right",
    "ACTION_EXPAND": "expand",
    "ACTION_COLLAPSE": "collapse",
    "ACTION_DISMISS": "dismiss",
    "ACTION_SHOW_ON_SCREEN": "show-on-screen",
    "ACTION_NEXT_AT_MOVEMENT_GRANULARITY": "next-text-unit",
    "ACTION_PREVIOUS_AT_MOVEMENT_GRANULARITY": "previous-text-unit",
    "ACTION_NEXT_HTML_ELEMENT": "next-html-element",
    "ACTION_PREVIOUS_HTML_ELEMENT": "previous-html-element",
    "ACTION_COPY": "copy",
    "ACTION_CUT": "cut",
    "ACTION_PASTE": "paste",
    "ACTION_CONTEXT_CLICK": "context-click",
    "ACTION_MOVE_WINDOW": "move-window",
    "ACTION_SHOW_TOOLTIP": "show-tooltip",
    "ACTION_HIDE_TOOLTIP": "hide-tooltip",
    "ACTION_PRESS_AND_HOLD": "press-and-hold",
    "ACTION_IME_ENTER": "ime-enter",
    "ACTION_DRAG_START": "drag-start",
    "ACTION_DRAG_DROP": "drag-drop",
    "ACTION_DRAG_CANCEL": "drag-cancel",
    "ACTION_SHOW_TEXT_SUGGESTIONS": "show-text-suggestions",
}


def _accessibility_actions(attrs):
    return [
        action.strip()
        for action in (attrs.get("actions") or "").split(",")
        if action.strip()
    ]


def _append_once(values, value):
    if value and value not in values:
        values.append(value)


def _normalized_action(action):
    mapped = _ACTION_CAPABILITIES.get(action)
    if mapped:
        return mapped
    if action.startswith("ACTION_"):
        return action[len("ACTION_"):].lower().replace("_", "-")
    return action.lower().replace("_", "-")


def _capabilities_for(attrs, *, editable, actions):
    capabilities = []
    for attr, capability in (
        ("clickable", "activate"),
        ("focusable", "focus"),
        ("long-clickable", "long-press"),
        ("context-clickable", "context-click"),
        ("checkable", "toggle"),
        ("scrollable", "scroll"),
        ("dismissable", "dismiss"),
    ):
        if attrs.get(attr) == "true":
            _append_once(capabilities, capability)
    if editable:
        _append_once(capabilities, "set-text")
    for action in actions:
        _append_once(capabilities, _normalized_action(action))
    return capabilities


def _semantic_traits(attrs):
    traits = []
    for attr, trait in (
        ("heading", "heading"),
        ("text-entry-key", "text-entry-key"),
        ("text-has-clickable-span", "clickable-span"),
    ):
        if attrs.get(attr) == "true":
            traits.append(trait)
    return traits


def _extra_value(attrs, key):
    """One allowlisted value from UiAutomator2's semicolon-packed extras."""
    for entry in (attrs.get("extras") or "").split(";"):
        name, separator, value = entry.partition("=")
        if separator and name.strip() == key:
            return value.strip()
    return ""


def _role_for(cls, attrs):
    for suffix, role in ROLE_MAP:
        if cls.endswith(suffix):
            return role
    if attrs.get("scrollable") == "true":
        return "scrollable"
    return "item"


def _is_hidden(attrs):
    """Whether the driver says the user cannot see this node."""
    return any(attrs.get(attr) == "false" for attr in VISIBILITY_ATTRS)


def _parse_bounds(s):
    m = BOUNDS_RE.match(s or "")
    if not m:
        return None
    x1, y1, x2, y2 = map(int, m.groups())
    if x2 <= x1 or y2 <= y1:
        return None
    return (x1, y1, x2, y2)


#: Widgets whose `text` is the user's own content rather than the widget's name.
EDITABLE_CLASSES = ("EditText", "AutoCompleteTextView")


def _is_editable(attrs):
    return (attrs.get("class") or "").endswith(EDITABLE_CLASSES)


def _holds_a_typed_value(attrs):
    """Whether this node's `text` is what somebody typed into it.

    An empty field reports its placeholder in `text` and says so with
    `showing-hint`; a filled one reports the value and says nothing.
    """
    return _is_editable(attrs) and attrs.get("showing-hint") != "true"


def _label_attrs_for(attrs):
    """Which attributes may name this node, in order of preference.

    A filled field is named by its LABEL, never by its contents. Taking the
    contents renames the element the moment it is typed into, puts whatever was
    typed — an address, a card number — into the prompt, and makes two fields
    holding similar values indistinguishable.
    """
    if _holds_a_typed_value(attrs):
        return _LABEL_ATTRS[1:]
    return _LABEL_ATTRS


def _own_text(attrs):
    """This node's own label, ignoring descendants."""
    for xml_attr, _ in _label_attrs_for(attrs):
        value = (attrs.get(xml_attr) or "").strip()
        if value:
            return value
    return ""


#: XML attribute a label may come from, paired with the selector clause that can
#: match it. Order matches _own_text's preference.
_LABEL_ATTRS = (("text", "text"), ("content-desc", "description"), ("hint", "text"))


def _label_with_source(attrs):
    """(value, clause) for this node's own label; ('', '') when it has none.

    The clause travels with the value because a label matched with the wrong one
    resolves nothing: most toolkits put row labels in content-desc, which
    `.text()` never matches.

    The value is the label as one line, because that is the form everything
    downstream compares it in. Apps pad their labels — `content-desc=" Top picks
    for you"`, `text="    is_resproxy:false"` — and a selector carrying the
    trimmed value while the attribute holds the padded one resolves nothing.
    """
    for xml_attr, clause in _label_attrs_for(attrs):
        value = _clean_label(attrs.get(xml_attr) or "")
        if value:
            return value, clause
    return "", ""


def _labels_under(node):
    """Every (value, clause) inside this subtree, bounded by interaction.

    A node that is a target in its own right ends the descent. Without that
    boundary a card collects the labels of the buttons inside it, and
    `ancestor_of` on one of those resolves the BUTTON — the nearest interactive
    ancestor of that label is the button, not the card. A scroll container
    collects every visible row's label the same way.
    """
    found = []

    def collect(current):
        if _is_interactive(current.attrib):
            return
        value, clause = _label_with_source(current.attrib)
        if value:
            found.append((value, clause))
        for child in current:
            collect(child)

    for child in node:
        collect(child)
    return found


#: How many containers up from a node its identifying label may live. A grid
#: card's product name sits in a different branch of the card from the button
#: inside it — three levels away on the reference app.
MAX_ANCHOR_CLIMB = 5


def _sibling_labels(node, parent_of, is_unique):
    """The labels carried by the subtrees this node shares a container with.

    Climbs rather than reading the direct siblings alone, because a card's own
    title is rarely a direct sibling of the button inside it — on the reference
    shopping grid it sits three containers away.

    Each label carries the number of containers crossed to reach it, so a
    consumer can prefer the nearest one. The climb stops at the first level that
    yields a screen-unique label, below a scroll container, and after
    `MAX_ANCHOR_CLIMB` levels.
    """
    found = []
    current = node
    for level in range(1, MAX_ANCHOR_CLIMB + 1):
        parent = parent_of.get(current)
        if parent is None or parent.get("scrollable") == "true":
            break
        for sibling in parent:
            if sibling is current:
                continue
            value, clause = _label_with_source(sibling.attrib)
            if value:
                found.append((value, clause, level))
            found.extend((v, c, level) for v, c in _labels_under(sibling))
        if any(is_unique(value, clause) for value, clause, _ in found):
            break
        current = parent
    return found


def _collect_texts(node, out, seen):
    """Fold descendant labels into a parent's name.

    Stops descending into any child that gets its own entry in the flat list —
    not only a clickable one, but a switch, a field, a long-press target or a
    WebView. Folding such a child's text into the ancestor duplicates it and
    blurs two targets. Fragments are de-duplicated and capped so one chatty
    container can't dominate the prompt.
    """
    for child in node:
        if len(out) >= MAX_NAME_FRAGMENTS:
            return
        if _is_interactive(child.attrib):
            continue
        text = _own_text(child.attrib)
        key = text.casefold()
        if text and key not in seen:
            seen.add(key)
            out.append(text)
            if len(out) >= MAX_NAME_FRAGMENTS:
                return
        _collect_texts(child, out, seen)


def _fold_name(node):
    fragments = []
    _collect_texts(node, fragments, set())
    return FRAGMENT_SEPARATOR.join(fragments)[:MAX_NAME_LEN]


#: Anything that would break a label out of the line it is rendered on.
_LABEL_WHITESPACE = re.compile(r"[\s\u0085\u2028\u2029]+")

#: Android icon fonts commonly expose their glyphs as private-use characters.
#: They are legal XML, but they are not text a model can search for or reason
#: about, so remove them from every label before folding, anchoring or rendering.
_PRIVATE_USE = re.compile(r"[\ue000-\uf8ff]")
_ORPHANED_ICON_SEPARATOR = re.compile(r"^[\s,;:·|/\\-]+|[\s,;:·|/\\-]+$")


def _clean_label(value):
    """A label as one line of text.

    App-controlled strings are screen content, not part of the format they are
    rendered in: a newline inside one would otherwise start what looks like
    another element's line.
    """
    without_icons = _PRIVATE_USE.sub("", value)
    if without_icons != value:
        without_icons = _ORPHANED_ICON_SEPARATOR.sub("", without_icons)
    return _LABEL_WHITESPACE.sub(" ", without_icons).strip()


def _visual_label(value):
    """Legacy visual-mode label normalization, retaining icon-font glyphs."""
    return _LABEL_WHITESPACE.sub(" ", value).strip()


def position_hint(cx, cy, w, h):
    """The screen cell containing a point, expressed as row-column."""
    col = ["left", "center", "right"][min(2, cx * 3 // max(w, 1))]
    row = ["top", "middle", "bottom"][min(2, cy * 3 // max(h, 1))]
    return f"{row}-{col}"


_position_hint = position_hint


def _is_interactive(a):
    cls = a.get("class") or ""
    return (
        a.get("clickable") == "true"
        or a.get("long-clickable") == "true"
        or a.get("context-clickable") == "true"
        or a.get("checkable") == "true"
        or a.get("scrollable") == "true"
        or a.get("focused") == "true"
        or cls.endswith("EditText")
        # A WebView is rarely interactive itself, but it marks where the native
        # surface ends. Without it nothing downstream can tell that a screen has
        # web content at all, and an unreadable WebView looks like a bare screen.
        or cls.endswith("WebView")
        # A control the user drags rather than taps often sets none of the flags.
        or cls.endswith(TOUCH_SURFACE_CLASSES)
    )


def _has_clickable_descendant(node):
    for child in node:
        if child.get("clickable") == "true" or _has_clickable_descendant(child):
            return True
    return False


def _states_for(attrs):
    states = []
    for attr, value, state in (
        ("checked", "true", "checked"),
        ("enabled", "false", "disabled"),
        ("focused", "true", "focused"),
        ("selected", "true", "selected"),
        ("password", "true", "password"),
    ):
        if attrs.get(attr) == value:
            states.append(state)
    return states


def _affordances_for(attrs):
    """What this node responds to that its role does not already say.

    ``unlabelled`` is uiautomator's own NAF flag: the node takes a touch, is
    enabled, and nothing anywhere beneath it carries text or a description. A
    reader searching for it by name will never find it.
    """
    found = []
    if attrs.get("long-clickable") == "true":
        found.append("long-press")
    if attrs.get("NAF") == "true":
        found.append("unlabelled")
    return found


def _scroll_axis(node, cls, scrollable):
    """The directions a scrollable container can plausibly move.

    UiAutomator exposes only a boolean ``scrollable`` flag. The widget class is
    authoritative where Android has an axis-specific container; grid, recycler,
    and custom implementations are inferred from the arrangement of their
    visible children. An indeterminate container stays unknown instead of
    inventing a direction from its viewport aspect ratio.
    """
    if not scrollable:
        return None
    short_cls = (cls or "").rsplit(".", 1)[-1]
    if "HorizontalScrollView" in short_cls or "ViewPager" in short_cls:
        return "horizontal"
    if short_cls.endswith(("ScrollView", "ListView")):
        return "vertical"
    child_centers = []
    for child in node:
        child_bounds = _parse_bounds(child.attrib.get("bounds", ""))
        if child_bounds:
            x1, y1, x2, y2 = child_bounds
            child_centers.append(((x1 + x2) // 2, (y1 + y2) // 2))
    if len(child_centers) < 2:
        return None
    x_span = max(x for x, _ in child_centers) - min(x for x, _ in child_centers)
    y_span = max(y for _, y in child_centers) - min(y for _, y in child_centers)
    if x_span == y_span == 0:
        return None
    return "horizontal" if x_span > y_span else "vertical"


def parse_tree(xml_str, screen_w, screen_h):
    """Return the viewport's useful nodes in document order, indexed 1-based.

    Raises ValueError when the document cannot be parsed. A page source captured
    mid-transition is sometimes truncated, and that is a transient condition the
    caller can retry — which it cannot do if the parser raises the XML library's
    own error from three frames down.

    A node earns a row when it has a label, a developer id, or responds to
    touch. Pure layout wrappers are skipped and their children are promoted.
    ``interactive`` preserves the old actionable subset for visual-mode callers;
    text mode can assign a ref to every row, including informational content.

    Readable text that once travelled in a second, ungroundable list is now
    represented by ordinary rows in the returned list.
    """
    try:
        root = ET.fromstring(ILLEGAL_XML.sub("", xml_str or ""))
    except ET.ParseError as e:
        raise ValueError(
            f"page source is not parseable ({e}); it was {len(xml_str or '')} "
            f"characters long. A capture taken mid-transition can be truncated."
        ) from e
    elements = []
    parent_of = {child: node for node in root.iter() for child in node}
    #: How often each (clause, value) pair occurs anywhere in the tree. An anchor
    #: has to be unique to name one element, and that is only knowable across the
    #: whole tree. Counting by value alone would reject a `.text("Settings")` that
    #: collides with nothing but a `.description("Settings")` elsewhere.
    label_counts = Counter(
        (clause, value) for clause, value in
        ((c, v) for v, c in (_label_with_source(n.attrib) for n in root.iter()) if v)
    )
    # What the DRIVER would match — counted over every node, exactly as the
    # anchors' `label_counts` above already are, and for the same reason.
    #
    # A node earns a row only if it carries a label, an id or an interaction AND
    # still has drawable area inside the viewport; `find_elements` queries the
    # hierarchy and honours none of that. Chrome projects a web link into the
    # native tree twice, the second copy with zero height: the parser rejects it,
    # the driver returns it. Uniqueness judged on the rows is judged on a set that
    # copy was removed from, and the selector that gets recorded resolves to two
    # elements at replay.
    #
    # Android publishes each of these row fields verbatim from the attribute its
    # clause compares against, so — unlike a folded or trimmed label — the counts
    # line up with the row without any normalisation.
    query_counts = {field: Counter() for field in _QUERY_FIELDS}
    pair_counts = Counter()
    for node in root.iter():
        node_attrs = node.attrib
        for field, xml_attr in _QUERY_FIELDS.items():
            value = node_attrs.get(xml_attr, "")
            if value:
                query_counts[field][value] += 1
        view_id, node_text = (node_attrs.get("resource-id", ""),
                              node_attrs.get("text", ""))
        if view_id and node_text:
            pair_counts[(view_id, node_text)] += 1

    def _query_matches(resource_id, content_desc, text):
        """The driver-side count for each field this row's selectors compile from.

        A field the row does not carry is absent rather than zero: nothing was
        measured, so nothing is claimed, and the consumer keeps its own count.
        """
        matches = {}
        for field, value in (("resource_id", resource_id),
                             ("content_desc", content_desc), ("text", text)):
            if value:
                matches[field] = query_counts[field][value]
        if resource_id and text:
            matches["resource_id+text"] = pair_counts[(resource_id, text)]
        return matches

    def _anchors_for(node):
        """Screen-unique labels that can name this element by its relationships.

        ``descendant`` names the element as the nearest interactive ancestor of one
        of its own labels — a row whose text lives in child views. ``sibling`` names
        it as a relative of a label in a neighbouring subtree — a card's button and
        the card's title. Each carries the relation it came from and the number of
        containers crossed, which is what lets a consumer prefer the nearest.
        Both are recorded here because the tree is only in scope during the walk;
        the flat list the caller receives has no parents.
        """
        is_unique = lambda v, c: label_counts[(c, v)] == 1  # noqa: E731

        def entry(value, clause, relation, climb):
            return {
                "value": value,
                "clause": clause,
                "relation": relation,
                "climb": climb,
            }

        return {
            "descendant": [
                entry(v, c, "descendant", 0)
                for v, c in _labels_under(node)
                if is_unique(v, c)
            ],
            "sibling": [
                entry(v, c, "sibling", level)
                for v, c, level in _sibling_labels(node, parent_of, is_unique)
                if is_unique(v, c)
            ],
        }

    # Raw source paths let a retained row name its nearest retained parent even
    # when one or more layout-only XML wrappers are promoted away. The map is
    # also kept through de-duplication so a child of a discarded duplicate can
    # still climb to the nearest published ancestor.
    emitted_parent_by_path = {}

    def walk(node, depth=0, source_path=(), emitted_parent_path=None):
        attrs = node.attrib
        bounds = _parse_bounds(attrs.get("bounds", ""))
        emitted = False
        if bounds and not _is_hidden(attrs):
            x1, y1, x2, y2 = bounds
            # viewport intersection
            if x2 > 0 and y2 > 0 and x1 < screen_w and y1 < screen_h:
                cls = attrs.get("class", "")
                scrollable = attrs.get("scrollable") == "true"
                interactive = _is_interactive(attrs)
                name = _own_text(attrs)
                if not name and attrs.get("clickable") == "true":
                    # Folding only reads non-interactive descendants, so a row's
                    # own label never leaks into its wrapper.
                    name = _fold_name(node)
                # P4 — prefer row-level clickables over outer containers: a
                # clickable wrapper that contributes no label of its own and
                # wraps clickable children is pure chrome; the children are the
                # real targets. Scrollables always survive (scroll affordance).
                if (not name and not scrollable
                        and attrs.get("clickable") == "true"
                        and _has_clickable_descendant(node)):
                    for child_ordinal, child in enumerate(node):
                        walk(child, depth, source_path + (child_ordinal,),
                             emitted_parent_path)
                    return
                resource_id = attrs.get("resource-id", "")
                if not (name or resource_id or interactive):
                    for child_ordinal, child in enumerate(node):
                        walk(child, depth, source_path + (child_ordinal,),
                             emitted_parent_path)
                    return
                role = _role_for(cls, attrs)
                # `item` is a pushed navigation role. An id-only inert wrapper
                # is useful to grep or ground, but is not a target the model
                # should receive on every page change.
                if not interactive and role == "item":
                    role = "group"
                elif not interactive and role in {
                        "button", "input", "switch", "checkbox", "radio",
                        "slider", "picker", "dropdown"}:
                    role = "text" if name else "group"
                # An unlabelled clickable covering the screen is the sheet a
                # dialog puts behind itself to catch a dismissing tap. It stays —
                # dismissing is a real move — but as an anonymous full-screen
                # "item" it reads like a target, and its centre is the middle of
                # whatever the dialog is covering.
                if (not name and not scrollable and role == "item"
                        and attrs.get("clickable") == "true"
                        and (x2 - x1) * (y2 - y1)
                        >= BACKDROP_AREA_FRACTION * screen_w * screen_h):
                    role = "backdrop"
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                content_desc = attrs.get("content-desc", "")
                # A password field's contents never leave the device: not into
                # a selector, a recorded step, or a prompt — so nothing counts a
                # text query for one either.
                text_value = ("" if attrs.get("password") == "true"
                              else attrs.get("text", ""))
                editable = _is_editable(attrs)
                accessibility_actions = _accessibility_actions(attrs)
                input_type = _optional_int(attrs, "input-type")
                displayed = _optional_bool(attrs, "displayed")
                if displayed is None:
                    displayed = _optional_bool(attrs, "visible-to-user")
                elements.append({
                    "role": role,
                    "name": _clean_label(name)[:MAX_NAME_LEN],
                    # Searchable names drop icon-font glyphs, while visual mode
                    # remains byte-compatible with pre-enrichment recordings.
                    "visual_name": _visual_label(name)[:MAX_NAME_LEN],
                    "bounds": bounds,
                    "center": (cx, cy),
                    "states": _states_for(attrs),
                    "affordances": _affordances_for(attrs),
                    "scrollable": scrollable,
                    "scroll_axis": _scroll_axis(node, cls, scrollable),
                    "interactive": interactive,
                    "editable": editable,
                    "raw_child_count": len(node),
                    "depth": depth,
                    "cls": cls,
                    "package": attrs.get("package", ""),
                    "resource_id": resource_id,
                    "content_desc": content_desc,
                    "text": text_value,
                    "hint": attrs.get("hint", ""),
                    # The node reports its `text` currently holds the placeholder.
                    "showing_hint": attrs.get("showing-hint") == "true",
                    "position": position_hint(cx, cy, screen_w, screen_h),
                    "anchors": _anchors_for(node),
                    "query_matches": _query_matches(
                        resource_id, content_desc, text_value),
                    "source_index": _optional_int(attrs, "index"),
                    "source_path": source_path,
                    "_parent_source_path": emitted_parent_path,
                    "parent_index": None,
                    "displayed": displayed,
                    "clickable": _optional_bool(attrs, "clickable"),
                    "checkable": _optional_bool(attrs, "checkable"),
                    "checked": _optional_bool(attrs, "checked"),
                    "enabled": _optional_bool(attrs, "enabled"),
                    "focusable": _optional_bool(attrs, "focusable"),
                    "focused": _optional_bool(attrs, "focused"),
                    "long_clickable": _optional_bool(attrs, "long-clickable"),
                    "context_clickable": _optional_bool(attrs, "context-clickable"),
                    "selected": _optional_bool(attrs, "selected"),
                    "dismissable": _optional_bool(attrs, "dismissable"),
                    "accessibility_focused": _optional_bool(attrs, "a11y-focused"),
                    "a11y_important": _optional_bool(attrs, "a11y-important"),
                    "screen_reader_focusable": _optional_bool(
                        attrs, "screen-reader-focusable"),
                    "input_type": input_type,
                    "input_kind": _input_kind(input_type),
                    "multiline": _optional_bool(attrs, "multiline"),
                    "max_text_length": _optional_nonnegative_int(
                        attrs, "max-text-length"),
                    "selection_start": _optional_nonnegative_int(
                        attrs, "selection-start"),
                    "selection_end": _optional_nonnegative_int(
                        attrs, "selection-end"),
                    "content_invalid": _optional_bool(attrs, "content-invalid"),
                    "error_text": attrs.get("error", ""),
                    "pane_title": attrs.get("pane-title", ""),
                    "tooltip_text": attrs.get("tooltip-text", ""),
                    "heading": _optional_bool(attrs, "heading"),
                    "text_entry_key": _optional_bool(attrs, "text-entry-key"),
                    "text_has_clickable_span": _optional_bool(
                        attrs, "text-has-clickable-span"),
                    "live_region": _optional_int(attrs, "live-region"),
                    "window_id": _optional_int(attrs, "window-id"),
                    "drawing_order": _optional_int(attrs, "drawing-order"),
                    "accessibility_actions": accessibility_actions,
                    "capabilities": _capabilities_for(
                        attrs, editable=editable, actions=accessibility_actions),
                    "semantic_traits": _semantic_traits(attrs),
                    "role_description": _extra_value(
                        attrs, "AccessibilityNodeInfo.roleDescription"),
                    "html_role": _extra_value(
                        attrs, "AccessibilityNodeInfo.chromeRole"),
                })
                emitted_parent_by_path[source_path] = emitted_parent_path
                emitted = True
        child_parent_path = source_path if emitted else emitted_parent_path
        for child_ordinal, child in enumerate(node):
            walk(child, depth + 1 if emitted else depth,
                 source_path + (child_ordinal,), child_parent_path)

    walk(root)

    # De-dup identical (role, name, center) rows, keeping the first.
    seen, unique = set(), []
    for e in elements:
        key = (e["role"], e["name"], e["center"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(e)

    for i, e in enumerate(unique, start=1):
        e["index"] = i

    index_by_source_path = {e["source_path"]: e["index"] for e in unique}
    for e in unique:
        parent_path = e.pop("_parent_source_path")
        while parent_path is not None and parent_path not in index_by_source_path:
            parent_path = emitted_parent_by_path.get(parent_path)
        e["parent_index"] = index_by_source_path.get(parent_path)

    return unique


def format_for_prompt(elements):
    """Render only the interactive subset, preserving visual-mode numbering."""
    lines = []
    for display_index, e in enumerate(
            (entry for entry in elements if entry.get("interactive", True)), start=1):
        visual_name = e.get("visual_name", e["name"])
        label = f'"{_visual_label(visual_name).replace(chr(34), chr(39))}"' \
            if visual_name else "(no label)"
        state = f' [{", ".join(e["states"])}]' if e["states"] else ""
        if e["scrollable"]:
            lines.append(
                f'[{display_index}] scrollable {label} — shows only items near the viewport; '
                f"more content may exist beyond it (scroll to reveal)"
            )
        else:
            lines.append(
                f'[{display_index}] {e["role"]} {label}{state} ({e["position"]})')
    if not lines:
        return "(no interactive elements detected — rely on the screenshot)"
    return "\n".join(lines)


#: Fingerprint keys used to match, most identifying first. Relaxation drops from
#: the end, so a developer-assigned id is the last thing given up. `css` is the
#: web surface's equivalent of a view id and is absent from a native fingerprint,
#: so a native re-find behaves exactly as it did before it existed.
_MATCH_KEYS = ("css", "resource_id", "content_desc", "text", "name")


def _contains(element, x, y):
    x1, y1, x2, y2 = element["bounds"]
    return x1 <= x <= x2 and y1 <= y <= y2


def _recorded_point(fp):
    """The centre the fingerprint was captured at, in either shape it travels in."""
    if fp.get("cx") is not None and fp.get("cy") is not None:
        return fp["cx"], fp["cy"]
    center = fp.get("center")
    if center and len(center) == 2:
        return center[0], center[1]
    return None


#: How far a candidate's box may sit from the recorded one, as a fraction of the
#: recorded box, before position stops being evidence about identity.
_POSITION_DRIFT = 0.25


def _same_box(element, fp):
    """Whether a candidate occupies the box the fingerprint was captured in.

    Containing the recorded centre is not enough on its own: a list that scrolled
    puts a DIFFERENT row over that point, and it will contain it just as well.
    Requiring the box to match too rejects a list that moved by anything other
    than a whole row, and rows inserted, removed or resized underneath.
    """
    recorded = fp.get("bounds")
    if not recorded or len(recorded) != 4:
        return True
    x1, y1, x2, y2 = element["bounds"]
    width = max(x2 - x1, 1)
    height = max(y2 - y1, 1)
    return (abs(recorded[0] - x1) <= width * _POSITION_DRIFT
            and abs(recorded[1] - y1) <= height * _POSITION_DRIFT
            and abs((recorded[2] - recorded[0]) - width) <= width * _POSITION_DRIFT
            and abs((recorded[3] - recorded[1]) - height) <= height * _POSITION_DRIFT)


def _by_position(matches, fp):
    """The match the recorded centre falls inside, or None.

    A row of chips or list rows shares one id and often carries no other
    attribute, so nothing textual can separate them. The centre was measured in
    the same parse the element came from, which names which one was captured.
    Anything short of exactly one containing element returns None: an almost-right
    row is a wrong tap, and the caller has a vision fallback that is not.

    Position is evidence about identity only while the screen has not moved, so a
    candidate must also still occupy the box the fingerprint was captured in.
    """
    point = _recorded_point(fp)
    if point is None:
        return None
    inside = [e for e in matches if _contains(e, *point) and _same_box(e, fp)]
    return inside[0] if len(inside) == 1 else None


def find_by_fingerprint(elements, fp):
    """Re-find a recorded element in a fresh tree. Returns element or None.

    Every attribute the fingerprint carries has to agree before a match counts,
    then the least identifying one is dropped and the tree is searched again — so
    a label that changed costs its own precision rather than the whole match.
    Candidates that remain tied are separated by the recorded position.
    """
    candidates = elements
    if fp.get("surface") == "web":
        candidates = [e for e in candidates if e.get("surface") == "web"]
        if "frame_path" in fp:
            # Frame identity is not a relaxable locator hint. The same CSS and
            # label can legitimately occur in two frames, and falling through to
            # the other one records and later heals the wrong target.
            candidates = [
                e for e in candidates
                if e.get("frame_path", "") == fp.get("frame_path", "")
            ]

    present = [k for k in _MATCH_KEYS if (fp.get(k) or "")]
    for cut in range(len(present), 0, -1):
        keys = present[:cut]
        matches = [e for e in candidates
                   if all((e.get(k) or "") == fp[k] for k in keys)]
        if len(matches) == 1:
            return matches[0]
        if matches:
            resolved = _by_position(matches, fp)
            if resolved is not None:
                return resolved
    return None
