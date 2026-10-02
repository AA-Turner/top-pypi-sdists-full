"""Selector strategy → AppiumBy compilation, as per-platform data tables.

The generator emits semantic strategy names only; the compilation to a concrete
`AppiumBy` + query string happens here, where the platform is known from configure().
Adding iOS is adding a column to `_TABLES`, not editing any caller.

Unknown strategies and unshipped platform columns raise. A recorded strategy this
binding version does not know about is producer/binding skew — guessing at it would
silently target the wrong element.
"""
import json
import re
from typing import Callable

from appium.webdriver.common.appiumby import AppiumBy

from testmu_appium._errors import UnknownStrategy, UnsupportedOnPlatform

#: The compound `view_id_text` strategy encodes both halves in one value, as
#: "{view_id}\n{text}". The value is opaque to everything but this module.
_COMPOUND_SEPARATOR = "\n"


#: Characters with a named Java escape. The backslash and the double quote break OUT
#: of the literal; the rest are C0 controls, which are not literal characters in a
#: Java string at all — a raw CR or LF ends the literal mid-string.
_NAMED_ESCAPES = {
    "\\": "\\\\",
    '"': '\\"',
    "\n": "\\n",
    "\r": "\\r",
    "\t": "\\t",
    "\b": "\\b",
    "\f": "\\f",
}

#: The last C0 control character. Everything at or below it (plus DEL) that has no
#: named escape becomes a \\uXXXX sequence.
_LAST_CONTROL = "\x1f"


def _escape(value: str) -> str:
    """Escape a value for embedding in a UiSelector Java string literal.

    Recorded labels legitimately carry control characters — a two-line list row, a
    pasted address, a tab-aligned table cell — and a raw one makes the selector an
    invalid Java string, which the UiAutomator2 parser rejects with an
    invalid-selector exception rather than a miss.
    """
    rendered = []
    for character in str(value):
        named = _NAMED_ESCAPES.get(character)
        if named is not None:
            rendered.append(named)
        elif character <= _LAST_CONTROL or character == "\x7f":
            rendered.append(f"\\u{ord(character):04x}")
        else:
            rendered.append(character)
    return "".join(rendered)


def _ui_selector(**clauses: str) -> str:
    """Render `new UiSelector().<clause>("<escaped>")...` in the given clause order."""
    rendered = "".join(
        f'.{name}("{_escape(value)}")' for name, value in clauses.items() if value
    )
    return f"new UiSelector(){rendered}"


def _android_text(value: str):
    return AppiumBy.ANDROID_UIAUTOMATOR, _ui_selector(text=value)


def _android_view_id(value: str):
    """Match a view id verbatim.

    `resourceId` compares against the node's own view-id string, so it matches both
    an Android resource name (`com.app:id/go`) and a bare identifier. Toolkits that
    render into a single native view — Flutter, React Native — set the id from a
    developer-supplied string that is not an Android resource, and `AppiumBy.ID`
    resolves none of those.
    """
    return AppiumBy.ANDROID_UIAUTOMATOR, _ui_selector(resourceId=value)


def _android_view_id_text(value: str):
    view_id, separator, text = value.partition(_COMPOUND_SEPARATOR)
    if not separator:
        # A producer that recorded no text half leaves a bare resource id; the
        # compound selector degrades to its resource-id clause rather than
        # matching on an empty text (which matches nothing).
        return AppiumBy.ANDROID_UIAUTOMATOR, _ui_selector(resourceId=view_id)
    return AppiumBy.ANDROID_UIAUTOMATOR, _ui_selector(resourceId=view_id, text=text)


#: XML attribute each recorded clause matches, for the XPath relational forms.
_XPATH_ATTR = {"text": "@text", "description": "@content-desc",
               "resource_id": "@resource-id"}

#: What makes an ancestor a plausible target. Mirrors the attributes the recorder
#: treats as interactive, minus `focused`, which is the state of one element at one
#: moment rather than a property of the element.
_INTERACTIVE_ANCESTOR = " or ".join(
    f"@{attr}='true'"
    for attr in ("clickable", "long-clickable", "checkable", "scrollable")
)


def _xpath_literal(value: str) -> str:
    """Quote a value for XPath 1.0, which has no escape character.

    A value containing both quote kinds has to be assembled with concat().
    """
    if "'" not in value:
        return f"'{value}'"
    if '"' not in value:
        return f'"{value}"'
    parts = ", ".join(
        f'"{chunk}"' if chunk == "'" else f"'{chunk}'"
        for chunk in re.split(r"(')", value) if chunk
    )
    return f"concat({parts})"


