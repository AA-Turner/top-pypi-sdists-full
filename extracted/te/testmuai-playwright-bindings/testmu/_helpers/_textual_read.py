"""Async local attribute extraction for V3 textual_query (Playwright).

Ports selenium-python's textmu_selenium._helpers.textual_query (sync Selenium
WebElement API) to async Playwright Locator/ElementHandle semantics.

Consumed only by the V3 textual_query locate-then-read path inside
``vision._textual_query_v3``. No V4 code imports this module.

Intentional parity gaps (documented; not bugs):
- ``role``: explicit-attr only (``get_attribute("role")``). Playwright has no
  synchronous computed aria-role without CDP; selenium reads the implicit role
  off ``aria_role``. Explicit-only covers the common authored case.
- ``size``: exposes ``{width, height}`` floats from ``bounding_box()``.
  Selenium returns integer-ish ``{width, height}`` (WebDriver Size object).
  ``None`` is returned as ``{}`` when the element is not visible.
- ``_rgba_to_name`` HSV buckets: ported verbatim from selenium for cross-binding
  output parity. Bucket thresholds differ from the V2 source — intentional.
"""

import colorsys
import logging
import re
from typing import Any, Optional

_log = logging.getLogger(__name__)

_RGBA_RE = re.compile(
    r"rgba?\s*\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})"
    r"(?:\s*,\s*[0-9.]+)?\s*\)",
    re.I,
)


def _rgba_to_name(css_value: Optional[str]) -> str:
    """Convert an rgb()/rgba() CSS string to a basic colour name.

    Returns "" on parse failure or empty/None input. HSV-bucket thresholds
    are verbatim from selenium-python ``_rgba_to_name`` for cross-binding output
    parity (deliberately diverges from the V2 source).

    Args:
        css_value: A CSS color string like ``"rgb(255,0,0)"`` or ``"rgba(0,0,255,0.5)"``.

    Returns:
        A basic colour name ("red", "orange", "yellow", "green", "blue",
        "purple", "white", "black"), or "" when the input cannot be parsed.
    """
    if not css_value:
        return ""
    match = _RGBA_RE.fullmatch(css_value.strip())
    if not match:
        return ""
    r, g, b = (int(match.group(i)) for i in range(1, 4))
    if any(v > 255 for v in (r, g, b)):
        return ""
    rn, gn, bn = r / 255, g / 255, b / 255
    h, s, v = colorsys.rgb_to_hsv(rn, gn, bn)
    if s < 0.05:
        return "white" if v > 0.75 else "black"
    hue_deg = h * 360
    if 0 <= hue_deg < 15 or hue_deg >= 345:
        return "red"
    if 15 <= hue_deg < 45:
        return "orange"
    if 45 <= hue_deg < 70:
        return "yellow"
    if 70 <= hue_deg < 170:
        return "green"
    if 170 <= hue_deg < 260:
        return "blue"
    if 260 <= hue_deg < 320:
        return "purple"
    return "red"


async def _safe_value(el) -> str:
    """Return meaningful text/value for any element, falling back gracefully.

    Read path:
    - input/textarea → ``input_value()``
    - select → evaluate JS to enumerate option values/text
    - contenteditable → ``innerText`` via evaluate
    - else → ``inner_text()`` (rendered visible text; parity with Selenium .text)

    Args:
        el: A Playwright Locator (or anything with the same async API surface).

    Returns:
        A string, possibly empty.
    """
    tag = (await el.evaluate("e => e.tagName") or "").lower()
    value = ""

    if tag in ("input", "textarea"):
        try:
            value = await el.input_value() or ""
        except Exception:
            value = ""
    elif tag == "select":
        try:
            value = await el.evaluate(
                "e => Array.from(e.options).map(o => o.value || o.text).join(', ')"
            ) or ""
        except Exception:
            value = ""
    else:
        try:
            ce = await el.evaluate("e => e.getAttribute('contenteditable')")
            if ce == "true":
                value = (await el.evaluate("e => e.innerText") or "").strip()
        except Exception:
            pass

    if value == "":
        try:
            # inner_text() returns only rendered visible text (parity with
            # Selenium's .text); text_content() would include hidden descendants.
            value = await el.inner_text() or ""
        except Exception:
            value = ""

    return value


