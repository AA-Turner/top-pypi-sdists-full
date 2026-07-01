"""Test _heal_cascade — V3 kwarg-based dispatcher over Heal class.

Strategy: patch the Heal tier methods directly to isolate cascade
dispatch/fall-through/exhaustion semantics from per-tier HTTP and DOM
internals (those are covered by test_heal_list_xpaths.py etc.).
"""
import json
import pytest
import httpx
from pathlib import Path
from unittest.mock import MagicMock, patch
from selenium.common.exceptions import StaleElementReferenceException

from testmu_selenium._heal import Heal
from testmu_selenium._heal_cascade import _heal_cascade, HealResult, _synthesize_current_action
from testmu_selenium._helpers._coordinate_resolver import ResolvedTarget
from testmu_selenium._errors import AutohealExhausted, HealTierMiss


FIXTURES = Path(__file__).parent / "fixtures" / "automind_responses"


@pytest.fixture
def mock_driver():
    d = MagicMock()
    d.session_id = "session-1"
    d.execute_script = MagicMock(return_value=None)
    d.capabilities = {"browserName": "chrome", "platformName": "linux"}
    d.page_source = "<html></html>"
    return d


@pytest.fixture
def selectors():
    return [
        {"selector": "[aria-label='Sign in']", "score": 85, "isXPath": False},
        {"selector": "//a[contains(@class,'gb_A')]", "score": 80, "isXPath": True},
    ]


def _load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text())


# ---------------------------------------------------------------------------
# HealResult shape
# ---------------------------------------------------------------------------

def test_heal_result_has_all_seven_fields():
    """Sanity check on HealResult dataclass shape — must include attempts_used
    and coordinates."""
    r = HealResult(
        selectors=[{"selector": "x", "isXPath": False}],
        frame_info=None,
        selector_payload=None,
        tier_used="LIST_XPATHS",
        latency_ms=100,
        attempts_used=2,
        coordinates=(10, 20),
    )
    assert r.attempts_used == 2
    assert r.selectors[0]["selector"] == "x"
    assert r.tier_used == "LIST_XPATHS"
    assert r.latency_ms == 100
    assert r.frame_info is None
    assert r.selector_payload is None
    assert r.coordinates == (10, 20)


def test_heal_result_defaults():
    """Fields with defaults should not require explicit values."""
    r = HealResult(selectors=[])
    assert r.frame_info is None
    assert r.selector_payload is None
    assert r.tier_used == ""
    assert r.latency_ms == 0
    assert r.attempts_used == 0


# ---------------------------------------------------------------------------
# driver=None guard
# ---------------------------------------------------------------------------

def test_driver_none_raises():
    with pytest.raises(ValueError, match="driver argument is required"):
        _heal_cascade(
            description="x",
            current_selector=[],
            current_frame_info=None,
            tiers=["LIST_XPATHS"],
            exception=StaleElementReferenceException(),
            driver=None,
        )


# ---------------------------------------------------------------------------
# LIST_XPATHS tier hit
# ---------------------------------------------------------------------------

def test_list_xpaths_tier_returns_heal_result(mock_driver, selectors):
    fixture = _load_fixture("list_xpaths_success.json")
    fake_response = httpx.Response(200, json=fixture)

    with patch.object(Heal, "list_xpaths", return_value=fake_response):
        result = _heal_cascade(
            description="Click Sign in",
            current_selector=selectors,
            current_frame_info=None,
            tiers=["LIST_XPATHS", "VISION_QUERY"],
            exception=StaleElementReferenceException(),
            driver=mock_driver,
        )

    assert isinstance(result, HealResult)
    assert result.tier_used == "LIST_XPATHS"
    assert len(result.selectors) == 2  # fixture has 2 xpaths
    assert result.selectors[0]["isXPath"] is True
    assert result.latency_ms >= 0


