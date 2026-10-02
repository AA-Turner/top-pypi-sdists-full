"""The web surface: reading a WebView's real DOM, and placing it on the screen.

A WebView's contents are not in the accessibility tree in any useful form — a
page using shadow DOM projects one field where thirty-one exist. The DOM is read
here, over the debug channel the WebView already publishes, while every ACTION
stays an ordinary Appium gesture in native context. There is no context switch.

Two facts about that channel shape this module:

- Sockets do not follow one naming convention. Alongside
  `chrome_devtools_remote` and `webview_devtools_remote_<pid>` a device may carry
  a Stetho socket from an unrelated app, so discovery matches a pattern and the
  caller decides what it can speak to.
- A DOM rectangle is in CSS pixels inside a viewport that is itself offset,
  scaled and scrollable. Converting one to a device point needs the content
  origin, and that origin must be DERIVED from an element visible on both
  surfaces rather than read off the WebView node's bounds — the latter produced
  taps that missed by hundreds of pixels.
"""
import json
import logging
import re
import subprocess
import sys
import urllib.request
from dataclasses import dataclass
from typing import Optional, Protocol, Sequence

from testmu_appium import _config
from testmu_appium._errors import UnsupportedOnPlatform

_log = logging.getLogger("testmu_appium")

#: Any abstract socket whose name ends in the devtools convention. Broader than
#: the two names Chrome and WebView use, because a device carries others.
_DEVTOOLS_SOCKET = re.compile(r"@(\S*devtools_remote\S*)")

#: `webview_devtools_remote_<pid>` — the only form that names its owning process.
_WEBVIEW_SOCKET = re.compile(r"^webview_devtools_remote_(\d+)$")

_BROWSER_SOCKET = "chrome_devtools_remote"


@dataclass(frozen=True)
class Socket:
    """One devtools endpoint published on the device.

    `pid` is set only for the WebView form, which is what lets a socket be tied
    to the app that owns it. `kind` records whether we expect to speak CDP:
    `other` is kept rather than dropped so an unrecognised endpoint is visible
    instead of silently missing.
    """

    name: str
    pid: Optional[int]
    kind: str  # "webview" | "browser" | "other"


def discover_sockets(proc_net_unix: str) -> list:
    """Devtools sockets named in the contents of /proc/net/unix."""
    found = []
    seen = set()
    for match in _DEVTOOLS_SOCKET.finditer(proc_net_unix or ""):
        name = match.group(1)
        if name in seen:
            continue
        seen.add(name)
        webview = _WEBVIEW_SOCKET.match(name)
        if webview:
            found.append(Socket(name, int(webview.group(1)), "webview"))
        elif name == _BROWSER_SOCKET:
            found.append(Socket(name, None, "browser"))
        else:
            found.append(Socket(name, None, "other"))
    return found


def socket_for_pid(sockets: Sequence, pid: int):
    """The WebView socket belonging to a process, or None."""
    for socket in sockets:
        if socket.pid == pid:
            return socket
    return None


# --- reaching the device ----------------------------------------------------
#
# A devtools socket is an abstract unix socket on the device, so it is reached by
# forwarding a host port onto it. `adb` runs on the host running the test: that
# host is the device's host for a local run and somebody else's machine for a
# cloud one, which is why `reachable()` gates on the run target rather than probing.

_ADB_TIMEOUT_S = 20

#: socket name → host port, for the forwards THIS session created. Teardown removes
#: exactly these, so a forward made by anything else on the machine survives.
_forwards: dict = {}

#: Session-scoped verdict, set by the first failure and cleared by reset().
_unreachable = False

#: Sockets that did not answer. A device carries sockets belonging to other apps
#: and to WebViews that have gone away; one of those must cost a session one
#: timeout, not one per action.
_dead: set = set()

#: The devtools target that last proved to be the page on screen, keyed by the
#: foreground package that owned it. The empty key retains the original public
#: no-package behaviour for callers that do not know the foreground app.
_remembered: dict[str, str] = {}

#: Whether the "no devtools socket" diagnostic (see mark_no_socket) has already
#: been logged this session. Set by the first firing, cleared by reset().
_no_socket_reported = False


def reset() -> None:
    """Release this session's forwards and re-arm discovery."""
    global _unreachable, _remembered, _no_socket_reported
    for port in list(_forwards.values()):
        try:
            _adb("forward", "--remove", f"tcp:{port}", timeout=5)
        except Exception as e:  # noqa: BLE001 — teardown must not replace a verdict
            _log.debug("[web] could not remove forward tcp:%d: %s", port, e)
    _forwards.clear()
    _dead.clear()
    _unreachable = False
    _remembered.clear()
    _no_socket_reported = False
    # Tab ordering is scoped to the same debug-channel lifetime.  Import late to
    # keep this low-level transport independent during module initialization.
    from testmu_appium._helpers.tabs import reset_tabs  # noqa: PLC0415
    reset_tabs()
    # The iOS provider keeps its own claims — an ios_webkit_debug_proxy child
    # process, its port, a remembered target and a sticky unreachable verdict —
    # and session teardown lands HERE for every platform. Reached through
    # sys.modules so an Android-only process never imports the iOS module just
    # to find nothing to release.
    ios = sys.modules.get("testmu_appium._helpers._web_ios")
    if ios is not None:
        ios.reset()
    remote = sys.modules.get("testmu_appium._helpers._web_remote")
    if remote is not None:
        remote.reset()


def remember_target(ws_url: str, package: str = "") -> None:
    """Remember a proven target for one foreground package.

    ``package`` is optional for compatibility with the original transport
    contract and with tab-management callers that operate on a browser endpoint
    rather than a foreground-app surface.
    """
    key = package or ""
    if ws_url:
        _remembered[key] = ws_url
    elif not package:
        # Historically ``remember_target("")`` cleared the only remembered
        # value. Keep it as the all-packages invalidation used by tab switches
        # and compatibility callers.
        _remembered.clear()
    else:
        _remembered.pop(key, None)


