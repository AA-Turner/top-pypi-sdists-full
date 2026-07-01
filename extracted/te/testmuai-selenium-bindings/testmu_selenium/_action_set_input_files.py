"""High-level set_input_files action — find the file <input>, send the path(s),
heal on failure (selector → coordinate).

Mirrors the clear/click/search/hover verbs: the wrapper threads through the
shared find+heal engine (_run_action) so a selectorless vision-agent upload
(empty selector + a description like "choose file") relocates the real
<input type="file"> via the heal cascade before send_keys uploads to it.

Selectorless DOM-first pre-step (V2 handle_upload parity): before the engine,
an empty-selector upload tries a pure-DOM resolve of the <input type="file">
(light + open shadow) — see _FIND_FIRST_FILE_INPUT_JS — because the coordinate
heal below dies when the page has no visible "choose file" element. On a miss it
falls through to the heal cascade unchanged.

Tier: DESKTOP_LOCATE only. LIST_XPATHS was dropped — it "succeeds" on any
non-empty xpaths list (even an unusable relative xpath like ``../div/...`` that
can't resolve), so as the first tier it monopolized the retry budget and the
working coordinate tier never ran (observed in production: 3× LIST_XPATHS,
0× coordinate, upload failed). VISION_QUERY stays out (its relocate needs the
dom-watcher tagify, absent in the exported runtime). DESKTOP_LOCATE
(/v2/locate/desktop — viewport screenshot, Basic auth, no tagify) is the working
tier: we can't send_keys to a pixel, but the coord_runner bridges the healed
coordinate to the file <input> via _RESOLVE_FILE_INPUT_JS.
"""
import logging

from selenium.common.exceptions import NoSuchElementException

from testmu_selenium._action_engine import _ActionSpec, _run_action

_log = logging.getLogger(__name__)

_HEAL_TIERS = ('DESKTOP_LOCATE',)

# Selectorless DOM-first resolver — V2 handle_upload parity (V2 source
# handle_upload). The Vision Agent can persist an upload op with NO
# selector (e.g. intent "choose file", no locator/coords/frame),
# which codegen emits as set_input_files(driver, [], description='choose file').
# The only runtime fallback was the COORDINATE vision heal, which dies when no
# visible "choose file" element exists (prod AutohealExhausted "Coordinates not
# resolved for choose file"). V2 never hit this: handle_upload found the <input
# type=file> via PURE DOM. This mirrors V2's last-resort Strategy 3
# ('//input[@type="file"]' → first match) but is shadow-aware (V2's
# document.evaluate can't cross shadow roots; this recurses OPEN ones), and does
# NOT filter by visibility — file inputs are commonly display:none behind a
# styled trigger (the exact shape that defeats coordinate heal), and send_keys
# works on hidden inputs. Reachability limits (no JS/xpath, incl. V2, can cross
# these): CLOSED shadow roots and CROSS-ORIGIN iframes; same-origin iframes are
# out of scope here (no frame walk) and fall through to the existing heal.
_FIND_FIRST_FILE_INPUT_JS = """
const found = [];
const collect = (root) => {
    let direct = [];
    try { direct = root.querySelectorAll('input[type=file]'); } catch (e) {}
    for (const inp of direct) found.push(inp);
    let all = [];
    try { all = root.querySelectorAll('*'); } catch (e) {}
    for (const host of all) { if (host.shadowRoot) collect(host.shadowRoot); }
};
collect(document);
return found.length ? found[0] : null;
"""


def _resolve_file_input_dom(driver):
    """Locate the first <input type=file> via pure DOM (light + open shadow).

    V2 handle_upload parity for selectorless uploads. Returns the WebElement or
    None — never raises (a probe failure must fall back to the heal path, not
    abort the upload).
    """
    try:
        return driver.execute_script(_FIND_FIRST_FILE_INPUT_JS)
    except Exception:  # noqa: BLE001 — probe is best-effort; fall back on any error
        _log.info("    [upload] DOM file-input probe failed", exc_info=True)
        return None

