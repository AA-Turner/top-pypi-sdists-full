"""V3 Selenium-binding textual query helper.

Locates an element via the selector list, extracts a named attribute
(or CSS property / computed value), and optionally applies a regex
over the element's outerHTML when the attribute is text/value.

Mirrors the V2 Selenium textual query mechanism
without reusing V2 code.

Intentional divergences from V2 (see plan Resolved Design Decisions #11):
- ``_safe_value`` skips ``sanitize_visible_text`` (V2-internal helper, not ported).
- ``_rgba_to_name`` returns "" on parse failure (V2 raises ValueError).
- ``populate_attributes`` drops ``location`` and ``custom_attributes_dict``
  cases (rely on V2-internal helpers, not ported).
"""

import colorsys
import re
from typing import Any, Dict, List, Optional

from selenium.webdriver.support.ui import Select, WebDriverWait

from testmu_selenium._helpers.find_element import findElement
from testmu_selenium._helpers.smart_wait import SmartWait


_RGBA_RE = re.compile(
    r"rgba?\s*\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})"
    r"(?:\s*,\s*[0-9.]+)?\s*\)",
    re.I,
)


def _extract_value(element, driver, selected_attribute_name, regex_pattern, return_type):
    """Post-findElement extraction — shared by textualQuery and the healed textual_query verb.

    Applies the img/canvas short-circuit, regex-over-outerHTML for text/value,
    and _coerce. Does NOT call findElement; callers own element location.
    """
    value = _populate_attribute(element, driver, selected_attribute_name)

    if element.tag_name in ("img", "canvas"):
        return _coerce(value, return_type)

    if selected_attribute_name in ("text", "value") and regex_pattern:
        outer_html = element.get_attribute("outerHTML") or ""
        matches = re.findall(regex_pattern, outer_html)
        if matches:
            return _coerce(matches[0], return_type)
        # Regex miss: return empty string, NOT 0.0 even for return_type="number".
        # If a caller wants numeric default-on-miss, they wrap the call.
        return ""

    return _coerce(value, return_type)


def textualQuery(
    driver,
    *,
    selector: List[Dict],
    selected_attribute_name: str,
    regex_pattern: Optional[str] = None,
    description: Optional[str] = None,
    return_type: Optional[str] = None,
):
    """Run a V3 textual query.

    Returns the extracted value (string by default, float when
    ``return_type == "number"``).
    """
    # Resolve ${param}/{{var}} templates before the description is used
    # (findElement / current_action).
    from testmu_selenium._vars import var
    if description:
        description = var(description)

    # AST field is ``selector`` (singular) but holds a List[Dict];
    # findElement's parameter is named ``selectors``. Pass via explicit
    # kwarg to make the naming bridge obvious.
    SmartWait(driver).smart_wait(is_vision=False)
    element = findElement(driver, selectors=selector, description=description)
    return _extract_value(element, driver, selected_attribute_name, regex_pattern, return_type)


# Attributes that _populate_attribute handles locally (the keys of its
# attribute_getters dict + "attributes"). Keep this set co-located with
# _populate_attribute so it is updated whenever the getter map grows.
# Callers use this to decide whether to attempt a local element-based read
# vs falling straight through to the server-snapshot path.
_LOCAL_READ_ATTRS: frozenset = frozenset({
    "tag_name", "text", "value", "id", "class", "href", "src",
    "enabled", "checked", "selected", "aria_label", "role", "displayed",
    "size", "background_color", "color", "font_size", "font_weight",
    "border_radius", "z_index", "opacity", "transform", "aria_expanded",
    "placeholder", "disabled",
    "attributes",  # handled by the early-return branch in _populate_attribute
})