def test_list_xpaths_hit_sets_frame_info(mock_driver, selectors):
    """frameInformation from fixture is forwarded to HealResult.frame_info."""
    fixture = {"xpaths": ["//button"], "frameInformation": [{"iframe": "//iframe[@id='f']"}]}
    fake_response = httpx.Response(200, json=fixture)

    with patch.object(Heal, "list_xpaths", return_value=fake_response):
        result = _heal_cascade(
            description="Click",
            current_selector=selectors,
            current_frame_info=None,
            tiers=["LIST_XPATHS"],
            exception=StaleElementReferenceException(),
            driver=mock_driver,
        )

    assert result.frame_info == [{"iframe": "//iframe[@id='f']"}]


# ---------------------------------------------------------------------------
# Fall-through: LIST_XPATHS miss → VISION_QUERY hit
# (TEXTUAL_QUERY is not a relocate tier — see test_textual_query_no_longer_a_relocate_tier)
# ---------------------------------------------------------------------------

def test_falls_through_list_miss_to_vision(mock_driver, selectors):
    vision_success_fixture = _load_fixture("vision_query_success.json")  # {"value": "//div[...]"}
    vision_success_resp = httpx.Response(200, json=vision_success_fixture)

    with patch.object(Heal, "list_xpaths", return_value=httpx.Response(200, json={"xpaths": []})), \
         patch.object(Heal, "vision_query_v2", return_value=vision_success_resp):
        result = _heal_cascade(
            description="Click",
            current_selector=selectors,
            current_frame_info=None,
            tiers=["LIST_XPATHS", "VISION_QUERY"],
            exception=StaleElementReferenceException(),
            driver=mock_driver,
        )

    assert result.tier_used == "VISION_QUERY"
    assert result.selectors[0]["selector"] == "//div[@role='button']"


def test_vision_boolean_answer_payload_is_a_miss(mock_driver, selectors):
    """/v1/heal/vision can return a presence ANSWER shape
    {"vision_query": true, "tag_id": "", ...} with no value/xpath. The boolean
    must NOT be treated as a selector — feeding it to findElement crashes Chrome
    (InvalidArgumentException: 'value' must be a string). The tier must miss so
    the cascade falls through; with only LIST_XPATHS+VISION_QUERY it exhausts.
    (Pre-RC3a: `vq = ... or payload.get("vision_query")` grabbed True and
    returned a HealResult — reverting turns this RED.)"""
    answer_payload = {"vision_query": True, "tag_id": "", "target_element_name": ""}
    with patch.object(Heal, "list_xpaths", return_value=httpx.Response(200, json={"xpaths": []})), \
         patch.object(Heal, "vision_query_v2", return_value=httpx.Response(200, json=answer_payload)):
        with pytest.raises(AutohealExhausted):
            _heal_cascade(
                description="choose file",
                current_selector=selectors,
                current_frame_info=None,
                tiers=["LIST_XPATHS", "VISION_QUERY"],
                exception=StaleElementReferenceException(),
                driver=mock_driver,
            )


# ---------------------------------------------------------------------------
# DESKTOP_LOCATE tier — hit and miss
# ---------------------------------------------------------------------------

def test_desktop_locate_tier_returns_heal_result_with_coordinates(mock_driver, selectors):
    """DESKTOP_LOCATE hit: desktop_locate() returns (css_x, css_y) → HealResult.coordinates set.
    When the resolver returns None, selectors is [] (coordinates-only path)."""
    with patch.object(Heal, "desktop_locate", return_value=(640, 400)), \
         patch("testmu_selenium._heal_cascade.resolve_coordinate", return_value=None):
        result = _heal_cascade(
            description="Click submit button",
            current_selector=selectors,
            current_frame_info=None,
            tiers=["DESKTOP_LOCATE"],
            exception=StaleElementReferenceException(),
            driver=mock_driver,
        )

    assert isinstance(result, HealResult)
    assert result.tier_used == "DESKTOP_LOCATE"
    assert result.coordinates == (640, 400)
    assert result.selectors == []  # resolver returned None → coordinates-only shape
    assert result.latency_ms >= 0


