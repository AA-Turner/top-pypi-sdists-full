"""Fold a WebView's DOM into the native flat list.

The canonical copy of this module: the v16 runner and any host that embeds the
binding (auteur) read it from ``testmu_appium.perception``.

The model receives one indexed list and never learns that a screen had more than
one surface. Each row keeps the surface it came from so the executor can send the
action back down the same channel it was read on — the trick the web path already
uses for locators, applied one level up.

Geometry is the seam. A DOM rectangle is in CSS pixels inside a viewport that is
scaled and offset; the accessibility tree reports device pixels. Where an element
reaches us from both, the device's numbers win: they are what a tap is measured
against.
"""

from enum import Enum

from testmu_appium._errors import UnsupportedOnPlatform
from testmu_appium._v4._helpers._tabs_android import is_chrome_package
from testmu_appium._v4._helpers._tree import position_hint

#: How near two elements must be, in device pixels, to be treated as the same
#: element seen from two surfaces. A card and its label are further apart than
#: this; a WebView's projection of a button and the button itself are not.
_SAME_ELEMENT_PX = 40

#: Which packages count as Chrome is the binding's rule, shared with the
#: visibility probe that confirms a candidate. In-app WebViews are excluded
#: there until their collapsed projection has been measured independently.
#: A collapsed Chrome projection covers effectively the whole content area.
#: Tolerances admit status/navigation insets without treating a focused picker
#: control as a page-sized surface. The measured node was [0,84][1080,2400] on
#: a 1080x2400 screen.
_CONTENT_MIN_WIDTH_RATIO = 0.90
_CONTENT_MIN_HEIGHT_RATIO = 0.90
_CONTENT_HORIZONTAL_EDGE_TOLERANCE = 0.05
_CONTENT_TOP_TOLERANCE = 0.20
_CONTENT_BOTTOM_TOLERANCE = 0.05


class NativeWebState(Enum):
    """What the already-parsed native tree says about web content."""

    AWAKE = "awake"
    COLLAPSED_CANDIDATE = "collapsed_candidate"
    NONE = "none"

#: Tags that make a DOM element interactive in its own right. Readable copy is
#: also a row, but it keeps an informational role and is not offered as an action.
_INTERACTIVE_TAGS = frozenset(
    {"A", "BUTTON", "INPUT", "TEXTAREA", "SELECT", "SUMMARY", "LABEL", "OPTION"})

#: ARIA roles that make an element a target in its own right. `tablist`, `img`
#: and `tabpanel` were all offered as rows before this existed — a tab is
#: tappable, the strip holding it is not.
_INTERACTIVE_ROLES = frozenset({
    "button", "link", "tab", "checkbox", "radio", "switch", "textbox",
    "searchbox", "combobox", "option", "menuitem", "menuitemcheckbox",
    "menuitemradio", "slider", "spinbutton", "treeitem",
})

#: DOM tag → the role vocabulary the native tree already speaks, so one list
#: reads consistently whichever surface a row came from.
#:
_ROLE_FOR_TAG = {
    "A": "link",
    "BUTTON": "button",
    "INPUT": "input",
    "TEXTAREA": "input",
    "SELECT": "dropdown",
    "LABEL": "text",
    "OPTION": "item",
    "SUMMARY": "item",
}

#: ARIA role → the same native vocabulary, for elements whose TAG says nothing
#: (a `div` carrying `role="option"`). Web and native name the same widgets
#: differently, and a document mixing both dialects asks the model to act on
#: words its instructions never gave it.
_ROLE_FOR_ARIA = {
    "textbox": "input", "searchbox": "input", "combobox": "input",
    "spinbutton": "input",
    "listbox": "dropdown", "menu": "dropdown",
    "option": "item", "menuitem": "item", "menuitemcheckbox": "item",
    "menuitemradio": "item", "treeitem": "item", "tab": "item", "row": "item",
    "radio": "checkbox",
    "heading": "text", "img": "image", "presentation": "text", "none": "text",
}