def _xpath_predicate(clauses: dict) -> str:
    """`@attr='value'` for every recorded clause, ANDed.

    The relational forms match a shape rather than one attribute, so every clause
    the recorder captured is applied: a card's stepper and its quantity readout
    share a view id and are told apart only by the label beside it.

    Values are compared through `normalize-space()` because the recorder stores a
    label as one line while the app keeps whatever padding it rendered with —
    `content-desc=" Top picks for you"` was measured — and an exact comparison
    against the padded attribute matches nothing.
    """
    rendered = []
    for clause, value in clauses.items():
        attr = _XPATH_ATTR.get(clause)
        if attr is None:
            raise UnknownStrategy(
                f"relational clause {clause!r}", "android", set(_XPATH_ATTR))
        rendered.append(f"normalize-space({attr})={_xpath_literal(value)}")
    return " and ".join(rendered)


def _android_sibling_of(value: str):
    """Match an element by its own attributes plus a label in a neighbouring subtree.

    The shape is a grid of cards: every card's button carries the same recycled
    view id, and the only thing saying WHICH card is the product name — which is
    not a descendant of the button and not a direct sibling of it either, but
    several containers away in another branch of the card.

    `ancestor::*[.//<target>][1]` is the nearest ancestor of the label whose
    subtree holds a target-shaped element: the smallest container the two share.
    Climbing a recorded number of levels instead would break as soon as the app
    added a wrapper.
    """
    spec = json.loads(value)
    anchor = spec["anchor"]
    target = _xpath_predicate(spec.get("target") or {})
    if not target:
        raise UnknownStrategy(
            "sibling_of carrying no target clause", "android", set(_XPATH_ATTR))
    label = _xpath_predicate({anchor["clause"]: anchor["value"]})
    return (
        AppiumBy.XPATH,
        f"//*[{label}]/ancestor::*[.//*[{target}]][1]//*[{target}]",
    )


def _android_ancestor_of(value: str):
    """Match the nearest interactive ancestor of a screen-unique label.

    The shape is a row that carries no attribute of its own and is labelled
    entirely by child views. UiSelector cannot express it: `childSelector`
    returns the matched descendant rather than the row containing it, and
    `fromParent` searches a parent's subtree without being able to return the
    parent. XPath's `ancestor::` axis is the only form that walks upward.

    `ancestor::` is a reverse axis, so `[1]` is the NEAREST matching ancestor: a
    clickable row still wins over the scrollable list that contains it.
    """
    spec = json.loads(value)
    anchor = spec["anchor"]
    label = _xpath_predicate({anchor["clause"]: anchor["value"]})
    return (
        AppiumBy.XPATH,
        f"//*[{label}]/ancestor::*[{_INTERACTIVE_ANCESTOR}][1]",
    )


def _android_attrs_xpath(value: str):
    """Match an element by its own attributes, searched across every window.

    Carries the same evidence as `view_id`, `accessibility_id` and `text`; only
    the search space differs. A UiSelector reads the ACTIVE window, and Compose
    and React Native render a dropdown, menu or dialog into a window of their
    own — so a producer reading a page source that spans windows records an
    element no UiSelector form can then find. XPath is evaluated over that same
    source, which makes this the only Android strategy able to reach one.

    Every recorded clause is ANDed, so this is at least as specific as any
    single-attribute strategy above it and often more.
    """
    spec = json.loads(value)
    target = _xpath_predicate(spec.get("target") or {})
    if not target:
        # `//*[]` is not an XPath, and a bare `//*` would match the whole screen.
        raise UnknownStrategy(
            "attrs_xpath carrying no clause", "android", set(_XPATH_ATTR))
    return AppiumBy.XPATH, f"//*[{target}]"


def _android_child_text(value: str):
    """A clickable container identified by the text of a descendant.

    A list row is often a clickable layout with no id, text or content-desc of its
    own, labelled entirely by a child TextView. `childSelector` reaches it: match the
    clickable ancestor whose descendant carries the recorded text.
    """
    child = _ui_selector(text=value)
    return (
        AppiumBy.ANDROID_UIAUTOMATOR,
        f"new UiSelector().clickable(true).childSelector({child})",
    )


