"""Acting on web content from native context.

The element is LOCATED over the debug channel and ACTED ON with the same Appium
gesture the native path uses. Appium never leaves `NATIVE_APP`, so the generated
test is ordinary Appium and one driver performs every action in it.

Locating is a live lookup rather than a replay of recorded coordinates: a DOM
rectangle is only true for the layout that produced it, and replay happens on
another day at another size. What is recorded is the selector; the geometry is
re-derived every time.

Two things have to be established before a web element can be tapped, and both
are decided by comparing the two surfaces rather than by assumption:

- **Which page is on screen.** A device publishes a debug target per open tab and
  per WebView. The page itself knows — `document.visibilityState` — and that is
  the only signal that separates two tabs showing the SAME site, which comparing
  content against the accessibility tree cannot. Where nothing claims to be
  visible, the page whose content the accessibility tree also describes is taken
  to be the one displayed.
- **Where its content sits on the screen.** Solved from elements both surfaces
  describe. `window.screenX/screenY` reads 0 on Android, and the WebView node's
  own bounds miss by hundreds of pixels wherever chrome is drawn inside it.
"""
import json
import time
import logging
from dataclasses import dataclass

from testmu_appium._errors import ElementNotFound
from testmu_appium._helpers import _web
from testmu_appium._helpers._perception import (
    Perception, attach_screenshot, build_perception,
)
from testmu_appium._helpers._tabs_android import is_chrome_package
from testmu_appium._helpers._tree import position_hint

_log = logging.getLogger("testmu_appium")

#: How far a converted point may sit from the OS's own bounds for the same
#: element before the conversion is treated as wrong. A wrong conversion is
#: silent — it yields a plausible point somewhere else entirely.
_AGREEMENT_TOLERANCE_PX = 12

#: How many elements the two surfaces must describe the same way before a page is
#: accepted as the one on screen and its origin is trusted. One sample cannot be
#: cross-checked, and single samples were seen to disagree by 59 px where the
#: accessibility tree described a different box for the same node.
_MIN_CALIBRATION_SAMPLES = 2

#: How far a single calibration sample may sit from the others, in device pixels,
#: before it is discarded as describing something else.
_CALIBRATION_TOLERANCE_PX = 24

#: How deep cross-origin recovery descends. A frame can contain another, and each
#: boundary costs one round. Measured depth on real pages was 1; the bound is
#: defensive against a page that frames itself.
_MAX_FRAME_RECOVERY_ROUNDS = 5

#: Native attributes a label can be carried in, in the order the tree prefers.
_NATIVE_LABEL_FIELDS = ("text", "content_desc", "name")

#: Shared labels that settle which page is on screen without reading the rest.
#: A device with thirteen open tabs is ordinary, and Chrome freezes the ones in
#: the background — each costs a connection timeout to rule out.
_DECISIVE_SHARED_LABELS = 4

#: How many targets one socket is probed for before the scan gives up on it.
#: Reached only when NOTHING calibrated, which is what a native app's screen does
#: to a browser's open tabs; the cap is what stops that screen paying for all of
#: them. Chrome lists targets most-recently-used first, so the visible tab is at
#: or near the front.
_MAX_TARGET_PROBES = 8


@dataclass(frozen=True)
class VisibleWebTarget:
    """A capture-scoped observation of a visible browser debug target."""

    present: bool
    target_id: str | None
    package: str
    reason: str


def _remembered_target(transport, package="", *, scoped_only=False):
    """Read package-scoped target memory without breaking v1 providers.

    Package-aware memory is additive to the provider contract. Existing cloud
    providers still implement the original no-argument method; ordinary surface
    reads may retain that behaviour, while the visibility probe deliberately
    refuses a global winner because it cannot establish package ownership.
    """
    method = getattr(transport, "remembered_target_for", None)
    if method is not None:
        return method(package)
    if scoped_only:
        return ""
    return transport.remembered_target()


def _remember_target(transport, target_id, package=""):
    """Write package-scoped target memory where the provider supports it."""
    method = getattr(transport, "remember_target_for", None)
    if method is not None:
        return method(package, target_id)
    return transport.remember_target(target_id)


_WEB_ROLE_BY_TAG = {
    "A": "link",
    "BUTTON": "button",
    "INPUT": "input",
    "TEXTAREA": "input",
    "SELECT": "dropdown",
    "OPTION": "option",
    "IMG": "image",
}

_WEB_DESCRIPTOR_KEYS = (
    "css", "label", "tag", "role", "states", "interactive", "editable",
    "disabled", "input_type", "path", "dom_path", "frame_id",
)


@dataclass(frozen=True)
class Surface:
    """One web page, placed on the screen.

    `elements` remains the viewport set actions resolve against. `all_elements`
    adds readable offscreen content without widening that action set.
    `twins` is the native bounds of every element both surfaces describe, keyed by
    label. It is what calibrated the origin, and it is also the only independent
    check available on a converted point.
    """

    channel: object
    elements: list
    all_elements: list
    page: dict
    origin: tuple
    twins: dict

    @property
    def blocked_frames(self) -> int:
        """Cross-origin frames that stayed UNREAD after recovery.

        Non-zero means this surface is PARTIAL: whole subdocuments — payment
        fields, challenges, embedded maps — are missing from `elements`, not
        absent from the page. Chrome recovers them (so this is normally 0
        there); WebKit's protocol cannot, and the count is the honest report.
        """
        return int(self.page.get("unreadFrames") or 0)


def _role_for(element) -> str:
    return (
        str(element.get("role") or "").strip().lower()
        or _WEB_ROLE_BY_TAG.get(str(element.get("tag") or "").upper(), "item")
    )


