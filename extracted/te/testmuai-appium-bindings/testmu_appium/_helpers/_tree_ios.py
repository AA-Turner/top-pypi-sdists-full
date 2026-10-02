"""Parse XCUITest page-source XML into the flat, indexed, LLM-ready element list.

The iOS producer of the contract `_tree.py` defines. Two producers, one contract —
not one parser parameterised over an attribute-name table, because Android's
`clickable`/`long-clickable`/`NAF` and iOS's `accessible`/`enabled`/`visible` are
not the same predicates spelled differently.

Everything here was measured against a 24-screen corpus (Proverbial, ShowcaseApp,
ADIB, Woolworths, Macy's, KAYAK, Safari, a camera app) captured on one 414x896
device. The findings that shaped it:

**`accessible` is the signal Android has no equivalent of.** UIKit already answers
"is this the thing a user perceives?" — and it answers it on the CONTAINER, not
its parts. Proverbial's six buttons are `accessible=true`; the `StaticText` inside
each one is `accessible=false`. That is Android's name-folding problem already
solved by the platform, which is why folding here is a fallback rather than the
main path.

**`visible` is trustworthy, and load-bearing.** Across the corpus it splits almost
exactly in half (1289/1283), and 491 nodes sit INSIDE the viewport while reporting
`visible=false` — occluded by a modal, alpha-0, or scrolled under a bar. Bounds
alone would wrongly admit every one of them. Android has to intersect the viewport
because `displayed` is mostly absent; here the driver has already done the work.

**`name` is an identifier, `label` is text.** Where they differ (481 of 1228 nodes
carrying both), `name` is what the developer wrote: `geoLocation`, `speedTest`,
`TabBarItemTitle`, and Interface Builder's own object ids (`iqY-AF-sfe`). Where
they are equal, iOS simply fell back to the label. So `name` feeds the selector and
`label` feeds the display — never the reverse.

**There is no `placeholderValue` and no separate hint attribute.** The corpus
carries exactly eleven attributes; `hint` is therefore always empty on iOS, and an
empty field reports nothing rather than reporting its placeholder as Android does.
"""

import re
import xml.etree.ElementTree as ET
from collections import Counter

from testmu_appium._helpers._tree import (
    FRAGMENT_SEPARATOR,
    ILLEGAL_XML,
    MAX_ANCHOR_CLIMB,
    MAX_NAME_FRAGMENTS,
    MAX_NAME_LEN,
    _clean_label,
    _optional_bool,
    _optional_int,
    _visual_label,
    position_hint,
)

#: Interface Builder's own object ids — three dash-separated alphanumeric groups.
#: ADIB's screens name every element this way.
_IB_OBJECT_ID = re.compile(r"^[A-Za-z0-9]{2,4}-[A-Za-z0-9]{2,4}-[A-Za-z0-9]{2,4}$")

#: An asset or symbol name: a lowercase run followed by at least one capitalised
#: word, with no spaces. Anchored so a real sentence never matches.
_CAMEL_CASE = re.compile(r"^[a-z]+(?:[A-Z][a-z0-9]*)+$")


#: XCUIElementType suffix → the neutral role the contract publishes. Ordered:
#: the first match wins, so more specific types precede the ones they resemble.
ROLE_MAP = [
    ("SecureTextField", "input"),
    ("SearchField", "input"),
    ("TextField", "input"),
    ("TextView", "input"),
    ("Switch", "switch"),
    ("Toggle", "switch"),
    ("CheckBox", "checkbox"),
    ("RadioButton", "radio"),
    ("Slider", "slider"),
    ("Stepper", "slider"),
    ("PickerWheel", "picker"),
    ("DatePicker", "picker"),
    ("Picker", "dropdown"),
    ("SegmentedControl", "dropdown"),
    ("Link", "link"),
    ("Button", "button"),
    ("Key", "button"),
    ("MenuItem", "item"),
    ("Cell", "item"),
    ("Image", "image"),
    ("StaticText", "text"),
    ("WebView", "webview"),
    ("ScrollView", "scrollable"),
    ("CollectionView", "scrollable"),
    ("Table", "scrollable"),
]