#: The words the model is told the document uses. A role outside this set is a
#: word the prompt never defined.
_NATIVE_VOCABULARY = frozenset({
    "button", "item", "input", "link", "dropdown", "picker", "checkbox",
    "switch", "text", "image", "webview", "scrollable", "group",
})


#: Tags whose own name outranks any ARIA role the page put on them.
#:
#: Only the form controls, and for one reason: these are the elements the model
#: TYPES into, and no ARIA word can make a TEXTAREA not typeable. Google's search
#: box is `<textarea role="textbox">`; honouring the ARIA word published it as
#: `textbox`, which is web vocabulary, into a document whose prompt declares the
#: vocabulary as `input`. The model would not reference a role it was never
#: given, fell back to describing the target for vision, and the text landed in
#: the app's native URL bar instead of the page.
#:
#: Deliberately NOT applied to A and BUTTON: `<a role="button">` is a button to
#: everyone who uses it, and letting the tag win there demotes it to a link.
_TAG_OUTRANKS_ARIA = frozenset({"INPUT", "TEXTAREA", "SELECT"})


def _role_of(element, tag, actionable):
    """One word from the native vocabulary for a DOM element.

    Web and native name the same widgets differently, and a document mixing both
    dialects asks the model to act on words its instructions never defined. The
    old third fallback was the raw tag name, which published `div`, `span`,
    `path` and `g-dropdown-menu` as roles for anything that reached it.
    """
    if not actionable:
        return "text" if element.get("label", "") else "group"
    if tag in _TAG_OUTRANKS_ARIA:
        return _ROLE_FOR_TAG[tag]
    aria = (element.get("role") or "").lower()
    if aria in _ROLE_FOR_ARIA:
        return _ROLE_FOR_ARIA[aria]
    if aria in _NATIVE_VOCABULARY:
        return aria
    by_tag = _ROLE_FOR_TAG.get(tag)
    if by_tag:
        return by_tag
    # Actionable, and nothing said what it is: `item` is the vocabulary's word
    # for "a tappable row", which is exactly what is known about it.
    return "item"


#: platform → how many device-space units one CSS pixel spans.
#:
#: The platforms disagree because their NATIVE trees are in different units, and
#: this factor's job is to land a DOM rectangle in whatever unit the native side
#: reports — that is what a tap is measured against.
#:
#: - Android's accessibility tree is in device PIXELS, so a CSS pixel is worth
#:   `devicePixelRatio` of them, times any pinch zoom.
#: - iOS's XCUIElement tree is in POINTS, and a CSS pixel IS a point. Applying
#:   dpr here would double every coordinate.
#:
#: Measured on an iPhone 11 rather than reasoned about: the WebView's native
#: bounds were 404x672 points while the page reported innerWidth 404 and
#: innerHeight 672 CSS pixels — a ratio of exactly 1.0, against dpr*scale of 2.0.
#: Every web tap would have landed at twice its offset.
_CSS_TO_DEVICE = {
    "android": lambda page: float(page.get("dpr", 1)) * float(page.get("scale", 1) or 1),
    "ios": lambda page: float(page.get("scale", 1) or 1),
}


def _factor(page, platform="android"):
    """How many device-space units one CSS pixel spans on this platform."""
    convert = _CSS_TO_DEVICE.get((platform or "").lower())
    if convert is None:
        raise UnsupportedOnPlatform("web surface placement", platform)
    return convert(page)


def is_actionable(element):
    """Whether a DOM element can be offered as an action target."""
    if "interactive" in element:
        return bool(element["interactive"])
    return (element.get("tag", "").upper() in _INTERACTIVE_TAGS
            or (element.get("role") or "").lower() in _INTERACTIVE_ROLES)


