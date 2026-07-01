"""Coordinate → element → verified-XPath derivation (design spec §3.1, §4).

Owns the CANONICAL resolver JS. The playwright-python twin and the
selenium-java resource must stay byte-identical to RESOLVER_JS — see the
parity test in selenium-python/tests/test_resolver_js_parity.py (created in
a later task).

Import-light on purpose: stdlib only. The parity test loads this file
standalone (importlib spec_from_file_location), bypassing the package.
"""
import logging
from dataclasses import dataclass

_log = logging.getLogger(__name__)

# === CANONICAL_RESOLVER_JS_START === (edit ALL trees together; spec §4.3)
RESOLVER_JS = """\
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
  if (hitTag === 'iframe' || hitTag === 'frame' || hitTag === 'canvas' || hitTag === 'video') { return null; }

  var INTERACTABLE = 'a, button, input, select, textarea, summary, label, [onclick], [contenteditable], [tabindex]:not([tabindex="-1"]), [role="button"], [role="link"], [role="checkbox"], [role="radio"], [role="menuitem"], [role="tab"], [role="option"], [role="switch"], [role="combobox"], [role="textbox"]';
  if (!(el.matches && el.matches(INTERACTABLE))) {
    var cur = el;
    var hops = 0;
    while (cur && cur !== document.documentElement && hops < 6) {
      cur = cur.parentElement;
      hops += 1;
      if (cur && cur.matches && cur.matches(INTERACTABLE)) { el = cur; break; }
    }
  }

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
    while (sib) {
      if (sib.tagName === node.tagName) { idx += 1; }
      sib = sib.previousElementSibling;
    }
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
# === CANONICAL_RESOLVER_JS_END ===

_WRAPPED_JS = "return (function(x, y) {" + RESOLVER_JS + "})(arguments[0], arguments[1]);"


@dataclass(frozen=True)
class ResolvedTarget:
    """A self-verified, document-rooted XPath for the element under a point."""
    xpath: str
    meta: dict  # {tag, id, text} — logging/telemetry only


def resolve_coordinate(driver, x, y) -> "ResolvedTarget | None":
    """Resolve viewport-CSS (x, y) to a verified XPath, or None.

    None ALWAYS means "use the coordinate fallback" (shadow-DOM hit, iframe
    hit, no node, verification failure, or any JS error). This function never
    raises — a derivation failure must never break a heal that would have
    succeeded via coord_runner (spec §3.1).
    """
    try:
        raw = driver.execute_script(_WRAPPED_JS, int(x), int(y))
    except Exception as exc:  # noqa: BLE001 — no-throw contract
        _log.info("    [resolver] derived_xpath=None reason=js-error: %s", exc)
        return None
    if not isinstance(raw, dict):
        _log.info("    [resolver] derived_xpath=None reason=no-node-or-bail")
        return None
    xpath = raw.get("xpath")
    if not isinstance(xpath, str) or not xpath:
        _log.info("    [resolver] derived_xpath=None reason=verify-failed")
        return None
    meta = {k: raw.get(k, "") for k in ("tag", "id", "text")}
    _log.info("    [resolver] derived_xpath=%s meta=%s", xpath, meta)
    return ResolvedTarget(xpath=xpath, meta=meta)


# === CANONICAL_READ_RESOLVER_JS_START === (RESOLVER_JS minus the interactable
# up-walk; for textual_query READS of non-interactable nodes. Keep in sync with
# RESOLVER_JS except for the omitted up-walk + optional text refinement.)
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

_WRAPPED_READ_JS = "return (function(x, y) {" + READ_RESOLVER_JS + "})(arguments[0], arguments[1]);"


def resolve_coordinate_read(driver, x, y) -> "ResolvedTarget | None":
    """Read-tuned twin of resolve_coordinate: identical contract (verified,
    document-rooted XPath or None; never raises) but does NOT climb to an
    interactable ancestor, so the derived xpath is the EXACT direct hit — correct
    for non-interactable nodes and non-inherited CSS. None → server fallback.
    """
    try:
        raw = driver.execute_script(_WRAPPED_READ_JS, int(x), int(y))
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
    return ResolvedTarget(xpath=xpath, meta=meta)
