"""Cross-tree parity: RESOLVER_JS must be byte-identical in both bindings."""
import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).parents[2]  # repo root


def _load_resolver(rel_path: str):
    path = ROOT / rel_path
    spec = importlib.util.spec_from_file_location("_resolver", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_resolver_js_parity():
    sel = _load_resolver("selenium-python/testmu_selenium/_helpers/_coordinate_resolver.py")
    pw = _load_resolver("playwright-python/testmu/_helpers/_coordinate_resolver.py")
    assert sel.RESOLVER_JS == pw.RESOLVER_JS, (
        "RESOLVER_JS diverged between selenium-python and playwright-python trees. "
        "Keep them in sync."
    )


def test_java_resource_matches_canonical_js():
    sel = _load_resolver("selenium-python/testmu_selenium/_helpers/_coordinate_resolver.py")
    java = (ROOT / "selenium-java" / "src" / "main" / "resources" / "testmu" / "coordinate_resolver.js").read_text(encoding="utf-8")
    assert sel.RESOLVER_JS == java, (
        "coordinate_resolver.js (Java resource) diverged from selenium-python RESOLVER_JS. "
        "Edit ALL trees together (spec §4.3)."
    )


def test_resolver_pierces_shadow_dom():
    """document.elementFromPoint stops at the shadow host (light DOM), so the
    resolver must descend through shadowRoot.elementFromPoint to reach the real
    target. A target inside a shadow root then trips the getRootNode()!==document
    bail → coordinate fallback, instead of deriving a (verified-but-wrong) xpath
    for the host container."""
    sel = _load_resolver("selenium-python/testmu_selenium/_helpers/_coordinate_resolver.py")
    js = sel.RESOLVER_JS
    assert "el.shadowRoot" in js, "resolver must pierce shadow roots"
    assert "el.shadowRoot.elementFromPoint(x, y)" in js, "resolver must descend via shadowRoot.elementFromPoint"


def test_resolver_bails_on_canvas_and_video():
    """A point whose topmost element is <canvas>/<video> must yield no derived
    xpath (return null), so the heal falls back to the resolved coordinate
    instead of clicking the canvas element's center."""
    sel = _load_resolver("selenium-python/testmu_selenium/_helpers/_coordinate_resolver.py")
    js = sel.RESOLVER_JS
    assert "hitTag === 'canvas'" in js, "resolver must bail on canvas hit"
    assert "hitTag === 'video'" in js, "resolver must bail on video hit"