def to_elements(surface, screen, platform="android"):
    """A read web surface as flat-list rows, positioned in device pixels.

    ``surface`` is what the binding's reader returns: elements in page CSS pixels
    plus the device-space origin it solved for them. Rows come back in the shape
    the native parser produces — same keys, same vocabulary — because everything
    downstream reads one list and must not have to ask which surface a row is
    from.
    """
    page, origin = surface.page, surface.origin
    screen_w, screen_h = screen
    factor = _factor(page, platform)
    offset_left = page.get("offsetLeft", 0)
    offset_top = page.get("offsetTop", 0)
    viewport_elements = {id(element) for element in surface.elements}
    rows = []
    for element in surface.all_elements:
        actionable = is_actionable(element)
        name = element.get("label", "")
        if not actionable and not name:
            continue
        cx = round(origin[0] + (element["x"] - offset_left + element["w"] / 2) * factor)
        cy = round(origin[1] + (element["y"] - offset_top + element["h"] / 2) * factor)
        tag = element.get("tag", "").upper()
        offscreen = id(element) not in viewport_elements
        rows.append({
            "surface": "web",
            "role": _role_of(element, tag, actionable),
            "name": name,
            "visual_name": name,
            "center": (cx, cy),
            "bounds": _bounds(element, origin, factor, offset_left, offset_top),
            "css": element.get("css", ""),
            # A selector naming THIS element, for when `css` is only a tag name.
            # Carried beside `css` rather than replacing it so every selector
            # that resolves today is unchanged.
            "css_path": element.get("css_path", ""),
            "clause": element.get("clause", "text"),
            "frame_path": element.get("path", ""),
            "dom_path": element.get("dom_path"),
            "states": [],
            "affordances": [],
            "scrollable": False,
            "scroll_axis": None,
            # Visual mode describes the screenshot and cannot offer an offscreen
            # box. Text mode still publishes the row and scrolls it before acting.
            "interactive": actionable and not offscreen,
            "editable": bool(element.get("editable")),
            "raw_child_count": 0,
            "offscreen": offscreen,
            "depth": 0,
            # The native row's keys, so no reader downstream has to branch. A DOM
            # element carries none of the Android attributes; its tag stands in
            # for the widget class, which is what `role` and `tag` are read from.
            "cls": tag,
            "package": "",
            "resource_id": "",
            "text": "",
            "content_desc": "",
            # The placeholder, which is the OTHER name this element has. A field
            # can carry an aria-label a screen reader speaks and a placeholder a
            # person reads, and they routinely differ — Google's box is
            # "Google Search" to the first and "Ask Google" to the second. An
            # objective is written by someone looking at the screen, so publishing
            # only the aria-label leaves their wording matching nothing: measured,
            # the model resolved this element by ref when it happened to say
            # "Google Search" and fell back to vision when it said "Ask Google".
            "hint": element.get("placeholder", ""),
            # A hint SHOWS when the field is empty, which is exactly when it is
            # the visible name. The native contract means the same thing by it.
            "showing_hint": bool(element.get("placeholder"))
            and not (element.get("value") or ""),
            "anchors": {"descendant": [], "sibling": []},
            "position": (None if offscreen
                         else position_hint(cx, cy, screen_w, screen_h)),
        })
    return rows


def _bounds(element, origin, factor, offset_left, offset_top):
    x1 = round(origin[0] + (element["x"] - offset_left) * factor)
    y1 = round(origin[1] + (element["y"] - offset_top) * factor)
    x2 = round(origin[0] + (element["x"] + element["w"] - offset_left) * factor)
    y2 = round(origin[1] + (element["y"] + element["h"] - offset_top) * factor)
    return (x1, y1, x2, y2)


def _webviews(native):
    return [e for e in native
            if e.get("role") == "webview" or "WebView" in (e.get("cls") or "")]