def remembered_target(package: str = "") -> str:
    return _remembered.get(package or "", "")


def reachable() -> bool:
    """Whether this session may look for devtools sockets at all."""
    platform = _config.platform()
    if platform != "android":
        raise UnsupportedOnPlatform("web debug channel", platform)
    return _config.run_target == "local" and not _unreachable


def mark_unreachable(error: BaseException) -> None:
    """Record that the device's debug channel cannot be reached this session.

    One failed attempt, not one per action: a device with no adb, no sockets or no
    debuggable web content answers the same way every time.
    """
    global _unreachable
    _unreachable = True
    _log.info(
        "[web] no reachable debug channel (%s); the accessibility projection "
        "serves web content for the rest of this session", error)


def mark_dead(socket: "Socket", error: BaseException) -> None:
    """Record that a socket does not answer, so this session stops asking."""
    _dead.add(socket.name)
    _log.info("[web] socket %s did not answer (%s); skipping it for the rest of "
              "this session", socket.name, error)


def is_dead(socket: "Socket") -> bool:
    return socket.name in _dead


def mark_no_socket(package: str) -> None:
    """Record that the foreground app publishes no devtools socket at all.

    Distinct from `mark_dead`: a socket that does not answer is a transport
    fact and may answer on a later action, but an app with no socket to answer
    on has webview debugging disabled in its build, which does not change for
    the rest of the session. Reported once, not once per action.
    """
    global _no_socket_reported
    if _no_socket_reported:
        return
    _no_socket_reported = True
    _log.info("[web] %s publishes no devtools socket — webview debugging is not "
              "enabled in this build", package)


def _adb(*args, timeout=_ADB_TIMEOUT_S) -> str:
    """One adb command against the configured device."""
    serial = _config.get("udid")
    prefix = ["adb", "-s", str(serial)] if serial else ["adb"]
    result = subprocess.run(  # noqa: S603 — fixed executable, no shell
        [*prefix, *args], capture_output=True, text=True, timeout=timeout)
    if result.returncode != 0:
        raise RuntimeError(
            f"adb {' '.join(args)} failed: {(result.stderr or result.stdout).strip()[:200]}")
    return result.stdout.strip()


def sockets() -> list:
    """Devtools sockets the device is publishing right now."""
    return discover_sockets(_adb("shell", "cat", "/proc/net/unix"))


def pids_of(package: str):
    """Every pid a package is running under, or None when it is not running.

    This is what ties a `webview_devtools_remote_<pid>` socket to the app that
    owns it — without it every other app's WebView is a candidate, and a stale
    one costs a connection timeout before it can be ruled out.

    A package commonly runs in more than one process: a component declared with
    `android:process=":name"` runs as `<package>:name`, a distinct process with
    its own pid, and the WebView need not live in the main one. `pidof` reports
    only the main process, so a WebView hosted in a child process reads as
    unowned and is filtered out along with every other app's. `ps -A` lists
    every process on the device with its pid and name, so a process is matched
    by its name being exactly the package or `<package>:`-prefixed — a name that
    merely shares the package as a text prefix (`com.app.other` against
    `com.app`) is not a match.
    """
    if not package:
        return None
    try:
        out = _adb("shell", "ps", "-A", timeout=10)
    except Exception as e:  # noqa: BLE001 — a device that cannot list processes reports none
        _log.debug("[web] ps -A (%s): %s", package, e)
        return None
    prefix = f"{package}:"
    found = set()
    for line in out.splitlines():
        fields = line.split()
        if len(fields) < 2 or not fields[1].isdigit():
            continue
        name = fields[-1]
        if name == package or name.startswith(prefix):
            found.add(int(fields[1]))
    return found or None


def forward(socket: Socket) -> int:
    """A host port reaching this device socket, created once per session."""
    if socket.name in _forwards:
        return _forwards[socket.name]
    port = int(_adb("forward", "tcp:0", f"localabstract:{socket.name}"))
    _forwards[socket.name] = port
    _log.info("[web] %s socket %s forwarded to 127.0.0.1:%d",
              socket.kind, socket.name, port)
    return port


#: platform → how many device units one CSS pixel spans, before zoom.
#:
#: The difference is what the OS reports element boxes in, and it is not a
#: detail: Android's accessibility tree is in device PIXELS, so a CSS pixel is
#: `dpr` of them. iOS's tree is in POINTS, and a CSS pixel IS a point — `dpr`
#: there describes the backing store, which neither side's coordinates are
#: expressed in. Appium taps iOS in points too, so the whole pipeline is points.
#:
#: Measured on a device rather than reasoned about, because the failure is
#: silent. Solving the origin from 10 samples of a Google page:
#:
#:     factor = dpr*scale = 2   origins (5,141) (-59,157) (-198,141) …   0/10 agree
#:     factor = scale     = 1   origins (5,141) (13,157) (5,141) …       8/10 agree
#:
#: A wrong factor does not misplace the page by a constant — every element
#: solves a DIFFERENT origin, so calibration finds no majority and the surface
#: is silently dropped as unplaceable. The whole web reader then looks absent
#: rather than broken.
_CSS_TO_DEVICE = {
    "android": lambda dpr, scale: float(dpr) * float(scale),
    "ios": lambda dpr, scale: float(scale),
}


def _viewport_factor(dpr: float, scale: float) -> float:
    """CSS pixels to device units, or raise.

    A zero on either term is not a viewport we can convert against; returning a
    point anyway would place a tap at the origin with full confidence.
    """
    platform = (_config.platform() or "").lower()
    try:
        convert = _CSS_TO_DEVICE[platform]
    except KeyError:
        raise UnsupportedOnPlatform("web viewport conversion", platform) from None
    factor = convert(dpr, scale)
    if factor <= 0:
        raise ValueError(f"degenerate viewport: dpr={dpr!r} scale={scale!r}")
    return factor