#: Types that earn a row even when the driver did not mark them accessible.
#:
#: This exists for ONE measured reason: web content projected into the native tree
#: arrives as `Link` and `Button` nodes that iOS leaves `accessible=false`. On a
#: Safari screen the rule added 23 rows, every one a real link target. Without it
#: the projected half of a WebView screen is silently dropped.
#:
#: Scroll containers are here for their scroll affordance, matching Android, where
#: `scrollable` earns a row of its own.
INTERACTIVE_TYPES = frozenset({
    "Button", "Cell", "Link", "Switch", "TextField", "SecureTextField",
    "SearchField", "TextView", "SegmentedControl", "Slider", "Stepper", "Key",
    "MenuItem", "Tab", "PickerWheel", "DatePicker", "Picker",
    "ScrollView", "CollectionView", "Table",
})

#: Types that mark where the native tree stops and a page begins.
#:
#: Admitted for one reason, and it is not that they are tappable: the web reader
#: only opens a debug channel for a screen that HAS web content, and it decides
#: that by looking for a row like this. iOS leaves `XCUIElementTypeWebView`
#: `accessible=false`, so without this the row never appears, `has_web_content`
#: is false on every iOS screen, and the entire web surface is unreachable —
#: measured at 27 such nodes across the corpus's 9 WebView screens, 0 emitted.
#:
#: Kept OUT of INTERACTIVE_TYPES deliberately: a WebView is a container, and
#: calling it interactive would offer the agent the page itself as a tap target.
WEB_CONTAINER_TYPES = frozenset({"WebView"})

#: Types whose `value` is what somebody typed, rather than a restatement of the
#: label. `StaticText` carries a `value` on every one of the corpus's 519
#: instances and it is always a copy of the label — reading it as content would
#: rename half the screen after itself.
EDITABLE_TYPES = frozenset({
    "TextField", "SecureTextField", "SearchField", "TextView",
})

#: Contents never leave the device for these, in a selector, a step or a prompt.
SECRET_TYPES = frozenset({"SecureTextField"})

#: Containers whose children repeat. The sibling-anchor climb stops here — the
#: iOS counterpart of Android stopping at `scrollable="true"` — because a label
#: found past this boundary belongs to the list, not to any one cell in it.
_SCROLL_CONTAINER_TYPES = frozenset({"ScrollView", "CollectionView", "Table"})

#: Types that scroll, and along which axis where the type itself says so.
_SCROLL_AXIS_BY_TYPE = {
    "Table": "vertical",
    "PickerWheel": "vertical",
    "DatePicker": "vertical",
}

#: Bidi control marks. Safari's address field reports its value as
#: "‎zomato.com" — invisible, and it makes an exact selector comparison miss.
_BIDI_MARKS = str.maketrans("", "", "‎‏‪‫‬‭‮")

#: How much of the screen an unlabelled tappable has to cover before it is the
#: dismiss-catching sheet behind a sheet rather than a target. Mirrors Android's.
BACKDROP_AREA_FRACTION = 0.9

#: Attribute a recorded clause matches. iOS publishes its own clause vocabulary —
#: `_strategy.py`'s iOS column compiles exactly these, and rejects Android's.
_CLAUSE_ATTRS = (("label", "label"), ("name", "name"), ("value", "value"))


def _text(attrs, key):
    return (attrs.get(key) or "").translate(_BIDI_MARKS)


def _role_for(type_name, attrs):
    for suffix, role in ROLE_MAP:
        if type_name == suffix:
            return role
    if attrs.get("accessible") == "true":
        return "item"
    return "item"