def _position_for(element, page) -> str:
    left, top, right, bottom = _web.viewport_box(page)
    x1 = float(element.get("x", 0))
    y1 = float(element.get("y", 0))
    x2 = x1 + float(element.get("w", 0))
    y2 = y1 + float(element.get("h", 0))
    if y2 <= top:
        return "above viewport"
    if y1 >= bottom:
        return "below viewport"
    if x2 <= left:
        return "left of viewport"
    if x1 >= right:
        return "right of viewport"
    return position_hint(
        int((x1 + x2) / 2 - left),
        int((y1 + y2) / 2 - top),
        int(max(1, right - left)),
        int(max(1, bottom - top)),
    )


def _accepts_action(element, action_type: str, allow_inert: bool) -> bool:
    """Whether a DOM row can safely receive ``action_type``.

    Recorded-selector replay and semantic healing must agree on this boundary.
    In particular, a text selector for an offscreen input must not turn into a
    type action on its same-named ``LABEL`` while another field still has focus.
    """
    if str(element.get("tag") or "").upper() in {"SELECT", "OPTION"}:
        # Web select has no established mobile replay runner yet.
        return False
    if element.get("disabled") or "disabled" in (element.get("states") or []):
        return False
    if element.get("dom_path") is None:
        return False
    if allow_inert or action_type == "scroll":
        return True
    if action_type == "type":
        return bool(element.get("editable"))
    return bool(element.get("interactive"))


def _is_candidate(element, action_type: str, allow_inert: bool) -> bool:
    if not (element.get("label") or "").strip():
        return False
    return _accepts_action(element, action_type, allow_inert)


def capture_perception(
    driver,
    surface: Surface,
    action_type: str,
    *,
    allow_inert: bool = False,
) -> Perception:
    """Adapt current DOM rows into the canonical autoheal tree.

    The server sees the same normalized fields used for native healing. DOM
    identity remains in the private descriptor map.
    """
    normalized = []
    for element in surface.all_elements:
        if not _is_candidate(element, action_type, allow_inert):
            continue
        states = list(element.get("states") or [])
        boundary_path = str(element.get("path") or "")
        if (">f" in boundary_path or ">x" in boundary_path) \
                and "in-frame" not in states:
            states.append("in-frame")
        if ">s" in boundary_path and "in-shadow" not in states:
            states.append("in-shadow")
        normalized.append({
            **element,
            "role": _role_for(element),
            "name": str(element.get("label") or "").strip(),
            "states": states,
            "position_hint": _position_for(element, surface.page),
        })
    perception = build_perception(
        normalized, descriptor_keys=_WEB_DESCRIPTOR_KEYS
    )
    return attach_screenshot(perception, driver)


def read_all(channel):
    """Full-page and viewport elements, with unread frames folded into both.

    Recovery is recursive: a cross-origin frame can itself contain one, and the
    walk inside the recovered frame reports its own blocked children. Reading only
    the top document's blocked list loses everything below the first boundary.

    Recovery is an ENRICHMENT and cannot fail the read. The page has already been
    walked by the time it starts, so a recovery that raises still leaves a whole
    main document in hand — discarding that to report nothing is strictly worse
    than reporting it without the frames the walk was already blocked from.
    """
    page = channel.read_page()
    elements = _web.usable(page.get("elements", []))
    pending = [(page, "")]
    seen: set = set()
    try:
        for _ in range(_MAX_FRAME_RECOVERY_ROUNDS):
            found = []
            for parent, parent_path in pending:
                for index, (frame_id, url) in enumerate(
                        channel.unreachable_frames(parent, seen)):
                    seen.add(url)
                    path = f"{parent_path}>x{index}"
                    sub = channel.read_frame(frame_id, path)
                    if sub is None:
                        _log.info("    [web] frame %s could not be read", url[:60])
                        continue
                    elements.extend(_web.usable(sub.get("elements", [])))
                    found.append((sub, path))
            if not found:
                break
            pending = found
    except Exception as e:  # noqa: BLE001 — see the docstring: enrichment, not the read
        _log.info(
            "    [web] cross-origin frames were not recovered (%s); the main "
            "document stands with %d element(s)", e, len(elements))
    unread = max(0, (page.get("blockedFrames") or 0) - len(seen))
    # Written back so Surface.blocked_frames reports what stayed UNREAD, not
    # what the walk initially bounced off: on Chrome recovery folds those
    # frames in and this is normally 0.
    page["unreadFrames"] = unread
    if unread:
        # A tree missing whole frames must not read as a complete one: the
        # controls inside them — payment fields, challenges, embedded maps —
        # are absent from every consumer downstream, and "the page has no such
        # element" and "the element is in a frame this protocol cannot reach"
        # call for different next moves.
        _log.info(
            "    [web] %d cross-origin frame(s) could not be read; the web "
            "surface is PARTIAL", unread)
    return elements, _web.usable(elements, page), page


def _unique_by_label(elements):
    """label → element, for labels naming exactly one element."""
    seen = {}
    for element in elements:
        label = (element.get("label") or "").strip()
        if label:
            seen.setdefault(label, []).append(element)
    return {label: found[0] for label, found in seen.items() if len(found) == 1}


def _native_label(element):
    for field in _NATIVE_LABEL_FIELDS:
        value = (element.get(field) or "").strip()
        if value:
            return value
    return ""


def calibration_samples(web_elements, native_elements):
    """(label, css point, native bounds) for elements both surfaces describe once.

    Both sides must be unambiguous: a label naming two elements on either surface
    identifies neither, and pairing them anyway would calibrate against the wrong
    one without any sign that it had.
    """
    web = _unique_by_label(web_elements)
    counts = {}
    for element in native_elements:
        label = _native_label(element)
        if label:
            counts.setdefault(label, []).append(element)
    return [
        (label, (web[label]["x"], web[label]["y"]), found[0]["bounds"])
        for label, found in counts.items()
        if len(found) == 1 and label in web
    ]