def derive_origin(css, native_bounds, dpr, scale, offset_left=0, offset_top=0):
    """Solve for the web content's device-space origin.

    `css` is a point in page coordinates and `native_bounds` is where the OS
    reported that same element, so the difference is the origin. Deriving it
    beats assuming it from the WebView node: the WebView's own bounds do not
    account for browser chrome drawn inside it.

    The panning term is part of the model, not of the conversion alone: solving
    without it and then converting with it subtracts the pan twice, which on a
    pinch-panned page at dpr 3 and scale 2 is 300 device pixels of confident
    error. Every sample shifts by the same amount, so the agreement check cannot
    see it.
    """
    factor = _viewport_factor(dpr, scale)
    return (round(native_bounds[0] - (css[0] - offset_left) * factor),
            round(native_bounds[1] - (css[1] - offset_top) * factor))


def to_device(css_x, css_y, origin, dpr, scale, offset_left=0, offset_top=0):
    """A CSS point as a device point.

    `scale` is the visual viewport's zoom. Omitting it is worth several hundred
    pixels on a zoomed page, so it is a required argument rather than a default.
    """
    factor = _viewport_factor(dpr, scale)
    return (round(origin[0] + (css_x - offset_left) * factor),
            round(origin[1] + (css_y - offset_top) * factor))


def agrees(point, native_bounds, tolerance=8):
    """Whether a converted point falls in the box the OS reported for it.

    The check exists because a wrong conversion is silent: it yields a perfectly
    plausible point somewhere else on the screen. Tolerance is applied around the
    box rather than to its centre, so a large element is not judged by how near
    the middle the point landed.
    """
    x1, y1, x2, y2 = native_bounds
    return (x1 - tolerance <= point[0] <= x2 + tolerance
            and y1 - tolerance <= point[1] <= y2 + tolerance)


#: How deep the walk descends. Shadow roots and same-origin frames both count as
#: one level, so the cross cases (shadow in frame, frame in shadow) need no
#: special handling. Measured depth on real pages was 2; the bound is defensive.
MAX_WALK_DEPTH = 12

#: Nodes whose text is source code rather than content. CDP's innerText picks
#: these up; the accessibility projection never does.
_NON_CONTENT_TAGS = frozenset({"SCRIPT", "STYLE", "NOSCRIPT", "TEMPLATE", "HEAD"})