def _bounds(attrs):
    """Device-point box, or None when the node has no drawable area.

    XCUITest reports origin plus size, where uiautomator reports two corners; the
    contract wants two corners, so the conversion happens here rather than leaking
    a second bounds shape to every consumer.
    """
    try:
        x = int(float(attrs.get("x", 0)))
        y = int(float(attrs.get("y", 0)))
        w = int(float(attrs.get("width", 0)))
        h = int(float(attrs.get("height", 0)))
    except (TypeError, ValueError):
        return None
    if w <= 0 or h <= 0:
        return None
    return (x, y, x + w, y + h)


def _is_editable(type_name):
    return type_name in EDITABLE_TYPES


def _holds_a_typed_value(type_name, attrs):
    return _is_editable(type_name) and bool(_text(attrs, "value"))


def _is_identifier_like(value):
    """Whether this string is something a developer wrote for themselves.

    `name` doubles as both the accessibility identifier and, where none was set,
    a copy of the label — so it is the right last resort for a display name and
    the wrong one whenever it holds an identifier. Three shapes were measured:

    - Interface Builder object ids, which ADIB's screens are built entirely from:
      `iqY-AF-sfe`, `DEC-ep-PfG`. Unique, stable, meaningless to a reader.
    - Safari's internal handles, which carry a query string:
      `TabDocument?IsLoadedUsingDesktopUserAgent=false`.
    - camelCase and snake_case asset names: `icBackNavigation`, `geoLocation`.

    Deliberately narrow. A one-word label with no case transition — "Done",
    "Delete", "Back", "1" — is text a person reads and must survive.
    """
    stripped = value.strip()
    if not stripped or " " in stripped:
        return False
    return bool(_IB_OBJECT_ID.match(stripped)
                or "?" in stripped
                or _CAMEL_CASE.match(stripped)
                or "_" in stripped)


def _own_label(attrs, type_name):
    """This node's own display label, ignoring descendants.

    A filled field is named by its LABEL, never by its contents: taking the
    contents renames the element the moment it is typed into, puts whatever was
    typed into the prompt, and makes two fields holding similar values
    indistinguishable.

    `name` is the last resort, and only when it is not an identifier — an
    Interface Builder object id reaching the prompt tells the model nothing and
    costs it a row it cannot reason about. The identifier is still published as
    `content_desc`, where the selector wants it.
    """
    label = _clean_label(_text(attrs, "label"))
    name = _clean_label(_text(attrs, "name"))
    # label == name is iOS reporting one string twice, not two agreeing sources:
    # UIKit publishes the identifier as the label when the developer set no label.
    # So the identifier test applies to it exactly as it does to `name` — without
    # this, `icBackNavigation` arrives as a display label because it was copied.
    if label and not (label == name and _is_identifier_like(label)):
        return label
    if not _holds_a_typed_value(type_name, attrs):
        value = _clean_label(_text(attrs, "value"))
        if value:
            return value
    return "" if _is_identifier_like(name) else name


def _label_with_source(attrs, type_name):
    """(value, clause) for this node's own label; ('', '') when it has none.

    The clause travels with the value because a label matched with the wrong
    attribute resolves nothing — `label` and `name` routinely hold different
    strings on the same node.
    """
    for xml_attr, clause in _CLAUSE_ATTRS:
        if clause == "value" and _holds_a_typed_value(type_name, attrs):
            continue
        value = _clean_label(_text(attrs, xml_attr))
        if value:
            return value, clause
    return "", ""


def _type_of(node):
    return (node.get("type") or node.tag or "").replace("XCUIElementType", "")