def test_desktop_locate_tier_miss_raises_autoheal_exhausted(mock_driver, selectors):
    """DESKTOP_LOCATE miss (HealTierMiss from desktop_locate) → falls through → exhausted."""
    with patch.object(
        Heal, "desktop_locate",
        side_effect=HealTierMiss("DESKTOP_LOCATE", "element not found ([0,0])"),
    ):
        with pytest.raises(AutohealExhausted) as exc_info:
            _heal_cascade(
                description="Click submit button",
                current_selector=selectors,
                current_frame_info=None,
                tiers=["DESKTOP_LOCATE"],
                exception=StaleElementReferenceException(),
                driver=mock_driver,
            )

    assert exc_info.value.last_miss is not None


def test_falls_through_vision_miss_to_desktop_locate(mock_driver, selectors):
    """VISION_QUERY miss → DESKTOP_LOCATE hit: cascade returns coordinates (resolver=None path)."""
    with patch.object(Heal, "vision_query_v2", return_value=httpx.Response(200, json={"error": "no match"})), \
         patch.object(Heal, "desktop_locate", return_value=(500, 300)), \
         patch("testmu_selenium._heal_cascade.resolve_coordinate", return_value=None):
        result = _heal_cascade(
            description="Click",
            current_selector=selectors,
            current_frame_info=None,
            tiers=["VISION_QUERY", "DESKTOP_LOCATE"],
            exception=StaleElementReferenceException(),
            driver=mock_driver,
        )

    assert result.tier_used == "DESKTOP_LOCATE"
    assert result.coordinates == (500, 300)
    assert result.selectors == []


def test_default_order_runs_desktop_locate_first(mock_driver, selectors):
    """With the default tier order, DESKTOP_LOCATE must be the FIRST and only tier.
    Reverting _DEFAULT_HEAL_TIERS to a multi-tier or non-DESKTOP_LOCATE-first
    order turns this RED."""
    from testmu_selenium._action_engine import _DEFAULT_HEAL_TIERS

    call_order: list[str] = []

    def _track_lx(self):
        call_order.append("LIST_XPATHS")
        return httpx.Response(200, json={"xpaths": ["//div[@id='wrong']"]})

    def _track_vq(self):
        call_order.append("VISION_QUERY")
        return httpx.Response(200, json={"value": "//div[@id='vision-wrong']"})

    def _track_desktop(self):
        call_order.append("DESKTOP_LOCATE")
        return (709, 468)

    with patch.object(Heal, "list_xpaths", _track_lx), \
         patch.object(Heal, "vision_query_v2", _track_vq), \
         patch.object(Heal, "desktop_locate", _track_desktop), \
         patch("testmu_selenium._heal_cascade.resolve_coordinate", return_value=None):
        result = _heal_cascade(
            description="Canvas UI Demo input field",
            current_selector=[],  # empty selector — vision/canvas op shape
            current_frame_info=None,
            tiers=list(_DEFAULT_HEAL_TIERS),
            exception=StaleElementReferenceException(),
            driver=mock_driver,
        )

    # DESKTOP_LOCATE must have been the first (and only) tier called when it hits;
    # the cascade short-circuits on first success.
    assert call_order == ["DESKTOP_LOCATE"], (
        f"Expected DESKTOP_LOCATE to run first and short-circuit, got call order "
        f"{call_order}. If LIST_XPATHS or VISION_QUERY ran first, _DEFAULT_HEAL_TIERS "
        f"has been reverted — see the docstring for the failure mode that motivated "
        f"DESKTOP_LOCATE-only default."
    )
    assert result.tier_used == "DESKTOP_LOCATE"
    assert result.coordinates == (709, 468)


# ---------------------------------------------------------------------------
# All tiers miss → AutohealExhausted
# ---------------------------------------------------------------------------

def test_all_tiers_miss_raises_autoheal_exhausted(mock_driver, selectors):
    original_exc = StaleElementReferenceException("stale")

    with patch.object(Heal, "list_xpaths", return_value=httpx.Response(200, json={"xpaths": []})), \
         patch.object(Heal, "vision_query_v2", return_value=httpx.Response(200, json={"error": "no match"})), \
         patch.object(
             Heal, "desktop_locate",
             side_effect=HealTierMiss("DESKTOP_LOCATE", "element not found"),
         ):
        with pytest.raises(AutohealExhausted) as exc_info:
            _heal_cascade(
                description="Click Sign in",
                current_selector=selectors,
                current_frame_info=None,
                tiers=["LIST_XPATHS", "VISION_QUERY", "DESKTOP_LOCATE"],
                exception=original_exc,
                driver=mock_driver,
            )

    assert exc_info.value.original is original_exc
    assert exc_info.value.last_miss is not None