WALK_JS = """
(() => {
  const MAX_DEPTH = %d;
  const out = [];
  let blocked = 0, shadowRoots = 0, frames = 0, transformed = 0;
  const vv = window.visualViewport || {};
  const blockedUrls = [];
  const interactiveTags = new Set(
    ['A', 'BUTTON', 'INPUT', 'TEXTAREA', 'SELECT', 'SUMMARY', 'LABEL', 'OPTION']);
  const interactiveRoles = new Set([
    'button', 'link', 'tab', 'checkbox', 'radio', 'switch', 'textbox',
    'searchbox', 'combobox', 'option', 'menuitem', 'menuitemcheckbox',
    'menuitemradio', 'slider', 'spinbutton', 'treeitem'
  ]);
  const editableInputTypes = new Set([
    '', 'email', 'number', 'password', 'search', 'tel', 'text', 'url'
  ]);
  const modalByDocument = new WeakMap();
  const absolute = (src) => {
    try { return new URL(src || 'about:blank', location.href).href; }
    catch (e) { return 'about:blank'; }
  };
  const composedParent = (el) => {
    if (el.parentElement) return el.parentElement;
    const root = el.getRootNode ? el.getRootNode() : null;
    return root && root.host ? root.host : null;
  };
  const styleOf = (el) => {
    const view = el.ownerDocument && el.ownerDocument.defaultView;
    return (view || window).getComputedStyle(el);
  };
  const ariaHiddenOrInert = (el) => {
    for (let current = el; current; current = composedParent(current)) {
      if ((current.getAttribute('aria-hidden') || '').toLowerCase() === 'true') {
        return true;
      }
      if (current.inert || current.hasAttribute('inert')) return true;
    }
    return false;
  };
  const potentiallyVisible = (el) => {
    if (typeof el.checkVisibility === 'function') {
      return el.checkVisibility({checkOpacity: true, checkVisibilityCSS: true});
    }
    const style = styleOf(el);
    return style.display !== 'none' && style.visibility !== 'hidden'
      && Number(style.opacity) !== 0;
  };
  const activeModal = (doc) => {
    if (modalByDocument.has(doc)) return modalByDocument.get(doc);
    let modal = null;
    try { modal = doc.querySelector('dialog:modal'); } catch (e) {}
    if (!modal) {
      modal = Array.from(
        doc.querySelectorAll('[role="dialog"][aria-modal="true"]')
      ).find((candidate) => {
        const box = candidate.getBoundingClientRect();
        return box.width > 0 && box.height > 0 && potentiallyVisible(candidate);
      }) || null;
    }
    modalByDocument.set(doc, modal);
    return modal;
  };
  const insideActiveModal = (el) => {
    const modal = activeModal(el.ownerDocument);
    if (!modal) return true;
    for (let current = el; current; current = composedParent(current)) {
      if (current === modal) return true;
    }
    return false;
  };
  // Whether an ancestor's box is the one a positioned descendant is laid out
  // against. `position: fixed` normally resolves against the viewport, but any
  // of these properties makes an ancestor the containing block instead — at
  // which point its overflow DOES clip.
  const anchorsPositioned = (style) => {
    return style.transform !== 'none' || style.perspective !== 'none'
      || style.filter !== 'none'
      || (style.willChange || '').indexOf('transform') !== -1
      || (style.contain || '').indexOf('paint') !== -1
      || (style.contain || '').indexOf('layout') !== -1;
  };
  // Whether this element is cut off by an ancestor that clips its overflow.
  //
  // Comparing rectangles alone is not enough, and the failure is total rather
  // than cosmetic. `overflow` clips a descendant only when the clipping element
  // is on that descendant's CONTAINING BLOCK chain — a `position: fixed` subtree
  // resolves against the viewport, so an ancestor's overflow never reaches it.
  //
  // Measured on Google's search suggestions, which are a fixed overlay inside a
  // static `<form class="tsf">` collapsed to height 0 at y=182 with
  // overflow:hidden. The overlay draws at y=4; the naive test read "bottom 52 <=
  // top 182" and called it clipped. Everything the overlay contains — the Ask
  // Google box and every suggestion on screen — was dropped before any filter or
  // role mapping ran, while the stale homepage BEHIND the overlay survived,
  // because it is not inside the fixed subtree. The page the model was given was
  // the one it could not see.
  const clippedOut = (el, rect) => {
    let position = styleOf(el).position;
    for (let parent = composedParent(el); parent; parent = composedParent(parent)) {
      if (parent.ownerDocument !== el.ownerDocument) break;
      const style = styleOf(parent);
      const anchors = anchorsPositioned(style);
      const escapes = (position === 'fixed' && !anchors)
        || (position === 'absolute' && style.position === 'static' && !anchors);
      if (!escapes) {
        const clipsX = style.overflowX === 'hidden' || style.overflowX === 'clip';
        const clipsY = style.overflowY === 'hidden' || style.overflowY === 'clip';
        if (clipsX || clipsY) {
          const box = parent.getBoundingClientRect();
          if ((clipsX && (rect.right <= box.left || rect.left >= box.right))
              || (clipsY && (rect.bottom <= box.top || rect.top >= box.bottom))) {
            return true;
          }
        }
      }
      // Past its containing block the subtree is in that ancestor's flow again,
      // so ancestors above this one clip it the ordinary way.
      if (position === 'fixed' && anchors) position = 'static';
      else if (position === 'absolute'
               && (style.position !== 'static' || anchors)) position = 'static';
      // Then ascend: this parent becomes the subtree root, so from here up it is
      // the PARENT's positioning that decides what clips. The element itself is
      // usually static and the escape belongs to an ancestor — Google's overlay
      // is a fixed DIV wrapping a static textarea — so reading only the starting
      // element's position finds no escape and clips the whole subtree away.
      if (style.position === 'fixed' || style.position === 'absolute') {
        position = style.position;
      }
    }
    return false;
  };
  const isVisible = (el, rect, hiddenByHost) => {
    return !hiddenByHost && potentiallyVisible(el) && !ariaHiddenOrInert(el)
      && insideActiveModal(el) && !clippedOut(el, rect);
  };
  const isInteractive = (el) => {
    const role = el.getAttribute('role') || '';
    return interactiveTags.has(el.tagName) || interactiveRoles.has(role.toLowerCase());
  };
  const isCompoundInteractive = (el) => {
    if (!isInteractive(el)) return false;
    const lines = String(el.innerText || '').split(/\\n+/)
      .map((line) => line.trim()).filter(Boolean);
    return new Set(lines).size > 1;
  };
  const isEditable = (el) => {
    const role = (el.getAttribute('role') || '').toLowerCase();
    if (el.getAttribute('aria-readonly') === 'true'
        || (('readOnly' in el) && el.readOnly === true)) {
      return false;
    }
    const writableInput = el.tagName === 'INPUT'
      && editableInputTypes.has((el.getAttribute('type') || '').toLowerCase());
    return el.isContentEditable || writableInput || el.tagName === 'TEXTAREA'
      || role === 'textbox' || role === 'searchbox';
  };
  const ownsRenderedText = (el) => {
    if (el.tagName === 'HTML' || el.tagName === 'BODY' || isInteractive(el)) {
      return false;
    }
    if (!(el.innerText || '').trim()) return false;
    return !Array.from(el.children).some((child) => {
      const display = styleOf(child).display;
      const block = display !== 'contents' && !display.startsWith('inline');
      return block && (child.innerText || '').trim()
        && potentiallyVisible(child) && !ariaHiddenOrInert(child);
    });
  };
  const ownText = (el) => {
    for (let parent = composedParent(el); parent; parent = composedParent(parent)) {
      if (isInteractive(parent) && !isCompoundInteractive(parent)) return '';
    }
    if (!ownsRenderedText(el)) return '';
    const display = styleOf(el).display;
    const parent = composedParent(el);
    if ((display === 'contents' || display.startsWith('inline'))
        && parent && ownsRenderedText(parent)) {
      return '';
    }
    return el.innerText || '';
  };
  const structuralPath = (el, root) => {
    const nodes = [];
    for (let current = el; current && current !== root;) {
      const parent = current.parentNode;
      if (!parent || !parent.children) return null;
      const index = Array.prototype.indexOf.call(parent.children, current);
      if (index < 0) return null;
      nodes.unshift(index);
      current = parent;
    }
    return nodes;
  };
  // Ids a framework minted for this render. Mirrors the ranker's _GENERATED_ID
  // so the two agree on what counts as a durable id; an id that changes per
  // session is unique and worthless.
  const GENERATED_ID = /\\d{4,}|(?:ember|react-select)[-_]?\\d+/i;
  // A CSS selector that names THIS element rather than its kind.
  //
  // `css` is `#id` when the element has one and the bare tag name otherwise,
  // and a bare tag is rejected downstream as naming a kind rather than one
  // element — correctly, but it leaves nothing. Measured on a Google page: 64 of
  // 68 web rows carried an unusable selector, so an element the model had
  // resolved still could not be acted on.
  //
  // Published ALONGSIDE `css`, never replacing it, so every selector that works
  // today is byte-identical and only rows that had nothing gain something.
  const cssPathFor = (el) => {
    const parts = [];
    for (let cur = el; cur && cur.nodeType === 1 && parts.length < 8;
         cur = cur.parentElement) {
      if (cur.id && !GENERATED_ID.test(cur.id)) {
        parts.unshift('#' + cur.id);
        return parts.join(' > ');
      }
      let part = cur.tagName.toLowerCase();
      const parent = cur.parentElement;
      if (!parent) { parts.unshift(part); break; }
      const twins = Array.prototype.filter.call(
        parent.children, (c) => c.tagName === cur.tagName);
      if (twins.length > 1) {
        part += ':nth-of-type(' + (Array.prototype.indexOf.call(twins, cur) + 1) + ')';
      }
      parts.unshift(part);
    }
    return parts.join(' > ');
  };
  const statesOf = (el) => {
    const states = [];
    if (el.disabled === true || el.getAttribute('aria-disabled') === 'true') {
      states.push('disabled');
    }
    if (el.readOnly === true || el.getAttribute('aria-readonly') === 'true') {
      states.push('readonly');
    }
    if (el.checked === true || el.getAttribute('aria-checked') === 'true') {
      states.push('checked');
    }
    if (el.selected === true || el.getAttribute('aria-selected') === 'true') {
      states.push('selected');
    }
    if (el.getAttribute('aria-expanded') === 'true') states.push('expanded');
    if (el.getAttribute('aria-expanded') === 'false') states.push('collapsed');
    return states;
  };
  const walk = (root, depth, path, ox, oy, hiddenByHost = false, route = []) => {
    if (depth > MAX_DEPTH) return;
    let nodes;
    try { nodes = root.querySelectorAll('*'); } catch (e) { blocked++; return; }
    for (const el of nodes) {
      const tag = el.tagName;
      const rect = el.getBoundingClientRect();
      const role = el.getAttribute('role') || '';
      const aria = el.getAttribute('aria-label') || '';
      const interactive = isInteractive(el);
      const localPath = structuralPath(el, root);
      const fieldLabel = Array.from(el.labels || [])
        .map((candidate) => candidate.innerText || '').join(' ').trim();
      // `value` is a number on progress, meter and a numbered list item, so the
      // fallback chain can yield a non-string and String() is what makes trim
      // safe to call on every element. Editable values are deliberately omitted:
      // they are user data, not the stable name of the field.
      const label = String(
        aria || fieldLabel || el.getAttribute('placeholder')
        || (interactive ? el.innerText : ownText(el))
        || (isEditable(el) ? '' : el.value) || ''
      ).trim().slice(0, 80);
      const visible = isVisible(el, rect, hiddenByHost);
      if (visible) {
        out.push({
          tag: tag, role: role, label: label, interactive: interactive,
          editable: isEditable(el),
          input_type: tag === 'INPUT'
            ? (el.getAttribute('type') || '').toLowerCase() : '',
          disabled: el.disabled === true || el.getAttribute('aria-disabled') === 'true',
          states: statesOf(el),
          visible: true, clause: aria ? 'aria-label' : 'text',
          // The placeholder, kept SEPARATE rather than folded into `label`.
          // The label chain is `aria || fieldLabel || placeholder || ...`, which
          // short-circuits: an element with both publishes only the aria-label,
          // and the placeholder is the string a person actually sees. Google's
          // box is aria-label "Google Search" / placeholder "Ask Google", so an
          // objective naming what is on screen matched nothing in the document.
          placeholder: el.getAttribute('placeholder') || '',
          css: el.id ? '#' + el.id : tag.toLowerCase(),
          css_path: cssPathFor(el),
          dom_path: localPath === null ? null
            : route.concat([{kind: 'element', nodes: localPath}]),
          x: rect.x + ox, y: rect.y + oy, w: rect.width, h: rect.height,
          depth: depth, path: path
        });
      }
      if (el.shadowRoot) {
        const shadowRoute = localPath === null ? null
          : route.concat([{kind: 'shadow', nodes: localPath}]);
        if (shadowRoute !== null) {
        walk(el.shadowRoot, depth + 1, path + '>s' + (shadowRoots++), ox, oy,
             hiddenByHost, shadowRoute);
        }
      }
      if (tag === 'IFRAME') {
        const index = frames++;
        try {
          const doc = el.contentDocument;
          if (doc) {
            // Composing frame geometry by translation alone is only right while
            // the frame is drawn at its own scale. A CSS-transformed frame shows
            // up as a mismatch between the box it occupies and the viewport its
            // children measure against, and its children are skipped rather than
            // placed by arithmetic that does not describe them.
            const inner = doc.documentElement ? doc.documentElement.clientWidth : 0;
            const outer = rect.width - 2 * el.clientLeft;
            if (inner && Math.abs(outer - inner) > 4) {
              transformed++;
            } else {
              const frameRoute = localPath === null ? null
                : route.concat([{kind: 'frame', nodes: localPath}]);
              // A frame's rects are measured against ITS OWN viewport, so the
              // frame's position on the page is carried down and added to them.
              if (frameRoute !== null) {
                walk(doc, depth + 1, path + '>f' + index,
                     ox + rect.x + el.clientLeft, oy + rect.y + el.clientTop,
                     hiddenByHost || !visible, frameRoute);
              }
            }
          } else if (visible) {
            blocked++;
            blockedUrls.push(absolute(el.src));
          }
        } catch (e) {
          if (visible) {
            blocked++;
            blockedUrls.push(absolute(el.src));
          }
        }
      }
    }
  };
  walk(document, 0, '', 0, 0, false, []);
  return JSON.stringify({
    dpr: window.devicePixelRatio, scale: vv.scale || 1,
    scrollX: window.scrollX, scrollY: window.scrollY,
    offsetLeft: vv.offsetLeft || 0, offsetTop: vv.offsetTop || 0,
    viewportWidth: window.innerWidth, viewportHeight: window.innerHeight,
    visualWidth: vv.width || window.innerWidth,
    visualHeight: vv.height || window.innerHeight,
    shadowRoots: shadowRoots, frames: frames, blockedFrames: blocked,
    transformedFrames: transformed,
    blockedUrls: blockedUrls, elements: out
  });
})()
""" % MAX_WALK_DEPTH