def _is_admitted(node, screen_w, screen_h, parent=None):
    """Whether this node earns a row.

    `visible` is the gate, and it is the driver's own answer rather than a bounds
    test — 491 nodes in the corpus sit inside the viewport and report false.
    Bounds are still intersected, because 4 nodes reported visible while lying
    entirely outside it.

    One rescue: an on-screen ACCESSIBLE node whose parent reports
    `visible="true"` is admitted despite its own false. WDA's flag is wrong in
    exactly one systematic place — tab-bar buttons on screen, drawn, and
    tappable report `visible="false"` while the bar containing them reports
    true — and that dropped an app's primary navigation from every capture.
    The parent's word plus `accessible` plus on-screen bounds is the narrowest
    gate that readmits them: measured across the corpus it adds 8 rows, where
    trusting bounds alone adds ~700.
    """
    attrs = node.attrib
    if attrs.get("visible") != "true":
        if not (attrs.get("accessible") == "true" and parent is not None
                and parent.attrib.get("visible") == "true"):
            return False
    box = _bounds(attrs)
    if box is None:
        return False
    x1, y1, x2, y2 = box
    if x2 <= 0 or y2 <= 0 or x1 >= screen_w or y1 >= screen_h:
        return False
    return (attrs.get("accessible") == "true"
            or _type_of(node) in INTERACTIVE_TYPES
            or _type_of(node) in WEB_CONTAINER_TYPES)


def _states_for(type_name, attrs):
    states = []
    if attrs.get("enabled") == "false":
        states.append("disabled")
    value = _text(attrs, "value")
    if type_name in ("Switch", "Toggle", "CheckBox", "RadioButton"):
        # A switch reports its position as the string "1"/"0", not a boolean.
        if value in ("1", "true", "YES"):
            states.append("checked")
    elif value == "1" and type_name in ("Button", "Cell", "Tab", "MenuItem"):
        # The selected tab reports value="1"; an unselected one reports nothing.
        states.append("selected")
    if type_name in SECRET_TYPES:
        states.append("password")
    return states


def _affordances_for(attrs):
    """What this node responds to that its role does not already say.

    `unlabelled` is the counterpart of uiautomator's NAF flag, derived rather than
    read: iOS publishes no such attribute, so a node the driver calls an
    accessibility element while carrying nothing to search for is the same finding.
    """
    found = []
    if (attrs.get("accessible") == "true"
            and not (_text(attrs, "label") or _text(attrs, "name")
                     or _text(attrs, "value"))):
        found.append("unlabelled")
    return found