# ---------------------------------------------------------------------------
# Unknown tier treated as miss → AutohealExhausted
# ---------------------------------------------------------------------------

def test_unknown_tier_treated_as_miss(mock_driver, selectors):
    """Unknown tier raises ValueError internally → caught as miss → continues.
    With only unknown tiers configured, all-miss path raises AutohealExhausted."""
    with pytest.raises(AutohealExhausted):
        _heal_cascade(
            description="x",
            current_selector=selectors,
            current_frame_info=None,
            tiers=["NOT_A_REAL_TIER"],
            exception=StaleElementReferenceException(),
            driver=mock_driver,
        )


# ---------------------------------------------------------------------------
# current_action synthesis
# ---------------------------------------------------------------------------

def test_synthesizes_current_action_when_not_provided(mock_driver, selectors):
    """When current_action is None, _synthesize_current_action builds one from kwargs."""
    fixture = _load_fixture("list_xpaths_success.json")

    with patch.object(Heal, "list_xpaths", return_value=httpx.Response(200, json=fixture)) as mock_lx, \
         patch("testmu_selenium._heal_cascade.Heal", wraps=Heal) as mock_heal_cls:
        _heal_cascade(
            description="Click Sign in button",
            current_selector=selectors,
            current_frame_info=None,
            tiers=["LIST_XPATHS"],
            exception=StaleElementReferenceException(),
            driver=mock_driver,
        )

    # Heal was constructed with a synthesized current_action
    call_args = mock_heal_cls.call_args
    synthesized = call_args[0][0]  # first positional arg
    assert synthesized["operation_intent"] == "Click Sign in button"
    assert synthesized["operation_type"] == "click"
    assert synthesized["version"] == "v3"


def test_synthesized_action_carries_operation_dict_queried_value():
    """The automind /v1/heal endpoints read the query from
    sub_instruction_obj.operation_dict.queried_value (same shape the
    vision_query / textual_query helpers send). A synthesized action that omits
    it makes the VISION_QUERY tier 500 with KeyError 'operation_dict' on the
    server (2026-05-23). Seed it so selectorless heal works.
    """
    action = _synthesize_current_action("choose file", [])
    op_dict = action["sub_instruction_obj"]["operation_dict"]
    assert op_dict["queried_value"] == "choose file"


def test_uses_provided_current_action(mock_driver, selectors):
    """When current_action is provided, it is passed through unchanged."""
    fixture = _load_fixture("list_xpaths_success.json")
    custom_action = {
        "operation_type": "input",
        "operation_intent": "Type email",
        "version": "v3",
        "use_query_v2": True,
    }

    with patch.object(Heal, "list_xpaths", return_value=httpx.Response(200, json=fixture)), \
         patch("testmu_selenium._heal_cascade.Heal", wraps=Heal) as mock_heal_cls:
        _heal_cascade(
            description="Type email",
            current_selector=selectors,
            current_frame_info=None,
            tiers=["LIST_XPATHS"],
            exception=StaleElementReferenceException(),
            driver=mock_driver,
            current_action=custom_action,
        )

    call_args = mock_heal_cls.call_args
    passed_action = call_args[0][0]
    assert passed_action["operation_type"] == "input"


# ---------------------------------------------------------------------------
# Tier-specific score values
# ---------------------------------------------------------------------------

def test_list_xpaths_selectors_have_score_50(mock_driver, selectors):
    fixture = _load_fixture("list_xpaths_success.json")
    with patch.object(Heal, "list_xpaths", return_value=httpx.Response(200, json=fixture)):
        result = _heal_cascade(
            description="x", current_selector=selectors, current_frame_info=None,
            tiers=["LIST_XPATHS"], exception=StaleElementReferenceException(), driver=mock_driver,
        )
    assert all(s["score"] == 50 for s in result.selectors)