# Resolve the file <input> from a healed viewport coordinate. Two stages:
#   1. Anchor on the pixel: elementFromPoint, then walk up ancestors AND across
#      OPEN shadow boundaries (shadowRoot / getRootNode().host), checking
#      label.control and each node's shadow/light subtree.
#   2. Shadow-aware global fallback: elementFromPoint returns null for points
#      below the fold and querySelector can't pierce shadow, so recurse the light
#      DOM + every open shadow root, collecting input[type=file], and pick the one
#      nearest the healed pixel. (Prod failure: input nested in an open shadow
#      root at y=2166, far below the 1080 viewport — the old light-DOM-only
#      elementFromPoint/querySelector resolver could never reach it.)
_RESOLVE_FILE_INPUT_JS = """
const x = arguments[0], y = arguments[1];
const isFile = (n) => !!n && n.tagName === 'INPUT' && (n.type || '').toLowerCase() === 'file';

let el = document.elementFromPoint(x, y);
if (isFile(el)) return el;
if (el && el.closest) {
    const lbl = el.closest('label');
    if (lbl && isFile(lbl.control)) return lbl.control;
}
let node = el;
while (node) {
    if (isFile(node)) return node;
    if (node.shadowRoot) {
        const inner = node.shadowRoot.querySelector('input[type=file]');
        if (inner) return inner;
    }
    if (node.querySelector) {
        const inner = node.querySelector('input[type=file]');
        if (inner) return inner;
    }
    const root = node.getRootNode && node.getRootNode();
    node = node.parentElement || (root instanceof ShadowRoot ? root.host : null);
}

const found = [];
const collect = (root) => {
    let direct = [];
    try { direct = root.querySelectorAll('input[type=file]'); } catch (e) {}
    for (const inp of direct) found.push(inp);
    let all = [];
    try { all = root.querySelectorAll('*'); } catch (e) {}
    for (const host of all) { if (host.shadowRoot) collect(host.shadowRoot); }
};
collect(document);
if (found.length === 1) return found[0];
if (found.length > 1) {
    let best = null, bestDist = Infinity;
    for (const inp of found) {
        const r = inp.getBoundingClientRect();
        const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
        const d = (cx - x) * (cx - x) + (cy - y) * (cy - y);
        if (d < bestDist) { bestDist = d; best = inp; }
    }
    return best;
}
return null;
"""


def _path_value(ctx):
    """The send_keys value: newline-joined file_paths, else file_path."""
    file_paths = ctx.get("file_paths")
    if file_paths:
        return "\n".join(str(p) for p in file_paths)
    return str(ctx.get("file_path"))


def _set_input_files_runner(element, ctx):
    """Send the resolved file path(s) to the located <input type="file">.

    Selenium uploads via send_keys on the input element. The list form
    (file_paths) wins when both are present; multiple paths are newline-joined
    per Selenium's multi-file upload convention.
    """
    element.send_keys(_path_value(ctx))
    return None


def _set_input_files_coord_runner(driver, x, y, ctx):
    """DESKTOP_LOCATE-tier path: bridge the healed pixel to the file <input> via
    document.elementFromPoint, then send_keys. Raises NoSuchElementException if
    no file input can be resolved at/near the coordinate."""
    element = driver.execute_script(_RESOLVE_FILE_INPUT_JS, x, y)
    if element is None:
        raise NoSuchElementException(
            f"set_input_files: no <input type='file'> at/near healed coordinate ({x}, {y})"
        )
    element.send_keys(_path_value(ctx))
    return None


_SET_INPUT_FILES_SPEC = _ActionSpec(
    runner=_set_input_files_runner,
    coord_runner=_set_input_files_coord_runner,
)


def set_input_files(driver, selector, *, file_path=None, file_paths=None,
                    description='', tiers=None, autoheal=True,
                    max_attempts=4, retry_delay=0.5, search_root=None,
                    fallback_coordinates=None):
    """Find the file input and send the upload path(s), healing on failure.

    Defaults to DESKTOP_LOCATE only (see module docstring); an explicit ``tiers``
    always wins so codegen can omit it and callers can override.

    fallback_coordinates: recorded authoring-time (x, y) used as the absolute last
    resort if the heal cascade exhausts (API returned [0,0]). Only honoured on
    AutohealExhausted — never short-circuits a fresh resolve (spec §3.4).
    """
    if tiers is None:
        tiers = _HEAL_TIERS
    # V2 handle_upload parity: for a truly selectorless upload, resolve the file
    # <input> via pure DOM first (no vision/coords) before the COORDINATE heal,
    # which can't anchor without a visible "choose file" element. Gated to the
    # selectorless case with no shadow-context constraint (search_root) and only
    # when healing is enabled (DOM discovery is the parity replacement for the
    # heal). A probe miss or a send_keys failure falls through to _run_action.
    # Ordering note: DOM-first preempts the COORDINATE heal whenever ANY file
    # input exists; on a multi-input page it takes the FIRST input (chosen
    # "pick first" V2 Strategy-3 parity), which can differ from the input the
    # coordinate heal would have anchored on via the visible trigger.
    if not selector and search_root is None and autoheal:
        element = _resolve_file_input_dom(driver)
        if element is not None:
            try:
                element.send_keys(_path_value(
                    {'file_path': file_path, 'file_paths': file_paths}))
                return None
            except Exception:  # noqa: BLE001 — fall back to the heal path
                _log.info(
                    "    [upload] DOM-first send_keys failed; falling back to heal",
                    exc_info=True,
                )
    return _run_action(
        driver, _SET_INPUT_FILES_SPEC, selector,
        description=description, tiers=tiers, autoheal=autoheal,
        max_attempts=max_attempts, retry_delay=retry_delay,
        search_root=search_root,
        fallback_coordinates=fallback_coordinates,
        file_path=file_path, file_paths=file_paths,
    )
