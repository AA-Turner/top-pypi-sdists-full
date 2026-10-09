"""Read-tuned coordinate → element → verified-XPath (textual_query read path).

Playwright-python read twin of selenium-python's READ_RESOLVER_JS /
resolve_coordinate_read. Byte-identical to the selenium-python canonical constant
READ_RESOLVER_JS — parity enforced by tests/test_resolver_read_js_parity.py.

Key difference from _coordinate_resolver.py / RESOLVER_JS:
  The interactable ancestor up-walk (INTERACTABLE selector + 6-hop parentElement
  loop) is OMITTED. ``el`` stays the exact elementFromPoint hit, so non-inherited
  CSS properties (background-color) are read from the correct box, not a climbed
  ``a``/``button``/``[role]`` ancestor.

All other behaviours are identical: open-shadow pierce, cross-document root bail,
iframe/frame/canvas/video/img bail, xpath candidate ladder, no-throw contract.

Import-light on purpose: stdlib only. The parity test loads this file standalone
(importlib spec_from_file_location), bypassing the package.
"""
import logging
from dataclasses import dataclass

_log = logging.getLogger(__name__)

# === CANONICAL_READ_RESOLVER_JS_START === (edit ALL trees together; spec §4.3)
READ_RESOLVER_JS = """\
try {
  var el = document.elementFromPoint(x, y);
  if (!el) { return null; }
  while (el.shadowRoot) {
    var deeper = el.shadowRoot.elementFromPoint(x, y);
    if (!deeper || deeper === el) { break; }
    el = deeper;
  }
  if (el.getRootNode && el.getRootNode() !== document) { return null; }
  var hitTag = el.tagName ? el.tagName.toLowerCase() : '';
  if (hitTag === 'iframe' || hitTag === 'frame' || hitTag === 'canvas' || hitTag === 'video' || hitTag === 'img') { return null; }

  // *** NO interactable up-walk here (the ONLY structural difference from
  // RESOLVER_JS): the read must stay on the exact direct hit so non-inherited
  // CSS (background-color) is read off the correct box. ***

  function xpathLiteral(v) {
    if (v.indexOf("'") === -1) { return "'" + v + "'"; }
    if (v.indexOf('"') === -1) { return '"' + v + '"'; }
    return "concat('" + v.split("'").join("', \\"'\\", '") + "')";
  }
  function verifies(xp) {
    try {
      var r = document.evaluate(xp, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
      return r.snapshotLength === 1 && r.snapshotItem(0) === el;
    } catch (e) { return false; }
  }
  var tag = el.tagName.toLowerCase();
  var candidates = [];
  if (el.id) { candidates.push('//*[@id=' + xpathLiteral(el.id) + ']'); }
  var ATTRS = ['data-testid', 'data-test', 'data-qa', 'name', 'aria-label', 'placeholder', 'title'];
  for (var i = 0; i < ATTRS.length; i++) {
    var av = el.getAttribute(ATTRS[i]);
    if (av) { candidates.push('//' + tag + '[@' + ATTRS[i] + '=' + xpathLiteral(av) + ']'); break; }
  }
  var text = (el.textContent || '').replace(/\\s+/g, ' ').trim();
  if (text && text.length <= 64) {
    candidates.push('//' + tag + '[normalize-space(.)=' + xpathLiteral(text) + ']');
  }
  var parts = [];
  var node = el;
  while (node && node.nodeType === 1) {
    var name = node.tagName.toLowerCase();
    var idx = 1;
    var sib = node.previousElementSibling;
    while (sib) { if (sib.tagName === node.tagName) { idx += 1; } sib = sib.previousElementSibling; }
    parts.unshift(name + '[' + idx + ']');
    node = node.parentElement;
  }
  candidates.push('/' + parts.join('/'));
  for (var c = 0; c < candidates.length; c++) {
    if (verifies(candidates[c])) {
      return { xpath: candidates[c], tag: tag, id: el.id || '', text: text.slice(0, 80) };
    }
  }
  return null;
} catch (e) {
  return null;
}
"""
# === CANONICAL_READ_RESOLVER_JS_END ===

# Playwright arrow-function form (mirrors the _WRAPPED_JS pattern in
# _coordinate_resolver.py — note the different wrapping vs selenium's
# IIFE form).
_WRAPPED_READ_JS = "([x, y]) => { " + READ_RESOLVER_JS + " }"


@dataclass(frozen=True)
class ResolvedRead:
    """A self-verified, document-rooted XPath for the element under a point (read path)."""
    xpath: str
    meta: dict  # {tag, id, text} — logging/telemetry only


async def resolve_coordinate_read(page, x, y) -> "ResolvedRead | None":
    """Resolve viewport-CSS (x, y) to a verified XPath for READING, or None.

    Identical no-throw contract to resolve_coordinate but uses READ_RESOLVER_JS
    (no interactable up-walk), so the derived xpath is the EXACT direct hit —
    correct for non-interactable nodes and non-inherited CSS (background-color).

    None ALWAYS means "use the server fallback" (shadow-DOM hit, iframe hit,
    canvas/video/img hit, no node, verification failure, or any JS error).

    Args:
        page: Playwright page object (live connection).
        x: Viewport-CSS x coordinate.
        y: Viewport-CSS y coordinate.

    Returns:
        ResolvedRead with a verified xpath, or None.
    """
    try:
        raw = await page.evaluate(_WRAPPED_READ_JS, [int(x), int(y)])
    except Exception as exc:  # noqa: BLE001 — no-throw contract
        _log.info("    [read-resolver] derived_xpath=None reason=js-error: %s", exc)
        return None
    if not isinstance(raw, dict):
        _log.info("    [read-resolver] derived_xpath=None reason=no-node-or-bail")
        return None
    xpath = raw.get("xpath")
    if not isinstance(xpath, str) or not xpath:
        _log.info("    [read-resolver] derived_xpath=None reason=verify-failed")
        return None
    meta = {k: raw.get(k, "") for k in ("tag", "id", "text")}
    _log.info("    [read-resolver] derived_xpath=%s meta=%s", xpath, meta)
    return ResolvedRead(xpath=xpath, meta=meta)