def test_vision_query_selector_has_score_40(mock_driver, selectors):
    vision_success = _load_fixture("vision_query_success.json")
    with patch.object(Heal, "vision_query_v2", return_value=httpx.Response(200, json=vision_success)):
        result = _heal_cascade(
            description="x", current_selector=selectors, current_frame_info=None,
            tiers=["VISION_QUERY"], exception=StaleElementReferenceException(), driver=mock_driver,
        )
    assert result.selectors[0]["score"] == 40


def test_desktop_locate_tier_always_populates_coordinates(mock_driver, selectors):
    """DESKTOP_LOCATE always populates HealResult.coordinates on a hit.
    When the resolver derives an xpath, both coordinates AND selectors are set;
    when the resolver returns None, coordinates is set and selectors is [].
    Pre-2026-05-01 the old COORDINATE tier returned synthetic placeholder selectors;
    DESKTOP_LOCATE uses HealResult.coordinates as the primary dispatch path."""
    with patch.object(Heal, "desktop_locate", return_value=(640, 400)), \
         patch("testmu_selenium._heal_cascade.resolve_coordinate", return_value=None):
        result = _heal_cascade(
            description="x", current_selector=selectors, current_frame_info=None,
            tiers=["DESKTOP_LOCATE"], exception=StaleElementReferenceException(), driver=mock_driver,
        )
    assert result.tier_used == "DESKTOP_LOCATE"
    assert result.selectors == []  # resolver=None → coordinates-only shape
    assert result.coordinates is not None
    x, y = result.coordinates
    assert (x, y) == (640, 400)


# ---------------------------------------------------------------------------
# TEXTUAL_QUERY is not a relocate tier
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# _synthesize_current_action — op_type threading (RED until Edit D implemented)
# ---------------------------------------------------------------------------

def test_synthesize_current_action_default_op_type_is_click():
    """Without an explicit op_type, synthesized action must use 'click' for
    backward compatibility with all existing action specs."""
    action = _synthesize_current_action("click the button", [])
    assert action["operation_type"] == "click"


def test_synthesize_current_action_scroll_until_element_op_type():
    """When op_type='scroll_until_element' is passed, the synthesized action
    must carry that value so _heal.py gates full-page tagify correctly."""
    action = _synthesize_current_action("scroll to footer", [], op_type="scroll_until_element")
    assert action["operation_type"] == "scroll_until_element"


def test_desktop_locate_runtime_error_converts_to_autoheal_exhausted(mock_driver, selectors):
    """FIX 9 — cascade coverage for retry-exhaustion exceptions.

    A non-HealTierMiss exception from desktop_locate (e.g. TransientHTTPError
    bubbling after all internal retries) must be converted to a tier-miss by the
    cascade's generic except clause, then raise AutohealExhausted — not crash the
    test with an unhandled RuntimeError.

    Reverting the cascade's `except Exception → HealTierMiss` wrapper turns this
    RED (RuntimeError propagates uncaught instead of AutohealExhausted).
    """
    with patch.object(
        Heal, "desktop_locate",
        side_effect=RuntimeError("TransientHTTPError: 503 after retries"),
    ):
        with pytest.raises(AutohealExhausted) as exc_info:
            _heal_cascade(
                description="click submit",
                current_selector=selectors,
                current_frame_info=None,
                tiers=["DESKTOP_LOCATE"],
                exception=StaleElementReferenceException(),
                driver=mock_driver,
            )

    exc = exc_info.value
    assert isinstance(exc, AutohealExhausted)
    # last_miss is a HealTierMiss wrapping the RuntimeError message
    assert exc.last_miss is not None
    assert "TransientHTTPError" in str(exc.last_miss)


# ---------------------------------------------------------------------------
# DESKTOP_LOCATE + xpath derivation (Task 2: spec §3.2)
# ---------------------------------------------------------------------------