def viewport_box(page):
    """The rectangle of the page a user can actually see, in CSS pixels.

    On a pinch-zoomed page that is the VISUAL viewport — a window onto the layout
    viewport, offset by however far the user has panned. Filtering against the
    layout viewport instead would keep elements that are on the page but off the
    screen.
    """
    left = page.get("offsetLeft", 0) or 0
    top = page.get("offsetTop", 0) or 0
    width = page.get("visualWidth") or page.get("viewportWidth") or 0
    height = page.get("visualHeight") or page.get("viewportHeight") or 0
    return (left, top, left + width, top + height)


def visible_part(element, box):
    """The part of an element inside `box`, or None when none of it is.

    An element half off the left edge is still actable — at the middle of the part
    that is on screen. Its full-rectangle centre can be off the screen entirely:
    one at x=-90 w=100 has its centre at x=-40.
    """
    left, top, right, bottom = box
    x1 = max(element.get("x", 0), left)
    y1 = max(element.get("y", 0), top)
    x2 = min(element.get("x", 0) + element.get("w", 0), right)
    y2 = min(element.get("y", 0) + element.get("h", 0), bottom)
    if x2 <= x1 or y2 <= y1:
        return None
    return (x1, y1, x2, y2)


def usable(elements, viewport=None):
    """Elements worth reading from the page.

    Drops source bodies, zero-sized nodes and anything the walk found hidden.
    When a viewport is supplied it also returns the subset currently on screen;
    omitting one preserves real offscreen boxes for reading and scrolling.

    `viewport` is either a (width, height) pair or the page dict, in which case
    the visual viewport and any panning are honoured.
    """
    box = None
    if viewport is not None:
        box = (viewport_box(viewport) if isinstance(viewport, dict)
               else (0, 0, viewport[0], viewport[1]))
    kept = []
    for element in elements:
        if element.get("tag", "").upper() in _NON_CONTENT_TAGS:
            continue
        if element.get("visible") is False:
            continue
        if element.get("w", 0) <= 0 or element.get("h", 0) <= 0:
            continue
        if box is not None and visible_part(element, box) is None:
            continue
        kept.append(element)
    return kept