def _scroll_axis(node, type_name, scrollable):
    """The direction a scrollable container can plausibly move.

    XCUITest publishes no scroll axis at all, so where the type does not say it is
    inferred from how the visible children are laid out — the same fallback the
    Android parser uses for a custom container. An indeterminate one stays unknown
    rather than inventing a direction from the viewport's aspect ratio.
    """
    if not scrollable:
        return None
    known = _SCROLL_AXIS_BY_TYPE.get(type_name)
    if known:
        return known
    centres = []
    for child in node:
        box = _bounds(child.attrib)
        if box:
            centres.append(((box[0] + box[2]) // 2, (box[1] + box[3]) // 2))
    if len(centres) < 2:
        return None
    x_span = max(c[0] for c in centres) - min(c[0] for c in centres)
    y_span = max(c[1] for c in centres) - min(c[1] for c in centres)
    if x_span == y_span == 0:
        return None
    return "horizontal" if x_span > y_span else "vertical"


def _labels_under(node):
    """Every (value, clause) inside this subtree, bounded by interaction.

    A node that is a target in its own right ends the descent, so a card does not
    collect the labels of the buttons inside it — `ancestor_of` on one of those
    would otherwise resolve the button rather than the card.
    """
    found = []

    def collect(current):
        for child in current:
            if child.attrib.get("accessible") == "true" or _type_of(child) in INTERACTIVE_TYPES:
                continue
            value, clause = _label_with_source(child.attrib, _type_of(child))
            if value:
                found.append((value, clause))
            collect(child)

    collect(node)
    return found


def _sibling_labels(node, parent_of, is_unique):
    """Labels carried by the subtrees this node shares a container with.

    Climbs rather than reading direct siblings alone: a card's title is rarely a
    direct sibling of the button inside it. Each carries the number of containers
    crossed so a consumer can prefer the nearest.
    """
    found = []
    current = node
    for level in range(1, MAX_ANCHOR_CLIMB + 1):
        parent = parent_of.get(current)
        # Stopping at a scroll container is what the Android climb does with
        # `scrollable="true"`, and for the same reason: past that boundary the
        # "sibling" is a header OUTSIDE the list, one label every repeated cell
        # would inherit — an anchor that is unique on screen and matches every
        # copy of the control it was meant to tell apart.
        if parent is None or _type_of(parent) in _SCROLL_CONTAINER_TYPES:
            break
        for sibling in parent:
            if sibling is current:
                continue
            value, clause = _label_with_source(sibling.attrib, _type_of(sibling))
            if value:
                found.append((value, clause, level))
            found.extend((v, c, level) for v, c in _labels_under(sibling))
        if any(is_unique(value, clause) for value, clause, _ in found):
            break
        current = parent
    return found


def _collect_texts(node, out, seen):
    """Fold descendant labels into a container that carries none of its own.

    Far less load-bearing than on Android: UIKit already publishes the folded
    result as one `accessible` node in the common case. This covers the containers
    it does not — a projected web card, a custom control assembled from parts.
    """
    for child in node:
        if len(out) >= MAX_NAME_FRAGMENTS:
            return
        if child.attrib.get("accessible") == "true" or _type_of(child) in INTERACTIVE_TYPES:
            continue
        text = _own_label(child.attrib, _type_of(child))
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


def parse_tree(xml_str, screen_w, screen_h):
    """Return the viewport's useful nodes in document order, indexed 1-based.

    Raises ValueError when the document cannot be parsed, so a caller can retry a
    capture taken mid-transition instead of receiving the XML library's own error
    from three frames down.
    """
    try:
        root = ET.fromstring(ILLEGAL_XML.sub("", xml_str or ""))
    except ET.ParseError as e:
        raise ValueError(
            f"page source is not parseable ({e}); it was {len(xml_str or '')} "
            f"characters long. A capture taken mid-transition can be truncated."
        ) from e

    parent_of = {child: node for node in root.iter() for child in node}

    # The owning application, the nearest counterpart of Android's package.
    # Resolved ONCE from the Application element: the root is normally the
    # AppiumAUT wrapper (or an Application that is `accessible=false`), so no
    # emitted row is ever the root and a `root is node` test stamped every row
    # with "".
    application = next(
        (n for n in root.iter() if _type_of(n) == "Application"), root)
    owner = _text(application.attrib, "name")

    # What the DRIVER would match — counted over every node, exactly as the
    # anchors' `label_counts` below already are, and for the same reason.
    #
    # A node earns a row only if `_is_admitted` says so, and UIKit publishes a
    # control's caption as a separate `accessible="false"` StaticText carrying the
    # SAME `name`. That caption is not a row and is not meant to be — it would
    # double every button in the document the model reads. But `find_elements`
    # queries the hierarchy, not the rows, and returns it: on the Proverbial home
    # screen `accessibility_id "Text"` resolves to the button AND its caption,
    # while the rows show one. Uniqueness judged on the rows is judged on a set
    # the element was removed from, and the selector that gets recorded resolves
    # to two elements at replay.
    #
    # Keys mirror the row fields a selector compiles from, so a consumer counting
    # `content_desc` over its rows can ask the document the same question.
    identifier_counts = Counter()
    identifier_type_counts = Counter()
    # `text` compiles to `label == v OR name == v OR value == v`, so a node
    # answering on two of the three is still one element: count nodes, not
    # attributes.
    text_query_counts = Counter()
    for node in root.iter():
        attrs = node.attrib
        identifier = _text(attrs, "name")
        if identifier:
            identifier_counts[identifier] += 1
            identifier_type_counts[(attrs.get("type", ""), identifier)] += 1
        for value in {_text(attrs, a) for a in ("label", "name", "value")} - {""}:
            text_query_counts[value] += 1

    def _query_matches(attrs, name, text):
        """The driver-side count for each field this node's selectors compile from.

        A folded or truncated `name` belongs to no single node and counts 0 —
        honestly, since the query built from it matches nothing. The consumer
        keeps its own count where this one is smaller, so a 0 costs nothing.
        """
        matches = {}
        identifier = _text(attrs, "name")
        if identifier:
            matches["content_desc"] = identifier_counts[identifier]
            matches["content_desc+cls"] = identifier_type_counts[
                (attrs.get("type", ""), identifier)]
        if name:
            matches["name"] = text_query_counts[name]
        if text:
            matches["text"] = text_query_counts[text]
        return matches

    label_counts = Counter(
        (clause, value)
        for clause, value in (
            (c, v) for v, c in (
                _label_with_source(n.attrib, _type_of(n)) for n in root.iter()
            ) if v
        )
    )

    def _anchors_for(node):
        """Screen-unique labels that can name this element by its relationships."""
        is_unique = lambda v, c: label_counts[(c, v)] == 1  # noqa: E731

        def entry(value, clause, relation, climb):
            return {
                "value": value, "clause": clause,
                "relation": relation, "climb": climb,
            }

        return {
            "descendant": [
                entry(v, c, "descendant", 0)
                for v, c in _labels_under(node) if is_unique(v, c)
            ],
            "sibling": [
                entry(v, c, "sibling", level)
                for v, c, level in _sibling_labels(node, parent_of, is_unique)
                if is_unique(v, c)
            ],
        }

    elements = []
    emitted_parent_by_path = {}

    def walk(node, depth=0, source_path=(), emitted_parent_path=None):
        emitted = False
        if _is_admitted(node, screen_w, screen_h, parent_of.get(node)):
            attrs = node.attrib
            type_name = _type_of(node)
            box = _bounds(attrs)
            assert box is not None  # _is_admitted already rejected an unbounded node
            x1, y1, x2, y2 = box
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            if type_name in WEB_CONTAINER_TYPES:
                # A WebView is a marker, not a labelled element. Its own name is a
                # class token ("WebView") and folding its descendants restates the
                # page — iOS nests three of these wrappers, and each folds a
                # DIFFERENT subset ("Vertical scroll bar, 2 pages…", "Google ·
                # banner · Search settings"), so three near-identical rows survive
                # a de-dup that keys on the name. Nameless, they collapse to one
                # through the de-dup already at the end of this function.
                name = ""
            else:
                name = _own_label(attrs, type_name)
                if not name:
                    name = _fold_name(node)
            role = _role_for(type_name, attrs)
            scrollable = type_name in ("ScrollView", "CollectionView", "Table",
                                       "PickerWheel", "DatePicker")

            # An unlabelled tappable covering the screen is the sheet a dialog puts
            # behind itself to catch a dismissing tap. It stays — dismissing is a
            # real move — but as an anonymous full-screen item it reads like a
            # target, and its centre is the middle of whatever it covers.
            if (not name and not scrollable and role == "item"
                    and (x2 - x1) * (y2 - y1)
                    >= BACKDROP_AREA_FRACTION * screen_w * screen_h):
                role = "backdrop"

            secret = type_name in SECRET_TYPES
            row_name = name[:MAX_NAME_LEN]
            row_text = "" if secret else _text(attrs, "value")
            elements.append({
                "role": role,
                "name": row_name,
                "visual_name": _visual_label(name)[:MAX_NAME_LEN],
                "bounds": box,
                "center": (cx, cy),
                "states": _states_for(type_name, attrs),
                "affordances": _affordances_for(attrs),
                "scrollable": scrollable,
                "scroll_axis": _scroll_axis(node, type_name, scrollable),
                "interactive": (attrs.get("accessible") == "true"
                                or type_name in INTERACTIVE_TYPES),
                "editable": _is_editable(type_name),
                "depth": depth,
                "cls": attrs.get("type", ""),
                # The owning application, the nearest counterpart of a package —
                # resolved once above, because the Application element itself is
                # `accessible=false` and never earns a row of its own.
                "package": owner,
                # iOS has no developer id SEPARATE from the accessibility one:
                # `name` IS the accessibilityIdentifier, and it is published as
                # content_desc because that is the field the accessibility_id
                # strategy compiles from. Leaving resource_id empty is the honest
                # answer — there is no second identifier for a `view_id` row to
                # mean, which is why the iOS strategy column has no such row.
                "resource_id": "",
                "content_desc": _text(attrs, "name"),
                "text": row_text,
                # No placeholderValue attribute exists on this producer, so an
                # empty field advertises nothing rather than reporting its
                # placeholder the way Android's showing-hint does.
                "hint": "",
                "showing_hint": False,
                "position": position_hint(cx, cy, screen_w, screen_h),
                "anchors": _anchors_for(node),
                "query_matches": _query_matches(attrs, row_name, row_text),
                # The additive producer-metadata columns of the contract. This
                # producer answers the ones its XML carries — `visible`,
                # `enabled`, `selected`, the sibling `index` — and publishes
                # honest absence for the rest: the remaining columns describe
                # AccessibilityNodeInfo facts XCUITest has no counterpart for,
                # and None/empty means "not measured", never "false".
                "raw_child_count": len(node),
                "source_index": _optional_int(attrs, "index"),
                "source_path": source_path,
                "_parent_source_path": emitted_parent_path,
                "parent_index": None,
                "displayed": _optional_bool(attrs, "visible"),
                "clickable": None,
                "checkable": None,
                "checked": None,
                "enabled": _optional_bool(attrs, "enabled"),
                "focusable": None,
                "focused": _optional_bool(attrs, "focused"),
                "long_clickable": None,
                "context_clickable": None,
                "selected": _optional_bool(attrs, "selected"),
                "dismissable": None,
                "accessibility_focused": None,
                "a11y_important": None,
                "screen_reader_focusable": None,
                "input_type": None,
                "input_kind": None,
                "multiline": None,
                "max_text_length": None,
                "selection_start": None,
                "selection_end": None,
                "content_invalid": None,
                "error_text": "",
                "pane_title": "",
                "tooltip_text": "",
                "heading": None,
                "text_entry_key": None,
                "text_has_clickable_span": None,
                "live_region": None,
                "window_id": None,
                "drawing_order": None,
                "accessibility_actions": [],
                "capabilities": [],
                "semantic_traits": [],
                "role_description": "",
                "html_role": "",
            })
            emitted_parent_by_path[source_path] = emitted_parent_path
            emitted = True
        child_parent_path = source_path if emitted else emitted_parent_path
        for child_ordinal, child in enumerate(node):
            walk(child, depth + 1 if emitted else depth,
                 source_path + (child_ordinal,), child_parent_path)

    walk(root)

    # De-dup identical (role, name, centre) rows, keeping the first. iOS nests a
    # tappable inside its own semantic wrapper — a projected web Link contains a
    # Button at byte-identical bounds — so this is load-bearing here, not a tidy-up.
    seen, unique = set(), []
    for element in elements:
        key = (element["role"], element["name"], element["center"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(element)

    for index, element in enumerate(unique, start=1):
        element["index"] = index

    # Resolve each row's nearest EMITTED ancestor to its row index, climbing
    # over ancestors the de-dup dropped — the same walk the Android producer
    # makes, so `parent_index` means one thing on both platforms.
    index_by_source_path = {e["source_path"]: e["index"] for e in unique}
    for element in unique:
        parent_path = element.pop("_parent_source_path")
        while parent_path is not None and parent_path not in index_by_source_path:
            parent_path = emitted_parent_by_path.get(parent_path)
        element["parent_index"] = index_by_source_path.get(parent_path)

    return unique