# ── iOS ──────────────────────────────────────────────────────────────────────
#
# iOS carries no developer-assigned id separate from its label: `name` is the
# accessibilityIdentifier when the developer set one and a copy of the label when
# they did not. So there is no `view_id` row here, and no compound `view_id_text` —
# the pair that makes those worth having on Android does not exist.
#
# What iOS has instead is two query languages, predicate and class chain, which
# pin attributes the simple strategies cannot reach. They are strategies in their
# own right rather than an implementation detail, because a healed or hand-written
# selector legitimately arrives as one.

#: XCUIElement attribute each recorded clause matches. The iOS parser publishes
#: these clause names; Android's `_XPATH_ATTR` publishes its own. The two never
#: mix — a recorded selector is compiled by the column that produced it.
_IOS_XPATH_ATTR = {"label": "@label", "name": "@name", "value": "@value"}

#: Element types that can plausibly BE the target of a tap, for the relational
#: forms. Deliberately narrower than the parser's admission set: that decides what
#: the model may be shown, this decides what an anchor is allowed to resolve to.
#: iOS publishes no `clickable` attribute, so the type is the only signal there is.
_IOS_INTERACTIVE_ANCESTOR = " or ".join(
    f"@type='XCUIElementType{kind}'"
    for kind in ("Button", "Cell", "Link", "Switch", "TextField", "SecureTextField",
                 "SearchField", "MenuItem", "Tab", "TabBar", "SegmentedControl")
)


def _predicate_literal(value: str) -> str:
    """Quote a value for an NSPredicate string comparison.

    NSPredicate string literals are double-quoted, so a label containing a quote
    or a backslash ends the literal early and the driver rejects the whole query
    as malformed — a parse error rather than a miss, which is worse to diagnose.
    """
    escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _ios_accessibility_id(value: str):
    """Match on `name` — the accessibilityIdentifier where the developer set one.

    ACCESSIBILITY_ID is the direct form and the fastest lookup iOS offers. React
    Native's `testID` surfaces here rather than as any kind of resource id, which
    is why this outranks everything else on an RN screen.
    """
    return AppiumBy.ACCESSIBILITY_ID, value


def _ios_text(value: str):
    """Match the element a person would call by this text.

    iOS splits what Android keeps in one attribute: `label` is the accessibility
    text and `value` is the current contents. A recorded label may have come from
    either, and the recorder does not preserve which, so both are compared. `name`
    is included because it falls back to the label whenever the developer assigned
    no identifier — omitting it loses every unlabelled-but-named element.
    """
    literal = _predicate_literal(value)
    return (
        AppiumBy.IOS_PREDICATE,
        f"label == {literal} OR name == {literal} OR value == {literal}",
    )


def _ios_predicate(value: str):
    """A recorded NSPredicate, passed through as written."""
    return AppiumBy.IOS_PREDICATE, value


def _ios_class_chain(value: str):
    """A recorded class chain, passed through as written."""
    return AppiumBy.IOS_CLASS_CHAIN, value


def _ios_xpath_predicate(clauses: dict) -> str:
    """`@attr='value'` for every recorded clause, ANDed.

    Compared through `normalize-space()` for the same reason Android does: an app
    renders its label with whatever padding it likes while the recorder stores one
    trimmed line, and an exact comparison against the padded attribute matches
    nothing.
    """
    rendered = []
    for clause, value in clauses.items():
        attr = _IOS_XPATH_ATTR.get(clause)
        if attr is None:
            raise UnknownStrategy(
                f"relational clause {clause!r}", "ios", set(_IOS_XPATH_ATTR))
        rendered.append(f"normalize-space({attr})={_xpath_literal(value)}")
    return " and ".join(rendered)


def _ios_ancestor_of(value: str):
    """Match the nearest tappable ancestor of a screen-unique label.

    XPath, not class chain: a class chain only ever descends, and this shape needs
    to walk UP from a label to the row that carries it. iOS XPath is slower than a
    class chain, which is why this strategy is ranked below the ones that name the
    element directly and is only reached when they were ambiguous.
    """
    spec = json.loads(value)
    anchor = spec["anchor"]
    label = _ios_xpath_predicate({anchor["clause"]: anchor["value"]})
    return (
        AppiumBy.XPATH,
        f"//*[{label}]/ancestor::*[{_IOS_INTERACTIVE_ANCESTOR}][1]",
    )