def _median(values):
    ordered = sorted(values)
    return ordered[len(ordered) // 2]


def calibrate(samples, dpr, scale, offset_left=0, offset_top=0):
    """The web content's device-space origin, or None.

    Every sample solves for the origin independently; the median is taken and
    samples that disagree with it are dropped. This is not defensive tidying — a
    page can scroll between the two reads, and the accessibility tree sometimes
    reports a different box for the same node, both of which produce one
    confident, wrong answer from a single sample.
    """
    solved = [(label, _web.derive_origin(css, bounds, dpr, scale,
                                         offset_left, offset_top))
              for label, css, bounds in samples]
    if len(solved) < _MIN_CALIBRATION_SAMPLES:
        return None, solved
    middle = (_median([o[1][0] for o in solved]), _median([o[1][1] for o in solved]))
    agreeing = [
        (label, origin) for label, origin in solved
        if abs(origin[0] - middle[0]) <= _CALIBRATION_TOLERANCE_PX
        and abs(origin[1] - middle[1]) <= _CALIBRATION_TOLERANCE_PX
    ]
    if len(agreeing) < _MIN_CALIBRATION_SAMPLES:
        return None, solved
    return middle, agreeing


def _still_moving(channel, page):
    """Whether the page scrolled while it was being read.

    The origin is solved from a native tree read at one moment and a DOM read at
    another. A page that scrolls between them shifts EVERY calibration sample by
    the same amount, so the samples still agree — on an origin wrong by however
    far it moved, and the twin check passes because it uses the same stale tree.

    The native side is already required to be still (settling compares consecutive
    page sources). This is the same requirement on the web side, measured directly
    rather than by comparing two walks: a page reports where it is scrolled to.
    """
    try:
        left, top = channel.scroll_position()
    except Exception as e:  # noqa: BLE001 — a surface that cannot say is not moving
        _log.debug("[web] scroll position unavailable: %s", e)
        return False
    return (abs(left - float(page.get("scrollX", left))) > 1
            or abs(top - float(page.get("scrollY", top))) > 1)


def _corroborated_origin(solved, native_elements):
    """An origin backed by one sample AND the WebView's own box, or None.

    `_MIN_CALIBRATION_SAMPLES` is 2 because a lone sample cannot be cross-checked
    — single samples were seen to disagree by 59px where the accessibility tree
    reported a different box for the same node. That reasoning holds; what it
    overlooks is that the tree carries a SECOND opinion about where the page
    starts, independent of any element: the WebView node's own top-left.

    A screen can share very few labels between the two surfaces and still be
    perfectly placeable. Measured on a Google suggestions screen: 41 native rows
    of which 33 were keyboard keys, ONE shared label, and it solved (5, 141) —
    byte-identical to the WebView node's box (5, 141, 409, 813). The page was
    discarded anyway, and everything on it became unreachable.

    This is a corroboration, never an assumption. A browser draws its own chrome
    INSIDE its WebView, so there the box leads the content by the toolbar's
    height and the two disagree — which is precisely when this declines, leaving
    that screen unplaced rather than placing it confidently wrong.
    """
    boxes = [element.get("bounds") for element in native_elements
             if element.get("role") == "webview"
             or "WebView" in (element.get("cls") or "")]
    for label, origin in solved:
        for box in boxes:
            if (box and abs(origin[0] - box[0]) <= _CALIBRATION_TOLERANCE_PX
                    and abs(origin[1] - box[1]) <= _CALIBRATION_TOLERANCE_PX):
                _log.info(
                    "    [web] one shared label placed the page at %s, and the "
                    "WebView's own box agrees", origin)
                return origin, [(label, origin)]
    return None, solved


def open_surface(channel, native_elements):
    """Place one page on the screen, or None when its origin cannot be solved."""
    all_elements, elements, page = read_all(channel)
    if page.get("transformedFrames"):
        _log.info("    [web] %d frame(s) are drawn at a scale their contents do not "
                  "share; their elements are not offered", page["transformedFrames"])
    if _still_moving(channel, page):
        _log.info("    [web] the page moved while it was read; not placing it")
        return None
    samples = calibration_samples(elements, native_elements)
    origin, agreeing = calibrate(
        samples, page.get("dpr", 1), page.get("scale", 1) or 1,
        page.get("offsetLeft", 0), page.get("offsetTop", 0))
    if origin is None:
        # `agreeing` is the full solved list on this path, not the survivors.
        origin, agreeing = _corroborated_origin(agreeing, native_elements)
    if origin is None:
        return None
    kept = {label for label, _ in agreeing}
    twins = {label: bounds for label, _, bounds in samples if label in kept}
    return Surface(channel=channel, elements=elements,
                   all_elements=all_elements, page=page,
                   origin=origin, twins=twins)


def prepared_target_is_current(surface: Surface, element) -> bool:
    """Whether an authoring capture still describes this top-document target.

    The handoff is deliberately narrower than a cache. It is accepted only for
    the immediately following action, only when the same structural DOM target
    still has the same identity, and only when page/viewport/target geometry is
    unchanged. Frames and shadow roots keep the ordinary fresh capture path:
    cheaply revalidating their accumulated transforms would be as much work as
    reading them again.

    One CDP evaluation replaces a full DOM walk plus repeated native page-source
    settlement.  Any missing signal or protocol error fails closed to the normal
    capture path.
    """
    channel = getattr(surface, "channel", None)
    route = (element or {}).get("dom_path") or []
    if (
        channel is None
        or (element or {}).get("path", "")
        or len(route) != 1
        or route[0].get("kind") != "element"
        or not isinstance(route[0].get("nodes"), list)
    ):
        return False

    expression = """((nodes) => {
      let el = document;
      for (const index of nodes || []) {
        if (!el || !el.children || !el.children[index]) return null;
        el = el.children[index];
      }
      const box = el.getBoundingClientRect();
      const vv = window.visualViewport || {};
      const fieldLabel = Array.from(el.labels || [])
        .map((candidate) => candidate.innerText || '').join(' ').trim();
      const label = String(
        el.getAttribute('aria-label') || fieldLabel
        || el.getAttribute('placeholder') || el.innerText || ''
      ).trim().slice(0, 80);
      return [
        document.visibilityState, window.scrollX, window.scrollY,
        window.devicePixelRatio, vv.scale || 1,
        vv.offsetLeft || 0, vv.offsetTop || 0,
        window.innerWidth, window.innerHeight,
        vv.width || window.innerWidth, vv.height || window.innerHeight,
        box.x, box.y, box.width, box.height,
        el.disabled === true || el.getAttribute('aria-disabled') === 'true',
        el.tagName, label
      ];
    })(%s)""" % json.dumps(route[0]["nodes"])
    try:
        state = channel.evaluate(expression)
    except Exception as exc:  # noqa: BLE001 — stale handoff falls back safely
        _log.debug("[web] prepared target validation failed: %s", exc)
        return False
    if not isinstance(state, list) or len(state) != 18 or state[0] != "visible":
        return False

    page = surface.page
    expected = [
        page.get("scrollX", 0), page.get("scrollY", 0),
        page.get("dpr", 1), page.get("scale", 1) or 1,
        page.get("offsetLeft", 0), page.get("offsetTop", 0),
        page.get("viewportWidth", 0), page.get("viewportHeight", 0),
        page.get("visualWidth") or page.get("viewportWidth", 0),
        page.get("visualHeight") or page.get("viewportHeight", 0),
        element.get("x", 0), element.get("y", 0),
        element.get("w", 0), element.get("h", 0),
    ]
    actual = state[1:15]
    tolerances = [1, 1, 0.01, 0.01, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    try:
        if any(
            abs(float(got) - float(want)) > tolerance
            for got, want, tolerance in zip(actual, expected, tolerances)
        ):
            return False
    except (TypeError, ValueError):
        return False
    if bool(state[15]) != bool(element.get("disabled")):
        return False
    if str(state[16] or "").upper() != str(element.get("tag") or "").upper():
        return False
    return str(state[17] or "").strip() == str(element.get("label") or "").strip()


def open_unplaced_surface(channel):
    """Read a page for DOM-only work that does not need device coordinates."""
    all_elements, elements, page = read_all(channel)
    return Surface(
        channel=channel,
        elements=elements,
        all_elements=all_elements,
        page=page,
        origin=(0, 0),
        twins={},
    )


def open_web_surface(native_elements, package="", transport=None):
    """The web page currently on screen, or None.

    Every debuggable target on the device is a candidate — background tabs, other
    apps' WebViews. The page that reports itself visible is the one on screen;
    where none does, the page whose content the accessibility tree also describes
    is taken to be it. The previous winner is tried first and kept if it still
    reports visible, so a run does not re-scan every tab per action.

    `package` is the app in the foreground. A WebView socket names its owning
    process, so naming the app rules out every other app's WebView before a
    connection is attempted — a stale one costs a full connection timeout.

    Only a device that cannot be enumerated at all is called unreachable. A single
    target that does not answer is one of the several a device always carries, and
    must not decide anything about the others.
    """
    transport = transport or _web.debug_transport()
    if not transport.reachable():
        return None
    remembered = _remembered_target(transport, package)
    if remembered:
        surface, _, _ = _read_target(
            remembered, native_elements, require_visible=True, transport=transport
        )
        if surface is not None:
            return surface
    try:
        sockets = transport.sockets()
    except Exception as e:  # noqa: BLE001 — an unreachable device is a fact, not a crash
        transport.mark_unreachable(e)
        return None
    pids = transport.pids_of(package)
    hidden: set = set()
    surface, saw_visible = _scan_targets(
        sockets, native_elements, pids, require_visible=True, hidden=hidden,
        transport=transport, package=package)
    if surface is not None or saw_visible:
        # A page that claimed visibility IS the one on screen. Failing to place it
        # is a fact about that page — it projects too little into the
        # accessibility tree to solve an origin against (§5.2) — and no other
        # target is going to be it.
        return surface
    return _scan_targets(
        sockets, native_elements, pids, skip=hidden, transport=transport, package=package
    )[0]


def _channel_if_visible(ws_url, transport):
    """A channel to this target when it reports itself on screen, else None."""
    try:
        channel = transport.channel(ws_url)
        return channel if channel.is_visible() else None
    except Exception as e:  # noqa: BLE001 — a target that cannot answer is not the page
        _log.info("    [web] a debug target did not answer (%s)", e)
        return None


def probe_visible_web_target(package: str, transport=None) -> VisibleWebTarget:
    """Confirm that ``package`` owns a browser target visible right now.

    Version one intentionally recognises only Chrome's named browser socket.
    Unlike a WebView socket, that endpoint carries no pid; the foreground Chrome
    package is the ownership proof. No negative result is remembered: a socket
    or target absent during this capture may be published by the next one.

    The remembered winner is package-scoped and is accepted only after another
    ``document.visibilityState`` check. Target and socket failures are ordinary
    misses so one stale tab cannot prevent another target from being considered.
    """
    transport = transport or _web.debug_transport()
    if not is_chrome_package(package):
        return VisibleWebTarget(False, None, package, "unsupported-package")
    if not transport.reachable():
        return VisibleWebTarget(False, None, package, "transport-unreachable")

    remembered = _remembered_target(transport, package, scoped_only=True)
    if remembered:
        channel = _channel_if_visible(remembered, transport)
        if channel is not None:
            return VisibleWebTarget(
                True, remembered, package, "remembered-target-visible")
        _remember_target(transport, "", package)

    try:
        sockets = transport.sockets()
    except Exception as e:  # noqa: BLE001 — parity with the existing web readers
        transport.mark_unreachable(e)
        return VisibleWebTarget(False, None, package, "socket-enumeration-failed")

    browser_sockets = [socket for socket in sockets if socket.kind == "browser"]
    if not browser_sockets:
        return VisibleWebTarget(False, None, package, "no-browser-socket")

    for socket in browser_sockets:
        if transport.is_dead(socket):
            continue
        try:
            targets = transport.list_targets(transport.forward(socket))
        except Exception as e:  # noqa: BLE001 — one stale socket is not the device
            transport.mark_dead(socket, e)
            continue
        for probed, target in enumerate(targets):
            if probed >= _MAX_TARGET_PROBES:
                break
            target_id = target.get("webSocketDebuggerUrl")
            if not target_id:
                continue
            channel = _channel_if_visible(target_id, transport)
            if channel is None:
                continue
            _remember_target(transport, target_id, package)
            return VisibleWebTarget(
                True, target_id, package, "discovered-target-visible")
    return VisibleWebTarget(False, None, package, "no-visible-target")


def visible_channel(package="", transport=None):
    """The page on screen as a channel, without placing it on the device.

    `open_web_surface` solves an origin and returns None when it cannot, because
    everything it offers is measured in device pixels. A caller that only reads or
    drives the DOM needs no origin, and gating it on one would withhold the page
    exactly on the screens whose accessibility tree describes too little to
    calibrate against.

    The previous winner is tried first, so a run that has already acted on this
    page does not re-scan the device's targets.
    """
    transport = transport or _web.debug_transport()
    if not transport.reachable():
        return None
    remembered = _remembered_target(transport, package)
    if remembered:
        channel = _channel_if_visible(remembered, transport)
        if channel is not None:
            return channel
    try:
        sockets = transport.sockets()
    except Exception as e:  # noqa: BLE001 — an unreachable device is a fact, not a crash
        transport.mark_unreachable(e)
        return None
    pids = transport.pids_of(package)
    owned = [socket for socket in sockets if _owns_socket(socket, pids, package)]
    if pids is not None and not owned:
        transport.mark_no_socket(package)
    for socket in owned:
        if transport.is_dead(socket):
            continue
        try:
            targets = transport.list_targets(transport.forward(socket))
        except Exception as e:  # noqa: BLE001
            transport.mark_dead(socket, e)
            continue
        for probed, target in enumerate(targets):
            if probed >= _MAX_TARGET_PROBES:
                break
            channel = _channel_if_visible(
                target["webSocketDebuggerUrl"], transport
            )
            if channel is not None:
                _remember_target(
                    transport, target["webSocketDebuggerUrl"], package)
                return channel
    return None


def _read_target(
    ws_url, native_elements, require_visible=False, hidden=None, transport=None
):
    """(surface, answered, visible) for one target.

    `answered` separates "this is not the page on screen" from "this target is not
    there anymore". Only the second is grounds for writing a socket off, and a
    pass that asked for the visible page will say no to almost everything.

    `visible` records that this target claimed to be the page on screen, which is
    true whether it could then be placed.

    `hidden` collects the targets that said they are NOT on screen, so the content
    pass — which exists for surfaces that cannot answer at all — never re-admits a
    page that answered plainly.

    `require_visible` asks the page whether it is the one being displayed before
    walking it. That probe is one small evaluate against a full pierced walk, so
    ruling a background tab out this way is far cheaper than reading it.
    """
    transport = transport or _web.debug_transport()
    try:
        channel = transport.channel(ws_url)
    except Exception as e:  # noqa: BLE001 — a target that cannot be opened is gone
        _log.info("    [web] a debug target could not be opened (%s)", e)
        return None, False, False

    if require_visible:
        try:
            visible = channel.is_visible()
        except Exception as e:  # noqa: BLE001
            # A surface that cannot answer is not thereby gone: the content
            # comparison is still to come, and writing the socket off here would
            # take it away.
            _log.info("    [web] a target did not report its visibility (%s)", e)
            return None, True, False
        if not visible:
            if hidden is not None:
                hidden.add(ws_url)
            return None, True, False
    try:
        return open_surface(channel, native_elements), True, require_visible
    except Exception as e:  # noqa: BLE001 — a target that cannot be read is a miss
        # It answered before it failed, so the socket is alive; only a target that
        # never spoke at all is grounds for writing one off.
        _log.info("    [web] a debug target could not be read (%s)", e)
        return None, require_visible, require_visible


def _owns_socket(socket, pids, package) -> bool:
    """Whether `socket` could belong to the app currently in the foreground.

    A WebView socket names its owning pid, so a mismatch rules it out exactly
    like another app's WebView. A browser socket carries no pid — Chrome is
    identified by package instead — so it is attributed to the foreground app
    only when that app IS the browser; otherwise `chrome_devtools_remote` is a
    stale, backgrounded or unrelated browser process, not the page this session
    means to read. An unrecognised ("other") socket never belongs to anything.
    """
    if socket.kind == "webview":
        return pids is None or socket.pid in pids
    if socket.kind == "browser":
        return pids is None or is_chrome_package(package)
    return False


def _scan_targets(sockets, native_elements, pids=None, require_visible=False,
                  skip=(), hidden=None, transport=None, package=""):
    """(surface, saw_visible) — the page on screen, and whether one claimed to be.

    `saw_visible` is what stops a page that named itself and then could not be
    placed from sending the scan through every other tab on the device.

    Sockets not owned by the foreground app (§_owns_socket) are never probed.
    When that leaves nothing to scan for a known foreground package, this is a
    build fact — webview debugging is off — not a transport failure, and is
    reported as such rather than as a socket that "did not answer".
    """
    transport = transport or _web.debug_transport()
    owned = [socket for socket in sockets if _owns_socket(socket, pids, package)]
    if pids is not None and not owned:
        transport.mark_no_socket(package)
    best = None
    saw_visible = False
    for socket in owned:
        if transport.is_dead(socket):
            continue
        try:
            targets = transport.list_targets(transport.forward(socket))
        except Exception as e:  # noqa: BLE001
            transport.mark_dead(socket, e)
            continue
        answered = False
        for probed, target in enumerate(targets):
            if probed >= _MAX_TARGET_PROBES:
                _log.info("    [web] %s publishes %d targets; stopped after %d without "
                          "finding the page on screen",
                          socket.name, len(targets), _MAX_TARGET_PROBES)
                break
            if target["webSocketDebuggerUrl"] in skip:
                continue
            surface, reachable, visible = _read_target(
                target["webSocketDebuggerUrl"], native_elements, require_visible, hidden,
                transport=transport)
            answered = answered or reachable
            saw_visible = saw_visible or visible
            if surface is None:
                if visible:
                    # This IS the page on screen; it just could not be placed.
                    break
                continue
            if best is None or len(surface.twins) > len(best[0].twins):
                best = (surface, target)
            if require_visible or len(surface.twins) >= _DECISIVE_SHARED_LABELS:
                # A page that says it is visible settles it outright. Failing
                # that, a decisive share of labels does: the remaining targets
                # are not worth a connection timeout each.
                return _chosen(
                    *best, transport=transport, package=package), saw_visible
        if targets and not answered:
            transport.mark_dead(socket, RuntimeError("no target answered"))
        if saw_visible:
            break
    return (
        _chosen(*best, transport=transport, package=package) if best else None
    ), saw_visible


def _chosen(surface, target, transport=None, package=""):
    transport = transport or _web.debug_transport()
    _remember_target(transport, target["webSocketDebuggerUrl"], package)
    _log.info("    [web] reading %s — %d elements, origin %s, %d shared with the device",
              target.get("url", "")[:60], len(surface.elements),
              surface.origin, len(surface.twins))
    return surface


def _match(elements, selector):
    """Elements a recorded selector names, by whichever clause it was recorded in."""
    strategy = selector.get("strategy")
    value = selector.get("selector", "")
    if strategy == "css":
        # Either css field, because either can be the one the recorder ranked.
        # `css` is `#id` or the bare tag name; when it is only a tag the ranker
        # rejects it as naming a kind rather than an element and records the
        # structural `css_path` instead. Comparing against `css` alone then
        # cannot match by construction: the element is found, ranked, published
        # and re-found by nothing.
        return [e for e in elements
                if e.get("css") == value or e.get("css_path") == value]
    if strategy in ("text", "accessibility_id"):
        return [e for e in elements if (e.get("label") or "") == value]
    return []


def locate(
    elements,
    selectors,
    frame_path="",
    *,
    strict_path=False,
    action_type="",
    allow_inert=False,
):
    """The one element a recorded selector names, or None.

    Selectors are tried in the order the recorder ranked them and a strategy
    matching several elements is skipped like a miss — the same cardinality rule
    the native walk uses, for the same reason: an almost-right element is a wrong
    action.

    By default `frame_path` is the legacy tie-breaker for callers that did not
    record surface identity. Replay passes ``strict_path=True``: the path
    (including ``""`` for the top document) is then a non-relaxable boundary, so
    a locator moving to another frame fails and reaches heal instead of acting
    on the wrong copy. When ``action_type`` is provided, a selector match also
    has to be a valid target for that action. This prevents a lower-priority
    text selector from resolving a non-editable label for a type action after
    the intended offscreen input's CSS selector missed.
    """
    for selector in selectors or []:
        matches = _match(elements, selector)
        if action_type:
            matches = [
                element
                for element in matches
                if _accepts_action(element, action_type, allow_inert)
            ]
        if strict_path:
            matches = [
                e for e in matches if e.get("path", "") == (frame_path or "")
            ]
        elif len(matches) > 1 and frame_path:
            matches = [e for e in matches if e.get("path", "") == frame_path] or matches
        if len(matches) == 1:
            return matches[0]
        if matches:
            _log.info("    [web] strategy %s matched %d elements — ambiguous, "
                      "trying the next", selector.get("strategy"), len(matches))
    return None


def clear_value(surface, element):
    """Empty a web field through the page, returning whether it was emptied.

    The coordinate path clears through `switch_to.active_element`, which only
    knows NATIVE focus. With the caret inside a WKWebView there is no native
    element to name: XCUITest raises NoSuchElementException while the page
    reports its focused textarea perfectly well, so a replace-into-a-web-field
    fails with "the tap opened no text field, so there was nothing to clear" —
    on a field that was found, ranked, located and tapped correctly.

    The page is the one surface that can answer, so it is asked directly. Returns
    False rather than raising when it cannot: the caller then leaves the native
    clear in place, so nothing that works today changes.
    """
    selector = _sole_match_selector(element)
    if not selector:
        return False
    script = (
        "(function(s){"
        # The selector must name EXACTLY ONE element, counted fresh here: a
        # bare-tag `css` ("input") or an unanchored `css_path` matches the
        # FIRST element in the whole document — including hidden twins the
        # perception walk dropped — and emptying a hidden duplicate reports
        # success while the real field keeps its text.
        "if(document.querySelectorAll(s).length!==1)return false;"
        "var e=document.querySelector(s);"
        "if(!e||!('value' in e))return false;"
        "e.focus();e.value='';"
        # Frameworks track their own state and repaint from it; a value set
        # without these events is overwritten the moment the field is touched.
        "e.dispatchEvent(new Event('input',{bubbles:true}));"
        "e.dispatchEvent(new Event('change',{bubbles:true}));"
        "return true;})(" + json.dumps(selector) + ")"
    )
    try:
        return bool(surface.channel.evaluate(script))
    except Exception as e:  # noqa: BLE001 — a page that cannot answer is not fatal
        _log.info("    [web] could not clear through the page (%s)", e)
        return False


def _sole_match_selector(element) -> str:
    """The element's selector, when one exists and can be queried at all.

    Empty means "do not shortcut through the page": a framed element is not
    reachable by a top-document query, and an element with no selector has
    nothing to query by. Cardinality is checked IN the page script, not here —
    the answer is only true at the moment it is asked.
    """
    selector = element.get("css_path") or element.get("css") or ""
    if not selector or element.get("path"):
        return ""
    return selector


#: How long the page gets to finish a focus-triggered redraw before the focused
#: field's position is read. Measured on Google's search box, whose suggestions
#: overlay relocates the field to the top of the page.
_PREFOCUS_SETTLE_S = 0.8


def prefocus_point(surface, element):
    """Focus the field through the PAGE, and say where it now is.

    The steal this defuses: a page that redraws on focus swaps its layout in
    while a tap's finger is still down, and the click dispatches to whatever
    now occupies the point — measured on Google, where it landed on a trending
    row and NAVIGATED, three runs straight. Focusing via script triggers that
    same redraw with NO click in flight, so there is nothing to steal; the tap
    that follows (still required — page focus alone is not a native first
    responder, measured cold on the same device) lands on the already-focused
    field at its POST-redraw position, where a click activates nothing.

    Returns the device point to tap, or None when this route does not apply —
    a framed or selector-less element, a page that refuses script focus, or a
    field that settled outside the viewport. None always means "tap where the
    surface said", never an error.
    """
    selector = _sole_match_selector(element)
    if not selector:
        return None
    try:
        focused = surface.channel.evaluate(
            # Same sole-match rule as clear_value, for the same reason: a
            # bare-tag selector focuses the FIRST match in the document —
            # possibly a hidden twin — and everything after would aim at it.
            "(function(s){if(document.querySelectorAll(s).length!==1)return false;"
            "var e=document.querySelector(s);if(!e)return false;"
            "e.focus();var a=document.activeElement;"
            "return !!a && (a.tagName==='INPUT'||a.tagName==='TEXTAREA'"
            "||a.isContentEditable===true)})(" + json.dumps(selector) + ")"
        )
        if not focused:
            return None
        time.sleep(_PREFOCUS_SETTLE_S)
        raw = surface.channel.evaluate(
            "(function(){var a=document.activeElement;"
            "if(!a||!(a.tagName==='INPUT'||a.tagName==='TEXTAREA'"
            "||a.isContentEditable===true))return '';"
            "var r=a.getBoundingClientRect();"
            "return JSON.stringify({x:r.x+r.width/2,y:r.y+r.height/2})})()"
        )
        if not raw:
            return None
        centre = json.loads(raw)
        # A field that settled OUTSIDE the visual viewport is not tappable at
        # the converted point — an off-screen W3C tap is a driver error, not a
        # graceful decline, and this route must never be a new way to fail.
        left, top, right, bottom = _web.viewport_box(surface.page)
        if not (left <= centre["x"] <= right and top <= centre["y"] <= bottom):
            _log.info("    [web] the focused field settled outside the "
                      "viewport; tapping as located")
            return None
        page = surface.page
        x, y = _web.to_device(
            centre["x"], centre["y"], origin=surface.origin,
            dpr=page["dpr"], scale=page["scale"] or 1,
            offset_left=page.get("offsetLeft", 0),
            offset_top=page.get("offsetTop", 0))
        if x < 1 or y < 1:
            return None
        _log.info("    [web] focused through the page; the field now sits at "
                  "(%d, %d)", x, y)
        return x, y
    except Exception as e:  # noqa: BLE001 — this route is an upgrade, never a new failure
        _log.info("    [web] prefocus unavailable (%s); tapping as located", e)
        return None


def focus_state(surface):
    """Where the page stands right now: its location, and whether an editable
    element holds focus.

    The question a type action must ask between its focus tap and its keys. A
    page that redraws on focus (a search box swapping in a suggestions overlay)
    can steal the tap's click for whatever now occupies the point — measured on
    Google, where the click landed on a trending row and NAVIGATED, and six
    keystrokes then went to a page that no longer existed. Deliberately loose
    about WHICH editable holds focus: the overlay's replacement field is a
    different DOM node than the one located, and it is the correct field.

    Returns None when the page cannot answer — a caller treats that as "no
    verification available", never as a verdict.
    """
    script = (
        "(function(a){return JSON.stringify({href: location.href,"
        "editable: !!a && (a.tagName==='INPUT'||a.tagName==='TEXTAREA'"
        "||a.isContentEditable===true)})})(document.activeElement)"
    )
    try:
        raw = surface.channel.evaluate(script)
        return json.loads(raw) if raw else None
    except Exception as e:  # noqa: BLE001 — a page that cannot answer verifies nothing
        _log.info("    [web] focus state unavailable (%s)", e)
        return None


def resolve_descriptor(elements, descriptor):
    """Resolve one private web descriptor against a fresh DOM capture.

    Unlike recorded-selector lookup, this is deliberately strict. A healed
    descriptor is a short-lived identity for one exact DOM node; allowing a
    frame-path fallback here could turn a correct model answer into a tap on the
    same selector in another frame.
    """
    matches = []
    for element in elements:
        if element.get("dom_path") != descriptor.get("dom_path"):
            continue
        if element.get("path", "") != descriptor.get("path", ""):
            continue
        if element.get("frame_id") != descriptor.get("frame_id"):
            continue
        if str(element.get("tag") or "").upper() != str(
                descriptor.get("tag") or "").upper():
            continue
        if (element.get("label") or "").strip() != (
                descriptor.get("label") or "").strip():
            continue
        if _role_for(element) != str(descriptor.get("role") or ""):
            continue
        if bool(element.get("editable")) != bool(descriptor.get("editable")):
            continue
        if "input_type" in descriptor and str(element.get("input_type") or "") != str(
                descriptor.get("input_type") or ""):
            continue
        if "interactive" in descriptor and bool(element.get("interactive")) != bool(
                descriptor.get("interactive")):
            continue
        if "disabled" in descriptor and bool(element.get("disabled")) != bool(
                descriptor.get("disabled")):
            continue
        matches.append(element)
    return matches[0] if len(matches) == 1 else None


def descriptor_for(element):
    """The private descriptor shape for one already-read DOM element."""
    normalized = {**element, "role": _role_for(element)}
    return {
        key: normalized.get(key)
        for key in _WEB_DESCRIPTOR_KEYS
        if key in normalized
    }


def in_view(surface: Surface, element) -> bool:
    """Whether any actable part of ``element`` is in the visual viewport."""
    return _web.visible_part(element, _web.viewport_box(surface.page)) is not None


#: Reports what the page did, so the caller can tell "no such element" apart from
#: "scrolled but still not fully in the viewport" — a sticky header can hold the
#: second, and it is not a failure to find anything.
_SCROLL_INTO_VIEW_JS = """(() => {
  const el = document.querySelector(%s);
  if (!el) return 'missing';
  el.scrollIntoView({block: 'center', inline: 'nearest'});
  const box = el.getBoundingClientRect();
  return (box.top >= 0 && box.bottom <= window.innerHeight) ? 'visible' : 'moved';
})()"""


def css_of(selectors):
    """The recorded css strategy, or None when this target was not read from a DOM."""
    for selector in selectors or []:
        if selector.get("strategy") == "css" and selector.get("selector"):
            return selector["selector"]
    return None


def scroll_into_view(channel, css):
    """Scroll the page so `css` lies in the viewport; returns what the page reported.

    The DOM knows where its own elements are, so this is one round trip rather
    than the gesture-and-recheck loop the native path runs: that loop exists
    because a native tree cannot say where an unrendered row will be.
    """
    return channel.evaluate(_SCROLL_INTO_VIEW_JS % json.dumps(css))


_SCROLL_DESCRIPTOR_JS = """((route) => {
  const childAt = (root, nodes) => {
    let current = root;
    for (const index of nodes) {
      if (!current || !current.children || !current.children[index]) return null;
      current = current.children[index];
    }
    return current;
  };
  let root = document;
  let element = null;
  for (const step of route || []) {
    const found = childAt(root, step.nodes || []);
    if (!found) return 'missing';
    if (step.kind === 'shadow') {
      if (!found.shadowRoot) return 'missing';
      root = found.shadowRoot;
    } else if (step.kind === 'frame') {
      if (!found.contentDocument) return 'missing';
      found.scrollIntoView({block: 'center', inline: 'nearest'});
      root = found.contentDocument;
    } else if (step.kind === 'element') {
      element = found;
    } else {
      return 'missing';
    }
  }
  if (!element) return 'missing';
  element.scrollIntoView({block: 'center', inline: 'nearest'});
  const box = element.getBoundingClientRect();
  return (box.top >= 0 && box.bottom <= window.innerHeight) ? 'visible' : 'moved';
})(%s)"""


def scroll_descriptor(channel, descriptor):
    """Scroll the exact healed DOM node represented by ``descriptor``."""
    route = descriptor.get("dom_path")
    if not route:
        return "missing"
    expression = _SCROLL_DESCRIPTOR_JS % json.dumps(route)
    frame_id = descriptor.get("frame_id")
    if frame_id:
        if not channel.scroll_frame_into_view(frame_id):
            return "missing"
        return channel.evaluate_in_frame(frame_id, expression)
    return channel.evaluate(expression)


def device_point(element, page, origin):
    """Where to tap a web element, in device pixels.

    The centre of the part of it that is ON SCREEN, not of the whole rectangle: an
    element scrolled half off an edge is still actable, and its full-rectangle
    centre can be off the screen entirely.
    """
    part = _web.visible_part(element, _web.viewport_box(page))
    if part is None:
        centre_x = element["x"] + element["w"] / 2
        centre_y = element["y"] + element["h"] / 2
    else:
        centre_x = (part[0] + part[2]) / 2
        centre_y = (part[1] + part[3]) / 2
    return _web.to_device(
        centre_x, centre_y,
        origin=origin, dpr=page["dpr"], scale=page["scale"],
        offset_left=page.get("offsetLeft", 0), offset_top=page.get("offsetTop", 0),
    )


def verified_point(element, page, origin, native_bounds=None):
    """A device point, refused unless it agrees with the OS where both can see it.

    `native_bounds` is where the accessibility tree reported the same element. It
    is the only independent check on a conversion, and it exists because getting
    the conversion wrong places a confident tap hundreds of pixels away.
    """
    point = device_point(element, page, origin)
    if native_bounds and not _web.agrees(point, native_bounds, _AGREEMENT_TOLERANCE_PX):
        raise ElementNotFound(
            element.get("label", "") or element.get("css", ""), ["css"],
            f"the converted point {point} does not lie in the bounds the device "
            f"reported for this element ({native_bounds}); refusing to tap")
    return point


def point_for(surface, element):
    """Where to tap for a located web element, checked against the device."""
    label = (element.get("label") or "").strip()
    return verified_point(element, surface.page, surface.origin,
                          native_bounds=surface.twins.get(label))


def device_bounds(surface, element):
    """A located web element's box in device pixels, for the step's telemetry."""
    page, origin = surface.page, surface.origin
    convert = lambda x, y: _web.to_device(  # noqa: E731 — one expression, read inline
        x, y, origin=origin, dpr=page["dpr"], scale=page["scale"],
        offset_left=page.get("offsetLeft", 0), offset_top=page.get("offsetTop", 0))
    x1, y1 = convert(element["x"], element["y"])
    x2, y2 = convert(element["x"] + element["w"], element["y"] + element["h"])
    return x1, y1, x2, y2