#: Chrome refuses a devtools WebSocket carrying a browser Origin header, with
#: `403 Rejected an incoming WebSocket connection from the http://127.0.0.1:<port>
#: origin`. The header must be suppressed, not set to something plausible.
_SUPPRESS_ORIGIN = True

#: Connect + first-response budget for a devtools call. A live page answers a
#: full pierced walk in a few hundred milliseconds — 349 ms measured end to end,
#: adb included. The budget is not for that: it is how long a target belonging to
#: a frozen background tab or a WebView that has gone away is waited on before it
#: is written off, and a scan pays it once per such target.
_CDP_TIMEOUT_S = 3.0


def list_targets(port):
    """Page targets on a forwarded devtools port, newest protocol first.

    Only `page` targets are returned: a socket also advertises service workers
    and background pages, which have no geometry and cannot be acted on.
    """
    raw = urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=8).read()
    return [t for t in json.loads(raw)
            if t.get("type") == "page" and t.get("webSocketDebuggerUrl")]


class Channel:
    """One devtools connection to one page target.

    A connection per call rather than a long-lived socket: a devtools socket
    outlives neither a page navigation nor a WebView teardown, and a stale one
    fails in ways that look like an empty page.
    """

    def __init__(self, ws_url, websocket_module=None, timeout=_CDP_TIMEOUT_S):
        self._ws_url = ws_url
        self._id = 0
        self._timeout = timeout
        if websocket_module is None:
            import websocket as websocket_module  # noqa: PLC0415
        self._ws = websocket_module

    def call(self, method, params=None):
        self._id += 1
        connection = self._ws.create_connection(
            self._ws_url, timeout=self._timeout, suppress_origin=_SUPPRESS_ORIGIN)
        try:
            connection.send(json.dumps(
                {"id": self._id, "method": method, "params": params or {}}))
            while True:
                message = json.loads(connection.recv())
                if message.get("id") == self._id:
                    if "error" in message:
                        raise RuntimeError(f"{method}: {message['error']}")
                    return message.get("result", {})
        finally:
            connection.close()

    def call_function(self, function_declaration, arguments=()):
        """Invoke a page function with structured CDP arguments.

        ``Runtime.evaluate`` does not accept arguments. Embedding values into its
        JavaScript expression would make storage and other value-carrying verbs
        vulnerable to quoting mistakes and script injection. Resolve the page's
        global object and call the function on the SAME DevTools connection so
        its session-scoped ``objectId`` remains valid.
        """
        connection = self._ws.create_connection(
            self._ws_url, timeout=self._timeout, suppress_origin=_SUPPRESS_ORIGIN)
        try:
            self._id += 1
            connection.send(json.dumps({
                "id": self._id,
                "method": "Runtime.evaluate",
                "params": {"expression": "globalThis", "returnByValue": False},
            }))
            evaluated = self._receive(connection, self._id, "Runtime.evaluate")
            object_id = evaluated.get("result", {}).get("objectId")
            if not object_id:
                raise RuntimeError(
                    "Runtime.evaluate: visible page returned no global object"
                )

            self._id += 1
            connection.send(json.dumps({
                "id": self._id,
                "method": "Runtime.callFunctionOn",
                "params": {
                    "functionDeclaration": function_declaration,
                    "objectId": object_id,
                    "arguments": [{"value": value} for value in arguments],
                    "returnByValue": True,
                    "awaitPromise": True,
                },
            }))
            called = self._receive(
                connection, self._id, "Runtime.callFunctionOn"
            )
            if called.get("exceptionDetails"):
                raise RuntimeError(
                    "Runtime.callFunctionOn: page function raised an exception"
                )
            return called.get("result", {}).get("value")
        finally:
            connection.close()

    @staticmethod
    def _receive(connection, request_id, method):
        while True:
            message = json.loads(connection.recv())
            if message.get("id") != request_id:
                continue
            if "error" in message:
                raise RuntimeError(f"{method}: {message['error']}")
            return message.get("result", {})

    def evaluate(self, expression, context_id=None):
        """The expression's value, or None where it produced none.

        A script that THREW also produces none, and the two are indistinguishable
        in the return. Callers read that as an empty page, so the throw is
        reported here — a walk that crashes on one element otherwise takes the
        whole surface with it and leaves nothing in the log to say so.
        """
        params = {"expression": expression, "returnByValue": True}
        if context_id is not None:
            params["contextId"] = context_id
        answer = self.call("Runtime.evaluate", params)
        details = answer.get("exceptionDetails")
        if details:
            described = ((details.get("exception") or {}).get("description")
                         or details.get("text") or "")
            _log.warning("    [web] a page script threw; its result reads as "
                         "empty: %s", described.splitlines()[0][:200])
        return answer.get("result", {}).get("value")

    # ── page state: cookies and history ─────────────────────────────────
    #
    # These live on the CHANNEL rather than in the verb modules because they are
    # the part that differs by protocol: Chrome answers in the Network/Storage
    # vocabulary below, WebKit in its own (see IosChannel). The verbs validate
    # and log; the channel is what knows how to say it on this wire.

    def get_cookies(self) -> list:
        """Every cookie the browser holds, in the wire's own field names."""
        return self.call("Storage.getCookies").get("cookies", [])

    def set_cookies(self, params: list) -> None:
        """Set already-validated cookie params in one wire call."""
        self.call("Network.setCookies", {"cookies": params})

    def delete_cookie(self, cookie: dict) -> None:
        """Delete one cookie AS ENUMERATED — scope fields ride along so the
        deletion lands on the same cookie the read described."""
        params = {"name": cookie["name"]}
        for field in ("domain", "path", "partitionKey"):
            if cookie.get(field) is not None:
                params[field] = cookie[field]
        self.call("Network.deleteCookies", params)

    def clear_cookies(self) -> None:
        self.call("Network.clearBrowserCookies")

    def navigate_history(self, delta: int) -> bool:
        """Move ``delta`` entries through this page's history.

        False means the boundary was already reached — this wire can ask WHERE
        it stands (``Page.getNavigationHistory``) before it moves, so a back at
        the first entry reports "did not move" rather than silently staying.
        """
        history = self.call("Page.getNavigationHistory")
        entries = history.get("entries") or []
        current = history.get("currentIndex")
        if not isinstance(current, int):
            raise RuntimeError("Page.getNavigationHistory returned no currentIndex")
        target = current + delta
        if target < 0 or target >= len(entries):
            return False
        entry_id = entries[target].get("id")
        if entry_id is None:
            raise RuntimeError("Page.getNavigationHistory returned an entry without id")
        self.call("Page.navigateToHistoryEntry", {"entryId": entry_id})
        return True

    def is_visible(self):
        """Whether this page is the one being displayed.

        The page knows. Measured on a device with 16 open targets: exactly one
        reported `visible`, and five tabs of the SAME site all reported `hidden` —
        which is the case no amount of comparing content against the accessibility
        tree can separate. An in-app WebView reports it too, and flips to `hidden`
        when its app goes to the background.
        """
        return self.evaluate("document.visibilityState") == "visible"

    def scroll_position(self):
        """Where the page is scrolled to, as one cheap evaluate.

        Compared against the position the walk recorded: a page still moving when
        it was read has a stale geometry, and every calibration sample shifts by
        the same amount so their agreement says nothing.
        """
        raw = self.evaluate("window.scrollX + ',' + window.scrollY")
        left, _, top = str(raw or "0,0").partition(",")
        return (float(left or 0), float(top or 0))

    def read_page(self):
        """The pierced page: elements, geometry, and what the walk could not reach."""
        raw = self.evaluate(WALK_JS)
        return json.loads(raw) if raw else {"elements": [], "blockedFrames": 0}

    def unreachable_frames(self, page, seen=()):
        """Frames the JS walk could not enter, as (frame_id, url) pairs.

        A cross-origin frame returns null for `contentDocument`, so the walk sees
        nothing inside it and says so rather than reporting a partial page as a
        whole one. These are read through their own execution context instead.

        Only the frames the walk NAMED as blocked are returned. The frame tree
        also lists every frame the walk already descended, and reading one of
        those again would put each of its elements in the candidate pool twice —
        which the cardinality-1 rule then reads as ambiguity and skips.
        """
        blocked = {url for url in (page or {}).get("blockedUrls", []) if url}
        blocked -= set(seen)
        if not blocked:
            return []
        tree = self.call("Page.getFrameTree").get("frameTree", {})
        found = []

        def descend(node, is_root):
            frame = node.get("frame", {})
            if not is_root and frame.get("url", "") in blocked:
                found.append((frame.get("id"), frame.get("url", "")))
            for child in node.get("childFrames", []):
                descend(child, False)

        descend(tree, True)
        return found

    def read_frame(self, frame_id, path=""):
        """Read one frame through an isolated world in it.

        This is what recovers a cross-origin frame: the walk cannot cross the
        boundary, but an execution context created inside the frame can read it.

        The rects come back measured against the FRAME's viewport, so the frame's
        own position is added to them — otherwise a frame halfway down the page
        reports its contents as though they were at the top of the screen.

        `path` prefixes the frame's own paths. The walk inside a recovered frame
        starts at the root and would otherwise label its elements as belonging to
        the top document, which is the one place they are certainly not.
        """
        world = self.call("Page.createIsolatedWorld",
                          {"frameId": frame_id, "worldName": "testmu_probe"})
        context = world.get("executionContextId")
        if context is None:
            return None
        raw = self.evaluate(WALK_JS, context_id=context)
        if not raw:
            return None
        page = json.loads(raw)
        offset = self.frame_offset(frame_id)
        if offset is None:
            # Placing it at (0,0) would put its contents over the top document,
            # which is a confident tap in the wrong place rather than a missing
            # one.
            _log.info("    [web] frame %s could not be located in the page; "
                      "its contents are not usable", frame_id)
            return None
        for element in page.get("elements", []):
            element["x"] += offset[0]
            element["y"] += offset[1]
            element["path"] = path + element.get("path", "")
            # The isolated-world id is short-lived, but the frame id is stable for
            # this document and lets a later descriptor scroll be evaluated in the
            # same cross-origin frame without exposing it to the autoheal service.
            element["frame_id"] = frame_id
        return page

    def evaluate_in_frame(self, frame_id, expression):
        """Evaluate in a fresh isolated world for ``frame_id``.

        Execution-context ids are invalidated by navigation, so callers retain
        only the frame id and create a world immediately before the operation.
        """
        world = self.call(
            "Page.createIsolatedWorld",
            {"frameId": frame_id, "worldName": "testmu_action"},
        )
        context = world.get("executionContextId")
        if context is None:
            return None
        return self.evaluate(expression, context_id=context)

    def scroll_frame_into_view(self, frame_id):
        """Ask CDP to reveal the owner of a cross-origin frame."""
        owner = self.call("DOM.getFrameOwner", {"frameId": frame_id})
        node = owner.get("backendNodeId")
        if node is None:
            return False
        self.call("DOM.scrollIntoViewIfNeeded", {"backendNodeId": node})
        return True

    def frame_offset(self, frame_id):
        """Where a frame's own viewport sits in the top document, or None.

        The frame's owning `<iframe>` is resolved through the DOM domain because
        the JS walk never saw it as a container — a cross-origin frame is exactly
        the one the walk could not enter.

        None means "cannot say", and the caller drops the frame. A frame placed at
        (0,0) because its owner could not be resolved reports a control 400 px down
        the page as though it were at the top of the screen.
        """
        owner = self.call("DOM.getFrameOwner", {"frameId": frame_id})
        node = owner.get("backendNodeId")
        if node is None:
            return None
        box = self.call("DOM.getBoxModel", {"backendNodeId": node}).get("model", {})
        content = box.get("content")
        if not content:
            return None
        return (content[0], content[1])

    def pierce_closed_roots(self):
        """The structural document including closed shadow roots.

        `.shadowRoot` is null for a closed root by specification, so no script can
        reach one. `pierce` resolves them at engine level.

        NOT in the read path. This returns a node tree with no geometry, and
        turning it into actable rows needs a box-model call per node. Controls that
        exist ONLY inside a closed shadow root are therefore not offered today; the
        mechanism is proven and the flattening is not built.
        """
        return self.call("DOM.getDocument", {"depth": -1, "pierce": True})