def _ios_sibling_of(value: str):
    """Match an element by its own attributes plus a label sharing a container.

    The grid-card shape: every card's button is identical and only the product name
    says which card. `ancestor::*[.//<target>][1]` is the smallest container holding
    both, so it works however many wrappers the app puts between them.
    """
    spec = json.loads(value)
    anchor = spec["anchor"]
    target = _ios_xpath_predicate(spec.get("target") or {})
    if not target:
        raise UnknownStrategy(
            "sibling_of carrying no target clause", "ios", set(_IOS_XPATH_ATTR))
    label = _ios_xpath_predicate({anchor["clause"]: anchor["value"]})
    return (
        AppiumBy.XPATH,
        f"//*[{label}]/ancestor::*[.//*[{target}]][1]//*[{target}]",
    )


#: platform → strategy name → compiler.
_TABLES: dict[str, dict[str, Callable[[str], tuple[str, str]]]] = {
    "android": {
        "accessibility_id": lambda v: (AppiumBy.ACCESSIBILITY_ID, v),
        "view_id": _android_view_id,
        "view_id_text": _android_view_id_text,
        "text": _android_text,
        "child_text": _android_child_text,
        "ancestor_of": _android_ancestor_of,
        "sibling_of": _android_sibling_of,
        "attrs_xpath": _android_attrs_xpath,
    },
    "ios": {
        "accessibility_id": _ios_accessibility_id,
        "text": _ios_text,
        "predicate": _ios_predicate,
        "class_chain": _ios_class_chain,
        "ancestor_of": _ios_ancestor_of,
        "sibling_of": _ios_sibling_of,
    },
}

#: Portable textual-query field → Appium attribute name. A missing field is not
#: platform skew: it tells textual_query to keep its legacy analyzer path.
_SELECTED_ATTRIBUTES = {
    "android": {
        "text": "text",
        "content_desc": "content-desc",
        "hint": "hint",
        "resource_id": "resource-id",
    },
    "ios": {
        "text": "value",
        "content_desc": "name",
    },
}


def _table(platform: str) -> dict[str, Callable[[str], tuple[str, str]]]:
    platform = (platform or "").lower()
    if platform not in _TABLES:
        raise UnsupportedOnPlatform(f"selector strategies for platform {platform!r}", platform)
    table = _TABLES[platform]
    if not table:
        raise UnsupportedOnPlatform("ios tables not shipped", platform)
    return table


def known_strategies(platform: str) -> set:
    """The strategy names this binding can compile for the given platform."""
    return set(_table(platform))


def selected_attribute(field: str, platform: str) -> str | None:
    """Resolve a portable textual-query field to Appium's platform attribute."""
    platform = (platform or "").lower()
    fields = _SELECTED_ATTRIBUTES.get(platform)
    if fields is None:
        raise UnsupportedOnPlatform(
            f"textual_query local attributes for platform {platform!r}", platform
        )
    return fields.get(field)


def compile_selector(selector: dict, platform: str) -> tuple[str, str]:
    """Compile one recorded selector dict into an (AppiumBy, value) pair.

    The dict is the AST wire shape: the locator value lives under the `selector` key
    and `strategy` names what identifies the element. `isXPath` rides along for legacy
    web consumers and is ignored whenever `strategy` is present.
    """
    table = _table(platform)
    strategy = selector.get("strategy")
    if strategy not in table:
        raise UnknownStrategy(str(strategy), platform, table)
    return table[strategy](selector.get("selector", ""))


def order_by_score(selectors) -> list:
    """Recorded selectors, highest score first; ties keep their recorded order.

    The recorded order already encodes the producer's ambiguity demotions, so the
    sort must be stable.
    """
    return sorted(selectors or [], key=lambda s: -int(s.get("score", 0) or 0))