class TestDesktopLocateXpathDerivation:
    """DESKTOP_LOCATE tier integrates resolve_coordinate after a successful locate."""

    def test_derived_xpath_returned_with_coordinates(self, mock_driver, selectors):
        """When resolver derives an xpath, result carries BOTH selector and coordinates."""
        resolved = ResolvedTarget(xpath="//*[@id='x']", meta={"tag": "button", "id": "x", "text": ""})
        with patch.object(Heal, "desktop_locate", return_value=(120, 240)), \
             patch("testmu_selenium._heal_cascade.resolve_coordinate", return_value=resolved):
            result = _heal_cascade(
                description="click x",
                current_selector=selectors,
                current_frame_info=None,
                tiers=["DESKTOP_LOCATE"],
                exception=StaleElementReferenceException(),
                driver=mock_driver,
            )
        assert result.coordinates == (120, 240)
        assert result.selectors == [{"selector": "//*[@id='x']", "isXPath": True, "score": 45}]
        assert result.tier_used == "DESKTOP_LOCATE"

    def test_resolver_none_keeps_empty_selectors(self, mock_driver, selectors):
        """When resolver returns None, selectors is [] but coordinates is still set."""
        with patch.object(Heal, "desktop_locate", return_value=(120, 240)), \
             patch("testmu_selenium._heal_cascade.resolve_coordinate", return_value=None):
            result = _heal_cascade(
                description="click x",
                current_selector=selectors,
                current_frame_info=None,
                tiers=["DESKTOP_LOCATE"],
                exception=StaleElementReferenceException(),
                driver=mock_driver,
            )
        assert result.selectors == []
        assert result.coordinates == (120, 240)

    def test_api_miss_skips_resolver(self, mock_driver, selectors):
        """HealTierMiss from desktop_locate occurs BEFORE any resolver call."""
        mock_resolver = MagicMock()
        with patch.object(
            Heal, "desktop_locate",
            side_effect=HealTierMiss("DESKTOP_LOCATE", "element not found ([0,0])"),
        ), patch("testmu_selenium._heal_cascade.resolve_coordinate", mock_resolver):
            with pytest.raises(AutohealExhausted):
                _heal_cascade(
                    description="click x",
                    current_selector=selectors,
                    current_frame_info=None,
                    tiers=["DESKTOP_LOCATE"],
                    exception=StaleElementReferenceException(),
                    driver=mock_driver,
                )
        mock_resolver.assert_not_called()

    def test_resolver_receives_scaled_coords(self, mock_driver, selectors):
        """resolve_coordinate is called with (driver, css_x, css_y) from desktop_locate."""
        resolved = ResolvedTarget(xpath="//*[@id='x']", meta={"tag": "button", "id": "x", "text": ""})
        mock_resolver = MagicMock(return_value=resolved)
        with patch.object(Heal, "desktop_locate", return_value=(120, 240)), \
             patch("testmu_selenium._heal_cascade.resolve_coordinate", mock_resolver):
            _heal_cascade(
                description="click x",
                current_selector=selectors,
                current_frame_info=None,
                tiers=["DESKTOP_LOCATE"],
                exception=StaleElementReferenceException(),
                driver=mock_driver,
            )
        mock_resolver.assert_called_once_with(mock_driver, 120, 240)


# ---------------------------------------------------------------------------
# DESKTOP_LOCATE_FULL_PAGE tier — cascade dispatch (spec §9)
# ---------------------------------------------------------------------------