def _covers_content_area(bounds, screen):
    if not bounds:
        return False
    screen_w, screen_h = screen
    if screen_w <= 0 or screen_h <= 0:
        return False
    x1, y1, x2, y2 = bounds
    width = max(0, x2 - x1)
    height = max(0, y2 - y1)
    return (
        width >= screen_w * _CONTENT_MIN_WIDTH_RATIO
        and height >= screen_h * _CONTENT_MIN_HEIGHT_RATIO
        and x1 <= screen_w * _CONTENT_HORIZONTAL_EDGE_TOLERANCE
        and x2 >= screen_w * (1 - _CONTENT_HORIZONTAL_EDGE_TOLERANCE)
        and y1 <= screen_h * _CONTENT_TOP_TOLERANCE
        and y2 >= screen_h * (1 - _CONTENT_BOTTOM_TOLERANCE)
    )


def classify_native_web_state(native, screen):
    """Classify an awake WebView or Chrome's measured collapsed projection.

    The collapsed label is intentionally ignored because Chrome localises it.
    ``interactive`` represents the source node's focusability in the normalized
    row contract, while ``focused`` remains a state. A leaf plus near-screen
    bounds separates the projection from Chrome's native pickers and toolbar.
    """
    if _webviews(native):
        return NativeWebState.AWAKE
    collapsed = any(
        is_chrome_package(row.get("package") or "")
        and row.get("raw_child_count") == 0
        and row.get("interactive") is True
        and "focused" in (row.get("states") or ())
        and _covers_content_area(row.get("bounds"), screen)
        for row in native
    )
    return (
        NativeWebState.COLLAPSED_CANDIDATE
        if collapsed
        else NativeWebState.NONE
    )


def has_web_content(native):
    """Whether this screen shows a WebView at all.

    The web reader costs a devtools round trip per page on the device, so a
    screen with no web content must not pay for one.
    """
    return bool(_webviews(native))


def _inside(bounds, center):
    x1, y1, x2, y2 = bounds
    return x1 <= center[0] <= x2 and y1 <= center[1] <= y2


def is_ready(native, web_elements, *, native_state=None, collapsed_confirmed=False):
    """Whether this screen's web content can be read yet.

    A WebView populates its accessibility tree only once the page has loaded —
    measured at 0 descendants two seconds after the screen opened and 262 eight
    seconds later, with nothing done in between. A capture taken in that window
    sees an opaque rectangle, and reporting it as an empty surface would record a
    screen that never existed.

    Parenting is gone by the time the flat list exists, so a WebView's content is
    identified by geometry: a labelled row whose centre lies inside the WebView.
    """
    # A successfully calibrated and placed DOM surface is authoritative even if
    # its native host uses a class other than android.webkit.WebView.
    if any(not element.get("offscreen") for element in web_elements):
        return True
    webviews = _webviews(native)
    if webviews:
        # No CDP rows, so the projection is the reader: a WebView with a
        # labelled element inside it has published something and is loaded.
        return any(
            _inside(webview["bounds"], row["center"])
            for webview in webviews
            for row in native
            if row is not webview and row.get("name") and row.get("bounds")
        )
    if native_state is NativeWebState.COLLAPSED_CANDIDATE:
        # The native shape is only a candidate. A missing/failed transport probe
        # must fail open to today's native-only capture rather than wait.
        return not collapsed_confirmed
    return True


def _same_element(native_row, web_row):
    if (native_row.get("name") or "") != (web_row.get("name") or ""):
        return False
    nx, ny = native_row["center"]
    wx, wy = web_row["center"]
    return abs(nx - wx) <= _SAME_ELEMENT_PX and abs(ny - wy) <= _SAME_ELEMENT_PX


def _dom_identity(row):
    """A hashable address for one element inside one DOM boundary."""
    route = row.get("dom_path")
    if not isinstance(route, list) or not route:
        return None
    normalized = []
    for segment in route:
        if not isinstance(segment, dict):
            return None
        kind = segment.get("kind")
        nodes = segment.get("nodes")
        if not kind or not isinstance(nodes, list):
            return None
        normalized.append((str(kind), tuple(nodes)))
    return (row.get("frame_path", ""), tuple(normalized))