def _populate_attribute(element, driver, requested_attribute: str) -> Any:
    """Dispatch over attribute name.

    Mirrors the V2 populate_attributes logic without sharing code.
    Add new cases here when the V2 attribute list grows.

    Drops V2 cases ``location`` (needs ``get_section_from_bbox``) and
    ``custom_attributes_dict`` (needs ``get_all_element_attributes``) —
    both depend on V2-internal helpers. Raises ValueError for them
    so a regression is loud rather than silent.
    """
    # ``custom_attribute_name`` is V2's alias for ``custom_attributes_dict``.
    if requested_attribute == "custom_attribute_name":
        requested_attribute = "custom_attributes_dict"

    attribute_getters = {
        "tag_name": lambda: element.tag_name or "",
        "text": lambda: _safe_value(element, driver),
        "value": lambda: _safe_value(element, driver),
        "id": lambda: element.get_attribute("id") or "",
        "class": lambda: element.get_attribute("class") or "",
        "href": lambda: element.get_attribute("href") or "",
        "src": lambda: element.get_attribute("src") or "",
        "enabled": lambda: element.is_enabled(),
        "checked": lambda: element.is_selected(),
        "selected": lambda: element.is_selected(),
        "aria_label": lambda: element.get_attribute("aria-label") or "",
        "role": lambda: element.aria_role or "",
        "displayed": lambda: element.is_displayed(),
        "size": lambda: element.size or {},
        "background_color": lambda: _rgba_to_name(
            element.value_of_css_property("background-color")
        ),
        "color": lambda: _rgba_to_name(element.value_of_css_property("color")),
        "font_size": lambda: element.value_of_css_property("font-size") or "",
        "font_weight": lambda: element.value_of_css_property("font-weight") or "",
        "border_radius": lambda: element.value_of_css_property("border-radius") or "",
        "z_index": lambda: element.value_of_css_property("z-index") or "",
        "opacity": lambda: element.value_of_css_property("opacity") or "",
        "transform": lambda: element.value_of_css_property("transform") or "",
        "aria_expanded": lambda: element.get_attribute("aria-expanded") or "",
        "placeholder": lambda: element.get_attribute("placeholder") or "",
        "disabled": lambda: not element.is_enabled(),
    }

    if requested_attribute == "attributes":
        return driver.execute_script(
            "return Array.from(arguments[0].attributes).map(a => a.name);",
            element,
        )

    if requested_attribute in ("location", "custom_attributes_dict"):
        raise ValueError(
            f"Attribute '{requested_attribute}' is not yet supported in V3 "
            f"testmu_selenium.textualQuery. Tracked as a follow-up; if you "
            f"hit this in production, port the V2 source helper into "
            f"this binding as a private utility."
        )

    if requested_attribute not in attribute_getters:
        raise ValueError(f"Unknown attribute: {requested_attribute}")

    return attribute_getters[requested_attribute]()


def _safe_value(element, driver, timeout: float = 2.0) -> str:
    """Return meaningful text/value for any element, falling back gracefully."""
    tag = (element.tag_name or "").lower()
    value = ""

    if tag in ("input", "textarea"):
        try:
            WebDriverWait(driver, timeout).until(
                lambda d: element.get_property("value") not in ("", None)
            )
        except Exception:
            pass
        value = element.get_property("value") or ""
    elif tag == "select":
        sel = Select(element)
        options = sel.options
        all_values = [opt.get_attribute("value") or opt.text for opt in options]
        value = ", ".join(all_values)
    elif element.get_attribute("contenteditable") == "true":
        value = (element.get_property("innerText") or "").strip()

    if value == "":
        value = element.text or ""

    return value


def _rgba_to_name(css_value: Optional[str]) -> str:
    """Convert an rgb()/rgba() CSS string to a basic colour name."""
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


def _coerce(value: Any, return_type: Optional[str]) -> Any:
    """Coerce to float when return_type == 'number', else pass through.

    Empty/None inputs pass through unchanged (e.g., regex-miss returns "").
    Direct conversion is tried first; falls back to digit-filter for
    formatted numerics like "$1,234.56".
    """
    if return_type != "number":
        return value
    if value is None or value == "":
        return value
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(value)
    except (ValueError, TypeError):
        s = str(value)
        is_negative = "-" in s
        filtered = "".join(c for c in s if c.isdigit() or c == ".")
        if not filtered:
            return 0.0
        result = float(filtered)
        return -result if is_negative else result