def _android_descriptor(descriptor: dict) -> tuple[str, str]:
    """Compile an Android perception descriptor into a fresh strict lookup.

    Used after heal resolves a `dom_index`: the parsed entry is a static dict, so the
    binding rebuilds a real query from the element's source attributes and requires
    exactly one live match. Clause preference goes most-specific first — a
    resource-id + text pair identifies a row far more tightly than a class name.

    The compiled lookup is only as specific as the attributes the element carries, so
    repeated resource-ids (RecyclerView rows) still resolve to several live matches.
    `disambiguate_by_centre` resolves those from the bounds/centre the same descriptor
    retained.
    """
    resource_id = (descriptor.get("resource_id") or "").strip()
    text = (descriptor.get("text") or "").strip()
    content_desc = (descriptor.get("content_desc") or "").strip()
    cls = (descriptor.get("cls") or "").strip()

    if resource_id and text:
        return AppiumBy.ANDROID_UIAUTOMATOR, _ui_selector(resourceId=resource_id, text=text)
    if resource_id:
        return AppiumBy.ANDROID_UIAUTOMATOR, _ui_selector(resourceId=resource_id)
    if content_desc:
        return AppiumBy.ACCESSIBILITY_ID, content_desc
    if cls and text:
        return AppiumBy.ANDROID_UIAUTOMATOR, _ui_selector(className=cls, text=text)
    if text:
        return AppiumBy.ANDROID_UIAUTOMATOR, _ui_selector(text=text)
    if cls:
        return AppiumBy.ANDROID_UIAUTOMATOR, _ui_selector(className=cls)

    raise UnknownStrategy(
        "descriptor with no identifying attribute", "android", known_strategies("android")
    )


def _ios_descriptor(descriptor: dict) -> tuple[str, str]:
    """Compile an iOS perception descriptor into a fresh strict lookup.

    The mirror of `_android_descriptor`, used after heal resolves a `dom_index`.
    Clause preference is most-specific first, and on iOS that means the identifier
    before the label: `name` is the developer's own handle whenever they set one,
    while `label` is user-visible text that localizes and gets reworded.

    Pairing the type with the label is what separates the two controls that share
    a label on the same screen — a "Done" button and the "Done" text beside it.
    As on Android the compiled lookup is only as specific as the attributes the
    element carries, so repeated cells still resolve to several live matches and
    `disambiguate_by_centre` settles those from the retained geometry.
    """
    # The CONTRACT's field names, not iOS's attribute names, and the two do not
    # line up: iOS's `name` is its accessibility identifier, which the parser
    # publishes as `content_desc` because that is the field the accessibility_id
    # strategy compiles from. `name` on the contract is the display label.
    name = (descriptor.get("content_desc") or "").strip()
    label = (descriptor.get("name") or "").strip()
    value = (descriptor.get("text") or "").strip()
    cls = (descriptor.get("cls") or "").strip()

    if name:
        # The producer measured how many elements each clause matches across
        # the WHOLE document (`query_matches`) — including nodes the parser
        # admitted no row for, which is exactly where a duplicate identifier
        # hides. When the bare identifier is measured ambiguous and pinning
        # the type is measured unique, compile the compound; geometry can
        # still settle what neither clause can, but heal fires precisely when
        # the layout has shifted, which is when geometry is weakest.
        matches = descriptor.get("query_matches") or {}
        if cls and matches.get("content_desc", 1) > 1 \
                and matches.get("content_desc+cls", 0) == 1:
            return (
                AppiumBy.IOS_PREDICATE,
                f"type == {_predicate_literal(cls)} "
                f"AND name == {_predicate_literal(name)}",
            )
        return AppiumBy.ACCESSIBILITY_ID, name
    if cls and label:
        return (
            AppiumBy.IOS_PREDICATE,
            f"type == {_predicate_literal(cls)} AND label == {_predicate_literal(label)}",
        )
    if label:
        return AppiumBy.IOS_PREDICATE, f"label == {_predicate_literal(label)}"
    if cls and value:
        return (
            AppiumBy.IOS_PREDICATE,
            f"type == {_predicate_literal(cls)} AND value == {_predicate_literal(value)}",
        )
    if cls:
        return AppiumBy.IOS_PREDICATE, f"type == {_predicate_literal(cls)}"

    raise UnknownStrategy(
        "descriptor with no identifying attribute", "ios", known_strategies("ios")
    )


_DESCRIPTOR_COMPILERS = {
    "android": _android_descriptor,
    "ios": _ios_descriptor,
}


def compile_descriptor(descriptor: dict, platform: str) -> tuple[str, str]:
    """Compile a retained perception descriptor through the platform column."""
    platform = (platform or "").lower()
    compiler = _DESCRIPTOR_COMPILERS.get(platform)
    if compiler is None:
        raise UnsupportedOnPlatform("descriptor lookup", platform)
    return compiler(descriptor)


