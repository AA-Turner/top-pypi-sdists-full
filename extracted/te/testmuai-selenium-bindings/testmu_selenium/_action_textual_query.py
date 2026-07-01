"""High-level textual_query action — find element, extract attribute value, heal on failure."""
import json
import time
from typing import List, Dict, Optional

from selenium.common.exceptions import NoSuchElementException

from testmu_selenium._action_engine import _ActionSpec, _run_action
from testmu_selenium._heal import Heal
from testmu_selenium._helpers.find_element import findElement
from testmu_selenium._helpers.snapshot import capture_a11y_dom_snapshot
from testmu_selenium._helpers.smart_wait import SmartWait
from testmu_selenium._helpers.textual_query import _coerce, _extract_value
from testmu_selenium._helpers._coordinate_resolver import resolve_coordinate_read


def _textual_query_runner(element, ctx):
    return _extract_value(
        element,
        ctx['driver'],
        ctx['selected_attribute_name'],
        ctx.get('regex_pattern'),
        ctx.get('return_type'),
    )


# Coordinate-tier fallback. Heal cascade exhausted all selector-based tiers
# and returned viewport pixel coords. Use the READ-tuned resolver (no
# interactable up-walk, open-shadow pierce, iframe/canvas/video bail) to pick
# the EXACT direct-hit element, then read locally via WebElement semantics.
# Unlike click/type, there is no interaction — extraction only.
# This runner is shared by BOTH the selector-less DESKTOP_LOCATE_FULL_PAGE_READ
# path AND the selector-present coordinate fallback (same V3 verb; no V4 risk).
def _textual_query_coord_runner(driver, x, y, ctx):
    resolved = resolve_coordinate_read(driver, x, y)
    if resolved is None:
        # iframe/frame/canvas/video hit, closed-shadow/cross-document root, or no
        # xpath verified → cannot read locally; raise so the wrapper routes to
        # the server-snapshot fallback.
        raise NoSuchElementException(
            f"read-resolver returned no element at ({x}, {y}); routing to server fallback."
        )
    element = findElement(driver, [{"selector": resolved.xpath, "isXPath": True}])
    return _extract_value(
        element,
        driver,
        ctx['selected_attribute_name'],
        ctx.get('regex_pattern'),
        ctx.get('return_type'),
    )


# Recoverable set inherits the engine default — see _DEFAULT_RECOVERABLE
# in _action_engine. Keeps textual_query in lockstep with future additions.
_TEXTUAL_QUERY_SPEC = _ActionSpec(
    runner=_textual_query_runner,
    coord_runner=_textual_query_coord_runner,
)

# Selector-less server read: settle + retry to absorb late layout settling (an in-flight
# #anchor scroll / reflow mislands the viewport rect, making the snapshot read flaky).
_DIRECT_READ_ATTEMPTS = 3
_DIRECT_READ_SETTLE_SECS = 0.5


def _direct_textual_read(
    driver,
    *,
    selected_attribute_name: str,
    return_type: Optional[str],
    description: str,
):
    """Selector-less read: capture an a11y+DOM snapshot and read the value
    from the automind textual-query endpoint directly.

    Mirrors the V2 selector-less textual query path — these ops were vision/LLM-resolved
    at authoring time and carry no element selector, so there is nothing to
    locate. The endpoint reads the value server-side from the snapshot; we use
    its `value` as the answer (NOT as a selector to relocate).
    """
    # /v1/heal/textual_query reads the query from
    # current_action.sub_instruction_obj.operation_dict.queried_value and
    # hard-subscripts operation_id / instruction_id / sub_instruction_obj.
    # It's stateless — everything comes from this payload, nothing is looked up server-side.
    current_action = {
        "operation_type": "TEXTUAL_QUERY",
        "operation_intent": description or "",
        "instruction_id": "",
        "operation_id": "",
        "use_query_v2": True,
        "version": "v3",
        "selector": [],
        "frame_info": [],
        "sub_instruction_obj": {
            "operation_dict": {
                "queried_value": description or "",
                "selected_attribute_name": selected_attribute_name,
            },
        },
    }
    healer = Heal(current_action, driver)

    # This read bypasses the action engine and its pre-action SmartWait, so the snapshot can
    # be taken while the page is still settling (an in-flight #anchor scroll / late reflow):
    # that mislands the viewport rect, drops the target node, and the server returns
    # found=false -> HTTP 500. SmartWait's idle heuristics don't always catch it, so each
    # attempt settles (SmartWait + a short hard wait) and RETRIES the snapshot+read; return the
    # first non-error response. Re-settling per attempt gives a flaky late-settle another chance.
    last_error = None
    for _attempt in range(_DIRECT_READ_ATTEMPTS):
        SmartWait(driver).smart_wait()
        time.sleep(_DIRECT_READ_SETTLE_SECS)
        a11y_snapshot, dom_snapshot, viewport_node_indices = capture_a11y_dom_snapshot(driver)
        resp = healer.textual_query_v2(a11y_snapshot, dom_snapshot, viewport_node_indices)
        payload = json.loads(resp.text)
        if not payload.get("error"):
            return _coerce(payload.get("value"), return_type)
        last_error = payload["error"]
    raise NoSuchElementException(
        f"textual_query direct read failed after {_DIRECT_READ_ATTEMPTS} attempts: {last_error}"
    )


def textual_query(
    driver,
    selector,
    *,
    selected_attribute_name: str,
    regex_pattern: Optional[str] = None,
    return_type: Optional[str] = None,
    description: str = '',
    tiers=None,
    autoheal: bool = True,
    max_attempts: int = 4,
    retry_delay: float = 0.5,
    search_root=None,
):
    """Read a textual value from the page.

    Two paths, mirroring V2's element-vs-prompt split:

    - Selector present: find the element and extract the attribute, retrying
      via the heal cascade (relocate) on recoverable errors. The raw
      testmu_selenium.textualQuery is unchanged and available for back-compat.
    - Selector empty/None (vision/LLM-resolved ops with no durable locator):
      read the value directly from an a11y+DOM snapshot via the automind
      endpoint (V2 textual_query_v2). This is the ONLY selector-less path — the
      DESKTOP_LOCATE_FULL_PAGE_READ locate tier was removed because
      /v2/locate/desktop refuses read/inspect intents by protocol (it always
      returns found=false for a read), so it never resolved a textual_query.
    """
    if not selector:
        # Selector-less V3 read (vision/LLM-resolved op, no durable locator): the server
        # snapshot read (V2 textual_query) is the ONLY path. The DESKTOP_LOCATE_FULL_PAGE_READ
        # locate tier was removed — /v2/locate/desktop refuses read/inspect intents by protocol
        # (always found=false for a read), so it never resolved a textual_query; it only added a
        # wasted ~6s locate roundtrip before this server read.
        return _direct_textual_read(
            driver,
            selected_attribute_name=selected_attribute_name,
            return_type=return_type,
            description=description,
        )
    return _run_action(
        driver, _TEXTUAL_QUERY_SPEC, selector,
        description=description, tiers=tiers, autoheal=autoheal,
        max_attempts=max_attempts, retry_delay=retry_delay,
        search_root=search_root,
        selected_attribute_name=selected_attribute_name,
        regex_pattern=regex_pattern,
        return_type=return_type,
    )