class TestDesktopLocateFullPage:
    """DESKTOP_LOCATE_FULL_PAGE tier: full-page locate, scroll-into-viewport, xpath derivation."""

    def test_happy_path_derives_xpath_and_scrolls(self, mock_driver, selectors):
        """Happy path: page=(600, 2400), viewport=1200x800, scroll_offsets=(0, 2000).

        Expected:
          - window.scrollTo called with (max(0, 600-600), max(0, 2400-400)) = (0, 2000)
          - resolver called with (driver, vx=600, vy=400)  [vx=600-0=600, vy=2400-2000=400]
          - HealResult: selectors=[{score=45}], coordinates=(600, 400),
            tier_used='DESKTOP_LOCATE_FULL_PAGE'
        """
        import time as _time_mod
        resolved = ResolvedTarget(
            xpath="//*[@id='checkout-btn']",
            meta={"tag": "button", "id": "checkout-btn", "text": ""},
        )
        # execute_script call order in cascade branch:
        #   1. "return [window.innerWidth, window.innerHeight]" → [1200, 800]
        #   2. "window.scrollTo(...)" → None
        #   3. "return [window.scrollX, window.scrollY]" → [0, 2000]
        mock_driver.execute_script.side_effect = [
            [1200, 800],
            None,
            [0, 2000],
        ]

        with patch.object(Heal, "desktop_locate_full_page", return_value=(600, 2400)), \
             patch("testmu_selenium._heal_cascade.resolve_coordinate", return_value=resolved) as mock_resolver, \
             patch("testmu_selenium._heal_cascade.time.sleep"):
            result = _heal_cascade(
                description="checkout button below fold",
                current_selector=selectors,
                current_frame_info=None,
                tiers=["DESKTOP_LOCATE_FULL_PAGE"],
                exception=StaleElementReferenceException(),
                driver=mock_driver,
            )

        assert result.tier_used == "DESKTOP_LOCATE_FULL_PAGE"
        assert result.coordinates == (600, 400)
        assert result.selectors == [
            {"selector": "//*[@id='checkout-btn']", "isXPath": True, "score": 45}
        ]
        assert result.latency_ms >= 0

        # Verify scrollTo was called with (0, 2000)
        scrollto_call = mock_driver.execute_script.call_args_list[1]
        assert "scrollTo" in scrollto_call.args[0]
        assert scrollto_call.args[1] == 0    # scroll-x target
        assert scrollto_call.args[2] == 2000  # scroll-y target

        # Verify resolver was called with viewport coords
        mock_resolver.assert_called_once_with(mock_driver, 600, 400)

    def test_resolver_none_returns_coordinates_only(self, mock_driver, selectors):
        """When resolver returns None, HealResult has coordinates but no selectors."""
        mock_driver.execute_script.side_effect = [
            [1200, 800],
            None,
            [0, 2000],
        ]

        with patch.object(Heal, "desktop_locate_full_page", return_value=(600, 2400)), \
             patch("testmu_selenium._heal_cascade.resolve_coordinate", return_value=None), \
             patch("testmu_selenium._heal_cascade.time.sleep"):
            result = _heal_cascade(
                description="checkout button below fold",
                current_selector=selectors,
                current_frame_info=None,
                tiers=["DESKTOP_LOCATE_FULL_PAGE"],
                exception=StaleElementReferenceException(),
                driver=mock_driver,
            )

        assert result.tier_used == "DESKTOP_LOCATE_FULL_PAGE"
        assert result.coordinates == (600, 400)
        assert result.selectors == []

    def test_heal_tier_miss_skips_scroll_and_resolver(self, mock_driver, selectors):
        """HealTierMiss from desktop_locate_full_page: no scroll, no resolver, AutohealExhausted."""
        mock_resolver = MagicMock()

        with patch.object(
            Heal, "desktop_locate_full_page",
            side_effect=HealTierMiss("DESKTOP_LOCATE_FULL_PAGE", "element not found ([0,0])"),
        ), patch("testmu_selenium._heal_cascade.resolve_coordinate", mock_resolver):
            with pytest.raises(AutohealExhausted):
                _heal_cascade(
                    description="below-fold target",
                    current_selector=selectors,
                    current_frame_info=None,
                    tiers=["DESKTOP_LOCATE_FULL_PAGE"],
                    exception=StaleElementReferenceException(),
                    driver=mock_driver,
                )

        # Neither scroll nor resolver called when the tier misses
        mock_driver.execute_script.assert_not_called()
        mock_resolver.assert_not_called()

    def test_falls_through_to_vision_query_on_miss(self, mock_driver, selectors):
        """DESKTOP_LOCATE_FULL_PAGE miss → VISION_QUERY hit: cascade continues."""
        vision_resp = httpx.Response(200, json={"value": "//div[@id='footer-btn']"})

        with patch.object(
            Heal, "desktop_locate_full_page",
            side_effect=HealTierMiss("DESKTOP_LOCATE_FULL_PAGE", "not found"),
        ), patch.object(Heal, "vision_query_v2", return_value=vision_resp):
            result = _heal_cascade(
                description="footer button",
                current_selector=selectors,
                current_frame_info=None,
                tiers=["DESKTOP_LOCATE_FULL_PAGE", "VISION_QUERY"],
                exception=StaleElementReferenceException(),
                driver=mock_driver,
            )

        assert result.tier_used == "VISION_QUERY"
        assert result.selectors[0]["selector"] == "//div[@id='footer-btn']"


