"""Tests for testmu_selenium._helpers._coordinate_resolver (spec §3.1, §4)."""
from unittest.mock import MagicMock

import pytest

from testmu_selenium._helpers._coordinate_resolver import (
    RESOLVER_JS,
    ResolvedTarget,
    resolve_coordinate,
)
from testmu_selenium._helpers._coordinate_resolver import (
    READ_RESOLVER_JS,
    resolve_coordinate_read,
)


def _driver(script_result=None, side_effect=None):
    d = MagicMock()
    if side_effect is not None:
        d.execute_script.side_effect = side_effect
    else:
        d.execute_script.return_value = script_result
    return d


class TestResolveCoordinate:
    def test_derived_happy_path(self):
        raw = {"xpath": "//*[@id='cart']", "tag": "button", "id": "cart", "text": "Add to cart"}
        d = _driver(script_result=raw)
        result = resolve_coordinate(d, 412, 803)
        assert isinstance(result, ResolvedTarget)
        assert result.xpath == "//*[@id='cart']"
        assert result.meta == {"tag": "button", "id": "cart", "text": "Add to cart"}

    def test_js_null_returns_none(self):
        assert resolve_coordinate(_driver(script_result=None), 1, 2) is None

    def test_js_exception_returns_none(self):
        d = _driver(side_effect=Exception("boom"))
        assert resolve_coordinate(d, 1, 2) is None

    def test_missing_xpath_key_returns_none(self):
        assert resolve_coordinate(_driver(script_result={"tag": "div"}), 1, 2) is None

    def test_empty_xpath_returns_none(self):
        assert resolve_coordinate(_driver(script_result={"xpath": ""}), 1, 2) is None

    def test_non_dict_result_returns_none(self):
        assert resolve_coordinate(_driver(script_result="//*[@id='x']"), 1, 2) is None

    def test_coordinates_passed_as_ints(self):
        d = _driver(script_result=None)
        resolve_coordinate(d, 12.7, 34.2)
        args = d.execute_script.call_args[0]
        assert args[1] == 12 and args[2] == 34
        assert isinstance(args[1], int) and isinstance(args[2], int)

    def test_meta_missing_fields_default_to_empty(self):
        result = resolve_coordinate(_driver(script_result={"xpath": "//*[@id='x']"}), 1, 2)
        assert result is not None
        assert result.meta == {"tag": "", "id": "", "text": ""}

    def test_wrapped_js_embeds_canonical_body(self):
        d = _driver(script_result=None)
        resolve_coordinate(d, 1, 2)
        sent = d.execute_script.call_args[0][0]
        assert RESOLVER_JS in sent
        assert sent.startswith("return (function(x, y) {")
        assert sent.endswith("})(arguments[0], arguments[1]);")


class TestCanonicalJs:
    def test_no_throw_contract_markers(self):
        # The body must open with try and close by returning null on error.
        assert RESOLVER_JS.lstrip().startswith("try {")
        assert "catch (e) {" in RESOLVER_JS
        assert "elementFromPoint" in RESOLVER_JS
        assert "XPathResult.ORDERED_NODE_SNAPSHOT_TYPE" in RESOLVER_JS


# ---------------------------------------------------------------------------
# Task 4 — READ_RESOLVER_JS + resolve_coordinate_read
# ---------------------------------------------------------------------------

class TestResolveCoordinateRead:
    def test_derived_happy_path(self):
        raw = {"xpath": "//div[2]", "tag": "div", "id": "", "text": "warn"}
        assert resolve_coordinate_read(_driver(script_result=raw), 10, 20).xpath == "//div[2]"

    def test_js_null_returns_none(self):
        assert resolve_coordinate_read(_driver(script_result=None), 1, 2) is None

    def test_js_exception_returns_none(self):
        assert resolve_coordinate_read(_driver(side_effect=Exception("x")), 1, 2) is None

    def test_coords_passed_as_ints(self):
        d = _driver(script_result=None)
        resolve_coordinate_read(d, 12.7, 34.2)
        a = d.execute_script.call_args[0]
        assert a[1] == 12 and a[2] == 34

    def test_wrapped_read_js_embeds_canonical_read_body(self):
        d = _driver(script_result=None)
        resolve_coordinate_read(d, 1, 2)
        sent = d.execute_script.call_args[0][0]
        assert READ_RESOLVER_JS in sent
        assert sent.startswith("return (function(x, y) {")


class TestReadResolverJsShape:
    def test_keeps_shadow_pierce_and_bails(self):
        assert "el.shadowRoot.elementFromPoint(x, y)" in READ_RESOLVER_JS
        assert "hitTag === 'iframe'" in READ_RESOLVER_JS
        assert "hitTag === 'canvas'" in READ_RESOLVER_JS
        assert "hitTag === 'img'" in READ_RESOLVER_JS
        assert "XPathResult.ORDERED_NODE_SNAPSHOT_TYPE" in READ_RESOLVER_JS

    def test_omits_interactable_up_walk(self):
        # THE key difference vs RESOLVER_JS: no climb to interactable ancestors.
        assert "INTERACTABLE" not in READ_RESOLVER_JS
        # parentElement walk is only present AFTER "var parts" (the positional
        # xpath builder), not before — no up-walk for interactable ancestor.
        assert "parentElement" not in READ_RESOLVER_JS.split("var parts")[0]