def _web_parents(web_elements):
    """Map each DOM row to its nearest retained ancestor.

    Structural wrappers without a readable or actionable row are intentionally
    skipped: the resulting depth describes the compact document the model sees,
    not every ``div`` in the source page.
    """
    identities = {
        identity for row in web_elements
        if (identity := _dom_identity(row)) is not None
    }
    parents = {}
    for child in web_elements:
        child_id = _dom_identity(child)
        if child_id is None:
            continue
        frame_path, route = child_id
        kind, nodes = route[-1]
        if kind != "element":
            continue
        for length in range(len(nodes) - 1, 0, -1):
            candidate = (
                frame_path,
                route[:-1] + ((kind, nodes[:length]),),
            )
            if candidate in identities:
                parents[child_id] = candidate
                break
    return parents


#: How closely two WebView boxes must coincide to be the same view seen twice.
#: One app reported two WebView nodes 2 px apart — a stale accessibility snapshot
#: alongside the live one.
_SAME_WEBVIEW_PX = 8


def _drop_duplicate_webviews(rows):
    """Collapse a WebView reported twice at the same place.

    An app was seen publishing two WebView nodes with 263 and 262 descendants at
    boxes 2 px apart: a stale accessibility snapshot alongside the live one. Both
    reach the model as unlabelled rows that name the same thing.
    """
    kept = []
    for row in rows:
        if row.get("role") != "webview":
            kept.append(row)
            continue
        twin = any(
            other.get("role") == "webview"
            and all(abs(a - b) <= _SAME_WEBVIEW_PX
                    for a, b in zip(other["bounds"], row["bounds"]))
            for other in kept)
        if not twin:
            kept.append(row)
    return kept


def merge(native, web_elements):
    """One indexed list from both surfaces, deduplicated.

    An element projected into the accessibility tree AND read from the DOM
    arrives twice. The web row survives because it carries the better identity —
    a real selector rather than a label — but it inherits the native centre and
    bounds, because the device's geometry is what a tap is measured against.
    """
    rows = []
    for element in _drop_duplicate_webviews(native):
        rows.append({**element, "surface": element.get("surface", "native")})

    web_elements = list(web_elements or [])
    web_parents = _web_parents(web_elements)
    web_results = {}
    native_twins = set()
    for web_row in web_elements:
        web_id = _dom_identity(web_row)
        twin = next((r for r in rows if r["surface"] == "native"
                     and _same_element(r, web_row)), None)
        if twin is None:
            result = dict(web_row)
            rows.append(result)
            if web_id is not None:
                web_results[web_id] = result
            continue
        merged = {
            **twin,
            **web_row,
            "center": twin["center"],
            "bounds": twin["bounds"],
            # DOM rows have no Android containment or relationship metadata.
            # Empty web defaults must not erase the native evidence that placed
            # this row in the document and makes it re-findable.
            "depth": twin.get("depth", 0),
            "package": twin.get("package", ""),
            "resource_id": twin.get("resource_id", ""),
            "anchors": twin.get("anchors") or {
                "descendant": [], "sibling": []},
        }
        rows[rows.index(twin)] = merged
        if web_id is not None:
            web_results[web_id] = merged
            native_twins.add(web_id)

    for index, row in enumerate(rows, start=1):
        row["index"] = index

    depths = {}

    def depth_for(web_id, visiting=frozenset()):
        if web_id in depths:
            return depths[web_id]
        row = web_results[web_id]
        if web_id in native_twins:
            depth = int(row.get("depth", 0))
        else:
            parent_id = web_parents.get(web_id)
            if parent_id in web_results and parent_id not in visiting:
                parent = web_results[parent_id]
                row["parent_index"] = parent["index"]
                depth = depth_for(parent_id, visiting | {web_id}) + 1
            else:
                depth = 0
            row["depth"] = depth
        depths[web_id] = depth
        return depth

    for web_id in web_results:
        depth_for(web_id)
    return rows
