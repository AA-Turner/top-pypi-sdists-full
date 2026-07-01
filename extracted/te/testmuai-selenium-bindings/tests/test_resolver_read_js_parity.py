"""Parity guard for READ_RESOLVER_JS.

Pins the structural relationship of READ_RESOLVER_JS to RESOLVER_JS within
selenium-python: same shadow-pierce, same iframe/canvas/video bail, same xpath
candidate ladder, MINUS the INTERACTABLE up-walk.

Cross-tree byte-identity checks against playwright-python and selenium-java
are deferred behind skipif until those twins land (matching the pattern from
test_resolver_js_parity.py). Once the twins exist and the skipif guards
activate, this file enforces cross-binding byte-identity for the read snippet.

Note: READ_RESOLVER_JS is currently selenium-python-local only (no active
cross-tree pin in this PR). This is a known, documented drift risk until the
PW/Java twins land (see Release Step 5 in the TDD plan).
"""
import importlib.util
import pathlib

import pytest

ROOT = pathlib.Path(__file__).parents[2]  # repo root

SEL_RESOLVER = ROOT / "selenium-python" / "testmu_selenium" / "_helpers" / "_coordinate_resolver.py"
PW_RESOLVER = ROOT / "playwright-python" / "testmu" / "_helpers" / "_coordinate_resolver.py"
JAVA_READ_RESOURCE = ROOT / "selenium-java" / "src" / "main" / "resources" / "testmu" / "coordinate_resolver_read.js"


def _load_resolver(path):
    spec = importlib.util.spec_from_file_location("_resolver", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# Structural relationship to RESOLVER_JS (within selenium-python)
# ---------------------------------------------------------------------------

class TestReadResolverJsVsResolverJs:
    """READ_RESOLVER_JS is RESOLVER_JS minus the interactable up-walk."""

    def test_read_resolver_js_exists(self):
        sel = _load_resolver(SEL_RESOLVER)
        assert hasattr(sel, "READ_RESOLVER_JS")
        assert isinstance(sel.READ_RESOLVER_JS, str) and len(sel.READ_RESOLVER_JS) > 100

    def test_read_resolver_has_shadow_pierce(self):
        sel = _load_resolver(SEL_RESOLVER)
        assert "el.shadowRoot.elementFromPoint(x, y)" in sel.READ_RESOLVER_JS

    def test_read_resolver_has_iframe_canvas_bail(self):
        sel = _load_resolver(SEL_RESOLVER)
        assert "hitTag === 'iframe'" in sel.READ_RESOLVER_JS
        assert "hitTag === 'canvas'" in sel.READ_RESOLVER_JS
        assert "hitTag === 'video'" in sel.READ_RESOLVER_JS
        # img bails to server fallback: an img-element's pixel content is
        # opaque to DOM text/attribute reads, matching the V2 source deferral.
        assert "hitTag === 'img'" in sel.READ_RESOLVER_JS

    def test_read_resolver_has_xpath_candidate_ladder(self):
        sel = _load_resolver(SEL_RESOLVER)
        js = sel.READ_RESOLVER_JS
        assert "XPathResult.ORDERED_NODE_SNAPSHOT_TYPE" in js
        assert "data-testid" in js
        assert "xpathLiteral" in js

    def test_read_resolver_omits_interactable_up_walk(self):
        """THE key difference: no INTERACTABLE selector, no up-walk before var parts."""
        sel = _load_resolver(SEL_RESOLVER)
        js = sel.READ_RESOLVER_JS
        assert "INTERACTABLE" not in js
        # parentElement appears only inside the positional xpath builder
        # (after "var parts"), never in an up-walk for interactable ancestors.
        assert "parentElement" not in js.split("var parts")[0]

    def test_resolver_js_still_has_interactable_up_walk(self):
        """RESOLVER_JS must be untouched: verify it still has the up-walk."""
        sel = _load_resolver(SEL_RESOLVER)
        assert "INTERACTABLE" in sel.RESOLVER_JS

    def test_read_resolver_no_throw_contract(self):
        """Body must open with try and close by returning null on error."""
        sel = _load_resolver(SEL_RESOLVER)
        js = sel.READ_RESOLVER_JS
        assert js.lstrip().startswith("try {")
        assert "catch (e) {" in js


# ---------------------------------------------------------------------------
# Cross-tree byte-identity (skipif-deferred until PW/Java twins land)
# ---------------------------------------------------------------------------

def _pw_has_read_resolver_js() -> bool:
    """True only when the PW file exists AND contains READ_RESOLVER_JS."""
    return PW_RESOLVER.exists() and "READ_RESOLVER_JS" in PW_RESOLVER.read_text(encoding="utf-8")


@pytest.mark.skipif(
    not _pw_has_read_resolver_js(),
    reason="playwright-python READ_RESOLVER_JS not yet present — "
           "activate once the PW twin lands (Release Step 5)",
)
def test_read_resolver_js_parity_pw():
    sel = _load_resolver(SEL_RESOLVER)
    pw = _load_resolver(PW_RESOLVER)
    assert sel.READ_RESOLVER_JS == pw.READ_RESOLVER_JS, (
        "READ_RESOLVER_JS diverged between selenium-python and playwright-python. "
        "Keep them in sync."
    )


@pytest.mark.skipif(
    not JAVA_READ_RESOURCE.exists(),
    reason="selenium-java coordinate_resolver_read.js not yet present — "
           "activate once the Java twin lands (Release Step 5)",
)
def test_read_resolver_js_parity_java():
    sel = _load_resolver(SEL_RESOLVER)
    java = JAVA_READ_RESOURCE.read_text(encoding="utf-8")
    assert sel.READ_RESOLVER_JS == java, (
        "coordinate_resolver_read.js (Java resource) diverged from selenium-python "
        "READ_RESOLVER_JS. Edit ALL trees together (spec §4.3)."
    )
