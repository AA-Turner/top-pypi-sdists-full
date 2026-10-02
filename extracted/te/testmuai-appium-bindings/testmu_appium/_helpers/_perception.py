"""One fresh-perception pass: page source → wire entries + retained descriptors.

Heal posts a flat entry list to /api/v1/autoheal and receives back a
``dom_index`` into it. The parsed entries are static dictionaries, never actable
handles, so the binding keeps a private ``index → descriptor`` map from the SAME
parse and compiles a fresh strict lookup from the descriptor when the response
arrives. Nothing element-shaped survives across the HTTP call.

The wire entries carry only what the server needs to reason about the screen
(index/role/name/states/position_hint); the descriptors hold the source attributes
(resource-id, text, content-desc, class, bounds, center) that a fresh lookup is
built from.
"""
import base64
import logging
from dataclasses import dataclass, field
from typing import Any, Optional

from testmu_appium import _config
from testmu_appium._helpers import _screen
from testmu_appium._errors import ScreenshotUnavailable
from testmu_appium._helpers import _mjpeg

_log = logging.getLogger("testmu_appium")

#: Keys of a normalized entry that go on the wire. Anything else stays local.
_WIRE_KEYS = ("index", "role", "name", "states")

#: Descriptor keys retained per entry for the post-heal fresh lookup.
_DESCRIPTOR_KEYS = (
    "resource_id", "text", "content_desc", "hint", "cls", "bounds", "center",
    "interactive",
    # The producer's driver-side match counts, kept so the post-heal fresh
    # lookup can tell an identifier that names ONE element from one that names
    # two — and compile the compound clause only when it must.
    "query_matches",
)

#: Descriptor keys that ride as `attributes` on an element snapshot, under the
#: names the Android source uses for them.
_SNAPSHOT_ATTRIBUTES = (
    ("resource_id", "resource-id"),
    ("content_desc", "content-desc"),
    ("hint", "hint"),
    ("bounds", "bounds"),
)


@dataclass
class Perception:
    """A single capture: what the server sees plus what the binding kept back.

    `screenshot_source` names the path that served the pixels — ``"mjpeg"`` or
    ``"appium"`` — and is None when no screenshot was taken or the capture lost it.
    """

    entries: list[dict] = field(default_factory=list)
    descriptors: dict[int, dict[str, Any]] = field(default_factory=dict)
    screenshot_b64: Optional[str] = None
    window: tuple[int, int] = (0, 0)
    screenshot_source: Optional[str] = None


def build_perception(
    elements: list[dict[str, Any]],
    *,
    descriptor_keys: tuple[str, ...],
) -> Perception:
    """Build the canonical wire tree and its private descriptor map.

    ``elements`` is deliberately source-neutral. The native collector adapts
    Appium page-source rows and the web collector adapts DOM rows, but both feed
    this one indexing/wire-format boundary. Execution-only identity stays in the
    descriptor map and never reaches the autoheal service.
    """
    entries: list[dict[str, Any]] = []
    descriptors: dict[int, dict[str, Any]] = {}
    for index, element in enumerate(elements, start=1):
        entry = {
            "index": index,
            "role": str(element.get("role") or ""),
            "name": str(element.get("name") or ""),
            "states": list(element.get("states") or []),
            "position_hint": str(
                element.get("position_hint") or element.get("position") or ""
            ),
        }
        entries.append(entry)
        descriptors[index] = {
            key: element.get(key)
            for key in descriptor_keys
            if key in element
        }
    return Perception(entries=entries, descriptors=descriptors)