class WebDebugTransport(Protocol):
    """Provider boundary for discovering and opening web debug targets.

    The shipped provider is local ADB. A cloud provider can implement this
    contract without changing DOM capture, calibration, healing, or gestures.
    """

    def capabilities(self) -> dict:
        """Versioned provider capabilities for session negotiation."""
        ...

    def reachable(self) -> bool:
        ...

    def remembered_target(self):
        ...

    def remembered_target_for(self, package):
        """The last proven target owned by ``package``, if any."""
        ...

    def channel(self, target_id):
        """Open CDP messaging for a provider-owned opaque target id."""
        ...

    def sockets(self):
        ...

    def pids_of(self, package):
        ...

    def is_dead(self, socket):
        ...

    def forward(self, socket):
        ...

    def list_targets(self, endpoint):
        ...

    def mark_dead(self, socket, cause):
        ...

    def mark_unreachable(self, cause):
        ...

    def mark_no_socket(self, package):
        ...

    def remember_target(self, target_id):
        ...

    def remember_target_for(self, package, target_id):
        ...


class LocalAdbWebDebugTransport:
    """Current local-device implementation of :class:`WebDebugTransport`."""

    def capabilities(self):
        return {
            "contract_version": 1,
            "provider": "local-adb",
            "cdp_rpc": True,
            "session_bound": False,
        }

    def reachable(self):
        return reachable()

    def remembered_target(self):
        return remembered_target()

    def remembered_target_for(self, package):
        return remembered_target(package)

    def channel(self, ws_url):
        return Channel(ws_url)

    def sockets(self):
        return sockets()

    def pids_of(self, package):
        return pids_of(package)

    def is_dead(self, socket):
        return is_dead(socket)

    def forward(self, socket):
        return forward(socket)

    def list_targets(self, port):
        return list_targets(port)

    def mark_dead(self, socket, cause):
        return mark_dead(socket, cause)

    def mark_unreachable(self, cause):
        return mark_unreachable(cause)

    def mark_no_socket(self, package):
        return mark_no_socket(package)

    def remember_target(self, ws_url):
        return remember_target(ws_url)

    def remember_target_for(self, package, ws_url):
        return remember_target(ws_url, package)