def _android_picker_options(*, text: str = "", list_resource_id: str = ""):
    """Compile the two ways a native picker option may be addressed."""
    if text:
        return AppiumBy.ANDROID_UIAUTOMATOR, _ui_selector(text=text)
    if list_resource_id:
        child = "new UiSelector().clickable(true)"
        return (
            AppiumBy.ANDROID_UIAUTOMATOR,
            _ui_selector(resourceId=list_resource_id) + f".childSelector({child})",
        )
    raise ValueError("picker option lookup requires text or list_resource_id")


def _ios_picker_options(*, text: str = "", list_resource_id: str = ""):
    """Compile the two ways an iOS picker option may be addressed.

    iOS presents a choice in shapes Android does not: an action sheet or alert of
    buttons, and a PickerWheel whose options are a spun value rather than a list of
    tappable rows. Matching on the option's own text covers both — a sheet button
    carries it as `label`, a wheel entry as `value`.

    `list_resource_id` keeps the shared signature and carries something different
    here: iOS has no resource ids, so the picker row names the container by TYPE
    ("XCUIElementTypeSheet") and this compiles a class chain to the buttons inside
    it. A caller that passes an identifier instead still works — the chain matches
    on `name` when the value does not look like an element type.
    """
    if text:
        literal = _predicate_literal(text)
        return AppiumBy.IOS_PREDICATE, f"label == {literal} OR value == {literal}"
    if list_resource_id:
        if list_resource_id.startswith("XCUIElementType"):
            return (
                AppiumBy.IOS_CLASS_CHAIN,
                f"**/{list_resource_id}/**/XCUIElementTypeButton",
            )
        return (
            AppiumBy.IOS_CLASS_CHAIN,
            f'**/XCUIElementTypeAny[`name == {_predicate_literal(list_resource_id)}`]'
            f'/**/XCUIElementTypeButton',
        )
    raise ValueError("picker option lookup requires text or list_resource_id")


_PICKER_OPTION_COMPILERS = {
    "android": _android_picker_options,
    "ios": _ios_picker_options,
}


def compile_picker_options(
    platform: str,
    *,
    text: str = "",
    list_resource_id: str = "",
) -> tuple[str, str]:
    """Compile a picker-option query using the selected platform column."""
    platform = (platform or "").lower()
    compiler = _PICKER_OPTION_COMPILERS.get(platform)
    if compiler is None:
        raise UnsupportedOnPlatform("picker option lookup", platform)
    return compiler(text=text, list_resource_id=list_resource_id)


#: How far a live element's centre may sit from the descriptor's recorded centre and
#: still be considered the same element, as a fraction of the descriptor's own box.
#: A row that scrolled by a fraction of its own height is the same row; one a whole
#: row-height away is its neighbour.
_CENTRE_TOLERANCE = 0.5


def _centre_of(element):
    """The live element's centre, or None when its geometry cannot be read."""
    try:
        rect = element.rect
        return (
            int(rect["x"]) + int(rect["width"]) // 2,
            int(rect["y"]) + int(rect["height"]) // 2,
        )
    except Exception:  # noqa: BLE001 — an unreadable element simply cannot be scored
        return None


def disambiguate_by_centre(matches, descriptor):
    """Pick the match sitting where the descriptor said, or None.

    A compiled descriptor is only as specific as the attributes the element carries,
    and RecyclerView rows routinely share one resource-id with no text of their own,
    so the lookup resolves to every row on screen. The descriptor retained the bounds
    and centre from the SAME parse the server's dom_index refers to, which names WHICH
    of those rows was meant.

    Returns None rather than a best guess whenever the answer is not unambiguous:
    no recorded centre, no readable geometry, nothing inside the tolerance, or a tie.
    """
    recorded = descriptor.get("centre") or descriptor.get("center")
    bounds = descriptor.get("bounds")
    if not recorded or len(recorded) != 2 or not bounds or len(bounds) != 4:
        return None

    width, height = abs(bounds[2] - bounds[0]), abs(bounds[3] - bounds[1])
    if width <= 0 or height <= 0:
        return None
    limit_x, limit_y = width * _CENTRE_TOLERANCE, height * _CENTRE_TOLERANCE

    within = []
    for element in matches:
        centre = _centre_of(element)
        if centre is None:
            continue
        dx, dy = abs(centre[0] - recorded[0]), abs(centre[1] - recorded[1])
        if dx <= limit_x and dy <= limit_y:
            within.append((dx + dy, element))

    if len(within) != 1:
        # Zero means the recorded position matches nothing on screen; more than one
        # means the rows overlap enough that position cannot separate them either.
        return None
    return within[0][1]