def element_snapshot(perception: Perception, index: int) -> dict[str, Any]:
    """The analyzer's single-element view of one entry, built from its descriptor.

    The analyzer's DOM extract leg reads ``tag_name``, ``text_content``,
    ``attributes``, ``styles`` and ``states``. A native element has no computed
    style, so ``styles`` is always empty; the rest come from the descriptor kept
    back at capture time plus the wire entry's states. An index the capture never
    saw yields the empty snapshot rather than raising.
    """
    descriptor = perception.descriptors.get(index) or {}
    entry = next(
        (e for e in perception.entries if e.get("index") == index), {}
    )
    return {
        "tag_name": str(descriptor.get("cls") or entry.get("role") or ""),
        "text_content": str(descriptor.get("text") or entry.get("name") or ""),
        "attributes": {
            name: str(descriptor[key])
            for key, name in _SNAPSHOT_ATTRIBUTES
            if descriptor.get(key)
        },
        "styles": {},
        "states": {str(state): True for state in (entry.get("states") or [])},
    }


def _window_size(driver) -> tuple[int, int]:
    size = _screen.window_size(driver)
    return size[0], size[1]


def _capture_screenshot(driver) -> tuple[bytes, str]:
    """Grab the screen, MJPEG-first, and report which path served it.

    The stream is the fast path wherever it is reachable and the Appium screencap is
    the fallback; a stream that fails is not tried again for the rest of the session.
    `screenshot_source="mjpeg"` forbids the fallback, so a stream failure surfaces as
    a capture failure instead of silently returning a differently-timed frame.
    """
    forced = _mjpeg.source() == _config.SOURCE_MJPEG
    if _mjpeg.usable():
        try:
            return _mjpeg.read_latest_frame(), _config.SOURCE_MJPEG
        except Exception as e:  # noqa: BLE001 — any stream failure degrades the path
            _mjpeg.mark_unreachable(e)
            if forced:
                raise
    elif forced:
        raise RuntimeError(
            "the MJPEG stream is unavailable and screenshot_source='mjpeg' "
            "forbids the Appium screenshot"
        )
    return driver.get_screenshot_as_png(), _config.SOURCE_APPIUM


def attach_screenshot(
    perception: Perception,
    driver,
    *,
    require_screenshot: bool = False,
) -> Perception:
    """Attach current pixels and window metadata to a canonical perception.

    Collectors use this after building their source-neutral entries, so native
    and web healing have identical screenshot failure behavior.
    """
    perception.window = _window_size(driver)
    try:
        screenshot, perception.screenshot_source = _capture_screenshot(driver)
        perception.screenshot_b64 = base64.b64encode(screenshot).decode()
    except Exception as e:  # noqa: BLE001 — see capture_perception
        perception.screenshot_source = None
        if require_screenshot:
            raise ScreenshotUnavailable(
                f"the screen could not be captured: {e}"
            ) from e
        _log.warning("[perception] screenshot failed (continuing without): %s", e)
    return perception


def capture_perception(
    driver, *, include_screenshot: bool = True, require_screenshot: bool = False
) -> Perception:
    """Parse the live page source into wire entries + descriptors.

    The screenshot comes from the MJPEG stream where that is reachable and from
    `driver.get_screenshot_as_png()` otherwise; the served path is on the returned
    `Perception.screenshot_source`.

    `require_screenshot` picks which failure mode a lost screenshot gets:

    - HEAL's perception (the default, fail-open) logs and continues, since the entry
      list alone still lets the server reason about the screen.
    - The VISION verb passes True and gets a raise: a visual query answered from the
      entry list alone is a different question, answered against no pixels.
    """
    width, height = _window_size(driver)
    # Through the public dispatcher, so heal and vision read the same rows the
    # configured platform's producer emits. Calling the Android module directly
    # parsed an iOS hierarchy to zero rows — imported lazily because the public
    # module reaches back through _action_web to this one.
    from testmu_appium import perception as _perception_api  # noqa: PLC0415
    parsed = _perception_api.parse_tree(driver.page_source, width, height)

    perception = build_perception(parsed, descriptor_keys=_DESCRIPTOR_KEYS)

    if include_screenshot:
        attach_screenshot(
            perception, driver, require_screenshot=require_screenshot
        )
    else:
        perception.window = (width, height)
    return perception