# ---------------------------------------------------------------------------
# DESKTOP_LOCATE_FULL_PAGE_READ tier — Task 3
# ---------------------------------------------------------------------------

def test_full_page_read_tier_uses_read_resolver_and_returns_xpath_and_coords(mock_driver):
    """DESKTOP_LOCATE_FULL_PAGE_READ: uses resolve_coordinate_read (not the click
    resolver), returns selectors + coordinates."""
    from selenium.common.exceptions import NoSuchElementException
    mock_driver.execute_script.side_effect = [
        [1920, 1080],   # innerWidth/innerHeight
        None,           # scrollTo
        [0, 4000],      # scrollX/scrollY after scroll
    ]
    resolved = ResolvedTarget(xpath="//div[3]", meta={"tag": "div", "id": "", "text": ""})
    with patch("testmu_selenium._heal_cascade.Heal") as m_heal_cls, \
         patch("testmu_selenium._heal_cascade.resolve_coordinate_read", return_value=resolved) as m_rcr, \
         patch("testmu_selenium._heal_cascade.resolve_coordinate") as m_rc, \
         patch("testmu_selenium._heal_cascade.time.sleep"):
        m_heal_cls.return_value.desktop_locate_full_page.return_value = (960, 4395)
        result = _heal_cascade(description="the warning box", current_selector=[],
                               current_frame_info=None, tiers=["DESKTOP_LOCATE_FULL_PAGE_READ"],
                               exception=NoSuchElementException("x"), driver=mock_driver)
    assert result.tier_used == "DESKTOP_LOCATE_FULL_PAGE_READ"
    assert result.selectors == [{"selector": "//div[3]", "isXPath": True, "score": 45}]
    assert result.coordinates is not None          # post-scroll viewport coords kept as fallback
    m_rcr.assert_called_once()                     # READ resolver, not the click resolver
    m_rc.assert_not_called()                       # shared click resolver untouched on this path


def test_full_page_read_tier_coordinates_only_when_resolver_returns_none(mock_driver):
    """resolver None → selectors == [], coordinates populated."""
    from selenium.common.exceptions import NoSuchElementException
    mock_driver.execute_script.side_effect = [
        [1920, 1080],
        None,
        [0, 4000],
    ]
    with patch("testmu_selenium._heal_cascade.Heal") as m_heal_cls, \
         patch("testmu_selenium._heal_cascade.resolve_coordinate_read", return_value=None), \
         patch("testmu_selenium._heal_cascade.time.sleep"):
        m_heal_cls.return_value.desktop_locate_full_page.return_value = (960, 4395)
        result = _heal_cascade(description="the warning box", current_selector=[],
                               current_frame_info=None, tiers=["DESKTOP_LOCATE_FULL_PAGE_READ"],
                               exception=NoSuchElementException("x"), driver=mock_driver)
    assert result.selectors == []
    assert result.coordinates is not None


def test_textual_query_no_longer_a_relocate_tier(mock_driver, selectors):
    """TEXTUAL_QUERY must not act as a relocate tier. Textual-query autoheal
    belongs only to the textual_query action's direct read; the relocate cascade
    must treat TEXTUAL_QUERY as an unknown tier (miss) even when the textual
    endpoint would return a value — so it never feeds a read value back into
    findElement as a bogus selector."""
    textual_success = _load_fixture("textual_query_success.json")
    with patch.object(Heal, "get_outer_html", return_value="<html/>"), \
         patch.object(Heal, "textual_query_v2",
                      return_value=httpx.Response(200, json=textual_success)):
        with pytest.raises(AutohealExhausted):
            _heal_cascade(
                description="x",
                current_selector=selectors,
                current_frame_info=None,
                tiers=["TEXTUAL_QUERY"],
                exception=StaleElementReferenceException(),
                driver=mock_driver,
            )