_LOCAL_TRANSPORT = LocalAdbWebDebugTransport()

#: platform → a zero-arg factory for its provider. Imported lazily so the Android
#: path never pays for the iOS module and vice versa, and so this module stays
#: importable on a host with neither toolchain installed.
_PROVIDERS: dict = {"android": lambda: _LOCAL_TRANSPORT}


def _ios_transport():
    from testmu_appium._helpers._web_ios import IwdpWebDebugTransport
    return IwdpWebDebugTransport(udid=str(_config.get("udid") or ""))


_PROVIDERS["ios"] = _ios_transport


def debug_transport() -> WebDebugTransport:
    """The active provider for the configured platform.

    Android reaches a page by forwarding the app's own devtools socket; iOS
    reaches every page on the device through one ios_webkit_debug_proxy. Nothing
    above this line knows which — `_action_web` scans, places and reads through
    the same contract either way.
    """
    platform = (_config.platform() or "").lower()
    # A cloud session's device is on a LambdaTest host: neither adb nor an iwdp
    # spawned here can reach it, so its debug channel is published by that
    # host's Mobile Binary instead (see _web_remote).
    from testmu_appium._helpers import _web_remote  # noqa: PLC0415
    if _web_remote.available():
        remote = _web_remote.transport_for(platform)
        if remote is not None:
            return remote
    provider = _PROVIDERS.get(platform)
    if provider is None:
        raise UnsupportedOnPlatform("web debug transport", platform)
    return provider()