async def _populate_attribute(el, requested_attribute: str) -> Any:
    """Dispatch over attribute name and return the raw value for ``el``.

    Mirrors selenium's ``_populate_attribute`` (``textual_query.py``) using
    Playwright async semantics. Computed CSS properties use
    ``getComputedStyle(e).getPropertyValue(...)`` via ``evaluate``; HTML
    attributes use ``get_attribute``; states use ``is_enabled``/``is_checked``/
    ``is_visible``.

    Drops V2 cases ``location`` and ``custom_attributes_dict`` — both need
    V2-internal helpers. Raises ``ValueError`` for them (loud-not-silent parity
    with selenium).

    Args:
        el: Playwright Locator.
        requested_attribute: Attribute name string (e.g. "color", "text", "enabled").

    Returns:
        Extracted value (str, bool, float, list, or dict). Type depends on attribute.

    Raises:
        ValueError: For ``location``, ``custom_attributes_dict``, or unknown attributes.
    """
    # Normalise alias used in V2.
    if requested_attribute == "custom_attribute_name":
        requested_attribute = "custom_attributes_dict"

    if requested_attribute in ("location", "custom_attributes_dict"):
        raise ValueError(
            f"Attribute '{requested_attribute}' is not yet supported in V3 "
            f"testmu (Playwright) textual_query. Tracked as a follow-up; if you "
            f"hit this in production, port the V2 source helper into "
            f"this binding as a private utility."
        )

    # Computed CSS properties — MUST use getPropertyValue (not bracket access).
    _CSS_MAP = {
        "color": "color",
        "background_color": "background-color",
        "font_size": "font-size",
        "font_weight": "font-weight",
        "border_radius": "border-radius",
        "z_index": "z-index",
        "opacity": "opacity",
        "transform": "transform",
    }

    if requested_attribute in _CSS_MAP:
        css_prop = _CSS_MAP[requested_attribute]
        raw = await el.evaluate(
            f"e => getComputedStyle(e).getPropertyValue('{css_prop}')"
        )
        if requested_attribute in ("color", "background_color"):
            return _rgba_to_name(raw or "")
        return raw or ""

    # HTML attributes.
    _ATTR_MAP = {
        "id": "id",
        "class": "class",
        "href": "href",
        "src": "src",
        "aria_label": "aria-label",
        "aria-label": "aria-label",
        "aria_expanded": "aria-expanded",
        "aria-expanded": "aria-expanded",
        "placeholder": "placeholder",
        "title": "title",
    }

    if requested_attribute in _ATTR_MAP:
        return await el.get_attribute(_ATTR_MAP[requested_attribute]) or ""

    # States.
    if requested_attribute == "enabled":
        return await el.is_enabled()
    if requested_attribute in ("checked", "selected"):
        return await el.is_checked()
    if requested_attribute == "displayed":
        return await el.is_visible()
    if requested_attribute == "disabled":
        return not (await el.is_enabled())

    # tag_name.
    if requested_attribute == "tag_name":
        return (await el.evaluate("e => e.tagName") or "").lower()

    # role — explicit HTML attribute only (no computed implicit role via CDP).
    # Parity gap: selenium reads the computed role (e.g. <button> → "button");
    # PW would need CDP Accessibility.getComputedRoleForNode for that.
    if requested_attribute == "role":
        return await el.get_attribute("role") or ""

    # text / value — delegates to _safe_value.
    if requested_attribute in ("text", "value"):
        return await _safe_value(el)

    # size — bounding_box floats; {} when element not visible.
    if requested_attribute == "size":
        bb = await el.bounding_box()
        if bb is None:
            return {}
        return {"width": bb["width"], "height": bb["height"]}

    # outerHTML.
    if requested_attribute == "outerHTML":
        return await el.evaluate("e => e.outerHTML") or ""

    # attributes — list of attribute names.
    if requested_attribute == "attributes":
        return await el.evaluate("e => Array.from(e.attributes).map(a => a.name)") or []

    # Presence query: "does element have attribute X?" (mirrors selenium's
    # textual_query has_ branch). The producer emits the raw HTML attribute
    # name after the "has_" prefix (e.g. 'has_aria-expanded' -> 'aria-expanded'),
    # so no underscore->hyphen conversion is applied. get_attribute returns None
    # iff the attribute is absent, making `is not None` the presence test.
    if requested_attribute.startswith("has_"):
        base_attr = requested_attribute[4:]
        return (await el.get_attribute(base_attr)) is not None

    raise ValueError(f"Unknown attribute: {requested_attribute!r}")


async def _extract_value(
    el,
    selected_attribute_name: str,
    regex_pattern: Optional[str],
    return_type: Optional[str],
) -> Any:
    """Post-locate extraction — shared entry-point for the V3 locate-then-read path.

    Applies the img/canvas short-circuit, regex-over-outerHTML for text/value,
    and ``_coerce_textual_value``. Does NOT locate the element; callers own that.

    ``regex_pattern`` is accepted for selenium-parity-readiness but ``vision.
    _textual_query_v3`` currently passes ``None`` (the public ``textual_query``
    signature cannot be extended without touching the protected 313-339 dispatcher
    range; deferred to a coordinated change).

    Args:
        el: Playwright Locator (must already point at the located element).
        selected_attribute_name: Attribute to extract (e.g. "color", "text").
        regex_pattern: Optional regex applied to outerHTML for text/value attrs.
        return_type: Coercion hint; "number" triggers float coercion.

    Returns:
        Extracted and coerced value.

    Raises:
        ValueError: For unsupported attributes (``location``,
            ``custom_attributes_dict``, unknown names).
    """
    from testmu._helpers.vision import _coerce_textual_value

    value = await _populate_attribute(el, selected_attribute_name)

    # img/canvas: skip regex; coerce and return.
    tag = (await el.evaluate("e => e.tagName") or "").lower()
    if tag in ("img", "canvas"):
        return _coerce_textual_value(value, return_type)

    # text/value + regex: apply over outerHTML.
    if selected_attribute_name in ("text", "value") and regex_pattern:
        outer_html = await el.evaluate("e => e.outerHTML") or ""
        matches = re.findall(regex_pattern, outer_html)
        if matches:
            return _coerce_textual_value(matches[0], return_type)
        # Regex miss: return empty string per selenium parity.
        return ""

    return _coerce_textual_value(value, return_type)
